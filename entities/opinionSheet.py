'''
Clase que modela una entidad "opinion" de una automovil
'''
class OpinionSheet:
    def __init__(self, idA, in_favor, against, seeMore):
        self.__idA=idA
        self.__in_favor=in_favor
        self.__against=against
        self.__seeMore=seeMore


    def getIdAuto(self):
        return self.__idA

    def setIdAuto(self, idA):
        self.__idA=idA

    def getInFavor(self):
        return self.in_favor

    def setInFavor(self, a_favor):
        self.in_favor=a_favor

    def getAgainst(self):
        return self.__against

    def setAgainst(self, against):
        self.__against=against

    def getOpinion(self):
        data={"idAuto":self.__idA, "positive":self.__in_favor, "negative":self.__against, "seeMore":self.__seeMore}
        return data