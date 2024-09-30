import logging
import sys

from confluent_kafka import Consumer, KafkaException, Producer
import json
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, VALIDATED_ORDERS_TOPIC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.flush = sys.stdout.flush
logging.getLogger().addHandler(handler)
def create_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'order-validator-group',
        'auto.offset.reset': 'earliest'
    })
    return consumer

def create_kafka_producer():
    producer = Producer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
    })
    return producer

def consume_and_validate_orders():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)  # Wait for a message for 1 second
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Error consuming message: {msg.error()}")
                raise KafkaException(msg.error())

            order = json.loads(msg.value().decode('utf-8'))
            logging.info(f"Consumed Order: {order}")

            # Example validation logic (you can modify this)
            if order.get("valid", True):
                logging.info(f"Valid Order: {order}")
                producer.produce(VALIDATED_ORDERS_TOPIC, json.dumps(order))
            else:
                logging.warning(f"Invalid Order: {order}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_and_validate_orders()
