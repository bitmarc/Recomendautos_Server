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
        #insertar perfil a tabla
        # iniciar recomendador
        #insertar resultados a tabla
        #devolver recomendacion
        pass