---
title: "Harness / Agent-first Engineering Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
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
- [ ] Graphify를 탐색에 사용할 때만 health를 advisory로 확인한다.
- [ ] 문서를 편집하기 전에 runtime policy 변경이 필요 없는지 확인한다.
- [ ] 새 stage doc이 template을 사용하고 parent README 파일이 갱신되었는지 확인한다.
- [ ] hook quoting/parsing 변경 후에는 hook payload simulation을 실행한다.
- [ ] 아래 적용 가능한 verification command의 입력·부작용·필요 도구를 먼저 확인한다. 공개/sanitized checkout이 없거나 private 접근·Docker 실행이 승인되지 않았으면 해당 검사를 BLOCKED/NOT_RUN으로 남긴다.

### Procedure

1. workspace 상태를 확인한다. Graphify report와 health는 해당 탐색을 사용할 때만 읽는 advisory이며 필수 QA가 아니다.

   ```bash
   git status --short --branch
   if [ -f graphify-out/GRAPH_REPORT.md ]; then sed -n '1,120p' graphify-out/GRAPH_REPORT.md; else echo 'NOT_RUN: Graphify report absent'; fi
   bash scripts/knowledge/report-graphify-health.sh
   ```

2. Graphify health를 해석한다.

   - `status=clean`: Graphify를 navigation aid로 사용할 수 있다.
   - `status=advisory`: Graphify는 계속 읽을 수 있지만, architecture와 codebase 주장은 tracked source 파일, `.agents/`, 그리고 active stage doc과 대조 검증해야 한다.
   - report는 count와 guidance만 출력해야 하며, source 파일 내용을 출력해서는 안 된다.

3. 실제 변경의 선택과 prerequisites를 조회한다. 이 조회는 실행 결과가 아니다.

   ```bash
   python3 scripts/validation/run-ci-gate.py --profile changed --explain
   ```

   변경된 JSON/shell의 등록된 read-only style과 문서 content 검사는 원격
   후보가 소유한다. 모든 shell을 따로 순회하거나 같은 링크 검사를 반복하지 않는다.

4. hook quoting/parsing 자체를 변경했고 해당 수동 관측이 Task에 선택·승인된 경우에만 아래 simulation을 수행한다. 일반 문서 변경에는 적용하지 않는다.

   ```bash
   printf '{"tool_input":{"file_path":"infra/10-communication/stalwart/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
   CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
   CLAUDE_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh SessionStart
   printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh PreToolUse
   printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/post-tool-validate.sh
   ```

   이 command들은 local script 동작과 JSON/system-message 출력을 검증한다. 외부 Claude/Codex platform의 event delivery를 증명하지는 않는다.

5. 실제 infra 변경으로 선택된 검사만 수행한다. 아래는 각 owner의 진단 명령 예시이며, 후보 gate가 이미 실행한 같은 입력의 leaf를 다시 실행하는 절차가 아니다.

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

6. 현행 canonical owner와 retired-authority 재도입 방지는 등록된 content
   validator의 결과로 확인한다. 과거 cutover의 고정 문자열 목록을 별도
   반복 QA로 실행하지 않는다.

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
4. 변경된 동작의 focused regression과 등록된 read-only style 검사를 수행한다.
   원격 PR 후보가 selected changed aggregate를 한 번 실행한다. 로컬 결과를
   hosted 결과로 표시하거나 push 전·merge 후 같은 QA를 반복하지 않는다.
5. `changed --explain`으로 선택과 도구·예산을 확인한다. `full`은 별도 승인된
   전체 감사용이다. main push의 보안/SARIF는 merged revision의 다른 관측이다.
   PR concurrency는 revision 변경만 대상으로 하며 title edited가 후보 증거를
   대체하거나 취소하지 않는다.
6. caller·등록·소유자 조사 후 필요 없어진 QA만 폐기한다. 현재 DAG와 정책에
   계속되는 보장을 이전하고 전용 helper·fixture·test를 제거한다. 현재 관측과
   과거 완료 사건의 고정 SHA·수량은 같은 보장이 아니다.

### Evaluation and QA Ownership

agent 답변 점수와 완료된 Spec/Task 사건을 재증명하는 fixture는 정기 workspace
QA가 아니다. 현재 [품질 정책](../../../.agents/governance/quality-standards.md)이
허용하는 문서 형태·관계·상태·보존 및 Docker/Compose 보장만 선택한다. provider
공식 사실·native envelope 검토와 live 실행 관측은 각각의 owner에 남기며,
합성 점수나 소스 설정으로 실제 provider entitlement/runtime을 수용하지 않는다.
`.agents/evaluations/README.md`는 별도 평가 주기의 동일 작업 baseline/Skill 출력과
채점·집계의 소유 관계를 안내한다. 실제 원문과 시행·채점자·기준·보정 상태를
보존하며 대표 결과를 전체 구성원 PASS로 확대하지 않는다.

선택된 infrastructure leaf의 부작용은 먼저 확인한다. Compose render는 임시
입력을 만들 수 있고 Conftest는 격리 Docker 컨테이너를 실행한다. 필요한 도구와
입력이 없으면 해당 lane을 BLOCKED/NOT_RUN으로 남기고 독립적인 안전 작업을
계속한다. static PASS를 HOME capacity·복구·배포 성공으로 확대하지 않는다.

### Verification Steps

`--explain`은 실행하지 않는 계획 조회다. 후보 aggregate QA는
[quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix)의
원격 PR 경로가 소유하며 조회 결과를 검증 PASS로 기록하지 않는다.

이 runbook의 수용은 실제 변경에 선택된 현재 보장 검사와 독립 리뷰의 결과로 판단한다. 무관한 hook simulation·Graphify 보고·전체 QA를 모든 변경에 요구하지 않는다. `report-graphify-health.sh`는 실패로 취급하지 않는 advisory evidence이다. `status=advisory`는 대조 검증이 필요하지만 repository gate를 실패시키지는 않는다.

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
