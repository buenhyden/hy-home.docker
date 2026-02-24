# ksqlDB

ksqlDB is the streaming SQL engine for Apache Kafka. It allows you to build stream processing applications using a SQL-like syntax.

## Services

| Service        | Image                           | Role               | Resources         |
| :------------- | :------------------------------ | :----------------- | :---------------- |
| `ksqldb-server`| `confluentinc/ksqldb-server:latest` | Stream Processor | 1 CPU / 2GB RAM   |
| `ksqldb-cli`   | `confluentinc/ksqldb-cli:latest`    | CLI Tool           | -                 |

## Dependencies

- **Kafka**: Connects to the Kafka broker (`infra/05-messaging/kafka`).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and SQL examples.  |
