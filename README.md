# Event-Driven Order Management System

This project implements a microservices-based order management system using Kafka for event-driven communication between services.

## Technologies Used
- **Kafka**: For event-driven messaging between microservices.
- **Docker**: To containerize services like Kafka, Zookeeper, and Kafka UI.
- **Python**: To implement producer and consumer microservices using Confluent Kafka.

## Microservices
- **Order Producer**: Produces new orders and sends them to Kafka.
- **Order Validator**: Validates orders and publishes them to another topic.
- **Inventory Service**: Checks inventory and processes or fails the order.

## How to Run
- Use `docker-compose` to start Kafka, Zookeeper, and Kafka UI.
- Run the Python producer and consumer services.
