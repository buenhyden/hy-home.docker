from __future__ import annotations

import importlib.util
import hashlib
import pathlib
import subprocess
import sys
import tempfile
import unittest

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
) -> dict[str, object]:
    secret_safety = "path-only" if path.startswith("secrets/") else "not-applicable"
    replacement: str | None = None
    direct_consumers: list[str] = []
    validators: list[str] = []
    tests: list[str] = []
    provenance: list[str] = []
    rollback: list[str] = []
    spec_verdict = "pending"
    quality_verdict = "pending"
    if disposition in {"migrate", "delete"}:
        direct_consumers = ["docs/03.specs/135-target-surface-delta-convergence/spec.md"]
        replacement = "withdrawn" if disposition == "delete" else path
        validators = ["scripts/validation/check-target-surface-delta-contract.py"]
        tests = ["tests/validation/test_target_surface_delta_contracts.py"]
        provenance = [f"{changed_since}:{path}"]
        rollback = ["revert the owning logical task commit"]
        spec_verdict = "pass"
        quality_verdict = "pass"
    return {
        "path": path,
        "surface_class": "native-platform",
        "profile": None,
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
            "examples/sample/service.md": "# Service fixture\n",
            "infra/README.md": "# Infrastructure\n",
            "projects/app/config.json": "{}\n",
            "scripts/tool.sh": "#!/usr/bin/env bash\n",
            "secrets/example.env.example": "PASSWORD=SUPER_SECRET_VALUE\n",
            "tests/test_sample.py": "def test_sample():\n    assert True\n",
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
        return self

    def __exit__(self, *_args: object) -> None:
        self.directory.cleanup()

    @property
    def changed_paths(self) -> tuple[str, ...]:
        return (
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
        self.assertEqual(PREDECESSOR_CLOSURE, document.predecessor_closure)
        self.assertEqual(IMPLEMENTATION_BASE, document.implementation_base)
        self.assertEqual("advisory", document.enforcement)
        self.assertEqual(
            contract.changed_target_paths(ROOT, PREDECESSOR_CLOSURE),
            tuple(row.path for row in document.entries),
        )
        self.assertEqual(
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
            },
            {
                row.path
                for row in document.entries
                if row.disposition == "update"
            },
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


if __name__ == "__main__":
    unittest.main()
