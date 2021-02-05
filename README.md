# SERVIDOR RECOMENDAUTOS
## MANUAL DE INSTALCIÓN Y USO

###### *Recomendautos v1.0.1 / febrero 2021* 
___
## Cóntenido:
- [ Inicio](#servidor-recomendautos)
- [1. Requisitos](#1-requisitos)
- [2. Preparacion del entorno](#2-preparacion-del-entorno)
- [3. Instalación del proyecto](#3-instalacion-del-proyecto)
- [4. Instalación de librerias](#4-instalacion-de-librerias)
- [5. Creación y configuración de la base de datos](#5-creacion-y-configuracion-de-la-base-de-datos)
- [6. Configuración de conexión con base de datos](#6-configuracion-de-conexion-con-base-de-datos)
- [7. Ejecución del servidor](#7-ejecucion-del-servidor)
- [8. Exportación de datos](#8-exportacion-de-datos)
- [Anexo problemas y soluciones](#anexo-problemas-y-soluciones)
- [Contacto](#contacto-del-programador)
___
&nbsp;

>Nota: Este manual considera el uso del sistema opertaivo windows como plataforma para la instalación, en caso de utilizar otro sistema operativo se deberá buscar la alternativa a algunos procedimientos aqui descritos.

## 1. Requisitos
Para la instalcion y configuracion del servidor, se requiere el siguiente software: 

- Python 3.8 o superor (obligatorio)
- Mysql server (obligatorio)
- Visual studio code (recomendado)
- MySql Workbench (recomendado)
- git (opcional)

## 2. Preparacion del entorno
Antes de comenzar a instalar las dependencias se recomienda el uso de un entorno virtual.
A continuación se explica como instalar **virtualenv** y crear un entorno virtual. 

> Si esta en Windows asegurese de tener Python agregado la variable PATH del sistema para poder ejecutarlo en una terminal sobre cualquier ruta del sistema. si no sabe como ahcerlo puede visitar este [enlace](https://www.kyocode.com/2019/10/agregar-python-path-windows/) para guiarse

2.1. **Actualizar el gestor de paquetes pip.** Abrir el CMD o su terminal de preferencia y ejecutar el siguiente comando:
```cmd
C:\> python -m pip install --upgrade pip
```
2.2. **Instalar virtualenv**. Una vez actualizado pip, ejecutar el siguiente comando:
```cmd
C:\> pip install virtualenv
```
2.3. **Crear un entorno virtual**. Mediante su terminal acceda al directorio en donde desee crear su entorno virtual (creará una carpeta de configuración), y ejecute el siguiente comando:
```cmd
C:\dir> virtualenv nombre_entorno -p python
```
2.4. Para **activar** el entrono utilice `activate`. Estando en el directorio donde creó el entorno ejecute:
```cmd
C:\dir> nombre_entorno/scripts/activate
```
2.5. Para **desactivar** el entorno utilice `activate`. Del mismo modo:
```cmd
(nombre_entorno)C:\dir> nombre_entorno/scripts/deactivate
```

## 3. Instalacion del proyecto
Medinte su terminal dirigase a la ruta de su preferencia donde instalará el proyecto. Si ha instalado **git**, puede clonarlo directamente del repositorio de github como se explicac a continuación.

En caso de que ya cuente cuetne con el Zip del proyecto, descomprimalo en al ruta seleccionada y omita el resto del paso 3 y valla al paso 4.

3.1. En su terminal, ejecute el siguiente comando:
```cmd
C:\dir> git clone https://github.com/bitmarc/Recomendautos_Server.git
```
A continuación el proyecto será descargado en la ruta actual.
## 4. Instalacion de librerias
Para continuar asegurese de que ha activado su entorno virtual. (puede verificarlo si en al inicio de la linea de comando aparece el nombre de su entorno). Medainte el uso del gestor de paquetes pip deberá instalar las siguietnes dependencias. Para esto use  `pip install`  y a continuación el nombre de cada paquete. Si experimenta algun problema en la instalación revise la sección de [problemas y soluciones](#anexo-problemas-y-soluciones)
- falsk
- Flask-RESTful
- Flask-MySQLdb
- boto3
- scrapy
- kmodes
- scikit-learn
- mysql-flask
- passlib
- pandas
- SQLAlchemy
- PyMySQL 
- domo


## 5. Creacion y configuracion de la base de datos
Antes de ejecutar el servidor, deberá crear la base de datos en mysql server y configurar algunos parámetros para poder conectarse de manera remota, para ello, siga los siguientes pasos:

5.1. Cree un nuevo usuario:
* Ejecute MySqlWorkbech e inicie la instancia de root
* En la pestala de administración seleccione la opcion **usuarios y privilegios**
* Seleccione **agregar nueva cuenta** y a continuacion llene los campos de nombre de usuario, contraseña y cambie el tipo de autenticación a *"estandar"*
*  Dirigase a la pestaña de **roles administrativos** y agregue el rol de *"DbManager"*, a continuacion aplique los cambios

5.2. Cree una nueva conexión:
* Dentro de la pestaña principal, seleccione **agregar un nueva conexión**.
* Establesca el nombre de la conexión, el nombre de usuario y contraseña que definió en el paso anterior. Deje el vpuerto y direccion en los valores por default: `127.0.0.1` y puerto `3306`, a continuacion de en aceptar.

5.3. Entre a la conexion creada y cree la base de datos.:
* Seleccione la opcion **crear nuevo schema** debajo de la barra de herramientas
* Establesca el nombre "recomendautosdb" y a continuación establesca como set de caracteres de codificación `UTF8mb4_unicode_ci`
*  A continuación cargue el script `CreateRecomendautosdb.sql` que se encuentra dentro de la carpeta **sqlDb** dentro del directorio del proyecto
* Ejecute el script.

5.4. Ahora cargue el script: `formRecomendautos.sql` ubicado en la carpeta del proyecto.
5.5. Configure MySql server para recibir conexiones remotas:
* Abra el archivo `my.cnf` ubicado en `C:\ProgramData\MySQL\Mysql Server 8.0`.
* Busque la linea `bind-addres=127.0.0.1` dentro de la sección [mysqld] y cambie la direccion ip por `0.0.0.0`. 
* Guarde los cambios y cierre el archivo.
* Reinicie el servicio de Mysql server mediante al administrador de tareas.
> Nota: asegurese de tener el puerto habilitado en el firewall de Windows o establesca una regla inbound.

## 6. Configuracion de conexion con base de datos
Para que el servidor pueda establecer conexion con la base de datos, deberá configurar algunos parámetros de conexión. para ello siga los siguietes pasos:
1. Mediante su editor de codigo o cualquier editor de texto abra el archivo `dbManager.py` el cual se encuentra en la raiz del proyecto.
2. Debera localizar y cambiar las siguientes lineas que hacen referencia a los parametros de conexion con la base de datos.
```py
self.__host='dirección_ip'  #direccion ip del host en el que se aloja la base de datos
self.__user='usuario'       #nombre del usurio de base de datos
self.__password='contraseña'#contraseña del usaurio de base de datos
self.__db='recomendautosdb' #nombre de la base de datos
```
3. Guerde los cambios.

> Nota:
En caso de que la base de datos se encuentre en el mismo equipo, debera especificar la direccion `127.0.0.1`, y deberá verificar que el servicio se encuentre activo. En caso de precentar un error de conexion por contraseña invalida, debera revisar correctamente los pasos de la [sección 5](#5-creacion-y-configuracion-de-la-base-de-datos).


## 7. Ejecucion del servidor
Para poder ejecutar el servidor, se debera acceder a la ruta raiz del proyecto y verificar que se tenga activo el entorno virtual donde se instalaron todas las librerias. Una vez echo esto, se ejecutará el siguiente comando:
```cmd
(virtualenv)C:\dir> python server.py
```
Esto ejecutará la instancia del servidor y podrá visualizar lo siguiete en terminal:

[![ejecucón de servidor en terminalterminal](http://drive.google.com/uc?export=view&id=1AzBZm17ifcTBanKdu3CoA-u5sCWgGIh8)](http://drive.google.com/uc?export=view&id=1ebculvM-oLpQfggtl4FR9z9CZIOpirQg)

Puede verificar que efectivamente el servidor esta funcionando accediendo a la direccion ip del host a travez del puerto 5000 (especificado por default) especificado mediante un navegador o un softwware de peticiones como se ve acontinuación:

[![ejecucón de servidor en terminalterminal](http://drive.google.com/uc?export=view&id=1ebculvM-oLpQfggtl4FR9z9CZIOpirQg)](http://drive.google.com/uc?export=view&id=1AzBZm17ifcTBanKdu3CoA-u5sCWgGIh8)

## 8. Exportacion de datos

Antes de intentar consumir el servicio, deberá exportar los datos escenciales a la base de datos, para ello deberá seguir los  siguientes pasos:

>**IMPORTANTE**
Este procedimiento deber'a ser ejecutado una sola vez, por lo que se recomienda no interrumpirlo. o ejecutarlo una segunda vez, si esto pasa, el sistema precentara errores debido a la duplicaci'on de algunos datos, en este caso vea la seccion de [problemas y soluciónes](#anexo-problemas-y-soluciones).

1. Con el servicio activo, abra su navegoador web o algun software simulador de peticiones como *postman* o *insomnia*.
2. Envie una peticion ***GET*** a la siguiente ruta: `http://192.168.0.104:5000/exportData` cambiando por supuesto la direccion ip con la de su host y el puerto que corresponda.
3. Deberá esperar unos minutos a que finalize la exportacion de los datos (podrá ver el estado del proceso en terminal)

&nbsp;
______

##### En este punto el servidor queda configurado y listo para recibir peticiones desde la aplicación movil. Si aún no cuenta con ella puede descargar el repositorio de la misma  [aquí](https://github.com/bitmarc/Recommender)
______
&nbsp;
## ANEXO problemas y soluciones

A continuación se precentan algunos problemas que podrían sergir y como soluciónarlos.

- **Error de consola, no detecta python como comando valido.**
Es posible que tenga dos versiones de python instaladas v2 y v3 , en dicho caso, deberá ejecutar python médiante "python3" para ejecutarcon el interprete de python 3. si el problema persiste, deberá asegurarse de que python está instalado en su versión 3.8 y se encuentra en las variables PATH del sistema. puede verificar su instalación mediante la ejecución de  `python --version` desde su terminal.

- **Error al activar un entorno virtual desde Visual Studio**
Por defecto visual studio code no permite la activación del comando, por lo que si es primera vez que ejecuta un entorno virtual, deberá ir a **File -> Preferences -> Settings** y a continuacion en la barra de busqueda de onfiguración tclee: `automation`. Dspués deberá clickear la opción "**Edit in settings.json**" dentro de la categoria correspondiente a su sistema operativo. Una vez ahí asegurece de tener el siguiente codigo, al finalizar guerdelo y reinicie Visual Studio

```json
"terminal.integrated.shellArgs.windows": [
        "-ExecutionPolicy",
        "Bypass"
    ],
    ...
```
- **Error al instalar flask-mysqldb "requiere visual c++ 14.0 o superior"**
si ya cuenta con la versión más actual de visual c++, deberá descargar e instalar ***Visual studio build tools*** desde la web oficial. una vez instalada, o si ya la tiene instalada, al abrir visual studio installer debera dar click en *"modify"* y posteriormente en la pestaña "workloads" marcar el recuadro de "***C++  build tools***", finalmente cerrar e intentarlo nuevamente.

- **Error al instalar flask-mysqldb "wheel error running setup.py"**
debéra instalar primero **mysqlclient** mediante `pip install mysqlclient`, si por alguna razón le arroja un error relacionado a ´´wheel´´. deberá instalarlo manualmente. Para ello descrgue la el binario de la libreria correspondiente a su plataforma desde este [sitio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient). si no sabe cual es el archivo correcto , deberá porbar uno por uno. Para instalarlo, guarde el archivo en cualquier directorio y desde su terminal en esa ruta ejecute: `pip intsal mysqlclient... *.whl` , sustituyendo al nombre del archivo correspondiente. Al finalizar, deberia poder instalar **flask-mysqlclient** sin problemas.

- **Error al instalar scrapy "Failed building wheel for Twisted"**
debéra instalar twisted manualmente. Para ello descrgue la el binario de la libreria correspondiente a su plataforma desde este [sitio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted). Para instalarlo, guarde el archivo en cualquier directorio y desde su terminal en esa ruta ejecute: `pip intsal Twisted... *.whl` , sustituyendo al nombre del archivo correspondiente. Al finalizar, deberia poder instalar **scrapy** sin problemas.


Licencia
----
*Open source*

**Free Software**


### Contacto del programador:

[@hermuslife](https://twitter.com/hermuslife)

marcoarojas.95@gmail.com

&nbsp;

