#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Declare/create a random queue, by not giving RabbitMQ any queue names like below.
# The queue name will be some sort like amq.gen-JzTY20BRgKO-HjmUJj0wLg when show all queues using command.
# Add exclusive=True, so when the consumers (worker.py) instances' connections are closed, this queue will be deleted.
result = channel.queue_declare(queue='', exclusive=True)

# The name of the queue is in result.method.queue.
# Assign result.method.queue to a new variable called queue_name.
queue_name = result.method.queue

# Link/Bind the exchange to your generated queue(s).
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()