# Messaging Operations (05-messaging)

> Operational policies for event streaming, message brokering, and real-time data processing.

## Overview

This document outlines the operational policies for the Messaging tier, ensuring high availability, reliable persistence, and efficient resource utilization across Kafka and RabbitMQ.

## Operational Policies

### 1. High Availability (HA)

- **Kafka Cluster**: Use a 3-node KRaft quorum for fault tolerance.
- **Service Replication**: Ensure topics are created with a minimum replication factor of `3`.
- **RabbitMQ HA**: Use mirrored queues or quorum queues for critical workloads.

### 2. Retention and Compaction

- **Log Retention**: Default Kafka retention is set to 7 days or 50GB per topic.
- **Compaction**: Enable log compaction for configuration and state-store topics.

### 3. Monitoring and Alerting

- **Metrics**: Monitor broker disk usage, consumer lag, and under-replicated partitions.
- **Tools**: Use Kafbat UI and Prometheus/Grafana for real-time visibility.

### 4. Security

- **Access Control**: Use dedicated service accounts and ACLs where possible.
- **TLS/SSL**: All external ingress via Traefik is secured with SSL.

## Maintenance Procedures

### Scaling the Cluster
- **Horizontal Scaling**: Adding new Kafka brokers requires updating the `controller_quorum_voters` in the `docker-compose.yml`.
- **Partition Rebalancing**: Use specialized tools to redistribute partitions after adding brokers.

---

## Related Documentation

- [Infrastructure Source](../../../infra/05-messaging/README.md)
- [Messaging Guides](../../07.guides/05-messaging/README.md)
- [Recovery Runbook](../../09.runbooks/05-messaging/README.md)
