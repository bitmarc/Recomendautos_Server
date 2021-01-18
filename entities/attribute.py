class Attribute:

    def __init__(self, id, name, description):
        self.__id=id
        self.__name=name
        self.__description=description

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id=id

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name=name

    def getDescription(self):
        return self.__description

    def setDescription(self, description):
        self.__description=description

    def getAttribute(self):
        data={"id":self.__id, "name":self.__name, "description":self.__description}
        return data