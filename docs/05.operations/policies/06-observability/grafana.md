---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/grafana.md -->

# Grafana Operational Policy (06-observability) Operations Policy

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

- [Grafana System Usage](../../guides/06-observability/grafana.md)
- [Loki Operational Policy (Retention)](./loki.md)

---

## Overview

이 문서는 `docs/05.operations/policies/06-observability/grafana.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

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

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/grafana.md)
- [Recovery runbook](../../runbooks/06-observability/grafana.md)
