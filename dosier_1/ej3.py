import sys
import mysql.connector

def help():
    print("""
          Usage: python3 contacts.py <command>
          Available commands:
            - add <title> <name> <surname> <email>
            - ls [<filter>]
            - update <email> <title> <name> <surname>
            - rm <email>
            - addfriend <email> <friend_email>
            - rmfriend <email> <friend_email>
            - lsfriends <email>
          """)
    
def init():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ej3")
    cursor.execute("USE ej3")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            title VARCHAR(32),
            name VARCHAR(32) NOT NULL,
            surname VARCHAR(32) NOT NULL,
            email VARCHAR(32),
            PRIMARY KEY(email)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS friends (
            src VARCHAR(32),
            target VARCHAR(32),
            PRIMARY KEY (src, target),
            FOREIGN KEY(src) REFERENCES users(email),
            FOREIGN KEY(target) REFERENCES users(email)
        )
    """)
    con.commit()
    cursor.close()
    con.close()

    print("Done")

init()

def addUser(title, name, surname, email):
    con = mysql.connector.connect(user='root', password='root', host='ej3')
    cur = con.cursor()
    cur.execute(f"Insert into users values ({title}, {name}, {surname}, {email})")
    con.commit()
    con.close()

def ls(filter=""):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    query = "SELECT * FROM users"
    if filter:
        query += f" WHERE {filter}"
    cur.execute(query)
    res = cur.fetchall()
    for x in res:
        print(x)
    con.close()

def update(email, title, name, surname):
    con = mysql.connector.connect(user='root', password='root', host='ej3')
    cur = con.cursor()
    cur.execute("UPDATE users SET title=%s, name=%s, surname=%s WHERE email=%s", (title, name, surname, email))
    con.commit()
    con.close()
    print("User updated")

def rm(email):
    con = mysql.connector.connect(user='root', password='root', host='ej3')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    con.commit()
    con.close()
    print("User removed")

def addFriend(email, friend_email):
    con = mysql.connector.connect(user='root', password='root', host='ej3')
    cur = con.cursor()
    cur.execute("INSERT INTO friends VALUES (%s, %s)", (email, friend_email))
    con.commit()
    con.close()

print(sys.argv)

if len(sys.argv) <= 1:
    help()
elif (sys.argv[1] == 'add'):
    addUser(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print('User added')
elif (sys.argv[1] == 'ls'):
    filter = sys.argv[2] if len(sys.argv) > 2 else ""
    ls(filter)
elif (sys.argv[1] == 'update'):
    print('Updating contact')
elif (sys.argv[1] == 'rm'):
    print('Removing contact')
elif (sys.argv[1] == 'addfriend'):
    addFriend(sys.argv[2], sys.argv[3])
elif (sys.argv[1] == 'rmfriend'):
    print('Removing friend')
else:
    help()