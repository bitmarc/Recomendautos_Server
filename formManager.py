from dbManager import Querys
from entities.form import Form
from entities.option import Option
from entities.question import Question

class FormManager:

    @staticmethod
    def buildForm(MyConnection):
        formQuestionsQuery=MyConnection.getFormQ()
        formOptionsQuery=MyConnection.getFormO()
        arrQ=[]
        for rowQ in formQuestionsQuery:
            arrOp=[]
            for rowO in formOptionsQuery:
                if rowO[3]== rowQ[0]: #si el idquestion de opcion es el mismo que el idquestion de question
                    arrOp.append(Option(rowO[0],rowO[1],rowO[2])) #falta agregar el valor de cada opcion
            arrQ.append(Question(rowQ[0],rowQ[1],rowQ[3],arrOp))
        formResult=Form(1,arrQ)
        return formResult