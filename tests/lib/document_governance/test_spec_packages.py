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
from scripts.lib.document_governance.registry import load_registry


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _current_spec_rows(index_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in index_text.splitlines():
        if line.startswith("| SPEC-"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows[cells[0]] = cells[2]
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
    status: str = "active",
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
            "| 1 | W1 | PASS: focused check exit 0 | N/A: local validation only |",
        )
    return text


def _write_package(
    stage: pathlib.Path,
    *,
    number: str = "0001",
    slug: str = "example",
    spec_id: str | None = None,
    spec_status: str = "active",
    plan: bool = False,
    plan_status: str = "active",
    task: bool = False,
    task_status: str = "in-progress",
    task_parent_ids: tuple[str, ...] | None = None,
) -> pathlib.Path:
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
            (f"SPEC-{number}", f"SPEC-{number}-PLAN-0001")
            if plan
            else (f"SPEC-{number}",)
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


def _branch_handoff_fixture(
    root: pathlib.Path,
    *,
    carrier: str = "current",
    completed_record: str = "committed",
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
        slug="source",
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
    preserved = (
        root
        / "docs/98.archive/superseded/03.specs/0001-source"
    )
    preserved.parent.mkdir(parents=True)
    shutil.copytree(source, preserved)
    shutil.rmtree(source)
    receipt = {
        "source_commit": commit,
        "source_package_path": "docs/03.specs/0001-source",
        "source_artifact_id": "SPEC-0001",
        "preserved_package_path": (
            "docs/98.archive/superseded/03.specs/0001-source"
        ),
        "target_package_path": "docs/03.specs/0002-target",
        "target_artifact_id": "SPEC-0002",
        "disposition": "historical-superseded",
    }
    receipt.update(receipt_updates or {})
    if carrier == "current":
        task = target / "tasks/tsk-0001-implement.md"
    elif carrier == "completed":
        archived_target = (
            root
            / "docs/98.archive/completed/03.specs/0002-target"
        )
        archived_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, archived_target)
        _set_status(archived_target / "spec.md", "active", "completed")
        _set_status(archived_target / "plan.md", "active", "completed")
        task = archived_target / "tasks/tsk-0001-implement.md"
        _set_status(task, "in-progress", "completed")
        shutil.rmtree(target)
    elif carrier == "missing":
        return stage, commit, receipt
    else:
        raise AssertionError(f"unsupported carrier: {carrier}")
    _set_frontmatter_value(task, "branch_integration_receipts", [receipt])
    return stage, commit, receipt


class SpecPackageTests(unittest.TestCase):
    ACTIVE_ROUTE_FILES = (
        ROOT / "docs/00.agent-governance/policies/documentation-protocol.md",
        ROOT / "docs/00.agent-governance/policies/quality-standards.md",
        ROOT / "docs/00.agent-governance/skills/execution-plan-agent.md",
        ROOT / ".claude/skills/execution-plan-agent/SKILL.md",
        ROOT / "README.md",
        ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml",
        ROOT / "scripts/validation/run-agent-precommit-all-files.sh",
    )

    def test_completed_coverage_accepts_pass_and_ignores_examples(
        self,
    ) -> None:
        spec_packages = _spec_packages_module()
        for result in ("PASS: focused check exit 0",):
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
                    .replace("PASS: focused check exit 0", result)
                    .replace(
                        "N/A: local validation only",
                        "[Current policy](../../../00.agent-governance/policies/bootstrap.md)",
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
                ("SPEC-0001", "SPEC-0001-PLAN-0001"),
                status="cancelled",
            )
            (package / "tasks/tsk-0002-cancelled.md").write_text(
                re.sub(r"(?m)^\|.*\n?", "", cancelled)
            )
            self.assertEqual(2, len(spec_packages.load_spec_packages(stage)[0].tasks))

    def test_completed_package_requires_structural_acceptance_evidence(self) -> None:
        spec_packages = _spec_packages_module()
        rows = "| 1 | W1 | PASS: focused check exit 0 | N/A: local validation only |"
        cases = {
            "missing-criterion": ("spec.md", "2. Another criterion.\n"),
            "uncovered-work": ("plan.md", "2. W2: Additional planned work.\n"),
            "skipped-criterion": (
                "row",
                rows.replace("PASS: focused check exit 0", "SKIP: runtime unavailable"),
            ),
            "draft-unreceipted-task": ("extra-task", "draft"),
            "commented-task": ("comment", "tasks/tsk-0001-implement.md"),
            "commented-spec": ("comment", "spec.md"),
            "commented-plan": ("comment", "plan.md"),
            "unknown-work": ("row", rows.replace("W1", "W9")),
            "unknown-criterion": ("row", rows.replace("| 1 |", "| 9 |")),
            "empty-result": ("row", rows.replace("PASS: focused check exit 0", "")),
            "bare-pass": ("row", rows.replace("PASS: focused check exit 0", "PASS")),
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
                                ("SPEC-0001", "SPEC-0001-PLAN-0001"),
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
                    spec_packages.SpecPackageError, "completion"
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
            ("completed", "active", "in-progress", "current Task requires active Spec"),
            ("active", "completed", "blocked", "current Task requires active Plan"),
            ("completed", "active", "completed", "active Plan requires active Spec"),
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
                    spec_packages.load_spec_packages(after_stage),
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
            ("active", "in-progress", "docs/03.specs/0001-example/plan.md"),
            (
                "active",
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
                    spec_packages.load_spec_packages(after_stage),
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
            ["previous", "current", "retired_paths", "preserved_paths"],
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
                stage, commit, receipt = _branch_handoff_fixture(
                    root, carrier=carrier
                )
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
                receipt_updates={
                    "source_package_path": "docs/03.specs/../0001-source"
                },
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
                        root
                        / "docs/98.archive/completed/03.specs/0001-source"
                    )
                elif mutation == "modified-completed-origin":
                    completed_spec = (
                        root
                        / "docs/98.archive/completed/03.specs/0001-source/spec.md"
                    )
                    with completed_spec.open("a", encoding="utf-8") as file:
                        file.write("\nmodified\n")
                elif mutation == "inactive-target":
                    target = stage / "0002-target"
                    _set_status(target / "spec.md", "active", "draft")
                    _set_status(target / "plan.md", "active", "completed")
                    _set_status(
                        target / "tasks/tsk-0001-implement.md",
                        "in-progress",
                        "completed",
                    )
                elif mutation == "archived-target-missing-evidence":
                    task = (
                        root
                        / "docs/98.archive/completed/03.specs/0002-target/"
                        "tasks/tsk-0001-implement.md"
                    )
                    text = task.read_text(encoding="utf-8")
                    task.write_text(
                        text.replace(
                            "| 1 | W1 | PASS: focused check exit 0 | N/A: local validation only |\n",
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
                preserved = (
                    root
                    / "docs/98.archive/superseded/03.specs/0001-source"
                )
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
            _set_status(mirror / "spec.md", "active", "completed")
            _set_status(mirror / "plan.md", "active", "completed")
            _set_status(
                mirror / "tasks/tsk-0001-implement.md",
                "in-progress",
                "completed",
            )
            task = mirror / "tasks/tsk-0001-implement.md"
            receipt = "| 1 | W1 | PASS: focused check exit 0 | N/A: local validation only |\n"
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
        packages = spec_packages.load_spec_packages(ROOT / "docs/03.specs")
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

    def test_current_index_status_matches_each_current_spec(self) -> None:
        rows = _current_spec_rows(
            (ROOT / "docs/03.specs/README.md").read_text(encoding="utf-8")
        )
        for spec_path in sorted((ROOT / "docs/03.specs").glob("*/spec.md")):
            metadata = parse_frontmatter_text(spec_path.read_text(encoding="utf-8"))
            artifact_id = metadata["artifact_id"]
            row = rows[artifact_id]
            self.assertIn(metadata["status"], row, artifact_id)
            self.assertEqual(
                metadata["status"] == "active",
                re.search(r"\bactive\b", row) is not None,
                artifact_id,
            )

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
