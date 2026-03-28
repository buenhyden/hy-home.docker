# 11-Laboratory Optimization Hardening Guide

## Overview (KR)

이 문서는 `11-laboratory` 계층 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 관리 UI 보안 경계, 네트워크 표준화, 최소권한 적용, 기준선 검증 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Platform SRE
- DevOps Engineer
- Security Reviewer

## Purpose

- 관리 UI를 gateway+allowlist+SSO 경계로 정렬한다.
- dashboard direct host 노출을 제거하고 Traefik 경유 접근으로 통일한다.
- dozzle 최소권한(socket read-only)을 적용한다.
- laboratory 하드닝 회귀를 script/CI로 조기 차단한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/11-laboratory` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

## Step-by-step Instructions

1. 정적 구성 점검
   - `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. Ingress 경계 정렬
   - 각 Laboratory 라우터에 `gateway-standard-chain + service-ipallowlist + sso-errors + sso-auth`를 적용한다.
3. 네트워크 경계 표준화
   - 모든 compose에 `infra_net` external 선언을 명시한다.
4. 최소권한 적용
   - dashboard `ports` 제거 후 `expose`만 사용한다.
   - dozzle docker socket을 `:ro`로 전환한다.
5. 기준선 검증 실행
   - `bash scripts/check-laboratory-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - dashboard 만료 정책, dozzle 로그 제한, portainer 승인 정책, redisinsight 감사 정책을 tasks/operations에 반영한다.

## Common Pitfalls

- allowlist CIDR 설정 누락으로 운영자 접근이 차단되는 실수
- dashboard direct 포트 노출을 되돌려 우회 경로를 만드는 실수
- dozzle socket 권한을 read-write로 유지하는 실수
- 문서 링크/README 인덱스 동기화를 누락하는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/11-laboratory/optimization-hardening.md](../../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/11-laboratory/optimization-hardening.md](../../09.runbooks/11-laboratory/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
