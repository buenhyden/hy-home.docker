# Loki Log Aggregation System

> Cloud-native log aggregation system inspired by Prometheus.

## Overview

Loki is optimized for high-volume logs, indexing labels rather than content to maintain low storage costs. It uses MinIO for long-term persistence and is tightly integrated with Grafana for LogQL querying.

## Audience

- Developers (Debugging)
- SREs (Log retention)

## Tech Stack

| Component | Technology | Version | Backend |
| :--- | :--- | :--- | :--- |
| Logging | Loki | v3.6.6 | MinIO (S3) |

## Configuration

- **Ingestion**: Handled by Alloy or Docker log drivers.
- **Persistence**: Bucket `loki` in MinIO.

## AI Agent Guidance

1. Use `LogQL` for structured log analysis.
2. Ensure log labels are consistent with Prometheus metrics for easy correlation.
3. Check `Retention` policies before archiving large log volumes.
