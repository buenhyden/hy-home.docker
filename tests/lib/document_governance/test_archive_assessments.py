from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest
from types import SimpleNamespace

from scripts.lib.document_governance import archive_assessments as api


class ArchiveAssessmentTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.git("init", "-q")
        self.unit = "completed/03.specs/0001-example/"
        self.origin = "docs/03.specs/0001-example"
        self.task = "docs/03.specs/0002-approval/tasks/tsk-0001-approval.md"
        self.catalog = "docs/98.archive/retention-catalog.md"
        self.registry = SimpleNamespace(
            common={
                "archive_retention": {
                    "standard_version": "3.0.0",
                    "catalog_path": self.catalog,
                    "capture_section": "Retention Catalog",
                    "capture_columns": ["Record", "Class", "Names", "Source"],
                    "assessment_section": "Current Assessments",
                    "assessment_columns": [
                        "Record",
                        "Assessment",
                        "Availability",
                        "Current Owner",
                        "Decision",
                        "Reason",
                        "Assessed At",
                        "Hold",
                    ],
                    "assessment_values": [
                        "unreviewed",
                        "usable",
                        "superseded",
                        "withdrawn",
                        "invalidated",
                    ],
                    "availability_values": ["retained", "git-history-only"],
                    "default_assessment": "unreviewed",
                    "default_availability": "retained",
                    "absence_token": "none",
                }
            }
        )
        self.write(f"{self.origin}/spec.md", "# Preserved original\n")
        self.write(self.task, self.approval())
        self.commit("source")
        self.source = self.git("rev-parse", "HEAD")
        target = self.root / "docs/98.archive" / self.unit
        target.parent.mkdir(parents=True)
        self.git("mv", self.origin, str(target.relative_to(self.root)))
        self.write_catalog()
        self.commit("capture")

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            [
                "git",
                "-c",
                "user.name=fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                *args,
            ],
            cwd=self.root,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def approval(
        self, actions: tuple[str, ...] = ("assess", "remove", "rehabilitate")
    ) -> str:
        authorizations = "".join(
            f"  - unit: {self.unit}\n    action: {action}\n"
            "    approved_by: '@owner'\n    approved_at: '2026-09-28'\n"
            f"    evidence: '#approval-{action}'\n    status: approved\n"
            for action in actions
        )
        quotations = "".join(
            f"\n## Approval {action}\n\n"
            f"> @owner approved {action} for {self.unit} on 2026-09-28.\n"
            for action in actions
        )
        return (
            "---\ntype: sdlc/task\nstatus: in-progress\nowner: '@owner'\n"
            "artifact_id: SPEC-0002-TSK-0001\narchive_authorizations:\n"
            f"{authorizations}---\n# Approval\n{quotations}"
        )

    def write_catalog(self, assessment: str | None = None, **changes: str) -> None:
        text = (
            "# Catalog\n\n## Retention Catalog\n\n"
            "| Record | Class | Names | Source |\n| --- | --- | --- | --- |\n"
            f"| `{self.unit}` | completed | no durable contract | "
            f"`{self.source}:{self.origin}` |\n"
        )
        if assessment is not None:
            values = {
                "assessment": assessment,
                "availability": "retained",
                "owner": "none",
                "decision": f"{self.source}:{self.task}",
                "reason": "Evidence reviewed.",
                "date": "2026-09-28",
                "hold": "none",
            }
            values.update(changes)
            text += (
                "\n## Current Assessments\n\n"
                "| Record | Assessment | Availability | Current Owner | Decision | "
                "Reason | Assessed At | Hold |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                f"| `{self.unit}` | {values['assessment']} | "
                f"{values['availability']} | "
                f"{values['owner']} | `{values['decision']}` | {values['reason']} | "
                f"{values['date']} | {values['hold']} |\n"
            )
        self.write(self.catalog, text)

    def codes(self) -> set[str]:
        return {
            f.code
            for f in api.validate_archive_assessments(self.root, registry=self.registry)
        }

    def test_absent_assessment_has_effective_defaults_without_writing(self) -> None:
        before = (self.root / self.catalog).read_bytes()
        row = api.assessment_lookup(self.root, self.registry)[self.unit]
        self.assertEqual(("unreviewed", "retained"), (row.assessment, row.availability))
        self.assertEqual(
            (self.source, self.origin),
            api.capture_sources(self.root, self.registry)[self.unit],
        )
        self.assertEqual(set(), self.codes())
        self.assertEqual(before, (self.root / self.catalog).read_bytes())

    def test_pinned_matching_task_approval_passes(self) -> None:
        self.write_catalog("usable")
        self.assertEqual(set(), self.codes())

    def test_bad_rows_and_duplicate_assessments_fail_closed(self) -> None:
        for changes in (
            {"date": "2026-02-30"},
            {"reason": " "},
            {"availability": "purged"},
            {"owner": "none", "assessment": "superseded"},
        ):
            with self.subTest(changes=changes):
                self.write_catalog(**{"assessment": "usable", **changes})
                self.assertTrue(self.codes())
        self.write_catalog("usable")
        path = self.root / self.catalog
        text = path.read_text()
        path.write_text(text + text.splitlines()[-1] + "\n")
        with self.assertRaises(ValueError):
            api.assessment_lookup(self.root, self.registry)

    def test_approval_rejects_wrong_action_unit_owner_status_or_quote(self) -> None:
        for old, new in (
            ("status: in-progress", "status: draft"),
            ("type: sdlc/task", "type: sdlc/adr"),
            ("status: approved", "status: proposed"),
            ("approved_by: '@owner'", "approved_by: '@stranger'"),
            (f"unit: {self.unit}", "unit: retired/01.requirements/9999-other.md"),
            ("action: assess", "action: remove"),
            ("> @owner approved assess", "@owner approved assess"),
        ):
            with self.subTest(change=new):
                self.write(self.task, self.approval().replace(old, new))
                self.write_catalog()
                self.commit("bad approval")
                decision = f"{self.git('rev-parse', 'HEAD')}:{self.task}"
                self.write_catalog("usable", decision=decision)
                self.assertIn("assessment-approval-invalid", self.codes())

    def test_history_only_requires_whole_absence_approval_and_no_hold(self) -> None:
        self.write_catalog("withdrawn", availability="git-history-only")
        self.assertIn("assessment-history-only-payload-present", self.codes())
        (self.root / "docs/98.archive" / self.unit / "spec.md").unlink()
        self.assertEqual(set(), self.codes())
        self.write_catalog(
            "withdrawn", availability="git-history-only", hold="review pending"
        )
        self.assertIn("assessment-removal-held", self.codes())
        self.write_catalog("withdrawn")
        self.assertIn("assessment-retained-payload-missing", self.codes())

    def test_capture_and_assessment_rows_cannot_disappear_from_history(self) -> None:
        self.write_catalog("usable")
        self.commit("assess")
        self.write_catalog()
        self.assertIn("assessment-row-removed", self.codes())
        self.write(self.catalog, "# Catalog\n")
        (self.root / "docs/98.archive" / self.unit / "spec.md").unlink()
        self.assertIn("capture-row-removed", self.codes())

    def test_previously_deleted_capture_is_found_beyond_head(self) -> None:
        (self.root / "docs/98.archive" / self.unit / "spec.md").unlink()
        self.write(self.catalog, "# Catalog\n")
        self.commit("unapproved loss")
        self.assertIn("capture-row-removed", self.codes())

    def test_invalidated_rehabilitation_needs_specific_authorization(self) -> None:
        self.write_catalog("invalidated")
        self.commit("invalidate")
        self.write(self.task, self.approval(("assess",)))
        self.commit("ordinary reassessment approval")
        self.write_catalog(
            "usable", decision=f"{self.git('rev-parse', 'HEAD')}:{self.task}"
        )
        self.assertIn("assessment-approval-invalid", self.codes())
        self.write_catalog("invalidated")
        self.write(self.task, self.approval())
        self.commit("fresh rehabilitation approval")
        self.write_catalog(
            "usable",
            reason="Corrected evidence rehabilitates the record.",
            decision=f"{self.git('rev-parse', 'HEAD')}:{self.task}",
        )
        self.assertEqual(set(), self.codes())

    def test_committed_row_deletion_cannot_be_hidden_by_restoration(self) -> None:
        self.write_catalog("usable")
        self.commit("assess")
        restored = (self.root / self.catalog).read_text()
        self.write_catalog()
        self.commit("erase assessment")
        self.write(self.catalog, restored)
        self.assertIn("assessment-row-removed", self.codes())

    def test_missing_uncatalogued_historical_unit_is_not_invisible(self) -> None:
        other = "docs/98.archive/resolved/05.operations/incidents/2026/0001-example"
        self.write(other + "/incident.md", "# Incident\n")
        self.write(other + "/postmortem.md", "# Postmortem\n")
        self.commit("legacy uncatalogued incident")
        (self.root / other / "incident.md").unlink()
        (self.root / other / "postmortem.md").unlink()
        self.commit("erase whole incident")
        self.assertIn("capture-history-unit-unrecorded", self.codes())

    def test_retained_partial_unit_is_rejected(self) -> None:
        self.write(f"{self.origin}/spec.md", "# Source\n")
        self.write(f"{self.origin}/plan.md", "# Plan\n")
        self.commit("larger source")
        self.source = self.git("rev-parse", "HEAD")
        # The capture source changes too, but member loss must have its own finding.
        self.write_catalog()
        self.assertIn("assessment-unit-partial", self.codes())

    def test_negative_or_fenced_approval_quote_does_not_authorize(self) -> None:
        for replacement in (
            "> @owner has not approved assess",
            "```text\n> @owner approved assess",
            "```text\n```not-a-close\n> @owner approved assess",
            "    > @owner approved assess",
        ):
            with self.subTest(replacement=replacement):
                text = self.approval().replace("> @owner approved assess", replacement)
                if replacement.startswith("```"):
                    text = text.replace("## Approval remove", "```\n## Approval remove")
                self.write(self.task, text)
                self.write_catalog()
                self.commit("invalid quotation")
                self.write_catalog(
                    "usable", decision=f"{self.git('rev-parse', 'HEAD')}:{self.task}"
                )
                self.assertIn("assessment-approval-invalid", self.codes())

    def test_public_retention_route_checks_approval_and_allows_whole_removal(
        self,
    ) -> None:
        import dataclasses
        import json
        from unittest import mock

        from scripts.lib.document_governance import archive
        from scripts.lib.document_governance.registry import (
            DEFAULT_REGISTRY,
            load_registry,
        )

        registered = load_registry()
        contract = {
            **self.registry.common["archive_retention"],
            "legacy_capture_revision": self.source,
            "legacy_transition_units": registered.common["archive_retention"][
                "legacy_transition_units"
            ],
        }
        registered = dataclasses.replace(
            registered, common={**registered.common, "archive_retention": contract}
        )
        raw_registry = json.loads(DEFAULT_REGISTRY.read_text())
        raw_registry["common"]["archive_retention"]["legacy_capture_revision"] = (
            self.source
        )
        self.write("docs/99.templates/registry.json", json.dumps(raw_registry))
        self.commit("register fixture contract")
        self.write_catalog("withdrawn", availability="git-history-only")
        payload = self.root / "docs/98.archive" / self.unit
        (payload / "spec.md").unlink()
        payload.rmdir()
        payload.parent.rmdir()
        with mock.patch.object(archive, "_catalog_registry", return_value=registered):
            self.assertEqual((), archive.validate_retention(self.root, self.source))
            self.assertEqual((), archive.validate_retention_catalog(self.root))
            self.write_catalog(
                "withdrawn", availability="git-history-only", hold="pending"
            )
            codes = {
                finding.code
                for finding in archive.validate_retention(self.root, self.source)
            }
            self.assertIn("assessment-removal-held", codes)
            self.assertTrue(archive.validate_retention_catalog(self.root))

    def test_committed_rehabilitation_still_needs_its_specific_action(self) -> None:
        self.write(self.task, self.approval(("assess",)))
        self.commit("ordinary approval")
        decision = f"{self.git('rev-parse', 'HEAD')}:{self.task}"
        self.write_catalog("invalidated", decision=decision)
        self.commit("invalidate")
        self.write_catalog(
            "usable", decision=decision, reason="Evidence was corrected."
        )
        self.commit("unapproved rehabilitation")
        self.assertIn("assessment-approval-invalid", self.codes())

    def test_committed_resurrection_is_not_hidden_by_current_retained_state(
        self,
    ) -> None:
        payload = self.root / "docs/98.archive" / self.unit / "spec.md"
        body = payload.read_text()
        payload.unlink()
        self.write_catalog("withdrawn", availability="git-history-only")
        self.commit("remove with scoped authorization")
        self.write(str(payload.relative_to(self.root)), body)
        self.write_catalog("usable", reason="Restored without a new current document.")
        self.commit("resurrect")
        self.assertIn("assessment-payload-resurrection", self.codes())

    def test_malformed_authorization_values_report_instead_of_crashing(self) -> None:
        for old, new in (
            ("action: assess", "action: [assess]"),
            ("status: in-progress", "status: [in-progress]"),
            ("approved_by: '@owner'", "approved_by: {owner: yes}"),
        ):
            with self.subTest(value=new):
                self.write(self.task, self.approval().replace(old, new))
                self.write_catalog()
                self.commit("malformed approval")
                self.write_catalog(
                    "usable", decision=f"{self.git('rev-parse', 'HEAD')}:{self.task}"
                )
                self.assertIn("assessment-approval-invalid", self.codes())

    def test_approval_quote_in_html_comment_is_not_evidence(self) -> None:
        text = self.approval().replace("## Approval assess", "<!--\n## Approval assess")
        text = text.replace("## Approval remove", "-->\n## Approval remove")
        self.write(self.task, text)
        self.commit("commented approval")
        self.write_catalog(
            "usable", decision=f"{self.git('rev-parse', 'HEAD')}:{self.task}"
        )
        self.assertIn("assessment-approval-invalid", self.codes())

    def test_unrelated_older_base_does_not_replace_latest_assessment(self) -> None:
        self.write_catalog("usable")
        self.commit("assess retained")
        self.write("unrelated.txt", "fixture\n")
        self.commit("unrelated baseline")
        base = self.git("rev-parse", "HEAD")
        payload = self.root / "docs/98.archive" / self.unit / "spec.md"
        body = payload.read_text()
        payload.unlink()
        self.write_catalog("withdrawn", availability="git-history-only")
        self.commit("approved history only")
        self.write(str(payload.relative_to(self.root)), body)
        self.write_catalog("usable", reason="Attempted resurrection.")
        codes = {
            finding.code
            for finding in api.validate_archive_assessments(
                self.root, base=base, registry=self.registry
            )
        }
        self.assertIn("assessment-payload-resurrection", codes)

    def test_malformed_current_owner_status_reports_instead_of_crashing(self) -> None:
        owner = "docs/02.architecture/descriptions/0004-owner.md"
        self.write(owner, "---\nstatus: [active]\nartifact_id: AD-0004\n---\n# Owner\n")
        self.commit("malformed owner")
        self.write_catalog("superseded", owner=f"`{owner}`")
        self.assertIn("assessment-owner-invalid", self.codes())

    def test_parallel_catalog_and_readme_edits_do_not_fake_row_deletion(self) -> None:
        initial = self.git("symbolic-ref", "--short", "HEAD")
        self.git("checkout", "-q", "-b", "assessment-branch")
        self.write_catalog("usable")
        self.commit("assess on parallel branch")
        self.git("checkout", "-q", initial)
        self.write("docs/98.archive/README.md", "# Archive navigation\n")
        self.commit("change only navigation")
        self.git("merge", "--no-edit", "assessment-branch")
        self.assertEqual(set(), self.codes())

    def test_capture_source_lookup_rejects_wrong_origin_or_unreachable_object(
        self,
    ) -> None:
        original = (self.root / self.catalog).read_text()
        tree = self.git("rev-parse", "HEAD^{tree}")
        orphan = self.git("commit-tree", tree, "-m", "orphan fixture")
        for source in (
            f"{self.source}:docs/03.specs/0002-approval",
            f"{orphan}:{self.origin}",
            f"{tree}:{self.origin}",
        ):
            with self.subTest(source=source):
                self.write(
                    self.catalog,
                    original.replace(f"{self.source}:{self.origin}", source),
                )
                with self.assertRaises(ValueError):
                    api.capture_sources(self.root, self.registry)

    def test_surface_assessment_removal_and_unapproved_change_are_rejected(
        self,
    ) -> None:
        self.write_catalog("usable")
        prior = (self.root / self.catalog).read_text()
        self.write_catalog()
        current = (self.root / self.catalog).read_text()
        findings = api.validate_assessment_snapshot(
            self.root, current, prior, self.registry, "index"
        )
        self.assertIn("assessment-row-removed", {item.code for item in findings})
        self.assertTrue(all(item.detail == "index" for item in findings))
        self.write_catalog("usable", decision=f"{self.source}:{self.origin}/spec.md")
        current = (self.root / self.catalog).read_text()
        findings = api.validate_assessment_snapshot(
            self.root, current, prior, self.registry, "index"
        )
        self.assertIn("assessment-approval-invalid", {item.code for item in findings})

    def test_unrelated_tracked_document_move_does_not_hide_current_owner(self) -> None:
        owner = "docs/02.architecture/descriptions/0004-owner.md"
        old = "docs/02.architecture/decisions/0003-moved.md"
        self.write(owner, "---\nstatus: active\nartifact_id: AD-0004\n---\n# Owner\n")
        self.write(old, "---\nstatus: accepted\nartifact_id: ADR-0003\n---\n# Old\n")
        self.commit("current owner and old document")
        (self.root / old).unlink()
        (self.root / old).parent.rmdir()
        self.write_catalog("superseded", owner="AD-0004")
        self.assertEqual(set(), self.codes())

    def test_historical_assessment_cannot_borrow_a_later_merged_approval(self) -> None:
        initial = self.git("symbolic-ref", "--short", "HEAD")
        self.git("checkout", "-q", "-b", "approval-branch")
        self.write(self.task, self.approval() + "\nNew approval revision.\n")
        self.commit("approval on sibling")
        approval = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", initial)
        self.write_catalog("usable", decision=f"{approval}:{self.task}")
        self.commit("assessment before approval ancestry")
        self.git("merge", "--no-edit", "approval-branch")
        self.assertIn("assessment-approval-invalid", self.codes())

    def test_removing_registered_contract_cannot_disable_public_gates(self) -> None:
        import json

        from scripts.lib.document_governance import archive

        registry_path = "docs/99.templates/registry.json"
        self.write(
            registry_path,
            json.dumps(
                {
                    "common": {
                        "archive_disposition_model": "adopted",
                        "archive_retention": self.registry.common["archive_retention"],
                    }
                }
            ),
        )
        self.commit("adopt assessment contract")
        self.write(
            registry_path,
            json.dumps({"common": {"archive_disposition_model": "adopted"}}),
        )
        self.commit("attempt policy downgrade")
        codes = {finding.code for finding in archive.validate_retention(self.root)}
        self.assertIn("assessment-contract-unavailable", codes)
        self.assertTrue(archive.validate_retention_catalog(self.root))

    def test_changed_assessment_requires_fresh_pinned_decision_and_reason(self) -> None:
        self.write_catalog("usable")
        self.commit("assess usable")
        self.write_catalog("withdrawn", reason="Current reliance was withdrawn.")
        self.assertIn("assessment-decision-unchanged", self.codes())
        self.write_catalog("usable")
        self.write(self.task, self.approval() + "\nNew assessment approval.\n")
        self.commit("fresh approval")
        decision = f"{self.git('rev-parse', 'HEAD')}:{self.task}"
        self.write_catalog("withdrawn", decision=decision)
        self.assertIn("assessment-reason-unchanged", self.codes())
        self.write_catalog(
            "withdrawn", decision=decision, reason="Current reliance was withdrawn."
        )
        self.assertEqual(set(), self.codes())

    def test_index_owner_retirement_cannot_be_hidden_by_worktree(self) -> None:
        owner = "docs/02.architecture/descriptions/0004-owner.md"
        text = "---\nstatus: active\nartifact_id: AD-0004\n---\n# Owner\n"
        self.write(owner, text)
        self.commit("owner")
        self.write_catalog("superseded", owner="AD-0004")
        catalog = (self.root / self.catalog).read_text()
        self.assertEqual(
            (),
            api.validate_assessment_snapshot(
                self.root, catalog, None, self.registry, "HEAD"
            ),
        )
        self.git("rm", "--cached", owner)
        findings = api.validate_assessment_snapshot(
            self.root, catalog, None, self.registry, "index"
        )
        self.assertIn("assessment-owner-invalid", {item.code for item in findings})
        self.write(owner, text.replace("active", "retired"))
        self.git("add", owner)
        self.write(owner, text)
        findings = api.validate_assessment_snapshot(
            self.root, catalog, None, self.registry, "index"
        )
        self.assertIn("assessment-owner-invalid", {item.code for item in findings})

    def test_history_only_requires_previously_archived_payload(self) -> None:
        self.git("reset", "--hard", self.source)
        self.write_catalog("withdrawn", availability="git-history-only")
        self.assertIn("assessment-removal-without-capture", self.codes())
        findings = api.validate_assessment_snapshot(
            self.root,
            (self.root / self.catalog).read_text(),
            None,
            self.registry,
            "index",
        )
        self.assertIn(
            "assessment-removal-without-capture", {item.code for item in findings}
        )

    def test_index_registry_owner_classification_uses_selected_surface(self) -> None:
        import json

        from scripts.lib.document_governance.registry import DEFAULT_REGISTRY

        raw = json.loads(DEFAULT_REGISTRY.read_text())
        owner = "docs/02.architecture/descriptions/0004-owner.md"
        self.write(owner, "---\nstatus: active\nartifact_id: AD-0004\n---\n")
        self.write("docs/99.templates/registry.json", json.dumps(raw))
        self.commit("registry and owner")
        self.assertTrue(api._current_owner(self.root, "AD-0004", "index"))
        original = (self.root / "docs/99.templates/registry.json").read_text()
        raw["profiles"] = [
            profile
            for profile in raw["profiles"]
            if profile["id"] != "architecture-description"
        ]
        self.write("docs/99.templates/registry.json", json.dumps(raw))
        self.git("add", "docs/99.templates/registry.json")
        self.write("docs/99.templates/registry.json", original)
        try:
            accepted = api._current_owner(self.root, "AD-0004", "index")
        except ValueError:
            accepted = False
        self.assertFalse(accepted)

    def test_shallow_history_is_not_a_pass(self) -> None:
        (self.root / ".git/shallow").write_text(self.git("rev-parse", "HEAD") + "\n")
        self.assertIn("assessment-history-unavailable", self.codes())


if __name__ == "__main__":
    unittest.main()
