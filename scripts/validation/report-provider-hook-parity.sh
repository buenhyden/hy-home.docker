#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
mode="write"
mode_seen=0
root_seen=0
usage='Usage: bash scripts/validation/report-provider-hook-parity.sh [--check|--dry-run|--validate-only] [--root PATH]'
while [[ "$#" -gt 0 ]]; do
  case "$1" in
  --check | --dry-run | --validate-only)
    if [[ "$mode_seen" -eq 1 ]]; then
      printf '%s\n' "$usage" >&2
      exit 2
    fi
    mode="${1#--}"
    mode_seen=1
    ;;
  --root)
    if [[ "$root_seen" -eq 1 || "$#" -lt 2 || -z "$2" ]]; then
      printf '%s\n' "$usage" >&2
      exit 2
    fi
    ROOT="$2"
    root_seen=1
    shift
    ;;
  -h | --help)
    printf '%s\n' "$usage"
    exit 0
    ;;
  *)
    printf '%s\n' "$usage" >&2
    exit 2
    ;;
  esac
  shift
done

python3 - "$ROOT" "$mode" <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import stat
import sys

import yaml


root = pathlib.Path(sys.argv[1]).absolute()
mode = sys.argv[2]
registry_path = root / "docs/00.agent-governance/providers/registry.yaml"
output = root / "docs/90.references/data/0072-provider-hook-parity-matrix/README.md"
provider_ids = ("claude", "codex")
events = (
    ("session-start", "SessionStart", "SessionStart"),
    ("user-prompt-intake", "UserPromptSubmit", "UserPromptSubmit"),
    ("pre-tool", "PreToolUse", "PreToolUse"),
    ("post-tool", "PostToolUse", "PostToolUse"),
    ("stop", "Stop", "Stop"),
    ("pre-compaction", "PreCompact", "PreCompact"),
    ("session-end", "SessionEnd", None),
)
expected_native_events = {
    "claude": tuple(item[1] for item in events),
    "codex": tuple(item[2] for item in events if item[2] is not None),
}
expected_commands = {
    "claude": {
        "SessionStart": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"',
        "PreToolUse": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/docker-compose-pre.sh"',
        "PostToolUse": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-validate.sh"',
        "Stop": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/stop.sh"',
        "SessionEnd": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh"',
        "PreCompact": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-compact.sh"',
        "UserPromptSubmit": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/user-prompt-submit.sh"',
    },
    "codex": {
        event: (
            'HY_HOME_HOOK_PROVIDER=codex bash '
            '"${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/'
            f'agent-event-hook.sh" {event}'
        )
        for event in expected_native_events["codex"]
    },
}
expected_state_ids = (
    "discover",
    "design/plan",
    "approval",
    "implement",
    "validate",
    "independent-review",
    "evidence",
    "handoff",
)
state_keys = {
    "state_id",
    "owner_agent",
    "required_inputs",
    "mutation_authority",
    "entry_condition",
    "exit_gate",
    "max_attempts",
    "failure_return",
    "evidence_fields",
    "handoff_target",
}
loop_keys = {
    "owner_agent",
    "reviewer_agent",
    "permission_profile",
    "workflow_states",
    "max_attempts",
    "stop_condition",
    "on_failure",
}
expected_loops = {
    "context-bootstrap": (
        "workflow-supervisor", "rules-engineer", "read-only", ("discover",), 1,
        "bootstrap-contract-pass", "escalate",
    ),
    "bounded-implementation": (
        "qa-engineer", "code-reviewer", "workspace-write", ("implement", "validate"), 2,
        "focused-checks-pass", "narrow-then-escalate",
    ),
    "independent-review": (
        "code-reviewer", "eval-engineer", "read-only", ("independent-review", "evidence"), 2,
        "critical-and-important-zero", "escalate",
    ),
    "approved-all-files-gate": (
        "qa-engineer", "code-reviewer", "workspace-write", ("validate", "evidence"), 1,
        "controlled-wrapper-pass", "record-and-stop",
    ),
}
expected_layers = (
    ("canonical-contract", "rules-engineer", "canonical-authority", "design-plan"),
    ("role-skill-routing", "workflow-supervisor", "registered-routing", "discover"),
    ("permission-boundary", "rules-engineer", "explicit-authority", "approval"),
    ("provider-model-policy", "eval-engineer", "native-schema-compatibility", "design-plan"),
    ("semantic-events", "hook-developer", "native-event-honesty", "implement"),
    ("controlled-validation", "qa-engineer", "deterministic-checks", "implement"),
    ("tracked-ci", "ci-cd-engineer", "least-privilege-workflow", "implement"),
    ("sanitized-evidence", "eval-engineer", "value-free-evidence", "evidence"),
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


class _UniqueLoader(yaml.SafeLoader):
    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[object, object]:
        result: dict[object, object] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                fail("provider registry contains a non-string or duplicate key")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def load_yaml(path: pathlib.Path) -> dict[str, object]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        fail(f"cannot load provider registry: {error}")
    if not isinstance(value, dict):
        fail("provider registry must be a mapping")
    return value


def load_json(path: pathlib.Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"cannot load JSON config {path.relative_to(root)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object: {path.relative_to(root)}")
    return value


registry = load_yaml(registry_path)
role_ids: set[str] = set()
for role_path in sorted((root / "docs/00.agent-governance/roles").glob("*.md")):
    try:
        role_text = role_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        fail(f"cannot load canonical role {role_path}: {error}")
    match = re.match(r"\A---\n(.*?)\n---\n", role_text, flags=re.DOTALL)
    if match is None:
        fail(f"canonical role frontmatter missing: {role_path.name}")
    try:
        frontmatter = yaml.load(match.group(1), Loader=_UniqueLoader)
    except yaml.YAMLError as error:
        fail(f"canonical role frontmatter invalid: {role_path.name}: {error}")
    agent_id = frontmatter.get("agent_id") if isinstance(frontmatter, dict) else None
    if isinstance(agent_id, str):
        role_ids.add(agent_id)
if len(role_ids) != 14:
    fail("canonical role inventory differs")
providers = registry.get("providers")
if not isinstance(providers, list) or tuple(
    item.get("provider_id") if isinstance(item, dict) else None for item in providers
) != provider_ids:
    fail("provider registry must contain exactly claude and codex")

semantic_events = registry.get("semantic_events")
contracts = registry.get("hook_contracts")
if not isinstance(semantic_events, dict) or set(semantic_events) != set(provider_ids):
    fail("semantic event providers differ")
if not isinstance(contracts, dict) or set(contracts) != set(provider_ids):
    fail("hook contract providers differ")

configs = {
    "claude": load_json(root / ".claude/settings.json"),
    "codex": load_json(root / ".codex/hooks.json"),
}
for provider in provider_ids:
    registered_events = semantic_events.get(provider)
    provider_contracts = contracts.get(provider)
    native_hooks = configs[provider].get("hooks")
    if (
        not isinstance(registered_events, list)
        or set(registered_events) != set(expected_native_events[provider])
        or len(registered_events) != len(expected_native_events[provider])
        or not isinstance(provider_contracts, dict)
        or tuple(provider_contracts) != tuple(registered_events)
        or not isinstance(native_hooks, dict)
        or set(native_hooks) != set(registered_events)
    ):
        fail(f"event binding differs for {provider}")
    for event in registered_events:
        contract = provider_contracts.get(event)
        entries = native_hooks.get(event)
        if not isinstance(contract, dict) or set(contract) != {
            "command",
            "timeout",
            "matcher",
            "executable",
        }:
            fail(f"hook contract shape differs for {provider}/{event}")
        if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
            fail(f"native hook multiplicity differs for {provider}/{event}")
        entry = entries[0]
        expected_entry_keys = {"hooks"} | ({"matcher"} if contract["matcher"] is not None else set())
        if set(entry) != expected_entry_keys or entry.get("matcher") != contract["matcher"]:
            fail(f"native matcher differs for {provider}/{event}")
        hooks = entry.get("hooks")
        if not isinstance(hooks, list) or len(hooks) != 1 or not isinstance(hooks[0], dict):
            fail(f"native dispatcher multiplicity differs for {provider}/{event}")
        hook = hooks[0]
        if contract.get("command") != expected_commands[provider].get(event):
            fail(f"immutable command template differs for {provider}/{event}")
        if set(hook) != {"type", "command", "timeout"} or hook != {
            "type": "command",
            "command": contract["command"],
            "timeout": contract["timeout"],
        }:
            fail(f"native command or timeout differs for {provider}/{event}")
        executable_value = contract.get("executable")
        if not isinstance(executable_value, str):
            fail(f"executable path missing for {provider}/{event}")
        executable_path = pathlib.PurePosixPath(executable_value)
        if executable_path.is_absolute() or ".." in executable_path.parts:
            fail(f"unsafe executable path for {provider}/{event}")
        executable = root / executable_path
        try:
            metadata = executable.lstat()
            wrapper = executable.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            fail(f"unreadable executable for {provider}/{event}: {error}")
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o111 == 0:
            fail(f"executable mode differs for {provider}/{event}")
        if executable_value not in str(contract["command"]):
            fail(f"command does not bind registered executable for {provider}/{event}")
        if provider == "claude":
            expected_dispatch = f'exec bash "$PROJECT_DIR/scripts/hooks/agent-event-hook.sh" {event}'
            if expected_dispatch not in wrapper:
                fail(f"Claude wrapper dispatch differs for {event}")
        elif not str(contract["command"]).endswith(f" {event}"):
            fail(f"Codex dispatcher event differs for {event}")

states = registry.get("workflow_states")
if not isinstance(states, list) or tuple(
    item.get("state_id") if isinstance(item, dict) else None for item in states
) != expected_state_ids:
    fail("workflow state identities or order differ")
for state in states:
    if not isinstance(state, dict) or set(state) != state_keys:
        fail("workflow state shape differs")
    if (
        not isinstance(state["max_attempts"], int)
        or not 1 <= state["max_attempts"] <= 2
        or not isinstance(state["required_inputs"], list)
        or not state["required_inputs"]
        or state["evidence_fields"] != registry.get("evidence_fields")
    ):
        fail(f"workflow state fields differ for {state.get('state_id')}")
    if state["owner_agent"] not in role_ids:
        fail(f"workflow state owner differs for {state.get('state_id')}")
    if state["mutation_authority"] not in registry.get("permissions", {}):
        fail(f"workflow mutation authority differs for {state.get('state_id')}")
    if state["failure_return"] not in {*expected_state_ids, "stop"}:
        fail(f"workflow failure return differs for {state.get('state_id')}")
    if state["handoff_target"] not in {*expected_state_ids, "complete"}:
        fail(f"workflow handoff target differs for {state.get('state_id')}")

layers = registry.get("harness_layers")
if not isinstance(layers, list) or len(layers) != len(expected_layers):
    fail("harness layer identities differ")
actual_layers = []
for layer in layers:
    if not isinstance(layer, dict) or set(layer) != {
        "layer_id", "owner_agent", "gate", "failure_return"
    }:
        fail("harness layer shape differs")
    values = tuple(
        layer.get(field)
        for field in ("layer_id", "owner_agent", "gate", "failure_return")
    )
    if any(not isinstance(value, str) or not value for value in values):
        fail("harness layer values must be non-empty strings")
    if layer["owner_agent"] not in role_ids:
        fail(f"harness layer owner differs for {layer.get('layer_id')}")
    actual_layers.append(values)
if tuple(actual_layers) != expected_layers:
    fail("harness layer values differ")

loops = registry.get("harness_loops")
if not isinstance(loops, dict) or set(loops) != set(expected_loops):
    fail("harness loop identities differ")
for loop_id, expected_values in expected_loops.items():
    loop = loops.get(loop_id)
    if (
        not isinstance(loop, dict)
        or set(loop) != loop_keys
        or loop.get("owner_agent") not in role_ids
        or loop.get("reviewer_agent") not in role_ids
        or not isinstance(loop.get("max_attempts"), int)
        or not 1 <= loop["max_attempts"] <= 2
        or loop.get("permission_profile") not in {"read-only", "workspace-write"}
        or not isinstance(loop.get("stop_condition"), str)
        or not loop["stop_condition"]
        or not isinstance(loop.get("on_failure"), str)
        or not loop["on_failure"]
    ):
        fail(f"harness loop differs for {loop_id}")
    actual_values = (
        loop["owner_agent"],
        loop["reviewer_agent"],
        loop["permission_profile"],
        tuple(loop["workflow_states"]),
        loop["max_attempts"],
        loop["stop_condition"],
        loop["on_failure"],
    )
    if actual_values != expected_values:
        fail(f"harness loop values differ for {loop_id}")

rows = [
    (
        semantic_id,
        claude_event,
        "configured",
        codex_event or "N/A",
        "configured" if codex_event is not None else "unsupported",
    )
    for semantic_id, claude_event, codex_event in events
]
lines = [
    "---",
    "status: active",
    "observed_at: 2026-08-21",
    "generated_by: scripts/validation/report-provider-hook-parity.sh",
    "---",
    "",
    "# Provider Hook Parity Matrix",
    "",
    "## Overview",
    "",
    "Generated comparison of tracked Claude and Codex semantic-event adoption.",
    "Configured entries prove repository adoption, not observed live execution.",
    "",
    "## Purpose",
    "",
    "Expose deterministic provider-event configuration parity without claiming live execution.",
    "",
    "## Repository Role",
    "",
    "This generated Stage 90 datum supports validation and cannot override Stage 00 policy.",
    "",
    "## Scope",
    "",
    "Tracked Claude and Codex event configuration only; runtime observation is out of scope.",
    "",
    "## Definitions / Facts",
    "",
    "Configured means a tracked native hook entry exists; unsupported means no native mapping is registered.",
    "",
    "## Data",
    "",
    "| Semantic Event | Claude | Status | Codex | Status |",
    "| --- | --- | --- | --- | --- |",
]
lines.extend(
    f"| `{semantic}` | `{claude_event}` | `{claude_status}` | `{codex_event}` | `{codex_status}` |"
    for semantic, claude_event, claude_status, codex_event, codex_status in rows
)
lines.extend(
    [
        "",
        "## Sources",
        "",
        "- `docs/00.agent-governance/providers/registry.yaml`",
        "- `.claude/settings.json`",
        "- `.codex/hooks.json`",
        "",
        "## Maintenance",
        "",
        "Regenerate after provider registry or native hook configuration changes.",
        "",
        "## Related Documents",
        "",
        "- [Provider capability matrix](../../../../00.agent-governance/policies/provider-capability-matrix.md)",
        "- [Provider registry](../../../../00.agent-governance/providers/registry.yaml)",
        "",
    ]
)
content = "\n".join(lines)
if mode == "dry-run":
    print(content, end="")
elif mode == "check":
    try:
        current = output.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        current = None
    if current != content:
        fail(f"stale generated provider hook parity matrix: {output.relative_to(root)}")
    print(f"PASS: generated provider hook parity matrix is fresh: {output.relative_to(root)}")
elif mode == "write":
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"Generated {output.relative_to(root)} providers=2 events={len(rows)}")
elif mode == "validate-only":
    print("PASS: provider hook parity dispatchers=13 loops=4 workflow_states=8")
else:
    fail(f"unsupported mode: {mode}")
PY
