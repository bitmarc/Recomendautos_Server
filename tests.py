'''
script de Pruebas 
'''
#from dataExportManager import DataExportManager
#from clusteringModel.kmodesManager import KmodesManager\
from recommenderCore.contentBased import ContentBased
import numpy as np
#from csv1.csvcleaner import Csvcleaner
#from comprehend.comprehend import Comprehend
#from comprehend.analyzer import Analyzer
#import pandas as pd
#import json
#from datetime import datetime

# solo puebas
print('hola')
#DataExportManager.exportAtributes('mycon')
#KmodesManager.generateModel(6)
#KmodesManager.defineProfiles()

s=[3, 4, 8, 9, 14, 15, 19, 21, 23, 25, 29, 30, 33, 37, 40, 43, 46]
#perfil=KmodesManager.getProfile(s)
#print(perfil)

#Analyzer.AnalizeOpinautos()
#Analyzer.AnalizeAutotest()

#ContentBased.getSimilarAutos()
ContentBased.getSimilarAutos(s)
'''
# filtrar datos extraidos
Csvcleaner.FilterDataAutotest()
Csvcleaner.FilterDataMotorpasion()
Csvcleaner.FilterDataQuecoche()
Csvcleaner.FilterDataOpinautos()
print('ok')
'''
'''
myjson={
    "id": "0",
    "questions": [
        {
            "answer": 1,
            "hint": "",
            "id": "1",
            "options": [
                {
                    "id": "1",
                    "title": "No se debe escatimar en seguridad."
                },
                {
                    "id": "2",
                    "title": "No necesariamente tiene que ser el m\u00e1s seguro."
                },
                {
                    "id": "3",
                    "title": "me da igual"
                }
            ],
            "title": "\u00bfQue piensa usted sobre la seguridad?"
        },
        {
            "answer": 5,
            "hint": "",
            "id": "2",
            "options": [
                {
                    "id": "4",
                    "title": "Solo conduzo yo y a lo maximo voy acompa\u00f1ado de otra persona."
                },
                {
                    "id": "5",
                    "title": "Ademas de mi, es comun que viajen hasta cuatro personas m\u00e1s."
                },
                {
                    "id": "6",
                    "title": "Casi siempre somos m\u00e1s de 5 personas en el vehiculo."
                }
            ],
            "title": "\u00bfCu\u00e1ntas personas viajan en el vehiculo?"
        },
        {
            "answer": 8,
            "hint": "ayuda",
            "id": "3",
            "options": [
                {
                    "id": "7",
                    "title": "Si suele transportar a bebes o ni\u00f1os peque\u00f1os"
                },
                {
                    "id": "8",
                    "title": "No suele transportar a bebes o ni\u00f1os peque\u00f1os"
                }
            ],
            "title": "Suele transportar a bebes o ni\u00f1os peque\u00f1os, ya sea en silla de bebe o no."
        }
    ]
}

#print(json.dumps(myjson, sort_keys=True, indent=4))
#print(json.dumps(myjson['questions'][0]['answer'], sort_keys=True, indent=4))
for x in myjson['questions']:
            print(x['id'])

now = datetime.now()
print(now)
'''
'''
# se;alizacion
df_opinautos=Csvcleaner.FilterDataOpinautos() # filtro de datos
df_opinautos['Sentimiento']=''
df_opinautos['P_positivo']=''
df_opinautos['P_negativo']=''
df_opinautos['P_neutral']=''
df_opinautos['P_mixto']=''
df_opinautos['keyPhrases']=''
df_opinautos['Scores']=''
comprehend=Comprehend(service='comprehend', region='us-east-2', language='es')

sentimentResult=comprehend.getSentiment(text=df_opinautos.iloc[7448,4]) #sentiment
print(json.dumps(sentimentResult, sort_keys=True, indent=4))
keyPrasesResult=comprehend.getKeyPhrases(text=df_opinautos.iloc[7448,4]) #keyphraes
print(json.dumps(keyPrasesResult, sort_keys=True, indent=4))

keyPhrases=''
sccores=''
for keyP in keyPrasesResult['KeyPhrases']:
    keyPhrases+=str(keyP['Text'])
    keyPhrases+=','
    sccores+=str(keyP['Score'])
    sccores+=','
print(' kp: ',keyPhrases)
print(' s: ',sccores)

df_opinautos.iloc[7448,7]=sentimentResult['Sentiment']
df_opinautos.iloc[7448,8]=sentimentResult['SentimentScore']['Positive']
df_opinautos.iloc[7448,9]=sentimentResult['SentimentScore']['Negative']
df_opinautos.iloc[7448,10]=sentimentResult['SentimentScore']['Neutral']
df_opinautos.iloc[7448,11]=sentimentResult['SentimentScore']['Mixed']
df_opinautos.iloc[7448,12]=keyPhrases
df_opinautos.iloc[7448,13]=sccores
print(df_opinautos['Sentimiento'])
print(df_opinautos['keyPhrases'])
print(df_opinautos['Scores'])

print(df_opinautos)
df_opinautos.to_csv("quecoche_items_parsed1.csv",index=False)
'''