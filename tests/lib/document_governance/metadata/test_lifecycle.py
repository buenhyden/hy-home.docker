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
from tests.lib.document_governance.metadata._support import REGISTRY, metadata


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

    def test_legacy_archive_route_type_requires_source_binding(self) -> None:
        profiles = metadata.build_registry_profiles(metadata.load_registry(REGISTRY))
        record = metadata.Record(
            pathlib.Path("docs/98.archive/migrations/9999-example.md"),
            {
                "artifact_id": "MIG-9999",
                "type": "archive/migration",
                "status": "completed",
                "parent_ids": ["SPEC-0001"],
            },
            "migration",
            frontmatter_present=True,
        )
        manifest = metadata.build_manifest([record])

        unbound = metadata.validate_record(record, profiles, manifest)
        bound = metadata.validate_record(
            record, profiles, manifest, source_bound_legacy_type=True
        )

        self.assertIn("type-mismatch", {finding.code for finding in unbound})
        self.assertNotIn("type-mismatch", {finding.code for finding in bound})
