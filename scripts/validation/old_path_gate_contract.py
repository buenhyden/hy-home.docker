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
_DEST = rf"{_SLUG_BODY}(?:/|(?=[)>\"'\s\]]|$))"

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
        re.compile(rf"(?:href|src)\s*=\s*[\"'][^\"']*{_DEST}", re.IGNORECASE),
    ),
    ("autolink", re.compile(rf"<[^<>\s]*{_DEST}[^<>]*>", re.IGNORECASE)),
)

# A settled verdict states positively that a review happened. Requiring a
# positive marker rather than banning the word "pending" matters: several
# reviewed rows legitimately note that post-deletion lifecycle reconciliation is
# still pending, which is a future activity and not an open review. The bare word
# "pass" is deliberately absent: it occurs in ordinary prose and was load-bearing
# for no live row.
# Two ways to settle, preferring the structured form. A severity triple is a
# token an author cannot write ambiguously, so it stands alone. Prose markers are
# accepted only when the cell carries no negation at all, because polarity in free
# text cannot be chased reliably: an earlier attempt to read polarity positionally
# still settled "REVIEWED-BY-NOBODY".
SETTLED_SEVERITY = re.compile(r"\bC0/I0\b")
SETTLED_MARKER = re.compile(r"(?i)\b(?:reviewed|approved)\b")
NEGATION = re.compile(
    r"(?i)\b(?:not|no|nobody|none|never|without|un(?:reviewed|approved)|non"
    r"|fail|fails|failed|reject|rejected|outstanding|blocked|pending review"
    r"|review pending)\b"
)


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
    """True when the cell positively states a completed review."""
    if SETTLED_SEVERITY.search(verdict):
        return True
    if NEGATION.search(verdict):
        return False
    return bool(SETTLED_MARKER.search(verdict))


def _normalize(text: str) -> str:
    """Percent-decode and case-fold so encoding or case cannot hide a match."""
    try:
        decoded = urllib.parse.unquote(text)
    except (UnicodeDecodeError, ValueError):
        decoded = text
    return decoded.casefold()


def _clickable_lines(text: str) -> dict[int, str]:
    """Return {line number: form name} for every clickable destination."""
    normalized = _normalize(text)
    hits: dict[int, str] = {}
    for name, pattern in CLICKABLE_FORMS:
        for match in pattern.finditer(normalized):
            line = normalized.count("\n", 0, match.start()) + 1
            hits.setdefault(line, name)
    return hits


def _headings_by_line(text: str) -> dict[int, str]:
    """Map each line to its enclosing Markdown heading text."""
    current = ""
    mapping: dict[int, str] = {}
    for number, line in enumerate(text.split("\n"), start=1):
        if line.startswith("#"):
            current = line.lstrip("#").strip()
        mapping[number] = current
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
        headings = _headings_by_line(text)
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
            if row.anchors and not any(
                anchor.lower() in headings[number].lower()
                or anchor.lower() in line.lower()
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
