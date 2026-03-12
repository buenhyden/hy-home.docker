# Operations Index

This document is the central index for the `hy-home.docker` operational policies and execution frameworks.

- **Design reference:** [`ARCHITECTURE.md`](ARCHITECTURE.md) (Architecture principles)
- **Product vision:** [`docs/prd/README.md`](docs/prd/README.md) (Project goals)
- **Executable manuals:** [`runbooks/README.md`](runbooks/README.md) (Incident response by tier)
- **Shared memory:** [`operations/README.md`](operations/README.md) (Postmortem and incident archives)

---

## 1. Environment Tiers

| Tier | Name | Target Hardware | Purpose |
| :--- | :--- | :--- | :--- |
| **L1** | Local Dev | Host Laptop | Service iteration and specification validation. |
| **L2** | Home-Lab | Dedicated Server | Integration testing and 24/7 availability. |
| **L3** | Pro-Lab | High-spec Host | Performance benchmarking and recovery drills. |

## 2. Operational Principles

1. **Runbook-first:** Follow procedures defined in [`runbooks/`](runbooks/) before executing commands manually.
2. **Validate-then-apply:** Run [`scripts/validate-docker-compose.sh`](scripts/validate-docker-compose.sh) before every modification.
3. **Secrets hygiene:** 100% of sensitive data must flow through Docker Secrets at `/run/secrets/`.
4. **Blameless culture:** Perform a blameless postmortem ([operations/postmortems/](operations/postmortems/)) for all SEV-1/2 incidents.

## 3. Incident Severity & Response

| Severity | Impact | Action | Tracking Hub |
| :--- | :--- | :--- | :--- |
| **SEV-1** | Core failure (Gateway/Auth) | Immediate response via `runbooks/core/`. | [Incident History](operations/incidents/) |
| **SEV-2** | Service degradation (DB/Data) | Response within 4 hours. | [Incident History](operations/incidents/) |
| **SEV-3** | Minor/Intermittent issue | Log via GitHub Issues. | N/A |

## 4. Observability & Monitoring

- **Log centralization:** All services must use the `loki` driver. Perform queries via [Grafana Explore](https://grafana.${DEFAULT_URL}/explore).
- **Metric collection:** Prometheus scrapes exporters every 15 seconds. Standard dashboards are in [`infra/06-observability/grafana/dashboards/`](infra/06-observability/grafana/dashboards/).
- **Alerting:** Alertmanager routes critical alerts to configured messengers. Logic is defined in [`runbooks/alerting/`](runbooks/alerting/).

## 5. Backup & Disaster Recovery

- **DB snapshots:** Automated nightly dumps for PostgreSQL and OpenSearch are saved to `/mnt/backup/db/`.
- **Secret backups:** Encrypted copies of `.env` and `secrets/` are stored in an offline-first tier.
- **Recovery SLO:** Core Auth/Gateway services must be restorable within 30 minutes from L2/L3 hardware.

## 6. Project References

- **Infra lifecycle:** [`docs/context/core/infra-lifecycle-ops.md`](docs/context/core/infra-lifecycle-ops.md)
- **Security policy:** [`.github/SECURITY.md`](.github/SECURITY.md)
- **RCA hub:** [`operations/postmortems/README.md`](operations/postmortems/README.md)

---
> [!TIP]
> Keep detailed operational logic in the `runbooks/` directory instead of this index document.
