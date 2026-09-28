---
title: "Research Packages"
version: "1.5.0"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
created: "2026-07-02"
---

# Research Packages

## Overview

외부 증거와 출처 기반 분석입니다. Research package는 현재 owner를
대체하지 않고 정보를 제공합니다.

Stage 90 authority boundary와 package lifecycle 규칙은
[References index](../README.md)와 Stage 99 Registry가 정의합니다.

## Packages

| Stable ID | Package | Status |
| :--- | :--- | :--- |
| RES-0001 | Agentic Engineering Research Pack | 은퇴; 본문은 `docs/98.archive/retired/` 아래에 보존되며 tombstone으로 기록됨 |
| [RES-0002](./0002-agentic-engineering-research-pack/README.md) | Agentic Engineering Research Pack; canonical 외부 연구·역사 증거 hub | active |
| [RES-0084](./0084-github-actions-platform/README.md) | Reference: GitHub Actions Platform Mechanics; RES-0002 routing 아래 전문 증거 | active |
| [RES-0085](./0085-workspace-engineering-main-baseline-assessment/README.md) | Workspace Engineering Main Baseline Assessment; RES-0002를 위한 보존된 날짜 증거 | review — 날짜가 있는 증거; 이후 전이는 별도 승인 필요 |
| [RES-0096](./0096-archive-disposition-consistency/README.md) | Archive Disposition Consistency Assessment; RES-0002에서 링크되는 별도 archive-domain 증거 | draft — SPEC-0177, SPEC-0178을 위한 날짜 증거 |

### Consolidated Package Routing

`RES-0002`는 현재 주제 연구와 cross-category routing의 canonical hub입니다.
관련된 세 package는 증거 모델이 본질적으로 달라서 별도로
남습니다.

| Package | Canonical role | Integration rule |
| --- | --- | --- |
| RES-0084 | GitHub Actions platform mechanics와 날짜가 있는 Hosted/remote 증거 | RES-0002에서 링크한다; claim 단위의 workflow 증거를 복사하지 않는다. |
| RES-0085 | 날짜가 있는 baseline 범위와 identity-recovery carrier | 역사적 증거로 보존한다; 날짜가 있는 baseline 해석은 RES-0002-m0020으로 route하며 이번 갱신에서 새로 평가하지 않는다. |
| RES-0096 | archive disposition consistency 평가 | infrastructure/provider 연구와 분리해 유지한다; lifecycle 증거가 관련 있을 때만 링크한다. |

이는 논리적 통합이며 삭제나 내용 병합이 아닙니다. package identity, 관찰
날짜, lifecycle, 복구 provenance는 그대로 유지됩니다. 이전 RES-0080/RES-0081
learning-roadmap 계열은 더 이상 활성 research package가 아닙니다.
RES-0081은 RES-0002를 현재 routing 후속으로 두고 superseded 이력으로
보존됩니다.

### External Research Refresh

2026-09-27의 외부 자료만 갱신한 결과는 [RES-0002](./0002-agentic-engineering-research-pack/README.md)에만 속합니다. member coverage matrix와 후속 internal-check index는 primary-source 사실, 조건부 권고, 보존된 역사 관찰을 구분합니다. 내부 구현, runtime, 계정과 보안 상태는 `Not assessed in this run`입니다. 문서 baseline은 `f30b168e2fbb0959e4a31749935568fd5b3942f1`이며, 이는 새 workspace 평가가 아닙니다. 새 Actions 연구는 RES-0002-m0004에 속하고, RES-0084는 별도 날짜 증거를 유지합니다.

### Historical workspace observations — not reassessed in this refresh

아래 route와 채택 label은 날짜가 있는 역사 기록이며 현재 승인이나 새 평가가 아닙니다. 2026-09-10 LLM Wiki 은퇴 기록도 보존되며, 이번 갱신으로 복원하지 않습니다.

#### Workspace Engineering Request Route

#### Re-review Baseline

날짜가 있는 workspace baseline 재검증은
[RES-0002](./0002-agentic-engineering-research-pack/README.md)의 `m0020`
구성원에 `main@71da6654e2fa3def174b238ad309c92fe46e9dae` 기준으로
2026-09-05에 관찰된 뒤 통합되어 있습니다. 통합 baseline
`main@a89c600c05c0b61f5cbd592e196ac3673f9eeb4b`와 평가된 baseline
`main@4c6d211129615eab372d720ebd209b6c27618c86`는 날짜가 있는 증거로 계속
보존되며 RES-0085는 자체 binding request, identity-recovery 증거와
함께 후자를 소유한 채 publication review를 진행합니다.

그 baseline의 local gate 결과는 checkout에 따라 달라집니다: 격리된
`main` 전용 clone에서는 전체 profile이 통과하고 merge되지 않은 branch에
닿을 수 있는 개발자 clone에서는 실패합니다. 결과를 인용할 때는 반드시
commit과 도달 가능한 ref 범위를 함께 밝힙니다.
[RES-0002](./0002-agentic-engineering-research-pack/README.md)의 `m0019`
구성원이 그 분석을 소유합니다.

주제 연구는 계속 RES-0002와 RES-0084가 소유합니다. 저장소 고유의 구현
사실은 공통 Agent 거버넌스 정책, provider adapter, Stage 03 계약, Stage 05
운영, 추적되는 runtime 파일, script, test, CI 정의에 남습니다.

#### Design Decisions

1. **Canonical research를 재사용합니다.** 같은 subject를 두 번째 research
   pack에 복사하는 대신 기존 owner를 확장하거나 수정합니다.
2. **증거 깊이를 구분합니다.** 외부 capability, 추적된 configuration, local
   실행, repository 강제, provider runtime 수용, remote control-plane
   증명을 구분합니다.
3. **하나의 provider-neutral control plane을 유지합니다.** 공통 Agent
   거버넌스가 공유 정책을 소유하고, `.agents/`는 작성된 governance, role,
   skill을 소유하며, `AGENTS.md`와 `CLAUDE.md`는 entrypoint이고, `.claude/`와
   `.codex/`는 작성된 provider adapter와 생성된/native 메커니즘을
   유지합니다.
4. **구현은 SDLC를 통해서만 route합니다.** research gap은 승인된
   Requirement, Architecture/ADR, Spec, Plan, Task, 검증 증거, 독립 검토를
   거쳐야만 저장소 변경이 됩니다.
5. **runtime 상태를 추론하지 않습니다.** 추적되는 Docker Compose, hook,
   model, CI configuration은 실제로 관찰된 수준까지만 채택 깊이를
   증명합니다.

#### Category Routing and Current Assessment

아래 표의 각 항목은 [RES-0002](./0002-agentic-engineering-research-pack/README.md)
구성원(괄호 안 `m####`)이 소유하며 자세한 내용은 해당 package의
README에서 찾습니다.

| Requested area | Research owner | Implementation evidence | Assessment |
| --- | --- | --- | --- |
| Harness engineering | Harness engineering (`m0008`) | Harness audit | 부분적 |
| Loop engineering | Loop engineering (`m0010`) | Loop audit | 부분적 |
| Workspace harness, loop, rules, and environment | Workspace baseline (`m0020`) | Workspace rules audit | 부분적 |
| Claude Code and Codex implementation | Provider comparison (`m0012`) | Provider audit | 부분적 |
| Shared Claude/Codex governance | Provider comparison (`m0012`) | [공통 Agent 거버넌스](../../../.agents/README.md)와 [provider registry](../../../.agents/governance/providers/registry.yaml) | Repository-enforced로 투영됨; cross-provider 수용은 여전히 point-in-time |
| System prompts and context loading | Agent instructions (`m0001`) | [Bootstrap policy](../../../.agents/governance/bootstrap.md), [AGENTS.md](../../../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md) | 구현됨 |
| Spec-driven development | Spec-driven SDLC (`m0018`) | [Stage 03](../../03.specs/README.md)와 SDLC audit | 등록된 형태에는 Repository-enforced; intended-use 수용은 여전히 owner-bound |
| PRD, SPEC, PLAN, TASK, and ADR | SDLC document roles (`m0016`) | [Stage 99 templates](../../99.templates/README.md) | 등록된 저장소 형태에는 구현됨 |
| SDLC purpose, governance, and lifecycle | Spec-driven SDLC (`m0018`) | [SDLC policy](../../../.agents/governance/sdlc.md)와 [workflows](../../../.agents/governance/workflows.md) | 구현됨 |
| Guide, Incident, Postmortem, Policy, Release, and Runbook | SDLC document roles (`m0016`) | [Operations](../../05.operations/README.md)와 SDLC audit | Guide/Policy/Runbook/Incident/Postmortem는 등록됨; Release는 profile이 아니라 composed evidence |
| Diátaxis and documentation architecture | Documentation architecture (`m0007`) | [Documentation protocol](../../../.agents/governance/documentation-protocol.md) | 부분적 |
| C4 Model and arc42 | Documentation architecture (`m0007`) | [Architecture stage](../../02.architecture/README.md) | 부분적 |
| ADR | SDLC document roles (`m0016`) | [Architecture decisions](../../02.architecture/decisions/README.md) | 구현됨 |
| LLM Wiki | LLM Wiki system (`m0009`) | 2026-09-10에 generator, 생성된 index와 함께 은퇴; 탐색은 이제 `llms.txt`와 각 surface README를 통함 | 은퇴됨 |
| Docker Compose and infrastructure | Docker Compose and infrastructure (`m0005`) | Compose readiness audit | 부분적; static 증거가 runtime 증거를 초과 |
| CI/CD | Automation pipeline (`m0004`) | Quality audit | 부분적; CD보다 CI가 강함 |
| GitHub Actions | [GitHub Actions platform](./0084-github-actions-platform/README.md) | [CI workflow](../../../.github/workflows/ci-quality.yml)와 [protection record](../../../.github/rulesets/main-protection.md) | Hosted aggregate job과 2026-09-05 remote check read-back 검증됨 |
| QA, formatting, linting, testing, and syntax | Quality, CI, and formatting (`m0014`) | Quality audit | 등록된 surface 전반에 구현됨 |
| Security | Security governance (`m0017`) | Security audit | 부분적 |
| Verification and Validation | Verification and validation (`m0019`) | 현재 Task 증거와 등록된 gate | 부분적; intended-use 수용은 여전히 owner-bound |
| AI agent catalog and agency-agents | AI agent catalogs (`m0003`) | Instruction/catalog/model audit | 부분적 |
| Task-aware model selection | Agent model selection (`m0002`) | [Provider registry](../../../.agents/governance/providers/registry.yaml) | 추적된 정책으로 구현됨; entitlement는 검증되지 않음 |
| Agent memory hierarchy | Memory hierarchy (`m0011`) | 현재 Task 증거; 공유 governance memory root는 아직 채택되지 않음 | 부분적 |
| Git pre-commit hooks | Quality, CI, and formatting (`m0014`) | [.pre-commit-config.yaml](../../../.pre-commit-config.yaml) | 구현됨 |
| Editor shortcuts and code actions | Workspace baseline (`m0020`) | 등록된 저장소 전역 editor action 계약 없음 | 미구현 |
| Rate limits, cost, tokens, and context | Provider model landscape (`m0013`) | Provider registry와 bounded context-loading 규칙 | 구성됨; entitlement 관찰은 point-in-time이고 비용은 측정되지 않음 |
| Test and CI agent hooks | Automation pipeline (`m0004`) | Claude/Codex hook과 CI 정의 | 부분적 |
| Claude/Codex context sharing | Provider comparison (`m0012`) | 공통 Agent 거버넌스 canonical source와 생성된 provider 투영 | 구조적으로 구현됨; live handoff는 여전히 부분적 |
| README purpose and role | Documentation architecture (`m0007`) | [Repository README](../../../README.md)와 등록된 README profile | 구현됨 |

#### Prioritized Design Gaps

1. 사용자 전역 설정을 읽거나 계정 entitlement를 가정하지 않고 native
   provider 수용 test를 추가합니다.
2. 강한 예산을 도입하기 전에 추적되는 provider-neutral 비용/rate-limit
   증거 계약을 정의합니다.
3. 내구성 있는 memory promotion, retention, expiry, privacy, deletion
   규칙을 완성합니다.
4. editor task와 code action은 명령, 권한, 문서화 hook 경계가 명시된
   뒤에만 등록합니다.
5. 배포 promotion, Release 증거, rollback 자동화, runtime 수용을 기존 CI
   quality plane에서 분리합니다.
6. 경쟁하는 문서 계층을 만드는 대신 Architecture stage를 통해 C4와
   arc42를 선택적으로 적용합니다.

깨끗한 `main` baseline은 2026-09-05에
`python3 scripts/validation/run-ci-gate.py --profile full`을
통과했습니다. 이는 local-execution과 repository-enforcement 증거이며
배포나 runtime 수용 증거가 아닙니다.

각 항목의 구현을 요청하면 별도로 승인된 활성 Spec이 필요합니다. 이
index는 routing과 설계만 기록하며, runtime, remote, provider, secret,
infrastructure 변경을 승인하지 않습니다.

## Authoring

package는 `research/####-<slug>/` 아래에만 만들고, 대응하는 Stage 99
템플릿을 사용합니다. 관찰 날짜, 인용, provenance, 활성 owner
Traceability를 보존합니다.

새 research identity를 발급하기 전에 활성 package와 audit을 먼저
검색합니다. question, 증거 모델, lifecycle이 이미 다뤄지고 있다면 기존
owner를 확장합니다.

## Related Documents

- [References index](../README.md)
- [Agentic engineering research](./0002-agentic-engineering-research-pack/README.md)
- [GitHub Actions platform mechanics](./0084-github-actions-platform/README.md)
- [Dated workspace-baseline evidence](./0085-workspace-engineering-main-baseline-assessment/README.md)
- [Archive disposition consistency assessment](./0096-archive-disposition-consistency/README.md)
- [공통 Agent 거버넌스](../../../.agents/README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
