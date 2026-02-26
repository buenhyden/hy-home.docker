---
title: '[SPEC-OBS-01] Observability Rules Technical Specification'
status: 'Draft'
version: 'v0.1.0'
owner: 'Observability Engineer'
tags: ['spec', 'technical', 'observability', 'prometheus', 'alerting']
---

# [SPEC-OBS-01] Observability Rules Technical Specification

## 1. Overview

This specification defines the critical alerting thresholds and health indicators for the Hy-Home infrastructure.

## 2. Infrastructure Health Rules

| Metric | Threshold | Level | Action |
| --- | --- | --- | --- |
| CPU Usage | > 85% for 15m | Critical | Alert Manager (Slack/Email) |
| Memory Usage | > 90% for 5m | Warning | Alert Manager |
| Container Restarts | > 10 in 1h | Critical | Infrastructure Audit |

## 3. Database & Data Tier

| Component | Metric | Threshold | logic |
| --- | --- | --- | --- |
| PostgreSQL | `pg_up` | == 0 | Service Down |
| Patroni | `patroni_leader_count` | != 1 | Cluster Split Brain |
| Valkey | `redis_up` | == 0 | Cache Tier Down |

## 4. Messaging Tier (Kafka)

| Alert Name | Metric | Logic | Description |
| --- | --- | --- | --- |
| ConsumerLag | `kafka_consumergroup_lag` | > 1000 | Consumer is falling behind |
| BrokerCount | `kafka_brokers` | < 3 | Quorum lost / Node Failure |

## 5. Deployment

Rules are loaded via Prometheus `rule_files` directive as `.yaml` fragments.
