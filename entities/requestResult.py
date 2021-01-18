
'''
Clase que maneja el resultado de una solicitud de recomendacion del usuario
'''
class RequestResult:

    def __init__(self, id, date, profile, nResults,arrAutos,form):
        self.__id=id
        self.__date=date
        self.__nResults=nResults
        self.__profile=profile
        self.__arrAutos=arrAutos
        self.__form=form
    
    def get_RequestResult(self):
        data=[]
        for auto in self.__arrAutos:
            data.append(auto.get_automobile())
        data={"id":self.__id, "date":self.__date, "results":self.__nResults, "profile":self.__profile.get_profile(), "autos":data, "form":self.__form.getForm()}
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