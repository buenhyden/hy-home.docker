---
title: "OpenTofu Policy"
version: "2.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
layer: "operations"
artifact_id: "POL-0082"
parent_ids:
- "AD-0009"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# OpenTofu Policy

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

OpenTofu는 명시적인 `iac` job이다. 정적 선택과 검증은 provider 계정을 읽거나
원격 인프라를 변경할 권한을 결코 뜻하지 않는다.

###### Authority
<!-- core-payload-level:4 -->

- [Platform Operations·Quality 아키텍처](../../../02.architecture/01.descriptions/0009-tooling-architecture.md)

- [OpenTofu Compose 소스](../../../../infra/09-platform-ops/opentofu/docker-compose.yml)
- [파생 Compose 이미지 projection](../../../../infra/tech-stack.versions.json)

##### Applies To

로컬 이미지 빌드, `/workspace`, 마운트된 클라우드 자격 증명, 백엔드 상태,
lock, plan, provider 작업, 업그레이드, 서비스 폐기.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0082-R1 | 활성화 시 | 필수: `iac` 아래에서 루트 프로젝트의 명명된 `opentofu` job을 호출한다 | 수동 | none |
| POL-0082-R2 | 항상 | 금지: HOME이나 일반 tooling 시작에 `opentofu` 포함 | 수동 | none |
| POL-0082-R3 | 항상 | 필수: 계정, workspace, 백엔드, 예상 리소스, 허용된 명령 클래스를 식별한다 | 수동 | none |
| POL-0082-R4 | 항상 | 금지: plan 권한을 apply, destroy, import, 상태 변경, force-unlock 승인으로 취급 | 수동 | none |
| POL-0082-R5 | 항상 | 필수: 마운트된 AWS/Azure 디렉터리를 읽기 전용이어도 민감한 권한으로 취급한다 | 수동 | none |
| POL-0082-R6 | 항상 | 금지: workspace에 자격 증명 추가 또는 값 캡처 | 수동 | none |
| POL-0082-R7 | 항상 | 필수: 상태와 저장된 plan을 Git, stdout 증거, 공유 로그에서 제외한다 | 수동 | none |
| POL-0082-R8 | 항상 | 필수: 백업은 모드 `0600`과 별도의 보존 소유자로 보호한다 | 수동 | none |
| POL-0082-R9 | 항상 | 필수: 백엔드 잠금을 보존한다 | 수동 | none |
| POL-0082-R10 | force-unlock 시 | 필수: 어떤 운영자나 자동화도 해당 lock을 소유하지 않는다는 증명을 갖추고 기록된 lock ID만 대상으로 한다 | 수동 | none |
| POL-0082-R11 | 상태 변경/업그레이드 전 | 필수: 로컬 상태와 원격 상태를 식별하고 보호된 스냅샷을 만든다 | 수동 | none |
| POL-0082-R12 | 상태 변경/업그레이드 전 | 필수: 격리된 상태에서 복구를 리허설한다 | 수동 | none |
| POL-0082-R13 | 업그레이드 시 | 필수: 중간 노트를 검토하고 provider/백엔드 호환성을 검증한다 | 수동 | none |
| POL-0082-R14 | 런타임 소스 변경 전 | 필수: 적용되지 않은 plan을 비교한다 | 수동 | none |
| POL-0082-R15 | 제거 시 | 필수: 관리되는 모든 리소스에 후속 시스템이 생길 때까지 workspace, 백엔드 상태, 자격 증명, 소유권 기록을 보존한다 | 수동 | none |
| POL-0082-R16 | 항상 | 금지: 컨테이너 제거로 인프라를 파괴 | 수동 | none |
| POL-0082-R17 | 버전 조회·format/validate 시 | 필수: 선언된 마운트와 실행 영향을 확인한다 | 수동 | none |
| POL-0082-R18 | 복구 시 | 필수: 사용한 이미지·provider lock 식별자를 보존한다 | 수동 | none |
| POL-0082-R19 | Terraform workspace 이관 시 | 필수: 기존 state와 lock 정보를 보존하고 암호화된 복구본을 먼저 준비한다 | 수동 | none |
| POL-0082-R20 | Terraform workspace 이관 시 | 필수: 복제 workspace에서 provider 및 backend 호환성을 검증하고 이관 대상별 실제 엔진을 확인한다 | 수동 | none |
| POL-0082-R21 | Terraform workspace 이관 시 | 필수: CLI 교체와 실제 remote resource 변경을 별도 검토한다 | 수동 | none |
| POL-0082-R22 | `apply`, `destroy`, state rewrite, force-unlock 시 | 필수: 정확한 대상 승인을 받는다 | 수동 | none |
| POL-0082-R23 | 항상 | 금지: 새로운 Terraform 서비스나 병렬 updater 생성 | 수동 | none |
| POL-0082-R24 | 호환성 때문에 기존 CLI가 필요할 때 | 필수: 담당자, 대상 workspace, 지원 종료 조건과 검증 계획을 기록한다 | 수동 | none |
| POL-0082-R25 | 항상 | 금지: private state 공개 | 수동 | none |

- **Activation:** `iac` 아래에서 루트 프로젝트의 명명된 `opentofu` job을
  호출한다. HOME이나 일반 tooling 시작에는 절대 포함하지 않는다.
- **Authorization:** 계정, workspace, 백엔드, 예상 리소스, 허용된 명령
  클래스를 식별한다. plan 권한을 받았다고 apply, destroy, import, 상태 변경,
  또는 force-unlock까지 승인된 것은 아니다.
- **Credentials:** 마운트된 AWS/Azure 디렉터리는 읽기 전용이더라도 민감한
  권한이다. workspace에 자격 증명을 추가하거나 값을 캡처하지 않는다.
- **State and plans:** 상태와 저장된 plan에는 시크릿이 포함될 수 있다. Git,
  stdout 증거, 공유 로그에서 제외한다. 백업은 모드 `0600`과 별도의 보존
  소유자로 보호한다.
- **Locking:** 백엔드 잠금을 보존한다. Force-unlock을 하려면 어떤 운영자나
  자동화도 해당 lock을 소유하지 않는다는 증명이 있어야 하며 기록된 lock ID만
  대상으로 한다.
- **Backup/recovery:** 로컬 상태와 원격 상태를 식별하고 상태 변경/업그레이드
  전에 보호된 스냅샷을 만들며 격리된 상태에서 복구를 리허설한다.
- **Upgrade:** 중간 노트를 검토하고, provider/백엔드 호환성을 검증하며,
  런타임 소스를 변경하기 전에 적용되지 않은 plan을 비교한다.
- **Removal:** 관리되는 모든 리소스에 후속 시스템이 생길 때까지 workspace,
  백엔드 상태, 자격 증명, 소유권 기록을 보존한다. 컨테이너 제거가 의도적으로
  인프라를 파괴하는 일은 결코 없다.

###### 책임과 도구 범위
<!-- core-payload-level:4 -->

책임자는 `@buenhyden`이다. 버전 조회·format/validate라도 선언된 마운트와
실행 영향을 확인한다. 정확한 바이너리 태그 외의 distro 패키지와 provider 선택은
완전히 고정된 빌드가 아니므로 복구 시 사용한 이미지·provider lock 식별자를 보존한다.

###### Terraform 이관
<!-- core-payload-level:4 -->

- 기존 state와 lock 정보를 보존하고 암호화된 복구본을 먼저 준비한다.
- 복제 workspace에서 provider 및 backend 호환성을 검증하고, 이관 대상별 실제 엔진을 확인한다.
- CLI 교체와 실제 remote resource 변경을 별도 검토한다. `apply`, `destroy`, state rewrite와 force-unlock은 정확한 대상 승인을 요구한다.
- 새로운 Terraform 서비스나 병렬 updater를 만들지 않는다. 호환성 때문에 기존 CLI가 필요하면 담당자, 대상 workspace, 지원 종료 조건과 검증 계획을 기록하며 private state 공개는 허용하지 않는다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

별도의 변경 승인, 상태 보호, 또는 lock 소유권을 우회하는 예외는 없다. 범위,
만료, 복구 아티팩트, 종료 조건을 기록한다.

###### Approval and Review
<!-- core-payload-level:4 -->

모든 provider/백엔드/런타임 업그레이드 전, 그리고 자격 증명 마운트, 네트워크
접근, 또는 workspace 소유권이 변경될 때마다 검토한다.

#### Enforcement

##### Mechanisms

정적 Compose 점검은 선택만 증명한다. 런타임 증거는 버전, init/validate,
plan, apply, apply 이후 결과를 구분한다. 실행되지 않은 상태 복구와 업그레이드
리허설은 공백으로 남는다.

##### Limits

정책은 정적 Compose 점검이 선택만 증명한다고 밝히며 모든 규칙은 전용 검사 없이 수동 검토와 승인에 의존한다.

- 활성화: 수동 검토/승인에 의존: `POL-0082-R1`, `POL-0082-R2`
- 권한: 수동 검토/승인에 의존: `POL-0082-R3`, `POL-0082-R4`
- 자격 증명: 수동 검토/승인에 의존: `POL-0082-R5`, `POL-0082-R6`
- 상태·plan: 수동 검토/승인에 의존: `POL-0082-R7`, `POL-0082-R8`
- 잠금: 수동 검토/승인에 의존: `POL-0082-R9`, `POL-0082-R10`
- 백업·복구: 수동 검토/승인에 의존: `POL-0082-R11`, `POL-0082-R12`
- 업그레이드: 수동 검토/승인에 의존: `POL-0082-R13`, `POL-0082-R14`
- 제거: 수동 검토/승인에 의존: `POL-0082-R15`, `POL-0082-R16`
- 도구 범위: 수동 검토/승인에 의존: `POL-0082-R17`, `POL-0082-R18`
- Terraform 이관: 수동 검토/승인에 의존: `POL-0082-R19`, `POL-0082-R20`, `POL-0082-R21`, `POL-0082-R22`, `POL-0082-R23`, `POL-0082-R24`, `POL-0082-R25`
- 실행되지 않은 상태 복구와 업그레이드 리허설은 공백(`NOT_RUN`)으로 남는다.
- 런타임 증거는 버전, init/validate, plan, apply, apply 이후 결과를 구분해야 한다.
- 정확한 바이너리 태그 외의 distro 패키지와 provider 선택은 완전히 고정된 빌드가 아니다.

#### Ownership

##### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

##### Review Triggers

- [가이드](../../01.guides/10.platform-and-backup/0082-opentofu.md) (`GDE-0082`)
- [런북](../../03.runbooks/10.platform-and-backup/0082-opentofu.md) (`RUN-0082`)

- [OpenTofu 상태 저장소](https://opentofu.org/docs/language/state/backends/)
- [OpenTofu state 명령 안전성](https://opentofu.org/docs/cli/commands/state/)
- [운영 인덱스](../../README.md)

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
