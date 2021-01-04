'''
Clase que contiene los métodos que permiten "limpiar" la información extraida por el servicio de web scrapper
(Es implementada directamente por la calse analyzer)
'''
import pandas as pd
import re
from pathlib import Path

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
                 dataframe[brandField].str.contains('alfa', flags = re.IGNORECASE)].reset_index(drop=True)
        return dataframe

    @staticmethod
    def FilterModel(dataframe, ModelField):
        dataframe=dataframe.loc[~dataframe[ModelField].str.contains('np300', flags = re.IGNORECASE)& 
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
