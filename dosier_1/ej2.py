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
    con = mysql.connector.connect(user='root', password='root', host='ej1')
    cur = con.cursor()
    cur.execute(f"Insert into users values ({title}, {name}, {surname}, {email})")
    con.commit()
    con.close()

def ls(filter=""):
    con = mysql.connector.connect(user='root', password='root', host='ej1')
    cur = con.cursor()
    cur.execute(f"select * from users where email "+ filter)
    res = cur.fetchall()
    for x in res:
        print(x)
    con.close()

def update(email, title, name, surname):
    con = mysql.connector.connect(user='root', password='root', host='ej1')
    cur = con.cursor()
    cur.execute("UPDATE users SET title=%s, name=%s, surname=%s WHERE email=%s", (title, name, surname, email))
    con.commit()
    con.close()
    print("User updated")

def rm(email):
    con = mysql.connector.connect(user='root', password='root', host='ej1')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    con.commit()
    con.close()
    print("User removed")

print(sys.argv)

if len(sys.argv) <= 1:
    help()
elif (sys.argv[1] == 'add'):
    addUser(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print('User added')
elif (sys.argv[1] == 'ls'):
    print('Listing contacts')
elif (sys.argv[1] == 'update'):
    print('Updating contact')
elif (sys.argv[1] == 'rm'):
    print('Removing contact')
else:
    help()
