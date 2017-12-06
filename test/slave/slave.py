import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='command', exchange_type='fanout')
channel.exchange_declare(exchange='responses', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='command' , queue=queue_name)
print(' [*] Waiting for commands. To exit press CTRL+C')


def callback(ch, method, properties, body):
    #doStuff
    message = 'HELLO WORLD'
    resp_channel = connection.channel()
    resp_channel.basic_publish(exchange='responses', routing_key='', body=message)
    resp_channel.close()


channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
