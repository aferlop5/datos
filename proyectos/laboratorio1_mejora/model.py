import mysql.connector
import uuid
import time

def init():
    con = mysql.connector.connect(user="root", password="root")
    cur = con.cursor()
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS twitter")
        cur.execute("USE twitter")
        cur.execute("""CREATE TABLE IF NOT EXISTS Users(
            id CHAR(32) PRIMARY KEY,
            name CHAR(32) NOT NULL,
            surname CHAR(32) NOT NULL,
            email CHAR(32) NOT NULL UNIQUE,
            password CHAR(32) NOT NULL,
            nick CHAR(32) NOT NULL UNIQUE
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Tweets(
            id CHAR(32) PRIMARY KEY,
            type CHAR(32),
            date INT,
            content TEXT,
            user CHAR(32) NOT NULL,
            ref CHAR(32),
            FOREIGN KEY (user) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (ref) REFERENCES Tweets(id) ON DELETE SET NULL
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Following(
            follower CHAR(32),
            following CHAR(32),
            PRIMARY KEY(follower, following),
            FOREIGN KEY(follower) REFERENCES Users(id),
            FOREIGN KEY(following) REFERENCES Users(id)
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS Likes(
            user CHAR(32),
            tweet CHAR(32),
            positive INT,
            PRIMARY KEY(user, tweet),
            FOREIGN KEY(user) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY(tweet) REFERENCES Tweets(id) ON DELETE CASCADE
        )""")
        con.commit()
    except Exception as e:
        print(e)
        print("Database already exists.")
    finally:
        con.close()

init()

def addUser(user):
    required = ["name", "surname", "email", "password", "nick"]
    for field in required:
        if field not in user:
            raise Exception(f"Missing {field}")
    if type(user) != dict:
        raise Exception("Incorrect parameter")

    user["id"] = uuid.uuid4().hex
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Users WHERE email='{user['email']}' OR nick='{user['nick']}'")
        if cur.fetchone() is not None:
            raise Exception("User already exists")
        cur.execute(f"INSERT INTO Users VALUES('{user['id']}', '{user['name']}', '{user['surname']}', '{user['email']}', '{user['password']}', '{user['nick']}')")
        con.commit()
    finally:
        con.close()
    return user

def login(email, passwd):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Users WHERE email='{email}' AND password='{passwd}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("Wrong authentication")
    finally:
        con.close()
    return row[0]

def validateToken(token):
    """Validates if the token corresponds to an existing user."""
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM Users WHERE id='{token}'")
        if cur.fetchone() is None:
            raise Exception("Invalid token")
    finally:
        con.close()

# Nueva función para verificar si el usuario tiene permiso de acceso al tweet
def canAccessTweet(token, tweetId):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT user FROM Tweets WHERE id='{tweetId}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("Tweet not found")
        tweet_owner = row[0]
        if tweet_owner == token:
            return True
        # Comprueba que token sigue al usuario del tweet
        cur.execute(f"SELECT * FROM Following WHERE follower='{token}' AND following='{tweet_owner}'")
        if cur.fetchone() is None:
            raise Exception("No tienes permiso para retwittear contenido de este usuario")
    finally:
        con.close()
    return True


def updateUser(token, new_data):
    validateToken(token)   # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        updates = []
        for key in ["name", "surname", "email", "password", "nick"]:
            if key in new_data:
                updates.append(f"{key}='{new_data[key]}'")
        if not updates:
            raise Exception("No data to update")
        sql = f"UPDATE Users SET {', '.join(updates)} WHERE id='{token}'"
        cur.execute(sql)
        con.commit()
        cur.execute(f"SELECT * FROM Users WHERE id='{token}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("User not found")
        user = {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "nick": row[5]
        }
    finally:
        con.close()
    return user


def removeUser(token):
    validateToken(token)   # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"DELETE FROM Users WHERE id='{token}'")
        con.commit()
    finally:
        con.close()
    return True


def addTweet(token, content):
    validateToken(token)   # Se añade validación de token
    tweet_id = uuid.uuid4().hex
    current_time = int(time.time())
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"INSERT INTO Tweets VALUES('{tweet_id}', 'tweet', {current_time}, '{content}', '{token}', NULL)")
        con.commit()
        return {"id": tweet_id, "type": "tweet", "date": current_time, "content": content, "user": token, "ref": None}
    finally:
        con.close()


def addRetweet(token, tweetId):
    validateToken(token)                   # Se añade validación de token
    canAccessTweet(token, tweetId)           # Comprueba que el usuario puede acceder al tweet original
    tweet_id = uuid.uuid4().hex
    current_time = int(time.time())
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT content FROM Tweets WHERE id='{tweetId}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("Original tweet not found")
        original_content = row[0]
        cur.execute(f"INSERT INTO Tweets VALUES('{tweet_id}', 'retweet', {current_time}, '{original_content}', '{token}', '{tweetId}')")
        con.commit()
        return {"id": tweet_id, "type": "retweet", "date": current_time, "content": original_content, "user": token, "ref": tweetId}
    finally:
        con.close()


def follow(token, nick):
    validateToken(token)  # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM Users WHERE nick='{nick}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("User to follow not found")
        following_id = row[0]
        if following_id == token:
            raise Exception("Cannot follow yourself")
        cur.execute(f"SELECT * FROM Following WHERE follower='{token}' AND following='{following_id}'")
        if cur.fetchone() is not None:
            raise Exception("Already following")
        cur.execute(f"INSERT INTO Following VALUES('{token}', '{following_id}')")
        con.commit()
    finally:
        con.close()
    return True


def unfollow(token, nick):
    validateToken(token)  # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM Users WHERE nick='{nick}'")
        row = cur.fetchone()
        if row is None:
            raise Exception("User to unfollow not found")
        following_id = row[0]
        cur.execute(f"DELETE FROM Following WHERE follower='{token}' AND following='{following_id}'")
        con.commit()
    finally:
        con.close()
    return True


def like(token, tweetId):
    validateToken(token)  # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Likes WHERE user='{token}' AND tweet='{tweetId}'")
        if cur.fetchone() is not None:
            raise Exception("You have already rated this tweet")
        cur.execute(f"INSERT INTO Likes VALUES('{token}', '{tweetId}', 1)")
        con.commit()
    finally:
        con.close()
    return True


def dislike(token, tweetId):
    validateToken(token)  # Se añade validación de token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Likes WHERE user='{token}' AND tweet='{tweetId}'")
        if cur.fetchone() is not None:
            raise Exception("You have already rated this tweet")
        cur.execute(f"INSERT INTO Likes VALUES('{token}', '{tweetId}', 0)")
        con.commit()
    finally:
        con.close()
    return True

def listUsers(token, query=""):
    validateToken(token)  # Validate token
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    users = []
    try:
        cur = con.cursor()
        sql = "SELECT id, name, surname, email, nick FROM Users"
        if query:
            sql += f" WHERE name LIKE '%{query}%' OR surname LIKE '%{query}%' OR nick LIKE '%{query}%'"
        cur.execute(sql)
        for row in cur.fetchall():
            users.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "email": row[3],
                "nick": row[4]
            })
    finally:
        con.close()
    return users

def listFollowing(token, query="", ini=0, count=10, sort=""):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    users = []
    try:
        cur = con.cursor()
        sql = f"""SELECT U.id, U.name, U.surname, U.email, U.nick FROM Users U
                  INNER JOIN Following F ON U.id = F.following
                  WHERE F.follower='{token}'"""
        if query and len(query) > 0:
            sql += f" AND {query}"
        if sort:
            sql += f" ORDER BY {sort}"
        sql += f" LIMIT {ini}, {count}"
        cur.execute(sql)
        for row in cur.fetchall():
            users.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "email": row[3],
                "nick": row[4]
            })
    finally:
        con.close()
    return users

def listFollowers(token, query="", ini=0, count=10, sort=""):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    users = []
    try:
        cur = con.cursor()
        sql = f"""SELECT U.id, U.name, U.surname, U.email, U.nick FROM Users U
                  INNER JOIN Following F ON U.id = F.follower
                  WHERE F.following='{token}'"""
        if query and len(query) > 0:
            sql += f" AND {query}"
        if sort:
            sql += f" ORDER BY {sort}"
        sql += f" LIMIT {ini}, {count}"
        cur.execute(sql)
        for row in cur.fetchall():
            users.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "email": row[3],
                "nick": row[4]
            })
    finally:
        con.close()
    return users

def listTweets(token, query="", ini=0, count=10, sort=""):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    tweets = []
    try:
        cur = con.cursor()
        cur.execute(f"SELECT following FROM Following WHERE follower='{token}'")
        following = [token]  
        following.extend([row[0] for row in cur.fetchall()])
        following_list = "', '".join(following)
        sql = f"SELECT * FROM Tweets WHERE user IN ('{following_list}')"
        if query and len(query)>0:
            sql += f" AND {query}"
        if sort:
            sql += f" ORDER BY {sort}"
        sql += f" LIMIT {ini}, {count}"
        cur.execute(sql)
        for row in cur.fetchall():
            tweet = {
                "id": row[0],
                "type": row[1],
                "date": row[2],
                "content": row[3],
                "user": row[4],
                "ref": row[5]
            }
            cur.execute(f"SELECT COUNT(*) FROM Likes WHERE tweet='{row[0]}' AND positive=1")
            likes = cur.fetchone()[0]
            cur.execute(f"SELECT COUNT(*) FROM Likes WHERE tweet='{row[0]}' AND positive=0")
            dislikes = cur.fetchone()[0]
            tweet["likes"] = likes
            tweet["dislikes"] = dislikes
            tweets.append(tweet)
    finally:
        con.close()
    return tweets

def listLikes(token, tweetId, ini=0, count=10):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    users = []
    try:
        cur = con.cursor()
        sql = f"""SELECT U.id, U.name, U.surname, U.nick FROM Users U
                  INNER JOIN Likes L ON U.id = L.user
                  WHERE L.tweet='{tweetId}' AND L.positive=1
                  LIMIT {ini}, {count}"""
        cur.execute(sql)
        for row in cur.fetchall():
            users.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "nick": row[3]
            })
    finally:
        con.close()
    return users

def listDislikes(token, tweetId, ini=0, count=10):
    con = mysql.connector.connect(user="root", password="root", database="twitter")
    users = []
    try:
        cur = con.cursor()
        sql = f"""SELECT U.id, U.name, U.surname, U.nick FROM Users U
                  INNER JOIN Likes L ON U.id = L.user
                  WHERE L.tweet='{tweetId}' AND L.positive=0
                  LIMIT {ini}, {count}"""
        cur.execute(sql)
        for row in cur.fetchall():
            users.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "nick": row[3]
            })
    finally:
        con.close()
    return users
