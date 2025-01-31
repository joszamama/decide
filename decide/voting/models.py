from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from base import mods
from base.models import Auth, Key

class Question(models.Model):
    desc = models.TextField()

    preferences = models.BooleanField(default=False,verbose_name="Preferences", help_text="Check for creating a preference question")
    sino = models.BooleanField(default=False, help_text="Marcala si quieres que las respuestas genericas sean Si/No. No añadir mas respuesta.")


    def clean(self):
        if self.sino and self.preferences:
            raise ValidationError('You can not make a question of the type yes/no and preferences at the same time')

    def __str__(self):
        return self.desc

    

@receiver(post_save, sender=Question)
def sino(sender, instance, **kwargs):
    options = instance.options.all() 
    if instance.sino==True and instance.options.all().count()==0: 
        op1 = QuestionOption(question=instance, number=1, option="Si")
        op1.save()
        op2 = QuestionOption(question=instance, number=2, option="No") 
        op2.save()

class QuestionOption(models.Model): 
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE) 
    number = models.PositiveIntegerField(blank=True, null=True) 
    option = models.TextField() 



    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

        return super().save() 
        
    def __str__(self): 
        return '{} ({})'.format(self.option, self.number) 
    
    def clean(self): 
        if self.question.sino and not self.question.options.all().count()==2: 
            raise ValidationError('This type of question must not have other options added by you.') 


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ManyToManyField(Question, related_name='votings')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    tipo_votacion = [("IDENTITY", "IDENTITY"),("HUNTINGTONHILL", "HUNTINGTONHILL"),("DHONT","DHONT"), ('HAMILTON', 'HAMILTON'),("BIPARTITANSHIP", "BIPARTITANSHIP"),("IMPERIALI", "IMPERIALI"),("SAINTELAGUE","SAINTELAGUE")]
    tipo = models.CharField(choices=tipo_votacion, max_length=20, default="IDENTITY", verbose_name='Count method')
    numEscanyos = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name='Seats')
    
    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally

        question = self.question.all()

        for q in question:
            options = q.options.all()
            opts = []
            for opt in options:
                if isinstance(tally, list):
                    votes = tally.count(opt.number)
                else:
                    votes = 0
                opts.append({
                    'option': opt.option,
                    'number': opt.number,
                    'votes': votes,
                    'tipo': self.tipo
                })


        data = { 'type': self.tipo, 'options': opts , 'numEscanyos': self.numEscanyos }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
