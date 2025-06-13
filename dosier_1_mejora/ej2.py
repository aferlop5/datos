# ej2.py corregido
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
          """)

def addUser(title, name, surname, email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej1')
    cur = con.cursor()
    cur.execute("INSERT INTO users (title, name, surname, email) VALUES (%s, %s, %s, %s)", 
                (title, name, surname, email))
    con.commit()
    con.close()

def ls(filter=""):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej1')
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
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej1')
    cur = con.cursor()
    cur.execute("UPDATE users SET title=%s, name=%s, surname=%s WHERE email=%s", 
                (title, name, surname, email))
    con.commit()
    con.close()

def rm(email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej1')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    con.commit()
    con.close()

if len(sys.argv) <= 1:
    help()
elif sys.argv[1] == 'add' and len(sys.argv) == 6:
    addUser(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print('User added')
elif sys.argv[1] == 'ls':
    filter = sys.argv[2] if len(sys.argv) > 2 else ""
    ls(filter)
elif sys.argv[1] == 'update' and len(sys.argv) == 6:
    update(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print('User updated')
elif sys.argv[1] == 'rm' and len(sys.argv) == 3:
    rm(sys.argv[2])
    print('User removed')
else:
    help()