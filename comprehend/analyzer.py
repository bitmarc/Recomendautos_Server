import json
import csv
import pandas
from comprehend import Comprehend

class Analyzer:

    @staticmethod
    def AnalizeOpinautos():
        df_opinautos=Csvcleaner.FilterDataOpinautos() # filtro y limpieza de de datos extraidos

        df_opinautos['Sentimiento']=''
        df_opinautos['P_positivo']=''
        df_opinautos['P_negativo']=''
        df_opinautos['P_neutral']=''
        df_opinautos['P_mixto']=''
        df_opinautos['keyPhrases']=''
        df_opinautos['Scores']=''

        comprehend=Comprehend(service='comprehend', region='us-east-2', language='es')

        for index, row in df_opinautos.iterrows():
            sentimentResult=comprehend.getSentiment(text=df_opinautos.iloc[index,4]) #sentiment
            keyPrasesResult=comprehend.getKeyPhrases(text=df_opinautos.iloc[index,4]) #keyphraes
            keyPhrases=''
            sccores=''
            for keyP in keyPrasesResult['KeyPhrases']:
                keyPhrases+=str(keyP['Text'])
                keyPhrases+=','
                sccores+=str(keyP['Score'])
                sccores+=','

            df_opinautos.iloc[index,7]=sentimentResult['Sentiment']
            df_opinautos.iloc[index,8]=sentimentResult['SentimentScore']['Positive']
            df_opinautos.iloc[index,9]=sentimentResult['SentimentScore']['Negative']
            df_opinautos.iloc[index,10]=sentimentResult['SentimentScore']['Neutral']
            df_opinautos.iloc[index,11]=sentimentResult['SentimentScore']['Mixed']
            df_opinautos.iloc[index,12]=keyPhrases
            df_opinautos.iloc[index,13]=sccores
        print(df_opinautos)
        df_opinautos.to_csv("quecoche_items_parsed.csv",index=False)
