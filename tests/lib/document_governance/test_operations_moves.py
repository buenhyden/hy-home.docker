from __future__ import annotations

import json
import pathlib
import unittest
from dataclasses import FrozenInstanceError, replace

from scripts.lib.document_governance.operations_moves import (
    DocumentInput,
    MoveError,
    ReviewedMove,
    preflight_operations_moves,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]
PROFILES = {
    row["id"]: row
    for row in json.loads((ROOT / "docs/99.templates/registry.json").read_text())[
        "profiles"
    ]
}
DOMAINS = ("security", "workflow", "labs")


def document(
    path="docs/05.operations/guides/0031-example-note.md",
    artifact="GDE-0031",
    kind="guide",
):
    return DocumentInput(
        path,
        f"---\ntitle: Synthetic\ntype: operation/{kind}\nartifact_id: {artifact}\n---\n# 합성 문서\n",
    )


def reviewed(doc, domain="security", lab=False):
    family = doc.path.split("/")[2]
    name = doc.path.split("/")[-1]
    return ReviewedMove(
        doc.path,
        "GDE-0031",
        f"docs/05.operations/{family}/{domain}/{name}",
        domain,
        lab,
    )


class OperationsMovesTests(unittest.TestCase):
    def run_plan(self, docs, rows=(), domains=DOMAINS):
        return preflight_operations_moves(
            tuple(docs), tuple(rows), profiles=PROFILES, domains=domains
        )

    def test_exact_review_preserves_filename_suffix_and_plans_readme_coverage(self):
        doc = document()
        result = self.run_plan([doc], [reviewed(doc)])
        self.assertEqual("MOVE", result.entries[0].state)
        self.assertEqual(
            "docs/05.operations/guides/security/0031-example-note.md",
            result.entries[0].target,
        )
        self.assertEqual(
            (
                "docs/05.operations",
                "docs/05.operations/guides",
                "docs/05.operations/guides/security",
            ),
            result.required_readme_folders,
        )
        self.assertTrue(result.entries[0].source_registered)
        self.assertFalse(result.entries[0].target_registered)

    def test_unknown_subject_is_review_required_without_numeric_fallback(self):
        result = self.run_plan([document()])
        self.assertEqual("REVIEW_REQUIRED", result.entries[0].state)
        self.assertIsNone(result.entries[0].target)
        self.assertEqual((), result.required_readme_folders)

    def test_same_number_different_family_does_not_share_lab_classification(self):
        guide = document()
        run = document(
            "docs/05.operations/runbooks/0031-example.md", "RUN-0031", "runbook"
        )
        rows = [
            reviewed(guide, "labs", True),
            ReviewedMove(
                run.path,
                "RUN-0031",
                "docs/05.operations/runbooks/workflow/0031-example.md",
                "workflow",
                False,
            ),
        ]
        result = self.run_plan([guide, run], rows)
        self.assertEqual(
            ["labs", "workflow"], [entry.domain for entry in result.entries]
        )

    def test_lab_targets_are_inside_each_operations_family(self):
        for family, kind, prefix in (
            ("guides", "guide", "GDE"),
            ("policies", "policy", "POL"),
            ("runbooks", "runbook", "RUN"),
        ):
            with self.subTest(family=family):
                doc = document(
                    f"docs/05.operations/{family}/0031-example.md",
                    f"{prefix}-0031",
                    kind,
                )
                row = ReviewedMove(
                    doc.path,
                    f"{prefix}-0031",
                    f"docs/05.operations/{family}/labs/0031-example.md",
                    "labs",
                    True,
                )
                self.assertEqual(
                    row.target, self.run_plan([doc], [row]).entries[0].target
                )

    def test_arranged_source_is_proposal_not_current_registry_admission(self):
        doc = document("docs/05.operations/guides/security/0031-example-note.md")
        entry = self.run_plan([doc], [reviewed(doc)]).entries[0]
        self.assertEqual("ALREADY_ARRANGED", entry.state)
        self.assertFalse(entry.source_registered)

    def test_wrong_existing_domain_requires_review_instead_of_silent_move(self):
        doc = document("docs/05.operations/guides/workflow/0031-example-note.md")
        entry = self.run_plan([doc], [reviewed(doc)]).entries[0]
        self.assertEqual("REVIEW_REQUIRED", entry.state)
        self.assertEqual("existing-domain-conflict", entry.reason)

    def test_runtime_and_nonoperations_inputs_are_out_of_scope(self):
        for path in (
            "labs/kafka-cluster.md",
            "infra/04-data/docker-compose.yml",
            "docs/05.operations/README.md",
            "docs/05.operations/guides/README.md",
            "docs/05.operations/incidents/incident.md",
        ):
            with self.subTest(path=path):
                entry = self.run_plan([DocumentInput(path, "not YAML")]).entries[0]
                self.assertEqual("OUT_OF_SCOPE", entry.state)

    def assert_refused(self, code, docs, rows=(), domains=DOMAINS):
        with self.assertRaises(MoveError) as caught:
            self.run_plan(docs, rows, domains)
        self.assertEqual(code, caught.exception.code)

    def test_raw_unsafe_paths_rejected_before_normalization(self):
        for path in (
            "/docs/05.operations/guides/0031-example.md",
            "docs//05.operations/guides/a.md",
            "docs/./05.operations/guides/a.md",
            "docs/../05.operations/guides/a.md",
            "docs\\05.operations\\guides\\a.md",
            "",
            "docs/05.operations/guides/a.md/",
            "docs/05.operations/guides/a\x00.md",
        ):
            with self.subTest(path=path):
                self.assert_refused("unsafe-path", [DocumentInput(path, "")])

    def test_unsafe_review_paths_and_unknown_domains_refused(self):
        doc = document()
        row = reviewed(doc)
        for field in ("source", "target"):
            self.assert_refused(
                "unsafe-path", [doc], [replace(row, **{field: "../escape.md"})]
            )
        self.assert_refused("unknown-domain", [doc], [replace(row, domain="unknown")])
        for domain in ("../labs", "", "Security", "security/tools"):
            self.assert_refused("invalid-domain", [doc], [row], (domain,))

    def test_type_identity_and_parser_failures_propagate(self):
        for artifact, code in (
            ("RUN-0031", "artifact-id-invalid"),
            ("GDE-0032", "path-id-mismatch"),
        ):
            self.assert_refused(code, [document(artifact=artifact)])
        self.assert_refused("type-path-mismatch", [document(kind="runbook")])
        self.assert_refused(
            "frontmatter-missing", [DocumentInput(document().path, "# no metadata")]
        )
        self.assert_refused(
            "duplicate-key",
            [
                DocumentInput(
                    document().path,
                    "---\ntype: operation/guide\ntype: operation/guide\n---\n",
                )
            ],
        )
        self.assert_refused(
            "malformed-yaml", [DocumentInput(document().path, "---\ntype: [\n---\n")]
        )

    def test_review_exact_id_and_source_must_match(self):
        doc = document()
        self.assert_refused(
            "review-id-mismatch",
            [doc],
            [replace(reviewed(doc), artifact_id="GDE-0032")],
        )
        self.assert_refused(
            "review-source-missing",
            [doc],
            [replace(reviewed(doc), source="docs/05.operations/guides/0032-absent.md")],
        )

    def test_target_family_filename_and_lab_contracts_refused(self):
        doc = document()
        row = reviewed(doc)
        for target in (
            "labs/0031-example-note.md",
            "docs/05.operations/runbooks/security/0031-example-note.md",
            "docs/05.operations/guides/security/0031-renamed.md",
            "docs/05.operations/guides/security/deeper/0031-example-note.md",
        ):
            with self.subTest(target=target):
                self.assert_refused(
                    "target-contract", [doc], [replace(row, target=target)]
                )
        self.assert_refused("lab-domain-mismatch", [doc], [replace(row, lab=True)])
        self.assert_refused(
            "lab-domain-mismatch", [doc], [reviewed(doc, "labs", False)]
        )

    def test_source_review_and_identity_duplicates_refused(self):
        doc = document()
        self.assert_refused("source-collision", [doc, doc])
        self.assert_refused(
            "review-source-collision", [doc], [reviewed(doc), reviewed(doc)]
        )
        other = document("docs/05.operations/guides/0031-other.md")
        self.assert_refused("artifact-id-collision", [doc, other])
        self.assert_refused(
            "source-collision", [doc, DocumentInput(doc.path.upper(), "")]
        )

    def test_target_collides_with_other_existing_source_even_when_out_of_scope(self):
        doc = document()
        row = reviewed(doc)
        existing = DocumentInput(row.target.upper(), "")
        self.assert_refused("target-collision", [doc, existing], [row])

    def test_unknown_existing_domain_refused(self):
        doc = document("docs/05.operations/guides/unknown/0031-example-note.md")
        self.assert_refused("unknown-domain", [doc])

    def test_outputs_are_immutable_and_inputs_are_unchanged(self):
        doc = document()
        row = reviewed(doc)
        result = self.run_plan([doc], [row])
        with self.assertRaises(FrozenInstanceError):
            result.entries[0].state = "APPROVED"
        self.assertEqual("security", row.domain)
        self.assertEqual(document(), doc)

    def test_unadmitted_source_filename_and_excess_nesting_refused(self):
        self.assert_refused(
            "source-profile-invalid",
            [document("docs/05.operations/guides/not-numbered.md")],
        )
        self.assert_refused(
            "source-contract",
            [document("docs/05.operations/guides/security/deeper/0031-example.md")],
        )

    def test_review_cannot_classify_out_of_scope_input(self):
        doc = DocumentInput("labs/example.md", "")
        row = ReviewedMove(
            doc.path,
            "GDE-0031",
            "docs/05.operations/guides/labs/0031-example.md",
            "labs",
            True,
        )
        self.assert_refused("review-source-not-operation", [doc], [row])

    def test_empty_corpus_has_no_placeholder_folder_obligations(self):
        self.assertEqual((), self.run_plan([]).entries)
        self.assertEqual((), self.run_plan([]).required_readme_folders)

    def test_parser_cyclic_alias_refusal_propagates(self):
        text = "---\ntype: operation/guide\nartifact_id: GDE-0031\nx: &cycle [*cycle]\n---\n"
        self.assert_refused("cyclic-value", [DocumentInput(document().path, text)])

    def test_no_filesystem_or_process_calls_are_needed(self):
        from unittest.mock import patch

        with (
            patch("pathlib.Path.read_text", side_effect=AssertionError("no I/O")),
            patch("subprocess.run", side_effect=AssertionError("no process")),
        ):
            result = self.run_plan([document()], [reviewed(document())])
        self.assertEqual("MOVE", result.entries[0].state)

    def test_public_fixture_is_synthetic_and_exactly_bound(self):
        fixture = json.loads(
            (
                ROOT
                / "tests/fixtures/document_governance/operations-moves/reviewed-map.json"
            ).read_text()
        )
        self.assertEqual("synthetic", fixture["purpose"])
        docs = tuple(DocumentInput(**row) for row in fixture["documents"])
        rows = tuple(ReviewedMove(**row) for row in fixture["reviewed_moves"])
        plan = self.run_plan(docs, rows, tuple(fixture["domains"]))
        self.assertEqual(
            ["MOVE", "MOVE", "ALREADY_ARRANGED", "REVIEW_REQUIRED"],
            [entry.state for entry in plan.entries],
        )


if __name__ == "__main__":
    unittest.main()
