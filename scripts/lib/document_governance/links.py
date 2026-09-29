"""Shared Markdown document graph and deterministic link validators."""

from __future__ import annotations

import bisect
import dataclasses
import html
import json
import pathlib
import posixpath
import re
import subprocess
import urllib.parse
from collections.abc import Iterable, Mapping
from html.parser import HTMLParser
from types import MappingProxyType

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.language import language_mismatch
from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
    read_bounded_regular,
)
from scripts.lib.document_governance.registry import (
    ARCHIVE_MODEL_ADOPTED,
    admitted_preserved_dispositions,
    archive_disposition_model,
    classify_path,
    load_registry,
)

_URL = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_LINK_OPEN = re.compile(r"(?<!!)\[(?P<label>[^\[\]\n]*)\]\(")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
_CATALOG_PAIR = re.compile(r"\[OPER\]\(([^)]+)\),\s*\[RUN\]\(([^)]+)\)")
_DOC_ROOT = "docs"
# Stage directories are numbered by construction, so the pattern keeps matching
# a stage that is added or removed without a second list to keep in step.
_STAGE_DIRECTORY = re.compile(rf"^{_DOC_ROOT}/[0-9]{{2}}\.[^/]+(?:/|$)")
_ACTIVE_STAGE_PREFIXES = (
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
)
# Only `completed/` may be referenced from outside the archive. The rest of the
# archive is preserved evidence, not a citable current source, so an outside
# document naming it invites a superseded record to be read as current state.
# Incident and postmortem records are the exception: reconstructing what
# happened is exactly the case where the preserved body is the right citation.
_CITABLE_ARCHIVE_PREFIX = "docs/98.archive/completed/"
# Once ADR-0035 is adopted, citability follows what each disposition names:
# `resolved/` names a corrective-work owner and joins `completed/`, and its body
# is preserved like the others, so its outbound links are not checked either.
_ADOPTED_CITABLE_ARCHIVE_PREFIXES = (
    _CITABLE_ARCHIVE_PREFIX,
    "docs/98.archive/resolved/",
)
_ARCHIVE_CITING_PROFILES = ("operation/incident", "operation/postmortem")
# A route disposition holds no body. The incident and postmortem exception
# exists to reach preserved evidence, so it has nothing to reach here and the
# boundary closes these two paths to every source.
_ROUTE_RECORD_PREFIXES = (
    "docs/98.archive/tombstones/",
    "docs/98.archive/migrations/",
)
_ROOT_PREFIXES = (
    ".agents/",
    "docs/",
    "infra/",
    "scripts/",
    ".github/",
    ".claude/",
    ".codex/",
    "secrets/",
    "projects/",
    "tests/",
)
_ROOT_FILES = frozenset(
    {
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "RTK.md",
        "docker-compose.yml",
        "llms.txt",
        ".env.example",
    }
)
_MAX_ANCHOR_BYTES = 4 * 1024 * 1024


@dataclasses.dataclass(frozen=True)
class DocumentNode:
    """One Markdown document in the current graph."""

    path: pathlib.PurePosixPath
    text: str
    metadata: Mapping[str, object]
    headings: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class DocumentLink:
    """One parsed repository-local Markdown link."""

    source: pathlib.PurePosixPath
    target: pathlib.PurePosixPath
    raw_target: str
    fragment: str | None
    line: int
    absolute: bool = False
    outside_repository: bool = False
    label: str = ""

    @property
    def decoded_target(self) -> str:
        """Return the full percent-decoded destination, including query and fragment."""

        return urllib.parse.unquote(self.raw_target)

    @property
    def is_directory_route(self) -> bool:
        """Report whether the destination's path component denotes a directory."""

        path_component = re.split(r"[?#]", self.decoded_target, maxsplit=1)[0]
        return bool(path_component) and path_component.endswith("/")

    @property
    def has_unsafe_target(self) -> bool:
        """Reject unsafe location flags and decoded controls across the full target."""

        return (
            self.absolute
            or self.outside_repository
            or "\\" in self.decoded_target
            or any(
                ord(character) < 32 or ord(character) == 127
                for character in self.decoded_target
            )
        )


@dataclasses.dataclass(frozen=True)
class DocumentGraph:
    """A deterministic immutable view of documents and their local links."""

    repo_root: pathlib.Path
    nodes: tuple[DocumentNode, ...]
    links: tuple[DocumentLink, ...]
    input_findings: tuple[LinkFinding, ...] = ()


@dataclasses.dataclass(frozen=True, order=True)
class LinkFinding:
    """One stable link/traceability validation result."""

    path: str
    code: str
    message: str
    severity: str = "error"


def _without_html_comments(line: str, active: bool) -> tuple[str, bool]:
    """Blank HTML comments without shifting link offsets or line numbers."""

    rendered = list(line)
    opening_source = _without_inline_code(line)
    cursor = 0
    while cursor < len(line):
        if active:
            closing = line.find("-->", cursor)
            end = len(line) if closing < 0 else closing + 3
            for offset in range(cursor, end):
                rendered[offset] = " "
            if closing < 0:
                return "".join(rendered), True
            active = False
            cursor = end
            continue
        opening = opening_source.find("<!--", cursor)
        if opening < 0:
            break
        active = True
        cursor = opening
    return "".join(rendered), active


_REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[(?!\^)([^\]]+)\]:\s*<?([^\s>]+)")
_REFERENCE_USE = re.compile(r"(?<!!)(?<!\[)\[([^\[\]]+)\]\[([^\[\]]*)\]")
_WIKI_LINK = re.compile(r"(?<!!)\[\[([^\[\]\n]+)\]\]")


class _HrefAttributeParser(HTMLParser):
    """Collect values from exact ``href`` attributes in one bounded tag."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.values.extend(
            value for name, value in attrs if name == "href" and value is not None
        )


def _html_href_values(tag: str) -> tuple[str, ...]:
    parser = _HrefAttributeParser()
    parser.feed(tag)
    parser.close()
    return tuple(parser.values)


def _is_escaped(text: str, offset: int) -> bool:
    backslashes = 0
    while offset > 0 and text[offset - 1] == "\\":
        backslashes += 1
        offset -= 1
    return backslashes % 2 == 1


def _html_tag_end(
    text: str, index: int, quote: str | None = None
) -> tuple[int, str | None, bool]:
    """Advance once through a tag, retaining only its unfinished quote state."""

    while index < len(text):
        character = text[index]
        if quote is not None:
            if character == quote:
                quote = None
        elif character in "\"'":
            quote = character
        elif character == ">":
            return index + 1, None, True
        index += 1
    return index, quote, False


def _html_tag_spans(line: str) -> Iterable[tuple[int, int]]:
    """Yield raw HTML tag spans, respecting quotes and bounding malformed input."""

    cursor = 0
    while (start := line.find("<", cursor)) >= 0:
        index = start + 1
        if index < len(line) and line[index] == "/":
            index += 1
        if index >= len(line) or not line[index].isascii() or not line[index].isalpha():
            cursor = start + 1
            continue
        index += 1
        while index < len(line) and (
            line[index] == "-" or (line[index].isascii() and line[index].isalnum())
        ):
            index += 1
        if index < len(line) and not (line[index].isspace() or line[index] in "/>"):
            cursor = start + 1
            continue
        end, _, complete = _html_tag_end(line, index)
        yield start, end
        if not complete:
            return
        cursor = end


def _unfenced_lines(
    text: str, *, include_fenced: bool = False
) -> Iterable[tuple[int, str]]:
    fence: str | None = None
    html_comment = False
    for line_no, line in enumerate(text.splitlines(), start=1):
        raw_stripped = line.lstrip()
        raw_marker = (
            "```"
            if raw_stripped.startswith("```")
            else "~~~"
            if raw_stripped.startswith("~~~")
            else None
        )
        # A visible fence opener owns its entire info string. In particular,
        # an example such as `````text <!--`` must not leak HTML-comment state
        # beyond the fence. A marker already inside an active HTML comment is
        # still masked by the comment scanner below.
        if fence is None and not html_comment and raw_marker is not None:
            fence = raw_marker
            continue
        if fence is None:
            line, html_comment = _without_html_comments(line, html_comment)
        stripped = line.lstrip()
        marker = (
            "```"
            if stripped.startswith("```")
            else "~~~"
            if stripped.startswith("~~~")
            else None
        )
        if marker is not None:
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None or include_fenced:
            yield line_no, line


def _without_inline_code(line: str) -> str:
    """Blank inline code spans without shifting link offsets."""

    rendered = list(line)
    index = 0
    while index < len(line):
        if line[index] != "`":
            index += 1
            continue
        width = 1
        while index + width < len(line) and line[index + width] == "`":
            width += 1
        closing = line.find("`" * width, index + width)
        if closing < 0:
            index += width
            continue
        for offset in range(index, closing + width):
            rendered[offset] = " "
        index = closing + width
    return "".join(rendered)


def _markdown_destinations(line: str) -> Iterable[tuple[str, str, int, int]]:
    """Yield labeled destinations with angle and nested-parenthesis support."""

    def consume_tail(text: str, cursor: int) -> int | None:
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor < len(text) and text[cursor] == ")":
            return cursor + 1
        if cursor >= len(text) or text[cursor] not in "\"'(":
            return None
        delimiter = ")" if text[cursor] == "(" else text[cursor]
        cursor += 1
        while cursor < len(text):
            if text[cursor] == "\\":
                cursor += 2
                continue
            if text[cursor] == delimiter:
                cursor += 1
                break
            cursor += 1
        else:
            return None
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor < len(text) and text[cursor] == ")":
            return cursor + 1
        return None

    text = _without_inline_code(line)
    position = 0
    while (opening := _LINK_OPEN.search(text, position)) is not None:
        if _is_escaped(text, opening.start()):
            position = opening.end()
            continue
        cursor = opening.end()
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text):
            return
        if text[cursor] == "<":
            closing = text.find(">", cursor + 1)
            if closing < 0:
                return
            end = consume_tail(text, closing + 1)
            if end is None:
                return
            yield (
                opening.group("label"),
                text[cursor + 1 : closing],
                opening.start(),
                end,
            )
            position = end
            continue
        start = cursor
        depth = 0
        while cursor < len(text):
            character = text[cursor]
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    destination = text[start:cursor].strip()
                    if destination:
                        yield (
                            opening.group("label"),
                            destination.split(maxsplit=1)[0],
                            opening.start(),
                            cursor + 1,
                        )
                    position = cursor + 1
                    break
                depth -= 1
            elif character.isspace() and depth == 0:
                destination = text[start:cursor]
                end = consume_tail(text, cursor)
                if end is None:
                    return
                if destination:
                    yield opening.group("label"), destination, opening.start(), end
                position = end
                break
            cursor += 1
        else:
            return


def _slug(value: str) -> str:
    text = re.sub(r"<[^>]+>", "", value).strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"[ -]+", "-", text).strip("-")


def _headings(text: str) -> tuple[str, ...]:
    values: list[str] = []
    counts: dict[str, int] = {}
    for _, line in _unfenced_lines(text):
        match = _HEADING.match(line)
        if match is None:
            continue
        base = _slug(match.group(1))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        values.append(base if count == 0 else f"{base}-{count}")
    return tuple(values)


def _normalized_target(
    source: pathlib.PurePosixPath,
    raw: str,
) -> tuple[pathlib.PurePosixPath, str | None, bool, bool] | None:
    if not raw or _URL.match(raw):
        return None
    unquoted = urllib.parse.unquote(raw)
    without_query = unquoted.split("?", 1)[0]
    path_text, separator, fragment = without_query.partition("#")
    if not path_text:
        return source, (fragment if separator and fragment else None), False, False
    absolute = path_text.startswith("/")
    clean = path_text.lstrip("/") if absolute else path_text
    if absolute or clean in _ROOT_FILES or clean.startswith(_ROOT_PREFIXES):
        combined = clean
    else:
        combined = posixpath.join(source.parent.as_posix(), clean)
    normalized = posixpath.normpath(combined)
    outside = normalized == ".." or normalized.startswith("../")
    target = pathlib.PurePosixPath(normalized.lstrip("/"))
    return target, (fragment if separator and fragment else None), absolute, outside


def _continued_html_lines(
    lines: Iterable[tuple[int, str]],
) -> Iterable[tuple[int, str]]:
    """Join only unfinished tags in linear time, bounded by supplied text.

    Gaps in selected physical lines break continuity. Markdown titles cannot
    start HTML state, and unfinished attributes remain masked at end of input.
    """

    chunks: list[str] = []
    first = previous = 0
    quote: str | None = None
    pending = False
    for number, line in lines:
        if chunks and number != previous + 1:
            yield first, "\n".join(chunks)
            chunks = []
            pending, quote = False, None
        if not chunks:
            first = number
        chunks.append(line)
        previous = number
        offset = 0
        if pending:
            offset, quote, complete = _html_tag_end(line, 0, quote)
            if not complete:
                continue
            pending = False
        for start, end in _html_tag_spans(line[offset:]):
            start += offset
            end += offset
            if end != len(line):
                continue
            if any(
                not _is_escaped(line, opening.start())
                and opening.end() <= start
                and not line[opening.end() : start].strip()
                for opening in _LINK_OPEN.finditer(line)
            ):
                # An unfinished angle destination belongs to Markdown; it must
                # not carry HTML state into the next physical line.
                continue
            if any(
                begin <= start < finish
                for _, _, begin, finish in _markdown_destinations(line)
            ):
                continue
            _, quote, complete = _html_tag_end(line, start + 1)
            if not complete:
                pending = True
        if not pending:
            yield first, "\n".join(chunks)
            chunks = []
    if chunks:
        yield first, "\n".join(chunks)


def _link_destinations(
    lines: Iterable[tuple[int, str]],
) -> Iterable[tuple[int, str, str]]:
    """Share destination syntax without changing which lines each mode reads."""

    lines = tuple(
        _continued_html_lines(
            (number, _without_inline_code(line)) for number, line in lines
        )
    )
    references: dict[str, str] = {}
    for _, line in lines:
        definition = _REFERENCE_DEFINITION.match(line)
        if definition is not None:
            key = " ".join(definition[1].casefold().split())
            references.setdefault(key, definition[2])
    for line_no, line in lines:
        if _REFERENCE_DEFINITION.match(line):
            continue
        tags = tuple(_html_tag_spans(line))
        destinations: list[tuple[int, str, str]] = []
        newlines = tuple(index for index, char in enumerate(line) if char == "\n")
        spans = list(tags)
        inline_spans: list[tuple[int, int]] = []
        tag_index = 0
        for label, raw, start, end in _markdown_destinations(line):
            while tag_index < len(tags) and tags[tag_index][1] <= start:
                tag_index += 1
            if (
                tag_index < len(tags)
                and tags[tag_index][0] <= start < tags[tag_index][1]
            ):
                continue
            destinations.append((start, label, raw))
            spans.append((start, end))
            inline_spans.append((start, end))
        inline_index = 0
        for tag_start, tag_end in tags:
            while (
                inline_index < len(inline_spans)
                and inline_spans[inline_index][1] <= tag_start
            ):
                inline_index += 1
            if (
                inline_index < len(inline_spans)
                and inline_spans[inline_index][0]
                <= tag_start
                < inline_spans[inline_index][1]
            ):
                continue
            if not line[tag_start:tag_end].endswith(">"):
                continue
            destinations.extend(
                (tag_start, "", value)
                for value in _html_href_values(line[tag_start:tag_end])
            )
        masked = list(line)
        for start, end in spans:
            masked[start:end] = " " * (end - start)
        remaining = "".join(masked)
        for use in _REFERENCE_USE.finditer(remaining):
            if _is_escaped(remaining, use.start()):
                continue
            key = " ".join((use[2] or use[1]).casefold().split())
            if key in references:
                destinations.append((use.start(), use[1], references[key]))
        for match in _WIKI_LINK.finditer(remaining):
            if _is_escaped(remaining, match.start()):
                continue
            target, separator, label = match[1].partition("|")
            destinations.append((match.start(), label if separator else target, target))
        for offset, label, raw in destinations:
            yield line_no + bisect.bisect_left(newlines, offset), label, raw


def parse_local_markdown_links(
    source: pathlib.PurePosixPath,
    text: str,
) -> tuple[DocumentLink, ...]:
    """Parse normalized local links from supplied Markdown without filesystem I/O."""

    links: list[DocumentLink] = []
    for line_no, label, raw in _link_destinations(_unfenced_lines(text)):
        resolved = _normalized_target(source, raw)
        if resolved is None:
            continue
        target, fragment, absolute, outside = resolved
        links.append(
            DocumentLink(
                source=source,
                target=target,
                raw_target=raw,
                fragment=fragment,
                line=line_no,
                absolute=absolute,
                outside_repository=outside,
                label=label,
            )
        )
    return tuple(links)


def _strict_relative_path(
    root: pathlib.Path,
    path: pathlib.Path,
) -> pathlib.PurePosixPath | None:
    """Return a lexical repository-relative path without resolving symlinks."""

    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        return None
    return pathlib.PurePosixPath(relative.as_posix())


def _has_symlink_ancestor(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
) -> bool:
    """Report symlinks in the path below ``root`` but above its leaf."""

    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink():
            return True
    return False


def build_document_graph(
    paths: Iterable[pathlib.Path],
    *,
    repo_root: pathlib.Path,
) -> DocumentGraph:
    """Read the supplied Markdown paths once and build a sorted local graph."""

    root = repo_root.absolute()
    nodes: list[DocumentNode] = []
    links: list[DocumentLink] = []
    input_findings: list[LinkFinding] = []
    selected = sorted(
        {item.absolute() for item in paths}, key=lambda item: item.as_posix()
    )
    for path in selected:
        relative = _strict_relative_path(root, path)
        if relative is None:
            input_findings.append(
                LinkFinding(
                    path.as_posix(), "document-outside-repository", path.as_posix()
                )
            )
            continue
        if _has_symlink_ancestor(root, relative):
            input_findings.append(
                LinkFinding(
                    relative.as_posix(),
                    "document-symlink-ancestor",
                    relative.as_posix(),
                )
            )
            continue
        try:
            status = path.lstat()
        except OSError:
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-unreadable", relative.as_posix()
                )
            )
            continue
        if path.is_symlink():
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-symlink", relative.as_posix()
                )
            )
            continue
        if not path.is_file():
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-not-regular", relative.as_posix()
                )
            )
            continue
        if status.st_size > _MAX_ANCHOR_BYTES:
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-too-large", relative.as_posix()
                )
            )
            continue
        try:
            text = read_bounded_regular(
                root, relative, max_bytes=_MAX_ANCHOR_BYTES
            ).decode("utf-8")
        except UnicodeError:
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-invalid-utf8", relative.as_posix()
                )
            )
            continue
        except (OSError, OperationsAuthorityError):
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-unreadable", relative.as_posix()
                )
            )
            continue
        try:
            metadata = frontmatter_record_from_text(path, text).metadata
        except FrontmatterError as error:
            metadata = MappingProxyType({})
            input_findings.append(
                LinkFinding(
                    relative.as_posix(),
                    "document-frontmatter-invalid",
                    error.code,
                )
            )
        nodes.append(DocumentNode(relative, text, metadata, _headings(text)))
        links.extend(parse_local_markdown_links(relative, text))
    return DocumentGraph(
        root,
        tuple(sorted(nodes, key=lambda item: item.path.as_posix())),
        tuple(
            sorted(
                links,
                key=lambda item: (
                    item.source.as_posix(),
                    item.line,
                    item.target.as_posix(),
                    item.raw_target,
                ),
            )
        ),
        tuple(sorted(set(input_findings))),
    )


def _diagnostic_text(message: str) -> str:
    return json.dumps(message, ensure_ascii=True)[1:-1][:512]


def _finding(link: DocumentLink, code: str, message: str) -> LinkFinding:
    return LinkFinding(
        f"{link.source.as_posix()}:{link.line}", code, _diagnostic_text(message)
    )


def _document_profile(
    nodes: dict[pathlib.PurePosixPath, DocumentNode],
    source: pathlib.PurePosixPath,
) -> str:
    """Return the source document's declared `type`, or an empty string."""

    node = nodes.get(source)
    if node is None:
        return ""
    lines = node.text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:60]:
        if line.strip() == "---":
            break
        if line.startswith("type:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def _preserved_link_prefixes(graph: DocumentGraph) -> tuple[str, ...]:
    """Return the preserved-body prefixes the graph root's archive model admits."""

    return tuple(
        f"docs/98.archive/{disposition}/"
        for disposition in admitted_preserved_dispositions(
            archive_disposition_model(graph.repo_root)
        )
    )


def _node_map(graph: DocumentGraph) -> dict[pathlib.PurePosixPath, DocumentNode]:
    return {node.path: node for node in graph.nodes}


def _regular_target(
    graph: DocumentGraph, target: pathlib.PurePosixPath
) -> tuple[pathlib.Path | None, str | None]:
    if target.is_absolute() or any(part in {"", ".", ".."} for part in target.parts):
        return None, "link-outside-repository"
    path = graph.repo_root.joinpath(*target.parts)
    relative = _strict_relative_path(graph.repo_root, path)
    if relative is None:
        return None, "link-outside-repository"
    if _has_symlink_ancestor(graph.repo_root, relative):
        return None, "link-target-symlink-ancestor"
    try:
        status = path.lstat()
    except FileNotFoundError:
        return None, "missing-link-target"
    except OSError:
        return None, "link-target-unreadable"
    if path.is_symlink():
        return None, "link-target-symlink"
    if path.is_dir():
        indexes = (
            path / "README.md",
            path / "spec.md",
            *sorted(path.glob("*.md"), key=lambda item: item.name),
        )
        for index in indexes:
            try:
                index_status = index.lstat()
            except OSError:
                continue
            if (
                not index.is_symlink()
                and index.is_file()
                and index_status.st_size <= _MAX_ANCHOR_BYTES
            ):
                return index, None
        # A folder with no Markdown index is still a route when it holds
        # content: a router links such a child as the folder itself
        # (SPEC-0184 rule 1). It has no headings, so a fragment cannot match.
        try:
            has_content = any(path.iterdir())
        except OSError:
            has_content = False
        if has_content:
            return path, None
        return None, "link-target-not-regular"
    if not path.is_file():
        return None, "link-target-not-regular"
    if status.st_size > _MAX_ANCHOR_BYTES:
        return None, "link-target-too-large"
    return path, None


def _target_headings(
    graph: DocumentGraph,
    nodes: Mapping[pathlib.PurePosixPath, DocumentNode],
    target: pathlib.PurePosixPath,
) -> tuple[tuple[str, ...] | None, str | None]:
    node = nodes.get(target)
    if node is not None:
        return node.headings, None
    path, code = _regular_target(graph, target)
    if path is None:
        return None, code
    if path.is_dir():
        return (), None
    try:
        return _headings(path.read_text(encoding="utf-8")), None
    except UnicodeError:
        return None, "link-target-invalid-utf8"
    except OSError:
        return None, "link-target-unreadable"


def _historical_headings(root, provenance):
    """Select the same directory index as current links, at the original tree."""
    from scripts.lib.document_governance.git_provenance import _run_git

    object_id = provenance.object_id
    if provenance.object_type == "tree":
        listed = _run_git(root, ["ls-tree", "-z", object_id])
        if listed.returncode:
            return None
        indexes = {}
        for entry in listed.stdout.split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            mode, kind, oid = header.decode("ascii").split()
            name = name.decode("utf-8")
            if mode in {"100644", "100755"} and kind == "blob" and name.endswith(".md"):
                indexes[name] = oid
        candidates = ("README.md", "spec.md", *sorted(indexes))
        object_id = next(
            (indexes[name] for name in candidates if name in indexes), None
        )
        if object_id is None:
            return ()
    if not isinstance(object_id, str) or not re.fullmatch(
        r"[0-9a-f]{40}|[0-9a-f]{64}", object_id
    ):
        return None
    blob = _run_git(root, ["cat-file", "blob", object_id])
    if blob.returncode:
        return None
    try:
        return _headings(blob.stdout.decode("utf-8"))
    except UnicodeError:
        return None


def _historical_link_findings(graph, links, sources, registry, legacy_units=()):
    """Resolve frozen links at their capture, never against today's checkout."""
    from scripts.lib.document_governance.archive import retention_unit
    from scripts.lib.document_governance.archive_snapshots import is_legacy_capture
    from scripts.lib.document_governance.git_provenance import (
        verify_recovery_blobs_batch,
    )

    findings = []
    requests = []
    generations = {}
    unrecorded = 0
    for link in links:
        relative = link.source.as_posix().removeprefix("docs/98.archive/")
        unit = retention_unit(relative)
        if unit not in sources:
            unrecorded += 1
            continue
        if unit not in generations:
            generations[unit] = unit in legacy_units or is_legacy_capture(
                graph.repo_root, unit, registry
            )
        severity = "warning" if generations[unit] else "error"
        commit, origin = sources[unit]
        member = relative[len(unit) :] if unit.endswith("/") else ""
        original = (
            pathlib.PurePosixPath(origin) / member
            if member
            else pathlib.PurePosixPath(origin)
        )
        resolved = _normalized_target(original, link.raw_target)
        if resolved is None:
            continue
        target, fragment, absolute, outside = resolved
        if absolute or outside or link.has_unsafe_target:
            findings.append(
                LinkFinding(
                    f"{link.source}:{link.line}",
                    "historical-link-unsafe-target",
                    _diagnostic_text(link.raw_target),
                    severity,
                )
            )
            continue
        requests.append((link, target, fragment, commit, severity))
    identities = tuple(
        dict.fromkeys((target, commit) for _, target, _, commit, _ in requests)
    )
    proven = {}
    for offset in range(0, len(identities), 512):
        batch = identities[offset : offset + 512]
        proven.update(
            zip(
                batch,
                verify_recovery_blobs_batch(batch, repo_root=graph.repo_root),
                strict=True,
            )
        )
    heading_cache = {}
    for link, target, fragment, commit, severity in requests:
        result = proven[target, commit]
        code = None
        if not result.exists:
            code = "historical-link-missing-target"
        elif not result.is_regular_blob and result.object_type != "tree":
            code = "historical-link-unsafe-target"
        elif fragment:
            if result.object_id not in heading_cache:
                heading_cache[result.object_id] = _historical_headings(
                    graph.repo_root, result
                )
            headings = heading_cache[result.object_id]
            if headings is None:
                code = "historical-link-unreadable-target"
            elif fragment not in headings:
                code = "historical-link-missing-anchor"
        if code:
            findings.append(
                LinkFinding(
                    f"{link.source}:{link.line}",
                    code,
                    _diagnostic_text(f"{commit}:{target}: {link.raw_target}"),
                    severity,
                )
            )
    if unrecorded:
        findings.append(
            LinkFinding(
                "docs/98.archive/retention-catalog.md",
                "historical-links-unrecorded",
                f"{unrecorded} legacy links have no capture source; historical resolution unverified",
                "warning",
            )
        )
    return findings


def _sealed_route_sources(graph, registry):
    """Unchanged sealed route records retain their last authored Git context."""
    from scripts.lib.document_governance.git_provenance import _run_git

    sources = {}
    legacy = set()
    linked = {link.source for link in graph.links}
    for node in graph.nodes:
        path = node.path.as_posix()
        if (
            node.path not in linked
            or not path.startswith(_ROUTE_RECORD_PREFIXES)
            or node.metadata.get("status") != "sealed"
        ):
            continue
        head = _run_git(graph.repo_root, ["cat-file", "blob", f"HEAD:{path}"])
        if head.returncode or head.stdout != node.text.encode("utf-8"):
            continue
        changed = _run_git(
            graph.repo_root, ["log", "-1", "--format=%H", "HEAD", "--", path]
        )
        commit = changed.stdout.decode("ascii").strip()
        if changed.returncode or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("sealed route source unavailable")
        unit = path.removeprefix("docs/98.archive/")
        sources[unit] = (commit, path)
        revision = registry.common["archive_retention"]["legacy_capture_revision"]
        baseline = _run_git(graph.repo_root, ["cat-file", "blob", f"{revision}:{path}"])
        if not baseline.returncode and baseline.stdout == head.stdout:
            legacy.add(unit)
    return sources, frozenset(legacy)


def _archive_link_context(root):
    """Load the adopted contract; pre-contract fixture trees keep legacy routing."""
    from scripts.lib.document_governance.archive_assessments import (
        assessment_lookup,
        capture_sources,
        retention_contract_enabled,
    )

    if not retention_contract_enabled(root):
        return None, {}, {}
    path = pathlib.Path("docs/99.templates/registry.json")
    raw = json.loads(read_bounded_regular(root, path))
    if not isinstance(raw, Mapping) or not isinstance(raw.get("common", {}), Mapping):
        raise ValueError("Archive Registry is not an object")
    if raw["common"].get("archive_disposition_model") != ARCHIVE_MODEL_ADOPTED:
        raise ValueError("Archive retention requires the adopted disposition model")
    contract = raw["common"]["archive_retention"]
    if (
        not isinstance(contract, Mapping)
        or not isinstance(contract.get("blocked_assessments"), list)
        or not all(isinstance(value, str) for value in contract["blocked_assessments"])
        or not isinstance(contract.get("history_only_availability"), str)
        or not isinstance(contract.get("legacy_capture_revision"), str)
    ):
        raise ValueError("Archive retention contract is malformed")
    registry = load_registry(root / path)
    return registry, assessment_lookup(root, registry), capture_sources(root, registry)


def check_alignment(graph: DocumentGraph) -> list[LinkFinding]:
    """Validate current local links, archive boundaries, anchors, and old templates."""

    findings: list[LinkFinding] = list(graph.input_findings)
    nodes = _node_map(graph)
    preserved_prefixes = _preserved_link_prefixes(graph)
    try:
        registry, assessments, sources = _archive_link_context(graph.repo_root)
    except (OSError, ValueError, TypeError, KeyError, OperationsAuthorityError):
        registry, assessments, sources = None, {}, {}
        findings.append(
            LinkFinding(
                "docs/98.archive/retention-catalog.md",
                "archive-link-contract-invalid",
                "cannot resolve Archive assessment/source contract",
            )
        )
    route_sources = {}
    if registry is not None:
        try:
            route_sources, legacy_routes = _sealed_route_sources(graph, registry)
            historical = tuple(
                link
                for link in graph.links
                if link.source.as_posix().startswith(preserved_prefixes)
                or link.source.as_posix().removeprefix("docs/98.archive/")
                in route_sources
            )
            findings.extend(
                _historical_link_findings(
                    graph,
                    historical,
                    {**sources, **route_sources},
                    registry,
                    legacy_routes,
                )
            )
        except (OSError, ValueError, TypeError, KeyError):
            findings.append(
                LinkFinding(
                    "docs/98.archive/retention-catalog.md",
                    "historical-link-source-invalid",
                    "bounded historical source validation failed",
                )
            )
    citable_prefixes = (
        _ADOPTED_CITABLE_ARCHIVE_PREFIXES
        if archive_disposition_model(graph.repo_root) == ARCHIVE_MODEL_ADOPTED
        else (_CITABLE_ARCHIVE_PREFIX,)
    )
    for link in graph.links:
        if (
            link.source.as_posix().startswith(preserved_prefixes)
            or link.source.as_posix().removeprefix("docs/98.archive/") in route_sources
        ):
            # The historical pass above owns frozen outbound links.
            continue
        if link.absolute:
            findings.append(_finding(link, "absolute-local-link", link.raw_target))
            continue
        if link.outside_repository:
            findings.append(_finding(link, "link-outside-repository", link.raw_target))
            continue
        if link.has_unsafe_target:
            findings.append(_finding(link, "unsafe-local-link", link.raw_target))
        target_text = link.target.as_posix()
        if registry is not None and target_text.startswith("docs/98.archive/"):
            relative = target_text.removeprefix("docs/98.archive/")
            matches = [
                value
                for unit, value in assessments.items()
                if relative == unit.rstrip("/")
                or (unit.endswith("/") and relative.startswith(unit))
            ]
            if len(matches) > 1:
                findings.append(
                    _finding(
                        link,
                        "archive-link-contract-invalid",
                        "ambiguous assessment unit",
                    )
                )
            assessment = matches[0] if len(matches) == 1 else None
            contract = registry.common["archive_retention"]
            if assessment is not None and (
                assessment.assessment in contract["blocked_assessments"]
                or assessment.availability == contract["history_only_availability"]
            ):
                findings.append(
                    _finding(link, "archive-assessment-link", link.raw_target)
                )
        outside_archive = not link.source.as_posix().startswith("docs/98.archive/")
        if (
            outside_archive
            and target_text.startswith("docs/98.archive/")
            and target_text != "docs/98.archive/README.md"
            and not target_text.startswith(citable_prefixes)
            and (
                target_text.startswith(_ROUTE_RECORD_PREFIXES)
                or _document_profile(nodes, link.source) not in _ARCHIVE_CITING_PROFILES
            )
        ):
            findings.append(_finding(link, "active-archive-link", link.raw_target))
        target_path, target_error = _regular_target(graph, link.target)
        if target_path is None:
            findings.append(
                _finding(link, target_error or "missing-link-target", link.raw_target)
            )
            continue
        if link.fragment:
            headings, heading_error = _target_headings(graph, nodes, link.target)
            if heading_error is not None:
                findings.append(_finding(link, heading_error, link.raw_target))
            elif headings is not None and link.fragment not in headings:
                findings.append(_finding(link, "missing-link-anchor", link.raw_target))
    for node in graph.nodes:
        for line_no, line in _unfenced_lines(node.text):
            if "operation.template.md" in line:
                findings.append(
                    LinkFinding(
                        f"{node.path.as_posix()}:{line_no}",
                        "removed-template-name",
                        "operation.template.md",
                    )
                )
    return sorted(set(findings))


def _link_targets(graph: DocumentGraph, source: pathlib.PurePosixPath) -> set[str]:
    return {
        link.target.as_posix()
        for link in graph.links
        if link.source == source and not link.outside_repository
    }


def traceability_pair_total(graph: DocumentGraph) -> int:
    catalog = pathlib.PurePosixPath(
        "docs/05.operations/policies/0006-infrastructure-optimization-governance.md"
    )
    node = _node_map(graph).get(catalog)
    return 0 if node is None else len(_CATALOG_PAIR.findall(node.text))


def archive_direct_link_total(graph: DocumentGraph) -> int:
    """Count active-stage links that cross directly into archived evidence."""

    return sum(
        1
        for link in graph.links
        if link.source.as_posix().startswith(_ACTIVE_STAGE_PREFIXES)
        and link.target.as_posix().startswith("docs/98.archive/")
        and link.target.as_posix() != "docs/98.archive/README.md"
        and not link.target.as_posix().startswith("docs/98.archive/migrations/")
    )


def removed_template_mention_total(graph: DocumentGraph) -> int:
    return sum(
        1
        for node in graph.nodes
        for _, line in _unfenced_lines(node.text)
        if "operation.template.md" in line
    )


def check_traceability(graph: DocumentGraph) -> list[LinkFinding]:
    """Validate reciprocal Stage 03/05 routing and every catalog OPER/RUN pair."""

    findings: list[LinkFinding] = list(graph.input_findings)
    nodes = _node_map(graph)
    specs = pathlib.PurePosixPath("docs/03.specs/README.md")
    operations = pathlib.PurePosixPath("docs/05.operations/README.md")
    catalog = pathlib.PurePosixPath(
        "docs/05.operations/policies/0006-infrastructure-optimization-governance.md"
    )
    for path in (specs, operations, catalog):
        if path not in nodes:
            findings.append(
                LinkFinding(
                    path.as_posix(), "traceability-file-missing", path.as_posix()
                )
            )
    if specs in nodes and operations.as_posix() not in _link_targets(graph, specs):
        findings.append(
            LinkFinding(
                specs.as_posix(), "operations-index-link-missing", operations.as_posix()
            )
        )
    if operations in nodes and specs.as_posix() not in _link_targets(graph, operations):
        findings.append(
            LinkFinding(
                operations.as_posix(), "spec-index-link-missing", specs.as_posix()
            )
        )
    catalog_node = nodes.get(catalog)
    if catalog_node is not None:
        for oper_raw, run_raw in _CATALOG_PAIR.findall(catalog_node.text):
            for role, raw in (("OPER", oper_raw), ("RUN", run_raw)):
                resolved = _normalized_target(catalog, raw)
                if resolved is None:
                    findings.append(
                        LinkFinding(
                            catalog.as_posix(),
                            "catalog-target-invalid",
                            f"{role}:{raw}",
                        )
                    )
                    continue
                target, _, _, outside = resolved
                target_path, _ = _regular_target(graph, target)
                if outside or target_path is None:
                    findings.append(
                        LinkFinding(
                            catalog.as_posix(),
                            "catalog-target-missing",
                            f"{role}:{raw}",
                        )
                    )
    return sorted(set(findings))


def _entrypoint_target(
    graph: DocumentGraph, source: pathlib.PurePosixPath, raw: str
) -> pathlib.PurePosixPath | None:
    """Normalize routing spellings only; never fetch a URL or resolve a path."""

    value = urllib.parse.unquote(html.unescape(raw)).replace("\\", "/").casefold()
    if _URL.match(value) or value.startswith("//"):
        try:
            url = urllib.parse.urlsplit(value)
        except ValueError:
            return None
        if url.scheme == "file" and url.hostname in {None, "localhost"}:
            value = url.path
        else:
            # Explicit identity keeps offline/source-only graphs deterministic.
            own = "/buenhyden/hy-home.docker/"
            if not url.path.startswith(own):
                return None
            tail = url.path[len(own) :]
            if url.hostname == "github.com" and tail.startswith(("blob/", "raw/")):
                tail = tail.split("/", 1)[1]
            elif url.hostname != "raw.githubusercontent.com":
                return None
            # Git refs may contain slashes; conservatively classify the docs
            # suffix without resolving the ref against a network or Git state.
            stage = re.search(r"/(docs/[0-9]{2}\.[^/]+(?:/.*)?)$", tail)
            if stage is None:
                return None
            value = stage[1]
    root = graph.repo_root.as_posix().casefold().rstrip("/") + "/"
    if value.startswith(root):
        value = value[len(root) :]
    resolved = _normalized_target(
        pathlib.PurePosixPath(source.as_posix().casefold()), value
    )
    if resolved is None:
        return None
    target = resolved[0]
    path = re.split(r"[?#]", value, maxsplit=1)[0]
    directory = len(target.parts) == 2 or (path.endswith("/") and not target.suffix)
    if target.name == "readme.md" or directory:
        return None
    return target


def check_entrypoint(graph: DocumentGraph) -> list[LinkFinding]:
    """Reject outside-docs individual stage links, retaining navigation routes.

    Fenced clickable forms are checked too; literal examples and provenance
    remain semantic review inputs, not mechanically inferred authority.
    """

    findings: list[LinkFinding] = list(graph.input_findings)
    for node in graph.nodes:
        if node.path.as_posix().casefold().startswith(f"{_DOC_ROOT}/"):
            continue
        lines = tuple(_unfenced_lines(node.text, include_fenced=True))
        destinations = list(_link_destinations(lines))
        destinations.extend(
            (number, "", match[1])
            for number, text in lines
            for match in re.finditer(
                r"<((?:https?|file)://[^<>\s]+)>", _without_inline_code(text), re.I
            )
        )
        for line, _, raw in destinations:
            target = _entrypoint_target(graph, node.path, raw)
            if target is not None and _STAGE_DIRECTORY.match(target.as_posix()):
                findings.append(
                    LinkFinding(
                        f"{node.path.as_posix()}:{line}", "stage-link-outside-docs", raw
                    )
                )
    return sorted(set(findings))


_TREE_BRANCH = re.compile(r"(?:├──|└──|\|--|`--) ")
_NAVIGATION_IGNORED_CHILDREN = frozenset({"README.md", ".gitkeep"})
_FROZEN_README_PREFIX = "docs/98.archive/"


def _tracked_files(root: pathlib.Path) -> frozenset[str] | None:
    """Return the repository's tracked paths, or None when Git cannot list them."""

    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        return None
    return frozenset(item for item in result.stdout.decode("utf-8").split("\0") if item)


def _direct_children(
    tracked: frozenset[str], directory: str
) -> tuple[set[str], set[str]]:
    """Split a directory's tracked children into (directories, files)."""

    prefix = f"{directory}/" if directory else ""
    directories: set[str] = set()
    files: set[str] = set()
    for path in tracked:
        if not path.startswith(prefix):
            continue
        rest = path[len(prefix) :]
        head, separator, _ = rest.partition("/")
        if separator:
            directories.add(head)
        elif head not in _NAVIGATION_IGNORED_CHILDREN:
            files.add(head)
    return directories, files


def _fenced_lines(text: str) -> Iterable[tuple[int, str]]:
    """Yield the lines inside fenced code blocks."""

    fence: str | None = None
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker = next((m for m in ("```", "~~~") if stripped.startswith(m)), None)
        if marker is not None and (fence is None or fence == marker):
            fence = None if fence else marker
            continue
        if fence is not None:
            yield line_no, line


def _navigation_destinations(node: DocumentNode) -> Iterable[tuple[int, str, str]]:
    """Include unused reference definitions in the router's destinations.

    The graph includes reference uses and HTML links; a router must also not
    hide descendant enumeration in an unused reference definition.
    """

    for line_no, line in _unfenced_lines(node.text):
        match = _REFERENCE_DEFINITION.match(line)
        if match:
            yield line_no, "", match.group(2)
        for start, end in _html_tag_spans(line):
            tag = line[start:end]
            if not tag.endswith(">"):
                continue
            for href in _html_href_values(tag):
                yield line_no, "", href


def _raw_label(lines: list[str], link: DocumentLink) -> str:
    """Recover a label whose inline code the link parser blanked."""

    if link.label.strip() or not 0 < link.line <= len(lines):
        return link.label
    match = re.search(
        r"\[([^\]]*)\]\(<?" + re.escape(link.raw_target), lines[link.line - 1]
    )
    return match.group(1) if match else link.label


def check_navigation(graph: DocumentGraph) -> list[LinkFinding]:
    """Keep a folder router's links to its direct children.

    A README whose directory holds only subdirectories (besides itself and a
    `.gitkeep`) routes readers one level down. Listing documents inside those
    children duplicates membership the children own and drifts as soon as a
    child changes, which is how the Stage 03 index came to carry Plan and Task
    rows. Links outside the router's own subtree are citations, not listings.
    """

    tracked = _tracked_files(graph.repo_root)
    if tracked is None:
        # Without the tracked tree no README can be classified; passing
        # silently would hide every router finding.
        return sorted(
            {
                *graph.input_findings,
                LinkFinding(
                    ".",
                    "navigation-tree-unavailable",
                    "git ls-files failed; folder routers cannot be classified",
                ),
            }
        )
    tracked_directories = {str(pathlib.PurePosixPath(path).parent) for path in tracked}
    tracked_directories |= {
        parent.as_posix()
        for path in tracked
        for parent in pathlib.PurePosixPath(path).parents
    }
    findings: list[LinkFinding] = list(graph.input_findings)
    for node in graph.nodes:
        if node.path.name != "README.md":
            continue
        # Frozen Stage 98 bodies keep the contract they were preserved under.
        if node.path.as_posix().startswith(_FROZEN_README_PREFIX):
            continue
        directory = node.path.parent
        directory_text = "" if directory.as_posix() == "." else directory.as_posix()
        children, files = _direct_children(tracked, directory_text)
        router = bool(children) and not files
        source_lines = node.text.splitlines()
        destinations = [
            (link.line, _raw_label(source_lines, link), link.target)
            for link in graph.links
            if link.source == node.path
        ]
        for line_no, label, raw in _navigation_destinations(node):
            resolved = _normalized_target(node.path, raw)
            if resolved is not None:
                destinations.append((line_no, label, resolved[0]))
        where = f"{node.path.as_posix()}"
        for line_no, label, target in destinations:
            target_text = target.as_posix()
            folder_label = label.strip().strip("`*_ ")
            if folder_label.endswith("/"):
                folder = (
                    target.parent
                    if target.name == "README.md"
                    else target
                    if target_text in tracked_directories
                    else None
                )
                wanted = folder_label.rstrip("/")
                if folder is None or not (
                    wanted in {".", ".."}
                    or f"/{folder.as_posix()}".endswith(f"/{wanted}")
                ):
                    findings.append(
                        LinkFinding(
                            f"{where}:{line_no}",
                            "navigation-label-mismatch",
                            f"folder label {label.strip()} resolves to {target_text}",
                        )
                    )
            if not router or target == directory:
                continue
            try:
                parts = target.relative_to(directory).parts
            except ValueError:
                continue
            if len(parts) >= 2 and parts[1:] != ("README.md",):
                findings.append(
                    LinkFinding(
                        f"{where}:{line_no}",
                        "navigation-descendant-link",
                        f"folder router links inside a child: {target_text}",
                    )
                )
        if not router:
            continue
        branches = [
            (line_no, branch.start(), line[branch.end() :])
            for line_no, line in _fenced_lines(node.text)
            if (branch := _TREE_BRANCH.search(line)) is not None
        ]
        # Trees indent each level by a fixed width that varies between
        # diagrams (3 or 4 columns); the smallest nonzero indent is one level.
        unit = min((start for _, start, _ in branches if start), default=4)
        subtree_directories = {
            pathlib.PurePosixPath(path).name
            for path in tracked_directories
            if directory_text and path.startswith(f"{directory_text}/")
        }
        for line_no, start, rest in branches:
            depth = start // unit + 1
            name = rest.split("#", 1)[0].strip().split(" ")[0]
            if (
                depth >= 2
                and name
                and not name.endswith("/")
                and name != "README.md"
                and name not in subtree_directories
                and "<" not in name
            ):
                findings.append(
                    LinkFinding(
                        f"{where}:{line_no}",
                        "navigation-descendant-tree",
                        f"folder router tree names a file inside a child: {name}",
                    )
                )
    return sorted(set(findings))


def check_language(graph: DocumentGraph) -> list[LinkFinding]:
    """Hold every document to the language its Registry profile declares.

    SPEC-0187 migrated the corpus, so every document is judged, not only the
    ones a change touches. A profile with no declared language, such as a
    Stage 98 record or a generated adapter, is not judged.
    """

    registry = load_registry()
    findings: list[LinkFinding] = list(graph.input_findings)
    for node in graph.nodes:
        profile_id = classify_path(node.path.as_posix(), registry)
        declared = registry.profiles.get(profile_id or "", {}).get("language")
        if not isinstance(declared, str):
            continue
        reason = language_mismatch(node.text, declared)
        if reason is not None:
            findings.append(
                LinkFinding(node.path.as_posix(), "document-language-mismatch", reason)
            )
    return sorted(set(findings))


_COMMAND_FENCE_LANGUAGES = frozenset({"", "bash", "sh", "shell", "console", "zsh"})
_ILLUSTRATIVE_COMMAND_MARKER = "# doc-paths: illustrative"
_COMMAND_PATHS_UNTRACKED_BY_DESIGN = ("secrets/",)
_COMMAND_PATH_PLACEHOLDERS = "<>${}*"
_COMMAND_PATH_TOKEN = re.compile(
    r"(?<![\w./-])\.?/?([A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+)"
)


def _command_blocks(text: str) -> Iterable[tuple[int, tuple[str, ...]]]:
    """Yield the first content line number and body of each command fence."""

    fence: str | None = None
    language = ""
    start = 0
    buffer: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker = (
            "```"
            if stripped.startswith("```")
            else "~~~"
            if stripped.startswith("~~~")
            else None
        )
        if marker is None:
            if fence is not None:
                buffer.append(line)
            continue
        if fence is None:
            fence = marker
            language = stripped[len(marker) :].strip().lower()
            start = line_no + 1
            buffer = []
            continue
        if fence == marker:
            if language in _COMMAND_FENCE_LANGUAGES:
                yield start, tuple(buffer)
            fence = None
            language = ""
            buffer = []


def check_commands(graph: DocumentGraph) -> list[LinkFinding]:
    """Report a fenced command that names a repository path nothing resolves.

    A reader runs what a command block says. When the block names a script the
    tree no longer carries, the document sends them at a path that cannot be
    opened, and no link check sees it because a fenced line is not a link.

    Only the repository's own top-level surfaces are candidates, so a URL, a
    flag, or an unrelated word with a slash is not read as a path. `secrets/`
    is excluded because those files are created by the operator and are
    untracked by design, and a preserved body under `docs/98.archive/` is
    excluded because naming a path the tree has since dropped is what a
    preserved record is for and its bytes may not be edited to satisfy a check. A block whose paths are illustrative rather than
    runnable declares that on its own first line with the stated marker, which
    keeps the exemption visible in the document instead of in a predicate.
    """

    root = graph.repo_root
    surfaces = {entry.name for entry in root.iterdir()} if root.is_dir() else set()
    findings: list[LinkFinding] = []
    preserved_prefixes = _preserved_link_prefixes(graph)
    for node in graph.nodes:
        if node.path.as_posix().startswith(preserved_prefixes):
            continue
        for start, lines in _command_blocks(node.text):
            if any(line.strip() == _ILLUSTRATIVE_COMMAND_MARKER for line in lines):
                continue
            for offset, line in enumerate(lines):
                if line.lstrip().startswith("#"):
                    continue
                for match in _COMMAND_PATH_TOKEN.finditer(line):
                    token = match.group(1).rstrip(".,;:)")
                    if any(char in token for char in _COMMAND_PATH_PLACEHOLDERS):
                        continue
                    if token.split("/", 1)[0] not in surfaces:
                        continue
                    if token.startswith(_COMMAND_PATHS_UNTRACKED_BY_DESIGN):
                        continue
                    if (root / token).exists():
                        continue
                    findings.append(
                        LinkFinding(
                            path=f"{node.path}:{start + offset}",
                            code="document-command-path-missing",
                            message=(
                                f"fenced command names {token}, which the tree "
                                "does not carry"
                            ),
                        )
                    )
    return sorted(set(findings))


MODE_HANDLERS = {
    "traceability": check_traceability,
    "alignment": check_alignment,
    "entrypoint": check_entrypoint,
    "commands": check_commands,
    "navigation": check_navigation,
    "language": check_language,
}


def run_mode(mode: str, graph: DocumentGraph) -> list[LinkFinding]:
    """Run one registered link mode or reject the unknown mode."""

    try:
        handler = MODE_HANDLERS[mode]
    except KeyError as error:
        raise ValueError(f"unsupported link-check mode: {mode}") from error
    return handler(graph)
