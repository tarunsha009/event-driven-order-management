from confluent_kafka import Consumer, KafkaException
import json
from consumer1.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

def create_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    return consumer

def consume_orders():
    consumer = create_kafka_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)  # Wait for a message for 1 second
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            order = json.loads(msg.value().decode('utf-8'))
            print(f"Consumed Order: {order}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
