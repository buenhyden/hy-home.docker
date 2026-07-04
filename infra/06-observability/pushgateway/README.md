# Pushgateway

## Overview

Pushgateway allows ephemeral and batch jobs to expose metrics to Prometheus in cases where the standard pull model is not feasible (e.g., short-lived CI/CD tasks or batch scripts). It acts as a temporary buffer that Prometheus can scrape when the matching scrape job is configured.

## Audience

이 README의 주요 독자:

- DevOps Engineers
- Backend Developers (Batch/CI)
- AI Agents

## Scope

### In Scope

- Pushgateway service configuration and deployment.
- Metrics ingestion and exposure for ephemeral jobs.
- Prometheus scraping contract and verification.

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
| Scraper | [Prometheus](../prometheus/README.md) | v3.13.0 | Expected scrape-to-pull bridge; verify the scrape job before depending on pushed metrics |

## Usage Instructions

### Starting the Service

From the repository root, start or restart Pushgateway through the observability profile:

```bash
docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d pushgateway
docker compose -f infra/06-observability/docker-compose.yml --profile obs restart pushgateway
```

### Pushing Metrics

Jobs can push metrics via simple HTTP POST/PUT requests:

```bash
echo "some_metric 42" | curl --data-binary @- http://pushgateway:9091/metrics/job/some_job
```

## Configuration

- **Ingestion**: Standard Prometheus Pushgateway API (Port 9091).
- **Exposure**: Accessible via `https://pushgateway.${DEFAULT_URL}` through the protected Traefik route.
- **Network**: Integrated into `infra_net`.
- **Persistence**: No Pushgateway persistence option is declared in the current Compose service.

## Operational Status

> [!CAUTION]
> Pushgateway is **not** a general-purpose proxy. Metrics persist in the gateway until explicitly deleted or overwritten. Unmanaged metric growth can lead to memory exhaustion and performance degradation.

## AI Agent Guidance

1. **PromQL Optimization**: When querying metrics from Pushgateway, always include the `job` label to distinguish between different batch runs.
2. **Maintenance**: Periodically check for stale metrics that haven't been updated.
3. **Traceability**: Refer to the dedicated guide and runbook for cleanup logic and evidence capture.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify metric push by checking `docker logs --tail=200 pushgateway` and confirming pushed metrics appear in the Pushgateway UI.
- Before relying on Prometheus dashboards or alerts, confirm a Pushgateway scrape job exists in `infra/06-observability/prometheus/config/prometheus.yml` and the target appears UP in the Prometheus Targets page.

## Troubleshooting

- Start with `docker compose -f infra/06-observability/docker-compose.yml --profile obs config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For push errors: validate the push URL format (`http://pushgateway:9091/metrics/job/<job>`) and confirm network connectivity from the pushing service.
- For stale metrics: use the Pushgateway UI or runbook DELETE commands to remove stale job groups.
- For persistence requirements: treat `--persistence.file` as a runtime configuration change and update the policy, runbook, and Compose evidence before enabling it.
- For scrape errors: verify the Pushgateway scrape job is defined in `prometheus.yml`; if it is absent, record an implementation gap instead of treating Pushgateway as down.

## Related Documents

- [Usage guide](../../../docs/05.operations/guides/06-observability/pushgateway.md)
- [Operations policy](../../../docs/05.operations/policies/06-observability/pushgateway.md)
- [Recovery runbook](../../../docs/05.operations/runbooks/06-observability/pushgateway.md)

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
