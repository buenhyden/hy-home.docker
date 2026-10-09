---
title: "Platform Operations and Quality Optimization Hardening Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0063"
parent_ids:
- "GDE-0063"
created: "2026-05-17"
---

# Platform Operations and Quality Optimization Hardening Runbook

## Overview

`09-platform-ops`와 `11-quality` 하드닝 회귀가 의심될 때 문서화된 기준을 복구하는 절차다.
공개 경계 SSO 체인, root가 소유한 network 경계, 독립 Locust LAB worker healthcheck,
k6 volume 계약, 문서·검증 링크를 현재 구현 기준으로 되돌린다.
범위는 선택한 profile에 해당하는 패키지로 한정한다.

## Trigger and Preconditions

service-local compose 단독 검증과 root compose context를 혼동하지 않고 하드닝 기준선을 다시 확인한다.
다음 중 하나일 때 사용한다.

- `09-platform-ops`·`11-quality`의 CI 또는 로컬 하드닝 검사가 실패한다.
- SonarQube/Terrakube middleware 체인이 승인된 설정과 달라진다.
- 독립 Locust LAB worker의 healthcheck 또는 명령 계약이 바뀐다.
- k6 volume 또는 서비스명 문서가 구현과 달라진다.
- 활성 문서가 profile 선택 leaf를 root 문맥 없이 단독 실행할 수 있다고 설명한다.

## Procedure

- [ ] Failure category를 middleware, network, healthcheck, volume, docs, script 중 하나로 분류한다.
- [ ] 최근 변경 커밋과 affected files를 확인한다.
- [ ] root `docker-compose.yml`이 09-platform-ops 및 11-quality Compose 파일을 모두 include하는지 확인하고, 이번 세션에서 선택한 profile을 기록한다.

### Steps

1. 하드닝 기준선을 실행한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality
   ```

2. 문서 계약과 stale literal guard를 실행한다.

   ```bash
   python3 scripts/validation/run-ci-gate.py --profile changed --explain
   python3 scripts/validation/check-document-links.py --mode alignment
   ```

3. 증상별로 복구한다.
   - Middleware drift: SonarQube/Terrakube 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 복원한다.
   - Network drift: tooling 서비스의 선언된 network 연결과 root Compose network 정의를 복원한다.
   - Locust LAB drift: `labs/locust.yml`의 `lab-locust-worker` command와 worker process healthcheck를 복원한다. root profile에는 다시 추가하지 않는다.
   - k6 drift: `k6` service name과 `k6-data:/scripts:ro` volume 계약을 복원한다.
   - Documentation drift: active docs에서 없는 worker/route/version/service-local standalone claims를 제거한다.

4. 재검증한다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality
   bash scripts/validation/check-template-security-baseline.sh
   python3 scripts/validation/check-document-links.py --mode traceability
   python3 scripts/validation/run-ci-gate.py --profile changed --explain
   ```

### 검토된 하드닝 변경 순서

1. 정적 구성 점검
   - `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
   - `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
2. Gateway/SSO 경계 정렬
   - SonarQube/Terrakube 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 네트워크 경계 표준화
   - tooling 서비스의 선언된 network 연결과 root Compose의 network 정의를 함께 확인한다. service-local compose 파일은 root network/secret context 없이 단독 config 대상으로 취급하지 않는다.
4. 테스트 런타임 안정화
   - `labs/locust.yml`의 Locust LAB worker healthcheck를 별도 entrypoint로 확인한다.
   - k6 leaf는 `k6` 단일 작업이며, `k6-data:/scripts:ro` volume 계약을 유지한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`
6. 카탈로그 확장 로드맵 반영
   - 도구별 확장 항목(opentofu/terrakube/registry/sonarqube/k6/locust/renovate)을 tasks/operations에 반영한다.

## Verification

- 명령 결과, 시각, 실패 검사명, 변경 diff와 최종 검증 상태를 기록한다.
- Compose 렌더링을 근거로 남길 때 선택한 프로필을 기록한다.

`--explain`은 실행하지 않는 계획 조회다. 후보 aggregate QA는
[quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix)의
원격 PR 경로가 소유하며 조회 결과를 검증 PASS로 기록하지 않는다.

- tooling hardening script 실패 0건.
- repo contracts 실패 0건.
- optimization-hardening guide/policy/runbook links가 guide, policy, runbook 각각의 목적 bucket을 가리킨다.
- profile로 선택되는 tooling leaf runtime 검증은 root network/secret/dependency context 필요성이 문서화되어 있다.

### 증거 출처

- **Logs**: CI·로컬 검증 결과와 별도 런타임 승인이 있을 때의 제한된 서비스 로그.
- **Metrics**: 문서 하드닝에는 런타임 지표가 적용되지 않는다. 리허설 지표는 별도 근거다.
- **Evidence to Capture**: 실패한 검사, 변경 파일, 변경 전후 하드닝 결과와 문서 링크 결과.

## Rollback and Escalation

### Rollback or Recovery

위의 한정된 복구 단계만 사용한다. 실행 환경·데이터·자격 증명 변경이 필요하면 중단하고 `## Escalation`을 따른다.

1. 문서-only 회귀는 직전 diff 단위로 되돌리거나 current-truth 문서로 정정한다.
2. compose/script 회귀는 affected file만 최소 복구하고 hardening check를 재실행한다.
3. runtime 재시작은 이 런북 범위를 벗어나며 대상 service runbook과 사용자 승인을 따른다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

한정된 복구 후에도 검사가 실패하거나 비밀 노출, 루트 Compose 문맥 복구 실패, 실행 환경 변경 필요성이 있으면 책임자에게 보고한다.

## Related Documents

### Traceability

- 상위 문서: [Platform Operations and Quality Optimization Hardening Usage Guide](../guides/0063-tooling-optimization-hardening.md) (`GDE-0063`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0063-tooling-optimization-hardening.md) (`GDE-0063`), [Policy](../policies/0063-tooling-optimization-hardening.md) (`POL-0063`)

현재 IaC helper는 OpenTofu다. 기존 Terraform workspace는 [migration handoff](../guides/0068-terraform.md)를 따른다. Syncthing runtime은 제거되었으며 현재 하드닝 기동 대상에 포함하지 않는다.

- [Operations index](../README.md)
- [Usage guide](../guides/0063-tooling-optimization-hardening.md)
- [Operations policy](../policies/0063-tooling-optimization-hardening.md)
