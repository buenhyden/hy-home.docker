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
_PUNCTUATION = ";&|()<>\n"
# A heredoc body is data unless its delimiter is unquoted; either way it is
# not judged (residual: an unquoted body's `$(...)` would run).
_HEREDOC = re.compile(
    r"<<-?[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_-]*)\1([^\n]*)\n(?:.*?\n)??[ \t]*\2[ \t]*(?=\n|$)",
    re.S,
)
_SUBSTITUTION = re.compile(r"\$\(((?:[^()]|\([^()]*\))*)\)|`([^`]*)`")
# Commands that run a string argument as a shell command.
_RUNNERS = frozenset({"bash", "sh", "zsh", "dash", "eval", "su", "watch", "script"})
# Global git options that take a separate value.
_GIT_VALUE_OPTIONS = frozenset(
    {
        "-C",
        "-c",
        "--git-dir",
        "--work-tree",
        "--namespace",
        "--super-prefix",
        "--attr-source",
        "--config-env",
    }
)
_VALUE_OPTIONS = frozenset(
    {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
)
_ALL_BRANCHES = frozenset({"--all", "--branches", "--mirror"})
_MAIN = frozenset({"main", "heads/main", "refs/heads/main"})
# Shell keywords and grouping words that may precede a command in a segment.
_KEYWORDS = frozenset(
    {"if", "then", "elif", "else", "do", "while", "until", "!", "{", "}", "time"}
)
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*")
_LOCATION_OPTIONS = ("--git-dir", "--work-tree")
_PUSH_CONFIG = re.compile(r"^(push\.|remote\..*\.(push|mirror)|alias\.)", re.I)
# `git`, its global options, then the `push` subcommand, anywhere in a segment.
_GIT_PUSH = re.compile(
    r"\bgit(?:\s+(?:-[Cc]|--git-dir|--work-tree|--namespace|--config-env)\s+[^-\s]\S*"
    r"|\s+-\S+)*\s+push\b"
)


class _Unknown(Exception):
    """A push whose destination cannot be determined from the command."""


def _git(directory: pathlib.Path, location: list[str], *arguments: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(directory), *location, *arguments],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _segments(command: str) -> list[object]:
    """Split a command into word lists, `(` and `)`, honouring quotes.

    Redirections and their targets are dropped. Unbalanced quotes raise
    ValueError.
    """

    lexer = shlex.shlex(command, posix=True, punctuation_chars=_PUNCTUATION)
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""  # comments are removed from the raw text first
    items: list[object] = []
    words: list[str] = []
    target = False
    for token in lexer:
        if not (token and set(token) <= set(_PUNCTUATION)):
            if target:
                target = False
            else:
                words.append(token)
            continue
        redirect = min((token.index(c) for c in "<>" if c in token), default=None)
        for character in token if redirect is None else token[:redirect]:
            if words:
                items.append(words)
                words = []
            if character in "()":
                items.append(character)
        if redirect is not None:
            if words and words[-1].isdigit():
                words.pop()
            target = True
    if words:
        items.append(words)
    return items


def _strip_comments(command: str) -> str:
    """Blank every shell comment: a `#` that starts a word outside quotes."""

    out = list(command)
    quote = ""
    index = 0
    while index < len(command):
        character = command[index]
        if quote == "'":
            quote = "" if character == "'" else quote
        elif character == "\\":
            index += 1
        elif quote == '"':
            quote = "" if character == '"' else quote
        elif character in "'\"":
            quote = character
        elif character == "#" and (index == 0 or command[index - 1] in " \t\n;&|()<>"):
            end = command.find("\n", index)
            end = len(command) if end < 0 else end
            out[index:end] = " " * (end - index)
            index = end
            continue
        index += 1
    return "".join(out)


def implicit_main_push(command: str, cwd: pathlib.Path) -> bool:
    """Return whether any `git push` in `command` could update `main`.

    Explicit refspecs are judged by text, `HEAD` and `@` by the current branch,
    and an implicit refspec by the branch, push target and push configuration
    of the repository the push runs in (`cd`, `pushd`/`popd`, subshells,
    `git -C`, `--git-dir`, `--work-tree`, `GIT_DIR` and `GIT_WORK_TREE`
    honoured). The check fails closed: a push whose destination it cannot
    determine counts as a push to `main`.
    """

    try:
        return _scan(command, cwd)
    except _Unknown:
        return True


def _scan(
    command: str, cwd: pathlib.Path | None, head_branch: str | None = None
) -> bool:
    # ponytail: a lexical approximation of the shell, not a parser. A push it
    # cannot resolve raises _Unknown (deny); text that only mentions a push in
    # an argument is data and is not judged.
    command = _strip_comments(
        _HEREDOC.sub(lambda match: f"<<{match.group(2)}{match.group(3)}", command)
    ).replace("\\\n", " ")
    try:
        items = _segments(command)
    except ValueError:
        if _GIT_PUSH.search(command):
            raise _Unknown from None
        return False
    # Command substitutions run wherever bash expands them, which excludes
    # single quotes and escaped characters.
    for inner in _live_substitutions(command):
        if _scan(inner, cwd, head_branch):
            return True
    directory = cwd
    subshells: list[pathlib.Path | None] = []
    pushed: list[pathlib.Path | None] = []
    for item in items:
        if item == "(":
            subshells.append(directory)
            continue
        if item == ")":
            directory = subshells.pop() if subshells else directory
            # A checkout is on-disk state; after a directory change it can no
            # longer be tied to the repository a later push runs in.
            head_branch = head_branch and "?"
            continue
        words = list(item)  # type: ignore[call-overload]
        location: list[str] = []
        while words and (words[0] in _KEYWORDS or _ASSIGNMENT.fullmatch(words[0])):
            _locate(words.pop(0), location)
        if not words:
            continue
        head = pathlib.PurePath(words[0]).name
        if head in {"cd", "pushd", "popd"}:
            head_branch = head_branch and "?"
        if head in {"cd", "pushd"} and len(words) > 1:
            if head == "pushd":
                pushed.append(directory)
            target = words[1]
            directory = (
                None
                if directory is None or any(c in target for c in "$`{")
                else directory / pathlib.Path(target).expanduser()
            )
            continue
        if head == "popd":
            directory = pushed.pop() if pushed else directory
            continue
        runner = next(
            (
                i
                for i, word in enumerate(words)
                if pathlib.PurePath(word).name in _RUNNERS
            ),
            None,
        )
        if runner is not None and not any(
            pathlib.PurePath(word).name == "git" for word in words[:runner]
        ):
            script = _runner_script(
                pathlib.PurePath(words[runner]).name, words[runner + 1 :]
            )
            if script is not None and _scan(script, directory, head_branch):
                return True
            continue
        for index, word in enumerate(words):
            if pathlib.PurePath(word).name != "git":
                continue
            here = list(location)
            for prefix in words[:index]:
                _locate(prefix, here)
            moved = _head_change(words[index:], directory, here)
            if moved is not None:
                head_branch = moved
                continue
            if _git_push_targets_main(words[index:], directory, here, head_branch):
                return True
    return False


def _live_substitutions(command: str) -> list[str]:
    """Return the bodies of `$(...)` and backticks that bash would run."""

    masked = list(command)
    quote = ""
    index = 0
    while index < len(command):
        character = command[index]
        if quote == "'":
            if character == "'":
                quote = ""
            masked[index] = " "
        elif character == "\\" and index + 1 < len(command):
            masked[index] = masked[index + 1] = " "
            index += 1
        elif character == "'" and not quote:
            quote = "'"
        elif character == '"':
            quote = "" if quote == '"' else '"'
        index += 1
    return [
        command[match.start(1) : match.end(1)]
        if match.group(1) is not None
        else command[match.start(2) : match.end(2)]
        for match in _SUBSTITUTION.finditer("".join(masked))
    ]


def _runner_script(head: str, arguments: list[str]) -> str | None:
    """Return the command string a runner executes, or None for a script file."""

    if head == "eval":
        return " ".join(arguments)
    if head == "watch":
        rest = list(arguments)
        while rest and rest[0].startswith("-"):
            option = rest.pop(0)
            if option in {"-n", "--interval", "-d", "--differences"} and rest:
                if option in {"-n", "--interval"}:
                    rest.pop(0)
        return " ".join(rest)
    for index, word in enumerate(arguments):
        if word.startswith("-") and not word.startswith("--") and "c" in word[1:]:
            return arguments[index + 1] if index + 1 < len(arguments) else ""
    return None


def _subcommand_index(tokens: list[str]) -> int:
    index = 1
    while index < len(tokens) and tokens[index].startswith("-"):
        index += 2 if tokens[index] in _GIT_VALUE_OPTIONS else 1
    return index


def _head_change(
    tokens: list[str], directory: pathlib.Path | None, location: list[str]
) -> str | None:
    """Return the branch a checkout or switch leaves HEAD on.

    `?` means HEAD moved somewhere this check cannot name; None means this git
    command does not move HEAD.
    """

    index = _subcommand_index(tokens)
    subcommand = tokens[index] if index < len(tokens) else ""
    arguments = tokens[index + 1 :]
    elsewhere = bool(location) or any(
        word in _GIT_VALUE_OPTIONS - {"-c", "--namespace", "--attr-source"}
        or word.startswith(("--git-dir=", "--work-tree="))
        for word in tokens[1:index]
    )
    if subcommand == "symbolic-ref" or (
        subcommand == "branch" and {"-m", "-M", "--move"} & set(arguments)
    ):
        return "?"
    if subcommand not in {"checkout", "switch"}:
        return None
    if subcommand == "checkout" and (
        ("--" in arguments and arguments.index("--") + 1 < len(arguments))
        or len([word for word in arguments if not word.startswith("-")]) > 1
    ):
        return None  # a pathspec checkout leaves HEAD where it is
    if elsewhere:
        return "?"
    for position, word in enumerate(arguments):
        if word in {"-b", "-B", "-c", "-C", "--orphan"}:
            return arguments[position + 1] if position + 1 < len(arguments) else "?"
    if "-" in arguments:
        return "?"
    before = arguments[: arguments.index("--")] if "--" in arguments else arguments
    names = [word for word in before if not word.startswith("-")]
    if not names:
        return None
    if subcommand == "switch" or names[0] in _MAIN:
        return "main" if names[0] in _MAIN else names[0]
    here = (directory or pathlib.Path("/")) / "."
    known = _git(
        here, location, "rev-parse", "--verify", "--quiet", f"refs/heads/{names[0]}"
    )
    return names[0] if known is not None else None


def _locate(word: str, location: list[str]) -> None:
    name, equals, value = word.partition("=")
    if not equals or not _ASSIGNMENT.fullmatch(word):
        return
    if name in {"GIT_DIR", "GIT_WORK_TREE"} and value:
        option = "--git-dir" if name == "GIT_DIR" else "--work-tree"
        location.append(f"{option}={value}")
    elif name.startswith("GIT_CONFIG"):
        location.append("--unknown-config")


def _git_push_targets_main(
    tokens: list[str],
    directory: pathlib.Path | None,
    location: list[str],
    head_branch: str | None = None,
) -> bool:
    here = directory or pathlib.Path("/")
    index = 1
    while index < len(tokens) and tokens[index].startswith("-"):
        option = tokens[index]
        value = tokens[index + 1] if index + 1 < len(tokens) else ""
        if option == "-C":
            here = here / value
            index += 2
        elif option == "-c":
            if _PUSH_CONFIG.match(value):
                raise _Unknown
            index += 2
        elif option.startswith("--config-env"):
            raise _Unknown
        elif option in _LOCATION_OPTIONS:
            location.append(f"{option}={value}")
            index += 2
        elif option.startswith(tuple(f"{name}=" for name in _LOCATION_OPTIONS)):
            location.append(option)
            index += 1
        elif option in {"--namespace", "--super-prefix", "--attr-source"}:
            index += 2
        else:
            index += 1
    subcommand = tokens[index] if index < len(tokens) else ""
    if subcommand in {"rebase", "submodule"} and any(
        _GIT_PUSH.search(token) or token == "push" for token in tokens[index + 1 :]
    ):
        raise _Unknown
    if subcommand != "push":
        return False
    if (
        directory is None
        or "--unknown-config" in location
        or any(c in token for token in tokens for c in "$`{")
    ):
        raise _Unknown
    positional = []
    skip = False
    for token in tokens[index + 1 :]:
        if skip:
            skip = False
        elif token in _ALL_BRANCHES or (
            len(token) > 2 and any(option.startswith(token) for option in _ALL_BRANCHES)
        ):
            return True
        elif token in _VALUE_OPTIONS:
            skip = True
        elif not token.startswith("-"):
            positional.append(token)
    remote, refspecs = (positional[0] if positional else ""), positional[1:]
    if not refspecs and "--tags" in tokens:
        return False
    if head_branch == "?" and (
        not refspecs
        or any(spec.lstrip("+").partition(":")[0] in {"HEAD", "@"} for spec in refspecs)
    ):
        raise _Unknown
    branch = head_branch or _git(here, location, "rev-parse", "--abbrev-ref", "HEAD")
    if branch is None:
        return True
    # Without a named remote any configured remote may be used.
    pattern = rf"^remote\.{re.escape(remote) if remote else '.*'}\.(push|mirror)$"
    settings = _git(here, location, "config", "--get-regexp", pattern) or ""
    for line in settings.splitlines():
        key, _, value = line.partition(" ")
        if (key.endswith(".mirror") and value == "true") or (
            key.endswith(".push")
            and (
                _MAIN & set(re.split(r"[:+]", value))
                or "*" in value
                or value.lstrip("+") == ":"
            )
        ):
            return True
    for refspec in refspecs:
        source, colon, destination = refspec.lstrip("+").partition(":")
        if not colon:
            destination = source
        if destination in {"HEAD", "@"}:
            destination = branch
        if "*" in refspec or destination in _MAIN:
            return True
    if refspecs:
        return False
    if branch == "main":
        return True
    default = _git(here, location, "config", "push.default")
    if default == "matching":
        return True
    if (
        default in {"upstream", "tracking"}
        and _git(here, location, "config", f"branch.{branch}.merge") in _MAIN
    ):
        return True
    target = _git(
        here,
        location,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{push}",
    )
    return target is not None and target.endswith("/main")
