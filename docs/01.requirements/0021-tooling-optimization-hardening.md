---
profile_id: requirements-package
status: active
artifact_id: REQ-0021
artifact_type: requirements-package
parent_ids: []
created: 2026-03-28
updated: 2026-09-01
---
# 09-Tooling Optimization & Hardening Product Requirements

## Problem and Goals

이 문서는 `infra/09-tooling` 계층(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)의 최적화/하드닝 요구사항을 정의한다. 목표는 관리 경로 보안 강화, 네트워크 경계 명확화, 테스트/운영 도구 안정성 향상, 그리고 카탈로그 기반 확장 항목의 실행 로드맵 수립이다.

## Stakeholders and User Needs

Tooling tier를 "기본적으로 안전하고, 운영 감사가 가능하며, 성능/품질 회귀를 조기에 차단하는" 플랫폼 엔지니어링 기반 계층으로 표준화한다.

## Problem Statement

- 일부 공개 tooling 라우터가 gateway 표준 체인만 적용하고 SSO 체인을 누락해 접근 통제가 불균일하다.
- tooling compose의 네트워크 경계 선언이 서비스마다 일관되지 않아 운영 환경 drift가 발생할 수 있다.
- locust/k6 테스트 구성에서 runtime 계약(healthcheck/volume 참조) 편차가 존재한다.
- tooling tier 하드닝 회귀를 PR 단계에서 차단하는 전용 정책 게이트가 부재하다.
- 카탈로그가 요구한 terraform/terrakube/registry/sonarqube/k6/locust/syncthing 확장 항목이 실행 문서로 충분히 연결되지 않았다.

## Personas

- **Platform SRE**: 내부 운영 도구의 보안/가용성/감사성을 동시에 관리해야 한다.
- **DevOps Engineer**: IaC/품질/성능 도구를 표준 정책으로 유지해야 한다.
- **Platform Product Owner**: 도구별 승인 게이트와 확장 정책을 관리해야 한다.

## Key Use Cases

- **STORY-TLG-01**: 운영자는 tooling UI 경로가 gateway+SSO 정책을 준수하는지 검증한다.
- **STORY-TLG-02**: 엔지니어는 locust/k6 분산 테스트 구성을 안정적으로 운영하고 회귀를 차단한다.
- **STORY-TLG-03**: CI는 tooling tier 하드닝 회귀를 PR 단계에서 자동 차단한다.
- **STORY-TLG-04**: 팀은 카탈로그 확장 항목을 Plan/Tasks/Operations에서 추적한다.

## Functional Requirements

- **REQ-0021-FR-0001**: SonarQube/Terrakube/Syncthing 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용해야 한다.
- **REQ-0021-FR-0002**: tooling compose는 `infra_net` external 경계 선언을 명시해야 한다.
- **REQ-0021-FR-0003**: locust-worker는 healthcheck를 제공해야 하며, k6 volume 참조 drift를 제거해야 한다.
- **REQ-0021-FR-0004**: `scripts/hardening/check-all-hardening.sh 09-tooling`와 CI `infrastructure-hardening` job을 제공해야 한다.
- **REQ-0021-FR-0005**: `docs/{01.requirements,02.architecture,03.specs,05.operations}` optimization-hardening 문서 세트와 README 인덱스를 동기화해야 한다.
- **REQ-0021-FR-0006**: 카탈로그 기준으로 terraform 승인/백업/drift, terrakube 권한/감사로그, registry 서명/스캔 차단, sonarqube 품질게이트 재정의, k6 회귀 baseline, locust 분산 토폴로지/정리 루틴, syncthing ACL/암호화/충돌 정책을 작업 로드맵에 반영해야 한다.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.
## Acceptance Criteria

- **REQ-0021-FR-0001**: `bash scripts/hardening/check-all-hardening.sh 09-tooling` 실패 0건.
- **REQ-0021-FR-0002**: tooling hardening check와 optional root-context compose 검증 경계가 문서화되고 실패 0건을 유지한다.
- **REQ-0021-FR-0003**: tooling optimization-hardening 문서 간 양방향 링크 정합성 확보.
- **REQ-0021-FR-0004**: 카탈로그 09-tooling 확장 항목이 Plan/Tasks/Operations에 반영.

## Constraints

- **In Scope**:
  - `infra/09-tooling/*/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 09-tooling`
  - `.github/workflows/ci-quality.yml`
  - `docs/{01.requirements,02.architecture,03.specs,05.operations}` tooling optimization-hardening 문서/README
- **Out of Scope**:
  - 신규 도구 도입(예: 신규 테스트 프레임워크)
  - 즉시 모든 카탈로그 확장 항목의 런타임 구현
- **Non-goals**:
  - Terrakube/SonarQube major version migration
  - Registry backend 아키텍처 전환

## Risks

- SSO 강화로 기존 테스트/운영 접근 경로 일부 조정이 필요할 수 있다.
- tooling tier는 `01-gateway` Traefik, `02-auth` SSO, `04-data` PostgreSQL/Valkey/MinIO에 의존한다.
- 카탈로그 확장 항목은 정책/승인/운영 준비 단계를 포함하므로 단일 릴리스에서 전면 구현하지 않는다.

## AI Agent Requirements

- **Allowed Actions**: tooling compose/script/docs/ci 하드닝 변경과 정적 검증 실행
- **Disallowed Actions**: 무승인 인증 완화, unpinned 이미지 전환, 검증 게이트 우회
- **Human-in-the-loop Requirement**: 접근제어 완화/승인 게이트 완화/로그 보존 완화는 승인 필수
- **Evaluation Expectation**: `check-all-hardening.sh 09-tooling` + 공통 기준선 + 문서 추적성 통과

## Traceability

- **Architecture Description**: [../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md](../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/010-tooling/spec.md](../03.specs/0010-tooling/spec.md)
- **ADR**: [../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../05.operations/guides/09-tooling/optimization-hardening.md](../05.operations/catalog/09-tooling/0063-optimization-hardening/guide.md)
- **Operation**: [../05.operations/policies/09-tooling/optimization-hardening.md](../05.operations/catalog/09-tooling/0063-optimization-hardening/policy.md)
- **Runbook**: [../05.operations/runbooks/09-tooling/optimization-hardening.md](../05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md)
