---
title: "Prometheus Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0045"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Prometheus Operations Policy

관련 구성요소의 현재 선언은 [버전 레지스트리](../../../../../infra/tech-stack.versions.json)가 가리키는 Compose 원본에서 확인합니다.

## Overview

This policy defines Prometheus controls for scrape target registration, alerting
rule management, TSDB persistence, lifecycle reload, secret file references, and
protected access. Ordered recovery or reload procedures belong in the matching
runbook.

## Policy Scope

This policy applies to the current `infra/06-observability/prometheus` compose,
config, and alert-rule surfaces.

- **Systems**: compose service `prometheus`, container `infra-prometheus`, image [Compose image declaration](../../../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/prometheus/config/prometheus.yml`, rules directory `infra/06-observability/prometheus/config/alert_rules`, volume `prometheus-data`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Prometheus service는 `template-stateful-high`, image
    [Compose image declaration](../../../../../infra/06-observability/docker-compose.yml), tmpfs `/tmp` and `/etc/prometheus:size=10M`,
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
    `/etc/prometheus/alert_rules/alert_rules.keycloak.yml`,
    `/etc/prometheus/alert_rules/alert_rules.vault.yml`, and
    `/etc/prometheus/alert_rules/recording_rules.yml`.
  - Alert rules must include `expr`, `for` when applicable, `labels.severity`,
    and actionable `annotations`.
  - `opensearch_exporter_password` and `openbao_token` are Docker Secret file
    references only; their values must not appear in docs, logs, or task
    evidence.
    Active Prometheus neither declares nor mounts it; preserve any existing
    private value until separately approved migration closeout, revocation, and
    file disposition.
  - `SEC-002` / `openbao_token` is a manual least-privilege OpenBao
    `prometheus`-policy credential contract. Source declaration does not prove
    a token was issued, loaded by the running container, or produced an UP
    scrape target.
  - Prometheus route must keep
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - The `prometheus-api` route admits only `/api/v1/` on the Prometheus host,
    behind `prometheus-api-auth@file` (Basic Auth from `INFRA-007`, derived
    from `OBS-012`/`OBS-013`). It serves machine clients that cannot pass SSO,
    such as the hy-home.k8s cluster's remote write and Kiali queries. The UI
    and every other path stay behind SSO, and the admin API stays disabled.
  - TSDB retention changes must be paired with
    [retention policy](../0048-telemetry-retention/policy.md), volume impact review, and plan/task
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
  - Widening the `prometheus-api` rule beyond `/api/v1/`, enabling
    `--web.enable-admin-api` while that route exists, or publishing an
    unauthenticated Prometheus host port
  - Declaring retention behavior that is not backed by compose/config and the
    retention policy

### Lifecycle and data controls

- Keep Prometheus `HOME`; retain gateway auth, least-privilege scrape secrets, validated rules, and the declared local TSDB boundary.
- Back up `prometheus-data` only with an approved consistent stopped copy/snapshot under current source. Do not call `/api/v1/admin/tsdb/snapshot` unless `--web.enable-admin-api` is separately reviewed and enabled.
- Rehearse against isolated TSDB storage and no production remote-write/alerts. Verify WAL replay, historical/current queries, target labels, rule evaluation, Alertmanager delivery, and any remote-write receiver clients.
- Resource/retention changes require measured disk growth, query/scrape pressure, and rollback thresholds. Removal requires scraper/client migration and explicit TSDB-retention/deletion approval.

## Exceptions

- Scrape interval, retention, secret reference, route, or rule-loading
  exceptions require user approval and related plan/task evidence.
- Emergency reload or target suppression must be recorded through the Prometheus
  runbook with rollback evidence.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: prom/prometheus:|--web.enable-lifecycle|--web.enable-remote-write-receiver|prometheus-data|opensearch_exporter_password|openbao_token|prometheus.middlewares' infra/06-observability/docker-compose.yml`
- Prometheus config:
  `rg -n 'scrape_interval: 30s|evaluation_interval: 30s|rule_files:|alert_rules.local|recording_rules.yml|password_file: "/run/secrets/opensearch_exporter_password"|bearer_token_file: /run/secrets/openbao_token' infra/06-observability/prometheus/config/prometheus.yml`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- Prometheus image, runtime flags, scrape jobs, alert rules, recording rules,
  secret references, route, retention, or mounted paths change.
- Regular review follows quarterly cadence.

## Traceability

- Declared parent: [Observability Architecture Description](../../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](guide.md) (`GDE-0045`), [Runbook](runbook.md) (`RUN-0045`)

## Related Documents

- [Runtime image declarations](../../../../../infra/06-observability/docker-compose.yml)
- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Retention policy](../0048-telemetry-retention/policy.md)
