'''
Clase que maneja la solicitud y emisión de recomendaciones
'''
from entities.recommendation import Recommendation
from entities.profile import Profile
from entities.automobile import Automobile
from clusteringModel.kmodesManager import KmodesManager
from recommenderCore.contentBased import ContentBased
from entities.opinionSheet import OpinionSheet
import numpy as np

class RecommendationManager:

    @staticmethod
    def getRecommendation(form,idReq,MyConnection):
        RecommendationManager.setResults(form, MyConnection,idReq)#1. Almaceno formulrio en base de datos.
        array=RecommendationManager.getNumpyForm(form)# Traslado formulario a un numerico numerico
        cluster=KmodesManager.getCluster(array,MyConnection)#2. Clasifico formulario para obtener perfil.
        idModel=MyConnection.getLastModel()[0]#obtengo el ultimo modelo definido (la posicion 0 indica el id)
        profile=MyConnection.getPerfil(cluster,idModel)# obtengo los datos de puntuaci'on de perfil
        idRecom=MyConnection.addRecom(idReq,profile[0]) #3. creo una recomendacion en base de datos y asigno el perfil(posicion 0 es el id del perfil)
        if(idRecom):#4.genero recomendacion %% requiere generate OVERVIEW
            print('::OK::Formulario recibido: ',array[0])
            
            '''
            autos1=ContentBased.getBestRatedAutos(False,cluster,idModel,MyConnection,40)# En caso de tener restricciones de autos, agregarlo como primer parametro, en caso contraario se introduce False
            print('Autos después del filtrado de perfil: ',autos1)
            autos1=ContentBased.getSimilarAutos(MyConnection,array[0],8,autos1) ## En caso de tener una resticccioon sobre ciertos automoviles, agregarlo como tercer parametro
            print('filtro basado en contenido ok: ',autos1)
            '''  
            autos1=ContentBased.getSimilarAutos(MyConnection,array[0],30) ## En caso de tener una resticccioon sobre ciertos automoviles, agregarlo como segundo parametro
            print('Autos después del filtrado de caracteristicas: ',autos1)
            autos1=ContentBased.getBestRatedAutos(autos1,cluster,idModel,MyConnection,8)# En caso de tener restricciones de autos, agregarlo como primer parametro, en caso contraario se introduce False
            print('Autos después del filtrado de perfil: ',autos1)
            #'''

            autos1=ContentBased.getRestrictedAutos(MyConnection,autos1,Nresults=5,MaxMarca=2,Maxmodel=1)# Restricciones de marca y modelo por recomendación
            print('Autos despues de las restricciones : ',autos1)
            j=1 # Se guardan los autos resultado de recomendación en base de datos
            for auto in autos1:
                if not MyConnection.addResultRecom(idRecom,j,auto+1):
                    print('error')
                    return False
                j+=1
            print('::OK:: Datos almacenados en BD')
            data_Autos=MyConnection.getAutosByIdRecom(idRecom[0])# 7. recupero autos para crear el objeto respuesta
            if(data_Autos):
                profileResponse=Profile(profile[0],profile[1],profile[2])
                arrAutosResponse=[]
                for data_Auto in data_Autos:
                    auxAuto=Automobile(data_Auto[1],data_Auto[2],data_Auto[3],data_Auto[4],data_Auto[5],)
                    arrAutosResponse.append(auxAuto)
                recomResponse=Recommendation(idRecom[0],arrAutosResponse,profileResponse)
                print(recomResponse.get_recommendation())
                return recomResponse.get_recommendation()
            else:
                return False
        else:
            print('Error al crear nueva recomendacion')
            return False



    # ----------------------- METODOS AUXILIARES ------------------
    @staticmethod
    def setResults(questions,MyConnection,idReq):
        for x in questions['questions']:
            idResp=x['answer']
            idQues=x['id']
            MyConnection.addResult(idReq,idQues,idResp)
        print('formulario guardado en DB')
        return True

    @staticmethod
    def getNumpyForm(questions):
        formList=[]
        for x in questions['questions']:
            formList.append(x['answer'])
        return np.asarray(formList).reshape(1, -1)#forma admitida