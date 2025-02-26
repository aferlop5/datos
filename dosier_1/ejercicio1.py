import mysql.connector

con=mysql.connector.connect(user="root",password="root")
cur=con.cursor()
cur.execute("create database ej1")
cur.execute("use ej1")
cur.execute("create table users(title varchar(50), name varchar(32), surname varchar(32), email varchar(32)")
cur.commit()
con.close()
print("Base de datos creada")