"""Lifecycle generation 6 contracts (SPEC-0231)."""

from __future__ import annotations

import dataclasses
import pathlib
import unittest

from scripts.lib.document_governance import spec_packages as module
from scripts.lib.document_governance.registry import load_registry

ROOT = pathlib.PurePosixPath("docs/03.specs/0001-example")
SPEC = module.SpecDocument(
    ROOT / "spec.md",
    "spec",
    "SPEC-0001",
    "approved",
    ("REQ-0001",),
    "## Acceptance Criteria\n\n1. First.\n2. Second.\n",
)
PLAN = module.SpecDocument(
    ROOT / "plan.md",
    "plan",
    "SPEC-0001-PLAN-0001",
    "approved",
    ("SPEC-0001",),
    """## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | First | None | TSK-0001 | Check |
| W2 | 2 | Second | W1 | TSK-0001 | Check |
""",
)
HEADER = """## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""
ACCEPTANCE = """
## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
"""


def task(
    evidence: str,
    acceptance: str,
    status: str = "in-progress",
    *,
    items: tuple[tuple[str, ...], ...] = (),
) -> module.SpecDocument:
    return module.SpecDocument(
        ROOT / "tasks/tsk-0001-work.md",
        "task",
        "SPEC-0001-TSK-0001",
        status,
        ("SPEC-0001-PLAN-0001",),
        HEADER + evidence + ACCEPTANCE + acceptance,
        items=items,
    )


PASS_BOTH = """| One | 1 | W1 | Unit | fixture | PASS | test | - |
| Two | 2 | W2 | Unit | fixture | PASS | test | - |
"""
ACCEPT_BOTH = """| 1 | accepted | One | - |
| 2 | accepted | Two | - |
"""


class Generation6EvidenceTests(unittest.TestCase):
    registry = load_registry()

    def contract(self, *tasks: module.SpecDocument) -> module.PackageEvidence:
        return module._v6_evidence_contract(SPEC, PLAN, tasks, self.registry)

    def test_completed_task_with_pass_and_accepted_criteria_is_ready(self) -> None:
        done = task(PASS_BOTH, ACCEPT_BOTH, "completed")
        package = module.SpecPackage(
            pathlib.Path(ROOT), "0001", "example", SPEC, PLAN, (done,), ()
        )
        self.assertEqual(
            (), module.archive_readiness_findings(package, self.contract(done))
        )

    def test_unresolved_fail_blocks_acceptance(self) -> None:
        rows = PASS_BOTH + "| Retry | 1 | W1 | Unit | fixture | FAIL | test | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "unresolved FAIL"):
            self.contract(task(rows, ACCEPT_BOTH))

    def test_a_later_pass_resolves_an_earlier_fail(self) -> None:
        rows = """| Broken | 1 | W1 | Unit | fixture | FAIL | test | - |
| One | 1 | W1 | Unit | fixture | PASS | test | Broken |
| Two | 2 | W2 | Unit | fixture | PASS | test | - |
"""
        evidence = self.contract(task(rows, ACCEPT_BOTH))
        self.assertEqual(frozenset(), evidence.unresolved_failures)

    def test_resolves_must_name_an_earlier_fail_with_a_shared_criterion(self) -> None:
        for resolves in ("Missing", "Two"):
            rows = f"""| One | 1 | W1 | Unit | fixture | PASS | test | - |
| Two | 2 | W2 | Unit | fixture | FAIL | test | - |
| Three | 1 | W1 | Unit | fixture | PASS | test | {resolves} |
"""
            with self.subTest(resolves=resolves):
                with self.assertRaisesRegex(module.SpecPackageError, "Resolves"):
                    self.contract(task(rows, "| 1 | pending | - | - |\n"))

    def test_accepted_criterion_needs_pass_evidence(self) -> None:
        rows = "| One | 1 | W1 | Unit | fixture | NOT_RUN | test | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "no PASS"):
            self.contract(task(rows, "| 1 | accepted | One | - |\n"))

    def test_rejected_and_not_required_need_a_decision(self) -> None:
        for decision in ("rejected", "not-required"):
            with self.subTest(decision=decision):
                with self.assertRaisesRegex(module.SpecPackageError, "Decision"):
                    self.contract(task(PASS_BOTH, f"| 1 | {decision} | - | - |\n"))

    def test_one_decision_per_criterion(self) -> None:
        twice = "| 1 | accepted | One | - |\n| 1 | pending | - | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "more than one"):
            self.contract(task(PASS_BOTH, twice))

    def test_evidence_names_are_unique(self) -> None:
        rows = PASS_BOTH + "| One | 1 | W1 | Unit | fixture | PASS | test | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "unique"):
            self.contract(task(rows, "| 1 | pending | - | - |\n"))

    def test_completed_task_needs_its_criteria_accepted(self) -> None:
        pending = "| 1 | accepted | One | - |\n| 2 | pending | - | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "criteria accepted"):
            self.contract(task(PASS_BOTH, pending, "completed"))

    def test_completed_task_needs_pass_for_every_assigned_pair(self) -> None:
        rows = "| One | 1 | W1 | Unit | fixture | PASS | test | - |\n"
        decisions = "| 1 | accepted | One | - |\n| 2 | not-required | - | Dropped |\n"
        self.contract(task(rows, decisions, "completed"))
        with self.assertRaisesRegex(module.SpecPackageError, "PASS evidence"):
            self.contract(task(rows, "| 1 | accepted | One | - |\n", "completed"))

    def test_open_criteria_and_tasks_keep_a_package_unready(self) -> None:
        current = task(PASS_BOTH, "| 1 | accepted | One | - |\n")
        package = module.SpecPackage(
            pathlib.Path(ROOT), "0001", "example", SPEC, PLAN, (current,), ()
        )
        self.assertEqual(
            ("SPEC-0001-TSK-0001 is in-progress", "criterion 2 is not accepted"),
            module.archive_readiness_findings(package, self.contract(current)),
        )


ITEMS_HEADER = """## Work Log

### Execution Items

| Item | Work Unit | Scope | Owner | Status | Blocker |
| --- | --- | --- | --- | --- | --- |
"""


class Generation6ItemTests(unittest.TestCase):
    registry = load_registry()

    def test_items_derive_the_task_status(self) -> None:
        body = ITEMS_HEADER + (
            "| A | W1 | First | @owner | completed | - |\n"
            "| B | W2 | Second | @owner | blocked | Waiting on review |\n"
        )
        rows = module._execution_item_rows(body, self.registry, ROOT / "t.md")
        self.assertEqual(
            "blocked",
            module._item_status_summary(
                [row[4] for row in rows], frozenset({"completed", "cancelled"})
            ),
        )

    def test_items_reject_shared_work_units_and_silent_blockers(self) -> None:
        for second in (
            "| B | W1 | Second | @owner | draft | - |",
            "| B | W2 | Second | @owner | blocked | - |",
        ):
            body = ITEMS_HEADER + "| A | W1 | First | @owner | draft | - |\n" + second
            with self.subTest(second=second):
                with self.assertRaises(module.SpecPackageError):
                    module._execution_item_rows(body, self.registry, ROOT / "t.md")

    def test_a_completed_item_needs_pass_for_its_work(self) -> None:
        items = (
            ("A", "W1", "First", "@owner", "completed", "-"),
            ("B", "W2", "Second", "@owner", "in-progress", "-"),
        )
        passed = task(
            "| One | 1 | W1 | Unit | fixture | PASS | test | - |\n",
            "| 1 | accepted | One | - |\n",
            items=items,
        )
        module._v6_evidence_contract(SPEC, PLAN, (passed,), self.registry)
        not_run = task(
            "| One | 1 | W1 | Unit | fixture | NOT_RUN | test | - |\n",
            "| 1 | pending | - | - |\n",
            items=items,
        )
        with self.assertRaisesRegex(module.SpecPackageError, "PASS evidence"):
            module._v6_evidence_contract(SPEC, PLAN, (not_run,), self.registry)


class Generation6ParentTests(unittest.TestCase):
    def parents(self, spec: str, plan: str, *tasks: str) -> None:
        module._validate_parent_authority(
            module.SpecDocument(ROOT / "spec.md", "spec", "SPEC-0001", spec, ()),
            module.SpecDocument(
                ROOT / "plan.md", "plan", "SPEC-0001-PLAN-0001", plan, ()
            ),
            tuple(
                module.SpecDocument(
                    ROOT / f"tasks/tsk-{index:04d}-x.md",
                    "task",
                    f"SPEC-0001-TSK-{index:04d}",
                    status,
                    (),
                )
                for index, status in enumerate(tasks, 1)
            ),
        )

    def test_tasks_run_only_under_approved_parents(self) -> None:
        self.parents("approved", "approved", "in-progress", "blocked")
        self.parents("in-review", "draft", "draft", "blocked", "completed")
        with self.assertRaisesRegex(module.SpecPackageError, "approved Spec and Plan"):
            self.parents("in-review", "in-review", "in-progress")

    def test_a_running_item_needs_approved_parents(self) -> None:
        items = (
            ("A", "W1", "First", "@owner", "in-progress", "-"),
            ("B", "W2", "Second", "@owner", "blocked", "Waiting on review"),
        )
        running = module.SpecDocument(
            ROOT / "tasks/tsk-0001-x.md",
            "task",
            "SPEC-0001-TSK-0001",
            "blocked",
            (),
            items=items,
        )
        with self.assertRaisesRegex(module.SpecPackageError, "approved Spec and Plan"):
            module._validate_parent_authority(
                dataclasses.replace(SPEC, status="in-review"),
                dataclasses.replace(PLAN, status="in-review"),
                (running,),
            )

    def test_plan_cannot_be_ahead_of_its_spec(self) -> None:
        with self.assertRaisesRegex(module.SpecPackageError, "ahead"):
            self.parents("draft", "approved")

    def test_execution_statuses_are_not_parent_statuses(self) -> None:
        for status in ("in-progress", "blocked", "completed"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(module.SpecPackageError, "outside"):
                    self.parents(status, status)


if __name__ == "__main__":
    unittest.main()
