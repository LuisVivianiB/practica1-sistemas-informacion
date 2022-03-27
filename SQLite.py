import sqlite3

import json


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

    con.commit()

def sql_create_tables(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS emails (usuario text primary key, total integer, phising integer, cliclados integer, FOREIGN KEY ('usuario') REFERENCES usuarios (nombre) )")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre text primary key, telefono integer, contrasena text, provincia text, permisos boolean, email text, fechas text, ips text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS legal (url text primary key, cookies real, aviso real, proteccion_de_datos real, creacion real)")
    #cursorObj.execute("CREATE TABLE IF NOT EXISTS fechas ()
    #cursorObj.execute("INSERT INTO usuarios VALUES ('X', 'isaac', '1.85') ")
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