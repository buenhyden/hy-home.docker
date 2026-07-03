# Pushgateway

> Metrics buffer for ephemeral and batch jobs within the `06-observability` tier.

## Overview

Pushgateway allows ephemeral and batch jobs to expose metrics to Prometheus in cases where the standard pull model is not feasible (e.g., short-lived CI/CD tasks or batch scripts). It acts as a temporary buffer that Prometheus scrapes at its own pace.

## Audience

이 README의 주요 독자:

- DevOps Engineers
- Backend Developers (Batch/CI)
- AI Agents

## Scope

### In Scope

- Pushgateway service configuration and deployment.
- Metrics ingestion and exposure for ephemeral jobs.
- Integration with Prometheus scraping.

### Out of Scope

- General-purpose metrics proxy or long-term storage.
- High-cardinality time-series storage (use direct instrumentation where possible).

## Structure

```text
pushgateway/
└── README.md           # This file
```

## Tech Stack

| Category | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| Buffer | [prom/pushgateway](https://hub.docker.com/r/prom/pushgateway) | v1.11.3 | Metrics ingestion buffer |
| Ingress | [Traefik](../../01-gateway/README.md) | v3.3.4 | SSL Termination & Routing |
| Scraper | [Prometheus](../prometheus/README.md) | v3.13.0 | Scrape-to-pull bridge |

## Usage Instructions

### Pushing Metrics

Jobs can push metrics via simple HTTP POST/PUT requests:

```bash
echo "some_metric 42" | curl --data-binary @- http://pushgateway:9091/metrics/job/some_job
```

## Configuration

- **Ingestion**: Standard Prometheus Pushgateway API (Port 9091).
- **Exposure**: Accessible via `pushgateway.${DEFAULT_URL}` with SSL.
- **Network**: Integrated into `infra_net`.

## Operational Status

> [!CAUTION]
> Pushgateway is **not** a general-purpose proxy. Metrics persist in the gateway until explicitly deleted or overwritten. Unmanaged metric growth can lead to memory exhaustion and performance degradation.

## AI Agent Guidance

1. **PromQL Optimization**: When querying metrics from Pushgateway, always include the `job` label to distinguish between different batch runs.
2. **Maintenance**: Periodically check for stale metrics that haven't been updated.
3. **Traceability**: Refer to the dedicated guide for complex TTL or cleanup logic.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify metric push by checking `docker logs pushgateway | grep -i 'error\|warn'` and confirming pushed metrics appear in the Pushgateway UI.
- Confirm Prometheus scrapes Pushgateway by verifying the target appears UP in the Prometheus Targets page.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For push errors: validate the push URL format (`http://pushgateway:9091/metrics/job/<job>`) and confirm network connectivity from the pushing service.
- For stale metrics: use the Pushgateway UI to delete stale job groups; configure `--persistence.file` for persistence across restarts.
- For scrape errors: verify the Pushgateway scrape job is defined in `prometheus.yml` and the target is reachable.

## Related Documents

- [System Guide](../../../docs/05.operations/guides/06-observability/pushgateway.md)
- [Operational Policy](../../../docs/05.operations/policies/06-observability/pushgateway.md)
- [Recovery Runbook](../../../docs/05.operations/runbooks/06-observability/pushgateway.md)

---

Copyright (c) 2026. Licensed under the MIT License.

---

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
