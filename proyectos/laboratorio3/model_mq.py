import pika
import json

def publish_message(msg, routing_key="default"):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Se utiliza un exchange de tipo direct para un enrutamiento específico
    channel.exchange_declare(exchange='twitter-exchange', exchange_type='direct', durable=False)
    channel.basic_publish(exchange='twitter-exchange', routing_key=routing_key, body=json.dumps(msg))
    connection.close()

def addUser(user):
    msg = {"type": "addUser", "data": user}
    publish_message(msg, routing_key="user")

def updateUser(token, new_data):
    msg = {"type": "updateUser", "token": token, "data": new_data}
    publish_message(msg, routing_key="user")

def removeUser(token):
    msg = {"type": "removeUser", "data": token}
    publish_message(msg, routing_key="user")

def follow(token, nick):
    msg = {"type": "follow", "data": {"token": token, "nick": nick}}
    publish_message(msg, routing_key="user")

def unfollow(token, nick):
    msg = {"type": "unfollow", "data": {"token": token, "nick": nick}}
    publish_message(msg, routing_key="user")

def addTweet(token, content):
    msg = {"type": "addTweet", "data": {"token": token, "content": content}}
    publish_message(msg, routing_key="tweet")

def addRetweet(token, tweetId):
    msg = {"type": "addRetweet", "data": {"token": token, "tweetId": tweetId}}
    publish_message(msg, routing_key="tweet")

def like(token, tweetId):
    msg = {"type": "like", "data": {"token": token, "tweetId": tweetId}}
    publish_message(msg, routing_key="tweet")

def dislike(token, tweetId):
    msg = {"type": "dislike", "data": {"token": token, "tweetId": tweetId}}
    publish_message(msg, routing_key="tweet")