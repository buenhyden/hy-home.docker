---
status: active
---
<!-- Target: docs/05.operations/guides/11-laboratory/optimization-hardening.md -->

# 11-Laboratory Optimization Hardening Usage Guide

## Usage

### Overview (KR)

이 문서는 `11-laboratory` 계층 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 관리 UI 보안 경계, 네트워크 표준화, 최소권한 적용, 기준선 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Platform SRE
- DevOps Engineer
- Security Reviewer

### Purpose

- 관리 UI를 gateway+allowlist+SSO 경계로 정렬한다.
- dashboard direct host 노출을 제거하고 Traefik 경유 접근으로 통일한다.
- dozzle 최소권한(socket read-only)을 적용한다.
- open-notebook UI route를 allowlist+large-body+SSO 경계로 보호하고 secret-file 주입을 유지한다.
- laboratory 하드닝 회귀를 script/CI로 조기 차단한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/11-laboratory` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

### Step-by-step Instructions

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
2. Ingress 경계 정렬
   - 각 Laboratory UI 라우터에 `gateway-standard-chain + service-ipallowlist + sso-errors + sso-auth`를 적용한다.
   - Open Notebook은 upload boundary를 위해 `large-body@file`을 추가한다.
3. 네트워크 경계 표준화
   - 모든 compose에 root `infra_net` context에 합류하는 service network block을 유지한다.
4. 최소권한 적용
   - dashboard `ports` 제거 후 `expose`만 사용한다.
   - dozzle docker socket을 `:ro`로 전환한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - dashboard 만료 정책, dozzle 로그 제한, portainer 승인 정책, redisinsight 감사 정책, open-notebook data retention/direct-port review를 tasks/operations에 반영한다.

### Common Pitfalls

- allowlist CIDR 설정 누락으로 운영자 접근이 차단되는 실수
- dashboard direct 포트 노출을 되돌려 우회 경로를 만드는 실수
- dozzle socket 권한을 read-write로 유지하는 실수
- 문서 링크/README 인덱스 동기화를 누락하는 실수
- service-local standalone compose render를 root readiness evidence로 오해하는 실수

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/11-laboratory/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/11-laboratory/optimization-hardening.md)
- [Recovery runbook](../../runbooks/11-laboratory/optimization-hardening.md)
