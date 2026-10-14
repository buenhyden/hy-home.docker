"""Evaluate the canonical hook rules against one tool-use payload.

The rule files under `.agents/governance/hooks/` are not prose:
their frontmatter is the machine part (`name`, `enabled`, `event`, `action`, and
either a flat `pattern` or a list of `conditions`) and the body is the message a
rule shows when it fires. Until now nothing read them, so every rule declared
`enabled: true` while being enforced by neither the shared dispatcher nor any
external tool. This module is the reader, so the files that state the rules are
also the files that run them.

Frontmatter is parsed here rather than with PyYAML on purpose. This runs inside
`agent-event-hook.sh` on every tool call, and a hook that dies on a missing
import would break every call; the accepted schema is small enough to read
directly. Invalid configured rules raise an error so the dispatcher can deny
the tool call instead of silently dropping policy.

`event: stop` rules are deliberately not evaluated. Both carry `pattern: .*`,
which is a placeholder rather than a condition — evaluating
`require-logical-commits-before-stop` generically would block every stop. Their
real conditions are contextual and already live in the dispatcher's
`logical_commit_stop_gate`.

A push whose refspec is implicit (`git push`, `git push origin`) cannot be
judged from the command text: `implicit_main_push` resolves it against the
repository the command runs in.
"""

from __future__ import annotations

import json
import pathlib
import re
import shlex
import subprocess
from dataclasses import dataclass

RULES_DIRECTORY = ".agents/governance/hooks"
EVALUATED_EVENTS = frozenset({"bash", "file"})
CONDITION_FIELDS = frozenset({"file_path", "new_text"})
MAX_RULE_BYTES = 64 * 1024


class RuleConfigurationError(RuntimeError):
    """The configured rule source cannot be loaded safely."""


@dataclass(frozen=True)
class Rule:
    """One rule, with its conditions compiled and its message ready to print."""

    name: str
    event: str
    action: str
    conditions: tuple[tuple[str, re.Pattern[str]], ...]
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
        if path.is_symlink() or not path.is_file():
            raise RuleConfigurationError(
                f"hook rule is not a regular file: {path.name}"
            )
        if path.stat().st_size > MAX_RULE_BYTES:
            raise RuleConfigurationError(f"hook rule exceeds byte limit: {path.name}")
        text = path.read_text(encoding="utf-8")
    except RuleConfigurationError:
        raise
    except (OSError, UnicodeError) as error:
        raise RuleConfigurationError(f"hook rule is unreadable: {path.name}") from error

    lines, body = _split_frontmatter(text)
    if not lines:
        raise RuleConfigurationError(f"hook rule has invalid frontmatter: {path.name}")

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
            conditions[-1][_unquote(key)] = _unquote(value)
            continue
        if in_conditions and line.startswith("  ") and conditions:
            key, _, value = line.strip().partition(":")
            conditions[-1][_unquote(key)] = _unquote(value)
            continue
        if line.startswith(" "):
            continue
        in_conditions = False
        key, _, value = line.partition(":")
        scalars[_unquote(key)] = _unquote(value)

    enabled = scalars.get("enabled", "").lower()
    if enabled not in {"true", "false"}:
        raise RuleConfigurationError(
            f"hook rule has invalid enabled value: {path.name}"
        )
    if enabled == "false":
        return None
    event = scalars.get("event", "")
    action = scalars.get("action", "")
    name = scalars.get("name", "")
    if not name or action not in {"warn", "block"}:
        raise RuleConfigurationError(
            f"hook rule has invalid identity or action: {path.name}"
        )
    if event == "stop":
        return None
    if event not in EVALUATED_EVENTS:
        raise RuleConfigurationError(f"hook rule has invalid event: {path.name}")

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
            raise RuleConfigurationError(f"hook rule has invalid operator: {path.name}")
        if event == "file" and field not in CONDITION_FIELDS:
            raise RuleConfigurationError(f"hook rule has invalid field: {path.name}")
        if event == "bash" and field != "command":
            raise RuleConfigurationError(f"hook rule has invalid field: {path.name}")
        try:
            compiled.append((field, re.compile(condition.get("pattern", ""))))
        except re.error as error:
            raise RuleConfigurationError(
                f"hook rule has invalid regex: {path.name}"
            ) from error
    if not compiled:
        raise RuleConfigurationError(
            f"hook rule has no evaluable condition: {path.name}"
        )

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
    if directory.is_symlink() or not directory.is_dir():
        raise RuleConfigurationError(
            "configured hook policy directory is missing or invalid"
        )
    try:
        paths = sorted(directory.glob("hookify.*.md"))
    except OSError as error:
        raise RuleConfigurationError(
            "configured hook policy directory is unreadable"
        ) from error
    if not paths:
        raise RuleConfigurationError(
            "configured hook policy directory contains no rules"
        )
    rules = [rule for path in paths if (rule := _parse_rule(path)) is not None]
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


IMPLICIT_MAIN_PUSH = Rule(
    name="block-direct-main-push",
    event="bash",
    action="block",
    conditions=(),
    message=(
        "Direct push to `main` blocked (project rule): this `git push` targets "
        "`main` through the current branch or its push target. Push a feature "
        "branch with an explicit refspec (`git push origin "
        "HEAD:refs/heads/<branch>`) and open a pull request."
    ),
)
_SEPARATORS = re.compile(r"&&|\|\||[;&|\n]")
_VALUE_OPTIONS = frozenset(
    {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
)


def _git(directory: pathlib.Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(directory), *arguments],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _targets_main(refspec: str) -> bool:
    destination = refspec.lstrip("+").rpartition(":")[2] or refspec.lstrip("+")
    return destination in {"main", "refs/heads/main"}


def implicit_main_push(command: str, cwd: pathlib.Path) -> bool:
    """Return whether any `git push` in `command` would update `main`.

    Explicit refspecs are judged by text; an implicit one by the branch and
    push target of the directory the push runs in (`cd` and `git -C` honoured).
    """

    # ponytail: splits on shell separators without quote awareness; a separator
    # inside a quoted argument only makes the check stricter.
    directory = cwd
    for segment in _SEPARATORS.split(command):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            continue
        if not tokens:
            continue
        if tokens[0] == "cd" and len(tokens) > 1:
            directory = directory / pathlib.Path(tokens[1]).expanduser()
            continue
        if tokens[0] != "git":
            continue
        here = directory
        index = 1
        while index < len(tokens) and tokens[index].startswith("-"):
            if tokens[index] == "-C" and index + 1 < len(tokens):
                here = here / tokens[index + 1]
                index += 2
            elif tokens[index] == "-c":
                index += 2
            else:
                index += 1
        if index >= len(tokens) or tokens[index] != "push":
            continue
        positional = []
        rest = tokens[index + 1 :]
        skip = False
        for token in rest:
            if skip:
                skip = False
            elif token in {"--all", "--mirror"}:
                return True
            elif token in _VALUE_OPTIONS:
                skip = True
            elif not token.startswith("-"):
                positional.append(token)
        if any(_targets_main(refspec) for refspec in positional[1:]):
            return True
        if len(positional) <= 1:
            if _git(here, "rev-parse", "--abbrev-ref", "HEAD") == "main":
                return True
            target = _git(
                here, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{push}"
            )
            if target.endswith("/main"):
                return True
    return False
