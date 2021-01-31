'''
Clase principal, contiene la logica de ejecución del servidor y rutas para consumo de la API
'''
from entities.profile import Profile
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import pandas as pd

from sessionManager import SessionManager as sm
from dbManager import Querys
from formManager import FormManager
from entities.user import User
from csv1.csvcleaner import Csvcleaner
from entities.opinionSheet import OpinionSheet
from entities.dataSheet import Datasheet
from entities.attribute import Attribute
from recommendationManger import RecommendationManager
from recommenderCore.contentBased import ContentBased
from entities.requestResult import RequestResult
from entities.history import History
from entities.automobile import Automobile
from dataExportManager import DataExportManager
from clusteringModel.kmodesManager import KmodesManager

from sqlalchemy import create_engine
import pymysql


# VARIABLES
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
MyConnection = Querys(app)

# Metodo de verificacion de password para autenticación basica
@auth.verify_password
def verify_password(username, password):
    userQ=MyConnection.getUserByUsername(username)
    if(userQ):
        user = User("0",userQ[2],"0","0")
        user.setPasswordHash(userQ[4])
        if not user or not user.verify_password(password):
            print("usuario '{0}' no autorizado".format(username))
            return False
        print("usuario '{0}' autorizado".format(username))
        return userQ[1:3]
    print("usuario '{0}' no autorizado".format(username))
    return False

# Principal
class home(Resource):
    def get(self):
        lis=MyConnection.getCursorParams()
        db_connection_str = 'mysql+pymysql://'+lis[1]+':'+lis[2]+'@'+lis[0]+'/'+lis[3]
        db_connection = create_engine(db_connection_str)
        dfAutos = pd.read_sql('call sp_obtenerPuntuaciones()', con=db_connection)
        print(dfAutos)
        #return jsonify(dfAutos.to_dict())
        return jsonify({"message": "Bienvenido a recommendautos"})

# Bienvenida a usuario
class wellcome(Resource):
    @auth.login_required
    def get(self):
        return jsonify({"message":"{}".format(auth.current_user()[0])})

# Registro de nuevos usaurios
class addUser(Resource):
    def post(self):
        user1=User(request.json['personname'],request.json['username'],request.json['email'],request.json['password'])
        user1.hash_password()
        if(MyConnection.addNewUser(user1)):
            print("El usuario '{}' se agrego satisfactoriamente".format(user1.getUserName()))
            return jsonify({"message":"Usuario agregado satisfactoriamente", "user": user1.get_userBasic()})
        print("Error al agregar al usuario '{}'".format(user1.getUserName()))
        return jsonify({"message":"Error al agregar nuevo usuario", "user": user1.get_userBasic()})

# Consultar si un nombre de usuario esta regisytrado
class checkUser(Resource):
    def get(self,user_name):
        user=MyConnection.getUserByUsername(user_name)
        if(user):
            print("El nombre de usuario '{}' ya existe".format(user_name))
            return jsonify({"message":"El usuario ya existe"})
        print("El nombre de usuario '{}' no existe".format(user_name))
        return jsonify({"message":"El usuario no existe"})

# Consultar si un correo electronico ya esta registrado
class checkEmail(Resource):
    def get(self):
        pass

# Realizar el inicio de sesión
class verifyUser(Resource):
    def post(self):
        fakeUser=User("person",request.json['username'],"email",request.json['password'])
        GUID=request.json['id']
        user=MyConnection.getUserByUsername(fakeUser.getUserName())
        if(user):
            fakeUser.setPasswordHash(user[4])
            if(fakeUser.verify_password(request.json['password'])):
                sk=sm.generateSessionkey(user[0],GUID)
                if(MyConnection.addSk(user[0],sk,"ACTIVOS")):
                    fakeUser.setId(sk)
                    fakeUser.setPersonName(user[1])
                    fakeUser.setEmail(user[3])
                    print("El usuario {} accedio satisfactoriamente".format(fakeUser.getUserName()))
                    return jsonify({"message":"El usuario accedio satisfactoriamente", "user": fakeUser.get_user()})
                print("Error al agregar sk en db")
        print("el usuario no existe o contraseña icorecta")
        return jsonify({"message":"Error de autenticación", "user": fakeUser.get_user()})

# Obtener o actualizar la informacion de un usuario
class dataUser(Resource):
    @auth.login_required
    def post(self):
        fakeUser=User("0","0","0","0")
        fakeUser.setId(request.json['id'])
        user=MyConnection.getUserBySessionKey(fakeUser.getId()) # el id que maneja la app es el sessionkey (es cambiante)
        if(user):
            fakeUser.setPersonName(user[1])
            fakeUser.setUserName(user[2])
            fakeUser.setPassword("password")# El password nunca se envia como uan respuesta de servidor
            fakeUser.setEmail(user[4])
            print("Datos del usuario {} encontrados correctamente".format(fakeUser.getUserName()))
            return jsonify({"message":"Autenticacion correcta, usuario encontrado", "user": fakeUser.get_user()})
        print("Error al obtener los datos del usuario con sk: '{}'".format(fakeUser.getId()))
        return jsonify({"message":"Error: No se autentico correctamente o el usuario no existe", "user": fakeUser.get_user()})

    def patch(self):
        fakeUser=User(request.json['personname'],request.json['username'],request.json['email'],request.json['password'])
        fakeUser.hash_password()
        sk=request.json['id'] # id en la app es el session key
        fakeUser.setId(sk)
        id=MyConnection.getIdBySessionKey(sk)
        if(id):
            if(MyConnection.updateUser(fakeUser, id[0])):
                user=MyConnection.getUserById(id[0])
                if(user):
                    fakeUser.setPersonName(user[1])
                    fakeUser.setUserName(user[2])
                    fakeUser.setPassword("password") #el password nunca se envia como una respuesta
                    fakeUser.setEmail(user[3])
                    print("El usuario {},ha sido actualizado correctamente".format(fakeUser.getUserName()))
                    return jsonify({"message":"Usuario actualizado correctamente", "user": fakeUser.get_user()}) 
                print("El usuario {},ha sido actualizado correctamente, error al retornar nuevos datos".format(fakeUser.getUserName()))
                return jsonify({"message":"Usuario actualizado, error al retornar nuevo usuario", "user": fakeUser.get_user()})
        print("Error al actualizar datos del usuario{}, id no encontrado".format(fakeUser.getUserName()))
        return jsonify({"message":"Error al actualizar datos de usuario", "user": fakeUser.get_user()})

# Obtener formulario
class getForm(Resource):
    def get(self):
        formulario=FormManager.buildForm(MyConnection)
        return jsonify(formulario.getForm())

# Obtener recomendacion
class getRecom(Resource):
    def post(self):
        #myString = json.dumps(request.json, sort_keys=True, indent=4)
        #print(myString)
        now = datetime.now()
        id=MyConnection.getIdBySessionKey(request.json['user']['id']) #obtengo id mediante su sessionKey #sk=request.json['user']['id']
        if (id):
            idReq=MyConnection.addRequest("FormA",now,id[0])# genero una nueva solicitud
            if(idReq):
                result=RecommendationManager.getRecommendation(request.json['form'],idReq[0],MyConnection)
                if(result):
                    return jsonify(result)
                else:
                    return jsonify({"idRecommendation":"100"})
        else:
            return jsonify({"idRecommendation":"100"})

# Obtener historial
class getHistory(Resource):
    @auth.login_required
    def get(self):
        idUser=MyConnection.getIdByUsername(auth.current_user()[1])
        hRequests=MyConnection.getHistoryRequestByIdUser(idUser)
        print(hRequests)
        print(len(hRequests))
        if(hRequests):
            arrRequests=[]
            for hRequest in hRequests:
                data_Autos=MyConnection.getAutosByIdReq(hRequest[0])
                dataProfile=MyConnection.getProfileById(hRequest[2])
                userprofile=Profile(dataProfile[0],dataProfile[1],dataProfile[2])
                arrAutos=[]
                for data_Auto in data_Autos:
                    arrAutos.append(Automobile(data_Auto[1],data_Auto[2],data_Auto[3],data_Auto[4],data_Auto[5]))
                form=FormManager.buildFormResponse(MyConnection,hRequest[0])
                arrRequests.append(RequestResult(hRequest[0],hRequest[1],userprofile,hRequest[3],arrAutos,form))
            response=History(len(arrRequests),arrRequests)
            return jsonify(response.getHistory())
        else:
            #response=History(0,RequestResult(0,0,0,0,0,0))
            return jsonify({"requests":0})

# Obtener detalle de vehiculos
class getCarDetails(Resource):
    def post(self):
        print(request.json['id'])
        attribs=MyConnection.getAttributesByIdAuto(request.json['id'])
        if(attribs):
            print(attribs)
            arrAttribs=[]
            for attrib in attribs:
                arrAttribs.append(Attribute(attrib[0],attrib[1],attrib[2]))
            opinions=MyConnection.getOpinions(request.json['id'])
            if(opinions):
                opinionsheet=OpinionSheet(request.json['id'],opinions[0],opinions[1],opinions[2])
            else:
                urlA=MyConnection.getUrlAuto(request.json['id'])
                opinionsheet=OpinionSheet(request.json['id'],'','',urlA[0])
            datasheet=Datasheet(request.json['id'],arrAttribs,opinionsheet)
            print(datasheet.getDataSheet())
            return jsonify(datasheet.getDataSheet())
        return jsonify({'message':'error'})

# exportarAtributos
class exportData(Resource):
    def get(self):
        msg='failed'
        msg=DataExportManager.exportAttributes(MyConnection)
        print('exportAttributes ok')
        msg=ContentBased.generateOverview() #genera overview
        print('generateOverview ok')
        msg=DataExportManager.exportAutos(MyConnection)
        print('exportAutos ok')
        msg=DataExportManager.exportAutosAttributes(MyConnection)
        print('exportAutosAttributes ok')
        msg=DataExportManager.exportTags(MyConnection)
        print('exportTags ok')
        msg=DataExportManager.exportTagsAttributes(MyConnection)
        print('exportTagsAttributes ok')
        msg=DataExportManager.exportResponsesAttributes(MyConnection)
        print('exportResponsesAttributes ok')
        Csvcleaner.generateScoreSheet()
        print('generateScoreSheet ok')
        msg=DataExportManager.exportScoresheet(MyConnection)
        print('exportScoresheet ok')
        msg=DataExportManager.parseAttribs(MyConnection)
        print('parseAttribs ok')
        msg=DataExportManager.exportForms(MyConnection)#solo pasa a numeric, no a bd--
        print('exportForms ok')
        return jsonify('status: '+msg)

# Entrenar modelo
class trainModel(Resource):
    def get(self):
        msg='ok'
        k=6
        KmodesManager.generateModel(k,MyConnection,'Cao')
        msg=KmodesManager.defineProfiles(MyConnection,k)##===aun no se ejecuta
        #ContentBased.generateOverview() #solo cuando hay cambios en los datos de coches
        return msg


# Entrenar modelo
class updateProfiles(Resource):
    def post(self):
        msg='Error'
        if(MyConnection.updateProfileByNcluster(request.json['nombrePerfil'],request.json['descripcionPerfil'],request.json['cluster'])):
            msg='perfiles actualizados!'
        return msg



# ASOCIACION DE RECURSOS Y RUTAS
api.add_resource(home,"/")
api.add_resource(wellcome,"/wellcome")
api.add_resource(addUser,"/signUp")
api.add_resource(checkUser,"/signUp/user/<string:user_name>")
api.add_resource(checkEmail,"/signUp/email/<string:user_email>")
api.add_resource(verifyUser,"/logIn")
api.add_resource(dataUser,"/user")
api.add_resource(getForm,"/form")
api.add_resource(getRecom,"/recom")
api.add_resource(getHistory,"/history")
api.add_resource(getCarDetails,"/details")
api.add_resource(exportData,"/exportData")
api.add_resource(trainModel,"/trainModel")
api.add_resource(updateProfiles,"/setProfile")


# CONFIGURACION DE EJCUCION
if __name__ == "__main__":
    app.run(host= '0.0.0.0',debug=True)