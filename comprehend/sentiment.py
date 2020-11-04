import json
import csv
import pandas
from comprehend import Comprehend

df_opinautos = pandas.read_csv('C:\\Users\\Marco\\projects\\csv\\opinautos_items.csv',
encoding='utf-8',
header=0,
names=['Nombre', 'Marca','Modelo', 'Estrellas','Opinion','Votos','Fecha'])
#df_opinautos['Fecha']=pandas.to_datetime(df_opinautos['Fecha'])
#pandas.Timestamp.fromisoformat
print(df_opinautos)
df_opinautos['Sentiment'] = ''
k=0

analizador=Comprehend(service='comprehend',region='us-east-2', language='es')

for opinion in df_opinautos['Opinion']:
    if k > 10:
        break
    op=opinion.replace(u"\r",u" ").replace(u"\n",u" ").strip() #obtengo texto sin saltos de linea ni retorno de linea
    result=analizador.getSentiment(op)
    print(f'#{k}.- {op}')
    df_opinautos.loc[k,['Sentiment']]=result['Sentiment']
    k+=1


'''
# Ejemplo de prueba
personas = pandas.read_csv('C:\\Users\\Marco\\projects\\csv\\items.csv',
encoding='utf-8',
header=0,
names=['Nombre', 'Edad','Sexo'])
personas['Sex'] = ''
k=0
for persona in personas['Nombre']:
    if persona=='LUCERO':
        personas.loc[k,['Sex']]='encontrao'
    k+=1
print(personas)
personas.to_csv("items_edit.csv",index=False)
'''

'''
# Ejemplo de prueba
analizador=Analitics(service='comprehend',region='us-east-2', language='es')
text= "Al inicio me funciono muy bien pero después de unos meses el sistema de enfriamiento me empezó a dar problemas"
score=analizador.getSentiment(text)
print(json.dumps(score,sort_keys=True, indent=4))
'''