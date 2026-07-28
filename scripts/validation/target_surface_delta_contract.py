from __future__ import annotations

import argparse
import collections
import os
import pathlib
import re
import stat
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Final

import yaml


TARGET_ROOTS: Final[tuple[str, ...]] = (
    ".github",
    "archive",
    "examples",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
)
DELTA_MANIFEST: Final[pathlib.PurePosixPath] = pathlib.PurePosixPath(
    "docs/90.references/data/governance/target-surface-delta-manifest.yaml"
)
DELTA_SUMMARY: Final[pathlib.PurePosixPath] = pathlib.PurePosixPath(
    "docs/90.references/data/governance/target-surface-delta-summary.md"
)
PROFILE_REGISTRY: Final[pathlib.PurePosixPath] = pathlib.PurePosixPath(
    "docs/99.templates/support/document-metadata-profiles.yaml"
)
DEFAULT_PREDECESSOR_CLOSURE: Final = (
    "63039b5b0b20c99a10aae7162627afefcd7a1d8b"
)
DEFAULT_IMPLEMENTATION_BASE: Final = (
    "19ee47270e3897073ab9a3f86dfd4cce0f4b2e74"
)
SCHEMA_VERSION: Final = 1
MAX_CONTRACT_FILE_BYTES: Final = 2 * 1_048_576
FULL_SHA_RE: Final = re.compile(r"^[0-9a-f]{40}$")
README_PROFILE_NAME_RE: Final = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
DISPOSITIONS: Final = frozenset({"preserve", "update", "migrate", "delete"})
REVIEW_VERDICTS: Final = frozenset({"pending", "pass", "fail"})
SECRET_SAFETY_VALUES: Final = frozenset({"not-applicable", "path-only"})
SURFACE_CLASSES: Final = frozenset(
    {
        "content-archive",
        "executable-script",
        "native-configuration",
        "native-file",
        "native-platform",
        "python-source",
        "readme",
        "test-or-fixture",
        "typed-example",
    }
)
TOP_LEVEL_KEYS: Final = frozenset(
    {
        "schema_version",
        "predecessor_closure",
        "implementation_base",
        "enforcement",
        "target_roots",
        "entries",
    }
)
ROW_KEYS: Final = frozenset(
    {
        "path",
        "surface_class",
        "profile",
        "changed_since",
        "disposition",
        "canonical_owner",
        "direct_consumers",
        "finding",
        "replacement",
        "secret_safety",
        "validators",
        "tests",
        "provenance",
        "rollback",
        "spec_verdict",
        "quality_verdict",
    }
)
PLANNED_UPDATE_PATHS: Final = frozenset(
    {
        ".github/INDEX.md",
        ".github/rulesets/main-protection.md",
        ".github/workflows/ci-quality.yml",
        ".github/workflows/tech-stack-version-sync.yml",
        "examples/sample-web-service/README.md",
        "examples/sample-web-service/service.md",
        "scripts/README.md",
        "scripts/validation/check-repo-contracts.sh",
        "scripts/validation/run-local-qa-gates.sh",
    }
)
PLANNED_UPDATE_FINDINGS: Final = {
    ".github/INDEX.md": (
        "Task 4 will align the GitHub navigation index with the typed workflow contract."
    ),
    ".github/rulesets/main-protection.md": (
        "Task 4 will align desired branch-protection evidence with the required job set."
    ),
    ".github/workflows/ci-quality.yml": (
        "Task 4 will remove duplicate CI execution and replace mutable nested Action behavior."
    ),
    ".github/workflows/tech-stack-version-sync.yml": (
        "Task 4 will register the omitted non-gating workflow trigger and runner contract."
    ),
    "examples/sample-web-service/README.md": (
        "Task 2 will normalize this bounded example through the examples README profile."
    ),
    "examples/sample-web-service/service.md": (
        "Task 2 will resolve typed example parentage without creating an active SDLC chain."
    ),
    "scripts/README.md": (
        "Task 4 will align the script inventory with typed CI and QA ownership."
    ),
    "scripts/validation/check-repo-contracts.sh": (
        "Task 4 will replace overlapping inline workflow checks with the focused owner."
    ),
    "scripts/validation/run-local-qa-gates.sh": (
        "Task 4 will align local gate listing and execution with the typed CI contract."
    ),
}


@dataclass(frozen=True, order=True, slots=True)
class DeltaFinding:
    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class DeltaManifestRow:
    path: str
    surface_class: str
    profile: str | None
    changed_since: str
    disposition: str
    canonical_owner: str
    direct_consumers: tuple[str, ...]
    finding: str
    replacement: str | None
    secret_safety: str
    validators: tuple[str, ...]
    tests: tuple[str, ...]
    provenance: tuple[str, ...]
    rollback: tuple[str, ...]
    spec_verdict: str
    quality_verdict: str


@dataclass(frozen=True, slots=True)
class DeltaManifestDocument:
    schema_version: int
    predecessor_closure: str
    implementation_base: str
    enforcement: str
    target_roots: tuple[str, ...]
    entries: tuple[DeltaManifestRow, ...]


@dataclass(frozen=True, slots=True)
class TargetInventory:
    paths: tuple[str, ...]
    counts_by_root: tuple[tuple[str, int], ...]
    markdown_count: int
    readme_count: int


class ContractInputError(Exception):
    def __init__(self) -> None:
        super().__init__("invalid delta contract input")


class _DuplicateKeyError(yaml.YAMLError):
    pass


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
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
            raise _DuplicateKeyError("duplicate mapping key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _safe_load_unique(source: str) -> object:
    return yaml.load(source, Loader=_UniqueKeyLoader)


def _canonical_relative(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "://" in value
        or "|" in value
        or "`" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise ContractInputError
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix():
        raise ContractInputError
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ContractInputError
    return value


def _safe_label(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value.encode("utf-8")) > 1_024
        or any(character in value for character in ("\0", "\r", "\n"))
    ):
        raise ContractInputError
    return value


def _safe_tuple(value: object, *, paths: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ContractInputError
    parser = _canonical_relative if paths else _safe_label
    parsed = tuple(parser(item) for item in value)
    if len(parsed) != len(set(parsed)):
        raise ContractInputError
    return parsed


def _read_contract_text(repo_root: pathlib.Path, relative: str) -> str:
    canonical = _canonical_relative(relative)
    try:
        parent_descriptor = os.open(repo_root, os.O_RDONLY | os.O_DIRECTORY)
    except OSError:
        raise ContractInputError from None

    descriptors = [parent_descriptor]
    try:
        parts = pathlib.PurePosixPath(canonical).parts
        for component in parts[:-1]:
            descriptor = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptors[-1],
            )
            descriptors.append(descriptor)
        file_descriptor = os.open(
            parts[-1],
            os.O_RDONLY | os.O_NOFOLLOW,
            dir_fd=descriptors[-1],
        )
        descriptors.append(file_descriptor)
        opened = os.fstat(file_descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_size > MAX_CONTRACT_FILE_BYTES:
            raise ContractInputError
        chunks: list[bytes] = []
        remaining = opened.st_size + 1
        while remaining > 0:
            chunk = os.read(file_descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > MAX_CONTRACT_FILE_BYTES:
            raise ContractInputError
        final = os.fstat(file_descriptor)
        if (
            opened.st_dev,
            opened.st_ino,
            opened.st_mode,
            opened.st_size,
            opened.st_mtime_ns,
            opened.st_ctime_ns,
        ) != (
            final.st_dev,
            final.st_ino,
            final.st_mode,
            final.st_size,
            final.st_mtime_ns,
            final.st_ctime_ns,
        ):
            raise ContractInputError
        return payload.decode("utf-8", errors="strict")
    except (OSError, UnicodeError):
        raise ContractInputError from None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _git_bytes(
    repo_root: pathlib.Path,
    *arguments: str,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=repo_root,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        raise ContractInputError from None


def _git_text(
    repo_root: pathlib.Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, UnicodeError, subprocess.SubprocessError):
        raise ContractInputError from None


def _decode_nul_paths(payload: bytes) -> set[str]:
    paths: set[str] = set()
    try:
        chunks = payload.split(b"\0")
        if chunks and chunks[-1] == b"":
            chunks.pop()
        for raw_path in chunks:
            paths.add(_canonical_relative(raw_path.decode("utf-8", errors="strict")))
    except UnicodeError:
        raise ContractInputError from None
    return paths


def _is_target_path(path: str, roots: tuple[str, ...] = TARGET_ROOTS) -> bool:
    return any(path == root or path.startswith(f"{root}/") for root in roots)


def changed_target_paths(
    root: pathlib.Path,
    predecessor_commit: str,
    roots: tuple[str, ...] = TARGET_ROOTS,
) -> tuple[str, ...]:
    repo_root = pathlib.Path(root).resolve()
    if FULL_SHA_RE.fullmatch(predecessor_commit) is None:
        raise ContractInputError
    paths: set[str] = set()
    commands = (
        (
            "diff",
            "--name-only",
            "-z",
            "--no-renames",
            f"{predecessor_commit}..HEAD",
            "--",
            *roots,
        ),
        ("diff", "--name-only", "-z", "--no-renames", "--cached", "--", *roots),
        ("diff", "--name-only", "-z", "--no-renames", "--", *roots),
        ("ls-files", "--others", "--exclude-standard", "-z", "--", *roots),
    )
    for arguments in commands:
        result = _git_bytes(repo_root, *arguments)
        if result.returncode != 0:
            raise ContractInputError
        paths.update(_decode_nul_paths(result.stdout))
    return tuple(sorted(path for path in paths if _is_target_path(path, roots)))


def current_target_inventory(root: pathlib.Path) -> TargetInventory:
    repo_root = pathlib.Path(root).resolve()
    result = _git_bytes(repo_root, "ls-files", "-z", "--", *TARGET_ROOTS)
    if result.returncode != 0:
        raise ContractInputError
    paths = tuple(sorted(_decode_nul_paths(result.stdout)))
    counts: collections.Counter[str] = collections.Counter()
    for path in paths:
        if not _is_target_path(path):
            raise ContractInputError
        try:
            metadata = os.lstat(repo_root / path)
        except OSError:
            raise ContractInputError from None
        if not stat.S_ISREG(metadata.st_mode):
            raise ContractInputError
        counts[pathlib.PurePosixPath(path).parts[0]] += 1
    return TargetInventory(
        paths=paths,
        counts_by_root=tuple((root_name, counts[root_name]) for root_name in TARGET_ROOTS),
        markdown_count=sum(path.endswith((".md", ".mdx")) for path in paths),
        readme_count=sum(path.endswith("README.md") for path in paths),
    )


def _optional_label(value: object) -> str | None:
    if value is None:
        return None
    return _safe_label(value)


def _replacement(value: object) -> str | None:
    candidate = _optional_label(value)
    if candidate is None or candidate == "withdrawn":
        return candidate
    return _canonical_relative(candidate)


def _parse_row(value: object) -> DeltaManifestRow:
    if not isinstance(value, dict) or set(value) != ROW_KEYS:
        raise ContractInputError
    path = _canonical_relative(value["path"])
    if not _is_target_path(path):
        raise ContractInputError
    row = DeltaManifestRow(
        path=path,
        surface_class=_safe_label(value["surface_class"]),
        profile=_optional_label(value["profile"]),
        changed_since=_safe_label(value["changed_since"]),
        disposition=_safe_label(value["disposition"]),
        canonical_owner=_canonical_relative(value["canonical_owner"]),
        direct_consumers=_safe_tuple(value["direct_consumers"], paths=True),
        finding=_safe_label(value["finding"]),
        replacement=_replacement(value["replacement"]),
        secret_safety=_safe_label(value["secret_safety"]),
        validators=_safe_tuple(value["validators"], paths=True),
        tests=_safe_tuple(value["tests"], paths=True),
        provenance=_safe_tuple(value["provenance"]),
        rollback=_safe_tuple(value["rollback"]),
        spec_verdict=_safe_label(value["spec_verdict"]),
        quality_verdict=_safe_label(value["quality_verdict"]),
    )
    return row


def load_delta_manifest(
    root: pathlib.Path,
    path: pathlib.PurePosixPath = DELTA_MANIFEST,
) -> DeltaManifestDocument:
    repo_root = pathlib.Path(root).resolve()
    relative = _canonical_relative(path.as_posix())
    try:
        raw = _safe_load_unique(_read_contract_text(repo_root, relative))
        if not isinstance(raw, dict) or set(raw) != TOP_LEVEL_KEYS:
            raise ContractInputError
        if type(raw["schema_version"]) is not int:
            raise ContractInputError
        roots = _safe_tuple(raw["target_roots"], paths=True)
        if not isinstance(raw["entries"], list):
            raise ContractInputError
        entries = tuple(_parse_row(entry) for entry in raw["entries"])
        paths = tuple(entry.path for entry in entries)
        if len(paths) != len(set(paths)):
            raise ContractInputError
        return DeltaManifestDocument(
            schema_version=raw["schema_version"],
            predecessor_closure=_safe_label(raw["predecessor_closure"]),
            implementation_base=_safe_label(raw["implementation_base"]),
            enforcement=_safe_label(raw["enforcement"]),
            target_roots=roots,
            entries=entries,
        )
    except (KeyError, TypeError, yaml.YAMLError):
        raise ContractInputError from None


def _commit_exists(root: pathlib.Path, revision: str) -> bool:
    if FULL_SHA_RE.fullmatch(revision) is None:
        return False
    result = _git_text(root, "cat-file", "-e", f"{revision}^{{commit}}")
    return result.returncode == 0


def _is_ancestor(root: pathlib.Path, older: str, newer: str) -> bool:
    result = _git_text(root, "merge-base", "--is-ancestor", older, newer)
    return result.returncode == 0


def _readme_glob_matches(path: pathlib.PurePosixPath, pattern: str) -> bool:
    path_parts = path.parts
    pattern_parts = pathlib.PurePosixPath(pattern).parts
    return len(path_parts) == len(pattern_parts) and all(
        pattern_part == "*" or pattern_part == path_part
        for path_part, pattern_part in zip(path_parts, pattern_parts, strict=True)
    )


def _load_readme_profiles(root: pathlib.Path) -> dict[str, tuple[str, ...]]:
    try:
        raw = _safe_load_unique(
            _read_contract_text(root, PROFILE_REGISTRY.as_posix())
        )
        if not isinstance(raw, dict):
            raise ContractInputError
        profiles = raw.get("readme_profiles")
        if not isinstance(profiles, dict) or not profiles:
            raise ContractInputError
        result: dict[str, tuple[str, ...]] = {}
        for name, profile in profiles.items():
            if (
                not isinstance(name, str)
                or README_PROFILE_NAME_RE.fullmatch(name) is None
                or not isinstance(profile, dict)
            ):
                raise ContractInputError
            patterns = profile.get("path_globs")
            if not isinstance(patterns, list) or not patterns:
                raise ContractInputError
            result[name] = tuple(
                _canonical_relative(pattern) for pattern in patterns
            )
        return result
    except yaml.YAMLError:
        raise ContractInputError from None


def _matching_readme_profiles(
    path: str,
    profiles: dict[str, tuple[str, ...]],
) -> tuple[str, ...]:
    pure = pathlib.PurePosixPath(path)
    return tuple(
        sorted(
            name
            for name, patterns in profiles.items()
            if any(_readme_glob_matches(pure, pattern) for pattern in patterns)
        )
    )


def _expected_profile(
    path: str,
    readme_profiles: dict[str, tuple[str, ...]] | None,
) -> str | None:
    if path.endswith("README.md") and readme_profiles is not None:
        matches = _matching_readme_profiles(path, readme_profiles)
        return matches[0] if len(matches) == 1 else None
    if path.startswith("archive/") and path.endswith((".md", ".mdx")):
        return "content-archive"
    if path == "examples/sample-web-service/service.md":
        return "service"
    return None


def _finding(code: str, path: str, message: str) -> DeltaFinding:
    return DeltaFinding(code=code, path=path, message=message)


def _tracked_regular(root: pathlib.Path, path: str) -> bool:
    tracked = _git_bytes(root, "ls-files", "--error-unmatch", "-z", "--", path)
    if tracked.returncode != 0 or _decode_nul_paths(tracked.stdout) != {path}:
        return False
    try:
        metadata = os.lstat(root / path)
    except OSError:
        return False
    return stat.S_ISREG(metadata.st_mode)


def _valid_provenance(
    root: pathlib.Path,
    row_path: str,
    evidence: tuple[str, ...],
) -> bool:
    for item in evidence:
        match = re.fullmatch(
            r"git:([0-9a-f]{40})(?:\.\.([0-9a-f]{40}))?:(.+)",
            item,
        )
        if match is None or match.group(3) != row_path:
            continue
        older, newer = match.group(1), match.group(2)
        if not _commit_exists(root, older):
            continue
        if newer is None:
            return True
        if _commit_exists(root, newer) and _is_ancestor(root, older, newer):
            return True
    return False


def _valid_rollback(
    root: pathlib.Path,
    row_path: str,
    evidence: tuple[str, ...],
) -> bool:
    for item in evidence:
        match = re.fullmatch(r"git-revert:([0-9a-f]{40}):(.+)", item)
        if (
            match is not None
            and match.group(2) == row_path
            and _commit_exists(root, match.group(1))
        ):
            return True
    return False


def validate_delta_manifest(
    root: pathlib.Path,
    document: DeltaManifestDocument,
) -> tuple[DeltaFinding, ...]:
    repo_root = pathlib.Path(root).resolve()
    findings: list[DeltaFinding] = []
    manifest_path = DELTA_MANIFEST.as_posix()

    predecessor_valid = _commit_exists(repo_root, document.predecessor_closure)
    implementation_valid = _commit_exists(repo_root, document.implementation_base)
    if (
        not predecessor_valid
        or not implementation_valid
        or not _is_ancestor(
            repo_root,
            document.predecessor_closure,
            document.implementation_base,
        )
        or not _is_ancestor(repo_root, document.implementation_base, "HEAD")
    ):
        findings.append(
            _finding(
                "delta-baseline-invalid",
                manifest_path,
                "delta baseline commits or ancestry are invalid",
            )
        )
    if document.schema_version != SCHEMA_VERSION:
        findings.append(
            _finding(
                "delta-schema-invalid",
                manifest_path,
                "delta manifest schema version is invalid",
            )
        )
    if document.enforcement not in {"advisory", "blocking"}:
        findings.append(
            _finding(
                "delta-enforcement-invalid",
                manifest_path,
                "delta enforcement mode is invalid",
            )
        )
    if document.target_roots != TARGET_ROOTS:
        findings.append(
            _finding(
                "delta-target-roots-invalid",
                manifest_path,
                "delta target roots do not match the canonical ordered set",
            )
        )

    try:
        changed = set(
            changed_target_paths(
                repo_root,
                document.predecessor_closure,
                TARGET_ROOTS,
            )
        )
    except ContractInputError:
        changed = set()
        findings.append(
            _finding(
                "delta-git-delta-invalid",
                manifest_path,
                "target path delta could not be computed",
            )
        )
    rows = {entry.path: entry for entry in document.entries}
    for path in sorted(changed - rows.keys()):
        findings.append(
            _finding(
                "delta-coverage-missing",
                path,
                "changed target path is absent from the successor manifest",
            )
        )
    for path in sorted(rows.keys() - changed):
        findings.append(
            _finding(
                "delta-coverage-extra",
                path,
                "successor manifest path is not in the computed target delta",
            )
        )
    if tuple(rows) != tuple(sorted(rows)):
        findings.append(
            _finding(
                "delta-entry-order-invalid",
                manifest_path,
                "successor manifest entries are not sorted by path",
            )
        )

    try:
        readme_profiles = _load_readme_profiles(repo_root)
    except ContractInputError:
        readme_profiles = None
        findings.append(
            _finding(
                "delta-readme-registry-invalid",
                PROFILE_REGISTRY.as_posix(),
                "README profile registry is missing, unsafe, or invalid",
            )
        )
    else:
        try:
            inventory = current_target_inventory(repo_root)
        except ContractInputError:
            findings.append(
                _finding(
                    "delta-inventory-invalid",
                    manifest_path,
                    "current target inventory is not regular-file safe",
                )
            )
        else:
            for path in inventory.paths:
                if not path.endswith("README.md"):
                    continue
                matches = _matching_readme_profiles(path, readme_profiles)
                if len(matches) != 1:
                    findings.append(
                        _finding(
                            "delta-readme-profile-invalid",
                            path,
                            "README path does not match exactly one profile",
                        )
                    )

    for row in document.entries:
        if (
            row.surface_class not in SURFACE_CLASSES
            or row.surface_class != _surface_class(row.path)
        ):
            findings.append(
                _finding(
                    "delta-surface-class-invalid",
                    row.path,
                    "row surface class does not match the closed path-derived vocabulary",
                )
            )
        if row.changed_since != document.predecessor_closure:
            findings.append(
                _finding(
                    "delta-changed-since-invalid",
                    row.path,
                    "row predecessor relationship does not match the manifest",
                )
            )
        if row.disposition not in DISPOSITIONS:
            findings.append(
                _finding(
                    "delta-disposition-invalid",
                    row.path,
                    "row disposition is not in the canonical vocabulary",
                )
            )
        if row.spec_verdict not in REVIEW_VERDICTS or row.quality_verdict not in REVIEW_VERDICTS:
            findings.append(
                _finding(
                    "delta-review-invalid",
                    row.path,
                    "row review verdict is not in the canonical vocabulary",
                )
            )
        expected_secret_safety = (
            "path-only" if row.path.startswith("secrets/") else "not-applicable"
        )
        if (
            row.secret_safety not in SECRET_SAFETY_VALUES
            or row.secret_safety != expected_secret_safety
        ):
            findings.append(
                _finding(
                    "delta-secret-safety-invalid",
                    row.path,
                    "row secret-safety class does not match its path boundary",
                )
            )
        if not (row.path.endswith("README.md") and readme_profiles is None):
            expected_profile = _expected_profile(row.path, readme_profiles)
            if row.profile != expected_profile:
                findings.append(
                    _finding(
                        "delta-profile-invalid",
                        row.path,
                        "row document profile does not match its native consumer",
                    )
                )
        if not _tracked_regular(repo_root, row.canonical_owner):
            findings.append(
                _finding(
                    "delta-owner-invalid",
                    row.path,
                    "row canonical owner is not an existing tracked regular file",
                )
            )
        for consumer in row.direct_consumers:
            if not _tracked_regular(repo_root, consumer):
                findings.append(
                    _finding(
                        "delta-consumer-invalid",
                        row.path,
                        "row direct consumer is not an existing tracked regular file",
                    )
                )
                break
        for validator in row.validators:
            if not _tracked_regular(repo_root, validator):
                findings.append(
                    _finding(
                        "delta-validator-invalid",
                        row.path,
                        "row validator is not an existing tracked regular file",
                    )
                )
                break
        for test in row.tests:
            if not _tracked_regular(repo_root, test):
                findings.append(
                    _finding(
                        "delta-test-invalid",
                        row.path,
                        "row test is not an existing tracked regular file",
                    )
                )
                break

        if row.disposition in {"preserve", "update"} and row.replacement is not None:
            findings.append(
                _finding(
                    "delta-nondestructive-replacement-invalid",
                    row.path,
                    "non-destructive row must not declare replacement evidence",
                )
            )
        if row.disposition == "migrate" and (
            row.replacement in {None, "withdrawn", row.path}
            or not _tracked_regular(repo_root, row.replacement)
        ):
            findings.append(
                _finding(
                    "delta-migrate-replacement-invalid",
                    row.path,
                    "migrate row replacement is not a distinct tracked regular path",
                )
            )
        if row.disposition == "delete" and (
            row.replacement == row.path
            or (
                row.replacement not in {None, "withdrawn"}
                and not _tracked_regular(repo_root, row.replacement)
            )
        ):
            findings.append(
                _finding(
                    "delta-delete-replacement-invalid",
                    row.path,
                    "delete row replacement is not withdrawal or a distinct tracked regular path",
                )
            )

        if row.disposition in {"migrate", "delete"}:
            if not row.direct_consumers:
                findings.append(
                    _finding(
                        "delta-destructive-consumers-missing",
                        row.path,
                        "destructive row lacks direct-consumer evidence",
                    )
                )
            if row.replacement is None:
                findings.append(
                    _finding(
                        "delta-destructive-replacement-missing",
                        row.path,
                        "destructive row lacks replacement or withdrawal evidence",
                    )
                )
            if not row.provenance:
                findings.append(
                    _finding(
                        "delta-destructive-provenance-missing",
                        row.path,
                        "destructive row lacks immutable provenance evidence",
                    )
                )
            elif not _valid_provenance(repo_root, row.path, row.provenance):
                findings.append(
                    _finding(
                        "delta-destructive-provenance-invalid",
                        row.path,
                        "destructive row provenance is not commit-bound and path-bound",
                    )
                )
            if not row.rollback:
                findings.append(
                    _finding(
                        "delta-destructive-rollback-missing",
                        row.path,
                        "destructive row lacks rollback evidence",
                    )
                )
            elif not _valid_rollback(repo_root, row.path, row.rollback):
                findings.append(
                    _finding(
                        "delta-destructive-rollback-invalid",
                        row.path,
                        "destructive row rollback is not commit-bound and path-bound",
                    )
                )
            if not row.validators:
                findings.append(
                    _finding(
                        "delta-destructive-validators-missing",
                        row.path,
                        "destructive row lacks validator evidence",
                    )
                )
            elif any(
                not validator.startswith("scripts/validation/")
                for validator in row.validators
            ):
                findings.append(
                    _finding(
                        "delta-destructive-validators-invalid",
                        row.path,
                        "destructive row validators are outside the validation boundary",
                    )
                )
            if not row.tests:
                findings.append(
                    _finding(
                        "delta-destructive-tests-missing",
                        row.path,
                        "destructive row lacks test evidence",
                    )
                )
            elif any(not test.startswith("tests/") for test in row.tests):
                findings.append(
                    _finding(
                        "delta-destructive-tests-invalid",
                        row.path,
                        "destructive row tests are outside the test boundary",
                    )
                )
            if row.spec_verdict != "pass" or row.quality_verdict != "pass":
                findings.append(
                    _finding(
                        "delta-destructive-review-invalid",
                        row.path,
                        "destructive row lacks two passing review verdicts",
                    )
                )
    return tuple(sorted(set(findings)))


def _surface_class(path: str) -> str:
    pure = pathlib.PurePosixPath(path)
    suffix = pure.suffix.lower()
    if path.endswith("README.md"):
        return "readme"
    if path == "examples/sample-web-service/service.md":
        return "typed-example"
    if path.startswith("archive/") and suffix in {".md", ".mdx"}:
        return "content-archive"
    if path.startswith(".github/"):
        return "native-platform"
    if path.startswith("tests/"):
        return "test-or-fixture"
    if suffix == ".sh":
        return "executable-script"
    if suffix == ".py":
        return "python-source"
    if suffix in {
        ".cfg",
        ".conf",
        ".env",
        ".example",
        ".hcl",
        ".ini",
        ".json",
        ".toml",
        ".xml",
        ".yaml",
        ".yml",
    }:
        return "native-configuration"
    return "native-file"


def _canonical_owner(path: str) -> str:
    fixture_owners = (
        (
            "tests/fixtures/compose-core-readiness/",
            "tests/validation/test_compose_core_readiness.py",
        ),
        (
            "tests/fixtures/postgres-logical-upgrade/",
            "tests/validation/test_postgres_logical_upgrade_rehearsal.py",
        ),
        (
            "tests/fixtures/sample-service-delivery/",
            "tests/validation/test_sample_service_delivery_rehearsal.py",
        ),
        (
            "tests/fixtures/supply-chain/",
            "tests/validation/test_supply_chain_policy.py",
        ),
    )
    for prefix, owner in fixture_owners:
        if path.startswith(prefix):
            return owner
    if path == "projects/storybook/nextjs/package-lock.json":
        return "projects/storybook/nextjs/package.json"
    if path == "scripts/validation/check-target-surface-delta-contract.py":
        return "scripts/validation/target_surface_delta_contract.py"
    return path


def _direct_consumers(path: str) -> tuple[str, ...]:
    if path == "projects/storybook/nextjs/package-lock.json":
        return (".github/workflows/ci-quality.yml",)
    if path.startswith("tests/fixtures/"):
        return (_canonical_owner(path),)
    if path in {
        "infra/supply-chain.cosign-offline-signing-config.json",
        "infra/supply-chain.cosign-offline-trusted-root.json",
    }:
        return ("scripts/security/verify-sample-service-supply-chain.sh",)
    if path.startswith("infra/supply-chain."):
        return ("scripts/validation/check-supply-chain-policy.py",)
    if path == "examples/sample-web-service/.dockerignore":
        return ("scripts/validation/check-supply-chain-policy.py",)
    if path == "examples/sample-web-service/Dockerfile":
        return ("examples/sample-web-service/docker-compose.yml",)
    if path == "examples/sample-web-service/docker-compose.yml":
        return ("examples/sample-web-service/service.md",)
    if path == "examples/sample-web-service/service.md":
        return ("examples/sample-web-service/README.md",)
    if path == ".github/workflows/ci-quality.yml":
        return (".github/rulesets/main-protection.md",)
    if path.startswith(".github/workflows/"):
        return (".github/INDEX.md",)
    if path == ".github/rulesets/main-protection.md":
        return (".github/INDEX.md",)
    if path == "scripts/validation/target_surface_delta_contract.py":
        return (
            "scripts/validation/check-target-surface-delta-contract.py",
            "tests/validation/test_target_surface_delta_contracts.py",
        )
    if path == "scripts/validation/check-target-surface-delta-contract.py":
        return (
            "scripts/validation/check-repo-contracts.sh",
            "scripts/validation/run-local-qa-gates.sh",
        )
    if path == "tests/validation/test_target_surface_delta_contracts.py":
        return (
            "scripts/validation/check-repo-contracts.sh",
            "scripts/validation/run-local-qa-gates.sh",
        )
    if path == "scripts/validation/check-repo-contracts.sh":
        return (
            ".github/workflows/ci-quality.yml",
            ".pre-commit-config.yaml",
            "scripts/validation/run-local-qa-gates.sh",
        )
    if path == "scripts/validation/run-local-qa-gates.sh":
        return ("scripts/validation/validate-harness.sh",)
    return ()


def _classification_finding(path: str, disposition: str) -> str:
    if disposition == "update":
        return PLANNED_UPDATE_FINDINGS[path]
    owner = _canonical_owner(path)
    if path.startswith("tests/fixtures/"):
        return (
            f"Preserve {path} as value-free regression input exercised by {owner}."
        )
    if path.startswith("tests/"):
        return (
            f"Preserve {path} as the tracked test oracle for its current validation "
            "boundary."
        )
    if path.startswith(".github/workflows/"):
        return (
            f"Preserve {path} as a GitHub-native workflow registered by "
            ".github/INDEX.md."
        )
    if path.startswith("infra/") and pathlib.PurePosixPath(path).name.startswith(
        "docker-compose"
    ):
        return (
            f"Preserve {path} as its service-local Compose declaration; no root "
            "Compose consumer is asserted."
        )
    if path.startswith("infra/supply-chain."):
        return (
            f"Preserve {path} as a value-free supply-chain policy or trust input "
            "consumed by its declared checker."
        )
    if path.startswith("scripts/"):
        return (
            f"Preserve {path} as an implemented validation or operations support "
            f"surface owned by {owner}."
        )
    if path.startswith("projects/"):
        return (
            f"Preserve {path} as a project-native dependency or source surface "
            f"owned by {owner}."
        )
    if path.startswith("examples/"):
        return (
            f"Preserve {path} as a bounded sample-service implementation artifact "
            f"owned by {owner}."
        )
    if path.startswith(".github/"):
        return (
            f"Preserve {path} as a GitHub-native repository control surface owned "
            f"by {owner}."
        )
    return f"Preserve {path} as the current tracked native target owned by {owner}."


def _bootstrap_row(
    path: str,
    predecessor_commit: str,
    implementation_base_commit: str,
    evidence_head: str,
    readme_profiles: dict[str, tuple[str, ...]] | None,
) -> DeltaManifestRow:
    disposition = "update" if path in PLANNED_UPDATE_PATHS else "preserve"
    return DeltaManifestRow(
        path=path,
        surface_class=_surface_class(path),
        profile=_expected_profile(path, readme_profiles),
        changed_since=predecessor_commit,
        disposition=disposition,
        canonical_owner=_canonical_owner(path),
        direct_consumers=_direct_consumers(path),
        finding=_classification_finding(path, disposition),
        replacement=None,
        secret_safety=(
            "path-only" if path.startswith("secrets/") else "not-applicable"
        ),
        validators=(
            "scripts/validation/check-target-surface-delta-contract.py",
        ),
        tests=("tests/validation/test_target_surface_delta_contracts.py",),
        provenance=(
            f"git:{predecessor_commit}..{evidence_head}:{path}",
            f"implementation-base:{implementation_base_commit}",
        ),
        rollback=(f"git-revert:{evidence_head}:{path}",),
        spec_verdict="pending",
        quality_verdict="pending",
    )


def _row_mapping(row: DeltaManifestRow) -> dict[str, object]:
    raw = asdict(row)
    for key in (
        "direct_consumers",
        "validators",
        "tests",
        "provenance",
        "rollback",
    ):
        raw[key] = list(raw[key])
    return raw


def _document_mapping(document: DeltaManifestDocument) -> dict[str, object]:
    return {
        "schema_version": document.schema_version,
        "predecessor_closure": document.predecessor_closure,
        "implementation_base": document.implementation_base,
        "enforcement": document.enforcement,
        "target_roots": list(document.target_roots),
        "entries": [_row_mapping(row) for row in document.entries],
    }


def _write_new_file(path: pathlib.Path, payload: bytes) -> None:
    try:
        file_descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o644,
        )
    except OSError:
        raise ContractInputError from None
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(file_descriptor, payload[offset:])
    except OSError:
        raise ContractInputError from None
    finally:
        os.close(file_descriptor)


def bootstrap_delta_manifest(
    root: pathlib.Path,
    output: pathlib.Path,
    predecessor_commit: str,
    implementation_base_commit: str,
) -> None:
    repo_root = pathlib.Path(root).resolve()
    candidate = pathlib.Path(output)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    try:
        relative = candidate.relative_to(repo_root).as_posix()
    except ValueError:
        raise ContractInputError from None
    _canonical_relative(relative)
    if os.path.lexists(candidate):
        raise ContractInputError
    if (
        not _commit_exists(repo_root, predecessor_commit)
        or not _commit_exists(repo_root, implementation_base_commit)
        or not _is_ancestor(
            repo_root,
            predecessor_commit,
            implementation_base_commit,
        )
        or not _is_ancestor(repo_root, implementation_base_commit, "HEAD")
    ):
        raise ContractInputError

    readme_profiles = _load_readme_profiles(repo_root)
    head_result = _git_text(repo_root, "rev-parse", "HEAD")
    evidence_head = head_result.stdout.strip()
    if head_result.returncode != 0 or FULL_SHA_RE.fullmatch(evidence_head) is None:
        raise ContractInputError
    rows = tuple(
        _bootstrap_row(
            path,
            predecessor_commit,
            implementation_base_commit,
            evidence_head,
            readme_profiles,
        )
        for path in changed_target_paths(repo_root, predecessor_commit)
    )
    document = DeltaManifestDocument(
        schema_version=SCHEMA_VERSION,
        predecessor_closure=predecessor_commit,
        implementation_base=implementation_base_commit,
        enforcement="advisory",
        target_roots=TARGET_ROOTS,
        entries=rows,
    )
    payload = yaml.safe_dump(
        _document_mapping(document),
        sort_keys=False,
        allow_unicode=False,
        width=1_000,
    ).encode("utf-8")
    if len(payload) > MAX_CONTRACT_FILE_BYTES:
        raise ContractInputError
    candidate.parent.mkdir(parents=True, exist_ok=True)
    _write_new_file(candidate, payload)


def render_delta_summary(
    document: DeltaManifestDocument,
    inventory: TargetInventory,
) -> str:
    dispositions = collections.Counter(row.disposition for row in document.entries)
    lines = [
        "# Target Surface Delta Summary",
        "",
        "> Generated by `scripts/validation/check-target-surface-delta-contract.py`; "
        "do not edit manually.",
        "",
        f"- Schema version: `{document.schema_version}`",
        f"- Predecessor closure: `{document.predecessor_closure}`",
        f"- Implementation base: `{document.implementation_base}`",
        f"- Enforcement: `{document.enforcement}`",
        f"- Delta entries: {len(document.entries)}",
        f"- Current tracked target paths: {len(inventory.paths)}",
        f"- Current Markdown/MDX paths: {inventory.markdown_count}",
        f"- Current README paths: {inventory.readme_count}",
        "",
        "## Current Inventory",
        "",
        "| Root | Tracked paths |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{root_name}` | {count} |"
        for root_name, count in inventory.counts_by_root
    )
    lines.extend(
        [
            "",
            "## Dispositions",
            "",
        ]
    )
    lines.extend(
        f"- `{disposition}`: {dispositions[disposition]}"
        for disposition in ("preserve", "update", "migrate", "delete")
    )
    lines.extend(
        [
            "",
            "## Classified Delta",
            "",
            "| Path | Surface | Profile | Disposition | Secret safety | Spec | Quality |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in document.entries:
        profile = row.profile if row.profile is not None else "none"
        lines.append(
            f"| `{row.path}` | `{row.surface_class}` | `{profile}` | "
            f"`{row.disposition}` | `{row.secret_safety}` | "
            f"`{row.spec_verdict}` | `{row.quality_verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            "- This summary contains repository paths and typed classifications only.",
            "- Secret payloads, credentials, raw logs, and runtime state are not read or rendered.",
            "- Pending verdicts are advisory and do not authorize destructive disposition.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_summary(root: pathlib.Path, summary: str) -> None:
    repo_root = pathlib.Path(root).resolve()
    relative = _canonical_relative(DELTA_SUMMARY.as_posix())
    payload = summary.encode("utf-8")
    if len(payload) > MAX_CONTRACT_FILE_BYTES:
        raise ContractInputError
    try:
        root_descriptor = os.open(
            repo_root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
        )
    except OSError:
        raise ContractInputError from None
    descriptors = [root_descriptor]
    try:
        parts = pathlib.PurePosixPath(relative).parts
        for component in parts[:-1]:
            descriptor = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptors[-1],
            )
            descriptors.append(descriptor)
        parent_descriptor = descriptors[-1]
        try:
            file_descriptor = os.open(
                parts[-1],
                os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW,
                dir_fd=parent_descriptor,
            )
        except FileNotFoundError:
            file_descriptor = os.open(
                parts[-1],
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o644,
                dir_fd=parent_descriptor,
            )
        descriptors.append(file_descriptor)
        opened = os.fstat(file_descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise ContractInputError
        offset = 0
        while offset < len(payload):
            written = os.write(file_descriptor, payload[offset:])
            if written <= 0:
                raise ContractInputError
            offset += written
        os.fsync(file_descriptor)
        final = os.fstat(file_descriptor)
        linked = os.stat(
            parts[-1],
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        opened_identity = (opened.st_dev, opened.st_ino, opened.st_mode)
        if (
            opened_identity
            != (final.st_dev, final.st_ino, final.st_mode)
            or opened_identity
            != (linked.st_dev, linked.st_ino, linked.st_mode)
            or final.st_size != len(payload)
        ):
            raise ContractInputError
    except OSError:
        raise ContractInputError from None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _summary_finding(root: pathlib.Path, expected: str) -> DeltaFinding | None:
    try:
        actual = _read_contract_text(root, DELTA_SUMMARY.as_posix())
    except ContractInputError:
        return _finding(
            "delta-summary-missing",
            DELTA_SUMMARY.as_posix(),
            "generated successor summary is missing or unsafe",
        )
    if actual != expected:
        return _finding(
            "delta-summary-stale",
            DELTA_SUMMARY.as_posix(),
            "generated successor summary is stale",
        )
    return None


def _blocking_review_findings(
    document: DeltaManifestDocument,
) -> tuple[DeltaFinding, ...]:
    findings: list[DeltaFinding] = []
    for row in document.entries:
        if row.spec_verdict != "pass":
            findings.append(
                _finding(
                    "delta-spec-verdict-not-pass",
                    row.path,
                    "blocking mode requires a passing specification verdict",
                )
            )
        if row.quality_verdict != "pass":
            findings.append(
                _finding(
                    "delta-quality-verdict-not-pass",
                    row.path,
                    "blocking mode requires a passing quality verdict",
                )
            )
    return tuple(findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Spec 135 successor target-surface delta."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=("advisory", "blocking"))
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument(
        "--predecessor-commit",
        default=DEFAULT_PREDECESSOR_CLOSURE,
    )
    parser.add_argument(
        "--implementation-base-commit",
        default=DEFAULT_IMPLEMENTATION_BASE,
    )
    arguments = parser.parse_args(argv)
    root = pathlib.Path(arguments.root).resolve()

    if arguments.bootstrap:
        if arguments.write_summary:
            print(
                "delta-input-invalid: bootstrap and summary write are mutually exclusive",
                file=sys.stderr,
            )
            return 2
        try:
            bootstrap_delta_manifest(
                root,
                root / DELTA_MANIFEST,
                arguments.predecessor_commit,
                arguments.implementation_base_commit,
            )
        except ContractInputError:
            print(
                f"delta-bootstrap-refused: {DELTA_MANIFEST}: "
                "bootstrap requires a missing output and valid Git baselines",
                file=sys.stderr,
            )
            return 2
        return 0

    try:
        document = load_delta_manifest(root)
        findings = list(validate_delta_manifest(root, document))
        blocking = (
            document.enforcement == "blocking" or arguments.mode == "blocking"
        )
        if blocking:
            findings.extend(_blocking_review_findings(document))
        if arguments.write_summary and findings:
            for finding in sorted(set(findings)):
                print(
                    f"{finding.code}: {finding.path}: {finding.message}",
                    file=sys.stderr,
                )
            return 1
        inventory = current_target_inventory(root)
        summary = render_delta_summary(document, inventory)
        if arguments.write_summary:
            _write_summary(root, summary)
        else:
            freshness = _summary_finding(root, summary)
            if freshness is not None:
                findings.append(freshness)
    except ContractInputError:
        print(
            f"delta-manifest-invalid: {DELTA_MANIFEST}: "
            "successor manifest or repository input is invalid",
            file=sys.stderr,
        )
        return 2

    for finding in sorted(set(findings)):
        print(
            f"{finding.code}: {finding.path}: {finding.message}",
            file=sys.stderr,
        )
    return 1 if blocking and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
