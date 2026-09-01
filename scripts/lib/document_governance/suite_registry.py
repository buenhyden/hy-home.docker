"""Immutable ownership of public validation suites."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import re
import stat
from types import MappingProxyType
from typing import Mapping

import yaml

from scripts.lib.document_governance.frontmatter import safe_load_unique


PUBLIC_SUITE_NAMES = (
    "agent-governance",
    "document-contract",
    "document-graph",
    "document-lifecycle",
    "operations",
    "repository-integrity",
)
EXECUTION_CONTEXT_NAMES = (
    "local",
    "pull_request",
    "push",
    "workflow_dispatch",
)
_MIRRORED_TEST_ROOT = PurePosixPath("tests/lib/document_governance")
MAX_MANIFEST_BYTES = 1_048_576
MAX_MANIFEST_DEPTH = 64


MAX_EXECUTION_ARGV = 8
MAX_ARGUMENT_LENGTH = 64
_LONG_OPTION = re.compile(r"^--[a-z][a-z0-9-]*$")
_ARGUMENT_VALUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_REJECTED_OPTIONS = frozenset({"--help"})
COMPLETE_CAPABILITY_ARGV = MappingProxyType(
    {
        "agent_output_eval.py": ("--check-fixtures", "--check-regressions"),
        "check-agent-governance-contract.py": ("--mode", "repository", "--section", "all"),
        "check-document-links.py": ("--mode", "all"),
        "check-document-metadata.py": ("--mode", "check-changed"),
        "check-operations-catalog.py": ("--mode", "complete"),
        "check-supply-chain-policy.py": ("--check",),
        "check-target-surface-delta-contract.py": ("--mode", "advisory"),
        "report-audit-pack-coverage.sh": ("--check",),
        "report-provider-hook-parity.sh": ("--check",),
    }
)


def validate_execution_argv(path: PurePosixPath, argv: tuple[str, ...]) -> None:
    """Admit a bounded argument shape and the complete capability of a modal CLI.

    Membership is manifest data, so this rule no longer consults a validator
    inventory. Shape admission is generic: bounded length, a restricted
    character set, long options only, and at most one value each.

    `COMPLETE_CAPABILITY_ARGV` is a separate safety control, not a membership
    list. A validator whose CLI accepts a narrower mode can be silently weakened
    by a manifest edit alone -- `check-document-links.py --mode traceability`
    passes while checking far less than `--mode all` -- and generic shape rules
    cannot see that. Those validators pin their complete capability here. A
    validator that fails closed without arguments needs no entry.
    """

    if len(argv) > MAX_EXECUTION_ARGV:
        raise SuiteRegistryError(
            f"{path}: execution arguments must not exceed {MAX_EXECUTION_ARGV} tokens"
        )
    seen: set[str] = set()
    expects_value = False
    for token in argv:
        if not token or len(token) > MAX_ARGUMENT_LENGTH:
            raise SuiteRegistryError(f"{path}: execution argument has an unbounded length")
        if token.startswith("--"):
            if not _LONG_OPTION.match(token) or token in _REJECTED_OPTIONS:
                raise SuiteRegistryError(f"{path}: {token!r} is not an admitted long option")
            if token in seen:
                raise SuiteRegistryError(f"{path}: {token!r} is repeated")
            seen.add(token)
            expects_value = True
            continue
        if token.startswith("-"):
            raise SuiteRegistryError(f"{path}: short options are not admitted")
        if not expects_value:
            raise SuiteRegistryError(f"{path}: {token!r} does not follow a long option")
        if not _ARGUMENT_VALUE.match(token):
            raise SuiteRegistryError(f"{path}: {token!r} is not a safe argument value")
        expects_value = False

    complete = COMPLETE_CAPABILITY_ARGV.get(path.name)
    if complete is not None and argv != complete:
        raise SuiteRegistryError(
            f"{path}: execution arguments must preserve the complete validation capability"
        )


class SuiteRegistryError(ValueError):
    """Raised when manifest suite ownership is incomplete or ambiguous."""


@dataclass(frozen=True, slots=True)
class ValidatorOwnership:
    path: PurePosixPath
    public_suites: tuple[str, ...]
    execution_argv: tuple[str, ...]
    execution_contexts: tuple[str, ...]


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


def load_manifest_document(path: Path) -> object:
    """Read the execution authority through one bounded, no-follow YAML boundary."""

    def snapshot(value: os.stat_result) -> tuple[int, ...]:
        return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
                value.st_mtime_ns, value.st_ctime_ns)

    def ancestor_snapshot(value: os.stat_result) -> tuple[int, ...]:
        # Identity, not content. What an ancestor must not do mid-read is
        # become a *different* directory, which changes its device and inode.
        # A directory's mtime and ctime also move whenever any entry is created
        # or removed inside it, and this walk reaches every ancestor up to the
        # filesystem root — including the operator's home directory, where
        # unrelated processes write constantly. Comparing those made the read
        # fail for reasons that have nothing to do with this file: measured,
        # 191 of 306 reads failed while nothing touched the manifest at all.
        return (value.st_dev, value.st_ino, value.st_mode)

    descriptors: list[int] = []
    try:
        absolute = path.absolute()
        if ".." in absolute.parts:
            raise ValueError("parent traversal is forbidden")
        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        parent = os.open(os.path.sep, directory_flags)
        descriptors.append(parent)
        ancestors: list[tuple[int, str, int, os.stat_result]] = []
        for name in absolute.parts[1:-1]:
            child = os.open(name, directory_flags, dir_fd=parent)
            descriptors.append(child)
            ancestors.append((parent, name, child, os.fstat(child)))
            parent = child
        before = os.stat(absolute.name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_MANIFEST_BYTES:
            raise ValueError("expected a bounded regular file")
        descriptor = os.open(
            absolute.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
            dir_fd=parent,
        )
        descriptors.append(descriptor)
        if snapshot(os.fstat(descriptor)) != snapshot(before):
            raise ValueError("file changed before read")
        raw = bytearray()
        while len(raw) <= MAX_MANIFEST_BYTES:
            chunk = os.read(descriptor, min(65_536, MAX_MANIFEST_BYTES + 1 - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
        if len(raw) != before.st_size or len(raw) > MAX_MANIFEST_BYTES:
            raise ValueError("file changed or exceeded its byte limit")
        if snapshot(os.fstat(descriptor)) != snapshot(before) or snapshot(
            os.stat(absolute.name, dir_fd=parent, follow_symlinks=False)
        ) != snapshot(before):
            raise ValueError("file changed during read")
        for ancestor, name, child, expected in ancestors:
            if ancestor_snapshot(os.fstat(child)) != ancestor_snapshot(
                expected
            ) or ancestor_snapshot(
                os.stat(name, dir_fd=ancestor, follow_symlinks=False)
            ) != ancestor_snapshot(expected):
                raise ValueError("ancestor changed during read")
        source = raw.decode("utf-8")
        depth = 0
        for event in yaml.parse(source):
            if isinstance(event, yaml.events.AliasEvent) or getattr(event, "anchor", None):
                raise ValueError("YAML aliases and anchors are forbidden")
            if isinstance(event, (yaml.events.MappingStartEvent, yaml.events.SequenceStartEvent)):
                depth += 1
                if depth > MAX_MANIFEST_DEPTH:
                    raise ValueError("YAML depth limit exceeded")
            elif isinstance(event, (yaml.events.MappingEndEvent, yaml.events.SequenceEndEvent)):
                depth -= 1
        return safe_load_unique(source)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, RecursionError) as error:
        raise SuiteRegistryError(f"manifest input is invalid: {error}") from error
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def load(path: Path = Path("scripts/manifest.yaml")) -> SuiteRegistry:
    """Load a closed, immutable suite mapping from the script manifest."""

    document = load_manifest_document(path)
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
            execution_argv = _optional_strings(
                row.get("execution_argv", []), row_path, "execution_argv"
            )
            validate_execution_argv(row_path, execution_argv)
            execution_contexts = _execution_contexts(
                row.get("execution_contexts"), row_path
            )
            expected_contexts = (
                ()
                if row_path.as_posix().startswith("scripts/lib/")
                else EXECUTION_CONTEXT_NAMES[1:]
                if row_path == PurePosixPath("scripts/hardening/check-all-hardening.sh")
                else EXECUTION_CONTEXT_NAMES
            )
            if execution_contexts != expected_contexts:
                raise SuiteRegistryError(
                    f"{row_path}: execution contexts must match the retained safety policy"
                )
            validators.append(
                ValidatorOwnership(
                    row_path,
                    public_suites,
                    execution_argv,
                    execution_contexts,
                )
            )
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
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
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


def _optional_strings(
    value: object, row_path: PurePosixPath, field: str
) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SuiteRegistryError(f"{row_path}: {field} must be a string list")
    return tuple(value)


def _execution_contexts(value: object, row_path: PurePosixPath) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SuiteRegistryError(f"{row_path}: execution_contexts must be a string list")
    contexts = tuple(value)
    expected_order = tuple(name for name in EXECUTION_CONTEXT_NAMES if name in contexts)
    if contexts != expected_order or len(contexts) != len(set(contexts)):
        raise SuiteRegistryError(
            f"{row_path}: execution_contexts must be unique and canonically ordered"
        )
    return contexts
