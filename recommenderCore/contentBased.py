from pathlib import Path
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# linear_kernel
from sklearn.metrics.pairwise import linear_kernel
# cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity


class ContentBased:

    @staticmethod #SE EJECUTA EN FASE 0 [**Metdodo principal**]
    def generateOverview():
        base_path = Path(__file__).parent
        file_path_autos = (base_path / "../data_csv/autos_data_mod_csv.csv").resolve()
        dfAutos = pd.read_csv(file_path_autos, encoding='utf-8')
        dfAutos = dfAutos.fillna(0)
        dfAutos["nombre"] = dfAutos["marca"] +' '+ dfAutos["modelo"] +' '+ dfAutos["versión"]
        words=[]
        for index, row in dfAutos.iterrows():
            words.append(ContentBased.getColumnNamesA(row,dfAutos))
        dfAutos['overview']=words
        dfAutos.to_csv(file_path_autos,index=False, encoding='utf-8')
        return 'ok'
    
    @staticmethod #SE EJECUTA POR CADA RECOMENDACION [**Metdodo principal**]
    def getSimilarAutos(MyConnection,numericForm, Nresults, idsAutos=False):# Requiere numpy array o lista simple
        params=MyConnection.getCursorParams()
        db_connection_str = 'mysql+pymysql://'+params[1]+':'+params[2]+'@'+params[0]+'/'+params[3]
        db_connection = create_engine(db_connection_str)
        dfAutos = pd.read_sql('SELECT marca, modelo, año, version as "versión", resumen as "overview" FROM automoviles', con=db_connection)
        dfAutos["nombre"] = dfAutos["marca"] +' '+ dfAutos["modelo"] +' '+ dfAutos["versión"]
        labels=ContentBased.getAttribArray(MyConnection,numericForm)# Transformo las respuestas de formulario a un string de atributos 
        palabras = labels.split(" ")#   paso string a un diccionario para contabilizar las palabras
        diccionario = dict()
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
        dfaux = pd.DataFrame(diccionario.items(), columns=['IdAtrib', 'Count'])# Lo paso a un dataframe y reescribo el rated count con un numero decimal entro que reprecenta la cantidad de veces que una palabra debera ser repetida
        ratedCount=[]
        for index, row in dfaux.iterrows():
            ratedCount.append(ContentBased.getFactor(int(dfaux.iloc[index,0]),MyConnection))
        dfaux['ratedCount']=ratedCount
        dfaux['ratedCount']=round((dfaux['Count']/dfaux['ratedCount'])*20)# factor 20
        text1=''# Defino la nueva variable "resumen de atributos" (tomando en cuenta la popularidad del atributo)
        for index, row in dfaux.iterrows():
            idA=row['IdAtrib']
            for k in range(int(row['ratedCount'])):
                text1+=idA
                text1+=' '
        text1=text1[:-1]
        dfAutos=dfAutos.append({'nombre' : 'modelo' , 'overview' : text1} , ignore_index=True)# Agrego el nuevo "auto modelo" al dataframe de autos para procesarlo junto a los demas
        if idsAutos:#restriccion solo listado de autos
            autos=idsAutos
            autos.append(dfAutos.index[-1])
            dfAutos=dfAutos.loc[autos]

        dfAutos=ContentBased.setRestrictions(numericForm,dfAutos,MyConnection,True,True) #PRECIO, TRANSMISION #aplico restricciones de precio y transmision?
        # Obtengo la matriz de similitud
        #tfidf_cosine_sim=ContentBased.tfidfVectorizer(dfAutos)
        cv_cosine_sim=ContentBased.countVectorizer(dfAutos)
        recomendationsF1=ContentBased.get_recommendations('modelo',dfAutos,cv_cosine_sim)
        list=(dfAutos.loc[recomendationsF1])['index'].to_list()
        return list[:Nresults]

    @staticmethod
    def getBestRatedAutos(idsAutos,cluster,idModel,MyConnection,Nresults):
        params=MyConnection.getCursorParams()
        db_connection_str = 'mysql+pymysql://'+params[1]+':'+params[2]+'@'+params[0]+'/'+params[3]
        db_connection = create_engine(db_connection_str)
        dfScores = pd.read_sql('call sp_obtenerPuntuaciones()', con=db_connection)
        dfScores["nombre"] = dfScores["marca"] +' '+ dfScores["modelo"] +' '+ dfScores["versión"]
        dfScores.replace({'0':np.nan, 0:np.nan}, inplace=True)

        # Verifico si idsAutos tiene valores, si no se toman todos los autos como entrada
        if idsAutos:
            dfScores=dfScores.loc[idsAutos]
        tags=MyConnection.getTagsByCM(cluster,idModel)
        tagList=[]
        ratingList=[]
        for tag in tags:
            tagList.append(tag[0])
            ratingList.append(tag[1])
        
        print(tagList,ratingList)
        pg=ContentBased.getPgeneral(dfScores,tagList,ratingList)
        dfScores['Pgeneral']=pg
        dfScores=dfScores.nlargest(Nresults,['Pgeneral'])
        print(dfScores[['nombre','Pgeneral']])
        autos=dfScores.index.tolist()
        return autos

    @staticmethod
    def getRestrictedAutos(MyConnection,idsAutos,Nresults=False, MaxMarca=3,Maxmodel=1):
        params=MyConnection.getCursorParams()
        db_connection_str = 'mysql+pymysql://'+params[1]+':'+params[2]+'@'+params[0]+'/'+params[3]
        db_connection = create_engine(db_connection_str)
        dfScores = pd.read_sql('call sp_obtenerPuntuaciones()', con=db_connection)
        dfScores["nombre"] = dfScores["marca"] +' '+ dfScores["modelo"] +' '+ dfScores["versión"]
        dfScores.replace({'0':np.nan, 0:np.nan}, inplace=True)
        dfScores=dfScores.loc[idsAutos]
        dfScores[['cMar','cMod']] = pd.DataFrame([[0, 0]], index=dfScores.index)
        resultados=[]# metodo para obtener la lista final de autos
        for rec1 in idsAutos:
            if dfScores.loc[rec1]['cMar']<MaxMarca: # máximo 4 autos de la misma marca
                if dfScores.loc[rec1]['cMod']<Maxmodel:
                    resultados.append(rec1)
                    dfScores.loc[dfScores['marca']==dfScores.loc[rec1]['marca'], 'cMar']+=1
                    dfScores.loc[dfScores['modelo']==dfScores.loc[rec1]['modelo'], 'cMod']+=1
        if Nresults:
            autos=resultados[:Nresults]
        else:
            autos=resultados
        return autos



    # --------------------------------- METODOS AUXILIARES ---------------------------------------------------------
    @staticmethod
    def getColumnNamesA(row,dfAutos):# Metodo para obtener el nombre de los atributos relacionados a una respuesta
        arrlist=''
        i=0
        for data in row:
            if data==1:
                arrlist+=dfAutos.columns[i]
                arrlist+=' '
            i+=1
        return arrlist #Me regresa un string de atribututos como palabras

    # Metodo para obtener el nombre de los atributos relacionados a una respuesta
    @staticmethod
    def getColumnNamesS(MyConnection,x):
        attribs=MyConnection.getAttributesByIdResp(x)
        arrlist=''
        for attrib in attribs:
            arrlist+=str(attrib[0])
            arrlist+=' '
        return arrlist #Me regresa un string de atribututos como palabras

    # Medoto para obtener un string con todos los atributos relacionados a un formulario
    @staticmethod
    def getAttribArray(MyConnection,responses):
        atributesArr=''
        for response in responses:
            atributesArr+=ContentBased.getColumnNamesS(MyConnection,response)
        return atributesArr[:-1]

    @staticmethod
    def getPgeneral(dfAutos,tags,rating):
        pgList=[]
        for index, row in dfAutos.iterrows():
            pg=0
            tg=0
            for tag in tags:
                if not (pd.isnull(dfAutos.loc[index][tag])):
                    pg=pg+(dfAutos.loc[index][tag])*(rating[tg])
                tg+=1
            pg=pg+((dfAutos.loc[index]['general'])+ContentBased.getComentsScore(dfAutos.loc[index]['cP'],dfAutos.loc[index]['cN']))
            pgList.append(pg)
        return pgList

    #En este caso se toma como metrica el numero maximo de posibles apariiones en un formulario
    @staticmethod
    def getFactor(idAttrib, MyConnection):
        val=0
        valMQ=MyConnection.getMaxValQuestByIdAttrib(idAttrib)
        if valMQ:
            val=valMQ[0]
        return val
    
    def getComentsScore(cp,cn):
        ct=cp+cn
        rcp=(cp*100)/ct
        if rcp>50:
            return rcp/10
        if rcp<50:
            rcn=(cn*100)/ct
            return rcn/-10
        return 0


    #Operacion de similitud utilizando el  termino de frecuencia inversa (le quita importancia a las palabras mas repetidas)
    @staticmethod
    def tfidfVectorizer(dfAutosMod):
        token_pattern_ = r'([a-zA-Z0-9-/]{1,})'
        tfidf = TfidfVectorizer(token_pattern = token_pattern_)
        tfidf_matrix = tfidf.fit_transform(dfAutosMod['overview'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        return cosine_sim
    
    #Operacion de similitud utilizando count vectorizer (importancia dada por la frecuencia de palabras)
    @staticmethod
    def countVectorizer(dfAutosMod):
        token_pattern_ = r'([a-zA-Z0-9-/]{1,})'
        count = CountVectorizer(token_pattern = token_pattern_)
        count_matrix = count.fit_transform(dfAutosMod['overview'])
        cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
        return cosine_sim2

    @staticmethod
    def get_recommendations(title, dfAutosMod, cosine_sim):
        indices = pd.Series(dfAutosMod.index, index=dfAutosMod['nombre']).drop_duplicates()
        # Obtengo el indice que corresponde al titulo del auto
        idx = indices[title]
        # Obtengo las puntuaciones de similitud por pares de todos los autos con el auto modelo
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Ordeno los autos con base a la puntuacion de similitud
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # obtengo las puntuaciones de los 30 autos mas parecidos
        sim_scores = sim_scores[1:30]
        # Obtengo los indices
        aouto_indices = [i[0] for i in sim_scores]
        # Regreso el top 30  de autos (indices respecto al df)
        #return dfAutosMod['nombre'].iloc[aouto_indices]
        return aouto_indices

    @staticmethod
    def lowCost(idsPrices):
        return idsPrices[2:4]
    @staticmethod
    def mediumCost(idsPrices):
        return idsPrices[3]
    @staticmethod
    def highCost(idsPrices):
        return idsPrices[0]
    @staticmethod
    def highestCost(idsPrices):
        return idsPrices[0:3]
    @staticmethod
    def none(idsTransmisions):
        return False
    @staticmethod
    def manual(idsTransmisions):
        return idsTransmisions[1:]
    @staticmethod
    def automatic(idsTransmisions):
        return idsTransmisions[0]
    @staticmethod
    def getPricesToExclude(idPriceR,idsAtrribsPrices):
        switcher = {
            45: ContentBased.lowCost,
            46: ContentBased.mediumCost,
            47: ContentBased.highCost,
            48: ContentBased.highestCost
        }
        func = switcher.get(idPriceR, lambda: "Invalid price")
        return func(idsAtrribsPrices)
    @staticmethod
    def getTransmisionsToExclude(idTransmisionR,idsTransmisions):
        switcher = {
            36: ContentBased.none,
            37: ContentBased.manual,
            38: ContentBased.automatic
        }
        func = switcher.get(idTransmisionR, lambda: "Invalid Transmision")
        return func(idsTransmisions)
    @staticmethod
    def setRestrictions(userForm, dfAutos,MyConnection, price, transmision):
        idsTRansmisions=[32,33,34,35]
        idsPrices=[113,114,115,116]
        dfAutosMod = dfAutos.copy()
        if price:
            k=ContentBased.getPricesToExclude(userForm[-1],idsPrices)# La posicion del precio es la ultima
            if isinstance(k, list):
                for jk in k:
                    ids=MyConnection.getIdAutoByAttrib(jk)
                    ids = [x[0] - 1 for x in ids] # resto 1 a todo y a la vez lo cambio a lista
                    dfAutosMod.drop(ids,errors='ignore', inplace=True)
            else:
                ids=MyConnection.getIdAutoByAttrib(k)
                ids = [x[0] - 1 for x in ids]
                dfAutosMod.drop(ids,errors='ignore', inplace=True)
                
        if transmision:
            k=ContentBased.getTransmisionsToExclude(userForm[13],idsTRansmisions)# El id de la pregunta de transmision es 13
            if k:
                if isinstance(k, list):
                    for jk in k:
                        ids=MyConnection.getIdAutoByAttrib(jk)
                        ids = [x[0] - 1 for x in ids] # resto 1 a todo y a la vez lo cambio a lista
                        dfAutosMod.drop(ids,errors='ignore', inplace=True)
                else:
                    print(k)
                    ids=MyConnection.getIdAutoByAttrib(k)
                    ids = [x[0] - 1 for x in ids]
                    dfAutosMod.drop(ids,errors='ignore', inplace=True)
        dfAutosMod.reset_index(inplace = True)
        
        return dfAutosMod