import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

msg = " ".join(sys.argv[1:])
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=False)
channel.basic_publish(exchange='logs', routing_key='', body=msg)

print('Sent')
connection.close()