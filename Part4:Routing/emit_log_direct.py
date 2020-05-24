import pika
import sys

# 4 Types of Exchanges:
# 1. direct (We are using this exchange in this tutorial): A type of exchange that will send to queues with the correct binding key(a.k.a routing_key).
# 2. topic
# 3. headers
# 4. fanout

# Usage of DIRECT type exchange is to selectively give queues messages.
# Like for example, there are many queues linked to the DIRECT exchange, but I ONLY WANT CERTAIN TYPE OF MESSAGE be listed in some queues only.

# For example, we create a direct exchange, then we create random queues.
# After that, when we create a binding between them, we will mention the routing_key.
# routing_key is IGNORED in the FANOUT type exchange, but will be USED by DIRECT type exchange.

# NOTE: Do not be confused with the routing_key between the one inside the basic_publish(...) with the producer sending messages,
#           channel.basic_publish(exchange="logs", routing_key="", body=message,)
# with the one that lies inside the binding of an exchange to a queue using queue_bind(...) method.
#           channel.queue_bind(exchange='logs', queue=queue_name)

# Also NOTE that: The routing_key means your destination queue name that your want to give your message to when sending/publish a message.

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

# If there's type of the message mentioned, use that. If not, default 'info' type of the message is selected.
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = " ".join(sys.argv[1:]) or "Hello World!"


channel.basic_publish(
    exchange="direct_logs", routing_key=severity, body=message,
)

print(" [x] Sent %r" % message)

connection.close()
