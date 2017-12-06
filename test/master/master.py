import pika
from time import sleep,time
import docker
import os

LOCAL_PATH = '/home/users/marco.arnaboldi/hyppo/powercap/_build/utils'
NUM_PACKAGES = 2
NUM_WORKERS = 2
TIME = 10

def callback(ch, method, properties, body):
    print(time())

def test(minW=50, maxW=200, step=10):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()
    channel.exchange_declare(exchange='command', exchange_type='fanout')
    channel.exchange_declare(exchange='responses', exchange_type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='responses', queue=queue_name)

    cmd_channel = connection.channel()
    for i in range(maxW, minW, -step):
        for p in range(NUM_PACKAGES):
            os.system('{0}/rapl-set --package={1} --constraint=0 --c-power-limit={2}'.format(LOCAL_PATH, p, i*1000000))
        cmd_channel.basic_publish(exchange='command', routing_key='', body='execute')
        sleep(TIME)
    cmd_channel.close()

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    client = docker.from_env()
    containers = []
    containers.append(client.containers.run('rabbitmq:3', detach=True, ports={'5672/tcp': 5672}))
    rabbit = containers[0]
    image = client.images.build(path='../slave')
    for i in range(0, NUM_WORKERS):
        containers.append(client.containers.run(image, detach=True))
    while True:
        if len(filter(lambda container: container.status is not 'ready')) == 0:
            break
        else:
            sleep(5)
    test()
    for el in containers:
        el.kill()
