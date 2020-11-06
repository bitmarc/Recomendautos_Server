from csv1.csvcleaner import Csvcleaner
from comprehend.comprehend import Comprehend
import pandas as pd
import json

# solo puebas


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