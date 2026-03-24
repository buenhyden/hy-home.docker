---
title: '[API Name/Feature] API Specification'
status: 'Draft | Proposed | Approved | Deprecated'
version: 'v1.0.0'
date: 'YYYY-MM-DD'
openapi_version: '3.1.0'
owner: 'buenhyden'
layer: 'backend'
tags: ['api', 'contract', 'specification']
---

# API Specification ([API Name/Feature])

> **Status**: [Draft | Proposed | Approved | Deprecated]
> **Version**: v1.0.0 (OpenAPI 3.1.0)
> **Date**: YYYY-MM-DD
> **Layer**: backend
> **Base URL**: `https://api.example.com/v1`
> **Related PRD**: [Link to PRD]
> **Related Spec**: [Link to Tech Spec]
> **Related ADR**: [Link to ADR]

**Overview (KR):** [API의 목적, 해결하려는 문제, 그리고 주요 소비층(Web, Mobile 등)을 한국어로 1-2문장 요약하세요.]

---

## 1. Overview & Use Cases

**Objective**: Briefly describe the problem this API solves.

**Primary Consumers**: [Web Client | Mobile App | Internal Service | 3rd Party]

**Use Cases**:

* **UC1**: [e.g., User can retrieve a list of widgets with cursor-based pagination]
* **UC2**: [e.g., User can create a new widget with validation]

---

## 2. Security & Authentication

### 2.1. Authentication Schemes

* **`BearerAuth`**: HTTP Bearer (JWT) - Primary for User-facing APIs.
* **`ApiKeyAuth`**: `X-API-Key` Header - Primary for Service-to-Service or Public APIs.

### 2.2. Authorization (Scopes)

| Scope | Description |
| ----- | ----------- |
| `read` | Read access to resources |
| `write` | Write access to resources |

---

## 3. Data Models (Schemas)

| Property | Type | Required | Description | Example |
| -------- | ---- | -------- | ----------- | ------- |
| `id` | `uuid` | Yes | Unique identifier | `550e8400-e29b-...` |

---

## 4. Endpoints Contract

### 4.1. `[METHOD] /v1/[resource]`

**Request**:

* **Authentication**: `BearerAuth` (Mandatory)
* **Content-Type**: `application/json`
* **Body Schema**: (Reference model or define inline)

**Responses**:

* **200 OK**: Success.
* **400 Bad Request**: Validation failure.
* **401 Unauthorized**: Missing/Invalid auth.

---

## 5. Non-Functional Requirements (NFRs)

* **Latency**: P95 < [Value]ms
* **Availability**: [Value]% SLA
* **Rate Limit**: [Number] req/min per [ID Type]
