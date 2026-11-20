---
title: "Provider Adapters"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Provider Adapters
  layer: provider
updated: "2026-11-20"
---

# Provider Adapters

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

Provider adapter는 agent governance policy, role, skill을 runtime syntax로
번역합니다. 공유 동작을 소유하지 않습니다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

Claude와 Codex만 지원됩니다. `registry.yaml`은 provider identity, work-profile
model 선택, permission translation, projection path, semantic event, hook
command에 대한 machine authority입니다. workflow, approval, retry, evidence,
stop, document-profile 규칙은 소유하지 않습니다.

##### Excluded Responsibilities

Provider adapter는 공유 동작을 소유하지 않으며, `registry.yaml`은 workflow, approval, retry, evidence, stop, document-profile 규칙을 소유하지 않습니다.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

| Path | Purpose |
| --- | --- |
| [registry.yaml](registry.yaml) | provider identity와 native 번역 사실 |

- [Claude provider](../../../.claude/provider.md) — Claude의 authored loading 방식과 runtime 동작.
- [Codex provider](../../../.codex/provider.md) — Codex의 authored loading 방식과 runtime 동작.

###### Classification
<!-- core-payload-level:4 -->

이 폴더의 정본은 `registry.yaml` 하나입니다. provider별 authored 문서(`.claude/provider.md`, `.codex/provider.md`)는 loading과 syntax 차이만 소유하며 공유 정책을 소유하지 않습니다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Bootstrap policy](../bootstrap.md)
- [Provider capability matrix](../provider-capability-matrix.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [Governance hub](../../README.md)
- [문서 작성 계약](../../../docs/00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- README 템플릿 `docs/99.templates/02.templates/91.agent-governance/provider-index.template.md`: 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다.

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

provider-neutral 동작은 agent governance policy, role, skill source에서
변경합니다. provider fact는 `.agents/governance/providers/registry.yaml`에서
변경하고 대응하는 authored native `provider.md`를 갱신합니다. 생성된 native
README는 output일 뿐이며 canonical `.agents/` source는 결코 renderer
output이 아닙니다. 승인된 canonical 변경 후에는 provider renderer를
`--write`로 한 번 실행하고 즉시 `--check`로 실행합니다. 일반 validation과
CI는 `--check`만 사용합니다.
`--write`가 quarantine된 stale projection을 보고하면 멈춥니다: 이 명령은
active provider path에서 제거했지만 재검증된 blob을
`.provider-surface-quarantine/` 아래에 의도적으로 보존했습니다. 보고된
path를 승인된 retirement와 Git recovery boundary에 대해 검증하고 명시적
cleanup 단계에서 그 정확한 quarantine 파일만 제거한 뒤 `--write`와
`--check`를 다시 실행합니다. 대기 중인 cleanup은 실패한 `--check` 상태이며
convergence로 보고해서는 안 됩니다.

###### Transition and Exit
<!-- core-payload-level:4 -->

이 README는 `navigation` 수명주기의 `active` 상태만 가지며 다른 상태로 전이하지 않습니다. 목록 항목을 추가·이동·삭제할 때 이 문서를 함께 갱신하고, 삭제한 항목의 이력은 Git이 기록합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
