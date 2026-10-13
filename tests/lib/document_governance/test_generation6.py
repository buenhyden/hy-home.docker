"""Lifecycle generation 6 contracts (SPEC-0231)."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import tempfile
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
ACCEPT_ONE = "| 1 | accepted | One | - |\n| 2 | pending | - | - |\n"
PENDING_BOTH = "| 1 | pending | - | - |\n| 2 | pending | - | - |\n"
# W1 and W2 assigned to two Tasks, so one Task can finish its share early.
SPLIT_PLAN = dataclasses.replace(
    PLAN,
    body=PLAN.body.replace(
        "| W2 | 2 | Second | W1 | TSK-0001 |", "| W2 | 2 | Second | W1 | TSK-0002 |"
    ),
)


def second_task(evidence: str, acceptance: str) -> module.SpecDocument:
    return dataclasses.replace(
        task(evidence, acceptance),
        path=ROOT / "tasks/tsk-0002-work.md",
        artifact_id="SPEC-0001-TSK-0002",
    )


def outcome(call, *args, **kwargs) -> str:
    try:
        call(*args, **kwargs)
    except module.SpecPackageError as error:
        return f"error: {error}"
    return "ok"


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
            self.contract(task(rows, ACCEPT_ONE))

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
            self.contract(task(rows, ACCEPT_ONE, "completed"))

    def test_open_criteria_and_tasks_keep_a_package_unready(self) -> None:
        current = task(PASS_BOTH, ACCEPT_ONE)
        package = module.SpecPackage(
            pathlib.Path(ROOT), "0001", "example", SPEC, PLAN, (current,), ()
        )
        self.assertEqual(
            ("SPEC-0001-TSK-0001 is in-progress", "criterion 2 is not accepted"),
            module.archive_readiness_findings(package, self.contract(current)),
        )

    def test_every_assigned_criterion_needs_one_row(self) -> None:
        self.contract(task(PASS_BOTH, PENDING_BOTH))
        with self.assertRaisesRegex(module.SpecPackageError, "no Criterion Acceptance"):
            self.contract(task(PASS_BOTH, "| 1 | pending | - | - |\n"))

    def test_a_row_outside_the_plan_assignment_is_rejected(self) -> None:
        one = "| One | 1 | W1 | Unit | fixture | PASS | test | - |\n"
        two = "| Two | 2 | W2 | Unit | fixture | PASS | test | - |\n"
        second = second_task(two, "| 2 | pending | - | - |\n")
        first = task(one, "| 1 | pending | - | - |\n")
        module._v6_evidence_contract(SPEC, SPLIT_PLAN, (first, second), self.registry)
        stray = task(one, PENDING_BOTH)
        with self.assertRaisesRegex(module.SpecPackageError, "outside the Plan Task"):
            module._v6_evidence_contract(
                SPEC, SPLIT_PLAN, (stray, second), self.registry
            )

    def test_acceptance_evidence_must_name_this_tasks_rows(self) -> None:
        self.contract(task(PASS_BOTH, ACCEPT_BOTH))
        cited = "| 1 | accepted | Missing | - |\n| 2 | pending | - | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "this Task's Evidence"):
            self.contract(task(PASS_BOTH, cited))

    def test_only_a_pass_row_may_resolve(self) -> None:
        rows = """| Broken | 1 | W1 | Unit | fixture | FAIL | test | - |
| Fixed | 1 | W1 | Unit | fixture | PASS | test | Broken |
"""
        self.contract(task(rows, PENDING_BOTH))
        again = rows.replace("| PASS | test | Broken |", "| FAIL | test | Broken |")
        with self.assertRaisesRegex(module.SpecPackageError, "only a PASS row"):
            self.contract(task(again, PENDING_BOTH))


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
            ACCEPT_ONE,
            items=items,
        )
        module._v6_evidence_contract(SPEC, PLAN, (passed,), self.registry)
        not_run = task(
            "| One | 1 | W1 | Unit | fixture | NOT_RUN | test | - |\n",
            PENDING_BOTH,
            items=items,
        )
        with self.assertRaisesRegex(module.SpecPackageError, "PASS evidence"):
            module._v6_evidence_contract(SPEC, PLAN, (not_run,), self.registry)

    def test_a_completed_item_needs_its_criteria_accepted(self) -> None:
        items = (
            ("A", "W1", "First", "@owner", "completed", "-"),
            ("B", "W2", "Second", "@owner", "in-progress", "-"),
        )
        module._v6_evidence_contract(
            SPEC, PLAN, (task(PASS_BOTH, ACCEPT_ONE, items=items),), self.registry
        )
        with self.assertRaisesRegex(module.SpecPackageError, "criteria accepted"):
            module._v6_evidence_contract(
                SPEC, PLAN, (task(PASS_BOTH, PENDING_BOTH, items=items),), self.registry
            )

    def test_single_mode_and_items_judge_equivalent_work_alike(self) -> None:
        """A finished first share of the work is judged the same either way."""

        items = (
            ("A", "W1", "First", "@owner", "completed", "-"),
            ("B", "W2", "Second", "@owner", "in-progress", "-"),
        )
        two_only = "| Two | 2 | W2 | Unit | fixture | PASS | test | - |\n"
        for evidence, decisions, expected in (
            (PASS_BOTH, ACCEPT_ONE, True),
            (PASS_BOTH, PENDING_BOTH, False),
            (two_only, PENDING_BOTH, False),
        ):
            rows = evidence.splitlines(keepends=True)
            first_row, second_row = decisions.splitlines(keepends=True)
            first = task(
                "".join(row for row in rows if "| W1 |" in row),
                first_row,
                "completed",
            )
            second = second_task(
                "".join(row for row in rows if "| W2 |" in row), second_row
            )
            contract = module._v6_evidence_contract
            single = outcome(contract, SPEC, SPLIT_PLAN, (first, second), self.registry)
            multi = outcome(
                contract,
                SPEC,
                PLAN,
                (task(evidence, decisions, items=items),),
                self.registry,
            )
            with self.subTest(evidence=evidence, decisions=decisions):
                self.assertEqual(expected, single == "ok", single)
                self.assertEqual(expected, multi == "ok", multi)

    def test_items_must_cover_exactly_the_tasks_work_units(self) -> None:
        items = (
            ("A", "W1", "First", "@owner", "draft", "-"),
            ("B", "W3", "Third", "@owner", "draft", "-"),
        )
        with self.assertRaisesRegex(module.SpecPackageError, "cover exactly"):
            module._v6_evidence_contract(
                SPEC, PLAN, (task(PASS_BOTH, PENDING_BOTH, items=items),), self.registry
            )

    def test_execution_items_need_two_rows(self) -> None:
        body = ITEMS_HEADER + "| A | W1 | First | @owner | draft | - |\n"
        with self.assertRaisesRegex(module.SpecPackageError, "at least 2 rows"):
            module._execution_item_rows(body, self.registry, ROOT / "t.md")

    def test_a_multi_item_task_declares_no_frontmatter_status(self) -> None:
        rows = (
            "| A | W1 | First | @owner | draft | - |\n"
            "| B | W2 | Second | @owner | draft | - |\n"
        )
        envelope = """---
title: "Work"
version: "0.1.0"
type: "sdlc/task"
{status}owner: "@owner"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0001-TSK-0001"
parent_ids:
- "SPEC-0001-PLAN-0001"
created: "2026-10-13"
---

# Work

"""
        for declared, error in (("", None), ('status: "draft"\n', "must not declare")):
            with self.subTest(declared=declared), tempfile.TemporaryDirectory() as root:
                path = pathlib.Path(root, "tsk-0001-work.md")
                path.write_text(envelope.format(status=declared) + ITEMS_HEADER + rows)
                parent = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    result = outcome(
                        module._parse_document,
                        parent,
                        path.name,
                        path,
                        ROOT / "tasks" / path.name,
                        profile_id="task",
                        expected_artifact_id="SPEC-0001-TSK-0001",
                        registry=self.registry,
                        budget=module._LoadBudget(),
                    )
                finally:
                    os.close(parent)
                if error is None:
                    self.assertEqual("ok", result)
                else:
                    self.assertIn(error, result)


class Generation6DepartureTests(unittest.TestCase):
    registry = load_registry()

    def test_only_a_ready_base_enters_the_completed_archive(self) -> None:
        done = task(PASS_BOTH, ACCEPT_BOTH, "completed")
        evidence = module._v6_evidence_contract(SPEC, PLAN, (done,), self.registry)
        archived = module.SpecPackage(
            pathlib.Path(ROOT), "0001", "example", SPEC, PLAN, (done,), ()
        )
        reopened = dataclasses.replace(
            archived, tasks=(dataclasses.replace(done, status="in-progress"),)
        )
        for status, copy, preserved in (
            ("approved", archived, True),
            ("draft", archived, False),
            ("cancelled", archived, False),
            ("approved", reopened, False),
        ):
            source = dataclasses.replace(
                archived,
                spec=dataclasses.replace(SPEC, status=status),
                plan=dataclasses.replace(PLAN, status=status),
                evidence=evidence,
            )
            with self.subTest(status=status, copy=copy is archived):
                self.assertEqual(
                    preserved,
                    SPEC.path
                    in module._ordinary_preserved_paths(
                        pathlib.Path("."), (source,), (), (copy,), self.registry
                    ),
                )


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
