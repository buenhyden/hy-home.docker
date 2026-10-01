---
title: "07-Workflow Optimization Hardening Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0054"
parent_ids:
- "GDE-0054"
created: "2026-05-17"
---

# 07-Workflow Optimization Hardening Runbook

## Overview

이 런북은 `07-workflow` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health dependency 회귀, n8n image/entrypoint drift, CI 게이트 실패를 중심으로 점검/복구한다.

### Purpose

- workflow 관리 경로 보안과 startup 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## When to Use

- `infrastructure-hardening` CI가 실패할 때
- Airflow/Flower/n8n 경로 접근 정책이 비정상일 때
- Airflow worker/scheduler startup이 불안정할 때
- n8n worker/task-runner 재시작 루프가 발생할 때

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.


### Checklist

- [ ] 실패 항목(middleware, healthcheck, depends_on, image, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(스케줄링, 자동화, 큐 지연) 평가

### Steps

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
   - `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
   - service-local compose 파일은 root network/secrets context 없이 단독 `config` 대상으로 쓰지 않는다.
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
3. 증상별 복구
   - middleware 회귀:
     - Airflow의 승인된 native Keycloak SSO와 `gateway-standard-chain@file`을 복원한다. Flower/n8n에는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 복원한다. 로그인·권한 검증 전 정상으로 선언하지 않는다.
   - Airflow startup race:
     - `dedicated-valkey` profile을 선택한 경우 `airflow-valkey` `service_healthy` dependency 복원
     - 선택하지 않은 경우 shared `mng-valkey` broker 경계와 validation evidence 확인
   - n8n worker/task-runner 이상:
     - healthcheck/depends_on 계약 복원
   - n8n image drift:
     - compose custom image 설정 복원
     - 선택된 dev.Dockerfile/production Dockerfile의 non-root USER와 matching entrypoint를 복원한다. 고정 guard가 selected broker secret을 검증한다고 가정하지 않는다; [RUN-0053](0053-n8n.md) preflight를 따른다.
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`

### Verification Steps

- [ ] workflow compose static validation 통과
- [ ] workflow hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening`, 컨테이너 상태, 큐 지연, scheduler heartbeat
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/Dockerfile/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,dev.Dockerfile,docker-entrypoint.sh,docker-entrypoint.dev.sh}`
  - `scripts/hardening/check-all-hardening.sh 07-workflow`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

### Static gate boundary

`check_07_workflow`는 파일과 일부 인증 문자열을 확인하고 Airflow double proxy-auth를 거부한다. Runner 호환성, 선택 Dockerfile/guard, 모든 probe, DB/broker readiness와 로그인 성공까지 증명하지 않는다. 필수 통제에는 추가 소스 검토와 승인된 런타임 근거가 필요하다. 문자열 검사 통과로 n8n 버전·timeout·guard 결함을 닫지 않는다.

## Evidence

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 위의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 설정 rollback rehearsal은 계획만 있으며 미실행 상태다. 상태 데이터 복구는 `RUN-0050`과 `RUN-0053`이 소유한다. 이 최적화 Runbook으로 DB·암호화 키·큐 복구를 입증하지 않는다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 `## Escalation`에 따라 보고한다.

## Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

## Traceability

- Declared parent: [07-Workflow Optimization Hardening Usage Guide](../guides/0054-workflow-optimization-hardening.md) (`GDE-0054`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0054-workflow-optimization-hardening.md) (`GDE-0054`), [Policy](../policies/0054-workflow-optimization-hardening.md) (`POL-0054`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0054-workflow-optimization-hardening.md)
- [Operations policy](../policies/0054-workflow-optimization-hardening.md)
