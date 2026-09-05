#!/usr/bin/env bash
# agent-event-hook.sh - provider-neutral event hook dispatcher.
set -euo pipefail

EVENT="${1:-}"
INPUT="$(cat || true)"
PROJECT_DIR="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"

cd "$PROJECT_DIR"

if [[ -z "$EVENT" ]]; then
  EVENT="$(
    HOOK_INPUT="$INPUT" python3 - <<'PY'
import json
import os

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
except Exception:
    data = {}

print(data.get("hook_event_name", "") if isinstance(data, dict) else "")
PY
  )"
fi

session_start() {
  python3 - "$PROJECT_DIR" <<'PY'
import json
import pathlib
import subprocess
import sys

project = pathlib.Path(sys.argv[1])

def run(command, fallback="unknown", timeout=3):
    try:
        result = subprocess.run(
            command,
            cwd=project,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception:
        return fallback
    text = result.stdout.strip()
    return text if result.returncode == 0 and text else fallback

branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
changed = run(["git", "status", "--short"], fallback="")
changed_count = len([line for line in changed.splitlines() if line.strip()]) if changed else 0
last_commit = run(["git", "log", "-1", "--format=%h %s"])
infra_dir = project / "infra"
infra_entries = ", ".join(sorted(path.name for path in infra_dir.iterdir())) if infra_dir.is_dir() else "none"

message = f"""hy-home.docker project context

Git status:
- Branch: `{branch}`
- Changed files: `{changed_count}`
- Last commit: `{last_commit}`

Infra layer:
{infra_entries}

Key rules:
- Use `AGENTS.md` and `docs/00.agent-governance/` as governance entry points.
- Treat Graphify as advisory when `scripts/knowledge/report-graphify-health.sh` reports contamination.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` before completion.
"""

print(json.dumps({"systemMessage": message.strip()}))
PY
}

pre_tool_use() {
  HOOK_INPUT="$INPUT" python3 - "$PROJECT_DIR" <<'PY'
import json
import os
import pathlib
import re
import sys

project = pathlib.Path(sys.argv[1])
raw = os.environ.get("HOOK_INPUT", "")

try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

if not isinstance(data, dict):
    data = {}

tool_name = str(data.get("tool_name") or "")
tool_input = data.get("tool_input", {})
if not isinstance(tool_input, dict):
    tool_input = {}

paths = []

def add(value):
    if isinstance(value, str) and value:
        paths.append(value)

for key in ("file_path", "path"):
    add(tool_input.get(key))

for key in ("files", "paths"):
    value = tool_input.get(key)
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                add(item)
            elif isinstance(item, dict):
                add(item.get("file_path") or item.get("path"))

edits = tool_input.get("edits")
if isinstance(edits, list):
    for edit in edits:
        if isinstance(edit, dict):
            add(edit.get("file_path") or edit.get("path"))

for match in re.finditer(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", raw, re.M):
    add(match.group(1).strip())
for match in re.finditer(r"^\*\*\* Move to: (.+)$", raw, re.M):
    add(match.group(1).strip())

seen = set()
paths = [path for path in paths if not (path in seen or seen.add(path))]

system_messages = []
additional_context = []

graph_tools = {"Bash", "Glob", "Grep", "Read", "LS"}
if (project / "graphify-out" / "graph.json").is_file() and (not tool_name or tool_name in graph_tools):
    additional_context.append(
        "graphify: Knowledge graph exists. Read graphify-out/GRAPH_REPORT.md first; "
        "when report health is advisory for any reason, including ignored volumes, "
        "gitlink/submodule content, generated/minified artifacts, meaningless god nodes, "
        "or unrelated cross-root inferred edges, corroborate against tracked source files, "
        "docs/00.agent-governance, and stage docs."
    )

edit_tools = {"Write", "Edit", "MultiEdit", "apply_patch", "ApplyPatch"}
if not tool_name or tool_name in edit_tools:
    def service_marker_for(short_path: str) -> bool:
        target = (project / short_path).resolve()
        directory = target.parent if target.name == "README.md" else target
        marker_names = {
            "compose.yml",
            "compose.yaml",
            "docker-compose.yml",
            "docker-compose.yaml",
            "Dockerfile",
        }
        try:
            return any((directory / name).exists() for name in marker_names)
        except Exception:
            return False

    for path in paths:
        short_path = path
        project_prefix = str(project) + "/"
        if short_path.startswith(project_prefix):
            short_path = short_path[len(project_prefix):]
        if re.search(r"docker-compose.*\.ya?ml$", short_path):
            system_messages.append(
                "Docker Compose file edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "After editing, run `python3 scripts/validation/run-ci-gate.py --profile changed`."
            )
            break
    for path in paths:
        short_path = path
        project_prefix = str(project) + "/"
        if short_path.startswith(project_prefix):
            short_path = short_path[len(project_prefix):]
        short_path = short_path.removeprefix("./")
        if short_path.startswith(".agents/"):
            system_messages.append(
                "Non-authoritative .agents container edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "An absent or empty real `.agents/` directory is allowed, but it has no shared "
                "roles, skills, generated README, or native picker route. Unknown or nonempty "
                "contents fail closed and must be preserved; do not regenerate or delete them. "
                "Load common policies, roles, and procedures from `docs/00.agent-governance/`; "
                "do not infer a compatibility projection. "
                "After editing, run `python3 scripts/validation/run-ci-gate.py --profile changed`."
            )
            break
    for path in paths:
        short_path = path
        project_prefix = str(project) + "/"
        if short_path.startswith(project_prefix):
            short_path = short_path[len(project_prefix):]
        short_path = short_path.removeprefix("./")
        if re.match(r"docs/(01\.requirements|02\.architecture|03\.specs|04\.execution|05\.operations|90\.references)/", short_path):
            system_messages.append(
                "Target-stage documentation edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "Before writing or updating this document, load the matching template from "
                "`docs/99.templates/` and preserve its required headings, target path guidance, "
                "target-relative links, and `## Related Documents` section. The PostToolUse and "
                "Stop hooks run `python3 scripts/validation/run-ci-gate.py --profile changed` to enforce the "
                "changed-doc template gate."
            )
            break
    for path in paths:
        short_path = path
        project_prefix = str(project) + "/"
        if short_path.startswith(project_prefix):
            short_path = short_path[len(project_prefix):]
        short_path = short_path.removeprefix("./")
        if short_path.endswith("README.md"):
            if short_path.startswith("infra/") and service_marker_for(short_path):
                system_messages.append(
                    "Infra service README edit detected.\n\n"
                    f"Path: `{short_path}`\n\n"
                    "Use `docs/99.templates/templates/common/readme-stage.template.md` with the Infra Service "
                    "Readiness snippet. Include Purpose, Config files, Config values, "
                    "Compose linkage, Networks, Volumes, Ports, Labels, Secret refs, "
                    "Healthcheck, Operations, Validation, and Troubleshooting. Record "
                    "secret names and mount paths only; never read or paste secret values."
                )
            else:
                system_messages.append(
                    "README edit detected.\n\n"
                    f"Path: `{short_path}`\n\n"
                    "Use `docs/99.templates/templates/common/readme-stage.template.md` as the target-path guide. "
                    "Decide whether this README is a folder index or service leaf before "
                    "editing, preserve `## Related Documents`, and calculate links from "
                    "the README target path rather than from `docs/99.templates/`."
                )
            break

# Evaluate the Stage 00 hook rules. Their frontmatter is the machine part and
# their body is the message; before this they were enforced by nothing.
denials = []
try:
    rules_module = project / "scripts" / "hooks" / "hook_rules.py"
    sys.path.insert(0, str(rules_module.parent))
    import hook_rules

    command = tool_input.get("command")
    command = command if isinstance(command, str) else ""
    project_prefix = str(project) + "/"

    def _short(value):
        return value[len(project_prefix):] if value.startswith(project_prefix) else value

    replacement = ""
    for key in ("content", "new_string", "new_text"):
        value = tool_input.get(key)
        if isinstance(value, str):
            replacement = value
            break
    edits = [(_short(path), replacement) for path in paths]
    nested = tool_input.get("edits")
    if isinstance(nested, list):
        for edit in nested:
            if not isinstance(edit, dict):
                continue
            target = edit.get("file_path") or edit.get("path")
            text = edit.get("new_string") or edit.get("new_text")
            if isinstance(target, str) and isinstance(text, str):
                edits.append((_short(target), text))

    warnings, blocks = hook_rules.evaluate(
        hook_rules.load_rules(project), command=command, edits=tuple(edits)
    )
    system_messages.extend(rule.message for rule in warnings)
    denials.extend(blocks)
except Exception:
    # A defect in rule evaluation must not break every tool call.
    denials = []

if denials:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "\n\n".join(rule.message for rule in denials),
    }}))
    sys.exit(0)

if not system_messages and not additional_context:
    sys.exit(0)

output = {}
if system_messages:
    output["systemMessage"] = "\n\n".join(system_messages)
if additional_context:
    output["hookSpecificOutput"] = {
        "hookEventName": "PreToolUse",
        "additionalContext": "\n\n".join(additional_context),
    }

print(json.dumps(output))
PY
}

post_tool_use() {
  printf '%s' "$INPUT" | CODEX_PROJECT_DIR="$PROJECT_DIR" CLAUDE_PROJECT_DIR="$PROJECT_DIR" bash scripts/hooks/post-tool-validate.sh
}

session_end() {
  python3 - "$PROJECT_DIR" <<'PY' || true
import json
import pathlib
import subprocess
import sys

project = pathlib.Path(sys.argv[1])

def run(cmd, fallback="unknown", timeout=3):
    try:
        r = subprocess.run(cmd, cwd=project, capture_output=True, text=True, timeout=timeout, check=False)
        t = r.stdout.strip()
        return t if r.returncode == 0 and t else fallback
    except Exception:
        return fallback

branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
last_commit = run(["git", "log", "-1", "--format=%h %s"])
changed = run(["git", "status", "--short"], fallback="")
changed_count = len([line for line in changed.splitlines() if line.strip()]) if changed else 0

msg = f"""Session ending — governance reminder:

- Update the active co-located Stage 03 Task named by the current bootstrap/spec context before this session closes.
- Record changed files, verification evidence, and any residual risk or open gap.
- When repository-modifying work is complete, create small Conventional Commits by logical unit before the final response unless the user explicitly asked not to commit, the work is incomplete, or required checks/approvals are missing.
- Stage only task-owned files or hunks, and leave unrelated untracked files untouched.

Current state:
- Branch: `{branch}`
- Last commit: `{last_commit}`
- Uncommitted changes: `{changed_count}` files"""

print(json.dumps({"systemMessage": msg.strip()}))
PY
}

has_changed_target_stage_docs() {
  python3 - <<'PY'
from __future__ import annotations

import pathlib
import subprocess
import sys

stage_roots = (
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/05.operations"),
    pathlib.Path("docs/90.references"),
)


def run_git(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


paths: set[pathlib.Path] = set()
for git_args in (
    ["diff", "--name-only", "--diff-filter=AM"],
    ["diff", "--cached", "--name-only", "--diff-filter=AM"],
    ["ls-files", "--others", "--exclude-standard"],
):
    paths.update(pathlib.Path(path) for path in run_git(git_args))

for path in paths:
    if path.suffix.lower() not in {".md", ".yaml", ".yml", ".graphql", ".proto"}:
        continue
    if any(is_relative_to(path, root) for root in stage_roots):
        sys.exit(0)

sys.exit(1)
PY
}

template_stop_gate() {
  if ! has_changed_target_stage_docs; then
    return 0
  fi

  local output
  if output="$(python3 scripts/validation/run-ci-gate.py --profile changed 2>&1)"; then
    return 0
  fi

  GATE_OUTPUT="$output" HOOK_INPUT="$INPUT" python3 - <<'PY'
import json
import os

output = os.environ.get("GATE_OUTPUT", "").strip()
reason = (
    "Changed target-stage documentation does not satisfy the docs/99.templates "
    "contract. Continue the task, fix the document from the mapped template, "
    "and rerun `python3 scripts/validation/run-ci-gate.py --profile changed`."
)
if output:
    reason = f"{reason}\n\nValidator output:\n{output[-6000:]}"

if os.environ.get("HY_HOME_HOOK_PROVIDER") == "codex":
    try:
        payload = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
    except (TypeError, ValueError):
        payload = {}
    if isinstance(payload, dict) and payload.get("stop_hook_active") is True:
        print(json.dumps({
            "continue": False,
            "stopReason": f"Stop retry limit reached. {reason}",
        }))
    else:
        print(json.dumps({"decision": "block", "reason": reason}))
else:
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "systemMessage": reason,
    }))
PY
  return 1
}

logical_commit_stop_gate() {
  if [[ "${AGENT_ALLOW_UNCOMMITTED_STOP:-}" == "1" ]]; then
    return 0
  fi

  local output
  output="$(
    python3 - <<'PY'
from __future__ import annotations

import pathlib
import subprocess

try:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
except subprocess.CalledProcessError:
    raise SystemExit(0)

REGISTRY = "docs/00.agent-governance/policies/approval-boundaries.md"
SCHEMA = "agent-governance/deferred-paths/v1"


def deferred_paths() -> set[str]:
    """Paths tracked governance declares intentionally dirty.

    Fails closed: any missing, untracked, unreadable, or malformed registry
    yields no exemptions, so the gate keeps blocking exactly as before.
    """
    registry = pathlib.Path(REGISTRY)
    if not registry.is_file():
        return set()

    # The declaration must itself be committed, so exempting a path is a
    # reviewable act rather than a local edit the gate would trust blindly.
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", REGISTRY],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if tracked.returncode != 0:
        return set()

    try:
        import yaml
    except ImportError:
        return set()

    try:
        document = yaml.safe_load(registry.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return set()

    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        return set()

    entries = document.get("deferrals")
    if not isinstance(entries, list):
        return set()

    declared: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        reason = entry.get("reason")
        owning_task = entry.get("owning_task")
        if not isinstance(path, str) or not path.strip():
            continue
        if not isinstance(reason, str) or not reason.strip():
            continue
        if not isinstance(owning_task, str) or not owning_task.strip():
            continue
        if not pathlib.Path(owning_task).is_file():
            continue
        declared.add(path.strip())
    return declared


exempt = deferred_paths()

paths: list[str] = []
for line in result.stdout.splitlines():
    if not line.strip():
        continue
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    if path in exempt:
        continue
    paths.append(path)

print("\n".join(paths[:80]))
PY
  )"

  if [[ -z "$output" ]]; then
    return 0
  fi

  GATE_OUTPUT="$output" HOOK_INPUT="$INPUT" python3 - <<'PY'
import json
import os

paths = os.environ.get("GATE_OUTPUT", "").strip()
reason = (
    "Repository-modifying work still has uncommitted task-owned changes. "
    "Before the final response, inspect the diff, run the relevant checks, "
    "stage only task-owned files or hunks, and create small Conventional "
    "Commits by logical unit. Leave unrelated untracked paths untouched. "
    "If this stop is intentionally an incomplete handoff, record the reason "
    "and set AGENT_ALLOW_UNCOMMITTED_STOP=1 for that stop attempt."
)
if paths:
    reason = f"{reason}\n\nUncommitted paths:\n{paths}"

if os.environ.get("HY_HOME_HOOK_PROVIDER") == "codex":
    try:
        payload = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
    except (TypeError, ValueError):
        payload = {}
    if isinstance(payload, dict) and payload.get("stop_hook_active") is True:
        print(json.dumps({
            "continue": False,
            "stopReason": f"Stop retry limit reached. {reason}",
        }))
    else:
        print(json.dumps({"decision": "block", "reason": reason}))
else:
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "systemMessage": reason,
    }))
PY
  return 1
}

stop() {
  if template_stop_gate && logical_commit_stop_gate; then
    session_end
  fi
}

user_prompt_submit() {
  HOOK_INPUT="$INPUT" python3 - "$PROJECT_DIR" <<'PY'
import json
import os
import sys

project = sys.argv[1]
raw = os.environ.get("HOOK_INPUT", "")

try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

prompt = str(data.get("prompt", "")).lower()

FUNCTIONS = [
    {
        "label": "compose-stack-agent",
        "path": "docs/00.agent-governance/skills/compose-stack-agent.md",
        "desc": "Compose 서비스 스택 검토 및 QW-001~005 인프라 기준선 검사",
        "keywords": [
            "healthcheck", "health check", "restart policy",
            "qw-001", "qw-002", "qw-003", "qw-004", "qw-005", "quickwin",
            "compose stack", "infra tier",
        ],
    },
    {
        "label": "requirements-to-design-agent",
        "path": "docs/00.agent-governance/skills/requirements-to-design-agent.md",
        "desc": "Stage 01→02 PRD→ARD/ADR 트레이서빌리티 갭 분석",
        "keywords": [
            "prd", "ard", "requirements to design", "architecture decision",
            "stage 01", "stage 02", "01.requirements", "02.architecture", "adr",
        ],
    },
    {
        "label": "execution-plan-agent",
        "path": "docs/00.agent-governance/skills/execution-plan-agent.md",
        "desc": "Stage 03 스펙→플랜 분해 및 실행 계획 작성",
        "keywords": [
            "execution plan", "spec to plan", "stage 03",
            "03.specs", "plan template", "implementation plan",
        ],
    },
    {
        "label": "task-breakdown-agent",
        "path": "docs/00.agent-governance/skills/task-breakdown-agent.md",
        "desc": "플랜→태스크 분해 및 실행 증거 기록",
        "keywords": [
            "task breakdown", "task evidence", "plan to task",
            "effort estimation", "execution task", "task template",
        ],
    },
    {
        "label": "ops-runbook-agent",
        "path": "docs/00.agent-governance/skills/ops-runbook-agent.md",
        "desc": "Stage 05 운영 런북 작성 및 장애 대응 절차 문서화",
        "keywords": [
            "runbook", "stage 05", "05.operations", "backup procedure",
            "recovery procedure", "incident runbook", "ops runbook",
        ],
    },
    {
        "label": "knowledge-map-agent",
        "path": "docs/00.agent-governance/skills/knowledge-map-agent.md",
        "desc": "Graphify 지식 그래프 탐색 및 문서 간 트레이서빌리티 갭 감지",
        "keywords": [
            "graphify", "knowledge graph", "traceability gap", "orphaned doc",
            "cross-document", "missing link", "knowledge map",
        ],
    },
    {
        "label": "policy-gate-agent",
        "path": "docs/00.agent-governance/skills/policy-gate-agent.md",
        "desc": "전체 검증 스크립트 오케스트레이션 및 정책 게이트 통과 확인",
        "keywords": [
            "policy gate", "validation suite", "public gate",
            "changed profile", "full profile",
            "policy validation",
        ],
    },
]

matched = [function for function in FUNCTIONS if any(keyword in prompt for keyword in function["keywords"])]

if not matched:
    sys.exit(0)

lines = ["Canonical Stage 00 function routes that may apply to this prompt:"]
for function in matched:
    lines.append(
        f"  - **{function['label']}** (`{function['path']}`): {function['desc']}"
    )

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "\n".join(lines),
    }
}))
PY
}

pre_compact() {
  python3 - "$PROJECT_DIR" <<'PY' || true
import json
import pathlib
import subprocess
import sys

project = pathlib.Path(sys.argv[1])

def run(cmd, fallback="unknown", timeout=3):
    try:
        r = subprocess.run(cmd, cwd=project, capture_output=True, text=True, timeout=timeout, check=False)
        t = r.stdout.strip()
        return t if r.returncode == 0 and t else fallback
    except Exception:
        return fallback

branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
last_commit = run(["git", "log", "-1", "--format=%h %s"])
changed = run(["git", "status", "--short"], fallback="")
changed_count = len([l for l in changed.splitlines() if l.strip()]) if changed else 0

msg = f"""Context compaction imminent — state snapshot:

- Branch: `{branch}`
- Last commit: `{last_commit}`
- Uncommitted changes: `{changed_count}` files

Before compaction, ensure:
- Current tracked, staged, and untracked state is preserved without hiding unrelated work.
- The active co-located Stage 03 Task named by the current bootstrap/spec context reflects current progress.
- Any in-flight plan or decision is recorded in that Task or its governing Spec/Plan."""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreCompact",
        "additionalContext": msg.strip(),
    }
}))
PY
}

case "$EVENT" in
SessionStart)
  session_start
  ;;
PreToolUse)
  pre_tool_use
  ;;
PostToolUse)
  post_tool_use
  ;;
SessionEnd)
  session_end
  ;;
Stop)
  stop
  ;;
PreCompact)
  pre_compact
  ;;
UserPromptSubmit)
  user_prompt_submit
  ;;
*)
  exit 0
  ;;
esac
