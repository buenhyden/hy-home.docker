"""Evaluate the Stage 00 hook rules against one tool-use payload.

The rule files under `docs/00.agent-governance/policies/hooks/` are not prose:
their frontmatter is the machine part (`name`, `enabled`, `event`, `action`, and
either a flat `pattern` or a list of `conditions`) and the body is the message a
rule shows when it fires. Until now nothing read them, so every rule declared
`enabled: true` while being enforced by neither the shared dispatcher nor any
external tool. This module is the reader, so the files that state the rules are
also the files that run them.

Frontmatter is parsed here rather than with PyYAML on purpose. This runs inside
`agent-event-hook.sh` on every tool call, and a hook that dies on a missing
import would break every call; the accepted schema is small enough to read
directly, and anything outside it is skipped rather than raised.

`event: stop` rules are deliberately not evaluated. Both carry `pattern: .*`,
which is a placeholder rather than a condition — evaluating
`require-logical-commits-before-stop` generically would block every stop. Their
real conditions are contextual and already live in the dispatcher's
`template_stop_gate` and `logical_commit_stop_gate`.
"""

from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass

RULES_DIRECTORY = "docs/00.agent-governance/policies/hooks"
EVALUATED_EVENTS = frozenset({"bash", "file"})
CONDITION_FIELDS = frozenset({"file_path", "new_text"})
MAX_RULE_BYTES = 64 * 1024


@dataclass(frozen=True)
class Rule:
    """One rule, with its conditions compiled and its message ready to print."""

    name: str
    event: str
    action: str
    conditions: tuple[tuple[str, "re.Pattern[str]"], ...]
    message: str


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
        return decoded if isinstance(decoded, str) else value
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def _split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        return [], ""
    end = text.find("\n---", 3)
    if end == -1:
        return [], ""
    return text[4:end].splitlines(), text[end + 4 :].lstrip("\n")


def _parse_rule(path: pathlib.Path) -> Rule | None:
    try:
        if path.stat().st_size > MAX_RULE_BYTES:
            return None
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None

    lines, body = _split_frontmatter(text)
    if not lines:
        return None

    scalars: dict[str, str] = {}
    conditions: list[dict[str, str]] = []
    in_conditions = False
    for line in lines:
        if not line.strip():
            continue
        if line == "conditions:":
            in_conditions = True
            continue
        if in_conditions and (line.startswith("- ") or line.startswith("  - ")):
            conditions.append({})
            item = line[2:] if line.startswith("- ") else line[4:]
            key, _, value = item.partition(":")
            conditions[-1][key.strip()] = _unquote(value)
            continue
        if in_conditions and line.startswith("  ") and conditions:
            key, _, value = line.strip().partition(":")
            conditions[-1][key.strip()] = _unquote(value)
            continue
        if line.startswith(" "):
            continue
        in_conditions = False
        key, _, value = line.partition(":")
        scalars[key.strip()] = _unquote(value)

    if scalars.get("enabled", "").lower() != "true":
        return None
    event = scalars.get("event", "")
    action = scalars.get("action", "")
    name = scalars.get("name", "")
    if event not in EVALUATED_EVENTS or action not in {"warn", "block"} or not name:
        return None

    if not conditions and "pattern" in scalars:
        conditions = [
            {
                "field": "command",
                "operator": "regex_match",
                "pattern": scalars["pattern"],
            }
        ]

    compiled: list[tuple[str, re.Pattern[str]]] = []
    for condition in conditions:
        field = condition.get("field", "")
        if condition.get("operator") != "regex_match":
            return None
        if event == "file" and field not in CONDITION_FIELDS:
            return None
        if event == "bash" and field != "command":
            return None
        try:
            compiled.append((field, re.compile(condition.get("pattern", ""))))
        except re.error:
            return None
    if not compiled:
        return None

    return Rule(
        name=name,
        event=event,
        action=action,
        conditions=tuple(compiled),
        message=body.strip(),
    )


def load_rules(root: pathlib.Path) -> tuple[Rule, ...]:
    """Return every enabled, evaluable rule, sorted by name."""

    directory = root / RULES_DIRECTORY
    if not directory.is_dir():
        return ()
    rules = [
        rule
        for path in sorted(directory.glob("*.md"))
        if (rule := _parse_rule(path)) is not None
    ]
    return tuple(sorted(rules, key=lambda item: item.name))


def _matches(rule: Rule, subjects: dict[str, str]) -> bool:
    # Conditions are ANDed: a two-condition file rule pairs a path filter with a
    # content filter, and both must hold before the rule fires.
    for field, pattern in rule.conditions:
        if pattern.search(subjects.get(field, "")) is None:
            return False
    return True


def evaluate(
    rules: tuple[Rule, ...],
    *,
    command: str = "",
    edits: tuple[tuple[str, str], ...] = (),
) -> tuple[tuple[Rule, ...], tuple[Rule, ...]]:
    """Return the (warning, blocking) rules this payload triggers, in name order."""

    fired: dict[str, Rule] = {}
    for rule in rules:
        if rule.event == "bash":
            if command and _matches(rule, {"command": command}):
                fired[rule.name] = rule
            continue
        for file_path, new_text in edits:
            if _matches(rule, {"file_path": file_path, "new_text": new_text}):
                fired[rule.name] = rule
                break

    warnings = tuple(rule for rule in fired.values() if rule.action == "warn")
    blocks = tuple(rule for rule in fired.values() if rule.action == "block")
    return warnings, blocks
