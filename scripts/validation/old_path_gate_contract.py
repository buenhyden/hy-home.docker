#!/usr/bin/env python3
"""Validate Spec 137 pre-deletion gate 4.

Gate 4 requires zero clickable references to the retiring research pack across
all tracked text outside the retiring directory. Verified native Migration
source fields and unchanged, multiplicity-bound occurrences in its exact renamed
source files retain their source-evidence role; other permitted non-link literals
require the owning Task's reviewed allowlist. Clickable links are never exempted.

Scope limit, stated so this module is not read as more than it is. The Spec's
deterministic evidence set for gate 4 has four items; this module implements the
first, the literal scan. It does not run the repository contract check, the
implementation-alignment check, or the LLM Wiki freshness checks, and it has no
notion of the mandated pre-deletion and post-deletion double run. Passing here is
necessary, not sufficient.

Declared non-coverage, so these are limits rather than silent gaps. The
clickable check does NOT detect: a tag opened further above its attribute than
WINDOW_LINES; a destination split over more lines than WINDOW_LINES; a
`<meta http-equiv="refresh">` target; a CSS `url(...)` reference; tracked text
that is not valid UTF-8 (counted as `unreadable_files_skipped`, never silent);
and a tracked symlink, which is read through to its target rather than scanned
as a blob. Detection is bounded on purpose: eight review rounds established
that widening it trades one error direction for the other, and gate 4's
evidence is a human-reviewed finding list, not this module's unaided verdict.

Review-verdict limit. The settled-verdict predicate checks that a row states a
review happened. It cannot establish that a review actually happened, so it does
not detect the defect that motivated it, where a record was relabelled from
"review pending" to "Approved" without a covering review. It only removes the
easy form of that failure, a row that never claimed a verdict at all.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import html
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, field

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from scripts.lib.document_governance import archive  # noqa: E402
from scripts.lib.document_governance.git_provenance import HistoricalDocument  # noqa: E402

# The pack was RENAMED, not deleted, so one constant no longer serves both jobs
# this module asks of it. `49522aa1` moved all twenty leaves from the date slug
# to `0001-…`, and while this module still derived everything from the date slug
# the gate reported `failures=0` while enforcing nothing: `RETIRING_DIR` named an
# empty path so the self-exclusion excluded nothing, and a clickable link to the
# pack where it actually lives matched no pattern at all.
#
# The two jobs are therefore separated. SLUG names where the pack IS, and fixes
# the directory the scan protects and excludes. RETIRED_SLUG names what the pack
# WAS, and stays in the detected set because tracked text still carries it and a
# stale reference to the old name is exactly what gate 4 exists to find. Both are
# detected; only the live one bounds a directory.
SLUG = "0001-agentic-research-pack-refresh"
RETIRED_SLUG = "2026-07-05-agentic-research-pack-refresh"
RETIRING_DIR = f"docs/90.references/research/{SLUG}"
# The Migration's task-9 rename rows are keyed by the pack's PRE-rename paths,
# because that is what they renamed from. Source-evidence selection reads this,
# never RETIRING_DIR.
RETIRED_DIR = f"docs/90.references/research/{RETIRED_SLUG}"
SLUGS = (SLUG, RETIRED_SLUG)
TASK_PATH = "docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"
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

_SLUG_BODY = "(?:" + "|".join(re.escape(slug) for slug in SLUGS) + ")"
# A destination reaches the retiring directory when the slug is followed by a
# path separator or ends the destination. The earlier form required a trailing
# slash and therefore missed a direct link to the directory itself.
_DEST = rf"{_SLUG_BODY}(?:[/\\]|(?=[)>\"'\s\]?#&,;\\]|$))"

_INLINE = re.compile(rf"\]\(\s*<?[^)\n]*{_DEST}", re.IGNORECASE)
_REFERENCE = re.compile(rf"^\s*\[[^\]]+\]:\s*<?[^\s]*{_DEST}", re.IGNORECASE | re.M)
# Any attribute that resolves a URL. ONE rule, not a two-tier split by name.
#
# Three rounds oscillated here. Requiring an enclosing tag prefix lost real
# links; dropping it for the "unambiguous" names re-acquired unsuppressable
# false positives on those names (`src = "..."` in Python, `--src=` in a shell
# line). Both directions were caused by trying to recognise tag structure with
# a prefix pattern. The rule now is only that a `<` must appear before the
# attribute in the scanned text: prose and assignments have none, and every
# real attribute sits inside a tag. `>` is deliberately allowed between, so a
# `>` inside an earlier quoted value cannot block the match.
_URL_ATTR = r"href|src|srcset|data|poster|action|formaction|cite|ping|manifest|longdesc"
_ATTR_VALUE = r"(?:[\"'][^\"']*|[^\s>\"']*)"
_HTML_ATTR = re.compile(
    rf"<[^\n]*?\b(?:{_URL_ATTR})\s*=\s*{_ATTR_VALUE}{_DEST}", re.IGNORECASE
)
_AUTOLINK = re.compile(rf"<[^<>\s]*{_DEST}[^<>]*>", re.IGNORECASE)

# How many lines a cross-line destination may span. The straddle rule keeps
# attribution correct at any width, so this is a coverage/cost dial. It is a
# HARD bound: a destination split over more than this many lines is not
# detected, which is the original two-line defect at a larger constant.
#
# Cost, stated in full because two earlier versions of this comment recorded
# only the flattering half. Roughly linear in the bound: on the largest
# slug-bearing tracked file -- graphify-out/graph.json at 17.5 MB, NOT the
# largest Markdown file, which one earlier version measured instead and
# thereby understated this by about 22x -- 1.17s at 2, 2.07s at 4, 2.96s at 6.
#
# Full repository scan is about 22s. It was about 10s for exactly one round,
# when every URL attribute required an enclosing tag and the pattern could
# fail fast; that anchor was removed for href, src, srcset, poster,
# formaction and longdesc because requiring it lost genuinely clickable HTML.
# The 2.3x is therefore the accepted price of that recall, not a regression to
# be optimised away by restoring the anchor.
#
# The remaining hazard is unrelated to this constant: `_INLINE` is superlinear
# in LINE LENGTH, and the window multiplies whatever that costs. Measured on a
# pathological `](`-repetition line: 0.038s at 11 KB, 0.167s at 23 KB, 0.579s at
# 46 KB, roughly 3.5x per doubling. An earlier version of this comment recorded
# "about 50s at 46 KB" on a reviewer's figure that neither that reviewer's
# successor nor this measurement reproduces; treat the growth rate as the claim,
# not the magnitude. No input-size guard and no timeout exist, so raising this
# constant multiplies that class of cost.
#
# A skip-if-the-joined-text-lacks-the-slug guard was tried and removed: it
# showed no measurable gain, because the cost concentrates in exactly the
# slug-bearing files it cannot skip.
WINDOW_LINES = 6
# The newline is mandatory. With it optional this pattern also matched wholly
# inside the second line of the window while the hit was recorded against the
# first, fabricating a finding on the line before every inline link.
_MULTILINE = re.compile(rf"\]\(\s*<?[^)\n]*\n[^)\n]*{_DEST}", re.IGNORECASE)

# Forms evaluated against a single line.
CLICKABLE_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("inline-link", _INLINE),
    ("reference-definition", _REFERENCE),
    ("html-attribute", _HTML_ATTR),
    ("autolink", _AUTOLINK),
)

# Forms evaluated against a two-line window joined by a newline.
NEWLINE_WINDOW_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("multiline-link", _MULTILINE),
)

# Forms evaluated against a WINDOW_LINES-line window joined with nothing at all. A URL
# parser strips CR and LF before parsing, so a destination broken across lines
# rejoins into a working link. Only concatenation reproduces that, and only
# these constructs can legally span the break.
# Forms evaluated against a WINDOW_LINES-line window joined by a SPACE. Tag
# structure, unlike a destination, does not survive concatenation: `<a` on one
# line and `href=` on the next join to `<ahref=`, which no word boundary can
# match, so every multi-line tag was missed. A space rejoins the structure; the
# concat window below still covers a destination broken mid-URL.
SPACED_WINDOW_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("spaced-html-attribute", _HTML_ATTR),
)

CONCAT_WINDOW_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("split-inline-link", _INLINE),
    ("split-reference-definition", _REFERENCE),
    ("split-html-attribute", _HTML_ATTR),
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
    r"|\bnobody\b"
    r"|\breview\s+pending\b|\bpending\s+review\b"
    # A requested review is an open state. Read this as a fail-closed rule, not
    # as a structural one: an earlier version of this comment claimed the latter
    # while the code excluded six nouns unconditionally, so the outcome turned
    # on voice rather than state. What the code actually does is treat
    # "requested" as open EXCEPT where it is followed by a named work noun AND a
    # named completion verb -- two enumerations, both on the settling side, so an
    # unrecognised phrasing stays unsettled. Known cost of that choice: cells
    # like "requested changes have been merged" are reported unsettled. That is
    # the safe direction and is recorded as an accepted limit in the Task.
    # "requested" is an open state in
    # every position except the adjectival one, where it modifies a noun naming
    # work already identified -- "Approved; requested changes were applied".
    # Excluding only that shape also removes the inverse false positive, where
    # "review requested changes were incorporated" demoted an approved row.
    # The exclusion must name work that was actually COMPLETED, not merely a
    # noun. Excluding on the noun alone was an unconditional escape hatch:
    # "requested changes remain open" and the active-voice forge verdict "the
    # seat requested changes" both settled, so the result depended on voice
    # rather than on state. Requiring a completion verb fails closed -- an
    # unrecognised phrasing stays unsettled rather than settling.
    r"|\brequested\b(?!\s+(?:changes|fixes|edits|corrections|updates|revisions)\s+"
    r"(?:(?:were|was|are|is|have\s+been|has\s+been)\s+)?"
    r"(?:applied|incorporated|landed|addressed|resolved|supplied|made)\b)"
    r"|\b(?:to\s+be|will\s+be|scheduled\s+to\s+be)\s+(?:reviewed|approved)\b"
    # Self-approval. The ledger requires a seat other than the author, and the
    # checker cannot see who settled a row, so at least the wording is rejected.
    r"|\bself[-\s]?(?:reviewed|approved)\b"
    r"|\bauto[-\s]?approved\b"
    r"|\b(?:reviewed|approved)\s+by\s+the\s+(?:author|module\s+author|maintainer)\b"
    r"|\bapproved\s*\(\s*self\s*\)"
    r")"
)
HISTORICAL_NEGATION = re.compile(r"(?i)\b(?:needs?\s+fixes|rejected)\b")
# An open state anywhere after a historical negation keeps the row unsettled.
OPEN_STATE = re.compile(
    r"(?i)(?:\bawaiting\b|\bexpected\b|\btarget\s+is\b|\bin\s+progress\b"
    r"|\babandoned\b|\bdo\s+not\b|\bcannot\b|\bhas\s+not\b"
    r"|\boutstanding\s+(?:critical|important|finding|findings|issue)\b)"
)
# Closing a historical negation requires an explicit statement that the round
# closed, not merely a later approval token. Two seats' verdicts listed side by
# side — "quality Needs fixes ...; specification Approved ..." — must not settle,
# and must not settle differently depending on which clause is written first.
CLOSURE = re.compile(
    r"(?i)(?:\bthen\s+received\b|\bclosure\b|\bclosed\b|\bresolved\b"
    r"|\bsubsequently\s+approved\b"
    r"|\bre-?review(?:s|ed)?\s+(?:returned|approved|are\s+approved)\b)"
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


def _collapse_rows(path_rows: list["AllowRow"]) -> "AllowRow | None":
    """Fail-closed view of every allowlist row declared for one path."""
    if not path_rows:
        return None
    forbidden = next((row for row in path_rows if row.forbidden_class), None)
    if forbidden is not None:
        return forbidden
    unsettled = next((row for row in path_rows if not row.settled), None)
    if unsettled is not None:
        return unsettled
    anchors: tuple[str, ...] = ()
    for row in path_rows:
        anchors += row.anchors
    first = path_rows[0]
    return AllowRow(
        path=first.path,
        anchors=anchors,
        literal_class=first.literal_class,
        verdict=first.verdict,
        settled=True,
        forbidden_class=False,
    )


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    generated_occurrences: int = 0
    anchor_unbound: int = 0
    unreadable_files: int = 0
    rows: dict[str, list[AllowRow]] = field(default_factory=dict)


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _git_or_unavailable(root: pathlib.Path, *args: str) -> str:
    try:
        return _git(root, *args)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        # Not a repository, or git absent. The gate cannot run; it has not
        # passed and it has not failed, and the contract requires that
        # distinction so an environment fault pauses deletion.
        raise AllowlistUnavailable(f"{root}: tracked-file listing failed") from error


def tracked_files(root: pathlib.Path) -> list[str]:
    # NUL-delimited. With the default `core.quotePath`, git escapes non-ASCII
    # names as `"docs/\346\227\245..."`, which then fails `is_file()` and was
    # skipped with no diagnostic -- a silent coverage hole in output that is
    # itself the gate's evidence. NUL also survives a newline in a filename,
    # which `splitlines()` would have split into two bogus entries.
    listing = _git_or_unavailable(root, "-c", "core.quotePath=false", "ls-files", "-z")
    return [name for name in listing.split("\0") if name]


class AllowlistUnavailable(RuntimeError):
    """The Task document backing the allowlist is missing or unreadable."""


def _cells(line: str) -> list[str]:
    """Split a Markdown table row on unescaped pipes."""
    parts = re.split(r"(?<!\\)\|", line)
    return [part.replace(r"\|", "|").strip() for part in parts]


def read_allowlist(root: pathlib.Path) -> dict[str, list[AllowRow]]:
    """Parse the Task's allowlist, resolving columns by header name."""
    task = root / TASK_PATH
    if not task.is_file():
        # A missing or renamed Task doc is a gate failure, not a traceback. The
        # caller reads the finding list; an uncaught FileNotFoundError leaves it
        # with no verdict at all.
        raise AllowlistUnavailable(f"{TASK_PATH}: allowlist source is missing")
    try:
        text = task.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        # The class docstring said "missing or unreadable" while only missing
        # was covered, so an unreadable or undecodable Task still produced a
        # bare traceback at the same exit status as a legitimate gate failure.
        raise AllowlistUnavailable(
            f"{TASK_PATH}: allowlist source is unreadable: {type(error).__name__}"
        ) from error
    lines = text.split("\n")
    try:
        start = next(
            index
            for index, line in enumerate(lines)
            if line.startswith(ALLOWLIST_HEADING)
        )
    except StopIteration:
        return {}

    header: list[str] | None = None
    malformed: list[tuple[int, str]] = []
    # Keyed by path to a LIST of rows. Spec 137's Route-1 admission and split-row
    # evaluation amendment makes each declared row a separate subject: one
    # document may hold literals of different classes under separate rows, each
    # with its own route, class and verdict. Storing one row per path let a
    # later row silently overwrite an earlier one, so a settled verdict could
    # mark literals reviewed that no reviewer had seen.
    rows: dict[str, list[AllowRow]] = {}
    # The fence is tracked by its marker, not as a boolean: a `~~~` inside a
    # ``` block does not close it in CommonMark, and toggling on either marker
    # let the row after the mismatched line back in as a live grant.
    fence: tuple[str, int] | None = None
    in_comment = False
    previous = ""
    for line in lines[start + 1 :]:
        stripped = line.lstrip()
        # Comment state is resolved BEFORE fence state. Checking the fence
        # first let a ``` inside an HTML comment open a real fence, which then
        # swallowed the closing `-->` and dropped every later row.
        if in_comment:
            if "-->" in line:
                in_comment = False
            previous = line
            continue
        if fence is not None:
            marker, width = fence
            run = len(stripped) - len(stripped.lstrip(marker))
            # The indent rule applies to CLOSING too. Applying it only to the
            # opening left a four-space-indented run still closing the fence,
            # so the rows after it became live grants anyway.
            if len(line) - len(stripped) >= 4:
                previous = line
                continue
            # CommonMark: a closing fence needs at least the opening width and
            # carries no info string. Matching on a bare prefix let a ``` close
            # a ```` block, and let ```` ```text ```` close one at all.
            if (
                stripped.startswith(marker)
                and run >= width
                and not stripped[run:].strip()
            ):
                fence = None
            previous = line
            continue
        indent = len(line) - len(stripped)
        # Four or more spaces makes it code content, not a fence, so
        # treating it as one closed a fence CommonMark keeps open and
        # admitted the illustrative rows after it as live grants.
        if indent < 4 and stripped.startswith(("```", "~~~")):
            marker = stripped[0]
            fence = (marker, len(stripped) - len(stripped.lstrip(marker)))
            previous = line
            continue
        # An HTML comment spans lines. Skipping only a line that itself starts
        # with `<!--` left the block form -- the normal way to comment a table
        # out -- granting real exemptions. The consuming branch lives above the
        # fence check, because a fence opened inside a comment swallowed the
        # closing `-->`; a duplicate of it stood here and was unreachable.
        if stripped.startswith("<!--") and "-->" not in line:
            in_comment = True
            previous = line
            continue
        # Any subsequent heading ends the table. `#{2,}` contradicted this
        # comment by letting a level-1 heading through, and an ATX-only test
        # let a setext heading through for the same reason.
        if re.match(r"^#{1,6}\s", line) or (
            re.match(r"^(?:={2,}|-{2,})\s*$", line)
            and previous.strip()
            and not previous.startswith("|")
        ):
            break
        previous = line
        if stripped.startswith("<!--"):
            continue
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
        if len(cells) != len(header):
            # A row whose cell count does not match the header is misread by
            # position, not skipped: `pick` indexes by header position, so an
            # unescaped `|` inside a cell shifts every later field and the
            # review verdict is read from the wrong one. That failed closed only
            # by luck on 2026-08-19, when a pasted table fragment put the text
            # `Criteria source` where the verdict belongs. Fail loudly instead.
            malformed.append((len(cells), line))
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
        rows.setdefault(path, []).append(AllowRow(
            path=path,
            anchors=anchors,
            literal_class=literal_class,
            verdict=verdict,
            settled=_is_settled(verdict),
            forbidden_class=bool(FORBIDDEN_CLASSES.search(literal_class)),
        ))
    if malformed:
        raise ValueError(
            "allowlist rows do not match the header cell count; escape any "
            f"literal `|` inside a cell as `\\|`: {malformed[:3]}"
        )
    return rows


def _is_settled(verdict: str) -> bool:
    """True when the cell positively states a completed review.

    Negation is evaluated first and applies to both settling routes, including
    the structured severity token.
    """
    if TERMINAL_NEGATION.search(verdict) or OPEN_STATE.search(verdict):
        return False

    def settles(text: str) -> bool:
        return bool(SETTLED_SEVERITY.search(text) or SETTLED_MARKER.search(text))

    historical = [match.end() for match in HISTORICAL_NEGATION.finditer(verdict)]
    if historical:
        # Blocked unless the record explicitly states the round closed. The tail
        # must carry a closure statement and a structured severity token, and
        # must not carry an open state. Requiring the closure statement rather
        # than any later approval token makes the result independent of the order
        # the clauses were written in.
        tail = verdict[historical[-1] :]
        if OPEN_STATE.search(tail) or TERMINAL_NEGATION.search(tail):
            return False
        return bool(CLOSURE.search(tail) and SETTLED_SEVERITY.search(tail))
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
    # Deleted rather than replaced with a space. The WHATWG URL parser removes
    # ASCII tab, LF, and CR from the input, so any of the three inside a
    # destination must not break the slug apart. Tab was missed while the other
    # two were handled, which let a genuinely resolving link score zero
    # findings; entity forms mattered most, because `html.unescape` runs first
    # and materializes `&#9;` or `&Tab;` into a tab this step then had to drop.
    for stripped in ("\t", "\r", "\n"):
        decoded = decoded.replace(stripped, "")
    return decoded.casefold()


def _normalized_lines(text: str) -> list[str]:
    """Normalize per line, so indices match the original exactly."""
    return [_normalize(line) for line in text.split("\n")]


def _clickable_lines(text: str) -> dict[int, str]:
    """Return {original line number: form name} for clickable destinations."""
    lines = _normalized_lines(text)
    hits: dict[int, str] = {}
    for number, line in enumerate(lines, start=1):
        for name, pattern in CLICKABLE_FORMS:
            if pattern.search(line):
                hits.setdefault(number, name)
        if number >= len(lines):
            continue
        following = lines[number]
        for name, pattern in NEWLINE_WINDOW_FORMS:
            if pattern.search(f"{line}\n{following}"):
                hits.setdefault(number, name)
        # The window spans several following lines, not one. Newlines are legal
        # inside a quoted HTML attribute value and the URL parser strips them,
        # so a destination broken across three or more lines still resolves; a
        # two-line window scored zero findings on it, in both halves of the gate.
        span = lines[number - 1 : number - 1 + WINDOW_LINES]
        for joiner, forms in ((" ", SPACED_WINDOW_FORMS), ("", CONCAT_WINDOW_FORMS)):
            joined = joiner.join(span)
            for name, pattern in forms:
                match = pattern.search(joined)
                if match and match.start() < len(line) < match.end():
                    hits.setdefault(number, name)

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


def _migration_literal_evidence(
    root: pathlib.Path,
) -> tuple[dict[str, collections.Counter[str]], str, str]:
    """Classify proved source occurrences, never a directory or current owner."""
    path = archive._migration_path(root)
    if not path.exists():
        return {}, "", ""
    try:
        document = archive._migration_document(root)
        approved = archive._approved_migration_document(root)
        sources = {
            row["source_path"] for row in approved["rows"]
            if row["owner_task"] == 9 and row["action"] == "rename"
            and row["source_path"].startswith(f"{RETIRED_DIR}/")
        }
        bodies = {}
        for row in document["rows"]:
            if row["source_path"] in sources:
                text = HistoricalDocument(
                    root, approved["baseline_commit"], row["source_path"]
                ).read_text()
                bodies[row["target_path"]] = collections.Counter(
                    line
                    for line in text.splitlines()
                    if any(slug in _normalize(line) for slug in SLUGS)
                )
        raw = archive._read_regular(path)
        if archive._parse_migration_document(raw) != document:
            raise ValueError("Migration changed after native proof")
        text = raw.decode("utf-8")
        block = re.search(r"^```yaml\n(.*?)^```[ \t]*$", text, re.MULTILINE | re.DOTALL)
        node = yaml.compose(block.group(1), Loader=yaml.SafeLoader)
        rows_node = next(value for key, value in node.value if key.value == "rows")
        classified = list(text)
        for row_node, row in zip(rows_node.value, document["rows"], strict=True):
            for key, value in row_node.value:
                if key.value != "source_path" or row["source_path"] not in sources:
                    continue
                if (
                    not isinstance(value, yaml.ScalarNode)
                    or value.value != row["source_path"]
                    or value.start_mark.index <= key.end_mark.index
                ):
                    raise ValueError("Migration source scalar differs from native proof")
                start = block.start(1) + value.start_mark.index
                end = block.start(1) + value.end_mark.index
                classified[start:end] = ["\n" if character == "\n" else " " for character in text[start:end]]
        return bodies, text, "".join(classified)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
        raise AllowlistUnavailable(f"Migration source evidence is unavailable: {error}") from error


def _unproved_source_text(text: str, proved: collections.Counter[str]) -> str:
    """Keep changed/new/excess lines; consume each historical occurrence once."""
    remaining = proved.copy()
    lines = []
    for line in text.split("\n"):
        if remaining[line] > 0:
            remaining[line] -= 1
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def scan(root: pathlib.Path) -> ScanResult:
    """Run the gate-4 literal scan."""
    rows = read_allowlist(root)
    result = ScanResult(rows=rows)
    needles = tuple(_normalize(slug) for slug in SLUGS)
    source_bodies, migration_text, classified_migration = _migration_literal_evidence(root)
    migration_path = archive._migration_path(root)

    for relative in tracked_files(root):
        if relative.startswith(f"{RETIRING_DIR}/"):
            continue
        absolute = root / relative
        try:
            # `is_file()` sat outside this guard, so a stat failure -- an
            # unreadable parent directory, a symlink loop -- raised uncaught
            # and exited 1, indistinguishable from a legitimate gate failure.
            if not absolute.is_file():
                result.unreadable_files += 1
                continue
            text = (
                archive._read_regular(absolute).decode("utf-8")
                if relative in source_bodies or absolute == migration_path
                else absolute.read_text(encoding="utf-8")
            )
        except (UnicodeDecodeError, OSError, ValueError) as error:
            if relative in source_bodies or absolute == migration_path:
                raise AllowlistUnavailable(f"proved source target is unreadable: {relative}: {error}") from error
            # Counted, never silent. Most of these are genuinely binary, but a
            # UTF-16 or Latin-1 Markdown file containing a live link lands here
            # too, and a hole in the output that IS the gate's evidence cannot
            # be left invisible.
            result.unreadable_files += 1
            continue
        normalized_text = _normalize(text)
        if not any(needle in normalized_text for needle in needles):
            continue

        clickable = _clickable_lines(text)
        headings = _headings_by_line(text, relative.endswith(".md"))
        if absolute == migration_path and migration_text:
            if text != migration_text:
                raise AllowlistUnavailable("Migration changed after native source-span proof")
            text = classified_migration
        elif relative in source_bodies:
            text = _unproved_source_text(text, source_bodies[relative])
        # Every row declared for this path applies to it, and the amendment
        # states that settling one row settles nothing for its siblings. The
        # declared anchors are prose descriptors, so an occurrence cannot be
        # attributed to one sibling reliably; the evaluation therefore fails
        # closed across the whole group. A forbidden class anywhere in the group
        # is reported, a single unsettled sibling leaves the path unreviewed,
        # and only a fully settled group clears it.
        path_rows = rows.get(relative) or []
        row = _collapse_rows(path_rows)
        generated = relative.startswith(GENERATED_PREFIXES)

        for number, line in enumerate(text.split("\n"), start=1):
            normalized = _normalize(line)
            occurrences = sum(normalized.count(needle) for needle in needles)
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

    try:
        result = scan(root)
    except AllowlistUnavailable as error:
        # Previously this only renamed the exception: nothing caught it, so the
        # operator still got a traceback with no verdict, no counters and no
        # finding list, at the same exit status as a legitimate failure. A
        # distinct status lets a caller tell "gate failed" from "gate could not
        # run", which the contract requires to pause deletion rather than pass.
        print(f"FAIL [OLD-PATH-GATE-UNRUNNABLE] {error}", file=sys.stderr)
        print("gate_could_not_run=1", file=sys.stderr)
        return 2

    for finding in sorted(result.findings, key=lambda item: (item.path, item.line)):
        print(
            f"FAIL [{finding.code}] {finding.path}:{finding.line}: {finding.message}",
            file=sys.stderr,
        )

    def count(code: str) -> int:
        return sum(1 for item in result.findings if item.code == code)

    all_rows = [row for group in result.rows.values() for row in group]
    settled = sum(1 for row in all_rows if row.settled)
    print("Old-path gate 4 check")
    print(f"allowlist_rows_reviewed={settled}")
    print(f"allowlist_rows_unreviewed={len(all_rows) - settled}")
    print(f"clickable_links={count('OLD-PATH-CLICKABLE-LINK')}")
    print(f"unallowlisted_literals={count('OLD-PATH-UNALLOWLISTED')}")
    print(f"unreviewed_allowlist_literals={count('OLD-PATH-ALLOWLIST-UNREVIEWED')}")
    print(f"forbidden_class_literals={count('OLD-PATH-FORBIDDEN-CLASS')}")
    print(f"generated_surface_occurrences={result.generated_occurrences}")
    print(f"anchor_unbound_occurrences_advisory={result.anchor_unbound}")
    print(f"unreadable_files_skipped={result.unreadable_files}")
    print(f"failures={len(result.findings)}")
    if result.findings:
        return 1
    print("PASS: no clickable old-pack reference and no unallowlisted literal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
