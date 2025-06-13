# ej3.py corregido
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
            FOREIGN KEY(src) REFERENCES users(email) ON DELETE CASCADE,
            FOREIGN KEY(target) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    con.commit()
    cursor.close()
    con.close()

init()

def addUser(title, name, surname, email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("INSERT INTO users (title, name, surname, email) VALUES (%s, %s, %s, %s)", 
                (title, name, surname, email))
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
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("UPDATE users SET title=%s, name=%s, surname=%s WHERE email=%s", 
                (title, name, surname, email))
    con.commit()
    con.close()

def rm(email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE email=%s", (email,))
    con.commit()
    con.close()

def addFriend(email, friend_email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("INSERT INTO friends (src, target) VALUES (%s, %s)", (email, friend_email))
    con.commit()
    con.close()

def rmFriend(email, friend_email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("DELETE FROM friends WHERE src=%s AND target=%s", (email, friend_email))
    con.commit()
    con.close()

def lsFriends(email):
    con = mysql.connector.connect(user='root', password='root', host='localhost', database='ej3')
    cur = con.cursor()
    cur.execute("""
        SELECT u.* 
        FROM friends f
        JOIN users u ON f.target = u.email
        WHERE f.src = %s
    """, (email,))
    friends = cur.fetchall()
    for friend in friends:
        print(friend)
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
elif sys.argv[1] == 'addfriend' and len(sys.argv) == 4:
    addFriend(sys.argv[2], sys.argv[3])
    print('Friend added')
elif sys.argv[1] == 'rmfriend' and len(sys.argv) == 4:
    rmFriend(sys.argv[2], sys.argv[3])
    print('Friend removed')
elif sys.argv[1] == 'lsfriends' and len(sys.argv) == 3:
    lsFriends(sys.argv[2])
else:
    help()