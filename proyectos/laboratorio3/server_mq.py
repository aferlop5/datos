import pika
import json
 
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='twitter-exchange', exchange_type='fanout', durable=False)
channel.queue_declare(queue='twitter-queue', durable=False)
channel.queue_bind(exchange='twitter-exchange', queue='twitter-queue', routing_key='')

def callback(ch, method, properties, body):
    print(f"Received: {body}")
    msg = json.loads(body)
    if msg['type'] == 'addUser': 
        print('add user')
        try:
            model.addUser(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'updateUser': 
        print('update user')
        try:
            model.updateUser(msg['token', msg['data']])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'removeUser':
        print('remove user')
        try:
            model.removeUser(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'follow':
        print('follow')
        try:
            model.followUser(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'unfollow':
        print('unfollow')
        try:
            model.unfollowUser(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'addTweet':
        print('add tweet')
        try:
            model.addTweet(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'addRetweet':
        print('add retweet')
        try:
            model.addRetweet(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'like':
        print('like')
        try:
            model.like(msg['data'])
        except Exception as exc:
            print(exc)
    elif msg['type'] == 'dislike':
        print('dislike')
        try:
            model.dislike(msg['data'])
        except Exception as exc:
            print(exc)
    else: pass

channel.basic_consume(queue='twitter-queue', on_message_callback=callback,
 auto_ack=True)
channel.start_consuming()