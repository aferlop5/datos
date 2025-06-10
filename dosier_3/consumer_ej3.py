import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs2', exchange_type='direct', durable=False)

severities = sys.argv[1:] if len(sys.argv) > 1 else ['info']

result = channel.queue_declare(queue='', exclusive=True, durable=False)
queue_name = result.method.queue

for severity in severities:
    channel.queue_bind(exchange='logs2', queue=queue_name, routing_key=severity)

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()