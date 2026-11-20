---
title: "Conftest Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0095"
parent_ids:
- "AD-0009"
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Conftest Operations Policy

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

`infra/11-quality/conftest/policy/` 아래의 Rego 규칙은 저장소 컨테이너
baseline의 실행 가능한 부분집합이다. 이 정책은 새 통제를 정의하지 않으며, 규칙을
추가할 때도 각 규칙은 다른 정책이 이미 소유한 통제를 그대로 다시 적은 것이어야 한다.

###### Authority
<!-- core-payload-level:4 -->

- [Compose profile vocabulary](../01.common/0078-compose-profile-vocabulary.md)
- [Conftest Compose source](../../../../infra/11-quality/conftest/docker-compose.yml)

##### Applies To

규칙, 그 allowlist, job의 접근 범위, 실패의 해결 방식.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0095-R1 | 규칙 추가 시 | 필수: 모든 규칙은 같은 디렉터리에 unit test를 둔다 | `bash scripts/validation/check-conftest-policy.sh --mode verify`(`leaf.conftest-policy-tests`, local 전용) | none |
| POL-0095-R2 | job 실행 시 | 필수: 소스를 테스트하기 전에 `conftest verify`를 실행한다 | `bash scripts/validation/check-conftest-policy.sh --mode verify`(`leaf.conftest-policy-tests`, local 전용) | none |
| POL-0095-R3 | 항상 | 필수: 등록된 `verify`·`corpus` lane을 분리하고 기본 `all`은 두 단계를 순서대로 실행한다 | none | none |
| POL-0095-R4 | 규칙 병합 시 | 금지: 실패·통과 케이스가 모두 없는 규칙의 병합 | none | none |
| POL-0095-R5 | allowlist 항목 추가 시 | 필수: 정책 파일에 서비스명과 이유를 명시한다 | none | none |
| POL-0095-R6 | allowlist 확대 시 | 필수: 검토된 변경으로만 늘린다 | 수동 | none |
| POL-0095-R7 | 새 `deny` 병합 전 | 필수: 현재 소스에서 통과해야 한다 | `bash scripts/validation/check-conftest-policy.sh --mode corpus`(CI `leaf.conftest-policy`) | none |
| POL-0095-R8 | 소스가 충족할 수 없는 규칙 | 필수: `warn`으로 시작한다 | none | none |
| POL-0095-R9 | job 실행 시 | 필수: 공개 `infra/`·`labs/`와 wrapper가 준비한 공개 파생 입력만 읽기 전용으로 마운트한다 | none | none |
| POL-0095-R10 | job 실행 시 | 필수: 네트워크 없이 non-root 사용자로 실행한다 | none | none |
| POL-0095-R11 | 항상 | 금지: `secrets/`, `.env`, Docker socket, 호스트 root·Git·scripts 마운트 | none | none |
| POL-0095-R12 | corpus 선정 시 | 필수: corpus 권위는 기존 canonical Git 추적 소스 목록이다 | none | none |
| POL-0095-R13 | 항상 | 금지: 무시된 설치 산출물 읽기 | none | none |
| POL-0095-R14 | 무시되지 않은 미추적 소스 후보가 있을 때 | 필수: Docker 실행 전에 실패한다 | none | none |
| POL-0095-R15 | overlay 입력 보충 시 | 필수: POL-0078로 검증한 overlay의 원본 base profile만 정책 입력에 보충한다 | none | none |
| POL-0095-R16 | 항상 | 금지: 이 보충을 실행용 Compose나 다른 정책 필드를 바꾸는 예외로 사용 | none | none |
| POL-0095-R17 | `corpus`·기본 `all` 실행 시 | 필수: wrapper의 완전한 두 소스 목록과 digest를 요구하고 준비가 없거나 잘못되면 실패한다 | none | none |
| POL-0095-R18 | 항상 | 금지: raw fallback | none | none |
| POL-0095-R19 | 직접 job `verify` 실행 시 | 필수: 직접 job `verify`를 유지한다 | none | none |
| POL-0095-R20 | 항상 | 금지: 원본·기존 권한 변경 | none | none |
| POL-0095-R21 | 실행 종료 후 | 필수: 임시 입력을 정리한다 | none | none |
| POL-0095-R22 | `deny` 발동 시 | 필수: 규칙이 아니라 선언을 고친다 | none | none |
| POL-0095-R23 | 항상 | 필수: raw 파일 탐색으로 선택되지 않는 inline Dockerfile과 최종 Compose·실행 상태의 통제를 별도로 요구한다 | none | none |
| POL-0095-R24 | 항상 | 금지: 이 도구의 PASS를 전체 인프라 보안 준수 판정으로 해석 | none | none |
| POL-0095-R25 | 새 규칙의 단계적 `warn` 도입 시 | 금지: 도입 조건을 기존 강제 통제를 약화할 허가로 사용 | none | none |
| POL-0095-R26 | 새 규칙의 단계적 `warn` 도입 시 | 필수: 정책 단위 테스트·검토된 예외 근거를 유지한다 | none | none |

- 모든 규칙은 같은 디렉터리에 unit test를 가지며, job은 소스를 테스트하기
  전에 `conftest verify`를 실행한다. 등록된 `verify`·`corpus` lane은 분리되며
  기본 `all`은 두 단계를 순서대로 실행한다. 실패·통과 케이스가 모두 없는 규칙은
  병합하지 않는다.
- allowlist 항목(예: privileged에 대한 `cadvisor`)은 정책 파일에 서비스명과
  이유를 명시한다. allowlist는 검토된 변경으로만 늘어난다.
- 새 `deny`는 병합되기 전에 현재 소스에서 통과해야 한다. 소스가 충족할 수
  없는 규칙은 `warn`으로 시작한다.
- job은 공개 `infra/`·`labs/`와 wrapper가 준비한 공개 파생 입력만 읽기 전용으로
  마운트하고 네트워크 없이 non-root 사용자로 실행한다. `secrets/`, `.env`,
  Docker socket, 호스트 root·Git·scripts는 마운트하지 않는다.
- corpus 권위는 기존 canonical Git 추적 소스 목록이다. 무시된 설치 산출물은
  읽지 않으며 무시되지 않은 미추적 소스 후보는 Docker 전에 실패한다.
  wrapper는 POL-0078로 검증한 overlay의 원본 base profile만 정책 입력에
  보충한다. 실행용 Compose나 다른 정책 필드를 바꾸는 예외가 아니다.
- `corpus`·기본 `all`에는 wrapper의 완전한 두 소스 목록과 digest가 필요하다.
  준비가 없거나 잘못되면 실패하며 raw fallback은 없다. 직접 job `verify`는
  유지한다. 원본·기존 권한을 변경하지 않고 임시 입력만 종료 후 정리한다.
- `deny`가 발동하면 규칙이 아니라 선언을 고친다.

###### 적용 범위와 책임
<!-- core-payload-level:4 -->

책임자는 `@buenhyden`이다. raw 파일 탐색으로 선택되지 않는 inline Dockerfile과
최종 Compose·실행 상태의 통제도 여전히 요구된다. 이 도구의 PASS는 전체 인프라 보안
준수 판정이 아니다. 새 규칙의 단계적 warn 도입 조건은 기존 강제 통제를 약화할
허가가 아니며 정책 단위 테스트·검토된 예외 근거를 유지한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

정책 파일의 allowlist를 넘어서는 예외는 없다.

###### Approval and Review
<!-- core-payload-level:4 -->

컨테이너 baseline 통제가 바뀔 때, Conftest 또는 OPA major 업그레이드 시,
allowlist 항목이 추가될 때마다 검토한다.

#### Enforcement

##### Mechanisms

`bash scripts/validation/check-conftest-policy.sh --mode verify`(정책 unit test)가
통과하고, 각 규칙의 unit test가 실패 케이스를 실제로 거부해야 한다.
`--mode corpus`는 wrapper가 준비한 Git 추적 Compose·Dockerfile corpus에서 `deny` 없이
끝나야 한다. CI는 `leaf.conftest-policy`(`--mode corpus`)를 실행하고,
`leaf.conftest-policy-tests`(`--mode verify`)는 local 전용이다.

##### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(규칙 테스트): `POL-0095-R3`, `POL-0095-R4`
- 이름 있는 검사 없음(allowlist): `POL-0095-R5`
- 이름 있는 검사 없음(deny): `POL-0095-R8`
- 이름 있는 검사 없음(마운트): `POL-0095-R9`, `POL-0095-R10`, `POL-0095-R11`
- 이름 있는 검사 없음(corpus): `POL-0095-R12`, `POL-0095-R13`, `POL-0095-R14`, `POL-0095-R15`, `POL-0095-R16`
- 이름 있는 검사 없음(wrapper): `POL-0095-R17`, `POL-0095-R18`, `POL-0095-R19`, `POL-0095-R20`, `POL-0095-R21`
- 이름 있는 검사 없음(deny 대응): `POL-0095-R22`
- 이름 있는 검사 없음(범위): `POL-0095-R23`, `POL-0095-R24`, `POL-0095-R25`, `POL-0095-R26`
- 수동 검토·승인에 의존(allowlist): `POL-0095-R6`
- 정책이 스스로 밝힌 한계: 이 도구의 PASS는 전체 인프라 보안 준수 판정이 아니며 inline Dockerfile과 최종 Compose·실행 상태의 통제는 별도로 요구된다.
- `leaf.conftest-policy-tests`(`--mode verify`)는 local 전용이고 CI는 `leaf.conftest-policy`(`--mode corpus`)만 실행한다.

#### Ownership

##### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

##### Review Triggers

- [가이드](../../01.guides/12.testing-and-quality/0095-conftest.md) (`GDE-0095`)
- [런북](../../03.runbooks/12.testing-and-quality/0095-conftest.md) (`RUN-0095`)
- [Dependency version management](../10.platform-and-backup/0086-dependency-version-management.md)

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
