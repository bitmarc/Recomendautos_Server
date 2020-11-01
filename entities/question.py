class Question:
    def __init__(self, id, title, hint, arrOptions):
        self.__id=id
        self.__title=title
        self.__hint=hint
        self.__arrOptions=arrOptions

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id

    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title=title

    def getHint(self):
        return self.__hint

    def setHint(self, hint):
        self.__hint=hint
    
    def getAnswer(self):
        return self.__answer

    def setAnswer(self, answer):
        self.__answer=answer

    def getArrOptions(self):
        return self.__arrOptions
    


    def getQuestion(self):
        data=[]
        for option in self.__arrOptions:
            data.append(option.getOption())
        data={"id":self.__id, "title":self.__title, "hint":self.__hint, "options":data}
        return data