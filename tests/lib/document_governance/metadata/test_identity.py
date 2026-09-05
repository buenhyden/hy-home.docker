"""Identity collection and report-rendering behavior tests."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance.metadata import identity as identity_module
from scripts.lib.document_governance.metadata.lifecycle import collect_records
from tests.lib.document_governance.metadata._support import (
    current_profiles,
    git,
    init_git,
    metadata,
    write_doc,
)


class IdentityBehaviorTests(unittest.TestCase):
    def test_changed_carrier_keeps_unchanged_reciprocal_task_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            task_path = pathlib.Path(
                "docs/03.specs/0172-recovery/tasks/tsk-0001-recovery.md"
            )
            carrier_path = pathlib.Path(
                "docs/90.references/research/0085-workspace/m0001-request-scope.md"
            )
            decision = {
                "source_commit": "0" * 40,
                "source_path": (
                    "docs/90.references/research/0085-workspace/REQUEST-SCOPE.md"
                ),
                "source_artifact_id": "RES-0085-SCOPE",
                "target_path": carrier_path.as_posix(),
                "target_artifact_id": "RES-0085-m0001",
                "disposition": "consolidated",
            }
            write_doc(
                root / task_path,
                {
                    "artifact_id": "SPEC-0172-TSK-0001",
                    "identity_recovery_decisions": [decision],
                },
            )
            write_doc(
                root / carrier_path,
                {
                    "artifact_id": "RES-0085-m0001",
                    "identity_recovery": {
                        "source_commit": "0" * 40,
                        "source_path": decision["source_path"],
                        "source_artifact_id": "RES-0085-SCOPE",
                        "decision_path": task_path.as_posix(),
                        "decision_artifact_id": "SPEC-0172-TSK-0001",
                        "disposition": "consolidated",
                    },
                },
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            self.assertEqual(
                0, git(root, "commit", "-qm", "recovery evidence fixture").returncode
            )
            write_doc(
                root / carrier_path,
                {
                    "artifact_id": "RES-0085-m0001",
                    "identity_recovery": {
                        "source_commit": "0" * 40,
                        "source_path": decision["source_path"],
                        "source_artifact_id": "RES-0085-SCOPE",
                        "decision_path": task_path.as_posix(),
                        "decision_artifact_id": "SPEC-0172-TSK-0001",
                        "disposition": "consolidated",
                    },
                },
                body="# Changed carrier only\n",
            )

            changed = git(root, "diff", "--name-only").stdout.splitlines()
            records = collect_records(
                root,
                current_profiles(),
                selected_paths=[carrier_path.as_posix()],
                require_git=True,
            )
            by_path = {record.path.as_posix(): record for record in records}

            self.assertEqual([carrier_path.as_posix()], changed)
            self.assertEqual(
                [decision],
                by_path[task_path.as_posix()].metadata["identity_recovery_decisions"],
            )

    def test_inventory_exposes_all_semantic_state_columns(self) -> None:
        profiles = current_profiles()
        records = [
            metadata.Record(
                pathlib.Path("docs/03.specs/README.md"),
                {
                    "title": "Specs",
                    "version": "1.0.0",
                    "type": "common/readme",
                    "status": "active",
                    "owner": "@buenhyden",
                    "updated": "2026-08-01",
                    "layer": "specs",
                },
                "readme",
                frontmatter_present=True,
            ),
            metadata.Record(
                pathlib.Path(
                    "docs/90.references/data/0001-generated/m0001-generated.md"
                ),
                {
                    "title": "Generated Data Member",
                    "version": "1.0.0",
                    "type": "reference/data",
                    "status": "published",
                    "owner": "@buenhyden",
                    "updated": "2026-08-01",
                    "layer": "references",
                    "artifact_id": "DATA-0001-m0001",
                    "parent_ids": ["DATA-0001"],
                    "created": "2026-08-01",
                    "generated_by": "scripts/example.py",
                },
                "generated",
                frontmatter_present=True,
            ),
        ]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(
                record,
                profiles,
                manifest,
            )
            for record in records
        }
        rendered = metadata.render_report(records, profiles, findings)
        self.assertIn(
            "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
            rendered,
        )
        self.assertIn("allowed-syntax", rendered)
        # The Registry classifies this README, so the advisory inventory names
        # its registered profile instead of the retired legacy sub-profile.
        self.assertIn(
            "README profile=readme; consumer=registry; role=folder-index",
            rendered,
        )
        self.assertIn("generated profile; owner=scripts/example.py", rendered)
        self.assertIn("reviewed_at=forbidden:not-provided", rendered)

    def test_inventory_records_identity_relations_and_transition_evidence(self) -> None:
        profiles = current_profiles()
        parent = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/0123-parent.md"),
            {
                "status": "active",
                "artifact_id": "AD-0123",
                "artifact_type": "architecture-description",
                "parent_ids": [],
                "created": "2026-08-07",
                "updated": "2026-08-07",
            },
            "architecture-description",
            frontmatter_present=True,
        )
        child = metadata.Record(
                pathlib.Path("docs/03.specs/0123-child/spec.md"),
            {
                "status": "completed",
                "artifact_id": "SPEC-0123",
                "artifact_type": "spec",
                "parent_ids": ["AD-0123"],
                "created": "2026-08-07",
                "updated": "2026-08-07",
            },
            "spec",
            previous_status="active",
            frontmatter_present=True,
        )
        records = [parent, child]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(record, profiles, manifest)
            for record in records
        }
        report = metadata.render_report(records, profiles, findings)
        child_row = next(
            line
            for line in report.splitlines()
            if "docs/03.specs/0123-child/spec.md" in line
        )
        self.assertIn(
            "| valid | parents=resolved:1; order=declared-list; supersedes=not-provided |",
            child_row,
        )
        self.assertIn("available:active->completed; valid", child_row)
