#!/usr/bin/env python
import pika
import time

# 4 Types of Exchanges:
# 1. direct
# 2. topic
# 3. headers
# 4. fanout (We are using this in this tutorial)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)

# Start consuming task_queue queue
channel.basic_consume(queue='task_queue', on_message_callback=callback)

# Indicate the message has been received successfully
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
