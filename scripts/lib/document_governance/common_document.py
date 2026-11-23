"""Consume the common document envelope without changing role or native meaning."""

from __future__ import annotations

import functools
import json
import pathlib
import re
from collections.abc import Mapping
from types import MappingProxyType

ROOT = pathlib.Path(__file__).resolve().parents[3]
CORE_PATH = "docs/99.templates/01.contracts/common-document-contract.json"


class CommonDocumentError(ValueError):
    """A common definition, binding or authored document is not trustworthy."""


def _unique(pairs: list[tuple[str, object]]) -> dict:
    value = dict(pairs)
    if len(value) != len(pairs):
        raise CommonDocumentError("common contract has duplicate JSON keys")
    return value


def _immutable_json(value: object) -> object:
    """Freeze a JSON tree; JSON has neither YAML aliases nor custom values."""
    if isinstance(value, dict):
        return MappingProxyType(
            {key: _immutable_json(child) for key, child in value.items()}
        )
    if isinstance(value, list):
        return tuple(_immutable_json(child) for child in value)
    return value


@functools.lru_cache(maxsize=4)
def _decode_contract(raw: bytes) -> Mapping:
    from scripts.lib.document_governance.semver import is_numeric_version

    try:
        document = json.loads(raw, object_pairs_hook=_unique)
    except (ValueError, UnicodeError) as error:
        raise CommonDocumentError("common document contract is not JSON") from error
    if (
        not isinstance(document, dict)
        or document.get("contract_id") != "WORKSPACE-DOCUMENT-CORE"
        or not is_numeric_version(document.get("version"))
        or not isinstance(document.get("headings"), dict)
        or not isinstance(document.get("payload_profiles"), dict)
        or not isinstance(document.get("section_rules"), dict)
        or not isinstance(document.get("payload_encoding"), dict)
    ):
        raise CommonDocumentError("common document contract is incomplete")
    for parent, children in document["headings"].items():
        if (
            not isinstance(parent, str)
            or not isinstance(children, list)
            or not children
            or not all(isinstance(child, str) for child in children)
        ):
            raise CommonDocumentError("common document sections are invalid")
        if any(child not in document["section_rules"] for child in children):
            raise CommonDocumentError("common section lacks authoring guidance")
    try:
        metadata = document["metadata"]
        valid_metadata = set(metadata) == {
            "title",
            "version",
            "kind",
            "owner",
            "lifecycle",
            "scope",
        }
        valid_metadata = valid_metadata and metadata["lifecycle"]["enum"] == [
            "draft",
            "active",
            "deprecated",
        ]
        valid_layers = metadata["scope"]["properties"]["layer"]["enum"]
        encoding = document["payload_encoding"]
        valid_encoding = (
            encoding["marker"]
            == f"<!-- document-core: {document['contract_id']}/{document['version']} -->"
            and encoding["heading_shift"] == 2
        )
        if (
            not valid_metadata
            or not valid_encoding
            or not isinstance(valid_layers, list)
            or not all(isinstance(value, str) for value in valid_layers)
        ):
            raise CommonDocumentError("common metadata or payload encoding is invalid")
    except (KeyError, TypeError) as error:
        raise CommonDocumentError(
            "common metadata or payload encoding is incomplete"
        ) from error
    relations = document.get("relation_kinds")
    if (
        not isinstance(relations, list)
        or not relations
        or not all(isinstance(value, str) and value.strip() for value in relations)
        or len(relations) != len(set(relations))
    ):
        raise CommonDocumentError("common semantic relations must be unique names")
    return _immutable_json(document)


def load_contract(*, root: pathlib.Path = ROOT) -> Mapping:
    """Read a bounded regular source; cached parsing is keyed by actual bytes."""
    from scripts.lib.document_governance.file_access import read_bounded_regular

    try:
        return _decode_contract(
            read_bounded_regular(
                root, pathlib.PurePosixPath(CORE_PATH), max_bytes=256 * 1024
            )
        )
    except (OSError, ValueError) as error:
        if isinstance(error, CommonDocumentError):
            raise
        raise CommonDocumentError("cannot read the common document contract") from error


def _markdown_unfenced_lines(text: str) -> list[str]:
    """Return Markdown lines outside backtick and tilde fenced blocks."""

    lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        if fence_character is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if opening:
                marker = opening.group(1)
                info_string = opening.group(2)
                if marker[0] == "`" and "`" in info_string:
                    lines.append(line)
                    continue
                fence_character = marker[0]
                fence_length = len(marker)
                continue
            lines.append(line)
            continue
        if re.match(
            rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
            line,
        ):
            fence_character = None
            fence_length = 0
    return lines


# Keyed by the exact text: one corpus run (current and base revisions) parses
# each document once instead of on every envelope or payload query.
@functools.lru_cache(maxsize=4096)
def _markdown_form_lines(
    text: str,
) -> tuple[tuple[int, str, tuple[int, str] | None], ...]:
    """Map source lines to real headings and exclude blocks used as examples."""

    from markdown_it import MarkdownIt

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    tokens = MarkdownIt("commonmark").parse(normalized)
    headings: dict[int, tuple[int, str]] = {}
    hidden: set[int] = set()
    for index, token in enumerate(tokens):
        if token.map is None:
            continue
        start, end = token.map
        if (
            token.type == "heading_open"
            and token.level == 0
            and token.markup.startswith("#")
        ):
            title = tokens[index + 1].content
            if title:
                headings[start] = (len(token.markup), title)
        elif token.type in {"fence", "code_block", "blockquote_open"}:
            hidden.update(range(start, end))
        elif token.type in {"bullet_list_open", "ordered_list_open"}:
            hidden.update(
                line
                for line in range(start, end)
                if lines[line].lstrip().startswith("|")
            )
        elif token.type == "html_block" and end > start + 1:
            hidden.update(range(start, end))
    return tuple(
        (index, "" if index in hidden else line, headings.get(index))
        for index, line in enumerate(lines)
    )


def _headings(text: str) -> list[tuple[int, int, str]]:
    return [
        (index, heading[0], heading[1])
        for index, _, heading in _markdown_form_lines(text)
        if heading is not None
    ]


def is_enveloped(text: str) -> bool:
    core = load_contract()
    marker = core["payload_encoding"]["marker"]
    body = re.sub(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", "", text, count=1, flags=re.S)
    structural_marker = any(
        re.fullmatch(r" {0,3}" + re.escape(marker) + r"[ \t]*", line)
        for line in _markdown_unfenced_lines(body)
    )
    return structural_marker or any(
        level == 2 and title in core["headings"] for _, level, title in _headings(text)
    )


def _payload_span(text: str) -> tuple[int, int] | None:
    core = load_contract()
    if not is_enveloped(text):
        return None
    found = _headings(text)
    expected = [
        pair
        for parent, children in core["headings"].items()
        for pair in [(2, parent), *((3, child) for child in children)]
    ]
    actual = [(level, title) for _, level, title in found if level in (2, 3)]
    if actual != expected:
        raise CommonDocumentError(
            "common H2/H3 sections are missing, duplicated or reordered"
        )
    payload_title = tuple(core["headings"].values())[1][1]
    start = next(
        index + 1
        for index, level, title in found
        if (level, title) == (3, payload_title)
    )
    stop = next(
        (index for index, level, _ in found if index >= start and level <= 3),
        len(text.splitlines()),
    )
    if not any(line.strip() for line in text.splitlines()[start:stop]):
        raise CommonDocumentError("the common envelope has no role payload")
    return start, stop


def _depth_annotations(
    lines: list[str], headings: Mapping[int, tuple[int, str]], start: int, stop: int
) -> dict[int, int]:
    """Read only the reserved comment immediately after an actual payload H6."""
    annotations = {}
    for index, (level, _) in headings.items():
        if not (start <= index < stop - 1 and level == 6):
            continue
        match = re.fullmatch(
            r"<!-- core-payload-level:([456]) -->", lines[index + 1].rstrip("\r\n")
        )
        if match:
            annotations[index + 1] = int(match[1])
    return annotations


def payload_text(text: str) -> str:
    """Expose role headings while preserving physical line numbers for diagnostics."""
    span = _payload_span(text)
    if span is None:
        return text
    lines = text.splitlines(keepends=True)
    start, stop = span
    found = {index: (level, title) for index, level, title in _headings(text)}
    annotations = _depth_annotations(lines, found, start, stop)
    first = next(index for index, level, _ in _headings(text) if level == 2)
    title_index = next(index for index, level, _ in _headings(text) if level == 1)
    marker = load_contract()["payload_encoding"]["marker"]
    for index, line in enumerate(lines):
        if title_index < index < first and line.strip() == marker:
            lines[index] = "\n"
        elif first <= index < start or index >= stop or index in annotations:
            lines[index] = "\n"
        elif start <= index < stop and index in found:
            level, title = found[index]
            if level < 4:
                raise CommonDocumentError("a role heading escapes its payload")
            original = annotations.get(index + 1, level - 2)
            lines[index] = "#" * original + " " + title + "\n"
    return "".join(lines)


def compact_payload(text: str) -> str:
    """Extract the same role bytes without envelope-only spacing for native output."""
    span = _payload_span(text)
    if span is None:
        return text
    viewed = payload_text(text).splitlines(keepends=True)
    headings = {index: (level, title) for index, level, title in _headings(text)}
    annotations = _depth_annotations(text.splitlines(keepends=True), headings, *span)
    first = next(index for index, level, _ in _headings(text) if level == 2)
    prefix = "".join(viewed[:first]).strip()
    body = "".join(
        line
        for index, line in enumerate(viewed)
        if span[0] <= index < span[1] and index not in annotations
    ).strip()
    return prefix + "\n\n" + body + "\n"


def wrap_document(text: str, *, kind: str) -> str:
    """Put an authored Markdown role payload under the shared outer sections."""
    core = load_contract()
    if not isinstance(kind, str) or kind not in core["payload_profiles"]:
        raise CommonDocumentError(f"unknown document kind: {kind}")
    if is_enveloped(text):
        _payload_span(text)
        return text
    front = re.match(r"\A---\n.*?\n---\n", text, re.S)
    prefix = front[0] if front else ""
    body = text[len(prefix) :]
    lines = body.splitlines(keepends=True)
    found = _headings(body)
    titles = [(index, title) for index, level, title in found if level == 1]
    if len(titles) != 1:
        raise CommonDocumentError("a Markdown output needs one actual H1")
    title_index, title = titles[0]
    preamble = "".join(lines[:title_index]).strip("\n")
    payload = []
    headings = {index: (level, held) for index, level, held in found}
    for index, line in enumerate(lines):
        if index <= title_index:
            continue
        if index in headings:
            level, held = headings[index]
            line = "#" * min(level + 2, 6) + " " + held + "\n"
            if level >= 4:
                line += f"<!-- core-payload-level:{level} -->\n"
        payload.append(line)
    korean = kind in {
        "readme",
        "reference-pack",
        "knowledge-index",
        "prompt-index",
        "provider-index",
    }
    entries = (
        [
            "독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.",
            "적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.",
            "실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.",
            "",
            "아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.",
            "해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.",
            "현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.",
            "외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.",
        ]
        if korean
        else [
            f"Readers use the {kind} payload below for this document's information and judgments.",
            "The frontmatter and role payload own the maintained subject, owner and applicability.",
            "Actual inputs and preconditions are those declared by the role payload below.",
            "",
            "Use the procedures or reading order stated in the role payload.",
            "Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.",
            "The role payload retains the current owner and dependency references.",
            "External basis and its limits remain those stated in the role payload; a citation grants no authority.",
        ]
    )
    rendered = [
        "\n\n".join(
            part for part in (prefix.rstrip("\n"), preamble, "# " + title) if part
        ),
        "",
        core["payload_encoding"]["marker"],
        "",
    ]
    index = 0
    for parent, children in core["headings"].items():
        rendered.extend(["## " + parent, ""])
        for child in children:
            content = "".join(payload).strip("\n") if index == 3 else entries[index]
            rendered.extend(["### " + child, "", content, ""])
            index += 1
    return "\n".join(rendered).lstrip("\n").rstrip() + "\n"


def _binding(registry: object, path: str) -> Mapping:
    from scripts.lib.document_governance.registry import classify_path

    common = registry.common.get("document_core")
    if not isinstance(common, Mapping):
        raise CommonDocumentError("Registry lacks the common document binding")
    profile = classify_path(path, registry)
    if profile == "template-source":
        role = next(
            (
                role
                for role in registry.template_roles.values()
                if role["source"] == path
            ),
            None,
        )
        if role is None:
            raise CommonDocumentError(
                "template definition has no explicit output binding"
            )
        profile = role["profiles"][0]
    result = common["profile_bindings"].get(profile)
    if not isinstance(result, Mapping):
        raise CommonDocumentError(f"unmapped common document profile: {profile}")
    result = {**result, **common.get("path_bindings", {}).get(path, {})}
    if any(
        role["source"] == path and role.get("native_source")
        for role in registry.template_roles.values()
    ):
        result = {
            **result,
            "scope_layers": ("template",),
            "lifecycle_field": "status",
            "lifecycle_values": {"draft": "draft"},
        }
    return result


def requires_envelope(registry: object, path: str) -> bool:
    """Require current normative forms; retain recorded evidence and native syntax."""
    from scripts.lib.document_governance.registry import (
        classify_path,
        recorded_package_profile,
    )

    if not isinstance(registry.common.get("document_core"), Mapping):
        return False
    for role in registry.template_roles.values():
        if role["source"] == path:
            return True
        if role.get("native_source") == path:
            return False
    profile = classify_path(path, registry)
    if (
        profile == "task"
        and recorded_package_profile(
            registry.common, profile, registry.profiles[profile], path
        )
        is not None
    ):
        return False
    if profile in {
        "research-member",
        "audit-member",
        "generated",
        "incident",
        "postmortem",
    }:
        return False
    binding = registry.common["document_core"]["profile_bindings"].get(profile)
    return isinstance(binding, Mapping) and binding["kind"] not in {
        "native-asset",
        "skill",
    }


def common_metadata(registry: object, path: str, metadata: Mapping) -> Mapping:
    """Read one explicit source for each common meaning; never promote execution."""
    from scripts.lib.document_governance.frontmatter import _freeze
    from scripts.lib.document_governance.semver import is_numeric_version

    binding = _binding(registry, path)
    core = load_contract()
    required = ("title", "version", "owner")
    if any(
        not isinstance(metadata.get(key), str) or not metadata[key].strip()
        for key in required
    ):
        raise CommonDocumentError("common title, version and owner must be nonempty")
    if not is_numeric_version(metadata["version"]):
        raise CommonDocumentError("document version is not an exact numeric X.X.X")
    kind = binding["kind"]
    if not isinstance(kind, str) or kind not in core["payload_profiles"]:
        raise CommonDocumentError("unknown common document kind")
    state_field = binding.get("lifecycle_field", "status")
    raw_state = metadata.get(state_field)
    if not isinstance(raw_state, str):
        raise CommonDocumentError("normative lifecycle source must be a string")
    state = binding.get("lifecycle_values", {}).get(raw_state)
    if state not in core["metadata"]["lifecycle"]["enum"]:
        raise CommonDocumentError("normative lifecycle has no explicit valid source")
    scope = metadata.get("document_scope")
    if (
        not isinstance(scope, Mapping)
        or set(scope) != {"subject", "layer"}
        or not isinstance(scope.get("subject"), str)
        or not scope["subject"].strip()
        or not isinstance(scope.get("layer"), str)
        or scope.get("layer")
        not in core["metadata"]["scope"]["properties"]["layer"]["enum"]
        or scope["layer"] not in binding["scope_layers"]
    ):
        raise CommonDocumentError(
            "common scope needs an actual subject and bound layer"
        )
    return _freeze(
        {
            **{key: metadata[key] for key in required},
            "kind": kind,
            "lifecycle": state,
            "scope": dict(scope),
        }
    )


def template_payload(
    registry: object, template_id: str, *, root: pathlib.Path = ROOT
) -> str:
    """Read the real typed output asset, or the Markdown definition's role payload."""
    from scripts.lib.document_governance.file_access import read_bounded_regular

    role = registry.template_roles.get(template_id)
    if not isinstance(role, Mapping):
        raise CommonDocumentError(f"unknown template role: {template_id}")
    source = str(role.get("native_source", role["source"]))
    relative = pathlib.PurePosixPath(source)
    if relative.is_absolute() or ".." in relative.parts:
        raise CommonDocumentError("template payload path is not repository-relative")
    try:
        text = read_bounded_regular(root, relative, max_bytes=512 * 1024).decode(
            "utf-8"
        )
    except (OSError, ValueError, UnicodeError) as error:
        raise CommonDocumentError("cannot read a bounded template payload") from error
    return text if role.get("native_source") else compact_payload(text)
