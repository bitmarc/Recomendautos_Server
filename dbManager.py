from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from entities.user import User

class Querys:
    
    def __init__(self,app):
        app.config['MYSQL_HOST'] = '192.168.0.102'
        app.config['MYSQL_USER'] = 'adm1'
        app.config['MYSQL_PASSWORD'] = 'marcpass'
        app.config['MYSQL_DB'] = 'recomendautosdb'
        self.__mysql = MySQL(app)

# CONSULTAS USUARIO
    def addNewUser(self, user):#+
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertaUsuario(%s,%s,%s,%s)',
            (user.getPersonName(), user.getUserName(), user.getEmail(), user.getPasswordHash()))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar nuevo usuario en la base de datos: " + str(e))
            return False

    def getUserByUsername(self, username):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerUsuarioPorNusuario(%s)',[username])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener datos de usuario de la base de datos: " + str(e))
            return False
    
    def getUserById(self, id):
        cur = self.__mysql.connection.cursor()
        cur.execute('CALL sp_obtenerUsuarioPorId(%s)',[id])
        data=cur.fetchone()
        return data

    def getIdByUsername(self, username):
        cur = self.__mysql.connection.cursor()
        cur.execute('CALL sp_obtenerIdPorNombreU(%s)',[username])
        data=cur.fetchone()
        return data

    def updateUser(self, user, id):#+
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_actualizarUsuario(%s,%s,%s,%s,%s)', 
            (user.getPersonName(), user.getUserName(), user.getEmail(), user.getPasswordHash(), id))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizr datos de usuario: " + str(e))
            return False

# CONSULTAS sesion
    def addSk(self,id,sk,status):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarSesion(%s,%s,%s)',(id, sk, status))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar sk de la base de datos: " + str(e))
            return False

    def getUserBySessionKey(self, sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerUsuarioPorSk(%s)',[sk])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener usuario medainte sk de la base de datos: " + str(e))
            return False

    def getIdBySessionKey(self, sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerIdPorSk(%s)',[sk])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener Id: " + str(e))
            return False

    def UpdateSessionbyId(self, id, sk, estado):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_actualizarSesionPorId(%s,%s,%s)', (id,sk,estado))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizar sesion: " + str(e))
            return False

    def getIdSessionBySessionKey(self, sk):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerIdSesionPorSk',[sk])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener Id: " + str(e))
            return False

# CONSULTAS preguntas

    def getFormQ(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("select * from preguntas")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener preguntas de formulario de base de datos: " + str(e))
            return False

# CONSULTAS respuestas

    def getFormO(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("select * from respuestas")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener opciones de formulario de base de datos: " + str(e))
            return False

# CONSULTAS solicitudes

    def getForm(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL obtenerFormulario()')
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener formulario de base de datos: " + str(e))
            return False

    def getFormResponsesByIdReq(self, id_Req):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerResultadosPorIdSol(%s)',[id_Req])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener resultados de base de datos: " + str(e))
            return False

    def addRequest(self,typeR,date,idUser):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarSolicitud(%s,%s,%s)',(typeR, date, idUser))
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al agregar y obtener datos de solicitud : " + str(e))
            return False

# CONSULTAS resultados

    def addResult(self,id_Req,id_que,id_resp):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarResultado(%s,%s,%s)',(id_Req, id_que, id_resp))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar resultado de la base de datos: " + str(e))
            return False

# CONSULTAS recomendacion

    def addRecom(self,id_Req,id_prof):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarRecomendacion(%s,%s)',(id_Req, id_prof))
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al agregar y obtener recomendacion en la base de datos: " + str(e))
            return False

    def addResultRecom(self,idRecom,idAuto):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarResultadoRecom(%s,%s)',(idRecom, idAuto))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al obtener formulario de base de datos: " + str(e))
            return False

    def getRecomByIdReq(self,id_Req):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerRecomPorIdSol(%s)',[id_Req])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener recomendacion de la base de datos: " + str(e))
            return False

    def getAutosByIdRecom(self,id_Recom):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerAutomovilesPorIdRecom(%s)',[id_Recom])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener resultados de automoviles de la base de datos: " + str(e))
            return False

    def getAutosByIdReq(self,id_Req):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerAutomovilesPorIdSol(%s)',[id_Req])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener resultados de automoviles de la base de datos: " + str(e))
            return False

    def getHistoryRequestByIdUser(self,id_user):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerHistSolPorIdUser(%s)',[id_user])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener historial de solicitudes de la base de datos: " + str(e))
            return False
            
# CONSULTAS automoviles
    def getAuto(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            SELECT * FROM automoviles""")
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener automoviles de base de datos: " + str(e))
            return False

# CONSULTAS perfiles

    def getPerfil(self,id_prof):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("""
            SELECT * FROM perfiles 
            WHERE id_perfil=%s """,[id_prof])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener perfil de base de datos: " + str(e))
            return False


    def getMysql(self):
        return self.__mysql

