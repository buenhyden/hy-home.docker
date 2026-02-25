---
title: 'Infrastructure Resource Budgets Implementation Spec'
status: 'Draft'
version: '1.1'
owner: 'Platform/DevOps'
prd_reference: 'N/A'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'implementation', 'infra', 'performance', 'resource-budget']
---

# Infrastructure Resource Budgets Implementation Spec

## 1. Technical Overview

This spec defines standardized CPU/memory budgets for all infrastructure services to prevent OOM and CPU starvation. It applies to compose `deploy.resources.limits` and `reservations`.

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority |
| :--- | :--- | :--- |
| **REQ-RES-001** | All Tier 1 services MUST have high redundancy and reserved memory. | High |
| **REQ-RES-002** | All Tier 2/3 services MUST have hard memory limits. | High |
| **REQ-RES-003** | Supabase services MUST follow the defined budget tiers. | High |

## 3. Component Breakdown

### Tier 1: Critical Core

High-availability and performance-critical services.

| Component | CPU Limit | RAM Limit | RAM Reservation |
| :--- | :--- | :--- | :--- |
| PostgreSQL (pg-0/1/2) | 1.0 | 2G | 1G |
| Supabase DB | 1.0 | 2G | 1G |
| Traefik | 1.0 | 1G | 512M |
| Keycloak | 1.5 | 1.5G | 1G |
| MinIO | 1.0 | 1G | 512M |

### Tier 2: State Handlers & Control Planes

Services supporting core functionality.

| Component | CPU Limit | RAM Limit | RAM Reservation |
| :--- | :--- | :--- | :--- |
| Etcd (3x nodes) | 0.5 | 256M | 128M |
| HAProxy (Pg-router) | 0.5 | 256M | 128M |
| OAuth2-Proxy | 0.5 | 256M | 128M |
| Supavisor | 0.5 | 512M | 256M |
| Supabase Auth | 0.5 | 512M | 256M |
| Supabase Rest | 0.5 | 512M | 256M |
| Supabase Studio | 0.5 | 512M | 256M |
| Supabase Realtime | 0.5 | 512M | 256M |
| Supabase Storage | 0.5 | 512M | 256M |
| Supabase Analytics | 1.0 | 1G | 512M |
| Vector | 0.5 | 512M | 256M |

### Tier 3: Observability (Best Effort)

| Component | CPU Limit | RAM Limit | RAM Reservation |
| :--- | :--- | :--- | :--- |
| Prometheus | 2.0 | 2G | 1G |
| Loki | 1.0 | 1G | 512M |
| Tempo | 1.0 | 1G | 512M |
| Grafana | 0.5 | 512M | 256M |
| Alloy | 0.5 | 512M | 256M |

## 4. Verification Plan

- **[VAL-RES-001]**: `docker compose config` verification.
- **[VAL-RES-002]**: `docker stats` audit after deployment.
