#!/usr/bin/env bash
set -euo pipefail

ROOT=""
mode="check"
mode_seen=0
root_seen=0
usage='Usage: bash scripts/validation/report-provider-hook-parity.sh [--write|--check|--dry-run|--validate-only] [--root PATH]'
while [[ "$#" -gt 0 ]]; do
  case "$1" in
  --write | --check | --dry-run | --validate-only)
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

if [[ "$root_seen" -eq 0 ]]; then
  ROOT="$(git rev-parse --show-toplevel)"
fi

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
safe_repository_path_part = re.compile(r"\.?[A-Za-z0-9][A-Za-z0-9._-]*")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def semantic_id(event: str) -> str:
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", event).replace("_", "-")
    return words.casefold()


def expected_hook_command(
    provider: str, event: str, executable: pathlib.PurePosixPath
) -> str:
    if provider == "claude":
        return f'bash "$CLAUDE_PROJECT_DIR/{executable.as_posix()}"'
    return (
        "HY_HOME_HOOK_PROVIDER=codex bash "
        '"${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/'
        f'{executable.as_posix()}" {event}'
    )


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

event_order: list[str] = []
for provider in provider_ids:
    registered_events = semantic_events.get(provider)
    if (
        not isinstance(registered_events, list)
        or not registered_events
        or any(not isinstance(event, str) or not event for event in registered_events)
        or any(
            re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", event) is None
            for event in registered_events
        )
        or len(registered_events) != len(set(registered_events))
    ):
        fail(f"semantic event inventory differs for {provider}")
    for event in registered_events:
        if event not in event_order:
            event_order.append(event)

configs = {
    "claude": load_json(root / ".claude/settings.json"),
    "codex": load_json(root / ".codex/hooks.json"),
}
for provider in provider_ids:
    registered_events = semantic_events.get(provider)
    provider_contracts = contracts.get(provider)
    native_hooks = configs[provider].get("hooks")
    if (
        not isinstance(provider_contracts, dict)
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
        executable_value = contract.get("executable")
        if not isinstance(executable_value, str):
            fail(f"executable path missing for {provider}/{event}")
        executable_path = pathlib.PurePosixPath(executable_value)
        if (
            executable_path.is_absolute()
            or not executable_path.parts
            or any(part in {"", ".", ".."} for part in executable_path.parts)
            or any(
                safe_repository_path_part.fullmatch(part) is None
                for part in executable_path.parts
            )
        ):
            fail(f"unsafe executable path for {provider}/{event}")
        if contract.get("command") != expected_hook_command(
            provider, event, executable_path
        ):
            fail(f"registered command template differs for {provider}/{event}")
        if set(hook) != {"type", "command", "timeout"} or hook != {
            "type": "command",
            "command": contract["command"],
            "timeout": contract["timeout"],
        }:
            fail(f"native command or timeout differs for {provider}/{event}")
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

rows = [
    (
        semantic_id(event),
        event if event in semantic_events["claude"] else "N/A",
        "configured" if event in semantic_events["claude"] else "unsupported",
        event if event in semantic_events["codex"] else "N/A",
        "configured" if event in semantic_events["codex"] else "unsupported",
    )
    for event in event_order
]
lines = [
    "---",
    "title: Provider Hook Parity Matrix",
    "type: references/data",
    "layer: reference",
    "status: active",
    "owner: \"@buenhyden\"",
    "artifact_id: DATA-0072",
    "parent_ids: []",
    "created: '2026-08-21'",
    "updated: '2026-08-28'",
    "observed_at: '2026-08-21'",
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
        "- [Provider capability matrix](../../../00.agent-governance/policies/provider-capability-matrix.md)",
        "- [Provider registry](../../../00.agent-governance/providers/registry.yaml)",
        "",
        "## Schema",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
        "",
        "## Provenance",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
        "",
        "## Inventory",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
        "",
        "## Refresh",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
        "",
        "## Consumers",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
        "",
        "## Traceability",
        "",
        "This package preserves its existing data evidence under the Stage 99 `data` contract.",
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
    dispatchers = sum(len(semantic_events[provider]) for provider in provider_ids)
    print(f"PASS: provider hook parity providers=2 dispatchers={dispatchers}")
else:
    fail(f"unsupported mode: {mode}")
PY
