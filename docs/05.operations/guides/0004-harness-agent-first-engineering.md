---
title: "Harness / Agent-first Engineering Usage Guide"
version: "1.3.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---

# Harness / Agent-first Engineering Usage Guide

## Overview

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Audience and Goal

대상 독자는 AI Agent, 문서 작성자, 인프라 운영자, 저장소 유지보수자다.

목표는 workspace purpose, rules, runtime surface, governance contract, validation gate를 반복 가능한 방식으로 조사하는 것이다. 필요하면 stage 문서와 README를 템플릿에 맞춰 갱신한다. 이 문서는 하네스 구조와 감사 경계를 설명하는 가이드다.

## Usage

시작하기 전에 다음을 확인한다.

- `AGENTS.md`를 읽는다.
- architecture/codebase 조사 전에 report 존재와 유효성을 확인하고, 존재하면 `graphify-out/GRAPH_REPORT.md`를 읽는다.
- `graphify-out/`이 존재하면 `bash scripts/knowledge/report-graphify-health.sh`를 실행한다.
- `.agents/`에서 활성 role, skill, provider, policy route를 확인한다.
- secret이나 credential 파일을 검사하지 않는다.

[bootstrap](../../../.agents/governance/bootstrap.md)와 해당 provider adapter가
읽기 순서를 소유한다. root README와 `docs/`, `infra/`, `scripts/` README는
탐색 경로이며 `.agents/`의 governance·role·skill·Provider Registry가 현재
권위를 소유한다. `.claude`와 `.codex`는 native adapter다. Codex는 canonical
skill을 명시적으로 읽고 Claude는 thin generated pointer를 사용한다.
정적 discovery와 projection parity는 live picker·invocation·hook delivery나
runtime 승인을 증명하지 않는다. authoring은 Stage99 template과 parent README를
함께 다루며 실행 증거는 현재 Task에 남긴다.

Graphify는 source 대조를 돕는 navigation 자료다. report가 없거나 health가
advisory이면 그 사실을 기록하고 tracked source를 사용한다. health가 clean이어도
HEAD가 다르면 bootstrap의 stale-snapshot 경계가 적용된다. 실행 순서와 hook
payload 검증은 [Runbook](../runbooks/0004-harness-agent-first-engineering.md#procedure)이
소유하며, syntax 성공만으로 payload parsing이나 native 전달을 증명하지 않는다.

### CI quality-gate version alignment

hosted quality gate가 local 결과와 어긋나면, 진단을 억제하거나 무관한 Dockerfile을
변경하기 전에 tracked workflow가 선택한 executable을 먼저 식별한다.

[CI workflow](../../../.github/workflows/ci-quality.yml),
[workflow contract](../../../.github/workflow-contract.yml)와
[pre-commit 설정](../../../.pre-commit-config.yaml)이 실행 도구·event·gate를 소유한다.
Hook repository revision과 container entry tag는 다른 선택이므로 둘을 대조한다.
현재 Hadolint는 짝지어진 revision과 image tag를 사용하지만 image byte까지
고정한 것은 아니다. digest 도입에는 별도 검토된 update/rollback 경계가 필요하다.

현재 PR 후보의 aggregate QA는 원격 public `changed` profile이 소유한다.
로컬은 작성 중 한정 회귀와 읽기 전용 진단을 수행하며 동일 후보의 aggregate를
반복하지 않는다. main security는 병합된 SHA의 별도 관측이며, 릴리스는 승인된
main revision에 대한 단일 수동 SemVer 생산자가 소유한다. 정확한 단계·선택·권한은
[quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix)와
[release runbook](../runbooks/0009-release-management.md)이 소유한다.
소스 설정을 실제 hosted 성공이나 릴리스 게시로 기록하지 않는다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, GDE-0004 CI quality-gate version alignment.
> CI Quality Gates에 대해 승인된 2026-09-20 follow-up은 `PR_TITLE`이 gate
> input이므로 pull-request trigger에 `edited`를 추가한다. 또 manual 진단이
> main-push validation을 취소하지 않도록 concurrency key를 workflow, ref, event로
> 지정하고 비용이 큰 leaf보다 먼저 기존 pre-commit leaf를 실행한다. 이
> follow-up은 당시 gate set, job identity, `SKIP` ownership, changed/full 분리를 유지했다.
> hosted verification은 여전히 필수이다.
>
> 2026-09-20 PR #169 incident와 그에 따른 Hadolint 정렬은
> [SPEC-0180 Task 0006](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0006-ci-quality-version-alignment.md)에
> 기록되어 있다. 이 문서는 실패한 hosted revision을 local 증거, 향후
> GitHub Actions 통합 제안과 구분한다.

### Evaluation Maintenance

자동 답변 점수 evaluator와 과거 사건을 재증명하는 전용 QA는 폐기됐다.
현재 QA 적용 범위는 quality policy가 소유하며 `.agents/evaluations/README.md`는
동일 작업의 baseline/Skill 출력·채점·집계 증거와 작성·보존 경계를 안내한다.
새 평가 주기는 기존 원문을 보존하고 별도 Task·권한·예산·profile을 확정한다.
대표 점수는 모든 Skill의 PASS나 native 실행 증거가 아니다. provider/model의 수동 비교에는 현재 skill과
날짜가 있는 공식 근거를 사용하며 native 실행이나 모델 품질을 추정하지 않는다.
구체적인 live 관측과 파생 배포는 별도 Task·승인 범위로 둔다.

### Common Checks

- 연결된 Runbook에서 적용 가능한 검증의 실제 결과와 범위, 실패·차단·미실행을 확인한다.

### Runbook Handoff

반복 검증, evidence capture, rollback 또는 escalation 절차는
[Harness / Agent-first Engineering Runbook](../runbooks/0004-harness-agent-first-engineering.md)을 따른다.

### Traceability

- 과거 구현 출처: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- 같은 주제: [Policy](../policies/0004-harness-agent-first-engineering.md) (`POL-0004`), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) (`RUN-0004`)

## Troubleshooting

다음 실수를 피한다.

- `.codex/agents/*.toml` 또는 `.claude/agents/*.md`를 canonical agent governance catalog에 대한 provider-native adapter가 아니라 canonical role catalog로 취급하는 것.
- authored `.agents` source를 오래된 generated 파일로 취급하거나, canonical body를 native skill adapter로 복사하거나, static discovery 설정으로부터 live picker/invocation 승인을 추론하는 것.
- governance hub 대신 root shim을 편집하는 것.
- 오염된 Graphify output을 authoritative architecture 증거로 취급하는 것.
- `status=advisory` Graphify health를 실패나 architecture authority로 취급하는 것. advisory health는 격하된 navigation context일 뿐이다.
- 서로 다른 validator의 선택 범위를 합쳐 전체 서비스 검증으로 주장하는 것.
- catalog parity check를 모든 agent/skill content에 대한 semantic parity로 취급하는 것.
- 승인 범위 밖 Compose remediation을 하네스 점검에 끌어들이는 것. 현재 영향받은 선택과 gate 실패는 별도 기록한다.
- hook quoting, event dispatch, parsing 변경 후 hook event 및 payload 시뮬레이션을 건너뛰는 것.
- parent README를 갱신하지 않고 stage 문서를 추가하는 것.
- `graphify` CLI를 사용할 수 없는데 graph refresh를 주장하는 것.
- repository 안내에도 불구하고 `pre-commit`을 수동으로 실행하는 것.

## Related Documents

- [Operations index](../README.md)
- [Operations policy](../policies/0004-harness-agent-first-engineering.md)
- [Operations runbook](../runbooks/0004-harness-agent-first-engineering.md)
