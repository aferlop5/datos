import mysql.connector

try:
    con = mysql.connector.connect(
        user="root",
        password="Agustife2005",
        host="127.0.0.1"
    )

    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS ej1")
    print("Base de datos creada o ya existente")

    cur.execute("USE ej1")

    cur.execute("CREATE TABLE IF NOT EXISTS users(title VARCHAR(50), name VARCHAR(32), surname VARCHAR(32), email VARCHAR(32))")
    print("Tabla creada correctamente")

    con.commit()  # Aquí es con la conexión, no con el cursor
    print("Cambios guardados")

except mysql.connector.Error as e:
    print("❌ Error de conexión:", e)

finally:
    if con.is_connected():
        cur.close()
        con.close()
        print("🔌 Conexión cerrada")

