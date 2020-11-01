from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

from sessionManager import SessionManager as sm
from dbManager import Querys
from formManager import FormManager
from entities.user import User
from entities.form import Form
from entities.option import Option
from entities.question import Question

# Variables
app = Flask(__name__)
auth = HTTPBasicAuth()
MyConnection=Querys(app)

# Metodo de verificacion de password para autenticación
@auth.verify_password
def verify_password(username, password):
    userQ=MyConnection.getUserByUsername(username)
    if(userQ):
        user = User("0",userQ[2],"0","0")
        user.setPasswordHash(userQ[3])
        if not user or not user.verify_password(password):
            print("usuario '{0}' no autorizado".format(username))
            return False
        print("usuario '{0}' autorizado".format(username))
        return userQ[1]
    print("usuario '{0}' no autorizado".format(username))
    return False

# Ruta principal
@app.route("/")
def home():
    return jsonify({"message": "Bienvenido a recommendautos"})
    
# Ruta de bienvenida a usuario
@app.route("/wellcome")
@auth.login_required
def wellcome():
    return jsonify({"message":"Hola {}!,\n Bienvenido".format(auth.current_user())})

# Ruta para registro de nuevos usaurios
@app.route("/signUp", methods=['POST'])
def addUser():
    user1=User(request.json['personname'],request.json['username'],request.json['email'],request.json['password'])
    user1.hash_password()
    if(MyConnection.addNewUser(user1)):
        print("El usuario '{}' se agrego satisfactoriamente".format(user1.getUserName()))
        return jsonify({"message":"Usuario agregado satisfactoriamente", "user": user1.get_userBasic()})
    print("Error al agregar al usuario '{}'".format(user1.getUserName()))
    return jsonify({"message":"Error al agregar nuevo usuario", "user": user1.get_userBasic()})

# Ruta para consultar si un nombre de usuario esta regisytrado
@app.route("/signUp/user/<string:user_name>", methods=['GET'])
def checkUser(user_name):
    user=MyConnection.getUserByUsername(user_name)
    if(user):
        print("El nombre de usuario '{}' ya existe".format(user_name))
        return jsonify({"message":"El usuario ya existe"})
    print("El nombre de usuario '{}' no existe".format(user_name))
    return jsonify({"message":"El usuario no existe"})

# Ruta para consultar si un correo electronico ya esta registrado
@app.route("/signUp/email/<string:user_email>", methods=['GET'])
def checkEmail():
    pass

# Ruta para realizar el inicio de sesión
@app.route("/logIn", methods=['POST'])
def verifyUser():
    fakeUser=User("person",request.json['username'],"email",request.json['password'])
    GUID=request.json['id']
    user=MyConnection.getUserByUsername(fakeUser.getUserName())
    if(user):
        fakeUser.setPasswordHash(user[3])
        if(fakeUser.verify_password(request.json['password'])):
            sk=sm.generateSessionkey(user[0],GUID)
            if(MyConnection.addSk(user[0],sk)):
                fakeUser.setId(sk)
                fakeUser.setPersonName(user[1])
                fakeUser.setEmail(user[4])
                print("El usuario {} accedio satisfactoriamente".format(fakeUser.getUserName()))
                return jsonify({"message":"El usuario accedio satisfactoriamente", "user": fakeUser.get_user()})
            print("Error al agregar sk en db")
    print("el usuario no existe o contraseña icorecta")
    return jsonify({"message":"Error de autenticación", "user": fakeUser.get_user()})

# Ruta para obtener la informacion de un usuario
@app.route("/user", methods=['POST'])
@auth.login_required
def getDataUser():
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

# Ruta para actualizar datos de un usuario
@app.route("/user", methods=['PATCH']) # para actualizar los datos de un usuario
def updateUser():
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
                fakeUser.setEmail(user[4])
                print("El usuario {},ha sido actualizado correctamente".format(fakeUser.getUserName()))
                return jsonify({"message":"Usuario actualizado correctamente", "user": fakeUser.get_user()}) 
            print("El usuario {},ha sido actualizado correctamente, error al retornar nuevos datos".format(fakeUser.getUserName()))
            return jsonify({"message":"Usuario actualizado, error al retornar nuevo usuario", "user": fakeUser.get_user()})
    print("Error al actualizar datos del usuario{}, id no encontrado".format(fakeUser.getUserName()))
    return jsonify({"message":"Error al actualizar datos de usuario", "user": fakeUser.get_user()})


# Ruta para obtener formulario
@app.route("/form", methods=['GET'])
def getForm():
    formulario=FormManager.buildForm(MyConnection)
    return jsonify(formulario.getForm())

@app.route("/test", methods=['GET'])
def getQ():
    formulario=FormManager.buildForm(MyConnection)
    return jsonify(formulario.getForm())

if __name__ == "__main__":
    app.run(host= '0.0.0.0',debug=True)
    #app.run(debug=True, port=4000)
    # comentario prueba