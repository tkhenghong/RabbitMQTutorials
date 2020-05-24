import pika
import sys

# 4 Types of Exchanges:
# 1. direct
# 2. topic
# 3. headers
# 4. fanout (We are using this in this tutorial): The most basic exchange that this exchange will publish to all queues that are subscribed to this type of exchange.

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

# Declare/Create a new exchange called 'logs', with type fanout.
channel.exchange_declare(exchange="logs", exchange_type="fanout")

message = " ".join(sys.argv[1:]) or "Hello World!"

# Send a message to an exchange with name 'logs', with no defined routing_key(means queue name)
channel.basic_publish(
    exchange="logs", routing_key="", body=message,
)

print(" [x] Sent %r" % message)

# To list all exchanges that you have created, type in terminal:
# sudo rabbitmqctl list_exchanges
