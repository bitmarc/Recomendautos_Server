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
        file_path = (base_path / "../extractors/motorpasion_items.csv").resolve()
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
        file_path = (base_path / "../extractors/quecochemecompro_items.csv").resolve()
        file_path_out = (base_path / "../extractors/quecochemecompro_items_filtered.csv").resolve()
        df_quecoche = pd.read_csv(file_path,encoding='utf-8',
        header=0,
        names=['Nombre', 'Marca', 'Puntuacion', 'Informativo', 'C_peque_manej', 'C_deportivo', 'C_bueno_barato',
       'C_practico', 'C_ecologico', 'C_atractivo', 'Lo_mejor', 'Lo_peor'])
        df_quecoche=Csvcleaner.FilterBrand(df_quecoche,'Marca')# Filtrado de marcas
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

        col_list = ["marca", "modelo", "año", "versión"]
        dfAutos = pd.read_csv(file_autos_path, encoding='utf-8', usecols=col_list)
        dfQuecoche = pd.read_csv(file_quecoche_path, encoding='utf-8')
        dfAutoTest = pd.read_csv(file_autotest_path, encoding='utf-8')
        dfMotorPasion = pd.read_csv(file_motorpasion_path, encoding='utf-8')

        columns=['general', 'confort', 'desempeño','tecnologia','ostentosidad','deportividad','economia','eficiencia','seguridad','a_favor','en_contra']
        dfAutos[columns] = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]], index=dfAutos.index)
        def remove_accents(a):
            return unidecode.unidecode(a)
        dfAutos['modelo'] = dfAutos['modelo'].apply(remove_accents)
        dfQuecoche['Nombre'] = dfQuecoche['Nombre'].apply(remove_accents)
        dfAutoTest['Nombre'] = dfAutoTest['Nombre'].apply(remove_accents)
        dfMotorPasion['Nombre'] = dfMotorPasion['Nombre'].apply(remove_accents)

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
            afavor=''
            encontra=''
            
            dfAux=dfQuecoche.loc[dfQuecoche['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfQuecoche['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            if not dfAux.empty:
                if not dfAux['Puntuacion'].isnull().values.any():
                    general.append(float(dfAux.iloc[0]['Puntuacion'].replace(",", ".")))
                if not dfAux['C_peque_manej'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_peque_manej'])
                if not dfAux['C_atractivo'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_atractivo'])
                if not dfAux['C_deportivo'].isnull().values.any():
                    deportividad.append(dfAux.iloc[0]['C_deportivo'])
                if not dfAux['C_bueno_barato'].isnull().values.any():
                    economia.append(dfAux.iloc[0]['C_bueno_barato'])
                if not dfAux['C_peque_manej'].isnull().values.any():
                    economia.append(dfAux.iloc[0]['C_peque_manej'])
                if not dfAux['C_peque_manej'].isnull().values.any():
                    eficiencia.append(dfAux.iloc[0]['C_peque_manej'])
                if not dfAux['C_ecologico'].isnull().values.any():
                    eficiencia.append(dfAux.iloc[0]['C_ecologico'])
                if not dfAux['Lo_mejor'].isnull().values.any():
                    afavor+dfAux.iloc[0]['Lo_mejor']
                if not dfAux['Lo_peor'].isnull().values.any():
                    encontra+dfAux.iloc[0]['Lo_peor']
                    
            dfAux=dfAutoTest.loc[dfAutoTest['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfAutoTest['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            if not dfAux.empty:
                if not dfAux['C_General'].isnull().values.any():
                    general.append(dfAux.iloc[0]['C_General'])
                if not dfAux['C_Vida'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Vida'])
                if not dfAux['C_Diseño'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Diseño'])
                if not dfAux['C_Manejo'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Manejo'])
                if not dfAux['C_Manejo'].isnull().values.any():
                    desempeño.append(dfAux.iloc[0]['C_Manejo'])
                if not dfAux['C_Performance'].isnull().values.any():
                    desempeño.append(dfAux.iloc[0]['C_Performance'])
                if not dfAux['C_Vida'].isnull().values.any():
                    tecnologia.append(dfAux.iloc[0]['C_Vida'])
                if not dfAux['C_Manejo'].isnull().values.any():
                    deportividad.append(dfAux.iloc[0]['C_Manejo'])
                if not dfAux['C_Performance'].isnull().values.any():
                    eficiencia.append(dfAux.iloc[0]['C_Performance'])
                if not dfAux['C_Diseño'].isnull().values.any():
                    seguridad.append(dfAux.iloc[0]['C_Diseño'])
                if not dfAux['A_favor'].isnull().values.any():
                    afavor+=', '+dfAux.iloc[0]['A_favor']
                if not dfAux['En_contra'].isnull().values.any():
                    encontra+=', '+dfAux.iloc[0]['En_contra']
            
            dfAux=dfMotorPasion.loc[dfMotorPasion['Nombre'].str.contains(row['marca']+' ', flags = re.IGNORECASE) &
                                dfMotorPasion['Nombre'].str.contains(' '+row['modelo'], flags = re.IGNORECASE)]
            if not dfAux.empty:
                if not dfAux['C_General'].isnull().values.any():
                    general.append(dfAux.iloc[0]['C_General'])
                if not dfAux['C_Equipamiento'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Equipamiento'])
                if not dfAux['C_Infotenimiento'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Infotenimiento'])
                if not dfAux['C_Espacio'].isnull().values.any():
                    confort.append(dfAux.iloc[0]['C_Espacio'])
                if not dfAux['C_Comportamiento'].isnull().values.any():
                    desempeño.append(dfAux.iloc[0]['C_Comportamiento'])
                if not dfAux['C_Transmision'].isnull().values.any():
                    desempeño.append(dfAux.iloc[0]['C_Transmision'])
                if not dfAux['C_Motor'].isnull().values.any():
                    desempeño.append(dfAux.iloc[0]['C_Motor'])
                if not dfAux['C_Infotenimiento'].isnull().values.any():
                    tecnologia.append(dfAux.iloc[0]['C_Infotenimiento'])
                if not dfAux['C_Acabados'].isnull().values.any():
                    ostentosidad.append(dfAux.iloc[0]['C_Acabados'])
                if not dfAux['C_Equipamiento'].isnull().values.any():
                    ostentosidad.append(dfAux.iloc[0]['C_Equipamiento'])
                if not dfAux['C_Comportamiento'].isnull().values.any():
                    deportividad.append(dfAux.iloc[0]['C_Comportamiento'])
                if not dfAux['C_Motor'].isnull().values.any():
                    deportividad.append(dfAux.iloc[0]['C_Motor'])
                if not dfAux['C_Precio'].isnull().values.any():
                    economia.append(dfAux.iloc[0]['C_Precio'])
                if not dfAux['C_Consumo'].isnull().values.any():
                    eficiencia.append(dfAux.iloc[0]['C_Consumo'])
                if not dfAux['C_Motor'].isnull().values.any():
                    eficiencia.append(dfAux.iloc[0]['C_Motor'])
                if not dfAux['C_Seguridad'].isnull().values.any():
                    seguridad.append(dfAux.iloc[0]['C_Seguridad'])
                if not dfAux['Lo_Bueno'].isnull().values.any():
                    afavor+=', '+dfAux.iloc[0]['Lo_Bueno']
                if not dfAux['Lo_Malo'].isnull().values.any():
                    encontra+=', '+dfAux.iloc[0]['Lo_Malo']
                    
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
            dfAutos.iloc[index,13]=afavor
            dfAutos.iloc[index,14]=encontra

        dfAutos['nombre']=dfAutos['marca']+' '+dfAutos['modelo']+' '+dfAutos['versión']
        dfAutos.to_csv(file_autos_path_out, encoding="utf-8", index=False) 