#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/governance/provider-hook-parity-matrix.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/report-provider-hook-parity.sh [--check|--dry-run]

Generate the provider-native hook parity matrix.

Options:
  --check    Fail when the generated matrix is stale.
  --dry-run  Print the generated matrix to stdout without writing it.
  -h, --help Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "") ;;
  --check) mode="check" ;;
  --dry-run) mode="dry-run" ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

python3 - "$mode" "$OUTPUT" <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import stat
import sys

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])

CONFIGS = {
    "claude": pathlib.Path(".claude/settings.json"),
    "codex": pathlib.Path(".codex/hooks.json"),
    "gemini": pathlib.Path(".gemini/settings.json"),
}
DISPATCHER = pathlib.Path("scripts/hooks/agent-event-hook.sh")
GEMINI_WRAPPER = pathlib.Path(".gemini/hooks/agent-event-hook.sh")

# Semantic ID, purpose, Claude event, Codex event, Gemini event.
EVENTS: list[tuple[str, str, str, str | None, str]] = [
    ("session-start", "Session/bootstrap guard", "SessionStart", "SessionStart", "SessionStart"),
    ("user-prompt-intake", "Prompt intake and routing guard", "UserPromptSubmit", "UserPromptSubmit", "BeforeAgent"),
    ("pre-tool", "Pre-mutation guard", "PreToolUse", "PreToolUse", "BeforeTool"),
    ("post-tool", "Post-edit validation guard", "PostToolUse", "PostToolUse", "AfterTool"),
    ("stop", "Completion gate", "Stop", "Stop", "AfterAgent"),
    ("pre-compaction", "Context handoff guard", "PreCompact", "PreCompact", "PreCompress"),
    ("session-end", "Session closure guard", "SessionEnd", None, "SessionEnd"),
]

GEMINI_SEMANTIC_EVENTS = {
    "AfterTool": "PostToolUse",
    "PreCompress": "PreCompact",
    "BeforeTool": "PreToolUse",
    "SessionEnd": "SessionEnd",
    "SessionStart": "SessionStart",
    "AfterAgent": "Stop",
    "BeforeAgent": "UserPromptSubmit",
}


def read_text(path: pathlib.Path) -> str:
    if not path.is_file():
        raise SystemExit(f"FAIL: missing required provider hook source: {path}")
    return path.read_text(errors="ignore")


def read_json(path: pathlib.Path) -> dict[str, object]:
    try:
        value = json.loads(read_text(path))
    except Exception as error:  # noqa: BLE001
        raise SystemExit(f"FAIL: invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit(f"FAIL: {path} must contain a JSON object")
    return value


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def extract_event(config: dict[str, object], event: str | None) -> dict[str, object]:
    if event is None:
        return {"present": False, "matcher": "", "commands": [], "timeouts": []}
    hooks = config.get("hooks", {})
    entries = hooks.get(event, []) if isinstance(hooks, dict) else []
    if not isinstance(entries, list) or not entries:
        return {"present": False, "matcher": "", "commands": [], "timeouts": []}
    matchers: list[str] = []
    commands: list[str] = []
    timeouts: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("matcher"):
            matchers.append(str(entry["matcher"]))
        handlers = entry.get("hooks", [])
        if not isinstance(handlers, list):
            continue
        for handler in handlers:
            if not isinstance(handler, dict):
                continue
            if handler.get("command"):
                commands.append(str(handler["command"]))
            if handler.get("timeout") is not None:
                timeouts.append(str(handler["timeout"]))
    return {
        "present": bool(commands),
        "matcher": ", ".join(matchers),
        "commands": commands,
        "timeouts": timeouts,
    }


def claude_status(native_event: str, data: dict[str, object]) -> tuple[str, str]:
    commands = [str(item) for item in data["commands"]]
    if not data["present"]:
        return "missing", "No configured Claude command"
    wrappers: list[pathlib.Path] = []
    for command in commands:
        match = re.search(r"(\.claude/hooks/[A-Za-z0-9_.-]+\.sh)", command)
        if not match:
            return "partial", "Command does not select a Claude wrapper"
        wrappers.append(pathlib.Path(match.group(1)))
    for wrapper in wrappers:
        text = read_text(wrapper)
        if "scripts/hooks/agent-event-hook.sh" not in text or native_event not in text:
            return "partial", f"{wrapper} does not delegate {native_event}"
        if stat.S_IMODE(wrapper.stat().st_mode) != 0o755:
            return "partial", f"{wrapper} is not mode 0755"
    return "native-wrapper", "Generated executable wrapper delegates to the shared dispatcher"


def codex_status(native_event: str | None, data: dict[str, object]) -> tuple[str, str]:
    if native_event is None:
        return "unsupported", "Codex has no native SessionEnd event in this contract"
    commands = [str(item) for item in data["commands"]]
    if not data["present"]:
        return "missing", "No configured Codex command"
    if any("scripts/hooks/agent-event-hook.sh" not in item or native_event not in item for item in commands):
        return "partial", "Command does not dispatch the expected native event"
    return "native-dispatch", "Quoted project-root command delegates to the shared dispatcher"


def gemini_status(native_event: str, data: dict[str, object]) -> tuple[str, str]:
    commands = [str(item) for item in data["commands"]]
    if not data["present"]:
        return "missing", "No configured Gemini command"
    if any(".gemini/hooks/agent-event-hook.sh" not in item or native_event not in item for item in commands):
        return "partial", "Command does not dispatch through the Gemini adapter"
    text = read_text(GEMINI_WRAPPER)
    semantic = GEMINI_SEMANTIC_EVENTS[native_event]
    if native_event not in text or semantic not in text or "scripts/hooks/agent-event-hook.sh" not in text:
        return "partial", "Gemini adapter does not map the expected semantic event"
    if stat.S_IMODE(GEMINI_WRAPPER.stat().st_mode) != 0o755:
        return "partial", "Gemini adapter is not mode 0755"
    note = "Native event adapter delegates to the shared dispatcher"
    if native_event == "AfterAgent":
        note += " with deny/retry-capable semantics"
    if native_event == "PreCompress":
        note += " as provider-inherent asynchronous advisory behavior"
    return "native-adapter", note


configs = {provider: read_json(path) for provider, path in CONFIGS.items()}
rows: list[dict[str, object]] = []
for semantic_id, purpose, claude_event, codex_event, gemini_event in EVENTS:
    claude = extract_event(configs["claude"], claude_event)
    codex = extract_event(configs["codex"], codex_event)
    gemini = extract_event(configs["gemini"], gemini_event)
    c_status, c_note = claude_status(claude_event, claude)
    x_status, x_note = codex_status(codex_event, codex)
    g_status, g_note = gemini_status(gemini_event, gemini)
    rows.append(
        {
            "semantic_id": semantic_id,
            "purpose": purpose,
            "claude_event": claude_event,
            "claude": claude,
            "claude_status": c_status,
            "claude_note": c_note,
            "codex_event": codex_event or "unsupported",
            "codex": codex,
            "codex_status": x_status,
            "codex_note": x_note,
            "gemini_event": gemini_event,
            "gemini": gemini,
            "gemini_status": g_status,
            "gemini_note": g_note,
        }
    )


def command_summary(data: object, unit: str) -> str:
    if not isinstance(data, dict):
        return "N/A"
    commands = [str(item) for item in data.get("commands", [])]
    timeouts = [str(item) for item in data.get("timeouts", [])]
    if not commands:
        return "N/A"
    result: list[str] = []
    for index, command in enumerate(commands):
        timeout = timeouts[index] if index < len(timeouts) else ""
        suffix = f" timeout={timeout}{unit}" if timeout else ""
        result.append(f"`{command}`{suffix}")
    return "<br>".join(result)


lines = [
    "---",
    "status: active",
    "generated_by: scripts/validation/report-provider-hook-parity.sh",
    "---",
    "",
    "<!-- Target: docs/90.references/data/governance/provider-hook-parity-matrix.md -->",
    "",
    "# Reference: Provider Hook Parity Matrix",
    "",
    "## Overview",
    "",
    "This generated reference compares semantic lifecycle coverage across the tracked Claude, Codex, and Gemini native surfaces.",
    "",
    "## Purpose",
    "",
    "Make event-name, timeout-unit, matcher, delegation, and unsupported-event differences reviewable without claiming false name parity.",
    "",
    "## Repository Role",
    "",
    "Generated audit context only. Stage 00 owns policy and `scripts/hooks/agent-event-hook.sh` owns shared behavior.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Tracked provider-native hook configuration and generated wrappers.",
    "- Semantic event mapping, timeout units, matchers, and delegation.",
    "",
    "### Out of Scope",
    "",
    "- Live provider execution, user-global settings, telemetry, logs, credentials, or runtime acceptance.",
    "",
    "## Definitions / Facts",
    "",
    "- **native-wrapper**: a Claude native event calls an executable generated wrapper.",
    "- **native-dispatch**: a Codex native event calls the shared dispatcher directly.",
    "- **native-adapter**: a Gemini native event passes through the one admitted event-name adapter.",
    "- **unsupported**: the provider does not expose the semantic event; it is not counted as parity.",
    "",
    "## Snapshot Summary",
    "",
    "| Metric | Value |",
    "| --- | ---: |",
    f"| Semantic events tracked | {len(rows)} |",
    f"| Claude native wrapper events | {sum(row['claude_status'] == 'native-wrapper' for row in rows)} |",
    f"| Codex native dispatch events | {sum(row['codex_status'] == 'native-dispatch' for row in rows)} |",
    f"| Codex unsupported events | {sum(row['codex_status'] == 'unsupported' for row in rows)} |",
    f"| Gemini native adapter events | {sum(row['gemini_status'] == 'native-adapter' for row in rows)} |",
    f"| Shared dispatcher present | {'yes' if DISPATCHER.is_file() else 'no'} |",
    "",
    "## Provider Hook Parity Matrix",
    "",
    "| Semantic Event | Purpose | Claude | Codex | Gemini |",
    "| --- | --- | --- | --- | --- |",
]
for row in rows:
    lines.append(
        "| `{semantic_id}` | {purpose} | `{claude_event}` / `{claude_status}` - {claude_note} | `{codex_event}` / `{codex_status}` - {codex_note} | `{gemini_event}` / `{gemini_status}` - {gemini_note} |".format(
            **{key: markdown_escape(value) for key, value in row.items() if not isinstance(value, dict)}
        )
    )

lines.extend(
    [
        "",
        "## Command Provenance",
        "",
        "| Semantic Event | Claude Matcher / Command (seconds) | Codex Matcher / Command (seconds) | Gemini Matcher / Command (milliseconds) |",
        "| --- | --- | --- | --- |",
    ]
)
for row in rows:
    lines.append(
        "| `{}` | {}<br>{} | {}<br>{} | {}<br>{} |".format(
            markdown_escape(row["semantic_id"]),
            markdown_escape(row["claude"].get("matcher") or "N/A"),
            markdown_escape(command_summary(row["claude"], "s")),
            markdown_escape(row["codex"].get("matcher") or "N/A"),
            markdown_escape(command_summary(row["codex"], "s")),
            markdown_escape(row["gemini"].get("matcher") or "N/A"),
            markdown_escape(command_summary(row["gemini"], "ms")),
        )
    )

lines.extend(
    [
        "",
        "## Source Rules",
        "",
        "- Regenerate after provider config, wrapper, semantic-event contract, or dispatcher changes.",
        "- Preserve provider-native names and units; do not add ignored matchers or unsupported config keys.",
        "- Tracked adoption does not prove provider entitlement or live runtime acceptance.",
        "",
        "## Sources",
        "",
        "- [Claude settings](../../../../.claude/settings.json)",
        "- [Codex hooks](../../../../.codex/hooks.json)",
        "- [Gemini settings](../../../../.gemini/settings.json)",
        "- [Gemini native event adapter](../../../../.gemini/hooks/agent-event-hook.sh)",
        "- [Provider semantic contract](../../../00.agent-governance/contracts/provider-models.yaml)",
        "- [Provider-neutral dispatcher](../../../../scripts/hooks/agent-event-hook.sh)",
        "",
        "## Maintenance",
        "",
        "- **Owner**: Hook Developer.",
        "- **Mandatory Reviewers**: Rules Engineer and Security Auditor.",
        "- **Update Trigger**: Any tracked provider event or adapter change.",
        "",
        "## Related Documents",
        "",
        "- **Governance data index**: [README.md](./README.md)",
        "- **Provider capability matrix**: [../../../00.agent-governance/rules/provider-capability-matrix.md](../../../00.agent-governance/rules/provider-capability-matrix.md)",
        "- **Provider hook parity spec**: [../../../03.specs/115-provider-hook-parity-matrix/spec.md](../../../03.specs/115-provider-hook-parity-matrix/spec.md)",
    ]
)

content = "\n".join(lines) + "\n"
if MODE == "dry-run":
    print(content, end="")
elif MODE == "check":
    if not OUTPUT.is_file() or OUTPUT.read_text(errors="ignore") != content:
        print(f"FAIL: stale generated provider hook parity matrix: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/validation/report-provider-hook-parity.sh", file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: generated provider hook parity matrix is fresh: {OUTPUT}")
elif MODE == "write":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(
        f"Generated {OUTPUT} with events={len(rows)}; "
        f"claude_native={sum(row['claude_status'] == 'native-wrapper' for row in rows)}; "
        f"codex_native={sum(row['codex_status'] == 'native-dispatch' for row in rows)}; "
        f"gemini_native={sum(row['gemini_status'] == 'native-adapter' for row in rows)}"
    )
else:
    raise SystemExit(f"FAIL: unsupported mode: {MODE}")
PY
