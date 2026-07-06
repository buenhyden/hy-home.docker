---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/prometheus.md -->

# Prometheus Operations Policy

## Overview

This policy defines Prometheus controls for scrape target registration, alerting
rule management, TSDB persistence, lifecycle reload, secret file references, and
protected access. Ordered recovery or reload procedures belong in the matching
runbook.

## Policy Scope

This policy applies to the current `infra/06-observability/prometheus` compose,
config, and alert-rule surfaces.

- **Systems**: compose service `prometheus`, container `infra-prometheus`, image `prom/prometheus:v3.13.0`, config `infra/06-observability/prometheus/config/prometheus.yml`, rules directory `infra/06-observability/prometheus/config/alert_rules`, volume `prometheus-data`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Prometheus service는 `template-stateful-high`, image
    `prom/prometheus:v3.13.0`, tmpfs `/tmp` and `/etc/prometheus:size=10M`,
    read-only config/rules mounts, persistent `prometheus-data` volume을
    유지한다.
  - Runtime command는 `--config.file=/etc/prometheus/prometheus.yml`,
    `--storage.tsdb.path=/prometheus`, `--web.enable-lifecycle`,
    `--web.enable-remote-write-receiver`를 유지한다.
  - Global cadence는 `scrape_interval: 30s`와 `evaluation_interval: 30s`를
    기준으로 한다. Service-specific intervals such as Prometheus `15s` and
    cAdvisor `1m` must remain intentional and reviewed.
  - Scrape jobs are managed in
    `infra/06-observability/prometheus/config/prometheus.yml`.
  - Alert and recording rules are loaded from
    `/etc/prometheus/alert_rules/alert_rules.local.*.yml`,
    `/etc/prometheus/alert_rules/alert_rules.k8s.yml`,
    `/etc/prometheus/alert_rules/alert_rules.keycloak.yml`,
    `/etc/prometheus/alert_rules/alert_rules.vault.yml`, and
    `/etc/prometheus/alert_rules/recording_rules.yml`.
  - Alert rules must include `expr`, `for` when applicable, `labels.severity`,
    and actionable `annotations`.
  - `opensearch_exporter_password` and `vault_token` are Docker Secret file
    references only; their values must not appear in docs, logs, or task
    evidence.
  - Prometheus route must keep
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - TSDB retention changes must be paired with
    [retention policy](./retention.md), volume impact review, and plan/task
    evidence. The current compose command does not declare an explicit
    `--storage.tsdb.retention.*` flag.
- **Allowed**:
  - New scrape targets may be added when the target exposes a stable metrics
    endpoint reachable from Prometheus networks and has matching alerting or
    documented no-alert rationale.
  - Expensive PromQL may be moved into recording rules after dashboard and rule
    impact review.
  - Lifecycle reload may be used after config/rule validation; operational
    reload steps belong in the runbook.
- **Disallowed**:
  - Scrape interval below `10s` without architectural approval and capacity
    evidence
  - High-cardinality label additions without cardinality review
  - UI/API-only changes that bypass git-managed `prometheus.yml` or
    `alert_rules`
  - Recording secret values, bearer tokens, or rendered secret content in
    documentation or evidence
  - Declaring retention behavior that is not backed by compose/config and the
    retention policy

## Exceptions

- Scrape interval, retention, secret reference, route, or rule-loading
  exceptions require user approval and related plan/task evidence.
- Emergency reload or target suppression must be recorded through the Prometheus
  runbook with rollback evidence.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: prom/prometheus:v3.13.0|--web.enable-lifecycle|--web.enable-remote-write-receiver|prometheus-data|opensearch_exporter_password|vault_token|prometheus.middlewares' infra/06-observability/docker-compose.yml`
- Prometheus config:
  `rg -n 'scrape_interval: 30s|evaluation_interval: 30s|rule_files:|alert_rules.local|recording_rules.yml|password_file: "/run/secrets/opensearch_exporter_password"|bearer_token_file: /run/secrets/vault_token' infra/06-observability/prometheus/config/prometheus.yml`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Prometheus image, runtime flags, scrape jobs, alert rules, recording rules,
  secret references, route, retention, or mounted paths change.
- Regular review follows quarterly cadence.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/prometheus.md)
- [Recovery runbook](../../runbooks/06-observability/prometheus.md)
- [Retention policy](./retention.md)
