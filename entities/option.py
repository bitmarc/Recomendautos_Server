class Option:
    def __init__(self, id, title, value):
        self.__title=title
        self.__id=id
        self.__value=value


    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id

    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title=title

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value=value

    def getOption(self):
        data={"id":self.__id, "title":self.__title}
        return data