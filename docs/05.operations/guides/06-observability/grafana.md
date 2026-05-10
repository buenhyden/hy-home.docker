# Grafana Operational Policy (06-observability)

Policies and procedures for maintaining the visualization and alerting hub.

## Dashboard Provisioning

1. **Code-First Mandate**: All production dashboards MUST be stored as JSON files in `infra/06-observability/grafana/dashboards/`.
2. **Directory Structure**:
   - `provisioning/dashboards/dashboards.yml`: Configuration for the dashboard provider.
   - `dashboards/`: Directory containing all `.json` dashboard definitions.
3. **Standard Headers**: Dashboards should include a standardized title, version, and appropriate template variables (e.g., `$job`, `$instance`).
4. **Lock Policy**: Provisioned dashboards are immutable in the UI to prevent drift. Changes must be committed to git.
5. **Adding a New Dashboard**:
   - Place the JSON file in `infra/06-observability/grafana/dashboards/`.
   - Ensure a unique `uid` is set in the JSON to prevent collisions.
   - Restart Grafana or wait for the provider to re-scan.

## RBAC Management

- **External Groups**: User access is exclusively managed through Keycloak groups (`/admins`, `/editors`).
- **Admin Access**: Limited to core infrastructure maintainers.
- **Editor Access**: Granted to developers for creating/testing new visualization patterns in development.

## Maintenance Procedures

### Datasource Management

New datasources must be added via `infra/06-observability/grafana/provisioning/datasources/datasource.yml`. Avoid manual datasource creation to ensure service portability and reliability. Note the `uid` mapping (e.g., `Prometheus`, `Loki`, `Tempo`) used in dashboard references.

### Version Upgrades

Grafana version updates are managed via `docker-compose.yml`. Before upgrading, verify compatibility with existing plugins and OIDC mapping logic.

### Backup & Persistence

- **Data Volume**: The `/var/lib/grafana` directory is persisted via a Docker volume (`grafana-data`).
- **Dashboard Backup**: Since dashboards are provisioned from git, recovery is as simple as restarting the container with the correct volume mount.

## References

- [Grafana System Usage](./grafana.md)
- [Loki Operational Policy (Retention)](./loki.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/06-observability/grafana.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Usage

> Migrated from `docs/05.operations/06-observability/grafana.md` during the 2026-05-10 operations taxonomy consolidation.

### Grafana System Usage (06-observability)

Unified visualization and observability hub for the `hy-home.docker` ecosystem.

#### Vision

To provide a single, unified observability portal that integrates metrics, logs, traces, and profiles across all infrastructure layers and services, ensuring rapid incident response and data-driven operational decisions.

#### Architecture

Grafana is the visualization frontend of the LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus). It functions as a stateless service that pulls data from multiple backends.

##### Key Components

- **Grafana Core**: v12.3.3 (OSS edition).
- **Provisioning System**: Uses YAML/JSON definitions for declarative management.
- **Datasource Integrations**:
  - **Prometheus**: Metrics ingestion point (`uid: Prometheus`).
  - **Loki**: Log aggregation and search (`uid: Loki`).
  - **Tempo**: Distributed tracing frontend with Log/Metric linking (`uid: Tempo`).
  - **Pyroscope**: Continuous profiling visualization (`uid: Pyroscope`).
  - **Alertmanager**: External alert status and silencing (`uid: alertmanager`).

##### Authentication & Authorization

- **Primary URL**: `https://grafana.${DEFAULT_URL}`
- **Authentication**: Keycloak SSO (OIDC) with automatic role mapping.
  - `/admins` group members are mapped to Grafana **Admin**.
  - `/editors` group members are mapped to Grafana **Editor**.
  - All other authenticated users default to **Viewer**.
- **Role Sync**: Managed via `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`.

#### Dashboards Catalog

The `hy-home.docker` ecosystem includes 34+ provisioned dashboards, categorized as follows:

- **Infrastructure**:
  - `Node Exporter Full`: Comprehensive host metrics.
  - `cAdvisor Exporter`: Container-level resource usage.
  - `Docker Dashboard`: Engine-level stats.
- **Middleware**:
  - `PostgreSQL Database`: Query performance and connection pooling.
  - `Redis Overview`: Cache hit rates and memory usage.
  - `Kafka Overview`: Broker health and topic throughput.
- **AI & Vector DB**:
  - `Ollama Exporter`: LLM inference performance.
  - `Qdrant Overview`: Vector search latency and index size.
- **Legacy/Other**:
  - Integrated dashboards from various community sources (e.g., dashboard IDs 15983, 1860, etc.).

#### Integration Patterns

##### Trace-to-Log Linking

Tempo is configured to provide links to Loki logs based on Trace ID, Span ID, and common labels (`job`, `instance`, `container_name`). This allows seamless navigation from a slow trace directly to the relevant container logs.

##### Service Graph

Service dependency graphs are generated by Tempo using metrics stored in Prometheus, providing a visual representation of system interactions.

#### References

- [Keycloak SSO Usage](../02-auth/keycloak.md)
- [Datasource Provisioning](../../../../infra/06-observability/grafana/provisioning/datasources/datasource.yml)

---

#### Overview (KR)

이 문서는 `docs/05.operations/06-observability/grafana.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Procedure

> Migrated from `docs/05.operations/06-observability/grafana.md` during the 2026-05-10 operations taxonomy consolidation.

### Grafana Recovery Procedure (06-observability)

Standardized procedures for resolving common Grafana service disruptions.

#### SSO Authentication Failures

##### Symptom: "OAuth Login Failed" or redirection loops

1. **Verify Keycloak Status**: Ensure the Keycloak service is healthy and reachable.
2. **Check Secrets**: Ensure `oauth2_proxy_client_secret` is correctly loaded as a secret in the `06-observability` tier.
3. **Inspect Logs**: Check Grafana logs for OAuth2 token validation errors:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml logs grafana | grep -i "oauth"
   ```

4. **Group Synchronization**: If a user has incorrect roles, verify their group membership in Keycloak. Groups must start with `/admins` or `/editors`.
5. **Time Sync**: Ensure clocks are synchronized between Grafana and Keycloak (NTP check).

#### Datasource Connection Issues

##### Symptom: Dashboard panels show "Datasource not found" or "Query error"

1. **Verify Backend Status**: Check if Prometheus, Loki, or Tempo containers are running and healthy.
2. **Check UID Matching**: Ensure the dashboard expects the same `uid` defined in `datasource.yml` (e.g., `Prometheus` vs `prometheus`).
3. **Trace-to-Log Link Break**: If "Logs" button disappears in Tempo, verify `tracesToLogsV2` configuration in `datasource.yml`.

#### Dashboard Provisioning Issues

1. **Verify Volume Mount**: Ensure `./grafana/dashboards` is correctly mounted to `/etc/grafana/dashboards`.
2. **Check YAML Config**: Inspect `infra/06-observability/grafana/provisioning/dashboards/dashboards.yml` for correct path references.
3. **Grafana Refresh**: Restart the Grafana service to force a re-scan of the provisioning directory:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml restart grafana
   ```

#### Service Unavailability

##### Symptom: HTTP/503 or healthcheck failed

1. **Resource Check**: Verify Grafana memory usage. By default, it is limited to 1GB.
2. **Database Integrity**: Check `/var/lib/grafana/grafana.db` (SQLite) for corruption if the service fails to start.
3. **Healthcheck Probe**: Run the healthcheck command manually:

   ```bash
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

#### References

- [Grafana System Usage](./grafana.md)
- [Keycloak Recovery Procedure](../02-auth/keycloak.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/06-observability/grafana.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
