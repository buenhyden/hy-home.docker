# SMTP Mail Relay Operational Guide

> **Component**: `mailhog`
> **Internal Port**: `1025` (SMTP), `8025` (HTTP UI)

## 1. Purpose

Provides a localized, zero-config SMTP relay for development and staging alert notifications. This ensures no real PII is leaked to external providers during testing.

## 2. Integration Specs

Applications (Grafana, Keycloak, n8n) should use the following settings for internal mail:

- **Host**: `mail`
- **Port**: `1025`
- **Auth**: None
- **Encryption**: Plain (Internal Docker network is considered trusted)

## 3. Inspection Dashboard

All outgoing mail is trapped and visualizable via the internal Traefik route:

- **URL**: `https://mail.${DEFAULT_URL}`

## 4. Common Tasks

### Clearing the Mail Buffer

MailHog stores messages in-memory by default. A container restart wipes the history.

```bash
docker restart infra-mail
```
