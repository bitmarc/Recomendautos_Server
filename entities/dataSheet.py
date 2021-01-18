'''
Clase que modela una entidad "hoja de datos" que incluye atributos y calificaciones de un automovil
'''
class Datasheet:
    def __init__(self, idCar, arrAttributes, opinionSheet):
        self.__idCar=idCar
        self.__arrAttributes=arrAttributes
        self.__opinionSheet=opinionSheet


    def getIdAuto(self):
        return self.__idCar

    def setIdAuto(self, idCar):
        self.__idCar=idCar

    def getarrAtributes(self):
        return self.__arrAttributes

    def setarrAttributes(self, arrAttributes):
        self.__arrAttributes=arrAttributes

    def getOpinionSheet(self):
        return self.__opinionSheet

    def setOpinionSheet(self, opinionSheet):
        self.__opinionSheet=opinionSheet

    def getDataSheet(self):
        data=[]
        for attribute in self.__arrAttributes:
            data.append(attribute.getAttribute())
        data={"idCar":self.__idCar, "attributes":data, "scoreSheet":self.__opinionSheet.getOpinion()}
        return data
