"""Metadata lifecycle and transition-evidence tests."""

from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

# Imported for its side effect and as the script manifest's evidence that this
# test covers that module. The entrypoint re-exports its names, so the module
# must be loaded before those attributes resolve. Not dead code.
from scripts.lib.document_governance.metadata import (
    lifecycle as lifecycle_module,
)
from scripts.lib.document_governance.metadata import version as version_module
from scripts.lib.document_governance.metadata.profile import Record
from tests.lib.document_governance.metadata._support import (
    REGISTRY,
    git,
    init_git,
    metadata,
    write_doc,
)


class HistoricalBlobBatchTests(unittest.TestCase):
    def test_batch_preserves_exact_unicode_and_newline_payloads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", "-C", str(root), *args], check=True, capture_output=True
                ).stdout

            git("init", "-q")
            git("config", "core.hooksPath", "")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.invalid")
            paths = ("docs/one (copy).md", "docs/한글.md", "docs/a[1].md", "docs/a1.md")
            for path in paths:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "# Payload\n\nblob 123\n한글 and a final newline.\n",
                    encoding="utf-8",
                )
            git("add", ".")
            git("commit", "-qm", "fixture")
            expected = {
                path: git("show", f"HEAD:{path}").decode("utf-8") for path in paths
            }
            self.assertEqual(
                expected,
                lifecycle_module._read_markdown_texts_at_ref(root, paths, "HEAD"),
            )
            self.assertEqual(
                {"docs/a[1].md": expected["docs/a[1].md"]},
                lifecycle_module._read_markdown_texts_at_ref(
                    root, ("docs/a[1].md",), "HEAD"
                ),
            )
            self.assertEqual(
                {},
                lifecycle_module._read_markdown_texts_at_ref(
                    root, ("docs/missing.md",), "HEAD"
                ),
            )
            oid = git("rev-parse", f"HEAD:{paths[0]}").decode("ascii").strip()
            size = len(expected[paths[0]].encode("utf-8"))
            for payload in (
                b"missing missing\n",
                f"{oid} blob {size}\nshort\n".encode("ascii"),
            ):
                with (
                    self.subTest(payload=payload),
                    mock.patch.object(
                        lifecycle_module,
                        "_bounded_git",
                        return_value=subprocess.CompletedProcess([], 0, payload, b""),
                    ),
                ):
                    with self.assertRaises(metadata.ProfileError):
                        lifecycle_module._read_markdown_texts_at_ref(
                            root, paths, "HEAD"
                        )
            (root / "docs/link.md").symlink_to("one (copy).md")
            git("add", ".")
            git("commit", "-qm", "symlink fixture")
            with self.assertRaisesRegex(metadata.ProfileError, "regular blob"):
                lifecycle_module._read_markdown_texts_at_ref(
                    root, ("docs/link.md",), "HEAD"
                )
            large = "# Large\n" + "x" * lifecycle_module._GIT_OUTPUT_BYTES
            (root / "docs/large.md").write_text(large, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "oversized fixture")
            self.assertEqual(
                {"docs/large.md": large},
                lifecycle_module._read_markdown_texts_at_ref(
                    root, ("docs/large.md",), "HEAD"
                ),
            )


class TransitionOverrideEvidencePathTests(unittest.TestCase):
    """The override's evidence path must name a Task form this repository has.

    `load_transition_overrides` required `docs/03.specs/spec-<slug>/task.md`.
    This repository has zero documents in that form and fifteen in the
    co-located `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` form, so
    every override was rejected while the error text said the evidence "must be
    an existing co-located Task". SPEC-0155 acceptance item 13 owns the
    correction.
    """

    def _override_file(self, root: pathlib.Path, evidence: str) -> pathlib.Path:
        override = root / "override.yaml"
        override.write_text(
            "transition_overrides:\n"
            "- path: docs/03.specs/0001-fixture/spec.md\n"
            "  previous_status: completed\n"
            "  new_status: active\n"
            f"  evidence_task: {evidence}\n"
            "  approval: reviewer\n"
            "  reason: corrects a mis-recorded status\n",
            encoding="utf-8",
        )
        return override

    def _tree(self, root: pathlib.Path, evidence: str) -> None:
        target = root / "docs/03.specs/0001-fixture/spec.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Fixture\n", encoding="utf-8")
        witness = root / evidence
        witness.parent.mkdir(parents=True, exist_ok=True)
        witness.write_text("# Task\n", encoding="utf-8")

    def test_co_located_task_evidence_is_accepted(self) -> None:
        evidence = "docs/03.specs/0001-fixture/tasks/tsk-0001-fixture.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            overrides = metadata.load_transition_overrides(
                self._override_file(root, evidence),
                root,
                metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
            )
        self.assertEqual(1, len(overrides))

    def test_a_package_root_task_form_is_rejected(self) -> None:
        evidence = "docs/03.specs/0001-fixture/task.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            with self.assertRaises(metadata.ProfileError):
                metadata.load_transition_overrides(
                    self._override_file(root, evidence),
                    root,
                    metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
                )


class RetiredStatusMigrationTests(unittest.TestCase):
    """D-02: a document whose base status the lifecycle no longer offers may
    move to the one successor the Registry registers, with no override file."""

    def codes(self, previous: str, status: str) -> set[str]:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        record = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/0031-fixture.md"),
            {
                "artifact_id": "AD-0031",
                "type": "sdlc/architecture-description",
                "status": status,
                "parent_ids": ["REQ-0001"],
            },
            "architecture-description",
            previous_status=previous,
            frontmatter_present=True,
        )
        manifest = metadata.build_manifest([record])
        return {
            item.code for item in metadata.validate_record(record, profiles, manifest)
        }

    def test_the_registered_successor_is_accepted(self) -> None:
        self.assertNotIn("invalid-transition", self.codes("active", "approved"))

    def test_any_other_move_from_the_retired_status_is_rejected(self) -> None:
        for status in ("draft", "in-review"):
            with self.subTest(status=status):
                self.assertIn("invalid-transition", self.codes("active", status))

    def test_a_status_the_lifecycle_still_offers_gets_no_shortcut(self) -> None:
        self.assertIn("invalid-transition", self.codes("approved", "draft"))


class CurrentSpecRelationTests(unittest.TestCase):
    def test_only_an_unchanged_generation_status_replaces_the_older_base(self) -> None:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        record = metadata.Record(
            pathlib.Path("docs/03.specs/0001-example/spec.md"),
            {
                "artifact_id": "SPEC-0001",
                "type": "sdlc/spec",
                "status": "blocked",
                "parent_ids": ["REQ-0001"],
            },
            "spec",
            previous_status="active",
            frontmatter_present=True,
        )
        manifest = metadata.build_manifest([record])

        unbound = metadata.validate_record(record, profiles, manifest)
        unchanged = metadata.validate_record(
            record,
            profiles,
            manifest,
            unchanged_generation_statuses={record.path.as_posix(): "blocked"},
        )
        different = metadata.validate_record(
            record,
            profiles,
            manifest,
            unchanged_generation_statuses={record.path.as_posix(): "draft"},
        )

        self.assertIn("invalid-transition", {item.code for item in unbound})
        self.assertNotIn("invalid-transition", {item.code for item in unchanged})
        self.assertIn("invalid-transition", {item.code for item in different})

    def test_a_typed_reference_to_a_reserved_only_identity_is_unresolved(
        self,
    ) -> None:
        """A retired number is reserved in the Registry, never resolvable."""

        registry = metadata.load_registry(REGISTRY)
        self.assertIn(29, registry.identity_spaces["adr"].reserved_history)
        self.assertIn(
            14, registry.identity_spaces["architecture-description"].reserved_history
        )
        profiles = metadata.build_registry_profiles(registry)
        record = metadata.Record(
            pathlib.Path("docs/02.architecture/decisions/0032-fixture.md"),
            {
                "artifact_id": "ADR-0032",
                "type": "sdlc/architecture-decision",
                "status": "accepted",
                "parent_ids": ["AD-0014"],
                "supersedes": ["ADR-0029"],
            },
            "adr",
            frontmatter_present=True,
        )
        codes = {
            finding.code
            for finding in metadata.validate_record(
                record,
                profiles,
                metadata.build_current_manifest(pathlib.Path("."), [record]),
            )
        }
        self.assertIn("unresolved-parent", codes)
        self.assertIn("unresolved-supersedes", codes)

    def test_a_historical_audit_id_is_not_a_current_identity(self) -> None:
        """H-W01-4: OPEN-01..OPEN-14 name an earlier audit's items
        (TERM-HISTORICAL-AUDIT). Used as a parent or supersession target they
        read as current state, so the validator leaves them unresolved."""

        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        for audit_id in ("OPEN-01", "OPEN-07", "OPEN-14"):
            record = metadata.Record(
                pathlib.Path("docs/03.specs/0001-example/spec.md"),
                {
                    "artifact_id": "SPEC-0001",
                    "type": "sdlc/spec",
                    "status": "draft",
                    "parent_ids": [audit_id],
                    "supersedes": [audit_id],
                },
                "spec",
                frontmatter_present=True,
            )
            codes = {
                finding.code
                for finding in metadata.validate_record(
                    record, profiles, metadata.build_manifest([record])
                )
            }
            with self.subTest(audit_id=audit_id):
                self.assertIn("unresolved-parent", codes)
                self.assertIn("unresolved-supersedes", codes)

    def test_current_spec_cannot_use_another_spec_as_its_parent(self) -> None:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        parent = metadata.Record(
            pathlib.Path("docs/03.specs/0001-parent/spec.md"),
            {
                "artifact_id": "SPEC-0001",
                "type": "sdlc/spec",
                "status": "draft",
                "parent_ids": ["REQ-0001"],
            },
            "spec",
            frontmatter_present=True,
        )
        child = metadata.Record(
            pathlib.Path("docs/03.specs/0002-child/spec.md"),
            {
                "artifact_id": "SPEC-0002",
                "type": "sdlc/spec",
                "status": "draft",
                "parent_ids": ["SPEC-0001"],
            },
            "spec",
            frontmatter_present=True,
        )

        findings = metadata.validate_record(
            child, profiles, metadata.build_manifest([parent, child])
        )

        self.assertIn("invalid-parent-type", {finding.code for finding in findings})

    def test_parent_cycles_and_a_second_plan_parent_are_rejected(self) -> None:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))

        def record(path: str, artifact_id: str, parents: list[str], profile: str):
            return metadata.Record(
                pathlib.Path(path),
                {
                    "artifact_id": artifact_id,
                    "type": f"sdlc/{profile}",
                    "status": "draft",
                    "parent_ids": parents,
                },
                profile,
                frontmatter_present=True,
            )

        first = record(
            "docs/03.specs/0001-a/spec.md", "SPEC-0001", ["SPEC-0002"], "spec"
        )
        second = record(
            "docs/03.specs/0002-b/spec.md", "SPEC-0002", ["SPEC-0001"], "spec"
        )
        plan = record(
            "docs/03.specs/0001-a/plan.md",
            "SPEC-0001-PLAN-0001",
            ["SPEC-0001", "SPEC-0002"],
            "plan",
        )
        manifest = metadata.build_manifest([first, second, plan])

        def codes(item: metadata.Record) -> set[str]:
            return {f.code for f in metadata.validate_record(item, profiles, manifest)}

        self.assertIn("parent-cycle", codes(first))
        self.assertIn("parent-cardinality", codes(plan))


class ExecutionItemsProbeTests(unittest.TestCase):
    """A multi-item Task declares its table at H3 (legacy) or H4 (common form)."""

    HEADER = "| Item | Work Unit | Scope | Owner | Status | Blocker |"

    def _declares(self, text: str) -> bool:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "tsk-0001-x.md"
            path.write_text(text, encoding="utf-8")
            record = metadata.Record(path, {}, "task")
            common = metadata.load_registry(REGISTRY).common
            return lifecycle_module._declares_execution_items(record, common)

    def test_either_heading_level_declares_the_table(self) -> None:
        table = f"{self.HEADER}\n| --- | --- | --- | --- | --- | --- |\n"
        for marker in ("### Execution Items", "#### Execution Items"):
            with self.subTest(marker=marker):
                self.assertTrue(self._declares(f"## Work Log\n{marker}\n{table}"))
        for text in (
            f"## Work Log\n##### Execution Items\n{table}",
            f"## Work Log\n## Execution Items\n{table}",
            "## Work Log\n#### Execution Items\nno table\n",
            f"## Work Log\n#### Other\n{table}",
        ):
            with self.subTest(text=text):
                self.assertFalse(self._declares(text))


class OperationsCurrencyTests(unittest.TestCase):
    """documentation-protocol.md: a passed next_review_at makes a Guide,
    Operations Policy or Runbook stale until reviewed (TSK-0063 H-W04-3)."""

    def codes(self, document_type: str = "operation/runbook", **extra: str) -> set[str]:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        record = metadata.Record(
            pathlib.Path("docs/05.operations/runbooks/01-common/0004-fixture.md"),
            {
                "artifact_id": "RUN-0004",
                "type": document_type,
                "status": "active",
                "parent_ids": ["POL-0004"],
                **extra,
            },
            "runbook",
            frontmatter_present=True,
        )
        manifest = metadata.build_manifest([record])
        return {
            item.code for item in metadata.validate_record(record, profiles, manifest)
        }

    def test_a_passed_review_date_is_stale(self) -> None:
        for document_type in (
            "operation/runbook",
            "operation/guide",
            "operation/policy",
        ):
            with self.subTest(type=document_type):
                self.assertIn(
                    "stale-active",
                    self.codes(document_type, next_review_at="2000-01-01"),
                )

    def test_other_types_are_not_operations_currency(self) -> None:
        self.assertNotIn(
            "stale-active",
            self.codes("operation/incident", next_review_at="2000-01-01"),
        )

    def messages(self, document_type: str, **extra: str) -> set[str]:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        record = metadata.Record(
            pathlib.Path("docs/05.operations/runbooks/01-common/0004-fixture.md"),
            {
                "artifact_id": "RUN-0004",
                "type": document_type,
                "status": "active",
                "parent_ids": ["POL-0004"],
                **extra,
            },
            "runbook",
            frontmatter_present=True,
        )
        manifest = metadata.build_manifest([record])
        return {
            f"{item.code}: {item.message}"
            for item in metadata.validate_record(record, profiles, manifest)
        }

    def test_a_missing_review_date_is_rejected(self) -> None:
        """SDLC-06: an active operations document cannot skip its review date."""

        for document_type in (
            "operation/runbook",
            "operation/guide",
            "operation/policy",
        ):
            with self.subTest(type=document_type):
                self.assertIn(
                    "missing-required-key: required key is missing: next_review_at",
                    self.messages(document_type),
                )
                self.assertNotIn(
                    "missing-required-key: required key is missing: next_review_at",
                    self.messages(document_type, next_review_at="2999-01-01"),
                )

    def test_a_review_date_beyond_the_interval_is_rejected(self) -> None:
        for document_type in (
            "operation/runbook",
            "operation/guide",
            "operation/policy",
        ):
            with self.subTest(type=document_type):
                self.assertIn(
                    "review-interval-exceeded",
                    self.codes(
                        document_type, updated="2026-11-14", next_review_at="2999-01-01"
                    ),
                )
                self.assertNotIn(
                    "review-interval-exceeded",
                    self.codes(
                        document_type, updated="2026-11-14", next_review_at="2027-05-13"
                    ),
                )

    def test_a_future_or_absent_review_date_is_current(self) -> None:
        self.assertNotIn("stale-active", self.codes(next_review_at="2999-01-01"))
        self.assertNotIn("stale-active", self.codes())

    def test_a_review_on_or_after_the_due_date_clears_it(self) -> None:
        self.assertNotIn(
            "stale-active",
            self.codes(next_review_at="2000-01-01", reviewed_at="2000-01-02"),
        )
        self.assertIn(
            "stale-active",
            self.codes(next_review_at="2000-01-02", reviewed_at="2000-01-01"),
        )


class VersionDowngradeTests(unittest.TestCase):
    """SemVer 2.0 precedence of a changed document's `version` against its base."""

    DOC = pathlib.Path("docs/90.references/research/0001-x/note.md")

    def findings(self, base: str | None, head: str | None, *, tracked: bool = True):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            other = pathlib.Path("README.md")
            write_doc(root / other, {"version": "9.9.9"})
            if tracked:
                write_doc(root / self.DOC, None if base is None else {"version": base})
            self.assertEqual(0, git(root, "add", ".").returncode)
            self.assertEqual(0, git(root, "commit", "-qm", "base").returncode)
            base_ref = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(root / self.DOC, {} if head is None else {"version": head})
            record = Record(self.DOC, {} if head is None else {"version": head}, "x")
            return version_module.version_downgrade_findings(
                root, {self.DOC.as_posix(): record}, base_ref
            )

    def test_lower_precedence_is_a_downgrade(self) -> None:
        for base, head in (
            ("1.2.0", "1.1.9"),
            ("1.2.0", "1.2.0-rc.1"),
            ("1.10.0", "1.9.0"),
            ("1.0.0-rc.1", "1.0.0-beta.11"),
        ):
            with self.subTest(base=base, head=head):
                (finding,) = self.findings(base, head)
                self.assertEqual("version-downgrade", finding.code)
                self.assertEqual(self.DOC.as_posix(), finding.path)
                self.assertEqual("error", finding.severity)

    def test_equal_or_higher_precedence_passes(self) -> None:
        for base, head in (
            ("1.2.0", "1.2.0"),
            ("1.2.0", "1.2.0+build.2"),
            ("1.2.0", "1.10.0"),
            ("1.2.0", "1.2.1-rc.1"),
            ("1.0.0-rc.1", "1.0.0"),
        ):
            with self.subTest(base=base, head=head):
                self.assertEqual([], self.findings(base, head))

    def test_new_document_or_missing_or_malformed_version_is_not_compared(
        self,
    ) -> None:
        self.assertEqual([], self.findings(None, "0.1.0", tracked=False))
        self.assertEqual([], self.findings(None, "0.1.0"))  # base has no version
        self.assertEqual([], self.findings("1.2.0", None))  # head has no version
        self.assertEqual([], self.findings("v1.2.0", "1.0.0"))
        self.assertEqual([], self.findings("1.2.0", "1.1"))

    def test_private_semver_agrees_with_release_reference(self) -> None:
        from scripts.operations import release

        chain = (
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
            "1.0.0-beta.2",
            "1.0.0-beta.11",
            "1.0.0-rc.1",
            "1.0.0",
            "1.0.1",
            "1.10.0",
        )
        for i, low in enumerate(chain):
            for j, high in enumerate(chain):
                expected = (i > j) - (i < j)
                with self.subTest(low=low, high=high):
                    self.assertEqual(expected, version_module.compare_semver(low, high))
                    self.assertEqual(expected, release.compare_semver(low, high))
        self.assertEqual(0, version_module.compare_semver("1.2.3+a", "1.2.3+b"))
