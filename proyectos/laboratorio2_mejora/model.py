import pymongo
from bson.objectid import ObjectId
import time

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter"]

# Inicialización de la base de datos: crea índices
def init():
    db.Users.create_index("email", unique=True)
    db.Users.create_index("nick", unique=True)
    db.Tweets.create_index("user")
    db.Following.create_index([("follower", 1), ("following", 1)], unique=True)
    # Ya no usamos colección Likes independiente
init()

# Helper: valida que el token (user _id) sea válido
def validateToken(token):
    try:
        user = db.Users.find_one({"_id": ObjectId(token)})
    except Exception as e:
        raise Exception("Token inválido")
    if not user:
        raise Exception("Token inválido")
    return user

# Agregar usuario usando ObjectId autogenerado
def addUser(user):
    required = ["name", "surname", "email", "password", "nick"]
    for field in required:
        if field not in user:
            raise Exception(f"Missing {field}")
    if type(user) != dict:
        raise Exception("Incorrect parameter")

    try:
        res = db.Users.insert_one(user)
    except pymongo.errors.DuplicateKeyError:
        raise Exception("User already exists")
    user["_id"] = res.inserted_id
    # Devolvemos el token como string del _id
    user["id"] = str(res.inserted_id)
    return user

def login(email, passwd):
    print(f"Attempting login with email: {email}, password: {passwd}")
    user = db.Users.find_one({"email": email, "password": passwd})
    if not user:
        raise Exception("Wrong authentication")
    return str(user["_id"])

def updateUser(token, new_data):
    validateToken(token)
    update_fields = {key: new_data[key] for key in ["name", "surname", "email", "password", "nick"] if key in new_data}
    if not update_fields:
        raise Exception("No data to update")
    result = db.Users.update_one({"_id": ObjectId(token)}, {"$set": update_fields})
    if result.matched_count == 0:
        raise Exception("User not found")
    return db.Users.find_one({"_id": ObjectId(token)}, {"_id": 0})

# Eliminar usuario y limpiar la BD (tweets, relaciones)
def removeUser(token):
    validateToken(token)
    res = db.Users.delete_one({"_id": ObjectId(token)})
    if res.deleted_count == 0:
        raise Exception("User not found")
    # Limpia tweets del usuario
    db.Tweets.delete_many({"user": token})
    # Limpia relaciones de Following en las que aparezca
    db.Following.delete_many({"$or": [{"follower": token}, {"following": token}]})
    return True

# listUsers ahora admite paginación (ini, count) y ordenación (opcional)
def listUsers(token, query="", ini=0, count=10, sort=None):
    validateToken(token)
    query_filter = eval(query) if query else {}
    cursor = db.Users.find(query_filter, {"password": 0})
    if sort:
        # sort debe ser una lista de tuplas, ej: [("name", 1)]
        cursor = cursor.sort(sort)
    users = list(cursor.skip(ini).limit(count))
    return users

def listFollowing(token, query="", ini=0, count=10, sort=None):
    validateToken(token)
    query_filter = eval(query) if query else {}
    following_docs = db.Following.find({"follower": token}, {"following": 1})
    following_ids = [doc["following"] for doc in following_docs]
    query_filter.update({"_id": {"$in": [ObjectId(uid) for uid in following_ids]}})
    cursor = db.Users.find(query_filter, {"password": 0})
    if sort:
        cursor = cursor.sort(sort)
    users = list(cursor.skip(ini).limit(count))
    return users

def listFollowers(token, query="", ini=0, count=10, sort=None):
    validateToken(token)
    query_filter = eval(query) if query else {}
    follower_docs = db.Following.find({"following": token}, {"follower": 1})
    follower_ids = [doc["follower"] for doc in follower_docs]
    query_filter.update({"_id": {"$in": [ObjectId(uid) for uid in follower_ids]}})
    cursor = db.Users.find(query_filter, {"password": 0})
    if sort:
        cursor = cursor.sort(sort)
    users = list(cursor.skip(ini).limit(count))
    return users

def follow(token, nick):
    validateToken(token)
    user_to_follow = db.Users.find_one({"nick": nick})
    if not user_to_follow:
        raise Exception("User to follow not found")
    if str(user_to_follow["_id"]) == token:
        raise Exception("Cannot follow yourself")
    try:
        db.Following.insert_one({"follower": token, "following": str(user_to_follow["_id"])})
    except pymongo.errors.DuplicateKeyError:
        raise Exception("Already following")
    return True

def unfollow(token, nick):
    validateToken(token)
    user_to_unfollow = db.Users.find_one({"nick": nick})
    if not user_to_unfollow:
        raise Exception("User to unfollow not found")
    result = db.Following.delete_one({"follower": token, "following": str(user_to_unfollow["_id"])})
    if result.deleted_count == 0:
        raise Exception("Not following this user")
    return True

# Se aprovecha la capacidad embebida en Tweets: se agregan arrays para likes/deslikes
def addTweet(token, content):
    validateToken(token)
    tweet = {
        "type": "tweet",
        "date": int(time.time()),
        "content": content,
        "user": token,
        "ref": None,
        "likes": [],
        "dislikes": []
    }
    res = db.Tweets.insert_one(tweet)
    tweet["_id"] = res.inserted_id
    tweet["id"] = str(res.inserted_id)
    return tweet

def addRetweet(token, tweetId):
    validateToken(token)
    original_tweet = db.Tweets.find_one({"_id": ObjectId(tweetId)})
    if not original_tweet:
        raise Exception("Original tweet not found")
    retweet = {
        "type": "retweet",
        "date": int(time.time()),
        "content": original_tweet["content"],
        "user": token,
        "ref": tweetId,
        "likes": [],
        "dislikes": []
    }
    res = db.Tweets.insert_one(retweet)
    retweet["_id"] = res.inserted_id
    retweet["id"] = str(res.inserted_id)
    return retweet

def listTweets(token, query="", ini=0, count=10, sort=None):
    validateToken(token)
    # Se obtienen los ids de los que se sigue, incluyendo al propio
    following_docs = db.Following.find({"follower": token}, {"following": 1})
    following_ids = [doc["following"] for doc in following_docs] + [token]
    query_filter = {"user": {"$in": following_ids}}
    if query:
        query_filter.update(eval(query))
    cursor = db.Tweets.find(query_filter, {"_id": 0})
    if sort:
        cursor = cursor.sort(sort)
    tweets = list(cursor.skip(ini).limit(count))
    # Los likes/dislikes ya están embebidos en cada tweet
    return tweets

# Actualiza likes/deslikes directamente en el documento tweet
def like(token, tweetId):
    validateToken(token)
    tweet = db.Tweets.find_one({"_id": ObjectId(tweetId)})
    if not tweet:
        raise Exception("Tweet not found")
    if token in tweet.get("likes", []):
        raise Exception("You have already liked this tweet")
    # Si estaba en dislikes, lo quitamos
    if token in tweet.get("dislikes", []):
        db.Tweets.update_one({"_id": ObjectId(tweetId)}, {"$pull": {"dislikes": token}})
    db.Tweets.update_one({"_id": ObjectId(tweetId)}, {"$push": {"likes": token}})
    return True

def dislike(token, tweetId):
    validateToken(token)
    tweet = db.Tweets.find_one({"_id": ObjectId(tweetId)})
    if not tweet:
        raise Exception("Tweet not found")
    if token in tweet.get("dislikes", []):
        raise Exception("You have already disliked this tweet")
    # Si estaba en likes, lo quitamos
    if token in tweet.get("likes", []):
        db.Tweets.update_one({"_id": ObjectId(tweetId)}, {"$pull": {"likes": token}})
    db.Tweets.update_one({"_id": ObjectId(tweetId)}, {"$push": {"dislikes": token}})
    return True

def listLikes(token, tweetId, ini=0, count=10):
    validateToken(token)
    tweet = db.Tweets.find_one({"_id": ObjectId(tweetId)})
    if not tweet:
        raise Exception("Tweet not found")
    user_ids = tweet.get("likes", [])[ini:ini+count]
    # Convertimos cada token (string) a ObjectId para la consulta
    users = list(db.Users.find({"_id": {"$in": [ObjectId(uid) for uid in user_ids]}}, {"password": 0}))
    return users

def listDislikes(token, tweetId, ini=0, count=10):
    validateToken(token)
    tweet = db.Tweets.find_one({"_id": ObjectId(tweetId)})
    if not tweet:
        raise Exception("Tweet not found")
    user_ids = tweet.get("dislikes", [])[ini:ini+count]
    users = list(db.Users.find({"_id": {"$in": [ObjectId(uid) for uid in user_ids]}}, {"password": 0}))
    return users