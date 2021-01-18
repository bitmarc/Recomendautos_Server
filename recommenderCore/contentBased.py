from pathlib import Path
import pandas as pd
#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# linear_kernel
from sklearn.metrics.pairwise import linear_kernel
# cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity


class ContentBased:

    #SE EJECUTA EN FASE 0 [**Metdodo principal**]
    @staticmethod
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
    
    #SE EJECUTA POR CADA RECOMENDACION [**Metdodo principal**]
    @staticmethod
    def getSimilarAutos(numericForm):# Requiere numpy array o lista simple
        # Dos fases:
        # 1. filtro basado en contenido(similitud de atributos)
        # 2. filtro basado en contenido(evaluacion de perfil)
        base_path = Path(__file__).parent
        file_path_autos = (base_path / "../data_csv/autos_data_mod_csv.csv").resolve()
        col_list = ["marca", "modelo", "año", "versión", "nombre", "overview"]
        dfAutos = pd.read_csv(file_path_autos, usecols=col_list, encoding='utf-8')
        #   Transformo las respuestas de formulario a un string de atributos 
        file_path_rules = (base_path / "../data_csv/datosMtxCsv.csv").resolve()
        dfRules = pd.read_csv(file_path_rules, encoding='utf-8')
        labels=ContentBased.getAttribArray(numericForm,dfRules)
        #   paso string a un diccionario para contabilizar las palabras
        palabras = labels.split(" ")
        diccionario = dict()
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
        #   Lo paso a un dataframe y reescribo el rated count con un numero decimal entro que reprecenta la cantidad de veces que una palabra debera ser repetida
        dfaux = pd.DataFrame(diccionario.items(), columns=['IdAtrib', 'Count'])
        file_path_attribs = (base_path / "../data_csv/datosAtributosCsv.csv").resolve()
        dfAttributes = pd.read_csv(file_path_attribs, encoding='utf-8')
        ratedCount=[]
        for index, row in dfaux.iterrows():
            ratedCount.append(ContentBased.getFactor(int(dfaux.iloc[index,0]),dfAttributes))
        dfaux['ratedCount']=ratedCount
        dfaux['ratedCount']=round((dfaux['Count']/dfaux['ratedCount'])*20)# factor 20
        #   Defino la nueva variable "resumen de atributos" (tomando en cuenta la popularidad del atributo)
        text1=''
        for index, row in dfaux.iterrows():
            idA=row['IdAtrib']
            for k in range(int(row['ratedCount'])):
                text1+=idA
                text1+=' '
        text1=text1[:-1]
        #   Agrego el nuevo "auto modelo" al dataframe de autos para procesarlo junto a los demas
        dfAutos=dfAutos.append({'nombre' : 'modelo' , 'overview' : text1} , ignore_index=True)
        #   Obtengo la matriz de similitud
        #tfidf_cosine_sim=ContentBased.tfidfVectorizer(dfAutos)
        cv_cosine_sim=ContentBased.countVectorizer(dfAutos)
        #   genero las recomendaciones de fase 1
        recomendationsF1=ContentBased.get_recommendations('modelo',dfAutos,cv_cosine_sim)
        return recomendationsF1[:30]
        ## CONTINUA FASE 2. FILTRO BASADO EN CONTENIDO (EVALUACION DE PERFIL)

    @staticmethod
    def getBestRatedAutos(idsAutos,cluster,idModel,MyConnection):
        base_path = Path(__file__).parent
        file_path_scores = (base_path / "../data_csv/scoreSheet.csv").resolve()
        dfScores = pd.read_csv(file_path_scores, encoding='utf-8')
        dfScores=dfScores.loc[idsAutos]
        tags=MyConnection.getTagsByCM(cluster,idModel)
        tagList=[]
        for tag in tags:
            tagList.append(tag[0])
        print(tagList)
        dfAux=dfScores.dropna(subset = tagList)
        dfAux=dfAux.nlargest(10,tagList)
        autos=dfAux.index.tolist()

        dfAux[['cMar','cMod']] = pd.DataFrame([[0, 0]], index=dfAux.index)
        # metodo para obtener la lista final de autos
        #119,120
        resultados=[]
        for rec1 in autos:
            if dfAux.loc[rec1]['cMar']<4: # máximo 4 autos de la misma marca
                #procede esa marca aun es menor a 3
                if dfAux.loc[rec1]['cMod']<1:
                    #procede modelo nuevo
                    resultados.append(rec1)
                    dfAux.loc[dfAux['marca']==dfAux.loc[rec1]['marca'], 'cMar']+=1
                    dfAux.loc[dfAux['modelo']==dfAux.loc[rec1]['modelo'], 'cMod']+=1
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
    def getColumnNamesS(x,dfRules):
        arrlist=''
        for index, row in dfRules.iterrows():
            if dfRules.iloc[index,0]==x:
                index=0
                for data in row[1:]:
                    index+=1
                    if data==1:
                        arrlist+=dfRules.columns[index]
                        arrlist+=' '
                break
        return arrlist #Me regresa un string de atribututos como palabras

    # Medoto para obtener un string con todos los atributos relacionados a un formulario
    @staticmethod
    def getAttribArray(responses,dfRules):
        atributesArr=''
        for response in responses:
            atributesArr+=ContentBased.getColumnNamesS(response,dfRules)
        return atributesArr[:-1]


    #En este caso se toma como metrica el numero maximo de posibles apariiones en un formulario
    @staticmethod
    def getFactor(idAttrib, dfAttributes):
        val=0
        for index, row in dfAttributes.iterrows():
            if dfAttributes.iloc[index,3]==idAttrib:
                val=dfAttributes.iloc[index,5]
                break
        return val


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