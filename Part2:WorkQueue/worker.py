#!/usr/bin/env python
# pika is unable to be run in Visual Code terminals, need to be run in MacOS terminals, run using Python CLI tool.
# import pika is auto highlighted not found here.
import pika
import time

# Connect to pika library, a Python library for communicating with RabbitMQ(Official recommended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare/create a new queue in RabbitMQ. It will always and only one no matter how many times you declare it.
# The RabbitMQ server will forget all the message if the RabbitMQ server is down. Set durable=True so the RabbitMQ will make sure particular queue in the RabbitMQ will not forget it's message and it will redeliver the message to the worker.py instances.
# BOTH side MUST declare durable=True.
channel.queue_declare(queue='hello', durable=True)

# Define a callback function to receive messages from RabbitMQ queues. It has created a timer to simulate the listener is working on something.
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")

    # Every message received NEED to create an acknowledgement to tell RabbitMQ that the message has been received so you won't lose any senders'/producers' messages.
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Consume/Receive/Retreive the message from 'hello' queue, with default exchange with auto_ack=true.

# auto_ack=true because auto_ack by default is false. When auto_ack=true the RabbitMQ will auto resend the message to other worker.py instance if it found out the worker.py instance it sent to has died.
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

# Indicate the message has been received successfully
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# NOTE: This will create a never stop program, every time when you execute send.py file, this file will receive message and show the message in the console screen.

# You can run multiple worker.py in multiple instances of terminal. (python worker.py)
# Now send a message by running (python new_task.py)
# The workers are getting the message in round robin fashion.

# You HAVE create ACKNOWLEDGEMENT message to prevent memory leak(Because RabbitMQ the message sent to the unexpected shutdowned worker.py instance are unacknowledged and unable to release those unsent messages)

# To check any unacknowledged message use the following command in the terminal:
# sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged

