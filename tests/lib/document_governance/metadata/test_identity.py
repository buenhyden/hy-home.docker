"""Identity inventory and report CLI tests."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance.metadata import identity as identity_module
from tests.lib.document_governance.metadata._support import (
    current_profiles,
    metadata,
    run_checker,
    write_doc,
)


class CheckerCliTests(unittest.TestCase):
    def test_duplicate_artifact_id_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            values = {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
            }
            write_doc(root / "docs/03.specs/spec-0123-a/spec.md", values)
            write_doc(root / "docs/03.specs/spec-0123-b/spec.md", values)
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("duplicate-artifact-id", result.stdout)
            self.assertIn("| duplicate |", result.stdout)

    def test_duplicate_yaml_key_has_distinct_inventory_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertEqual(2, result.returncode)
            self.assertIn("frontmatter-duplicate-key", result.stdout)
            self.assertIn("| duplicate-key |", result.stdout)

    def test_report_returns_nonzero_for_parser_failure_but_renders_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: [active\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("frontmatter-malformed-yaml", result.stdout)
            self.assertIn(path.relative_to(root).as_posix(), result.stdout)

    def test_unhashable_mapping_key_has_no_traceback_and_writes_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            output = root / "inventory.md"
            result = run_checker(root, "report", "--output", str(output))
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("frontmatter-malformed-yaml", rendered)
            self.assertIn("malformed-yaml", rendered)

    def test_report_order_is_deterministic_and_sorted_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/spec-0200-z/spec.md", {"status": "active"})
            write_doc(root / "docs/01.requirements/prd-0100-a.md", {"status": "active"})
            first = run_checker(root, "report")
            second = run_checker(root, "report")
            self.assertEqual(first.stdout, second.stdout)
            self.assertLess(
                first.stdout.index("docs/01.requirements/prd-0100-a.md"),
                first.stdout.index("docs/03.specs/spec-0200-z/spec.md"),
            )

    def test_report_output_check_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", None)
            output = root / "inventory.md"
            generated = run_checker(root, "report", "--output", str(output))
            fresh = run_checker(root, "report", "--output", str(output), "--check")
            output.write_text("stale\n", encoding="utf-8")
            stale = run_checker(root, "report", "--output", str(output), "--check")
            self.assertEqual(0, generated.returncode, generated.stderr)
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("metadata inventory is stale", stale.stderr)

    def test_active_mode_is_available_but_semantic_gate_is_not_auto_invoked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/spec-0123-example/spec.md", {"status": "active"})
            result = run_checker(root, "check-active")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("metadata check-active", result.stdout)

    def test_inventory_exposes_all_semantic_state_columns(self) -> None:
        profiles = current_profiles()
        records = [
            metadata.Record(
                pathlib.Path("docs/03.specs/README.md"),
                {"type": "common/readme", "status": "active"},
                "readme",
                frontmatter_present=True,
            ),
            metadata.Record(
                pathlib.Path(
                    "docs/90.references/data/0001-generated/m0001-generated.md"
                ),
                {
                    "title": "Generated Data Member",
                    "type": "references/data-member",
                    "layer": "reference",
                    "status": "active",
                    "owner": "@buenhyden",
                    "artifact_id": "DATA-0001-m0001",
                    "parent_ids": ["DATA-0001"],
                    "created": "2026-08-01",
                    "updated": "2026-08-01",
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
        self.assertIn(
            "README profile=unclassified; consumer=unavailable; role=folder-index",
            rendered,
        )
        self.assertIn("generated profile; owner=scripts/example.py", rendered)
        self.assertIn("reviewed_at=forbidden:not-provided", rendered)

    def test_inventory_records_identity_relations_and_transition_evidence(self) -> None:
        profiles = current_profiles()
        parent = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/ad-0123-parent.md"),
            {
                "status": "active",
                "artifact_id": "architecture-description:0123-parent",
                "artifact_type": "architecture-description",
                "parent_ids": [],
                "created": "2026-08-07",
                "updated": "2026-08-07",
            },
            "architecture-description",
            frontmatter_present=True,
        )
        child = metadata.Record(
            pathlib.Path("docs/03.specs/spec-0123-child/spec.md"),
            {
                "status": "completed",
                "artifact_id": "spec:0123-child",
                "artifact_type": "spec",
                "parent_ids": ["architecture-description:0123-parent"],
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
            record.path.as_posix(): metadata.validate_record(record, profiles, manifest) for record in records
        }
        report = metadata.render_report(records, profiles, findings)
        child_row = next(line for line in report.splitlines() if "docs/03.specs/spec-0123-child/spec.md" in line)
        self.assertIn("| valid | parents=resolved:1; order=declared-list; supersedes=not-provided |", child_row)
        self.assertIn("available:active->completed; valid", child_row)
