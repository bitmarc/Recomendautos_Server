#import numpy as np
import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
from pathlib import Path
import pickle
from datetime import datetime

class KmodesManager:
    #Metodo se ejecuta 1 vez
    @staticmethod
    def generateModel(k, MyConnection, method='Cao'):
        # Se utiliza para generar el modelo de entrenamiento y definir los perfiles tras su analisis
        # ------------------------- 1. Se genera el modelo -----------------------------------------------
        # 1.1 Cargo los datos
        base_path = Path(__file__).parent
        file_path_numericForms = (base_path / "../data_csv/datosFormularioNumericCsv.csv").resolve()
        dfNumericForms = pd.read_csv(file_path_numericForms, encoding='utf-8')
        npArrayForms = dfNumericForms.to_numpy()
        # 1.1 Ejecuto el algoritmo
        model = KModes(n_clusters=k, init=method, n_init=8, verbose=1) #inicializo
        clusters = model.fit_predict(npArrayForms)
        print('MODELO CREADO',model.labels_)
        #genero nombre y ruta de guardado
        fecha=datetime.now()
        filename=str(fecha)
        filename=filename[:-7].replace(':', '').replace(' ', '_')
        filename='model_'+filename
        route="../clusteringModel/"+filename+".pkl"
        file_out_path_model = (base_path / route).resolve()
        pickle.dump(model,open(file_out_path_model,"wb"))
        # 2. guardo modelo en base de datos
        MyConnection.addModel(filename,fecha)
        

    @staticmethod
    def defineProfiles(MyConnection,k, modelName=False):
        #1 cargo modelo
        base_path = Path(__file__).parent
        file_path_numericForms = (base_path / "../data_csv/datosFormularioNumericCsv.csv").resolve()
        if modelName:
            lastModel=MyConnection.getModelByName(modelName)
            if not lastModel:
                print('error al obtener nombre del modelo en DB, el modelo especificado debe haber sido generado y almacenado anterioremente')
            route="../clusteringModel/"+modelName+".pkl"#posicion 1 indica el nombre
        else:
            lastModel=MyConnection.getLastModel()
            if not lastModel:
                print('error al obtener nombre del modelo de la base de datos')
            route="../clusteringModel/"+lastModel[1]+".pkl"#posicion 1 indica el nombre
        print('leido ',route)
        file_path_model = (base_path / route).resolve()
        dfNumericForms = pd.read_csv(file_path_numericForms, encoding='utf-8')
        model=pickle.load(open(file_path_model,"rb")) #load model
        # ------------------------- 2. Se analizan los clusters y se definen los perfiles -------------------
        # 2.1. Agrupo formularios en una matriz (cada fila es un cluster y cada columna un formulario)
        mtx=[]
        for x in range(k):
            group=[]
            index=0
            for label in model.labels_: # LAS ETIQUETAS SON NUMEROS DEL 0 A K-1, DONDE K ES EL NUMERO DE CLUSTERS
                if(label==x):
                    group.append(index)
                index+=1
            mtx.append(group)

        # 2.2. Tradusco los grupos de formularios a grupos de atributos
        file_path_rules = (base_path / "../data_csv/datosMtxCsv.csv").resolve()
        dfRules = pd.read_csv(file_path_rules, encoding='utf-8')
        dfRules.drop(['20','24', '27'], axis=1, inplace=True) # ------------------------------- restriccion 23 - 28
        dfRules = dfRules.fillna(0)
        ArrayClusterlabels=[]
        for cluster in mtx:
            labels=''
            for form in cluster:
                labels+=KmodesManager.getAttribArray(dfNumericForms.loc[form],dfRules)
                labels+=', '
            labels=labels[:-2]
            ArrayClusterlabels.append(labels)
        # 2.3. Traslado los grupos de strings a diccionarios para contabilizar las palabras(atributos) y despues a daataframes(uno por cada cluster)
        dfArray=[]
        for cluster in ArrayClusterlabels:
            palabras = cluster.split(", ")
            diccionario = dict()
            for p in palabras:
                diccionario[p] = diccionario.get(p, 0) + 1
            dfArray.append(pd.DataFrame(diccionario.items(), columns=['IdAtrib', 'Count']))
        # 2.4. Analizo los datos de cada data frame considerando la puntuacion de popularidad de cada atributo
        file_path_attribtutes = (base_path / "../data_csv/datosAtributosCsv.csv").resolve()
        dfAttributes = pd.read_csv(file_path_attribtutes, encoding='utf-8')
        for df in dfArray:
            ratedCount=[]
            for index, row in df.iterrows():
                ratedCount.append(KmodesManager.getFactor(int(df.iloc[index,0]),dfAttributes))
            df['ratedCount']=ratedCount
            df['ratedCount']=df['Count']/df['ratedCount']
        # 2.5. tomo los atributos mas reprecentativos de cada perfil y los tradusco a tags
        LIST=[]
        valuePorcent=0.60
        for df in dfArray:
            ## CRITERIOS PARA DETERMINAR LOS ATRIBUTOS MAS REPRECENTATIVOS
            LIST.append(KmodesManager.getTagsList(df.nlargest(15,'ratedCount')['IdAtrib'].tolist(),dfAttributes))
            #LIST.append(KmodesManager.getTagsList(df.loc[df['ratedCount']>KmodesManager.getMin(df.nsmallest(1,'ratedCount').iloc[0,2],df.nlargest(1,'ratedCount').iloc[0,2],valuePorcent)]['IdAtrib'].tolist(),dfAttributes))
            #LIST.append(KmodesManager.getTagsList(df.loc[df['ratedCount']>(df.nlargest(1,'ratedCount').iloc[0,2]*valuePorcent)]['IdAtrib'].tolist(),dfAttributes))
        #NUEVO-----------------------------------------
        '''
        allTags=''
        for ind in dfAttributes.index:
            if(not pd.isnull(dfAttributes['TAGS'][ind])):
                allTags+=dfAttributes['TAGS'][ind]
                allTags+=', '
        allTags=allTags[:-2]
        palabras = allTags.split(", ")
        diccionarioG = dict()
        for p in palabras:
            diccionarioG[p] = diccionarioG.get(p, 0) + 1
        print(diccionarioG)
        #NUEVO-----------------------------------------
        '''
        # 2.6. Almaceno los clusters en diccionarios 
        dictarrayTags=[]
        #profilesTags=[]
        profiles=[] # TEMPORAL NOMBRE DEL PERFIL Y DESCRIPCION
        for cluster in LIST:
            palabras = cluster.split(", ")
            diccionario = dict()
            for p in palabras:
                diccionario[p] = diccionario.get(p, 0) + 1
            #NUEVO--------------------------------------------
            #for key in diccionario.keys():
            #    diccionario[key]=diccionario[key]/diccionarioG[key]
            #NUEVO--------------------------------------------
            dictarrayTags.append(diccionario)
            relevant=sorted(diccionario, key=diccionario.get, reverse=True)
            #print(relevant)
            #profilesTags.append(KmodesManager.getRelevantTags(relevant))
            prfileDescription='tus intereses ordenados son: '
            for tag in relevant:
                prfileDescription= prfileDescription+tag+': '+str(round(diccionario[tag],3))+', '
            prfileDescription=prfileDescription[:-2]
            profiles.append(prfileDescription)
        for x in range(k):
            nameP='Perfil '+str(x)
            print(nameP)

            if modelName: # si existe el modelo
                #obterner id de perfil
                idP=MyConnection.getPerfil(x,lastModel[0])
                if(idP):
                    MyConnection.removeProfileTag(idP[0])
                    for tag in dictarrayTags[x]:
                        MyConnection.linkProfileTag(idP[0],tag,dictarrayTags[x].get(tag))
                    print('Exito al agregar perfil (sobre escribido)')
                else:
                    print('Error al agregar perfil (sobre escribido)')
                
                # for link tags
            else:
                idP=MyConnection.addProfile(nameP,profiles[x],x,lastModel[0])#la posicion 0 de lastmodel indica el id
                if(idP):
                    for tag in dictarrayTags[x]:
                        MyConnection.linkProfileTag(idP[0],tag,dictarrayTags[x].get(tag))
                    print('Exito al agregar perfil')
                else:
                    print('Error al agregar perfil')
        return 'perfiles agregados correctamente!'


    @staticmethod
    def getCluster(form, MyConnection, modelName=False):
        if modelName:
            route="../clusteringModel/"+modelName+".pkl"#posicion 1 indica el nombre
        else:
            lastModel=MyConnection.getLastModel()
            if not lastModel:
                print('error al obtener nombre del ultimo modelo en DB')
            route="../clusteringModel/"+lastModel[1]+".pkl"#posicion 1 indica el nombre
        base_path = Path(__file__).parent
        file_path_model = (base_path / route).resolve()
        model=pickle.load(open(file_path_model,"rb")) #load model
        cluster=model.predict(form) # nsamples,nfeatures
        return cluster[0]


    # METODOS AUXILIARES
    @staticmethod
    def getColumnNamesS(response,dfRules):# Metodo para obtener el nombre de los atributos relacionados a una respuesta
        arrlist=''
        for index, row in dfRules.iterrows():
            if dfRules.iloc[index,0]==response:
                index=0
                for data in row[1:]:
                    index+=1
                    if data==1:
                        arrlist+=dfRules.columns[index]
                        arrlist+=', '
                break
        return arrlist #Me regresa un string de atribututos como palabras
    @staticmethod
    def getAttribArray(responses,dfRules):# Medoto para obtener un string con todos los atributos relacionados a un formulario
        atributesArr=''
        for response in responses:
            atributesArr+=KmodesManager.getColumnNamesS(response,dfRules)
        return atributesArr[:-2]
    
    @staticmethod
    def getFactor(idAttrib,dfAttributes):
        val=0
        for index, row in dfAttributes.iterrows():
            if dfAttributes.iloc[index,3]==idAttrib:
                val=dfAttributes.iloc[index,6]
                break
        return val
    @staticmethod
    def getMin(minVal, maxVal, porcent):
        return ((maxVal-minVal)*porcent)+minVal
    @staticmethod
    def getTagsList(arrAtribs,dfAttributes): # recibe como parametro la lista de ids de atributos (tr)
        groupTags=''
        for ind in dfAttributes.index:
            for item in arrAtribs:
                if int(item)==dfAttributes['IDAE'][ind]:
                    if(not pd.isnull(dfAttributes['TAGS'][ind])):
                        groupTags+=dfAttributes['TAGS'][ind]
                        groupTags+=', '
                    break
        return groupTags[:-2]
    
    @staticmethod   # metodo que obtiene los tags mas relevantes
    def getRelevantTags(relevant):
        if(len(relevant)>1):
            return relevant[:2]
        else:
            return relevant[0]
    