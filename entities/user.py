'''
Clase que modela la entidad "usuario" para uso de la aplicacion movil
'''
from passlib.apps import custom_app_context as pwd_context

class User:
    def __init__(self, personName, userName, email, password):
        self.__id="0"
        self.__personName=personName
        self.__userName=userName
        self.__email=email
        self.__password=password

    def get_user(self):
        data = {"id":self.__id, "username":self.__userName, "password":self.__password, "personname":self.__personName, "email":self.__email}
        return data
        
    def get_userBasic(self):
        data = {"username":self.__userName, "password":self.__password, "personname":self.__personName, "email":self.__email}
        return data

    def setId(self, id):
        self.__id=id
    
    def getId(self):
        return self.__id

    def setPersonName(self, personName):
        self.__personName=personName

    def getPersonName(self):
        return self.__personName

    def setUserName(self, userName):
        self.__userName=userName

    def getUserName(self):
        return self.__userName

    def setEmail(self, email):
        self.__email=email

    def getEmail(self):
        return self.__email

    def setPassword(self, password):
        self.__password=password

    def getPassword(self):
        return self.__password

    def getPasswordHash(self):
        return self.__password_hash

    def setPasswordHash(self, passwordHash):
        self.__password_hash=passwordHash

    def hash_password(self):
        self.__password_hash = pwd_context.encrypt(self.__password)

    def verify_password(self, password):
        #print(pwd_context._get_or_identify_record(self.__password_hash))
        return pwd_context.verify(password, self.__password_hash)