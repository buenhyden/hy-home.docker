from __future__ import annotations

import collections
import copy
import datetime as dt
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "validation" / "check-document-metadata.py"
PROFILES = ROOT / "docs" / "99.templates" / "support" / "document-metadata-profiles.yaml"
MIGRATION_CONTRACT = (
    ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "document-corpus-migration-contract.yaml"
)

spec = importlib.util.spec_from_file_location("check_document_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def write_doc(path: pathlib.Path, frontmatter: dict[str, object] | None, body: str = "# Fixture\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is None:
        path.write_text(body, encoding="utf-8")
        return
    rendered = yaml.safe_dump(frontmatter, sort_keys=False).rstrip()
    path.write_text(f"---\n{rendered}\n---\n\n{body}", encoding="utf-8")


def body_with_headings(*headings: str) -> str:
    """Build a concrete target body for tests whose subject is not body validation."""

    sections = "\n\n".join(f"{heading}\n\nFixture content." for heading in headings)
    return f"# Fixture\n\n{sections}\n"


PRD_TARGET_BODY = body_with_headings(
    "## Overview",
    "## Problem and Stakeholders",
    "## Requirements",
    "## Acceptance and Verification",
    "## Scope and Non-goals",
    "## Risks and Dependencies",
    "## Related Documents",
)

SPEC_TARGET_BODY = body_with_headings(
    "## Overview",
    "## Boundaries and Inputs",
    "## Contracts",
    "## Core Design",
    "## Interfaces and Data",
    "## Failure Modes and Guardrails",
    "## Verification",
    "## Related Documents",
)


def run_checker(
    root: pathlib.Path,
    mode: str = "report",
    *extra: str,
    env: dict[str, str] | None = None,
    profiles: pathlib.Path = PROFILES,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root),
            "--profiles",
            str(profiles),
            "--mode",
            mode,
            *extra,
        ],
        cwd=ROOT,
        env={**os.environ, **(env or {})},
        capture_output=True,
        text=True,
        check=False,
    )


def git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def failing_git_probe_env(directory: pathlib.Path, probe_name: str) -> dict[str, str]:
    """Return an environment whose Git delegates except for one discovery probe."""

    real_git = shutil.which("git")
    if real_git is None:
        raise RuntimeError("Git is required for metadata fixtures")
    bin_dir = directory / "bin"
    bin_dir.mkdir()
    wrapper = bin_dir / "git"
    wrapper.write_text(
        f"""#!{sys.executable}
import subprocess
import sys

args = sys.argv[1:]
probe = args[2:] if len(args) >= 2 and args[0] == "-C" else args
probe_name = {probe_name!r}
should_fail = (
    probe_name == "tracked"
    and probe[:2] == ["ls-files", "-z"]
    and "--others" not in probe
) or (
    probe_name == "unstaged"
    and probe[:1] == ["diff"]
    and "--cached" not in probe
    and not any(item.endswith("...HEAD") for item in probe)
) or (
    probe_name == "staged"
    and probe[:1] == ["diff"]
    and "--cached" in probe
) or (
    probe_name == "untracked"
    and probe[:1] == ["ls-files"]
    and "--others" in probe
)
if should_fail:
    raise SystemExit(73)
raise SystemExit(subprocess.run([{real_git!r}, *args], check=False).returncode)
""",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"}


def init_git(root: pathlib.Path) -> None:
    self_check = git(root, "init", "-q")
    if self_check.returncode != 0:
        raise RuntimeError(self_check.stderr)
    git(root, "config", "user.name", "Metadata Fixture")
    git(root, "config", "user.email", "metadata@example.invalid")


def commit_all(root: pathlib.Path, message: str = "fixture") -> None:
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    committed = git(root, "commit", "-qm", message)
    if committed.returncode != 0:
        raise RuntimeError(committed.stderr)


def copy_tracked_contract_fixture(root: pathlib.Path) -> pathlib.Path:
    """Copy the canonical contract inputs into a small isolated Git repository."""

    result = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--",
            "README.md",
            "_workspace/README.md",
            "_workspace/repo-support/README.md",
            "docs/05.operations/releases/README.md",
            "docs/99.templates/templates/**/*.template.md",
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "docs/99.templates/templates/spec-contracts/schema.template.graphql",
            "docs/99.templates/templates/spec-contracts/service.template.proto",
            "docs/99.templates/support/*.md",
            "docs/99.templates/support/document-metadata-profiles.yaml",
            "docs/00.agent-governance/rules/stage-authoring-matrix.md",
        ],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    paths = [pathlib.Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]
    for relative_path in paths:
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative_path, target)
    init_git(root)
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    return root / "docs/99.templates/support/document-metadata-profiles.yaml"


class FrontmatterParsingTests(unittest.TestCase):
    def test_valid_yaml_frontmatter_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "valid.md"
            write_doc(path, {"status": "active", "parent_ids": ["PRD-001"]})
            self.assertEqual(
                {"status": "active", "parent_ids": ["PRD-001"]},
                metadata.parse_frontmatter(path),
            )

    def test_missing_frontmatter_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "README.md"
            write_doc(path, None)
            self.assertEqual({}, metadata.parse_frontmatter(path))

    def test_invalid_yaml_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "invalid.md"
            path.write_text("---\nstatus: [active\n---\n# Invalid\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "duplicate.md"
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)

    def test_unhashable_yaml_mapping_key_is_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "unhashable.md"
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError) as context:
                metadata.parse_frontmatter(path)
            self.assertEqual("malformed-yaml", context.exception.code)


class ProfileSchemaTests(unittest.TestCase):
    def mutate_and_load(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "profiles.yaml"
            values = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
            mutate(values)
            target.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
            with self.assertRaises(metadata.ProfileError):
                metadata.load_profiles(target)

    def mutate_migration_contract_and_load(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "migration.yaml"
            values = yaml.safe_load(MIGRATION_CONTRACT.read_text(encoding="utf-8"))
            mutate(values)
            target.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
            with self.assertRaises(metadata.ProfileError):
                metadata.load_migration_contract(target)

    def valid_static_manifest(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "wave": "foundation",
            "baseline_commit": "a" * 40,
            "generated_by": "scripts/validation/check-document-corpus-lifecycle.py",
            "enforcement": "blocking",
            "entries": [
                {
                    "source_path": "docs/source.md",
                    "target_path": None,
                    "artifact_id": "reference:source",
                    "artifact_type": "reference",
                    "status_before": "active",
                    "status_after": "archived",
                    "parent_ids": ["spec:source"],
                    "disposition": "delete",
                    "canonical_replacement": None,
                    "active_consumers": [],
                    "partition_plan": None,
                    "preservation_class": "git-history",
                    "evidence": {
                        "commands": ["git show BASE:docs/source.md"],
                        "sources": ["docs/source.md"],
                        "repository_paths": ["docs/source.md"],
                        "consumer_scan": ["rg --fixed-strings docs/source.md"],
                        "rollback": ["revert logical task commit"],
                    },
                    "review_verdict": {
                        "specification": "pass",
                        "quality": "pass",
                    },
                }
            ],
        }

    def valid_static_exception_document(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "exceptions": [
                {
                    "finding_code": "known-finding",
                    "scope_paths": ["docs/source.md"],
                    "owner": "docs-platform",
                    "reason": "Bounded remediation is scheduled.",
                    "approved_at": "2026-07-01",
                    "expires_on": "2026-08-01",
                    "exit_condition": "Remove after the source is migrated.",
                    "evidence": ["docs/04.execution/tasks/2026-07-14-fixture.md"],
                }
            ],
        }

    def test_schema_version_rejects_boolean(self) -> None:
        self.mutate_and_load(lambda values: values.__setitem__("schema_version", True))

    def test_profile_lists_reject_non_string_members(self) -> None:
        self.mutate_and_load(lambda values: values["profiles"]["spec"]["required"].append(7))

    def test_transitions_reject_unknown_statuses(self) -> None:
        self.mutate_and_load(lambda values: values["common"]["transitions"]["active"].append("retired"))

    def test_frontmatter_order_requires_exact_unique_typed_keys(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        self.assertEqual(
            [
                "status",
                "artifact_id",
                "artifact_type",
                "parent_ids",
                "supersedes",
                "reviewed_at",
                "review_cycle",
                "generated_by",
                "archived_from",
                "archived_on",
                "archive_reason",
                "archive_disposition",
                "archived_commit",
                "archived_blob",
                "preservation_class",
                "current_replacement",
                "snapshot_path",
                "content_sha256",
                "snapshot_reason",
            ],
            profiles["common"]["frontmatter_order"],
        )
        mutations = (
            lambda values: values["common"]["frontmatter_order"].pop(),
            lambda values: values["common"]["frontmatter_order"].append("status"),
            lambda values: values["common"]["frontmatter_order"].__setitem__(0, 7),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.mutate_and_load(mutate)

    def test_archive_profile_has_canonical_v2_order(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        self.assertEqual(2, profiles["schema_version"])
        self.assertEqual(
            [
                "status",
                "artifact_id",
                "artifact_type",
                "parent_ids",
                "supersedes",
                "reviewed_at",
                "review_cycle",
                "generated_by",
                "archived_from",
                "archived_on",
                "archive_reason",
                "archive_disposition",
                "archived_commit",
                "archived_blob",
                "preservation_class",
                "current_replacement",
                "snapshot_path",
                "content_sha256",
                "snapshot_reason",
            ],
            profiles["common"]["frontmatter_order"],
        )
        archive = profiles["profiles"]["archive"]
        self.assertEqual(
            [
                "status",
                "artifact_id",
                "artifact_type",
                "parent_ids",
                "archived_from",
                "archived_on",
                "archive_reason",
                "archive_disposition",
                "archived_commit",
                "archived_blob",
                "preservation_class",
            ],
            archive["required"],
        )
        self.assertEqual(
            [
                "layer",
                "supersedes",
                "current_replacement",
                "snapshot_path",
                "content_sha256",
                "snapshot_reason",
            ],
            archive["optional"],
        )
        self.assertEqual(
            {
                "replacement": {
                    "field": "current_replacement",
                    "required_for": ["superseded", "duplicate", "conflict"],
                    "forbidden_for": ["withdrawn"],
                    "optional_for": ["evidence-preserve"],
                },
                "snapshot": {
                    "fields": ["snapshot_path", "content_sha256", "snapshot_reason"],
                    "required_for": ["immutable-snapshot"],
                    "forbidden_for": ["git-history"],
                },
            },
            archive["conditions"],
        )

    def test_archive_profile_rejects_unknown_condition_fields(self) -> None:
        def add_unknown_condition(values) -> None:
            values["profiles"]["archive"].setdefault("conditions", {})[
                "undeclared-condition"
            ] = []

        self.mutate_and_load(add_unknown_condition)

    def test_migration_contract_has_exact_nonoverlapping_ownership(self) -> None:
        self.assertTrue(MIGRATION_CONTRACT.is_file(), "migration contract is missing")
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        profiles = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(
            [
                "migrate",
                "preserve",
                "move",
                "merge",
                "archive",
                "delete",
                "regenerate",
                "exempt",
            ],
            contract["manifest"]["dispositions"],
        )
        self.assertEqual(
            ["superseded", "duplicate", "conflict", "withdrawn", "evidence-preserve"],
            contract["archive"]["dispositions"],
        )
        self.assertEqual(
            ["git-history", "immutable-snapshot"],
            contract["archive"]["preservation_classes"],
        )
        self.assertEqual(
            {"warning_at": 100, "block_new_leaf_at": 150},
            contract["directory_budgets"],
        )
        self.assertEqual(
            {"draft_days": 30, "active_days": 90, "completed_execution_days": 180},
            contract["review_signals"],
        )
        self.assertEqual(
            {
                "schema_version",
                "manifest",
                "archive",
                "directory_budgets",
                "review_signals",
                "manifest_schema",
                "exception_schema",
                "disposition_conditions",
                "replacement_requirements",
                "snapshot_admission",
                "safe_diagnostics",
                "waves",
                "planned_partitions",
            },
            set(contract),
        )
        self.assertEqual(
            {"schema_version"},
            set(contract) & set(profiles),
        )

        mutations = []
        duplicate = MIGRATION_CONTRACT.read_text(encoding="utf-8") + "\nschema_version: 1\n"
        mutations.append(duplicate)
        for mutate in (
            lambda values: values["manifest"]["dispositions"].append("unknown"),
            lambda values: values["directory_budgets"].__setitem__("warning_at", 0),
            lambda values: values["directory_budgets"].__setitem__("warning_at", 150),
            lambda values: values["waves"]["wave-d-archive-provenance"].__setitem__(
                "enforcement", "blocking"
            ),
            lambda values: values.__setitem__("profiles", {}),
            lambda values: values["waves"]["foundation"]["source_paths"].append(
                "/absolute.md"
            ),
            lambda values: values["waves"]["foundation"]["declared_outputs"].append(
                "docs/../unsafe.md"
            ),
        ):
            values = yaml.safe_load(MIGRATION_CONTRACT.read_text(encoding="utf-8"))
            mutate(values)
            mutations.append(yaml.safe_dump(values, sort_keys=False))
        for source in mutations:
            with self.subTest(source=source[-80:]):
                with tempfile.TemporaryDirectory() as directory:
                    target = pathlib.Path(directory) / "migration.yaml"
                    target.write_text(source, encoding="utf-8")
                    with self.assertRaises(metadata.ProfileError):
                        metadata.load_migration_contract(target)

    def test_migration_contract_declares_manifest_static_semantics(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        schema = contract["manifest_schema"]
        self.assertEqual(
            {
                "schema_version",
                "wave",
                "baseline_commit",
                "generated_by",
                "enforcement",
                "entries",
                "source_path",
                "target_path",
                "artifact_id",
                "artifact_type",
                "status_before",
                "status_after",
                "parent_ids",
                "disposition",
                "canonical_replacement",
                "active_consumers",
                "partition_plan",
                "preservation_class",
                "evidence",
                "review_verdict",
                "evidence.commands",
                "evidence.sources",
                "evidence.repository_paths",
                "evidence.consumer_scan",
                "evidence.rollback",
                "review_verdict.specification",
                "review_verdict.quality",
            },
            set(schema["field_contracts"]),
        )
        self.assertEqual(
            {
                "entries": "source_path",
                "parent_ids": "lexicographic",
                "active_consumers": "lexicographic",
                "evidence.commands": "lexicographic",
                "evidence.sources": "lexicographic",
                "evidence.repository_paths": "lexicographic",
                "evidence.consumer_scan": "lexicographic",
                "evidence.rollback": "lexicographic",
            },
            schema["deterministic_order"],
        )
        self.assertEqual(
            {
                "dispositions": ["merge", "archive", "delete"],
                "active_consumers_required": True,
                "empty_consumers_require": "evidence.consumer_scan",
                "non_empty_evidence": [
                    "commands",
                    "sources",
                    "repository_paths",
                    "consumer_scan",
                    "rollback",
                ],
                "preservation_class_required": True,
                "replacement_semantics": "replacement_requirements",
                "required_review": {"specification": "pass", "quality": "pass"},
            },
            schema["destructive_execution"],
        )

        self.assertEqual(
            {
                "artifact_id": {
                    "type": "string",
                    "nullable": True,
                    "domain": "canonical-metadata-artifact-id",
                    "null_condition": "selected-profile-does-not-require-artifact-id",
                },
                "status_before": {
                    "type": "string",
                    "nullable": True,
                    "domain": "registered-lifecycle-status",
                    "null_condition": "selected-profile-does-not-require-status",
                },
                "status_after": {
                    "type": "string",
                    "nullable": True,
                    "domain": "registered-lifecycle-status",
                    "null_condition": "selected-profile-does-not-require-status",
                },
            },
            {
                field: schema["field_contracts"][field]
                for field in ("artifact_id", "status_before", "status_after")
            },
        )
        for mutate in (
            lambda values: values["manifest_schema"]["field_contracts"][
                "baseline_commit"
            ].__setitem__("domain", "string"),
            lambda values: values["manifest_schema"]["field_contracts"][
                "target_path"
            ].__setitem__("nullable", False),
            lambda values: values["manifest_schema"]["deterministic_order"].pop(
                "active_consumers"
            ),
            lambda values: values["manifest_schema"]["destructive_execution"][
                "non_empty_evidence"
            ].remove("consumer_scan"),
            lambda values: values["manifest_schema"]["destructive_execution"][
                "required_review"
            ].__setitem__("quality", "pending"),
        ):
            with self.subTest(mutate=mutate):
                self.mutate_migration_contract_and_load(mutate)

    def test_archive_replacement_is_deferred_to_validated_target_disposition(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        self.assertEqual(
            {
                "required_for": ["merge"],
                "optional_for": ["archive", "delete"],
                "forbidden_for": [
                    "migrate",
                    "preserve",
                    "move",
                    "regenerate",
                    "exempt",
                ],
            },
            contract["replacement_requirements"],
        )
        manifest = self.valid_static_manifest()
        entry = manifest["entries"][0]
        entry.update(
            {
                "target_path": "docs/98.archive/source.md",
                "disposition": "archive",
                "canonical_replacement": None,
            }
        )
        metadata.validate_static_migration_manifest(
            manifest,
            contract,
            metadata.load_profiles(PROFILES, MIGRATION_CONTRACT),
        )

    def test_static_manifest_allows_actual_profile_identity_exception(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        profiles = metadata.load_profiles(PROFILES)
        valid = self.valid_static_manifest()
        declared_exception = copy.deepcopy(valid)
        declared_exception["entries"][0].update(
            {
                "source_path": "README.md",
                "target_path": "README.md",
                "artifact_id": None,
                "artifact_type": "readme",
                "status_before": None,
                "status_after": None,
                "parent_ids": [],
                "disposition": "exempt",
                "preservation_class": None,
            }
        )
        metadata.validate_static_migration_manifest(declared_exception, contract, profiles)

    def test_static_manifest_exempt_cannot_override_required_identity(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        profiles = metadata.load_profiles(PROFILES)
        for field in ("artifact_id", "status_before", "status_after"):
            with self.subTest(field=field):
                typed_exempt = self.valid_static_manifest()
                typed_exempt["entries"][0].update(
                    {
                        "target_path": "docs/source.md",
                        "disposition": "exempt",
                        "preservation_class": None,
                        field: None,
                    }
                )
                with self.assertRaises(metadata.ProfileError):
                    metadata.validate_static_migration_manifest(
                        typed_exempt,
                        contract,
                        profiles,
                    )

    def test_static_manifest_uses_canonical_artifact_id_validation(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        profiles = metadata.load_profiles(PROFILES)
        canonical_id = "reference:Source"
        record = metadata.Record(
            pathlib.Path("docs/source.md"),
            {
                "status": "active",
                "artifact_id": canonical_id,
                "artifact_type": "reference",
                "parent_ids": [],
            },
            "reference",
            frontmatter_present=True,
        )
        self.assertNotIn(
            "invalid-artifact-id",
            {finding.code for finding in metadata.validate_record(record, profiles, {})},
        )
        manifest = self.valid_static_manifest()
        manifest["entries"][0]["artifact_id"] = canonical_id
        metadata.validate_static_migration_manifest(manifest, contract, profiles)

    def test_static_manifest_validation_fails_closed(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        profiles = metadata.load_profiles(PROFILES)
        valid = self.valid_static_manifest()
        metadata.validate_static_migration_manifest(valid, contract, profiles)

        mutations = {
            "schema-type": lambda value: value.__setitem__("schema_version", True),
            "empty-wave": lambda value: value.__setitem__("wave", ""),
            "object-domain": lambda value: value.__setitem__("baseline_commit", "A" * 40),
            "enforcement-domain": lambda value: value.__setitem__("enforcement", "enforced"),
            "unsafe-source-path": lambda value: value["entries"][0].__setitem__(
                "source_path", "../source.md"
            ),
            "unsafe-target-path": lambda value: value["entries"][0].__setitem__(
                "target_path", "/tmp/source.md"
            ),
            "artifact-null-for-required-profile": lambda value: value["entries"][0].__setitem__(
                "artifact_id", None
            ),
            "artifact-type-domain": lambda value: value["entries"][0].__setitem__(
                "artifact_type", "unknown"
            ),
            "artifact-type-shape": lambda value: value["entries"][0].__setitem__(
                "artifact_type", []
            ),
            "disposition-shape": lambda value: value["entries"][0].__setitem__(
                "disposition", []
            ),
            "status-domain": lambda value: value["entries"][0].__setitem__(
                "status_after", "retired"
            ),
            "status-shape": lambda value: value["entries"][0].__setitem__(
                "status_after", []
            ),
            "status-null-for-required-profile": lambda value: value["entries"][0].__setitem__(
                "status_before", None
            ),
            "partition-plan-path": lambda value: value["entries"][0].__setitem__(
                "partition_plan", "docs/04.execution/tasks/not-a-plan.md"
            ),
            "unordered-parent-list": lambda value: value["entries"][0].__setitem__(
                "parent_ids", ["spec:z", "spec:a"]
            ),
            "unordered-consumer-list": lambda value: value["entries"][0].__setitem__(
                "active_consumers", ["docs/z.md", "docs/a.md"]
            ),
            "unordered-evidence-list": lambda value: value["entries"][0]["evidence"].__setitem__(
                "commands", ["z command", "a command"]
            ),
            "unordered-entries": lambda value: value["entries"].insert(
                0,
                {
                    **copy.deepcopy(value["entries"][0]),
                    "source_path": "docs/z-source.md",
                },
            ),
            "delete-target": lambda value: value["entries"][0].__setitem__(
                "target_path", "docs/source.md"
            ),
            "consumer-enumeration": lambda value: value["entries"][0].__setitem__(
                "active_consumers", None
            ),
            "consumer-scan-proof": lambda value: value["entries"][0]["evidence"].__setitem__(
                "consumer_scan", []
            ),
            "destructive-evidence": lambda value: value["entries"][0]["evidence"].__setitem__(
                "commands", []
            ),
            "destructive-preservation": lambda value: value["entries"][0].__setitem__(
                "preservation_class", None
            ),
            "preservation-shape": lambda value: value["entries"][0].__setitem__(
                "preservation_class", []
            ),
            "destructive-review": lambda value: value["entries"][0]["review_verdict"].__setitem__(
                "quality", "pending"
            ),
            "review-shape": lambda value: value["entries"][0]["review_verdict"].__setitem__(
                "quality", []
            ),
            "merge-replacement": lambda value: (
                value["entries"][0].__setitem__("disposition", "merge"),
                value["entries"][0].__setitem__("target_path", "docs/merged/source.md"),
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(valid)
                mutate(candidate)
                with self.assertRaises(metadata.ProfileError):
                    metadata.validate_static_migration_manifest(candidate, contract, profiles)

    def test_bounded_exception_contract_rejects_unbounded_entries(self) -> None:
        contract = metadata.load_migration_contract(MIGRATION_CONTRACT)
        schema = contract["exception_schema"]
        self.assertEqual(
            {
                "finding_code_source": "validator-known-finding-codes",
                "require_non_empty_scope_paths": True,
                "forbid_wildcards": True,
                "forbid_global_scopes": ["*", "**", ".", "all", "global"],
                "require_non_empty_text": ["owner", "reason", "exit_condition"],
                "approval": "approved_at-not-future",
                "expiry": "expires_on-after-validation-date",
                "require_non_empty_safe_evidence_paths": True,
            },
            schema["bounded_semantics"],
        )
        for mutate in (
            lambda values: values["exception_schema"]["field_contracts"][
                "finding_code"
            ].__setitem__("domain", "string"),
            lambda values: values["exception_schema"]["bounded_semantics"].__setitem__(
                "forbid_wildcards", False
            ),
            lambda values: values["exception_schema"]["bounded_semantics"][
                "require_non_empty_text"
            ].remove("owner"),
            lambda values: values["exception_schema"]["bounded_semantics"].__setitem__(
                "expiry", "permanent"
            ),
        ):
            with self.subTest(contract_mutation=mutate):
                self.mutate_migration_contract_and_load(mutate)
        valid = self.valid_static_exception_document()
        validation_date = dt.date(2026, 7, 14)
        metadata.validate_static_exception_document(
            valid,
            contract,
            {"known-finding"},
            validation_date,
        )

        mutations = {
            "wildcard": lambda value: value["exceptions"][0].__setitem__(
                "scope_paths", ["docs/*"]
            ),
            "global": lambda value: value["exceptions"][0].__setitem__(
                "scope_paths", ["global"]
            ),
            "ownerless": lambda value: value["exceptions"][0].__setitem__("owner", ""),
            "reasonless": lambda value: value["exceptions"][0].__setitem__("reason", ""),
            "permanent": lambda value: value["exceptions"][0].__setitem__(
                "expires_on", "permanent"
            ),
            "expired": lambda value: value["exceptions"][0].__setitem__(
                "expires_on", "2026-07-13"
            ),
            "unknown-code": lambda value: value["exceptions"][0].__setitem__(
                "finding_code", "unknown-finding"
            ),
            "empty-exit": lambda value: value["exceptions"][0].__setitem__(
                "exit_condition", ""
            ),
            "unsafe-evidence": lambda value: value["exceptions"][0].__setitem__(
                "evidence", ["/tmp/evidence.md"]
            ),
            "unapproved": lambda value: value["exceptions"][0].__setitem__(
                "approved_at", "2026-07-15"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(valid)
                mutate(candidate)
                with self.assertRaises(metadata.ProfileError):
                    metadata.validate_static_exception_document(
                        candidate,
                        contract,
                        {"known-finding"},
                        validation_date,
                    )

    def test_document_families_require_known_unique_profiles(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        self.assertEqual(
            {
                "sdlc": [
                    "prd",
                    "ard",
                    "adr",
                    "spec",
                    "plan",
                    "task",
                    "guide",
                    "policy",
                    "runbook",
                    "incident",
                    "postmortem",
                    "release",
                ],
                "common": [
                    "reference",
                    "audit",
                    "archive",
                    "readme",
                    "governance",
                    "generated",
                    "template-source",
                    "repo-support",
                    "unsupported",
                ],
            },
            profiles["document_families"],
        )
        mutations = (
            lambda values: values["document_families"]["sdlc"].append("unknown"),
            lambda values: values["document_families"]["common"].append("readme"),
            lambda values: values["document_families"].__setitem__("other", ["spec"]),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.mutate_and_load(mutate)

    def test_readme_profiles_reject_overlap_and_unknown_members(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        self.assertTrue(profiles["readme_profiles"])

        def overlap(values) -> None:
            names = list(values["readme_profiles"])
            first, second = names[:2]
            values["readme_profiles"][second]["path_globs"].append(
                values["readme_profiles"][first]["path_globs"][0]
            )

        def unknown_member(values) -> None:
            first = next(iter(values["readme_profiles"].values()))
            first["unknown_member"] = "not-declared"

        for mutate in (overlap, unknown_member):
            with self.subTest(mutate=mutate):
                self.mutate_and_load(mutate)

    def test_template_roles_require_exact_fields_and_unique_sources(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        roles = profiles["template_roles"]
        self.assertEqual(23, len(roles))
        sources = [role["source"] for role in roles.values()]
        self.assertEqual(len(sources), len(set(sources)))

    def test_template_roles_reject_unknown_profiles_and_heading_overlap(self) -> None:
        self.mutate_and_load(
            lambda values: values["template_roles"]["prd"].__setitem__(
                "artifact_profile", "missing-profile"
            )
        )

    def test_template_roles_reject_ambiguous_target_matchers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "profiles.yaml"
            values = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
            values["template_roles"]["spec"]["target_globs"] = [
                "docs/03.specs/*/s*ec.md"
            ]
            values["template_roles"]["api-spec"]["target_globs"] = [
                "docs/03.specs/*/sp*c.md"
            ]
            target.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(
                metadata.ProfileError,
                r"api-spec:.*sp\*c\.md and spec:.*s\*ec\.md; "
                r"witness=docs/03\.specs/x/spec\.md",
            ):
                metadata.load_profiles(target)


class ArtifactInferenceTests(unittest.TestCase):
    def test_supported_paths_infer_explicit_profiles(self) -> None:
        cases = {
            "docs/01.requirements/123-example.md": "prd",
            "docs/02.architecture/requirements/0123-example.md": "ard",
            "docs/02.architecture/decisions/0123-example.md": "adr",
            "docs/03.specs/123-example/spec.md": "spec",
            "docs/04.execution/plans/2026-07-11-example.md": "plan",
            "docs/04.execution/tasks/2026-07-11-example.md": "task",
            "docs/05.operations/guides/00-workspace/example.md": "guide",
            "docs/05.operations/policies/00-workspace/example.md": "policy",
            "docs/05.operations/runbooks/00-workspace/example.md": "runbook",
            "docs/05.operations/incidents/2026/INC-001-example/INC-001-example.md": "incident",
            "docs/05.operations/incidents/2026/INC-001-example/postmortem.md": "postmortem",
            "docs/05.operations/releases/2026-07-11.md": "release",
            "docs/90.references/research/example.md": "reference",
            "docs/90.references/audits/example.md": "audit",
            "docs/98.archive/04.execution/example.md": "archive",
            "docs/99.templates/templates/sdlc/spec.template.md": "template-source",
            "docs/00.agent-governance/rules/example.md": "governance",
            "README.md": "readme",
            "misc/example.md": "unsupported",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(expected, metadata.infer_artifact_type(pathlib.Path(path)))


class TemplateRoleInferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_registered_targets_have_one_exact_role(self) -> None:
        cases = {
            "docs/01.requirements/901-fixture.md": ("prd", "prd"),
            "docs/02.architecture/requirements/0901-fixture.md": ("ard", "ard"),
            "docs/02.architecture/decisions/0901-fixture.md": ("adr", "adr"),
            "docs/03.specs/901-fixture/spec.md": ("spec", "spec"),
            "docs/03.specs/901-fixture/api-spec.md": ("spec", "api-spec"),
            "docs/03.specs/901-fixture/agent-design.md": ("spec", "agent-design"),
            "docs/03.specs/901-fixture/data-model.md": ("spec", "data-model"),
            "docs/03.specs/901-fixture/service.md": ("spec", "service"),
            "docs/03.specs/901-fixture/tests.md": ("spec", "tests"),
            "docs/04.execution/plans/2026-07-13-fixture.md": ("plan", "plan"),
            "docs/04.execution/tasks/2026-07-13-fixture.md": ("task", "task"),
            "docs/05.operations/guides/00-workspace/fixture.md": ("guide", "guide"),
            "docs/05.operations/policies/00-workspace/fixture.md": ("policy", "policy"),
            "docs/05.operations/runbooks/00-workspace/fixture.md": ("runbook", "runbook"),
            "docs/05.operations/incidents/2026/INC-901-fixture/INC-901-fixture.md": ("incident", "incident"),
            "docs/05.operations/incidents/2026/INC-901-fixture/postmortem.md": ("postmortem", "postmortem"),
            "docs/05.operations/releases/2026-07-13-fixture.md": ("release", "release"),
            "docs/90.references/research/fixture.md": ("reference", "reference"),
            "docs/90.references/audits/fixture.md": ("audit", "audit"),
            "docs/98.archive/03.specs/fixture.md": ("archive", "archive"),
            "README.md": ("readme", "readme"),
            "docs/00.agent-governance/memory/fixture.md": ("governance", "memory"),
            "docs/00.agent-governance/memory/progress.md": ("governance", "progress"),
        }
        for path_text, (profile, expected_role) in cases.items():
            with self.subTest(path=path_text):
                self.assertEqual(
                    expected_role,
                    metadata.classify_template_role(
                        pathlib.Path(path_text), profile, self.profiles
                    ),
                )


class MetadataValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def record(
        self,
        path: str,
        values: dict[str, object],
        artifact_type: str,
        previous_status: str | None = None,
    ):
        return metadata.Record(
            pathlib.Path(path),
            values,
            artifact_type,
            previous_status=previous_status,
        )

    def codes(self, record, records=()) -> list[str]:
        all_records = [*records, record]
        manifest = metadata.build_manifest(all_records)
        return [finding.code for finding in metadata.validate_record(record, self.profiles, manifest)]

    def archive_record(
        self,
        overrides: dict[str, object] | None = None,
        *,
        remove: tuple[str, ...] = (),
    ):
        values: dict[str, object] = {
            "status": "archived",
            "artifact_id": "archive:04-execution-example",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": "docs/04.execution/example.md",
            "archived_on": "2026-07-14",
            "archive_reason": "Superseded by the canonical execution record.",
            "archive_disposition": "superseded",
            "archived_commit": "a" * 40,
            "archived_blob": "b" * 40,
            "preservation_class": "git-history",
            "current_replacement": "docs/04.execution/canonical.md",
        }
        values.update(overrides or {})
        for key in remove:
            values.pop(key, None)
        return self.record(
            "docs/98.archive/04.execution/example.md",
            values,
            "archive",
        )

    def test_valid_spec_metadata_passes(self) -> None:
        parent = self.record(
            "docs/01.requirements/123-parent.md",
            {"status": "active", "artifact_id": "PRD-123", "artifact_type": "prd", "parent_ids": []},
            "prd",
        )
        spec_record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-123"],
            },
            "spec",
        )
        self.assertEqual([], self.codes(spec_record, [parent]))

    def test_approved_crosscutting_spec_root_is_explicitly_permitted(self) -> None:
        record = self.record(
            "docs/03.specs/123-agentic-engineering-audit-remediation/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-agentic-engineering-audit-remediation",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertNotIn("missing-parent", self.codes(record))

    def test_readme_without_frontmatter_is_an_explicit_exception(self) -> None:
        record = self.record("docs/03.specs/README.md", {}, "readme")
        self.assertEqual([], self.codes(record))

    def test_readme_rejects_copied_template_draft_status(self) -> None:
        record = self.record("docs/03.specs/README.md", {"status": "draft"}, "readme")
        self.assertIn("invalid-status", self.codes(record))

    def test_frontmatter_presentation_order_is_enforced(self) -> None:
        record = self.record(
            "docs/01.requirements/123-example.md",
            {
                "artifact_id": "PRD-123",
                "status": "active",
                "artifact_type": "prd",
                "parent_ids": [],
            },
            "prd",
        )
        self.assertIn("frontmatter-order", self.codes(record))

    def test_parent_serialization_uses_type_precedence_then_id(self) -> None:
        spec_parent = self.record(
            "docs/03.specs/100-parent/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-Z",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        plan_a = self.record(
            "docs/04.execution/plans/2026-07-11-a.md",
            {
                "status": "active",
                "artifact_id": "PLAN-A",
                "artifact_type": "plan",
                "parent_ids": [],
            },
            "plan",
        )
        plan_b = self.record(
            "docs/04.execution/plans/2026-07-11-b.md",
            {
                "status": "active",
                "artifact_id": "PLAN-B",
                "artifact_type": "plan",
                "parent_ids": [],
            },
            "plan",
        )
        record = self.record(
            "docs/04.execution/tasks/2026-07-11-child.md",
            {
                "status": "active",
                "artifact_id": "TASK-CHILD",
                "artifact_type": "task",
                "parent_ids": ["PLAN-B", "PLAN-A", "SPEC-Z"],
            },
            "task",
        )
        self.assertIn("parent-order", self.codes(record, [plan_b, spec_parent, plan_a]))

        canonical = self.record(
            record.path.as_posix(),
            {**record.metadata, "parent_ids": ["SPEC-Z", "PLAN-A", "PLAN-B"]},
            "task",
        )
        self.assertNotIn("parent-order", self.codes(canonical, [plan_b, spec_parent, plan_a]))

    def test_parent_order_has_no_semantic_priority(self) -> None:
        parent_a = self.record(
            "docs/03.specs/100-a/spec.md",
            {"status": "active", "artifact_id": "SPEC-A", "artifact_type": "spec", "parent_ids": []},
            "spec",
        )
        parent_b = self.record(
            "docs/03.specs/100-b/spec.md",
            {"status": "active", "artifact_id": "SPEC-B", "artifact_type": "spec", "parent_ids": []},
            "spec",
        )
        ordered = self.record(
            "docs/04.execution/plans/2026-07-11-child.md",
            {
                "status": "active",
                "artifact_id": "PLAN-CHILD",
                "artifact_type": "plan",
                "parent_ids": ["SPEC-A", "SPEC-B"],
            },
            "plan",
        )
        reversed_record = self.record(
            ordered.path.as_posix(),
            {**ordered.metadata, "parent_ids": ["SPEC-B", "SPEC-A"]},
            "plan",
        )
        ordered_codes = set(self.codes(ordered, [parent_a, parent_b]))
        reversed_findings = metadata.validate_record(
            reversed_record,
            self.profiles,
            metadata.build_manifest([parent_a, parent_b, reversed_record]),
        )
        self.assertEqual(ordered_codes, {finding.code for finding in reversed_findings} - {"parent-order"})
        order_finding = next(finding for finding in reversed_findings if finding.code == "parent-order")
        self.assertNotIn("priority", order_finding.message.lower())
        self.assertIn("serialization", order_finding.message.lower())

    def test_unresolved_parent_is_reported(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-MISSING"],
            },
            "spec",
        )
        self.assertIn("unresolved-parent", self.codes(record))

    def test_wrong_parent_type_and_parent_cycle_are_reported(self) -> None:
        parent = self.record(
            "docs/04.execution/tasks/2026-07-11-parent.md",
            {
                "status": "active",
                "artifact_id": "TASK-PARENT",
                "artifact_type": "task",
                "parent_ids": ["SPEC-CHILD"],
            },
            "task",
        )
        child = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-CHILD",
                "artifact_type": "spec",
                "parent_ids": ["TASK-PARENT"],
            },
            "spec",
        )
        codes = self.codes(child, [parent])
        self.assertIn("invalid-parent-type", codes)
        self.assertIn("parent-cycle", codes)

    def test_declared_type_must_match_inferred_profile(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "plan",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertIn("artifact-type-mismatch", self.codes(record))

    def test_forbidden_and_type_inappropriate_keys_are_reported(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
                "type": "spec",
                "archived_from": "docs/03.specs/old/spec.md",
            },
            "spec",
        )
        codes = self.codes(record)
        self.assertIn("forbidden-key", codes)
        self.assertIn("type-inappropriate-key", codes)

    def test_valid_forward_lifecycle_transition_passes(self) -> None:
        record = self.record(
            "docs/04.execution/tasks/2026-07-11-example.md",
            {
                "status": "completed",
                "artifact_id": "TASK-2026-07-11-EXAMPLE",
                "artifact_type": "task",
                "parent_ids": [],
            },
            "task",
            previous_status="active",
        )
        self.assertNotIn("invalid-transition", self.codes(record))

    def test_reverse_lifecycle_transition_is_reported(self) -> None:
        record = self.record(
            "docs/04.execution/tasks/2026-07-11-example.md",
            {
                "status": "active",
                "artifact_id": "TASK-2026-07-11-EXAMPLE",
                "artifact_type": "task",
                "parent_ids": [],
            },
            "task",
            previous_status="completed",
        )
        self.assertIn("invalid-transition", self.codes(record))

    def test_superseded_artifact_requires_resolvable_replacement(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "superseded",
                "artifact_id": "SPEC-OLD",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertIn("replacement-free-supersession", self.codes(record))

    def test_replacement_requires_superseded_target_state(self) -> None:
        old = self.record(
            "docs/03.specs/122-old/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-OLD",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        new = self.record(
            "docs/03.specs/123-new/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-NEW",
                "artifact_type": "spec",
                "parent_ids": [],
                "supersedes": ["SPEC-OLD"],
            },
            "spec",
        )
        self.assertIn("invalid-supersession-state", self.codes(new, [old]))

    def test_generated_document_uses_generator_profile(self) -> None:
        record = self.record(
            "docs/90.references/data/example.md",
            {"status": "active", "generated_by": "scripts/example.py"},
            "generated",
        )
        self.assertEqual([], self.codes(record))

    def test_generated_document_rejects_human_typed_identity(self) -> None:
        record = self.record(
            "docs/90.references/data/example.md",
            {
                "status": "active",
                "generated_by": "scripts/example.py",
                "artifact_id": "REF-GENERATED",
            },
            "generated",
        )
        self.assertIn("type-inappropriate-key", self.codes(record))

    def test_freshness_requires_strict_iso_date_or_datetime(self) -> None:
        record = self.record(
            "docs/05.operations/policies/00-workspace/example.md",
            {
                "status": "active",
                "artifact_id": "POLICY-EXAMPLE",
                "artifact_type": "policy",
                "parent_ids": [],
                "reviewed_at": "yesterday",
                "review_cycle": "annual",
            },
            "policy",
        )
        self.assertIn("invalid-reviewed-at", self.codes(record))

    def test_generator_owner_rejects_absolute_and_traversal_paths(self) -> None:
        for generated_by in ("/tmp/generator.py", "scripts/../generator.py", "scripts\\generator.py"):
            with self.subTest(generated_by=generated_by):
                record = self.record(
                    "docs/90.references/data/example.md",
                    {"status": "active", "generated_by": generated_by},
                    "generated",
                )
                self.assertIn("invalid-generator", self.codes(record))

    def test_archive_provenance_types_are_validated(self) -> None:
        record = self.record(
            "docs/98.archive/04.execution/example.md",
            {
                "status": "archived",
                "archived_from": ["docs/04.execution/example.md"],
                "archived_on": "not-a-date",
                "archive_reason": 7,
                "current_replacement": "/absolute.md",
            },
            "archive",
        )
        codes = self.codes(record)
        self.assertIn("invalid-archived-from", codes)
        self.assertIn("invalid-archived-on", codes)
        self.assertIn("invalid-archive-reason", codes)
        self.assertIn("invalid-current-replacement", codes)

    def test_archive_replacement_is_conditional(self) -> None:
        cases = (
            ("superseded", False, "archive-replacement-required"),
            ("duplicate", False, "archive-replacement-required"),
            ("conflict", False, "archive-replacement-required"),
            ("withdrawn", True, "archive-replacement-forbidden"),
        )
        for disposition, include_replacement, expected_code in cases:
            with self.subTest(disposition=disposition):
                remove = () if include_replacement else ("current_replacement",)
                record = self.archive_record(
                    {"archive_disposition": disposition},
                    remove=remove,
                )
                self.assertIn(expected_code, self.codes(record))

        for include_replacement in (False, True):
            with self.subTest(disposition="evidence-preserve", replacement=include_replacement):
                record = self.archive_record(
                    {"archive_disposition": "evidence-preserve"},
                    remove=() if include_replacement else ("current_replacement",),
                )
                codes = self.codes(record)
                self.assertNotIn("archive-replacement-required", codes)
                self.assertNotIn("archive-replacement-forbidden", codes)

    def test_git_history_forbids_snapshot_fields(self) -> None:
        record = self.archive_record(
            {
                "snapshot_path": (
                    "docs/98.archive/evidence/" + ("c" * 64) + ".md.snapshot"
                ),
                "content_sha256": "c" * 64,
                "snapshot_reason": "Audit evidence.",
            }
        )
        codes = self.codes(record)
        self.assertIn("archive-snapshot-forbidden", codes)

    def test_immutable_snapshot_requires_all_snapshot_fields(self) -> None:
        snapshot_path = "docs/98.archive/evidence/" + ("c" * 64) + ".md.snapshot"
        complete_snapshot = {
            "archive_disposition": "evidence-preserve",
            "preservation_class": "immutable-snapshot",
            "snapshot_path": snapshot_path,
            "content_sha256": "c" * 64,
            "snapshot_reason": "Audit evidence.",
        }
        cases = (
            (
                complete_snapshot,
                ("snapshot_path",),
                "archive-snapshot-path-required",
            ),
            (
                complete_snapshot,
                ("content_sha256",),
                "archive-content-sha256-required",
            ),
            (
                complete_snapshot,
                ("snapshot_reason",),
                "archive-snapshot-reason-required",
            ),
            (
                {"archive_disposition": "withdrawn"},
                (),
                "archive-replacement-forbidden",
            ),
            (
                {"archive_disposition": "superseded"},
                ("current_replacement",),
                "archive-replacement-required",
            ),
            (
                {"archived_commit": "N/A"},
                (),
                "invalid-archived-commit",
            ),
            (
                {"archived_blob": "b" * 39},
                (),
                "invalid-archived-blob",
            ),
            (
                {**complete_snapshot, "content_sha256": "C" * 64},
                (),
                "invalid-content-sha256",
            ),
            (
                {
                    **complete_snapshot,
                    "snapshot_path": "docs/98.archive/evidence/../unsafe.md.snapshot",
                },
                (),
                "invalid-snapshot-path",
            ),
        )
        for overrides, remove, expected_code in cases:
            with self.subTest(code=expected_code):
                record = self.archive_record(overrides, remove=remove)
                self.assertIn(expected_code, self.codes(record))

    def test_immutable_snapshot_requires_admitted_archive_disposition(self) -> None:
        snapshot = {
            "preservation_class": "immutable-snapshot",
            "snapshot_path": "docs/98.archive/evidence/" + ("c" * 64) + ".md.snapshot",
            "content_sha256": "c" * 64,
            "snapshot_reason": "Audit evidence.",
        }
        for disposition in ("superseded", "duplicate", "conflict", "withdrawn"):
            with self.subTest(disposition=disposition):
                record = self.archive_record(
                    {**snapshot, "archive_disposition": disposition},
                    remove=("current_replacement",) if disposition == "withdrawn" else (),
                )
                self.assertIn(
                    "archive-snapshot-disposition-forbidden",
                    self.codes(record),
                )

        admitted = self.archive_record(
            {**snapshot, "archive_disposition": "evidence-preserve"}
        )
        self.assertNotIn(
            "archive-snapshot-disposition-forbidden",
            self.codes(admitted),
        )

    def test_archive_selector_shapes_fail_closed(self) -> None:
        cases = (
            ("archive_disposition", ["superseded"], "invalid-archive-disposition"),
            (
                "archive_disposition",
                {"value": "superseded"},
                "invalid-archive-disposition",
            ),
            ("preservation_class", ["git-history"], "invalid-preservation-class"),
            (
                "preservation_class",
                {"value": "git-history"},
                "invalid-preservation-class",
            ),
        )
        for field, malformed, expected_code in cases:
            with self.subTest(field=field, shape=type(malformed).__name__):
                self.assertIn(
                    expected_code,
                    self.codes(self.archive_record({field: malformed})),
                )

    def test_archive_rejects_sentinel_paths_hashes_and_object_ids(self) -> None:
        snapshot = {
            "archive_disposition": "evidence-preserve",
            "preservation_class": "immutable-snapshot",
            "snapshot_path": "docs/98.archive/evidence/" + ("c" * 64) + ".md.snapshot",
            "content_sha256": "c" * 64,
            "snapshot_reason": "Audit evidence.",
        }
        cases = (
            ({"archived_from": "N/A"}, "invalid-archived-from"),
            ({"current_replacement": "N/A"}, "invalid-current-replacement"),
            ({"archived_commit": ""}, "invalid-archived-commit"),
            ({"archived_commit": "A" * 40}, "invalid-archived-commit"),
            ({"archived_blob": "B" * 64}, "invalid-archived-blob"),
            ({**snapshot, "content_sha256": "N/A"}, "invalid-content-sha256"),
            ({**snapshot, "snapshot_path": "/absolute.md.snapshot"}, "invalid-snapshot-path"),
            ({"archive_disposition": "retired"}, "invalid-archive-disposition"),
            ({"preservation_class": "snapshot"}, "invalid-preservation-class"),
        )
        for overrides, expected_code in cases:
            with self.subTest(code=expected_code):
                self.assertIn(expected_code, self.codes(self.archive_record(overrides)))

    def test_existing_tombstones_remain_wave_d_advisory_debt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            write_doc(
                root / "docs/98.archive/04.execution/legacy.md",
                {
                    "status": "archived",
                    "archived_from": "docs/04.execution/legacy.md",
                    "archived_on": "2026-07-01",
                    "archive_reason": "Legacy archive debt assigned to Wave D.",
                    "current_replacement": "docs/04.execution/current.md",
                },
            )
            stage_index_body = body_with_headings(
                "## Overview",
                "## Audience",
                "## Scope",
                "## Structure",
                "## How to Work in This Area",
                "## Related Documents",
            )
            index = root / "docs/03.specs/README.md"
            write_doc(index, {"status": "active"}, stage_index_body)
            commit_all(root, "baseline")
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "Fixture content.", "Changed fixture content.", 1
                ),
                encoding="utf-8",
            )
            result = run_checker(root, "check-changed", "--base-ref", "HEAD")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("docs/98.archive/04.execution/legacy.md", result.stdout)

    def test_archive_template_transition_does_not_relax_target_requirements(self) -> None:
        record = self.record(
            "docs/98.archive/04.execution/new-target.md",
            {
                "status": "archived",
                "artifact_id": "archive:04-execution-new-target",
                "artifact_type": "archive",
                "parent_ids": [],
                "archived_from": "docs/04.execution/new-target.md",
                "archived_on": "2026-07-14",
                "archive_reason": "Fixture for the Task 3 template handoff.",
                "current_replacement": "docs/04.execution/current.md",
            },
            "archive",
        )
        findings = metadata.validate_record(
            record,
            self.profiles,
            metadata.build_manifest([record]),
        )
        self.assertEqual(
            {
                "required key is missing: archive_disposition",
                "required key is missing: archived_commit",
                "required key is missing: archived_blob",
                "required key is missing: preservation_class",
            },
            {
                finding.message
                for finding in findings
                if finding.code == "missing-required-key"
            },
        )

    def test_instantiated_document_rejects_template_placeholders(self) -> None:
        record = self.record(
            "docs/03.specs/124-example/spec.md",
            {
                "status": "draft",
                "artifact_id": "<artifact-id>",
                "artifact_type": "spec",
                "parent_ids": ["<parent-artifact-id>"],
            },
            "spec",
        )
        self.assertIn("template-placeholder-in-target", self.codes(record))

    def test_instantiated_document_rejects_composed_angle_bracket_placeholders(self) -> None:
        cases = (
            {
                "status": "draft",
                "artifact_id": "spec:<artifact-id>",
                "artifact_type": "spec",
                "parent_ids": ["prd:real-parent"],
            },
            {
                "status": "draft",
                "artifact_id": "spec:real-child",
                "artifact_type": "spec",
                "parent_ids": ["prefix:<parent-artifact-id>"],
            },
            {
                "status": "active",
                "artifact_id": "policy:real",
                "artifact_type": "policy",
                "parent_ids": ["spec:real-parent"],
                "reviewed_at": "reviewed-<reviewed-at>",
                "review_cycle": "annual",
            },
        )
        paths = (
            "docs/03.specs/124-example/spec.md",
            "docs/03.specs/124-example/spec.md",
            "docs/05.operations/policies/00-workspace/example.md",
        )
        types = ("spec", "spec", "policy")
        for values, path, artifact_type in zip(cases, paths, types, strict=True):
            with self.subTest(values=values):
                record = self.record(path, values, artifact_type)
                self.assertIn("template-placeholder-in-target", self.codes(record))

    def test_non_angle_date_marker_is_not_a_global_placeholder_token(self) -> None:
        record = self.record(
            "docs/01.requirements/124-example.md",
            {
                "status": "active",
                "artifact_id": "prd:release-YYYY-MM-DD",
                "artifact_type": "prd",
                "parent_ids": [],
            },
            "prd",
        )
        self.assertNotIn("template-placeholder-in-target", self.codes(record))

    def test_incident_profile_allows_root_but_event_children_stay_strict(self) -> None:
        incident = self.profiles["profiles"]["incident"]
        postmortem = self.profiles["profiles"]["postmortem"]
        release = self.profiles["profiles"]["release"]

        self.assertTrue(incident["allow_empty_parents"])
        self.assertEqual(["runbook"], incident["allowed_parent_types"])
        self.assertEqual(["incident"], postmortem["allowed_parent_types"])
        self.assertFalse(postmortem["allow_empty_parents"])
        self.assertEqual(["spec", "plan", "task"], release["allowed_parent_types"])
        self.assertFalse(release["allow_empty_parents"])


class ReadmeProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_every_tracked_readme_has_exactly_one_profile(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "*README.md"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        paths = [pathlib.Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]
        before = {path: (ROOT / path).read_bytes() for path in paths}

        for path in paths:
            with self.subTest(path=path):
                matches = metadata.matching_readme_profiles(path, self.profiles)
                self.assertEqual(1, len(matches), matches)
                self.assertEqual(matches[0], metadata.classify_readme_profile(path, self.profiles))

        self.assertEqual(before, {path: (ROOT / path).read_bytes() for path in paths})

    def test_status_bearing_readme_requires_declared_consumer(self) -> None:
        root_path = pathlib.Path("README.md")
        self.assertIsNone(metadata.readme_frontmatter_consumer(root_path, self.profiles))
        record = metadata.Record(root_path, {"status": "active"}, "readme", frontmatter_present=True)
        findings = metadata.validate_record(record, self.profiles, metadata.build_manifest([record]))
        self.assertIn("readme-frontmatter-forbidden", {finding.code for finding in findings})

        stage_path = pathlib.Path("docs/03.specs/README.md")
        self.assertEqual(
            "scripts/validation/check-document-metadata.py",
            metadata.readme_frontmatter_consumer(stage_path, self.profiles),
        )

    def test_current_audit_readme_count_matches_tracked_corpus(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "*README.md"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        tracked_count = len([raw for raw in result.stdout.split(b"\0") if raw])
        current_claim = f"all {tracked_count} tracked READMEs"
        claims = {
            "frontmatter-template-readme-implementation.md": 2,
            "sdlc-document-contracts-implementation.md": 1,
        }
        audit_pack = ROOT / "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack"
        for name, expected_occurrences in claims.items():
            with self.subTest(path=name):
                text = (audit_pack / name).read_text(encoding="utf-8")
                self.assertEqual(expected_occurrences, text.count(current_claim))


class TemplateMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_task_2_copyable_markdown_forms_have_one_h1_and_no_legacy_guidance(self) -> None:
        for role_name in ("readme", "reference", "audit", "archive", "memory", "progress"):
            with self.subTest(role=role_name):
                source = ROOT / self.profiles["template_roles"][role_name]["source"]
                text = source.read_text(encoding="utf-8")
                self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))
                self.assertNotIn("> Rules:", text)
                self.assertNotIn("<!-- Target:", text)

    def test_task_2_forms_match_their_registered_required_heading_envelopes(self) -> None:
        for role_name in ("readme", "reference", "audit", "archive", "memory", "progress"):
            with self.subTest(role=role_name):
                role = self.profiles["template_roles"][role_name]
                text = (ROOT / role["source"]).read_text(encoding="utf-8")
                headings = [line for line in text.splitlines() if line.startswith("## ")]
                self.assertEqual(role["required_headings"], headings)

    def test_task_2_governance_forms_have_exact_source_frontmatter(self) -> None:
        expected = {"layer": "agentic", "status": "draft"}
        for role_name in ("memory", "progress"):
            with self.subTest(role=role_name):
                source = ROOT / self.profiles["template_roles"][role_name]["source"]
                self.assertEqual(expected, metadata.parse_frontmatter(source))

    def test_task_2_memory_form_instantiates_the_memory_note_target_contract(self) -> None:
        source = ROOT / self.profiles["template_roles"]["memory"]["source"]
        rendered = source.read_text(encoding="utf-8")
        substitutions = {
            "title": "Fixture Memory Note",
            "date": "2026-07-13",
            "layer": "agentic",
            "status": "active",
            "applies_to": "template contract system",
            "tags": "templates, governance",
            "retrieval_keywords": "memory template contract",
            "last_verified": "2026-07-13",
            "problem": "Fixture problem.",
            "context": "Fixture context.",
            "resolution": "Fixture resolution.",
            "prevention": "Fixture prevention.",
            "evidence": "Fixture evidence.",
            "related_documents": "- Fixture link",
        }
        for token, value in substitutions.items():
            rendered = rendered.replace(f"{{{{{token}}}}}", value)

        self.assertNotIn("{{", rendered)
        memory_note_required = (
            "- Date:",
            "- Layer:",
            "- Status:",
            "- Applies To:",
            "- Tags:",
            "- Retrieval Keywords:",
            "- Last Verified:",
            "## Problem",
            "## Context",
            "## Resolution",
            "## Prevention",
            "## Evidence",
        )
        for literal in memory_note_required:
            with self.subTest(literal=literal):
                self.assertIn(literal, rendered)

    def test_task_2_stage00_protocol_matches_registered_template_source_metadata(self) -> None:
        protocol = (
            ROOT / "docs/00.agent-governance/rules/documentation-protocol.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(protocol.split())
        self.assertIn(
            "Governance Memory and Progress template sources use exactly "
            "`layer: agentic` and `status: draft`",
            normalized,
        )
        self.assertIn(
            "the README template source remains the registered status-only source",
            normalized,
        )
        self.assertIn(
            "other typed template sources follow their registry-defined source metadata",
            normalized,
        )
        self.assertNotIn("instead of `layer:`", normalized)
        self.assertNotIn("exempt from the `layer:` requirement", normalized)

    def test_task_2_common_confidentiality_boundary_covers_evidence_roles(self) -> None:
        contract = (
            ROOT / "docs/99.templates/support/common-document-contract.md"
        ).read_text(encoding="utf-8")
        discipline = contract.split("## Source and Evidence Discipline", 1)[1].split(
            "\n## ", 1
        )[0]
        for literal in (
            "Reference",
            "Audit",
            "generated output",
            "Repo-support",
            "secret values",
            "credentials or tokens",
            "private keys",
            "shell history",
            "raw secret-bearing logs",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, discipline)

    def test_audit_has_a_distinct_registered_form(self) -> None:
        role = self.profiles["template_roles"]["audit"]
        self.assertEqual("audit", role["artifact_profile"])
        self.assertTrue((ROOT / role["source"]).is_file())

    def test_memory_mirror_is_absent_and_stage99_is_referenced(self) -> None:
        self.assertFalse((ROOT / "docs/00.agent-governance/memory/template.md").exists())
        text = (ROOT / "docs/00.agent-governance/memory/README.md").read_text(encoding="utf-8")
        self.assertIn("docs/99.templates/templates/governance/memory.template.md", text)

    def test_task_has_one_source_and_no_harness_competitor(self) -> None:
        roles = self.profiles["template_roles"]
        task_sources = [
            role["source"]
            for role in roles.values()
            if role["artifact_profile"] == "task"
        ]
        self.assertEqual(
            ["docs/99.templates/templates/sdlc/task.template.md"],
            task_sources,
        )
        self.assertFalse(
            (
                ROOT
                / "docs/99.templates/templates/governance/harness-task-contract.template.md"
            ).exists()
        )

    def test_task_form_contains_protected_surface_and_qa_evidence(self) -> None:
        text = (
            ROOT / "docs/99.templates/templates/sdlc/task.template.md"
        ).read_text(encoding="utf-8")
        for heading in (
            "## Scope and Change Boundaries",
            "## Approval Evidence",
            "## Work Log",
            "## Verification Evidence",
            "## Review Evidence",
            "## Commit Ledger",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_deleted_harness_task_source_has_no_active_route(self) -> None:
        deleted_path = (
            "docs/99.templates/templates/governance/"
            "harness-task-contract.template.md"
        )
        active_route_files = (
            "docs/00.agent-governance/harness-implementation-map.md",
            "docs/00.agent-governance/rules/approval-boundaries.md",
            "docs/00.agent-governance/rules/documentation-protocol.md",
            "docs/00.agent-governance/rules/stage-authoring-matrix.md",
            "docs/00.agent-governance/rules/task-checklists.md",
            "docs/99.templates/README.md",
            "docs/99.templates/support/template-selection.md",
            "docs/99.templates/templates/governance/README.md",
        )
        for relative_path in active_route_files:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotIn(deleted_path, text)

    def test_stage_99_catalogs_publish_the_literal_canonical_role_inventory(self) -> None:
        catalogs = {
            "docs/99.templates/README.md": (
                "PRD, ARD, ADR, Spec, Plan, Task",
                "Guide, policy, runbook, incident, postmortem, Release",
                "README, reference, Audit, archive",
            ),
            "docs/99.templates/templates/README.md": (
                "`prd`, `ard`, `adr`, `spec`, `plan`, `task`",
                "`guide`, `policy`, `runbook`, `incident`, `postmortem`, `release`",
                "`readme`, `reference`, `audit`, `archive`",
                "`memory`, `progress`",
            ),
        }
        for relative_path, literal_inventories in catalogs.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                for literal_inventory in literal_inventories:
                    self.assertIn(literal_inventory, text)
                self.assertNotRegex(
                    text,
                    r"(?<![A-Za-z0-9_-])harness-task-contract(?![A-Za-z0-9_-])",
                )

    def test_leaf_templates_declare_valid_target_profiles_with_safe_placeholders(self) -> None:
        expected = {
            "docs/99.templates/templates/sdlc/prd.template.md": "prd",
            "docs/99.templates/templates/sdlc/ard.template.md": "ard",
            "docs/99.templates/templates/sdlc/adr.template.md": "adr",
            "docs/99.templates/templates/sdlc/spec.template.md": "spec",
            "docs/99.templates/templates/sdlc/plan.template.md": "plan",
            "docs/99.templates/templates/sdlc/task.template.md": "task",
            "docs/99.templates/templates/operations/guide.template.md": "guide",
            "docs/99.templates/templates/operations/policy.template.md": "policy",
            "docs/99.templates/templates/operations/runbook.template.md": "runbook",
            "docs/99.templates/templates/operations/incident.template.md": "incident",
            "docs/99.templates/templates/operations/postmortem.template.md": "postmortem",
            "docs/99.templates/templates/operations/release.template.md": "release",
            "docs/99.templates/templates/common/reference.template.md": "reference",
            "docs/99.templates/templates/common/audit.template.md": "audit",
            "docs/99.templates/templates/common/archive.template.md": "archive",
            "docs/99.templates/templates/common/readme.template.md": "readme",
            "docs/99.templates/templates/spec-contracts/agent-design.template.md": "spec",
            "docs/99.templates/templates/spec-contracts/api-spec.template.md": "spec",
            "docs/99.templates/templates/spec-contracts/data-model.template.md": "spec",
            "docs/99.templates/templates/spec-contracts/service.template.md": "spec",
            "docs/99.templates/templates/spec-contracts/tests.template.md": "spec",
            "docs/99.templates/templates/governance/memory.template.md": "governance",
            "docs/99.templates/templates/governance/progress.template.md": "governance",
        }
        role_sources = {
            role["source"]: role["artifact_profile"]
            for role in self.profiles["template_roles"].values()
        }
        self.assertEqual(expected, role_sources)
        for path_text, target_profile in expected.items():
            if target_profile in {"governance", "readme"}:
                continue
            with self.subTest(path=path_text):
                values = metadata.parse_frontmatter(ROOT / path_text)
                self.assertEqual("draft", values.get("status"))
                self.assertEqual(target_profile, values.get("artifact_type"))
                self.assertEqual("<artifact-id>", values.get("artifact_id"))
                record = metadata.Record(
                    pathlib.Path(path_text),
                    values,
                    "template-source",
                    frontmatter_present=True,
                )
                self.assertEqual(
                    [],
                    metadata.validate_record(record, self.profiles, metadata.build_manifest([record])),
                )

    def test_typed_leaf_templates_instantiate_valid_targets(self) -> None:
        targets = {
            "docs/99.templates/templates/sdlc/prd.template.md": "docs/01.requirements/901-fixture.md",
            "docs/99.templates/templates/sdlc/ard.template.md": "docs/02.architecture/requirements/0901-fixture.md",
            "docs/99.templates/templates/sdlc/adr.template.md": "docs/02.architecture/decisions/0901-fixture.md",
            "docs/99.templates/templates/sdlc/spec.template.md": "docs/03.specs/901-fixture/spec.md",
            "docs/99.templates/templates/sdlc/plan.template.md": "docs/04.execution/plans/2026-07-13-fixture.md",
            "docs/99.templates/templates/sdlc/task.template.md": "docs/04.execution/tasks/2026-07-13-fixture.md",
            "docs/99.templates/templates/operations/guide.template.md": "docs/05.operations/guides/00-workspace/fixture.md",
            "docs/99.templates/templates/operations/policy.template.md": "docs/05.operations/policies/00-workspace/fixture.md",
            "docs/99.templates/templates/operations/runbook.template.md": "docs/05.operations/runbooks/00-workspace/fixture.md",
            "docs/99.templates/templates/operations/incident.template.md": "docs/05.operations/incidents/2026/INC-901-fixture/INC-901-fixture.md",
            "docs/99.templates/templates/operations/postmortem.template.md": "docs/05.operations/incidents/2026/INC-901-fixture/postmortem.md",
            "docs/99.templates/templates/operations/release.template.md": "docs/05.operations/releases/2026-07-13-fixture.md",
            "docs/99.templates/templates/common/reference.template.md": "docs/90.references/research/fixture.md",
            "docs/99.templates/templates/common/audit.template.md": "docs/90.references/audits/fixture.md",
            "docs/99.templates/templates/common/archive.template.md": "docs/98.archive/03.specs/901-fixture/spec.md",
            "docs/99.templates/templates/spec-contracts/agent-design.template.md": "docs/03.specs/901-fixture/agent-design.md",
            "docs/99.templates/templates/spec-contracts/api-spec.template.md": "docs/03.specs/901-fixture/api-spec.md",
            "docs/99.templates/templates/spec-contracts/data-model.template.md": "docs/03.specs/901-fixture/data-model.md",
            "docs/99.templates/templates/spec-contracts/service.template.md": "docs/03.specs/901-fixture/service.md",
            "docs/99.templates/templates/spec-contracts/tests.template.md": "docs/03.specs/901-fixture/tests.md",
        }
        parents = {
            "prd": metadata.Record(
                pathlib.Path("docs/01.requirements/900-parent.md"),
                {
                    "status": "active",
                    "artifact_id": "fixture:prd-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
                "prd",
            ),
            "spec": metadata.Record(
                pathlib.Path("docs/03.specs/900-parent/spec.md"),
                {
                    "status": "active",
                    "artifact_id": "fixture:spec-parent",
                    "artifact_type": "spec",
                    "parent_ids": ["fixture:prd-parent"],
                },
                "spec",
            ),
            "runbook": metadata.Record(
                pathlib.Path("docs/05.operations/runbooks/00-workspace/parent.md"),
                {
                    "status": "active",
                    "artifact_id": "fixture:runbook-parent",
                    "artifact_type": "runbook",
                    "parent_ids": ["fixture:spec-parent"],
                    "reviewed_at": "2026-07-13",
                    "review_cycle": "annual",
                },
                "runbook",
            ),
            "incident": metadata.Record(
                pathlib.Path("docs/05.operations/incidents/2026/INC-900-parent/INC-900-parent.md"),
                {
                    "status": "active",
                    "artifact_id": "fixture:incident-parent",
                    "artifact_type": "incident",
                    "parent_ids": ["fixture:runbook-parent"],
                },
                "incident",
            ),
        }
        parent_by_target = {
            "ard": "prd",
            "adr": "prd",
            "spec": "prd",
            "plan": "spec",
            "task": "spec",
            "guide": "spec",
            "policy": "prd",
            "runbook": "spec",
            "incident": "runbook",
            "postmortem": "incident",
            "release": "spec",
        }
        placeholder_replacements = {
            "<reviewed-at>": "2026-07-13",
            "<review-cycle>": "annual",
            "docs/<original-path>.md": "docs/03.specs/899-retired/spec.md",
            "YYYY-MM-DD": "2026-07-13",
            "<archive-reason>": "Fixture retirement",
            "docs/<replacement-path>.md": "docs/03.specs/900-parent/spec.md",
        }

        typed_roles = {
            role["source"]: role["artifact_profile"]
            for role in self.profiles["template_roles"].values()
            if role["source"] in targets
        }
        for source_path, target_type in typed_roles.items():
            with self.subTest(source=source_path, target=targets[source_path]):
                parent_type = parent_by_target.get(target_type)
                parent_id = parents[parent_type].metadata["artifact_id"] if parent_type else None
                rendered = (ROOT / source_path).read_text(encoding="utf-8")
                rendered = rendered.replace("<artifact-id>", f"fixture:{pathlib.Path(source_path).stem}")
                if parent_id:
                    rendered = rendered.replace("<parent-artifact-id>", str(parent_id))
                for placeholder, replacement in placeholder_replacements.items():
                    rendered = rendered.replace(placeholder, replacement)
                values = metadata._parse_frontmatter_text(rendered)
                if target_type == "archive":
                    values["status"] = "archived"
                    replacement = values.pop("current_replacement")
                    values.update(
                        {
                            "archive_disposition": "superseded",
                            "archived_commit": "a" * 40,
                            "archived_blob": "b" * 40,
                            "preservation_class": "git-history",
                            "current_replacement": replacement,
                        }
                    )
                record = metadata.Record(
                    pathlib.Path(targets[source_path]),
                    values,
                    target_type,
                    frontmatter_present=True,
                )
                manifest_records = [*parents.values(), record]
                self.assertEqual(
                    [],
                    metadata.validate_record(
                        record,
                        self.profiles,
                        metadata.build_manifest(manifest_records),
                    ),
                )

    def test_release_routing_is_complete_without_an_event_record(self) -> None:
        selection = (ROOT / "docs/99.templates/support/template-selection.md").read_text(encoding="utf-8")
        matrix = (ROOT / "docs/00.agent-governance/rules/stage-authoring-matrix.md").read_text(encoding="utf-8")
        releases = (ROOT / "docs/05.operations/releases/README.md").read_text(encoding="utf-8")
        operations = (ROOT / "docs/05.operations/README.md").read_text(encoding="utf-8")
        operations_templates = (
            ROOT / "docs/99.templates/templates/operations/README.md"
        ).read_text(encoding="utf-8")
        spec_templates = (
            ROOT / "docs/99.templates/templates/spec-contracts/README.md"
        ).read_text(encoding="utf-8")
        sdlc_templates = (
            ROOT / "docs/99.templates/templates/sdlc/README.md"
        ).read_text(encoding="utf-8")
        templates = (ROOT / "docs/99.templates/templates/README.md").read_text(encoding="utf-8")
        template_root = (ROOT / "docs/99.templates/README.md").read_text(encoding="utf-8")

        route = "docs/05.operations/releases/YYYY-MM-DD-release-name.md"
        source = "docs/99.templates/templates/operations/release.template.md"
        self.assertIn(f"| Release | `{route}`", selection)
        self.assertIn(route, matrix)
        self.assertIn(source, matrix)
        self.assertIn("changelog/release-readiness evidence", releases)
        self.assertIn("Spec 127", releases)
        self.assertIn("[릴리스](./releases/README.md)", operations)
        self.assertIn("[release.template.md](./release.template.md)", operations_templates)
        self.assertIn("[api-spec.template.md](./api-spec.template.md)", spec_templates)
        self.assertIn("[task.template.md](./task.template.md)", sdlc_templates)
        self.assertIn("| Operations | [operations/](./operations/README.md)", templates)
        self.assertIn("`release`", templates)
        self.assertIn("[Release template](./templates/operations/release.template.md)", template_root)
        release_leaves = sorted(
            path
            for path in (ROOT / "docs/05.operations/releases").glob("*.md")
            if path.name != "README.md"
        )
        self.assertEqual([], release_leaves)

    def test_release_template_does_not_create_an_event_leaf(self) -> None:
        leaves = [
            path
            for path in (ROOT / "docs/05.operations/releases").glob("*.md")
            if path.name != "README.md"
        ]
        self.assertEqual([], leaves)

    def test_readme_template_remains_a_readme_exception_source(self) -> None:
        path_text = "docs/99.templates/templates/common/readme.template.md"
        values = metadata.parse_frontmatter(ROOT / path_text)
        self.assertEqual({"status": "draft"}, values)

    def test_governance_template_source_rejects_typed_leaf_metadata(self) -> None:
        record = metadata.Record(
            pathlib.Path("docs/99.templates/templates/governance/memory.template.md"),
            {
                "status": "draft",
                "artifact_id": "template-source:invalid",
                "artifact_type": "template-source",
                "parent_ids": [],
            },
            "template-source",
            frontmatter_present=True,
        )
        codes = {
            finding.code
            for finding in metadata.validate_record(
                record,
                self.profiles,
                metadata.build_manifest([record]),
            )
        }
        self.assertIn("invalid-template-metadata", codes)


class TemplateBodyContractTests(unittest.TestCase):
    TASK_2_ROLE_HEADINGS = {
        "readme": (
            "## Overview",
            "## Audience",
            "## Scope",
            "## Structure",
            "## How to Work in This Area",
            "## Related Documents",
        ),
        "reference": (
            "## Overview",
            "## Purpose",
            "## Scope",
            "## Facts and Definitions",
            "## Sources",
            "## Maintenance",
            "## Related Documents",
        ),
        "audit": (
            "## Overview",
            "## Scope and Criteria",
            "## Evidence",
            "## Findings",
            "## Gap Analysis",
            "## Disposition",
            "## Related Documents",
        ),
        "archive": (
            "## Overview",
            "## Archive Metadata",
            "## Current Replacement",
            "## Archive Ledger",
            "## Related Documents",
        ),
        "memory": (
            "## Problem",
            "## Context",
            "## Resolution",
            "## Prevention",
            "## Evidence",
            "## Related Documents",
        ),
        "progress": (
            "## Current Work Log",
            "## Phase Tracker",
            "## Layer Audit",
            "## Open Issues",
            "## Related Documents",
        ),
    }
    TASK_2_ROLE_PROFILES = {
        "readme": "readme",
        "reference": "reference",
        "audit": "audit",
        "archive": "archive",
        "memory": "governance",
        "progress": "governance",
    }
    TASK_2_ROLE_TOKENS = {
        "readme": {
            "title", "overview", "audience", "scope", "structure",
            "work_instructions", "related_documents",
        },
        "reference": {
            "title", "overview", "purpose", "scope", "facts_and_definitions",
            "sources", "maintenance", "related_documents",
        },
        "audit": {
            "title", "overview", "scope_and_criteria", "evidence", "findings",
            "gap_analysis", "disposition", "related_documents",
        },
        "archive": {
            "title", "overview", "archive_metadata", "current_replacement",
            "archive_ledger", "related_documents",
        },
        "memory": {
            "title", "date", "layer", "status", "applies_to", "tags",
            "retrieval_keywords", "last_verified", "problem", "context",
            "resolution", "prevention", "evidence", "related_documents",
        },
        "progress": {
            "title", "current_work_log", "phase_tracker", "layer_audit",
            "open_issues", "related_documents",
        },
    }
    TASK_3_ROLE_HEADINGS = {
        "prd": (
            "## Overview",
            "## Problem and Stakeholders",
            "## Requirements",
            "## Acceptance and Verification",
            "## Scope and Non-goals",
            "## Risks and Dependencies",
            "## AI Agent Requirements",
            "## Related Documents",
        ),
        "ard": (
            "## Overview and Context",
            "## Stakeholders and Concerns",
            "## Boundaries and Constraints",
            "## Quality Attributes",
            "## Architecture Views",
            "## Data and Infrastructure",
            "## Decision and Requirement Traceability",
            "## AI Agent Architecture",
            "## Related Documents",
        ),
        "adr": (
            "## Context and Decision Drivers",
            "## Considered Options",
            "## Decision",
            "## Consequences",
            "## Confirmation",
            "## Follow-up Decisions",
            "## Related Documents",
        ),
        "spec": (
            "## Overview",
            "## Boundaries and Inputs",
            "## Contracts",
            "## Core Design",
            "## Interfaces and Data",
            "## Failure Modes and Guardrails",
            "## Verification",
            "## Agent Role and IO Contract",
            "## Related Documents",
        ),
        "agent-design": (
            "## Overview",
            "## Role and Responsibilities",
            "## Inputs and Outputs",
            "## Orchestration",
            "## Tools and Permissions",
            "## Prompt Policy",
            "## Context and Memory",
            "## Guardrails",
            "## Failure Handling",
            "## Evaluation",
            "## Observability",
            "## Human Approval",
            "## Related Documents",
        ),
        "api-spec": (
            "## Overview",
            "## Parent and Scope",
            "## API Style",
            "## Authentication and Authorization",
            "## Operations",
            "## Request and Response Schemas",
            "## Errors",
            "## Compatibility",
            "## Non-functional Requirements",
            "## Machine-readable Contracts",
            "## Verification",
            "## Pagination",
            "## Related Documents",
        ),
        "data-model": (
            "## Overview",
            "## Parent and Scope",
            "## Entities",
            "## Relationships",
            "## Schema",
            "## Integrity",
            "## Storage",
            "## Privacy",
            "## Migration",
            "## Retention",
            "## Related Documents",
        ),
        "service": (
            "## Overview",
            "## Parent and Scope",
            "## Image and Build",
            "## Security",
            "## Networking and Storage",
            "## Secrets",
            "## Health and Operations",
            "## Validation",
            "## Scaling",
            "## Related Documents",
        ),
        "tests": (
            "## Overview",
            "## Parent and Scope",
            "## Verification Goals",
            "## TDD Scope",
            "## Test Matrix",
            "## Contract and Integration Tests",
            "## Non-functional Tests",
            "## Agent Evaluations",
            "## Fixtures",
            "## Execution",
            "## Evidence",
            "## Related Documents",
        ),
    }
    TASK_3_ROLE_PROFILES = {
        "prd": "prd",
        "ard": "ard",
        "adr": "adr",
        "spec": "spec",
        "agent-design": "spec",
        "api-spec": "spec",
        "data-model": "spec",
        "service": "spec",
        "tests": "spec",
    }
    TASK_3_ROLE_TOKENS = {
        "prd": {
            "title",
            "value_and_outcomes",
            "problem_statement",
            "stakeholders_and_use_cases",
            "requirements_with_stable_ids",
            "constraints_and_provenance",
            "acceptance_criteria",
            "success_measures",
            "verification_intent",
            "scope_and_non_goals",
            "risks_and_dependencies",
            "assumptions",
            "ai_agent_requirements",
            "related_documents",
        },
        "ard": {
            "title",
            "overview_and_context",
            "stakeholders_and_concerns",
            "boundaries_and_constraints",
            "quality_attributes",
            "architecture_views",
            "data_and_infrastructure",
            "decision_and_requirement_traceability",
            "ai_agent_architecture",
            "related_documents",
        },
        "adr": {
            "title",
            "context_and_decision_drivers",
            "considered_options",
            "decision",
            "consequences",
            "confirmation",
            "follow_up_decisions",
            "related_documents",
        },
        "spec": {
            "title",
            "overview",
            "boundaries_and_inputs",
            "api_contract_summary",
            "api_contract_ownership",
            "api_contract_link",
            "core_design",
            "service_contract_summary",
            "service_contract_ownership",
            "service_contract_link",
            "data_contract_summary",
            "data_contract_ownership",
            "data_contract_link",
            "failure_modes_and_guardrails",
            "verification",
            "test_contract_summary",
            "test_contract_ownership",
            "test_contract_link",
            "agent_design_summary",
            "agent_design_ownership",
            "agent_design_link",
            "related_documents",
        },
        "agent-design": {
            "title",
            "overview",
            "role_and_responsibilities",
            "inputs_and_outputs",
            "orchestration",
            "tools_and_permissions",
            "prompt_policy",
            "context_and_memory",
            "guardrails",
            "failure_handling",
            "evaluation",
            "observability",
            "human_approval",
            "related_documents",
        },
        "api-spec": {
            "title",
            "overview",
            "parent_spec_link",
            "scope_and_non_goals",
            "api_style",
            "authentication_and_authorization",
            "operations",
            "request_and_response_schemas",
            "errors",
            "compatibility",
            "non_functional_requirements",
            "machine_readable_contracts",
            "verification",
            "pagination",
            "related_documents",
        },
        "data-model": {
            "title",
            "overview",
            "parent_spec_link",
            "scope_and_non_goals",
            "entities",
            "relationships",
            "schema",
            "integrity",
            "storage",
            "privacy",
            "migration",
            "retention",
            "related_documents",
        },
        "service": {
            "title",
            "overview",
            "parent_spec_link",
            "scope_and_non_goals",
            "image_and_build",
            "security",
            "networking_and_storage",
            "secrets",
            "health_and_operations",
            "validation",
            "scaling",
            "related_documents",
        },
        "tests": {
            "title",
            "overview",
            "parent_spec_link",
            "scope",
            "verification_goals",
            "tdd_scope",
            "test_matrix",
            "contract_and_integration_tests",
            "non_functional_tests",
            "agent_evaluations",
            "fixtures",
            "execution",
            "evidence",
            "related_documents",
        },
    }
    TASK_4_ROLE_HEADINGS = {
        "plan": (
            "## Overview",
            "## Context and Inputs",
            "## Goals and Non-goals",
            "## Work Breakdown",
            "## Verification Plan",
            "## Risks and Rollback",
            "## Approval Gates",
            "## Completion Criteria",
            "## Related Documents",
        ),
        "task": (
            "## Overview",
            "## Inputs",
            "## Goals and Non-goals",
            "## Scope and Change Boundaries",
            "## Approval Evidence",
            "## Work Breakdown",
            "## Work Log",
            "## Verification Evidence",
            "## Controlled Agent Pre-commit Evidence",
            "## Review Evidence",
            "## Commit Ledger",
            "## Deferred and Blocked Items",
            "## Related Documents",
        ),
    }
    TASK_4_ROLE_PROFILES = {
        "plan": "plan",
        "task": "task",
    }
    TASK_4_ROLE_H1 = {
        "plan": "# {{title}} Implementation Plan",
        "task": "# Task: {{title}}",
    }
    TASK_4_ROLE_TOKENS = {
        "plan": {
            "title",
            "overview",
            "context_and_inputs",
            "goals_and_non_goals",
            "work_breakdown",
            "verification_commands",
            "expected_verification",
            "risks_and_rollback",
            "approval_gates",
            "completion_criteria",
            "related_documents",
        },
        "task": {
            "title",
            "overview",
            "inputs",
            "goals_and_non_goals",
            "allowed_paths",
            "forbidden_paths",
            "compose_impact",
            "security_impact",
            "operations_impact",
            "runtime_impact",
            "approval_source",
            "protected_surfaces",
            "approval_boundary",
            "rollback_or_recovery",
            "redaction_boundary",
            "work_breakdown",
            "work_log",
            "exact_commands",
            "expected_evidence",
            "actual_evidence",
            "verification_results",
            "controlled_wrapper_command",
            "controlled_wrapper_allowed_prefixes",
            "controlled_wrapper_exit_status",
            "controlled_wrapper_snapshot_result",
            "controlled_wrapper_observation_boundary",
            "controlled_wrapper_path_sets",
            "controlled_wrapper_disposition",
            "implementation_review_verdict",
            "specification_review_verdict",
            "quality_review_verdict",
            "review_findings_and_disposition",
            "commit_identity",
            "commit_logical_unit",
            "commit_validation",
            "deferred_items",
            "blocked_items",
            "deferral_destination",
            "related_documents",
        },
    }
    TASK_5_ROLE_HEADINGS = {
        "guide": (
            "## Overview",
            "## Audience and Prerequisites",
            "## Routine Usage",
            "## Common Checks",
            "## Runbook Handoff",
            "## Troubleshooting",
            "## Related Documents",
        ),
        "policy": (
            "## Overview",
            "## Scope",
            "## Controls",
            "## Exceptions",
            "## Verification",
            "## Review Cadence",
            "## Compliance Mapping",
            "## Related Documents",
        ),
        "runbook": (
            "## Overview",
            "## Trigger and Preconditions",
            "## Procedure",
            "## Verification Record",
            "## Evidence",
            "## Rollback or Recovery",
            "## Escalation",
            "## Automation Handoff",
            "## Related Documents",
        ),
        "incident": (
            "## Overview",
            "## Incident Metadata",
            "## Impact",
            "## Timeline and Response",
            "## Evidence",
            "## Resolution and Handoff",
            "## Runbook Links",
            "## Related Documents",
        ),
        "postmortem": (
            "## Overview",
            "## Incident and Impact",
            "## Timeline",
            "## Root Cause and Contributing Factors",
            "## Lessons",
            "## Action Items",
            "## Prevention and Verification",
            "## Feedback Loop",
            "## Detection Analysis",
            "## Related Documents",
        ),
        "release": (
            "## Overview",
            "## Identity and Scope",
            "## Included Changes",
            "## Artifacts",
            "## Validation Evidence",
            "## Approvals",
            "## Rollout and Rollback",
            "## Outcome and Known Issues",
            "## Compatibility Notes",
            "## Related Documents",
        ),
    }
    TASK_5_ROLE_PROFILES = {
        "guide": "guide",
        "policy": "policy",
        "runbook": "runbook",
        "incident": "incident",
        "postmortem": "postmortem",
        "release": "release",
    }
    TASK_5_ROLE_TOKENS = {
        "guide": {
            "title", "overview", "audience_and_prerequisites", "routine_usage",
            "common_checks", "runbook_handoff", "troubleshooting",
            "related_documents",
        },
        "policy": {
            "title", "overview", "scope", "controls", "exceptions",
            "verification", "review_cadence", "compliance_mapping",
            "related_documents",
        },
        "runbook": {
            "title", "overview", "trigger", "prerequisites", "safety_conditions",
            "step_order", "procedure_step", "expected_result",
            "verification_environment", "verification_command_or_procedure",
            "verification_result", "verification_evidence_location",
            "supporting_evidence", "rollback_or_recovery", "escalation",
            "automation_candidate_or_invocation",
            "human_or_operator_judgment_boundary", "related_documents",
        },
        "incident": {
            "title", "overview", "severity", "incident_lead",
            "current_response_state", "impact", "response_timestamp",
            "response_action", "response_action_owner", "response_state_change",
            "evidence", "mitigation", "resolution", "handoff", "runbook_links",
            "related_documents",
        },
        "postmortem": {
            "title", "overview", "incident_and_impact", "timeline",
            "root_cause_and_contributing_factors", "lessons",
            "reviewed_action_description", "action_owner", "action_priority",
            "action_tracking_identity", "verification_owner",
            "prevention_and_verification", "feedback_loop", "detection_analysis",
            "related_documents",
        },
        "release": {
            "title", "overview", "immutable_release_identity", "version_or_tag",
            "commit_identity", "release_scope", "included_changes",
            "artifact_identifier", "artifact_digest_or_immutable_evidence",
            "validation_check", "validation_result",
            "validation_evidence_location", "approval_authority",
            "approval_decision", "approval_evidence", "rollout_execution",
            "rollback_disposition", "rollout_evidence", "release_outcome",
            "known_issues", "compatibility_assessment", "related_documents",
        },
    }
    TASK_5_MANDATORY_EVIDENCE_TOKENS = {
        "runbook": {
            "prerequisites", "safety_conditions", "step_order", "procedure_step",
            "expected_result", "verification_environment",
            "verification_command_or_procedure", "verification_result",
            "verification_evidence_location",
            "automation_candidate_or_invocation",
            "human_or_operator_judgment_boundary",
        },
        "incident": {
            "severity", "incident_lead", "current_response_state",
            "response_action", "mitigation", "resolution", "handoff",
        },
        "postmortem": {
            "reviewed_action_description", "action_owner", "action_priority",
            "action_tracking_identity", "verification_owner",
        },
        "release": {
            "immutable_release_identity", "version_or_tag", "commit_identity",
            "artifact_identifier", "artifact_digest_or_immutable_evidence",
            "validation_result", "approval_decision", "compatibility_assessment",
            "rollout_execution", "rollback_disposition", "release_outcome",
            "known_issues",
        },
    }
    ALL_ROLE_SOURCES = {
        "readme": "docs/99.templates/templates/common/readme.template.md",
        "reference": "docs/99.templates/templates/common/reference.template.md",
        "audit": "docs/99.templates/templates/common/audit.template.md",
        "archive": "docs/99.templates/templates/common/archive.template.md",
        "memory": "docs/99.templates/templates/governance/memory.template.md",
        "progress": "docs/99.templates/templates/governance/progress.template.md",
        "prd": "docs/99.templates/templates/sdlc/prd.template.md",
        "ard": "docs/99.templates/templates/sdlc/ard.template.md",
        "adr": "docs/99.templates/templates/sdlc/adr.template.md",
        "spec": "docs/99.templates/templates/sdlc/spec.template.md",
        "plan": "docs/99.templates/templates/sdlc/plan.template.md",
        "task": "docs/99.templates/templates/sdlc/task.template.md",
        "guide": "docs/99.templates/templates/operations/guide.template.md",
        "policy": "docs/99.templates/templates/operations/policy.template.md",
        "runbook": "docs/99.templates/templates/operations/runbook.template.md",
        "incident": "docs/99.templates/templates/operations/incident.template.md",
        "postmortem": "docs/99.templates/templates/operations/postmortem.template.md",
        "release": "docs/99.templates/templates/operations/release.template.md",
        "agent-design": "docs/99.templates/templates/spec-contracts/agent-design.template.md",
        "api-spec": "docs/99.templates/templates/spec-contracts/api-spec.template.md",
        "data-model": "docs/99.templates/templates/spec-contracts/data-model.template.md",
        "service": "docs/99.templates/templates/spec-contracts/service.template.md",
        "tests": "docs/99.templates/templates/spec-contracts/tests.template.md",
    }
    MACHINE_TOKENS = {
        "docs/99.templates/templates/spec-contracts/openapi.template.yaml": {
            "API_TITLE",
            "API_VERSION",
            "API_DESCRIPTION",
            "SERVER_URL",
            "AUTH_SELECTION",
            "TAG_NAME",
            "RESOURCE_PATH",
            "HTTP_METHOD",
            "SUCCESS_STATUS",
            "ERROR_STATUS",
            "OPERATION_ID",
            "OPERATION_SUMMARY",
            "SUCCESS_DESCRIPTION",
            "ERROR_DESCRIPTION",
            "RESPONSE_SCHEMA",
            "IDENTIFIER_FIELD",
            "STATUS_FIELD",
        },
        "docs/99.templates/templates/spec-contracts/schema.template.graphql": {
            "QUERY_FIELD",
            "ARGUMENT_NAME",
            "OBJECT_TYPE",
            "IDENTIFIER_FIELD",
            "STATUS_FIELD",
        },
        "docs/99.templates/templates/spec-contracts/service.template.proto": {
            "PACKAGE_NAME",
            "SERVICE_NAME",
            "RPC_NAME",
            "REQUEST_MESSAGE",
            "RESPONSE_MESSAGE",
            "REQUEST_FIELD",
            "IDENTIFIER_FIELD",
            "STATUS_FIELD",
        },
    }
    SPEC_CHILD_HANDOFF_TOKENS = {
        f"{role}_{field}"
        for role in ("api_contract", "service_contract", "data_contract", "agent_design", "test_contract")
        for field in ("summary", "ownership", "link")
    }
    SPEC_CHILD_DETAIL_TOKENS = {
        "role_and_responsibilities",
        "inputs_and_outputs",
        "orchestration",
        "tools_and_permissions",
        "prompt_policy",
        "context_and_memory",
        "evaluation",
        "observability",
        "api_style",
        "authentication_and_authorization",
        "operations",
        "request_and_response_schemas",
        "errors",
        "compatibility",
        "machine_readable_contracts",
        "entities",
        "relationships",
        "schema",
        "integrity",
        "storage",
        "privacy",
        "migration",
        "image_and_build",
        "security",
        "networking_and_storage",
        "secrets",
        "health_and_operations",
        "verification_goals",
        "tdd_scope",
        "test_matrix",
        "contract_and_integration_tests",
        "non_functional_tests",
        "fixtures",
        "execution",
        "evidence",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    @staticmethod
    def fixture_record(path_text: str, artifact_type: str) -> object:
        return metadata.Record(
            pathlib.Path(path_text),
            {},
            artifact_type,
            frontmatter_present=False,
        )

    @staticmethod
    def literal_spec_body(*, include_requirements: bool = True) -> str:
        headings = [
            "## Overview",
            "## Boundaries and Inputs",
            "## Contracts",
            "## Core Design",
            "## Interfaces and Data",
            "## Failure Modes and Guardrails",
            "## Verification",
            "## Related Documents",
        ]
        if not include_requirements:
            headings.remove("## Contracts")
        return "# Fixture\n\n" + "\n\ncontent\n\n".join(headings) + "\n"

    def body_finding_codes(
        self,
        record: object,
        text: str,
        *,
        profiles: dict[str, object] | None = None,
        changed_boundary: bool = True,
    ) -> set[str]:
        return {
            finding.code
            for finding in metadata.validate_body_contract(
                record,
                text,
                profiles or self.profiles,
                changed_boundary=changed_boundary,
            )
        }

    def test_markdown_heading_extraction_ignores_fenced_examples(self) -> None:
        text = (
            "# Title\n\n"
            "~~~text\n## Tilde example\n~~~\n\n"
            "```markdown\n# Backtick example\n## Backtick H2\n```\n\n"
            "## Overview\n"
        )
        h1, h2 = metadata.extract_markdown_headings(text)
        self.assertEqual(["# Title"], h1)
        self.assertEqual(["## Overview"], h2)

    def test_commonmark_fence_scanner_honors_delimiter_specific_info_strings(self) -> None:
        cases = (
            (
                "backtick info may contain tilde",
                "# Title\n\n```markdown title=\"~example~\"\n# Hidden\n{{hidden_token}}\n```\n\n## Overview\n",
            ),
            (
                "tilde info may contain backticks and tildes",
                "# Title\n\n~~~markdown title=\"`example` ~draft~\"\n# Hidden\n{{hidden_token}}\n~~~\n\n## Overview\n",
            ),
            (
                "unclosed backtick fence hides the remaining example",
                "# Title\n\n```markdown title=\"~example~\"\n# Hidden\n{{hidden_token}}\n",
            ),
            (
                "unclosed tilde fence hides the remaining example",
                "# Title\n\n~~~markdown title=\"`example`\"\n# Hidden\n{{hidden_token}}\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label):
                h1, h2 = metadata.extract_markdown_headings(text)
                self.assertEqual(["# Title"], h1)
                expected_h2 = ["## Overview"] if "Overview" in text else []
                self.assertEqual(expected_h2, h2)

    def test_inline_code_scanner_requires_equal_backtick_run_lengths(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        documented = (
            self.literal_spec_body()
            + "\nDocument `> Rules:` and `{{single_token}}`.\n"
            + "Document `` `> Rules:` and `{{multi_token}}` ``.\n"
        )
        documented_codes = self.body_finding_codes(record, documented)
        self.assertNotIn("template-instruction-in-target", documented_codes)
        self.assertNotIn("template-body-token-in-target", documented_codes)

        genuine = documented + "\n> Rules:\n\n{{outside_code}}\n"
        genuine_codes = self.body_finding_codes(record, genuine)
        self.assertIn("template-instruction-in-target", genuine_codes)
        self.assertIn("template-body-token-in-target", genuine_codes)

    def test_required_heading_reports_code(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        missing = self.body_finding_codes(
            record,
            self.literal_spec_body(include_requirements=False),
        )
        self.assertIn("body-heading-missing", missing)

    def test_forbidden_heading_reports_code(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        forbidden = self.body_finding_codes(
            record,
            self.literal_spec_body() + "\n## Success Criteria\n\ncontent\n",
        )
        self.assertIn("body-heading-forbidden", forbidden)

    def test_conditional_heading_may_be_absent(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        conditional_absent = self.body_finding_codes(
            record,
            self.literal_spec_body(),
        )
        self.assertNotIn("body-heading-missing", conditional_absent)

    def test_two_h1_headings_report_code(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        codes = self.body_finding_codes(
            record,
            self.literal_spec_body() + "\n# Duplicate\n",
        )
        self.assertIn("body-h1-count", codes)

    def test_changed_target_rejects_template_instruction_and_body_token(self) -> None:
        record = self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec")
        text = self.literal_spec_body() + "\n> Rules:\n\n{{explain_scope}}\n"
        codes = self.body_finding_codes(record, text)
        self.assertIn("template-instruction-in-target", codes)
        self.assertIn("template-body-token-in-target", codes)
        documented = self.body_finding_codes(
            record,
            self.literal_spec_body()
            + "\nThe source syntax is `> Rules:` and `{{documented_token}}`.\n",
        )
        self.assertNotIn("template-instruction-in-target", documented)
        self.assertNotIn("template-body-token-in-target", documented)

    def test_zero_role_match_reports_code(self) -> None:
        missing = self.body_finding_codes(
            self.fixture_record("docs/03.specs/901-fixture/unknown.md", "spec"),
            self.literal_spec_body(),
        )
        self.assertIn("template-role-missing", missing)

    def test_ambiguous_role_match_reports_code(self) -> None:
        roles = dict(self.profiles["template_roles"])
        roles["api-spec"] = {
            **roles["api-spec"],
            "target_globs": ["docs/03.specs/*/spec.md"],
        }
        ambiguous_profiles = {**self.profiles, "template_roles": roles}
        ambiguous = self.body_finding_codes(
            self.fixture_record("docs/03.specs/901-fixture/spec.md", "spec"),
            self.literal_spec_body(),
            profiles=ambiguous_profiles,
        )
        self.assertIn("template-role-ambiguous", ambiguous)

    def test_template_catalog_readme_requires_profile_headings(self) -> None:
        catalog = self.fixture_record(
            "docs/99.templates/templates/README.md",
            "readme",
        )
        unrelated = self.fixture_record("README.md", "readme")
        text = "# Catalog\n\n## Overview\n"
        self.assertIn("readme-heading-missing", self.body_finding_codes(catalog, text))
        self.assertNotIn("readme-heading-missing", self.body_finding_codes(unrelated, text))

    def test_machine_source_requires_token(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        missing = self.body_finding_codes(
            record,
            "openapi: 3.1.0\ninfo:\n  title: fixture\n",
            changed_boundary=False,
        )
        self.assertIn("machine-template-token-missing", missing)

    def test_machine_source_rejects_example_host(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        concrete = self.body_finding_codes(
            record,
            "openapi: 3.1.0\nx-template-token: __API_TITLE__\nservers:\n  - url: https://api.example.com\n",
            changed_boundary=False,
        )
        concrete_auth = self.body_finding_codes(
            record,
            "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-auth: basic\n",
            changed_boundary=False,
        )
        self.assertIn("machine-template-example-value", concrete)
        self.assertIn("machine-template-example-value", concrete_auth)

    def test_machine_sources_reject_bounded_concrete_credential_assignments(self) -> None:
        cases = (
            (
                "openapi api key",
                "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-api-key: fixture-key\n",
            ),
            (
                "openapi password",
                "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npassword: fixture-password\n",
            ),
            (
                "openapi secret",
                "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nclient_secret: fixture-secret\n",
            ),
            (
                "graphql credential default",
                "docs/99.templates/templates/spec-contracts/schema.template.graphql",
                "input Login { password: String = \"fixture-password\" }\ntype Query { login: String }\n# __GRAPHQL_TOKEN__\n",
            ),
            (
                "graphql credential literal",
                "docs/99.templates/templates/spec-contracts/schema.template.graphql",
                "type Query { login: String }\nquery { login(apiKey: \"fixture-key\") }\n# __GRAPHQL_TOKEN__\n",
            ),
            (
                "protobuf credential default",
                "docs/99.templates/templates/spec-contracts/service.template.proto",
                "syntax = \"proto2\";\nmessage Login { optional string secret = 1 [default = \"fixture-secret\"]; }\n// __PROTO_TOKEN__\n",
            ),
            (
                "protobuf credential option",
                "docs/99.templates/templates/spec-contracts/service.template.proto",
                "syntax = \"proto3\";\noption (auth_token) = \"fixture-token\";\n// __PROTO_TOKEN__\n",
            ),
            (
                "bearer literal",
                "docs/99.templates/templates/spec-contracts/schema.template.graphql",
                "type Query { login: String }\nquery { login(token: \"Bearer fixture-token\") }\n# __GRAPHQL_TOKEN__\n",
            ),
            (
                "jwt literal",
                "docs/99.templates/templates/spec-contracts/service.template.proto",
                "syntax = \"proto3\";\noption (jwt) = \"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmaXh0dXJlIn0.signature\";\n// __PROTO_TOKEN__\n",
            ),
        )
        for label, relative_path, text in cases:
            with self.subTest(case=label):
                record = self.fixture_record(relative_path, "unsupported")
                codes = self.body_finding_codes(record, text, changed_boundary=False)
                self.assertIn("machine-template-example-value", codes)

    def test_machine_credential_gate_accepts_schema_declarations_and_current_sentinels(self) -> None:
        openapi_schema = (
            "openapi: 3.1.0\n"
            "x-template-auth-selection: __AUTH_SELECTION__\n"
            "components:\n"
            "  securitySchemes:\n"
            "    ApiKeyAuth:\n"
            "      type: apiKey\n"
            "      name: X-API-Key\n"
            "      in: header\n"
        )
        graphql_declaration = (
            "input Login { password: String, apiKey: String }\n"
            "type Query { login(input: Login): String }\n"
            "# __GRAPHQL_TOKEN__\n"
        )
        proto_declaration = (
            "syntax = \"proto3\";\n"
            "message Login { string password = 1; string api_key = 2; }\n"
            "// __PROTO_TOKEN__\n"
        )
        cases = (
            ("docs/99.templates/templates/spec-contracts/openapi.template.yaml", openapi_schema),
            ("docs/99.templates/templates/spec-contracts/schema.template.graphql", graphql_declaration),
            ("docs/99.templates/templates/spec-contracts/service.template.proto", proto_declaration),
        )
        for relative_path, text in cases:
            with self.subTest(path=relative_path):
                record = self.fixture_record(relative_path, "unsupported")
                codes = self.body_finding_codes(record, text, changed_boundary=False)
                self.assertNotIn("machine-template-example-value", codes)

    def test_openapi_parse_failures_are_static_and_fail_closed(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        cases = (
            (
                "malformed",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npaths: [fixture-parse-leak\n",
                "fixture-parse-leak",
            ),
            (
                "duplicate-key",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\ninfo: fixture-first\ninfo: fixture-duplicate-leak\n",
                "fixture-duplicate-leak",
            ),
            (
                "constructor",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-value: !!python/object:fixture-constructor-leak {}\n",
                "fixture-constructor-leak",
            ),
            (
                "non-mapping-root",
                "- __API_TITLE__\n- fixture-root-leak\n",
                "fixture-root-leak",
            ),
        )
        for label, text, private_value in cases:
            with self.subTest(case=label):
                findings = metadata._machine_template_findings(record, text)
                parse_findings = [
                    finding
                    for finding in findings
                    if finding.code == "machine-template-parse-error"
                ]
                self.assertEqual(1, len(parse_findings))
                self.assertEqual(
                    "machine template could not be parsed as a safe OpenAPI mapping",
                    parse_findings[0].message,
                )
                self.assertNotIn(private_value, repr(findings))

    def test_openapi_credential_schema_value_keywords_reject_concrete_values(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with self.subTest(keyword=keyword):
                text = (
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          {keyword}: {value}\n"
                )
                findings = metadata._machine_template_findings(record, text)
                self.assertIn(
                    "machine-template-example-value",
                    {finding.code for finding in findings},
                )
                self.assertNotIn("fixture-", repr(findings))
        with self.subTest(keyword="direct-list"):
            findings = metadata._machine_template_findings(
                record,
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "access_token: [__ACCESS_TOKEN__, fixture-direct-list-leak]\n",
            )
            self.assertIn(
                "machine-template-example-value",
                {finding.code for finding in findings},
            )
            self.assertNotIn("fixture-direct-list-leak", repr(findings))

    def test_openapi_credential_plural_examples_reject_nested_concrete_leaves_without_leaks(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        cases = {
            "scalar": "fixture-scalar-private",
            "list": "[__PASSWORD_PRIMARY__, fixture-list-private]",
            "map": "{primary: __PASSWORD_PRIMARY__, secondary: fixture-map-private}",
        }
        for label, examples in cases.items():
            with self.subTest(shape=label):
                text = (
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          examples: {examples}\n"
                )
                findings = metadata._machine_template_findings(record, text)
                self.assertIn(
                    "machine-template-example-value",
                    {finding.code for finding in findings},
                )
                self.assertNotIn("fixture-", repr(findings))

    def test_openapi_credential_plural_examples_accept_exact_nested_tokens(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        text = (
            "openapi: 3.1.0\n"
            "x-template-token: __API_TITLE__\n"
            "components:\n"
            "  schemas:\n"
            "    Login:\n"
            "      properties:\n"
            "        password:\n"
            "          type: string\n"
            "          examples:\n"
            "            primary: __PASSWORD_PRIMARY__\n"
            "            alternatives:\n"
            "              - __PASSWORD_SECONDARY__\n"
            "              - __PASSWORD_TERTIARY__\n"
        )
        codes = {
            finding.code
            for finding in metadata._machine_template_findings(record, text)
        }
        self.assertNotIn("machine-template-parse-error", codes)
        self.assertNotIn("machine-template-example-value", codes)

    def test_openapi_credential_context_accepts_exact_tokens_and_schema_only_fields(self) -> None:
        record = self.fixture_record(
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "unsupported",
        )
        cases = (
            (
                "direct-and-list-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "x-api-key: __API_KEY__\n"
                "access_token: [__ACCESS_TOKEN__, __REFRESH_TOKEN__]\n",
            ),
            (
                "credential-schema-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          default: __PASSWORD_DEFAULT__\n"
                "          example: __PASSWORD_EXAMPLE__\n"
                "          const: __PASSWORD_CONST__\n"
                "          enum: [__PASSWORD_PRIMARY__, __PASSWORD_SECONDARY__]\n",
            ),
            (
                "schema-only-and-unrelated-default",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      required: [password]\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          format: password\n"
                "          description: caller-supplied credential\n"
                "        displayName:\n"
                "          type: string\n"
                "          default: fixture display name\n",
            ),
            (
                "standard-example-token",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          example: __PASSWORD_EXAMPLE__\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label):
                codes = {
                    finding.code
                    for finding in metadata._machine_template_findings(record, text)
                }
                self.assertNotIn("machine-template-parse-error", codes)
                self.assertNotIn("machine-template-example-value", codes)

        for relative_path in (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "docs/99.templates/templates/spec-contracts/schema.template.graphql",
            "docs/99.templates/templates/spec-contracts/service.template.proto",
        ):
            with self.subTest(current_source=relative_path):
                record = self.fixture_record(relative_path, "unsupported")
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                codes = self.body_finding_codes(record, text, changed_boundary=False)
                self.assertNotIn("machine-template-example-value", codes)

    @staticmethod
    def body_tokens(text: str) -> set[str]:
        return set(re.findall(r"\{\{([a-z][a-z0-9_]*)\}\}", text))

    def copied_profiles_with_role(
        self,
        role_name: str,
        **role_updates: object,
    ) -> dict[str, object]:
        roles = dict(self.profiles["template_roles"])
        roles[role_name] = {**roles[role_name], **role_updates}
        return {**self.profiles, "template_roles": roles}

    def assert_markdown_role_contract(
        self,
        role_name: str,
        text: str,
        *,
        expected_headings: tuple[str, ...],
        expected_profile: str,
        expected_tokens: set[str],
        expected_h1: str,
        empty_parents: bool = False,
    ) -> None:
        role = self.profiles["template_roles"][role_name]
        h1_headings = [line for line in text.splitlines() if line.startswith("# ")]
        h2_headings = [line for line in text.splitlines() if line.startswith("## ")]
        registry_headings = [
            *role["required_headings"],
            *role["conditional_headings"],
        ]
        expected_frontmatter = {
            "status": "draft",
            "artifact_id": "<artifact-id>",
            "artifact_type": expected_profile,
            "parent_ids": [] if empty_parents else ["<parent-artifact-id>"],
        }

        self.assertEqual([expected_h1], h1_headings)
        self.assertEqual(list(expected_headings), h2_headings)
        self.assertEqual(
            collections.Counter(expected_headings),
            collections.Counter(registry_headings),
        )
        self.assertEqual(expected_profile, role["artifact_profile"])
        self.assertEqual(expected_frontmatter, metadata._parse_frontmatter_text(text))
        self.assertEqual(expected_tokens, self.body_tokens(text))
        self.assertNotIn("> Rules:", text)
        self.assertNotIn("<!-- Target:", text)

    def assert_task_3_markdown_contract(self, role_name: str, text: str) -> None:
        self.assert_markdown_role_contract(
            role_name,
            text,
            expected_headings=self.TASK_3_ROLE_HEADINGS[role_name],
            expected_profile=self.TASK_3_ROLE_PROFILES[role_name],
            expected_tokens=self.TASK_3_ROLE_TOKENS[role_name],
            expected_h1="# {{title}}",
            empty_parents=role_name == "prd",
        )

    def assert_task_4_markdown_contract(self, role_name: str, text: str) -> None:
        self.assert_markdown_role_contract(
            role_name,
            text,
            expected_headings=self.TASK_4_ROLE_HEADINGS[role_name],
            expected_profile=self.TASK_4_ROLE_PROFILES[role_name],
            expected_tokens=self.TASK_4_ROLE_TOKENS[role_name],
            expected_h1=self.TASK_4_ROLE_H1[role_name],
        )

    def assert_task_5_markdown_contract(self, role_name: str, text: str) -> None:
        role = self.profiles["template_roles"][role_name]
        h1_headings = [line for line in text.splitlines() if line.startswith("# ")]
        h2_headings = [line for line in text.splitlines() if line.startswith("## ")]
        expected_frontmatter = {
            "status": "draft",
            "artifact_id": "<artifact-id>",
            "artifact_type": self.TASK_5_ROLE_PROFILES[role_name],
            "parent_ids": [] if role_name == "incident" else ["<parent-artifact-id>"],
        }
        if role_name in {"policy", "runbook"}:
            expected_frontmatter.update(
                {"reviewed_at": "<reviewed-at>", "review_cycle": "<review-cycle>"}
            )
        elif role_name == "postmortem":
            expected_frontmatter["reviewed_at"] = "<reviewed-at>"

        self.assertEqual(["# {{title}}"], h1_headings)
        self.assertEqual(list(self.TASK_5_ROLE_HEADINGS[role_name]), h2_headings)
        self.assertEqual(
            collections.Counter(self.TASK_5_ROLE_HEADINGS[role_name]),
            collections.Counter(
                [*role["required_headings"], *role["conditional_headings"]]
            ),
        )
        self.assertEqual(self.TASK_5_ROLE_PROFILES[role_name], role["artifact_profile"])
        self.assertEqual(expected_frontmatter, metadata._parse_frontmatter_text(text))
        self.assertEqual(self.TASK_5_ROLE_TOKENS[role_name], self.body_tokens(text))
        self.assertNotIn("> Rules:", text)
        self.assertNotIn("<!-- Target:", text)
        self.assertNotIn("<!-- Release Target:", text)

    def assert_machine_source_contract(self, relative_path: str, text: str) -> None:
        expected_tokens = self.MACHINE_TOKENS[relative_path]
        actual_tokens = set(re.findall(r"__([A-Z][A-Z0-9_]*)__", text))
        self.assertEqual(expected_tokens, actual_tokens)
        comment_prefix = "//" if relative_path.endswith(".proto") else "#"
        self.assertIn(f"{comment_prefix} Target:", text)
        self.assertIn(f"{comment_prefix} Cross-links:", text)
        self.assertNotRegex(text, r"https?://")
        self.assertNotRegex(
            text,
            r"(?i)\b(?:[a-z0-9-]+\.)+(?:com|dev|invalid|io|local|net|org)\b",
        )
        self.assertNotRegex(
            text,
            r"(?i)\b(?:bearer|basic|oauth2?|openidconnect|api[_-]?key)\b",
        )
        self.assertNotRegex(text, r"(?i)\bexample(?:\.com)?\b")

        if relative_path.endswith("openapi.template.yaml"):
            document = yaml.safe_load(text)
            self.assertIsInstance(document, dict)
            self.assertEqual("__SERVER_URL__", document["servers"][0]["url"])
            self.assertEqual(
                "__AUTH_SELECTION__", document["x-template-auth-selection"]
            )
            self.assertNotIn("security", document)
            self.assertNotIn("securitySchemes", document.get("components", {}))
            allowed_path_item_keys = {
                "$ref",
                "summary",
                "description",
                "get",
                "put",
                "post",
                "delete",
                "options",
                "head",
                "patch",
                "trace",
                "servers",
                "parameters",
            }
            for path_item in document["paths"].values():
                invalid_keys = {
                    key
                    for key in path_item
                    if key not in allowed_path_item_keys and not key.startswith("x-")
                }
                self.assertEqual(set(), invalid_keys)
                operation = path_item["get"]
                self.assertEqual("__HTTP_METHOD__", operation["x-template-http-method"])
                self.assertEqual(
                    "__SUCCESS_STATUS__", operation["x-template-success-status"]
                )
                self.assertEqual(
                    "__ERROR_STATUS__", operation["x-template-error-status"]
                )
                response_keys = set(operation["responses"])
                self.assertEqual({"200", "default"}, response_keys)
                for key in response_keys:
                    self.assertRegex(key, r"^(?:default|[1-5](?:[0-9]{2}|XX))$")
        elif relative_path.endswith("schema.template.graphql"):
            body = "\n".join(
                line for line in text.splitlines() if not line.lstrip().startswith("#")
            )
            names = re.findall(r"(?<![A-Za-z0-9_])([_A-Za-z][_0-9A-Za-z]*)", body)
            self.assertEqual([], [name for name in names if name.startswith("__")])
            sentinel_map = {
                "_templateQueryField": "__QUERY_FIELD__",
                "_templateArgument": "__ARGUMENT_NAME__",
                "_TemplateObject": "__OBJECT_TYPE__",
                "_templateIdentifier": "__IDENTIFIER_FIELD__",
                "_templateStatus": "__STATUS_FIELD__",
            }
            for sentinel, token in sentinel_map.items():
                self.assertIn(f"# {sentinel} -> {token}", text)
                self.assertIn(sentinel, body)
            self.assertEqual(body.count("{"), body.count("}"))
        else:
            body = "\n".join(
                line for line in text.splitlines() if not line.lstrip().startswith("//")
            )
            self.assertIn('syntax = "proto3";', body)
            self.assertRegex(body, r"package\s+__PACKAGE_NAME__\s*;")
            self.assertRegex(body, r"service\s+__SERVICE_NAME__\s*\{")
            self.assertRegex(
                body,
                r"rpc\s+__RPC_NAME__\s*\(__REQUEST_MESSAGE__\)\s*"
                r"returns\s*\(__RESPONSE_MESSAGE__\)\s*;",
            )
            self.assertEqual(2, len(re.findall(r"message\s+__[A-Z0-9_]+__\s*\{", body)))
            self.assertEqual(body.count("{"), body.count("}"))

    def test_task_3_markdown_sources_match_exact_contracts(self) -> None:
        for role_name in self.TASK_3_ROLE_TOKENS:
            with self.subTest(role=role_name):
                role = self.profiles["template_roles"][role_name]
                text = (ROOT / role["source"]).read_text(encoding="utf-8")
                self.assert_task_3_markdown_contract(role_name, text)

    def test_task_4_plan_and_task_sources_match_exact_contracts(self) -> None:
        for role_name in self.TASK_4_ROLE_TOKENS:
            with self.subTest(role=role_name):
                role = self.profiles["template_roles"][role_name]
                text = (ROOT / role["source"]).read_text(encoding="utf-8")
                self.assert_task_4_markdown_contract(role_name, text)

    def test_task_5_operations_sources_match_exact_contracts(self) -> None:
        for role_name in self.TASK_5_ROLE_TOKENS:
            with self.subTest(role=role_name):
                source = ROOT / self.ALL_ROLE_SOURCES[role_name]
                self.assert_task_5_markdown_contract(
                    role_name, source.read_text(encoding="utf-8")
                )

    def test_operations_forms_have_non_overlapping_headings(self) -> None:
        base = ROOT / "docs/99.templates/templates/operations"
        guide = (base / "guide.template.md").read_text(encoding="utf-8")
        policy = (base / "policy.template.md").read_text(encoding="utf-8")
        runbook = (base / "runbook.template.md").read_text(encoding="utf-8")
        for forbidden in ("## Rollback or Recovery", "## Escalation"):
            with self.subTest(heading=forbidden):
                self.assertNotIn(forbidden, guide)
        self.assertNotIn("## Procedure", policy)
        self.assertEqual(1, runbook.count("## Rollback or Recovery"))

    def test_all_23_markdown_roles_have_independent_literal_contract_coverage(self) -> None:
        expected_headings = {
            **self.TASK_2_ROLE_HEADINGS,
            **self.TASK_3_ROLE_HEADINGS,
            **self.TASK_4_ROLE_HEADINGS,
            **self.TASK_5_ROLE_HEADINGS,
        }
        expected_profiles = {
            **self.TASK_2_ROLE_PROFILES,
            **self.TASK_3_ROLE_PROFILES,
            **self.TASK_4_ROLE_PROFILES,
            **self.TASK_5_ROLE_PROFILES,
        }
        expected_tokens = {
            **self.TASK_2_ROLE_TOKENS,
            **self.TASK_3_ROLE_TOKENS,
            **self.TASK_4_ROLE_TOKENS,
            **self.TASK_5_ROLE_TOKENS,
        }
        expected_roles = set(self.ALL_ROLE_SOURCES)
        self.assertEqual(23, len(expected_roles))
        self.assertEqual(expected_roles, set(self.profiles["template_roles"]))
        self.assertEqual(expected_roles, set(expected_headings))
        self.assertEqual(expected_roles, set(expected_profiles))
        self.assertEqual(expected_roles, set(expected_tokens))

        for role_name, source_path in self.ALL_ROLE_SOURCES.items():
            with self.subTest(role=role_name):
                role = self.profiles["template_roles"][role_name]
                text = (ROOT / source_path).read_text(encoding="utf-8")
                h1 = [line for line in text.splitlines() if line.startswith("# ")]
                h2 = [line for line in text.splitlines() if line.startswith("## ")]
                self.assertEqual(source_path, role["source"])
                self.assertEqual(expected_profiles[role_name], role["artifact_profile"])
                self.assertEqual(list(expected_headings[role_name]), h2)
                self.assertEqual(expected_tokens[role_name], self.body_tokens(text))
                if role_name in self.TASK_5_MANDATORY_EVIDENCE_TOKENS:
                    self.assertLessEqual(
                        self.TASK_5_MANDATORY_EVIDENCE_TOKENS[role_name],
                        self.body_tokens(text),
                    )
                self.assertEqual(1, len(h1))
                self.assertNotIn("> Rules:", text)
                self.assertNotRegex(text, r"<!-- (?:Release )?Target:")

    def test_task_5_negative_mutations_are_rejected(self) -> None:
        role_name = "runbook"
        text = (ROOT / self.ALL_ROLE_SOURCES[role_name]).read_text(encoding="utf-8")
        mutations = {
            "extra-h1": text.replace("# {{title}}", "# {{title}}\n\n# Duplicate", 1),
            "extra-heading": text.replace(
                "## Related Documents",
                "## Routine Usage\n\n{{overview}}\n\n## Related Documents",
                1,
            ),
            "duplicate-recovery": text.replace(
                "## Escalation",
                "## Rollback or Recovery\n\n{{rollback_or_recovery}}\n\n## Escalation",
                1,
            ),
            "missing-heading": text.replace("## Evidence\n\n", "", 1),
            "rules-block": text.replace("## Overview", "> Rules:\n\n## Overview", 1),
            "target-comment": text.replace(
                "# {{title}}",
                "<!-- Target: docs/05.operations/runbooks/fixture.md -->\n\n# {{title}}",
                1,
            ),
            "frontmatter-drift": text.replace(
                "artifact_type: runbook", "artifact_type: guide", 1
            ),
            "token-drift": text.replace(
                "{{verification_environment}}", "{{verification_context}}", 1
            ),
        }
        for name, mutated in mutations.items():
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                self.assert_task_5_markdown_contract(role_name, mutated)

    def test_task_5_mandatory_evidence_token_removal_is_rejected(self) -> None:
        for role_name, mandatory_tokens in self.TASK_5_MANDATORY_EVIDENCE_TOKENS.items():
            text = (ROOT / self.ALL_ROLE_SOURCES[role_name]).read_text(encoding="utf-8")
            for token in mandatory_tokens:
                with self.subTest(role=role_name, token=token):
                    self.assertIn(f"{{{{{token}}}}}", text)
                    mutated = text.replace(f"{{{{{token}}}}}", "", 1)
                    with self.assertRaises(AssertionError):
                        self.assert_task_5_markdown_contract(role_name, mutated)

    def test_plan_form_is_prospective_only(self) -> None:
        role = self.profiles["template_roles"]["plan"]
        text = (ROOT / role["source"]).read_text(encoding="utf-8")
        tokens = self.body_tokens(text)
        for forbidden_token in (
            "actual_evidence",
            "verification_results",
            "work_log",
            "implementation_review_verdict",
            "specification_review_verdict",
            "quality_review_verdict",
            "commit_identity",
        ):
            with self.subTest(token=forbidden_token):
                self.assertNotIn(forbidden_token, tokens)
        for forbidden_heading in (
            "## Verification Evidence",
            "## Work Log",
            "## Review Evidence",
            "## Commit Ledger",
        ):
            with self.subTest(heading=forbidden_heading):
                self.assertNotIn(forbidden_heading, text)

    def test_task_4_negative_mutations_are_rejected(self) -> None:
        task_role = self.profiles["template_roles"]["task"]
        task_text = (ROOT / task_role["source"]).read_text(encoding="utf-8")
        mutations = {
            "extra-h1": task_text.replace(
                "# Task: {{title}}",
                "# Task: {{title}}\n\n# Duplicate",
                1,
            ),
            "extra-heading": task_text.replace(
                "## Related Documents",
                "## Unregistered\n\n{{overview}}\n\n## Related Documents",
                1,
            ),
            "missing-heading": task_text.replace(
                "## Approval Evidence\n\n", "", 1
            ),
            "rules-block": task_text.replace(
                "## Overview", "> Rules:\n\n## Overview", 1
            ),
            "target-comment": task_text.replace(
                "# Task: {{title}}",
                "<!-- Target: docs/04.execution/tasks/fixture.md -->\n\n"
                "# Task: {{title}}",
                1,
            ),
            "frontmatter-drift": task_text.replace(
                "artifact_type: task", "artifact_type: plan", 1
            ),
            "token-drift": task_text.replace(
                "{{actual_evidence}}", "{{result_summary}}", 1
            ),
        }
        for name, mutated in mutations.items():
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                self.assert_task_4_markdown_contract("task", mutated)

    def test_parent_spec_has_all_child_handoffs_without_child_details(self) -> None:
        role = self.profiles["template_roles"]["spec"]
        text = (ROOT / role["source"]).read_text(encoding="utf-8")
        tokens = self.body_tokens(text)
        self.assertTrue(self.SPEC_CHILD_HANDOFF_TOKENS <= tokens)
        self.assertFalse(self.SPEC_CHILD_DETAIL_TOKENS & tokens)

    def test_machine_sources_match_exact_native_safe_contracts(self) -> None:
        for relative_path in self.MACHINE_TOKENS:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assert_machine_source_contract(relative_path, text)

    def test_task_3_negative_mutations_are_rejected(self) -> None:
        spec_role = self.profiles["template_roles"]["spec"]
        spec_text = (ROOT / spec_role["source"]).read_text(encoding="utf-8")
        markdown_mutations = {
            "extra-heading": spec_text.replace(
                "## Related Documents", "## Unregistered\n\n{{overview}}\n\n## Related Documents"
            ),
            "missing-heading": spec_text.replace(
                "## Agent Role and IO Contract\n\n", "", 1
            ),
        }
        for name, mutated in markdown_mutations.items():
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                self.assert_task_3_markdown_contract("spec", mutated)

        openapi_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        openapi = (ROOT / openapi_path).read_text(encoding="utf-8")
        machine_mutations = {
            "concrete-host": (
                openapi_path,
                openapi.replace(
                    "paths:\n",
                    "x-concrete-host: https://api.production.invalid\npaths:\n",
                    1,
                ),
            ),
            "concrete-auth": (
                openapi_path,
                openapi.replace(
                    "paths:\n",
                    "x-concrete-auth-selection: basic\npaths:\n",
                    1,
                ),
            ),
            "invalid-openapi-operation-key": (
                openapi_path,
                openapi.replace("    get:\n", "    __HTTP_METHOD__:\n", 1),
            ),
            "invalid-openapi-response-key": (
                openapi_path,
                openapi.replace('        "200":\n', '        "__SUCCESS_STATUS__":\n', 1),
            ),
        }
        graphql_path = (
            "docs/99.templates/templates/spec-contracts/schema.template.graphql"
        )
        graphql = (ROOT / graphql_path).read_text(encoding="utf-8")
        machine_mutations["reserved-graphql-name"] = (
            graphql_path,
            graphql + "\ntype __ReservedObject {\n  _templateValue: String\n}\n",
        )
        for name, (relative_path, mutated) in machine_mutations.items():
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                self.assert_machine_source_contract(relative_path, mutated)

    def test_coordinated_registry_and_source_heading_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["prd"]
        source = (ROOT / role["source"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "prd",
            required_headings=[
                "## Executive Summary"
                if heading == "## Overview"
                else heading
                for heading in role["required_headings"]
            ],
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_3_markdown_contract(
                    "prd",
                    source.replace("## Overview", "## Executive Summary", 1),
                )
        finally:
            self.profiles = original_profiles

    def test_coordinated_registry_and_source_profile_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["prd"]
        source = (ROOT / role["source"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "prd",
            artifact_profile="reference",
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_3_markdown_contract(
                    "prd",
                    source.replace("artifact_type: prd", "artifact_type: reference", 1),
                )
        finally:
            self.profiles = original_profiles

    def test_task_4_coordinated_registry_and_source_heading_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["plan"]
        source = (ROOT / role["source"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "plan",
            required_headings=[
                "## Delivery Plan"
                if heading == "## Work Breakdown"
                else heading
                for heading in role["required_headings"]
            ],
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_4_markdown_contract(
                    "plan",
                    source.replace("## Work Breakdown", "## Delivery Plan", 1),
                )
        finally:
            self.profiles = original_profiles

    def test_task_4_coordinated_registry_and_source_profile_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["task"]
        source = (ROOT / role["source"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "task",
            artifact_profile="plan",
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_4_markdown_contract(
                    "task",
                    source.replace("artifact_type: task", "artifact_type: plan", 1),
                )
        finally:
            self.profiles = original_profiles

    def test_task_5_coordinated_registry_and_source_heading_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["guide"]
        source = (ROOT / self.ALL_ROLE_SOURCES["guide"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "guide",
            required_headings=[
                "## Operator Workflow"
                if heading == "## Routine Usage"
                else heading
                for heading in role["required_headings"]
            ],
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_5_markdown_contract(
                    "guide",
                    source.replace("## Routine Usage", "## Operator Workflow", 1),
                )
        finally:
            self.profiles = original_profiles

    def test_task_5_coordinated_registry_and_source_profile_drift_is_rejected(self) -> None:
        role = self.profiles["template_roles"]["release"]
        source = (ROOT / self.ALL_ROLE_SOURCES["release"]).read_text(encoding="utf-8")
        mutated_profiles = self.copied_profiles_with_role(
            "release",
            artifact_profile="task",
        )
        original_profiles = self.profiles
        self.profiles = mutated_profiles
        try:
            with self.assertRaises(AssertionError):
                self.assert_task_5_markdown_contract(
                    "release",
                    source.replace("artifact_type: release", "artifact_type: task", 1),
                )
        finally:
            self.profiles = original_profiles


class RepositoryContractIntegrationTests(unittest.TestCase):
    def fixture(self, directory: str) -> tuple[pathlib.Path, pathlib.Path]:
        root = pathlib.Path(directory)
        return root, copy_tracked_contract_fixture(root)

    def write_profiles(self, path: pathlib.Path, values: dict[str, object]) -> None:
        path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")

    def run_contracts(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        return run_checker(root, "check-contracts", profiles=profiles)

    def test_exact_registry_extension_keys_fail_closed(self) -> None:
        mutations = (
            ("frontmatter_order", lambda values: values["common"].__setitem__("key_order", values["common"].pop("frontmatter_order"))),
            ("document_families", lambda values: values.__setitem__("families", values.pop("document_families"))),
            ("readme_profiles", lambda values: values.__setitem__("readmes", values.pop("readme_profiles"))),
        )
        for expected, mutate in mutations:
            with self.subTest(key=expected), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
                mutate(values)
                self.write_profiles(profiles, values)
                result = self.run_contracts(root, profiles)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(expected, result.stderr)

    def test_readme_ownership_overlap_and_unclassified_path_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
            names = list(values["readme_profiles"])
            values["readme_profiles"][names[1]]["path_globs"].append(
                values["readme_profiles"][names[0]]["path_globs"][0]
            )
            self.write_profiles(profiles, values)
            result = self.run_contracts(root, profiles)
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("README profile globs overlap", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            write_doc(root / "unclassified/README.md", None)
            staged = git(root, "add", "unclassified/README.md")
            self.assertEqual(0, staged.returncode, staged.stderr)
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("readme-unclassified", result.stdout)

    def test_repository_contracts_enforce_readme_profile_frontmatter_behavior(self) -> None:
        cases = (
            (
                "forbidden non-empty frontmatter",
                "README.md",
                "---\nstatus: active\n---\n\n",
                1,
                "readme-frontmatter-forbidden: README.md",
            ),
            (
                "forbidden empty frontmatter",
                "README.md",
                "---\n---\n\n",
                1,
                "readme-frontmatter-forbidden: README.md",
            ),
            (
                "optional allowed key",
                "docs/05.operations/releases/README.md",
                "---\nstatus: active\n---\n\n",
                0,
                "metadata repository contracts: violations=0",
            ),
            (
                "optional disallowed key",
                "docs/05.operations/releases/README.md",
                "---\nlayer: ops\n---\n\n",
                1,
                "readme-frontmatter-key: docs/05.operations/releases/README.md",
            ),
        )
        for label, path_text, contents, expected_exit, expected_output in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / path_text
                body = path.read_text(encoding="utf-8")
                if body.startswith("---\n"):
                    closing = body.find("\n---\n", 4)
                    self.assertNotEqual(-1, closing)
                    body = body[closing + len("\n---\n") :].lstrip("\n")
                path.write_text(contents + body, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(expected_exit, result.returncode, result.stdout + result.stderr)
                self.assertIn(expected_output, result.stdout)

    def test_repository_contracts_keep_readme_profile_identity_when_generated_by_is_present(self) -> None:
        cases = (
            (
                "forbidden root README",
                "README.md",
                "readme-frontmatter-forbidden: README.md",
            ),
            (
                "optional releases README",
                "docs/05.operations/releases/README.md",
                "readme-frontmatter-key: docs/05.operations/releases/README.md",
            ),
        )
        for label, path_text, expected_output in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / path_text
                body = path.read_text(encoding="utf-8")
                if body.startswith("---\n"):
                    closing = body.find("\n---\n", 4)
                    self.assertNotEqual(-1, closing)
                    body = body[closing + len("\n---\n") :].lstrip("\n")
                path.write_text(
                    "---\ngenerated_by: scripts/example.py\n---\n\n" + body,
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(expected_output, result.stdout)

    def test_typed_markdown_template_mapping_is_complete_and_consistent(self) -> None:
        source = "docs/99.templates/templates/spec-contracts/api-spec.template.md"
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
            values["template_roles"]["api-spec"]["source"] = (
                "docs/99.templates/templates/spec-contracts/missing.template.md"
            )
            self.write_profiles(profiles, values)
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("template-source-missing", result.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
            values["template_roles"]["api-spec"]["artifact_profile"] = "plan"
            self.write_profiles(profiles, values)
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"template-source-type-mismatch: {source}", result.stdout)

    def test_every_typed_markdown_template_leaf_requires_a_known_mapping(self) -> None:
        cases = (
            (
                "docs/99.templates/templates/common/rogue.md",
                "spec",
                "template-source-unmapped",
            ),
            (
                "docs/99.templates/templates/common/rogue.template.md",
                "typo",
                "template-source-unknown-type",
            ),
        )
        for source, artifact_type, expected in cases:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                write_doc(root / source, {"artifact_type": artifact_type})
                staged = git(root, "add", source)
                self.assertEqual(0, staged.returncode, staged.stderr)
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"{expected}: {source}", result.stdout)

    def test_mapped_template_requires_non_null_declared_target_type(self) -> None:
        source = "docs/99.templates/templates/spec-contracts/api-spec.template.md"
        for mutation in ("omitted", "null"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / source
                values = metadata.parse_frontmatter(path)
                if mutation == "omitted":
                    values.pop("artifact_type")
                else:
                    values["artifact_type"] = None
                write_doc(path, values)
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"template-source-missing-type: {source}", result.stdout)

    def test_release_selection_stage_00_and_stage_05_routes_fail_closed(self) -> None:
        route = "docs/05.operations/releases/YYYY-MM-DD-release-name.md"
        release_source = "docs/99.templates/templates/operations/release.template.md"
        route_files = (
            "docs/99.templates/support/template-selection.md",
            "docs/00.agent-governance/rules/stage-authoring-matrix.md",
            "docs/05.operations/releases/README.md",
        )
        for route_file in route_files:
            with self.subTest(path=route_file), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / route_file
                text = path.read_text(encoding="utf-8")
                path.write_text(
                    text.replace(route, "docs/05.operations/releases/MISSING.md")
                    .replace("YYYY-MM-DD-release-name.md", "MISSING.md")
                    .replace(
                        release_source,
                        "docs/99.templates/templates/operations/MISSING.template.md",
                    )
                    .replace("release.template.md", "MISSING.template.md"),
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"release-route-incomplete: {route_file}", result.stdout)

    def test_release_is_in_required_inventory(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        release_sources = [
            role["source"]
            for role in profiles["template_roles"].values()
            if role["artifact_profile"] == "release"
        ]
        self.assertEqual(
            ["docs/99.templates/templates/operations/release.template.md"],
            release_sources,
        )
        findings = metadata.validate_repository_contracts(ROOT, profiles)
        self.assertNotIn(
            "release-template-cardinality",
            {finding.code for finding in findings},
        )

    def test_repository_contracts_enforce_machine_source_safety(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            path = root / relative_path
            path.write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "servers:\n"
                "  - url: https://api.example.com\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )

    def test_repository_contracts_fail_closed_on_openapi_parse_boundaries_without_leaks(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        cases = (
            (
                "malformed",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npaths: [fixture-parse-leak\n",
                "fixture-parse-leak",
            ),
            (
                "duplicate-key",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\ninfo: fixture-first\ninfo: fixture-duplicate-leak\n",
                "fixture-duplicate-leak",
            ),
            (
                "constructor",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-value: !!python/object:fixture-constructor-leak {}\n",
                "fixture-constructor-leak",
            ),
            (
                "non-mapping-root",
                "- __API_TITLE__\n- fixture-root-leak\n",
                "fixture-root-leak",
            ),
        )
        for label, text, private_value in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-parse-error: {relative_path}: "
                    "machine template could not be parsed as a safe OpenAPI mapping",
                    result.stdout,
                )
                self.assertNotIn(private_value, rendered)
                self.assertNotRegex(rendered, r"(?i)(line|column) [0-9]+")

    def test_repository_contracts_bound_openapi_credential_value_keywords(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with self.subTest(keyword=keyword), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          {keyword}: {value}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)
        with self.subTest(keyword="direct-list"), tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "access_token: [__ACCESS_TOKEN__, fixture-direct-list-leak]\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )
            self.assertNotIn("fixture-direct-list-leak", rendered)

    def test_repository_contracts_reject_openapi_credential_plural_examples_without_leaks(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        cases = {
            "scalar": "fixture-scalar-cli-private",
            "list": "[__PASSWORD_PRIMARY__, fixture-list-cli-private]",
            "map": "{primary: __PASSWORD_PRIMARY__, secondary: fixture-map-cli-private}",
        }
        for label, examples in cases.items():
            with self.subTest(shape=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          examples: {examples}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)

    def test_repository_contracts_accept_exact_nested_openapi_credential_examples_tokens(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          examples:\n"
                "            primary: __PASSWORD_PRIMARY__\n"
                "            alternatives:\n"
                "              - __PASSWORD_SECONDARY__\n"
                "              - __PASSWORD_TERTIARY__\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_repository_contracts_accept_safe_openapi_credential_shapes(self) -> None:
        relative_path = (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml"
        )
        cases = (
            (
                "exact-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "x-api-key: __API_KEY__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          default: __PASSWORD_DEFAULT__\n"
                "          example: __PASSWORD_EXAMPLE__\n"
                "          const: __PASSWORD_CONST__\n"
                "          enum: [__PASSWORD_PRIMARY__, __PASSWORD_SECONDARY__]\n",
            ),
            (
                "schema-only-unrelated-default",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      required: [password]\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          format: password\n"
                "          description: caller-supplied credential\n"
                "        displayName:\n"
                "          type: string\n"
                "          default: fixture display name\n",
            ),
            (
                "standard-example-token",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          example: __PASSWORD_EXAMPLE__\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_changed_checker_enforces_body_contract_on_new_typed_target(self) -> None:
        relative_path = "docs/01.requirements/901-fixture.md"
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            commit_all(root, "base")
            write_doc(
                root / relative_path,
                {
                    "status": "draft",
                    "artifact_id": "prd:901-fixture",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
                "# Fixture\n\n"
                "## Overview\n\ncontent\n\n"
                "## Problem and Stakeholders\n\ncontent\n\n"
                "## Requirements\n\n> Rules:\n\n{{requirement}}\n\n"
                "## Acceptance and Verification\n\ncontent\n\n"
                "## Scope and Non-goals\n\ncontent\n\n"
                "## Risks and Dependencies\n\ncontent\n\n"
                "## Related Documents\n\ncontent\n",
            )
            result = run_checker(
                root,
                "check-changed",
                "--changed-path",
                relative_path,
                profiles=profiles,
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("template-instruction-in-target", result.stdout)
            self.assertIn("template-body-token-in-target", result.stdout)

    def test_shell_delegates_template_schema_without_duplicate_tables(self) -> None:
        text = (ROOT / "scripts/validation/check-repo-contracts.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "python3 scripts/validation/check-document-metadata.py --mode check-contracts",
            text,
        )
        self.assertNotIn("required_templates=(", text)
        self.assertNotIn("heading_requirements:", text)
        self.assertNotIn("operation_forbidden =", text)

    def test_human_support_document_cannot_copy_full_registry_array(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
            support = root / "docs/99.templates/support/common-document-contract.md"
            copied = yaml.safe_dump(
                {"frontmatter_order": values["common"]["frontmatter_order"]},
                sort_keys=False,
            )
            support.write_text(
                f"{support.read_text(encoding='utf-8')}\n```yaml\n{copied}```\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("registry-array-duplicated: docs/99.templates/support/common-document-contract.md", result.stdout)

    def test_registry_array_copies_are_yaml_serialization_independent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            values = yaml.safe_load(profiles.read_text(encoding="utf-8"))
            order = values["common"]["frontmatter_order"]
            quoted_order = ", ".join(
                f"'{member}'" if index % 2 else f'"{member}"'
                for index, member in enumerate(order)
            )
            singleton = values["common"]["inventory_excludes"][0]
            support = root / "docs/99.templates/support/common-document-contract.md"
            support.write_text(
                f"{support.read_text(encoding='utf-8')}\n"
                f"```yaml\nfrontmatter_order: [{quoted_order}]\n```\n"
                f"```yaml\ninventory_excludes: ['{singleton}']\n```\n"
                "```yaml\nallowed_parent_types: []\n```\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("registry-array-duplicated: docs/99.templates/support/common-document-contract.md", result.stdout)
            self.assertIn("common.frontmatter_order", result.stdout)
            self.assertIn("common.inventory_excludes", result.stdout)
            self.assertIn("profiles.prd.allowed_parent_types", result.stdout)

    def test_workspace_cannot_become_a_docs_inventory_prefix(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        original = metadata.TARGET_MARKDOWN_PREFIXES
        try:
            metadata.TARGET_MARKDOWN_PREFIXES = (*original, "_workspace/")
            findings = metadata.validate_repository_contracts(ROOT, profiles)
        finally:
            metadata.TARGET_MARKDOWN_PREFIXES = original
        self.assertIn(
            "workspace-inventory-coupling",
            {finding.code for finding in findings},
        )


class CheckerCliTests(unittest.TestCase):
    def test_duplicate_artifact_id_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            values = {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
            }
            write_doc(root / "docs/03.specs/123-a/spec.md", values)
            write_doc(root / "docs/03.specs/123-b/spec.md", values)
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("duplicate-artifact-id", result.stdout)
            self.assertIn("| duplicate |", result.stdout)

    def test_duplicate_yaml_key_has_distinct_inventory_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertEqual(2, result.returncode)
            self.assertIn("frontmatter-duplicate-key", result.stdout)
            self.assertIn("| duplicate-key |", result.stdout)

    def test_report_returns_nonzero_for_parser_failure_but_renders_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: [active\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("frontmatter-malformed-yaml", result.stdout)
            self.assertIn(path.relative_to(root).as_posix(), result.stdout)

    def test_unhashable_mapping_key_has_no_traceback_and_writes_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            output = root / "inventory.md"
            result = run_checker(root, "report", "--output", str(output))
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("frontmatter-malformed-yaml", rendered)
            self.assertIn("malformed-yaml", rendered)

    def test_changed_mode_fails_only_selected_violations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            invalid = root / "docs/03.specs/123-example/spec.md"
            valid = root / "docs/03.specs/README.md"
            write_doc(invalid, {"status": "active"})
            write_doc(valid, None)
            passing = run_checker(root, "check-changed", "--changed-path", "docs/03.specs/README.md")
            failing = run_checker(
                root,
                "check-changed",
                "--changed-path",
                "docs/03.specs/123-example/spec.md",
            )
            self.assertEqual(0, passing.returncode, passing.stdout + passing.stderr)
            self.assertNotEqual(0, failing.returncode)
            self.assertIn("missing-required-key", failing.stdout)

    def test_changed_mode_archive_selector_shape_has_no_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            path = "docs/98.archive/04.execution/new-target.md"
            write_doc(
                root / path,
                {
                    "status": "archived",
                    "artifact_id": "archive:04-execution-new-target",
                    "artifact_type": "archive",
                    "parent_ids": [],
                    "archived_from": "docs/04.execution/new-target.md",
                    "archived_on": "2026-07-14",
                    "archive_reason": "Bounded selector-shape fixture.",
                    "archive_disposition": ["superseded"],
                    "archived_commit": "a" * 40,
                    "archived_blob": "b" * 40,
                    "preservation_class": "git-history",
                    "current_replacement": "docs/04.execution/current.md",
                },
            )
            result = run_checker(root, "check-changed", "--changed-path", path)
            combined = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, combined)
            self.assertIn("invalid-archive-disposition", result.stdout)
            self.assertNotIn("Traceback", combined)

    def test_report_order_is_deterministic_and_sorted_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/200-z/spec.md", {"status": "active"})
            write_doc(root / "docs/01.requirements/100-a.md", {"status": "active"})
            first = run_checker(root, "report")
            second = run_checker(root, "report")
            self.assertEqual(first.stdout, second.stdout)
            self.assertLess(
                first.stdout.index("docs/01.requirements/100-a.md"),
                first.stdout.index("docs/03.specs/200-z/spec.md"),
            )

    def test_report_output_check_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", None)
            output = root / "inventory.md"
            generated = run_checker(root, "report", "--output", str(output))
            fresh = run_checker(root, "report", "--output", str(output), "--check")
            output.write_text("stale\n", encoding="utf-8")
            stale = run_checker(root, "report", "--output", str(output), "--check")
            self.assertEqual(0, generated.returncode, generated.stderr)
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("metadata inventory is stale", stale.stderr)

    def test_active_mode_is_available_but_semantic_gate_is_not_auto_invoked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/123-example/spec.md", {"status": "active"})
            result = run_checker(root, "check-active")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("metadata check-active", result.stdout)

    def test_inventory_exposes_all_semantic_state_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", {"status": "active"})
            write_doc(
                root / "docs/90.references/data/generated.md",
                {"status": "active", "generated_by": "scripts/example.py"},
            )
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(
                "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
                result.stdout,
            )
            self.assertIn("allowed-syntax", result.stdout)
            self.assertIn(
                "README profile=stage-index; consumer=scripts/validation/check-document-metadata.py; role=folder-index",
                result.stdout,
            )
            self.assertIn("generated profile; owner=scripts/example.py", result.stdout)
            self.assertIn("reviewed_at=forbidden:not-applicable", result.stdout)

    def test_inventory_records_identity_relations_and_transition_evidence(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        parent = metadata.Record(
            pathlib.Path("docs/01.requirements/123-parent.md"),
            {"status": "active", "artifact_id": "PRD-123", "artifact_type": "prd", "parent_ids": []},
            "prd",
            frontmatter_present=True,
        )
        child = metadata.Record(
            pathlib.Path("docs/03.specs/123-child/spec.md"),
            {
                "status": "completed",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-123"],
            },
            "spec",
            previous_status="active",
            frontmatter_present=True,
        )
        records = [parent, child]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(record, profiles, manifest) for record in records
        }
        report = metadata.render_report(records, profiles, findings)
        child_row = next(line for line in report.splitlines() if "docs/03.specs/123-child/spec.md" in line)
        self.assertIn("| valid | parents=resolved:1; order=declared-list; supersedes=not-provided |", child_row)
        self.assertIn("available:active->completed; valid", child_row)


class ChangedPathGitTests(unittest.TestCase):
    def new_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        init_git(root)
        write_doc(root / "docs/03.specs/README.md", None)
        commit_all(root)
        return directory, root

    def assert_changed_failure(self, root: pathlib.Path, *extra: str) -> None:
        result = run_checker(root, "check-changed", *extra)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing-required-key", result.stdout)

    def assert_git_probe_failure(self, probe_name: str, expected_label: str) -> None:
        directory, root = self.new_repo()
        with directory:
            result = run_checker(
                root,
                "check-changed",
                env=failing_git_probe_env(root, probe_name),
            )
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn(expected_label, result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def write_parent_relation_fixture(self, root: pathlib.Path) -> pathlib.Path:
        parent = root / "docs/01.requirements/123-parent.md"
        write_doc(
            parent,
            {
                "status": "active",
                "artifact_id": "prd:123-parent",
                "artifact_type": "prd",
                "parent_ids": [],
            },
            PRD_TARGET_BODY,
        )
        write_doc(
            root / "docs/03.specs/123-child/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-child",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-parent"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        commit_all(root, "typed parent relation")
        return parent

    def write_supersedes_relation_fixture(self, root: pathlib.Path) -> pathlib.Path:
        write_doc(
            root / "docs/01.requirements/123-root.md",
            {
                "status": "active",
                "artifact_id": "prd:123-root",
                "artifact_type": "prd",
                "parent_ids": [],
            },
        )
        replaced = root / "docs/03.specs/123-replaced/spec.md"
        write_doc(
            replaced,
            {
                "status": "superseded",
                "artifact_id": "spec:123-replaced",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-root"],
            },
        )
        write_doc(
            root / "docs/03.specs/123-replacement/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-replacement",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-root"],
                "supersedes": ["spec:123-replaced"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        commit_all(root, "typed supersedes relation")
        return replaced

    def write_identity_change_supersedes_fixture(self, root: pathlib.Path) -> pathlib.Path:
        write_doc(
            root / "docs/01.requirements/123-identity-root.md",
            {
                "status": "active",
                "artifact_id": "prd:123-identity-root",
                "artifact_type": "prd",
                "parent_ids": [],
            },
        )
        target = root / "docs/03.specs/123-identity-target/spec.md"
        write_doc(
            target,
            {
                "status": "superseded",
                "artifact_id": "spec:123-identity-old",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
            },
        )
        write_doc(
            root / "docs/03.specs/123-old-id-dependent/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-old-id-dependent",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
                "supersedes": ["spec:123-identity-old"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        write_doc(
            root / "docs/03.specs/123-new-id-replacement/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-new-id-replacement",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
                "supersedes": ["spec:123-identity-new"],
            },
        )
        commit_all(root, "typed identity-change supersedes relation")
        return target

    def rewrite_artifact_identity(
        self,
        root: pathlib.Path,
        target: pathlib.Path,
        *,
        staged: bool,
    ) -> None:
        if target.as_posix().endswith("docs/01.requirements/123-parent.md"):
            values = {
                "status": "active",
                "artifact_id": "prd:123-parent-new",
                "artifact_type": "prd",
                "parent_ids": [],
            }
            body = PRD_TARGET_BODY
        else:
            values = {
                "status": "superseded",
                "artifact_id": "spec:123-identity-new",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
            }
            body = SPEC_TARGET_BODY
        write_doc(target, values, body)
        if staged:
            self.assertEqual(0, git(root, "add", target.relative_to(root).as_posix()).returncode)

    def assert_identity_change_failure(
        self,
        root: pathlib.Path,
        target: pathlib.Path,
        dependent: str,
        finding_code: str,
        *,
        staged: bool,
    ) -> None:
        self.rewrite_artifact_identity(root, target, staged=staged)
        result = run_checker(root, "check-changed")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{dependent}: {finding_code}", result.stdout)
        self.assertNotIn("invalid-reviewed-at", result.stdout)
        self.assertIn("selected=2 violations=1", result.stdout)

    def assert_relation_deletion_failure(
        self,
        root: pathlib.Path,
        deleted: pathlib.Path,
        dependent: str,
        finding_code: str,
        *,
        staged: bool,
    ) -> None:
        relative = deleted.relative_to(root).as_posix()
        if staged:
            self.assertEqual(0, git(root, "rm", relative).returncode)
        else:
            deleted.unlink()
        result = run_checker(root, "check-changed")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{dependent}: {finding_code}", result.stdout)
        self.assertNotIn("invalid-reviewed-at", result.stdout)
        self.assertIn("selected=2 violations=1", result.stdout)

    def test_untracked_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(root / "docs/03.specs/123-new/spec.md", {"status": "active"})
            self.assert_changed_failure(root)

    def test_failed_tracked_file_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("tracked", "tracked Markdown")

    def test_failed_unstaged_diff_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("unstaged", "unstaged Markdown")

    def test_failed_staged_diff_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("staged", "staged Markdown")

    def test_failed_untracked_file_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("untracked", "untracked Markdown")

    def test_non_git_root_fails_closed_without_success_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/123-new/spec.md", {"status": "active"})
            result = run_checker(root, "check-changed")
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("Git worktree", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def test_missing_git_executable_fails_closed_without_traceback(self) -> None:
        directory, root = self.new_repo()
        with directory:
            result = run_checker(root, "check-changed", env={"PATH": ""})
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("Git executable", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def test_non_utf8_markdown_path_in_explicit_base_is_sanitized(self) -> None:
        directory, root = self.new_repo()
        with directory:
            raw_directory = os.fsencode(root / "docs/03.specs")
            raw_path = raw_directory + b"/private-base-path-\xff.md"
            descriptor = os.open(raw_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(b"private-base-body\n")
            commit_all(root, "non-UTF-8 base path")
            base = git(root, "rev-parse", "HEAD").stdout.strip()

            readme = root / "docs/03.specs/README.md"
            readme.write_text("# Specifications\n\nOrdinary current change.\n", encoding="utf-8")
            commit_all(root, "ordinary current change")

            result = run_checker(root, "check-changed", "--base-ref", base)
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("base Markdown discovery returned a non-UTF-8 path", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)
            self.assertNotIn("private-base-path", combined)
            self.assertNotIn("private-base-body", combined)
            self.assertNotIn("fatal:", combined)

    def test_staged_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/123-new/spec.md"
            write_doc(path, {"status": "active"})
            self.assertEqual(0, git(root, "add", path.relative_to(root).as_posix()).returncode)
            self.assert_changed_failure(root)

    def test_modified_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/123-existing/spec.md"
            write_doc(
                path,
                {"status": "active", "artifact_id": "SPEC-123", "artifact_type": "spec", "parent_ids": []},
            )
            commit_all(root)
            write_doc(path, {"status": "active"})
            self.assert_changed_failure(root)

    def test_renamed_invalid_document_fails_at_new_path(self) -> None:
        directory, root = self.new_repo()
        with directory:
            source = root / "docs/03.specs/README.md"
            target = root / "docs/03.specs/123-renamed/spec.md"
            target.parent.mkdir(parents=True)
            self.assertEqual(0, git(root, "mv", source.relative_to(root).as_posix(), target.relative_to(root).as_posix()).returncode)
            self.assert_changed_failure(root)

    def test_deleted_document_is_not_parsed_as_violation(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/01.requirements/123-deleted.md"
            write_doc(
                path,
                {
                    "status": "active",
                    "artifact_id": "prd:123-deleted",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root)
            path.unlink()
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=1 violations=0", result.stdout)

    def test_staged_deleted_document_is_retained_as_nonviolating_evidence(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/01.requirements/123-staged-deleted.md"
            write_doc(
                path,
                {
                    "status": "active",
                    "artifact_id": "prd:123-staged-deleted",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root)
            self.assertEqual(0, git(root, "rm", path.relative_to(root).as_posix()).returncode)
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=1 violations=0", result.stdout)

    def test_unstaged_parent_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_parent_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=False,
            )

    def test_staged_parent_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_parent_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=True,
            )

    def test_unstaged_supersedes_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_supersedes_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-replacement/spec.md",
                "unresolved-supersedes",
                staged=False,
            )

    def test_staged_supersedes_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_supersedes_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-replacement/spec.md",
                "unresolved-supersedes",
                staged=True,
            )

    def test_staged_typed_parent_rename_keeps_relation_resolved(self) -> None:
        directory, root = self.new_repo()
        with directory:
            source = self.write_parent_relation_fixture(root)
            target = root / "docs/01.requirements/123-parent-renamed.md"
            self.assertEqual(
                0,
                git(root, "mv", source.relative_to(root).as_posix(), target.relative_to(root).as_posix()).returncode,
            )
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("violations=0", result.stdout)

    def test_unstaged_parent_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=False,
            )

    def test_staged_parent_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=True,
            )

    def test_unstaged_supersedes_target_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_identity_change_supersedes_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-old-id-dependent/spec.md",
                "unresolved-supersedes",
                staged=False,
            )

    def test_staged_supersedes_target_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_identity_change_supersedes_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-old-id-dependent/spec.md",
                "unresolved-supersedes",
                staged=True,
            )

    def test_coherent_parent_id_change_updates_dependent_relation(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.rewrite_artifact_identity(root, target, staged=False)
            write_doc(
                root / "docs/03.specs/123-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:123-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:123-parent-new"],
                },
            )
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=2 violations=0", result.stdout)

    def test_explicit_untracked_path_is_parsed(self) -> None:
        directory, root = self.new_repo()
        with directory:
            relative = "docs/03.specs/123-explicit/spec.md"
            write_doc(root / relative, {"status": "active"})
            self.assert_changed_failure(root, "--changed-path", relative)


class ChangedBodyDeficitGitTests(unittest.TestCase):
    PATH = "docs/01.requirements/901-body-deficit.md"
    METADATA = {
        "status": "draft",
        "artifact_id": "prd:901-body-deficit",
        "artifact_type": "prd",
        "parent_ids": [],
    }

    def new_repo_with_body(
        self,
        body: str,
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        init_git(root)
        write_doc(root / self.PATH, self.METADATA, body)
        commit_all(root, "body-deficit baseline")
        base = git(root, "rev-parse", "HEAD").stdout.strip()
        return directory, root, base

    def run_explicit_base(
        self,
        root: pathlib.Path,
        base: str,
    ) -> subprocess.CompletedProcess[str]:
        return run_checker(root, "check-changed", "--base-ref", base)

    def test_identical_base_body_deficit_multiset_is_preserved(self) -> None:
        body = PRD_TARGET_BODY + "\n{{existing_token}}\n"
        directory, root, base = self.new_repo_with_body(body)
        with directory:
            write_doc(root / self.PATH, self.METADATA, body + "\nEditorial text.\n")
            result = self.run_explicit_base(root, base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("violations=0", result.stdout)

    def test_additional_same_class_body_deficit_is_blocked_without_value_leakage(self) -> None:
        base_body = PRD_TARGET_BODY + "\n{{existing_token}}\n"
        directory, root, base = self.new_repo_with_body(base_body)
        with directory:
            write_doc(
                root / self.PATH,
                self.METADATA,
                base_body + "\n{{additional_token}}\n",
            )
            result = self.run_explicit_base(root, base)
            combined = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, combined)
            self.assertIn("template-body-token-in-target", result.stdout)
            self.assertNotIn("existing_token", combined)
            self.assertNotIn("additional_token", combined)

    def test_different_same_count_body_deficit_is_blocked_without_value_leakage(self) -> None:
        directory, root, base = self.new_repo_with_body(
            PRD_TARGET_BODY + "\n{{original_token}}\n"
        )
        with directory:
            write_doc(
                root / self.PATH,
                self.METADATA,
                PRD_TARGET_BODY + "\n{{replacement_token}}\n",
            )
            result = self.run_explicit_base(root, base)
            combined = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, combined)
            self.assertIn("template-body-token-in-target", result.stdout)
            self.assertNotIn("original_token", combined)
            self.assertNotIn("replacement_token", combined)

    def test_new_instruction_literal_is_blocked_without_literal_echo(self) -> None:
        directory, root, base = self.new_repo_with_body(PRD_TARGET_BODY)
        with directory:
            write_doc(root / self.PATH, self.METADATA, PRD_TARGET_BODY + "\n> Rules:\n")
            result = self.run_explicit_base(root, base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("template-instruction-in-target", result.stdout)
            self.assertNotIn("> Rules:", result.stdout)

    def test_new_file_body_deficit_is_blocked(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        with directory:
            init_git(root)
            write_doc(root / "docs/03.specs/README.md", None)
            commit_all(root, "empty body-gate baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                root / self.PATH,
                self.METADATA,
                PRD_TARGET_BODY + "\n{{new_file_token}}\n",
            )
            result = self.run_explicit_base(root, base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("template-body-token-in-target", result.stdout)

    def test_preserved_body_deficit_does_not_suppress_relation_impact(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        with directory:
            init_git(root)
            parent = root / self.PATH
            write_doc(
                parent,
                self.METADATA,
                PRD_TARGET_BODY + "\n{{existing_token}}\n",
            )
            child = root / "docs/03.specs/901-body-child/spec.md"
            write_doc(
                child,
                {
                    "status": "draft",
                    "artifact_id": "spec:901-body-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:901-body-deficit"],
                },
                SPEC_TARGET_BODY,
            )
            commit_all(root, "body and relation baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                parent,
                {**self.METADATA, "artifact_id": "prd:901-renamed"},
                PRD_TARGET_BODY + "\n{{existing_token}}\n",
            )
            result = self.run_explicit_base(root, base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"{child.relative_to(root).as_posix()}: unresolved-parent", result.stdout)
            self.assertNotIn("template-body-token-in-target", result.stdout)

    def test_changed_checker_ignores_residue_inside_commonmark_code(self) -> None:
        cases = (
            (
                "backtick fence",
                "```markdown title=\"~example~\"\n> Rules:\n{{fenced_token}}\n```\n",
            ),
            (
                "tilde fence",
                "~~~markdown title=\"`example` ~draft~\"\n> Rules:\n{{fenced_token}}\n~~~\n",
            ),
            (
                "unclosed backtick fence",
                "```markdown title=\"~example~\"\n> Rules:\n{{fenced_token}}\n",
            ),
            (
                "unclosed tilde fence",
                "~~~markdown title=\"`example`\"\n> Rules:\n{{fenced_token}}\n",
            ),
            (
                "single and multi backtick spans",
                "Document `> Rules:` and `{{single_token}}`.\n"
                "Document `` `> Rules:` and `{{multi_token}}` ``.\n",
            ),
        )
        for label, example in cases:
            with self.subTest(case=label):
                directory, root, base = self.new_repo_with_body(PRD_TARGET_BODY)
                with directory:
                    write_doc(root / self.PATH, self.METADATA, PRD_TARGET_BODY + "\n" + example)
                    result = self.run_explicit_base(root, base)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_changed_checker_rejects_genuine_residue_outside_code(self) -> None:
        directory, root, base = self.new_repo_with_body(PRD_TARGET_BODY)
        with directory:
            body = (
                PRD_TARGET_BODY
                + "\n```markdown title=\"~example~\"\n{{fenced_token}}\n```\n"
                + "Document `` `{{inline_token}}` ``.\n"
                + "{{outside_token}}\n"
            )
            write_doc(root / self.PATH, self.METADATA, body)
            result = self.run_explicit_base(root, base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("template-body-token-in-target", result.stdout)


class ChangedModeRolloutTests(unittest.TestCase):
    def new_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        init_git(root)
        self.assertEqual(0, git(root, "branch", "-M", "main").returncode)
        write_doc(root / "docs/03.specs/README.md", None)
        commit_all(root, "base")
        return directory, root

    def test_committed_new_invalid_document_is_blocked_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid new doc")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("missing-required-key", result.stdout)
            self.assertIn(f"metadata base: source=explicit ref={base}", result.stderr)

    def test_changed_legacy_document_outside_migration_scope_is_explicitly_excepted(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"}, "# Legacy\n")
            commit_all(root, "legacy baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active"}, "# Legacy\n\nEditorial correction.\n")
            commit_all(root, "edit legacy doc")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=1", result.stdout)
            self.assertIn("legacy metadata exception", result.stderr)

    def test_partial_typed_migration_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active", "artifact_id": "spec:partial"})
            commit_all(root, "partial migration")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("missing-required-key", result.stdout)

    def test_new_stale_active_deficit_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/05.operations/policies/00-workspace/legacy.md"
            write_doc(path, {"status": "draft"})
            commit_all(root, "legacy draft policy")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active"})
            commit_all(root, "activate legacy policy")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("stale-active", result.stdout)

    def test_new_replacement_free_deficit_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy active spec")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "superseded"})
            commit_all(root, "supersede without replacement")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("replacement-free-supersession", result.stdout)

    def test_disappearing_legacy_deficit_remains_eligible(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/05.operations/policies/00-workspace/legacy.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy active policy")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "completed"})
            commit_all(root, "complete legacy policy")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=1", result.stdout)

    def test_committed_valid_parent_chain_passes_and_is_selected(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                root / "docs/01.requirements/124-parent.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
                PRD_TARGET_BODY,
            )
            write_doc(
                root / "docs/03.specs/124-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                },
                SPEC_TARGET_BODY,
            )
            commit_all(root, "valid typed chain")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=2", result.stdout)
            self.assertIn("violations=0", result.stdout)

    def test_committed_parent_deletion_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/01.requirements/124-parent.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            commit_all(root, "typed parent chain")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            self.assertEqual(0, git(root, "rm", parent.relative_to(root).as_posix()).returncode)
            commit_all(root, "delete typed parent")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-child/spec.md: unresolved-parent",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_parent_id_change_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/01.requirements/124-identity-parent.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-old",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-identity-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-identity-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-old"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            commit_all(root, "typed parent identity baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-new",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root, "change typed parent identity")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-identity-child/spec.md: unresolved-parent",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_supersedes_target_id_change_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(
                root / "docs/01.requirements/124-identity-root.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-root",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            target = root / "docs/03.specs/124-identity-target/spec.md"
            write_doc(
                target,
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-identity-old",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                },
            )
            write_doc(
                root / "docs/03.specs/124-old-id-dependent/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-old-id-dependent",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                    "supersedes": ["spec:124-identity-old"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            write_doc(
                root / "docs/03.specs/124-new-id-replacement/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-new-id-replacement",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                    "supersedes": ["spec:124-identity-new"],
                },
            )
            commit_all(root, "typed supersedes identity baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                target,
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-identity-new",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                },
            )
            commit_all(root, "change typed supersedes target identity")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-old-id-dependent/spec.md: unresolved-supersedes",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_replacement_free_superseded_document_is_blocked(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                root / "docs/01.requirements/124-parent.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-old/spec.md",
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-old",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                },
            )
            commit_all(root, "replacement-free supersession")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("replacement-free-supersession", result.stdout)

    def test_reverse_transition_without_override_is_blocked(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(
                root / "docs/03.specs/124-parent/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent-root"],
                },
            )
            write_doc(
                root / "docs/03.specs/124-parent-root/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent-root",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent-root"],
                },
            )
            task = root / "docs/04.execution/tasks/2026-07-11-transition.md"
            write_doc(
                task,
                {
                    "status": "completed",
                    "artifact_id": "task:transition",
                    "artifact_type": "task",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            commit_all(root, "completed task")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                task,
                {
                    "status": "active",
                    "artifact_id": "task:transition",
                    "artifact_type": "task",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            commit_all(root, "reverse task transition")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("invalid-transition", result.stdout)

    def test_scoped_transition_override_requires_complete_stage04_evidence(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/03.specs/124-parent/spec.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            task = root / "docs/04.execution/tasks/2026-07-11-transition.md"
            values = {
                "status": "completed",
                "artifact_id": "task:transition",
                "artifact_type": "task",
                "parent_ids": ["spec:124-parent"],
            }
            write_doc(task, values)
            evidence = root / "docs/04.execution/tasks/2026-07-11-transition-approval.md"
            write_doc(evidence, {"status": "active"}, "# Task: Transition Approval\n")
            commit_all(root, "completed task and evidence")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(task, {**values, "status": "active"})
            commit_all(root, "approved reverse transition")
            override = root / "override.yaml"
            override.write_text(
                yaml.safe_dump(
                    {
                        "transition_overrides": [
                            {
                                "path": task.relative_to(root).as_posix(),
                                "previous_status": "completed",
                                "new_status": "active",
                                "evidence_task": evidence.relative_to(root).as_posix(),
                                "approval": "Spec 123 Task 8 fixture approval",
                                "reason": "Reopened to correct incomplete evidence",
                            }
                        ]
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            result = run_checker(
                root,
                "check-changed",
                "--base-ref",
                base,
                "--transition-override-file",
                str(override),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("transition_overrides=1", result.stdout)

    def test_environment_base_is_used_before_local_candidates(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid branch doc")
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": base, "GITHUB_BASE_REF": "does-not-exist"},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("source=env:TEMPLATE_GATE_BASE", result.stderr)

    def test_invalid_explicit_base_is_a_configuration_error_without_fallback(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            result = run_checker(root, "check-changed", "--base-ref", "missing-ref")
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("explicit --base-ref is not a commit", result.stderr)
            self.assertNotIn("fallback=working-tree-only", result.stderr)

    def test_local_main_base_selects_committed_branch_delta(self) -> None:
        directory, root = self.new_repo()
        with directory:
            self.assertEqual(0, git(root, "switch", "-qc", "feature").returncode)
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid branch doc")
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": "", "GITHUB_BASE_REF": ""},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("source=local:main", result.stderr)

    def test_missing_base_falls_back_to_local_delta_without_whole_repo_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            write_doc(root / "docs/03.specs/README.md", None)
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": "", "GITHUB_BASE_REF": ""},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("metadata base: fallback=working-tree-only", result.stderr)
            self.assertIn("selected=2", result.stdout)


if __name__ == "__main__":
    unittest.main()
