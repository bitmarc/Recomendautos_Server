from comprehend.comprehend import Comprehend
from csv1.csvcleaner import Csvcleaner
import json
import csv
import pandas

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
            print(index)
        df_opinautos.to_csv("quecoche_items_parsed.csv",index=False)
        print(df_opinautos)

    @staticmethod
    def AnalizeAutotest():
        df_autotest=Csvcleaner.FilterDataAutotest() # filtro y limpieza de de datos extraidos

        df_autotest['keyPhrasesFavor']=''
        df_autotest['ScoresFavor']=''
        df_autotest['keyPhrasesContra']=''
        df_autotest['ScoresContra']=''

        comprehend=Comprehend(service='comprehend', region='us-east-2', language='es')

        for index, row in df_autotest.iterrows():
            keyPrasesFavorResult=comprehend.getKeyPhrases(text=df_autotest.iloc[index,8]) #keyphraes
            keyPrasesContraResult=comprehend.getKeyPhrases(text=df_autotest.iloc[index,9]) #keyphraes
            keyPhrasesFavor=''
            ScoresFavor=''
            keyPhrasesContra=''
            ScoresContra=''

            for keyP in keyPrasesFavorResult['KeyPhrases']:
                keyPhrasesFavor+=str(keyP['Text'])
                keyPhrasesFavor+=','
                ScoresFavor+=str(keyP['Score'])
                ScoresFavor+=','

            for keyP in keyPrasesContraResult['KeyPhrases']:
                keyPhrasesContra+=str(keyP['Text'])
                keyPhrasesContra+=','
                ScoresContra+=str(keyP['Score'])
                ScoresContra+=','

            df_autotest.iloc[index,10]=keyPhrasesFavor
            df_autotest.iloc[index,11]=ScoresFavor
            df_autotest.iloc[index,12]=keyPhrasesContra
            df_autotest.iloc[index,13]=ScoresContra
            
        print(df_autotest)
        df_autotest.to_csv("autotest_items_parsed.csv",index=False)

