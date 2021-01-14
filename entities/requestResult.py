
'''
Clase que maneja el resultado de una solicitud de recomendacion del usuario
'''
class RequestResult:

    def __init__(self, id, date, profile, nResults,arrAutos,form, arrOpinionSheet):
        self.__id=id
        self.__date=date
        self.__nResults=nResults
        self.__profile=profile
        self.__arrAutos=arrAutos
        self.__form=form
        self.__arrOpinionSheet=arrOpinionSheet
    
    def get_RequestResult(self):
        data=[]
        for auto in self.__arrAutos:
            data.append(auto.get_automobile())
        dataO=[]
        for opinionS in self.__arrOpinionSheet:
            dataO.append(opinionS.getOpinion())
        data={"id":self.__id, "date":self.__date, "results":self.__nResults, "profile":self.__profile, "autos":data, "form":self.__form.getForm(),"scores":dataO}
        return data

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id
    
    def getDate(self):
        return self.__date

    def setDate(self, date):
        self.__date=date

    def getResults(self):
        return self.__nResults

    def setResults(self, nResults):
        self.__nResults=nResults
    
    def getProfile(self):
        return self.__profile

    def setProfile(self, profile):
        self.__profile=profile
    
    def getArrAutos(self):
        return self.__arrAutos

    def setArrAutos(self, arrAutos):
        self.__arrAutos=arrAutos
    
    def getForm(self):
        return self.__form

    def setForm(self, form):
        self.__form=form

    def getOpinionS(self):
        return self.__arrOpinionSheet

    def setOpinionS(self, arrOpinionSheet):
        self.__arrOpinionSheet=arrOpinionSheet