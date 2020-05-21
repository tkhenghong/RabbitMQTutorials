import pika
import sys

# Connect to pika library, a Python library for communicating with RabbitMQ(Official recommended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare/create a new queue in RabbitMQ. It will always and only one no matter how many times you declare it.
# The RabbitMQ server will forget all the message if the RabbitMQ server is down. Set durable=True so the RabbitMQ will make sure particular queue in the RabbitMQ will not forget it's message and it will redeliver the message to the worker.py instances.
# BOTH side MUST declare durable=True.
channel.queue_declare(queue='hello', durable=True)


# Declare message variable, read the first argument given from outside or simply print Hello World
message = ' '.join(sys.argv[1:]) or "Hello World!"

# Publish/Produce/Send the message to 'hello' queue, with default exchange and body of message variable
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

# Indicate message has been sent successfully, with print out the message details.
print(" [x] Sent %r" % message)