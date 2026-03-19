---
layer: infra
---
# SMTP Mail Relay Operational Guide

**Overview (KR):** 시스템 알림 전송을 위한 SMTP 메일 릴레이(MailHog) 구성 및 운영 지침입니다.

> **Component**: `mailhog`
> **Profile**: `communication`
> **Internal SMTP Port**: `1025`
> **Internal Web UI Port**: `8025`

## 1. Purpose

MailHog is a dev-only SMTP trap. It accepts outgoing mail from any service on `infra_net` but does not forward it externally. All messages are held in memory and visible through its web UI. No PII reaches external mail providers during development or testing.

For production mail sending, use **Stalwart** (see [mail-server-operations.md](mail-server-operations.md)).

## 2. Integration Specs

Applications (Grafana, Keycloak, n8n) should use the following settings for internal mail:

- **Host**: `mail`
- **Port**: `1025`
- **Auth**: None
- **Encryption**: Plain (Internal Docker network is considered trusted)

## 3. Inspection Dashboard

All outgoing mail is trapped and visible through the MailHog web UI, routed via Traefik:

- **URL**: `https://mailhog.${DEFAULT_URL}`
- **Auth**: SSO-protected via `sso-auth@file` middleware

## 4. Common Tasks

### Starting the service

```bash
# Requires the 'communication' profile
docker compose --profile communication up -d mailhog
```

### Clearing the mail buffer

MailHog stores messages in memory. A restart wipes the history.

```bash
docker restart mailhog
```

### Checking health

```bash
docker inspect --format='{{.State.Health.Status}}' mailhog
```
