from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import inspect
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text
from scripts.lib.document_governance.registry import DEFAULT_REGISTRY, load_registry

ROOT = pathlib.Path(__file__).resolve().parents[3]


def _current_spec_rows(index_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in index_text.splitlines():
        if line.startswith("| SPEC-"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows[cells[0]] = " | ".join(cells[1:])
    return rows


def _spec_packages_module():
    module_name = "scripts.lib.document_governance.spec_packages"
    if importlib.util.find_spec(module_name) is None:
        raise AssertionError(f"missing production module: {module_name}")
    return importlib.import_module(module_name)


def _document_text(
    profile_id: str,
    artifact_id: str,
    parent_ids: tuple[str, ...],
    *,
    status: str = "in-progress",
) -> str:
    parents = "\n".join(f"  - {parent}" for parent in parent_ids)
    text = f"""---
title: Fixture {profile_id}
version: 1.0.0
type: sdlc/{profile_id}
status: {status}
owner: "@buenhyden"
updated: 2026-08-22
layer: specification
artifact_id: {artifact_id}
parent_ids:
{parents}
created: 2026-08-22
---

# Fixture {profile_id}

## Objective

Fixture objective.

## Inputs

Fixture inputs.

## Work Log

Fixture work log.

## Verification Evidence

Fixture verification evidence.

## Review Evidence

Fixture review evidence.

## Commit Ledger

Fixture commit ledger.
"""
    if profile_id == "spec":
        text += "\n## Acceptance Contract\n\n1. Validate the fixture.\n"
    elif profile_id == "plan":
        text += "\n## Execution Sequence\n\n1. W1: Validate the fixture.\n"
    elif profile_id == "task":
        text = text.replace(
            "Fixture verification evidence.",
            "| Acceptance criterion | Plan work unit | Task result | Durable owner |\n"
            "| --- | --- | --- | --- |\n"
            "| 1 | W1 | PASS | N/A: local validation only |",
        )
    return text


def _write_package(
    stage: pathlib.Path,
    *,
    number: str = "0001",
    slug: str = "example",
    spec_id: str | None = None,
    spec_status: str = "in-progress",
    plan: bool = False,
    plan_status: str = "in-progress",
    task: bool = False,
    task_status: str = "in-progress",
    task_parent_ids: tuple[str, ...] | None = None,
) -> pathlib.Path:
    fixture_registry = stage.parent / "99.templates/registry.json"
    if not fixture_registry.exists():
        fixture_registry.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DEFAULT_REGISTRY, fixture_registry)
    package = stage / f"{number}-{slug}"
    package.mkdir(parents=True)
    package.joinpath("spec.md").write_text(
        _document_text(
            "spec",
            spec_id or f"SPEC-{number}",
            ("REQ-0001",),
            status=spec_status,
        ),
        encoding="utf-8",
    )
    if plan:
        package.joinpath("plan.md").write_text(
            _document_text(
                "plan",
                f"SPEC-{number}-PLAN-0001",
                (f"SPEC-{number}",),
                status=plan_status,
            ),
            encoding="utf-8",
        )
    if task:
        tasks = package / "tasks"
        tasks.mkdir()
        parents = task_parent_ids or (
            (f"SPEC-{number}-PLAN-0001",) if plan else (f"SPEC-{number}",)
        )
        tasks.joinpath("tsk-0001-implement.md").write_text(
            _document_text(
                "task",
                f"SPEC-{number}-TSK-0001",
                parents,
                status=task_status,
            ),
            encoding="utf-8",
        )
        if task_status == "completed":
            task_path = _set_item_rows(
                package,
                (("1", "W1", "completed", "PASS", "N/A: local validation only"),),
            )
            _set_review_rows(task_path, (("1", "accepted", "Fixture review."),))
        else:
            _set_review_rows(
                tasks / "tsk-0001-implement.md",
                (("1", "pending", "Fixture review."),),
            )
    return package


def _set_frontmatter_value(path: pathlib.Path, key: str, value: object) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "created: 2026-08-22\n"
    if marker not in text:
        raise AssertionError(f"missing frontmatter insertion point: {path}")
    path.write_text(
        text.replace(marker, f"{key}: {json.dumps(value)}\n{marker}", 1),
        encoding="utf-8",
    )


def _set_status(path: pathlib.Path, before: str, after: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = f"status: {before}\n"
    if marker not in text:
        raise AssertionError(f"missing status {before}: {path}")
    path.write_text(text.replace(marker, f"status: {after}\n", 1), encoding="utf-8")


def _set_item_rows(
    package: pathlib.Path,
    rows: tuple[tuple[str, str, str, str, str], ...],
    *,
    add_reviews: bool = True,
) -> pathlib.Path:
    spec = package / "spec.md"
    plan = package / "plan.md"
    task = package / "tasks/tsk-0001-implement.md"
    if len(rows) > 1:
        spec.write_text(
            spec.read_text(encoding="utf-8")
            + "\n2. Validate the second fixture item.\n",
            encoding="utf-8",
        )
        plan.write_text(
            plan.read_text(encoding="utf-8")
            + "\n2. W2: Validate the second fixture item.\n",
            encoding="utf-8",
        )
    old = (
        "| Acceptance criterion | Plan work unit | Task result | Durable owner |\n"
        "| --- | --- | --- | --- |\n"
        "| 1 | W1 | PASS | N/A: local validation only |"
    )
    current = (
        "| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 1 | W1 | completed | PASS | N/A: local validation only |"
    )
    rendered = [
        "| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |",
        "| --- | --- | --- | --- | --- |",
        *("| " + " | ".join(row) + " |" for row in rows),
    ]
    text = task.read_text(encoding="utf-8")
    source = old if old in text else current
    if source not in text:
        raise AssertionError("missing Task receipt fixture")
    task.write_text(text.replace(source, "\n".join(rendered), 1), encoding="utf-8")
    if add_reviews:
        reviews = tuple(
            (
                criterion,
                "accepted"
                if status == "completed" and result.startswith("PASS")
                else "pending",
                "Fixture review record.",
            )
            for criterion, _, status, result, _ in rows
        )
        _set_review_rows(task, tuple(dict.fromkeys(reviews)))
    return task


def _set_review_rows(
    task: pathlib.Path,
    rows: tuple[tuple[str, str, str], ...],
) -> None:
    rendered = [
        "| Acceptance criterion | Acceptance | Evidence |",
        "| --- | --- | --- |",
        *("| " + " | ".join(row) + " |" for row in rows),
    ]
    text = task.read_text(encoding="utf-8")
    if "Fixture review evidence." in text:
        text = text.replace("Fixture review evidence.", "\n".join(rendered), 1)
    else:
        text = re.sub(
            r"(?m)^\| Acceptance criterion \| Acceptance \| Evidence \|\n"
            r"^\| --- \| --- \| --- \|\n(?:^\|.*\|\n?)+",
            "\n".join(rendered) + "\n",
            text,
            count=1,
        )
    task.write_text(text, encoding="utf-8")


def _add_lifecycle_events(
    task: pathlib.Path,
    rows: tuple[tuple[str, str, str, str], ...],
) -> None:
    anchors = "\n\n".join(
        f"### {evidence.removeprefix('#').replace('-', ' ').title()}\n\nObserved."
        for *_, evidence in rows
    )
    table = "\n".join(
        (
            "### Lifecycle Events",
            "",
            "| Artifact | From | To | Evidence |",
            "| --- | --- | --- | --- |",
            *("| " + " | ".join(row) + " |" for row in rows),
        )
    )
    text = task.read_text(encoding="utf-8")
    task.write_text(
        text.replace(
            "Fixture work log.", f"Fixture work log.\n\n{anchors}\n\n{table}", 1
        ),
        encoding="utf-8",
    )


def _branch_handoff_fixture(
    root: pathlib.Path,
    *,
    carrier: str = "current",
    completed_record: str = "committed",
    completed_slug: str = "source",
    receipt_updates: dict[str, str] | None = None,
) -> tuple[pathlib.Path, str, dict[str, str]]:
    subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
    stage = root / "docs/03.specs"
    source = _write_package(
        stage,
        number="0001",
        slug="source",
        plan=True,
        task=True,
    )
    contracts = source / "contracts"
    contracts.mkdir()
    contracts.joinpath("openapi.yaml").write_text(
        "openapi: 3.1.0\ninfo: {title: source, version: 1.0.0}\npaths: {}\n",
        encoding="utf-8",
    )
    target = _write_package(
        stage,
        number="0002",
        slug="target",
        plan=True,
        task=True,
    )
    subprocess.run(("git", "add", "-A"), cwd=root, check=True)
    subprocess.run(
        (
            "git",
            "-c",
            "user.name=Spec Fixture",
            "-c",
            "user.email=spec@example.invalid",
            "commit",
            "-qm",
            "baseline",
        ),
        cwd=root,
        check=True,
    )
    commit = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    _write_package(
        root / "docs/98.archive/completed/03.specs",
        number="0001",
        slug=completed_slug,
        spec_status="completed",
    )
    if completed_record == "committed":
        subprocess.run(("git", "add", "-A"), cwd=root, check=True)
        subprocess.run(
            (
                "git",
                "-c",
                "user.name=Spec Fixture",
                "-c",
                "user.email=spec@example.invalid",
                "commit",
                "-qm",
                "preserve completed record",
            ),
            cwd=root,
            check=True,
        )
    elif completed_record != "uncommitted":
        raise AssertionError(f"unsupported completed record: {completed_record}")
    preserved = root / "docs/98.archive/superseded/03.specs/0001-source"
    preserved.parent.mkdir(parents=True)
    shutil.copytree(source, preserved)
    shutil.rmtree(source)
    receipt = {
        "source_commit": commit,
        "source_package_path": "docs/03.specs/0001-source",
        "source_artifact_id": "SPEC-0001",
        "preserved_package_path": ("docs/98.archive/superseded/03.specs/0001-source"),
        "target_package_path": "docs/03.specs/0002-target",
        "target_artifact_id": "SPEC-0002",
        "disposition": "historical-superseded",
    }
    receipt.update(receipt_updates or {})
    if carrier == "current":
        task = target / "tasks/tsk-0001-implement.md"
    elif carrier == "completed":
        archived_target = root / "docs/98.archive/completed/03.specs/0002-target"
        archived_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, archived_target)
        _set_status(archived_target / "spec.md", "in-progress", "completed")
        _set_status(archived_target / "plan.md", "in-progress", "completed")
        task = archived_target / "tasks/tsk-0001-implement.md"
        _set_status(task, "in-progress", "completed")
        task.write_text(
            task.read_text(encoding="utf-8").replace(
                "| 1 | W1 | PASS | N/A: local validation only |",
                "| 1 | W1 | PASS: focused check | N/A: local validation only |",
                1,
            ),
            encoding="utf-8",
        )
        _set_review_rows(task, (("1", "accepted", "Fixture review."),))
        shutil.rmtree(target)
    elif carrier == "missing":
        return stage, commit, receipt
    else:
        raise AssertionError(f"unsupported carrier: {carrier}")
    _set_frontmatter_value(task, "branch_integration_receipts", [receipt])
    return stage, commit, receipt


class SpecPackageTests(unittest.TestCase):
    def test_v4_four_column_completion_requires_registered_result_and_review(self) -> None:
        spec_packages = _spec_packages_module()
        for result, acceptance, valid in (
            ("PASS", "accepted", True),
            ("BLOCKED", "accepted", False),
            ("PASS", "not-required", False),
        ):
            with (
                self.subTest(result=result, acceptance=acceptance),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    spec_status="completed",
                    plan_status="completed",
                    task_status="completed",
                )
                task = package / "tasks/tsk-0001-implement.md"
                text = task.read_text(encoding="utf-8")
                current = (
                    "| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| 1 | W1 | completed | PASS | N/A: local validation only |"
                )
                legacy = (
                    "| Acceptance criterion | Plan work unit | Task result | Durable owner |\n"
                    "| --- | --- | --- | --- |\n"
                    f"| 1 | W1 | {result} | N/A: local validation only |"
                )
                if current not in text:
                    raise AssertionError("missing current receipt fixture")
                text = text.replace(current, legacy, 1)
                task.write_text(text, encoding="utf-8")
                _set_review_rows(task, (("1", acceptance, "Fixture review."),))
                if valid:
                    self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))
                else:
                    with self.assertRaises(spec_packages.SpecPackageError):
                        spec_packages.load_spec_packages(stage)

    def test_v4_task_results_and_review_evidence_are_closed_contracts(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            ("invalid-result", "BLOCKED", (("1", "pending", "Pending."),), "result"),
            (
                "result-suffix",
                "PASS: arbitrary detail",
                (("1", "pending", "Pending."),),
                "result",
            ),
            ("missing-review", "NOT_RUN", (), "review evidence"),
            (
                "invalid-acceptance",
                "NOT_RUN",
                (("1", "approved", "Not a registered value."),),
                "acceptance",
            ),
            (
                "wrong-criterion",
                "NOT_RUN",
                (("2", "pending", "Wrong criterion."),),
                "criteria",
            ),
        )
        for label, result, reviews, message in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    spec_status="in-progress",
                    plan_status="in-progress",
                    task_parent_ids=("SPEC-0001-PLAN-0001",),
                )
                task = _set_item_rows(
                    package,
                    (("1", "W1", "in-progress", result, "Task owner"),),
                    add_reviews=bool(reviews),
                )
                if reviews:
                    _set_review_rows(task, reviews)
                else:
                    _set_review_rows(task, ())
                with self.assertRaisesRegex(spec_packages.SpecPackageError, message):
                    spec_packages.load_spec_packages(stage)

    def test_v4_completed_task_requires_pass_and_accepted_review(self) -> None:
        spec_packages = _spec_packages_module()
        for acceptance, accepted in (
            ("pending", False),
            ("not-required", False),
            ("accepted", True),
        ):
            with (
                self.subTest(acceptance=acceptance),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    spec_status="in-progress",
                    plan_status="in-progress",
                    task_status="completed",
                    task_parent_ids=("SPEC-0001-PLAN-0001",),
                )
                task = _set_item_rows(
                    package,
                    (("1", "W1", "completed", "PASS", "N/A: fixture"),),
                )
                _set_review_rows(task, (("1", acceptance, "Review record."),))
                if accepted:
                    self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))
                else:
                    with self.assertRaisesRegex(
                        spec_packages.SpecPackageError, "accepted review"
                    ):
                        spec_packages.load_spec_packages(stage)

    def test_v4_parent_status_projection_matches_remaining_tasks(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            ("in-progress", "in-progress", True),
            ("blocked", "blocked", True),
            ("ready", "approved", True),
            ("completed", "in-progress", True),
            ("blocked", "in-progress", False),
        )
        for task_status, parent_status, valid in cases:
            with (
                self.subTest(states=(task_status, parent_status)),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(
                    stage,
                    plan=True,
                    task=True,
                    spec_status=parent_status,
                    plan_status=parent_status,
                    task_status=task_status,
                    task_parent_ids=("SPEC-0001-PLAN-0001",),
                )
                if valid:
                    self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))
                else:
                    with self.assertRaisesRegex(
                        spec_packages.SpecPackageError, "status projection"
                    ):
                        spec_packages.load_spec_packages(stage)

        spec = spec_packages.SpecDocument(
            pathlib.PurePosixPath("docs/03.specs/0001-fixture/spec.md"),
            "spec",
            "SPEC-0001",
            "approved",
            (),
        )
        plan = spec_packages.SpecDocument(
            pathlib.PurePosixPath("docs/03.specs/0001-fixture/plan.md"),
            "plan",
            "SPEC-0001-PLAN-0001",
            "approved",
            ("SPEC-0001",),
        )
        mixed = (
            spec_packages.SpecDocument(
                pathlib.PurePosixPath(
                    "docs/03.specs/0001-fixture/tasks/tsk-0001-ready.md"
                ),
                "task",
                "SPEC-0001-TSK-0001",
                "ready",
                ("SPEC-0001-PLAN-0001",),
            ),
            spec_packages.SpecDocument(
                pathlib.PurePosixPath(
                    "docs/03.specs/0001-fixture/tasks/tsk-0002-blocked.md"
                ),
                "task",
                "SPEC-0001-TSK-0002",
                "blocked",
                ("SPEC-0001-PLAN-0001",),
            ),
        )
        spec_packages._validate_execution_states(spec, plan, mixed)
        for retained in ("in-progress", "blocked"):
            spec_packages._validate_execution_states(
                dataclasses.replace(spec, status=retained),
                dataclasses.replace(plan, status=retained),
                mixed,
            )
        spec_packages._validate_execution_states(spec, plan, ())
        spec_packages._validate_execution_states(
            dataclasses.replace(spec, status="blocked"),
            dataclasses.replace(plan, status="blocked"),
            (),
        )

    def test_v4_preexecution_and_terminal_package_occupancy(self) -> None:
        spec_packages = _spec_packages_module()
        spec = spec_packages.SpecDocument(
            pathlib.PurePosixPath("docs/03.specs/0001-fixture/spec.md"),
            "spec",
            "SPEC-0001",
            "draft",
            (),
        )
        plan = spec_packages.SpecDocument(
            pathlib.PurePosixPath("docs/03.specs/0001-fixture/plan.md"),
            "plan",
            "SPEC-0001-PLAN-0001",
            "draft",
            ("SPEC-0001",),
        )
        task = spec_packages.SpecDocument(
            pathlib.PurePosixPath(
                "docs/03.specs/0001-fixture/tasks/tsk-0001-fixture.md"
            ),
            "task",
            "SPEC-0001-TSK-0001",
            "draft",
            ("SPEC-0001-PLAN-0001",),
        )
        spec_packages._validate_execution_states(spec, plan, ())
        spec_packages._validate_execution_states(spec, plan, (task,))
        spec_packages._validate_execution_states(
            dataclasses.replace(spec, status="in-review"),
            dataclasses.replace(plan, status="in-review"),
            (task,),
        )
        for terminal in ("cancelled", "superseded"):
            spec_packages._validate_execution_states(
                dataclasses.replace(spec, status=terminal),
                dataclasses.replace(plan, status=terminal),
                (dataclasses.replace(task, status="cancelled"),),
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError, "active Plan or Task"
            ):
                spec_packages._validate_execution_states(
                    dataclasses.replace(spec, status=terminal), plan, (task,)
                )

    def test_v4_rejects_previous_status_aliases_and_dual_task_parents(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            ("active-spec", "active", ("SPEC-0001-PLAN-0001",), "lifecycle"),
            (
                "dual-task-parent",
                "in-progress",
                ("SPEC-0001", "SPEC-0001-PLAN-0001"),
                "owning Plan",
            ),
        )
        for label, spec_status, parents, message in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(
                    stage,
                    plan=True,
                    task=True,
                    spec_status=spec_status,
                    plan_status="in-progress",
                    task_parent_ids=parents,
                )
                with self.assertRaisesRegex(spec_packages.SpecPackageError, message):
                    spec_packages.load_spec_packages(stage)

    ACTIVE_ROUTE_FILES = (
        ROOT / ".agents/governance/documentation-protocol.md",
        ROOT / ".agents/governance/quality-standards.md",
        ROOT / ".agents/skills/execution-plan-agent/SKILL.md",
        ROOT / ".claude/skills/execution-plan-agent/SKILL.md",
        ROOT / "README.md",
        ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml",
        ROOT / "scripts/validation/run-agent-precommit-all-files.sh",
    )

    def test_multi_item_task_status_is_derived_from_registered_rows(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            (
                "blocked",
                (
                    ("1", "W1", "completed", "PASS", "N/A: local"),
                    ("2", "W2", "blocked", "DEFER", "Task owner"),
                ),
            ),
            (
                "in-progress",
                (
                    ("1", "W1", "completed", "PASS", "N/A: local"),
                    ("2", "W2", "ready", "NOT_RUN", "Task owner"),
                ),
            ),
        )
        for expected, rows in cases:
            with (
                self.subTest(expected=expected),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    task_status=expected,
                    spec_status="blocked" if expected == "blocked" else "in-progress",
                    plan_status="blocked" if expected == "blocked" else "in-progress",
                )
                _set_item_rows(package, rows)
                self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                plan=True,
                task=True,
                task_status="in-progress",
            )
            _set_item_rows(
                package,
                (("1", "W1", "blocked", "DEFER", "Task owner"),),
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError,
                "item status summary",
            ):
                spec_packages.load_spec_packages(stage)

    def test_multi_item_rows_reject_invalid_status_result_and_cancellation(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            (
                "invalid-status",
                "in-progress",
                (("1", "W1", "queued", "NOT_RUN: queued", "Task owner"),),
                "outside the Task lifecycle",
            ),
            (
                "missing-cancellation",
                "in-progress",
                (
                    ("1", "W1", "cancelled", "NOT_APPLICABLE: withdrawn", "Owner"),
                    ("2", "W2", "in-progress", "NOT_RUN: active", "Owner"),
                ),
                "cancellation",
            ),
        )
        for label, task_status, rows, message in cases:
            with (
                self.subTest(case=label),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    task_status=task_status,
                )
                _set_item_rows(package, rows)
                with self.assertRaisesRegex(spec_packages.SpecPackageError, message):
                    spec_packages.load_spec_packages(stage)

    def test_current_multi_row_receipt_requires_item_statuses(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            root.joinpath("baseline.txt").write_text("baseline\n", encoding="utf-8")
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
                cwd=root,
                check=True,
            )
            stage = root / "docs/03.specs"
            package = _write_package(
                stage,
                plan=True,
                task=True,
                task_status="completed",
            )
            spec = package / "spec.md"
            spec.write_text(
                spec.read_text(encoding="utf-8")
                + "\n2. Validate the blocked fixture item.\n",
                encoding="utf-8",
            )
            plan = package / "plan.md"
            plan.write_text(
                plan.read_text(encoding="utf-8")
                + "\n2. W2: Validate the blocked fixture item.\n",
                encoding="utf-8",
            )
            task = package / "tasks/tsk-0001-implement.md"
            item_table = (
                "| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| 1 | W1 | completed | PASS | N/A: local validation only |"
            )
            legacy_table = (
                "| Acceptance criterion | Plan work unit | Task result | Durable owner |\n"
                "| --- | --- | --- | --- |\n"
                "| 1 | W1 | PASS | N/A: local validation only |\n"
                "| 2 | W2 | PASS | N/A: historical completion |"
            )
            task.write_text(
                task.read_text(encoding="utf-8").replace(item_table, legacy_table, 1),
                encoding="utf-8",
            )
            _set_review_rows(
                task,
                (
                    ("1", "accepted", "Fixture review."),
                    ("2", "accepted", "Fixture review."),
                ),
            )
            current = spec_packages.load_spec_packages(stage)
            result = spec_packages._validate_legacy_multirow_receipts(
                (),
                current,
                load_registry(),
            )
            self.assertIn(
                "task-completion-items-invalid",
                {finding.code for finding in result},
            )

    def test_nonterminal_multi_row_receipt_requires_item_statuses_at_load(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True, task=True)
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| 1 | W1 | PASS | N/A: local validation only |",
                    "| 1 | W1 | PASS | N/A: local validation only |\n"
                    "| 2 | W2 | BLOCKED: runtime | Task owner |",
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError,
                "multi-row completion evidence requires item statuses",
            ):
                spec_packages.load_spec_packages(stage)

    def test_unchanged_terminal_multi_row_receipt_is_grandfathered(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            stage = root / "docs/03.specs"
            package = _write_package(
                stage,
                plan=True,
                task=True,
                task_status="completed",
            )
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| 1 | W1 | PASS | N/A: local validation only |",
                    "| 1 | W1 | PASS | N/A: local validation only |\n"
                    "| 2 | W2 | PARTIAL: historical | Task owner |",
                    1,
                ),
                encoding="utf-8",
            )
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
                cwd=root,
                check=True,
            )
            result = spec_packages.validate_repository_spec_package_lifecycle_details(
                root,
                spec_packages.load_spec_packages(stage),
                base_ref="HEAD",
            )
            self.assertNotIn(
                "task-completion-items-invalid",
                {finding.code for finding in result.findings},
            )

    def test_item_pairs_cannot_duplicate_legacy_receipt_pairs(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                plan=True,
                task=True,
                task_status="blocked",
                spec_status="blocked",
                plan_status="blocked",
            )
            _set_item_rows(
                package,
                (("1", "W1", "blocked", "DEFER", "Task owner"),),
            )
            second = package / "tasks/tsk-0002-legacy.md"
            second.write_text(
                _document_text(
                    "task",
                    "SPEC-0001-TSK-0002",
                    ("SPEC-0001-PLAN-0001",),
                    status="completed",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError,
                "duplicates a criterion/work pair",
            ):
                spec_packages.load_spec_packages(stage)
        for result in (
            "FAIL: focused",
            "BLOCKED: runtime",
            "NOT_RUN: pending",
            "SKIP: waived",
        ):
            with (
                self.subTest(result=result),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    plan=True,
                    task=True,
                    task_status="completed",
                )
                task = _set_item_rows(
                    package,
                    (("1", "W1", "completed", result, "N/A: local"),),
                )
                _set_review_rows(task, (("1", "accepted", "Fixture review."),))
                with self.assertRaisesRegex(
                    spec_packages.SpecPackageError,
                    "registered result values|completed item needs PASS",
                ):
                    spec_packages.load_spec_packages(stage)

    def test_completed_spec_counts_only_completed_pass_item_rows(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            _set_item_rows(
                package,
                (("1", "W1", "completed", "PASS", "N/A: local"),),
            )
            self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="cancelled",
            )
            task = _set_item_rows(
                package,
                (("1", "W1", "cancelled", "NOT_APPLICABLE", "Owner"),),
            )
            _set_frontmatter_value(
                task,
                "cancellation",
                {
                    "reason": "withdrawn",
                    "approved_by": "@owner",
                    "approved_at": "2026-10-04",
                    "criteria": [{"criterion": 1, "withdrawn": "obsolete"}],
                },
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError,
                "must cover every acceptance criterion",
            ):
                spec_packages.load_spec_packages(stage)

    def test_old_registry_and_preserved_load_do_not_require_new_tables(self) -> None:
        spec_packages = _spec_packages_module()
        registry = load_registry()
        common = dict(registry.common)
        completion = dict(common["spec_completion_evidence"])
        completion.pop("item_table_headers", None)
        common["spec_completion_evidence"] = completion
        common.pop("task_lifecycle_events", None)
        legacy = dataclasses.replace(registry, common=common)
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True, task=True)
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| Acceptance criterion | Plan work unit | Task result | Durable owner |",
                    "| Acceptance criterion | Plan work unit | Status | Broken |",
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                1,
                len(
                    spec_packages.load_spec_packages(
                        stage,
                        registry=legacy,
                        _completion_evidence=False,
                    )
                ),
            )

    def test_package_lifecycle_events_validate_the_actual_transition_chain(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            root.joinpath("baseline.txt").write_text("baseline\n", encoding="utf-8")
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
                cwd=root,
                check=True,
            )
            stage = root / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="in-progress",
                plan=True,
                plan_status="in-progress",
                task=True,
                task_status="in-progress",
            )
            task = package / "tasks/tsk-0001-implement.md"
            _add_lifecycle_events(
                task,
                (
                    ("SPEC-0001", "draft", "in-review", "#spec-review"),
                    ("SPEC-0001", "in-review", "approved", "#spec-approved"),
                    ("SPEC-0001", "approved", "in-progress", "#spec-active"),
                    ("SPEC-0001-PLAN-0001", "draft", "in-review", "#plan-review"),
                    ("SPEC-0001-PLAN-0001", "in-review", "approved", "#plan-approved"),
                    ("SPEC-0001-PLAN-0001", "approved", "in-progress", "#plan-active"),
                    ("SPEC-0001-TSK-0001", "draft", "ready", "#task-ready"),
                    (
                        "SPEC-0001-TSK-0001",
                        "ready",
                        "in-progress",
                        "#task-started",
                    ),
                    (
                        "SPEC-0001-TSK-0001",
                        "in-progress",
                        "blocked",
                        "#task-blocked-first",
                    ),
                    (
                        "SPEC-0001-TSK-0001",
                        "blocked",
                        "in-progress",
                        "#task-resumed-first",
                    ),
                    (
                        "SPEC-0001-TSK-0001",
                        "in-progress",
                        "blocked",
                        "#task-blocked-second",
                    ),
                    (
                        "SPEC-0001-TSK-0001",
                        "blocked",
                        "in-progress",
                        "#task-resumed-second",
                    ),
                ),
            )
            current = spec_packages.load_spec_packages(stage)
            result = spec_packages.validate_repository_spec_package_lifecycle_details(
                root,
                current,
                base_ref="HEAD",
            )
            self.assertEqual((), result.findings)
            self.assertEqual(
                frozenset(
                    {
                        ("docs/03.specs/0001-example/spec.md", "draft", "in-progress"),
                        (
                            "docs/03.specs/0001-example/plan.md",
                            "draft",
                            "in-progress",
                        ),
                        (
                            "docs/03.specs/0001-example/tasks/tsk-0001-implement.md",
                            "draft",
                            "in-progress",
                        ),
                    }
                ),
                result.actual_transitions,
            )

    def test_package_lifecycle_events_reject_unbound_or_broken_chains(self) -> None:
        spec_packages = _spec_packages_module()
        valid = (
            ("SPEC-0001", "draft", "in-review", "#spec-review"),
            ("SPEC-0001", "in-review", "approved", "#spec-approved"),
            ("SPEC-0001", "approved", "in-progress", "#spec-active"),
            ("SPEC-0001-PLAN-0001", "draft", "in-review", "#plan-review"),
            ("SPEC-0001-PLAN-0001", "in-review", "approved", "#plan-approved"),
            ("SPEC-0001-PLAN-0001", "approved", "in-progress", "#plan-active"),
            ("SPEC-0001-TSK-0001", "draft", "ready", "#task-ready"),
            (
                "SPEC-0001-TSK-0001",
                "ready",
                "in-progress",
                "#task-started",
            ),
        )
        cases = {
            "missing-step": (*valid[:1], *valid[2:]),
            "wrong-base": (
                ("SPEC-0001", "in-review", "approved", "#spec-approved"),
                *valid[2:],
            ),
            "wrong-end": (
                *valid[:-1],
                ("SPEC-0001-TSK-0001", "ready", "blocked", "#task-started"),
            ),
            "cross-package": (
                ("SPEC-9999", "draft", "review", "#spec-review"),
                *valid[1:],
            ),
            "missing-anchor": (
                *valid[:-1],
                ("SPEC-0001-TSK-0001", "ready", "in-progress", "#missing"),
            ),
            "outside-anchor": (
                *valid[:-1],
                (
                    "SPEC-0001-TSK-0001",
                    "ready",
                    "in-progress",
                    "other.md#task-started",
                ),
            ),
            "duplicate": (*valid, valid[-1]),
        }
        for label, rows in cases.items():
            with (
                self.subTest(case=label),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
                root.joinpath("baseline.txt").write_text("baseline\n", encoding="utf-8")
                subprocess.run(("git", "add", "-A"), cwd=root, check=True)
                subprocess.run(
                    (
                        "git",
                        "-c",
                        "user.name=Spec Fixture",
                        "-c",
                        "user.email=spec@example.invalid",
                        "commit",
                        "-qm",
                        "baseline",
                    ),
                    cwd=root,
                    check=True,
                )
                stage = root / "docs/03.specs"
                package = _write_package(
                    stage,
                    spec_status="in-progress",
                    plan=True,
                    plan_status="in-progress",
                    task=True,
                    task_status="in-progress",
                )
                task = package / "tasks/tsk-0001-implement.md"
                _add_lifecycle_events(task, rows)
                if label == "missing-anchor":
                    task.write_text(
                        task.read_text(encoding="utf-8").replace(
                            "### Missing\n\nObserved.\n\n",
                            "",
                            1,
                        ),
                        encoding="utf-8",
                    )
                result = (
                    spec_packages.validate_repository_spec_package_lifecycle_details(
                        root,
                        spec_packages.load_spec_packages(stage),
                        base_ref="HEAD",
                    )
                )
                self.assertIn(
                    "task-lifecycle-events-invalid",
                    {finding.code for finding in result.findings},
                )
                self.assertEqual(frozenset(), result.actual_transitions)

    def test_lifecycle_event_table_errors_use_registered_evidence_context(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            root.joinpath("baseline.txt").write_text("baseline\n", encoding="utf-8")
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
                cwd=root,
                check=True,
            )
            stage = root / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="in-progress",
                plan=True,
                plan_status="in-progress",
                task=True,
                task_status="in-progress",
            )
            task = package / "tasks/tsk-0001-implement.md"
            _add_lifecycle_events(
                task,
                (("SPEC-0001", "draft", "in-review", "#spec-review"),),
            )
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| Artifact | From | To | Evidence |",
                    "| Artifact | Before | To | Evidence |",
                    1,
                ),
                encoding="utf-8",
            )

            result = spec_packages.validate_repository_spec_package_lifecycle_details(
                root,
                spec_packages.load_spec_packages(stage),
                base_ref="HEAD",
            )

            self.assertIn(
                "registered evidence table has malformed headers",
                {finding.message for finding in result.findings},
            )

    def test_completed_coverage_accepts_pass_and_ignores_examples(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for result in ("PASS",):
            with (
                self.subTest(result=result),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    spec_status="completed",
                    plan=True,
                    plan_status="completed",
                    task=True,
                    task_status="completed",
                )
                task = package / "tasks/tsk-0001-implement.md"
                task.write_text(
                    task.read_text()
                    .replace("PASS", result)
                    .replace(
                        "N/A: local validation only",
                        "[Current policy](../../../../.agents/governance/bootstrap.md)",
                    )
                )
                spec = package / "spec.md"
                spec.write_text(
                    spec.read_text()
                    + "\n```markdown\n## Acceptance Contract\n2. Example only.\n```\n> 3. Historical example.\n"
                )
                loaded = spec_packages.load_spec_packages(stage)
                self.assertIn("1. Validate the fixture.", loaded[0].spec.body)

    def test_completion_comments_and_fences_do_not_hide_visible_evidence(self) -> None:
        spec_packages = _spec_packages_module()
        for example in (
            "```markdown\n<!--\n```\n",
            "~~~~markdown\n<!--\n~~~~\n",
            "<!--\n```markdown\n-->\n",
        ):
            with (
                self.subTest(example=example),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    spec_status="completed",
                    plan=True,
                    plan_status="completed",
                    task=True,
                    task_status="completed",
                )
                for relative in ("spec.md", "plan.md", "tasks/tsk-0001-implement.md"):
                    path = package / relative
                    path.write_text(
                        path.read_text().replace(
                            "\n# Fixture", "\n" + example + "\n# Fixture", 1
                        )
                    )
                self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))

    def test_disposition_members_follow_profile_registry_not_terminal_union(self):
        module = _spec_packages_module()
        registry = load_registry()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            _write_package(stage, plan=True, task=True, task_status="completed")
            previous = module.load_spec_packages(stage, registry=registry)
            current = (dataclasses.replace(previous[0], tasks=()),)
            contract = dict(registry.common["archive_retention"])
            states = {**contract.get("disposition_entry_statuses", {}), "task": ()}
            narrowed = dataclasses.replace(
                registry,
                common={
                    **registry.common,
                    "archive_retention": {
                        **contract,
                        "disposition_entry_statuses": states,
                    },
                },
            )
            self.assertEqual(
                (),
                module.validate_spec_package_lifecycle(
                    previous, current, registry=registry
                ),
            )
            self.assertEqual(
                "execution-evidence-deletion-forbidden",
                module.validate_spec_package_lifecycle(
                    previous, current, registry=narrowed
                )[0].code,
            )

    def test_task_cancellation_contract(self) -> None:
        module = _spec_packages_module()
        task_id = "SPEC-0001-TSK-0001"
        target = "SPEC-0001-TSK-0002"
        statuses = {task_id: "cancelled", target: "completed"}
        valid = {
            "reason": "Scope merged",
            "approved_by": "@owner",
            "approved_at": "2026-09-28",
            "criteria": [],
        }
        invalid = [
            None,
            "",
            " ",
            {},
            *[
                {**valid, key: value}
                for key, values in {
                    "reason": (None, "", " "),
                    "approved_by": (None, "", " "),
                    "approved_at": (None, "2026-02-30", "20260928", "2026-9-28"),
                    "criteria": (
                        None,
                        "1",
                        {},
                        [{"criterion": True, "withdrawn": "x"}],
                        [{"criterion": 2, "withdrawn": "x"}],
                        [{"criterion": 1}],
                        [{"criterion": 1, "withdrawn": "x", "reassigned_to": target}],
                        [{"criterion": 1, "withdrawn": " "}],
                        [{"criterion": 1, "reassigned_to": "SPEC-0002-TSK-0001"}],
                        [{"criterion": 1, "reassigned_to": task_id}],
                        [{"criterion": 1, "reassigned_to": []}],
                        [
                            {"criterion": 1, "withdrawn": "x"},
                            {"criterion": 1, "reassigned_to": target},
                        ],
                    ),
                }.items()
                for value in values
            ],
        ]
        for cancellation in invalid:
            with self.subTest(cancellation=cancellation):
                self.assertTrue(
                    module.task_cancellation_findings(
                        task_id, cancellation, frozenset({1}), statuses
                    )
                )
        for criteria in (
            [],
            [{"criterion": 1, "withdrawn": "Approved withdrawal"}],
            [{"criterion": 1, "reassigned_to": target}],
        ):
            self.assertEqual(
                (),
                module.task_cancellation_findings(
                    task_id, {**valid, "criteria": criteria}, frozenset({1}), statuses
                ),
            )
        self.assertTrue(
            module.task_cancellation_findings(
                task_id,
                {**valid, "criteria": [{"criterion": 1, "reassigned_to": target}]},
                frozenset({1}),
                {**statuses, target: "cancelled"},
            )
        )

    def test_cancelled_task_requires_cancellation_during_package_load(self) -> None:
        module = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage, plan=True, task=True, task_status="cancelled"
            )
            with self.assertRaisesRegex(module.SpecPackageError, "cancellation"):
                module.load_spec_packages(stage)
            _set_frontmatter_value(
                package / "tasks/tsk-0001-implement.md",
                "cancellation",
                {
                    "reason": "Withdrawn",
                    "approved_by": "@owner",
                    "approved_at": "2026-09-28",
                    "criteria": [{"criterion": 1, "withdrawn": "obsolete"}],
                },
            )
            self.assertEqual(1, len(module.load_spec_packages(stage)))

    def test_acceptance_criterion_numbers_ignores_examples(self) -> None:
        module = _spec_packages_module()
        self.assertEqual(
            (1, 3),
            module.acceptance_criterion_numbers(
                "## Acceptance Contract\n1. First.\n```\n2. Example.\n```\n"
                "<!-- 2. Hidden. -->\n3. Third.\n## Other\n4. Outside.\n",
                "Acceptance Contract",
            ),
        )

    def test_withdrawn_criterion_does_not_exempt_completion(self) -> None:
        module = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            spec = package / "spec.md"
            spec.write_text(spec.read_text() + "2. Still requires PASS.\n")
            task = package / "tasks/tsk-0002-cancelled.md"
            task.write_text(
                re.sub(
                    r"(?m)^\|.*\n?",
                    "",
                    _document_text(
                        "task",
                        "SPEC-0001-TSK-0002",
                        ("SPEC-0001-PLAN-0001",),
                        status="cancelled",
                    ),
                )
            )
            _set_frontmatter_value(
                task,
                "cancellation",
                {
                    "reason": "Withdrawn",
                    "approved_by": "@owner",
                    "approved_at": "2026-09-28",
                    "criteria": [{"criterion": 2, "withdrawn": "No longer requested"}],
                },
            )
            with self.assertRaisesRegex(module.SpecPackageError, "cover every"):
                module.load_spec_packages(stage)

    def test_completed_package_allows_cancelled_task_without_receipt(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(
                stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            cancelled = _document_text(
                "task",
                "SPEC-0001-TSK-0002",
                ("SPEC-0001-PLAN-0001",),
                status="cancelled",
            )
            (package / "tasks/tsk-0002-cancelled.md").write_text(
                re.sub(r"(?m)^\|.*\n?", "", cancelled)
            )
            _set_frontmatter_value(
                package / "tasks/tsk-0002-cancelled.md",
                "cancellation",
                {
                    "reason": "No assigned criteria",
                    "approved_by": "@owner",
                    "approved_at": "2026-09-28",
                    "criteria": [],
                },
            )
            self.assertEqual(2, len(spec_packages.load_spec_packages(stage)[0].tasks))

    def test_completed_package_requires_structural_acceptance_evidence(self) -> None:
        spec_packages = _spec_packages_module()
        rows = "| 1 | W1 | completed | PASS | N/A: local validation only |"
        cases = {
            "missing-criterion": ("spec.md", "2. Another criterion.\n"),
            "uncovered-work": ("plan.md", "2. W2: Additional planned work.\n"),
            "skipped-criterion": (
                "row",
                rows.replace("PASS", "SKIP: runtime unavailable"),
            ),
            "draft-unreceipted-task": ("extra-task", "draft"),
            "commented-task": ("comment", "tasks/tsk-0001-implement.md"),
            "commented-spec": ("comment", "spec.md"),
            "commented-plan": ("comment", "plan.md"),
            "unknown-work": ("row", rows.replace("W1", "W9")),
            "unknown-criterion": ("row", rows.replace("| 1 |", "| 9 |")),
            "empty-result": ("row", rows.replace("PASS", "")),
            "empty-owner": ("row", rows.replace("N/A: local validation only", "")),
            "bare-na": ("row", rows.replace("N/A: local validation only", "N/A")),
            "unlinked-owner": (
                "row",
                rows.replace("N/A: local validation only", "some owner"),
            ),
            "fenced-receipt": ("row", "```markdown\n" + rows + "\n```"),
            "quoted-receipt": ("row", "> " + rows),
            "duplicate-receipt": ("row", rows + "\n" + rows),
            "draft-task": ("status", "task"),
            "draft-plan": ("status", "plan"),
        }
        for label, (surface, value) in cases.items():
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(
                    stage,
                    spec_status="completed",
                    plan=True,
                    plan_status="completed",
                    task=True,
                    task_status="completed",
                )
                task = package / "tasks/tsk-0001-implement.md"
                if surface == "row":
                    task.write_text(task.read_text().replace(rows, value))
                elif surface == "extra-task":
                    (package / "tasks/tsk-0002-follow-up.md").write_text(
                        re.sub(
                            r"(?m)^\|.*\n?",
                            "",
                            _document_text(
                                "task",
                                "SPEC-0001-TSK-0002",
                                ("SPEC-0001-PLAN-0001",),
                                status=value,
                            ),
                        )
                    )
                elif surface == "comment":
                    path = package / value
                    body = path.read_text()
                    prefix, _, content = body.partition("\n# Fixture")
                    path.write_text(prefix + "\n<!--\n# Fixture" + content + "\n-->\n")
                elif surface == "status":
                    path = task if value == "task" else package / "plan.md"
                    path.write_text(
                        path.read_text().replace("status: completed", "status: draft")
                    )
                else:
                    path = package / surface
                    path.write_text(path.read_text() + value)
                with self.assertRaisesRegex(
                    spec_packages.SpecPackageError,
                    "completion|item evidence|Task result|status projection|completed item",
                ):
                    spec_packages.load_spec_packages(stage)

    def test_spec_package_roles_are_frozen_and_exact(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package_path = _write_package(stage, plan=True, task=True)
            contracts = package_path / "contracts"
            contracts.mkdir()
            contracts.joinpath("openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo: {title: fixture, version: 1.0.0}\npaths: {}\n",
                encoding="utf-8",
            )
            packages = spec_packages.load_spec_packages(stage)

        self.assertEqual(1, len(packages))
        package = packages[0]
        self.assertEqual("SPEC-0001", package.spec.artifact_id)
        self.assertEqual("SPEC-0001-PLAN-0001", package.plan.artifact_id)
        self.assertEqual("SPEC-0001-TSK-0001", package.tasks[0].artifact_id)
        self.assertEqual(
            ("openapi.yaml",), tuple(path.name for path in package.contracts)
        )
        self.assertTrue(dataclasses.is_dataclass(package))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            package.number = "9999"

    def test_loader_rejects_symlink_non_regular_oversized_non_utf8_and_race(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for mutation in ("symlink", "non-regular", "oversized", "non-utf8"):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(stage)
                target = package / "spec.md"
                if mutation == "symlink":
                    source = stage.parent / "source.md"
                    source.write_text(
                        target.read_text(encoding="utf-8"), encoding="utf-8"
                    )
                    target.unlink()
                    target.symlink_to(source)
                elif mutation == "non-regular":
                    target.unlink()
                    target.mkdir()
                elif mutation == "oversized":
                    target.write_bytes(b"x" * (spec_packages.MAX_SPEC_FILE_BYTES + 1))
                else:
                    target.write_bytes(b"\xff\xfe")
                with self.assertRaises(spec_packages.SpecPackageError):
                    spec_packages.load_spec_packages(stage)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage)
            target = package / "spec.md"
            registry = spec_packages.load_registry()
            opened = target.stat()
            changed_values = list(opened)
            changed_values[6] += 1
            changed = type(opened)(changed_values)
            with (
                mock.patch.object(
                    spec_packages.os,
                    "fstat",
                    side_effect=(opened, changed),
                ),
                self.assertRaisesRegex(spec_packages.SpecPackageError, "changed"),
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

    def test_directory_parent_swaps_and_final_file_symlink_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()

        for surface in ("stage", "package", "tasks", "contracts"):
            with (
                self.subTest(surface=surface),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage = root / "docs/03.specs"
                package = _write_package(stage, task=surface == "tasks")
                if surface == "contracts":
                    contracts = package / "contracts"
                    contracts.mkdir()
                    contracts.joinpath("openapi.yaml").write_text(
                        "openapi: 3.1.0\ninfo: {title: fixture, version: 1.0.0}\npaths: {}\n",
                        encoding="utf-8",
                    )
                target = {
                    "stage": stage,
                    "package": package,
                    "tasks": package / "tasks",
                    "contracts": package / "contracts",
                }[surface]
                target_call = {"stage": 1, "package": 2, "tasks": 3, "contracts": 3}[
                    surface
                ]
                original_scandir = spec_packages.os.scandir
                calls = 0

                def swap_on_scan(path):
                    nonlocal calls
                    calls += 1
                    if calls == target_call:
                        backup = target.with_name(target.name + ".original")
                        target.rename(backup)
                        target.symlink_to(backup, target_is_directory=True)
                    return original_scandir(path)

                with (
                    mock.patch.object(
                        spec_packages.os,
                        "scandir",
                        side_effect=swap_on_scan,
                    ),
                    self.assertRaisesRegex(
                        spec_packages.SpecPackageError, "changed|symlink"
                    ),
                ):
                    spec_packages.load_spec_packages(stage)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage)
            spec_path = package / "spec.md"
            original_stat = spec_packages.os.stat
            calls = 0

            def replace_after_open(path, *args, **kwargs):
                nonlocal calls
                result = original_stat(path, *args, **kwargs)
                if path == "spec.md" and kwargs.get("dir_fd") is not None:
                    calls += 1
                    if calls == 2:
                        saved = package / "saved-spec.md"
                        spec_path.rename(saved)
                        spec_path.symlink_to(saved)
                return result

            with (
                mock.patch.object(
                    spec_packages.os,
                    "stat",
                    side_effect=replace_after_open,
                ),
                self.assertRaisesRegex(
                    spec_packages.SpecPackageError, "changed|symlink"
                ),
            ):
                spec_packages.load_spec_packages(stage)

    def test_enumeration_and_aggregate_budgets_fail_before_unbounded_loading(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        registry = spec_packages.load_registry()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True)
            package.joinpath("README.md").write_text("# fixture\n", encoding="utf-8")
            with (
                mock.patch.object(spec_packages, "MAX_PACKAGE_ENTRIES", 2),
                self.assertRaisesRegex(
                    spec_packages.SpecPackageError, "too many entries"
                ),
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            _write_package(stage, number="0001")
            _write_package(stage, number="0002")
            with (
                mock.patch.object(spec_packages, "MAX_TOTAL_ENTRIES", 3),
                self.assertRaisesRegex(
                    spec_packages.SpecPackageError, "aggregate entry"
                ),
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            first = _write_package(stage, number="0001") / "spec.md"
            second = _write_package(stage, number="0002") / "spec.md"
            aggregate_limit = first.stat().st_size + second.stat().st_size - 1
            self.assertGreater(
                aggregate_limit, max(first.stat().st_size, second.stat().st_size)
            )
            with (
                mock.patch.object(
                    spec_packages,
                    "MAX_TOTAL_FILE_BYTES",
                    aggregate_limit,
                ),
                self.assertRaisesRegex(
                    spec_packages.SpecPackageError, "aggregate byte"
                ),
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

    def test_duplicate_and_mismatched_package_identities_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            _write_package(stage, number="0001", slug="one")
            _write_package(stage, number="0001", slug="two")
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "duplicate"):
                spec_packages.load_spec_packages(stage)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            _write_package(stage, number="0002", spec_id="SPEC-0001")
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "SPEC-0002"):
                spec_packages.load_spec_packages(stage)

    def test_forbidden_design_tests_and_singular_task_roles_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()
        for role in ("design.md", "tests.md", "task.md"):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(stage)
                package.joinpath(role).write_text("# forbidden\n", encoding="utf-8")
                with self.assertRaisesRegex(spec_packages.SpecPackageError, role):
                    spec_packages.load_spec_packages(stage)

    def test_invalid_task_naming_and_ownership_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage)
            tasks = package / "tasks"
            tasks.mkdir()
            tasks.joinpath("task-0001.md").write_text(
                _document_text("task", "SPEC-0001-TSK-0001", ("SPEC-0001",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "task.*path"):
                spec_packages.load_spec_packages(stage)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, task=True)
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                _document_text("task", "SPEC-0002-TSK-0001", ("SPEC-0001",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError, "SPEC-0001-TSK-0001"
            ):
                spec_packages.load_spec_packages(stage)

    def test_dangling_plan_and_task_parents_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True)
            package.joinpath("plan.md").write_text(
                _document_text("plan", "SPEC-0001-PLAN-0001", ("SPEC-9999",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "plan.*parent"):
                spec_packages.load_spec_packages(stage)

        for parents in (
            ("SPEC-0001", "SPEC-0001-PLAN-0001"),
            ("SPEC-0001", "SPEC-0001-TSK-9999"),
        ):
            with (
                self.subTest(parents=parents),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(stage, task=True, task_parent_ids=parents)
                with self.assertRaisesRegex(spec_packages.SpecPackageError, "parent"):
                    spec_packages.load_spec_packages(stage)

    def test_current_execution_states_require_consistent_parents(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            ("approved", "in-progress", "ready", "share one status"),
            ("completed", "in-progress", "in-progress", "share one status"),
            ("in-progress", "completed", "blocked", "share one status"),
            ("completed", "in-progress", "completed", "share one status"),
        )
        for spec_status, plan_status, task_status, message in cases:
            with (
                self.subTest(message=message),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(
                    stage,
                    spec_status=spec_status,
                    plan=True,
                    plan_status=plan_status,
                    task=True,
                    task_status=task_status,
                )
                with self.assertRaisesRegex(spec_packages.SpecPackageError, message):
                    spec_packages.load_spec_packages(stage)

        for spec_status, plan_status, task_status in (
            ("approved", "approved", "ready"),
            ("in-progress", "in-progress", "in-progress"),
            ("blocked", "blocked", "blocked"),
        ):
            with (
                self.subTest(states=(spec_status, plan_status, task_status)),
                tempfile.TemporaryDirectory() as directory,
            ):
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(
                    stage,
                    spec_status=spec_status,
                    plan=True,
                    plan_status=plan_status,
                    task=True,
                    task_status=task_status,
                )
                self.assertEqual(1, len(spec_packages.load_spec_packages(stage)))

    def test_recorded_terminal_retirement_needs_no_recovery_ledger(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(
                before_stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            _write_package(before_stage, number="0002", slug="keeper")
            _write_package(after_stage, number="0002", slug="keeper")
            self.assertEqual(
                (),
                spec_packages.validate_spec_package_lifecycle(
                    spec_packages.load_spec_packages(before_stage),
                    spec_packages.load_spec_packages(
                        after_stage,
                        _current_contracts=False,
                        _completion_evidence=False,
                    ),
                    retired_paths=frozenset(
                        {pathlib.PurePosixPath("docs/03.specs/0001-example/spec.md")}
                    ),
                ),
            )

    def test_unrecorded_retirement_fails_closed_whatever_the_status(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(before_stage, plan=True, task=True)
            _write_package(after_stage, number="0002", slug="keeper")
            _write_package(before_stage, number="0002", slug="keeper")
            self.assertEqual(
                {("package-retirement-unrecorded", "docs/03.specs/0001-example")},
                {
                    (finding.code, finding.path)
                    for finding in spec_packages.validate_spec_package_lifecycle(
                        spec_packages.load_spec_packages(before_stage),
                        spec_packages.load_spec_packages(after_stage),
                    )
                },
            )

    def test_retained_package_keeps_non_terminal_execution_evidence(self) -> None:
        spec_packages = _spec_packages_module()
        for plan_status, task_status, removed in (
            ("in-progress", "in-progress", "docs/03.specs/0001-example/plan.md"),
            (
                "in-progress",
                "in-progress",
                "docs/03.specs/0001-example/tasks/tsk-0001-implement.md",
            ),
        ):
            with (
                self.subTest(removed=removed),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                before_stage = root / "before/docs/03.specs"
                after_stage = root / "after/docs/03.specs"
                _write_package(
                    before_stage,
                    plan=True,
                    plan_status=plan_status,
                    task=True,
                    task_status=task_status,
                )
                _write_package(
                    after_stage,
                    plan=removed.endswith("tsk-0001-implement.md"),
                    task=removed.endswith("plan.md"),
                )
                findings = spec_packages.validate_spec_package_lifecycle(
                    spec_packages.load_spec_packages(before_stage),
                    spec_packages.load_spec_packages(
                        after_stage,
                        _current_contracts=False,
                        _completion_evidence=False,
                    ),
                )
                self.assertEqual(
                    {("execution-evidence-deletion-forbidden", removed)},
                    {(finding.code, finding.path) for finding in findings},
                )

    def test_retained_completed_package_keeps_execution_evidence(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(
                before_stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            _write_package(after_stage, spec_status="completed")
            spec_packages.load_spec_packages(before_stage)
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "completion"):
                spec_packages.load_spec_packages(after_stage)

    def test_open_time_identity_ignores_benign_parent_churn(self) -> None:
        """Another process writing to a traversed parent is not a swap."""

        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before = os.stat(root)
            (root / "sibling").mkdir()
            after = os.stat(root)
            # This is what /tmp does continuously on a shared machine: the
            # directory's link count and mtime move while the directory itself
            # is untouched.
            self.assertNotEqual(
                spec_packages._directory_snapshot(before),
                spec_packages._directory_snapshot(after),
            )
            # Identity is what a symlink swap cannot forge, and it is the only
            # thing the stat-then-open check is entitled to require. An
            # attacker can match mtime with utimensat; nobody can match st_ino.
            self.assertEqual(
                spec_packages._path_identity(before),
                spec_packages._path_identity(after),
            )

    def test_open_time_identity_still_separates_distinct_directories(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "one").mkdir()
            (root / "two").mkdir()
            self.assertNotEqual(
                spec_packages._path_identity(os.stat(root / "one")),
                spec_packages._path_identity(os.stat(root / "two")),
            )

    def test_whole_package_retirement_requires_a_tombstone(self) -> None:
        """Stage 00 retires a package with a Tombstone, not by silent deletion."""

        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(
                before_stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            _write_package(before_stage, number="0002", slug="keeper")
            _write_package(after_stage, number="0002", slug="keeper")
            before = spec_packages.load_spec_packages(before_stage)
            after = spec_packages.load_spec_packages(after_stage)
            self.assertEqual(
                {("package-retirement-unrecorded", "docs/03.specs/0001-example")},
                {
                    (finding.code, finding.path)
                    for finding in spec_packages.validate_spec_package_lifecycle(
                        before, after
                    )
                },
            )
            self.assertEqual(
                (),
                spec_packages.validate_spec_package_lifecycle(
                    before,
                    after,
                    retired_paths=frozenset(
                        {pathlib.PurePosixPath("docs/03.specs/0001-example/spec.md")}
                    ),
                ),
            )

    def test_a_catalog_row_records_a_retirement_once_adopted(self) -> None:
        """After adoption a Retention Catalog row, not a Tombstone, records it."""

        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            archive = root / "docs/98.archive"
            for name in ("migrations", "tombstones", "retired/03.specs/0001-example"):
                (archive / name).mkdir(parents=True)
            (archive / "retired/03.specs/0001-example/spec.md").write_text(
                "# Example\n", encoding="utf-8"
            )
            (archive / "README.md").write_text("# Archive\n", encoding="utf-8")
            (archive / "retention-catalog.md").write_text(
                "# Archive\n\n## Retention Catalog\n\n"
                "| Record | Class | Names | Source |\n| --- | --- | --- | --- |\n"
                "| `retired/03.specs/0001-example/` | retired | Withdrawn. | "
                "`x:docs/03.specs/0001-example` |\n",
                encoding="utf-8",
            )
            registry = root / "docs/99.templates/registry.json"
            registry.parent.mkdir(parents=True)
            expected = pathlib.PurePosixPath("docs/03.specs/0001-example/spec.md")
            for model, recorded in (("transition", False), ("adopted", True)):
                with self.subTest(model=model):
                    registry.write_text(
                        json.dumps({"common": {"archive_disposition_model": model}}),
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        recorded, expected in spec_packages._recorded_retirements(root)
                    )

    def test_unsafe_catalog_retirement_grants_no_exemption(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            archive = root / "docs/98.archive"
            for name in ("migrations", "tombstones"):
                (archive / name).mkdir(parents=True)
            (archive / "README.md").write_text("# Archive\n", encoding="utf-8")
            target = root / "relocated"
            target.mkdir()
            (archive / "retired").symlink_to(target, target_is_directory=True)
            registry = root / "docs/99.templates/registry.json"
            registry.parent.mkdir(parents=True)
            registry.write_text(
                json.dumps({"common": {"archive_disposition_model": "adopted"}}),
                encoding="utf-8",
            )
            self.assertEqual(frozenset(), spec_packages._recorded_retirements(root))

    def test_preserved_package_is_not_a_retirement(self) -> None:
        """Completion and withdrawal are different events with different records.

        A package moved to the archive keeps every document, so demanding a
        Tombstone for it would record a withdrawal that never happened. A
        package that leaves without being preserved still needs one.
        """

        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(
                before_stage,
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            after_stage.mkdir(parents=True, exist_ok=True)
            before = spec_packages.load_spec_packages(before_stage)
            after = spec_packages.load_spec_packages(after_stage)
            preserved = frozenset(
                {pathlib.PurePosixPath("docs/03.specs/0001-example/spec.md")}
            )
            self.assertEqual(
                (),
                spec_packages.validate_spec_package_lifecycle(
                    before, after, preserved_paths=preserved
                ),
            )
            self.assertEqual(
                {("package-retirement-unrecorded", "docs/03.specs/0001-example")},
                {
                    (finding.code, finding.path)
                    for finding in spec_packages.validate_spec_package_lifecycle(
                        before, after
                    )
                },
            )

    def test_lifecycle_authority_is_free_of_archive_and_fixed_count_coupling(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        source = ROOT.joinpath(
            "scripts/lib/document_governance/spec_packages.py"
        ).read_text(encoding="utf-8")
        for token in (
            "_read_migration_authority",
            "_approved_migration_document",
            "one_time_package_ids",
            "recovery_commits",
            "source_to_final",
        ):
            self.assertNotIn(token, source)
        self.assertIsNone(re.search(r"!=\s*(?:49|46)\b", source))
        signature = inspect.signature(spec_packages.validate_spec_package_lifecycle)
        # Both path sets are facts the caller injects. The validator still
        # reads no archive of its own, which is what this test guards.
        self.assertEqual(
            ["previous", "current", "retired_paths", "preserved_paths", "registry"],
            list(signature.parameters),
        )

    def test_public_repository_validator_enforces_snapshot_lifecycle(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            stage = root / "docs/03.specs"
            _write_package(stage, plan=True)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ],
                cwd=root,
                check=True,
            )
            stage.joinpath("0001-example/plan.md").unlink()
            findings = spec_packages.validate_repository_spec_package_lifecycle(
                root,
                spec_packages.load_spec_packages(stage),
                base_ref="HEAD",
            )
            self.assertEqual(
                {"execution-evidence-deletion-forbidden"},
                {finding.code for finding in findings},
            )

    def test_divergent_branch_handoff_accepts_each_durable_receipt_carrier(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for carrier in ("current", "completed"):
            with (
                self.subTest(carrier=carrier),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(root, carrier=carrier)
                self.assertEqual(
                    (),
                    spec_packages.validate_repository_spec_package_lifecycle(
                        root,
                        spec_packages.load_spec_packages(stage),
                        base_ref=commit,
                    ),
                )

    def test_current_receipt_carrier_accepts_blocked_but_not_ready(self) -> None:
        spec_packages = _spec_packages_module()
        for status, valid in (("blocked", True), ("ready", False)):
            with (
                self.subTest(status=status),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(root)
                task = stage / "0002-target/tasks/tsk-0001-implement.md"
                _set_status(task, "in-progress", status)
                if status == "blocked":
                    _set_status(stage / "0002-target/spec.md", "in-progress", "blocked")
                    _set_status(stage / "0002-target/plan.md", "in-progress", "blocked")
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                receipt_codes = {
                    finding.code
                    for finding in findings
                    if finding.code.startswith("branch-integration-receipt")
                }
                if valid:
                    self.assertEqual(set(), receipt_codes)
                else:
                    self.assertIn("branch-integration-receipt-invalid", receipt_codes)

    def test_divergent_branch_handoff_matches_completed_identity_across_slugs(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for mutation in ("none", "uncommitted", "modified", "ambiguous"):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(
                    root,
                    completed_slug="other-lineage",
                    completed_record=(
                        "uncommitted" if mutation == "uncommitted" else "committed"
                    ),
                )
                completed = root / "docs/98.archive/completed/03.specs"
                if mutation == "modified":
                    with (completed / "0001-other-lineage/spec.md").open(
                        "a", encoding="utf-8"
                    ) as file:
                        file.write("\nmodified\n")
                elif mutation == "ambiguous":
                    _write_package(
                        completed,
                        number="0001",
                        slug="source",
                        spec_status="completed",
                    )
                    with self.assertRaisesRegex(
                        spec_packages.SpecPackageError, "duplicate.*identity"
                    ):
                        spec_packages.validate_repository_spec_package_lifecycle(
                            root,
                            spec_packages.load_spec_packages(stage),
                            base_ref=commit,
                        )
                    continue
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                if mutation == "none":
                    self.assertEqual((), findings)
                else:
                    self.assertIn(
                        "branch-integration-receipt-invalid",
                        {finding.code for finding in findings},
                    )

    def test_divergent_branch_handoff_requires_exactly_one_receipt_carrier(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for carrier, expected in (
            ("missing", "branch-integration-receipt-required"),
            ("current", "branch-integration-receipt-duplicate"),
        ):
            with (
                self.subTest(carrier=carrier),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, receipt = _branch_handoff_fixture(root, carrier=carrier)
                if carrier == "current":
                    archived_target = _write_package(
                        root / "docs/98.archive/completed/03.specs",
                        number="0002",
                        slug="target",
                        spec_status="completed",
                        plan=True,
                        plan_status="completed",
                        task=True,
                        task_status="completed",
                    )
                    _set_frontmatter_value(
                        archived_target / "tasks/tsk-0001-implement.md",
                        "branch_integration_receipts",
                        [receipt],
                    )
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                self.assertIn(expected, {finding.code for finding in findings})

    def test_divergent_branch_handoff_rejects_invalid_receipt_bindings(self) -> None:
        spec_packages = _spec_packages_module()
        cases = {
            "wrong-base": {"source_commit": "f" * 40},
            "wrong-source-path": {
                "source_package_path": "docs/03.specs/0003-not-source"
            },
            "wrong-source-id": {"source_artifact_id": "SPEC-0003"},
            "wrong-preserved-path": {
                "preserved_package_path": (
                    "docs/98.archive/superseded/03.specs/0003-not-source"
                )
            },
            "wrong-target-path": {
                "target_package_path": "docs/03.specs/0003-not-target"
            },
            "wrong-target-id": {"target_artifact_id": "SPEC-0003"},
            "same-source-target-id": {"target_artifact_id": "SPEC-0001"},
        }
        for label, updates in cases.items():
            with (
                self.subTest(case=label),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(
                    root,
                    receipt_updates=updates,
                )
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                self.assertIn(
                    "branch-integration-receipt-invalid",
                    {finding.code for finding in findings},
                )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            stage, _, _ = _branch_handoff_fixture(
                root,
                receipt_updates={"source_package_path": "docs/03.specs/../0001-source"},
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "unsafe"):
                spec_packages.load_spec_packages(stage)

    def test_divergent_branch_handoff_rejects_missing_completed_origin_and_inactive_target(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for mutation in (
            "missing-completed-origin",
            "uncommitted-completed-origin",
            "modified-completed-origin",
            "inactive-target",
            "archived-target-missing-evidence",
        ):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(
                    root,
                    carrier=(
                        "completed"
                        if mutation == "archived-target-missing-evidence"
                        else "current"
                    ),
                    completed_record=(
                        "uncommitted"
                        if mutation == "uncommitted-completed-origin"
                        else "committed"
                    ),
                )
                if mutation == "missing-completed-origin":
                    shutil.rmtree(
                        root / "docs/98.archive/completed/03.specs/0001-source"
                    )
                elif mutation == "modified-completed-origin":
                    completed_spec = (
                        root / "docs/98.archive/completed/03.specs/0001-source/spec.md"
                    )
                    with completed_spec.open("a", encoding="utf-8") as file:
                        file.write("\nmodified\n")
                elif mutation == "inactive-target":
                    target = stage / "0002-target"
                    _set_status(target / "spec.md", "in-progress", "approved")
                    _set_status(target / "plan.md", "in-progress", "approved")
                    _set_status(
                        target / "tasks/tsk-0001-implement.md",
                        "in-progress",
                        "completed",
                    )
                    _set_review_rows(
                        target / "tasks/tsk-0001-implement.md",
                        (("1", "accepted", "Fixture review."),),
                    )
                elif mutation == "archived-target-missing-evidence":
                    task = (
                        root / "docs/98.archive/completed/03.specs/0002-target/"
                        "tasks/tsk-0001-implement.md"
                    )
                    text = task.read_text(encoding="utf-8")
                    task.write_text(
                        text.replace(
                            "| 1 | W1 | PASS: focused check | N/A: local validation only |\n",
                            "",
                        ),
                        encoding="utf-8",
                    )
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                self.assertIn(
                    "branch-integration-receipt-invalid",
                    {finding.code for finding in findings},
                )

    def test_divergent_branch_handoff_requires_exact_safe_package_bytes(self) -> None:
        spec_packages = _spec_packages_module()
        for mutation in (
            "changed",
            "missing",
            "extra",
            "outside-symlink",
            "non-regular",
            "oversized",
        ):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                stage, commit, _ = _branch_handoff_fixture(root)
                preserved = root / "docs/98.archive/superseded/03.specs/0001-source"
                if mutation == "changed":
                    with (preserved / "spec.md").open("a", encoding="utf-8") as file:
                        file.write("\nchanged\n")
                elif mutation == "missing":
                    (preserved / "plan.md").unlink()
                elif mutation == "extra":
                    (preserved / "extra.md").write_text("extra\n", encoding="utf-8")
                elif mutation == "outside-symlink":
                    outside = root / "outside"
                    outside.mkdir()
                    (outside / "spec.md").write_text("outside\n", encoding="utf-8")
                    shutil.rmtree(preserved)
                    preserved.symlink_to(outside, target_is_directory=True)
                elif mutation == "non-regular":
                    (preserved / "spec.md").unlink()
                    os.mkfifo(preserved / "spec.md")
                else:
                    (preserved / "spec.md").write_bytes(
                        b"x" * (spec_packages.MAX_SPEC_FILE_BYTES + 1)
                    )
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref=commit,
                )
                self.assertIn(
                    "branch-integration-receipt-invalid",
                    {finding.code for finding in findings},
                )

    def test_ordinary_preservation_requires_terminal_archive_metadata(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            stage = root / "docs/03.specs"
            source = _write_package(stage, plan=True, task=True)
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "baseline",
                ),
                cwd=root,
                check=True,
            )
            mirror = root / "docs/98.archive/completed/03.specs/0001-example"
            mirror.parent.mkdir(parents=True)
            shutil.copytree(source, mirror)
            shutil.rmtree(source)
            findings = spec_packages.validate_repository_spec_package_lifecycle(
                root,
                spec_packages.load_spec_packages(stage),
                base_ref="HEAD",
            )
            self.assertIn(
                "package-retirement-unrecorded",
                {finding.code for finding in findings},
            )
            _set_status(mirror / "spec.md", "in-progress", "completed")
            _set_status(mirror / "plan.md", "in-progress", "completed")
            _set_status(
                mirror / "tasks/tsk-0001-implement.md",
                "in-progress",
                "completed",
            )
            task = mirror / "tasks/tsk-0001-implement.md"
            _set_review_rows(task, (("1", "accepted", "Fixture review."),))
            task.write_text(
                task.read_text(encoding="utf-8").replace(
                    "| 1 | W1 | PASS | N/A: local validation only |",
                    "| 1 | W1 | PASS: focused check | N/A: local validation only |",
                    1,
                ),
                encoding="utf-8",
            )
            receipt = (
                "| 1 | W1 | PASS: focused check | N/A: local validation only |\n"
            )
            task_body = task.read_text(encoding="utf-8")
            task.write_text(task_body.replace(receipt, ""), encoding="utf-8")
            findings = spec_packages.validate_repository_spec_package_lifecycle(
                root,
                spec_packages.load_spec_packages(stage),
                base_ref="HEAD",
            )
            self.assertIn(
                "package-retirement-unrecorded",
                {finding.code for finding in findings},
            )
            task.write_text(task_body, encoding="utf-8")
            self.assertEqual(
                (),
                spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages.load_spec_packages(stage),
                    base_ref="HEAD",
                ),
            )

    def test_bounded_git_streams_both_pipes_and_reaps_on_failure(self) -> None:
        spec_packages = _spec_packages_module()
        real_popen = subprocess.Popen

        def invoke(
            script: str, *, byte_limit: int, timeout: float = 1.0
        ) -> tuple[bytes, list]:
            processes = []

            def spawn(_command, **kwargs):
                process = real_popen([sys.executable, "-c", script], **kwargs)
                processes.append(process)
                return process

            with (
                mock.patch.object(spec_packages.subprocess, "Popen", side_effect=spawn),
                mock.patch.object(
                    spec_packages,
                    "GIT_COMMAND_TIMEOUT_SECONDS",
                    timeout,
                ),
            ):
                result = spec_packages._bounded_git(
                    ROOT,
                    "fixture",
                    byte_limit=byte_limit,
                )
            return result, processes

        exact, exact_processes = invoke(
            "import sys; sys.stdout.buffer.write(b'x' * 64); sys.stdout.flush()",
            byte_limit=64,
        )
        self.assertEqual(b"x" * 64, exact)
        self.assertIsNotNone(exact_processes[0].poll())

        for stream in ("stdout", "stderr"):
            with self.subTest(stream=stream):
                processes = []

                def spawn(_command, **kwargs):
                    script = (
                        "import sys; "
                        f"sys.{stream}.buffer.write(b'x' * 65); "
                        f"sys.{stream}.flush()"
                    )
                    process = real_popen([sys.executable, "-c", script], **kwargs)
                    processes.append(process)
                    return process

                with (
                    mock.patch.object(
                        spec_packages.subprocess,
                        "Popen",
                        side_effect=spawn,
                    ),
                    mock.patch.object(
                        spec_packages,
                        "GIT_COMMAND_TIMEOUT_SECONDS",
                        1.0,
                    ),
                    self.assertRaisesRegex(
                        spec_packages.SpecPackageError, "byte budget"
                    ),
                ):
                    spec_packages._bounded_git(ROOT, "fixture", byte_limit=64)
                self.assertIsNotNone(processes[0].poll())

        timed_processes = []

        def spawn_timeout(_command, **kwargs):
            process = real_popen(
                [sys.executable, "-c", "import time; time.sleep(10)"],
                **kwargs,
            )
            timed_processes.append(process)
            return process

        started = time.monotonic()
        with (
            mock.patch.object(
                spec_packages.subprocess,
                "Popen",
                side_effect=spawn_timeout,
            ),
            mock.patch.object(
                spec_packages,
                "GIT_COMMAND_TIMEOUT_SECONDS",
                0.05,
            ),
            self.assertRaisesRegex(spec_packages.SpecPackageError, "deadline"),
        ):
            spec_packages._bounded_git(ROOT, "fixture", byte_limit=64)
        self.assertLess(time.monotonic() - started, 2.0)
        self.assertIsNotNone(timed_processes[0].poll())

    def test_base_snapshot_rejects_file_at_limit_plus_one(self) -> None:
        spec_packages = _spec_packages_module()
        commit = b"a" * 40 + b"\n"
        tree = b"100644 blob " + b"b" * 40 + b"\tdocs/03.specs/0001-example/spec.md\0"
        body = _document_text("spec", "SPEC-0001", ("REQ-0001",)).encode("utf-8")
        exact = body + b"\n" * (spec_packages.MAX_SPEC_FILE_BYTES - len(body))
        with mock.patch.object(
            spec_packages,
            "_bounded_git",
            side_effect=(commit, tree, exact),
        ):
            packages = spec_packages._load_base_spec_packages(
                ROOT,
                base_ref="HEAD",
            )
        self.assertEqual(1, len(packages))

        with (
            mock.patch.object(
                spec_packages,
                "_bounded_git",
                side_effect=(commit, tree, exact + b"\n"),
            ),
            self.assertRaisesRegex(spec_packages.SpecPackageError, "byte limit"),
        ):
            spec_packages._load_base_spec_packages(
                ROOT,
                base_ref="HEAD",
            )

    def test_restored_stage04_fails_closed(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            stage = root / "docs/03.specs"
            _write_package(stage)
            root.joinpath("docs/04.execution").mkdir()
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "Stage 04"):
                spec_packages.load_spec_packages(stage)

    def test_current_repository_spec_packages_cover_spec_directories(self) -> None:
        spec_packages = _spec_packages_module()
        registry = load_registry()
        packages = spec_packages.load_spec_packages(
            ROOT / "docs/03.specs", registry=registry
        )
        expected_paths = {
            path
            for path in (ROOT / "docs/03.specs").iterdir()
            if path.is_dir() and (path / "spec.md").is_file()
        }
        self.assertEqual(expected_paths, {package.path for package in packages})
        self.assertTrue(
            all(not package.path.name.startswith("spec-") for package in packages)
        )
        self.assertFalse((ROOT / "docs/04.execution").exists())
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/design.md")))
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/tests.md")))
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/task.md")))
        self.assertFalse((ROOT / "DESIGN.md").exists())
        lifecycle = spec_packages.validate_repository_spec_package_lifecycle_details(
            ROOT,
            packages,
            base_ref="main",
            registry=registry,
        )
        self.assertEqual((), lifecycle.findings)
        self.assertRegex(lifecycle.generation_source or "", r"^[0-9a-f]{40,64}$")
        self.assertTrue(lifecycle.actual_normalizations)

        proof_task = next(
            task
            for package in packages
            for task in package.tasks
            if "### Contract Migration" in task.body
        )
        missing = dataclasses.replace(
            proof_task,
            body=proof_task.body.split("### Contract Migration", 1)[0],
        )
        altered_packages = tuple(
            dataclasses.replace(
                package,
                tasks=tuple(
                    missing if task.path == missing.path else task
                    for task in package.tasks
                ),
            )
            for package in packages
        )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "migration proof"):
            spec_packages._migration_proof(altered_packages, registry)

        malformed_task = dataclasses.replace(
            proof_task,
            body=proof_task.body.replace(
                lifecycle.generation_source or "missing-source",
                "not-a-full-object-id",
                1,
            ),
        )
        malformed_packages = tuple(
            dataclasses.replace(
                package,
                tasks=tuple(
                    malformed_task if task.path == malformed_task.path else task
                    for task in package.tasks
                ),
            )
            for package in packages
        )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "full object ID"):
            spec_packages._migration_proof(malformed_packages, registry)

        source_registry = json.loads(
            json.dumps(
                spec_packages.load_registry_document_at_revision(
                    lifecycle.generation_source,
                    root=ROOT,
                )
            )
        )
        source_registry["common"]["lifecycle_generation"] = 4
        with self.assertRaisesRegex(
            spec_packages.SpecPackageError, "original lifecycle generation"
        ):
            spec_packages._validate_source_registry(source_registry)

        real_bounded_git = spec_packages._bounded_git

        def nonancestor(root, *arguments, byte_limit):
            if arguments and arguments[0] == "merge-base":
                return ("f" * 40 + "\n").encode()
            return real_bounded_git(root, *arguments, byte_limit=byte_limit)

        with (
            mock.patch.object(spec_packages, "_bounded_git", side_effect=nonancestor),
            self.assertRaisesRegex(
                spec_packages.SpecPackageError, "not a current ancestor"
            ),
        ):
            spec_packages.validate_repository_spec_package_lifecycle_details(
                ROOT,
                packages,
                base_ref="main",
                registry=registry,
            )

        source = spec_packages._load_base_spec_packages(
            ROOT, base_ref=lifecycle.generation_source
        )
        completed_package = next(
            package
            for package in packages
            if any(task.status == "completed" for task in package.tasks)
        )
        completed_task = next(
            task for task in completed_package.tasks if task.status == "completed"
        )
        changed_task = dataclasses.replace(
            completed_task,
            body=completed_task.body + "\nChanged terminal body.\n",
            source_text=completed_task.source_text + "\nChanged terminal body.\n",
        )
        changed_packages = tuple(
            dataclasses.replace(
                package,
                tasks=tuple(
                    changed_task if task.path == changed_task.path else task
                    for task in package.tasks
                ),
            )
            if package.path == completed_package.path
            else package
            for package in packages
        )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "body or identity"):
            spec_packages._validate_terminal_task_migration(source, changed_packages)

    def test_postcutover_v4_baseline_needs_no_migration_proof(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            stage = root / "docs/03.specs"
            _write_package(stage, plan=True, task=True)
            terminal_package = _write_package(
                stage,
                number="0002",
                slug="terminal",
                spec_status="completed",
                plan=True,
                plan_status="completed",
                task=True,
                task_status="completed",
            )
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)
            subprocess.run(
                (
                    "git",
                    "-c",
                    "user.name=Spec Fixture",
                    "-c",
                    "user.email=spec@example.invalid",
                    "commit",
                    "-qm",
                    "v4 baseline",
                ),
                cwd=root,
                check=True,
            )
            registry = load_registry()
            current = spec_packages.load_spec_packages(stage, registry=registry)
            result = spec_packages.validate_repository_spec_package_lifecycle_details(
                root,
                current,
                base_ref="HEAD",
                registry=registry,
            )
            self.assertEqual((), result.findings)
            self.assertIsNone(result.generation_source)
            self.assertEqual(frozenset(), result.actual_normalizations)

            terminal_task = terminal_package / "tasks/tsk-0001-implement.md"
            terminal_task.write_text(
                terminal_task.read_text(encoding="utf-8") + "\nChanged body.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                spec_packages.SpecPackageError, "body or identity"
            ):
                spec_packages.validate_repository_spec_package_lifecycle_details(
                    root,
                    spec_packages.load_spec_packages(stage, registry=registry),
                    base_ref="HEAD",
                    registry=registry,
                )

    def test_cross_generation_completion_composes_migration_and_v4_events(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        registry = load_registry()
        spec_path = pathlib.PurePosixPath("docs/03.specs/0001-example/spec.md")
        plan_path = pathlib.PurePosixPath("docs/03.specs/0001-example/plan.md")
        task_path = pathlib.PurePosixPath(
            "docs/03.specs/0001-example/tasks/tsk-0001-implement.md"
        )
        prefix = (
            ("SPEC-0001", "draft", "review", "#spec-review"),
            ("SPEC-0001", "review", "approved", "#spec-approved"),
            ("SPEC-0001", "approved", "active", "#spec-active"),
            ("SPEC-0001-PLAN-0001", "draft", "approved", "#plan-approved"),
            ("SPEC-0001-PLAN-0001", "approved", "active", "#plan-active"),
            ("SPEC-0001-TSK-0001", "draft", "ready", "#task-ready"),
            (
                "SPEC-0001-TSK-0001",
                "ready",
                "in-progress",
                "#task-started",
            ),
        )
        appended = (
            ("SPEC-0001", "in-progress", "completed", "#spec-completed"),
            (
                "SPEC-0001-PLAN-0001",
                "in-progress",
                "completed",
                "#plan-completed",
            ),
            (
                "SPEC-0001-TSK-0001",
                "in-progress",
                "completed",
                "#task-completed",
            ),
        )

        def task_body(rows):
            anchors = "\n\n".join(
                f"### {evidence[1:].replace('-', ' ').title()}\n\nObserved."
                for *_, evidence in rows
            )
            table = "\n".join(
                (
                    "### Lifecycle Events",
                    "",
                    "| Artifact | From | To | Evidence |",
                    "| --- | --- | --- | --- |",
                    *("| " + " | ".join(row) + " |" for row in rows),
                )
            )
            return f"## Work Log\n\n{anchors}\n\n{table}\n"

        def document(path, profile, artifact, status, body=""):
            return spec_packages.SpecDocument(
                path, profile, artifact, status, (), body=body, source_text=body
            )

        source = spec_packages.SpecPackage(
            pathlib.Path("docs/03.specs/0001-example"),
            "0001",
            "example",
            document(spec_path, "spec", "SPEC-0001", "active"),
            document(plan_path, "plan", "SPEC-0001-PLAN-0001", "active"),
            (
                document(
                    task_path,
                    "task",
                    "SPEC-0001-TSK-0001",
                    "in-progress",
                    task_body(prefix),
                ),
            ),
            (),
        )
        current = dataclasses.replace(
            source,
            spec=dataclasses.replace(source.spec, status="completed"),
            plan=dataclasses.replace(source.plan, status="completed"),
            tasks=(
                dataclasses.replace(
                    source.tasks[0],
                    status="completed",
                    body=task_body((*prefix, *appended)),
                    source_text=task_body((*prefix, *appended)),
                ),
            ),
        )
        source_registry = {
            "lifecycles": {
                "spec": {
                    "initial_status": "draft",
                    "transitions": {
                        "draft": ["review"],
                        "review": ["approved"],
                        "approved": ["active"],
                    },
                },
                "plan": {
                    "initial_status": "draft",
                    "transitions": {
                        "draft": ["approved"],
                        "approved": ["active"],
                    },
                },
                "task": {
                    "initial_status": "draft",
                    "transitions": {
                        "draft": ["ready"],
                        "ready": ["in-progress"],
                    },
                },
            }
        }
        normalizations = spec_packages._generation_normalizations(
            (source,), (current,), registry
        )
        self.assertEqual(
            frozenset(
                {
                    (spec_path.as_posix(), "active", "in-progress"),
                    (plan_path.as_posix(), "active", "in-progress"),
                }
            ),
            normalizations,
        )
        spec_packages._validate_terminal_task_migration((source,), (current,))
        findings, transitions = spec_packages._validate_task_lifecycle_events(
            (source,),
            (current,),
            registry,
            prefix_previous=(source,),
            normalizations=normalizations,
            source_registry=source_registry,
        )
        self.assertEqual((), findings)
        self.assertEqual(
            frozenset(
                {
                    (spec_path.as_posix(), "active", "completed"),
                    (plan_path.as_posix(), "active", "completed"),
                    (task_path.as_posix(), "in-progress", "completed"),
                }
            ),
            transitions,
        )
        missing = dataclasses.replace(
            current,
            tasks=(
                dataclasses.replace(
                    current.tasks[0],
                    body=task_body(prefix),
                    source_text=task_body(prefix),
                ),
            ),
        )
        with self.assertRaisesRegex(
            spec_packages.SpecPackageError, "unsupported lifecycle generation"
        ):
            spec_packages._generation_normalizations((source,), (missing,), registry)

        wrong_rows = (
            *prefix,
            ("SPEC-0001", "approved", "completed", "#spec-completed"),
            *appended[1:],
        )
        wrong = dataclasses.replace(
            current,
            tasks=(
                dataclasses.replace(
                    current.tasks[0],
                    body=task_body(wrong_rows),
                    source_text=task_body(wrong_rows),
                ),
            ),
        )
        wrong_normalizations = spec_packages._generation_normalizations(
            (source,), (wrong,), registry
        )
        wrong_findings, _ = spec_packages._validate_task_lifecycle_events(
            (),
            (wrong,),
            registry,
            prefix_previous=(source,),
            normalizations=wrong_normalizations,
            source_registry=source_registry,
        )
        self.assertIn(
            "lifecycle event is not a registered direct edge: approved -> completed",
            {finding.message for finding in wrong_findings},
        )

        source_terminal = dataclasses.replace(
            source,
            tasks=(dataclasses.replace(source.tasks[0], status="completed"),),
        )
        changed_status = dataclasses.replace(
            source_terminal,
            tasks=(dataclasses.replace(source_terminal.tasks[0], status="cancelled"),),
        )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "changed"):
            spec_packages._validate_terminal_task_migration(
                (source_terminal,), (changed_status,)
            )
        changed_body = dataclasses.replace(
            source_terminal,
            tasks=(
                dataclasses.replace(
                    source_terminal.tasks[0],
                    body=source_terminal.tasks[0].body + "\nChanged.\n",
                    source_text=source_terminal.tasks[0].source_text
                    + "\nChanged.\n",
                ),
            ),
        )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "body or identity"):
            spec_packages._validate_terminal_task_migration(
                (source_terminal,), (changed_body,)
            )
        with self.assertRaisesRegex(spec_packages.SpecPackageError, "removed"):
            spec_packages._validate_terminal_task_migration(
                (source_terminal,), (dataclasses.replace(current, tasks=()),)
            )

    def test_current_index_routes_each_current_package_by_directory(self) -> None:
        """SPEC-0184 rule 6: one directory-link row per package, no status copy."""

        rows = _current_spec_rows(
            (ROOT / "docs/03.specs/README.md").read_text(encoding="utf-8")
        )
        statuses = re.compile(
            r"\b(?:draft|review|approved|active|completed|cancelled|superseded)\b"
        )
        packages = sorted((ROOT / "docs/03.specs").glob("*/spec.md"))
        self.assertEqual(len(packages), len(rows))
        for spec_path in packages:
            metadata = parse_frontmatter_text(spec_path.read_text(encoding="utf-8"))
            row = rows[metadata["artifact_id"]]
            self.assertIn(f"](./{spec_path.parent.name}/)", row)
            self.assertIsNone(statuses.search(row), row)

    def test_active_route_authority_uses_only_canonical_spec_execution_paths(
        self,
    ) -> None:
        forbidden = (
            re.compile(r"docs/04\.execution(?:/|`|$)"),
            re.compile(r"docs/03\.specs/spec-[0-9]{4}-"),
            re.compile(r"docs/03\.specs/[0-9]{1,3}-[a-z0-9-]+"),
            re.compile(r"docs/03\.specs/[^\s`]+/task\.md"),
        )
        violations: list[str] = []
        for path in self.ACTIVE_ROUTE_FILES:
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden:
                for match in pattern.finditer(text):
                    violations.append(f"{path.relative_to(ROOT)}:{match.group(0)}")
        metadata_sources = (
            ROOT / "scripts/lib/document_governance/metadata_validator.py",
            *sorted((ROOT / "scripts/lib/document_governance/metadata").glob("*.py")),
        )
        for stale in (
            "docs/03.specs/005-data-analytics",
            "docs/03.specs/133-target-surface-contract-convergence",
        ):
            for path in metadata_sources:
                if stale in path.read_text(encoding="utf-8"):
                    violations.append(f"{path.relative_to(ROOT)}:{stale}")
        registry = load_registry(ROOT / "docs/99.templates/registry.json")
        self.assertEqual(
            "docs/03.specs/{package_number:4}-{slug}/plan.md",
            registry.profiles["plan"]["path_pattern"],
        )
        self.assertEqual(
            "docs/03.specs/{package_number:4}-{slug}/tasks/tsk-{task_number:4}-{slug}.md",
            registry.profiles["task"]["path_pattern"],
        )
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
