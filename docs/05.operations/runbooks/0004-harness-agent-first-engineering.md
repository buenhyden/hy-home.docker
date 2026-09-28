---
title: "Harness / Agent-first Engineering Runbook"
version: "1.0.5"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---
# Harness / Agent-first Engineering Runbook

## Overview

이 런북은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약이 계속 유효한지 반복 검증하는 절차를 제공한다.

## When to Use

- Root instruction 파일이 변경될 때
- `.claude` 또는 `.codex` 파일이 변경될 때
- `.agents/**`가 변경될 때
- 새 stage doc이 추가될 때
- harness 또는 Agent-first audit이 요청될 때

## Procedure

### Checklist

- [ ] `git status --short --branch`를 확인한다.
- [ ] `graphify-out/GRAPH_REPORT.md`를 읽는다.
- [ ] `bash scripts/knowledge/report-graphify-health.sh`를 실행한다.
- [ ] 문서를 편집하기 전에 runtime policy 변경이 필요 없는지 확인한다.
- [ ] 새 stage doc이 template을 사용하고 parent README 파일이 갱신되었는지 확인한다.
- [ ] hook quoting/parsing 변경 후에는 hook payload simulation을 실행한다.
- [ ] 아래의 모든 verification command를 실행한다.

### Procedure

1. workspace 상태를 확인한다.

   ```bash
   git status --short --branch
   sed -n '1,120p' graphify-out/GRAPH_REPORT.md
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
   bash -n .claude/hooks/*.sh scripts/**/*.sh
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

   이 check들은 default/core Compose와 supported hardening tier check로 본다. `services_total=5`를 근거로 전체 workspace Docker coverage를 주장하지 않는다.

6. source-label scan을 실행한다.

   ```bash
   # doc-paths: illustrative
   ! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md .claude .codex .agents
   ```

7. 변경된 파일, command 결과, Graphify health 상태, `10-communication` 같은 out-of-scope infra profile 실패를 포함한 잔여 위험을 보고한다.

### Verification Steps

이 runbook은 JSON parsing, hook payload simulation, Graphify health reporting, repository validator, default/core Docker check, supported hardening tier check, source-label scan이 모두 예상대로 완료되면 성공이다. `report-graphify-health.sh`는 실패로 취급하지 않는 advisory evidence이다. `status=advisory`는 대조 검증이 필요하지만 repository gate를 실패시키지는 않는다.

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
- `10-communication` 실패는 해당 profile이 명시적으로 범위에 포함되지 않는 한 별도의 infra remediation 경로를 연다.

### Related Operational Documents

- [Operations Policy](../policies/0004-harness-agent-first-engineering.md)
- [Usage Guide](../guides/0004-harness-agent-first-engineering.md)
- Plan
- Task Evidence
- [Agent Governance Hub](../../../.agents/README.md)

## Evidence

- 이 runbook을 실행할 때마다 command 출력, timestamp, operator 또는 agent 조치를 기록한다.
- 실패한 check, 관찰된 증상, 최종 recovery 또는 escalation 상태를 관련 task 또는 incident evidence에 기록한다.

## Rollback or Recovery

- 이 runbook에 이미 문서화된 recovery/rollback 단계만 사용한다.
- 관찰된 실패가 문서화된 단계와 일치하지 않으면 변경을 중단하고 evidence를 보존한 뒤 `## Escalation`에 따라 escalation한다.

## Escalation

verification이 실패하거나, secret 노출 위험이 나타나거나, 파괴적 데이터 변경이 필요하거나, 관찰된 상태가 예상 절차 결과와 다를 때 작업을 중단하고 담당 operator에게 escalation한다. 수집한 evidence, 시도한 단계, 현재 rollback/recovery 상태를 포함한다.

## Traceability

- Declared parent: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Guide](../guides/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Policy](../policies/0004-harness-agent-first-engineering.md) (`POL-0004`)

## Related Documents

- [Operations index](../README.md)
- [Specification](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md)
- [Usage guide](../guides/0004-harness-agent-first-engineering.md)
- [Operations policy](../policies/0004-harness-agent-first-engineering.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Subagent Protocol](../../../.agents/governance/agentic.md)
