---
title: "Harness / Agent-first Engineering Usage Guide"
version: "1.0.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---

# Harness / Agent-first Engineering Usage Guide

## Overview

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Usage

1. 루트 진입 파일을 읽는다: `README.md`, `AGENTS.md`, `CLAUDE.md`.
2. 환경 및 문서 맵을 읽는다: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. `bash scripts/knowledge/report-graphify-health.sh`로 Graphify health를 확인한다. `status=advisory`로 보고되면 Graphify는 navigation 용도로만 사용하고, 주장은 tracked 파일 및 canonical 문서와 대조한다.
4. governance policy를 읽는다: `.agents/README.md`, `.agents/governance/agentic.md`, `.agents/governance/documentation-protocol.md`, `.agents/governance/stage-authoring-matrix.md`.
5. provider-native runtime 표면을 점검한다: `.claude/provider.md`, `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`; `.codex/agents/*.toml`, `.codex/hooks.json`; 그리고 `.agents/governance/providers/README.md`, `.agents/governance/providers/registry.yaml`, `.codex/provider.md`, `scripts/hooks/agent-event-hook.sh`. Codex는 canonical `.agents/skills/<skill_id>/SKILL.md` 패키지를 발견하고 role이 선택한 절차를 명시적으로 읽으며, Claude는 thin generated pointer를 사용한다. Invocation은 명시적이며 runtime authority를 부여하지 않는다.
6. runtime projection을 `.agents/roles/**`, `.agents/skills/**`, `.agents/governance/providers/registry.yaml`과 비교한다.
7. validator를 검토한다: `scripts/validation/run-ci-gate.py`, `scripts/validation/check-document-links.py --mode traceability`, `scripts/validation/validate-docker-compose.sh`.
8. `.claude/hooks/*.sh`, `.codex/hooks.json`, `scripts/hooks/post-tool-validate.sh`가 변경되면 hook payload를 시뮬레이션한다. 구문 검사만으로는 `tool_input` 파싱을 증명하지 못한다.
9. 새 stage 문서가 필요하면 `docs/99.templates/`에서 시작하고 같은 변경에서 parent README를 갱신한다.
10. 완료를 선언하기 전에 runbook에 나열된 validation 명령을 실행한다.

### CI quality-gate version alignment

hosted quality gate가 local 결과와 어긋나면, 진단을 억제하거나 무관한 Dockerfile을
변경하기 전에 tracked workflow가 선택한 executable을 먼저 식별한다.

1. `.github/workflows/ci-quality.yml`, `.github/workflow-contract.yml`,
   `.pre-commit-config.yaml`, 그리고 실패한 job log를 읽는다. event, revision,
   job, hook, image 또는 binary 참조, rule identifier를 기록한다. local
   명령은 자신이 사용한 executable만 증명한다.
2. pre-commit repository의 `rev`를 hook manifest와 비교한다. upstream
   `v2.14.0`의 Hadolint `hadolint-docker` hook은 `docker_image` hook이며
   그 entry는 태그 없는 `ghcr.io/hadolint/hadolint hadolint`이다. 따라서
   hook revision이 container image 버전을 선택하지 않는다. entry를
   repository revision과 같은 release로 고정하고 focused regression으로
   한쪽으로 치우친 변경을 거부한다. upstream
   [v2.14.0 hook manifest](https://raw.githubusercontent.com/hadolint/hadolint/v2.14.0/.pre-commit-hooks.yaml)
   가 이 동작의 authority이다.
3. release tag는 선택된 Hadolint 버전을 정렬하지만 image byte까지 고정하지는
   않는다. immutable digest는 별도로 검토된 maintenance path를 거칠 때만
   고려한다. 이 path는 짝지어진 revision, tag, digest, update owner를 어떻게
   최신 상태로 유지할지 명시한다.
4. focused regression과 workflow-contract check를 실행한 다음, 적용 가능한
   가장 작은 local gate를 실행한다. hosted 결과는 GitHub Actions가 변경된
   revision을 실행할 때까지 pending 상태로 남는다. local reproduction 성공은
   rerun이 아니다.
5. `validation-changed`와 `validation-full`을 분리해서 유지한다. 전자는
   필수 pull-request gate이고, 후자는 main push 또는 manual dispatch에서
   실행되며 추가 권한으로 SARIF를 업로드한다. 공유된 setup은 중복의 증거가
   아니다. workflow/event/ref concurrency key는 push와 manual 실행을 분리한
   채 각 event/ref 그룹 안의 오래된 실행을 취소한다. 이 방식은
   [GitHub의 concurrency 안내](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency)를
   따른다.
6. trigger, permission, gate node, consumer가 사용되지 않음을 inventory가
   증명할 때까지는 단순화를 제안으로만 취급한다. commit 없이 title만 편집하면
   이전의 green 실행이 그대로 남을 수 있으므로, title-dependent validation에는
   `edited` event 평가가 필요하다. 이 가이드는 event, required check,
   permission, remote ruleset을 변경하지 않는다.

CI Quality Gates에 대해 승인된 2026-09-20 follow-up은 `PR_TITLE`이 gate
input이므로 pull-request trigger에 `edited`를 추가한다. 또 manual 진단이
main-push validation을 취소하지 않도록 concurrency key를 workflow, ref, event로
지정하고 비용이 큰 leaf보다 먼저 기존 pre-commit leaf를 실행한다. 이
follow-up은 gate set, job identity, `SKIP` ownership, changed/full 분리를 그대로 유지한다.
hosted verification은 여전히 필수이다.

2026-09-20 PR #169 incident와 그에 따른 Hadolint 정렬은
[SPEC-0180 Task 0006](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0006-ci-quality-version-alignment.md)에
기록되어 있다. 이 문서는 실패한 hosted revision을 local 증거, 향후
GitHub Actions 통합 제안과 구분한다.

### Audience and Prerequisites

#### Usage Type

How-to / audit guide.

#### Target Audience

- AI Agents
- Documentation Writers
- Infra Operators
- Repository Maintainers

#### Purpose

반복 가능한 방식으로 workspace purpose, rules, runtime surface, governance contracts, validation gates를 조사하고, 필요한 경우 stage 문서와 README를 템플릿에 맞춰 갱신한다.

#### Prerequisites

- `AGENTS.md`를 읽는다.
- architecture 또는 codebase 관련 답변 전에 `graphify-out/GRAPH_REPORT.md`를 읽는다.
- `graphify-out/`이 존재하면 `bash scripts/knowledge/report-graphify-health.sh`를 실행한다.
- `.agents/`에서 활성 role, skill, provider, policy route를 확인한다.
- secret이나 credential 파일을 검사하지 않는다.

## Troubleshooting

- `.codex/agents/*.toml` 또는 `.claude/agents/*.md`를 canonical agent governance catalog에 대한 provider-native adapter가 아니라 canonical role catalog로 취급하는 것.
- authored `.agents` source를 오래된 generated 파일로 취급하거나, canonical body를 native skill adapter로 복사하거나, static discovery 설정으로부터 live picker/invocation 승인을 추론하는 것.
- governance hub 대신 root shim을 편집하는 것.
- 오염된 Graphify output을 authoritative architecture 증거로 취급하는 것.
- `status=advisory` Graphify health를 실패나 architecture authority로 취급하는 것. advisory health는 격하된 navigation context일 뿐이다.
- default/core profile과 지원되는 hardening tier만 확인했으면서 전체 workspace Docker validation을 주장하는 것.
- catalog parity check를 모든 agent/skill content에 대한 semantic parity로 취급하는 것.
- 별도의 infra scope 없이 `10-communication` Compose remediation을 Harness / Agent-first pass에 끌어들이는 것.
- hook quoting, event dispatch, parsing 변경 후 hook event 및 payload 시뮬레이션을 건너뛰는 것.
- parent README를 갱신하지 않고 stage 문서를 추가하는 것.
- `graphify` CLI를 사용할 수 없는데 graph refresh를 주장하는 것.
- repository 안내에도 불구하고 `pre-commit`을 수동으로 실행하는 것.

## Common Checks

- `Routine Usage` 단계와 연결된 validator가 해결되지 않은 실패 없이 완료된다.

## Runbook Handoff

반복 검증, evidence capture, rollback 또는 escalation 절차는
[Harness / Agent-first Engineering Runbook](../runbooks/0004-harness-agent-first-engineering.md)을 따른다.

## Traceability

- Declared parent: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Policy](../policies/0004-harness-agent-first-engineering.md) (`POL-0004`), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) (`RUN-0004`)

## Related Documents

- [Operations index](../README.md)
- [Operations policy](../policies/0004-harness-agent-first-engineering.md)
- [Operations runbook](../runbooks/0004-harness-agent-first-engineering.md)
