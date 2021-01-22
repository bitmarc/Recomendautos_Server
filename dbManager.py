'''
Clase que administra y maneja la conexión a la base de datos y ejecucion de consultas
'''
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
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al agregar y obtener recomendacion en la base de datos: " + str(e))
            return False

    def addResultRecom(self,idRecom,numero,idAuto):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarResultadoRecom(%s,%s,%s)',(idRecom, numero, idAuto))
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

    def getUrlAuto(self,idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute("CALL  sp_obtenerUrlPorIdAuto(%s)",[idA])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener url de base de datos: " + str(e))
            return False

    def addAuto(self, marca, modelo, año, version, url):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarAutomoviles(%s,%s,%s,%s,%s)',
            (marca, modelo, año, version, url))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar nuevo automovil a la base de datos: " + str(e))
            return False
        
    def addDatasheet(self, idAuto, idAtributo):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarFicha(%s,%s)',
            (idAuto, idAtributo))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar ficha tecnica a la base de datos: " + str(e))
            return False

    def addTag(self, nombre, descripcion):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarEtiqueta(%s,%s)',
            (nombre, descripcion))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar etiqueta a la base de datos: " + str(e))
            return False

    def addLinkAttributeTag(self, idTag, idAttribute):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_asociarEtiquetas_Atributos(%s,%s)',
            (idTag, idAttribute))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al asociar atribto-etiqueta en la base de datos: " + str(e))
            return False

    def addLinkAttributeResponse(self, idResponse, idAttribute):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_asociarRespuestas_Atributos(%s,%s)',
            (idResponse, idAttribute))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al asociar atribto-respuesta en la base de datos: " + str(e))
            return False
    
    def addScoresheet(self, general, confort, desempeño, tecnologia, ostentosidad, deportividad, economia, eficiencia, seguridad, ecologia, afavor, encontra, idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarPuntuacion(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (general, confort,desempeño,tecnologia,ostentosidad,deportividad,economia,eficiencia,seguridad,ecologia,afavor,encontra,idA))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar hoja de puntuaciones en la base de datos: " + str(e))
            return False

    def getOpinions(self,idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerOpinionesPorIdAuto(%s)',[idA])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener opiniones de la base de datos: " + str(e))
            return False

# CONSULTAS perfiles y modelos
    def addModel(self, nombre, fecha):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarModelo(%s,%s)',
            (nombre, fecha))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar modelo a la base de datos: " + str(e))
            return False

    def getLastModel(self):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerUltimoModelo()')
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener modelo a la base de datos: " + str(e))
            return False

    def getPerfil(self,grupo,modelo):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerIdPerfilporClusterModelo(%s,%s)',(grupo, modelo))
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener perfil de la base de datos: " + str(e))
            return False

    def getProfileById(self,idP):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerPerfilporId(%s)',[idP])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener perfil por id de la base de datos: " + str(e))
            return False

    def addProfile(self, nombre, descripcion, grupo, modelo):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarPerfil(%s,%s,%s,%s)',
            (nombre, descripcion, grupo, modelo))
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al agregar perfil a la base de datos: " + str(e))
            return False

    def updateProfileByNcluster(self, nombreP, descripcionP, grupoP):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_actualizarPerfilPorGrupo(%s,%s,%s)',
            (nombreP, descripcionP, grupoP))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizar perfil : " + str(e))
            return False

    def updateProfileByNclusterModel(self, nombreP, descripcionP, grupoP, modeloP):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_actualizarPerfilPorGrupoModelo(%s,%s,%s,%s)',
            (nombreP, descripcionP, grupoP, modeloP))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizar perfil : " + str(e))
            return False

    def linkProfileTag(self, idp, TagName):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_asociarPerfilEtiqueta(%s,%s)',(idp, TagName))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al asociar perfil y etiqueta en la base de datos: " + str(e))
            return False

# tags
    def getTagsByCM(self,grupo,modelo):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerEtiquetasPorClusterModelo(%s,%s)',(grupo, modelo))
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener etiquetas de la base de datos: " + str(e))
            return False

# Atributos

    def addAtribute(self, nombreG, nombreE):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_insertarAtributo(%s,%s)',
            (nombreG, nombreE))
            self.__mysql.connection.commit()
            return True
        except Exception as e:
            print("Error al agregar nuevo atributo en la base de datos: " + str(e))
            return False

    def getAttributesByIdAuto(self, idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerAtributosPorIdAuto(%s)',[idA])
            data=cur.fetchall()
            return data
        except Exception as e:
            print("Error al obtener atributos de la base de datos: " + str(e))
            return False

    def getMaxValAnswByIdAttrib(self, idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerMaxAtribPorRespuesta(%s)',[idA])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener valor maximo de atributo(por respuesta) la base de datos: " + str(e))
            return False

    def getMaxValQuestByIdAttrib(self, idA):
        try:
            cur = self.__mysql.connection.cursor()
            cur.execute('CALL sp_obtenerMaxAtribPorPregunta(%s)',[idA])
            data=cur.fetchone()
            return data
        except Exception as e:
            print("Error al obtener valor maximo de atributo(por pregunta) la base de datos: " + str(e))
            return False


    def getMysql(self):
        return self.__mysql

