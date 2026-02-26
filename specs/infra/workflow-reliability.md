---
title: '[SPEC-WFL-01] Workflow Reliability Technical Specification'
status: 'Draft'
version: 'v0.1.0'
owner: 'Workflow Engineer'
tags: ['spec', 'technical', 'workflow', 'n8n', 'airflow']
---

# [SPEC-WFL-01] Workflow Reliability Technical Specification

## 1. Overview

This specification details the reliability and execution standards for the workflow automation tier (n8n, Airflow).

## 2. Execution Modes (n8n)

- **Primary Node**: Handles UI and workflow orchestration.
- **Workers**: Scalable pool for heavy node processing (LVM-compliant).
- **Task Runner**: Dedicated environment for native node executions (Python/Node).

## 3. Retry & Failure Policy

| Error Type | Default Action | Max Retries | Backoff |
| --- | --- | --- | --- |
| Network Timeout | Retry | 3 | Exponential (60s base) |
| Auth Failure | Fail | 0 | Manual intervention |
| Resource Limit | Kill & Alert | 1 | Delay 5m |

## 4. Queue Standards (Bull / Valkey)

- **Persistence**: `appendonly: yes` for the queue database.
- **Prefix**: `n8n` to avoid overlap in shared Redis instances.

## 5. Observability

- **Metrics**: Enabled via `N8N_METRICS` on port 5678.
- **Logs**: High-cardinality logs sent to Loki via Alloy.
