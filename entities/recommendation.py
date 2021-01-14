'''
Clase que modela una entidad de recomendación, contiene la informacion de automoviles y perfil
'''
class Recommendation:
    def __init__(self, id, arrAutomobiles, profile, arrOpinionSheet):
        self.__id=id
        self.__arrAutomobiles=arrAutomobiles
        self.__profile=profile
        self.__arrOpinionSheet=arrOpinionSheet

    def get_recommendation(self):
        dataA=[]
        for automobile in self.__arrAutomobiles:
            dataA.append(automobile.get_automobile())
        dataO=[]
        for opinionS in self.__arrOpinionSheet:
            dataO.append(opinionS.getOpinion())
        data={"idRecommendation":self.__id, "results":dataA, "profile":self.__profile.get_profile(), "scores":dataO}
        return data

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id

    def getArrAutomobiles(self):
        return self.__arrAutomobiles

    def setResults(self, arrAutomobiles):
        self.__arrAutomobiles=arrAutomobiles
    
    def getProfile(self):
        return self.__profile

    def setProfile(self, profile):
        self.__profile=profile
    
    def getOpinionS(self):
        return self.__arrOpinionSheet

    def setOpinionS(self, arrOpinionSheet):
        self.__arrOpinionSheet=arrOpinionSheet

    