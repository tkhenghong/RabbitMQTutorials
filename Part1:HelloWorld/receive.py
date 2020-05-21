#!/usr/bin/env python
# pika is unable to be run in Visual Code terminals, need to be run in MacOS terminals, run using Python CLI tool.
# import pika is auto highlighted not found here.
import pika

# Connect to pika library, a Python library for communicating with RabbitMQ(Official recommended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare/create a new queue in RabbitMQ. It will always and only one no matter how many times you declare it.
channel.queue_declare(queue='hello')

# Define a callback function to receive messages from RabbitMQ queues
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# Consume/Receive/Retreive the message from 'hello' queue, with default exchange with auto_ack=true.
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

# Indicate the message has been received successfully
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# NOTE: This will create a never stop program, every time when you execute send.py file, this file will receive message and show the message in the console screen.
