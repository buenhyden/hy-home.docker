---
title: "Reference: GitHub Actions Platform Mechanics"
version: "2.2.0"
type: "reference/research-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0084"
created: "2026-07-05"
observed_at: "2026-09-05"
---

# Reference: GitHub Actions Platform Mechanics

## Overview

### Overview

## Scope

- 저장소 baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- 저장소와 외부 관찰 날짜: 2026-09-05.
- 포함: workflow 권한, token/OIDC 모델, trigger, untrusted input, action
  pinning, concurrency, runner, aggregate gate, ruleset, required check,
  Hosted 증거, rollback.
- 제외: secret 값, 승인된 read-back에 없는 조직 정책, environment/deployment
  변경, artifact publication, 새 workflow dispatch, tag, release.
- Stage 90은 증거와 implication을 기록합니다. Workflow/configuration
  권위는 `.github/`에, 실행 증거는 소유 Task에, remote 사실은 날짜가 있는
  인증된 read-back에 남습니다.

## Structure

### Structure

## Usage

### Usage

### Question

이 저장소에 중요한 GitHub Actions 보안, 실행, 권한, identity,
supply-chain, runner, remote-enforcement mechanics는 무엇이며, 그 가운데
실제로 구성되었거나 실행되었거나 remote로 검증된 것은 무엇인가?

세부 platform 분석은
[RES-0084-m0001](m0001-platform-mechanics.md)이 소유합니다. 이 README는
package question, 증거 경계, 결과 요약, navigation만 소유합니다.

이 package는 [RES-0002](../0002-agentic-engineering-research-pack/README.md)의
cross-package routing 아래에서 GitHub Actions 전문 증거를 소유합니다.
경쟁하는 workspace baseline이나 일반 automation inventory가 아닙니다:
현재 cross-category 결론은 RES-0002를 통해 route되고, 세부 workflow,
Hosted, remote-control-plane 증거는 여기 남습니다.

### Method

1. 600줄짜리 package README를 남기거나 경쟁하는 research package를
   만드는 대신, 기존 platform 분석을 구성원으로 보존합니다.
2. 현재 workflow YAML과 typed workflow 계약을 2026-09-05에 다시 연 공식
   GitHub 문서와 비교합니다.
3. 추적된 configuration을 remote 증거로 취급하지 않고 SPEC-0172의 정확한
   Hosted 실행과 remote protection 증거를 사용합니다.
4. claim을 Configured, Repository-enforced, Hosted-executed,
   Remote-verified, Unverified로 분류합니다.
5. 분리 이후 구성원 identity, 링크, 생성된 index 신선도, public 저장소
   gate를 검증합니다.

### Findings

| Category | Member | Repository state | Evidence depth | Priority |
| --- | --- | --- | --- | --- |
| Permissions, OIDC, reusable actions/workflows, untrusted input, supply chain, execution, rulesets, runners, and static analysis | [Platform mechanics](m0001-platform-mechanics.md) | workflow 여섯 개; CI aggregate job 두 개; full-SHA action pin; least-privilege 권한 | Configured, Repository-enforced, Hosted-executed | High |
| Required status checks | [Platform mechanics](m0001-platform-mechanics.md) | `strict=true`; `validation-changed`와 `validation-full`이 app ID 15368에 결합됨 | 2026-09-05에 Remote-verified | High |
| CD, OIDC, environment, deployment, release | [Platform mechanics](m0001-platform-mechanics.md) | 정확한 live target이나 현재 publication route 없음 | Unverified / 채택되지 않음 | target이 생기면 High |

이전 package revision 대비 가장 큰 변화는 구조적입니다: 세부 분석이
구성원으로 옮겨졌습니다. 가장 큰 증거 변화는 Hosted aggregate job과
remote required-check 대체가 이제 관찰되었다는 점이며, deployment와
release는 여전히 증거 경계 밖에 있습니다.

### Sources

- [GitHub ruleset status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
- [GitHub Actions script injection](https://docs.github.com/en/actions/concepts/security/script-injections).
- [GitHub Actions OIDC](https://docs.github.com/en/actions/reference/security/oidc).
- [Workflow contract](../../../../.github/workflow-contract.yml)와
  [CI Quality Gates](../../../../.github/workflows/ci-quality.yml).
- [Main protection record](../../../../.github/rulesets/main-protection.md).
- [완료된 SPEC-0172 결과](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md).

세부 source inventory와 claim 단위 분석은 구성원이 소유합니다.

### Implications

- 인증된 read-back이 일치하는 동안 두 aggregate CI job을 workflow
  identity이자 strict required check로 유지합니다.
- 불일치 시 롤백에는 기록된 12-check 이전 상태를 사용하며, job 표시
  이름에서 대체를 추론하지 않습니다.
- 명시적 least-privilege 권한과 불변 action SHA를 계속 사용합니다.
- OIDC, environment, promotion, deployment는 명명된 target, trust
  boundary, 승인, 수용, rollback 계약이 생긴 뒤에만 도입합니다.
- 어떤 구현이든 Requirement → Architecture/ADR → Spec → Plan → Task →
  검증 → 독립 검토를 거쳐 route합니다.

### Limitations

- Remote protection은 2026-09-05 read-back 시점에만 검증되었습니다;
  이후 상태는 다를 수 있습니다.
- 이번 갱신에서는 secret, environment 값, artifact, raw log, 조직 수준
  Actions 정책을 조회하지 않았습니다.
- 새 workflow dispatch나 deployment, release, tag, provider 변경은
  없었습니다.
- Hosted CI 성공은 명명된 revision과 run만 증명하며, 미래 runner나 외부
  서비스 가용성을 증명하지 않습니다.
- GitHub platform 문서는 2026-09-05 이후 바뀔 수 있습니다.

## Related Documents

### Traceability

- Member: [RES-0084-m0001](m0001-platform-mechanics.md).
- Research index: [Research Packages](../README.md).
- 관련 주제 연구: [automation](../0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md),
  [quality](../0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md),
  [security](../0002-agentic-engineering-research-pack/m0017-security-governance.md),
  [verification](../0002-agentic-engineering-research-pack/m0019-verification-validation.md).
- 현재 baseline: [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).
- 날짜가 있는 baseline/recovery 증거:
  [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md).
- Governance: [공통 Agent 거버넌스](../../../../.agents/README.md).
- Requirement/Architecture: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md),
  [ADR-0032 Canonical Agent Governance Home](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md).
- Implementation/evidence: [완료된 SPEC-0172 결과](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md)와
  [현재 lifecycle reconciliation](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md).
- Templates and Registry: [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  [research-member template](../../../99.templates/templates/references/research.template.md),
  [Registry](../../../99.templates/registry.json).
