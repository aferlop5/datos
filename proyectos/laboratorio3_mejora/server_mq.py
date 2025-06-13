import pika
import json
import model  # Se utiliza la API de model (operaciones directas a la BD)

def validate_token(token):
    # Validación simple: se comprueba que exista un usuario con id == token.
    user = model.db.Users.find_one({"id": token})
    return bool(user)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# Se declara un exchange direct y se crean colas específicas para "user" y "tweet"
channel.exchange_declare(exchange='twitter-exchange', exchange_type='direct', durable=False)
channel.queue_declare(queue='user_queue', durable=False)
channel.queue_declare(queue='tweet_queue', durable=False)
channel.queue_bind(exchange='twitter-exchange', queue='user_queue', routing_key='user')
channel.queue_bind(exchange='twitter-exchange', queue='tweet_queue', routing_key='tweet')

def callback(ch, method, properties, body):
    print(f"Received: {body}")
    msg = json.loads(body)
    try:
        tipo = msg.get('type')
        # Operaciones sensibles que requieren token válido
        operaciones_sensibles = ['updateUser', 'removeUser', 'follow', 'unfollow', 'addTweet', 'addRetweet', 'like', 'dislike']
        if tipo in operaciones_sensibles:
            token_to_check = msg.get('data', {}).get('token')
            if not token_to_check or not validate_token(token_to_check):
                print("ERROR: Token inválido")
                return

        if tipo == 'addUser': 
            print('add user')
            model.addUser(msg['data'])
        elif tipo == 'updateUser': 
            print('update user')
            model.updateUser(msg['token'], msg['data'])
        elif tipo == 'removeUser':
            print('remove user')
            model.removeUser(msg['data'])
        elif tipo == 'follow':
            print('follow')
            model.follow(msg['data']['token'], msg['data']['nick'])
        elif tipo == 'unfollow':
            print('unfollow')
            model.unfollow(msg['data']['token'], msg['data']['nick'])
        elif tipo == 'addTweet':
            print('add tweet')
            model.addTweet(msg['data']['token'], msg['data']['content'])
        elif tipo == 'addRetweet':
            print('add retweet')
            model.addRetweet(msg['data']['token'], msg['data']['tweetId'])
        elif tipo == 'like':
            print('like')
            model.like(msg['data']['token'], msg['data']['tweetId'])
        elif tipo == 'dislike':
            print('dislike')
            model.dislike(msg['data']['token'], msg['data']['tweetId'])
        else:
            print("Tipo de mensaje desconocido")
    except Exception as exc:
        print(f"Error processing message: {exc}")

channel.basic_consume(queue='user_queue', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='tweet_queue', on_message_callback=callback, auto_ack=True)

print("Server MQ iniciado. Esperando mensajes...")
channel.start_consuming()