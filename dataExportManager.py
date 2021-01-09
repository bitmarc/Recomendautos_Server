'''
Esta clase permite automatizar el proceso de exportacion de datos de un CSV a base de datos
'''
import pandas as pd
from pathlib import Path
import re

class DataExportManager:

    @staticmethod
    def exportAtributes(MyConnection):
        base_path = Path(__file__).parent
        file_path = (base_path / "data_csv/datosAtributosCsv1.csv").resolve()
        dfAttributes = pd.read_csv(file_path,encoding='utf-8')
        for index, row in dfAttributes.iterrows():
            if(not MyConnection.addAtribute(row[4],row[2])):
                print('Error')
                break
        return "ok"


    @staticmethod
    def exportAutos(MyConnection):
        base_path = Path(__file__).parent
        file_path = (base_path / "data_csv/autos_data_mod_csv.csv").resolve()
        dfAutos = pd.read_csv(file_path,encoding='utf-8')
        dfAutos.fillna(0)
        for index, row in dfAutos.iterrows():
            if(not MyConnection.addAuto(row[0],row[1],row[2],row[3])):
                print('Error')
                break
        return "ok"
    
    @staticmethod
    def exportAutosAttributes(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path = (base_path / "data_csv/autos_data_mod_csv.csv").resolve()
        dfAutos = pd.read_csv(file_path,encoding='utf-8')
        dfAutos.drop(['marca','modelo','año','versión'],axis='columns', inplace=True)
        for index, row in dfAutos.iterrows():
            i=0
            idAttrib=[]
            for data in row:
                if data==1:
                    if(not MyConnection.addDatasheet(index+1,i+1)):
                        print('Error')
                        sms='failed'
                        break
                i+=1
            print('auto: ',index+1)
        return sms

    @staticmethod
    def exportTags(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path = (base_path / "data_csv/datosEtiquetasCsv.csv").resolve()
        dfTags = pd.read_csv(file_path,encoding='utf-8')
        for index, row in dfTags.iterrows():
            if(not MyConnection.addTag(row[1],'descripcion')):
                print('Error')
                sms='failed'
                break
        return sms

    @staticmethod
    def exportTagsAttributes(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path1 = (base_path / "data_csv/datosAtributosCsv1.csv").resolve()
        file_path2 = (base_path / "data_csv/datosEtiquetasCsv.csv").resolve()
        dfAttribs = pd.read_csv(file_path1,encoding='utf-8')
        dfTags = pd.read_csv(file_path2,encoding='utf-8')
        for index, row in dfTags.iterrows():
            dfAux=dfAttribs.loc[dfAttribs['TAGS'].str.contains(row['TAG'], flags = re.IGNORECASE)]
            for index1, row1 in dfAux.iterrows():
                if(not MyConnection.addLinkAttributeTag(index+1,index1+1)):
                    print('Error')
                    sms='failed'
                    break
        return sms

    @staticmethod
    def exportResponsesAttributes(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path1 = (base_path / "data_csv/datosMtxCsv.csv").resolve()
        dfMtx = pd.read_csv(file_path1,encoding='utf-8')
        dfMtx.drop(['ID R'],axis='columns', inplace=True)
        for index, row in dfMtx.iterrows():
            i=0
            for data in row:
                if data==1:
                    if(not MyConnection.addLinkAttributeResponse(index+1,int(dfMtx.columns[i]))):
                        sms='failed'
                        break
                i+=1
            print('auto: ',index+1)
        return sms