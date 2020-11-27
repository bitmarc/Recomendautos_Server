class History:

    def __init__(self,message,arrReqRes):
        self.__message=message # requests
        self.__arrReqRes=arrReqRes

    def getHistory(self):
        data=[]
        for reqRes in self.__arrReqRes:
            data.append(reqRes.get_RequestResult())
        data={"requests":self.__message, "arrRequest":data}
        return data

    def getMessage(self):
        return self.__message
    
    def setMessage(self,message):
        self.__message=message

    def getArrReqRes(self):
        return self.__arrReqRes
    
    def setArrReqRes(self,arrReqRes):
        self.__arrReqRes=arrReqRes