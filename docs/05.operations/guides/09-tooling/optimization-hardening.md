---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/optimization-hardening.md -->

# 09-Tooling Optimization Hardening Usage Guide

## Usage

### Overview

이 문서는 `09-tooling` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Platform Product Owner

### Purpose

- SonarQube/Terrakube/Syncthing 경로를 gateway+SSO 정책에 정렬한다.
- tooling compose 네트워크 경계를 일관화한다.
- locust/k6 테스트 런타임 계약을 안정화한다.
- tooling 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목을 운영 실행 가능한 로드맵으로 반영한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/09-tooling` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

### Step-by-step Instructions

1. 정적 구성 점검
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-repo-contracts.sh`
2. Gateway/SSO 경계 정렬
   - SonarQube/Terrakube/Syncthing 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 네트워크 경계 표준화
   - tooling compose에 `infra_net` external 선언을 명시한다. service-local compose 파일은 root network/secret context 없이 단독 config 대상으로 취급하지 않는다.
4. 테스트 런타임 안정화
   - locust-worker healthcheck를 확인한다.
   - k6 leaf는 현재 `k6-master` 단일 Locust wrapper이며, `k6-data:/mnt/locust:rw` volume 계약을 유지한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - 도구별 확장 항목(terraform/terrakube/registry/sonarqube/k6/locust/syncthing)을 tasks/operations에 반영한다.

### Common Pitfalls

- 공개 라우터에 SSO 체인을 누락하는 실수
- service-local compose 단독 config 실패를 root optional context와 구분하지 못하는 실수
- locust worker health 상태를 확인하지 않는 실수
- k6 leaf에 존재하지 않는 worker 또는 Traefik route를 문서화하는 실수

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/optimization-hardening.md)
- [Recovery runbook](../../runbooks/09-tooling/optimization-hardening.md)
