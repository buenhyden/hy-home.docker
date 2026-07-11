#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/governance/provider-hook-parity-matrix.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/report-provider-hook-parity.sh [--check|--dry-run]

Generate the provider hook parity matrix and Gemini behavioral reminder checklist.

Options:
  --check    Fail when the generated matrix is stale.
  --dry-run  Print the generated matrix to stdout without writing it.
  -h, --help Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  --dry-run)
    mode="dry-run"
    ;;
  -h|--help)
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
import sys

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])

CLAUDE_CONFIG = pathlib.Path(".claude/settings.json")
CODEX_CONFIG = pathlib.Path(".codex/hooks.json")
GEMINI_PROVIDER_NOTES = pathlib.Path("docs/00.agent-governance/providers/gemini.md")
PROVIDER_MATRIX = pathlib.Path("docs/00.agent-governance/rules/provider-capability-matrix.md")
AGENTS_README = pathlib.Path(".agents/README.md")
DISPATCHER = pathlib.Path("scripts/hooks/agent-event-hook.sh")

EVENTS: list[tuple[str, str]] = [
    ("SessionStart", "Session/bootstrap guard"),
    ("UserPromptSubmit", "Prompt intake and routing guard"),
    ("PreToolUse", "Pre-mutation guard"),
    ("PostToolUse", "Post-edit validation guard"),
    ("Stop", "Completion gate"),
    ("PreCompact", "Context handoff guard"),
    ("SessionEnd", "Session closure guard"),
]

GEMINI_REMINDERS: dict[str, str] = {
    "SessionStart": "Load `AGENTS.md`, provider notes, bootstrap, persona, checklist, one scope, and progress memory before repository mutation.",
    "UserPromptSubmit": "Classify task scope, resolve risky ambiguity, and route to the canonical stage before editing.",
    "PreToolUse": "Review requirements, guardrails, protected surfaces, and template-first rules before mutating files.",
    "PostToolUse": "Run relevant style, docs, generated-output, and repository contract checks after edits.",
    "Stop": "Confirm completion checklist, logical commit discipline, progress memory, and residual gaps before declaring completion.",
    "PreCompact": "Record durable progress and handoff context before compaction or context transition.",
    "SessionEnd": "Update progress evidence and leave the worktree/validation state explicit at session closure.",
}


def read_text(path: pathlib.Path) -> str:
    if not path.is_file():
        raise SystemExit(f"FAIL: missing required provider hook source: {path}")
    return path.read_text(errors="ignore")


def read_json(path: pathlib.Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"FAIL: invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"FAIL: {path} must contain a JSON object")
    return data


def markdown_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def extract_event(config: dict, event: str) -> dict[str, object]:
    hooks = config.get("hooks", {})
    entries = hooks.get(event, []) if isinstance(hooks, dict) else []
    if not isinstance(entries, list) or not entries:
        return {"event_present": False, "matcher": "", "commands": [], "timeouts": []}

    matchers: list[str] = []
    commands: list[str] = []
    timeouts: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        matcher = entry.get("matcher", "")
        if matcher:
            matchers.append(str(matcher))
        for hook in entry.get("hooks", []):
            if not isinstance(hook, dict):
                continue
            command = hook.get("command", "")
            timeout = hook.get("timeout", "")
            if command:
                commands.append(str(command))
            if timeout != "":
                timeouts.append(str(timeout))

    return {
        "event_present": bool(commands),
        "matcher": ", ".join(matchers),
        "commands": commands,
        "timeouts": timeouts,
    }


def claude_wrapper_for(command: str) -> pathlib.Path | None:
    match = re.search(r"(\.claude/hooks/[A-Za-z0-9_.-]+\.sh)", command)
    if not match:
        return None
    return pathlib.Path(match.group(1))


def claude_status(event: str, event_data: dict[str, object]) -> tuple[str, str]:
    commands = [str(item) for item in event_data.get("commands", [])]
    if not event_data.get("event_present") or not commands:
        return "missing", "No configured Claude hook command"
    wrappers = [claude_wrapper_for(command) for command in commands]
    if any(wrapper is None for wrapper in wrappers):
        return "partial", "Configured command does not point to `.claude/hooks/*.sh`"
    missing = [str(wrapper) for wrapper in wrappers if wrapper and not wrapper.is_file()]
    if missing:
        return "missing", "Missing wrapper: " + ", ".join(missing)
    delegate_failures: list[str] = []
    for wrapper in wrappers:
        assert wrapper is not None
        text = read_text(wrapper)
        if "scripts/hooks/agent-event-hook.sh" not in text or event not in text:
            delegate_failures.append(str(wrapper))
    if delegate_failures:
        return "partial", "Wrapper does not delegate expected event: " + ", ".join(delegate_failures)
    return "native-wrapper", "Configured native hook wrapper delegates to provider-neutral dispatcher"


def codex_status(event: str, event_data: dict[str, object]) -> tuple[str, str]:
    commands = [str(item) for item in event_data.get("commands", [])]
    if not event_data.get("event_present") or not commands:
        return "missing", "No configured Codex hook command"
    bad = [
        command
        for command in commands
        if "scripts/hooks/agent-event-hook.sh" not in command or event not in command
    ]
    if bad:
        return "partial", "Configured command does not dispatch the expected event"
    return "native-dispatch", "Configured hook dispatches through provider-neutral event hook"


def ensure_literal(path: pathlib.Path, literal: str) -> bool:
    return literal in read_text(path)


claude_config = read_json(CLAUDE_CONFIG)
codex_config = read_json(CODEX_CONFIG)
gemini_notes = read_text(GEMINI_PROVIDER_NOTES)
matrix_text = read_text(PROVIDER_MATRIX)
agents_readme = read_text(AGENTS_README)

required_gemini_literals = [
    "Hook Parity Contract",
    "behavioral contracts",
    "Pre-edit validation",
    "Post-edit validation",
    "Template-first guidance",
    "Commit discipline",
]
missing_gemini_literals = [
    literal for literal in required_gemini_literals if literal not in gemini_notes
]

matrix_hooks_declared = "no tracked `.gemini` adapter" in matrix_text
agents_rules_declared = "rules/" in agents_readme and "workflows/" in agents_readme
dispatcher_present = DISPATCHER.is_file()

rows: list[dict[str, object]] = []
for event, purpose in EVENTS:
    claude_event = extract_event(claude_config, event)
    codex_event = extract_event(codex_config, event)
    c_status, c_note = claude_status(event, claude_event)
    x_status, x_note = codex_status(event, codex_event)
    gemini_status = "behavioral-reminder"
    gemini_note = GEMINI_REMINDERS[event]
    if missing_gemini_literals or not matrix_hooks_declared or not agents_rules_declared:
        gemini_status = "needs-contract-review"
        problems = missing_gemini_literals[:]
        if not matrix_hooks_declared:
            problems.append("provider matrix lacks the no-tracked-Gemini-adapter hook contract")
        if not agents_rules_declared:
            problems.append(".agents README lacks rules/workflows reminder")
        gemini_note = "Contract review required: " + "; ".join(problems)
    rows.append(
        {
            "event": event,
            "purpose": purpose,
            "claude_status": c_status,
            "claude_note": c_note,
            "claude_matcher": claude_event.get("matcher", ""),
            "claude_commands": claude_event.get("commands", []),
            "claude_timeouts": claude_event.get("timeouts", []),
            "codex_status": x_status,
            "codex_note": x_note,
            "codex_matcher": codex_event.get("matcher", ""),
            "codex_commands": codex_event.get("commands", []),
            "codex_timeouts": codex_event.get("timeouts", []),
            "gemini_status": gemini_status,
            "gemini_note": gemini_note,
        }
    )

claude_native = sum(1 for row in rows if row["claude_status"] == "native-wrapper")
codex_native = sum(1 for row in rows if row["codex_status"] == "native-dispatch")
gemini_behavioral = sum(1 for row in rows if row["gemini_status"] == "behavioral-reminder")
events_total = len(EVENTS)


def command_summary(commands: object, timeouts: object) -> str:
    command_list = [str(item) for item in commands] if isinstance(commands, list) else []
    timeout_list = [str(item) for item in timeouts] if isinstance(timeouts, list) else []
    if not command_list:
        return "N/A"
    chunks: list[str] = []
    for index, command in enumerate(command_list):
        timeout = timeout_list[index] if index < len(timeout_list) else ""
        suffix = f" timeout={timeout}s" if timeout else ""
        chunks.append(f"`{command}`{suffix}")
    return "<br>".join(chunks)


lines: list[str] = [
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
    "This generated reference compares the repository's Claude, Codex, and Gemini",
    "hook surfaces. Claude and Codex expose programmatic hook configuration;",
    "Gemini is represented as a behavioral reminder checklist because the Stage 00",
    "provider capability matrix treats Gemini hooks as a non-native capability.",
    "",
    "## Purpose",
    "",
    "The matrix helps reviewers inspect provider hook parity without manually",
    "opening every hook config, wrapper script, and provider note.",
    "",
    "## Repository Role",
    "",
    "Use this document as generated audit context only. Active provider policy",
    "remains in `docs/00.agent-governance/`, and executable hook behavior remains",
    "in `.claude/`, `.codex/`, `.agents/`, and `scripts/hooks/`.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Tracked `.claude/settings.json` hook configuration.",
    "- Tracked `.codex/hooks.json` hook configuration.",
    "- Claude wrapper delegation to `scripts/hooks/agent-event-hook.sh`.",
    "- Codex provider-neutral hook dispatch commands.",
    "- Gemini behavioral checklist derived from Stage 00 provider notes.",
    "",
    "### Out of Scope",
    "",
    "- Personal settings such as `.claude/settings.local.json`.",
    "- Live provider runtime state, telemetry, shell history, or raw hook logs.",
    "- New native Gemini hook claims beyond the current Stage 00 contract.",
    "- Mutating provider configuration, model policy, secrets, credentials, or remote state.",
    "",
    "## Definitions / Facts",
    "",
    "- **native-wrapper**: Claude event is configured and delegates through a tracked wrapper script.",
    "- **native-dispatch**: Codex event is configured and dispatches directly through `scripts/hooks/agent-event-hook.sh`.",
    "- **behavioral-reminder**: Gemini has no tracked native hook event and must manually follow the shared hook contract.",
    "- **needs-contract-review**: A required Stage 00 Gemini behavioral contract literal is missing.",
    "",
    "## Snapshot Summary",
    "",
    "| Metric | Value |",
    "| --- | ---: |",
    f"| Hook events tracked | {events_total} |",
    f"| Claude native wrapper events | {claude_native} |",
    f"| Codex native dispatch events | {codex_native} |",
    f"| Gemini behavioral reminder events | {gemini_behavioral} |",
    f"| Provider-neutral dispatcher present | {'yes' if dispatcher_present else 'no'} |",
    f"| Gemini contract literals missing | {len(missing_gemini_literals)} |",
    "",
    "## Provider Hook Parity Matrix",
    "",
    "| Event | Purpose | Claude | Codex | Gemini |",
    "| --- | --- | --- | --- | --- |",
]

for row in rows:
    lines.append(
        "| `{event}` | {purpose} | `{claude_status}` - {claude_note} | `{codex_status}` - {codex_note} | `{gemini_status}` - {gemini_note} |".format(
            event=markdown_escape(row["event"]),
            purpose=markdown_escape(row["purpose"]),
            claude_status=markdown_escape(row["claude_status"]),
            claude_note=markdown_escape(row["claude_note"]),
            codex_status=markdown_escape(row["codex_status"]),
            codex_note=markdown_escape(row["codex_note"]),
            gemini_status=markdown_escape(row["gemini_status"]),
            gemini_note=markdown_escape(row["gemini_note"]),
        )
    )

lines.extend(
    [
        "",
        "## Command Provenance",
        "",
        "| Event | Claude Matcher | Claude Command | Codex Matcher | Codex Command |",
        "| --- | --- | --- | --- | --- |",
    ]
)
for row in rows:
    lines.append(
        "| `{event}` | {claude_matcher} | {claude_command} | {codex_matcher} | {codex_command} |".format(
            event=markdown_escape(row["event"]),
            claude_matcher=markdown_escape(row["claude_matcher"] or "N/A"),
            claude_command=markdown_escape(command_summary(row["claude_commands"], row["claude_timeouts"])),
            codex_matcher=markdown_escape(row["codex_matcher"] or "N/A"),
            codex_command=markdown_escape(command_summary(row["codex_commands"], row["codex_timeouts"])),
        )
    )

lines.extend(
    [
        "",
        "## Gemini Behavioral Reminder Checklist",
        "",
        "| Event | Manual Reminder |",
        "| --- | --- |",
    ]
)
for event, _purpose in EVENTS:
    lines.append(f"| `{event}` | {markdown_escape(GEMINI_REMINDERS[event])} |")

lines.extend(
    [
        "",
        "## Source Rules",
        "",
        "- Regenerate this file after changing Claude/Codex hook configs, Claude hook",
        "  wrappers, Gemini provider notes, provider capability matrix rules, or",
        "  `.agents/` runtime guidance.",
        "- Treat Gemini rows as manual behavioral reminders until Stage 00 provider",
        "  governance is updated with verified native hook support.",
        "- Do not read personal settings, hook logs, shell history, credentials,",
        "  tokens, `.env` values, or live provider runtime state.",
        "",
        "## Sources",
        "",
        "- [Claude settings](../../../../.claude/settings.json) - tracked Claude hook configuration.",
        "- [Codex hooks](../../../../.codex/hooks.json) - tracked Codex hook configuration.",
        "- [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) - Gemini behavioral hook contract.",
        "- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - provider hook capability boundary.",
        "- [Gemini shared runtime README](../../../../.agents/README.md) - `.agents/` rules and workflows surface.",
        "- [Provider-neutral dispatcher](../../../../scripts/hooks/agent-event-hook.sh) - shared hook event implementation.",
        "",
        "## Maintenance",
        "",
        "- **Owner**: Agentic Workflow Specialist / QA Engineer.",
        "- **Review Cadence**: Review after provider hook, adapter, or provider-note changes.",
        "- **Update Trigger**: Run the generator after tracked provider hook surfaces change.",
        "",
        "## Related Documents",
        "",
        "- **Governance data index**: [README.md](./README.md)",
        "- **Provider semantic parity spec**: [../../../03.specs/107-provider-semantic-parity-validator/spec.md](../../../03.specs/107-provider-semantic-parity-validator/spec.md)",
        "- **Provider hook parity spec**: [../../../03.specs/115-provider-hook-parity-matrix/spec.md](../../../03.specs/115-provider-hook-parity-matrix/spec.md)",
        "- **Automation candidates**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)",
    ]
)

content = "\n".join(lines) + "\n"

if MODE == "dry-run":
    print(content, end="")
elif MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated provider hook parity matrix: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text(errors="ignore")
    if current != content:
        print(f"FAIL: stale generated provider hook parity matrix: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/validation/report-provider-hook-parity.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated provider hook parity matrix is fresh: {OUTPUT}")
elif MODE == "write":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(
        f"Generated {OUTPUT} with events={events_total}; "
        f"claude_native={claude_native}; codex_native={codex_native}; gemini_behavioral={gemini_behavioral}"
    )
else:
    print(f"FAIL: unsupported mode: {MODE}", file=sys.stderr)
    sys.exit(2)
PY
