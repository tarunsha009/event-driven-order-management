from confluent_kafka import Consumer, Producer, KafkaException
import json
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, VALIDATED_ORDERS_TOPIC

def create_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    return consumer

def create_kafka_producer():
    producer = Producer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
    })
    return producer

def validate_order(order):
    if 'order_id' in order and 'product' in order and isinstance(order['quantity'], int):
        return True
    return False

def consume_and_validate_orders():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            order = json.loads(msg.value().decode('utf-8'))
            if validate_order(order):
                producer.produce(VALIDATED_ORDERS_TOPIC, value=json.dumps(order).encode('utf-8'))
                print(f"Valid Order Produced: {order}")
            else:
                print(f"Invalid Order: {order}")

            producer.flush()

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_and_validate_orders()