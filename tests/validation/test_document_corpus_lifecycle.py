from __future__ import annotations

import contextlib
import dataclasses
import importlib.util
import inspect
import io
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.git_provenance import HistoricalDocument
from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
METADATA_SCRIPT = ROOT / "scripts/validation/check-document-metadata.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"


def load_script(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lifecycle = load_script(SCRIPT, "document_corpus_lifecycle")
metadata = load_script(METADATA_SCRIPT, "document_metadata_for_lifecycle_tests")


def run(*args: str, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    """Run a child while forwarding only a valid held repository descriptor."""

    pass_fds: tuple[int, ...] = ()
    if (
        len(args) > 1
        and pathlib.Path(args[1]).resolve() in {SCRIPT, METADATA_SCRIPT}
    ):
        pass_fds = gate_root_pass_fds(ROOT)
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        pass_fds=pass_fds,
    )


def git(root: pathlib.Path, *args: str) -> str:
    result = run("git", *args, cwd=root)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def init_repo(root: pathlib.Path) -> None:
    git(root, "init", "-q")
    git(root, "config", "core.hooksPath", "")
    git(root, "config", "user.email", "lifecycle@example.invalid")
    git(root, "config", "user.name", "Lifecycle Fixture")
    git(root, "symbolic-ref", "HEAD", "refs/heads/main")


def commit_all(root: pathlib.Path, message: str = "fixture") -> str:
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


class SharedProvenanceTests(unittest.TestCase):
    def test_nested_cli_preserves_only_valid_same_root_descriptor(self) -> None:
        descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY)
        try:
            override = f"/proc/self/fd/{descriptor}"
            with mock.patch.dict(os.environ, {"HYHOME_CI_GATE_ROOT": override}):
                result = run(sys.executable, str(SCRIPT), "--help", cwd=ROOT)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("--mode", result.stdout)
                unrelated = run(
                    sys.executable,
                    "-c",
                    "import os; print(os.path.isdir(os.environ['HYHOME_CI_GATE_ROOT']))",
                    cwd=ROOT,
                )
                self.assertEqual("False\n", unrelated.stdout)
                self.assertEqual(override, os.environ["HYHOME_CI_GATE_ROOT"])
        finally:
            os.close(descriptor)

        with tempfile.TemporaryDirectory() as directory:
            other_root = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
            try:
                closed = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY)
                os.close(closed)
                for override in (
                    str(ROOT),
                    f"/proc/self/fd/{closed}",
                    f"/proc/self/fd/{other_root}",
                ):
                    with self.subTest(override=override), mock.patch.dict(
                        os.environ,
                        {"HYHOME_CI_GATE_ROOT": override},
                    ):
                        result = run(
                            sys.executable,
                            str(SCRIPT),
                            "--help",
                            cwd=ROOT,
                        )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(
                        "FAIL: invalid HYHOME_CI_GATE_ROOT",
                        result.stderr,
                    )
            finally:
                os.close(other_root)

    def test_regular_reader_rejects_oversized_and_symlink_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "evidence.md"
            target.write_bytes(b"x" * (4 * 1024 * 1024 + 1))
            self.assertIsNone(
                lifecycle._read_regular_repo_bytes(
                    root,
                    "evidence.md",
                    require_tracked=False,
                )
            )
            link = root / "link.md"
            link.symlink_to(target)
            self.assertIsNone(
                lifecycle._read_regular_repo_bytes(
                    root,
                    "link.md",
                    require_tracked=False,
                )
            )

    def test_lifecycle_uses_shared_git_provenance(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("scripts.lib.document_governance.git_provenance", source)
        self.assertNotIn("METADATA_SCRIPT", source)
        self.assertNotIn(
            'spec_from_file_location(\n        "document_metadata',
            source,
        )


class HistoricalDocumentRecoveryTests(unittest.TestCase):
    def test_recovery_reads_only_the_committed_regular_blob(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            document = root / "docs/current.md"
            document.parent.mkdir(parents=True)
            document.write_text("current recovery body\n", encoding="utf-8")
            link = root / "docs/link.md"
            link.symlink_to("current.md")
            commit = commit_all(root, "recovery objects")
            document.unlink()
            link.unlink()

            recovered = HistoricalDocument(root, commit, "docs/current.md")
            self.assertEqual("current recovery body\n", recovered.read_text())

            for path in ("docs", "docs/missing.md", "docs/link.md"):
                with self.subTest(path=path), self.assertRaisesRegex(
                    ValueError,
                    "regular blob",
                ):
                    HistoricalDocument(root, commit, path).read_bytes()


class CurrentPublicContractTests(unittest.TestCase):
    def valid_row(self, **overrides: object):
        values: dict[str, object] = {
            "source_path": pathlib.PurePosixPath(
                "docs/03.specs/0001-example/spec.md"
            ),
            "target_path": pathlib.PurePosixPath(
                "docs/03.specs/0001-example/spec.md"
            ),
            "artifact_id": "SPEC-0001",
            "artifact_type": "spec",
            "status_before": "active",
            "status_after": "active",
            "parent_ids": (),
            "disposition": "preserve",
            "canonical_replacement": None,
            "active_consumers": (),
            "partition_plan": None,
            "preservation_class": None,
            "evidence": lifecycle.ManifestEvidence((), (), (), (), ()),
            "review_verdict": lifecycle.ReviewVerdict("pending", "pending"),
        }
        values.update(overrides)
        return lifecycle.MigrationManifestRow(**values)

    def document(self, *, schema_version: int = 1):
        return lifecycle.MigrationManifestDocument(
            schema_version=schema_version,
            wave="fixture",
            baseline_commit="a" * 40,
            generated_by="check-document-corpus-lifecycle.py",
            enforcement="advisory",
            entries=(self.valid_row(),),
        )

    def write_manifest(self, text: str) -> pathlib.Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = pathlib.Path(directory.name) / "manifest.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_cli_defaults_to_registry_and_exposes_only_four_modes(self) -> None:
        parser = lifecycle._parser()
        self.assertEqual(REGISTRY.resolve(), parser.parse_args([]).profiles.resolve())
        self.assertEqual("check-public", parser.parse_args([]).mode)
        self.assertEqual(
            ("check-public", "check-contract", "check-promoted", "check-recovery"),
            lifecycle.MODES,
        )

    def test_public_dataclasses_are_frozen_and_tuple_backed(self) -> None:
        row = self.valid_row()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            row.disposition = "delete"  # type: ignore[misc]
        self.assertIsInstance(row.parent_ids, tuple)
        self.assertIsInstance(row.evidence.commands, tuple)

    def test_manifest_skeleton_signature_remains_plan_bound(self) -> None:
        self.assertEqual(
            str(inspect.signature(lifecycle.generate_manifest_skeleton)),
            "(root: 'pathlib.Path', contract: 'dict[str, object]', *, "
            "wave: 'str', baseline_ref: 'str') -> 'MigrationManifestDocument'",
        )

    def test_cli_misuse_fails_before_opening_repository_files(self) -> None:
        result = run(
            sys.executable,
            str(SCRIPT),
            "--mode",
            "check-contract",
            "--wave",
            "forbidden",
            "--profiles",
            "/missing/profiles.yaml",
            "--contract",
            "/missing/contract.yaml",
            cwd=ROOT,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("--wave", result.stderr)
        self.assertNotIn("configuration-error", result.stderr)

    def test_manifest_loader_rejects_unknown_and_missing_keys(self) -> None:
        loaded = yaml.safe_load(
            lifecycle.render_migration_manifest(self.document())
        )
        for mutation in ("unknown-top", "missing-entry"):
            candidate = {**loaded}
            candidate["entries"] = [dict(loaded["entries"][0])]
            if mutation == "unknown-top":
                candidate["unexpected"] = True
            else:
                del candidate["entries"][0]["status_after"]
            with self.subTest(mutation=mutation), self.assertRaises(
                lifecycle.ProfileError
            ):
                lifecycle.load_migration_manifest(
                    self.write_manifest(
                        yaml.safe_dump(candidate, sort_keys=False)
                    )
                )

    def test_manifest_serialization_is_deterministic_and_lf_only(self) -> None:
        rendered = lifecycle.render_migration_manifest(self.document())
        self.assertTrue(rendered.endswith("\n"))
        self.assertNotIn("\r", rendered)
        reloaded = lifecycle.load_migration_manifest(
            self.write_manifest(rendered)
        )
        self.assertEqual(
            rendered,
            lifecycle.render_migration_manifest(reloaded),
        )

    def test_manifest_v2_exposes_surface_transition_fields(self) -> None:
        loaded = yaml.safe_load(
            lifecycle.render_migration_manifest(self.document())
        )
        loaded["schema_version"] = 2
        row = loaded["entries"][0]
        row["artifact_type_before"] = row.pop("artifact_type")
        row["artifact_type_after"] = row["artifact_type_before"]
        row["surface_class"] = "typed-example"
        manifest = lifecycle.load_migration_manifest(
            self.write_manifest(yaml.safe_dump(loaded, sort_keys=False))
        )
        self.assertEqual(2, manifest.schema_version)
        self.assertEqual("spec", manifest.entries[0].artifact_type_before)
        self.assertEqual("spec", manifest.entries[0].artifact_type_after)
        self.assertEqual("typed-example", manifest.entries[0].surface_class)

    def test_current_public_mode_does_not_load_a_legacy_contract(self) -> None:
        with mock.patch.object(
            lifecycle,
            "load_migration_contract",
            side_effect=AssertionError("legacy authority loaded"),
        ), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, lifecycle.main(["--mode", "check-public"]))

    def test_recovery_mode_performs_only_archive_recovery_validation(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, lifecycle.main(["--mode", "check-recovery"]))
        self.assertIn("archive recovery:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
