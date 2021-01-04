'''
Clase que contiene los métodos que manejan la sesión del sistema cliente (aplicacion móvil)
'''

import random
import string
from uuid import getnode as get_mac

class SessionManager:

    @staticmethod
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    @staticmethod
    def fillId(idUser):
        id=str(idUser)
        r=""
        l=len(id)
        for x in range(l,4):
        	r+="0"
        idFill=r+id
        return idFill
 
    @staticmethod
    def generateSessionkey(idUser, GUID):
        hashCode=SessionManager.get_random_string(5)
        id=SessionManager.fillId(idUser)
        sessionKey="sk"+GUID+hashCode
        return sessionKey

    @staticmethod
    def getIdFromSK(sessionKey):
        FirstLetter=(sessionKey)[0]
        print(FirstLetter)
        SecondLetter=(sessionKey)[1:3]
        print(SecondLetter)
        Numbers=(sessionKey) [3:6]
        print(Numbers)
