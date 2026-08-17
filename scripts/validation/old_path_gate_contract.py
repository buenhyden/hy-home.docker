#!/usr/bin/env python3
"""Validate Spec 137 pre-deletion gate 4.

Gate 4 requires zero clickable references to the retiring research pack across
all tracked text outside the retiring directory, and requires every permitted
non-link literal to appear in the reviewed allowlist the Stage 04 Task owns.

Scope limit, stated so this module is not read as more than it is. The Spec's
deterministic evidence set for gate 4 has four items; this module implements the
first, the literal scan. It does not run the repository contract check, the
implementation-alignment check, or the LLM Wiki freshness checks, and it has no
notion of the mandated pre-deletion and post-deletion double run. Passing here is
necessary, not sufficient.

Review-verdict limit. The settled-verdict predicate checks that a row states a
review happened. It cannot establish that a review actually happened, so it does
not detect the defect that motivated it, where a record was relabelled from
"review pending" to "Approved" without a covering review. It only removes the
easy form of that failure, a row that never claimed a verdict at all.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import html
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, field

SLUG = "2026-07-05-agentic-research-pack-refresh"
RETIRING_DIR = f"docs/90.references/research/{SLUG}"
TASK_PATH = "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
ALLOWLIST_HEADING = "### Old-path allowlist"

# Generated advisory navigation. Spec 137's generated-artifact inventory closes
# this surface separately and authorizes no refresh, so it is reported rather
# than allowlisted. Never silently dropped: the count is always printed, and
# clickable links are still reported inside it.
GENERATED_PREFIXES = ("graphify-out/",)

# Spec 137: current routers, generated navigation, mutable provider or
# configuration routes/exceptions, and canonical-owner statements have no
# allowlist. A row declaring one of these classes grants nothing.
FORBIDDEN_CLASSES = re.compile(
    r"(?i)\b(?:current router|generated navigation|mutable (?:provider|config)"
    r"|configuration route|canonical[- ]owner)\b"
)

_SLUG_BODY = re.escape(SLUG)
# A destination reaches the retiring directory when the slug is followed by a
# path separator or ends the destination. The earlier form required a trailing
# slash and therefore missed a direct link to the directory itself.
_DEST = rf"{_SLUG_BODY}(?:/|(?=[)>\"'\s\]?#&,;]|$))"

# Clickable forms. Each is matched against whole-file text so a destination
# split across lines is still seen, and against a percent-decoded, case-folded
# copy so encoding or case cannot hide a working link.
CLICKABLE_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("inline-link", re.compile(rf"\]\(\s*<?[^)\n]*{_DEST}", re.IGNORECASE)),
    # A destination may wrap onto the next line. Bounded to a single newline and
    # no blank line, so the pattern cannot span unrelated content and misreport
    # the offending line.
    (
        "multiline-link",
        re.compile(rf"\]\(\s*<?[^)\n]*\n?[^)\n]*{_DEST}", re.IGNORECASE),
    ),
    (
        "reference-definition",
        re.compile(rf"^\s*\[[^\]]+\]:\s*<?[^\s]*{_DEST}", re.IGNORECASE | re.M),
    ),
    (
        "html-attribute",
        re.compile(
            rf"(?:href|src)\s*=\s*(?:[\"'][^\"']*|[^\s>\"']*){_DEST}",
            re.IGNORECASE,
        ),
    ),
    ("autolink", re.compile(rf"<[^<>\s]*{_DEST}[^<>]*>", re.IGNORECASE)),
)

# A settled verdict states positively that a review happened. Requiring a
# positive marker rather than banning the word "pending" matters: several
# reviewed rows legitimately note that post-deletion lifecycle reconciliation is
# still pending, which is a future activity and not an open review. The bare word
# "pass" is deliberately absent: it occurs in ordinary prose and was load-bearing
# for no live row.
# Settling is checked negation-first. An earlier version let a `C0/I0` token
# short-circuit ahead of the negation guard, which settled "Not Run; C0/I0
# placeholder" and "quality Needs fixes C0/I2/M10" — the second being the exact
# cell text these rows were likeliest to receive next. Thirty of the thirty-four
# live rows settle through the token, so that ordering left the guard protecting
# four rows.
SETTLED_SEVERITY = re.compile(r"\bC0/I0\b")
SETTLED_MARKER = re.compile(r"(?i)\b(?:reviewed|approved)\b")
# Negation targets the review assertion, not any negative word. A blanket list
# demoted ordinary approved cells such as "Approved; no new findings" and
# "Approved; non-blocking Minors only".
# Two tiers, because these cells are narratives rather than structured verdicts.
# A terminal status describes the row's current state and always blocks. A
# historical negation describes a round that was later closed, so it blocks only
# when no settling marker follows it. Several reviewed rows legitimately narrate
# "quality Needs fixes ... then received both external C0/I0/M0 approvals", and a
# blanket rule demoted them.
TERMINAL_NEGATION = re.compile(
    r"(?i)(?:"
    r"\bnot\s+(?:yet\s+)?(?:been\s+)?(?:reviewed|approved|run)\b"
    r"|\bno\s+(?:independent\s+)?review\b"
    r"|\bnever\s+(?:reviewed|approved)\b"
    r"|\bun[-\s]?(?:reviewed|approved)\b"
    r"|\bpre[-\s]?reviewed\b"
    r"|\bself[-\s]?reviewed\s+only\b"
    r"|\bnobody\b"
    r"|\breview\s+pending\b|\bpending\s+review\b"
    r"|\brequested\b"
    r"|\b(?:to\s+be|will\s+be|scheduled\s+to\s+be)\s+(?:reviewed|approved)\b"
    r")"
)
HISTORICAL_NEGATION = re.compile(r"(?i)\b(?:needs?\s+fixes|rejected)\b")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    message: str


@dataclass(frozen=True)
class AllowRow:
    path: str
    anchors: tuple[str, ...]
    literal_class: str
    verdict: str
    settled: bool
    forbidden_class: bool


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    generated_occurrences: int = 0
    anchor_unbound: int = 0
    rows: dict[str, AllowRow] = field(default_factory=dict)


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def tracked_files(root: pathlib.Path) -> list[str]:
    return [line for line in _git(root, "ls-files").splitlines() if line]


def _cells(line: str) -> list[str]:
    """Split a Markdown table row on unescaped pipes."""
    parts = re.split(r"(?<!\\)\|", line)
    return [part.replace(r"\|", "|").strip() for part in parts]


def read_allowlist(root: pathlib.Path) -> dict[str, AllowRow]:
    """Parse the Task's allowlist, resolving columns by header name."""
    lines = (root / TASK_PATH).read_text(encoding="utf-8").split("\n")
    try:
        start = next(
            index
            for index, line in enumerate(lines)
            if line.startswith(ALLOWLIST_HEADING)
        )
    except StopIteration:
        return {}

    header: list[str] | None = None
    rows: dict[str, AllowRow] = {}
    for line in lines[start + 1 :]:
        # Any subsequent heading ends the table, including a deeper one.
        if re.match(r"^#{2,}\s", line):
            break
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        if header is None:
            lowered = [cell.lower() for cell in cells]
            if "path" in lowered and any("review" in cell for cell in lowered):
                header = lowered
            continue
        if set("".join(cells)) <= {"-", " ", ":"}:
            continue

        def pick(name: str) -> str:
            assert header is not None
            for index, column in enumerate(header):
                if name in column and index < len(cells):
                    return cells[index]
            return ""

        path = pick("path").strip("`")
        if not path:
            continue
        verdict = pick("review")
        anchors = tuple(re.findall(r"`([^`]+)`", pick("anchor")))
        literal_class = pick("class")
        rows[path] = AllowRow(
            path=path,
            anchors=anchors,
            literal_class=literal_class,
            verdict=verdict,
            settled=_is_settled(verdict),
            forbidden_class=bool(FORBIDDEN_CLASSES.search(literal_class)),
        )
    return rows


def _is_settled(verdict: str) -> bool:
    """True when the cell positively states a completed review.

    Negation is evaluated first and applies to both settling routes, including
    the structured severity token.
    """
    if TERMINAL_NEGATION.search(verdict):
        return False

    def settles(text: str) -> bool:
        return bool(SETTLED_SEVERITY.search(text) or SETTLED_MARKER.search(text))

    historical = [match.end() for match in HISTORICAL_NEGATION.finditer(verdict)]
    if historical:
        # Blocked unless the record shows the round was later closed.
        return settles(verdict[historical[-1] :])
    return settles(verdict)


def _normalize(text: str) -> str:
    """Percent-decode, resolve HTML entities, and case-fold.

    Newlines introduced by decoding are neutralized so a decoded `%0A` cannot
    shift line numbering. Line alignment is a correctness property here: the
    finding's line is evidence, and an earlier version counted newlines in the
    decoded copy while enumerating the original, which both lost findings and
    misattributed them.
    """
    decoded = html.unescape(urllib.parse.unquote(text))
    return decoded.replace("\r", " ").replace("\n", " ").casefold()


def _normalized_lines(text: str) -> list[str]:
    """Normalize per line, so indices match the original exactly."""
    return [_normalize(line) for line in text.split("\n")]


def _clickable_lines(text: str) -> dict[int, str]:
    """Return {original line number: form name} for clickable destinations."""
    lines = _normalized_lines(text)
    hits: dict[int, str] = {}
    for number, line in enumerate(lines, start=1):
        for name, pattern in CLICKABLE_FORMS:
            if name == "multiline-link":
                continue
            if pattern.search(line):
                hits.setdefault(number, name)
        # A destination may wrap onto the next line. A two-line window keeps
        # indices exact where a whole-file match could not.
        if number < len(lines):
            window = f"{line}\n{lines[number]}"
            if dict(CLICKABLE_FORMS)["multiline-link"].search(window):
                hits.setdefault(number, "multiline-link")
    return hits


_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def _anchor_text(anchor: str) -> str:
    """Declared anchors carry their `#` prefix; heading chains do not."""
    return anchor.lstrip("#").strip().lower()


def _headings_by_line(text: str, markdown: bool) -> dict[int, tuple[str, ...]]:
    """Map each line to its enclosing heading chain.

    The chain, not just the innermost heading: a row may declare a file-scope
    anchor such as `# Title` while the literal sits under a deeper heading, and
    an innermost-only model reports those as unbound. Non-Markdown files return
    empty chains, because a leading `#` there is a shebang or a comment.
    """
    mapping: dict[int, tuple[str, ...]] = {}
    chain: list[tuple[int, str]] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if markdown:
            match = _HEADING.match(line)
            if match:
                level = len(match.group(1))
                chain = [entry for entry in chain if entry[0] < level]
                chain.append((level, match.group(2).strip()))
        mapping[number] = tuple(title for _, title in chain)
    return mapping


def scan(root: pathlib.Path) -> ScanResult:
    """Run the gate-4 literal scan."""
    rows = read_allowlist(root)
    result = ScanResult(rows=rows)
    needle = _normalize(SLUG)

    for relative in tracked_files(root):
        if relative.startswith(f"{RETIRING_DIR}/"):
            continue
        absolute = root / relative
        if not absolute.is_file():
            continue
        try:
            text = absolute.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if needle not in _normalize(text):
            continue

        clickable = _clickable_lines(text)
        headings = _headings_by_line(text, relative.endswith(".md"))
        row = rows.get(relative)
        generated = relative.startswith(GENERATED_PREFIXES)

        for number, line in enumerate(text.split("\n"), start=1):
            normalized = _normalize(line)
            occurrences = normalized.count(needle)
            if not occurrences and number not in clickable:
                continue

            # Clickable links are evaluated first and independently of the
            # allowlist. Gate 4 admits no clickable-link exception, so no
            # allowlist row may suppress this finding.
            if number in clickable:
                result.findings.append(
                    Finding(
                        "OLD-PATH-CLICKABLE-LINK",
                        relative,
                        number,
                        f"clickable {clickable[number]} to the retiring pack; "
                        "gate 4 admits no clickable-link exception",
                    )
                )
                continue

            if generated:
                result.generated_occurrences += occurrences
                continue

            if row is None:
                result.findings.append(
                    Finding(
                        "OLD-PATH-UNALLOWLISTED",
                        relative,
                        number,
                        "non-link literal outside the reviewed allowlist",
                    )
                )
                continue
            if row.forbidden_class:
                result.findings.append(
                    Finding(
                        "OLD-PATH-FORBIDDEN-CLASS",
                        relative,
                        number,
                        f"allowlist class {row.literal_class!r} is denied an "
                        "allowlist by Spec 137",
                    )
                )
                continue
            if not row.settled:
                result.findings.append(
                    Finding(
                        "OLD-PATH-ALLOWLIST-UNREVIEWED",
                        relative,
                        number,
                        "allowlist row exists but its review verdict is not settled",
                    )
                )
                continue
            # Advisory only. The declared anchors of the pre-existing rows are
            # prose descriptors rather than machine-precise locators, so binding
            # the exemption to them would manufacture findings against reviewed
            # rows. The unbound count is reported instead of hidden.
            chain = " \n".join(headings[number]).lower()
            if row.anchors and not any(
                _anchor_text(anchor) in chain or _anchor_text(anchor) in line.lower()
                for anchor in row.anchors
            ):
                result.anchor_unbound += occurrences
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Spec 137 pre-deletion gate 4 (old-path references)"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="repository root to scan (default: current directory)",
    )
    arguments = parser.parse_args(argv)
    root = pathlib.Path(arguments.root).resolve()

    result = scan(root)

    for finding in sorted(result.findings, key=lambda item: (item.path, item.line)):
        print(
            f"FAIL [{finding.code}] {finding.path}:{finding.line}: {finding.message}",
            file=sys.stderr,
        )

    def count(code: str) -> int:
        return sum(1 for item in result.findings if item.code == code)

    settled = sum(1 for row in result.rows.values() if row.settled)
    print("Old-path gate 4 check")
    print(f"allowlist_rows_reviewed={settled}")
    print(f"allowlist_rows_unreviewed={len(result.rows) - settled}")
    print(f"clickable_links={count('OLD-PATH-CLICKABLE-LINK')}")
    print(f"unallowlisted_literals={count('OLD-PATH-UNALLOWLISTED')}")
    print(f"unreviewed_allowlist_literals={count('OLD-PATH-ALLOWLIST-UNREVIEWED')}")
    print(f"forbidden_class_literals={count('OLD-PATH-FORBIDDEN-CLASS')}")
    print(f"generated_surface_occurrences={result.generated_occurrences}")
    print(f"anchor_unbound_occurrences_advisory={result.anchor_unbound}")
    print(f"failures={len(result.findings)}")
    if result.findings:
        return 1
    print("PASS: no clickable old-pack reference and no unallowlisted literal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
