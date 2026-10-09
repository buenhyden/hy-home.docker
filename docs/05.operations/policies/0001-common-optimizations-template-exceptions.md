---
title: "Common Optimizations Template Exceptions Policy"
version: "1.4.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0001"
created: "2026-06-04"
---


# Common Optimizations Template Exceptions Policy

## Overview

이 문서는 `infra/common-optimizations.yml` 적용 시 허용되는 예외 목록과 승인 기준을 정의한다.
예외는 임시 편의가 아니라 운영/보안 상의 명시적 승인 항목으로 관리하며, 모든 검증 스크립트와 운영 문서는 동일 레지스트리를 참조해야 한다.

## Scope

- `common-optimizations.yml` 템플릿 계열(`template-*`)의 제어항목 예외 관리
- Quick Win 기준선(`PLN-QW-001~005`) 검증 시 허용되는 서비스 단위 예외 관리

- **Systems**: Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}` (root 통합 Compose 해석 기준)
- **Environments**: Local, Dev, Stage, Production-like

## Rules

- **Required**:
  - 예외 목록 SSoT는 [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json)(schema v2) 단일 파일이다.
  - `scripts/validation/compose_controls.py`는 root를 모든 profile로, `labs/*.yml`을 각각 합성 입력으로 렌더한다. extends·merge 뒤 서비스의 최종 control을 읽는다. gate 진입점은 `scripts/validation/check-template-security-baseline.sh`다.
  - registry의 `controls`에 등록된 control만 강제한다. 현재 등록된 control은 `no_new_privileges`, `cap_drop_all`, `cap_add`, `privileged`, `init`, `restart`, `healthcheck`, `cpus`, `mem_limit`, `pids_limit`, `secrets_group`, `gpu`이다. 나머지(예: `read_only`)는 `--report`로 보고만 한다.
  - 모든 템플릿은 capability를 전부 버린다(`cap_drop: ALL`). 이미지가 필요로 하는 capability는 leaf가 `cap_add`로 더하고 정확한 예외로 남긴다.
  - `SECRETS_GID`는 secret 또는 secrets 디렉터리 아래 파일을 읽는 leaf만 선언한다. host group 소유 데이터 디렉터리에 쓰는 서비스는 기록된 예외로만 이 group을 유지한다.
  - `pids_limit`은 등급별 초기 예산이다(dev 128, low 256, med 512, high·DB 1024). 부하 측정 전에는 최적값이 아니다.
  - 예외 한 건은 `scope`(`root` 또는 `lab:<이름>`), `compose_file`, `service`, `control`, `allowed_value`를 정확히 지정한다. `kind`(`weakening` 또는 `compatibility`), `owner`, `reason`, `impact`, `mitigation`, `verification`, `reviewed`, `review_by`, `release_condition`도 필수다.
  - `review_by`는 `reviewed`로부터 1년 이내다. 날짜가 지난 예외는 실패한다.
  - `infra/` Compose의 모든 서비스는 `container_name`과 `hostname`을 선언하며, 둘 다 서비스 이름과 같아야 한다. Docker container 이름은 호스트 전체에서 유일해야 하므로 다른 `container_name`은 `naming_exceptions`에 `container_name`과 `reason`으로만 등록한다(`tests.validation.test_infra_tier_layout`가 검사).
- **약화 예외가 아닌 것**:
  - `restart: "no"`인 job은 healthcheck가 필요 없다. lifecycle 사실이므로 예외로 등록하지 않는다.
  - secret을 읽지 않는 서비스에는 Docker secret이 필요 없다(비적용).
  - 일반 업스트림 서비스 키(Supabase `db`, `auth` 등)의 `container_name`에 `supabase-` 접두어 유지; `hostname`은 서비스 이름.
- **Disallowed**:
  - wildcard 서비스·파일·scope, 미등록 control, 중복 예외
  - 실제 서비스가 없는 예외(고아), 서비스가 이미 기준을 지키는 예외(퇴역 대상), 실제 값과 다른 `allowed_value`
  - root와 LAB의 같은 서비스 이름을 하나의 예외로 묶는 것
  - 문서와 레지스트리 간 불일치 상태로 배포 진행

### AI Agent Policy

- **Model / Prompt Change Process**: [agentic governance](../../../.agents/governance/agentic.md)가 소유한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: [task checklists](../../../.agents/governance/task-checklists.md)를 따른다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Exceptions

- 예외의 상세 항목은 [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json)을 기준으로 한다.
  schema v1의 `template_exceptions`, `quickwin_baseline`, `security_baseline`은
  SPEC-0218에서 정확한 서비스 단위 예외로 옮기거나 퇴역했다. `pg-0`~`pg-2`, `etcd-*`처럼
  LAB 서비스를 root 이름으로만 적던 항목은 `lab:<이름>` scope로 옮기거나 없앴다.
  모든 서비스에 Docker secret을 요구하던 QW-005와 `check-quickwin-baseline.sh`는
  퇴역했다. secret을 읽는 서비스의 secret group 검사(SPEC-0218 W2에서 등록)가 그 자리를 맡는다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, POL-0001 Exceptions.
>
> - 2026-03-28 기준 승인된 서비스 예외:
>   - `healthcheck`: `pg-cluster-init`, `valkey-cluster-init`
>   - `secrets`: `etcd-1`, `etcd-2`, `etcd-3`

### Verification

- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/compose_controls.py --report`(등록 전 control 포함 전체 편차 보고)
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `bash scripts/validation/validate-docker-compose.sh`

검증기는 root 전체 profile과 모든 LAB을 렌더하지만 정적 선언만 검사한다.
runtime health, 실제 이미지의 capability 필요 여부, 자원 사용량은 증명하지 않는다.
`verification` 필드에 그 근거(실행 기록, 시험)를 적는다. 공개 입력·임시 파일 경계는
[RUN-0086](../runbooks/0086-dependency-version-management.md#static-configuration-validation)을
따른다. 구현이 통제를 충족하지 못하면 예외를 임의 추가하지 않고 별도 remediation으로 남긴다.

### Review Cadence

책임 소유자는 @buenhyden이다. registry의 role 표기는 책임 설명이며 별도 팀이나
새 승인을 만들지 않는다.

- 월 1회 정기 검토
- 신규 예외 추가/삭제 시 즉시 검토

### Traceability

- 같은 번호 `0001`의 Guide/Runbook은 없다.

## Related Documents

- Compose/Dockerfile이 runtime pin을 소유한다. [파생 projection](../../../infra/tech-stack.versions.json)은 Compose-image drift를 검사한다.
- [Operations index](../README.md)
