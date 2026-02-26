# [SPEC-SYS-01] Infrastructure Hardening & Optimization

## 1. Non-Functional Requirements (NFR) [REQ-SPT-05]

- **NFR-SEC-01 (Isolation)**: All containers MUST NOT have access to the host pid, network, or ipc namespaces unless explicitly justified in an ADR.
- **NFR-OBS-01 (Latency)**: Loki log ingestion latency SHALL be < 2 seconds for all local docker events.
- **NFR-RES-01 (Density)**: Infrastructure services MUST collectively utilize < 20% of system memory under idle conditions.

## 2. Storage Strategy [REQ-SPT-05]

- **Strategy-ST-01**: Sensitive credentials SHALL be stored as Docker Secrets (`/run/secrets/`).
- **Strategy-ST-02**: Persistent volume mounts MUST utilize the `infra_net` for distributed data access where applicable.
- **Strategy-ST-03**: Bind mounts MUST be `ro` (read-only) unless write access is functionally required.

## 3. Interfaces

- **Internal**: Every service SHALL expose metrics via an OTLP-compatible endpoint or Prometheus exporter.
- **External**: Public access MUST be routed through Traefik using TLS v1.2+.

## 4. Security Implementation [REQ-SPT-05]

- **Anchors**: Implementation utilizes local YAML anchors (`&security-baseline`) to enforce `no-new-privileges` and `cap_drop: ALL`.
- **Identity**: Root execution inside containers is STRICTLY PROHIBITED.

## 5. Ops & Observability [REQ-SPT-05]

- **Telemetry**: LGTM Stack (Loki, Grafana, Tempo, Pyroscope) serves as the primary observability plane.
- **Alerting**: Alertmanager SHALL trigger Slack notifications for any `hy-home.tier: infra` service downtime.

## 6. Verification Plan [REQ-SPT-10]

- **AC-SPEC-01 (Security Audit)**:
  - **Given**: A service deployed via standardized templates.
  - **When**: Running `docker inspect --format '{{.HostConfig.SecurityOpt}}' <container>`.
  - **Then**: Output MUST include `no-new-privileges:true`.
- **AC-SPEC-02 (Observability Integrity)**:
  - **Given**: A service crash or log event.
  - **When**: Searching Loki with `{job="infra", tier="gateway"}`.
  - **Then**: Relevant logs MUST be returned within 5 seconds of the event.
- **AC-SPEC-03 (Resource Ceiling)**:
  - **Given**: System at 80% CPU load.
  - **When**: Monitoring Prometheus `container_memory_usage_bytes`.
  - **Then**: Baseline infrastructure services MUST NOT exceed their defined memory limits.
