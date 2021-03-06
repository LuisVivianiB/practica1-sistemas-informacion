
import sqlite3
import pandas as pd
import json
from numpy import nan


def rellenarTablas(con):

    with open("users.json", "r") as f:
        users_data = json.load(f)

    with open("legal.json", "r") as f1:
        legal_data = json.load(f1)

    cursorObj = con.cursor()
    for i in range(len(legal_data['legal'])):
        for url in legal_data['legal'][i].keys():
            cursorObj.execute("INSERT INTO legal VALUES (?, ?, ?, ?, ?)", (url, legal_data['legal'][i][url]['cookies'], legal_data['legal'][i][url]['aviso'],legal_data['legal'][i][url]['proteccion_de_datos'], legal_data['legal'][i][url]['creacion']))
            con.commit()
    k = 0
    l = 0
    for i in range(len(users_data['usuarios'])):
        for nombre in users_data['usuarios'][i].keys():
            cursorObj.execute("INSERT INTO emails VALUES (?, ?, ?, ?)", (nombre, users_data['usuarios'][i][nombre]['emails']['total'], users_data['usuarios'][i][nombre]['emails']['phishing'], users_data['usuarios'][i][nombre]['emails']['cliclados']))

            for j in range(len(users_data['usuarios'][i][nombre]['ips'])):
                cursorObj.execute("INSERT INTO IpsDeUsuarios VALUES (?, ?, ?)", (k, users_data['usuarios'][i][nombre]['ips'][j], i))
                cursorObj.execute("INSERT INTO ips VALUES (?, ?)",(k, users_data['usuarios'][i][nombre]['ips'][j]))

                k += 1

            for j in range(len(users_data['usuarios'][i][nombre]['fechas'])):
                cursorObj.execute("INSERT INTO fechas VALUES (?, ?)",(l, users_data['usuarios'][i][nombre]['fechas'][j]))
                cursorObj.execute("INSERT INTO FechasDeUsuarios VALUES (?, ?, ?)", (l, users_data['usuarios'][i][nombre]['fechas'][j], i))
                l += 1
            cursorObj.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, users_data['usuarios'][i][nombre]['telefono'], users_data['usuarios'][i][nombre]['contrasena'], users_data['usuarios'][i][nombre]['provincia'], users_data['usuarios'][i][nombre]['permisos'], nombre, i, i))
            con.commit()



def sql_delete_table(con):
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists usuarios')
    cursorObj.execute('drop table if exists emails')
    cursorObj.execute('drop table if exists legal')
    cursorObj.execute('drop table if exists fechas')
    cursorObj.execute('drop table if exists FechasDeUsuarios')
    cursorObj.execute('drop table if exists ips')
    cursorObj.execute('drop table if exists IpsDeUsuarios')
    con.commit()


def sql_create_tables(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre text primary key, telefono integer, contrasena text, provincia text, permisos boolean, emails, fechas integer, ips integer, FOREIGN KEY ('emails') references emails(usuario))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS emails (usuario text primary key, total integer, phishing integer, cliclados integer, FOREIGN KEY ('usuario') REFERENCES usuarios (nombre) )")

    cursorObj.execute("CREATE TABLE IF NOT EXISTS legal (url text primary key, cookies integer, aviso integer, proteccion_de_datos integer, creacion integer)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS fechas (idfechas integer primary key autoincrement, fecha text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS FechasDeUsuarios (idfechas integer primary key autoincrement, fechasdeusua text, usuario integer, FOREIGN KEY ('usuario') references usuarios(fechas), FOREIGN KEY ('fechasdeusua') references fechas(fecha))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS ips(idips integer primary key autoincrement, ip text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS IpsDeUsuarios ( idips integer primary key autoincrement, ipdeusua text, usuario integer, FOREIGN KEY ('usuario') references usuarios(ips), FOREIGN KEY ('ipdeusua') REFERENCES ips (ip))")



    con.commit()

def ejer2(con):
    print("-----------------EJERCICIO 2------------------------")
    #contar numero de muestras de usuarios
    print("El numero de muestras de usuarios es: ")
    muestrasUsuarios = pd.DataFrame(pd.read_sql("SELECT nombre FROM usuarios", con))
    muestrasUsuarios.replace(to_replace=["None"], value=nan, inplace=True)
    num=muestrasUsuarios.count().sum()
    print(num)

    #contar numero de muestras de urls
    print("\n")
    print("El numero de muestras de urls es: ")
    muestrasUrls = pd.DataFrame(pd.read_sql("SELECT url FROM legal", con))
    muestrasUrls.replace(to_replace=["None"], value=nan, inplace=True)
    num = muestrasUrls.count().sum()
    print(num)
    print("\n")

    #media de inicios de sesion por fecha
    fechas= pd.DataFrame(pd.read_sql("SELECT * FROM FechasDeUsuarios",con),columns=["usuario","fechasdeusua"])


    print("Media de inicios de sesion por fecha: ")
    num = fechas.groupby('usuario').count().mean(numeric_only=True)[0]
    print("%.4f\n" %num)

    #Desviaci??n estandar de inicios de sesi??n por fecha

    print("Desviaci??n de inicios de sesion por fecha: ")
    num = fechas.groupby('usuario').count().std(numeric_only=True)[0]
    print("%.4f\n" %num)

    #media de IPS detectadas
    ips= pd.DataFrame(pd.read_sql("SELECT * FROM IpsDeUsuarios",con),columns=["usuario","ipdeusua"])

    print("Media de ips detectadas: ")
    num = ips.groupby('usuario').count().mean(numeric_only=True)[0]
    print("%.4f\n" %num)

    #Desviaci??n estandar de IPS detectadas

    print("Desviaci??n de ips detectadas: ")
    num = ips.groupby('usuario').count().std(numeric_only=True)[0]
    print("%.4f\n" %num)

    #media de numero de emails recibidos
    emails= pd.DataFrame(pd.read_sql("SELECT total FROM emails",con))

    print("Media de emails recibidos: ")
    num = emails.mean(numeric_only=True)[0]
    print("%.4f\n" %num)

    #Desviaci??n estandar de emails recibidos

    print("Desviaci??n de emails recibidos: ")
    num = emails.std(numeric_only=True)[0]
    print("%.4f\n" %num)

    #valor maximo del total de fechas que se ha iniciado sesion
    print("Valor maximo del total de fechas que se ha iniciado sesi??n: ")
    num = fechas.groupby('usuario').count().max().sum()
    print(num)
    print("\n")

    # valor minimo del total de fechas que se ha iniciado sesion
    print("Valor minimo del total de fechas que se ha iniciado sesi??n: ")
    num = fechas.groupby('usuario').count().min().sum()
    print(num)
    print("\n")
    
    # valor maximo de emails recibidos
    print("Valor maximo de emails recibidos: ")
    num = emails.max().sum()
    print(num)
    print("\n")

    # valor minimo de emails recibidos
    print("Valor minimo de emails recibidos: ")
    num = emails.min().sum()
    print(num)
    print("\n")

def ejer3(con):
    print("-----------------EJERCICIO 3------------------------")

    permisosUsuario = pd.DataFrame(pd.read_sql("SELECT e.phishing FROM usuarios u join emails e on u.nombre=e.usuario where u.permisos=0", con))
    #print(permisosUsuario)

    permisosAdmin= pd.DataFrame(pd.read_sql("SELECT e.phishing FROM usuarios u join emails e on u.nombre=e.usuario where u.permisos=1", con))
    #print(permisosAdmin)

    CorreosMas200= pd.DataFrame(pd.read_sql("SELECT e.phishing FROM usuarios u join emails e on u.nombre=e.usuario where e.total>=200",con))
    #print(CorreosMas200)

    CorreosMenos200 = pd.DataFrame(pd.read_sql("SELECT e.phishing FROM usuarios u join emails e on u.nombre=e.usuario where e.total < 200", con))
    #print(CorreosMenos200)

    ###reemplazar los NONE por NaN en todos los DataFrames
    permisosUsuario.replace(to_replace=["None"], value=nan, inplace=True)
    permisosAdmin.replace(to_replace=["None"], value=nan, inplace=True)
    CorreosMas200.replace(to_replace=["None"], value=nan, inplace=True)
    CorreosMenos200.replace(to_replace=["None"], value=nan, inplace=True)

    #Numero de observaciones para cada agrupaci??n

    #Usuarios con permiso de usuario 0
    print("El n??mero de observaciones de mail de phising de personas con permisos de usuarios (permiso 0): ")
    num = permisosUsuario.shape[0]
    print(num)
    print("\n")

    # Usuarios con permiso de administrador 1
    print("El n??mero de observaciones de mail de phishing de personas con permisos de administrados (permiso 1): ")
    num = permisosAdmin.shape[0]
    print(num)
    print("\n")

    # Usuarios con total de emails >= 200
    print("El numero de observaciones de mail de phising de usuarios con numero total de emails >= 200 es: ")
    num = CorreosMas200.shape[0]
    print(num)
    print("\n")

    # Usuarios con total de emails < 200
    print("El numero de observaciones de mail de phising de usuarios con numero total de emails < 200 es: ")
    num = CorreosMenos200.shape[0]
    print(num)
    print("\n")


    #Valores missing (entendemos que son los valores missing dentro de la variable phishing que ya se encuentra filtrada en cada dataframe)
    print("El numero de valores missing de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.isna().sum()[0]
    print (num)
    print("\n")

    print("El numero de valores missing de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.isna().sum()[0]
    print(num)
    print("\n")

    print("El numero de valores missing de mail de phising de usuarios con numero total de emails >= 200 es:  ")
    num = CorreosMas200.isna().sum()[0]
    print(num)
    print("\n")

    print("El numero de valores missing de mail de phising de usuarios con numero total de emails < 200 es:  ")
    num = CorreosMenos200.isna().sum()[0]
    print(num)
    print("\n")

    #Mediana

    print("El valor de la mediana de los valores de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.median()[0]
    print(num)
    print("\n")

    print("El valor de la mediana de los valores de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.median()[0]
    print(num)
    print("\n")

    print("El valor de la mediana de los valores de mail de phising de usuarios con numero de emails totales >= 200 : ")
    num = CorreosMas200.median()[0]
    print(num)
    print("\n")

    print("El valor de la mediana de los valores de mail de phising de usuarios con numero de emails totales < 200 : ")
    num = CorreosMenos200.median()[0]
    print(num)
    print("\n")

    #Media
    print("El valor de la media de los valores de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.mean()[0]
    print("%.4f\n" %num)

    print("El valor de la media de los valores de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.mean()[0]
    print("%.4f\n" %num)

    print("El valor de la media de los valores de mail de phising de usuarios con numero de emails totales >= 200 : ")
    num = CorreosMas200.mean()[0]
    print("%.4f\n" %num)

    print("El valor de la media de los valores de mail de phising de usuarios con numero de emails totales < 200 : ")
    num = CorreosMenos200.mean()[0]
    print("%.4f\n" %num)

    #Varianza

    print("El valor de la varianza de los valores de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.var()[0]
    print("%.4f\n" % num)

    print(
        "El valor de la varianza de los valores de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.var()[0]
    print("%.4f\n" % num)

    print("El valor de la varianza de los valores de mail de phising de usuarios con numero de emails totales >= 200 : ")
    num = CorreosMas200.var()[0]
    print("%.4f\n" % num)

    print("El valor de la varianza de los valores de mail de phising de usuarios con numero de emails totales < 200 : ")
    num = CorreosMenos200.var()[0]
    print("%.4f\n" % num)


    #Valores m??ximos
    print("El valor m??ximo de los valores de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.max().sum()
    print(num)
    print("\n")

    print("El valor m??ximo de los valores de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.max().sum()
    print(num)
    print("\n")

    print("El valor m??ximo de los valores de mail de phising de usuarios con numero de emails totales >= 200 : ")
    num = CorreosMas200.max().sum()
    print(num)
    print("\n")

    print("El valor m??ximo de los valores de mail de phising de usuarios con numero de emails totales < 200 : ")
    num = CorreosMenos200.max().sum()
    print(num)
    print("\n")

    #Valores m??nimos
    print("El valor m??nimo de los valores de mail de phising de usuarios con permisos de usuario (permiso 0): ")
    num = permisosUsuario.min().sum()
    print(num)
    print("\n")

    print("El valor m??nimo de los valores de mail de phising de usuarios con permisos de administrador (permiso 1): ")
    num = permisosAdmin.min().sum()
    print(num)
    print("\n")

    print("El valor m??nimo de los valores de mail de phising de usuarios con numero de emails totales >= 200 : ")
    num = CorreosMas200.min().sum()
    print(num)
    print("\n")

    print("El valor m??nimo de los valores de mail de phising de usuarios con numero de emails totales < 200 : ")
    num = CorreosMenos200.min().sum()
    print(num)
    print("\n")



con = sqlite3.connect('database.db')
sql_create_tables(con)
#rellenarTablas(con)
#ejer2(con)
#ejer3(con)
#sql_delete_table(con)
con.close()