import pika
from time import sleep,time
import docker
import os
import logging

LOCAL_PATH = '/home/users/marco.arnaboldi/hyppo/powercap/_build/utils'
NUM_PACKAGES = 2
NUM_WORKERS = 2
TIME = 1
logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body):
    print(body)

def test(minW=50, maxW=200, step=10):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()
    channel.exchange_declare(exchange='command', exchange_type='fanout')
    channel.exchange_declare(exchange='responses', exchange_type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='responses', queue=queue_name)

    cmd_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    cmd_channel = cmd_connection.channel()
    for i in range(maxW, minW, -step):
        print(i)
        for p in range(NUM_PACKAGES):
            os.system('{0}/rapl-set --package={1} --constraint=0 --c-power-limit={2}'.format(LOCAL_PATH, p, i*1000000))

        cmd_channel.basic_publish(exchange='command', routing_key='', body='execute')
        sleep(TIME)
    cmd_channel.close()

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    client = docker.from_env()
    test()
