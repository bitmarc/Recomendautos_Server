class Recommendation:
    def __init__(self, id, arrAutomobiles, profile):
        self.__id=id
        self.__arrAutomobiles=arrAutomobiles
        self.__profile=profile

    def get_recommendation(self):
        data=[]
        for automobile in self.__arrAutomobiles:
            data.append(automobile.get_automobile())
        data={"idRecommendation":self.__id, "results":data, "profile":self.__profile.get_profile()}
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

    