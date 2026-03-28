# 09-Tooling Optimization Hardening Technical Specification

## Overview (KR)

이 문서는 `infra/09-tooling` 계층(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)의 최적화/하드닝 기술 명세다. 공개 경계 보안, 네트워크 격리, 테스트 런타임 안정성, CI 정책 게이트, 카탈로그 기반 확장 항목을 구현 계약으로 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - tooling 공개 라우터 middleware 계약
  - tooling compose 네트워크 경계 계약
  - locust/k6 runtime 계약(health/volume)
  - `check-tooling-hardening.sh` 정책 게이트 계약
- **Does Not Own**:
  - 각 도구의 도메인 기능 구현 세부
  - 카탈로그 확장 항목의 즉시 전면 구현
  - 신규 도구 도입/교체

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../../02.ard/0024-tooling-optimization-hardening-architecture.md](../../02.ard/0024-tooling-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0009-tooling-services.md](../../03.adr/0009-tooling-services.md)
  - [../../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md](../../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - SonarQube/Terrakube/Syncthing 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 사용한다.
  - registry/sonarqube/terrakube/syncthing/locust/k6/terraform compose는 `infra_net` external 경계를 명시한다.
  - locust-worker는 worker 프로세스 healthcheck를 가진다.
  - k6는 `k6-data` 볼륨을 기준 경로(`/mnt/locust`)에 마운트한다.
- **Data / Interface Contract**:
  - tooling 서비스는 기존 PostgreSQL/Valkey/MinIO/InfluxDB 연계를 유지한다.
- **Governance Contract**:
  - `scripts/check-tooling-hardening.sh` 통과가 tooling tier 하드닝 기준선이다.
  - CI `tooling-hardening` job이 PR 단계에서 회귀를 차단한다.

## Core Design

- **Gateway Security Plane**:
  - 공개 tooling UI는 TLS 종료 후 gateway 표준 체인 + SSO 체인을 강제한다.
- **Network Isolation Plane**:
  - tooling compose는 공통 `infra_net` external 경계를 명시적으로 선언한다.
- **Runtime Stability Plane**:
  - locust worker healthcheck와 k6 volume 계약을 최소 안정성 기준으로 적용한다.
- **Policy Gate Plane**:
  - tooling hardening checker + CI job으로 변경 회귀를 조기 차단한다.

## Data Modeling & Storage Strategy

- registry/sonarqube/syncthing/k6/locust는 기존 bind volume 전략을 유지한다.
- terrakube/terraform은 기존 state/artifact 데이터 경계를 유지한다.
- drift/승격 정책은 operations/tasks에서 단계적으로 강화한다.

## Interfaces & Data Structures

### Tooling Hardening Control Surface

```yaml
tooling_hardening_controls:
  ingress_security:
    sonarqube: gateway-standard-chain + sso-errors + sso-auth
    terrakube_api: gateway-standard-chain + sso-errors + sso-auth
    terrakube_ui: gateway-standard-chain + sso-errors + sso-auth
    terrakube_executor: gateway-standard-chain + sso-errors + sso-auth
    syncthing: gateway-standard-chain + sso-errors + sso-auth
  network_boundary:
    compose_network: infra_net (external)
  runtime_stability:
    locust_worker_healthcheck: required
    k6_volume_contract: k6-data -> /mnt/locust
```

## Edge Cases & Error Handling

- SSO 체인 강화로 기존 자동화 접근 경로가 차단될 수 있으므로 운영 예외 절차를 적용한다.
- locust-worker healthcheck 오탐 시 worker 프로세스 기준으로 재조정한다.
- k6 시나리오 미존재로 실행 실패 시 baseline 시나리오 준비 태스크를 별도 추적한다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: tooling UI 접근 정책 회귀
  - **Fallback**: 최근 정상 middleware 설정으로 롤백
  - **Human Escalation**: Gateway/Auth 운영 승인자
- **Failure Mode**: locust worker 재시작 루프
  - **Fallback**: healthcheck/worker command 계약 재적용
  - **Human Escalation**: Performance tooling owner
- **Failure Mode**: k6 실행 데이터 경로 불일치
  - **Fallback**: `k6-data` volume 계약 복원
  - **Human Escalation**: DevOps on-call

## Verification

```bash
docker compose -f infra/09-tooling/registry/docker-compose.yml config
docker compose -f infra/09-tooling/sonarqube/docker-compose.yml config
docker compose -f infra/09-tooling/terrakube/docker-compose.yml config
docker compose -f infra/09-tooling/syncthing/docker-compose.yml config
docker compose -f infra/09-tooling/locust/docker-compose.yml config
docker compose -f infra/09-tooling/k6/docker-compose.yml config
docker compose -f infra/09-tooling/terraform/docker-compose.yml config
bash scripts/check-tooling-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-TLG-001**: tooling compose static validation 통과
- **VAL-TLG-002**: tooling hardening baseline script 실패 0건
- **VAL-TLG-003**: PRD~Runbook optimization-hardening 문서 링크 정합성 유지
- **VAL-TLG-004**: 카탈로그 `09-tooling` 확장 항목이 Plan/Tasks/Operations에 반영

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/09-tooling/optimization-hardening.md](../../07.guides/09-tooling/optimization-hardening.md)
- **Operation**: [../../08.operations/09-tooling/optimization-hardening.md](../../08.operations/09-tooling/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/09-tooling/optimization-hardening.md](../../09.runbooks/09-tooling/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
