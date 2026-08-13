"""Shared, deterministic Markdown frontmatter parsing."""

from __future__ import annotations

import dataclasses
import pathlib
from collections.abc import Mapping
from types import MappingProxyType

import yaml


class FrontmatterError(ValueError):
    """Raised when a Markdown frontmatter block cannot be parsed safely."""

    def __init__(self, message: str, code: str = "malformed-yaml") -> None:
        self.code = code
        super().__init__(message)


class UniqueKeyLoader(yaml.SafeLoader):
    """PyYAML safe loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping key must be a hashable scalar",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key: {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def safe_load_unique(source: str) -> object:
    """Parse YAML safely after proving that every mapping key is unique."""

    yaml.load(source, Loader=UniqueKeyLoader)
    return yaml.safe_load(source)


@dataclasses.dataclass(frozen=True)
class FrontmatterRecord:
    """One parsed Markdown document and its top-of-file metadata envelope."""

    path: pathlib.Path
    metadata: Mapping[str, object]
    body: str
    frontmatter_present: bool


def parse_frontmatter_text(text: str) -> dict[str, object]:
    """Return top-of-file YAML frontmatter, or an empty mapping when absent."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    closing = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
        None,
    )
    if closing is None:
        raise FrontmatterError("opening frontmatter fence has no closing fence")
    source = "\n".join(lines[1:closing])
    try:
        loaded = safe_load_unique(source)
    except yaml.YAMLError as error:
        summary = str(error).splitlines()[0]
        problem = getattr(error, "problem", "")
        code = "duplicate-key" if problem.startswith("duplicate key:") else "malformed-yaml"
        raise FrontmatterError(
            f"invalid YAML frontmatter: {summary}", code=code
        ) from error
    if loaded is None:
        return {}
    if not isinstance(loaded, dict) or not all(isinstance(key, str) for key in loaded):
        raise FrontmatterError(
            "frontmatter must be a string-keyed YAML mapping",
            code="malformed-yaml",
        )
    return dict(loaded)


def _freeze(value: object, active: set[int] | None = None) -> object:
    """Return a deeply immutable value, rejecting recursive YAML aliases."""

    if not isinstance(value, (Mapping, list, tuple, set, frozenset)):
        return value
    ancestors = set() if active is None else active
    identity = id(value)
    if identity in ancestors:
        raise FrontmatterError(
            "frontmatter contains a cyclic value",
            code="cyclic-value",
        )
    ancestors.add(identity)
    try:
        if isinstance(value, Mapping):
            return MappingProxyType(
                {
                    str(key): _freeze(item, ancestors)
                    for key, item in value.items()
                }
            )
        if isinstance(value, (list, tuple)):
            return tuple(_freeze(item, ancestors) for item in value)
        return frozenset(_freeze(item, ancestors) for item in value)
    finally:
        ancestors.remove(identity)


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    if isinstance(value, frozenset):
        return {_thaw(item) for item in value}
    return value


def frontmatter_record_from_text(path: pathlib.Path, text: str) -> FrontmatterRecord:
    """Build an immutable frontmatter record from already-read UTF-8 text."""

    metadata = parse_frontmatter_text(text)
    lines = text.splitlines(keepends=True)
    body = text
    present = bool(lines and lines[0].strip() == "---")
    if present:
        closing = next(
            (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
            None,
        )
        if closing is not None:
            body = "".join(lines[closing + 1 :])
    frozen = _freeze(metadata)
    assert isinstance(frozen, Mapping)
    return FrontmatterRecord(path, frozen, body, present)


def read_frontmatter(path: pathlib.Path) -> FrontmatterRecord:
    """Read one UTF-8 Markdown file and return its frozen parsed envelope."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise FrontmatterError(f"cannot read UTF-8 Markdown: {error}") from error
    return frontmatter_record_from_text(path, text)


def read_frontmatter_values(path: pathlib.Path) -> dict[str, object]:
    """Compatibility view for validators that consume only metadata values."""

    thawed = _thaw(read_frontmatter(path).metadata)
    assert isinstance(thawed, dict)
    return thawed


_safe_load_unique = safe_load_unique
