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
# Commenting this queue declaration because the queue's durable cannot be changed after the queue is created without durable=True for the first time.
# channel.queue_declare(queue='hello', durable=True)

# We MUST create another queue with durable=True in the FIRST TIME.
channel.queue_declare(queue='task_queue', durable=True)

# Define a callback function to receive messages from RabbitMQ queues. It has created a timer to simulate the listener is working on something.
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")

    # Every message received NEED to create an acknowledgement to tell RabbitMQ that the message has been received so you won't lose any senders'/producers' messages.
    ch.basic_ack(delivery_tag = method.delivery_tag)

# In basic RabbitMQ, when 2 or more workers are running, the RabbitMQ dispatches the messages to those workers with Round-Robin method.
# But the RabbitMQ never considered that 1 worker may received too much work while others received only light works.
# So, quality of service needs to be implemented. When one worker has a task on hand, RabbitMQ shouldn't give it more work and send the task to other free workers.
# If all workers have tasks on hand, the RabbitMQ will wait until the task has finished and get message acknowledgement from the worker and ready to receive another task.
# channel.basic_qos(prefetch_count=1) tells RabbitMQ to implement basic QoS, and every worker should only have 1 task on hand.
channel.basic_qos(prefetch_count=1)

# Consume/Receive/Retreive the message from 'hello' queue, with default exchange with auto_ack=true.
# auto_ack=true because auto_ack by default is false. When auto_ack=true the RabbitMQ will auto resend the message to other worker.py instance if it found out the worker.py instance it sent to has died.
# If you don't mention auto_ack=true, the RabbitMQ expect you to return the acknowledgement of the message by the worker of the queue itself.
# If the worker don't acknowledge the message, the message in the queue won't get deleted by the RabbitMQ.
# Reason of manual acknowledgement: If the message given to the worker of the queue fails, the RabbitMQ will attempt to give the message to another worker, instead of losing the message forever.
# Commenting this consume because we won't use 'hello' queue without durability.
# channel.basic_consume(queue='hello',
#                     #   auto_ack=True,
                      # on_message_callback=callback)

# Start consuming task_queue queue
channel.basic_consume(queue='task_queue', on_message_callback=callback)

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

