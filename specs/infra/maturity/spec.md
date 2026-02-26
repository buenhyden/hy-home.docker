---
title: 'Infra Maturity & Automation Phase 2 Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: '../../docs/prd/infra-automation-prd.md'
api_reference: 'N/A'
arch_reference: '../../docs/ard/infra-automation-ard.md'
tags: ['spec', 'implementation', 'infra', 'automation']
goal: 'standardize automation and scaling'
date_created: '2026-02-26'
last_updated: '2026-02-26'
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: `../../docs/prd/infra-automation-prd.md`
> **Related Architecture**: `../../docs/ard/infra-automation-ard.md`

## 0. Pre-Implementation Checklist (Governance)

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Modular Infra | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | `infra/<domain>` | Section 1 |
| Quality / Testing  | Test Strategy defined?                                | Must     | GWT scenarios | Section 22 |

## 1. Technical Overview

This spec covers the automation of resource initialization (MinIO/Kafka/OpenSearch) and standardization of monitoring/resource limits.

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority | Parent PRD REQ |
| --- | --- | --- | --- |
| **REQ-SPC-MAT-001** | Implement `init-sidecar` for OpenSearch index templates | Critical | REQ-AUTO-01 |
| **REQ-SPC-MAT-002** | Implement `init-sidecar` for Kafka topic creation | Critical | REQ-AUTO-01 |
| **REQ-SPC-MAT-003** | Convert manual Grafana dashboards to provisioned files | High | REQ-OBS-01 |
| **REQ-SPC-MAT-004** | Update `alloy` for `project_net` log aggregation | High | REQ-OPS-01 |
| **REQ-SPC-MAT-005** | Standardize `mem_reservation` across `04-data` | High | ADR-007 |

## 3. Data Modeling & Storage Strategy

Infrastructure sidecars use one-off scripts to communicate with core storage engines.

## 4. Acceptance Criteria (GWT)

### GWT-001: OpenSearch Initialization

- **Given**: OpenSearch service is healthy
- **When**: `opensearch-init` container runs
- **Then**: `logs_template` exists in OpenSearch API.

### GWT-002: Kafka Topic Creation

- **Given**: Kafka cluster is up
- **When**: `kafka-init` container runs
- **Then**: `infra-events` topic is listed with replication factor 3.

## 5. Implementation Steps

| Task | Description | Files Affected | Validation Criteria |
| --- | --- | --- | --- |
| TASK-001 | Init OpenSearch | `infra/04-data/opensearch/docker-compose.yml` | API 200 OK |
| TASK-002 | Init Kafka | `infra/05-messaging/kafka/docker-compose.yml` | topic exists |

## 22. Verification Plan

- **Verification-1**: `docker compose config` validation.
- **Verification-2**: Manual check of MinIO buckets after clean boot.
