import sqlite3

import json




def rellenartablas(con):

    #abrir json
    with open("users.json", "r") as f:
        users_data = json.load(f)

    with open("legal.json", "r") as f1:
        legal_data = json.load(f1)




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
    cursorObj.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre text primary key, telefono integer, contrasena text, provincia text, permisos boolean, email text, fechas text, ips text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS emails (usuario text primary key, total integer, phising integer, cliclados integer, FOREIGN KEY ('usuario') REFERENCES usuarios (nombre) )")

    cursorObj.execute("CREATE TABLE IF NOT EXISTS legal (url text primary key, cookies real, aviso real, proteccion_de_datos real, creacion real)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS fechas (idfechas integer primary key autoincrement, fecha text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS FechasDeUsuarios (idfechas integer primary key autoincrement, fechasdeusua text, usuario text, FOREIGN KEY ('usuario') references usuarios(nombre), FOREIGN KEY ('fechasdeusua') references fechas(fecha))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS ips(idips integer primary key autoincrement, ip text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS IpsDeUsuarios ( idips integer primary key autoincrement, ipdeusua text, usuario text, FOREIGN KEY ('usuario') references usuarios(nombre), FOREIGN KEY ('ipdeusua') REFERENCES usuarios (nombre))")
    cursorObj.execute("INSERT INTO legal VALUES ('X', '4', '1', '3', '5')")
    #sql_delete_table(con)

    con.commit()



con = sqlite3.connect('database.db')
sql_create_tables(con)
#sql_fetch(con)
#sql_update(con)
#sql_fetch(con)
#sql_delete(con)
#sql_fetch(con)
#sql_delete_table(con)
con.close()