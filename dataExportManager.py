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
                    if(not MyConnection.addLinkAttributeResponse(index+1,int(dfMtx.columns[i]))):# se trata a el nombre de la columna como id
                        sms='failed'
                        break
                i+=1
            print('auto: ',index+1)
        return sms

    @staticmethod
    def exportScoresheet(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path1 = (base_path / "data_csv/scoreSheet.csv").resolve()
        dfScoreS = pd.read_csv(file_path1,encoding='utf-8')
        dfScoreS.drop(['marca','modelo', 'año', 'versión','nombre'],axis='columns', inplace=True)#elimino columnas sobrantes
        dfScoreS=dfScoreS.dropna(subset=['general'])
        dfScoreS=dfScoreS.fillna(0)
        for index, row in dfScoreS.iterrows():
            if(not MyConnection.addScoresheet(row['general'],row['confort'],row['desempeño'],row['tecnologia'],
            row['ostentosidad'],row['deportividad'],row['economia'],row['eficiencia'],row['seguridad'],index+1)):
                sms='failed'
                break
            print('auto: ',index+1)
        return sms

    @staticmethod
    def exportForms(MyConnection):
        sms='ok'
        base_path = Path(__file__).parent
        file_path_forms = (base_path / "data_csv/results3_2021.csv").resolve()
        file_path_quest = (base_path / "data_csv/datosFormularioCsv.csv").resolve()
        file_path_out_numericForms = (base_path / "data_csv/datosFormularioNumericCsv.csv").resolve()
        header=['FECHA','EDAD','GENERO','OCUPACION','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
        dfForms = pd.read_csv(file_path_forms,encoding='utf-8', names=header, header=0)
        dfQuest=pd.read_csv(file_path_quest,encoding='utf-8')
        dfForms.drop(['FECHA','EDAD','GENERO','OCUPACION'],axis='columns', inplace=True)
        dfNumericForms=DataExportManager.translateResponses(dfForms,dfQuest)
        dfNumericForms.to_csv(file_path_out_numericForms,index=False)## ALMACENO EL FORMULARIO NUMERICO PARA SER UTILIZADO MAS ADELANTE
        print('Archivo "datosFormularioNumericCsv.csv" exportado con exito')
        for index, row in dfForms.iterrows():
            icol=1
            for data in row:
                if(not MyConnection.addResult(index+1000,icol,data)): #Se establece el id de solicitud al indice+1000 (no son solicitudes reales)
                        sms='failed'
                        break
                icol+=1
            if sms=='failed':
                break
            print('formulario',index+1,'ok')
        return sms


    # metodos de apoyo

    # METODO PARA TRADUCIR TITULO DE RESPUESTA POR ID REQUIERE ID DE PREGUNTA
    @staticmethod
    def getIdResp(resp,quest,dfQuest):
        for index, row in dfQuest.iterrows():
            if row['RESPUESTA']==resp and row['ID P']==quest:
                return row['ID R']
    
    # Metodo para leer todo el dataframe e intercambiar las respuetsas por el id numerico correspondiente
    @staticmethod
    def translateResponses(dfForms, dfQuest):
        dfResult=dfForms
        for index,row in dfResult.iterrows():
            pos=0
            for element in row:
                dfResult.iloc[index,pos]=DataExportManager.getIdResp(element,int(dfResult.columns[pos]),dfQuest)
                pos+=1
        return dfResult