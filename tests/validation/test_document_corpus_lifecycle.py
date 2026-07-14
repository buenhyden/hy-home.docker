from __future__ import annotations

import copy
import contextlib
import dataclasses
import datetime
import hashlib
import io
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
METADATA_SCRIPT = ROOT / "scripts/validation/check-document-metadata.py"
PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
CONTRACT = ROOT / "docs/99.templates/support/document-corpus-migration-contract.yaml"


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
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def git(root: pathlib.Path, *args: str) -> str:
    result = run("git", *args, cwd=root)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def init_repo(root: pathlib.Path) -> str:
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Lifecycle Test")
    return ""


def commit_all(root: pathlib.Path, message: str = "fixture") -> str:
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


class LifecycleTestCase(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)
        cls.contract = lifecycle.load_migration_contract(CONTRACT)

    def valid_row(self, **overrides: object) -> lifecycle.MigrationManifestRow:
        values: dict[str, object] = {
            "source_path": pathlib.PurePosixPath("docs/03.specs/source.md"),
            "target_path": pathlib.PurePosixPath("docs/03.specs/source.md"),
            "artifact_id": "spec:source",
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

    def document(
        self,
        baseline_commit: str,
        *,
        entries: tuple[lifecycle.MigrationManifestRow, ...] | None = None,
        wave: str = "fixture",
        enforcement: str = "advisory",
    ) -> lifecycle.MigrationManifestDocument:
        return lifecycle.MigrationManifestDocument(
            schema_version=1,
            wave=wave,
            baseline_commit=baseline_commit,
            generated_by="check-document-corpus-lifecycle.py",
            enforcement=enforcement,
            entries=entries if entries is not None else (self.valid_row(),),
        )

    def fixture_contract(
        self,
        source_paths: list[str],
        *,
        wave: str = "fixture",
        enforcement: str = "advisory",
        manifest_path: str | None = None,
    ) -> dict[str, object]:
        contract = copy.deepcopy(self.contract)
        contract["waves"] = {
            wave: {
                "enforcement": enforcement,
                "manifest_path": manifest_path,
                "scope_state": "approved",
                "source_paths": source_paths,
                "declared_outputs": [],
            }
        }
        return contract


class PublicContractTests(LifecycleTestCase):
    def test_modes_are_the_exact_fixed_tuple(self) -> None:
        self.assertEqual(
            lifecycle.MODES,
            (
                "check-contract",
                "generate-manifest",
                "check-manifest",
                "check-promoted",
                "generate-summary",
                "check-summary",
                "check-impacted",
                "report-duplicates",
                "report-full",
                "check-full",
                "check-archive",
                "check-directory-budget",
                "generate-archive-ledger",
                "check-archive-ledger",
                "generate-snapshot-manifest",
                "check-snapshot-manifest",
            ),
        )

    def test_public_dataclasses_are_frozen_and_tuple_backed(self) -> None:
        row = self.valid_row()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            row.disposition = "delete"  # type: ignore[misc]
        self.assertIsInstance(row.parent_ids, tuple)
        self.assertIsInstance(row.evidence.commands, tuple)

    def test_cli_misuse_returns_two_before_opening_repository_files(self) -> None:
        result = run(
            sys.executable,
            str(SCRIPT),
            "--mode",
            "generate-manifest",
            "--profiles",
            "/missing/profiles.yaml",
            "--contract",
            "/missing/contract.yaml",
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--wave", result.stderr)
        self.assertNotIn("configuration-error", result.stderr)

    def test_loader_rejects_unknown_and_missing_manifest_keys(self) -> None:
        valid = lifecycle.render_migration_manifest(
            self.document("a" * 40, entries=(self.valid_row(),))
        )
        loaded = yaml.safe_load(valid)
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.yaml"
            for mutation in ("unknown-top", "missing-entry"):
                candidate = copy.deepcopy(loaded)
                if mutation == "unknown-top":
                    candidate["unexpected"] = True
                else:
                    del candidate["entries"][0]["status_after"]
                path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
                with self.subTest(mutation=mutation), self.assertRaises(lifecycle.ProfileError):
                    lifecycle.load_migration_manifest(path)

    def test_manifest_serialization_is_canonical_deterministic_and_lf_only(self) -> None:
        row = self.valid_row(
            parent_ids=("spec:z", "spec:a"),
            active_consumers=(
                pathlib.PurePosixPath("docs/z.md"),
                pathlib.PurePosixPath("docs/a.md"),
            ),
            evidence=lifecycle.ManifestEvidence(
                ("z", "a"),
                ("z", "a"),
                (pathlib.PurePosixPath("docs/z.md"), pathlib.PurePosixPath("docs/a.md")),
                ("z", "a"),
                ("z", "a"),
            ),
        )
        rendered = lifecycle.render_migration_manifest(
            self.document("a" * 40, entries=(row,))
        )
        self.assertTrue(rendered.endswith("\n"))
        self.assertNotIn("\r", rendered)
        reloaded = lifecycle.load_migration_manifest(self.write_temp(rendered))
        rerendered = lifecycle.render_migration_manifest(reloaded)
        self.assertEqual(rendered, rerendered)
        self.assertEqual(reloaded.entries[0].parent_ids, ("spec:a", "spec:z"))

    def write_temp(self, text: str) -> pathlib.Path:
        directory = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        path = pathlib.Path(directory) / "value.yaml"
        path.write_text(text, encoding="utf-8")
        return path


class ManifestValidationTests(LifecycleTestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source = root / "docs/03.specs/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: spec:source\nartifact_type: spec\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root)
        return temporary, root, baseline

    def validate(
        self,
        root: pathlib.Path,
        baseline: str,
        entries: tuple[lifecycle.MigrationManifestRow, ...],
        *,
        enforcement: str = "advisory",
    ) -> set[str]:
        document = self.document(
            baseline,
            entries=entries,
            enforcement=enforcement,
        )
        contract = self.fixture_contract(["docs/03.specs/source.md"])
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root, self.profiles, contract, document
            )
        }

    def test_skeleton_has_one_pending_semantically_empty_row_per_baseline_path(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        contract = self.fixture_contract(["docs/03.specs/source.md"])
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=baseline,
        )
        self.assertEqual(document.baseline_commit, baseline)
        self.assertEqual(len(document.entries), 1)
        row = document.entries[0]
        self.assertEqual(row.source_path.as_posix(), "docs/03.specs/source.md")
        self.assertEqual(row.review_verdict, lifecycle.ReviewVerdict("pending", "pending"))
        self.assertEqual(row.parent_ids, ())
        self.assertIsNone(row.canonical_replacement)
        self.assertEqual(row.active_consumers, ())
        self.assertEqual(row.evidence, lifecycle.ManifestEvidence((), (), (), (), ()))
        self.assertIsNone(row.preservation_class)

    def test_manifest_coverage_path_type_and_target_conditions(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        valid = self.valid_row()
        cases = {
            "missing": ((), "manifest-source-missing"),
            "duplicate": ((valid, valid), "manifest-source-duplicate"),
            "delete-target": (
                (dataclasses.replace(valid, disposition="delete"),),
                "manifest-delete-target-invalid",
            ),
            "move-null": (
                (dataclasses.replace(valid, disposition="move", target_path=None),),
                "manifest-move-target-required",
            ),
            "preserve-distinct": (
                (
                    dataclasses.replace(
                        valid,
                        target_path=pathlib.PurePosixPath("docs/03.specs/other.md"),
                    ),
                ),
                "manifest-preserve-target-invalid",
            ),
            "absolute-source": (
                (dataclasses.replace(valid, source_path=pathlib.PurePosixPath("/tmp/source.md")),),
                "manifest-source-path-invalid",
            ),
            "unknown-type": (
                (dataclasses.replace(valid, artifact_type="mystery"),),
                "manifest-artifact-type-invalid",
            ),
        }
        for name, (entries, expected) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected, self.validate(root, baseline, entries))

    def test_baseline_must_resolve_to_the_exact_commit(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        document = self.document("f" * 40)
        findings = lifecycle.validate_migration_manifest(
            root,
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            document,
        )
        self.assertIn("manifest-baseline-commit-invalid", {item.code for item in findings})
        self.assertNotEqual(baseline, document.baseline_commit)

    def test_destructive_pending_row_is_rejected(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        row = self.valid_row(
            disposition="delete",
            target_path=None,
            preservation_class="git-history",
            active_consumers=(pathlib.PurePosixPath("docs/consumer.md"),),
            evidence=lifecycle.ManifestEvidence(
                ("git show BASE:docs/source.md",),
                ("docs/source.md",),
                (pathlib.PurePosixPath("docs/source.md"),),
                ("rg --fixed-strings docs/source.md",),
                ("revert logical task commit",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
        )
        self.assertIn(
            "manifest-destructive-review-required",
            self.validate(root, baseline, (row,), enforcement="blocking"),
        )


class PromotedManifestCliTests(LifecycleTestCase):
    def canonical_contract(
        self,
        *,
        enforcement: str = "advisory",
        manifest_path: str | None = None,
    ) -> dict[str, object]:
        contract = copy.deepcopy(self.contract)
        contract["waves"]["foundation"]["enforcement"] = enforcement
        contract["waves"]["foundation"]["manifest_path"] = manifest_path
        return contract

    def write_config(self, root: pathlib.Path, contract: dict[str, object]) -> tuple[pathlib.Path, pathlib.Path]:
        profiles = root / "profiles.yaml"
        profiles.write_text(PROFILES.read_text(encoding="utf-8"), encoding="utf-8")
        contract_path = root / "contract.yaml"
        contract_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
        return profiles, contract_path

    def invoke(self, root: pathlib.Path, profiles: pathlib.Path, contract: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return run(
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--profiles",
            str(profiles),
            "--contract",
            str(contract),
            "--mode",
            "check-promoted",
            cwd=ROOT,
        )

    def test_advisory_null_is_skipped_but_blocking_null_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            advisory = self.canonical_contract()
            profiles, contract_path = self.write_config(root, advisory)
            self.assertEqual(self.invoke(ROOT, profiles, contract_path).returncode, 0)

            blocking = self.canonical_contract(enforcement="blocking")
            _, contract_path = self.write_config(root, blocking)
            result = self.invoke(ROOT, profiles, contract_path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("promoted-manifest-path-required", result.stdout)

    def test_blocking_manifest_requires_existing_path_and_matching_enforcement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            contract = self.canonical_contract(
                enforcement="blocking",
                manifest_path=(
                    "docs/90.references/data/governance/"
                    "document-corpus-lifecycle/fixture.yaml"
                ),
            )
            source_paths = contract["waves"]["foundation"]["source_paths"]
            for path_text in source_paths:
                source = root / path_text
                source.parent.mkdir(parents=True, exist_ok=True)
                body = "---\nstatus: draft\n---\n\n# Fixture\n" if path_text.endswith("archive.template.md") else "# Fixture\n"
                source.write_text(body, encoding="utf-8")
            baseline = commit_all(root)
            profiles, contract_path = self.write_config(root, contract)
            missing = self.invoke(root, profiles, contract_path)
            self.assertEqual(missing.returncode, 1)
            self.assertIn("promoted-manifest-missing", missing.stdout)

            manifest = lifecycle.generate_manifest_skeleton(
                root,
                contract,
                wave="foundation",
                baseline_ref=baseline,
            )
            manifest = dataclasses.replace(manifest, enforcement="advisory")
            manifest_path = root / contract["waves"]["foundation"]["manifest_path"]
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                lifecycle.render_migration_manifest(manifest), encoding="utf-8"
            )
            commit_all(root, "track promoted manifest")
            mismatch = self.invoke(root, profiles, contract_path)
            self.assertEqual(mismatch.returncode, 1)
            self.assertIn("promoted-enforcement-mismatch", mismatch.stdout)


class CandidateManifestCliTests(LifecycleTestCase):
    def write_config(
        self,
        root: pathlib.Path,
        contract: dict[str, object],
    ) -> tuple[pathlib.Path, pathlib.Path]:
        profiles = root / "profiles.yaml"
        profiles.write_text(PROFILES.read_text(encoding="utf-8"), encoding="utf-8")
        contract_path = root / "contract.yaml"
        contract_path.write_text(
            yaml.safe_dump(contract, sort_keys=False),
            encoding="utf-8",
        )
        return profiles, contract_path

    def invoke(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
        contract: pathlib.Path,
        mode: str,
        manifest: pathlib.Path | str,
        *,
        output: pathlib.Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--profiles",
            str(profiles),
            "--contract",
            str(contract),
            "--mode",
            mode,
            "--manifest",
            str(manifest),
        ]
        if mode == "check-manifest":
            arguments.extend(("--wave", "foundation"))
        else:
            if output is None:
                raise AssertionError("summary modes require an output fixture")
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def make_fixture(
        self,
        root: pathlib.Path,
    ) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
        init_repo(root)
        contract = copy.deepcopy(self.contract)
        source_paths = contract["waves"]["foundation"]["source_paths"]
        for source_path in source_paths:
            source = root / source_path
            source.parent.mkdir(parents=True, exist_ok=True)
            if source_path.endswith("archive.template.md"):
                source.write_text(
                    "---\nstatus: draft\n---\n\n# Archive fixture\n",
                    encoding="utf-8",
                )
            else:
                source.write_bytes((ROOT / source_path).read_bytes())
        baseline = commit_all(root, "candidate baseline")
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="foundation",
            baseline_ref=baseline,
        )
        candidate = root / "docs/90.references/data/fixture.yaml"
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_text(
            lifecycle.render_migration_manifest(document),
            encoding="utf-8",
        )
        profiles, contract_path = self.write_config(root, contract)
        return candidate, profiles, contract_path

    def test_explicit_modes_accept_safe_untracked_candidate_before_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            candidate, profiles, contract = self.make_fixture(root)
            self.assertEqual(git(root, "ls-files", "--", candidate.relative_to(root)), "")

            checked = self.invoke(
                root,
                profiles,
                contract,
                "check-manifest",
                candidate.relative_to(root),
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

            summary = root / "docs/90.references/data/fixture-summary.md"
            generated = self.invoke(
                root,
                profiles,
                contract,
                "generate-summary",
                candidate.relative_to(root),
                output=summary,
            )
            self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
            self.assertTrue(summary.is_file())

            summary_checked = self.invoke(
                root,
                profiles,
                contract,
                "check-summary",
                candidate.relative_to(root),
                output=summary,
            )
            self.assertEqual(
                summary_checked.returncode,
                0,
                summary_checked.stdout + summary_checked.stderr,
            )

    def test_explicit_modes_reject_unsafe_candidate_paths_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            candidate, profiles, contract = self.make_fixture(root)
            outside = root.parent / f"{root.name}-outside-candidate.yaml"
            outside.write_bytes(candidate.read_bytes())
            self.addCleanup(lambda: outside.unlink(missing_ok=True))
            symlink = root / "docs/90.references/data/symlink.yaml"
            symlink.symlink_to(outside)
            unsafe_candidates: tuple[pathlib.Path | str, ...] = (
                symlink.relative_to(root),
                pathlib.Path("../escape.yaml"),
                outside,
            )

            for mode in ("check-manifest", "generate-summary", "check-summary"):
                for index, unsafe in enumerate(unsafe_candidates):
                    with self.subTest(mode=mode, candidate=unsafe):
                        output = root / f"unsafe-{mode}-{index}.md"
                        result = self.invoke(
                            root,
                            profiles,
                            contract,
                            mode,
                            unsafe,
                            output=output if mode != "check-manifest" else None,
                        )
                        self.assertEqual(result.returncode, 3)
                        self.assertFalse(output.exists())
                        self.assertNotIn("Traceback", result.stderr)


class ArchiveProvenanceTests(LifecycleTestCase):
    def archive_fixture(
        self, preservation_class: str = "git-history"
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, metadata.Record, bytes]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        payload = b"historical evidence\n"
        source = root / "docs/source.md"
        source.parent.mkdir()
        source.write_bytes(payload)
        commit = commit_all(root)
        blob = git(root, "rev-parse", f"{commit}:docs/source.md")
        sha256 = hashlib.sha256(payload).hexdigest()
        tombstone = root / "docs/98.archive/source.md"
        tombstone.parent.mkdir(parents=True)
        metadata_values: dict[str, object] = {
            "status": "archived",
            "artifact_id": "archive:source",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": "docs/source.md",
            "archived_on": "2026-07-14",
            "archive_reason": "Fixture.",
            "archive_disposition": "evidence-preserve",
            "archived_commit": commit,
            "archived_blob": blob,
            "preservation_class": preservation_class,
        }
        if preservation_class == "immutable-snapshot":
            snapshot = pathlib.PurePosixPath(
                f"docs/98.archive/evidence/{sha256}.md.snapshot"
            )
            (root / snapshot).parent.mkdir(parents=True)
            (root / snapshot).write_bytes(payload)
            metadata_values.update(
                snapshot_path=snapshot.as_posix(),
                content_sha256=sha256,
                snapshot_reason="Approved audit evidence.",
            )
        tombstone.write_text("# Tombstone\n", encoding="utf-8")
        commit_all(root, "track archive fixture")
        record = metadata.Record(
            pathlib.Path("docs/98.archive/source.md"), metadata_values, "archive"
        )
        return temporary, root, record, payload

    def test_commit_blob_path_and_snapshot_hashes_are_verified(self) -> None:
        temporary, root, record, _ = self.archive_fixture("immutable-snapshot")
        self.addCleanup(temporary.cleanup)
        self.assertEqual(lifecycle.validate_archive_provenance(root, record), [])

        mutations = {
            "commit": ({"archived_commit": "f" * 40}, "archive-commit-invalid"),
            "blob": ({"archived_blob": "f" * 40}, "archive-blob-invalid"),
            "path-equality": ({"archived_blob": git(root, "hash-object", "-w", str(root / "docs/98.archive/source.md"))}, "archive-blob-mismatch"),
            "snapshot-path": ({"snapshot_path": "docs/98.archive/evidence/wrong.md.snapshot"}, "archive-snapshot-path-mismatch"),
        }
        for name, (changes, expected) in mutations.items():
            with self.subTest(case=name):
                changed = dataclasses.replace(record, metadata={**record.metadata, **changes})
                self.assertIn(
                    expected,
                    {item.code for item in lifecycle.validate_archive_provenance(root, changed)},
                )
        snapshot_path = root / record.metadata["snapshot_path"]
        snapshot_path.write_bytes(b"changed evidence\n")
        self.assertIn(
            "archive-content-sha256-mismatch",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

    def test_git_history_forbids_snapshot_bytes(self) -> None:
        temporary, root, record, payload = self.archive_fixture("git-history")
        self.addCleanup(temporary.cleanup)
        sha256 = hashlib.sha256(payload).hexdigest()
        snapshot = root / f"docs/98.archive/evidence/{sha256}.md.snapshot"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_bytes(payload)
        changed = dataclasses.replace(
            record,
            metadata={
                **record.metadata,
                "snapshot_path": snapshot.relative_to(root).as_posix(),
                "content_sha256": sha256,
                "snapshot_reason": "Not admitted.",
            },
        )
        self.assertIn(
            "archive-snapshot-forbidden",
            {item.code for item in lifecycle.validate_archive_provenance(root, changed)},
        )

    def test_sensitive_snapshot_classes_are_rejected_without_payload_leakage(self) -> None:
        samples = (
            b"password=ultra-sensitive-value\n",
            b"credential: ultra-sensitive-value\n",
            b"token=ultra-sensitive-value\n",
            b"-----BEGIN PRIVATE KEY-----\nultra-sensitive-value\n",
            b".bash_history\nultra-sensitive-value\n",
            b"2026-07-14 ERROR ultra-sensitive-value\n",
        )
        for sample in samples:
            temporary, root, record, _ = self.archive_fixture("immutable-snapshot")
            try:
                sha256 = hashlib.sha256(sample).hexdigest()
                snapshot_path = pathlib.PurePosixPath(
                    f"docs/98.archive/evidence/{sha256}.md.snapshot"
                )
                (root / snapshot_path).write_bytes(sample)
                commit_all(root, "track confidentiality fixture")
                changed = dataclasses.replace(
                    record,
                    metadata={
                        **record.metadata,
                        "snapshot_path": snapshot_path.as_posix(),
                        "content_sha256": sha256,
                    },
                )
                findings = lifecycle.validate_archive_provenance(root, changed)
                self.assertIn("archive-snapshot-confidential", {item.code for item in findings})
                rendered = "\n".join(item.message for item in findings)
                self.assertNotIn("ultra-sensitive-value", rendered)
            finally:
                temporary.cleanup()

    def test_ledgers_are_deterministic_and_snapshot_manifest_excludes_git_history(self) -> None:
        first_tmp, first_root, first, _ = self.archive_fixture("immutable-snapshot")
        second_tmp, _, second, _ = self.archive_fixture("git-history")
        self.addCleanup(first_tmp.cleanup)
        self.addCleanup(second_tmp.cleanup)
        records = (dataclasses.replace(second, path=pathlib.Path("docs/98.archive/z.md")), first)
        ledger = lifecycle.render_archive_ledger(records)
        snapshot = lifecycle.render_snapshot_manifest(records)
        self.assertEqual(ledger, lifecycle.render_archive_ledger(tuple(reversed(records))))
        self.assertIn("docs/98.archive/source.md", snapshot)
        self.assertNotIn("docs/98.archive/z.md", snapshot)
        self.assertNotIn((first_root / "docs/source.md").read_text(), ledger)

    def test_ledger_and_snapshot_generate_check_modes_are_byte_equal(self) -> None:
        temporary, root, record, payload = self.archive_fixture("immutable-snapshot")
        self.addCleanup(temporary.cleanup)
        frontmatter = yaml.safe_dump(record.metadata, sort_keys=False)
        (root / record.path).write_text(
            f"---\n{frontmatter}---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        commit_all(root, "archive fixture")
        with tempfile.TemporaryDirectory() as output_directory:
            for generate_mode, check_mode, name in (
                ("generate-archive-ledger", "check-archive-ledger", "ledger.md"),
                (
                    "generate-snapshot-manifest",
                    "check-snapshot-manifest",
                    "snapshots.md",
                ),
            ):
                output = pathlib.Path(output_directory) / name
                generated = run(
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    generate_mode,
                    "--output",
                    str(output),
                    cwd=ROOT,
                )
                self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
                before = output.read_bytes()
                checked = run(
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    check_mode,
                    "--output",
                    str(output),
                    cwd=ROOT,
                )
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                self.assertEqual(output.read_bytes(), before)
                self.assertNotIn(payload.decode().strip(), output.read_text(encoding="utf-8"))


class DuplicateBudgetAndImpactTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "spec",
        **metadata_values: object,
    ) -> metadata.Record:
        values = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def test_duplicate_candidates_are_same_type_advisory_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            paths = {
                "docs/03.specs/a.md": "# Shared Title\n\nSame body.\n",
                "docs/03.specs/b.md": "# Shared Title\n\nSame body.\n",
                "docs/03.specs/c.md": "# shared-title\n\nDifferent.\n",
                "docs/04.execution/plans/d.md": "# Shared Title\n\nSame body.\n",
            }
            for path, body in paths.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
            records = (
                self.record("docs/03.specs/c.md"),
                self.record("docs/04.execution/plans/d.md", "plan"),
                self.record("docs/03.specs/b.md"),
                self.record("docs/03.specs/a.md"),
            )
            candidates = lifecycle.find_duplicate_candidates(root, records)
            self.assertEqual(candidates, tuple(sorted(candidates)))
            pairs = {(item.left_path.as_posix(), item.right_path.as_posix()): item for item in candidates}
            self.assertIn(("docs/03.specs/a.md", "docs/03.specs/b.md"), pairs)
            self.assertIn("exact-content", pairs[("docs/03.specs/a.md", "docs/03.specs/b.md")].signals)
            self.assertIn("normalized-title", pairs[("docs/03.specs/a.md", "docs/03.specs/c.md")].signals)
            self.assertFalse(any("d.md" in left or "d.md" in right for left, right in pairs))
            self.assertFalse(hasattr(candidates[0], "disposition"))

    def test_immediate_leaf_budget_boundaries_and_added_only_blocking(self) -> None:
        records_99 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(99)
        )
        below_warning = lifecycle.validate_directory_budgets(
            records_99,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-warning", {item.code for item in below_warning})

        records_100 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(100)
        )
        findings = lifecycle.validate_directory_budgets(
            records_100,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertIn("directory-budget-warning", {item.code for item in findings})
        self.assertNotIn("directory-budget-blocked", {item.code for item in findings})

        records_150 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(150)
        )
        added = pathlib.PurePosixPath("docs/04.execution/tasks/149.md")
        blocked = lifecycle.validate_directory_budgets(
            records_150,
            added_paths=frozenset({added}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertIn("directory-budget-blocked", {item.code for item in blocked})
        edited = lifecycle.validate_directory_budgets(
            records_150,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in edited})

        records_149 = records_150[:-1]
        below_block = lifecycle.validate_directory_budgets(
            records_149,
            added_paths=frozenset({pathlib.PurePosixPath("docs/04.execution/tasks/148.md")}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in below_block})

        approved_records = tuple(
            dataclasses.replace(
                record,
                metadata={
                    **record.metadata,
                    "partition_plan": "docs/04.execution/plans/2026-partition.md",
                    "review_verdict": {"specification": "pass", "quality": "pass"},
                },
            )
            if record.path.as_posix() == added.as_posix()
            else record
            for record in records_150
        )
        approved = lifecycle.validate_directory_budgets(
            approved_records,
            added_paths=frozenset({added}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in approved})

    def test_review_age_unavailable_is_advisory_and_does_not_mutate_status(self) -> None:
        record = self.record("docs/03.specs/source.md", status="active")
        original = copy.deepcopy(record.metadata)
        findings = lifecycle._review_findings(
            (record,), self.contract, today=datetime.date(2026, 7, 14)
        )
        self.assertIn("review-age-unavailable", {item.code for item in findings})
        self.assertTrue(all(item.severity == "warning" for item in findings))
        self.assertEqual(record.metadata, original)

    def test_impacted_records_include_declared_consumer_and_links_not_title_similarity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            bodies = {
                "docs/03.specs/source.md": "# Shared Title\n\nInitial.\n",
                "docs/03.specs/consumer.md": "# Consumer\n\n[Source](./source.md)\n",
                "docs/03.specs/similar.md": "# Shared Title\n\nUnlinked.\n",
            }
            for path, body in bodies.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
            baseline = commit_all(root)
            (root / "docs/03.specs/source.md").write_text(
                "# Shared Title\n\nChanged.\n", encoding="utf-8"
            )
            records = (
                self.record("docs/03.specs/source.md"),
                self.record("docs/03.specs/consumer.md"),
                self.record("docs/03.specs/similar.md"),
            )
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
                target_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
                active_consumers=(pathlib.PurePosixPath("docs/03.specs/consumer.md"),),
            )
            document = self.document(baseline, entries=(row,))
            selected = lifecycle.collect_impacted_records(
                root,
                records,
                self.profiles,
                self.fixture_contract(["docs/03.specs/source.md"]),
                (document,),
                base_ref=baseline,
            )
            paths = {item.path.as_posix() for item in selected}
            self.assertIn("docs/03.specs/source.md", paths)
            self.assertIn("docs/03.specs/consumer.md", paths)
            self.assertNotIn("docs/03.specs/similar.md", paths)


class ExceptionValidationTests(LifecycleTestCase):
    def write(self, exceptions: list[dict[str, object]]) -> pathlib.Path:
        directory = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        path = pathlib.Path(directory) / "exceptions.yaml"
        path.write_text(
            yaml.safe_dump({"schema_version": 1, "exceptions": exceptions}, sort_keys=False),
            encoding="utf-8",
        )
        return path

    def valid(self) -> dict[str, object]:
        return {
            "finding_code": "directory-budget-warning",
            "scope_paths": ["docs/04.execution/tasks/example.md"],
            "owner": "docs-platform",
            "reason": "Bounded migration debt.",
            "approved_at": "2026-07-01",
            "expires_on": "2026-08-01",
            "exit_condition": "Partition the directory.",
            "evidence": ["docs/04.execution/tasks/evidence.md"],
        }

    def codes(self, value: dict[str, object]) -> set[str]:
        return {
            item.code
            for item in lifecycle.validate_exceptions(
                self.write([value]),
                known_codes=frozenset({"directory-budget-warning"}),
                today=datetime.date(2026, 7, 14),
            )
        }

    def test_bounded_exception_schema_cases(self) -> None:
        valid = self.valid()
        cases = {
            "unknown-code": ({**valid, "finding_code": "unknown"}, "exception-code-unknown"),
            "wildcard": ({**valid, "scope_paths": ["docs/**"]}, "exception-scope-invalid"),
            "owner": ({**valid, "owner": ""}, "exception-owner-required"),
            "reason": ({**valid, "reason": ""}, "exception-reason-required"),
            "exit": ({**valid, "exit_condition": ""}, "exception-exit-condition-required"),
            "expired": ({**valid, "expires_on": "2026-07-14"}, "exception-expired"),
        }
        for name, (value, expected) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected, self.codes(value))
        self.assertEqual(self.codes(valid), set())

    def test_omitted_owner_uses_the_specific_required_code(self) -> None:
        value = self.valid()
        del value["owner"]
        self.assertIn("exception-owner-required", self.codes(value))


class ReviewRemediationTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "spec",
        **metadata_values: object,
    ) -> metadata.Record:
        values: dict[str, object] = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def test_cli_misuse_does_not_execute_repository_metadata_module(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            validation = root / "scripts/validation"
            validation.mkdir(parents=True)
            shutil.copy2(SCRIPT, validation / SCRIPT.name)
            marker = root / "metadata-loaded"
            (validation / "check-document-metadata.py").write_text(
                "import pathlib\n"
                f"pathlib.Path({str(marker)!r}).write_text('loaded')\n"
                "raise RuntimeError('metadata module executed')\n",
                encoding="utf-8",
            )
            result = run(
                sys.executable,
                str(validation / SCRIPT.name),
                "--mode",
                "generate-manifest",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertFalse(marker.exists())
            self.assertNotIn("metadata module executed", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_companion_reuses_canonical_static_manifest_and_exception_grammar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            readme = root / "README.md"
            readme.write_text("# Fixture\n", encoding="utf-8")
            baseline = commit_all(root)
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("README.md"),
                target_path=pathlib.PurePosixPath("README.md"),
                artifact_id="readme:forbidden",
                artifact_type="readme",
                status_before=None,
                status_after=None,
            )
            document = self.document(baseline, entries=(row,))
            contract = self.fixture_contract(["README.md"])
            with self.assertRaises(metadata.ProfileError):
                metadata.validate_static_migration_manifest(
                    lifecycle._manifest_mapping(document), contract, self.profiles
                )
            findings = lifecycle.validate_migration_manifest(
                root, self.profiles, contract, document
            )
            self.assertIn("manifest-static-invalid", {item.code for item in findings})

        invalid_scope = ExceptionValidationTests.valid(self)
        invalid_scope["scope_paths"] = ["ALL"]
        codes = {
            item.code
            for item in lifecycle.validate_exceptions(
                ExceptionValidationTests.write(self, [invalid_scope]),
                known_codes=frozenset({"directory-budget-warning"}),
                today=datetime.date(2026, 7, 14),
            )
        }
        self.assertIn("exception-scope-invalid", codes)

    def test_exception_nested_types_fail_closed_without_traceback_or_payload(self) -> None:
        marker = "do-not-echo-nested-payload"
        cases: tuple[object, ...] = (
            {marker: "value"},
            [marker],
            True,
            None,
            7,
        )
        for value in cases:
            with self.subTest(value_type=type(value).__name__):
                entry = ExceptionValidationTests.valid(self)
                entry["evidence"] = [value]
                path = ExceptionValidationTests.write(self, [entry])
                findings = lifecycle.validate_exceptions(
                    path,
                    known_codes=frozenset({"directory-budget-warning"}),
                    today=datetime.date(2026, 7, 14),
                )
                rendered = "\n".join(
                    f"{item.code}:{item.path}:{item.message}" for item in findings
                )
                self.assertIn("exception-evidence-invalid", rendered)
                self.assertNotIn(marker, rendered)

    def _impact_fixture(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str, tuple[metadata.Record, ...]]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        bodies = {
            "docs/03.specs/source.md": (
                "---\nstatus: active\nartifact_id: spec:source\n"
                "artifact_type: spec\nparent_ids: [spec:parent]\n---\n\n# Source\n"
            ),
            "docs/03.specs/parent.md": "# Parent\n",
            "docs/03.specs/dependent.md": "# Dependent\n",
            "docs/03.specs/superseder.md": "# Superseder\n",
            "docs/03.specs/link.md": "# Link\n\n[Source](./source.md)\n",
            "docs/03.specs/consumer.md": "# Consumer\n",
            "docs/03.specs/replacement.md": "# Replacement\n",
        }
        for path_text, body in bodies.items():
            target = root / path_text
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        baseline = commit_all(root)
        records = (
            self.record("docs/03.specs/parent.md", artifact_id="spec:parent"),
            self.record(
                "docs/03.specs/dependent.md", parent_ids=["spec:source"]
            ),
            self.record(
                "docs/03.specs/superseder.md", supersedes="spec:source"
            ),
            self.record("docs/03.specs/link.md"),
            self.record("docs/03.specs/consumer.md"),
            self.record(
                "docs/03.specs/replacement.md", artifact_id="spec:replacement"
            ),
        )
        return temporary, root, baseline, records

    def test_deletion_selects_old_path_and_every_direct_relation_class(self) -> None:
        temporary, root, baseline, records = self._impact_fixture()
        self.addCleanup(temporary.cleanup)
        (root / "docs/03.specs/source.md").unlink()
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
            target_path=None,
            artifact_id="spec:source",
            parent_ids=("spec:parent",),
            disposition="delete",
            canonical_replacement="spec:replacement",
            active_consumers=(
                pathlib.PurePosixPath("docs/03.specs/consumer.md"),
            ),
        )
        selected = lifecycle.collect_impacted_records(
            root,
            records,
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            (self.document(baseline, entries=(row,)),),
            base_ref=baseline,
        )
        self.assertEqual(
            {item.path.as_posix() for item in selected},
            {
                "docs/03.specs/parent.md",
                "docs/03.specs/dependent.md",
                "docs/03.specs/superseder.md",
                "docs/03.specs/link.md",
                "docs/03.specs/consumer.md",
                "docs/03.specs/replacement.md",
            },
        )

    def test_rename_diff_is_nul_safe_and_retains_both_paths(self) -> None:
        temporary, root, baseline, records = self._impact_fixture()
        self.addCleanup(temporary.cleanup)
        old = root / "docs/03.specs/source.md"
        new = root / "docs/03.specs/renamed.md"
        old.rename(new)
        current, triggers = lifecycle._changed_path_sets(root, baseline)
        self.assertIn("docs/03.specs/renamed.md", current)
        self.assertIn("docs/03.specs/source.md", triggers)
        self.assertIn("docs/03.specs/renamed.md", triggers)

        renamed = self.record(
            "docs/03.specs/renamed.md",
            artifact_id="spec:source",
            parent_ids=["spec:parent"],
        )
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
            target_path=pathlib.PurePosixPath("docs/03.specs/renamed.md"),
            artifact_id="spec:source",
            parent_ids=("spec:parent",),
            disposition="move",
            active_consumers=(
                pathlib.PurePosixPath("docs/03.specs/consumer.md"),
            ),
        )
        selected = lifecycle.collect_impacted_records(
            root,
            (*records, renamed),
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            (self.document(baseline, entries=(row,)),),
            base_ref=baseline,
        )
        paths = {item.path.as_posix() for item in selected}
        self.assertIn("docs/03.specs/renamed.md", paths)
        self.assertIn("docs/03.specs/link.md", paths)
        self.assertIn("docs/03.specs/parent.md", paths)
        self.assertIn("docs/03.specs/consumer.md", paths)

    def test_introduced_findings_subtract_identical_base_debt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            target = root / "docs/90.references/debt.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Existing debt\n", encoding="utf-8")
            baseline = commit_all(root)
            records = tuple(metadata.collect_records(root, self.profiles, require_git=True))
            findings = lifecycle._introduced_metadata_findings(
                root, records, records, self.profiles, base_ref=baseline
            )
            self.assertEqual(findings, [])

    def test_manifest_attestation_binds_baseline_transition_and_result_truth(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source = root / "docs/90.references/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root)
        source.write_text(
            "---\nstatus: completed\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/90.references/source.md"),
            target_path=pathlib.PurePosixPath("docs/90.references/source.md"),
            artifact_id="reference:source",
            artifact_type="reference",
            status_before="active",
            status_after="completed",
        )
        contract = self.fixture_contract(["docs/90.references/source.md"])

        valid = lifecycle.validate_migration_manifest(
            root, self.profiles, contract, self.document(baseline, entries=(row,))
        )
        binding_codes = {item.code for item in valid}
        self.assertFalse(any("mismatch" in code or "transition" in code for code in binding_codes))

        cases = {
            "baseline-id": (
                dataclasses.replace(row, artifact_id="reference:other"),
                "manifest-baseline-artifact-id-mismatch",
            ),
            "baseline-status": (
                dataclasses.replace(row, status_before="draft"),
                "manifest-baseline-status-mismatch",
            ),
            "reverse-transition": (
                dataclasses.replace(row, status_before="completed", status_after="active"),
                "manifest-transition-invalid",
            ),
            "result-id": (
                row,
                "manifest-target-artifact-id-mismatch",
            ),
        }
        for name, (candidate, expected) in cases.items():
            with self.subTest(case=name):
                if name == "result-id":
                    source.write_text(
                        source.read_text(encoding="utf-8").replace(
                            "reference:source", "reference:other"
                        ),
                        encoding="utf-8",
                    )
                findings = lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(candidate,)),
                )
                self.assertIn(expected, {item.code for item in findings})
                if name == "result-id":
                    source.write_text(
                        source.read_text(encoding="utf-8").replace(
                            "reference:other", "reference:source"
                        ),
                        encoding="utf-8",
                    )

        missing_target = dataclasses.replace(
            row,
            target_path=pathlib.PurePosixPath("docs/90.references/moved.md"),
            disposition="move",
        )
        self.assertIn(
            "manifest-target-missing",
            {
                item.code
                for item in lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(missing_target,)),
                )
            },
        )

        delete = dataclasses.replace(row, target_path=None, disposition="delete")
        self.assertIn(
            "manifest-source-result-present",
            {
                item.code
                for item in lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(delete,)),
                )
            },
        )

    def test_manifest_attestation_allows_legitimate_nullable_readme_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            (root / "README.md").write_text("# Readme\n", encoding="utf-8")
            baseline = commit_all(root)
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("README.md"),
                target_path=pathlib.PurePosixPath("README.md"),
                artifact_id=None,
                artifact_type="readme",
                status_before=None,
                status_after=None,
            )
            findings = lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(["README.md"]),
                self.document(baseline, entries=(row,)),
            )
            self.assertNotIn("manifest-static-invalid", {item.code for item in findings})
            self.assertFalse(any("mismatch" in item.code for item in findings))

    def test_check_full_blocks_warnings_and_safety_is_unsuppressible(self) -> None:
        warning = lifecycle._finding(
            "docs/90.references/debt.md",
            "review-age-unavailable",
            "review evidence is unavailable",
            "warning",
        )
        safety = lifecycle._finding(
            "docs/98.archive/value.md",
            "archive-snapshot-path-mismatch",
            "snapshot path is invalid",
        )
        with mock.patch.object(lifecycle, "_full_findings", return_value=((), [warning])):
            self.assertEqual(lifecycle.main(["--mode", "report-full"]), 0)
            self.assertEqual(lifecycle.main(["--mode", "check-full"]), 1)

        with tempfile.TemporaryDirectory() as directory:
            exceptions = pathlib.Path(directory) / "exceptions.yaml"
            entry = ExceptionValidationTests.valid(self)
            entry["finding_code"] = "archive-snapshot-path-mismatch"
            entry["scope_paths"] = ["docs/98.archive/value.md"]
            exceptions.write_text(
                yaml.safe_dump(
                    {"schema_version": 1, "exceptions": [entry]}, sort_keys=False
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                lifecycle, "_full_findings", return_value=((), [safety])
            ):
                self.assertEqual(
                    lifecycle.main(
                        [
                            "--mode",
                            "check-full",
                            "--exceptions",
                            str(exceptions),
                        ]
                    ),
                    3,
                )
            self.assertTrue(lifecycle._is_safety_finding(safety))

    def test_redaction_covers_all_contract_payload_classes_and_parser_errors(self) -> None:
        samples = (
            b"machine host.example login user password do-not-echo-auth\n",
            b'{"auths":{"registry":{"auth":"do-not-echo-auth"}}}\n',
            b"-----BEGIN ENCRYPTED PRIVATE KEY-----\ndo-not-echo-key\n",
            b"-----BEGIN DSA PRIVATE KEY-----\ndo-not-echo-key\n",
            b"-----BEGIN PGP PRIVATE KEY BLOCK-----\ndo-not-echo-key\n",
            b"sk-do-not-echo-token-1234567890\n",
            b"ghp_do_not_echo_token_1234567890\n",
            b'{"timestamp":"2026-07-14T10:00:00Z","level":"error","message":"do-not-echo-log"}\n',
            b'{"level":"error","message":"do-not-echo-log","timestamp":"2026-07-14T10:00:00Z"}\n',
        )
        for sample in samples:
            with self.subTest(sample=sample.splitlines()[0][:24]):
                self.assertTrue(
                    any(pattern.search(sample) for pattern in lifecycle.SENSITIVE_PAYLOAD_PATTERNS)
                )

        marker = "do-not-echo-yaml-payload"
        with tempfile.TemporaryDirectory() as directory:
            contract = pathlib.Path(directory) / "contract.yaml"
            contract.write_text(f"schema_version: [{marker}\n", encoding="utf-8")
            result = run(
                sys.executable,
                str(SCRIPT),
                "--mode",
                "check-contract",
                "--contract",
                str(contract),
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 3)
            self.assertNotIn(marker, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("configuration-error", result.stderr)

    def test_snapshot_and_manifest_symlinks_cannot_escape_repository(self) -> None:
        temporary, root, record, payload = ArchiveProvenanceTests.archive_fixture(
            self, "immutable-snapshot"
        )
        self.addCleanup(temporary.cleanup)
        snapshot = root / str(record.metadata["snapshot_path"])
        outside = root.parent / f"{root.name}-outside-snapshot"
        outside.write_bytes(payload)
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        snapshot.unlink()
        snapshot.symlink_to(outside)
        self.assertIn(
            "archive-snapshot-file-invalid",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

        manifest_root = root / "manifest-fixture"
        manifest_root.mkdir()
        init_repo(manifest_root)
        source = manifest_root / "docs/03.specs/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: spec:source\n"
            "artifact_type: spec\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(manifest_root, "manifest baseline")
        manifest_relative = "docs/90.references/manifests/foundation.yaml"
        manifest = manifest_root / manifest_relative
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            lifecycle.render_migration_manifest(
                self.document(baseline, entries=(self.valid_row(),))
            ),
            encoding="utf-8",
        )
        commit_all(manifest_root, "track manifest fixture")
        outside_manifest = root.parent / f"{root.name}-outside-manifest"
        outside_manifest.write_bytes(manifest.read_bytes())
        self.addCleanup(lambda: outside_manifest.unlink(missing_ok=True))
        manifest.unlink()
        manifest.symlink_to(outside_manifest)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._load_repo_migration_manifest(manifest_root, manifest_relative)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._repo_manifest_path(manifest_root, outside_manifest)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._repo_manifest_path(
                manifest_root,
                pathlib.Path("../escape.yaml"),
            )
        self.assertIsNone(
            lifecycle._read_regular_repo_bytes(
                manifest_root,
                "../escape.yaml",
                require_tracked=False,
            )
        )

        manifest.unlink()
        manifest_directory = manifest.parent
        manifest_directory.rmdir()
        outside_manifest_directory = root.parent / f"{root.name}-outside-manifest-dir"
        outside_manifest_directory.mkdir()
        self.addCleanup(
            lambda: shutil.rmtree(outside_manifest_directory, ignore_errors=True)
        )
        (outside_manifest_directory / manifest.name).write_bytes(
            outside_manifest.read_bytes()
        )
        manifest_directory.symlink_to(
            outside_manifest_directory,
            target_is_directory=True,
        )
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._load_repo_migration_manifest(manifest_root, manifest_relative)

        snapshot.unlink()
        evidence_dir = snapshot.parent
        evidence_dir.rmdir()
        outside_dir = root.parent / f"{root.name}-outside-dir"
        outside_dir.mkdir()
        self.addCleanup(lambda: shutil.rmtree(outside_dir, ignore_errors=True))
        (outside_dir / snapshot.name).write_bytes(payload)
        evidence_dir.symlink_to(outside_dir, target_is_directory=True)
        self.assertIn(
            "archive-snapshot-file-invalid",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

    def test_unicode_title_normalization_preserves_multilingual_alphanumerics(self) -> None:
        pairs = (
            ("# 운영 가이드\n", "# 운영-가이드\n"),
            ("# Café Guide\n", "# CAFE\u0301-guide\n"),
        )
        for index, (left_body, right_body) in enumerate(pairs):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                left = root / f"docs/90.references/{index}-left.md"
                right = root / f"docs/90.references/{index}-right.md"
                left.parent.mkdir(parents=True)
                left.write_text(left_body, encoding="utf-8")
                right.write_text(right_body, encoding="utf-8")
                records = (
                    self.record(left.relative_to(root).as_posix(), "reference"),
                    self.record(right.relative_to(root).as_posix(), "reference"),
                )
                candidates = lifecycle.find_duplicate_candidates(root, records)
                self.assertEqual(len(candidates), 1)
                self.assertIn("normalized-title", candidates[0].signals)

    def test_declared_manifests_load_in_registry_order_and_fail_before_use(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first_path = "docs/90.references/manifests/zeta.yaml"
            second_path = "docs/90.references/manifests/alpha.yaml"
            for path_text in (first_path, second_path):
                target = root / path_text
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture\n", encoding="utf-8")
            contract = self.fixture_contract(
                ["docs/03.specs/source.md"],
                wave="zeta",
                manifest_path=first_path,
            )
            contract["waves"]["alpha"] = {
                "enforcement": "advisory",
                "manifest_path": second_path,
                "scope_state": "approved",
                "source_paths": ["docs/03.specs/source.md"],
                "declared_outputs": [],
            }
            first = self.document("a" * 40, wave="zeta")
            calls: list[str] = []

            def load_declared(
                _root: pathlib.Path,
                relative_path: str,
            ) -> lifecycle.MigrationManifestDocument:
                calls.append(relative_path)
                if relative_path == second_path:
                    raise lifecycle.ProfileError("invalid declared manifest")
                return first

            with (
                mock.patch.object(
                    lifecycle,
                    "_load_repo_migration_manifest",
                    side_effect=load_declared,
                ),
                mock.patch.object(
                    lifecycle,
                    "validate_migration_manifest",
                    return_value=[],
                ),
                mock.patch.object(
                    lifecycle,
                    "_repo_manifest_matches",
                    return_value=True,
                ),
            ):
                documents, findings = lifecycle._load_declared_manifests(
                    root,
                    self.profiles,
                    contract,
                    promoted_only=False,
                )
            self.assertEqual(calls, [first_path, second_path])
            self.assertEqual(documents, (first,))
            self.assertIn(
                "promoted-manifest-file-invalid",
                {item.code for item in findings},
            )

        safety = lifecycle._finding(
            second_path,
            "promoted-manifest-file-invalid",
            "declared manifest is invalid",
        )
        with (
            mock.patch.object(
                lifecycle,
                "_load_declared_manifests",
                return_value=((), [safety]),
            ),
            mock.patch.object(lifecycle, "_collect_records") as collect_records,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(
                lifecycle.main(["--mode", "check-impacted", "--base-ref", "HEAD"]),
                3,
            )
        collect_records.assert_not_called()

    def test_all_sixteen_modes_have_table_driven_shape_contracts(self) -> None:
        valid_arguments: dict[str, list[str]] = {
            "check-contract": [],
            "generate-manifest": ["--wave", "foundation", "--base-ref", "HEAD", "--output", "out"],
            "check-manifest": ["--wave", "foundation", "--manifest", "manifest"],
            "check-promoted": [],
            "generate-summary": ["--manifest", "manifest", "--output", "out"],
            "check-summary": ["--manifest", "manifest", "--output", "out"],
            "check-impacted": ["--base-ref", "HEAD"],
            "report-duplicates": ["--output", "out"],
            "report-full": [],
            "check-full": [],
            "check-archive": [],
            "check-directory-budget": [],
            "generate-archive-ledger": ["--output", "out"],
            "check-archive-ledger": ["--output", "out"],
            "generate-snapshot-manifest": ["--output", "out"],
            "check-snapshot-manifest": ["--output", "out"],
        }
        self.assertEqual(tuple(valid_arguments), lifecycle.MODES)
        for mode, extra in valid_arguments.items():
            with self.subTest(mode=mode):
                parser = lifecycle._parser()
                args = parser.parse_args(["--mode", mode, *extra])
                lifecycle._validate_cli_shape(parser, args)
                if extra:
                    broken = ["--mode", mode, *extra[2:]]
                else:
                    broken = ["--mode", mode, "--wave", "forbidden"]
                with self.assertRaises(SystemExit) as raised:
                    parser = lifecycle._parser()
                    with contextlib.redirect_stderr(io.StringIO()):
                        lifecycle._validate_cli_shape(parser, parser.parse_args(broken))
                self.assertEqual(raised.exception.code, 2)

    def test_all_sixteen_modes_have_success_and_write_boundary_matrix(self) -> None:
        mode_contracts: dict[str, tuple[list[str], bool]] = {
            "check-contract": ([], False),
            "generate-manifest": (
                ["--wave", "fixture", "--base-ref", "HEAD", "--output", "{output}"],
                True,
            ),
            "check-manifest": (
                ["--wave", "fixture", "--manifest", "docs/manifest.yaml"],
                False,
            ),
            "check-promoted": ([], False),
            "generate-summary": (
                ["--manifest", "docs/manifest.yaml", "--output", "{output}"],
                True,
            ),
            "check-summary": (
                ["--manifest", "docs/manifest.yaml", "--output", "{output}"],
                False,
            ),
            "check-impacted": (["--base-ref", "HEAD"], False),
            "report-duplicates": (["--output", "{output}"], True),
            "report-full": ([], False),
            "check-full": ([], False),
            "check-archive": ([], False),
            "check-directory-budget": ([], False),
            "generate-archive-ledger": (["--output", "{output}"], True),
            "check-archive-ledger": (["--output", "{output}"], False),
            "generate-snapshot-manifest": (["--output", "{output}"], True),
            "check-snapshot-manifest": (["--output", "{output}"], False),
        }
        self.assertEqual(tuple(mode_contracts), lifecycle.MODES)
        write_modes = {mode for mode, (_, writes) in mode_contracts.items() if writes}
        self.assertEqual(
            write_modes,
            {
                "generate-manifest",
                "generate-summary",
                "report-duplicates",
                "generate-archive-ledger",
                "generate-snapshot-manifest",
            },
        )
        contract = copy.deepcopy(self.contract)
        document = self.document("a" * 40)
        for mode, (raw_extra, writes) in mode_contracts.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                output = root / f"{mode}.out"
                extra = [value.format(output=output) for value in raw_extra]
                if "--output" in extra and not writes:
                    output.write_bytes(b"sentinel")
                with (
                    mock.patch.object(
                        lifecycle,
                        "load_migration_contract",
                        return_value=contract,
                    ),
                    mock.patch.object(
                        lifecycle.metadata,
                        "load_profiles",
                        return_value=self.profiles,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "generate_manifest_skeleton",
                        return_value=document,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_load_candidate_migration_manifest",
                        return_value=document,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "validate_migration_manifest",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_candidate_manifest_matches",
                        return_value=True,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_load_declared_manifests",
                        return_value=((), []),
                    ),
                    mock.patch.object(lifecycle, "_collect_records", return_value=()),
                    mock.patch.object(
                        lifecycle,
                        "collect_impacted_records",
                        return_value=(),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_introduced_metadata_findings",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_added_record_paths",
                        return_value=frozenset(),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_full_findings",
                        return_value=((), []),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "validate_directory_budgets",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "find_duplicate_candidates",
                        return_value=(),
                    ),
                    mock.patch.object(lifecycle, "_check_output", return_value=True),
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()),
                ):
                    result = lifecycle.main(
                        ["--root", str(root), "--mode", mode, *extra]
                    )
                self.assertEqual(result, 0)
                if writes:
                    self.assertTrue(output.is_file())
                elif "--output" in extra:
                    self.assertEqual(output.read_bytes(), b"sentinel")
                else:
                    self.assertFalse(output.exists())

    def test_all_sixteen_modes_have_explicit_exit_class_matrix(self) -> None:
        arguments = {
            "check-contract": [],
            "generate-manifest": [
                "--wave",
                "fixture",
                "--base-ref",
                "HEAD",
                "--output",
                "{output}",
            ],
            "check-manifest": [
                "--wave",
                "fixture",
                "--manifest",
                "docs/manifest.yaml",
            ],
            "check-promoted": [],
            "generate-summary": [
                "--manifest",
                "docs/manifest.yaml",
                "--output",
                "{output}",
            ],
            "check-summary": [
                "--manifest",
                "docs/manifest.yaml",
                "--output",
                "{output}",
            ],
            "check-impacted": ["--base-ref", "HEAD"],
            "report-duplicates": ["--output", "{output}"],
            "report-full": [],
            "check-full": [],
            "check-archive": [],
            "check-directory-budget": [],
            "generate-archive-ledger": ["--output", "{output}"],
            "check-archive-ledger": ["--output", "{output}"],
            "generate-snapshot-manifest": ["--output", "{output}"],
            "check-snapshot-manifest": ["--output", "{output}"],
        }
        ordinary_exits = {
            "check-contract": 0,
            "generate-manifest": 0,
            "check-manifest": 1,
            "check-promoted": 1,
            "generate-summary": 1,
            "check-summary": 1,
            "check-impacted": 1,
            "report-duplicates": 0,
            "report-full": 0,
            "check-full": 1,
            "check-archive": 1,
            "check-directory-budget": 1,
            "generate-archive-ledger": 1,
            "check-archive-ledger": 1,
            "generate-snapshot-manifest": 1,
            "check-snapshot-manifest": 1,
        }
        self.assertEqual(tuple(arguments), lifecycle.MODES)
        self.assertEqual(tuple(ordinary_exits), lifecycle.MODES)
        contract = copy.deepcopy(self.contract)
        document = self.document("a" * 40)
        archive = self.record("docs/98.archive/item.md", "archive")

        for mode in lifecycle.MODES:
            for safety_case in (False, True):
                with (
                    self.subTest(mode=mode, safety=safety_case),
                    tempfile.TemporaryDirectory() as directory,
                    contextlib.ExitStack() as stack,
                ):
                    root = pathlib.Path(directory)
                    output = root / f"{mode}.out"
                    extra = [
                        value.format(output=output) for value in arguments[mode]
                    ]
                    finding = (
                        lifecycle._finding(
                            archive.path.as_posix(),
                            "archive-snapshot-file-invalid",
                            "safety failure",
                        )
                        if safety_case
                        else lifecycle._finding(
                            archive.path.as_posix(),
                            "directory-budget-blocked",
                            "ordinary blocking finding",
                        )
                    )
                    if mode == "check-contract" and safety_case:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "load_migration_contract",
                                side_effect=lifecycle.ProfileError("invalid contract"),
                            )
                        )
                    else:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "load_migration_contract",
                                return_value=contract,
                            )
                        )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle.metadata,
                            "load_profiles",
                            return_value=self.profiles,
                        )
                    )
                    if mode == "generate-manifest" and safety_case:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "generate_manifest_skeleton",
                                side_effect=lifecycle.ProfileError("unsafe baseline"),
                            )
                        )
                    else:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "generate_manifest_skeleton",
                                return_value=document,
                            )
                        )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_load_candidate_migration_manifest",
                            return_value=document,
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_migration_manifest",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_candidate_manifest_matches",
                            return_value=True,
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_load_declared_manifests",
                            return_value=((), [finding]),
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_full_findings",
                            return_value=((archive,), [finding]),
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_archive_provenance",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_directory_budgets",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(lifecycle, "_check_output", return_value=True)
                    )
                    stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
                    stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
                    result = lifecycle.main(
                        ["--root", str(root), "--mode", mode, *extra]
                    )
                    expected = 3 if safety_case else ordinary_exits[mode]
                    self.assertEqual(result, expected)


class FinalReviewRemediationTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "task",
        **metadata_values: object,
    ) -> metadata.Record:
        values: dict[str, object] = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def _invoke_corpus_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--mode",
            mode,
        ]
        if mode == "check-impacted":
            arguments.extend(("--base-ref", "HEAD"))
        if mode in {
            "report-duplicates",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        }:
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def test_corpus_modes_reject_final_and_intermediate_markdown_symlinks_without_leakage(
        self,
    ) -> None:
        marker = "outside-corpus-payload-marker"
        modes = (
            "report-full",
            "check-full",
            "report-duplicates",
            "check-impacted",
            "check-archive",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        )
        for attack in ("final", "intermediate"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                outside = fixture / "outside"
                root.mkdir()
                outside.mkdir()
                init_repo(root)
                outside_body = (
                    "---\nstatus: active\nartifact_id: reference:outside\n"
                    f"artifact_type: reference\nparent_ids: [{marker}]\n---\n\n# Outside\n"
                )
                relative = pathlib.PurePosixPath(
                    "docs/90.references/link.md"
                    if attack == "final"
                    else "docs/90.references/nested/link.md"
                )
                target = root / relative
                target.parent.mkdir(parents=True)
                if attack == "final":
                    outside_file = outside / "link.md"
                    outside_file.write_text(outside_body, encoding="utf-8")
                    target.symlink_to(outside_file)
                    commit_all(root, "track final symlink")
                else:
                    target.write_text("# Safe baseline\n", encoding="utf-8")
                    commit_all(root, "track regular file")
                    shutil.rmtree(target.parent)
                    (outside / "link.md").write_text(outside_body, encoding="utf-8")
                    target.parent.symlink_to(outside, target_is_directory=True)

                for mode in modes:
                    with self.subTest(attack=attack, mode=mode):
                        output = fixture / f"{attack}-{mode}.out"
                        check_mode = mode.startswith("check-") and mode.endswith(
                            ("ledger", "manifest")
                        )
                        if check_mode:
                            output.write_bytes(b"sentinel")
                        result = self._invoke_corpus_mode(root, mode, output)
                        rendered = result.stdout + result.stderr
                        self.assertEqual(result.returncode, 3, rendered)
                        self.assertNotIn(marker, rendered)
                        self.assertNotIn("Traceback", rendered)
                        if check_mode:
                            self.assertEqual(output.read_bytes(), b"sentinel")
                        else:
                            self.assertFalse(output.exists())

    def _archive_fixture(
        self,
    ) -> tuple[
        tempfile.TemporaryDirectory[str],
        pathlib.Path,
        str,
        lifecycle.MigrationManifestRow,
        pathlib.Path,
    ]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root, "archive source baseline")
        blob = git(root, "rev-parse", f"{baseline}:{source_relative.as_posix()}")
        source.unlink()
        replacement = root / "docs/90.references/data/replacement.md"
        replacement.parent.mkdir(parents=True, exist_ok=True)
        replacement.write_text(
            "---\nstatus: active\nartifact_id: reference:replacement\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n"
            "# Replacement\n\n## Overview\nCurrent replacement.\n\n"
            "## Purpose\nCanonical replacement.\n\n## Scope\nCurrent scope.\n\n"
            "## Facts and Definitions\nReplacement truth.\n\n"
            "## Sources\nRepository evidence.\n\n## Maintenance\nActive.\n\n"
            "## Related Documents\nNone.\n",
            encoding="utf-8",
        )
        commit_all(root, "track canonical replacement")
        target_relative = pathlib.PurePosixPath(
            "docs/98.archive/90.references/source.md"
        )
        target = root / target_relative
        target.parent.mkdir(parents=True)
        archive_metadata: dict[str, object] = {
            "status": "archived",
            "artifact_id": "reference:source",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": source_relative.as_posix(),
            "archived_on": "2026-07-14",
            "archive_reason": "Superseded by the canonical replacement.",
            "archive_disposition": "superseded",
            "archived_commit": baseline,
            "archived_blob": blob,
            "preservation_class": "git-history",
            "current_replacement": "docs/90.references/data/replacement.md",
        }
        target.write_text(
            "---\n"
            + yaml.safe_dump(archive_metadata, sort_keys=False)
            + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        row = self.valid_row(
            source_path=source_relative,
            target_path=target_relative,
            artifact_id="reference:source",
            artifact_type="reference",
            status_before="active",
            status_after="archived",
            parent_ids=(),
            disposition="archive",
            canonical_replacement="docs/90.references/data/replacement.md",
            active_consumers=(),
            preservation_class="git-history",
            evidence=lifecycle.ManifestEvidence(
                ("git show baseline source",),
                ("docs/90.references/source.md",),
                (pathlib.PurePosixPath("docs/90.references/source.md"),),
                ("verified no active consumers",),
                ("revert archive commit",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        return temporary, root, baseline, row, target

    def _archive_codes(
        self,
        root: pathlib.Path,
        baseline: str,
        row: lifecycle.MigrationManifestRow,
    ) -> set[str]:
        return {
            item.code
            for item in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract([row.source_path.as_posix()]),
                self.document(baseline, entries=(row,)),
            )
        }

    def test_archive_disposition_binds_source_to_canonical_validated_tombstone(
        self,
    ) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(self._archive_codes(root, baseline, row), set())

        original = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])
        cases: dict[str, tuple[dict[str, object], lifecycle.MigrationManifestRow, str]] = {
            "source": (
                {"archived_from": "docs/90.references/other.md"},
                row,
                "manifest-archive-source-mismatch",
            ),
            "type": (
                {"artifact_type": "reference"},
                row,
                "manifest-archive-target-profile-invalid",
            ),
            "status": (
                {"status": "active"},
                dataclasses.replace(row, status_after="active"),
                "manifest-archive-status-invalid",
            ),
            "parents": (
                {"parent_ids": ["reference:parent"]},
                row,
                "manifest-target-parent-ids-mismatch",
            ),
            "replacement": (
                {"current_replacement": "docs/90.references/other.md"},
                row,
                "manifest-archive-replacement-mismatch",
            ),
            "preservation": (
                {"preservation_class": "immutable-snapshot"},
                row,
                "manifest-archive-preservation-mismatch",
            ),
            "reviews": (
                {},
                dataclasses.replace(
                    row,
                    review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
                ),
                "manifest-destructive-review-required",
            ),
        }
        for name, (changes, candidate, expected) in cases.items():
            with self.subTest(case=name):
                target_metadata = {**original, **changes}
                target.write_text(
                    "---\n"
                    + yaml.safe_dump(target_metadata, sort_keys=False)
                    + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                codes = self._archive_codes(root, baseline, candidate)
                self.assertIn(expected, codes)
                if name != "reviews":
                    self.assertIn("manifest-transition-invalid", codes)
        target.write_text(
            "---\n" + yaml.safe_dump(original, sort_keys=False) + "---\n",
            encoding="utf-8",
        )
        non_archive = dataclasses.replace(
            row,
            source_path=pathlib.PurePosixPath("docs/98.archive/90.references/source.md"),
            target_path=pathlib.PurePosixPath("docs/98.archive/90.references/source.md"),
            artifact_type="archive",
            status_before="archived",
            status_after="active",
            disposition="preserve",
            canonical_replacement=None,
            preservation_class=None,
            evidence=lifecycle.ManifestEvidence((), (), (), (), ()),
            review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
        )
        reverse_contract = self.fixture_contract([non_archive.source_path.as_posix()])
        reverse_document = self.document(
            baseline,
            entries=(non_archive,),
        )
        reverse_contract["waves"]["fixture"]["source_paths"] = [
            non_archive.source_path.as_posix()
        ]
        reverse_codes = {
            item.code
            for item in lifecycle.validate_migration_manifest(
                root, self.profiles, reverse_contract, reverse_document
            )
        }
        self.assertIn("manifest-transition-invalid", reverse_codes)

    def test_archive_binds_manifest_baseline_blob_and_dynamic_replacement_truth(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        original_text = target.read_text(encoding="utf-8")
        original = yaml.safe_load(original_text.split("---", 2)[1])

        archived_bytes = run(
            "git",
            "cat-file",
            "blob",
            str(original["archived_blob"]),
            cwd=root,
        ).stdout.encode("utf-8")
        digest = hashlib.sha256(archived_bytes).hexdigest()
        snapshot_relative = pathlib.PurePosixPath(
            f"docs/98.archive/evidence/{digest}.md.snapshot"
        )
        snapshot = root / snapshot_relative
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(archived_bytes)
        immutable_values = {
            **original,
            "archive_disposition": "evidence-preserve",
            "preservation_class": "immutable-snapshot",
            "snapshot_path": snapshot_relative.as_posix(),
            "content_sha256": digest,
            "snapshot_reason": "Preserve exact evidence bytes.",
        }
        target.write_text(
            "---\n"
            + yaml.safe_dump(immutable_values, sort_keys=False)
            + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        commit_all(root, "track immutable archive snapshot")
        immutable_row = dataclasses.replace(
            row, preservation_class="immutable-snapshot"
        )
        self.assertEqual(self._archive_codes(root, baseline, immutable_row), set())
        target.write_text(original_text, encoding="utf-8")

        source_path = row.source_path.as_posix()
        newer_source = root / source_path
        newer_source.parent.mkdir(parents=True, exist_ok=True)
        newer_source.write_text(
            "---\nstatus: active\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n"
            "# Source\n\nUnique newer baseline evidence.\n",
            encoding="utf-8",
        )
        newer_baseline = commit_all(root, "newer source boundary")
        newer_source.unlink()
        git(root, "add", "-u")
        self.assertIn(
            "manifest-archive-baseline-blob-mismatch",
            self._archive_codes(root, newer_baseline, row),
        )
        self.assertNotIn(
            "manifest-archive-baseline-blob-mismatch",
            self._archive_codes(root, baseline, row),
        )

        variants = {
            "superseded": "docs/90.references/data/replacement.md",
            "duplicate": "docs/90.references/data/replacement.md",
            "conflict": "docs/90.references/data/replacement.md",
            "withdrawn": None,
            "evidence-preserve": None,
        }
        for disposition, replacement in variants.items():
            with self.subTest(disposition=disposition):
                values = {
                    **original,
                    "archive_disposition": disposition,
                }
                if replacement is None:
                    values.pop("current_replacement", None)
                else:
                    values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, canonical_replacement=replacement)
                self.assertEqual(self._archive_codes(root, baseline, candidate), set())

        invalid = {
            "superseded": None,
            "duplicate": None,
            "conflict": None,
            "withdrawn": "docs/90.references/data/replacement.md",
        }
        for disposition, replacement in invalid.items():
            with self.subTest(invalid_disposition=disposition):
                values = {**original, "archive_disposition": disposition}
                if replacement is None:
                    values.pop("current_replacement", None)
                else:
                    values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, canonical_replacement=replacement)
                codes = self._archive_codes(root, baseline, candidate)
                self.assertTrue(
                    {"manifest-replacement-required", "manifest-replacement-forbidden"}
                    & codes,
                    (disposition, codes),
                )

    def test_archive_replacement_resolves_unique_current_canonical_document(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        values = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])

        self.assertEqual(self._archive_codes(root, baseline, row), set())

        cases = {
            "missing": "docs/90.references/missing.md",
            "untracked": "docs/90.references/untracked.md",
            "self": row.source_path.as_posix(),
            "target": row.target_path.as_posix(),
        }
        (root / "docs/90.references/untracked.md").write_text(
            (root / "docs/90.references/data/replacement.md").read_text(encoding="utf-8")
            .replace("reference:replacement", "reference:untracked"),
            encoding="utf-8",
        )
        for name, replacement in cases.items():
            with self.subTest(case=name):
                values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                codes = self._archive_codes(
                    root,
                    baseline,
                    dataclasses.replace(row, canonical_replacement=replacement),
                )
                self.assertIn("manifest-replacement-invalid", codes)

        replacement_path = root / "docs/90.references/data/replacement.md"
        canonical = replacement_path.read_text(encoding="utf-8")
        outside = pathlib.Path(temporary.name).parent / (
            pathlib.Path(temporary.name).name + "-outside-replacement"
        )
        outside.write_text(canonical, encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        replacement_path.unlink()
        replacement_path.symlink_to(outside)
        values["current_replacement"] = "docs/90.references/data/replacement.md"
        target.write_text(
            "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        with self.assertRaises(lifecycle._CorpusSafetyError):
            self._archive_codes(root, baseline, row)
        replacement_path.unlink()
        replacement_path.write_text(canonical, encoding="utf-8")
        for name, mutation in {
            "wrong-profile": canonical.replace(
                "artifact_type: reference", "artifact_type: archive"
            ),
            "wrong-status": canonical.replace("status: active", "status: draft"),
            "wrong-body": canonical.replace("## Sources", "### Sources"),
        }.items():
            with self.subTest(case=name):
                replacement_path.write_text(mutation, encoding="utf-8")
                values["current_replacement"] = "docs/90.references/data/replacement.md"
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._archive_codes(root, baseline, row),
                )
        replacement_path.write_text(canonical, encoding="utf-8")
        duplicate = root / "docs/90.references/data/duplicate.md"
        duplicate.parent.mkdir(parents=True, exist_ok=True)
        duplicate.write_text(canonical, encoding="utf-8")
        commit_all(root, "duplicate replacement identity")
        values["current_replacement"] = "reference:replacement"
        target.write_text(
            "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._archive_codes(
                root,
                baseline,
                dataclasses.replace(
                    row, canonical_replacement="reference:replacement"
                ),
            ),
        )

    def _partition_fixture(
        self,
        *,
        plan_state: str,
        reviews: lifecycle.ReviewVerdict = lifecycle.ReviewVerdict("pass", "pass"),
    ) -> tuple[
        tempfile.TemporaryDirectory[str],
        pathlib.Path,
        str,
        lifecycle.MigrationManifestRow,
        tuple[metadata.Record, ...],
    ]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath(
            "docs/04.execution/tasks/149.md"
        )
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: task:149\nartifact_type: task\n"
            "parent_ids: [plan:partition]\n---\n\n# Task: New Leaf\n",
            encoding="utf-8",
        )
        baseline = commit_all(root, "partition baseline")
        plan_relative = pathlib.PurePosixPath(
            "docs/04.execution/plans/2026-partition.md"
        )
        plan = root / plan_relative
        plan.parent.mkdir(parents=True, exist_ok=True)
        parent = root / "docs/03.specs/partition/spec.md"
        parent.parent.mkdir(parents=True, exist_ok=True)
        parent.write_text(
            "---\nstatus: active\nartifact_id: spec:partition\n"
            "artifact_type: spec\nparent_ids: [spec:root]\n---\n\n# Partition Spec\n",
            encoding="utf-8",
        )
        valid_plan = (
            "---\nstatus: active\nartifact_id: plan:partition\n"
            "artifact_type: plan\nparent_ids: [spec:partition]\n---\n\n"
            "# Document Partition Plan\n\n"
            "## Overview\nPartition approval.\n\n"
            "## Context and Inputs\nValidated corpus.\n\n"
            "## Goals and Non-goals\nBounded partition.\n\n"
            "## Work Breakdown\nApply the partition.\n\n"
            "## Verification Plan\nRun lifecycle validation.\n\n"
            "## Risks and Rollback\nRevert the migration commit.\n\n"
            "## Completion Criteria\nAll budgets pass.\n\n"
            "## Related Documents\nParent Spec.\n"
        )
        if plan_state == "missing":
            pass
        elif plan_state == "untracked":
            plan.write_text(valid_plan, encoding="utf-8")
        elif plan_state == "wrong-profile":
            plan.write_text(
                valid_plan.replace("artifact_type: plan", "artifact_type: spec"),
                encoding="utf-8",
            )
            commit_all(root, "track wrong-profile plan")
        elif plan_state == "draft":
            plan.write_text(
                valid_plan.replace("status: active", "status: draft"),
                encoding="utf-8",
            )
            commit_all(root, "track draft plan")
        elif plan_state in {"tracked", "symlink"}:
            plan.write_text(valid_plan, encoding="utf-8")
            commit_all(root, "track partition plan")
            if plan_state == "symlink":
                outside = pathlib.Path(temporary.name).parent / (
                    pathlib.Path(temporary.name).name + "-outside-plan"
                )
                outside.write_text("outside-plan-marker\n", encoding="utf-8")
                self.addCleanup(lambda: outside.unlink(missing_ok=True))
                plan.unlink()
                plan.symlink_to(outside)
        else:
            raise AssertionError(plan_state)
        row = self.valid_row(
            source_path=source_relative,
            target_path=source_relative,
            artifact_id="task:149",
            artifact_type="task",
            status_before="active",
            status_after="active",
            parent_ids=("plan:partition",),
            partition_plan=plan_relative,
            review_verdict=reviews,
        )
        records = tuple(
            self.record(
                f"docs/04.execution/tasks/{index:03}.md",
                "task",
                artifact_id=f"task:{index:03}",
            )
            for index in range(150)
        )
        return temporary, root, baseline, row, records

    def test_partition_approval_requires_tracked_canonical_reviewed_plan(self) -> None:
        cases = {
            "missing": "manifest-partition-plan-invalid",
            "untracked": "manifest-partition-plan-invalid",
            "symlink": "manifest-partition-plan-invalid",
            "wrong-profile": "manifest-partition-plan-profile-invalid",
            "draft": "manifest-partition-plan-status-invalid",
            "unreviewed": "manifest-partition-plan-review-required",
        }
        for name, expected in cases.items():
            state = "tracked" if name == "unreviewed" else name
            reviews = (
                lifecycle.ReviewVerdict("pending", "pending")
                if name == "unreviewed"
                else lifecycle.ReviewVerdict("pass", "pass")
            )
            temporary, root, baseline, row, records = self._partition_fixture(
                plan_state=state,
                reviews=reviews,
            )
            try:
                contract = self.fixture_contract([row.source_path.as_posix()])
                document = self.document(baseline, entries=(row,))
                codes = {
                    item.code
                    for item in lifecycle.validate_migration_manifest(
                        root, self.profiles, contract, document
                    )
                }
                self.assertIn(expected, codes, name)
                applied = lifecycle._apply_partition_approvals(
                    records,
                    (document,),
                    root=root,
                    profiles=self.profiles,
                )
                findings = lifecycle.validate_directory_budgets(
                    applied,
                    added_paths=frozenset(
                        {pathlib.PurePosixPath("docs/04.execution/tasks/149.md")}
                    ),
                    warning_at=100,
                    block_new_leaf_at=150,
                    enforce_all=False,
                )
                self.assertIn("directory-budget-blocked", {item.code for item in findings})
            finally:
                temporary.cleanup()

        temporary, root, baseline, row, records = self._partition_fixture(
            plan_state="tracked"
        )
        self.addCleanup(temporary.cleanup)
        contract = self.fixture_contract([row.source_path.as_posix()])
        document = self.document(baseline, entries=(row,))
        self.assertFalse(
            any(
                item.code.startswith("manifest-partition-plan-")
                for item in lifecycle.validate_migration_manifest(
                    root, self.profiles, contract, document
                )
            )
        )
        applied = lifecycle._apply_partition_approvals(
            records,
            (document,),
            root=root,
            profiles=self.profiles,
        )
        approved = lifecycle.validate_directory_budgets(
            applied,
            added_paths=frozenset(
                {pathlib.PurePosixPath("docs/04.execution/tasks/149.md")}
            ),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in approved})

    def test_partition_plan_uses_canonical_metadata_relations_and_body_role(self) -> None:
        temporary, root, _baseline, row, _records = self._partition_fixture(
            plan_state="tracked"
        )
        self.addCleanup(temporary.cleanup)
        plan = root / row.partition_plan.as_posix()
        canonical = plan.read_text(encoding="utf-8")
        wrong_parent = root / "docs/90.references/data/wrong-parent.md"
        wrong_parent.parent.mkdir(parents=True, exist_ok=True)
        wrong_parent.write_text(
            "---\nstatus: active\nartifact_id: reference:wrong-parent\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Wrong Parent\n",
            encoding="utf-8",
        )
        commit_all(root, "track wrong parent type")
        cases = {
            "invalid-optional": canonical.replace(
                "parent_ids: [spec:partition]",
                "parent_ids: [spec:partition]\nsupersedes: invalid-scalar",
            ),
            "unresolved-parent": canonical.replace(
                "parent_ids: [spec:partition]", "parent_ids: [spec:missing]"
            ),
            "self-parent": canonical.replace(
                "parent_ids: [spec:partition]", "parent_ids: [plan:partition]"
            ),
            "wrong-parent-type": canonical.replace(
                "parent_ids: [spec:partition]",
                "parent_ids: [reference:wrong-parent]",
            ),
            "frontmatter-order": canonical.replace(
                "status: active\nartifact_id: plan:partition\nartifact_type: plan",
                "artifact_type: plan\nstatus: active\nartifact_id: plan:partition",
            ),
            "placeholder": canonical.replace(
                "Partition approval.", "{{overview}}"
            ),
            "missing-heading": canonical.replace("## Work Breakdown", "### Work Breakdown"),
            "forbidden-heading": canonical + "\n## Verification Evidence\nNot permitted.\n",
        }
        for name, candidate in cases.items():
            with self.subTest(case=name):
                plan.write_text(candidate, encoding="utf-8")
                codes = {
                    item.code
                    for item in lifecycle._partition_plan_findings(
                        root, self.profiles, row
                    )
                }
                self.assertIn("manifest-partition-plan-profile-invalid", codes)
        plan.write_text(canonical, encoding="utf-8")
        self.assertEqual(
            lifecycle._partition_plan_findings(root, self.profiles, row), []
        )

    def test_directory_budget_counts_only_immediate_eligible_markdown_leaves(self) -> None:
        records = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md")
            for index in range(99)
        ) + (
            self.record("docs/04.execution/tasks/README.md", "readme"),
            self.record("docs/04.execution/tasks/generated.md", "generated"),
            self.record("docs/04.execution/tasks/repo-support.md", "repo-support"),
            self.record("docs/04.execution/tasks/unsupported.md", "unsupported"),
            self.record("docs/04.execution/tasks/not-markdown.txt", "task"),
            self.record("docs/04.execution/tasks/2026/nested.md", "task"),
        )
        findings = lifecycle.validate_directory_budgets(
            records,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertFalse(
            any(
                item.path == "docs/04.execution/tasks"
                and item.code == "directory-budget-warning"
                for item in findings
            )
        )

    def test_impacted_cli_snapshots_safe_untracked_records_and_blocks_150th_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
            baseline = git(root, "rev-parse", "HEAD")
            candidate = root / "docs/90.references/data/new.md"
            candidate.parent.mkdir(parents=True)
            valid = (
                "---\nstatus: active\nartifact_id: reference:new\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# New Reference\n"
            )
            candidate.write_text(valid, encoding="utf-8")
            accepted = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "check-impacted",
                "--base-ref",
                baseline,
                cwd=ROOT,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            self.assertIn("selected=1 violations=0", accepted.stdout)
            candidate.write_text(
                valid.replace("status: active", "status: invalid-status"),
                encoding="utf-8",
            )
            rejected = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "check-impacted",
                "--base-ref",
                baseline,
                cwd=ROOT,
            )
            self.assertEqual(rejected.returncode, 1, rejected.stdout + rejected.stderr)
            self.assertIn("selected=1 violations=", rejected.stdout)

        for attack in ("final", "intermediate"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                outside = fixture / "outside"
                root.mkdir()
                outside.mkdir()
                init_repo(root)
                git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
                marker = "outside-untracked-marker"
                (outside / "leak.md").write_text(marker, encoding="utf-8")
                target = root / "docs/90.references/data/leak.md"
                target.parent.mkdir(parents=True)
                if attack == "final":
                    target.symlink_to(outside / "leak.md")
                else:
                    target.parent.joinpath("nested").symlink_to(
                        outside, target_is_directory=True
                    )
                result = run(
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    "check-impacted",
                    "--base-ref",
                    "HEAD",
                    cwd=ROOT,
                )
                rendered = result.stdout + result.stderr
                self.assertEqual(result.returncode, 3, rendered)
                self.assertNotIn(marker, rendered)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            budget = root / "docs/90.references/data/budget"
            budget.mkdir(parents=True)
            for index in range(148):
                (budget / f"{index:03}.md").write_text(
                    "---\nstatus: active\n"
                    f"artifact_id: reference:budget-{index:03}\n"
                    "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                    encoding="utf-8",
                )
            base_148 = commit_all(root, "148 leaves")
            leaf_149 = budget / "148.md"
            leaf_149.write_text(
                "---\nstatus: active\nartifact_id: reference:budget-148\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                encoding="utf-8",
            )
            before_limit = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "check-impacted",
                "--base-ref",
                base_148,
                cwd=ROOT,
            )
            self.assertEqual(before_limit.returncode, 0, before_limit.stdout + before_limit.stderr)
            base_149 = commit_all(root, "149 leaves")
            (budget / "149.md").write_text(
                "---\nstatus: active\nartifact_id: reference:budget-149\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                encoding="utf-8",
            )
            at_limit = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "check-impacted",
                "--base-ref",
                base_149,
                cwd=ROOT,
            )
            self.assertEqual(at_limit.returncode, 1, at_limit.stdout + at_limit.stderr)
            self.assertIn("directory-budget-blocked", at_limit.stdout)

    def test_cli_diagnostics_never_emit_metadata_payloads_across_modes(self) -> None:
        cases = (
            ("report-full", "sk-do-not-echo-1234567890"),
            ("check-full", "password=do-not-echo"),
            ("check-impacted", "credential=do-not-echo"),
            ("check-archive", "-----BEGIN PRIVATE KEY-----"),
            ("generate-archive-ledger", "authorization: Bearer do-not-echo-value"),
            ("check-archive-ledger", ".zsh_history"),
            ("generate-snapshot-manifest", "2026-07-14T10:00:00 ERROR do-not-echo"),
            ("check-snapshot-manifest", "token=do-not-echo"),
        )
        for mode, marker in cases:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                init_repo(root)
                git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
                baseline = git(root, "rev-parse", "HEAD")
                path = root / "docs/90.references/data/diagnostic.md"
                path.parent.mkdir(parents=True)
                path.write_text(
                    "---\n"
                    + yaml.safe_dump(
                        {
                            "status": "active",
                            "artifact_id": "reference:diagnostic",
                            "artifact_type": "reference",
                            "parent_ids": [marker],
                        },
                        sort_keys=False,
                    )
                    + "---\n\n# Diagnostic\n",
                    encoding="utf-8",
                )
                commit_all(root, "track diagnostic")
                output = root / "output.md"
                arguments = [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    mode,
                ]
                if mode == "check-impacted":
                    arguments.extend(("--base-ref", baseline))
                if mode in {
                    "generate-archive-ledger",
                    "check-archive-ledger",
                    "generate-snapshot-manifest",
                    "check-snapshot-manifest",
                }:
                    arguments.extend(("--output", str(output)))
                    if mode.startswith("check-"):
                        output.write_text("sentinel\n", encoding="utf-8")
                result = run(*arguments, cwd=ROOT)
                rendered = result.stdout + result.stderr
                self.assertNotIn(marker, rendered)
                self.assertNotIn(marker, output.read_text(encoding="utf-8") if output.exists() else "")
                if mode in {"report-full", "check-full", "check-impacted"}:
                    self.assertEqual(result.returncode, 3, rendered)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            path = root / "docs/90.references/data/ordinary.md"
            path.parent.mkdir(parents=True)
            missing_id = "reference:ordinary-unresolved-id"
            path.write_text(
                "---\nstatus: active\nartifact_id: reference:ordinary\n"
                f"artifact_type: reference\nparent_ids: [{missing_id}]\n---\n\n# Ordinary\n",
                encoding="utf-8",
            )
            commit_all(root)
            result = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "report-full",
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("unresolved-parent", result.stdout)
            self.assertNotIn(missing_id, result.stdout + result.stderr)

    def test_generated_markdown_table_cells_escape_pipe_and_control_characters(self) -> None:
        record = self.record(
            "docs/98.archive/a|b.md",
            "archive",
            archived_from="docs/source|name.md\nnext-row",
            archive_disposition="withdrawn",
            preservation_class="git-history",
            archived_commit="a" * 40,
            archived_blob="b" * 40,
        )
        ledger = lifecycle.render_archive_ledger((record,))
        self.assertIn("docs/98.archive/a\\|b.md", ledger)
        self.assertIn("docs/source\\|name.md next-row", ledger)
        self.assertNotIn("docs/source|name.md\nnext-row", ledger)


class AcceptanceFindingRemediationTests(LifecycleTestCase):
    _archive_fixture = FinalReviewRemediationTests._archive_fixture
    _archive_codes = FinalReviewRemediationTests._archive_codes

    @staticmethod
    def _reference_text(
        artifact_id: str,
        title: str,
        *,
        parent_ids: tuple[str, ...] = (),
        status: str = "active",
    ) -> str:
        metadata_values = {
            "status": status,
            "artifact_id": artifact_id,
            "artifact_type": "reference",
            "parent_ids": list(parent_ids),
        }
        return (
            "---\n"
            + yaml.safe_dump(metadata_values, sort_keys=False)
            + f"---\n\n# {title}\n\n"
            "## Overview\nCurrent reference.\n\n"
            "## Purpose\nCanonical purpose.\n\n"
            "## Scope\nCurrent scope.\n\n"
            "## Facts and Definitions\nCanonical facts.\n\n"
            "## Sources\nRepository evidence.\n\n"
            "## Maintenance\nActive.\n\n"
            "## Related Documents\nNone.\n"
        )

    @staticmethod
    def _destructive_evidence() -> lifecycle.ManifestEvidence:
        return lifecycle.ManifestEvidence(
            ("git show baseline source",),
            ("docs/90.references/source.md",),
            (pathlib.PurePosixPath("docs/90.references/source.md"),),
            ("verified active consumers",),
            ("revert destructive commit",),
        )

    def _invoke_corpus_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
        *,
        base_ref: str = "HEAD",
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--mode",
            mode,
        ]
        if mode == "check-impacted":
            arguments.extend(("--base-ref", base_ref))
        if mode in {
            "report-duplicates",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        }:
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def test_real_impacted_cli_accepts_unstaged_delete_and_rename_snapshots(self) -> None:
        for operation in ("delete", "rename"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                init_repo(root)
                source = root / "docs/90.references/source.md"
                consumer = root / "docs/90.references/consumer.md"
                source.parent.mkdir(parents=True)
                source.write_text(
                    self._reference_text("reference:source", "Source"),
                    encoding="utf-8",
                )
                consumer.write_text(
                    self._reference_text("reference:consumer", "Consumer")
                    + "\n[Source](./source.md)\n",
                    encoding="utf-8",
                )
                baseline = commit_all(root, "impacted baseline")
                if operation == "delete":
                    source.unlink()
                    expected_selected = 1
                else:
                    source.rename(root / "docs/90.references/renamed.md")
                    expected_selected = 2

                result = self._invoke_corpus_mode(
                    root,
                    "check-impacted",
                    root / "unused",
                    base_ref=baseline,
                )
                rendered = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, rendered)
                self.assertIn(
                    f"selected={expected_selected} violations=0",
                    result.stdout,
                )
                self.assertNotIn("corpus-markdown-file-invalid", rendered)

    def test_safety_exception_paths_are_redacted_across_corpus_reading_modes(self) -> None:
        marker = "token=do-not-echo-1234567890"
        modes = (
            "report-full",
            "check-full",
            "report-duplicates",
            "check-impacted",
            "check-archive",
            "check-directory-budget",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        )
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            root = fixture / "repository"
            outside = fixture / "outside.md"
            root.mkdir()
            init_repo(root)
            outside.write_text("outside payload", encoding="utf-8")
            unsafe = root / f"docs/90.references/{marker}.md"
            unsafe.parent.mkdir(parents=True)
            unsafe.symlink_to(outside)
            commit_all(root, "track unsafe token-shaped path")

            for mode in modes:
                with self.subTest(mode=mode):
                    output = fixture / f"{mode}.out"
                    if mode in {"check-archive-ledger", "check-snapshot-manifest"}:
                        output.write_bytes(b"existing-output")
                    result = self._invoke_corpus_mode(root, mode, output)
                    rendered = result.stdout + result.stderr
                    self.assertEqual(result.returncode, 3, rendered)
                    self.assertNotIn(marker, rendered)
                    self.assertNotIn("Traceback", rendered)
                    if mode in {"check-archive-ledger", "check-snapshot-manifest"}:
                        self.assertEqual(output.read_bytes(), b"existing-output")
                    else:
                        self.assertFalse(output.exists())

    def _merge_fixture(
        self,
        *,
        track_target: bool = True,
        baseline_target_artifact_type: str = "reference",
        duplicate_baseline_owner: bool = False,
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str, lifecycle.MigrationManifestRow]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            self._reference_text("reference:duplicate", "Duplicate Source"),
            encoding="utf-8",
        )
        target_relative = pathlib.PurePosixPath(
            "docs/90.references/data/canonical.md"
        )
        target = root / target_relative
        canonical_target = self._reference_text(
            "reference:canonical", "Canonical Owner"
        )
        if track_target:
            target.parent.mkdir(parents=True)
            target.write_text(
                canonical_target.replace(
                    "artifact_type: reference",
                    f"artifact_type: {baseline_target_artifact_type}",
                ),
                encoding="utf-8",
            )
        duplicate_owner = root / "docs/90.references/data/duplicate-owner.md"
        if duplicate_baseline_owner:
            duplicate_owner.write_text(canonical_target, encoding="utf-8")
        baseline = commit_all(root, "merge baseline")
        source.unlink()
        if track_target and baseline_target_artifact_type != "reference":
            target.write_text(canonical_target, encoding="utf-8")
        if duplicate_baseline_owner:
            duplicate_owner.unlink()
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "remove merged source")
        if not track_target:
            target.parent.mkdir(parents=True)
            target.write_text(canonical_target, encoding="utf-8")
        row = self.valid_row(
            source_path=source_relative,
            target_path=target_relative,
            artifact_id="reference:duplicate",
            artifact_type="reference",
            status_before="active",
            status_after="active",
            parent_ids=(),
            disposition="merge",
            canonical_replacement=target_relative.as_posix(),
            active_consumers=(),
            preservation_class="git-history",
            evidence=self._destructive_evidence(),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        return temporary, root, baseline, row

    def _manifest_codes(
        self,
        root: pathlib.Path,
        baseline: str,
        rows: tuple[lifecycle.MigrationManifestRow, ...],
    ) -> set[str]:
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(
                    [row.source_path.as_posix() for row in rows]
                ),
                self.document(baseline, entries=rows),
            )
        }

    def test_merge_and_delete_replacements_resolve_and_bind_to_canonical_results(self) -> None:
        temporary, root, baseline, row = self._merge_fixture()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(self._manifest_codes(root, baseline, (row,)), set())
        self.assertEqual(
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:canonical",
                    ),
                ),
            ),
            set(),
        )

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text("reference:other", "Other"),
            encoding="utf-8",
        )
        commit_all(root, "track mismatched replacement")
        invalid_replacements = (
            "docs/90.references/data/missing.md",
            "reference:missing",
            "docs/90.references/data/other.md",
            "reference:other",
        )
        for replacement in invalid_replacements:
            with self.subTest(replacement=replacement):
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(
                        root,
                        baseline,
                        (dataclasses.replace(row, canonical_replacement=replacement),),
                    ),
                )

        target = root / row.target_path
        canonical = target.read_text(encoding="utf-8")
        for name, mutation in {
            "invalid-profile": canonical.replace(
                "artifact_type: reference", "artifact_type: archive"
            ),
            "invalid-body": canonical.replace("## Sources", "### Sources"),
        }.items():
            with self.subTest(target_mutation=name):
                target.write_text(mutation, encoding="utf-8")
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(root, baseline, (row,)),
                )
        target.write_text(canonical, encoding="utf-8")

        outside = pathlib.Path(temporary.name).parent / (
            pathlib.Path(temporary.name).name + "-merge-outside.md"
        )
        outside.write_text(canonical, encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        target.unlink()
        target.symlink_to(outside)
        with self.assertRaises(lifecycle._CorpusSafetyError):
            self._manifest_codes(root, baseline, (row,))
        target.unlink()
        target.write_text(canonical, encoding="utf-8")

        duplicate = root / "docs/90.references/data/duplicate.md"
        duplicate.write_text(canonical, encoding="utf-8")
        commit_all(root, "duplicate merged identity")
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:canonical",
                    ),
                ),
            ),
        )

        untracked_temporary, untracked_root, untracked_baseline, untracked_row = (
            self._merge_fixture(track_target=False)
        )
        self.addCleanup(untracked_temporary.cleanup)
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                untracked_root, untracked_baseline, (untracked_row,)
            ),
        )

        delete_source = root / "docs/90.references/delete-source.md"
        delete_source.write_text(
            self._reference_text("reference:delete-source", "Delete Source"),
            encoding="utf-8",
        )
        delete_baseline = commit_all(root, "delete baseline")
        delete_source.unlink()
        commit_all(root, "remove delete source")
        delete_row = dataclasses.replace(
            row,
            source_path=pathlib.PurePosixPath("docs/90.references/delete-source.md"),
            target_path=None,
            artifact_id="reference:delete-source",
            disposition="delete",
            canonical_replacement="docs/90.references/data/other.md",
        )
        self.assertEqual(
            self._manifest_codes(root, delete_baseline, (delete_row,)),
            set(),
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                root,
                delete_baseline,
                (
                    dataclasses.replace(
                        delete_row,
                        canonical_replacement="docs/90.references/data/missing.md",
                    ),
                ),
            ),
        )

    def test_distinct_identity_merge_rejects_owner_target_and_identity_mutations(
        self,
    ) -> None:
        temporary, root, baseline, row = self._merge_fixture()
        self.addCleanup(temporary.cleanup)

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text("reference:other", "Other Owner"),
            encoding="utf-8",
        )
        commit_all(root, "track other owner")

        wrong_owner = dataclasses.replace(
            row,
            canonical_replacement="reference:other",
        )
        wrong_target = dataclasses.replace(
            row,
            target_path=pathlib.PurePosixPath("docs/90.references/data/other.md"),
            canonical_replacement="reference:canonical",
        )
        baseline_identity_mutation = dataclasses.replace(
            row,
            artifact_id="reference:canonical",
        )
        for name, mutated, expected in (
            ("wrong-owner", wrong_owner, "manifest-replacement-invalid"),
            ("wrong-target", wrong_target, "manifest-replacement-invalid"),
            (
                "baseline-row-identity",
                baseline_identity_mutation,
                "manifest-baseline-artifact-id-mismatch",
            ),
        ):
            with self.subTest(name=name):
                self.assertIn(
                    expected,
                    self._manifest_codes(root, baseline, (mutated,)),
                )

        target = root / row.target_path
        canonical = target.read_text(encoding="utf-8")
        target.write_text(
            canonical.replace("reference:canonical", "reference:mutated"),
            encoding="utf-8",
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(root, baseline, (row,)),
        )

    def test_merge_can_preserve_source_identity_when_the_target_is_new(self) -> None:
        temporary, root, baseline, row = self._merge_fixture(track_target=False)
        self.addCleanup(temporary.cleanup)
        target = root / row.target_path
        target.write_text(
            self._reference_text("reference:duplicate", "Consolidated Result"),
            encoding="utf-8",
        )
        commit_all(root, "track consolidated result")

        self.assertEqual(self._manifest_codes(root, baseline, (row,)), set())
        self.assertEqual(
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:duplicate",
                    ),
                ),
            ),
            set(),
        )

    def test_merge_rejects_distinct_identity_created_after_the_baseline(self) -> None:
        temporary, root, baseline, row = self._merge_fixture(track_target=False)
        self.addCleanup(temporary.cleanup)
        commit_all(root, "track post-baseline canonical identity")

        for replacement in (
            row.target_path.as_posix(),
            "reference:canonical",
        ):
            with self.subTest(replacement=replacement):
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(
                        root,
                        baseline,
                        (
                            dataclasses.replace(
                                row,
                                canonical_replacement=replacement,
                            ),
                        ),
                    ),
                )

    def test_merge_rejects_ambiguous_or_wrong_profile_baseline_owner(self) -> None:
        fixtures = (
            ("ambiguous-owner", {"duplicate_baseline_owner": True}),
            ("wrong-profile", {"baseline_target_artifact_type": "archive"}),
        )
        for name, options in fixtures:
            with self.subTest(name=name):
                temporary, root, baseline, row = self._merge_fixture(**options)
                self.addCleanup(temporary.cleanup)
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(root, baseline, (row,)),
                )

    def test_merge_accepts_preexisting_distinct_owner_moved_by_the_same_wave(
        self,
    ) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        owner_relative = pathlib.PurePosixPath(
            "docs/90.references/data/old-owner.md"
        )
        target_relative = pathlib.PurePosixPath(
            "docs/90.references/data/canonical.md"
        )
        source = root / source_relative
        owner = root / owner_relative
        source.parent.mkdir(parents=True)
        owner.parent.mkdir(parents=True)
        source.write_text(
            self._reference_text("reference:duplicate", "Duplicate Source"),
            encoding="utf-8",
        )
        owner.write_text(
            self._reference_text("reference:canonical", "Canonical Owner"),
            encoding="utf-8",
        )
        baseline = commit_all(root, "moving merge-owner baseline")
        source.unlink()
        owner.unlink()
        target = root / target_relative
        target.write_text(
            self._reference_text("reference:canonical", "Moved Canonical Owner"),
            encoding="utf-8",
        )
        commit_all(root, "move canonical owner and merge duplicate")

        def evidence(path: pathlib.PurePosixPath) -> lifecycle.ManifestEvidence:
            return lifecycle.ManifestEvidence(
                (f"git show baseline:{path.as_posix()}",),
                (path.as_posix(),),
                (path,),
                ("verified active consumers",),
                ("revert destructive commit",),
            )

        owner_row = self.valid_row(
            source_path=owner_relative,
            target_path=target_relative,
            artifact_id="reference:canonical",
            artifact_type="reference",
            status_before="active",
            status_after="active",
            parent_ids=(),
            disposition="move",
            canonical_replacement=None,
            active_consumers=(),
            preservation_class="git-history",
            evidence=evidence(owner_relative),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        merge_row = dataclasses.replace(
            owner_row,
            source_path=source_relative,
            artifact_id="reference:duplicate",
            disposition="merge",
            canonical_replacement=target_relative.as_posix(),
            evidence=evidence(source_relative),
        )
        for replacement in (target_relative.as_posix(), "reference:canonical"):
            with self.subTest(replacement=replacement):
                candidate = dataclasses.replace(
                    merge_row,
                    canonical_replacement=replacement,
                )
                self.assertEqual(
                    self._manifest_codes(root, baseline, (owner_row, candidate)),
                    set(),
                )

    WRITE_MODES = (
        "generate-manifest",
        "generate-summary",
        "report-duplicates",
        "generate-archive-ledger",
        "generate-snapshot-manifest",
    )
    CHECK_MODES = (
        "check-summary",
        "check-archive-ledger",
        "check-snapshot-manifest",
    )

    def _mode_fixture(
        self,
        mode: str,
        output: pathlib.Path,
    ) -> tuple[list[str], str, lifecycle.MigrationManifestDocument]:
        document = self.document("a" * 40)
        arguments = ["--mode", mode]
        if mode == "generate-manifest":
            arguments.extend(
                (
                    "--wave",
                    "fixture",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(output),
                )
            )
            rendered = lifecycle.render_migration_manifest(document)
        elif mode in {"generate-summary", "check-summary"}:
            arguments.extend(
                ("--manifest", "docs/manifest.yaml", "--output", str(output))
            )
            rendered = lifecycle._render_summary(document)
        elif mode == "report-duplicates":
            arguments.extend(("--output", str(output)))
            rendered = yaml.safe_dump(
                {"schema_version": 1, "candidates": []},
                sort_keys=False,
                width=1000,
            )
        elif mode in {"generate-archive-ledger", "check-archive-ledger"}:
            arguments.extend(("--output", str(output)))
            rendered = lifecycle.render_archive_ledger(())
        elif mode in {"generate-snapshot-manifest", "check-snapshot-manifest"}:
            arguments.extend(("--output", str(output)))
            rendered = lifecycle.render_snapshot_manifest(())
        else:
            raise AssertionError(f"unsupported output mode: {mode}")
        return arguments, rendered, document

    def _invoke_output_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
    ) -> tuple[int, str, str]:
        arguments, _, document = self._mode_fixture(mode, output)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                lifecycle,
                "load_migration_contract",
                return_value=copy.deepcopy(self.contract),
            ),
            mock.patch.object(
                lifecycle.metadata,
                "load_profiles",
                return_value=self.profiles,
            ),
            mock.patch.object(
                lifecycle,
                "generate_manifest_skeleton",
                return_value=document,
            ),
            mock.patch.object(
                lifecycle,
                "_load_candidate_migration_manifest",
                return_value=document,
            ),
            mock.patch.object(
                lifecycle,
                "validate_migration_manifest",
                return_value=[],
            ),
            mock.patch.object(
                lifecycle,
                "_candidate_manifest_matches",
                return_value=True,
            ),
            mock.patch.object(lifecycle, "_full_findings", return_value=((), [])),
            mock.patch.object(
                lifecycle,
                "find_duplicate_candidates",
                return_value=(),
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = lifecycle.main(["--root", str(root), *arguments])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_all_output_modes_reject_final_and_intermediate_symlinks(self) -> None:
        modes = self.WRITE_MODES + self.CHECK_MODES
        for attack in ("final", "intermediate"):
            for mode in modes:
                with (
                    self.subTest(attack=attack, mode=mode),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    fixture = pathlib.Path(directory)
                    root = fixture / "repository"
                    root.mkdir()
                    outside = fixture / "outside"
                    outside.mkdir()
                    output_parent = fixture / "selected"
                    output_parent.mkdir()
                    _, rendered, _ = self._mode_fixture(
                        mode,
                        output_parent / "placeholder",
                    )
                    expected = rendered.encode("utf-8")
                    if attack == "final":
                        victim = outside / "victim"
                        original = expected if mode in self.CHECK_MODES else b"victim-sentinel"
                        victim.write_bytes(original)
                        output = output_parent / "result"
                        output.symlink_to(victim)
                    else:
                        alias = output_parent / "alias"
                        alias.symlink_to(outside, target_is_directory=True)
                        output = alias / "result"
                        victim = outside / "result"
                        original = expected if mode in self.CHECK_MODES else None
                        if original is not None:
                            victim.write_bytes(original)

                    result, stdout, stderr = self._invoke_output_mode(
                        root,
                        mode,
                        output,
                    )
                    rendered_diagnostic = stdout + stderr
                    self.assertEqual(result, 3, rendered_diagnostic)
                    self.assertNotIn("Traceback", rendered_diagnostic)
                    self.assertNotIn("victim-sentinel", rendered_diagnostic)
                    if original is None:
                        self.assertFalse(victim.exists())
                    else:
                        self.assertEqual(victim.read_bytes(), original)
                    self.assertFalse(
                        any("lifecycle-output" in path.name for path in fixture.rglob("*"))
                    )

    def test_all_output_modes_reject_nonregular_final_entries(self) -> None:
        for mode in self.WRITE_MODES + self.CHECK_MODES:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                root.mkdir()
                output = fixture / "selected-output"
                output.mkdir()
                result, stdout, stderr = self._invoke_output_mode(root, mode, output)
                self.assertEqual(result, 3, stdout + stderr)
                self.assertTrue(output.is_dir())
                self.assertNotIn("Traceback", stdout + stderr)

    def test_all_output_modes_accept_regular_absolute_paths(self) -> None:
        for mode in self.WRITE_MODES + self.CHECK_MODES:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                root.mkdir()
                output = fixture / "nested" / "result"
                _, rendered, _ = self._mode_fixture(mode, output)
                if mode in self.CHECK_MODES:
                    output.parent.mkdir()
                    output.write_bytes(rendered.encode("utf-8"))
                result, stdout, stderr = self._invoke_output_mode(root, mode, output)
                self.assertEqual(result, 0, stdout + stderr)
                self.assertEqual(output.read_bytes(), rendered.encode("utf-8"))

    def test_atomic_publication_cannot_redirect_a_concurrent_final_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            output = fixture / "result"
            victim = fixture / "victim"
            victim.write_bytes(b"victim-sentinel")
            original_replace = os.replace

            def swap_then_replace(
                source: str,
                target: str,
                *,
                src_dir_fd: int | None = None,
                dst_dir_fd: int | None = None,
            ) -> None:
                os.symlink(victim, target, dir_fd=dst_dir_fd)
                original_replace(
                    source,
                    target,
                    src_dir_fd=src_dir_fd,
                    dst_dir_fd=dst_dir_fd,
                )

            with mock.patch.object(
                lifecycle.os,
                "replace",
                side_effect=swap_then_replace,
            ) as replaced:
                lifecycle._write_output(output, "complete\n")

            replaced.assert_called_once()
            self.assertEqual(victim.read_bytes(), b"victim-sentinel")
            self.assertEqual(output.read_bytes(), b"complete\n")
            self.assertFalse(
                any("lifecycle-output" in path.name for path in fixture.iterdir())
            )

    def test_interrupted_publication_preserves_existing_output_and_cleans_temp(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            output = fixture / "result"
            output.write_bytes(b"existing-output")
            original_write = os.write
            calls = 0

            def partial_then_fail(descriptor: int, payload: bytes) -> int:
                nonlocal calls
                calls += 1
                if calls == 1:
                    original_write(descriptor, payload[: max(1, len(payload) // 2)])
                    raise OSError("simulated interrupted publication")
                return original_write(descriptor, payload)

            with mock.patch.object(
                lifecycle.os,
                "write",
                side_effect=partial_then_fail,
            ):
                with self.assertRaises((OSError, lifecycle._CorpusSafetyError)):
                    lifecycle._write_output(output, "complete-output\n")

            self.assertGreater(calls, 0)
            self.assertEqual(output.read_bytes(), b"existing-output")
            self.assertFalse(
                any("lifecycle-output" in path.name for path in fixture.iterdir())
            )

    def test_archive_result_relations_use_the_held_full_result_manifest(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        original = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text(
                "reference:other",
                "Other",
                parent_ids=("reference:source",),
            ),
            encoding="utf-8",
        )
        spec_parent = root / "docs/03.specs/parent.md"
        spec_parent.parent.mkdir(parents=True)
        spec_parent.write_text(
            "---\nstatus: active\nartifact_id: spec:parent\n"
            "artifact_type: spec\nparent_ids: []\n---\n\n# Parent Spec\n",
            encoding="utf-8",
        )
        archive_parent = root / "docs/98.archive/other.md"
        archive_parent.parent.mkdir(parents=True, exist_ok=True)
        archive_parent.write_text(
            "---\nstatus: archived\nartifact_id: reference:archive-parent\n"
            "artifact_type: archive\nparent_ids: []\n---\n\n# Other Archive\n",
            encoding="utf-8",
        )
        commit_all(root, "track archive relation graph")

        cases: tuple[tuple[str, dict[str, object], tuple[str, ...], str], ...] = (
            ("unresolved-parent", {"parent_ids": ["reference:missing"]}, ("reference:missing",), "unresolved-parent"),
            ("self-parent", {"parent_ids": ["reference:source"]}, ("reference:source",), "self-parent"),
            ("wrong-parent-type", {"parent_ids": ["reference:archive-parent"]}, ("reference:archive-parent",), "invalid-parent-type"),
            ("parent-order", {"parent_ids": ["reference:replacement", "spec:parent"]}, ("reference:replacement", "spec:parent"), "parent-order"),
            ("parent-cycle", {"parent_ids": ["reference:other"]}, ("reference:other",), "parent-cycle"),
            ("unresolved-supersedes", {"supersedes": ["reference:missing"]}, (), "unresolved-supersedes"),
            ("self-supersession", {"supersedes": ["reference:source"]}, (), "self-supersession"),
            ("invalid-supersession-state", {"supersedes": ["reference:replacement"]}, (), "invalid-supersession-state"),
        )
        for name, mutation, parents, expected in cases:
            with self.subTest(case=name):
                values = {**original, **mutation}
                target.write_text(
                    "---\n"
                    + yaml.safe_dump(values, sort_keys=False)
                    + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, parent_ids=parents)
                self.assertIn(expected, self._archive_codes(root, baseline, candidate))

    def test_multi_row_archive_relations_resolve_against_untracked_result_targets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            archive_source_path = pathlib.PurePosixPath("docs/90.references/archive-source.md")
            parent_source_path = pathlib.PurePosixPath("docs/90.references/parent-source.md")
            for path, artifact_id, title in (
                (archive_source_path, "reference:archive-source", "Archive Source"),
                (parent_source_path, "reference:parent", "Parent Source"),
            ):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(self._reference_text(artifact_id, title), encoding="utf-8")
            baseline = commit_all(root, "multi-row baseline")
            archived_blob = git(root, "rev-parse", f"{baseline}:{archive_source_path.as_posix()}")
            (root / archive_source_path).unlink()
            (root / parent_source_path).unlink()
            commit_all(root, "remove multi-row sources")

            archive_target_path = pathlib.PurePosixPath(
                "docs/98.archive/90.references/archive-source.md"
            )
            archive_target = root / archive_target_path
            archive_target.parent.mkdir(parents=True)
            archive_target.write_text(
                "---\n"
                + yaml.safe_dump(
                    {
                        "status": "archived",
                        "artifact_id": "reference:archive-source",
                        "artifact_type": "archive",
                        "parent_ids": ["reference:parent"],
                        "archived_from": archive_source_path.as_posix(),
                        "archived_on": "2026-07-14",
                        "archive_reason": "Withdrawn with preserved provenance.",
                        "archive_disposition": "withdrawn",
                        "archived_commit": baseline,
                        "archived_blob": archived_blob,
                        "preservation_class": "git-history",
                    },
                    sort_keys=False,
                )
                + "---\n\n# Archived Source\n",
                encoding="utf-8",
            )
            parent_target_path = pathlib.PurePosixPath(
                "docs/90.references/data/parent.md"
            )
            parent_target = root / parent_target_path
            parent_target.parent.mkdir(parents=True)
            parent_target.write_text(
                self._reference_text("reference:parent", "Moved Parent"),
                encoding="utf-8",
            )
            archive_row = self.valid_row(
                source_path=archive_source_path,
                target_path=archive_target_path,
                artifact_id="reference:archive-source",
                artifact_type="reference",
                status_before="active",
                status_after="archived",
                parent_ids=("reference:parent",),
                disposition="archive",
                canonical_replacement=None,
                active_consumers=(),
                preservation_class="git-history",
                evidence=self._destructive_evidence(),
                review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
            )
            parent_row = self.valid_row(
                source_path=parent_source_path,
                target_path=parent_target_path,
                artifact_id="reference:parent",
                artifact_type="reference",
                status_before="active",
                status_after="active",
                parent_ids=(),
                disposition="move",
            )
            self.assertEqual(
                self._manifest_codes(root, baseline, (archive_row, parent_row)),
                set(),
            )


if __name__ == "__main__":
    unittest.main()
