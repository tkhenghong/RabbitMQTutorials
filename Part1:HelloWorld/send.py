#!/usr/bin/env python
# pika is unable to be run in Visual Code terminals, need to be run in MacOS terminals, run using Python CLI tool.
# import pika is auto highlighted not found here.
import pika

# Connect to pika library, a Python library for communicating with RabbitMQ(Official recommended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare/create a new queue in RabbitMQ. It will always and only one no matter how many times you declare it.
channel.queue_declare(queue='hello')

# Publish/Produce/Send the message to 'hello' queue, with default exchange and body of message variable
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

# Indicate message has been sent successfully sent, with print out the message details.
connection.close()