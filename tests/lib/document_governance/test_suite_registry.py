from __future__ import annotations

import copy
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.suite_registry import SuiteRegistryError, load


MANIFEST = Path("scripts/manifest.yaml")


class SuiteRegistryTests(unittest.TestCase):
    def test_supply_chain_owner_requires_the_exact_check_capability(self) -> None:
        """The predicate, not the registry, enforces its complete capability."""

        path = "scripts/validation/check-supply-chain-policy.py"
        owner = next(
            item for item in load(MANIFEST).validators if str(item.path) == path
        )
        self.assertEqual(("--check",), owner.execution_argv)
        for argv in ([], ["--write"], ["--oci-archive-config-digest", "archive"]):
            with self.subTest(argv=argv):
                result = subprocess.run(
                    [sys.executable, path, *argv],
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd(),
                )
                self.assertNotEqual(
                    0,
                    result.returncode,
                    "the supply-chain validator must fail closed without --check",
                )

    def test_membership_is_data_not_a_python_inventory(self) -> None:
        """A manifest edit alone changes membership; no Python map mirrors it."""

        import scripts.lib.document_governance.suite_registry as module

        self.assertFalse(
            hasattr(module, "IMMUTABLE_RETAINED_VALIDATOR_OWNERSHIP"),
            "validator ownership must be derived from the manifest, not duplicated in Python",
        )

        path = "scripts/validation/check-supply-chain-policy.py"
        baseline = {
            item.path.as_posix(): item.public_suites[0]
            for item in load(MANIFEST).validators
        }
        self.assertEqual("repository-integrity", baseline[path])

        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        next(row for row in document["files"] if row["path"] == path)[
            "public_suites"
        ] = ["document-contract"]
        moved = {
            item.path.as_posix(): item.public_suites[0]
            for item in self._load(document).validators
        }
        self.assertEqual("document-contract", moved[path])

        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        document["files"] = [row for row in document["files"] if row["path"] != path]
        dropped = {item.path.as_posix() for item in self._load(document).validators}
        self.assertNotIn(path, dropped)
        self.assertEqual(len(baseline) - 1, len(dropped))

    def test_execution_argv_shape_is_generic_for_an_unpinned_validator(self) -> None:
        """Shape admission is a generic rule, not a per-file argument table."""

        path = "scripts/validation/check-script-manifest.py"
        for argv in ([], ["--mode", "all"], ["--root", "docs"]):
            with self.subTest(argv=argv, accepted=True):
                document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
                next(row for row in document["files"] if row["path"] == path)[
                    "execution_argv"
                ] = argv
                self._load(document)
        for argv in (
            ["--help"],
            ["-h"],
            ["--check; rm -rf /"],
            ["--check", "--check"],
            ["--mode"] * 9,
            ["not-an-option"],
        ):
            with self.subTest(argv=argv, accepted=False):
                document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
                next(row for row in document["files"] if row["path"] == path)[
                    "execution_argv"
                ] = argv
                with self.assertRaises(SuiteRegistryError):
                    self._load(document)

    def test_a_modal_validator_cannot_be_narrowed_by_a_manifest_edit(self) -> None:
        """A shape-valid but narrower mode still weakens the gate, so it is pinned."""

        path = "scripts/validation/check-document-links.py"
        for argv in (["--mode", "traceability"], ["--mode", "alignment"], []):
            with self.subTest(argv=argv):
                document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
                next(row for row in document["files"] if row["path"] == path)[
                    "execution_argv"
                ] = argv
                with self.assertRaisesRegex(
                    SuiteRegistryError, "complete validation capability"
                ):
                    self._load(document)

    def test_manifest_input_rejects_ambiguous_unbounded_and_nonregular_bytes(
        self,
    ) -> None:
        from tests.lib.document_governance.test_links import load_script_manifest_cli

        checker = load_script_manifest_cli()
        valid = b"schema_version: 1\nfiles: []\n"
        cases = (
            b"schema_version: 0\n" + valid,
            b"files: [{path: one, path: two}]\n",
            b"files: &a []\nother: *a\n",
            b"files: []\nother: {<<: {a: b}}\n",
            b"files: []\nother: " + b"[" * 65 + b"]" * 65,
            valid + b"#" * 1_048_576,
            valid + b"\xff",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            for raw in cases:
                with self.subTest(raw=raw[:50]):
                    path.write_bytes(raw)
                    with self.assertRaises(SuiteRegistryError):
                        load(path)
                    self.assertIn("_load_error", checker._load_manifest(path))
            path.unlink()
            target = Path(directory) / "source.yaml"
            target.write_bytes(valid)
            path.symlink_to(target)
            with self.assertRaises(SuiteRegistryError):
                load(path)
            self.assertIn("_load_error", checker._load_manifest(path))
            path.unlink()
            path.mkdir()
            with self.assertRaises(SuiteRegistryError):
                load(path)
            self.assertIn("_load_error", checker._load_manifest(path))

    def test_manifest_ancestor_symlink_and_regular_to_fifo_race_fail_closed(
        self,
    ) -> None:
        from scripts.lib.document_governance import suite_registry
        from tests.lib.document_governance.test_links import load_script_manifest_cli

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            path = source / "manifest.yaml"
            path.write_text("files: []\n", encoding="utf-8")
            (root / "alias").symlink_to(source, target_is_directory=True)
            for read in (
                suite_registry.load,
                load_script_manifest_cli()._load_manifest,
            ):
                with self.subTest(read=read.__name__):
                    if read is suite_registry.load:
                        with self.assertRaises(SuiteRegistryError):
                            read(root / "alias/manifest.yaml")
                    else:
                        self.assertIn("_load_error", read(root / "alias/manifest.yaml"))
            real_open = os.open

            def swap_before_open(name, flags, *args, **kwargs):
                if Path(name).name == path.name:
                    path.unlink()
                    os.mkfifo(path)
                    self.assertTrue(flags & os.O_NONBLOCK, "FIFO open must not block")
                return real_open(name, flags, *args, **kwargs)

            with mock.patch.object(
                suite_registry.os, "open", side_effect=swap_before_open
            ):
                with self.assertRaises(SuiteRegistryError):
                    load(path)

    def test_public_suites_and_atomic_ownership_are_exact(self) -> None:
        registry = load(MANIFEST)
        self.assertEqual(
            registry.public_names,
            (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
        )
        self.assertTrue(
            all(len(item.public_suites) == 1 for item in registry.validators)
        )
        self.assertTrue(
            all(item.has_mirrored_test for item in registry.production_modules)
        )

    def test_rejects_duplicate_behavioral_consumers_and_suite_ownership(self) -> None:
        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        validator = next(row for row in document["files"] if row["kind"] == "validator")
        validator["public_suites"] = ["document-contract", "document-graph"]
        with self.assertRaisesRegex(SuiteRegistryError, "exactly one"):
            self._load(document)

        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(
            next(row for row in document["files"] if row["kind"] == "validator")
        )
        duplicate["path"] = "scripts/lib/document_governance/duplicate.py"
        duplicate["kind"] = "library"
        duplicate.pop("public_suites")
        duplicate["consumers"] = ["scripts/lib/gate/ci_gate_contract.py"] * 2
        document["files"].append(duplicate)
        with self.assertRaisesRegex(SuiteRegistryError, "duplicates"):
            self._load(document)

    def test_rejects_missing_mirrored_tests_and_suite_logic_rows(self) -> None:
        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        module = next(
            row
            for row in document["files"]
            if row["path"] == "scripts/lib/document_governance/suite_registry.py"
        )
        module["tests"] = ["tests/validation/test_script_manifest.py"]
        with self.assertRaisesRegex(SuiteRegistryError, "mirrored library test"):
            self._load(document)

        module["public_suites"] = ["repository-integrity"]
        with self.assertRaisesRegex(SuiteRegistryError, "only validators"):
            self._load(document)

    def _load(self, document: dict[str, object]):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.yaml"
            manifest.write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            return load(manifest)
