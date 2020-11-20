from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

from sessionManager import SessionManager as sm
from dbManager import Querys
from formManager import FormManager
from entities.user import User
from entities.form import Form
from entities.option import Option
from entities.question import Question

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
        return userQ[1]
    print("usuario '{0}' no autorizado".format(username))
    return False

# Principal
class home(Resource):
    def get(self):
        return jsonify({"message": "Bienvenido a recommendautos"})

# Bienvenida a usuario
class wellcome(Resource):
    @auth.login_required
    def get(self):
        return jsonify({"message":"Hola {}!,\n Bienvenido".format(auth.current_user())})

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

# ASOCIACION DE RECURSOS Y RUTAS
api.add_resource(home,"/")
api.add_resource(wellcome,"/wellcome")
api.add_resource(addUser,"/signUp")
api.add_resource(checkUser,"/signUp/user/<string:user_name>")
api.add_resource(checkEmail,"/signUp/email/<string:user_email>")
api.add_resource(verifyUser,"/logIn")
api.add_resource(dataUser,"/user")
api.add_resource(getForm,"/form")

# CONFIGURACION DE EJCUCION
if __name__ == "__main__":
    app.run(host= '0.0.0.0',debug=True)
