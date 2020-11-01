from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from entities.user import User

class Querys:
    
    def __init__(self,app):
        app.config['MYSQL_HOST'] = '192.168.0.102'
        app.config['MYSQL_USER'] = 'adm1'
        app.config['MYSQL_PASSWORD'] = 'marcpass'
        app.config['MYSQL_DB'] = 'dbtestuser'
        self.__mysql = MySQL(app)

    def addNewUser(self, user):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('INSERT INTO Users (personal_Name, username, password1, email) VALUES (%s, %s, %s, %s)',(user.getPersonName(), user.getUserName(), user.getPasswordHash(), user.getEmail()))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar nuevo usuario en la base de datos: " + str(e))
            return False

    def getUserByUsername(self, username):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("SELECT * FROM Users WHERE username = %s",[username])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener datos de usuario de la base de datos: " + str(e))
            return False

    def getUserBySessionKey(self, sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            SELECT Users.idUser, personal_Name, username, password1, email 
            FROM Users INNER JOIN Sessions 
            ON Users.idUser = Sessions.idUser WHERE session_key = %s""",[sk])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener usuario medainte sk de la base de datos: " + str(e))
            return False
        
    # EDIT el password no cambia por ahora
    def updateUser(self, user, id):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            UPDATE Users 
            SET personal_name = %s,
            username = %s,
            email = %s,
            password1 = %s 
            WHERE idUser = %s
            """, (user.getPersonName(), user.getUserName(), user.getEmail(), user.getPasswordHash(), id))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizr datos de usuario: " + str(e))
            return False

    def getIdByUsername(self, username):
        cur = self.__mysql.connection.cursor()
        cur.execute("SELECT idUser FROM Users WHERE username = %s",[username])
        data=cur.fetchone()
        return data

    def getIdBySessionKey(self, sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            SELECT Users.idUser 
            FROM Users INNER JOIN Sessions 
            ON Users.idUser = Sessions.idUser WHERE session_key = %s""",[sk])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener Id: " + str(e))
            return False

    def getUserById(self, id):
        cur = self.__mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE idUser = %s",[id])
        data=cur.fetchone()
        return data

    def addSk(self,id,sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            INSERT INTO Sessions 
            (idUser, session_key, status_session) 
            VALUES (%s, %s, %s)""",(id, sk, "active"))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar sk de la base de datos: " + str(e))
            return False

    def getForm(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            SELECT * FROM Questions AS q 
            INNER JOIN  Qoptions AS o 
            ON q.idQuestion=o.idQuestion""")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener formulario de base de datos: " + str(e))
            return False

    def getFormQ(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("select * from Questions")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener preguntas de formulario de base de datos: " + str(e))
            return False

    def getFormO(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("select * from Qoptions")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener opciones de formulario de base de datos: " + str(e))
            return False

    def getMysql(self):
        return self.__mysql

