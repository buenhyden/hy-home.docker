from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.registry import load_registry


ROOT = pathlib.Path(__file__).resolve().parents[3]


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
    return f"""---
profile_id: {profile_id}
status: {status}
artifact_id: {artifact_id}
artifact_type: {profile_id}
parent_ids:
{parents}
created: 2026-08-22
updated: 2026-08-22
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


def _write_package(
    stage: pathlib.Path,
    *,
    number: str = "0001",
    slug: str = "example",
    spec_id: str | None = None,
    spec_status: str = "active",
    plan: bool = False,
    task: bool = False,
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
            _document_text("plan", f"plan-{number}", (f"SPEC-{number}",)),
            encoding="utf-8",
        )
    if task:
        tasks = package / "tasks"
        tasks.mkdir()
        parents = task_parent_ids or (
            (f"SPEC-{number}", f"plan-{number}")
            if plan
            else (f"SPEC-{number}",)
        )
        tasks.joinpath("tsk-0001-implement.md").write_text(
            _document_text("task", f"task-{number}-0001", parents),
            encoding="utf-8",
        )
    return package


class SpecPackageTests(unittest.TestCase):
    ACTIVE_ROUTE_FILES = (
        ROOT / "docs/00.agent-governance/policies/documentation-protocol.md",
        ROOT / "docs/00.agent-governance/policies/quality-standards.md",
        ROOT / "docs/00.agent-governance/skills/execution-plan-agent.md",
        ROOT / ".agents/skills/execution-plan-agent/SKILL.md",
        ROOT / ".claude/skills/execution-plan-agent/SKILL.md",
        ROOT / "README.md",
        ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml",
        ROOT / "scripts/validation/run-agent-precommit-all-files.sh",
    )

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
        self.assertEqual("plan-0001", package.plan.artifact_id)
        self.assertEqual("task-0001-0001", package.tasks[0].artifact_id)
        self.assertEqual(("openapi.yaml",), tuple(path.name for path in package.contracts))
        self.assertTrue(dataclasses.is_dataclass(package))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            package.number = "9999"

    def test_loader_rejects_symlink_non_regular_oversized_non_utf8_and_race(self) -> None:
        spec_packages = _spec_packages_module()
        for mutation in ("symlink", "non-regular", "oversized", "non-utf8"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                package = _write_package(stage)
                target = package / "spec.md"
                if mutation == "symlink":
                    source = stage.parent / "source.md"
                    source.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
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
            with mock.patch.object(
                spec_packages.os,
                "fstat",
                side_effect=(opened, changed),
            ), self.assertRaisesRegex(spec_packages.SpecPackageError, "changed"):
                spec_packages.load_spec_packages(stage, registry=registry)

    def test_directory_parent_swaps_and_final_file_symlink_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()

        for surface in ("stage", "package", "tasks", "contracts"):
            with self.subTest(surface=surface), tempfile.TemporaryDirectory() as directory:
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

                with mock.patch.object(
                    spec_packages.os,
                    "scandir",
                    side_effect=swap_on_scan,
                ), self.assertRaisesRegex(spec_packages.SpecPackageError, "changed|symlink"):
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

            with mock.patch.object(
                spec_packages.os,
                "stat",
                side_effect=replace_after_open,
            ), self.assertRaisesRegex(spec_packages.SpecPackageError, "changed|symlink"):
                spec_packages.load_spec_packages(stage)

    def test_enumeration_and_aggregate_budgets_fail_before_unbounded_loading(self) -> None:
        spec_packages = _spec_packages_module()
        registry = spec_packages.load_registry()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True)
            package.joinpath("README.md").write_text("# fixture\n", encoding="utf-8")
            with mock.patch.object(spec_packages, "MAX_PACKAGE_ENTRIES", 2), self.assertRaisesRegex(
                spec_packages.SpecPackageError, "too many entries"
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            _write_package(stage, number="0001")
            _write_package(stage, number="0002")
            with mock.patch.object(spec_packages, "MAX_TOTAL_ENTRIES", 3), self.assertRaisesRegex(
                spec_packages.SpecPackageError, "aggregate entry"
            ):
                spec_packages.load_spec_packages(stage, registry=registry)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            first = _write_package(stage, number="0001") / "spec.md"
            second = _write_package(stage, number="0002") / "spec.md"
            aggregate_limit = first.stat().st_size + second.stat().st_size - 1
            self.assertGreater(aggregate_limit, max(first.stat().st_size, second.stat().st_size))
            with mock.patch.object(
                spec_packages,
                "MAX_TOTAL_FILE_BYTES",
                aggregate_limit,
            ), self.assertRaisesRegex(spec_packages.SpecPackageError, "aggregate byte"):
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
                _document_text("task", "task-0001-0001", ("SPEC-0001",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "task.*path"):
                spec_packages.load_spec_packages(stage)

        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, task=True)
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                _document_text("task", "task-0002-0001", ("SPEC-0001",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "task-0001-0001"):
                spec_packages.load_spec_packages(stage)

    def test_dangling_plan_and_task_parents_fail_closed(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/03.specs"
            package = _write_package(stage, plan=True)
            package.joinpath("plan.md").write_text(
                _document_text("plan", "plan-0001", ("SPEC-9999",)),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(spec_packages.SpecPackageError, "plan.*parent"):
                spec_packages.load_spec_packages(stage)

        for parents in (("SPEC-0001", "plan-0001"), ("SPEC-0001", "task-0001-9999")):
            with self.subTest(parents=parents), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(stage, task=True, task_parent_ids=parents)
                with self.assertRaisesRegex(spec_packages.SpecPackageError, "parent"):
                    spec_packages.load_spec_packages(stage)

    def test_lifecycle_rejects_illegal_evidence_and_living_spec_deletion(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            package = _write_package(before_stage, plan=True, task=True)
            package.joinpath("plan.md").write_text(
                _document_text(
                    "plan",
                    "plan-0001",
                    ("SPEC-0001",),
                    status="completed",
                ),
                encoding="utf-8",
            )
            task = package / "tasks/tsk-0001-implement.md"
            task.write_text(
                _document_text(
                    "task",
                    "task-0001-0001",
                    ("SPEC-0001", "plan-0001"),
                    status="completed",
                ),
                encoding="utf-8",
            )
            _write_package(after_stage)
            before = spec_packages.load_spec_packages(before_stage)
            after = spec_packages.load_spec_packages(after_stage)
            findings = spec_packages.validate_spec_package_lifecycle(before, after)
            self.assertEqual(
                {"execution-evidence-recovery-missing"},
                {finding.code for finding in findings},
            )

            recovered = spec_packages.validate_spec_package_lifecycle(
                before,
                after,
                recovery_commits={
                    pathlib.PurePosixPath(
                        "docs/03.specs/0001-example/plan.md"
                    ): "a" * 40,
                    pathlib.PurePosixPath(
                        "docs/03.specs/0001-example/tasks/tsk-0001-implement.md"
                    ): "b" * 40,
                },
            )
            self.assertFalse(recovered)

            empty_stage = root / "empty/docs/03.specs"
            empty_stage.mkdir(parents=True)
            empty = spec_packages.load_spec_packages(empty_stage)
            spec_findings = spec_packages.validate_spec_package_lifecycle(before, empty)
            self.assertIn(
                "living-spec-deletion-forbidden",
                {finding.code for finding in spec_findings},
            )
            migration_findings = spec_packages.validate_spec_package_lifecycle(
                before,
                empty,
                one_time_package_ids=frozenset({"SPEC-0001"}),
            )
            self.assertIn(
                "one-time-package-recovery-missing",
                {finding.code for finding in migration_findings},
            )

    def test_one_time_exception_requires_whole_package_retirement_proof(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            before_stage = root / "before/docs/03.specs"
            after_stage = root / "after/docs/03.specs"
            _write_package(before_stage, plan=True, task=True)
            _write_package(after_stage)
            before = spec_packages.load_spec_packages(before_stage)
            after = spec_packages.load_spec_packages(after_stage)
            partial = spec_packages.validate_spec_package_lifecycle(
                before,
                after,
                one_time_package_ids=frozenset({"SPEC-0001"}),
            )
            self.assertEqual(
                {
                    "docs/03.specs/0001-example/plan.md",
                    "docs/03.specs/0001-example/tasks/tsk-0001-implement.md",
                },
                {
                    finding.path
                    for finding in partial
                    if finding.code == "execution-evidence-recovery-missing"
                },
            )

            empty_stage = root / "empty/docs/03.specs"
            empty_stage.mkdir(parents=True)
            retired = spec_packages.validate_spec_package_lifecycle(
                before,
                spec_packages.load_spec_packages(empty_stage),
                recovery_commits={
                    pathlib.PurePosixPath(
                        "docs/03.specs/0001-example/spec.md"
                    ): "c" * 40,
                },
                one_time_package_ids=frozenset({"SPEC-0001"}),
            )
            self.assertFalse(retired)

    def test_public_repository_validator_enforces_snapshot_lifecycle(self) -> None:
        spec_packages = _spec_packages_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(
                ("git", "init", "--quiet"),
                cwd=root,
                check=True,
            )
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
            current = spec_packages.load_spec_packages(stage)
            with mock.patch.object(
                spec_packages,
                "_read_migration_authority",
                return_value=({}, {}, frozenset()),
            ):
                findings = spec_packages.validate_repository_spec_package_lifecycle(
                    root,
                    current,
                    base_ref="HEAD",
                )
            self.assertIn(
                "execution-evidence-recovery-missing",
                {finding.code for finding in findings},
            )

    def test_bounded_git_streams_both_pipes_and_reaps_on_failure(self) -> None:
        spec_packages = _spec_packages_module()
        real_popen = subprocess.Popen

        def invoke(script: str, *, byte_limit: int, timeout: float = 1.0) -> tuple[bytes, list]:
            processes = []

            def spawn(_command, **kwargs):
                process = real_popen([sys.executable, "-c", script], **kwargs)
                processes.append(process)
                return process

            with mock.patch.object(spec_packages.subprocess, "Popen", side_effect=spawn), mock.patch.object(
                spec_packages,
                "GIT_COMMAND_TIMEOUT_SECONDS",
                timeout,
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

                with mock.patch.object(
                    spec_packages.subprocess,
                    "Popen",
                    side_effect=spawn,
                ), mock.patch.object(
                    spec_packages,
                    "GIT_COMMAND_TIMEOUT_SECONDS",
                    1.0,
                ), self.assertRaisesRegex(spec_packages.SpecPackageError, "byte budget"):
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
        with mock.patch.object(
            spec_packages.subprocess,
            "Popen",
            side_effect=spawn_timeout,
        ), mock.patch.object(
            spec_packages,
            "GIT_COMMAND_TIMEOUT_SECONDS",
            0.05,
        ), self.assertRaisesRegex(spec_packages.SpecPackageError, "deadline"):
            spec_packages._bounded_git(ROOT, "fixture", byte_limit=64)
        self.assertLess(time.monotonic() - started, 2.0)
        self.assertIsNotNone(timed_processes[0].poll())

    def test_base_snapshot_rejects_file_at_limit_plus_one(self) -> None:
        spec_packages = _spec_packages_module()
        commit = b"a" * 40 + b"\n"
        tree = (
            b"100644 blob "
            + b"b" * 40
            + b"\tdocs/03.specs/0001-example/spec.md\0"
        )
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
                source_to_final={},
            )
        self.assertEqual(1, len(packages))

        with mock.patch.object(
            spec_packages,
            "_bounded_git",
            side_effect=(commit, tree, exact + b"\n"),
        ), self.assertRaisesRegex(spec_packages.SpecPackageError, "byte limit"):
            spec_packages._load_base_spec_packages(
                ROOT,
                base_ref="HEAD",
                source_to_final={},
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
        self.assertTrue(all(not package.path.name.startswith("spec-") for package in packages))
        self.assertFalse((ROOT / "docs/04.execution").exists())
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/design.md")))
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/tests.md")))
        self.assertFalse(tuple((ROOT / "docs/03.specs").glob("*/task.md")))
        self.assertFalse((ROOT / "DESIGN.md").exists())

    def test_active_route_authority_uses_only_canonical_spec_execution_paths(self) -> None:
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
                    violations.append(
                        f"{path.relative_to(ROOT)}:{match.group(0)}"
                    )
        metadata_sources = (
            ROOT / "scripts/lib/document_governance/metadata_validator.py",
            *sorted(
                (ROOT / "scripts/lib/document_governance/metadata").glob("*.py")
            ),
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
