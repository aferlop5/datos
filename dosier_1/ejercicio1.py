import mysql.connector

con = mysql.connector.connect(user="root", password="root")
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS ej1")
cur.execute("USE ej1")
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        title VARCHAR(50),
        name VARCHAR(32),
        surname VARCHAR(32),
        email VARCHAR(32)
    )
""")
con.commit()
con.close()
print("Base de datos creada")
