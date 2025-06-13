import pymongo
import uuid
import time

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter"]

# Inicialización de la base de datos
def init():
    db.Users.create_index("email", unique=True)
    db.Users.create_index("nick", unique=True)
    db.Tweets.create_index("user")
    db.Following.create_index([("follower", 1), ("following", 1)], unique=True)
    db.Likes.create_index([("user", 1), ("tweet", 1)], unique=True)

init()

def addUser(user):
    required = ["name", "surname", "email", "password", "nick"]
    for field in required:
        if field not in user:
            raise Exception(f"Missing {field}")
    if type(user) != dict:
        raise Exception("Incorrect parameter")
    user["id"] = str(uuid.uuid4())  # Usar UUID string
    try:
        db.Users.insert_one(user)
    except pymongo.errors.DuplicateKeyError:
        raise Exception("User already exists")
    return user

def login(email, passwd):
    print(f"Attempting login with email: {email}, password: {passwd}")
    user = db.Users.find_one({"email": email, "password": passwd})
    if not user:
        raise Exception("Wrong authentication")
    return user["id"]

def updateUser(token, new_data):
    update_fields = {key: new_data[key] for key in ["name", "surname", "email", "password", "nick"] if key in new_data}
    if not update_fields:
        raise Exception("No data to update")
    result = db.Users.update_one({"id": token}, {"$set": update_fields})
    if result.matched_count == 0:
        raise Exception("User not found")
    return db.Users.find_one({"id": token}, {"_id": 0})

def removeUser(token):
    result = db.Users.delete_one({"id": token})
    if result.deleted_count == 0:
        raise Exception("User not found")
    return True

def listUsers(token, query=""):
    query_filter = eval(query) if query else {}
    users = list(db.Users.find(query_filter, {"_id": 0, "password": 0}))
    return users

def listFollowing(token, query="", ini=0, count=10, sort=""):
    query_filter = eval(query) if query else {}
    following_ids = db.Following.find({"follower": token}, {"following": 1})
    following_ids = [f["following"] for f in following_ids]
    query_filter.update({"id": {"$in": following_ids}})
    users = list(db.Users.find(query_filter, {"_id": 0}).skip(ini).limit(count))
    return users

def listFollowers(token, query="", ini=0, count=10, sort=""):
    query_filter = eval(query) if query else {}
    follower_ids = db.Following.find({"following": token}, {"follower": 1})
    follower_ids = [f["follower"] for f in follower_ids]
    query_filter.update({"id": {"$in": follower_ids}})
    users = list(db.Users.find(query_filter, {"_id": 0}).skip(ini).limit(count))
    return users

def follow(token, nick):
    user_to_follow = db.Users.find_one({"nick": nick})
    if not user_to_follow:
        raise Exception("User to follow not found")
    if user_to_follow["id"] == token:
        raise Exception("Cannot follow yourself")
    try:
        db.Following.insert_one({"follower": token, "following": user_to_follow["id"]})
    except pymongo.errors.DuplicateKeyError:
        raise Exception("Already following")
    return True

def unfollow(token, nick):
    user_to_unfollow = db.Users.find_one({"nick": nick})
    if not user_to_unfollow:
        raise Exception("User to unfollow not found")
    result = db.Following.delete_one({"follower": token, "following": user_to_unfollow["id"]})
    if result.deleted_count == 0:
        raise Exception("Not following this user")
    return True

def addTweet(token, content):
    tweet = {
        "id": str(uuid.uuid4()),  # UUID como string para serialización
        "type": "tweet",
        "date": int(time.time()),
        "content": content,
        "user": token,
        "ref": None
    }
    db.Tweets.insert_one(tweet)
    return tweet

def addRetweet(token, tweetId):
    original_tweet = db.Tweets.find_one({"id": tweetId})
    if not original_tweet:
        raise Exception("Original tweet not found")
    retweet = {
        "id": uuid.uuid4().hex,
        "type": "retweet",
        "date": int(time.time()),
        "content": original_tweet["content"],
        "user": token,
        "ref": tweetId
    }
    db.Tweets.insert_one(retweet)
    return retweet

def listTweets(token, query="", ini=0, count=10, sort=""):
    following_ids = db.Following.find({"follower": token}, {"following": 1})
    following_ids = [f["following"] for f in following_ids] + [token]
    query_filter = {"user": {"$in": following_ids}}
    if query:
        query_filter.update(eval(query))
    tweets = list(db.Tweets.find(query_filter, {"_id": 0}).skip(ini).limit(count))
    for tweet in tweets:
        tweet["likes"] = db.Likes.count_documents({"tweet": tweet["id"], "positive": 1})
        tweet["dislikes"] = db.Likes.count_documents({"tweet": tweet["id"], "positive": 0})
    return tweets

def like(token, tweetId):
    if db.Likes.find_one({"user": token, "tweet": tweetId}):
        raise Exception("You have already rated this tweet")
    db.Likes.insert_one({"user": token, "tweet": tweetId, "positive": 1})
    return True

def dislike(token, tweetId):
    if db.Likes.find_one({"user": token, "tweet": tweetId}):
        raise Exception("You have already rated this tweet")
    db.Likes.insert_one({"user": token, "tweet": tweetId, "positive": 0})
    return True

def listLikes(token, tweetId, ini=0, count=10):
    user_ids = db.Likes.find({"tweet": tweetId, "positive": 1}, {"user": 1}).skip(ini).limit(count)
    user_ids = [u["user"] for u in user_ids]
    users = list(db.Users.find({"id": {"$in": user_ids}}, {"_id": 0}))
    return users

def listDislikes(token, tweetId, ini=0, count=10):
    user_ids = db.Likes.find({"tweet": tweetId, "positive": 0}, {"user": 1}).skip(ini).limit(count)
    user_ids = [u["user"] for u in user_ids]
    users = list(db.Users.find({"id": {"$in": user_ids}}, {"_id": 0}))
    return users