#!/usr/bin/env bash
# agent-event-hook.sh - provider-neutral event hook dispatcher.
set -euo pipefail

EVENT="${1:-}"
HOOK_PAYLOAD_MODULE="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")/../lib/hooks/tool_payload.py"
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
- Use `AGENTS.md` and `.agents/` as governance entry points.
- Treat Graphify as advisory when `scripts/knowledge/report-graphify-health.sh` reports contamination.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` before completion.
"""

print(json.dumps({"systemMessage": message.strip()}))
PY
}

pre_tool_use() {
  if python3 - "$PROJECT_DIR" "$HOOK_PAYLOAD_MODULE" 3<<<"$INPUT" <<'PY'
import json
import pathlib
import re
import sys

project = pathlib.Path(sys.argv[1])
raw = open(3, encoding="utf-8").read().removesuffix("\n")

def deny_policy_failure(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    raise SystemExit(0)

try:
    sys.path.insert(0, str(pathlib.Path(sys.argv[2]).resolve().parents[3]))
    from scripts.lib.hooks.tool_payload import decode_payload, edit_targets
    data = decode_payload(raw)
    edits = edit_targets(project, data)
except Exception:
    deny_policy_failure("PreToolUse input is invalid; policy evaluation could not run.")

if not isinstance(data, dict):
    deny_policy_failure("PreToolUse input is invalid; policy evaluation could not run.")

tool_name = str(data.get("tool_name") or "")
tool_input = data.get("tool_input", {})
if not isinstance(tool_input, dict):
    tool_input = {}

paths = list(dict.fromkeys(path for path, _ in edits))

system_messages = []
additional_context = []

graph_tools = {"Bash", "Glob", "Grep", "Read", "LS"}
if (project / "graphify-out" / "graph.json").is_file() and (not tool_name or tool_name in graph_tools):
    additional_context.append(
        "graphify: Knowledge graph exists. Read graphify-out/GRAPH_REPORT.md first; "
        "when report health is advisory for any reason, including ignored volumes, "
        "gitlink/submodule content, generated/minified artifacts, meaningless god nodes, "
        "or unrelated cross-root inferred edges, corroborate against tracked source files, "
        ".agents/governance, and stage docs."
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
                "Canonical agent governance edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "Load shared policy from `.agents/governance/`, role intent from `.agents/roles/`, "
                "and callable procedures from `.agents/skills/`. Preserve canonical sources; "
                "regenerate only registered native provider outputs. "
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
                "target-relative links, and `## Related Documents` section. The Stop hook runs "
                "`python3 scripts/validation/run-ci-gate.py --profile changed` to enforce the "
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

# Evaluate the canonical hook rules. Their frontmatter is the machine part and
# their body is the message; before this they were enforced by nothing.
denials = []
try:
    rules_module = project / "scripts" / "hooks" / "hook_rules.py"
    sys.path.insert(0, str(rules_module.parent))
    import hook_rules

    command = tool_input.get("command") if tool_name in {"", "Bash"} else ""
    command = command if isinstance(command, str) else ""
    warnings, blocks = hook_rules.evaluate(
        hook_rules.load_rules(project), command=command, edits=tuple(edits)
    )
    system_messages.extend(rule.message for rule in warnings)
    denials.extend(blocks)
except Exception:
    deny_policy_failure(
        "Repository hook policy could not be loaded or evaluated; resolve the "
        "policy configuration before retrying."
    )

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
  then
    return 0
  fi
  return 2
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

stop_retry_active() {
  HOOK_INPUT="$INPUT" python3 - <<'PY'
import json
import os

try:
    payload = json.loads(os.environ.get("HOOK_INPUT", "") or "{}")
except (TypeError, ValueError):
    payload = {}
raise SystemExit(0 if isinstance(payload, dict) and payload.get("stop_hook_active") is True else 1)
PY
}

emit_stop_block() {
  local reason="$1"
  local retry="${2:-0}"
  STOP_RETRY="$retry" python3 3<<<"$reason" <<'PY'
import json
import os

reason = os.fdopen(3, encoding="utf-8").read().removesuffix("\n")
retry = os.environ.get("STOP_RETRY") == "1"
if retry:
    reason = f"Stop retry limit reached. {reason}"
if retry:
    print(json.dumps({"continue": False, "stopReason": reason}))
elif os.environ.get("HY_HOME_HOOK_PROVIDER") == "codex":
    print(json.dumps({"decision": "block", "reason": reason}))
else:
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "systemMessage": reason,
    }))
PY
}

changed_profile_stop_gate() {
  local output result
  if ! command -v timeout >/dev/null 2>&1; then
    emit_stop_block "The changed validation profile could not start because the bounded timeout command is unavailable. Manually run \`python3 scripts/validation/run-ci-gate.py --profile changed\` and continue the task."
    return 1
  fi
  if output="$(timeout --kill-after=5s 540s python3 scripts/validation/run-ci-gate.py --profile changed 2>&1)"; then
    return 0
  else
    result=$?
  fi

  local reason
  if [[ "$result" -eq 124 || "$result" -eq 137 ]]; then
    reason="The changed validation profile timed out or was incomplete after its 540-second hook budget. Manually run \`python3 scripts/validation/run-ci-gate.py --profile changed\`, inspect the complete result, and continue the task."
  else
    reason="Changed repository state does not satisfy the changed validation profile. Continue the task, fix the reported contract failure, and manually rerun \`python3 scripts/validation/run-ci-gate.py --profile changed\`."
  fi
  if [[ -n "$output" ]]; then
    reason="$reason

Validator output:
${output: -6000}"
  fi
  emit_stop_block "$reason"
  return 1
}

logical_commit_stop_gate() {
  if [[ "${AGENT_ALLOW_UNCOMMITTED_STOP:-}" == "1" ]]; then
    return 0
  fi

  local output git_status="$1"
  if ! output="$(
    python3 3<<<"$git_status" <<'PY'
from __future__ import annotations

import os
import pathlib
import subprocess

REGISTRY = ".agents/governance/approval-boundaries.md"
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
for line in os.fdopen(3, encoding="utf-8").read().splitlines():
    if not line.strip():
        continue
    if len(line) < 4 or line[2] != " ":
        raise SystemExit(2)
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    if path in exempt:
        continue
    paths.append(path)

display_limit = 6000
notice = "\n[additional changed-path bytes omitted]"
payload = "\n".join(paths[:80]).encode("utf-8")
if len(payload) > display_limit:
    prefix_limit = display_limit - len(notice.encode("utf-8"))
    display = payload[:prefix_limit].decode("utf-8", errors="ignore") + notice
else:
    display = payload.decode("utf-8")
print(display)
PY
  )"; then
    emit_stop_block "Git status could not be parsed, so repository cleanliness and completion cannot be proven. Resolve the malformed status output, manually run \`python3 scripts/validation/run-ci-gate.py --profile changed\`, and continue the task."
    return 1
  fi

  if [[ -z "$output" ]]; then
    return 0
  fi

  local reason
  reason="$(
    python3 3<<<"$output" <<'PY'
import os
paths = os.fdopen(3, encoding="utf-8").read().removesuffix("\n")
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
print(reason)
PY
  )"
  emit_stop_block "$reason"
  return 1
}

stop() {
  if stop_retry_active; then
    emit_stop_block "Automatic Stop validation already ran for this stop interaction. Manually run \`python3 scripts/validation/run-ci-gate.py --profile changed\` after any fix, record the result, and request a new stop interaction." 1
    return 0
  fi

  local git_status
  if ! git_status="$(git status --porcelain=v1 --untracked-files=normal 2>/dev/null)"; then
    emit_stop_block "Git status could not be inspected, so repository cleanliness and completion cannot be proven. Resolve the Git error, manually run \`python3 scripts/validation/run-ci-gate.py --profile changed\`, and continue the task."
    return 0
  fi

  if [[ -n "$git_status" ]] && ! changed_profile_stop_gate; then
    return 0
  fi
  if logical_commit_stop_gate "$git_status"; then
    session_end
  fi
  return 0
}

user_prompt_submit() {
  HOOK_INPUT="$INPUT" python3 - "$PROJECT_DIR" <<'PY'
import json
import os
import pathlib
import sys

project = sys.argv[1]
raw = os.environ.get("HOOK_INPUT", "")

try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

prompt = str(data.get("prompt", "")).lower()

# Routing owns keywords only. The skill id derives the canonical path and the
# skill's own `description` is the routing summary, so a route cannot drift from
# the procedure it points at and a new skill needs one keyword line, not a copy
# of its identity.
ROUTES = {
    "adr-writing": [
        "adr", "architecture decision record", "decision record",
        "alternatives considered", "write a decision",
    ],
    "change-review-execution": [
        "change review", "diff review", "review this diff", "commit range",
        "specification compliance", "independent verdict",
    ],
    "ci-cd-patterns": [
        "ci gate", "ci/cd", "github actions", "workflow contract",
        "required check", "pipeline gate", "least-privilege job",
    ],
    "code-review-dimensions": [
        "code review", "review dimensions", "review checklist",
        "maintainability review",
    ],
    "compose-stack-agent": [
        "healthcheck", "health check", "restart policy",
        "qw-001", "qw-002", "qw-003", "qw-004", "qw-005", "quickwin",
        "compose stack", "infra tier",
    ],
    "container-threat-modeling": [
        "threat model", "trust boundary", "attack surface",
        "container security", "exploit path",
    ],
    "deployment-pipeline-design": [
        "deployment pipeline", "release pipeline", "rollout", "canary",
        "blue-green", "artifact promotion", "approval gate",
    ],
    "docker-compose-patterns": [
        "docker compose", "compose pattern", "compose topology",
        "service topology", "compose profile",
    ],
    "e2e-testing": [
        "e2e", "end-to-end", "end to end", "acceptance scenario",
        "smoke test", "user journey",
    ],
    "execution-plan-agent": [
        "execution plan", "spec to plan", "stage 03",
        "03.specs", "plan template", "implementation plan",
    ],
    "incident-response": [
        "incident", "outage", "postmortem", "post-mortem", "escalation",
        "service degradation",
    ],
    "infra-cross-validate": [
        "cross validate", "cross-validate", "infra review",
        "infrastructure review", "cross-file review",
    ],
    "infra-validate": [
        "infra validate", "infrastructure validation", "compose validate",
        "static infrastructure check", "runtime observation",
    ],
    "knowledge-map-agent": [
        "graphify", "knowledge graph", "traceability gap", "orphaned doc",
        "cross-document", "missing link", "knowledge map",
    ],
    "ops-runbook-agent": [
        "runbook", "stage 05", "05.operations", "backup procedure",
        "recovery procedure", "incident runbook", "ops runbook",
    ],
    "policy-gate-agent": [
        "policy gate", "validation suite", "public gate",
        "changed profile", "full profile",
        "policy validation",
    ],
    "provider-model-evaluation": [
        "provider registry", "provider evaluation", "model selection",
        "model evaluation", "llm provider", "native schema",
    ],
    "requirements-to-design-agent": [
        "prd", "ard", "requirements to design", "architecture decision",
        "stage 01", "stage 02", "01.requirements", "02.architecture", "adr",
    ],
    "security-audit": [
        "security audit", "vulnerability", "secret scan", "hardcoded secret",
        "privilege escalation", "exposed input",
    ],
    "style-validation": [
        "pre-commit", "precommit", "markdownlint", "yamllint", "shellcheck",
        "lint", "formatting", "style check", "document metadata",
    ],
    "task-breakdown-agent": [
        "task breakdown", "task evidence", "plan to task",
        "effort estimation", "execution task", "task template",
    ],
    "test-authoring": [
        "red test", "failing test", "regression test", "write a test",
        "test first", "tdd", "witnessed test",
    ],
    "workspace-audit-revalidation": [
        "revalidate", "revalidation", "stale audit", "audit refresh",
        "workspace audit",
    ],
}


def canonical_summary(skill_id):
    """Read the matched skill's own description.

    Routing summarises nothing itself: an unreadable or description-less skill
    routes with its path alone rather than with a guess that could drift.
    """
    path = pathlib.Path(project) / ".agents/skills" / skill_id / "SKILL.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    seen_opening_fence = False
    for line in text.splitlines():
        if line.strip() == "---":
            if seen_opening_fence:
                break
            seen_opening_fence = True
            continue
        if line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value.startswith('"'):
                try:
                    return json.loads(value)
                except ValueError:
                    return value.strip('"')
            return value
    return ""


matched = [
    skill_id
    for skill_id, keywords in ROUTES.items()
    if any(keyword in prompt for keyword in keywords)
]

if not matched:
    sys.exit(0)

lines = ["Canonical agent function routes that may apply to this prompt:"]
for skill_id in matched:
    entry = f"  - **{skill_id}** (`.agents/skills/{skill_id}/SKILL.md`)"
    summary = canonical_summary(skill_id)
    lines.append(f"{entry}: {summary}" if summary else entry)

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
