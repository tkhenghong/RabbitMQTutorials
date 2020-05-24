import pika
import sys

# 4 Types of Exchanges:
# 1. direct
# 2. topic
# 3. headers
# 4. fanout (We are using this in this tutorial): The most basic exchange that this exchange will publish to all queues that are subscribed to this type of exchange.

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare/Create a new exchange called 'logs', with type fanout.
channel.exchange_declare(exchange="logs", exchange_type="fanout")

message = " ".join(sys.argv[1:]) or "Hello World!"

# Send a message to an exchange with name 'logs', with no defined routing_key(means queue name)
# NOTE: The routing_key's value is IGNORED, when send a message to a fanout type exchanges.
channel.basic_publish(
    exchange="logs", routing_key="", body=message,
)

print(" [x] Sent %r" % message)

connection.close()

# To list all exchanges that you have created, type in terminal:
# rabbitmqctl list_exchanges

# To list all the bindings in the RabbitMQ, type in the terminal:
# rabbitmqctl list_bindings

# NOTE: When you run this part of the tutorial, please run the receive_logs.py first.
# Because the exchange will need to have queues to linked with it first before have any messages sent.

# Steps to run this part of the tutorial:
# python receive_logs.py (Open multiple terminals, cd to the directory where our file are, and repeat this command)
# python emit_log.py

# RESULT: You will see all the terminals that typed 'python receive_logs.py' received the message from the 'python emit_log.py'.
# Type 'rabbitmqctl list_bindings' command and you'll see many bindings, one of the bindings will have 2 or more records,
# which source name called 'logs', source_kind 'exchange', with destination_name called 'amq.gen-ETjukttwB0pJ0C4HraJYEg'(or some sort) ,
# destination_kind 'queue' and arguments '[]'.
# Minor finding: destination_name and routing_key are same when a queue is generated in basic.