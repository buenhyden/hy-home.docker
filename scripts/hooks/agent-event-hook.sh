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
containers = run(["docker", "ps", "--format", "{{.Names}}"], fallback="docker not running")
container_lines = [line for line in containers.splitlines() if line.strip() and line != "docker not running"]
infra_dir = project / "infra"
infra_entries = ", ".join(sorted(path.name for path in infra_dir.iterdir())) if infra_dir.is_dir() else "none"

message = f"""hy-home.docker project context

Git status:
- Branch: `{branch}`
- Changed files: `{changed_count}`
- Last commit: `{last_commit}`

Docker services:
- Running: {len(container_lines)}
- Services: {', '.join(container_lines) if container_lines else containers}

Infra layer:
{infra_entries}

Key rules:
- Use `AGENTS.md` and `docs/00.agent-governance/` as governance entry points.
- Treat Graphify as advisory when `scripts/knowledge/report-graphify-health.sh` reports contamination.
- Run `bash scripts/validation/validate-docker-compose.sh` before deployment-related completion.
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
    for path in paths:
        short_path = path
        project_prefix = str(project) + "/"
        if short_path.startswith(project_prefix):
            short_path = short_path[len(project_prefix):]
        if re.search(r"docker-compose.*\.ya?ml$", short_path):
            system_messages.append(
                "Docker Compose file edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "After editing, verify with `bash scripts/validation/validate-docker-compose.sh` "
                "and check port conflicts, volume paths, missing environment variables, "
                "and existing network names."
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
                ".agents compatibility surface edit detected.\n\n"
                f"Path: `{short_path}`\n\n"
                "Keep `.agents/` aligned with `docs/00.agent-governance/` and the "
                "canonical `.claude/` runtime catalog. It must not introduce a "
                "parallel policy source, unknown skills, or stale runtime paths. "
                "After editing, run `bash scripts/validation/check-repo-contracts.sh`."
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
                "Stop hooks run `bash scripts/validation/check-repo-contracts.sh` to enforce the "
                "changed-doc template gate."
            )
            break

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

msg = f"""Session ending — governance reminder:

- Update `docs/00.agent-governance/memory/progress.md` with a work log entry before this session closes.
- Record changed files, verification evidence, and any residual risk or open gap.

Current state:
- Branch: `{branch}`
- Last commit: `{last_commit}`"""

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
    pathlib.Path("docs/04.execution"),
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
  if output="$(bash scripts/validation/check-repo-contracts.sh 2>&1)"; then
    return 0
  fi

  GATE_OUTPUT="$output" python3 - <<'PY'
import json
import os

output = os.environ.get("GATE_OUTPUT", "").strip()
reason = (
    "Changed target-stage documentation does not satisfy the docs/99.templates "
    "contract. Continue the task, fix the document from the mapped template, "
    "and rerun `bash scripts/validation/check-repo-contracts.sh`."
)
if output:
    reason = f"{reason}\n\nValidator output:\n{output[-6000:]}"

print(json.dumps({
    "decision": "block",
    "reason": reason,
    "systemMessage": reason,
}))
PY
  return 1
}

stop() {
  if template_stop_gate; then
    session_end
  fi
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
- Active work is committed or stashed.
- `docs/00.agent-governance/memory/progress.md` reflects current progress.
- Any in-flight plan or decision is recorded in a memory note."""

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
  *)
    exit 0
    ;;
esac
