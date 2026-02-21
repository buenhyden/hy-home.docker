---
description: Workflow for Kafka Messaging Implementation
---

1. **Environment Setup**

    Start Kafka using Docker Compose.

    ```yaml
    # docker-compose.yml
    services:
      zookeeper:
        image: confluentinc/cp-zookeeper:latest
        environment:
          ZOOKEEPER_CLIENT_PORT: 2181

      kafka:
        image: confluentinc/cp-kafka:latest
        depends_on: [zookeeper]
        ports: ["9092:9092"]
        environment:
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
          KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
          KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ```

    // turbo

    ```bash
    docker-compose up -d
    ```

2. **Topic Management**

    Create necessary topics.

    ```bash
    docker exec -it kafka kafka-topics --create \
        --bootstrap-server localhost:9092 \
        --replication-factor 1 \
        --partitions 3 \
        --topic user-events
    ```

3. **Producer Implementation**

    Implement message publishing.

    ```python
    # python (using kafka-python)
    from kafka import KafkaProducer
    import json

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    producer.send('user-events', value={'user_id': 1, 'action': 'login'})
    producer.flush()
    ```

4. **Consumer Implementation**

    Implement message processing loop.

    ```python
    from kafka import KafkaConsumer
    import json

    consumer = KafkaConsumer(
        'user-events',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='analytics-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        print(f"Processing: {message.value}")
        # Process event logic here
    ```

5. **Verification**

    Monitor messages using `kcat` (formerly kafkacat).

    ```bash
    # Listen to topic
    kcat -b localhost:9092 -C -t user-events
    ```

    // turbo

    ```bash
    # Check topic list
    docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
    ```

6. **Error Handling Strategy**

    - **Retry**: Local retry for transient errors.
    - **DLQ**: Send failing messages to `user-events-dlq` after N retries.
