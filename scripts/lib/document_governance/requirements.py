"""Bounded immutable parsing for canonical Stage 01 Requirement Packages."""

from __future__ import annotations

import dataclasses
import json
import os
import pathlib
import re
import stat

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    IdentitySpace,
    RequirementAllocationBaseline,
    load_registry,
    validate_requirement_allocation_transition,
)


MAX_REQUIREMENT_BYTES = 512 * 1024
MAX_REQUIREMENT_ITEMS = 2048
_PACKAGE_PATH = re.compile(r"(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md")
_SECTION = re.compile(r"(?ms)^## (?P<name>[^\n]+)\n(?P<body>.*?)(?=^## |\Z)")
_LIST_DECLARATION = re.compile(
    r"^[ \t]*[-*+]\s+\*\*(?P<identity>REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4})"
    r"(?:\s+—\s+[^*]+)?\*\*:\s*(?P<text>.*)$"
)
_TABLE_DECLARATION = re.compile(
    r"^\s*\|\s*(?P<identity>REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4})\s*\|"
    r"(?P<text>.*)\|\s*$"
)
_FULL_CHILD_ID = re.compile(
    r"REQ-(?P<package>[0-9]{4})-(?P<kind>FR|NFR|IF)-(?P<number>[0-9]{4})"
)
_RETIRED_ID = re.compile(
    r"(?<![A-Za-z0-9-])(?:(?:PRD|SRS|IFR)-[A-Za-z0-9-]+|"
    r"interface-[0-9]{4}(?:-[a-z0-9-]+)?)(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
_LEGACY_REQUIREMENT_PATH = re.compile(
    r"docs/01\.requirements/(?:prd|srs|ifr|interface)-", re.IGNORECASE
)
_BARE_CHILD_ID = re.compile(
    r"(?<![A-Za-z0-9-])(?:FR|NFR|IF)-[0-9]{4}(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
_OPENAPI_YAML = re.compile(
    r"(?mix)(?:^|[{,])[ \t]*(?:>\s*)?[\"']?"
    r"(?P<kind>openapi|swagger)[\"']?[ \t\r\n]*:[ \t\r\n]*"
    r"(?:(?:![!A-Za-z0-9_./:-]+|&[A-Za-z_][A-Za-z0-9_-]*)[ \t\r\n]*){0,4}"
    r"[\"']?(?P<version>3(?:\.[0-9]+)+|2(?:\.0)?)[\"']?"
    r"(?=[ \t\r\n,#}])"
)
_YAML_VERSION_ANCHOR = re.compile(
    r"(?mix)&(?P<anchor>[A-Za-z_][A-Za-z0-9_-]*)[ \t\r\n]+"
    r"[\"']?(?P<version>3(?:\.[0-9]+)+|2(?:\.0)?)[\"']?"
)
_OPENAPI_YAML_ALIAS = re.compile(
    r"(?mix)(?:^|[{,])[ \t]*(?:>\s*)?[\"']?"
    r"(?P<kind>openapi|swagger)[\"']?[ \t\r\n]*:[ \t\r\n]*"
    r"\*(?P<anchor>[A-Za-z_][A-Za-z0-9_-]*)"
)
_OPENAPI_BLOCK_SCALAR_HEADER = re.compile(
    r"(?i)[\"']?(?P<kind>openapi|swagger)[\"']?[ \t]*:[ \t]*"
    r"(?P<scalar>[>|][+-]?)(?:[ \t]+#[^\n]*)?"
)
_OPENAPI_BLOCK_SCALAR_VERSION = re.compile(
    r"[\"']?(?P<version>3(?:\.[0-9]+)+|2(?:\.0)?)[\"']?"
    r"(?:[ \t]+#[^\n]*)?"
)
_JSON_STRING_PAIR = re.compile(
    r'(?P<key>"(?:\\.|[^"\\])*")\s*:\s*'
    r'(?P<value>"(?:\\.|[^"\\])*")'
)
_GRAPHQL_DECLARATION_START = re.compile(
    r"(?mi)^[ \t]*(?:>[ \t]*)*(?P<declaration>"
    r"extend|schema|type|interface|input|enum)\b"
)
_GRAPHQL_LEAF_DECLARATION = re.compile(
    r"(?mix)^[ \t]*(?:>[ \t]*)?(?:extend[ \t\r\n]+)?(?:"
    r"scalar[ \t\r\n]+[A-Za-z_][A-Za-z0-9_]*|"
    r"union[ \t\r\n]+[A-Za-z_][A-Za-z0-9_]*[ \t\r\n]*=|"
    r"directive[ \t\r\n]+@[A-Za-z_][A-Za-z0-9_]*)"
)
_PROTO_SYNTAX = re.compile(
    r"(?mi)^[ \t]*(?:>\s*)?syntax\s*=\s*[\"']proto[23][\"']\s*;"
)
_PROTO_MESSAGE = re.compile(
    r"(?mi)^[ \t]*(?:>\s*)?message\s+[A-Za-z_][A-Za-z0-9_]*\s*\{"
)
_PROTO2_FIELD = re.compile(
    r"(?mi)^[ \t]*(?:>\s*)?(?:required|optional|repeated)\s+"
    r"[A-Za-z_][A-Za-z0-9_.<> ,]*\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*"
    r"[1-9][0-9]*\s*(?:\[[^\n\]]*\])?\s*;"
)
_PROTO2_INLINE_MESSAGE = re.compile(
    r"(?mi)^[ \t]*(?:>\s*)?message\s+[A-Za-z_][A-Za-z0-9_]*\s*\{"
    r"[^\n{}]{0,2048}\b(?:required|optional|repeated)\s+"
    r"[A-Za-z_][A-Za-z0-9_.<> ,]*\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*"
    r"[1-9][0-9]*\s*(?:\[[^\n\]]*\])?\s*;"
)
_PROTO_SERVICE_START = re.compile(
    r"(?mi)^[ \t]*(?:>[ \t]*)*(?P<declaration>service)\b"
)
_SYNTAX_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|'
    r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+(?:\.[0-9]+)*|"
    r"[@{}()[\]:!&|=,;.$<>+\-/]"
)
_EXECUTABLE_SCAN_CHARS = 8192
_EXECUTABLE_TOKEN_LIMIT = 4096
_EXECUTABLE_SUFFIXES = frozenset({".graphql", ".proto", ".yaml", ".yml"})
_SECTION_KINDS = {
    "Functional Requirements": "FR",
    "Non-functional Requirements": "NFR",
    "Interface Requirements": "IF",
}


class RequirementPackageError(ValueError):
    """Raised when a Stage 01 package or stage boundary is not trustworthy."""


@dataclasses.dataclass(frozen=True, order=True)
class RequirementItem:
    """One immutable, package-owned requirement declaration."""

    identity: str
    kind: str
    text: str
    line_number: int


@dataclasses.dataclass(frozen=True)
class RequirementPackage:
    """One validated Requirement Package."""

    path: pathlib.PurePosixPath
    artifact_id: str
    status: str
    items: tuple[RequirementItem, ...]


def _contains_retired_requirement_reference(text: str) -> bool:
    """Return whether live Requirement text uses any retired identity shape."""

    return bool(
        _RETIRED_ID.search(text)
        or _LEGACY_REQUIREMENT_PATH.search(text)
        or _BARE_CHILD_ID.search(text)
    )


def _openapi_kind_matches_version(kind: str, version: str) -> bool:
    return (kind.lower() == "openapi" and version.startswith("3.")) or (
        kind.lower() == "swagger" and version in {"2", "2.0"}
    )


def _contains_openapi_yaml(text: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        candidate = line.lstrip(" \t")
        while candidate.startswith(">"):
            candidate = candidate[1:].lstrip(" \t")
        header = _OPENAPI_BLOCK_SCALAR_HEADER.fullmatch(candidate)
        if header is None:
            continue
        for continuation in lines[index + 1 : index + 9]:
            value = continuation.lstrip(" \t")
            while value.startswith(">"):
                value = value[1:].lstrip(" \t")
            if not value or value.startswith("#"):
                continue
            version = _OPENAPI_BLOCK_SCALAR_VERSION.fullmatch(value)
            if version and _openapi_kind_matches_version(
                header.group("kind"), version.group("version")
            ):
                return True
            break
    for match in _OPENAPI_YAML.finditer(text):
        if _openapi_kind_matches_version(
            match.group("kind"), match.group("version")
        ):
            return True
    anchors: dict[str, str] = {}
    for index, match in enumerate(_YAML_VERSION_ANCHOR.finditer(text)):
        if index >= MAX_REQUIREMENT_ITEMS:
            break
        anchors[match.group("anchor")] = match.group("version")
    for alias in _OPENAPI_YAML_ALIAS.finditer(text):
        version = anchors.get(alias.group("anchor"))
        if version and _openapi_kind_matches_version(alias.group("kind"), version):
            return True
    return False


def _strip_syntax_comments(
    text: str,
    *,
    line_marker: str,
    block_comments: bool = False,
) -> str:
    """Replace bounded language comments with whitespace while preserving strings."""

    characters = list(text)
    index = 0
    quote = ""
    while index < len(characters):
        character = characters[index]
        if quote:
            if character == "\\":
                index += 2
                continue
            if character == quote:
                quote = ""
            index += 1
            continue
        if character in {'"', "'"}:
            quote = character
            index += 1
            continue
        if text.startswith(line_marker, index):
            end = text.find("\n", index)
            end = len(characters) if end < 0 else end
            characters[index:end] = " " * (end - index)
            index = end
            continue
        if block_comments and text.startswith("/*", index):
            end = text.find("*/", index + 2)
            end = len(characters) if end < 0 else end + 2
            for position in range(index, end):
                if characters[position] != "\n":
                    characters[position] = " "
            index = end
            continue
        index += 1
    return "".join(characters)


def _syntax_tokens(text: str) -> tuple[str, ...]:
    return tuple(
        match.group(0)
        for index, match in enumerate(_SYNTAX_TOKEN.finditer(text))
        if index < _EXECUTABLE_TOKEN_LIMIT
    )


def _consume_balanced_tokens(
    tokens: tuple[str, ...], index: int
) -> int | None:
    pairs = {"(": ")", "[": "]", "{": "}"}
    if index >= len(tokens) or tokens[index] not in pairs:
        return None
    stack = [pairs[tokens[index]]]
    index += 1
    while index < len(tokens) and stack:
        token = tokens[index]
        if token in pairs:
            stack.append(pairs[token])
        elif token == stack[-1]:
            stack.pop()
        index += 1
    return index if not stack else None


def _contains_graphql_block_declaration(text: str) -> bool:
    for match in _GRAPHQL_DECLARATION_START.finditer(text):
        window = text[
            match.start("declaration") :
            match.start("declaration") + _EXECUTABLE_SCAN_CHARS
        ]
        tokens = _syntax_tokens(
            _strip_syntax_comments(window, line_marker="#")
        )
        if not tokens:
            continue
        index = 0
        if tokens[index] == "extend":
            index += 1
        if index >= len(tokens) or tokens[index] not in {
            "schema",
            "type",
            "interface",
            "input",
            "enum",
        }:
            continue
        kind = tokens[index]
        index += 1
        if kind != "schema":
            if index >= len(tokens) or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", tokens[index]
            ):
                continue
            index += 1
        if index < len(tokens) and tokens[index] == "implements":
            index += 1
            if index < len(tokens) and tokens[index] == "&":
                index += 1
            while index < len(tokens) and re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", tokens[index]
            ):
                index += 1
                if index >= len(tokens) or tokens[index] != "&":
                    break
                index += 1
        while index < len(tokens) and tokens[index] == "@":
            index += 1
            if index >= len(tokens) or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", tokens[index]
            ):
                break
            index += 1
            if index < len(tokens) and tokens[index] == "(":
                balanced_end = _consume_balanced_tokens(tokens, index)
                if balanced_end is None:
                    break
                index = balanced_end
        if index < len(tokens) and tokens[index] == "{":
            return True
    return False


def _consume_proto_type(tokens: tuple[str, ...], index: int) -> int | None:
    if index < len(tokens) and tokens[index] == "stream":
        index += 1
    if index < len(tokens) and tokens[index] == ".":
        index += 1
    if index >= len(tokens) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*", tokens[index]
    ):
        return None
    index += 1
    while index + 1 < len(tokens) and tokens[index] == "." and re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*", tokens[index + 1]
    ):
        index += 2
    return index


def _is_proto_rpc(tokens: tuple[str, ...], index: int) -> bool:
    index += 1
    if index >= len(tokens) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*", tokens[index]
    ):
        return False
    index += 1
    if index >= len(tokens) or tokens[index] != "(":
        return False
    index = _consume_proto_type(tokens, index + 1) or -1
    if index < 0 or index >= len(tokens) or tokens[index] != ")":
        return False
    index += 1
    if index >= len(tokens) or tokens[index] != "returns":
        return False
    index += 1
    if index >= len(tokens) or tokens[index] != "(":
        return False
    index = _consume_proto_type(tokens, index + 1) or -1
    return bool(
        index >= 0
        and index + 1 < len(tokens)
        and tokens[index] == ")"
        and tokens[index + 1] in {";", "{"}
    )


def _contains_proto_service_rpc(text: str) -> bool:
    for match in _PROTO_SERVICE_START.finditer(text):
        window = text[
            match.start("declaration") :
            match.start("declaration") + _EXECUTABLE_SCAN_CHARS
        ]
        clean = _strip_syntax_comments(
            window, line_marker="//", block_comments=True
        )
        tokens = _syntax_tokens(clean)
        if (
            len(tokens) < 3
            or tokens[0] != "service"
            or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", tokens[1]) is None
            or tokens[2] != "{"
        ):
            continue
        depth = 1
        index = 3
        while index < len(tokens) and depth:
            token = tokens[index]
            if depth == 1 and token == "rpc" and _is_proto_rpc(tokens, index):
                return True
            if token == "{":
                depth += 1
            elif token == "}":
                depth -= 1
            index += 1
    return False


def _contains_executable_payload(text: str) -> bool:
    """Detect bounded OpenAPI, GraphQL, and Proto source embedded in Markdown."""

    if (
        _contains_openapi_yaml(text)
        or _contains_graphql_block_declaration(text)
        or _GRAPHQL_LEAF_DECLARATION.search(text)
        or _PROTO_SYNTAX.search(text)
        or (_PROTO_MESSAGE.search(text) and _PROTO2_FIELD.search(text))
        or _PROTO2_INLINE_MESSAGE.search(text)
        or _contains_proto_service_rpc(text)
    ):
        return True
    for pair in _JSON_STRING_PAIR.finditer(text):
        try:
            key = json.loads(pair.group("key"))
            value = json.loads(pair.group("value"))
        except json.JSONDecodeError:
            continue
        if key == "openapi" and re.fullmatch(r"3(?:\.[0-9]+)+", value):
            return True
        if key == "swagger" and re.fullmatch(r"2(?:\.0)?", value):
            return True
    return False


def _read_regular_utf8(path: pathlib.Path) -> str:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise RequirementPackageError(f"cannot stat requirement package: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RequirementPackageError(
            "requirement package must be a regular non-symlink file"
        )
    if metadata.st_size > MAX_REQUIREMENT_BYTES:
        raise RequirementPackageError("requirement package exceeds the byte limit")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0) | os.O_NONBLOCK
    try:
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise RequirementPackageError(
                    "requirement package changed to a non-regular file"
                )
            if (
                opened.st_dev != metadata.st_dev
                or opened.st_ino != metadata.st_ino
                or opened.st_size != metadata.st_size
            ):
                raise RequirementPackageError(
                    "requirement package changed while opening"
                )
            if opened.st_size > MAX_REQUIREMENT_BYTES:
                raise RequirementPackageError(
                    "requirement package exceeds the byte limit"
                )
            chunks: list[bytes] = []
            length = 0
            while True:
                chunk = os.read(
                    descriptor,
                    min(64 * 1024, MAX_REQUIREMENT_BYTES + 1 - length),
                )
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > MAX_REQUIREMENT_BYTES:
                    raise RequirementPackageError(
                        "requirement package exceeds the byte limit"
                    )
            final = os.fstat(descriptor)
            if final.st_size != opened.st_size or length != opened.st_size:
                raise RequirementPackageError(
                    "requirement package changed while reading or produced a short read"
                )
            payload = b"".join(chunks)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise RequirementPackageError(f"cannot read requirement package: {error}") from error
    if len(payload) > MAX_REQUIREMENT_BYTES:
        raise RequirementPackageError("requirement package exceeds the byte limit")
    try:
        return payload.decode("utf-8")
    except UnicodeError as error:
        raise RequirementPackageError("requirement package must be UTF-8") from error


def _required_sections(registry: DocumentRegistry) -> tuple[str, ...]:
    profile = registry.profiles.get("requirements-package")
    if profile is None:
        raise RequirementPackageError("requirements-package profile is not registered")
    sections = profile.get("required_sections")
    if not isinstance(sections, tuple) or not all(
        isinstance(section, str) for section in sections
    ):
        raise RequirementPackageError("requirements-package sections are malformed")
    return sections


def _parse_items(text: str, package_number: str) -> tuple[RequirementItem, ...]:
    items: list[RequirementItem] = []
    seen: set[str] = set()
    last_numbers = {kind: 0 for kind in _SECTION_KINDS.values()}
    for section in _SECTION.finditer(text):
        expected_kind = _SECTION_KINDS.get(section.group("name"))
        if expected_kind is None:
            continue
        section_line = text.count("\n", 0, section.start("body")) + 1
        for offset, line in enumerate(section.group("body").splitlines(), start=1):
            declaration = _LIST_DECLARATION.fullmatch(line)
            if declaration is None:
                declaration = _TABLE_DECLARATION.fullmatch(line)
            tokens = tuple(_FULL_CHILD_ID.finditer(line))
            if declaration is None:
                table_cells = tuple(
                    cell.strip() for cell in line.strip().strip("|").split("|")
                )
                if line.lstrip().startswith("|") and table_cells and (
                    table_cells[0].casefold() == "id"
                    or set(table_cells[0]) <= {"-", ":", " "}
                ):
                    continue
                if tokens or re.match(r"^[ \t]*(?:[-*+]\s+|\|)", line):
                    raise RequirementPackageError(
                        f"malformed requirement declaration at line {section_line + offset}"
                    )
                continue
            identity = declaration.group("identity")
            identity_match = _FULL_CHILD_ID.fullmatch(identity)
            assert identity_match is not None
            kind = identity_match.group("kind")
            number = int(identity_match.group("number"))
            if identity_match.group("package") != package_number:
                raise RequirementPackageError(
                    f"requirement declaration {identity} has a foreign package owner"
                )
            if identity in seen:
                raise RequirementPackageError(
                    f"duplicate or reused requirement identity: {identity}"
                )
            if kind != expected_kind:
                raise RequirementPackageError(
                    f"requirement declaration {identity} uses the wrong section kind"
                )
            if number <= last_numbers[kind]:
                raise RequirementPackageError(
                    f"reused or non-monotonic {kind} identity: {identity}"
                )
            item_text = declaration.group("text").strip()
            if not item_text or set(item_text) <= {"-", ":", "|", " "}:
                raise RequirementPackageError(
                    f"requirement declaration {identity} has no statement"
                )
            seen.add(identity)
            last_numbers[kind] = number
            items.append(
                RequirementItem(identity, kind, item_text, section_line + offset)
            )
            if len(items) > MAX_REQUIREMENT_ITEMS:
                raise RequirementPackageError("requirement package exceeds the item limit")
    return tuple(items)


def _allocation_space(
    registry: DocumentRegistry, package_number: str, kind: str
) -> IdentitySpace:
    requirement = registry.identity_spaces.get("requirement")
    if requirement is None:
        raise RequirementPackageError("Requirement allocation space is not registered")
    name = f"REQ-{package_number}.{kind}"
    allocation = requirement.child_spaces.get(name)
    if allocation is None:
        raise RequirementPackageError(f"Requirement allocation space is missing: {name}")
    return allocation


def _validate_item_allocations(
    items: tuple[RequirementItem, ...],
    package_number: str,
    registry: DocumentRegistry,
) -> None:
    for item in items:
        match = _FULL_CHILD_ID.fullmatch(item.identity)
        assert match is not None
        number = int(match.group("number"))
        allocation = _allocation_space(registry, package_number, item.kind)
        if number > allocation.high_water:
            raise RequirementPackageError(
                f"requirement identity exceeds allocation high-water: {item.identity}"
            )
        if number not in allocation.current_issued:
            raise RequirementPackageError(
                "reserved requirement identity is not currently issued: "
                f"{item.identity}"
            )


def _validate_allocation_history(
    allocation: IdentitySpace, allocation_name: str
) -> None:
    current = allocation.current_issued
    reserved = allocation.reserved_history
    if current != tuple(sorted(set(current))) or reserved != tuple(
        sorted(set(reserved))
    ):
        raise RequirementPackageError(
            f"Requirement allocation history is not canonical: {allocation_name}"
        )
    current_numbers = set(current)
    reserved_numbers = set(reserved)
    if current_numbers & reserved_numbers:
        raise RequirementPackageError(
            f"reserved allocation history was reissued: {allocation_name}"
        )
    if current_numbers | reserved_numbers != set(
        range(1, allocation.high_water + 1)
    ):
        raise RequirementPackageError(
            f"Requirement allocation history is incomplete: {allocation_name}"
        )
    if allocation.next_number != allocation.high_water + 1:
        raise RequirementPackageError(
            f"Requirement allocation advance is incoherent: {allocation_name}"
        )


def _validate_registry_allocation_transition(
    registry: DocumentRegistry,
    trusted_baseline: RequirementAllocationBaseline | None,
    allow_transition: bool,
) -> None:
    if not allow_transition:
        return
    findings = validate_requirement_allocation_transition(
        registry, trusted_baseline
    )
    if findings:
        first = findings[0]
        raise RequirementPackageError(
            f"{first.code}: {first.message}"
        )


def _validate_complete_allocation(
    package: RequirementPackage, registry: DocumentRegistry
) -> None:
    package_number = package.artifact_id.removeprefix("REQ-")
    for kind in _SECTION_KINDS.values():
        allocation = _allocation_space(registry, package_number, kind)
        _validate_allocation_history(allocation, f"REQ-{package_number}.{kind}")
        actual = tuple(
            int(item.identity.rsplit("-", 1)[1])
            for item in package.items
            if item.kind == kind
        )
        if actual != allocation.current_issued:
            raise RequirementPackageError(
                f"{package.artifact_id}.{kind} declarations do not match current_issued"
            )


def parse_requirement_package(
    path: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
    trusted_requirement_baseline: RequirementAllocationBaseline | None = None,
    allow_requirement_allocation_transition: bool = False,
) -> RequirementPackage:
    """Parse one canonical Requirement Package into frozen records."""

    path = pathlib.Path(path)
    path_match = _PACKAGE_PATH.fullmatch(path.name)
    if path_match is None:
        raise RequirementPackageError("requirement package path is not canonical")
    package_number = path_match.group("number")
    text = _read_regular_utf8(path)
    if _contains_retired_requirement_reference(text):
        if _BARE_CHILD_ID.search(text):
            raise RequirementPackageError(
                "requirement package contains a bare child identity"
            )
        raise RequirementPackageError(
            "requirement package contains a retired identity"
        )
    if _contains_executable_payload(text):
        raise RequirementPackageError(
            "executable interface payloads belong to the related Stage 03 Spec package"
        )
    try:
        record = frontmatter_record_from_text(path, text)
    except FrontmatterError as error:
        raise RequirementPackageError(str(error)) from error
    expected_artifact = f"REQ-{package_number}"
    artifact_id = record.metadata.get("artifact_id")
    if artifact_id != expected_artifact:
        raise RequirementPackageError(
            f"path requires {expected_artifact}, found {artifact_id!r}"
        )
    if record.metadata.get("profile_id") != "requirements-package":
        raise RequirementPackageError("requirement package has the wrong profile_id")
    if record.metadata.get("artifact_type") != "requirements-package":
        raise RequirementPackageError("requirement package has the wrong artifact_type")
    status = record.metadata.get("status")
    if not isinstance(status, str) or not status:
        raise RequirementPackageError("requirement package status is missing")
    active_registry = load_registry() if registry is None else registry
    _validate_registry_allocation_transition(
        active_registry,
        trusted_requirement_baseline,
        allow_requirement_allocation_transition,
    )
    sections = tuple(section.group("name") for section in _SECTION.finditer(text))
    missing = tuple(
        required for required in _required_sections(active_registry) if required not in sections
    )
    if missing:
        raise RequirementPackageError(
            "requirement package is missing required sections: " + ", ".join(missing)
        )
    items = _parse_items(text, package_number)
    if not items:
        raise RequirementPackageError("requirement package declares no requirements")
    _validate_item_allocations(items, package_number, active_registry)
    package = RequirementPackage(
        pathlib.PurePosixPath(path.as_posix()), expected_artifact, status, items
    )
    _validate_complete_allocation(package, active_registry)
    return package


def load_requirement_packages(
    stage_root: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
    trusted_requirement_baseline: RequirementAllocationBaseline | None = None,
    allow_requirement_allocation_transition: bool = False,
) -> tuple[RequirementPackage, ...]:
    """Load the bounded Stage 01 corpus and reject executable contract payloads."""

    stage_root = pathlib.Path(stage_root)
    try:
        root_metadata = stage_root.lstat()
    except OSError as error:
        raise RequirementPackageError(f"cannot stat Stage 01: {error}") from error
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        raise RequirementPackageError("Stage 01 must be a regular non-symlink directory")
    paths: list[pathlib.Path] = []
    for entry in sorted(stage_root.iterdir(), key=lambda item: item.name):
        if entry.name == "README.md":
            continue
        if entry.suffix.lower() in _EXECUTABLE_SUFFIXES:
            raise RequirementPackageError(
                "executable interface payloads belong to the related Stage 03 Spec package"
            )
        if entry.is_symlink() or not entry.is_file() or _PACKAGE_PATH.fullmatch(entry.name) is None:
            raise RequirementPackageError(f"unregistered Stage 01 entry: {entry.name}")
        paths.append(entry)
    active_registry = load_registry() if registry is None else registry
    _validate_registry_allocation_transition(
        active_registry,
        trusted_requirement_baseline,
        allow_requirement_allocation_transition,
    )
    packages = tuple(
        parse_requirement_package(path, registry=active_registry) for path in paths
    )
    package_ids = tuple(package.artifact_id for package in packages)
    if len(package_ids) != len(set(package_ids)):
        raise RequirementPackageError("duplicate or reused Requirement Package identity")
    requirement_space = active_registry.identity_spaces.get("requirement")
    if requirement_space is None:
        raise RequirementPackageError("Requirement package allocation space is missing")
    expected_package_ids = {
        f"REQ-{number:04d}"
        for number in range(1, requirement_space.high_water + 1)
    }
    if set(package_ids) != expected_package_ids:
        raise RequirementPackageError(
            "Requirement package coverage does not match the Registry high-water"
        )
    child_ids = tuple(item.identity for package in packages for item in package.items)
    if len(child_ids) != len(set(child_ids)):
        raise RequirementPackageError("duplicate or reused requirement child identity")
    return packages
