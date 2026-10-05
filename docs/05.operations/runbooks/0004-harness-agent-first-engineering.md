---
title: "Harness / Agent-first Engineering Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---
# Harness / Agent-first Engineering Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

이 런북은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약이 계속 유효한지 반복 검증하는 절차를 제공한다.

### When to Use

- Root instruction 파일이 변경될 때
- `.claude` 또는 `.codex` 파일이 변경될 때
- `.agents/**`가 변경될 때
- 새 stage doc이 추가될 때
- harness 또는 Agent-first audit이 요청될 때

## Procedure

### Procedure

### Checklist

- [ ] `git status --short --branch`를 확인한다.
- [ ] bootstrap/provider와 승인 범위를 읽고 report가 존재하는 경우에만 읽는다.
- [ ] `bash scripts/knowledge/report-graphify-health.sh`를 실행한다.
- [ ] 문서를 편집하기 전에 runtime policy 변경이 필요 없는지 확인한다.
- [ ] 새 stage doc이 template을 사용하고 parent README 파일이 갱신되었는지 확인한다.
- [ ] hook quoting/parsing 변경 후에는 hook payload simulation을 실행한다.
- [ ] 아래 적용 가능한 verification command의 입력·부작용·필요 도구를 먼저 확인한다. 공개/sanitized checkout이 없거나 private 접근·Docker 실행이 승인되지 않았으면 해당 검사를 BLOCKED/NOT_RUN으로 남긴다.

### Procedure

1. workspace 상태를 확인한다.

   ```bash
   git status --short --branch
   if [ -f graphify-out/GRAPH_REPORT.md ]; then sed -n '1,120p' graphify-out/GRAPH_REPORT.md; else echo 'NOT_RUN: Graphify report absent'; fi
   bash scripts/knowledge/report-graphify-health.sh
   ```

2. Graphify health를 해석한다.

   - `status=clean`: Graphify를 navigation aid로 사용할 수 있다.
   - `status=advisory`: Graphify는 계속 읽을 수 있지만, architecture와 codebase 주장은 tracked source 파일, `.agents/`, 그리고 active stage doc과 대조 검증해야 한다.
   - report는 count와 guidance만 출력해야 하며, source 파일 내용을 출력해서는 안 된다.

3. governance와 docs check를 실행한다.

   ```bash
   python3 -m json.tool .codex/hooks.json >/dev/null
   python3 -m json.tool .claude/settings.json >/dev/null
   while IFS= read -r -d '' file; do bash -n "$file" || exit; done < <(git ls-files -z '*.sh')
   python3 scripts/validation/run-ci-gate.py --profile changed
   python3 scripts/validation/check-document-links.py --mode traceability
   ```

4. hook payload simulation을 실행한다.

   ```bash
   printf '{"tool_input":{"file_path":"infra/10-communication/stalwart/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
   CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
   CLAUDE_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh SessionStart
   printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh PreToolUse
   printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/post-tool-validate.sh
   ```

   이 command들은 local script 동작과 JSON/system-message 출력을 검증한다. 외부 Claude/Codex platform의 event delivery를 증명하지는 않는다.

5. infrastructure와 baseline check를 실행한다.

   ```bash
   bash scripts/validation/validate-docker-compose.sh
   bash scripts/validation/check-template-security-baseline.sh
   bash scripts/validation/check-quickwin-baseline.sh
   bash scripts/hardening/check-all-hardening.sh
   ```

   Compose validator의 기본 선택은 모든 선언 profile과 HOME이며, 두 baseline
   script의 기본 선택은 `core`다. `HYHOME_COMPOSE_PROFILES` override와 hardening의
   실제 대상 범위를 각각 기록한다. selector별 합계는 중복 서비스가 포함될 수 있다.
   [RUN-0086](0086-dependency-version-management.md#static-configuration-validation)의
   입력·부작용 경계를 먼저 적용하며 config PASS를 live readiness로 기록하지 않는다.

6. source-label scan을 실행한다.

   ```bash
   # doc-paths: illustrative
   ! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md .claude .codex .agents
   ```

7. 변경 파일, command 결과, Graphify 유효성, 실제 선택 범위와 범위 밖 infra 실패를 현재 Task에 기록한다. 실패를 지우기 위해 범위를 넓히거나 통제를 낮추지 않는다.

### CI quality-gate version alignment

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

### Model-free Evaluation Maintenance

평가 변경에는 저장소 루트에서 합성 입력만 사용하는 다음 명령을 실행한다.

```bash
bash .agents/evaluations/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions
```

종료 코드와 fixture·regression 결과를 현재 Task에 기록한다. 이 명령은 모델을
호출하거나 실제 복구를 수행하지 않는다. 필요한 네 소스와 소비자만 유지하고
별도 deployment-skeleton·파생 패키지·개인 상태·이전 승인 복사본은 추가하지 않는다.

상위 changed/full 게이트와 infrastructure 단계는 먼저 실제 leaf의 부작용을
검토한다. Compose 검증은 환경·임시 secret 경로를 만들 수 있고 Conftest는 Docker
컨테이너를 실행한다. 승인된 비밀 없는 격리 사본과 필요한 도구·이미지를 확보하지
못하면 해당 검사는 BLOCKED/NOT_RUN으로 기록하고 가능한 정적 검사를 계속한다.
합성 fixture 성공으로 누락된 전체 게이트나 native 관측을 대체하지 않는다.

### Verification Steps

이 runbook은 JSON parsing, hook payload simulation, Graphify health reporting, repository validator, 실제 선택이 기록된 Compose/baseline/hardening check, source-label scan이 모두 예상대로 완료되면 성공이다. `report-graphify-health.sh`는 실패로 취급하지 않는 advisory evidence이다. `status=advisory`는 대조 검증이 필요하지만 repository gate를 실패시키지는 않는다.

### Observability and Evidence Sources

- validation script의 command 출력.
- `git diff --stat`.
- `scripts/knowledge/report-graphify-health.sh`의 상태와 contamination count.
- `scripts/validation/run-ci-gate.py`의 runtime agent/function catalog 섹션.
- hook payload simulation 출력.
- 새 구현 변경이 진행 중일 때의 현재 co-located Task.

### Safe Rollback or Recovery Procedure

- 문서 실수는 영향받은 stage doc 또는 README hunk만 되돌린다.
- runtime catalog drift는 canonical agent governance role, skill, provider registry에서 provider projection을 다시 생성한다.
- Compose validation 실패는 관련 없는 파일을 편집하기 전에 변경된 Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}` 파일을 먼저 점검한다.
- 영향받은 infra 실패가 승인된 범위 밖이면 별도 remediation으로 전달하며 실패/미실행 상태를 성공으로 바꾸지 않는다.

### Related Operational Documents

- [Operations Policy](../policies/0004-harness-agent-first-engineering.md)
- [Usage Guide](../guides/0004-harness-agent-first-engineering.md)
- 현재 승인된 Spec Package의 Plan과 Task evidence
- [Agent Governance Hub](../../../.agents/README.md)

## Verification

### Evidence

- 이 runbook을 실행할 때마다 command 출력, timestamp, operator 또는 agent 조치를 기록한다.
- 실패한 check, 관찰된 증상, 최종 recovery 또는 escalation 상태를 관련 task 또는 incident evidence에 기록한다.

## Rollback and Escalation

### Rollback or Recovery

- 이 runbook에 이미 문서화된 recovery/rollback 단계만 사용한다.
- 관찰된 실패가 문서화된 단계와 일치하지 않으면 변경을 중단하고 evidence를 보존한 뒤 `## Escalation`에 따라 escalation한다.

### Escalation

verification이 실패하거나, secret 노출 위험이 나타나거나, 파괴적 데이터 변경이 필요하거나, 관찰된 상태가 예상 절차 결과와 다를 때 작업을 중단하고 @buenhyden에게 escalation한다. 수집한 evidence, 시도한 단계, 현재 rollback/recovery 상태를 포함한다.

### Traceability

- 과거 구현 출처: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- 같은 주제: [Guide](../guides/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Policy](../policies/0004-harness-agent-first-engineering.md) (`POL-0004`)

## Related Documents

- [Operations index](../README.md)
- [Specification](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md)
- [Usage guide](../guides/0004-harness-agent-first-engineering.md)
- [Operations policy](../policies/0004-harness-agent-first-engineering.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Subagent Protocol](../../../.agents/governance/agentic.md)
