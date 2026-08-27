"""Immutable ownership of public validation suites."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping

import yaml


PUBLIC_SUITE_NAMES = (
    "agent-governance",
    "document-contract",
    "document-graph",
    "document-lifecycle",
    "operations",
    "repository-integrity",
)
_MIRRORED_TEST_ROOT = PurePosixPath("tests/lib/document_governance")


class SuiteRegistryError(ValueError):
    """Raised when manifest suite ownership is incomplete or ambiguous."""


@dataclass(frozen=True, slots=True)
class ValidatorOwnership:
    path: PurePosixPath
    public_suites: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProductionModule:
    path: PurePosixPath
    tests: tuple[PurePosixPath, ...]

    @property
    def has_mirrored_test(self) -> bool:
        return any(test.is_relative_to(_MIRRORED_TEST_ROOT) for test in self.tests)


@dataclass(frozen=True, slots=True)
class PublicSuite:
    name: str
    validators: tuple[PurePosixPath, ...]


@dataclass(frozen=True, slots=True)
class SuiteRegistry:
    public_names: tuple[str, ...]
    suites: tuple[PublicSuite, ...]
    validators: tuple[ValidatorOwnership, ...]
    production_modules: tuple[ProductionModule, ...]

    @property
    def by_name(self) -> Mapping[str, PublicSuite]:
        return MappingProxyType({suite.name: suite for suite in self.suites})


def load(path: Path = Path("scripts/manifest.yaml")) -> SuiteRegistry:
    """Load a closed, immutable suite mapping from the script manifest."""

    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise SuiteRegistryError("manifest is unreadable") from error
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        raise SuiteRegistryError("manifest files must be a list")

    rows = document["files"]
    validators: list[ValidatorOwnership] = []
    modules: list[ProductionModule] = []
    suites: dict[str, list[PurePosixPath]] = {name: [] for name in PUBLIC_SUITE_NAMES}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise SuiteRegistryError("manifest rows require a path")
        row_path = PurePosixPath(row["path"])
        _paths(row.get("consumers"), row_path, "consumers")
        tests = _paths(row.get("tests"), row_path, "tests")
        if row.get("kind") == "validator":
            public_suites = _suite_names(row.get("public_suites"), row_path)
            validators.append(ValidatorOwnership(row_path, public_suites))
            suites[public_suites[0]].append(row_path)
        elif "public_suites" in row:
            raise SuiteRegistryError(f"{row_path}: only validators may declare public_suites")
        if row.get("kind") == "library" and row_path.name != "__init__.py" and row_path.is_relative_to(
            PurePosixPath("scripts/lib/document_governance")
        ):
            modules.append(ProductionModule(row_path, tests))

    for module in modules:
        if not module.has_mirrored_test:
            raise SuiteRegistryError(f"{module.path}: requires a mirrored library test")

    return SuiteRegistry(
        public_names=PUBLIC_SUITE_NAMES,
        suites=tuple(PublicSuite(name, tuple(suites[name])) for name in PUBLIC_SUITE_NAMES),
        validators=tuple(validators),
        production_modules=tuple(modules),
    )


def _paths(value: object, row_path: PurePosixPath, field: str) -> tuple[PurePosixPath, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SuiteRegistryError(f"{row_path}: {field} must be a string list")
    paths = tuple(PurePosixPath(item) for item in value)
    if len(paths) != len(set(paths)):
        raise SuiteRegistryError(f"{row_path}: {field} must not contain duplicates")
    return paths


def _suite_names(value: object, row_path: PurePosixPath) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], str):
        raise SuiteRegistryError(f"{row_path}: validator must map to exactly one public suite")
    if value[0] not in PUBLIC_SUITE_NAMES:
        raise SuiteRegistryError(f"{row_path}: unknown public suite {value[0]!r}")
    return (value[0],)
