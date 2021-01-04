'''
Clase que modela la entidad "Automovil"
'''
class Automobile:
    def __init__(self, id, marca, modelo, año, version):
        self.__id=id
        self.__marca=marca
        self.__modelo=modelo
        self.__año=año
        self.__version=version
    
    def get_automobile(self):
        data = {"id":self.__id, "brand":self.__marca, "model":self.__modelo, "year":self.__año, "version":self.__version}
        return data
        
    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id
    
    def getMarca(self):
        return self.__marca

    def setMarca(self, marca):
        self.__marca=marca
    
    def getModelo(self):
        return self.__modelo

    def setModelo(self, modelo):
        self.__modelo=modelo
    
    def getAño(self):
        return self.__año

    def setAño(self, año):
        self.__año=año

    def getVersion(self):
        return self.__version

    def setVersion(self, version):
        self.__version=version