from pathlib import Path
from server import verify_password
import pandas as pd

class ContentBased:

    #METODO SE EJECUTA UNA VEZ
    @staticmethod
    def generateOverview():
        base_path = Path(__file__).parent
        file_path_autos = (base_path / "../data_csv/autos_data_mod_csv.csv").resolve()
        dfAutos = pd.read_csv(file_path_autos, encoding='utf-8')
        dfAutos = dfAutos.fillna(0)
        dfAutos["nombre"] = dfAutos["marca"] +' '+ dfAutos["modelo"] +' '+ dfAutos["versión"]
        words=[]
        for index, row in dfAutos.iterrows():
            words.append(ContentBased.getColumnNamesA(row,dfAutos))
        dfAutos['overview']=words
        dfAutos.to_csv(file_path_autos,index=False, encoding='utf-8')
        print("preprocesamiento terminado")
    
    @staticmethod
    def getSimilarAutos(numericForm):#numpy array o lista simple
        base_path = Path(__file__).parent
        file_path_autos = (base_path / "../data_csv/autos_data_mod_csv.csv").resolve()
        col_list = ["marca", "modelo", "año", "versión", "nombre", "overview"]
        dfAutos = pd.read_csv(file_path_autos, usecols=col_list, encoding='utf-8')
        # Transformo las respuestas de formulario a atributos 
        file_path_rules = (base_path / "../data_csv/datosMtxCsv.csv").resolve()
        dfRules = pd.read_csv(file_path_rules, encoding='utf-8')
        labels=ContentBased.getAttribArray(numericForm,dfRules)
        print(labels)


    

    # ------------ METODOS AUXILIARES ----------------
    @staticmethod
    def getColumnNamesA(row,dfAutos):# Metodo para obtener el nombre de los atributos relacionados a una respuesta
        arrlist=''
        i=0
        for data in row:
            if data==1:
                arrlist+=dfAutos.columns[i]
                arrlist+=' '
            i+=1
        return arrlist #Me regresa un string de atribututos como palabras
    
    # Metodo para obtener el nombre de los atributos relacionados a una respuesta
    def getColumnNamesS(x,dfRules):
        arrlist=''
        for index, row in dfRules.iterrows():
            if dfRules.iloc[index,0]==x:
                index=0
                for data in row[1:]:
                    index+=1
                    if data==1:
                        arrlist+=dfRules.columns[index]
                        arrlist+=' '
                break
        return arrlist #Me regresa un string de atribututos como palabras

    # Medoto para obtener un string con todos los atributos relacionados a un formulario
    def getAttribArray(responses,dfRules):
        atributesArr=''
        for response in responses:
            atributesArr+=ContentBased.getColumnNamesS(response,dfRules)
        return atributesArr[:-1]