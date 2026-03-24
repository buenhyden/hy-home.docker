---
title: '[Service Name] Service Guide'
status: 'Stable | Beta | Experimental'
version: 'v1.0.0'
date: 'YYYY-MM-DD'
owner: 'buenhyden'
layer: 'infra'
tags: ['service', 'guide', 'ops']
---

# Service Guide: [Service Name]

> **Status**: [Stable | Beta | Experimental]
> **Version**: v1.0.0
> **Date**: YYYY-MM-DD
> **Layer**: infra
> **Tier**: [01-10]

**Overview (KR):** [이 서비스의 역할, 주요 기능, 그리고 아키텍처 내에서의 위치를 한국어로 1-2문장 요약하세요.]

---

## 1. Architecture Context

* **Role**: Primary function of the service.
* **Upstream**: [Services that call this]
* **Downstream**: [Services this service calls]

---

## 2. Configuration & Secrets

### 2.1. Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `PORT`   | Listen port | `8080`  |

### 2.2. Secrets

| Secret | Purpose |
| ------ | ------- |
| `DB_PASSWORD` | Access to primary DB |

---

## 3. Operational Tasks

### 3.1. Local Setup

```bash
docker compose up [service-name]
```

### 3.2. Health Check

* Endpoint: `/health`
* Readiness: `/ready`

---

## 4. Observability

* **Log Level**: Controlled via `LOG_LEVEL` env.
* **Metrics Path**: `/metrics` (Prometheus)
* **Dashboard**: [Grafana Link]

---

## 5. Troubleshooting

| Symptom | Probable Cause | Fix |
| ------- | -------------- | --- |
| [503 Error] | [DB Connection] | [Check DB health] |
