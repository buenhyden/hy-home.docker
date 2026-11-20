---
title: "Common Optimizations Template Exceptions Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0001"
created: "2026-06-04"
next_review_at: "2027-05-13"
---

# Common Optimizations Template Exceptions Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

이 문서는 `infra/common-optimizations.yml` 적용 시 허용되는 예외 목록과 승인 기준을 정의한다.
예외는 임시 편의가 아니라 운영/보안 상의 명시적 승인 항목으로 관리하며, 모든 검증 스크립트와 운영 문서는 동일 레지스트리를 참조해야 한다.

###### Authority
<!-- core-payload-level:4 -->

- [infra/common-optimizations.exceptions.json](../../../../infra/common-optimizations.exceptions.json)
- [scripts/validation/compose_controls.py](../../../../scripts/validation/compose_controls.py)

##### Applies To

- `common-optimizations.yml` 템플릿 계열(`template-*`)의 제어항목 예외 관리
- Quick Win 기준선(`PLN-QW-001~005`) 검증 시 허용되는 서비스 단위 예외 관리

- **Systems**: Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}` (root 통합 Compose 해석 기준)
- **Environments**: Local, Dev, Stage, Production-like

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0001-R1 | 항상 | 필수: 예외 목록 SSoT는 `infra/common-optimizations.exceptions.json`(schema v2) 단일 파일 | none | none |
| POL-0001-R2 | 검증기 실행 시 | 필수: `scripts/validation/compose_controls.py`는 root를 모든 profile로, `labs/*/docker-compose.yml`을 각각 합성 입력으로 렌더하고 extends/merge 뒤 서비스의 최종 control을 읽는다 | none | none |
| POL-0001-R3 | 항상 | 필수: registry의 `controls`에 등록된 control만 강제한다 | none | none |
| POL-0001-R4 | `--report` 출력에 포함되지 않는 항목(`read_only`/UID/host namespace/Docker socket 권한) | 필수: 별도 서비스 조사로 확인한다 | 수동 | none |
| POL-0001-R5 | 모든 템플릿 | 필수: `cap_drop: ALL`로 capability를 전부 버린다 | none | none |
| POL-0001-R6 | 이미지가 capability를 필요로 할 때 | 필수: leaf가 `cap_add`로 더하고 정확한 예외로 남긴다 | none | none |
| POL-0001-R7 | 항상 | 필수: `SECRETS_GID`는 secret 또는 secrets 디렉터리 아래 파일을 읽는 leaf만 선언한다 | none | none |
| POL-0001-R8 | host group 소유 데이터 디렉터리에 쓰는 서비스 | 필수: 기록된 예외로만 이 group을 유지한다 | none | none |
| POL-0001-R9 | 항상 | 필수: `pids_limit`은 등급별 초기 예산(dev 128/low 256/med 512/high·DB 1024)을 따른다 | none | none |
| POL-0001-R10 | 예외 한 건 등록 시 | 필수: `scope`(`root` 또는 `lab:<이름>`)/`compose_file`/`service`/`control`/`allowed_value`를 정확히 지정한다 | none | none |
| POL-0001-R11 | 예외 한 건 등록 시 | 필수: `kind`(`weakening` 또는 `compatibility`)/`owner`/`reason`/`impact`/`mitigation`/`verification`/`reviewed`/`review_by`/`release_condition`을 지정한다 | none | none |
| POL-0001-R12 | 예외 검사 시 | 금지: `reviewed`를 검사일보다 미래일로 두는 것 | none | none |
| POL-0001-R13 | 예외 검사 시 | 필수: `review_by`는 `reviewed` 이상이며 그로부터 366일 이내 | none | none |
| POL-0001-R14 | 마감일이 지난 예외 | 필수: 검사에서 실패로 처리한다 | none | none |
| POL-0001-R15 | 검토일 또는 마감일이 검사일과 같을 때 | 허용: 유효한 값으로 인정한다 | none | none |
| POL-0001-R16 | 항상 | 필수: `reviewed`와 `review_by`는 ISO 날짜로 검사한다 | none | none |
| POL-0001-R17 | `infra/` Compose | 필수: `container_name`과 `hostname`은 서비스 이름과 같다 | none | none |
| POL-0001-R18 | `network_mode: host`로 실행하는 `node-exporter` | 허용: `hostname`을 선언하지 않는다 | none | none |
| POL-0001-R19 | 서비스 이름과 다른 `container_name` | 필수: root 레지스트리의 `naming_exceptions`에 `container_name`과 `reason`으로 등록한다 | `tests.validation.test_infra_tier_layout` | none |
| POL-0001-R20 | `restart: "no"`인 job | 허용: healthcheck 없이 둔다 | none | none |
| POL-0001-R21 | `restart: "no"`인 job의 healthcheck 부재 | 금지: lifecycle 사실을 예외로 등록한다 | none | none |
| POL-0001-R22 | secret을 읽지 않는 서비스 | 허용: Docker secret 없이 둔다(비적용) | none | none |
| POL-0001-R23 | 예외 등록 시 | 금지: wildcard 서비스/파일/scope | none | none |
| POL-0001-R24 | 예외 등록 시 | 금지: 미등록 control | none | none |
| POL-0001-R25 | 예외 등록 시 | 금지: 중복 예외 | none | none |
| POL-0001-R26 | 예외 등록 시 | 금지: 실제 서비스가 없는 예외(고아) | none | none |
| POL-0001-R27 | 예외 등록 시 | 금지: 서비스가 이미 기준을 지키는 예외(퇴역 대상) | none | none |
| POL-0001-R28 | 예외 등록 시 | 금지: 실제 값과 다른 `allowed_value` | none | none |
| POL-0001-R29 | 예외 등록 시 | 금지: root와 LAB의 같은 서비스 이름을 하나의 예외로 묶는 것 | none | none |
| POL-0001-R30 | 배포 시 | 금지: 문서와 레지스트리 간 불일치 상태로 배포 진행 | none | none |
| POL-0001-R31 | 모델/프롬프트 변경 | 필수: [agentic governance](../../../../.agents/governance/agentic.md)가 소유하는 절차를 따른다 | none | none |
| POL-0001-R32 | 문서 변경 후 | 필수: 관련 validation을 통과한다 | none | none |
| POL-0001-R33 | 로그/트레이스 보존 | 필수: [task checklists](../../../00.workspace/04.quality/task-checklists.md)를 따른다 | none | none |
| POL-0001-R34 | secret 노출 또는 승인 없는 runtime 변경 징후 | 필수: 즉시 중단한다 | none | none |

- **Required**:
  - 예외 목록 SSoT는 [infra/common-optimizations.exceptions.json](../../../../infra/common-optimizations.exceptions.json)(schema v2) 단일 파일이다.
  - `scripts/validation/compose_controls.py`는 root를 모든 profile로, `labs/*/docker-compose.yml`을 각각 합성 입력으로 렌더한다. extends·merge 뒤 서비스의 최종 control을 읽는다. gate 진입점은 `scripts/validation/check-template-security-baseline.sh`다.
  - registry의 `controls`에 등록된 control만 강제한다. 현재 등록된 control은 `no_new_privileges`, `cap_drop_all`, `cap_add`, `privileged`, `init`, `restart`, `healthcheck`, `cpus`, `mem_limit`, `pids_limit`, `secrets_group`, `gpu`이다. `--report`는 검증기가 지원하는 control의 편차를 출력한다. `read_only`, UID, host namespace와 Docker socket 권한은 이 출력에 포함되지 않으므로 별도 서비스 조사로 확인한다.
  - 모든 템플릿은 capability를 전부 버린다(`cap_drop: ALL`). 이미지가 필요로 하는 capability는 leaf가 `cap_add`로 더하고 정확한 예외로 남긴다.
  - `SECRETS_GID`는 secret 또는 secrets 디렉터리 아래 파일을 읽는 leaf만 선언한다. host group 소유 데이터 디렉터리에 쓰는 서비스는 기록된 예외로만 이 group을 유지한다.
  - `pids_limit`은 등급별 초기 예산이다(dev 128, low 256, med 512, high·DB 1024). 부하 측정 전에는 최적값이 아니다.
  - 예외 한 건은 `scope`(`root` 또는 `lab:<이름>`), `compose_file`, `service`, `control`, `allowed_value`를 정확히 지정한다. `kind`(`weakening` 또는 `compatibility`), `owner`, `reason`, `impact`, `mitigation`, `verification`, `reviewed`, `review_by`, `release_condition`도 필수다.
  - `reviewed`는 검사일보다 미래일 수 없고, `review_by`는 `reviewed` 이상이며 그로부터 366일 이내다. 검사일과 같은 검토일·마감일은 유효하며, 마감일이 지난 예외는 실패한다. 두 필드는 ISO 날짜로 검사한다.
  - `infra/` Compose의 `container_name`과 `hostname`은 서비스 이름과 같아야 한다.
    SPEC-0225의 host metric 수집을 위해 `network_mode: host`로 실행하는
    `node-exporter`는 현재 구현과 회귀검사에 따라 `hostname`을 선언하지 않는다.
    Docker container 이름은 호스트 전체에서 유일해야 하므로 다른 `container_name`은
    root 레지스트리의 `naming_exceptions`에 `container_name`과 `reason`으로 등록한다
    (`tests.validation.test_infra_tier_layout`가 검사).
- **약화 예외가 아닌 것**:
  - `restart: "no"`인 job은 healthcheck가 필요 없다. lifecycle 사실이므로 예외로 등록하지 않는다.
  - secret을 읽지 않는 서비스에는 Docker secret이 필요 없다(비적용).
- **Disallowed**:
  - wildcard 서비스·파일·scope, 미등록 control, 중복 예외
  - 실제 서비스가 없는 예외(고아), 서비스가 이미 기준을 지키는 예외(퇴역 대상), 실제 값과 다른 `allowed_value`
  - root와 LAB의 같은 서비스 이름을 하나의 예외로 묶는 것
  - 문서와 레지스트리 간 불일치 상태로 배포 진행

###### AI Agent Policy
<!-- core-payload-level:4 -->

- **Model / Prompt Change Process**: [agentic governance](../../../../.agents/governance/agentic.md)가 소유한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: [task checklists](../../../00.workspace/04.quality/task-checklists.md)를 따른다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

- 예외의 상세 항목은 [infra/common-optimizations.exceptions.json](../../../../infra/common-optimizations.exceptions.json)을 기준으로 한다.
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

###### Approval and Review
<!-- core-payload-level:4 -->

- 월 1회 정기 검토
- 신규 예외 추가/삭제 시 즉시 검토

#### Enforcement

##### Mechanisms

- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/compose_controls.py --report`(등록 전 control 포함 전체 편차 보고)
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `bash scripts/validation/validate-docker-compose.sh`

검증기는 root 전체 profile과 모든 LAB을 렌더하지만 정적 선언만 검사한다.
runtime health, 실제 이미지의 capability 필요 여부, 자원 사용량은 증명하지 않는다.
`verification` 필드에 그 근거(실행 기록, 시험)를 적는다. 공개 입력·임시 파일 경계는
[RUN-0086](../../03.runbooks/10.platform-and-backup/0086-dependency-version-management.md#static-configuration-validation)을
따른다. 구현이 통제를 충족하지 못하면 예외를 임의 추가하지 않고 별도 remediation으로 남긴다.

##### Limits

이 정책은 아래 규칙에 대해 명명된 자동 검사를 연결하지 않거나 수동 검토에 맡긴다.

- 예외 레지스트리: 명명된 검사 없음 R1 (`POL-0001-` 접두)
- control 렌더/강제: 명명된 검사 없음 R2, R3; 수동 검토 R4 (`POL-0001-` 접두)
- capability/secret group: 명명된 검사 없음 R5~R8 (`POL-0001-` 접두)
- pids_limit: 명명된 검사 없음 R9 (`POL-0001-` 접두)
- 예외 항목 필드: 명명된 검사 없음 R10, R11 (`POL-0001-` 접두)
- 검토일/마감일: 명명된 검사 없음 R12~R16 (`POL-0001-` 접두)
- 이름 규칙: 명명된 검사 없음 R17, R18 (`POL-0001-` 접두)
- 비적용 사례: 명명된 검사 없음 R20~R22 (`POL-0001-` 접두)
- 예외 등록 금지: 명명된 검사 없음 R23~R30 (`POL-0001-` 접두)
- AI Agent Policy: 명명된 검사 없음 R31~R34 (`POL-0001-` 접두)
- 검증기는 정적 선언만 검사하므로 runtime health, 실제 이미지의 capability 필요 여부, 자원 사용량은 증명되지 않으며 `verification` 필드에 적은 근거(실행 기록, 시험)로만 뒷받침된다.
- 구현이 통제를 충족하지 못할 때의 처리는 임의 예외 추가 없이 별도 remediation으로 남기는 수동 판단이다.

#### Ownership

##### Owner

책임 소유자는 @buenhyden이다. registry의 role 표기는 책임 설명이며 별도 팀이나
새 승인을 만들지 않는다.

##### Review Triggers

- 같은 번호 `0001`의 Guide/Runbook은 없다.

- Compose/Dockerfile이 runtime pin을 소유한다. [파생 projection](../../../../infra/tech-stack.versions.json)은 Compose-image drift를 검사한다.
- [Operations index](../../README.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
