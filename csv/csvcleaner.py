import pandas as pd
import re

class Csvcleaner:

    @staticmethod
    def FilterData(MyConnection):
        df_opinautos = pandas.read_csv('..\\extractors\\webextractor\\opinautos_items.csv',encoding='utf-8',
        header=0,
        names=['Nombre', 'Marca','Modelo', 'Estrellas','Opinion','Votos','Fecha'])
        print(df_opinautos)