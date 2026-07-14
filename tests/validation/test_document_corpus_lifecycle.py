from __future__ import annotations

import copy
import dataclasses
import datetime
import hashlib
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

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
            mismatch = self.invoke(root, profiles, contract_path)
            self.assertEqual(mismatch.returncode, 1)
            self.assertIn("promoted-enforcement-mismatch", mismatch.stdout)


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


if __name__ == "__main__":
    unittest.main()
