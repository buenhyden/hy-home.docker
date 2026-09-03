"""Shared Markdown document graph and deterministic link validators."""

from __future__ import annotations

import dataclasses
import pathlib
import posixpath
import re
import urllib.parse
from collections.abc import Iterable, Mapping
from types import MappingProxyType

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)


_URL = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_LINK_OPEN = re.compile(r"(?<!!)\[(?P<label>[^\]]*)\]\(")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
_CATALOG_PAIR = re.compile(r"\[OPER\]\(([^)]+)\),\s*\[RUN\]\(([^)]+)\)")
_ACTIVE_STAGE_PREFIXES = (
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
)
_ROOT_PREFIXES = (
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
        "AGENTS.md",
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


def _unfenced_lines(text: str) -> Iterable[tuple[int, str]]:
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
        if fence is None:
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


def _markdown_destinations(line: str) -> Iterable[tuple[str, str]]:
    """Yield labeled destinations with angle and nested-parenthesis support."""

    text = _without_inline_code(line)
    for opening in _LINK_OPEN.finditer(text):
        cursor = opening.end()
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text):
            continue
        if text[cursor] == "<":
            closing = text.find(">", cursor + 1)
            if closing >= 0:
                yield opening.group("label"), text[cursor + 1 : closing]
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
                        yield opening.group("label"), destination.split(maxsplit=1)[0]
                    break
                depth -= 1
            elif character.isspace() and depth == 0:
                destination = text[start:cursor]
                if destination:
                    yield opening.group("label"), destination
                break
            cursor += 1


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


def parse_local_markdown_links(
    source: pathlib.PurePosixPath,
    text: str,
) -> tuple[DocumentLink, ...]:
    """Parse normalized local links from supplied Markdown without filesystem I/O."""

    links: list[DocumentLink] = []
    for line_no, line in _unfenced_lines(text):
        for label, raw in _markdown_destinations(line):
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
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            input_findings.append(
                LinkFinding(
                    relative.as_posix(), "document-invalid-utf8", relative.as_posix()
                )
            )
            continue
        except OSError:
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


def _finding(link: DocumentLink, code: str, message: str) -> LinkFinding:
    return LinkFinding(f"{link.source.as_posix()}:{link.line}", code, message)


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
    try:
        return _headings(path.read_text(encoding="utf-8")), None
    except UnicodeError:
        return None, "link-target-invalid-utf8"
    except OSError:
        return None, "link-target-unreadable"


def check_alignment(graph: DocumentGraph) -> list[LinkFinding]:
    """Validate current local links, archive boundaries, anchors, and old templates."""

    findings: list[LinkFinding] = list(graph.input_findings)
    nodes = _node_map(graph)
    for link in graph.links:
        if link.absolute:
            findings.append(_finding(link, "absolute-local-link", link.raw_target))
            continue
        if link.outside_repository:
            findings.append(_finding(link, "link-outside-repository", link.raw_target))
            continue
        target_text = link.target.as_posix()
        active_source = link.source.as_posix().startswith(_ACTIVE_STAGE_PREFIXES)
        if (
            active_source
            and target_text.startswith("docs/98.archive/")
            and target_text != "docs/98.archive/README.md"
            and not target_text.startswith("docs/98.archive/migrations/")
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
        "docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md"
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
        "docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md"
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


MODE_HANDLERS = {
    "traceability": check_traceability,
    "alignment": check_alignment,
}


def run_mode(mode: str, graph: DocumentGraph) -> list[LinkFinding]:
    """Run one registered link mode or reject the unknown mode."""

    try:
        handler = MODE_HANDLERS[mode]
    except KeyError as error:
        raise ValueError(f"unsupported link-check mode: {mode}") from error
    return handler(graph)
