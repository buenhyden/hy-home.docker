---
title: "Platform Operations and Quality Optimization Hardening Operations Policy"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0063"
parent_ids:
- "AD-0009"
created: "2026-05-10"
---

# Platform Operations and Quality Optimization Hardening Operations Policy

## Overview

이 문서는 `09-platform-ops`·`11-quality`의 최적화/하드닝 운영 정책을 정의한다. 관리 경로 보안, 네트워크 경계, 테스트 도구 안정성, 카탈로그 확장 승인 게이트를 통제한다.

## Policy Scope

- `infra/09-platform-ops/*/docker-compose.yml` 및 `infra/11-quality/*/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`

- **Systems**: opentofu, terrakube, registry, sonarqube, k6, locust, renovate
- **Environments**: local·DEV·stage 및 production-like 환경

## Controls

- **Required**:
  - SonarQube/Terrakube 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - tooling 서비스는 root Compose가 정의한 선언된 network bridge에 연결한다.
  - locust-worker healthcheck를 유지한다.
  - k6 volume 계약(`k6-data:/scripts:ro`)을 유지한다.
  - tooling 변경은 `check-all-hardening.sh 09-platform-ops 11-quality` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - optimization-hardening 문서(PRD~Procedure) 링크를 유지해야 한다.
- **Allowed**:
  - 카탈로그 확장 항목을 단계적으로 도입하는 설계/운영 작업
  - 성능/품질/보안 기준의 보수적 강화
- **Disallowed**:
  - 무승인 SSO/middleware 완화
  - 검증 게이트 우회 배포
  - 감사/보존 정책 없이 확장 항목 운영 전환

### Catalog Expansion Approval Gates

- **opentofu 승인 조건**:
  - plan/apply 승인 게이트 문서화
  - state 잠금/백업 정책 및 drift 자동 탐지 절차 정의
- **terrakube 승인 조건**:
  - workspace 분리 전략 문서화
  - 실행 권한 모델/RBAC 및 감사로그 연계 정의
- **registry 승인 조건**:
  - cosign 서명/검증 정책 정의
  - 취약점 스캔 실패 차단 정책 및 예외 절차 정의
- **sonarqube 승인 조건**:
  - 품질게이트 임계값 재정의
  - 브랜치 정책과 보안 룰셋 분리 운영
- **k6/locust 승인 조건**:
  - 회귀 baseline 저장/비교 및 시나리오 태그 표준화
  - 분산 실행 토폴로지와 데이터 초기화/정리 루틴 문서화
- **renovate 승인 조건**:
  - `dependency-update` 수동 작업 범위와 최소 token 권한을 유지한다.
  - post-upgrade command 허용 목록과 변경 PR 검증을 확인한다.

## Exceptions

- 장애 대응 시 일시 완화는 승인 기록과 종료 조건이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- 프로필로 선택한 서비스는 루트 Compose의 네트워크·secret·의존성 문맥으로 검증한다. 개별 서비스 파일만으로 실행 구성을 판정하지 않는다.

## Review Cadence

- 월 1회 정기 검토
- tooling 구성/권한/정책 변경 시 수시 검토

### 확장 게이트와 현재 제한

위 카탈로그 항목은 추가 운영 전환의 승인 조건이며 구현 완료 목록이 아니다.
일반 변경·예외 절차는 [공통 운영 정책](0006-infrastructure-optimization-governance.md)을
따른다. Terrakube의 cookie ForwardAuth와 CLI/executor 비호환은 별도 구현 검토
대상이다. gateway 통제를 유지하면서 실행 활성화를 차단하고 `@buenhyden`에게 보고한다.

## Traceability

- 상위 문서: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0063-tooling-optimization-hardening.md) (`GDE-0063`), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) (`RUN-0063`)

현재 IaC helper는 OpenTofu다. 기존 Terraform workspace는 [migration handoff](../guides/0068-terraform.md)를 따른다. Syncthing runtime은 제거되었으며 현재 하드닝 기동 대상에 포함하지 않는다.

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0063-tooling-optimization-hardening.md)
- [Recovery runbook](../runbooks/0063-tooling-optimization-hardening.md)
