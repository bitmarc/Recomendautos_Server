'''
Clase que contiene los métodos que permiten "limpiar" la información extraida por el servicio de web scrapper
(Es implementada directamente por la calse analyzer)
'''
import pandas as pd
import re
from pathlib import Path
import numpy as np
import unidecode

class Csvcleaner:

    @staticmethod
    def FilterDataOpinautos():
        base_path = Path(__file__).parent
        file_path = (base_path / "../extractors/opinautos_items.csv").resolve()
        file_path_out = (base_path / "../extractors/opinautos_items_filtered.csv").resolve()
        df_opinautos = pd.read_csv(file_path,encoding='utf-8',
        header=0,
        names=['Nombre', 'Marca','Modelo', 'Estrellas','Opinion','Votos','Fecha'])
        df_opinautos=Csvcleaner.FilterBrand(df_opinautos,'Marca')# Filtrado de marcas
        df_opinautos=Csvcleaner.FilterModel(df_opinautos,'Modelo')# Filtrado de modelos
        df_opinautos=df_opinautos.loc[df_opinautos['Fecha'].str.contains('z', flags = re.IGNORECASE)].reset_index(drop=True)# Elimirar aquellos con fecha en otro formato
        for index, row in df_opinautos.iterrows():
            df_opinautos.iloc[index,4]=df_opinautos.iloc[index,4].replace(u"\r",u" ").replace(u"\n",u" ").strip()# Ajuste de texto en opiniones
        df_opinautos=df_opinautos.loc[df_opinautos['Opinion'].str.len()<3000].reset_index(drop=True) # limito numero de caracteres
        df_opinautos['Fecha'] = pd.to_datetime(df_opinautos['Fecha'])# Conversion de formato de fecha
        mask = (df_opinautos['Fecha'] > '2019-1-01') & (df_opinautos['Fecha'] <= '2021-1-1')
        df_opinautos=df_opinautos.loc[df_opinautos['Nombre'].str.contains('2019', flags = re.IGNORECASE) | df_opinautos['Nombre'].str.contains('2020', flags = re.IGNORECASE)]
        df_opinautos=df_opinautos.loc[mask]
        df_opinautos.to_csv(file_path_out,index=False)
        return df_opinautos

    @staticmethod
    def FilterDataAutotest():
        base_path = Path(__file__).parent
        file_path = (base_path / "../extractors/autotest_items.csv").resolve()
        file_path_out = (base_path / "../extractors/autotest_items_filtered.csv").resolve()
        df_autotest = pd.read_csv(file_path,encoding='utf-8',
        header=0,
        names=['Nombre', 'Marca','Modelo', 'C_General','C_Vida','C_Diseño','C_Manejo','C_Performance','A_favor','En_contra'])
        df_autotest=Csvcleaner.FilterBrand(df_autotest,'Marca')# Filtrado de marcas
        df_autotest=Csvcleaner.FilterModel(df_autotest,'Modelo')# Filtrado de modelos
        df_autotest.to_csv(file_path_out,index=False)
        return df_autotest

    @staticmethod
    def FilterDataMotorpasion():
        base_path = Path(__file__).parent
        file_path = (base_path / "../extractors/webextractor/motorpasion_items.csv").resolve()
        file_path_out = (base_path / "../extractors/motorpasion_items_filtered.csv").resolve()
        df_motor = pd.read_csv(file_path,encoding='utf-8',
        header=0,
        names=['Nombre', 'Version', 'C_General','C_Acabados','C_Seguridad','C_Equipamiento','C_Infotenimiento',
       'C_Comportamiento', 'C_Motor', 'C_Transmision', 'C_Consumo', 'C_Espacio', 'C_Precio', 'Lo_Bueno', 'Lo_Malo'])
        df_motor.dropna(subset=['Nombre'], inplace=True)
        df_motor=Csvcleaner.FilterBrand(df_motor,'Nombre')# Filtrado de marcas
        df_motor=Csvcleaner.FilterModel(df_motor,'Nombre')# Filtrado de modelos
        df_motor.to_csv(file_path_out,index=False)
        return df_motor

    @staticmethod
    def FilterDataQuecoche():
        base_path = Path(__file__).parent
        file_path = (base_path / "../extractors/webextractor/quecochemecompro_items.csv").resolve()
        file_path_out = (base_path / "../extractors/quecochemecompro_items_filtered.csv").resolve()
        df_quecoche = pd.read_csv(file_path,encoding='utf-8',
        header=0,
        names=['Nombre', 'Marca', 'Puntuacion', 'Informativo', 'C_peque_manej', 'C_deportivo', 'C_bueno_barato',
       'C_practico', 'C_ecologico', 'C_atractivo', 'Lo_mejor', 'Lo_peor'])
        df_quecoche=Csvcleaner.FilterBrand(df_quecoche,'Nombre')# Filtrado de marcas
        df_quecoche=Csvcleaner.FilterModel(df_quecoche,'Nombre')# Filtrado de modelos
        df_quecoche.to_csv(file_path_out,index=False)
        return df_quecoche


    @staticmethod
    def FilterBrand(dataframe, brandField):
        dataframe=dataframe.loc[dataframe[brandField].str.contains('nissan', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('chevrolet', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('buick', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('gmc', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('cadillac', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('audi', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('porsche', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('seat', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('volkswagen', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('toyota', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('ram', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('dodge', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('jeep', flags = re.IGNORECASE)| 
                 dataframe[brandField].str.contains('fiat', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('chrysler', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('alfa', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('kia', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('honda', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('mazda', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('hyundai', flags = re.IGNORECASE)|
                 dataframe[brandField].str.contains('renault', flags = re.IGNORECASE)].reset_index(drop=True)
        return dataframe

    @staticmethod
    def FilterModel(dataframe, ModelField):
        dataframe=dataframe.loc[~dataframe[ModelField].str.contains('malib', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('cabstar', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('urvan', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('express', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('silverado', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('caddy', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('crafter', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('transporter', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('hiace', flags = re.IGNORECASE)& 
                 ~dataframe[ModelField].str.contains('promaster', flags = re.IGNORECASE)&
                 ~dataframe[ModelField].str.contains('Ducato', flags = re.IGNORECASE)].reset_index(drop=True)
        return dataframe

# TODO: generar hoja de puntuaciones
    @staticmethod
    def generateScoreSheet():
        base_path = Path(__file__).parent
        file_autos_path = (base_path / "../data_csv/autos_data_mod_csv.csv").resolve()
        file_autos_path_out = (base_path / "../data_csv/scoreSheet.csv").resolve()
        file_quecoche_path = (base_path / "../extractors/quecochemecompro_items_filtered.csv").resolve()
        file_autotest_path = (base_path / "../extractors/autotest_items_filtered.csv").resolve()
        file_motorpasion_path = (base_path / "../extractors/motorpasion_items_filtered.csv").resolve()
        file_opinautos_path = (base_path / "../extractors/opinautos_items_Comprehend_parsed.csv").resolve()

        col_list = ["marca", "modelo", "año", "versión"]
        dfAutos = pd.read_csv(file_autos_path, encoding='utf-8', usecols=col_list)
        dfQuecoche = pd.read_csv(file_quecoche_path, encoding='utf-8')
        dfAutoTest = pd.read_csv(file_autotest_path, encoding='utf-8')
        dfMotorPasion = pd.read_csv(file_motorpasion_path, encoding='utf-8')
        dfOpinautos = pd.read_csv(file_opinautos_path, encoding='utf-8')

        columns=['general', 'confort', 'desempeño','tecnología','ostentosidad','deportividad','economía','eficiencia','seguridad','ecología','a_favor','en_contra','cP','cN']
        dfAutos[columns] = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]], index=dfAutos.index)
        dfAutos['modelo'] = dfAutos['modelo'].apply(Csvcleaner.remove_accents)
        dfQuecoche['Nombre'] = dfQuecoche['Nombre'].apply(Csvcleaner.remove_accents)
        dfAutoTest['Nombre'] = dfAutoTest['Nombre'].apply(Csvcleaner.remove_accents)
        dfMotorPasion['Nombre'] = dfMotorPasion['Nombre'].apply(Csvcleaner.remove_accents)
        dfOpinautos['Modelo'] = dfOpinautos['Modelo'].apply(Csvcleaner.remove_accents)

        for index, row in dfAutos.iterrows():
            general=[]
            confort=[]
            desempeño=[]
            tecnologia=[]
            ostentosidad=[]
            deportividad=[]
            economia=[]
            eficiencia=[]
            seguridad=[]
            ecologia=[]
            cp=[]
            cn=[]
            afavor=''
            encontra=''

            dfAux=dfQuecoche.loc[dfQuecoche['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfQuecoche['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            
            if not dfAux.empty:
                idxVersion=Csvcleaner.getVersionIndex(dfAux,' '+row['versión'],'Puntuacion')
                if not pd.isnull(dfAux.at[idxVersion, 'Puntuacion']):
                    general.append(float(dfAux.at[idxVersion, 'Puntuacion'].replace(",", ".")))
                if not pd.isnull(dfAux.at[idxVersion, 'C_peque_manej']):
                    confort.append(dfAux.at[idxVersion, 'C_peque_manej'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_atractivo']):
                    confort.append(dfAux.at[idxVersion, 'C_atractivo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_deportivo']):
                    deportividad.append(dfAux.at[idxVersion, 'C_deportivo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_bueno_barato']):
                    economia.append(dfAux.at[idxVersion, 'C_bueno_barato'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_peque_manej']):
                    economia.append(dfAux.at[idxVersion, 'C_peque_manej'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_peque_manej']):
                    eficiencia.append(dfAux.at[idxVersion, 'C_peque_manej'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_ecologico']):
                    eficiencia.append(dfAux.at[idxVersion, 'C_ecologico'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_ecologico']):
                    ecologia.append(dfAux.at[idxVersion, 'C_ecologico'])
                if not pd.isnull(dfAux.at[idxVersion, 'Lo_mejor']):
                    if len(afavor)<2:
                        afavor+=dfAux.at[idxVersion, 'Lo_mejor']
                    else:
                        afavor+=' '+dfAux.at[idxVersion, 'Lo_mejor']
                if not pd.isnull(dfAux.at[idxVersion, 'Lo_peor']):
                    if len(encontra)<2:
                        encontra+=dfAux.at[idxVersion, 'Lo_peor']
                    else:
                        encontra+=' '+dfAux.at[idxVersion, 'Lo_peor']

            dfAux=dfAutoTest.loc[dfAutoTest['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfAutoTest['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            if not dfAux.empty:
                idxVersion=Csvcleaner.getVersionIndex(dfAux,' '+row['versión'],'C_General')
                if not pd.isnull(dfAux.at[idxVersion, 'C_General']):
                    general.append(dfAux.at[idxVersion, 'C_General'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Vida']):
                    confort.append(dfAux.at[idxVersion, 'C_Vida'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Diseño']):
                    confort.append(dfAux.at[idxVersion, 'C_Diseño'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Manejo']):
                    confort.append(dfAux.at[idxVersion, 'C_Manejo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Manejo']):
                    desempeño.append(dfAux.at[idxVersion, 'C_Manejo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Performance']):
                    desempeño.append(dfAux.at[idxVersion, 'C_Performance'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Vida']):
                    tecnologia.append(dfAux.at[idxVersion, 'C_Vida'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Manejo']):
                    deportividad.append(dfAux.at[idxVersion, 'C_Manejo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Performance']):
                    eficiencia.append(dfAux.at[idxVersion, 'C_Performance'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Diseño']):
                    seguridad.append(dfAux.at[idxVersion, 'C_Diseño'])
                if not pd.isnull(dfAux.at[idxVersion, 'A_favor']):
                    if len(afavor)<2:
                        afavor+=dfAux.at[idxVersion, 'A_favor']
                    else:
                        afavor+=' '+dfAux.at[idxVersion, 'A_favor']
                if not pd.isnull(dfAux.at[idxVersion, 'En_contra']):
                    if len(encontra)<2:
                        encontra+=dfAux.at[idxVersion, 'En_contra']
                    else:
                        encontra+=' '+dfAux.at[idxVersion, 'En_contra']


            dfAux=dfMotorPasion.loc[dfMotorPasion['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfMotorPasion['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            if not dfAux.empty:
                idxVersion=Csvcleaner.getVersionIndex(dfAux,row['versión'],'C_General')
                if not pd.isnull(dfAux.at[idxVersion, 'C_General']):
                    general.append(dfAux.at[idxVersion, 'C_General'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Equipamiento']):
                    confort.append(dfAux.at[idxVersion, 'C_Equipamiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Infotenimiento']):
                    confort.append(dfAux.at[idxVersion, 'C_Infotenimiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Espacio']):
                    confort.append(dfAux.at[idxVersion, 'C_Espacio'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Comportamiento']):
                    desempeño.append(dfAux.at[idxVersion, 'C_Comportamiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Transmision']):
                    desempeño.append(dfAux.at[idxVersion, 'C_Transmision'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Motor']):
                    desempeño.append(dfAux.at[idxVersion, 'C_Motor'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Infotenimiento']):
                    tecnologia.append(dfAux.at[idxVersion, 'C_Infotenimiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Acabados']):
                    ostentosidad.append(dfAux.at[idxVersion, 'C_Acabados'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Equipamiento']):
                    ostentosidad.append(dfAux.at[idxVersion, 'C_Equipamiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Comportamiento']):
                    deportividad.append(dfAux.at[idxVersion, 'C_Comportamiento'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Motor']):
                    deportividad.append(dfAux.at[idxVersion, 'C_Motor'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Precio']):
                    economia.append(dfAux.at[idxVersion, 'C_Precio'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Consumo']):
                    eficiencia.append(dfAux.at[idxVersion, 'C_Consumo'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Motor']):
                    seguridad.append(dfAux.at[idxVersion, 'C_Motor'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Seguridad']):
                    seguridad.append(dfAux.at[idxVersion, 'C_Seguridad'])
                if not pd.isnull(dfAux.at[idxVersion, 'C_Consumo']):
                    ecologia.append(dfAux.at[idxVersion, 'C_Consumo'])
                    
                if not pd.isnull(dfAux.at[idxVersion, 'Lo_Bueno']):
                    if len(afavor)<2:
                        afavor+=dfAux.at[idxVersion, 'Lo_Bueno']
                    else:
                        afavor+=' '+dfAux.at[idxVersion, 'Lo_Bueno']
                if not pd.isnull(dfAux.at[idxVersion, 'Lo_Malo']):
                    if len(encontra)<2:
                        encontra+=dfAux.at[idxVersion, 'Lo_Malo']
                    else:
                        encontra+=' '+dfAux.at[idxVersion, 'Lo_Malo']
            dfAux=dfOpinautos.loc[dfOpinautos['Marca'].str.contains(row['marca'], flags = re.IGNORECASE) &
                    dfOpinautos['Modelo'].str.contains(row['modelo'], flags = re.IGNORECASE)]
            k=Csvcleaner.getCount(dfAux,'NEGATIVE')
            if k>0:
                cn.append(k)
            k=Csvcleaner.getCount(dfAux,'POSITIVE')
            if k>0:
                cp.append(k)

            if len(general)>0:
                dfAutos.iloc[index,4]=sum(general)/len(general)
            if len(confort)>0:
                dfAutos.iloc[index,5]=sum(confort)/len(confort)
            if len(desempeño)>0:
                dfAutos.iloc[index,6]=sum(desempeño)/len(desempeño)
            if len(tecnologia)>0:
                dfAutos.iloc[index,7]=sum(tecnologia)/len(tecnologia)
            if len(ostentosidad)>0:
                dfAutos.iloc[index,8]=sum(ostentosidad)/len(ostentosidad)
            if len(deportividad)>0:
                dfAutos.iloc[index,9]=sum(deportividad)/len(deportividad)
            if len(economia)>0:
                dfAutos.iloc[index,10]=sum(economia)/len(economia)
            if len(eficiencia)>0:
                dfAutos.iloc[index,11]=sum(eficiencia)/len(eficiencia)
            if len(seguridad)>0:
                dfAutos.iloc[index,12]=sum(seguridad)/len(seguridad)
            if len(ecologia)>0:
                dfAutos.iloc[index,13]=sum(ecologia)/len(ecologia)
            dfAutos.iloc[index,14]=afavor
            dfAutos.iloc[index,15]=encontra
            if len(cp)>0:
                dfAutos.iloc[index,16]=sum(cp)/len(cp)
            if len(cn)>0:
                dfAutos.iloc[index,17]=sum(cn)/len(cn)

        dfAutos['nombre']=dfAutos['marca']+' '+dfAutos['modelo']+' '+dfAutos['versión']
        dfAutos.to_csv(file_autos_path_out, encoding="utf-8", index=False)
        print('Hoja de puntuaciones generada correctamente')
        return 'ok'

    @staticmethod
    def getVersionIndex(dfScores,verson,puntGral):
        dfScores=dfScores.sort_values(by='Nombre', ascending=True)
        found=False
        for index, row in dfScores.iterrows():
            matchObj =  re.search(re.escape(verson), row['Nombre'], flags=re.IGNORECASE)
            if matchObj:
                found=index
                print(index)
                break
        if not found:
            for index, row in dfScores.iterrows():
                if not pd.isnull(row[puntGral]):
                    found=index
                    break
            if not found:
                found=dfScores.index[0]
        return found

    @staticmethod
    def getCount(df,sentiment):
        return len(df.loc[df['Sentimiento']==sentiment].index)

    @staticmethod
    def remove_accents(a):
        return unidecode.unidecode(a)