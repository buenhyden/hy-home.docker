---
title: "Workspace Engineering Main Baseline Assessment"
version: "1.0.0"
type: "reference/research-pack"
status: "in-review"
owner: "@buenhyden"
document_scope:
  subject: Workspace Engineering Main Baseline Assessment
  layer: reference
updated: "2026-11-20"
layer: "references"
artifact_id: "RES-0085"
created: "2026-09-04"
observed_at: "2026-09-05"
---

# Workspace Engineering Main Baseline Assessment

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

###### Overview
<!-- core-payload-level:4 -->

`main@4c6d211129615eab372d720ebd209b6c27618c86` 평가에서 어떤 binding
범위, 증거 경계, identity-recovery provenance를 보존해야 하는가?

이 package는 더 이상 가변적인 현재 상태 결론을 소유하지 않습니다.
publication lifecycle이 review를 거치는 동안 날짜가 있는 평가 envelope와
복구된 request identity를 보존합니다.

이 package는 [RES-0002](../0002-agentic-engineering-research-pack/README.md)
아래에서 보존된, 날짜가 있는 증거 carrier입니다.
[RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)은
과거 workspace-baseline 종합을, [RES-0084](../0084-github-actions-platform/README.md)는
GitHub Actions 주제 연구를 담습니다. 이 package는 identity-recovery tuple과
관찰 경계를 보존합니다.

###### Scope
<!-- core-payload-level:4 -->

- 날짜가 있는 저장소 baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- 저장소 관찰 날짜: 2026-09-05; 외부 source 확인 날짜: 2026-09-05.
- 포함: 원래 binding request, 정확한 baseline identity, 증거 class 정의,
  SPEC-0172 recovery tuple, 이 평가를 해석하는 데 필요한 날짜가 있는
  관찰.
- 제외: secret 또는 credential 값, 사용자 전역 Claude/Codex 설정, shell
  history, raw log, 새 provider call, 새 runtime 변경, live deployment,
  tag, release.
- 당시 baseline 해석과 주제 연구는
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)과
  그 형제 구성원에서 확인합니다. GitHub Actions mechanics는
  [RES-0084](../0084-github-actions-platform/README.md)에 남습니다.

##### Excluded Responsibilities

- secret, credential 값, 개인 key, environment 값, raw log, shell
  history, 사용자 전역 provider 설정은 조회하지 않았습니다.
- 이번 pass는 provider call, Compose service 시작, deployment, restart,
  rollout, recovery, tag, release 변경을 수행하지 않았습니다.
- 2026-09-04 provider/runtime과 2026-09-05 GitHub control-plane 증거는
  SPEC-0172의 point-in-time 기록이며 영구 보장이 아닙니다.
- `review`는 terminal disposition이 아닙니다. 이 package는 publication
  lifecycle이 이후 승인된 변경을 통해 진행될 때까지 남아 있습니다.
- Static Compose rendering은 네 가지 AUD-0097 domain 결함을 해결하지
  않으며 service 건강성, 내구성, 복구, 성능, production 적합성을 증명하지
  않습니다.
- 가변적인 외부 source는 2026-09-05 이후 바뀔 수 있습니다; 유료 ISO
  텍스트는 조회하지 않았고 public catalog/definition 자료만 그 공개
  범위 안에서 사용했습니다.

Revalidated 2026-11-06: AUD-0097은 2026-09-09에 은퇴했고 audit 범주에는
현재 package가 없습니다(`docs/90.references/02.audits/README.md`). 위 AUD-0097
언급은 날짜가 있는 관찰로 보존합니다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [m0001-request-scope.md](m0001-request-scope.md) | RES-0085-m0001: 원래 binding request와 복구된 request identity |

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 member의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

- 과거 workspace-baseline 종합은 RES-0002-m0020에서 확인합니다. 현재 구현은
  해당 소유자의 추적 소스로, 새 관찰은 범위가 승인된 Task의 증거로 확인합니다.
- forward publication lifecycle이 이후 `superseded` 전이를 허용할 때까지
  이 package를 그대로 유지합니다; redirect로 대체하지 않습니다.
- 그 lifecycle 동안 정확한 identity-recovery tuple과 Task decision을
  보존합니다.
- 현재 개선 사항은 소유 Requirement와 해당 Task에서 다룹니다.

###### Related Documents
<!-- core-payload-level:4 -->

- 과거 baseline 종합, 주제 구성원, 보존 선언:
  [RES-0002](../0002-agentic-engineering-research-pack/README.md)와
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).
- GitHub Actions mechanics: [RES-0084](../0084-github-actions-platform/README.md).
- Binding scope: [RES-0085-m0001](m0001-request-scope.md).
- Governance authority: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../00.workspace/02.architecture/01.descriptions/0027-agent-governance-canonical-adapter.md),
  [ADR-0032 Canonical Agent Governance Home](../../../00.workspace/02.architecture/02.decisions/0032-canonical-agent-governance-home.md).
- Lifecycle authority: [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md),
  [AD-0030](../../../00.workspace/02.architecture/01.descriptions/0030-document-lifecycle-governance.md),
  ADR-0031(은퇴; Git 이력).
- Identity-recovery 기록: SPEC-0173 Task 1과 완료된 SPEC-0172 결과.
  두 Spec은 tree에서 은퇴했으며 본문은 Git 이력에 있습니다.
- Operations authority: [Stage 05](../../../05.operations/README.md).
- 운영 증거: [k6 guide](../../../05.operations/01.guides/12.testing-and-quality/0061-k6.md).
  2026-09-05에 함께 인용된 implementation overview, LLM Wiki index,
  repository map은 은퇴했습니다.
- Package registry: [Research index](../README.md)와
  [Stage 99 Registry](../../../99.templates/registry.json).

##### Checks

###### Method
<!-- core-payload-level:4 -->

1. 정확한 baseline SHA, 관찰 날짜, source request, 복구된 artifact
   identity, 상호 Task decision을 보존합니다.
2. question, 증거 모델, lifecycle, decision-route 기준으로 이 package의
   question을 RES-0002-m0020과 비교합니다.
3. 당시 통합 결정은 recovery carrier의 경로와 식별자를 보존하면서
   workspace-baseline 종합을 RES-0002-m0020으로 옮겼습니다.
4. 이 package에 날짜가 있는 증거를 보존하고 주제 연구는 관련 구성원에 연결합니다.
5. `draft`에서 `review`로의 forward transition, identity recovery,
   inbound link, 보호된 RES-0002 집합, 생성된 index 신선도를
   검증합니다.

###### Sources
<!-- core-payload-level:4 -->

- 저장소 baseline: Git commit
  `4c6d211129615eab372d720ebd209b6c27618c86`.
- [공통 Agent 거버넌스](../../../../.agents/README.md)와
  [provider registry](../../../../.agents/governance/providers/registry.yaml).
- [Stage 99 Registry](../../../99.templates/registry.json),
  [research-pack template](../../../99.templates/02.templates/90.references/research-pack.template.md),
  [research-member template](../../../99.templates/02.templates/90.references/research.template.md).
- 완료된 SPEC-0172 결과와
  현재 identity-recovery decision.
- [CI workflow](../../../../.github/workflows/ci-quality.yml),
  [workflow contract](../../../../.github/workflow-contract.yml),
  [main protection record](../../../../.github/rulesets/main-protection.md).
- [GitHub ruleset status-check rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
  [Docker Compose specification](https://docs.docker.com/compose/compose-file/),
  [Claude Code feature model](https://code.claude.com/docs/en/features-overview),
  [Codex sandbox and approval controls](https://openai.com/index/running-codex-safely/),
  2026-09-05에 다시 확인함.
- 세부 주제와 당시 baseline source는 대응하는 RES-0002 구성원과 RES-0084에서
  확인합니다.

###### Findings
<!-- core-payload-level:4 -->

| Evidence retained here | Dated result | Evidence depth | Current owner / disposition |
| --- | --- | --- | --- |
| Assessment target | `main@4c6d211129615eab372d720ebd209b6c27618c86`, 2026-09-05 관찰 | Defined, Local-executed | 역사적 평가 경계; RES-0002-m0020에 당시 종합을 보존 |
| Request identity | `RES-0085-SCOPE`가 같은 package 안에서 `RES-0085-m0001`로 복구됨 | Repository-enforced | 정확한 carrier와 상호 SPEC-0173 Task 1 tuple을 보존 |
| Evidence classes | 저장소, Hosted, provider, runtime, remote 관찰은 서로 대체할 수 없음 | Defined | RES-0002-m0020의 역사적 평가에 적용 |
| Hosted and remote observations | 완료된 SPEC-0172 결과가 정확한 Hosted 실행과 2026-09-05 protection read-back을 기록 | Hosted-executed, cutoff 시점 Remote-verified | 완료된 Spec과 main-protection record가 날짜가 있는 증거를 보존 |
| Deployment and release | 정확한 target이나 version이 제공되지 않음 | Unverified / 채택되지 않음 | 수용 claim 없음; 별도 SDLC 작업 필요 |
| Consolidation lifecycle | package와 구성원이 `draft`에서 `review`로 진행 | Repository-enforced | publication과 이후 supersession은 후속 forward transition이 필요 |

당시 평가의 세부 finding은
[RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)에
통합되어 있습니다.

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
