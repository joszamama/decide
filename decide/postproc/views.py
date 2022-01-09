from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
import math
#import numpy as np


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)
    

    def hamilton(self, options, numEscanyos):
        #Definimos votos totales y el numero de escanyos asignados
        votos = 0
        numEscanyosAsignados=0
        #Hacemos recuento de votos totales y le añadimos a cada opción otro valor llamado postproc en el que almacenaremos el numero de escanyos que le asignamos
        for option in options:
            option['postproc']=0
            votos += option['votes']
        #Creamos una lista vacia para introducir el resto de cada partido al anyadir los escanyos
        lista=[]
        if votos>0 and numEscanyos>0:
            participantes = len(options)
            #Recorremos las opciones y al atributo postproc que habiamos creado anteriormente le asignamos un numero de escanyos mediante 
            #el siguiente calculo: (NumVotosPartido*NumEscanyos)//VotosTotales. El resultado sera una division exacta
            #A su vez rellenamos la lista vacia con un diccionario en el que ponemos el nombre de la opcion y el resto de la division
            #Tambien vamos incrementando el numero de escanyos asignados
            for option in options:
                option['postproc']=(option['votes']*numEscanyos)//votos
                lista.append({'number':option['number'],'votes':(option['votes']*numEscanyos)%votos})
                numEscanyosAsignados+=(option['votes']*numEscanyos)//votos


            lista.sort(key=lambda o: o['votes'],reverse=True)
            for option in lista:
                i = option['number']-1
                if(numEscanyosAsignados<numEscanyos):
                    options[i].update({'postproc' : options[i]['postproc']+1})
                    numEscanyosAsignados+=1
        return Response(options)


    def HuntingtonHill(self,options,numEscanyos):
    
        votosTotales = 0
        for x in options:
            votosTotales += x['votes']
        
        if votosTotales > 0 and numEscanyos > 0:

            limit = votosTotales/numEscanyos

            #Vamos a aplicar la regla rounding
            rounding = limit*0.001
            lower = limit-rounding
            upper = limit+rounding

            numEscanyosAsig = 0

            while(numEscanyosAsig != numEscanyos):

                #si llegamos a aplicar rounding rule y no llegamos al numero igual de escanos, 
                #reseteamos de nuevo el numero de escanos asig y empezamos de nuevo
              ##si no se cumple la regla reseteamos  cero
                
                numEscanyosAsig = 0

                for x in options:

                    if(x['votes']<limit):
                        x['postproc']=0
                    else:
                        cuota = x['votes']/limit
                        
                        if(isinstance(cuota,int)):
                            x['postproc']=cuota
                        else:
                            #Calculamos las cotas superior e inferior de la cuota y despues la media geometrica
                            lQ = int(cuota)
                            mediaG = math.sqrt(lQ*(lQ+1))

                            if(cuota > mediaG):
                                x['postproc']=(lQ+1)
                            else:
                                x['postproc']=lQ
                
                    numEscanyosAsig += x['postproc']

                #Rounding Rule:
                
                
                #For a quota q, let L denote it's lower quota, U its upper quota, and G the
                #geometric mean of L and U. If then round q down to L, otherwise
                #round q up to U.

                if(numEscanyosAsig < numEscanyos):

                    limit = lower
                    lower = limit-rounding
                    upper = limit+rounding

                else:
                    limit = upper
                    lower = limit-rounding
                    upper = limit+rounding
        else:
            for x in options:
                x.update({'postproc' : 0})
            return Response(options)
        
        return Response(options)


    def imperiali(self, options,numEscanyos):
        votosTotales = 0
        
        for i in options:
            votosTotales= votosTotales+ i['votes']
        
        if votosTotales>0 and numEscanyos>0:
            if votosTotales>(numEscanyos+2):
                q=round(votosTotales/(numEscanyos+2),0)

                escanyosAsigandos=0
                for i in options:
                    votos= i['votes']
                    escanyos=math.trunc(votos/q)
                    i.update({'postproc': escanyos})
                    escanyosAsigandos=escanyosAsigandos+i['postproc']
            
            #Mientras queden escaños libre

                while(escanyosAsigandos<numEscanyos):
                #Se almacenan los votos residuo
                    for i in options:
                        i.update({'votosResiduos': i['votes']- (q*i['postproc'])})
                
                
                #se ordena según los votos residuos
                    options.sort(key = lambda i :-i['votosResiduos'])


                #se añade un escaño más al que tenga mayor residuo
                    votoMayorResiduo= options[0]
                    votoMayorResiduo.update({'postproc': votoMayorResiduo['postproc']+1})
                    escanyosAsigandos=escanyosAsigandos+1

                #se elimina la nueva clave para que no afecte a futuras iteraciones
                    for i in options:
                        i.pop('votosResiduos')
                
                options.sort(key = lambda i :-i['postproc'])
            else:
                escanyosAsigandos=0
                for i in options:
                    votos= i['votes']
                    numOpciones=len(options)
                    escanyos=math.trunc(votos/numOpciones)
                    i.update({'postproc': escanyos})
                    escanyosAsigandos=escanyosAsigandos+i['postproc']

                if  escanyosAsigandos<numEscanyos:
                    for i in options:
                        options.sort(key = lambda i :-i['votes'])
                    votoMayorResiduo= options[0]
                    votoMayorResiduo.update({'postproc': votoMayorResiduo['postproc']+1})
                    escanyosAsigandos=escanyosAsigandos+1

            return Response(options)
            
        else:
            for i in options:
                i.update({'postproc': 0})
            return Response(options)

    def dHont(self, options, numEscanyos):

        #Añadimos un campo para el contador de escaños asignados a cada opción
        for op in options:
            op['postproc'] = 0
        
        #Para cada escaño recorremos todas las opciones usando la fórmula de d'Hont: número de votos de esa opción/(número de escaños asignados a esa opción + 1)
        for escano in range(0, numEscanyos):
             #Lista de tamaño igual al número de opciones. Recuento al aplicar la fórmula a cada opción (ordenados en la misma forma)
            recuento = []
            for op in options:
                r = op['votes'] / (op['postproc']+1)
                recuento.append(r)
            
            #Obtenemos el índice del máximo valor en la lista de recuento de votos (del ganador del escaño)
            ganador = recuento.index(max(recuento))
            #En la posicion del ganador le sumamos 1 escaño
            options[ganador]['postproc'] += 1

        return Response(options)



    def bipartitanship(self, options, numEscanyos):
        # función de ordenación
        def sortByVotes(e):
            return e['votes']
        # copiamos las opciones, ordenamos y obtenemos las dos con mayor número de votos        
        opts = options
        opts.sort(reverse=True,key=sortByVotes)
        option1=opts[0]
        option2=opts[1]
        #calculamos la proporción de peso por cada voto   
        votosTotales = option1['votes'] + option2['votes']
        proporcion = numEscanyos/votosTotales
        escanyos1 = round(option1['votes']*proporcion)
        escanyos2 = round(option2['votes']*proporcion)
        sumaEscanyos = escanyos1 + escanyos2
        #si queda algún escaño sin asignar se lo damos al primero
        if sumaEscanyos != numEscanyos:
            sobrante = numEscanyos-sumaEscanyos
            escanyos1 +=sobrante
        #inicializamos y asignamos los escaños a los dos primeros
        for op in opts:
            op['postproc'] = 0
        opts[0]['postproc'] = escanyos1
        opts[1]['postproc'] = escanyos2
        #reemplazamos las opciones y devolvemos el resultado
        options = opts
        return Response(options)


    def saintelague(self,options,numEscanyos):
        #tomamos los datos
        for op in options:
        #ardará el registro de los escaños de cada opción, añadimos a cada opción otro valor llamado postproc en el que almacenaremos el numero de escanyos que le asignamos

            op['postproc'] = 0
        #Para cada escaño recorremos todas las opciones usando la fórmula de SL : Nº de votos/(2 Nº de  escaños + 1)

        for i in range(0, numEscanyos):
            #Lista de tamaño igual al número de opciones. Recuento al aplicar la fórmula a cada opción (ordenados en la misma forma):
            options_copy = []

            for op in options:

                o = op['votes'] / (2*op['postproc']+1)

                options_copy.append(o)
            #procesamos los votos de las opciones para hacer el reparto de escaños. descartamos realizar el procedimiento para las opciones sin votos ya que no se llevarán ningún escaño.

            if op['votes'] != 0:
                #Buscamos de la lista copiada el mayor atributo ordenado por número de votos, esa será la opción elegida que ganará un escaño.
                maximo = max(options_copy)
                #La acción de añadir un escaño a la opción si la realizamos en la lista original así que para ello necesitamos la posición que tiene dicha opción en la copia de la lista pues será la misma posición que ocupe en nuestra lista original.
                pos_maximo = options_copy.index(maximo)
                #En la posición del ganador le sumamos 1 escaño
                options[pos_maximo]['postproc'] += 1
                #Una vez repartidos todos los escaños disponibles, procedemos a ordenar la lista resultante de mayor a menor según el número de escaños y devolvemos el resultado.
        options.sort(key=lambda x: -x['postproc'])

        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | HUNTINGTONHILL | DHONT | HAMILTON | BIPARTITANSHIP| IMPERIALI| SAINTELAGUE
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanyos = request.data.get('numEscanyos', 0)


        if t == 'IDENTITY':
            return self.identity(opts)
        
        elif t=='HUNTINGTONHILL':
            return self.HuntingtonHill(options=opts, numEscanyos=numEscanyos)

        elif t == 'DHONT':
            return self.dHont(options=opts, numEscanyos=numEscanyos)
          
        elif t== 'HAMILTON':
            return self.hamilton(options=opts, numEscanyos=numEscanyos)
          
        elif t == 'BIPARTITANSHIP':
            return self.bipartitanship(options=opts, numEscanyos=numEscanyos)
        
        elif t=='IMPERIALI':
            return self.imperiali(options=opts, numEscanyos=numEscanyos)

        elif t == 'SAINTELAGUE':
            return self.saintelague(options=opts, numEscanyos=numEscanyos)
          
        return Response({})
