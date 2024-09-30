import logging
import sys
import time

from confluent_kafka import Consumer, Producer, KafkaException
import json
from config import KAFKA_BOOTSTRAP_SERVERS, VALIDATED_ORDERS_TOPIC, STOCK_UPDATED_ORDERS_TOPIC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.flush = sys.stdout.flush
logging.getLogger().addHandler(handler)


inventory_data = {
    "item1": 10,
    "item2": 20,
    "item3": 0
}

def create_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'inventory-group',
        'auto.offset.reset': 'earliest'
    })
    return consumer

def create_kafka_producer():
    producer = Producer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
    })
    return producer


def check_inventory(order):
    item = order['product']
    if inventory_data.get(item , 0) > 0:
        inventory_data[item] -=1
        return True
    else:
        return False
def consume_and_update_inventory():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    consumer.subscribe([VALIDATED_ORDERS_TOPIC])

    # while True:
    #     try:
    #         consumer.subscribe([VALIDATED_ORDERS_TOPIC])
    #         break
    #     except KafkaException as e:
    #         logging.error(f"Error subscribing to topic: {e}")
    #         time.sleep(5)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                logging.error(f"Error consuming message: {msg.error()}")
                raise KafkaException(msg.error())

            order = json.loads(msg.value().decode('utf-8'))
            logging.info(f"Consumed Validated Order: {order}")

            # Check inventory
            if check_inventory(order):
                logging.info(f"Stock available for order: {order}")
                order['stock_status'] = 'available'
            else:
                logging.warning(f"Stock not available for order: {order}")
                order['stock_status'] = 'out_of_stock'

            # Produce updated order to stock-updated-orders topic
            producer.produce(STOCK_UPDATED_ORDERS_TOPIC, json.dumps(order))
            producer.flush()

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_and_update_inventory()


