from __future__ import annotations

import argparse
import os
import pathlib
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from typing import Final

import yaml


TARGET_MANIFEST: Final = pathlib.PurePosixPath(
    "docs/90.references/data/governance/document-corpus-lifecycle/"
    "target-surface-convergence.yaml"
)
TARGET_ROOTS: Final = (
    ".github",
    "archive",
    "examples",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
)
PHANTOM_GITLINK_PATH: Final = "projects/storybook/mcp"
PHANTOM_CLAIM_PATHS: Final = (
    ".prettierignore",
    "projects/storybook/README.md",
    "projects/storybook/nextjs/README.md",
    "scripts/knowledge/report-graphify-health.sh",
    "scripts/hooks/agent-event-hook.sh",
)
INFLUX_ACTIVE_PATHS: Final = (
    "infra/04-data/analytics/influxdb/README.md",
    "docs/01.requirements/005-data-analytics.md",
    "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
    "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
    "docs/03.specs/005-data-analytics/README.md",
    "docs/03.specs/005-data-analytics/spec.md",
    "docs/05.operations/guides/04-data/analytics/README.md",
    "docs/05.operations/guides/04-data/analytics/influxdb.md",
    "docs/05.operations/policies/04-data/analytics/influxdb.md",
    "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
)
REMOVED_ACTIVE_PATTERNS: Final = (
    re.compile(r"(?<![A-Za-z0-9_])influxdb[ \t]+v?2(?![A-Za-z0-9_])", re.IGNORECASE),
    re.compile(r"(?<![A-Za-z0-9_])legacy[ \t]+flux(?![A-Za-z0-9_])", re.IGNORECASE),
    re.compile(
        r"(?<![A-Za-z0-9_.-])docker-compose\.v2\.yml(?![A-Za-z0-9_.-])",
        re.IGNORECASE,
    ),
    re.compile(r"(?<![0-9])8086(?![0-9])"),
)
PHANTOM_CLAIM_PATTERNS: Final = (re.compile(re.escape(PHANTOM_GITLINK_PATH)),)
SAMPLE_SERVICE_PATH: Final = "examples/sample-web-service/service.md"
SAMPLE_SERVICE_METADATA: Final = {
    "status": "active",
    "artifact_id": "spec:sample-web-service",
    "artifact_type": "spec",
    "parent_ids": ["spec:133-target-surface-contract-convergence"],
}
SAMPLE_SERVICE_KEYS: Final = (
    "status",
    "artifact_id",
    "artifact_type",
    "parent_ids",
)
SAMPLE_SERVICE_HEADINGS: Final = (
    "## Overview",
    "## Parent and Scope",
    "## Image and Build",
    "## Security",
    "## Networking and Storage",
    "## Secrets",
    "## Health and Operations",
    "## Validation",
    "## Related Documents",
)
SAMPLE_SERVICE_RESIDUE: Final = (
    "<artifact-id>",
    "<parent-artifact-id>",
    "{{",
    "}}",
    "When authoring a real service",
    "copy the template",
)
OPENSEARCH_DUPLICATE_PATH: Final = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example"
)
OPENSEARCH_RETAINED_PATH: Final = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt"
)
MAX_CONTRACT_FILE_BYTES: Final = 2 * 1_048_576
FULL_SHA_RE: Final = re.compile(r"^[0-9a-f]{40}$")

FINDING_CODES: Final = frozenset(
    {
        "target-duplicate-disposition-invalid",
        "target-manifest-coverage-missing",
        "target-manifest-invalid",
        "target-phantom-gitlink-claim",
        "target-phantom-gitlink-present",
        "target-removed-active-claim",
        "target-removed-path-present",
        "target-sample-service-metadata-invalid",
        "target-sample-service-sections-invalid",
        "target-sample-service-template-residue",
    }
)


@dataclass(frozen=True, order=True, slots=True)
class Finding:
    code: str
    path: str
    message: str


class ContractInputError(Exception):
    pass


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
    if not isinstance(value, str) or not value:
        raise ContractInputError
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix():
        raise ContractInputError
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ContractInputError
    return value


def _read_contract_text(repo_root: pathlib.Path, relative: str) -> str | None:
    try:
        canonical = _canonical_relative(relative)
        parent_descriptor = os.open(repo_root, os.O_RDONLY | os.O_DIRECTORY)
    except (ContractInputError, OSError):
        return None

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
            return None
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
            return None
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
            return None
        return payload.decode("utf-8", errors="strict")
    except (OSError, UnicodeError):
        return None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _git(
    repo_root: pathlib.Path, *arguments: str
) -> subprocess.CompletedProcess[str] | None:
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
        return None


def _load_manifest(
    repo_root: pathlib.Path, manifest_path: pathlib.Path
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    try:
        relative = manifest_path.relative_to(repo_root).as_posix()
        manifest_text = _read_contract_text(repo_root, relative)
        if manifest_text is None:
            raise ContractInputError
        document = _safe_load_unique(manifest_text)
        if not isinstance(document, dict):
            raise ContractInputError
        if document.get("schema_version") != 2:
            raise ContractInputError
        if document.get("wave") != "target-surface-convergence":
            raise ContractInputError
        baseline = document.get("baseline_commit")
        if not isinstance(baseline, str) or FULL_SHA_RE.fullmatch(baseline) is None:
            raise ContractInputError
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise ContractInputError
        rows: dict[str, dict[str, object]] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                raise ContractInputError
            source_path = _canonical_relative(entry.get("source_path"))
            if source_path in rows:
                raise ContractInputError
            target_path = entry.get("target_path")
            if target_path is not None:
                _canonical_relative(target_path)
            rows[source_path] = entry
    except (ContractInputError, OSError, UnicodeError, yaml.YAMLError):
        raise ContractInputError from None
    return document, rows


def _manifest_coverage_findings(
    repo_root: pathlib.Path,
    baseline: str,
    rows: dict[str, dict[str, object]],
) -> list[Finding]:
    result = _git(
        repo_root,
        "ls-tree",
        "-r",
        "--name-only",
        baseline,
        "--",
        *TARGET_ROOTS,
    )
    if result is None or result.returncode != 0:
        raise ContractInputError
    expected: set[str] = set()
    for raw_path in result.stdout.splitlines():
        expected.add(_canonical_relative(raw_path))

    required_contract_paths = {
        *PHANTOM_CLAIM_PATHS,
        *INFLUX_ACTIVE_PATHS,
        SAMPLE_SERVICE_PATH,
        OPENSEARCH_DUPLICATE_PATH,
        OPENSEARCH_RETAINED_PATH,
    }
    missing = sorted((expected | required_contract_paths) - rows.keys())
    return [
        Finding(
            "target-manifest-coverage-missing",
            path,
            "required target path is absent from the target manifest",
        )
        for path in missing
    ]


def _removed_path_findings(
    repo_root: pathlib.Path, rows: dict[str, dict[str, object]]
) -> list[Finding]:
    findings: list[Finding] = []
    for path, row in rows.items():
        if row.get("disposition") != "delete":
            continue
        if row.get("review_verdict") != {
            "specification": "pass",
            "quality": "pass",
        }:
            continue
        if os.path.lexists(repo_root / path):
            findings.append(
                Finding(
                    "target-removed-path-present",
                    path,
                    "reviewed removed target path is present",
                )
            )
    return findings


def _active_claim_findings(
    repo_root: pathlib.Path,
    paths: tuple[str, ...],
    patterns: tuple[re.Pattern[str], ...],
    code: str,
    message: str,
) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        text = _read_contract_text(repo_root, path)
        if text is None or any(pattern.search(text) for pattern in patterns):
            findings.append(Finding(code, path, message))
    return findings


def _gitlink_findings(repo_root: pathlib.Path) -> list[Finding]:
    result = _git(repo_root, "ls-files", "--stage", "--", "projects/storybook")
    if result is None or result.returncode != 0:
        raise ContractInputError
    findings: list[Finding] = []
    for line in result.stdout.splitlines():
        index_entry, separator, path = line.partition("\t")
        if separator and index_entry.startswith("160000 "):
            findings.append(
                Finding(
                    "target-phantom-gitlink-present",
                    _canonical_relative(path),
                    "tracked Storybook gitlink is forbidden by the target contract",
                )
            )
    return findings


def _sample_service_findings(
    repo_root: pathlib.Path, rows: dict[str, dict[str, object]]
) -> list[Finding]:
    path = SAMPLE_SERVICE_PATH
    text = _read_contract_text(repo_root, path)
    row = rows.get(path)
    metadata_valid = False
    sections_valid = False
    if text is not None:
        lines = text.splitlines()
        if len(lines) >= 3 and lines[0] == "---":
            try:
                closing = lines.index("---", 1)
                raw_frontmatter = lines[1:closing]
                frontmatter = yaml.safe_load("\n".join(raw_frontmatter))
                keys = tuple(
                    line.split(":", 1)[0]
                    for line in raw_frontmatter
                    if line and not line.startswith((" ", "\t")) and ":" in line
                )
                metadata_valid = (
                    frontmatter == SAMPLE_SERVICE_METADATA
                    and keys == SAMPLE_SERVICE_KEYS
                    and isinstance(row, dict)
                    and row.get("surface_class") == "typed-example"
                    and row.get("disposition") == "migrate"
                    and row.get("target_path") == path
                )
            except (ValueError, yaml.YAMLError):
                metadata_valid = False
        sections_valid = (
            tuple(line for line in lines if line.startswith("## "))
            == SAMPLE_SERVICE_HEADINGS
        )

    findings: list[Finding] = []
    if not metadata_valid:
        findings.append(
            Finding(
                "target-sample-service-metadata-invalid",
                path,
                "sample Service metadata does not match its exact target contract",
            )
        )
    if not sections_valid:
        findings.append(
            Finding(
                "target-sample-service-sections-invalid",
                path,
                "sample Service sections do not match the registered envelope",
            )
        )
    if text is None or any(marker in text for marker in SAMPLE_SERVICE_RESIDUE):
        findings.append(
            Finding(
                "target-sample-service-template-residue",
                path,
                "sample Service contains unreadable or uninstantiated template content",
            )
        )
    return findings


def _blob_at(repo_root: pathlib.Path, revision: str, path: str) -> str | None:
    result = _git(repo_root, "rev-parse", f"{revision}:{path}")
    if result is None or result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value if FULL_SHA_RE.fullmatch(value) else None


def _duplicate_disposition_findings(
    repo_root: pathlib.Path,
    baseline: str,
    rows: dict[str, dict[str, object]],
) -> list[Finding]:
    duplicate = rows.get(OPENSEARCH_DUPLICATE_PATH)
    retained = rows.get(OPENSEARCH_RETAINED_PATH)
    duplicate_blob = _blob_at(repo_root, baseline, OPENSEARCH_DUPLICATE_PATH)
    retained_blob = _blob_at(repo_root, baseline, OPENSEARCH_RETAINED_PATH)
    try:
        duplicate_exists = os.path.lexists(repo_root / OPENSEARCH_DUPLICATE_PATH)
        retained_metadata = os.lstat(repo_root / OPENSEARCH_RETAINED_PATH)
        retained_exists = stat.S_ISREG(retained_metadata.st_mode)
    except OSError:
        duplicate_exists = os.path.lexists(repo_root / OPENSEARCH_DUPLICATE_PATH)
        retained_exists = False

    valid = (
        isinstance(duplicate, dict)
        and duplicate.get("target_path") is None
        and duplicate.get("disposition") == "delete"
        and duplicate.get("review_verdict")
        == {"specification": "pass", "quality": "pass"}
        and isinstance(retained, dict)
        and retained.get("target_path") == OPENSEARCH_RETAINED_PATH
        and not duplicate_exists
        and retained_exists
        and duplicate_blob is not None
        and duplicate_blob == retained_blob
    )
    if valid:
        return []
    return [
        Finding(
            "target-duplicate-disposition-invalid",
            OPENSEARCH_DUPLICATE_PATH,
            "reviewed duplicate disposition does not match retained target evidence",
        )
    ]


def validate(
    repo_root: pathlib.Path | str,
    manifest_path: pathlib.Path | str | None = None,
) -> tuple[Finding, ...]:
    root = pathlib.Path(repo_root).resolve()
    manifest_candidate = (
        pathlib.Path(manifest_path)
        if manifest_path is not None
        else root / TARGET_MANIFEST
    )
    if not manifest_candidate.is_absolute():
        manifest_candidate = root / manifest_candidate
    try:
        manifest = manifest_candidate.resolve(strict=False)
        manifest_display = manifest.relative_to(root).as_posix()
    except ValueError:
        return (
            Finding(
                "target-manifest-invalid",
                TARGET_MANIFEST.as_posix(),
                "target manifest or its immutable Git baseline is invalid",
            ),
        )

    try:
        document, rows = _load_manifest(root, manifest)
        baseline = str(document["baseline_commit"])
        findings = _manifest_coverage_findings(root, baseline, rows)
        findings.extend(_removed_path_findings(root, rows))
        findings.extend(
            _active_claim_findings(
                root,
                INFLUX_ACTIVE_PATHS,
                REMOVED_ACTIVE_PATTERNS,
                "target-removed-active-claim",
                "active target surface contains a removed runtime claim",
            )
        )
        findings.extend(
            _active_claim_findings(
                root,
                PHANTOM_CLAIM_PATHS,
                PHANTOM_CLAIM_PATTERNS,
                "target-phantom-gitlink-claim",
                "active target surface contains a phantom Storybook gitlink claim",
            )
        )
        findings.extend(_gitlink_findings(root))
        findings.extend(_sample_service_findings(root, rows))
        findings.extend(_duplicate_disposition_findings(root, baseline, rows))
    except ContractInputError:
        return (
            Finding(
                "target-manifest-invalid",
                manifest_display,
                "target manifest or its immutable Git baseline is invalid",
            ),
        )
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate focused target-surface convergence contracts."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest")
    arguments = parser.parse_args(argv)
    findings = validate(arguments.root, arguments.manifest)
    for finding in findings:
        print(
            f"{finding.code}: {finding.path}: {finding.message}",
            file=sys.stderr,
        )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
