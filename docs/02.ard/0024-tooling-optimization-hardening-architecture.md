# 09-Tooling Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `09-tooling` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 관리 경로의 gateway+SSO 경계, tooling 네트워크 격리, 테스트 도구 runtime 안정성, 카탈로그 기반 확장 정책을 아키텍처 관점으로 정리한다.

## Summary

Tooling tier는 플랫폼 운영 품질을 담당하는 control plane 성격의 서비스 집합이다.

- IaC: terraform/terrakube
- Quality: sonarqube
- Performance: k6/locust
- Artifact/Data sync: registry/syncthing

모든 공개 관리 경로는 Traefik TLS 경계 뒤에서 정책 통제되어야 한다.

## Boundaries & Non-goals

- **Owns**:
  - tooling 공개 라우터 gateway/SSO 경계 계약
  - tooling 네트워크 경계(`infra_net` external) 계약
  - 테스트 도구(locust/k6) runtime 안정성 계약
  - tooling 하드닝 CI 정책 게이트
  - 09-tooling 카탈로그 확장 로드맵
- **Consumes**:
  - `01-gateway` middleware chain
  - `02-auth` SSO middleware
  - `04-data` PostgreSQL/Valkey/MinIO/InfluxDB
- **Does Not Own**:
  - 각 도구의 비즈니스 도메인 로직
  - 카탈로그 항목의 전면 구현 완료 상태
- **Non-goals**:
  - 즉시 멀티클러스터 toolchain 운영
  - 신규 툴체인 도입/교체

## Quality Attributes

- **Performance**: locust/k6 분산 실행의 최소 runtime 안정성 계약을 확보한다.
- **Security**: 공개 tooling UI에 gateway+SSO 체인을 강제한다.
- **Reliability**: worker healthcheck/compose 계약으로 startup 안정성을 강화한다.
- **Scalability**: 카탈로그 기반으로 성능 회귀 baseline/분산 토폴로지 표준화를 준비한다.
- **Observability**: tooling hardening script + CI gate로 회귀를 조기 탐지한다.
- **Operability**: 정책/가이드/런북 연계를 통해 변경/복구를 표준화한다.

## System Overview & Context

- **Ingress path**:
  - Operator/Developer -> Traefik(websecure) -> SonarQube/Terrakube/Syncthing
- **Execution plane**:
  - terraform job container
  - terrakube api/ui/executor
  - locust master/worker, k6 service
- **Shared dependencies**:
  - PostgreSQL, Valkey, MinIO, InfluxDB, Keycloak

## Data Architecture

- **Key Entities / Flows**:
  - tfstate/workspace metadata, quality gate results, perf metrics, image artifacts, sync metadata
- **Storage Strategy**:
  - registry/syncthing/sonarqube/persistence는 bind volume + data tier backend를 사용
- **Data Boundaries**:
  - tooling tier는 운영 도구 메타데이터와 실행 정책을 소유한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose (`infra/09-tooling/*`)
- **Deployment Model**:
  - 서비스별 독립 compose + 공통 template(`common-optimizations.yml`)
- **Operational Evidence**:
  - compose static checks
  - `scripts/check-tooling-hardening.sh`
  - CI `tooling-hardening` job

## Catalog-aligned Expansion Targets

- **terraform**: plan/apply 승인 게이트, state 잠금/백업 강화, drift 자동 탐지
- **terrakube**: workspace 분리, 실행 권한 제어, 감사 로그 연동
- **registry**: cosign 기반 서명/검증, 취약점 스캔 실패 차단 정책
- **sonarqube**: 품질게이트 임계값 재정의, 브랜치/보안 룰셋 분리
- **k6**: 성능 회귀 baseline 저장/비교 자동화, 시나리오 태그 표준화
- **locust**: 분산 토폴로지 표준화, 테스트 데이터 초기화/정리 루틴
- **syncthing**: 폴더 ACL/암호화 강화, 충돌 파일 처리 정책 명문화

## Related Documents

- **PRD**: [../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **Spec**: [../04.specs/09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Plan**: [../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md](../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/09-tooling/optimization-hardening.md](../07.guides/09-tooling/optimization-hardening.md)
- **Operation**: [../08.operations/09-tooling/optimization-hardening.md](../08.operations/09-tooling/optimization-hardening.md)
- **Runbook**: [../09.runbooks/09-tooling/optimization-hardening.md](../09.runbooks/09-tooling/optimization-hardening.md)
