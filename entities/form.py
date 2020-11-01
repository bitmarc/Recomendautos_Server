from entities.question import Question

class Form:

    def __init__(self,id,arrQuestions):
        self.__id=0
        self.__qArr=arrQuestions
    
    def getId(self):
        return self.__id
    
    def setId(self,id):
        self.__id=id
    
    def addQuestioArray(self,qArr):
        self.__qArr=qArr
    

    def getForm(self):
        data=[]
        for question in self.__qArr:
            data.append(question.getQuestion())
        data={"id":self.__id, "questions":data}
        return data