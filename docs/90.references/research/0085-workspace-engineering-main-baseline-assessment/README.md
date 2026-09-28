---
title: "Workspace Engineering Main Baseline Assessment"
version: "0.4.1"
type: "reference/research-pack"
status: "review"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0085"
parent_ids: []
created: "2026-09-04"
observed_at: "2026-09-05"
---

# Workspace Engineering Main Baseline Assessment

현재 routing(2026-09-06): [공통 Agent 거버넌스](../../../../.agents/README.md)와
[ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md)가
활성 source 위치를 소유합니다. 아래의 이전 Stage 00 경로, inventory,
provider 투영, check 결과는 날짜가 있는 관찰로 남으며, 현재 지시나 새
runtime 수용 증거가 아닙니다. Source 링크는 이제 현재 owner로
연결되며, 원래의 `observed_at`, `reviewed_at`, status, 측정된 사실은
그대로 보존됩니다.

## Question

현재 workspace-baseline 소유권이 RES-0002-m0020으로 통합된 뒤,
`main@4c6d211129615eab372d720ebd209b6c27618c86` 평가에서 어떤 binding
범위, 증거 경계, identity-recovery provenance를 보존해야 하는가?

이 package는 더 이상 가변적인 현재 상태 결론을 소유하지 않습니다.
publication lifecycle이 review를 거치는 동안 날짜가 있는 평가 envelope와
복구된 request identity를 보존합니다.

이 package는 [RES-0002](../0002-agentic-engineering-research-pack/README.md)
아래에서 보존된, 날짜가 있는 증거 carrier입니다. 현재 baseline owner인
[RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)이나
전문 GitHub Actions 증거인
[RES-0084](../0084-github-actions-platform/README.md)와 경쟁하지 않습니다.
identity-recovery tuple과 관찰 경계는 그대로 유지됩니다.

## Scope

- 날짜가 있는 저장소 baseline: `buenhyden/hy-home.docker`
  `main@4c6d211129615eab372d720ebd209b6c27618c86`.
- 저장소 관찰 날짜: 2026-09-05; 외부 source 확인 날짜: 2026-09-05.
- 포함: 원래 binding request, 정확한 baseline identity, 증거 class 정의,
  SPEC-0172 recovery tuple, 이 평가를 해석하는 데 필요한 날짜가 있는
  관찰.
- 제외: secret 또는 credential 값, 사용자 전역 Claude/Codex 설정, shell
  history, raw log, 새 provider call, 새 runtime 변경, live deployment,
  tag, release.
- 현재 baseline 해석과 주제 연구는
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)과
  그 형제 구성원이 소유합니다. GitHub Actions mechanics는
  [RES-0084](../0084-github-actions-platform/README.md)에 남습니다.

## Method

1. 정확한 baseline SHA, 관찰 날짜, source request, 복구된 artifact
   identity, 상호 Task decision을 보존합니다.
2. question, 증거 모델, lifecycle, decision-route 기준으로 이 package의
   question을 RES-0002-m0020과 비교합니다.
3. recovery carrier를 옮기거나 재식별하지 않고 가변적인 현재 baseline
   소유권을 RES-0002-m0020으로 옮깁니다.
4. 여기에는 날짜가 있는 증거만 남기고, 주제나 현재 claim은 canonical
   구성원으로 route합니다.
5. `draft`에서 `review`로의 forward transition, identity recovery,
   inbound link, 보호된 RES-0002 집합, 생성된 index 신선도를
   검증합니다.

## Findings

| Evidence retained here | Dated result | Evidence depth | Current owner / disposition |
| --- | --- | --- | --- |
| Assessment target | `main@4c6d211129615eab372d720ebd209b6c27618c86`, 2026-09-05 관찰 | Defined, Local-executed | 역사적 평가 경계; 현재 baseline은 RES-0002-m0020으로 이동 |
| Request identity | `RES-0085-SCOPE`가 같은 package 안에서 `RES-0085-m0001`로 복구됨 | Repository-enforced | 정확한 carrier와 상호 SPEC-0173 Task 1 tuple을 보존 |
| Evidence classes | 저장소, Hosted, provider, runtime, remote 관찰은 서로 대체할 수 없음 | Defined | RES-0002-m0020이 이 class를 현재 결론에 적용 |
| Hosted and remote observations | 완료된 SPEC-0172 결과가 정확한 Hosted 실행과 2026-09-05 protection read-back을 기록 | Hosted-executed, cutoff 시점 Remote-verified | 완료된 Spec과 main-protection record가 날짜가 있는 증거를 보존 |
| Deployment and release | 정확한 target이나 version이 제공되지 않음 | Unverified / 채택되지 않음 | 수용 claim 없음; 별도 SDLC 작업 필요 |
| Consolidation lifecycle | package와 구성원이 `draft`에서 `review`로 진행 | Repository-enforced | publication과 이후 supersession은 후속 forward transition이 필요 |

세부 현재 finding은 여기서 반복하지 않습니다. 그 내용은
[RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)에
통합되어 있습니다.

## Sources

- 저장소 baseline: Git commit
  `4c6d211129615eab372d720ebd209b6c27618c86`.
- [공통 Agent 거버넌스](../../../../.agents/README.md)와
  [provider registry](../../../../.agents/governance/providers/registry.yaml).
- [Stage 99 Registry](../../../99.templates/registry.json),
  [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  [research-member template](../../../99.templates/templates/references/research.template.md).
- [완료된 SPEC-0172 결과](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md)와
  [현재 identity-recovery decision](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md).
- [CI workflow](../../../../.github/workflows/ci-quality.yml),
  [workflow contract](../../../../.github/workflow-contract.yml),
  [main protection record](../../../../.github/rulesets/main-protection.md).
- [GitHub ruleset status-check rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
  [Docker Compose specification](https://docs.docker.com/compose/compose-file/),
  [Claude Code feature model](https://code.claude.com/docs/en/features-overview),
  [Codex sandbox and approval controls](https://openai.com/index/running-codex-safely/),
  2026-09-05에 다시 확인함.
- 세부 주제와 현재 baseline source는 대응하는 RES-0002 구성원과
  RES-0084에 남습니다; 이 날짜가 있는 증거 package는 그 source
  inventory를 복사하지 않습니다.

## Implications

- 현재 workspace-baseline 결론과 향후 baseline 재관찰에는
  RES-0002-m0020을 사용합니다.
- forward publication lifecycle이 이후 `superseded` 전이를 허용할 때까지
  이 package를 그대로 유지합니다; redirect로 대체하지 않습니다.
- 그 lifecycle 동안 정확한 identity-recovery tuple과 Task decision을
  보존합니다.
- 실행 가능한 현재 gap은 canonical RES-0002 구성원과 일반적인
  Requirement-to-Task chain을 통해 route합니다.

## Traceability

- 현재 baseline, 주제 구성원, 보존 선언:
  [RES-0002](../0002-agentic-engineering-research-pack/README.md)와
  [RES-0002-m0020](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md).
- GitHub Actions mechanics: [RES-0084](../0084-github-actions-platform/README.md).
- Binding scope: [RES-0085-m0001](m0001-request-scope.md).
- Governance authority: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md),
  [ADR-0032 Canonical Agent Governance Home](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md).
- Lifecycle authority: [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md),
  [AD-0030](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md),
  ADR-0031.
- 현재 identity-recovery owner: [SPEC-0173 Task 1](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md);
  [완료된 SPEC-0172 결과](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md)가 날짜가 있는 구현 결과를 보존.
- Operations authority: [Stage 05](../../../05.operations/README.md).
- Audit/data 증거: implementation overview, [k6 guide](../../../05.operations/guides/0061-k6.md),
  LLM Wiki index, repository map.
- Package registry: [Research index](../README.md)와
  [Stage 99 Registry](../../../99.templates/registry.json).

## Limitations

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
