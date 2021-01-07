'''
Clase que maneja la solicitud y emisión de recomendaciones
'''
from entities.recommendation import Recommendation
from entities.profile import Profile
from entities.automobile import Automobile

class RecommendationManager:


    @staticmethod
    def setResults(questions,MyConnection,idReq):
        for x in questions['questions']:
            idResp=x['answer']
            idQues=x['id']
            MyConnection.addResult(idReq,idQues,idResp)
        print('ok')
        return True

    @staticmethod
    def getRecommendation(idReq,MyConnection):
        # obtener perfil
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