'''
Clase que maneja la solicitud y emisión de recomendaciones
'''
from entities.recommendation import Recommendation
from entities.profile import Profile
from entities.automobile import Automobile
from clusteringModel.kmodesManager import KmodesManager
import numpy as np

class RecommendationManager:

    @staticmethod
    def getRecommendation(form,idReq,MyConnection):
        # PROCEDIMIENTO:
        # 1. Almaceno formulario en base de datos
        # 2. Clasifico formulario para obtener perfil
        # 3. creo una recomendacion en base de datos y asigno el perfil
        # 4. Filtro basado en contenido
        # 5. Filtro basado en calificaciones
        # 6. Almaceno resultados en base de datos (genero resultados de recomendacion)
        # 7. Debuelvo resultados
        #
        #1. Almaceno formulrio en base de datos.
        RecommendationManager.setResults(form, MyConnection,idReq)
        #2. Clasifico formulario para obtener perfil.
        array=RecommendationManager.getNumpyForm(form)
        cluster=KmodesManager.getProfile(array)
        #3. creo una recomendacion en base de datos y asigno el perfil
        idRecom=MyConnection.addRecom(idReq,cluster+3) ## actualizar ej. 0+3=3 mis perfiles inician en 3
        if(idRecom):
            #4. filtro basado en contenido
            print('d')
        else:
            print('Error al crear nueva recomendacion')
            return False



        # generar recomendacion y asignar perfil y solicitud en recomendacion
        idRecom=MyConnection.addRecom(idReq,2) # id perfil
        if(idRecom):
            #agregar resultados(automoviles)a la recomendacion
            #for
            MyConnection.addResultRecom(idRecom,214,2) # id automovil
            MyConnection.addResultRecom(idRecom,215,3)
        # obtener datos nediante id de solisitud idReq
        # en estecaso solo usare las consultas de db sp para regresar resultados
        #la respuesta se devuelve en objetos recommendation
        data_recommendation=MyConnection.getRecomByIdReq(idReq)
        if(data_recommendation):
            data_Autos=MyConnection.getAutosByIdRecom(data_recommendation[0][0])
            if(data_Autos):
                profileResponse=Profile(data_recommendation[0][1],data_recommendation[0][2],data_recommendation[0][3])
                arrAutosResponse=[]
                for data_Auto in data_Autos:
                    auxAuto=Automobile(data_Auto[1],data_Auto[2],data_Auto[3],data_Auto[4],data_Auto[5])
                    arrAutosResponse.append(auxAuto)
                recomResponse=Recommendation(data_recommendation[0][0],arrAutosResponse,profileResponse)
                print(recomResponse.get_recommendation())
                return recomResponse.get_recommendation()
            else:
                return False
        else:
            return False
        #recom=Recommendation(1,)
        # iniciar recomendador
        #insertar resultados a tabla
        #devolver recomendacion


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