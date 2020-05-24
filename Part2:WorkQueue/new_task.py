import pika
import sys

# Connect to pika library, a Python library for communicating with RabbitMQ(Official recommended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare/create a new queue in RabbitMQ. It will always and only one no matter how many times you declare it.
# The RabbitMQ server will forget all the message if the RabbitMQ server is down. Set durable=True so the RabbitMQ will make sure particular queue in the RabbitMQ will not forget it's message and it will redeliver the message to the worker.py instances.
# BOTH side MUST declare durable=True.
# Commenting this queue declaration because the queue's durable cannot be changed after the queue is created without durable=True for the first time.
# channel.queue_declare(queue='hello', durable=True)

# We MUST create another queue with durable=True in the FIRST TIME.
channel.queue_declare(queue='task_queue', durable=True)


# Declare message variable, read the first argument given from outside or simply print Hello World
message = ' '.join(sys.argv[1:]) or "Hello World!"

# Publish/Produce/Send the message to 'hello' queue, with default exchange and body of message variable
# Commenting this publish because we won't use 'hello' queue without durability.
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=message)

# Publishing a message with durability:
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

# Indicate message has been sent successfully, with print out the message details.
print(" [x] Sent %r" % message)