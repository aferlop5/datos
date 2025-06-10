import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='log-queue', durable=False)
channel.queue_bind(exchange='logs', queue='log-queue', routing_key='log')

def callback(ch, method, properties, body):
    print(f"Received: {body}")

channel.basic_consume(queue='log-queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()