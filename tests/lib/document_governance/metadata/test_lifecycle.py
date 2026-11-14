"""Metadata lifecycle and transition-evidence tests."""

from __future__ import annotations

import json
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


class VersionChangeTests(unittest.TestCase):
    """A changed document's `version` against the same path at the merge base."""

    DOC = pathlib.Path("docs/90.references/research/0001-x/note.md")
    BASE_BODY = "# Fixture\n"

    def findings(
        self,
        base: str | None,
        head: str | None,
        *,
        tracked: bool = True,
        head_body: str = "# Fixture changed\n",
        head_extra: dict[str, object] | None = None,
        base_extra: dict[str, object] | None = None,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            other = pathlib.Path("README.md")
            write_doc(root / other, {"version": "9.9.9"})
            if tracked:
                write_doc(
                    root / self.DOC,
                    None if base is None else {"version": base, **(base_extra or {})},
                    self.BASE_BODY,
                )
            self.assertEqual(0, git(root, "add", ".").returncode)
            self.assertEqual(0, git(root, "commit", "-qm", "base").returncode)
            base_ref = git(root, "rev-parse", "HEAD").stdout.strip()
            values = {} if head is None else {"version": head, **(head_extra or {})}
            write_doc(root / self.DOC, values, head_body)
            record = Record(self.DOC, values, "x")
            return version_module.version_change_findings(
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

    def test_changed_content_with_the_same_precedence_is_unchanged(self) -> None:
        for base, head in (("1.2.0", "1.2.0"), ("1.2.0", "1.2.0+build.2")):
            with self.subTest(base=base, head=head):
                (finding,) = self.findings(base, head)
                self.assertEqual("version-unchanged", finding.code)
                self.assertEqual(self.DOC.as_posix(), finding.path)
                self.assertEqual("error", finding.severity)

    def test_raised_precedence_passes(self) -> None:
        for base, head in (
            ("1.2.0", "1.10.0"),
            ("1.2.0", "1.2.1-rc.1"),
            ("1.0.0-rc.1", "1.0.0"),
        ):
            with self.subTest(base=base, head=head):
                self.assertEqual([], self.findings(base, head))

    def test_old_and_new_producer_against_old_and_new_consumer(self) -> None:
        old, new = "1.2.0", "1.3.0-rc.1+build.7"
        expected = {
            (old, old): "version-unchanged",
            (old, new): None,
            (new, old): "version-downgrade",
            (new, new): "version-unchanged",
        }
        for (base, head), code in expected.items():
            with self.subTest(base=base, head=head):
                self.assertEqual(
                    [] if code is None else [code],
                    [finding.code for finding in self.findings(base, head)],
                )

    def test_a_path_whose_bytes_did_not_change_is_not_a_change(self) -> None:
        self.assertEqual([], self.findings("1.2.0", "1.2.0", head_body=self.BASE_BODY))

    def test_a_lifecycle_only_edit_does_not_need_a_new_version(self) -> None:
        # Status and review dates are lifecycle state, independent of content.
        for extra_base, extra_head in (
            ({"status": "draft"}, {"status": "active"}),
            ({"updated": "2026-01-01"}, {"updated": "2026-02-02"}),
            (
                {"next_review_at": "2026-03-01"},
                {"next_review_at": "2026-09-01", "reviewed_at": "2026-02-01"},
            ),
        ):
            with self.subTest(head=extra_head):
                self.assertEqual(
                    [],
                    self.findings(
                        "1.2.0",
                        "1.2.0",
                        head_body=self.BASE_BODY,
                        base_extra=extra_base,
                        head_extra=extra_head,
                    ),
                )
        # A body edit beside a status change is still a content change.
        (finding,) = self.findings(
            "1.2.0",
            "1.2.0",
            base_extra={"status": "draft"},
            head_extra={"status": "active"},
        )
        self.assertEqual("version-unchanged", finding.code)
        # A change to another frontmatter key is a content change too.
        (finding,) = self.findings(
            "1.2.0",
            "1.2.0",
            head_body=self.BASE_BODY,
            base_extra={"owner": "@a"},
            head_extra={"owner": "@b"},
        )
        self.assertEqual("version-unchanged", finding.code)

    def test_new_document_or_missing_or_malformed_version_is_not_compared(
        self,
    ) -> None:
        self.assertEqual([], self.findings(None, "0.1.0", tracked=False))
        self.assertEqual([], self.findings(None, "0.1.0"))  # base has no version
        self.assertEqual([], self.findings("1.2.0", None))  # head has no version
        self.assertEqual([], self.findings("v1.2.0", "1.0.0"))
        self.assertEqual([], self.findings("1.2.0", "1.1"))

    def test_q07_numbering_is_not_a_version(self) -> None:
        # A renumbered artifact id or input label never counts as a version.
        for head in ("SPEC-0064", "v14.7", "0064"):
            with self.subTest(head=head):
                self.assertEqual([], self.findings("1.2.0", head))

    def test_the_comparator_is_the_shared_one(self) -> None:
        from scripts.lib.document_governance import semver

        self.assertIs(semver, version_module.semver)
        self.assertFalse(hasattr(version_module, "_SEMVER"))
        self.assertFalse(hasattr(version_module, "compare_semver"))


class ProductVersionTests(unittest.TestCase):
    """The inventoried product version fields against the merge base."""

    NODE = "projects/storybook/nextjs/package.json"
    PYTHON = "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/pyproject.toml"

    @staticmethod
    def package(version: str | None, dependency: str = "1.0.0") -> str:
        body = {"name": "x", "dependencies": {"left-pad": dependency}}
        if version is not None:
            body = {"name": "x", "version": version, **body}
        return json.dumps(body, indent=2) + "\n"

    @staticmethod
    def project(version: str | None, dependency: str = "1.0.0") -> str:
        line = "" if version is None else f'version = "{version}"\n'
        return (
            f'[project]\nname = "hermes-publisher"\n{line}'
            f'dependencies = ["requests=={dependency}"]\n'
        )

    def findings(self, path: str, base: str | None, head: str | None):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            if base is not None:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(base, encoding="utf-8")
            self.assertEqual(0, git(root, "add", ".").returncode)
            self.assertEqual(0, git(root, "commit", "-qm", "base").returncode)
            base_ref = git(root, "rev-parse", "HEAD").stdout.strip()
            if head is not None:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(head, encoding="utf-8")
            elif (root / path).exists():
                (root / path).unlink()
            return version_module.product_version_findings(root, base_ref)

    def codes(self, path: str, base: str | None, head: str | None) -> list[str]:
        return [finding.code for finding in self.findings(path, base, head)]

    def test_inventory_lists_the_four_product_version_files(self) -> None:
        self.assertEqual(
            {
                "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/nodes/"
                "OpsflowSmtp/package.json",
                self.PYTHON,
                self.NODE,
                "projects/storybook/nextjs/packages/ui/package.json",
            },
            set(version_module.PRODUCT_VERSION_FILES),
        )

    def test_a_lower_version_is_a_downgrade(self) -> None:
        self.assertEqual(
            ["version-downgrade"],
            self.codes(self.NODE, self.package("1.2.0"), self.package("1.1.9")),
        )
        self.assertEqual(
            ["version-downgrade"],
            self.codes(self.PYTHON, self.project("1.0.0"), self.project("1.0.0-rc.1")),
        )

    def test_a_malformed_changed_version_is_refused(self) -> None:
        for head in ("v1.2.0", "1.2", "01.2.0", "SPEC-0064", "14.7", ""):
            with self.subTest(head=head):
                self.assertEqual(
                    ["version-malformed"],
                    self.codes(self.NODE, self.package("1.0.0"), self.package(head)),
                )
        self.assertEqual(
            ["version-malformed"],
            self.codes(self.NODE, self.package("1.0.0"), self.package(None)),
        )
        self.assertEqual(
            ["version-malformed"],
            self.codes(self.PYTHON, self.project("1.0.0"), self.project("1.2")),
        )

    def test_a_raised_version_passes(self) -> None:
        self.assertEqual(
            [], self.codes(self.NODE, self.package("1.0.0"), self.package("1.0.1"))
        )
        self.assertEqual(
            [],
            self.codes(
                self.PYTHON, self.project("1.0.0"), self.project("1.1.0-rc.1+build.7")
            ),
        )

    def test_an_unchanged_version_with_other_edits_is_allowed(self) -> None:
        # A product releases on its own cadence; the version field is the object.
        self.assertEqual(
            [],
            self.codes(
                self.NODE,
                self.package("1.0.0"),
                self.package("1.0.0", dependency="2.0.0"),
            ),
        )
        self.assertEqual(
            [],
            self.codes(
                self.PYTHON,
                self.project("1.0.0"),
                self.project("1.0.0", dependency="2.0.0"),
            ),
        )

    def test_an_untouched_deleted_new_or_unparsable_file_is_not_compared(self) -> None:
        base = self.package("1.0.0")
        self.assertEqual([], self.codes(self.NODE, base, base))
        self.assertEqual([], self.codes(self.NODE, None, self.package("0.0.1")))
        self.assertEqual([], self.codes(self.NODE, base, None))
        self.assertEqual([], self.codes(self.NODE, "{not json", self.package("0.1.0")))
        self.assertEqual([], self.codes(self.NODE, base, "{not json"))

    def test_only_the_inventoried_files_are_checked(self) -> None:
        other = "projects/other/package.json"
        self.assertEqual(
            [], self.codes(other, self.package("1.2.0"), self.package("1.1.0"))
        )
