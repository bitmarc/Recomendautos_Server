#import numpy as np
import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
from pathlib import Path
import pickle
from datetime import datetime
from sqlalchemy import create_engine
import pymysql

class KmodesManager:
    #################################       METODOS PRINCIPALES      ################################
    @staticmethod
    def generateModel(k, MyConnection, method='Cao', includeDB=False):
        '''
        Los datos se obtienen directamente del CSV de formularios, en caso de especificar includeDB=True,
        se anexarán los datos de formularios almacenados en base de datos. Al finalizar genera un archivo
        con extención ".pkl"
        '''
        base_path = Path(__file__).parent
        file_path_numericForms = (base_path / "../data_csv/datosFormularioNumericCsv.csv").resolve()
        dfNumericForms = pd.read_csv(file_path_numericForms, encoding='utf-8')

        if includeDB:
            params=MyConnection.getCursorParams()
            db_connection_str = 'mysql+pymysql://'+params[1]+':'+params[2]+'@'+params[0]+'/'+params[3]
            db_connection = create_engine(db_connection_str)
            dfforms1 = pd.read_sql('call sp_obtenerTodosResultados()', con=db_connection)
            r=dfforms1['solicitud'].describe()['max']
            for i in range(int(r)):
                lista=[]
                for index, row in dfforms1.loc[dfforms1['solicitud']==i+1].iterrows():
                    lista.append(row['idRespuesta'])
                a_series = pd.Series(lista, index = dfNumericForms.columns)
                dfNumericForms = dfNumericForms.append(a_series, ignore_index=True)
                ##df_length = len(df)
                ##df.loc[df_length] = to_append

        npArrayForms = dfNumericForms.to_numpy()
        model = KModes(n_clusters=k, init=method, n_init=5, verbose=1)# defino los parametros de la instancia
        clusters = model.fit_predict(npArrayForms)#1.2 Ejecuto el algoritmo
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
        print('modelo ok')
        return 'modelo generado correctamente!'

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
        file_path_model = (base_path / route).resolve()
        dfNumericForms = pd.read_csv(file_path_numericForms, encoding='utf-8')
        model=pickle.load(open(file_path_model,"rb")) #load model
        print('leido ',route)
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
        ArrayClusterlabels=[]
        for cluster in mtx:
            labels=''
            for form in cluster:
                labels+=KmodesManager.getAttribArray(dfNumericForms.loc[form],MyConnection)
                labels+=' '
            labels=labels[:-1]
            ArrayClusterlabels.append(labels)
        # 2.3. Traslado los grupos de strings a diccionarios para contabilizar las palabras(atributos) y despues a daataframes(uno por cada cluster)
        dfArray=[]
        for cluster in ArrayClusterlabels:
            palabras = cluster.split(" ")
            diccionario = dict()
            for p in palabras:
                diccionario[p] = diccionario.get(p, 0) + 1
            dfArray.append(pd.DataFrame(diccionario.items(), columns=['IdAtrib', 'Count']))
        # 2.4. Analizo los datos de cada data frame considerando la puntuacion de popularidad de cada atributo
        for df in dfArray:
            ratedCount=[]
            for index, row in df.iterrows():
                ratedCount.append(KmodesManager.getFactor(int(df.iloc[index,0]),MyConnection))
            df['ratedCount']=ratedCount
            df['ratedCount']=df['Count']/df['ratedCount']
        # 2.5. tomo los atributos mas reprecentativos de cada perfil y los tradusco a tags
        LIST=[]## CRITERIOS PARA DETERMINAR LOS ATRIBUTOS MAS REPRECENTATIVOS
        valuePorcent=0.60
        for df in dfArray:
            LIST.append(KmodesManager.getTagsList(df.nlargest(15,'ratedCount')['IdAtrib'].tolist(),MyConnection))
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
            palabras = cluster.split(" ")
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
                idP=MyConnection.getPerfil(x,lastModel[0])#obterner id de perfil
                if(idP):
                    MyConnection.removeProfileTag(idP[0])
                    for tag in dictarrayTags[x]:
                        MyConnection.linkProfileTag(idP[0],tag,dictarrayTags[x].get(tag))
                    print('Exito al agregar perfil (sobre escribido)')
                else:
                    print('Error al agregar perfil (sobre escribido)')
            else:# for link tags
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


    #################################       METODOS AUXILIARES      ################################
    
    @staticmethod
    def getColumnNamesS(response,MyConnection):# Metodo para obtener el nombre de los atributos relacionados a una respuesta
        attribs=MyConnection.getAttributesByIdResp(response)
        arrlist=''
        for attrib in attribs:
            arrlist+=str(attrib[0])
            arrlist+=' '
        return arrlist #Me regresa un string de atribututos como palabras
    
    @staticmethod
    def getAttribArray(responses,MyConnection):# Medoto para obtener un string con todos los atributos relacionados a un formulario
        # ------------------------------- restriccion 23 - 28 -----------------------
        atributesArr=''
        for response in responses:
            atributesArr+=KmodesManager.getColumnNamesS(response,MyConnection)
        return atributesArr[:-1]
    
    @staticmethod
    def getFactor(idAttrib,MyConnection):
        val=0
        valMA=MyConnection.getMaxValAnswByIdAttrib(idAttrib)
        if valMA:
            val=valMA[0]
        return val
    
    @staticmethod
    def getMin(minVal, maxVal, porcent):
        return ((maxVal-minVal)*porcent)+minVal
    
    @staticmethod
    def getTagsList(arrAttribs,MyConnection): # recibe como parametro la lista de ids de atributos (tr)
        groupTags=''
        for attribute in arrAttribs:
            tags=MyConnection.getTagsByIdAttrib(attribute)
            for tag in tags:
                groupTags+=tag[0]+' '
        return groupTags[:-1]
    
    @staticmethod   # metodo que obtiene los tags mas relevantes
    def getRelevantTags(relevant):
        if(len(relevant)>1):
            return relevant[:2]
        else:
            return relevant[0]
    