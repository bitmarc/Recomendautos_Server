'''
Clase que modela la entidad de perfil de usuario
'''
class Profile:
    def __init__(self,id,name,parameter):
        self.__id=id
        self.__name=name
        self.__parameter=parameter

    def get_profile(self):
        data={"id":self.__id, "name":self.__name, "parameter":self.__parameter}
        return data

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name=name
    
    def getParameter(self):
        return self.__parameter

    def setParameter(self, parameter):
        self.__parameter=parameter
