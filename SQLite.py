import sqlite3

import json
import pandas as pd




def rellenarTablas(con):
    #abrir json
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




def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE usuarios SET nombre = "Sergio" where dni = "X"')
    con.commit()

def sql_fetch(con):
   cursorObj = con.cursor()
   cursorObj.execute('SELECT * FROM usuarios')
   #SELECT dni, nombre FROM usuarios WHERE altura > 1.0
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM usuarios where dni = "X"')
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
    cursorObj.execute("CREATE TABLE IF NOT EXISTS emails (usuario text primary key, total integer, phising integer, cliclados integer, FOREIGN KEY ('usuario') REFERENCES usuarios (nombre) )")

    cursorObj.execute("CREATE TABLE IF NOT EXISTS legal (url text primary key, cookies integer, aviso integer, proteccion_de_datos integer, creacion integer)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS fechas (idfechas integer primary key autoincrement, fecha text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS FechasDeUsuarios (idfechas integer primary key autoincrement, fechasdeusua text, usuario integer, FOREIGN KEY ('usuario') references usuarios(fechas), FOREIGN KEY ('fechasdeusua') references fechas(fecha))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS ips(idips integer primary key autoincrement, ip text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS IpsDeUsuarios ( idips integer primary key autoincrement, ipdeusua text, usuario integer, FOREIGN KEY ('usuario') references usuarios(ips), FOREIGN KEY ('ipdeusua') REFERENCES ips (ip))")


    #sql_delete_table(con)

    con.commit()

def ejer2(con):
    #contar numero de muestras de usuarios
    print("El numero de muestras de usuarios es: ")
    muestrasUsuarios = pd.DataFrame(pd.read_sql("SELECT nombre FROM usuarios", con))
    num=muestrasUsuarios.count().sum()
    print(num)

    #contar numero de muestras de urls
    print("\n")
    print("El numero de muestras de urls es: ")
    muestrasUrls = pd.DataFrame(pd.read_sql("SELECT url FROM legal", con))
    num = muestrasUrls.count().sum()
    print(num)
    print("\n")

    #media de inicios de sesion por fecha
    fechasParaMedia= pd.DataFrame(pd.read_sql("SELECT * FROM FechasDeUsuarios",con),columns=["usuario","fechasdeusua"])
    #print(fechasParaMedia)

    print("Media de inicios de sesion por fecha: ")
    num = fechasParaMedia.groupby('usuario').count().mean(numeric_only=True)[0]
    print("%.4f\n" %num)

    #Desviación estandar de inicios de sesión por fecha
    

con = sqlite3.connect('database.db')
sql_create_tables(con)
#rellenarTablas(con)
ejer2(con)
#sql_fetch(con)
#sql_update(con)
#sql_fetch(con)
#sql_delete(con)
#sql_fetch(con)
#sql_delete_table(con)
con.close()