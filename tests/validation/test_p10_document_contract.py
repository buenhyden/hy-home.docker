"""P10 current-Task bindings for the generation 7 evidence contract."""

from __future__ import annotations

import pathlib
import unittest

from scripts.lib.document_governance import spec_packages
from scripts.lib.document_governance.registry import load_registry

REPOSITORY = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = pathlib.PurePosixPath(
    "docs/03.specs/0212-request-baseline-and-reconciliation"
)


TASK_CONTRACTS = (
    (
        "tsk-0047-image-supply-chain-storybook.md",
        (("86", "W91"), ("87", "W92"), ("88", "W93"), ("89", "W94")),
    ),
    (
        "tsk-0048-role-resource-retirement.md",
        (("90", "W95"), ("91", "W96"), ("92", "W97"), ("93", "W98")),
    ),
    (
        "tsk-0049-document-governance-qa-ci.md",
        (("94", "W99"), ("95", "W100"), ("96", "W101"), ("97", "W102")),
    ),
)


class P10DocumentContractTests(unittest.TestCase):
    def test_current_p08_to_p10_tasks_use_generation_7_evidence_contract(self) -> None:
        """Current Tasks bind every observation to their Plan work unit."""
        registry = load_registry(REPOSITORY / "docs/99.templates/registry.json")
        actual_plan_path = PACKAGE / "plan.md"
        actual_plan = spec_packages._snapshot_document(
            actual_plan_path,
            (REPOSITORY / actual_plan_path).read_text(encoding="utf-8"),
            registry=registry,
        )
        self.assertIsNotNone(actual_plan)
        assert actual_plan is not None
        actual_plan_rows = {
            row[0]: row for row in spec_packages._v5_plan_rows(actual_plan, registry)
        }
        for task_name, criterion_units in TASK_CONTRACTS:
            with self.subTest(task=task_name):
                task_path = PACKAGE / "tasks" / task_name
                task = spec_packages._snapshot_document(
                    task_path,
                    (REPOSITORY / task_path).read_text(encoding="utf-8"),
                    registry=registry,
                )
                self.assertIsNotNone(task)
                assert task is not None
                short_task_id = "-".join(task.artifact_id.split("-")[-2:])
                for criterion, work_unit in criterion_units:
                    self.assertIn(work_unit, actual_plan_rows)
                    actual_row = actual_plan_rows[work_unit]
                    self.assertEqual(criterion, actual_row[1])
                    self.assertIn(
                        short_task_id,
                        {reference.strip() for reference in actual_row[4].split(",")},
                    )

                spec = spec_packages.SpecDocument(
                    PACKAGE / "spec.md",
                    "spec",
                    "SPEC-0212",
                    "approved",
                    ("REQ-0027",),
                    "## Acceptance Criteria\n\n"
                    + "\n".join(
                        f"{criterion}. P10 contract fixture."
                        for criterion, _ in criterion_units
                    )
                    + "\n",
                )
                plan_rows = "\n".join(
                    f"| {work_unit} | {criterion} | P10 contract fixture | None | "
                    f"{task.artifact_id} | Generation 7 evidence |"
                    for criterion, work_unit in criterion_units
                )
                plan = spec_packages.SpecDocument(
                    PACKAGE / "plan.md",
                    "plan",
                    "SPEC-0212-PLAN-0001",
                    "approved",
                    ("SPEC-0212",),
                    """## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
"""
                    + plan_rows
                    + "\n",
                )

                evidence_rows = spec_packages._v6_evidence_rows(task, registry)
                observed_pairs = {
                    (criterion.strip(), row[2])
                    for row in evidence_rows
                    for criterion in row[1].split(",")
                }
                self.assertEqual(set(criterion_units), observed_pairs)

                acceptance_rows = spec_packages._criterion_acceptance_rows(
                    task, registry
                )
                self.assertEqual(
                    {criterion for criterion, _ in criterion_units},
                    {row[0] for row in acceptance_rows},
                )

                spec_packages._v6_evidence_contract(spec, plan, (task,), registry)


if __name__ == "__main__":
    unittest.main()
