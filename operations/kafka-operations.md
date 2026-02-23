# Kafka Operational Blueprint

> Standard operating procedures for creating topics, resetting consumer groups, and managing partition state inside the KRaft cluster.

## 1. Command Execution Context

Because the stack utilizes the Confluent Platform enterprise images, the binary paths require specific `.sh` extensions differently than raw Apache binaries. All commands should be run using `docker exec` against `kafka-1`.

> [!NOTE]
> Since we use KRaft natively, we point to `--bootstrap-server` exclusively rather than deprecated `--zookeeper` flags.

## 2. Topic Management

**Create a Topic (3 Partitions, 3 Replicas)**

```bash
docker exec -it kafka-1 kafka-topics \
  --create \
  --bootstrap-server localhost:19092 \
  --replication-factor 3 \
  --partitions 3 \
  --topic analytics.events.v1
```

**Alter Partitions (Scale Up Only)**

```bash
docker exec -it kafka-1 kafka-topics \
  --alter \
  --bootstrap-server localhost:19092 \
  --topic analytics.events.v1 \
  --partitions 6
```

_Note: You cannot decrease partitions natively in Kafka._

## 3. Consumer Group Interventions

Oftentimes developers need to replay messages for testing or clear a poisoned dead letter queue.

**List Active Groups**

```bash
docker exec -it kafka-1 kafka-consumer-groups \
  --bootstrap-server localhost:19092 \
  --list
```

**Reset Consumer Group Offset to "Earliest"**

```bash
docker exec -it kafka-1 kafka-consumer-groups \
  --bootstrap-server localhost:19092 \
  --group analytics-processor-group \
  --topic analytics.events.v1 \
  --reset-offsets --to-earliest \
  --execute
```

## 4. JMX Memory Adjustments

Heap size is bounded globally in `docker-compose.yml` (`KAFKA_HEAP_OPTS: '-Xms1G -Xmx1G'`). If you experience `OutOfMemoryError: Java heap space` due to massive data influx:

1. Scale up the node limitations in `docker-compose.yml`.
2. Increase the `deploy.resources.limits.memory` cap to at least `2.5G`.
3. Modify the JVM opts: `KAFKA_HEAP_OPTS: '-Xms2G -Xmx2G'`.
4. Perform a rolling restart (node 3 -> node 2 -> node 1).
