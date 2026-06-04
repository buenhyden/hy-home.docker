# [INFRA] 06-observability: prometheus

> High-performance time-series database for system and application metrics.

## Scope

Prometheus is the core metrics engine for the `hy-home.docker` platform. It scrapes targets defined via service discovery, stores time-series data, and evaluates alerting rules. It supports high-cardinality data and provides a powerful query language (PromQL).

- **Role**: Metrics Aggregation & Alerting Engine.
- **Layer**: `06-observability` (Telemetry Storage).
- **Interface**: [http://prometheus.hy-home.local](http://prometheus.hy-home.local) (via Traefik).

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Metrics DB | Prometheus | v3.12.0 |
| Configuration | YAML-based | Static & File-based SD |
| Tooling | promtool | Config/Rule Validation |

## System Components

- **Scrape Configs**: Defined in `config/prometheus.yml` (20+ internal & infra jobs).
- **Alerting Rules**: Modularized in `config/alert_rules/` (9+ files by domain).
- **Storage**: Persistent TSDB volume with retention policies.

## Management Guide

### 1. Operations & Configuration

- **Scrape Targets**: Update `scrape_configs` in `prometheus.yml`.
- **Alerting Rules**: Add/Modify YAML files in `config/alert_rules/`.
- **Validation**:

  ```bash
  docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
  ```

### 2. Traceability

- **System Guide**: [docs/05.operations/guides/06-observability/prometheus.md](../../../docs/05.operations/guides/06-observability/prometheus.md)
- **Operations Policy**: [docs/05.operations/policies/06-observability/prometheus.md](../../../docs/05.operations/policies/06-observability/prometheus.md)
- **Runbook**: [docs/05.operations/runbooks/06-observability/prometheus.md](../../../docs/05.operations/runbooks/06-observability/prometheus.md)

## AI Agent Guidance

1. **PromQL Optimization**: Use Recording Rules for expensive dashboard queries.
2. **Rule Management**: Always validate with `promtool` before applying changes.
3. **Scrape Settings**: Standard intervals: 15s (infra), 30s-60s (apps).
4. **Networking**: Scrape targets must be reachable via the `infra_net`.

---

## Overview

`infra/06-observability/prometheus`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Structure

```text
infra/06-observability/prometheus/
├── config/  # 하위 구성 영역
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify scrape targets are UP by checking the Prometheus UI Targets page after `prometheus.yml` changes.
- Confirm alert rules load correctly by checking `docker logs prometheus | grep -i 'error\|warn'`.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For scrape errors: validate `prometheus.yml` scrape configs and confirm target endpoints are reachable from the Prometheus container.
- For alert rule errors: check YAML syntax in rule files and verify the `rule_files` paths are correctly mounted.
- For storage issues: confirm the Prometheus data volume is mounted and has sufficient disk space.

## Related Documents

- [infra/README.md](../../README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
