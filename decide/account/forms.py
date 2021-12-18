from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() 
        }