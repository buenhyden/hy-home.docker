from __future__ import annotations

import contextlib
import importlib.util
import hashlib
import io
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/validation/target_surface_delta_contract.py"
MANIFEST_PATH = (
    ROOT
    / "docs/90.references/data/governance/target-surface-delta-manifest.yaml"
)
SUMMARY_PATH = MANIFEST_PATH.with_name("target-surface-delta-summary.md")
METADATA_CHECKER = ROOT / "scripts/validation/check-document-metadata.py"
PROFILE_REGISTRY = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
PREDECESSOR_CLOSURE = "63039b5b0b20c99a10aae7162627afefcd7a1d8b"
IMPLEMENTATION_BASE = "19ee47270e3897073ab9a3f86dfd4cce0f4b2e74"
TASK_START = "72eef68cd0691a84e8ce80548f205de4fe964238"
TARGET_ROOTS = (
    ".github",
    "archive",
    "examples",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
)
PRE_TASK2_UPDATE_PATHS = frozenset(
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
TASK2_UPDATE_PATHS = frozenset(
    {
        "examples/sample-web-service/service.md",
        "infra/01-gateway/nginx/README.md",
        "infra/01-gateway/traefik/README.md",
        "infra/02-auth/README.md",
        "infra/02-auth/keycloak/README.md",
        "infra/02-auth/oauth2-proxy/README.md",
        "infra/03-security/README.md",
        "infra/03-security/vault/README.md",
        "infra/04-data/README.md",
        "infra/04-data/analytics/README.md",
        "infra/04-data/analytics/influxdb/README.md",
        "infra/04-data/analytics/ksql/README.md",
        "infra/04-data/analytics/opensearch/README.md",
        "infra/04-data/analytics/warehouses/README.md",
        "infra/05-messaging/README.md",
        "infra/05-messaging/kafka/README.md",
        "infra/05-messaging/rabbitmq/README.md",
        "infra/06-observability/README.md",
        "infra/06-observability/alertmanager/README.md",
        "infra/06-observability/alloy/README.md",
        "infra/06-observability/prometheus/README.md",
        "infra/06-observability/pushgateway/README.md",
        "infra/06-observability/pyroscope/README.md",
        "infra/06-observability/tempo/README.md",
        "infra/07-workflow/README.md",
        "infra/07-workflow/airflow/README.md",
        "infra/07-workflow/n8n/README.md",
        "infra/08-ai/README.md",
        "infra/09-tooling/README.md",
        "infra/README.md",
        "scripts/validation/check-document-corpus-lifecycle.py",
        "scripts/validation/check-document-metadata.py",
        "scripts/validation/target_surface_contract.py",
        "secrets/README.md",
        "tests/validation/test_document_corpus_lifecycle.py",
        "tests/validation/test_document_metadata.py",
        "tests/validation/test_target_surface_contracts.py",
        "tests/validation/test_target_surface_delta_contracts.py",
    }
)
TASK3_UPDATE_PATHS = frozenset(
    {
        "infra/01-gateway/README.md",
        "infra/tech-stack.versions.json",
        "scripts/hardening/check-all-hardening.sh",
        "tests/validation/test_tech_stack_version_contract.py",
    }
)
EXPECTED_UPDATE_PATHS = (
    PRE_TASK2_UPDATE_PATHS | TASK2_UPDATE_PATHS | TASK3_UPDATE_PATHS
)


def load_contract_module():
    spec = importlib.util.spec_from_file_location(
        "target_surface_delta_contract_under_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load delta contract: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_metadata_module():
    spec = importlib.util.spec_from_file_location(
        "target_surface_delta_metadata_under_test",
        METADATA_CHECKER,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load metadata checker: {METADATA_CHECKER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(root: pathlib.Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def write_text(root: pathlib.Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def valid_row(
    path: str,
    *,
    changed_since: str,
    disposition: str = "preserve",
    evidence_head: str | None = None,
) -> dict[str, object]:
    suffix = pathlib.PurePosixPath(path).suffix.lower()
    if path.endswith("README.md"):
        surface_class = "readme"
    elif path.startswith(".github/"):
        surface_class = "native-platform"
    elif path.startswith("tests/"):
        surface_class = "test-or-fixture"
    elif suffix == ".sh":
        surface_class = "executable-script"
    elif suffix == ".py":
        surface_class = "python-source"
    elif suffix in {".json", ".yaml", ".yml", ".example"}:
        surface_class = "native-configuration"
    else:
        surface_class = "native-file"
    secret_safety = "path-only" if path.startswith("secrets/") else "not-applicable"
    profile = "infrastructure-root" if path == "infra/README.md" else None
    replacement: str | None = None
    direct_consumers: list[str] = []
    validators: list[str] = []
    tests: list[str] = []
    provenance: list[str] = []
    rollback: list[str] = []
    spec_verdict = "pending"
    quality_verdict = "pending"
    if disposition in {"migrate", "delete"}:
        if evidence_head is None:
            raise ValueError("destructive rows require an evidence head")
        direct_consumers = ["docs/03.specs/135-target-surface-delta-convergence/spec.md"]
        replacement = (
            "withdrawn" if disposition == "delete" else "infra/replacement.txt"
        )
        validators = ["scripts/validation/check-target-surface-delta-contract.py"]
        tests = ["tests/validation/test_target_surface_delta_contracts.py"]
        provenance = [f"git:{changed_since}..{evidence_head}:{path}"]
        rollback = [f"git-revert:{evidence_head}:{path}"]
        spec_verdict = "pass"
        quality_verdict = "pass"
    return {
        "path": path,
        "surface_class": surface_class,
        "profile": profile,
        "changed_since": changed_since,
        "disposition": disposition,
        "canonical_owner": (
            "docs/03.specs/135-target-surface-delta-convergence/spec.md"
        ),
        "direct_consumers": direct_consumers,
        "finding": "Classified successor delta path.",
        "replacement": replacement,
        "secret_safety": secret_safety,
        "validators": validators,
        "tests": tests,
        "provenance": provenance,
        "rollback": rollback,
        "spec_verdict": spec_verdict,
        "quality_verdict": quality_verdict,
    }


def valid_document(
    predecessor: str,
    implementation_base: str,
    entries: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "predecessor_closure": predecessor,
        "implementation_base": implementation_base,
        "enforcement": "advisory",
        "target_roots": list(TARGET_ROOTS),
        "entries": entries,
    }


class TemporaryDeltaRepository:
    def __init__(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.directory.name)

    def __enter__(self) -> TemporaryDeltaRepository:
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Delta Contract Test")
        git(self.root, "config", "user.email", "delta@example.invalid")
        baseline = {
            ".github/workflows/ci.yml": "name: CI\n",
            "archive/note.md": "# Archived note\n",
            "docs/03.specs/135-target-surface-delta-convergence/spec.md": (
                "# Target Surface Delta Convergence\n"
            ),
            "docs/99.templates/support/document-metadata-profiles.yaml": (
                "readme_profiles:\n"
                "  infrastructure-root:\n"
                "    path_globs: [infra/README.md]\n"
            ),
            "examples/sample/service.md": "# Service fixture\n",
            "infra/README.md": "# Infrastructure\n",
            "infra/replacement.txt": "canonical replacement\n",
            "projects/app/config.json": "{}\n",
            "scripts/tool.sh": "#!/usr/bin/env bash\n",
            "scripts/validation/check-target-surface-delta-contract.py": (
                "#!/usr/bin/env python3\n"
            ),
            "secrets/example.env.example": "PASSWORD=SUPER_SECRET_VALUE\n",
            "tests/test_sample.py": "def test_sample():\n    assert True\n",
            "tests/validation/test_target_surface_delta_contracts.py": (
                "def test_contract():\n    assert True\n"
            ),
        }
        for path, text in baseline.items():
            write_text(self.root, path, text)
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "baseline")
        self.predecessor = git(self.root, "rev-parse", "HEAD")

        write_text(self.root, "infra/README.md", "# Current infrastructure\n")
        git(self.root, "add", "infra/README.md")
        git(self.root, "commit", "-qm", "committed target change")
        self.implementation_base = git(self.root, "rev-parse", "HEAD")

        write_text(
            self.root,
            "tests/test_delta.py",
            "def test_delta():\n    assert True\n",
        )
        git(self.root, "add", "tests/test_delta.py")
        write_text(
            self.root,
            "scripts/tool.sh",
            "#!/usr/bin/env bash\nset -euo pipefail\n",
        )
        write_text(
            self.root,
            ".github/untracked.yml",
            "name: untracked target evidence\n",
        )
        return self

    def __exit__(self, *_args: object) -> None:
        self.directory.cleanup()

    @property
    def changed_paths(self) -> tuple[str, ...]:
        return (
            ".github/untracked.yml",
            "infra/README.md",
            "scripts/tool.sh",
            "tests/test_delta.py",
        )

    def write_manifest(
        self,
        document: dict[str, object],
        relative: str = MANIFEST_PATH.relative_to(ROOT).as_posix(),
    ) -> pathlib.Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        return path


class ManifestReaderTests(unittest.TestCase):
    def test_duplicate_yaml_keys_are_rejected_without_values(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            manifest = fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    [
                        valid_row(
                            path,
                            changed_since=fixture.predecessor,
                        )
                        for path in fixture.changed_paths
                    ],
                )
            )
            source = manifest.read_text(encoding="utf-8")
            manifest.write_text(
                source.replace(
                    "schema_version: 1\n",
                    "schema_version: 1\nschema_version: 1\n",
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(contract.ContractInputError) as caught:
                contract.load_delta_manifest(fixture.root)
            self.assertNotIn("schema_version", str(caught.exception))

    def test_unknown_fields_are_rejected(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            document = valid_document(
                fixture.predecessor,
                fixture.implementation_base,
                [
                    valid_row(
                        path,
                        changed_since=fixture.predecessor,
                    )
                    for path in fixture.changed_paths
                ],
            )
            document["unexpected"] = "must-not-be-admitted"
            fixture.write_manifest(document)
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)

    def test_unknown_row_fields_are_rejected(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            row = valid_row(
                fixture.changed_paths[0],
                changed_since=fixture.predecessor,
            )
            row["unexpected"] = "must-not-be-admitted"
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    [row],
                )
            )
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)

    def test_noncanonical_paths_are_rejected(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            row = valid_row(
                "../secrets/private.env",
                changed_since=fixture.predecessor,
            )
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    [row],
                )
            )
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)

    def test_control_and_markdown_injection_paths_are_rejected(self) -> None:
        contract = load_contract_module()
        unsafe_paths = (
            "infra/table|escape.md",
            "infra/inline`escape.md",
            "infra/tab\tescape.md",
            "infra/cr\rescape.md",
            "infra/line\nescape.md",
            "infra/nul\0escape.md",
        )
        with TemporaryDeltaRepository() as fixture:
            for unsafe_path in unsafe_paths:
                with self.subTest(path=repr(unsafe_path)):
                    row = valid_row(
                        unsafe_path,
                        changed_since=fixture.predecessor,
                    )
                    fixture.write_manifest(
                        valid_document(
                            fixture.predecessor,
                            fixture.implementation_base,
                            [row],
                        )
                    )
                    with self.assertRaises(contract.ContractInputError):
                        contract.load_delta_manifest(fixture.root)

    def test_oversized_and_symlinked_manifest_inputs_are_rejected(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            manifest = fixture.root / MANIFEST_PATH.relative_to(ROOT)
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_bytes(b"x" * (contract.MAX_CONTRACT_FILE_BYTES + 1))
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)
            manifest.unlink()
            manifest.symlink_to(fixture.root / "infra/README.md")
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)


class DeltaCoverageTests(unittest.TestCase):
    def test_untracked_target_path_is_included_separately(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            untracked = ".github/untracked.yml"
            result = subprocess.run(
                ["git", "ls-files", "--error-unmatch", "--", untracked],
                cwd=fixture.root,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                f"?? {untracked}",
                git(fixture.root, "status", "--short", "--untracked-files=all"),
            )
            self.assertIn(
                untracked,
                contract.changed_target_paths(
                    fixture.root,
                    fixture.predecessor,
                ),
            )

    def test_every_changed_target_path_has_exactly_one_row(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            self.assertEqual(
                fixture.changed_paths,
                contract.changed_target_paths(
                    fixture.root,
                    fixture.predecessor,
                ),
            )
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    [
                        valid_row(
                            path,
                            changed_since=fixture.predecessor,
                        )
                        for path in fixture.changed_paths
                    ],
                )
            )
            document = contract.load_delta_manifest(fixture.root)
            self.assertEqual((), contract.validate_delta_manifest(fixture.root, document))

    def test_missing_root_wrong_baseline_invalid_disposition_and_ordering(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            entries = [
                valid_row(
                    fixture.changed_paths[0],
                    changed_since=fixture.predecessor,
                ),
                valid_row(
                    fixture.changed_paths[1],
                    changed_since=fixture.predecessor,
                ),
            ]
            entries[0]["disposition"] = "retire"
            entries[1]["changed_since"] = "0" * 40
            document = valid_document(
                "1" * 40,
                fixture.implementation_base,
                entries,
            )
            document["target_roots"] = list(TARGET_ROOTS[:-1])
            fixture.write_manifest(document)
            loaded = contract.load_delta_manifest(fixture.root)
            findings = contract.validate_delta_manifest(fixture.root, loaded)
            self.assertEqual(tuple(sorted(findings)), findings)
            codes = {finding.code for finding in findings}
            self.assertTrue(
                {
                    "delta-baseline-invalid",
                    "delta-changed-since-invalid",
                    "delta-disposition-invalid",
                    "delta-git-delta-invalid",
                    "delta-target-roots-invalid",
                }
                <= codes
            )

    def test_duplicate_rows_are_rejected(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            row = valid_row(
                fixture.changed_paths[0],
                changed_since=fixture.predecessor,
            )
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    [row, dict(row)],
                )
            )
            with self.assertRaises(contract.ContractInputError):
                contract.load_delta_manifest(fixture.root)


class DestructiveDispositionTests(unittest.TestCase):
    def test_migrate_and_delete_require_complete_evidence(self) -> None:
        contract = load_contract_module()
        required_codes = {
            "delta-destructive-consumers-missing",
            "delta-destructive-provenance-missing",
            "delta-destructive-replacement-missing",
            "delta-destructive-review-invalid",
            "delta-destructive-rollback-missing",
            "delta-destructive-tests-missing",
            "delta-destructive-validators-missing",
        }
        for disposition in ("migrate", "delete"):
            with self.subTest(disposition=disposition):
                with TemporaryDeltaRepository() as fixture:
                    rows = [
                        valid_row(
                            path,
                            changed_since=fixture.predecessor,
                        )
                        for path in fixture.changed_paths
                    ]
                    row = rows[0]
                    row["disposition"] = disposition
                    row["direct_consumers"] = []
                    row["replacement"] = None
                    row["provenance"] = []
                    row["rollback"] = []
                    row["tests"] = []
                    row["spec_verdict"] = "pending"
                    row["quality_verdict"] = "pending"
                    fixture.write_manifest(
                        valid_document(
                            fixture.predecessor,
                            fixture.implementation_base,
                            rows,
                        )
                    )
                    document = contract.load_delta_manifest(fixture.root)
                    findings = contract.validate_delta_manifest(
                        fixture.root,
                        document,
                    )
                    self.assertTrue(
                        required_codes <= {finding.code for finding in findings}
                    )

    def test_migrate_and_delete_accept_only_complete_path_bound_evidence(self) -> None:
        contract = load_contract_module()
        for disposition, replacement in (
            ("migrate", "infra/replacement.txt"),
            ("delete", "withdrawn"),
            ("delete", "infra/replacement.txt"),
        ):
            with self.subTest(disposition=disposition, replacement=replacement):
                with TemporaryDeltaRepository() as fixture:
                    rows = [
                        valid_row(
                            path,
                            changed_since=fixture.predecessor,
                            disposition=(
                                disposition if path == "infra/README.md" else "preserve"
                            ),
                            evidence_head=(
                                fixture.implementation_base
                                if path == "infra/README.md"
                                else None
                            ),
                        )
                        for path in fixture.changed_paths
                    ]
                    destructive = next(
                        row for row in rows if row["path"] == "infra/README.md"
                    )
                    destructive["replacement"] = replacement
                    fixture.write_manifest(
                        valid_document(
                            fixture.predecessor,
                            fixture.implementation_base,
                            rows,
                        )
                    )
                    document = contract.load_delta_manifest(fixture.root)
                    self.assertEqual(
                        (),
                        contract.validate_delta_manifest(fixture.root, document),
                    )

    def test_disposition_and_evidence_semantics_fail_closed(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            rows[0]["replacement"] = "infra/replacement.txt"
            destructive = next(
                row for row in rows if row["path"] == "infra/README.md"
            )
            destructive.update(
                valid_row(
                    "infra/README.md",
                    changed_since=fixture.predecessor,
                    disposition="migrate",
                    evidence_head=fixture.implementation_base,
                )
            )
            destructive["canonical_owner"] = "projects/missing-owner.md"
            destructive["direct_consumers"] = ["projects/missing-consumer.md"]
            destructive["replacement"] = "infra/README.md"
            destructive["validators"] = ["scripts/tool.sh"]
            destructive["tests"] = ["scripts/tool.sh"]
            destructive["provenance"] = [
                (
                    f"git:{fixture.predecessor}..{fixture.implementation_base}:"
                    "scripts/tool.sh"
                )
            ]
            destructive["rollback"] = [
                f"git-revert:{fixture.implementation_base}:scripts/tool.sh"
            ]
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    rows,
                )
            )
            document = contract.load_delta_manifest(fixture.root)
            codes = {
                finding.code
                for finding in contract.validate_delta_manifest(
                    fixture.root,
                    document,
                )
            }
            self.assertTrue(
                {
                    "delta-consumer-invalid",
                    "delta-destructive-provenance-invalid",
                    "delta-destructive-rollback-invalid",
                    "delta-destructive-tests-invalid",
                    "delta-destructive-validators-invalid",
                    "delta-migrate-replacement-invalid",
                    "delta-nondestructive-replacement-invalid",
                    "delta-owner-invalid",
                }
                <= codes
            )


class SummaryWriterSafetyTests(unittest.TestCase):
    def test_summary_overwrite_refuses_symlink(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            summary = fixture.root / contract.DELTA_SUMMARY
            summary.parent.mkdir(parents=True, exist_ok=True)
            victim = fixture.root / "victim.md"
            victim.write_text("victim\n", encoding="utf-8")
            summary.symlink_to(victim)
            with self.assertRaises(contract.ContractInputError):
                contract._write_summary(fixture.root, "replacement\n")
            self.assertEqual("victim\n", victim.read_text(encoding="utf-8"))

    def test_summary_overwrite_detects_directory_entry_swap(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            summary = fixture.root / contract.DELTA_SUMMARY
            summary.parent.mkdir(parents=True, exist_ok=True)
            summary.write_text("old\n", encoding="utf-8")
            replacement = summary.with_suffix(".swap")
            replacement.write_text("swapped\n", encoding="utf-8")

            def swap_entry(_descriptor: int) -> None:
                summary.unlink()
                replacement.replace(summary)

            with mock.patch.object(contract.os, "fsync", side_effect=swap_entry):
                with self.assertRaises(contract.ContractInputError):
                    contract._write_summary(fixture.root, "new\n")
            self.assertEqual("swapped\n", summary.read_text(encoding="utf-8"))


class FailClosedInputTests(unittest.TestCase):
    def test_unknown_surface_class_is_value_free_and_refuses_summary_write(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            rows[0]["surface_class"] = "unregistered-surface-class"
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    rows,
                )
            )
            summary = fixture.root / contract.DELTA_SUMMARY
            summary.parent.mkdir(parents=True, exist_ok=True)
            summary.write_text("sentinel\n", encoding="utf-8")

            loaded = contract.load_delta_manifest(fixture.root)
            findings = contract.validate_delta_manifest(fixture.root, loaded)
            self.assertIn(
                "delta-surface-class-invalid",
                {finding.code for finding in findings},
            )
            self.assertNotIn("unregistered-surface-class", repr(findings))

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = contract.main(
                    [
                        "--root",
                        str(fixture.root),
                        "--write-summary",
                    ]
                )
            self.assertEqual(1, result)
            self.assertEqual("sentinel\n", summary.read_text(encoding="utf-8"))
            self.assertNotIn("unregistered-surface-class", stderr.getvalue())

    def test_readme_registry_missing_or_invalid_is_one_value_free_finding(self) -> None:
        contract = load_contract_module()
        registry_relative = contract.PROFILE_REGISTRY.as_posix()
        invalid_sources = (
            None,
            "readme_profiles: []\n",
            (
                "readme_profiles:\n"
                "  infrastructure-root:\n"
                "    path_globs: [infra/README.md]\n"
                "  infrastructure-root:\n"
                "    path_globs: [infra/OTHER.md]\n"
            ),
            (
                "readme_profiles:\n"
                "  infrastructure-root:\n"
                "    path_globs: ['infra/README.md|PASSWORD=SECRET']\n"
            ),
            (
                "readme_profiles:\n"
                "  'PASSWORD=SECRET':\n"
                "    path_globs: [infra/README.md]\n"
            ),
        )
        for invalid_source in invalid_sources:
            with self.subTest(source=invalid_source):
                with TemporaryDeltaRepository() as fixture:
                    rows = [
                        valid_row(path, changed_since=fixture.predecessor)
                        for path in fixture.changed_paths
                    ]
                    fixture.write_manifest(
                        valid_document(
                            fixture.predecessor,
                            fixture.implementation_base,
                            rows,
                        )
                    )
                    registry = fixture.root / registry_relative
                    if invalid_source is None:
                        registry.unlink()
                    else:
                        registry.write_text(invalid_source, encoding="utf-8")
                    document = contract.load_delta_manifest(fixture.root)
                    findings = contract.validate_delta_manifest(
                        fixture.root,
                        document,
                    )
                    registry_findings = [
                        finding
                        for finding in findings
                        if finding.code == "delta-readme-registry-invalid"
                    ]
                    self.assertEqual(1, len(registry_findings))
                    self.assertEqual(registry_findings, list(findings))
                    self.assertNotIn("PASSWORD=SECRET", repr(findings))

    def test_secret_like_values_are_rejected_before_diagnostics_or_summary(
        self,
    ) -> None:
        contract = load_contract_module()
        row_mutations = {
            "path": "infra/PASSWORD=SUPER_SECRET_PATH",
            "surface_class": "api_key=SUPER_SECRET_CLASS",
            "profile": "access_token=SUPER_SECRET_PROFILE",
            "changed_since": "client_secret=SUPER_SECRET_BASELINE",
            "disposition": "authorization: Bearer SUPER_SECRET_MODE",
            "canonical_owner": "infra/token=SUPER_SECRET_OWNER",
            "finding": "PASSWORD=SUPER_SECRET_RATIONALE",
            "replacement": "infra/password=SUPER_SECRET_REPLACEMENT",
            "secret_safety": "credential=SUPER_SECRET_SAFETY",
            "spec_verdict": "AK" + "IA" + "ABCDEFGHIJKLMNOP",
            "quality_verdict": "xoxb-SUPER_SECRET_QUALITY_1234567890",
        }
        list_mutations = {
            "direct_consumers": "projects/sk-proj-SUPER_SECRET_CONSUMER_123456",
            "validators": (
                "scripts/validation/"
                "eyJhbGciOiJIUzI1NiJ9.SUPER_SECRET_VALIDATOR.signature"
            ),
            "tests": "tests/-----BEGIN PRIVATE KEY-----",
            "provenance": "ghp_SUPER_SECRET_PROVENANCE_1234567890123456",
            "rollback": "Bearer SUPER_SECRET_ROLLBACK_1234567890",
        }
        top_mutations = {
            "predecessor_closure": "PASSWORD=SUPER_SECRET_PREDECESSOR",
            "implementation_base": (
                "ghp_SUPER_SECRET_IMPLEMENTATION_1234567890123456"
            ),
            "enforcement": "Bearer SUPER_SECRET_ENFORCEMENT_1234567890",
            "target_roots": ["infra/token=SUPER_SECRET_ROOT"],
        }

        with TemporaryDeltaRepository() as fixture:
            cases: list[tuple[str, str, object]] = []
            cases.extend(
                (field, payload, ("row", field))
                for field, payload in row_mutations.items()
            )
            cases.extend(
                (field, payload, ("list", field))
                for field, payload in list_mutations.items()
            )
            cases.extend(
                (
                    field,
                    (
                        value
                        if isinstance(value, str)
                        else "infra/token=SUPER_SECRET_ROOT"
                    ),
                    ("top", field, value),
                )
                for field, value in top_mutations.items()
            )
            for field, payload, mutation in cases:
                with self.subTest(field=field):
                    rows = [
                        valid_row(path, changed_since=fixture.predecessor)
                        for path in fixture.changed_paths
                    ]
                    document = valid_document(
                        fixture.predecessor,
                        fixture.implementation_base,
                        rows,
                    )
                    mutation_kind = mutation[0]
                    if mutation_kind == "row":
                        rows[0][mutation[1]] = payload
                    elif mutation_kind == "list":
                        rows[0][mutation[1]] = [payload]
                    else:
                        document[mutation[1]] = mutation[2]
                    fixture.write_manifest(document)
                    summary = fixture.root / contract.DELTA_SUMMARY
                    summary.parent.mkdir(parents=True, exist_ok=True)
                    summary.write_text("sentinel\n", encoding="utf-8")

                    with self.assertRaises(contract.ContractInputError) as caught:
                        contract.load_delta_manifest(fixture.root)
                    self.assertNotIn(payload, str(caught.exception))

                    stderr = io.StringIO()
                    with contextlib.redirect_stderr(stderr):
                        result = contract.main(
                            [
                                "--root",
                                str(fixture.root),
                                "--write-summary",
                            ]
                        )
                    self.assertEqual(2, result)
                    self.assertEqual(
                        "sentinel\n",
                        summary.read_text(encoding="utf-8"),
                    )
                    self.assertNotIn(payload, stderr.getvalue())

    def test_full_commit_hash_and_path_bound_evidence_are_not_secret_like(
        self,
    ) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            rows[0]["provenance"] = [
                (
                    f"git:{fixture.predecessor}..{fixture.implementation_base}:"
                    f"{rows[0]['path']}"
                )
            ]
            rows[0]["rollback"] = [
                f"git-revert:{fixture.implementation_base}:{rows[0]['path']}"
            ]
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    rows,
                )
            )
            document = contract.load_delta_manifest(fixture.root)
            self.assertEqual(
                (),
                contract.validate_delta_manifest(fixture.root, document),
            )


class SecretSafetyTests(unittest.TestCase):
    def test_secret_rows_are_path_only_and_diagnostics_are_value_free(self) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            write_text(
                fixture.root,
                "secrets/example.env.example",
                "PASSWORD=SUPER_SECRET_VALUE_CHANGED\n",
            )
            rows = [
                valid_row(
                    path,
                    changed_since=fixture.predecessor,
                )
                for path in (*fixture.changed_paths, "secrets/example.env.example")
            ]
            rows[-1]["secret_safety"] = "not-applicable"
            fixture.write_manifest(
                valid_document(
                    fixture.predecessor,
                    fixture.implementation_base,
                    rows,
                )
            )
            document = contract.load_delta_manifest(fixture.root)
            findings = contract.validate_delta_manifest(fixture.root, document)
            self.assertIn(
                "delta-secret-safety-invalid",
                {finding.code for finding in findings},
            )
            self.assertNotIn("SUPER_SECRET_VALUE_CHANGED", repr(findings))


class WholeSurfaceTests(unittest.TestCase):
    def test_current_inventory_is_complete_and_native_safe(self) -> None:
        contract = load_contract_module()
        inventory = contract.current_target_inventory(ROOT)
        tracked = tuple(
            sorted(
                path
                for path in git(ROOT, "ls-files", "--", *TARGET_ROOTS).splitlines()
                if path
            )
        )
        self.assertEqual(tracked, inventory.paths)
        self.assertEqual(len(tracked), sum(count for _, count in inventory.counts_by_root))
        self.assertEqual(
            sum(path.endswith((".md", ".mdx")) for path in tracked),
            inventory.markdown_count,
        )
        self.assertEqual(
            sum(path.endswith("README.md") for path in tracked),
            inventory.readme_count,
        )
        for path in inventory.paths:
            with self.subTest(path=path):
                self.assertEqual(path, pathlib.PurePosixPath(path).as_posix())
                self.assertTrue((ROOT / path).is_file())
                self.assertFalse((ROOT / path).is_symlink())

        metadata = load_metadata_module()
        profiles = metadata.load_profiles(PROFILE_REGISTRY)
        for path in inventory.paths:
            if not path.endswith("README.md"):
                continue
            readme = pathlib.Path(path)
            with self.subTest(readme=path):
                self.assertEqual(
                    1,
                    len(metadata.matching_readme_profiles(readme, profiles)),
                )
                text = (ROOT / readme).read_text(encoding="utf-8")
                if text.startswith("---\n"):
                    self.assertIsNotNone(
                        metadata.readme_frontmatter_consumer(readme, profiles)
                    )

        document = contract.load_delta_manifest(ROOT)
        for row in document.entries:
            if not row.path.endswith((".md", ".mdx")):
                with self.subTest(native_profile=row.path):
                    self.assertIsNone(row.profile)

    def test_summary_is_deterministic_and_contains_no_secret_payload(self) -> None:
        contract = load_contract_module()
        document = contract.load_delta_manifest(ROOT)
        inventory = contract.current_target_inventory(ROOT)
        first = contract.render_delta_summary(document, inventory)
        second = contract.render_delta_summary(document, inventory)
        self.assertEqual(first, second)
        self.assertEqual(first, SUMMARY_PATH.read_text(encoding="utf-8"))
        self.assertNotIn("PASSWORD=", first)
        self.assertNotIn("SUPER_SECRET_VALUE", first)


class PredecessorIntegrityTests(unittest.TestCase):
    def test_spec_133_artifacts_match_closure_commit(self) -> None:
        predecessor_artifacts = (
            "docs/90.references/data/governance/document-corpus-lifecycle/"
            "target-surface-convergence.yaml",
            "docs/90.references/data/governance/document-corpus-lifecycle/"
            "target-surface-convergence-summary.md",
        )
        closure_artifacts = (
            "docs/03.specs/133-target-surface-contract-convergence/spec.md",
            "docs/04.execution/plans/"
            "2026-07-18-target-surface-contract-convergence.md",
            "docs/04.execution/tasks/"
            "2026-07-18-target-surface-contract-convergence.md",
        )
        self.assertEqual(
            "",
            git(
                ROOT,
                "diff",
                "--name-only",
                PREDECESSOR_CLOSURE,
                "--",
                *predecessor_artifacts,
            ),
        )
        self.assertEqual(
            "",
            git(
                ROOT,
                "diff",
                "--name-only",
                TASK_START,
                "--",
                *closure_artifacts,
            ),
        )
        subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                PREDECESSOR_CLOSURE,
                TASK_START,
            ],
            cwd=ROOT,
            check=True,
        )
        changed = git(
            ROOT,
            "diff",
            "--name-only",
            PREDECESSOR_CLOSURE,
            TASK_START,
            "--",
            *closure_artifacts,
        ).splitlines()
        self.assertEqual(sorted(closure_artifacts), sorted(changed))
        witness = subprocess.run(
            [
                "git",
                "diff",
                "--binary",
                PREDECESSOR_CLOSURE,
                TASK_START,
                "--",
                *closure_artifacts,
            ],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(
            "e6e65df87c4b7a30845fc01318ee2d0ea0d0798d7deef1dfaa0c658cbe3afbc5",
            hashlib.sha256(witness).hexdigest(),
        )


class RepositoryManifestTests(unittest.TestCase):
    def test_repository_manifest_has_fixed_baselines_and_truthful_owners(self) -> None:
        contract = load_contract_module()
        document = contract.load_delta_manifest(ROOT)
        rows = {row.path: row for row in document.entries}
        self.assertEqual(PREDECESSOR_CLOSURE, document.predecessor_closure)
        self.assertEqual(IMPLEMENTATION_BASE, document.implementation_base)
        self.assertEqual("advisory", document.enforcement)
        self.assertEqual(140, len(document.entries))
        self.assertEqual(
            contract.changed_target_paths(ROOT, PREDECESSOR_CLOSURE),
            tuple(row.path for row in document.entries),
        )
        self.assertEqual(
            EXPECTED_UPDATE_PATHS,
            {
                row.path
                for row in document.entries
                if row.disposition == "update"
            },
        )
        self.assertEqual(
            {"preserve": 90, "update": 50},
            {
                disposition: sum(
                    row.disposition == disposition for row in document.entries
                )
                for disposition in ("preserve", "update")
            },
        )
        for path in TASK2_UPDATE_PATHS:
            with self.subTest(task2_path=path):
                self.assertEqual("update", rows[path].disposition)
                self.assertEqual("pending", rows[path].spec_verdict)
                self.assertEqual("pending", rows[path].quality_verdict)
        task3_owners = {
            "infra/01-gateway/README.md": "infra/01-gateway/README.md",
            "infra/tech-stack.versions.json": (
                "scripts/operations/sync-tech-stack-versions.sh"
            ),
            "scripts/hardening/check-all-hardening.sh": (
                "scripts/hardening/check-all-hardening.sh"
            ),
            "tests/validation/test_tech_stack_version_contract.py": (
                "tests/validation/test_tech_stack_version_contract.py"
            ),
        }
        for path in TASK3_UPDATE_PATHS:
            with self.subTest(task3_path=path):
                self.assertEqual("update", rows[path].disposition)
                self.assertEqual(task3_owners[path], rows[path].canonical_owner)
                self.assertEqual("pending", rows[path].spec_verdict)
                self.assertEqual("pending", rows[path].quality_verdict)
                self.assertIn(
                    "tests/validation/test_tech_stack_version_contract.py",
                    rows[path].tests,
                )
        self.assertFalse(
            any(
                row.disposition in {"migrate", "delete"}
                for row in document.entries
            )
        )
        for row in document.entries:
            with self.subTest(owner=row.path):
                self.assertNotEqual(
                    "docs/03.specs/135-target-surface-delta-convergence/spec.md",
                    row.canonical_owner,
                )
                self.assertTrue((ROOT / row.canonical_owner).is_file())
                for consumer in row.direct_consumers:
                    self.assertTrue((ROOT / consumer).is_file())
        self.assertEqual((), contract.validate_delta_manifest(ROOT, document))

    def test_preserve_rationales_and_declared_consumers_are_factual(self) -> None:
        contract = load_contract_module()
        document = contract.load_delta_manifest(ROOT)
        retired_boilerplate = {
            "Retain this value-free fixture as focused regression evidence.",
            "Retain this focused test as post-predecessor contract evidence.",
            (
                "Retain this GitHub-native workflow until its registered owner "
                "changes it."
            ),
            (
                "Retain this Compose declaration; this task does not mutate "
                "runtime services."
            ),
            "Retain this value-free supply-chain policy or trust fixture.",
            "Retain this implemented validation or operations support surface.",
            "Retain this project-native dependency or source surface.",
            "Retain this bounded example implementation surface.",
            "Retain this GitHub-native repository control surface.",
            "Retain this current native target surface.",
        }
        focused_fixture_owners = (
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
        explicit_pairs = {
            (
                "examples/sample-web-service/.dockerignore",
                "scripts/validation/check-supply-chain-policy.py",
            ),
            (
                "scripts/validation/target_surface_contract.py",
                "scripts/validation/check-target-surface-contract.py",
            ),
            (
                "scripts/validation/target_surface_delta_contract.py",
                "scripts/validation/check-target-surface-delta-contract.py",
            ),
            (
                "tests/validation/test_target_surface_contracts.py",
                ".github/workflows/ci-quality.yml",
            ),
            (
                "tests/validation/test_target_surface_contracts.py",
                "scripts/validation/run-local-qa-gates.sh",
            ),
            (
                "tests/validation/test_target_surface_delta_contracts.py",
                "scripts/validation/run-local-qa-gates.sh",
            ),
        }

        def is_proven_consumer(artifact: str, consumer: str) -> bool:
            if (artifact, consumer) in explicit_pairs:
                return True
            if any(
                artifact.startswith(prefix) and consumer == owner
                for prefix, owner in focused_fixture_owners
            ):
                return True
            consumer_text = (ROOT / consumer).read_text(
                encoding="utf-8",
                errors="strict",
            )
            relative = os.path.relpath(
                artifact,
                pathlib.PurePosixPath(consumer).parent.as_posix(),
            ).replace(os.sep, "/")
            return any(
                token in consumer_text
                for token in (artifact, relative, f"./{relative}")
            )

        for row in document.entries:
            with self.subTest(path=row.path):
                self.assertNotIn(row.finding, retired_boilerplate)
                if row.disposition == "preserve":
                    self.assertIn(row.path, row.finding)
                for consumer in row.direct_consumers:
                    tracked = subprocess.run(
                        [
                            "git",
                            "ls-files",
                            "--error-unmatch",
                            "--",
                            consumer,
                        ],
                        cwd=ROOT,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, tracked.returncode)
                    self.assertTrue((ROOT / consumer).is_file())
                    self.assertFalse((ROOT / consumer).is_symlink())
                    self.assertTrue(is_proven_consumer(row.path, consumer))
        observability = next(
            row
            for row in document.entries
            if row.path == "infra/06-observability/docker-compose.yml"
        )
        self.assertEqual((), observability.direct_consumers)


class CommandLineTests(unittest.TestCase):
    def test_bootstrap_refuses_existing_manifest_and_check_is_advisory(self) -> None:
        contract = load_contract_module()
        self.assertEqual(
            2,
            contract.main(
                [
                    "--root",
                    str(ROOT),
                    "--bootstrap",
                    "--predecessor-commit",
                    PREDECESSOR_CLOSURE,
                    "--implementation-base-commit",
                    IMPLEMENTATION_BASE,
                ]
            ),
        )
        self.assertEqual(
            0,
            contract.main(["--root", str(ROOT), "--mode", "advisory"]),
        )

    def test_blocking_mode_rejects_every_non_pass_verdict_and_cannot_be_downgraded(
        self,
    ) -> None:
        contract = load_contract_module()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = contract.main(["--root", str(ROOT), "--mode", "blocking"])
        self.assertEqual(1, result)
        self.assertIn("delta-spec-verdict-not-pass", stderr.getvalue())
        self.assertIn("delta-quality-verdict-not-pass", stderr.getvalue())
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            document = valid_document(
                fixture.predecessor,
                fixture.implementation_base,
                rows,
            )
            document["enforcement"] = "blocking"
            fixture.write_manifest(document)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = contract.main(
                    [
                        "--root",
                        str(fixture.root),
                        "--mode",
                        "advisory",
                    ]
                )
            self.assertEqual(1, result)
            self.assertIn("delta-spec-verdict-not-pass", stderr.getvalue())

    def test_advisory_tolerates_only_pending_review_not_contract_findings(
        self,
    ) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            document = valid_document(
                fixture.predecessor,
                fixture.implementation_base,
                rows,
            )
            fixture.write_manifest(document)
            self.assertEqual(
                0,
                contract.main(
                    ["--root", str(fixture.root), "--write-summary"]
                ),
            )
            self.assertEqual(
                0,
                contract.main(
                    ["--root", str(fixture.root), "--mode", "advisory"]
                ),
            )

            document["entries"] = rows[1:]
            fixture.write_manifest(document)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = contract.main(
                    ["--root", str(fixture.root), "--mode", "advisory"]
                )
            self.assertEqual(1, result)
            self.assertIn("delta-coverage-missing", stderr.getvalue())

            document["entries"] = rows
            fixture.write_manifest(document)
            registry = fixture.root / contract.PROFILE_REGISTRY
            registry.write_text("readme_profiles: []\n", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = contract.main(
                    ["--root", str(fixture.root), "--mode", "advisory"]
                )
            self.assertEqual(1, result)
            self.assertIn("delta-readme-registry-invalid", stderr.getvalue())

    def test_advisory_rejects_explicit_failed_review_verdicts_value_free(
        self,
    ) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            rows = [
                valid_row(path, changed_since=fixture.predecessor)
                for path in fixture.changed_paths
            ]
            document = valid_document(
                fixture.predecessor,
                fixture.implementation_base,
                rows,
            )
            fixture.write_manifest(document)
            self.assertEqual(
                0,
                contract.main(
                    ["--root", str(fixture.root), "--write-summary"]
                ),
            )
            self.assertEqual(
                0,
                contract.main(
                    ["--root", str(fixture.root), "--mode", "advisory"]
                ),
            )
            self.assertEqual(
                1,
                contract.main(
                    ["--root", str(fixture.root), "--mode", "blocking"]
                ),
            )

            cases = (
                (
                    "spec_verdict",
                    "delta-spec-review-rejected",
                    "specification review did not approve the row",
                ),
                (
                    "quality_verdict",
                    "delta-quality-review-rejected",
                    "quality review did not approve the row",
                ),
            )
            for field, code, message in cases:
                with self.subTest(field=field):
                    rows[0]["spec_verdict"] = "pending"
                    rows[0]["quality_verdict"] = "pending"
                    rows[0][field] = "fail"
                    fixture.write_manifest(document)
                    loaded = contract.load_delta_manifest(fixture.root)
                    summary = contract.render_delta_summary(
                        loaded,
                        contract.current_target_inventory(fixture.root),
                    )
                    write_text(
                        fixture.root,
                        contract.DELTA_SUMMARY.as_posix(),
                        summary,
                    )

                    advisory_stderr = io.StringIO()
                    with contextlib.redirect_stderr(advisory_stderr):
                        advisory_result = contract.main(
                            [
                                "--root",
                                str(fixture.root),
                                "--mode",
                                "advisory",
                            ]
                        )
                    expected = (
                        f"{code}: {rows[0]['path']}: {message}"
                    )
                    self.assertEqual(1, advisory_result)
                    self.assertEqual(expected, advisory_stderr.getvalue().strip())

                    blocking_stderr = io.StringIO()
                    with contextlib.redirect_stderr(blocking_stderr):
                        blocking_result = contract.main(
                            [
                                "--root",
                                str(fixture.root),
                                "--mode",
                                "blocking",
                            ]
                        )
                    self.assertEqual(1, blocking_result)
                    self.assertIn(expected, blocking_stderr.getvalue())

    def test_bootstrap_creates_only_through_no_follow_repository_parents(
        self,
    ) -> None:
        contract = load_contract_module()
        with TemporaryDeltaRepository() as fixture:
            result = contract.main(
                [
                    "--root",
                    str(fixture.root),
                    "--bootstrap",
                    "--predecessor-commit",
                    fixture.predecessor,
                    "--implementation-base-commit",
                    fixture.implementation_base,
                ]
            )
            manifest = fixture.root / contract.DELTA_MANIFEST
            self.assertEqual(0, result)
            self.assertTrue(manifest.is_file())
            self.assertFalse(manifest.is_symlink())
            contract.load_delta_manifest(fixture.root)

        with (
            TemporaryDeltaRepository() as fixture,
            tempfile.TemporaryDirectory() as outside_directory,
        ):
            outside = pathlib.Path(outside_directory)
            governance = fixture.root / contract.DELTA_MANIFEST.parent
            governance.parent.mkdir(parents=True, exist_ok=True)
            governance.symlink_to(outside, target_is_directory=True)
            outside_manifest = outside / contract.DELTA_MANIFEST.name

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = contract.main(
                    [
                        "--root",
                        str(fixture.root),
                        "--bootstrap",
                        "--predecessor-commit",
                        fixture.predecessor,
                        "--implementation-base-commit",
                        fixture.implementation_base,
                    ]
                )
            self.assertEqual(2, result)
            self.assertFalse(outside_manifest.exists())
            self.assertIn("delta-bootstrap-refused", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
