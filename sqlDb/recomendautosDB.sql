/* 
	BASE DE DATOS PARA EL SISTEMA "RECOMENDAUTOS"
	SCRIPT 4.0
	febrero 2021
*/

# --------------------------------------------------------------------	CREACION E IMPLEMENTACION
USE recomendautosdb;
# --------------------------------------------------------------------	TABLA USUARIOS
CREATE TABLE usuarios(
id_usuario INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nombre_personal VARCHAR(60),
nombre_usuario VARCHAR(20),
correo_electronico VARCHAR(30),
contraseña VARCHAR(130)
);

# --------------------------------------------------------------------	TABLA SESIONES
CREATE TABLE sesiones(
id_sesion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_usuario INT,
llave_de_sesion VARCHAR(80),
estado VARCHAR(20),
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

# --------------------------------------------------------------------TABLA PREGUNTAS
CREATE TABLE preguntas(
id_pregunta INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
titulo VARCHAR(180),
ayuda VARCHAR(250)
);

# --------------------------------------------------------------------TABLA RESPUESTAS
CREATE TABLE respuestas(
id_respuesta INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
titulo VARCHAR(150),
id_pregunta INT,
FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
);

# --------------------------------------------------------------------TABLA MODELOS
CREATE TABLE modelos(
id_modelo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nombre_modelo VARCHAR(30),
fecha_creacion DATETIME
);

# --------------------------------------------------------------------TABLA PERFILES
CREATE TABLE perfiles(
id_perfil INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nombre VARCHAR(50),
descripcion VARCHAR(300),
grupo INT,
id_modelo INT,
FOREIGN KEY (id_modelo) REFERENCES modelos(id_modelo)
);

# --------------------------------------------------------------------TABLA SOLICITUDES
CREATE TABLE solicitudes(
id_solicitud INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
tipo VARCHAR(50),
fecha DATETIME,
id_usuario INT,
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

# --------------------------------------------------------------------TABLA RESULTADOS
CREATE TABLE resultados(
id_resultado INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_solicitud INT,
id_pregunta INT,
id_respuesta INT,
FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta),
FOREIGN KEY (id_respuesta) REFERENCES respuestas(id_respuesta)
);

# --------------------------------------------------------------------TABLA RECOMENDACION
CREATE TABLE recomendaciones(
id_recomendacion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_solicitud INT,
id_perfil INT,
FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
);

# --------------------------------------------------------------------TABLA AUTOMOVILES

CREATE TABLE automoviles(
id_automovil INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
marca VARCHAR(20),
modelo VARCHAR(20),
año VARCHAR(5),
version VARCHAR(50),
url VARCHAR(140),
resumen VARCHAR(250)
);

# --------------------------------------------------------------------TABLA RESULTADOS_RECOMENDACION
CREATE TABLE resultados_recomendacion(
id_resultado_recomendacion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_recomendacion INT,
numero INT,
id_automovil INT,
FOREIGN KEY (id_recomendacion) REFERENCES recomendaciones(id_recomendacion),
FOREIGN KEY (id_automovil) REFERENCES automoviles(id_automovil)
);

# --------------------------------------------------------------------TABLA atributos
CREATE TABLE atributos(
id_atributo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nombre_atributo_general VARCHAR(70),
nombre_atributo_especifico VARCHAR(70)
);
# --------------------------------------------------------------------TABLA autos_as_atributos   FICHAS TECNICAS
 
 CREATE TABLE fichas_tecnicas(
id_ficha INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_automovil INT,
id_atributo INT,
FOREIGN KEY (id_automovil) REFERENCES automoviles(id_automovil),
FOREIGN KEY (id_atributo) REFERENCES atributos(id_atributo)
);

# --------------------------------------------------------------------TABLA PUNTUACIONES

CREATE TABLE hojas_puntuaciones(
id_hoja_puntuacion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
p_general INT,
p_confort INT,
p_desempeño INT,
p_tecnologia INT,
p_ostentosidad INT,
p_deportividad INT,
p_economia INT,
p_eficiencia INT,
p_seguridad INT,
p_ecologia INT,
id_automovil INT,
a_favor VARCHAR(450),
en_contra VARCHAR(450),
cPositivos INT,
cNegativos INT,
FOREIGN KEY (id_automovil) REFERENCES automoviles(id_automovil)
);

# --------------------------------------------------------------------TABLA etiquetas
CREATE TABLE etiquetas(
id_etiqueta INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nombre_etiqueta VARCHAR(30),
descripcion VARCHAR(80)
);

CREATE TABLE perfiles_etiquetas(
id_perfil_etiqueta INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_perfil INT,
id_etiqueta INT,
puntuacion INT,
FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil),
FOREIGN KEY (id_etiqueta) REFERENCES etiquetas(id_etiqueta)
);

CREATE TABLE etiquets_atributos(
id_etiqueta_atributo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_etiqueta INT,
id_atributo INT,
FOREIGN KEY (id_etiqueta) REFERENCES etiquetas(id_etiqueta),
FOREIGN KEY (id_atributo) REFERENCES atributos(id_atributo)
);

CREATE TABLE respuestas_atributos(
id_respuesta_atributo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
id_respuesta INT,
id_atributo INT,
FOREIGN KEY (id_respuesta) REFERENCES respuestas(id_respuesta),
FOREIGN KEY (id_atributo) REFERENCES atributos(id_atributo)
);
#--------------------------------------------------------------------------------------------------------------------------------

/*
	PROCEDIMIENTOS ALMACENADOS PARA BASE DE DATOS recomendautosDB
    v4.0
*/

USE recomendautosdb;
# //////////////////////////////////////////////////////////////////////////////////////	USUARIOS	//////////////////////////

DROP procedure IF EXISTS `sp_insertaUsuario`;#----------------------	sp_insertaUsuario	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertaUsuario` (IN nombreP VARCHAR(60), 
										nombreU VARCHAR(20), 
                                        correo VARCHAR(30), 
                                        contrasenia VARCHAR(130))
BEGIN
INSERT INTO usuarios (nombre_personal, nombre_usuario, correo_electronico, contraseña)
VALUES (nombreP, nombreU, correo, contrasenia);
END$$
DELIMITER ;


DROP procedure IF EXISTS `sp_obtenerUsuarioPorNusuario`;#----------------------	sp_obtenerUsuarioPorNusuario	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerUsuarioPorNusuario` (IN nombreU VARCHAR(20))
BEGIN
SELECT * FROM usuarios WHERE nombre_usuario = nombreU;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerUsuarioPorId`;#----------------------	sp_obtenerUsuarioPorId	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerUsuarioPorId` (IN id INT)
BEGIN
SELECT * FROM usuarios WHERE id_usuario = id;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerIdPorNombreU`;#----------------------	sp_obtenerIdPorNombreU	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerIdPorNombreU` (IN nombreU VARCHAR(20))
BEGIN
SELECT id_usuario FROM usuarios WHERE nombre_usuario = nombreU;
END$$
DELIMITER ;


DROP procedure IF EXISTS `sp_actualizarUsuario`;#----------------------	sp_actualizarUsuario	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarUsuario` (IN nombreP VARCHAR(60),
											nombreU VARCHAR(20),
                                            correo VARCHAR(30),
                                            contrasenia VARCHAR(130),
                                            id INT)
BEGIN
UPDATE usuarios 
SET nombre_personal = nombreP, nombre_usuario = nombreU, correo_electronico = correo, contraseña = contrasenia 
WHERE id_usuario= id;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	SESIONES	//////////////////////////

DROP procedure IF EXISTS `sp_insertarSesion`;#----------------------	sp_insertarSesion	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarSesion` (IN idU INT,
									sk VARCHAR(80),
                                    estado VARCHAR(20))
BEGIN
INSERT INTO sesiones (id_usuario, llave_de_sesion, estado)
VALUES (idU, sk, estado);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerUsuarioPorSk`;#----------------------	sp_obtenerUsuarioPorSk	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerUsuarioPorSk` (IN sk VARCHAR(80))
BEGIN
SELECT usuarios.id_usuario, nombre_personal, nombre_usuario, contraseña, correo_electronico 
FROM usuarios INNER JOIN sesiones 
ON usuarios.id_usuario = sesiones.id_usuario
WHERE llave_de_sesion = sk;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerIdPorSk`;#----------------------	sp_obtenerIdPorSk	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerIdPorSk` (IN sk VARCHAR(80))
BEGIN
SELECT usuarios.id_usuario 
FROM usuarios INNER JOIN sesiones 
ON usuarios.id_usuario = sesiones.id_usuario
WHERE llave_de_sesion = sk;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_actualizarSesionPorId`;#----------------------	sp_actualizarSesionPorId	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarSesionPorId` (IN idS INT,
												sk VARCHAR(80),
                                                estadoS VARCHAR(20))
BEGIN
UPDATE sesiones
SET llave_de_sesion=sk, estado=estadoS
WHERE id_sesion=idS;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerIdSesionPorSk`;#----------------------	sp_obtenerIdSesionPorSk	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerIdSesionPorSk` (IN sk VARCHAR(80))
BEGIN
SELECT id_sesion FROM sesiones WHERE llave_de_sesion=sk;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	PREGUNTAS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarPregunta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarPregunta` (IN tituloP VARCHAR(180),
                                        ayudaP VARCHAR(250))
BEGIN
INSERT INTO preguntas (titulo, ayuda)
VALUES (tituloP,ayudaP);
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	RESPUESTAS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarRespuesta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarRespuesta` (IN tituloR VARCHAR(150),
											idPregunta INT)
BEGIN
INSERT INTO respuestas (titulo,id_pregunta)
VALUES (tituloR,idPregunta);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerFormulario`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerFormulario` ()
BEGIN
SELECT * FROM preguntas AS p
INNER JOIN respuestas AS r
ON p.id_pregunta = r.id_pregunta;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	MODELOS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarModelo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarModelo` (IN nombreM VARCHAR(30),
										fecha_creacion DATETIME)
BEGIN
INSERT INTO modelos (nombre_modelo, fecha_creacion)
VALUES (nombreM,fecha_creacion);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerUltimoModelo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerUltimoModelo` ()
BEGIN
select id_modelo, nombre_modelo from modelos where fecha_creacion=(SELECT MAX(fecha_creacion) FROM modelos);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerModeloPorNombre`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerModeloPorNombre`(IN
												nombreM VARCHAR(30))
BEGIN
select id_modelo, nombre_modelo from modelos where nombre_modelo=nombreM;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	PERFILES	//////////////////////////

DROP procedure IF EXISTS `sp_insertarPerfil`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarPerfil` (IN nombreP VARCHAR(50),
										descripcionP VARCHAR(300),
                                        grupoP INT,
                                        idModeloP INT)
BEGIN
INSERT INTO perfiles (nombre, descripcion, grupo, id_modelo)
VALUES (nombreP,descripcionP, grupoP, idModeloP);
SELECT id_perfil FROM perfiles WHERE id_modelo=idModeloP AND grupo=grupoP;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerIdPerfilporClusterModelo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerIdPerfilporClusterModelo` (IN grupoP INT,
														idModeloP INT)
BEGIN
SELECT * FROM perfiles WHERE id_modelo=idModeloP AND grupo=grupoP;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerPerfilporId`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerPerfilporId` (IN idP INT)
BEGIN
SELECT * FROM perfiles WHERE id_perfil=idP;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_asociarPerfilEtiqueta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_asociarPerfilEtiqueta` (IN idPerfil INT,
										nEtiqueta VARCHAR(30),
                                        puntuacionPE INT)
BEGIN
INSERT INTO perfiles_etiquetas (id_perfil, id_etiqueta, puntuacion)
VALUES (idPerfil,(SELECT id_etiqueta FROM etiquetas WHERE nombre_etiqueta=nEtiqueta),puntuacionPE);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_reescribirPerfilEtiqueta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_reescribirPerfilEtiqueta` (IN idPerfil INT)
BEGIN
DELETE FROM perfiles_etiquetas WHERE id_perfil = idPerfil;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_actualizarPerfilPorGrupo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarPerfilPorGrupo` (IN nombreP VARCHAR(40),
													descripcionP VARCHAR(200),
                                                    grupoP INT)
BEGIN
UPDATE perfiles
SET nombre=nombreP, descripcion=descripcionP
WHERE id_modelo=(select id_modelo from modelos where fecha_creacion=(SELECT MAX(fecha_creacion) FROM modelos)) AND grupo=grupoP;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_actualizarPerfilPorGrupoModelo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarPerfilPorGrupoModelo` (IN nombreP VARCHAR(40),
													descripcionP VARCHAR(200),
                                                    grupoP INT,
                                                    nombreMod VARCHAR(30))
BEGIN
UPDATE perfiles
SET nombre=nombreP, descripcion=descripcionP
WHERE id_modelo=(select id_modelo from modelos where nombre_modelo=nombreMod) AND grupo=grupoP;
END$$
DELIMITER ;
# //////////////////////////////////////////////////////////////////////////////////////	SOLICITUDES	//////////////////////////

DROP procedure IF EXISTS `sp_insertarSolicitud`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarSolicitud` (IN tipoS VARCHAR(50),
											fechaS DATETIME,
                                            idUserS INT)
BEGIN
INSERT INTO solicitudes (tipo, fecha, id_usuario)
VALUES (tipoS, fechaS, idUserS);
Select id_solicitud from solicitudes WHERE id_usuario=idUserS AND fecha=fechaS;
END$$
DELIMITER ;


# //////////////////////////////////////////////////////////////////////////////////////	RESULTADOS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarResultado`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarResultado` (IN idS INT, 
											idP INT, 
                                            idR INT)
BEGIN
INSERT INTO resultados (id_solicitud, id_pregunta, id_respuesta)
VALUES (idS,idP,idR);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerResultadosPorIdSol`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerResultadosPorIdSol` (IN idS INT)
BEGIN
SELECT id_solicitud, id_pregunta, id_respuesta FROM resultados
WHERE id_solicitud=idS;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerTodosResultados`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerTodosResultados` ()
BEGIN
SELECT id_solicitud AS solicitud, id_pregunta as idPregunta, id_respuesta as idRespuesta FROM resultados;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	RECOMENDACION	//////////////////////////

DROP procedure IF EXISTS `sp_insertarRecomendacion`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarRecomendacion` (IN idS INT,
												idP INT)
BEGIN
INSERT INTO recomendaciones (id_solicitud, id_perfil)
VALUES (idS,idP);
SELECT id_recomendacion FROM recomendaciones WHERE id_solicitud=idS;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerHistSolPorIdUser`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerHistSolPorIdUser` (IN idUser INT)
BEGIN
SELECT solicitudes.id_solicitud, solicitudes.fecha, perfiles.id_perfil AS "id_perfil", count(*) AS "items"
FROM solicitudes INNER JOIN recomendaciones INNER JOIN perfiles INNER JOIN resultados_recomendacion
ON recomendaciones.id_solicitud = solicitudes.id_solicitud AND recomendaciones.id_perfil = perfiles.id_perfil AND recomendaciones.id_recomendacion = resultados_recomendacion.id_recomendacion
WHERE solicitudes.id_usuario =idUser
GROUP BY resultados_recomendacion.id_recomendacion;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	AUTOMOVILES	//////////////////////////

DROP procedure IF EXISTS `sp_insertarAutomoviles`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarAutomoviles` (IN marcaA VARCHAR(20),
												modeloA VARCHAR(20),
                                                añoA VARCHAR(5),
                                                versionA VARCHAR(50),
                                                urlA VARCHAR(140),
                                                resumenA VARCHAR(250))
BEGIN
INSERT INTO automoviles(marca,modelo,año,version,url,resumen)
VALUES (marcaA,modeloA,añoA,versionA,urlA,resumenA);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_actualizarResumen`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarResumen` (IN idA INT,
										resumenA VARCHAR(250))
BEGIN
UPDATE automoviles
SET resumen = resumenA
WHERE id_automovil= idA;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerUrlPorIdAuto`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerUrlPorIdAuto` (IN idA INT)
BEGIN
SELECT url
FROM automoviles
WHERE id_automovil=idA;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerIdAutoPorAtributo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerIdAutoPorAtributo` (IN idAtributoA INT)
BEGIN
select id_automovil from fichas_tecnicas
where id_atributo=idAtributoA;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_actualizarUrl`;#----------------------	sp_actualizarUsuario	---
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_actualizarUrl` (IN idA INT,
											urlA VARCHAR(140))
BEGIN
UPDATE automoviles 
SET automoviles.url = urlA
WHERE automoviles.id_automovil= idA;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	RESULTADO_RECOMENDACION	//////////////////////////

DROP procedure IF EXISTS `sp_insertarResultadoRecom`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarResultadoRecom` (IN idR INT,
												num INT,
												idA INT)
BEGIN
INSERT INTO resultados_recomendacion (id_recomendacion, numero, id_automovil)
VALUES (idR, num, idA);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerRecomPorIdSol`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerRecomPorIdSol` (IN idSol INT)
BEGIN
SELECT recomendaciones.id_recomendacion, perfiles.id_perfil, perfiles.nombre, perfiles.descripcion, resultados_recomendacion.id_automovil, resultados_recomendacion.numero
FROM recomendaciones INNER JOIN perfiles INNER JOIN resultados_recomendacion
ON recomendaciones.id_perfil = perfiles.id_perfil AND recomendaciones.id_recomendacion=resultados_recomendacion.id_recomendacion
WHERE recomendaciones.id_solicitud = idSol;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerAutomovilesPorIdRecom`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerAutomovilesPorIdRecom` (IN idRecom INT)
BEGIN
SELECT resultados_recomendacion.id_recomendacion, automoviles.id_automovil, automoviles.marca, automoviles.modelo, automoviles.año, automoviles.version
FROM resultados_recomendacion INNER JOIN automoviles
ON resultados_recomendacion.id_automovil = automoviles.id_automovil
WHERE resultados_recomendacion.id_recomendacion = idRecom;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerAutomovilesPorIdSol`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerAutomovilesPorIdSol` (IN idSol INT)
BEGIN
SELECT recomendaciones.id_solicitud, automoviles.id_automovil, automoviles.marca, automoviles.modelo, automoviles.año, automoviles.version
FROM resultados_recomendacion INNER JOIN automoviles INNER JOIN recomendaciones
ON resultados_recomendacion.id_automovil = automoviles.id_automovil AND recomendaciones.id_recomendacion = resultados_recomendacion.id_recomendacion
WHERE recomendaciones.id_solicitud = idSol;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	FICHA_TECNICA	//////////////////////////

DROP procedure IF EXISTS `sp_insertarFicha`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarFicha` (IN idAuto INT,
										idAtrib INT)
BEGIN
INSERT INTO fichas_tecnicas (id_automovil, id_atributo)
VALUES (idAuto,idAtrib);
END$$
DELIMITER ;
# //////////////////////////////////////////////////////////////////////////////////////	ATRIBUTOS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarAtributo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarAtributo` (IN nombreA VARCHAR(70),
											categoriaA VARCHAR(70))
BEGIN
INSERT INTO atributos (nombre_atributo_general, nombre_atributo_especifico)
VALUES (nombreA,categoriaA);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerAtributosPorIdAuto`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerAtributosPorIdAuto` (IN idA INT)
BEGIN
SELECT a.id_atributo, a.nombre_atributo_general, a.nombre_atributo_especifico
FROM atributos AS a INNER JOIN fichas_tecnicas AS ft
ON a.id_atributo = ft.id_atributo
WHERE ft.id_automovil=idA;
END$$
DELIMITER ;

#---------------------------------------------------------factors
DROP procedure IF EXISTS `sp_obtenerMaxAtribPorRespuesta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerMaxAtribPorRespuesta` (IN idA INT)
BEGIN
SELECT count(*) FROM respuestas_atributos AS ra INNER JOIN respuestas AS r
ON ra.id_respuesta=r.id_respuesta
WHERE id_atributo=idA;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerMaxAtribPorPregunta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerMaxAtribPorPregunta` (IN idA INT)
BEGIN
SELECT count(DISTINCT r.id_pregunta) FROM respuestas_atributos AS ra INNER JOIN respuestas AS r
ON ra.id_respuesta=r.id_respuesta
WHERE id_atributo=idA;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	FICHAS_ATRIBUTOS	//////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////	PUNTUACIONES	//////////////////////////

DROP procedure IF EXISTS `sp_insertarPuntuacion`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarPuntuacion` (IN pGeneral INT,
										pConfort INT,
                                        pDesempeño INT,
                                        pTecnologia INT,
                                        pOstentosidad INT,
                                        pDeportividad INT,
                                        pEconomia INT,
                                        pEficiencia INT,
                                        pSeguridad INT,
                                        pEcologia INT,
                                        afavor VARCHAR(450),
                                        encontra VARCHAR(450),
                                        cP INT,
                                        cN INT,
                                        idA INT)
BEGIN
INSERT INTO hojas_puntuaciones (p_general, p_confort, p_desempeño, p_tecnologia, p_ostentosidad, p_deportividad, p_economia, p_eficiencia, p_seguridad, p_ecologia, a_favor, en_contra, cPositivos, cNegativos, id_automovil)
VALUES (pGeneral,pConfort,pDesempeño,pTecnologia,pOstentosidad,pDeportividad,pEconomia,pEficiencia,pSeguridad,pEcologia,afavor,encontra,cP,cN,idA);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerOpinionesPorIdAuto`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerOpinionesPorIdAuto` (IN idA INT)
BEGIN
SELECT hp.a_favor, hp.en_contra, a.url
FROM hojas_puntuaciones as hp INNER JOIN automoviles as a
ON hp.id_automovil = a.id_automovil
WHERE a.id_automovil=idA;
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerPuntuaciones`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerPuntuaciones` ()
BEGIN
select a.marca,a.modelo,a.version as "versión",hp.p_confort as "confort", hp.p_deportividad as "deportividad", hp.p_desempeño as "desempeño", hp.p_ecologia as "ecología", hp.p_economia as "economía", hp.p_eficiencia as "eficiencia", hp.p_ostentosidad as "ostentosidad", hp.p_seguridad as "seguridad", hp.p_tecnologia as "tecnología", hp.p_general as "general", hp.cPositivos as "cP", hp.cNegativos as "cN"
from hojas_puntuaciones as hp right join automoviles as a
on hp.id_automovil=a.id_automovil;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	ETIQUETAS	//////////////////////////

DROP procedure IF EXISTS `sp_insertarEtiqueta`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_insertarEtiqueta` (IN nombreE VARCHAR(30),
										descripcionE VARCHAR(80))
BEGIN
INSERT INTO etiquetas (nombre_etiqueta, descripcion)
VALUES (nombreE,descripcionE);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerEtiquetasPorClusterModelo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerEtiquetasPorClusterModelo` (IN grupoP INT,
														idModeloP INT)
BEGIN
SELECT e.nombre_etiqueta, pe.puntuacion
FROM etiquetas AS e INNER JOIN perfiles AS p INNER JOIN perfiles_etiquetas AS pe
ON e.id_etiqueta=pe.id_etiqueta AND pe.id_perfil=p.id_perfil
WHERE p.id_modelo=idModeloP AND p.grupo=grupoP;
END$$
DELIMITER ;


DROP procedure IF EXISTS `sp_obtenerEtiquetasPorIdAtributo`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerEtiquetasPorIdAtributo` (IN idAtrib INT)
BEGIN
SELECT e.nombre_etiqueta  
FROM etiquets_atributos AS ea INNER JOIN etiquetas AS e
ON e.id_etiqueta=ea.id_etiqueta
WHERE ea.id_atributo = idAtrib;
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	ETIQUETAS_ATRIBUTOS	//////////////////////////
DROP procedure IF EXISTS `sp_asociarEtiquetas_atributos`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_asociarEtiquetas_atributos` (IN idetiqueta INT,
										idatributo INT)
BEGIN
INSERT INTO etiquets_atributos (id_etiqueta, id_atributo)
VALUES (idetiqueta,idatributo);
END$$
DELIMITER ;

# //////////////////////////////////////////////////////////////////////////////////////	RESPUESTAS_ATRIBUTOS	//////////////////////////
DROP procedure IF EXISTS `sp_asociarRespuestas_atributos`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_asociarRespuestas_atributos` (IN idrespuesta INT,
										idatributo INT)
BEGIN
INSERT INTO respuestas_atributos(id_respuesta, id_atributo)
VALUES (idrespuesta,idatributo);
END$$
DELIMITER ;

DROP procedure IF EXISTS `sp_obtenerAtributosPorIdResp`;
DELIMITER $$
USE `recomendautosdb`$$
CREATE PROCEDURE `sp_obtenerAtributosPorIdResp` (IN idRespuesta INT)
BEGIN
select id_atributo from respuestas_atributos
where id_respuesta=idRespuesta;
END$$
DELIMITER ;