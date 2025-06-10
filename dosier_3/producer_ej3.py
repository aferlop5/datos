import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

severity = sys.argv[1]
msg = " ".join(sys.argv[2:])

channel.exchange_declare(exchange='logs2', exchange_type='direct', durable=False)

channel.basic_publish(
    exchange='logs2',
    routing_key=severity,
    body=msg
)

print('Sent')
connection.close()