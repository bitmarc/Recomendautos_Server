from csv1.csvcleaner import Csvcleaner
import pandas as pd


df_opinautos=Csvcleaner.FilterDataOpinautos()
df_opinautos['Sentimiento']=''
df_opinautos['Entidades']=''
for index, row in df_opinautos.iterrows():
    df_opinautos.iloc[index,7]=
    df_opinautos.iloc[index,8]=
print(df_opinautos)