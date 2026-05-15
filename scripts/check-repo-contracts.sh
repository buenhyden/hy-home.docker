#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

failures=0

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

section() {
  echo
  echo "==> $1"
}

section "Docs top-level structure"
allowed_docs=(
  "00.agent-governance"
  "01.requirements"
  "02.architecture"
  "03.specs"
  "04.execution"
  "05.operations"
  "90.references"
  "99.templates"
)

mapfile -t actual_docs < <(find docs -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
expected_docs="$(printf '%s\n' "${allowed_docs[@]}" | sort)"
actual_docs_text="$(printf '%s\n' "${actual_docs[@]}")"

if [[ "$actual_docs_text" != "$expected_docs" ]]; then
  fail "docs top-level folders do not match the allowed taxonomy"
  echo "Expected:" >&2
  printf '  %s\n' "${allowed_docs[@]}" >&2
  echo "Actual:" >&2
  printf '  %s\n' "${actual_docs[@]}" >&2
fi

section "Required README files"
for d in "${allowed_docs[@]}"; do
  readme="docs/$d/README.md"
  if [[ ! -f "$readme" ]]; then
    fail "missing required README: $readme"
    continue
  fi
  if ! grep -Eiq '(^## (Purpose|Overview|Context and Objective|목적)|^## 1\. Context and Objective)' "$readme"; then
    fail "$readme missing purpose/overview section"
  fi
  if ! grep -Eiq '(^## (Scope|포함할 내용|Requirements and Constraints|Directory Structure|Structure|템플릿-폴더 매핑)|^## 2\. Requirements and Constraints|^## 3\. Directory Structure)' "$readme"; then
    fail "$readme missing allowed content/structure section"
  fi
  if ! grep -Eiq '(^## (Related Documents|Related References|관련 문서)|Related Documents|Related References)' "$readme"; then
    fail "$readme missing related folders/documents section"
  fi
  if ! grep -Eiq '(Example|Examples|예시|Structure|Directory Structure|권장 하위 구조|템플릿-폴더 매핑)' "$readme"; then
    fail "$readme missing examples or structure guidance"
  fi
done

section "Template inventory"
required_templates=(
  "adr.template.md"
  "agent-design.template.md"
  "api-spec.template.md"
  "ard.template.md"
  "data-model.template.md"
  "incident.template.md"
  "memory.template.md"
  "openapi.template.yaml"
  "operation.template.md"
  "plan.template.md"
  "postmortem.template.md"
  "progress.template.md"
  "prd.template.md"
  "readme.template.md"
  "reference.template.md"
  "schema.template.graphql"
  "service.template.proto"
  "spec.template.md"
  "task.template.md"
  "tests.template.md"
)

for template in "${required_templates[@]}"; do
  [[ -f "docs/99.templates/$template" ]] || fail "missing template: docs/99.templates/$template"
done

mapfile -t misplaced_templates < <(
  find docs -path docs/99.templates -prune -o -type f \
    \( -name '*.template.md' -o -name '*.template.yaml' -o -name '*.template.yml' -o -name '*.template.graphql' -o -name '*.template.proto' \) \
    -print
)
if [[ "${#misplaced_templates[@]}" -gt 0 ]]; then
  fail "templates found outside docs/99.templates"
  printf '  %s\n' "${misplaced_templates[@]}" >&2
fi

section "Banned stale references"
if rg -n 'docs/11|11\.postmortems|\.agent/|docs/(01\.prd|02\.ard|03\.adr|04\.specs|05\.plans|06\.tasks|07\.operations|07\.guides|08\.operations|09\.runbooks|10\.incidents)|(^|[^[:alnum:]_/-])(01\.prd|02\.ard|03\.adr|04\.specs|05\.plans|06\.tasks|07\.operations|07\.guides|08\.operations|09\.runbooks|10\.incidents)([^[:alnum:]_/-]|$)|guide\.template\.md|runbook\.template\.md|harness catalog|Runtime harness catalog' README.md AGENTS.md CLAUDE.md GEMINI.md docs infra scripts .github .claude .codex \
  --glob '!graphify-out/**' \
  --glob '!docs/README.md' \
  --glob '!docs/00.agent-governance/memory/**' \
  --glob '!scripts/check-repo-contracts.sh' >/tmp/check-repo-contracts-banned.txt; then
  fail "stale docs taxonomy, removed operations-stage, guide/runbook template, harness-catalog, or .agent references remain"
  cat /tmp/check-repo-contracts-banned.txt >&2
fi
rm -f /tmp/check-repo-contracts-banned.txt

section "Active docs taxonomy shorthand"
if rg -n 'docs/(0[1-9]~0?9|01~09|01~10|01-03|01-09)|docs/01[[:space:]]*[–-][[:space:]]*docs/10|docs/01.?to.?docs/10|Stage (06|07|10)|docs/07([^[:alnum:]_.-]|$)|docs/08([^[:alnum:]_.-]|$)|docs/09([^[:alnum:]_.-]|$)|05/08/09|07/08/09' README.md AGENTS.md CLAUDE.md GEMINI.md docs infra scripts .github .claude .codex \
  --glob '!graphify-out/**' \
  --glob '!docs/README.md' \
  --glob '!docs/00.agent-governance/memory/**' \
  --glob '!scripts/check-repo-contracts.sh' >/tmp/check-repo-contracts-taxonomy-shorthand.txt; then
  fail "active docs taxonomy shorthand or legacy stage shorthand remains"
  cat /tmp/check-repo-contracts-taxonomy-shorthand.txt >&2
fi
rm -f /tmp/check-repo-contracts-taxonomy-shorthand.txt

section "Operations target comments"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import json
import re
import sys

failures: list[str] = []
allowed_prefixes = (
    "docs/05.operations/guides/",
    "docs/05.operations/policies/",
    "docs/05.operations/runbooks/",
    "docs/05.operations/incidents/",
    "docs/05.operations/{guides,policies,runbooks}/",
)
pattern = re.compile(r"<!--\s*Target:\s*(docs/05\.operations/[^ >]+)\s*-->")

for path in sorted(pathlib.Path("docs").rglob("*.md")):
    if "graphify-out" in path.parts:
        continue
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = pattern.search(line)
        if not match:
            continue
        target = match.group(1)
        if not target.startswith(allowed_prefixes):
            failures.append(f"{path}:{line_no}: operations target must use guides/policies/runbooks/incidents: {target}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "GitHub Actions YAML and duplicate workflow steps"
if ! python3 - <<'PY'
from __future__ import annotations

import collections
import pathlib
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for GitHub Actions YAML parsing: {exc}", file=sys.stderr)
    sys.exit(1)

failures = 0
workflow_files = sorted(
    list(pathlib.Path(".github/workflows").glob("*.yml"))
    + list(pathlib.Path(".github/workflows").glob("*.yaml"))
)
yaml_files = sorted(
    list(pathlib.Path(".github").rglob("*.yml"))
    + list(pathlib.Path(".github").rglob("*.yaml"))
)

for path in yaml_files:
    try:
        yaml.safe_load(path.read_text())
    except Exception as exc:
        print(f"FAIL: YAML parse failed: {path}: {exc}", file=sys.stderr)
        failures += 1

for path in workflow_files:
    text = path.read_text()
    step_names = re.findall(r"(?m)^\s*-\s+name:\s*(.+)$", text)
    duplicate_steps = [(name, count) for name, count in collections.Counter(step_names).items() if count > 1]
    if duplicate_steps:
        print(f"FAIL: duplicate workflow step names in {path}: {duplicate_steps}", file=sys.stderr)
        failures += 1

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not re.match(r"^-\s+", stripped):
            continue
        if re.match(r"^-\s+\*[A-Za-z0-9_-]+\s*$", stripped):
            continue

        indent = len(line) - len(stripped)
        block = [line]
        for next_line in lines[index + 1 :]:
            next_stripped = next_line.lstrip()
            next_indent = len(next_line) - len(next_stripped)
            if next_stripped and next_indent <= indent and re.match(r"^-\s+", next_stripped):
                break
            if next_stripped and next_indent < indent:
                break
            block.append(next_line)

        block_text = "\n".join(block)
        has_uses = bool(
            re.search(r"(?m)^\s*uses:\s*", block_text)
            or re.search(r"(?m)^\s*-\s+(?:&[A-Za-z0-9_-]+\s+)?uses:\s*", block_text)
        )
        has_name = bool(
            re.search(r"(?m)^\s*name:\s*\S", block_text)
            or re.search(r"(?m)^\s*-\s+(?:&[A-Za-z0-9_-]+\s+)?name:\s*\S", block_text)
        )
        if has_uses and not has_name:
            print(f"FAIL: unnamed action step in {path}:{index + 1}", file=sys.stderr)
            failures += 1

    in_jobs = False
    job_ids: list[str] = []
    for line in text.splitlines():
        if re.match(r"^jobs:\s*$", line):
            in_jobs = True
            continue
        if in_jobs and re.match(r"^[A-Za-z0-9_-]+:", line):
            in_jobs = False
        if in_jobs:
            match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
            if match:
                job_ids.append(match.group(1))
    duplicate_jobs = [(name, count) for name, count in collections.Counter(job_ids).items() if count > 1]
    if duplicate_jobs:
        print(f"FAIL: duplicate workflow job ids in {path}: {duplicate_jobs}", file=sys.stderr)
        failures += 1

if failures:
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "GitHub workflow security contracts"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for GitHub workflow contract checks: {exc}", file=sys.stderr)
    sys.exit(1)

failures: list[str] = []
workflow_files = sorted(
    list(pathlib.Path(".github/workflows").glob("*.yml"))
    + list(pathlib.Path(".github/workflows").glob("*.yaml"))
)
sha_re = re.compile(r"^[0-9a-f]{40}$")

for path in workflow_files:
    text = path.read_text()
    data = yaml.safe_load(text) or {}
    jobs = data.get("jobs") or {}
    top_permissions = data.get("permissions")

    if top_permissions is None:
        failures.append(f"{path}: workflow is missing top-level permissions")
    if "pull_request_target:" in text:
        failures.append(f"{path}: pull_request_target is not allowed")
    if re.search(r"(?m)^\s*contents:\s*write\s*(#.*)?$", text):
        failures.append(f"{path}: contents: write is not allowed")
    if "git push origin main" in text:
        failures.append(f"{path}: direct push to main is not allowed")

    for line_no, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*uses:\s*([^#\s]+)", line)
        if not match:
            continue
        action = match.group(1).strip("'\"")
        if action.startswith("./"):
            continue
        if "@" not in action:
            failures.append(f"{path}:{line_no}: action reference is missing a pinned ref: {action}")
            continue
        ref = action.rsplit("@", 1)[1]
        if not sha_re.fullmatch(ref):
            failures.append(f"{path}:{line_no}: action reference must use a full commit SHA: {action}")

    if top_permissions is None:
        for job_id, job in jobs.items():
            if isinstance(job, dict) and "permissions" not in job:
                failures.append(f"{path}: job {job_id!r} is missing explicit permissions")

ci_quality = pathlib.Path(".github/workflows/ci-quality.yml")
required_jobs = {
    "docs-traceability",
    "repo-contracts",
    "git-flow-contract",
    "compose-validation",
    "compose-all-profiles-validation",
    "infrastructure-hardening",
    "template-security-baseline",
    "quickwin-baseline",
    "pre-commit",
    "zizmor",
}
ci_jobs: set[str] = set()
if ci_quality.is_file():
    data = yaml.safe_load(ci_quality.read_text()) or {}
    ci_jobs = set((data.get("jobs") or {}).keys())
    missing_jobs = sorted(required_jobs - ci_jobs)
    for job_id in missing_jobs:
        failures.append(f"{ci_quality}: missing required QA/CI job: {job_id}")
    unexpected_jobs = sorted(ci_jobs - required_jobs)
    for job_id in unexpected_jobs:
        failures.append(f"{ci_quality}: unexpected QA/CI job outside the ruleset contract: {job_id}")
else:
    failures.append("missing required workflow: .github/workflows/ci-quality.yml")

ruleset = pathlib.Path(".github/rulesets/main-protection.md")
if ruleset.is_file():
    text = ruleset.read_text()
    for literal in [
        "local GitHub settings proposal only",
        "does not apply remote repository settings by",
        "explicit owner approval",
        "not evidence that branch protection",
    ]:
        if literal not in text:
            failures.append(f"{ruleset}: missing remote enforcement boundary literal: {literal}")

    match = re.search(r"(?ms)^## Required Status Checks\s*(.*?)(?:\n## |\Z)", text)
    if not match:
        failures.append(f"{ruleset}: missing Required Status Checks section")
    else:
        listed_checks = set(re.findall(r"(?m)^-\s+`([^`]+)`\s*$", match.group(1)))
        expected_checks = ci_jobs or required_jobs
        missing_checks = sorted(expected_checks - listed_checks)
        extra_checks = sorted(listed_checks - expected_checks)
        for check in missing_checks:
            failures.append(f"{ruleset}: missing required status check from CI Quality Gates: {check}")
        for check in extra_checks:
            failures.append(f"{ruleset}: status check is not a CI Quality Gates job: {check}")
else:
    failures.append("missing local branch protection proposal: .github/rulesets/main-protection.md")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "GitHub governance surface"
if [[ -f ".github/copilot-instructions.md" || -d ".github/instructions" ]]; then
  fail "GitHub-native instruction files are not adopted in this repository"
fi

if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

codeowners = pathlib.Path(".github/CODEOWNERS")
if not codeowners.is_file():
    print("FAIL: missing .github/CODEOWNERS", file=sys.stderr)
    sys.exit(1)

required_patterns = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "RTK.md",
    ".github/**",
    ".claude/**",
    ".codex/**",
    "infra/**",
    "scripts/**",
    "secrets/**",
    "docs/00.agent-governance/**",
}

patterns = set()
for line in codeowners.read_text().splitlines():
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue
    patterns.add(stripped.split()[0])

missing = sorted(required_patterns - patterns)
if missing:
    for pattern in missing:
        print(f"FAIL: CODEOWNERS missing required governance pattern: {pattern}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Runtime agent/function catalog"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

failures: list[str] = []

def read(path: pathlib.Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""

def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text, re.M)
    return match.group(1).strip() if match else None

runtime_agents = sorted(p.stem for p in pathlib.Path(".claude/agents").glob("*.md"))
governance_agents = sorted(p.stem for p in pathlib.Path("docs/00.agent-governance/agents/agents").glob("*.md"))
if runtime_agents != governance_agents:
    failures.append(f"runtime agent catalog mismatch: .claude={runtime_agents} governance={governance_agents}")

runtime_functions = sorted(p.parent.name for p in pathlib.Path(".claude/skills").glob("*/skill.md"))
governance_functions = sorted(p.stem for p in pathlib.Path("docs/00.agent-governance/agents/functions").glob("*.md"))
if runtime_functions != governance_functions:
    failures.append(f"runtime function catalog mismatch: .claude={runtime_functions} governance={governance_functions}")

protocol = pathlib.Path("docs/00.agent-governance/subagent-protocol.md").read_text()
for agent in runtime_agents:
    agent_path = pathlib.Path(f".claude/agents/{agent}.md")
    text = read(agent_path)
    protocol_path = f".claude/agents/{agent}.md"
    model = frontmatter_value(text, "model")
    layer = frontmatter_value(text, "layer")
    expected_model = "opus" if agent == "workflow-supervisor" else "sonnet"
    expected_scope = f"@import docs/00.agent-governance/scopes/{layer}.md" if layer else None

    if protocol_path not in protocol:
        failures.append(f"subagent protocol missing runtime agent: {protocol_path}")
    if model != expected_model:
        failures.append(f"{agent_path}: expected model {expected_model!r}, found {model!r}")
    if not layer:
        failures.append(f"{agent_path}: missing layer front matter")
    elif expected_scope not in text:
        failures.append(f"{agent_path}: missing exact scope import {expected_scope!r}")

codex_readme = pathlib.Path(".codex/README.md")
codex_provider = pathlib.Path("docs/00.agent-governance/providers/codex.md")
for path in [codex_readme, codex_provider]:
    text = read(path)
    if not text:
        failures.append(f"missing Codex runtime/provider document: {path}")
        continue
    for required in [
        "AGENTS.md",
        ".codex/hooks.json",
        "scripts/agent-event-hook.sh",
        "docs/00.agent-governance/agents/",
        ".claude",
    ]:
        if required not in text:
            failures.append(f"{path}: missing Codex runtime boundary reference: {required}")

event_hook = pathlib.Path("scripts/agent-event-hook.sh")
if not event_hook.is_file():
    failures.append("missing provider-neutral agent event hook: scripts/agent-event-hook.sh")
else:
    event_hook_text = read(event_hook)
    for literal in [
        "SessionStart",
        "PreToolUse",
        "PostToolUse",
        "scripts/post-tool-validate.sh",
        "graphify-out",
    ]:
        if literal not in event_hook_text:
            failures.append(f"{event_hook}: missing event hook literal: {literal}")

for wrapper, event in {
    pathlib.Path(".claude/hooks/session-start.sh"): "SessionStart",
    pathlib.Path(".claude/hooks/docker-compose-pre.sh"): "PreToolUse",
    pathlib.Path(".claude/hooks/post-tool-validate.sh"): "PostToolUse",
}.items():
    text = read(wrapper)
    if not text:
        failures.append(f"missing Claude hook wrapper: {wrapper}")
        continue
    if "scripts/agent-event-hook.sh" not in text or event not in text:
        failures.append(f"{wrapper}: must delegate {event} to scripts/agent-event-hook.sh")

hook_configs = {
    pathlib.Path(".codex/hooks.json"): "scripts/agent-event-hook.sh",
    pathlib.Path(".claude/settings.json"): ".claude/hooks/",
}
for path, required_command_literal in hook_configs.items():
    text = read(path)
    if not text:
        failures.append(f"missing hook config: {path}")
        continue
    try:
        data = json.loads(text)
    except Exception as exc:
        failures.append(f"{path}: JSON parse failed for hook contract: {exc}")
        continue
    hooks = data.get("hooks", {}) if isinstance(data, dict) else {}
    for event in ["SessionStart", "PreToolUse", "PostToolUse"]:
        if event not in hooks:
            failures.append(f"{path}: missing hook event: {event}")
    if required_command_literal not in text:
        failures.append(f"{path}: missing hook command reference: {required_command_literal}")
    if path == pathlib.Path(".codex/hooks.json"):
        pre_tool_entries = hooks.get("PreToolUse") if isinstance(hooks, dict) else None
        pre_tool_matchers = []
        if isinstance(pre_tool_entries, list):
            pre_tool_matchers = [
                entry.get("matcher", "")
                for entry in pre_tool_entries
                if isinstance(entry, dict)
            ]
        matcher_text = "|".join(pre_tool_matchers)
        for matcher_literal in ["Bash", "Read", "Edit", "Write", "apply_patch"]:
            if matcher_literal not in matcher_text:
                failures.append(f"{path}: PreToolUse matcher must cover {matcher_literal!r}")

claude_settings = read(pathlib.Path(".claude/settings.json"))
if '"Bash(rg:*)"' not in claude_settings:
    failures.append(".claude/settings.json: missing read-only discovery permission Bash(rg:*)")

agents_md = read(pathlib.Path("AGENTS.md"))
if "graphify update ." not in agents_md:
    failures.append("AGENTS.md: missing graphify update command in Graphify contract")
graphify_contract = agents_md.lower()
if "unavailable" not in graphify_contract or "skipped" not in graphify_contract:
    failures.append("AGENTS.md: missing graphify unavailable/skipped fallback in Graphify contract")

stale_patterns = [
    re.compile(r"H100|Harness-100|harness-100|h100_pattern|examples/harness-100"),
    re.compile(r"AGENTS\.md §3 Agent Catalog|AGENTS\.md §4 Orchestration"),
]
scan_roots = [
    pathlib.Path("AGENTS.md"),
    pathlib.Path("CLAUDE.md"),
    pathlib.Path("GEMINI.md"),
    pathlib.Path(".claude"),
    pathlib.Path(".codex"),
    pathlib.Path("docs/00.agent-governance"),
]

files: list[pathlib.Path] = []
for root in scan_roots:
    if root.is_file():
        files.append(root)
    elif root.exists():
        files.extend(p for p in root.rglob("*") if p.is_file() and "memory" not in p.parts)

for path in files:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for pattern in stale_patterns:
        for match in pattern.finditer(text):
            failures.append(f"{path}: stale runtime/governance reference: {match.group(0)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Governance memory contract"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []

required_files = [
    pathlib.Path("docs/00.agent-governance/memory/README.md"),
    pathlib.Path("docs/00.agent-governance/memory/template.md"),
    pathlib.Path("docs/00.agent-governance/memory/progress.md"),
    pathlib.Path("docs/99.templates/memory.template.md"),
    pathlib.Path("docs/99.templates/progress.template.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing governance memory file: {path}")

checks = {
    pathlib.Path("AGENTS.md"): [
        "[LOAD:MEMORY]",
        "docs/00.agent-governance/memory/",
        "update `progress.md` during repository work",
    ],
    pathlib.Path("docs/00.agent-governance/README.md"): [
        "[LOAD:MEMORY]",
        "memory/README.md",
        "mandatory work progress log",
    ],
    pathlib.Path("docs/00.agent-governance/rules/bootstrap.md"): [
        "[LOAD:MEMORY]",
        "Memory is advisory",
        "memory/progress.md",
        "progress logging",
        "docs/99.templates/memory.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/agentic.md"): [
        "advisory retrieval context",
        "Memory notes must not",
        "running work log",
        "docs/99.templates/memory.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/rules/task-checklists.md"): [
        "progress.md",
        "durable finding report",
        "material task progress",
        "final status",
    ],
    pathlib.Path("docs/00.agent-governance/rules/stage-authoring-matrix.md"): [
        "docs/99.templates/memory.template.md",
        "docs/99.templates/progress.template.md",
        "progress log updated",
    ],
    pathlib.Path("docs/00.agent-governance/memory/README.md"): [
        "advisory retrieval context",
        "do not define active policy",
        "Retrieve relevant notes",
        "docs/99.templates/memory.template.md",
        "mandatory agent progress log",
        "docs/99.templates/progress.template.md",
    ],
    pathlib.Path("docs/00.agent-governance/memory/template.md"): [
        "docs/99.templates/memory.template.md",
        "Retrieval Keywords",
        "Last Verified",
        "Evidence",
    ],
    pathlib.Path("docs/99.templates/memory.template.md"): [
        "Memory notes are advisory retrieval context",
        "Retrieval Keywords",
        "Last Verified",
        "## Evidence",
    ],
    pathlib.Path("docs/00.agent-governance/memory/progress.md"): [
        "docs/99.templates/progress.template.md",
        "## Usage Contract",
        "## Current Work Log",
    ],
    pathlib.Path("docs/99.templates/progress.template.md"): [
        "AI agents must update",
        "## Current Work Log",
        "## Phase Tracker",
        "## Related Documents",
    ],
}

for path, literals in checks.items():
    if not path.is_file():
        failures.append(f"missing file for memory contract check: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing memory contract literal: {literal}")

memory_note_required = [
    "- Date:",
    "- Layer:",
    "- Status:",
    "- Applies To:",
    "- Tags:",
    "- Retrieval Keywords:",
    "- Last Verified:",
    "## Problem",
    "## Context",
    "## Resolution",
    "## Prevention",
    "## Evidence",
]
memory_dir = pathlib.Path("docs/00.agent-governance/memory")
for path in sorted(memory_dir.glob("*.md")) if memory_dir.exists() else []:
    if path.name in {"README.md", "progress.md", "template.md"}:
        continue
    text = path.read_text(errors="ignore")
    for literal in memory_note_required:
        if literal not in text:
            failures.append(f"{path}: missing memory note template literal: {literal}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Reference stage contract"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

failures: list[str] = []
root = pathlib.Path("docs/90.references")
template = pathlib.Path("docs/99.templates/reference.template.md")

if not root.is_dir():
    failures.append("missing reference stage folder: docs/90.references")

template_required = [
    "Reference docs provide stable context",
    "## Overview (KR)",
    "## Purpose",
    "## Repository Role",
    "## Scope",
    "## Definitions / Facts",
    "## Source Rules",
    "## Sources",
    "## Maintenance",
    "## Related Documents",
    "do not define active policy",
    "secret values",
]
if not template.is_file():
    failures.append(f"missing reference template: {template}")
else:
    text = template.read_text(errors="ignore")
    for literal in template_required:
        if literal not in text:
            failures.append(f"{template}: missing reference-template literal: {literal}")

readme_required = [
    "## Overview",
    "## Audience",
    "## Scope",
    "## Structure",
    "## How to Work in This Area",
    "## Related Documents",
]
for path in sorted(root.rglob("README.md")) if root.exists() else []:
    text = path.read_text(errors="ignore")
    for heading in readme_required:
        if heading not in text:
            failures.append(f"{path}: missing reference README heading: {heading}")
    if path == root / "README.md":
        for heading in [
            "## Repository Role",
            "## Required Format",
            "## Naming and Lifecycle Rules",
            "## Placement Rules",
        ]:
            if heading not in text:
                failures.append(f"{path}: missing reference root README heading: {heading}")
    elif "## Category Role" not in text:
        failures.append(f"{path}: missing reference category README heading: ## Category Role")

reference_required = [
    "## Overview (KR)",
    "## Purpose",
    "## Repository Role",
    "## Scope",
    "## Definitions / Facts",
    "## Sources",
    "## Maintenance",
    "## Related Documents",
]
placeholder_markers = [
    "[Item Name]",
    "[Why this reference exists",
    "[How this reference supports",
    "[What is covered]",
    "[What is not covered]",
    "[Source 1]",
    "<category>",
    "<item>",
    "<topic>",
]
for path in sorted(root.rglob("*.md")) if root.exists() else []:
    if path.name == "README.md":
        continue
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    has_status = (
        len(lines) >= 3
        and lines[0].strip() == "---"
        and any(line.startswith("status:") and line.split(":", 1)[1].strip() for line in lines[1:12])
    )
    if not has_status:
        failures.append(f"{path}: missing frontmatter status")
    for heading in reference_required:
        if heading not in text:
            failures.append(f"{path}: missing reference heading: {heading}")
    for marker in placeholder_markers:
        if marker in text:
            failures.append(f"{path}: unresolved reference-template marker: {marker}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "LLM Wiki contract"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

failures: list[str] = []

required_files = [
    pathlib.Path("llms.txt"),
    pathlib.Path("scripts/generate-llm-wiki-index.sh"),
    pathlib.Path("docs/05.operations/guides/llm-wiki-maintenance.md"),
    pathlib.Path("docs/90.references/llm-wiki/README.md"),
    pathlib.Path("docs/90.references/llm-wiki/index.md"),
    pathlib.Path("docs/90.references/llm-wiki/repository-map.md"),
    pathlib.Path(".claude/agents/wiki-curator.md"),
    pathlib.Path("docs/00.agent-governance/agents/agents/wiki-curator.md"),
    pathlib.Path("docs/03.specs/llm-wiki-agent-first-completion/spec.md"),
    pathlib.Path("docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md"),
    pathlib.Path("docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md"),
]

for path in required_files:
    if not path.is_file():
        failures.append(f"missing LLM Wiki file: {path}")

llms_path = pathlib.Path("llms.txt")
if llms_path.is_file():
    text = llms_path.read_text(errors="ignore")
    required_literals = [
        "docs/90.references/llm-wiki/index.md",
        "docs/90.references/llm-wiki/repository-map.md",
        "generated tracked repo-local path index",
        "tracked source files",
        "Runtime truth",
        "secrets/",
        "volumes/",
        "graphify-out/",
        "advisory",
        "not authoritative source material",
        "llms-full.txt",
        "public website",
    ]
    for literal in required_literals:
        if literal not in text:
            failures.append(f"{llms_path}: missing LLM Wiki boundary literal: {literal}")

readme_checks = {
    pathlib.Path("README.md"): [
        "llms.txt",
        "docs/90.references/llm-wiki/",
        "docs/90.references/llm-wiki/index.md",
    ],
    pathlib.Path("docs/README.md"): [
        "90.references/llm-wiki/",
        "LLM Wiki contract",
        "generated index freshness",
    ],
    pathlib.Path("docs/90.references/README.md"): [
        "llm-wiki/README.md",
        "llm-wiki/index.md",
    ],
    pathlib.Path("docs/05.operations/guides/README.md"): [
        "llm-wiki-maintenance.md",
    ],
    pathlib.Path("scripts/README.md"): [
        "generate-llm-wiki-index.sh",
        "--check",
    ],
    pathlib.Path("docs/00.agent-governance/agents/README.md"): [
        "wiki-curator",
    ],
    pathlib.Path("docs/00.agent-governance/subagent-protocol.md"): [
        ".claude/agents/wiki-curator.md",
        "wiki-curator",
    ],
    pathlib.Path(".claude/CLAUDE.md"): [
        "8 workers",
    ],
}
for path, literals in readme_checks.items():
    if not path.is_file():
        failures.append(f"missing file for LLM Wiki README registration: {path}")
        continue
    text = path.read_text(errors="ignore")
    for literal in literals:
        if literal not in text:
            failures.append(f"{path}: missing LLM Wiki registration literal: {literal}")

wiki_files = [path for path in pathlib.Path("docs/90.references/llm-wiki").glob("*.md")]
safety_files = [
    llms_path,
    pathlib.Path("docs/05.operations/guides/llm-wiki-maintenance.md"),
    *wiki_files,
]
for path in safety_files:
    if not path.is_file():
        continue
    text = path.read_text(errors="ignore")
    lower_text = text.lower()
    if "file://" in text:
        failures.append(f"{path}: file:// links are not allowed in LLM Wiki")
    unsafe_phrases = [
        "read secret values",
        "quote secret values",
        "dump secrets",
        "print secrets",
        "graphify-out/ is authoritative",
        "graphify-out is authoritative",
        "graphify-out/ as authoritative",
        "graphify-out as authoritative",
    ]
    for phrase in unsafe_phrases:
        if phrase in lower_text:
            failures.append(f"{path}: unsafe LLM Wiki wording: {phrase}")
    if (
        re.search(r"(?i)\bpublic\s+(site|website|wiki)\b", text)
        and "Out of Scope" not in text
        and "Disallowed" not in text
        and "does not define a public website" not in text
    ):
        failures.append(f"{path}: public wiki/site wording must be explicitly out of scope")

map_path = pathlib.Path("docs/90.references/llm-wiki/repository-map.md")
if map_path.is_file():
    text = map_path.read_text(errors="ignore")
    for literal in [
        "tracked source files",
        "Runtime truth",
        "secrets/",
        "volumes/",
        "graphify-out/",
        "authoritative source",
        "## Repository Map",
    ]:
        if literal not in text:
            failures.append(f"{map_path}: missing repository map boundary literal: {literal}")

index_path = pathlib.Path("docs/90.references/llm-wiki/index.md")
if index_path.is_file():
    text = index_path.read_text(errors="ignore")
    for literal in [
        "generated_by: scripts/generate-llm-wiki-index.sh",
        "Generated tracked repo-local index",
        "## Generated Index",
        "scripts/generate-llm-wiki-index.sh --check",
        "wiki-curator",
    ]:
        if literal not in text:
            failures.append(f"{index_path}: missing generated index literal: {literal}")

    generated_section = text.split("## Generated Index", 1)[-1].split("## Sources", 1)[0]
    for forbidden in [
        "volumes/",
        "graphify-out/",
        "node_modules/",
        ".min.js",
        ".min.css",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
    ]:
        if forbidden in generated_section:
            failures.append(f"{index_path}: generated index includes excluded path marker: {forbidden}")
    for match in re.finditer(r"\[([^\]]+)\]\(", generated_section):
        linked_path = match.group(1)
        if linked_path.startswith("secrets/") and linked_path != "secrets/README.md":
            failures.append(f"{index_path}: generated index includes secret content path: {linked_path}")

generator = pathlib.Path("scripts/generate-llm-wiki-index.sh")
if generator.is_file() and index_path.is_file():
    result = subprocess.run(
        ["bash", "scripts/generate-llm-wiki-index.sh", "--check"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        failures.append("generated LLM Wiki index is stale or generator check failed")
        for line in (result.stderr or result.stdout).splitlines():
            failures.append(f"generate-llm-wiki-index.sh --check: {line}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Script reference integrity"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

roots = [
    pathlib.Path(p)
    for p in [
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "docs",
        "infra",
        "scripts",
        ".github",
        ".claude",
        ".codex",
        "secrets",
        ".pre-commit-config.yaml",
        "docker-compose.yml",
    ]
    if pathlib.Path(p).exists()
]

failures: list[str] = []
pattern = re.compile(r"(?<![\w./-])(\./)?(scripts/[A-Za-z0-9._/-]+\.sh)")

for root in roots:
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and "graphify-out" not in p.parts]
    for path in files:
        if path == pathlib.Path("scripts/check-repo-contracts.sh"):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for match in pattern.finditer(text):
            ref = match.group(2)
            local_target = path.parent / ref
            root_target = pathlib.Path(ref)
            if local_target.is_file() or root_target.is_file():
                continue
            failures.append(f"{path}: missing script reference {match.group(0)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Service documentation coverage"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

stages = ["05.operations/guides"]

# Implementation path names sometimes differ from product names. Keep those
# differences explicit so missing docs do not get hidden by ad-hoc conventions.
document_path_overrides = {
    pathlib.Path("04-data/analytics/ksql"): pathlib.Path("04-data/analytics/ksqldb.md"),
}

# Aggregate compose files are documented by component-level docs in the same
# stage folder, not by a single service markdown file.
aggregate_compose_dirs = {
    pathlib.Path("06-observability"),
}

service_dirs = sorted(
    {
        path.parent.relative_to("infra")
        for path in pathlib.Path("infra").rglob("docker-compose*.yml")
        if path.is_file()
    }
)

failures: list[str] = []

for service_dir in service_dirs:
    if service_dir in aggregate_compose_dirs:
        continue

    doc_rel = document_path_overrides.get(service_dir, pathlib.Path(f"{service_dir}.md"))
    for stage in stages:
        doc_path = pathlib.Path("docs") / stage / doc_rel
        if not doc_path.is_file():
            failures.append(f"missing {stage} service documentation for infra/{service_dir}: expected {doc_path}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Script usage contract"
if ! python3 - <<'PY'
from __future__ import annotations

import pathlib
import sys

readme = pathlib.Path("scripts/README.md")
if not readme.is_file():
    print("FAIL: missing scripts/README.md", file=sys.stderr)
    sys.exit(1)

readme_text = readme.read_text()
failures: list[str] = []
required_readme_fragments = [
    "## Purpose Folder Plan",
    "scripts/validation/",
    "scripts/hardening/",
    "scripts/hooks/",
    "scripts/knowledge/",
    "scripts/operations/",
    "scripts/lib/",
    "root compatibility wrappers",
]
for fragment in required_readme_fragments:
    if fragment not in readme_text:
        failures.append(f"scripts/README.md missing script purpose-folder plan fragment: {fragment}")

# Root scripts in this set are intentionally allowed to be standalone: they
# must be inventoried in scripts/README.md, but do not need another repository
# entrypoint, stage document, runtime hook, or CI workflow reference.
external_reference_exemptions = {
    pathlib.Path("scripts/generate-local-certs.sh"),
}
root_scripts = sorted(path for path in pathlib.Path("scripts").glob("*.sh") if path.is_file())
lib_scripts = sorted(path for path in pathlib.Path("scripts/lib").glob("*.sh") if path.is_file())

for path in external_reference_exemptions:
    if not path.is_file():
        failures.append(f"external-reference exemption points to missing root script: {path}")

for path in root_scripts:
    if path.name not in readme_text and str(path) not in readme_text:
        failures.append(f"scripts/README.md missing root script inventory entry: {path}")

scan_roots = [
    pathlib.Path(p)
    for p in [
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "docs",
        "infra",
        "scripts",
        ".github",
        ".claude",
        ".codex",
        ".pre-commit-config.yaml",
        "docker-compose.yml",
    ]
    if pathlib.Path(p).exists()
]

def iter_files(root: pathlib.Path) -> list[pathlib.Path]:
    if root.is_file():
        return [root]
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and "graphify-out" not in path.parts
    ]

scanned_files: list[tuple[pathlib.Path, str]] = []
for root in scan_roots:
    for path in iter_files(root):
        try:
            scanned_files.append((path, path.read_text(errors="ignore")))
        except Exception:
            continue

for script in root_scripts:
    if script in external_reference_exemptions:
        continue
    candidates = {str(script), f"./{script}", script.name}
    referenced = False
    for path, text in scanned_files:
        if path in {script, readme}:
            continue
        if any(candidate in text for candidate in candidates):
            referenced = True
            break
    if not referenced:
        failures.append(
            "root script is not externally referenced and is not in the external-reference exemption set: "
            f"{script}"
        )

root_script_texts: list[tuple[pathlib.Path, str]] = []
for script in root_scripts:
    try:
        root_script_texts.append((script, script.read_text(errors="ignore")))
    except Exception:
        continue

for lib_script in lib_scripts:
    candidates = {str(lib_script), f"./{lib_script}", str(lib_script.relative_to("scripts")), lib_script.name}
    referenced = any(
        any(candidate in text for candidate in candidates)
        for _script, text in root_script_texts
    )
    if not referenced:
        failures.append(f"library script is not referenced by any root script: {lib_script}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Floating image tag policy"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

exceptions_path = pathlib.Path("infra/image-tag-policy.exceptions.json")
if not exceptions_path.is_file():
    print(f"FAIL: missing image tag exception registry: {exceptions_path}", file=sys.stderr)
    sys.exit(1)

exceptions_data = json.loads(exceptions_path.read_text())
exceptions = {
    item["image"]
    for item in exceptions_data.get("floating_image_exceptions", [])
    if item.get("image") and item.get("owner") and item.get("reason") and item.get("review_cadence")
}

floating_suffixes = (":main", ":latest", ":stable", ":edge", ":nightly", ":dev", ":sts", ":alpine")
failures: list[str] = []

def is_floating(image: str) -> bool:
    tag = image.rsplit(":", 1)[-1] if ":" in image.rsplit("/", 1)[-1] else ""
    if not tag:
        return True
    return image.endswith(floating_suffixes) or "latest" in tag

for path in sorted(pathlib.Path("infra").rglob("*")):
    if not path.is_file():
        continue
    if path.name.startswith("docker-compose") and path.suffix in {".yml", ".yaml"}:
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"image:\s*['\"]?([^'\"\s#]+)", stripped)
            if match:
                image = match.group(1)
                if is_floating(image) and image not in exceptions:
                    failures.append(f"{path}:{line_no}: floating image tag requires exception or pinned tag: {image}")
    elif path.name.endswith("Dockerfile") or path.name == "Dockerfile":
        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"FROM\s+([^@\s]+)", stripped)
            if match:
                image = match.group(1)
                if is_floating(image) and image not in exceptions:
                    failures.append(f"{path}:{line_no}: floating base image tag requires exception or pinned tag: {image}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

section "Tech-stack version drift"
if ! python3 - <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

registry_path = pathlib.Path("infra/tech-stack.versions.json")
if not registry_path.is_file():
    print(f"FAIL: missing tech-stack version registry: {registry_path}", file=sys.stderr)
    sys.exit(1)

try:
    registry = json.loads(registry_path.read_text())
except Exception as exc:
    print(f"FAIL: invalid JSON in {registry_path}: {exc}", file=sys.stderr)
    sys.exit(1)

entries = registry.get("entries")
if not isinstance(entries, list) or not entries:
    print(f"FAIL: {registry_path} must define a non-empty entries list", file=sys.stderr)
    sys.exit(1)

failures: list[str] = []
image_line_re = re.compile(r"(?m)^\s*image:\s*['\"]?([^'\"\s#]+)")
default_image_re = re.compile(r"\$\{[^}:]+:-([^}]+)\}")

def declared_images(path: pathlib.Path) -> set[str]:
    text = path.read_text(errors="ignore")
    images: set[str] = set()
    for match in image_line_re.finditer(text):
        raw = match.group(1)
        images.add(raw)
        default_match = default_image_re.search(raw)
        if default_match:
            images.add(default_match.group(1))
    return images

for index, entry in enumerate(entries, start=1):
    component = entry.get("component")
    images = entry.get("images")
    compose_files = entry.get("compose_files")

    if not component or not isinstance(images, list) or not images or not isinstance(compose_files, list) or not compose_files:
        failures.append(f"{registry_path}: entry #{index} must include component, images, and compose_files")
        continue

    discovered: set[str] = set()
    for compose_file in compose_files:
        compose_path = pathlib.Path(compose_file)
        if not compose_path.is_file():
            failures.append(f"{registry_path}: {component} references missing compose file: {compose_file}")
            continue
        discovered.update(declared_images(compose_path))

    for image in images:
        if image not in discovered:
            failures.append(f"{registry_path}: {component} expected image not declared in listed compose files: {image}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)
PY
then
  failures=$((failures + 1))
fi

echo
echo "Repo contract check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: repository Docker/docs contracts are synchronized"
