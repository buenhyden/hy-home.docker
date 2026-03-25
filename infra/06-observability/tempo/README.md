# Tempo Distributed Tracing

> High-scale, easy-to-use distributed tracing backend.

## Overview

Tempo stores trace data in an S3-compatible backend (MinIO). It enables "TraceQL" for powerful querying and allows correlation between metrics, logs, and traces starting from a Span ID.

## Audience

- Developers (Latency analysis)
- SREs (System bottleneck identification)

## Tech Stack

| Component | Technology | Version | Backend |
| :--- | :--- | :--- | :--- |
| Tracing | Tempo | v2.10.1 | MinIO (S3) |

## Configuration

- **Ingestion**: OTLP via Alloy collector.
- **Persistence**: Bucket `tempo` in MinIO.

## AI Agent Guidance

1. Enable `Service Graphs` in Grafana using Tempo metrics.
2. Use TraceQL to find high-latency dependencies across tiers.
