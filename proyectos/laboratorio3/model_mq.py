import pika
import json
def addUser(user): 
	msg = {"type": "addUser", "data": user}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout',
		durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='',
		body=json.dumps(msg))
	connection.close()
def updateUser(token, user): 
	msg = {"type": "updateUser", "token": token, "data": user}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange',exchange_type='fanout',
		durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='',
		body=json.dumps(msg))
	connection.close()
def removeUser(token):
	msg = {"type": "removeUser", "data": token}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def follow(token, nick):
	msg = {"type": "follow", "data": {"token": token, "nick": nick}}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def unfollow(token, nick):
	msg = {"type": "unfollow", "data": {"token": token, "nick": nick}}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def addTweet(tweet):
	msg = {"type": "addTweet", "data": tweet}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def addRetweet(tweet):
	msg = {"type": "addRetweet", "data": tweet}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def like(tweet):
	msg = {"type": "like", "data": tweet}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()
def dislike(tweet):
	msg = {"type": "dislike", "data": tweet}
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
	channel.basic_publish(exchange='twitter-exchange', routing_key='', body=json.dumps(msg))
	connection.close()