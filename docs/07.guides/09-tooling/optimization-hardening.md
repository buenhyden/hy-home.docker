# 09-Tooling Optimization Hardening Guide

## Overview (KR)

이 문서는 `09-tooling` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Platform Product Owner

## Purpose

- SonarQube/Terrakube/Syncthing 경로를 gateway+SSO 정책에 정렬한다.
- tooling compose 네트워크 경계를 일관화한다.
- locust/k6 테스트 런타임 계약을 안정화한다.
- tooling 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목을 운영 실행 가능한 로드맵으로 반영한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/09-tooling` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

## Step-by-step Instructions

1. 정적 구성 점검
   - `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. Gateway/SSO 경계 정렬
   - SonarQube/Terrakube/Syncthing 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 네트워크 경계 표준화
   - tooling compose에 `infra_net` external 선언을 명시한다.
4. 테스트 런타임 안정화
   - locust-worker healthcheck를 확인한다.
   - k6 volume 참조가 `k6-data:/mnt/locust:rw`로 정렬되었는지 확인한다.
5. 기준선 검증 실행
   - `bash scripts/check-tooling-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - 도구별 확장 항목(terraform/terrakube/registry/sonarqube/k6/locust/syncthing)을 tasks/operations에 반영한다.

## Common Pitfalls

- 공개 라우터에 SSO 체인을 누락하는 실수
- compose별 네트워크 선언 편차를 방치하는 실수
- locust worker health 상태를 확인하지 않는 실수
- k6/locust 구성 드리프트를 문서 없이 방치하는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **Spec**: [../../04.specs/09-tooling/spec.md](../../04.specs/09-tooling/spec.md)
- **Plan**: [../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/09-tooling/optimization-hardening.md](../../08.operations/09-tooling/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/09-tooling/optimization-hardening.md](../../09.runbooks/09-tooling/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
