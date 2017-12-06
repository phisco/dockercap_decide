import pika
import logging
from time import time
import os

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', port=5672))
        break
    except
channel = connection.channel()
channel.exchange_declare(exchange='command', exchange_type='fanout')
channel.exchange_declare(exchange='responses', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='command', queue=queue_name)
resp_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', port=5672))
logging.basicConfig(level=logging.INFO)

resp_channel = resp_connection.channel()
def callback(ch, method, properties, body):
    os.popen('stress-ng --cpu 1 --udp 1 --memcpy 1 -t 10 2>&1 1>/dev/null')
    logging.info(body)
    resp_channel.basic_publish(exchange='responses', routing_key='', body=str(time()))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
logging.info(' [*] Waiting for commands. To exit press CTRL+C')

channel.start_consuming()
