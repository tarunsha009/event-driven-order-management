from confluent_kafka import Producer
import json

from producer1.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def delivery_report(err, msg):
    """ Callback for when a message is delivered or an error occurs. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def create_kafka_producer():
    return Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})


def produce_orders():
    producer = create_kafka_producer()
    for i in range(11, 20):
        order = {'order_id': i, 'product': 'Widget', 'quantity': i + 1}
        producer.produce(KAFKA_TOPIC, value=json.dumps(order), callback=delivery_report)
        producer.flush()  # Wait for all messages to be delivered
        print(f"Sent: {order}")
