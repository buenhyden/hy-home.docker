# Messaging Recovery (09.runbooks/05-messaging)

> Emergency recovery runbooks for cluster failures and data inconsistencies.

## Overview

This runbook provides step-by-step procedures for recovering from common failure scenarios in the Messaging tier, including KRaft split-brain and RabbitMQ partition exhaustion.

## Emergency Scenarios

### 1. Kafka Cluster Partition/Split-Brain

**Symptoms**: Producers timeout with `NotControllerException`, Kafbat UI reports inconsistent broker roles.

1. **Stop the Cluster**:

   ```bash
   docker compose down
   ```

2. **Verify Persistence**:
   Ensure volumes are correctly mounted in `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/`.
3. **Reset Metadata (Standard Recovery)**:
   If metadata is corrupted, backup the `__cluster_metadata` volumes and restart brokers one-by-one, ensuring `controller_quorum_voters` are correct.
4. **Force Cluster Creation (Last Resort)**:
   Delete the `__cluster_metadata` directory to force a KRaft re-initialization. Note: This may impact topic ownership metadata.

### 2. RabbitMQ Disk Space Exhaustion

**Symptoms**: Management UI shows "Disk Alarms", brokers stop accepting new messages.

1. **Cleanup Logs**: Clear any large log files in the container.
2. **Purge Unused Queues**: Use the Management UI to purge or delete dead-letter queues or unused temporary queues.
3. **Increase Disk Limit**: If possible, increase the host volume size for `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`.

### 3. Schema Registry Inconsistency

**Symptoms**: Consumer fails to decode messages with `SerializationException`.

1. **Check Connectivity**: Ensure the Schema Registry service (`8081`) is reachable from the Kafka brokers.
2. **Manual Schema Upload**: If a schema is missing, re-register it via the Kafbat UI or REST API.

---

## Technical Escalation

- **Contact**: Infrastructure Lead / SRE Team
- **Logs**: Run `docker compose logs -f kafka` or `docker compose logs -f rabbitmq-management`.

## Related Documentation

- [Infrastructure Source](../../../infra/05-messaging/README.md)
- [Messaging Guides](../../07.guides/05-messaging/README.md)
- [Operations Policy](../../08.operations/05-messaging/README.md)
