from __future__ import annotations

import dataclasses
import io
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_adapters as adapters
from scripts.lib.gate import ci_gate_contract as contract
from scripts.validation import ci_gate_runner as runner

ROOT = pathlib.Path(__file__).resolve().parents[2]


REAL_SUBPROCESS_RUN = subprocess.run
REAL_SHUTIL_RMTREE = shutil.rmtree


def _invocation(
    gate_id: str,
    entrypoint: str,
    *,
    cwd: str = ".",
    allowed_env_keys: tuple[str, ...] = (),
) -> runner.GateInvocation:
    return runner.GateInvocation(
        gate_id=gate_id,
        entrypoint=pathlib.PurePosixPath(entrypoint),
        argv=(),
        cwd=pathlib.PurePosixPath(cwd),
        allowed_env_keys=allowed_env_keys,
        timeout_seconds=60,
    )


def _real_public_plan(
    selected_suites: tuple[str, ...],
    environ: dict[str, str],
) -> tuple[
    runner.GateInvocation,
    ...,
]:
    root = pathlib.Path(__file__).resolve().parents[2]
    document = contract.load_contract_document(root)
    gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
    public = contract.parse_public_gate_contract(document)
    return runner.build_public_validation_plan(
        gates,
        contract.public_root_gate_ids(public, selected_suites),
        public,
        selected_suites,
        runner.derive_execution_context(environ),
    )


def build_public_plan(
    profile: str,
    context: runner.ExecutionContext,
    changed_paths: tuple[str, ...] = (),
) -> tuple[runner.GateInvocation, ...]:
    root = pathlib.Path(__file__).resolve().parents[2]
    document = contract.load_contract_document(root)
    gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
    public = contract.parse_public_gate_contract(document)
    selected = contract.select_public_suites(public, profile, changed_paths)
    return runner.build_public_validation_plan(
        gates,
        contract.public_root_gate_ids(
            public,
            selected,
            changed_paths=changed_paths if profile == "changed" else None,
        ),
        public,
        selected,
        context,
        profile=profile,
    )


def _explained_identity(line: str) -> tuple[str, str, tuple[str, ...]]:
    _, entrypoint, gate_id, argv = line.split("\t")
    return gate_id, entrypoint, tuple(json.loads(argv))


def _invocation_identity(
    invocation: runner.GateInvocation,
) -> tuple[str, str, tuple[str, ...]]:
    return invocation.gate_id, invocation.entrypoint.as_posix(), invocation.argv


def _rebind_diff_gate(
    gates: contract.GateRegistry,
    entrypoint: pathlib.PurePosixPath,
    argv: tuple[str, ...] = (),
) -> contract.GateRegistry:
    return dataclasses.replace(
        gates,
        nodes=tuple(
            dataclasses.replace(node, entrypoint=entrypoint, argv=argv)
            if node.gate_id == "leaf.local-diff-hygiene"
            else node
            for node in gates.nodes
        ),
    )


class CiGateRunnerContractTests(unittest.TestCase):
    @staticmethod
    def _git(root: pathlib.Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )

    def _changed_path_repo(self, directory: pathlib.Path) -> pathlib.Path:
        repo = directory / "repo"
        repo.mkdir()
        self._git(repo, "init", "-q")
        self._git(repo, "config", "user.email", "t@example.com")
        self._git(repo, "config", "user.name", "Test")
        for relative in (
            "modified.txt",
            "deleted.txt",
            "rename-old.txt",
            "space name.txt",
        ):
            (repo / relative).write_text("before\n", encoding="utf-8")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-qm", "seed")
        return repo

    def test_local_changed_paths_cover_real_git_snapshots(self) -> None:
        def modify(repo: pathlib.Path) -> None:
            (repo / "modified.txt").write_text("after\n", encoding="utf-8")

        def stage(repo: pathlib.Path) -> None:
            modify(repo)
            self._git(repo, "add", "modified.txt")

        def partially_stage(repo: pathlib.Path) -> None:
            stage(repo)
            (repo / "modified.txt").write_text("after again\n", encoding="utf-8")

        def add(repo: pathlib.Path) -> None:
            (repo / "added.txt").write_text("added\n", encoding="utf-8")

        def stage_add(repo: pathlib.Path) -> None:
            add(repo)
            self._git(repo, "add", "added.txt")

        def delete(repo: pathlib.Path) -> None:
            (repo / "deleted.txt").unlink()

        def stage_delete(repo: pathlib.Path) -> None:
            delete(repo)
            self._git(repo, "add", "deleted.txt")

        def rename(repo: pathlib.Path) -> None:
            target = repo / "scripts/rename-new.txt"
            target.parent.mkdir()
            (repo / "rename-old.txt").rename(target)

        def stage_rename(repo: pathlib.Path) -> None:
            target = repo / "scripts/rename-new.txt"
            target.parent.mkdir()
            self._git(repo, "mv", "rename-old.txt", target.relative_to(repo).as_posix())

        def modify_space(repo: pathlib.Path) -> None:
            (repo / "space name.txt").write_text("after\n", encoding="utf-8")

        def change_type(repo: pathlib.Path) -> None:
            (repo / "modified.txt").unlink()
            (repo / "modified.txt").symlink_to("deleted.txt")

        def stage_type(repo: pathlib.Path) -> None:
            change_type(repo)
            self._git(repo, "add", "modified.txt")

        cases = (
            ("unstaged", modify, ("modified.txt",)),
            ("staged", stage, ("modified.txt",)),
            ("partially-staged", partially_stage, ("modified.txt",)),
            ("unstaged-add", add, ("added.txt",)),
            ("staged-add", stage_add, ("added.txt",)),
            ("unstaged-delete", delete, ("deleted.txt",)),
            ("staged-delete", stage_delete, ("deleted.txt",)),
            ("unstaged-rename", rename, ("rename-old.txt", "scripts/rename-new.txt")),
            (
                "staged-rename",
                stage_rename,
                ("rename-old.txt", "scripts/rename-new.txt"),
            ),
            ("space", modify_space, ("space name.txt",)),
            ("unstaged-type", change_type, ("modified.txt",)),
            ("staged-type", stage_type, ("modified.txt",)),
        )
        for name, mutate, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                repo = self._changed_path_repo(pathlib.Path(directory))
                mutate(repo)
                self.assertEqual(
                    expected,
                    runner.collect_changed_paths(repo, {"PATH": os.defpath}),
                )

        with tempfile.TemporaryDirectory() as directory:
            repo = self._changed_path_repo(pathlib.Path(directory))
            self.assertEqual(
                (), runner.collect_changed_paths(repo, {"PATH": os.defpath})
            )

    def test_initial_repository_collects_staged_and_untracked_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = pathlib.Path(directory)
            self._git(repo, "init", "-q")
            (repo / "staged.txt").write_text("staged\n", encoding="utf-8")
            (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            self._git(repo, "add", "staged.txt")
            self.assertEqual(
                ("staged.txt", "untracked.txt"),
                runner.collect_changed_paths(repo, {"PATH": os.defpath}),
            )
        with tempfile.TemporaryDirectory() as directory:
            repo = self._changed_path_repo(pathlib.Path(directory))
            (repo / "modified.txt").write_text("second commit\n", encoding="utf-8")
            self._git(repo, "add", "modified.txt")
            self._git(repo, "commit", "-qm", "second")
            self.assertEqual(
                (
                    "deleted.txt",
                    "modified.txt",
                    "rename-old.txt",
                    "space name.txt",
                ),
                runner.collect_changed_paths(
                    repo,
                    {
                        "EVENT_NAME": "push",
                        "PUSH_BEFORE_SHA": "0" * 40,
                        "PATH": os.defpath,
                    },
                ),
            )

    def test_changed_name_status_parser_fails_closed(self) -> None:
        for label, output in (
            ("missing-rename-target", b"R100\0old.txt\0"),
            ("unknown-status", b"X\0path.txt\0"),
            ("unmerged-status", b"U\0path.txt\0"),
            ("invalid-utf8", b"M\0\xff\0"),
            ("unterminated", b"M\0path.txt"),
        ):
            result = subprocess.CompletedProcess(["git"], 0, stdout=output)
            with (
                self.subTest(label=label),
                mock.patch.object(runner.subprocess, "run", return_value=result),
                self.assertRaises(contract.GateContractError) as raised,
            ):
                runner.collect_changed_paths(ROOT, {"PATH": os.defpath})
            self.assertEqual("ci-gate-changed-paths", raised.exception.code)

    def test_hosted_comparison_includes_both_rename_paths_and_requires_base(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = self._changed_path_repo(pathlib.Path(directory))
            base = self._git(repo, "rev-parse", "HEAD").stdout.strip()
            target = repo / "scripts/rename-new.txt"
            target.parent.mkdir()
            self._git(repo, "mv", "rename-old.txt", target.relative_to(repo).as_posix())
            self._git(repo, "commit", "-qm", "rename")
            head = self._git(repo, "rev-parse", "HEAD").stdout.strip()
            for event, key in (
                ("pull_request", "PR_BASE_SHA"),
                ("push", "PUSH_BEFORE_SHA"),
            ):
                with self.subTest(event=event):
                    environment = {"EVENT_NAME": event, key: base, "PATH": os.defpath}
                    if event == "pull_request":
                        environment["PR_HEAD_SHA"] = head
                    self.assertEqual(
                        ("rename-old.txt", "scripts/rename-new.txt"),
                        runner.collect_changed_paths(repo, environment),
                    )
            with self.assertRaises(contract.GateContractError) as missing:
                runner.collect_changed_paths(
                    repo,
                    {
                        "EVENT_NAME": "pull_request",
                        "PR_BASE_SHA": "f" * 40,
                        "PR_HEAD_SHA": head,
                        "PATH": os.defpath,
                    },
                )
            self.assertEqual("ci-gate-changed-paths", missing.exception.code)

    def test_shallow_hosted_comparison_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base_dir = pathlib.Path(directory)
            source = self._changed_path_repo(base_dir)
            missing_base = self._git(source, "rev-parse", "HEAD").stdout.strip()
            (source / "modified.txt").write_text("second\n", encoding="utf-8")
            self._git(source, "add", "modified.txt")
            self._git(source, "commit", "-qm", "second")
            shallow = base_dir / "shallow"
            subprocess.run(
                ["git", "clone", "-q", "--depth", "1", source.as_uri(), str(shallow)],
                check=True,
            )
            with self.assertRaises(contract.GateContractError) as raised:
                shallow_head = self._git(shallow, "rev-parse", "HEAD").stdout.strip()
                runner.collect_changed_paths(
                    shallow,
                    {
                        "EVENT_NAME": "pull_request",
                        "PR_BASE_SHA": missing_base,
                        "PR_HEAD_SHA": shallow_head,
                        "PATH": os.defpath,
                    },
                )
            self.assertEqual("ci-gate-changed-paths", raised.exception.code)

    def test_automatic_pre_commit_sees_index_content_and_untracked_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base_dir = pathlib.Path(directory)
            repo = self._changed_path_repo(base_dir)
            probe = repo / "probe.py"
            probe.write_text(
                "import os, pathlib, sys\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                "from scripts.validation import ci_gate_runner as runner\n"
                "print('OBSERVED=' + '|'.join(runner.collect_changed_paths("
                "pathlib.Path.cwd(), os.environ)))\n"
                "print('BYTES=' + pathlib.Path('modified.txt').read_text().strip())\n",
                encoding="utf-8",
            )
            (repo / ".pre-commit-config.yaml").write_text(
                "repos:\n"
                "  - repo: local\n"
                "    hooks:\n"
                "      - id: index-snapshot\n"
                "        name: index snapshot\n"
                "        entry: python3 probe.py\n"
                "        language: system\n"
                "        verbose: true\n"
                "        files: ^.*$\n"
                "        pass_filenames: false\n",
                encoding="utf-8",
            )
            self._git(repo, "add", "probe.py", ".pre-commit-config.yaml")
            self._git(repo, "commit", "-qm", "add probe")
            (repo / "modified.txt").write_text("staged\n", encoding="utf-8")
            self._git(repo, "add", "modified.txt")
            (repo / "modified.txt").write_text("unstaged remainder\n", encoding="utf-8")
            (repo / "space name.txt").write_text("unstaged only\n", encoding="utf-8")
            (repo / "untracked.txt").write_text("visible\n", encoding="utf-8")
            hook = repo / ".git/hooks/pre-commit"
            hook.write_text(
                "#!/bin/sh\nexec pre-commit hook-impl --config=.pre-commit-config.yaml "
                '--hook-type=pre-commit --hook-dir=.git/hooks -- "$@"\n',
                encoding="utf-8",
            )
            hook.chmod(0o755)
            environment = dict(os.environ)
            environment["PRE_COMMIT_HOME"] = str(base_dir / "pre-commit-cache")
            result = subprocess.run(
                ["git", "-c", "core.hooksPath=.git/hooks", "commit", "-m", "snapshot"],
                cwd=repo,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            output = result.stdout + result.stderr
            self.assertIn("OBSERVED=modified.txt|untracked.txt", output)
            self.assertIn("BYTES=staged", output)
            self.assertNotIn("space name.txt", output)
            self.assertEqual(
                "unstaged remainder\n", (repo / "modified.txt").read_text()
            )

    def test_changed_document_plan_omits_irrelevant_expensive_roots(self) -> None:
        document = contract.load_contract_document(ROOT)
        registry = contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        public = contract.parse_public_gate_contract(document)
        optional = {
            "ci.dependency-vulnerability-audit",
            "ci.frontend-quality",
            "ci.storybook-coverage",
            "ci.zizmor",
            "leaf.document-governance-library-regressions",
            "leaf.local-document-corpus-lifecycle-tests",
            "leaf.local-document-metadata-tests",
            "local.workflow-harness",
        }
        paths = ("docs/03.specs/0173-governance-qa-surface-convergence/plan.md",)
        selected = contract.select_public_suites(public, "changed", paths)
        roots = contract.public_root_gate_ids(public, selected, changed_paths=paths)
        self.assertFalse(optional & set(roots))
        plan = runner.build_public_validation_plan(
            registry,
            roots,
            public,
            selected,
            runner.ExecutionContext.PULL_REQUEST,
        )
        gate_ids = {invocation.gate_id for invocation in plan}
        self.assertIn("leaf.changed-style", gate_ids)
        self.assertIn("leaf.commit-message-contract", gate_ids)
        self.assertNotIn("leaf.dependency-vulnerability-audit", gate_ids)
        self.assertFalse(
            {
                "leaf.frontend-lint",
                "leaf.frontend-typecheck",
                "leaf.frontend-build",
                "leaf.frontend-quality",
                "leaf.storybook-coverage",
            }
            & gate_ids
        )

    def test_document_only_plan_keeps_content_and_common_checks_only(
        self,
    ) -> None:
        plan = build_public_plan(
            "changed",
            runner.ExecutionContext.PULL_REQUEST,
            ("docs/03.specs/0200-path-aware-pr-regressions/spec.md",),
        )
        ids = {item.gate_id for item in plan}
        self.assertEqual(
            {
                "leaf.repo-metadata-base",
                "leaf.repo-document-metadata",
                "leaf.local-document-corpus-lifecycle",
                "leaf.local-diff-hygiene",
                "leaf.changed-style",
                "leaf.commit-message-contract",
            },
            ids,
        )
        self.assertFalse(
            {
                "leaf.local-document-corpus-lifecycle-tests",
                "leaf.local-document-metadata-tests",
                "leaf.document-governance-library-regressions",
                "leaf.operations-catalog",
            }
            & ids
        )

    def test_operations_doc_plan_keeps_catalog(self) -> None:
        paths = ("docs/05.operations/guides/0001-example.md",)
        plan = build_public_plan(
            "changed",
            runner.ExecutionContext.PULL_REQUEST,
            paths,
        )
        ids = {item.gate_id for item in plan}
        self.assertEqual(
            {
                "leaf.repo-metadata-base",
                "leaf.repo-document-metadata",
                "leaf.local-document-corpus-lifecycle",
                "leaf.operations-catalog",
                "leaf.local-diff-hygiene",
                "leaf.changed-style",
                "leaf.commit-message-contract",
            },
            ids,
        )
        self.assertNotIn("leaf.local-document-metadata-tests", ids)
        self.assertNotIn("leaf.document-governance-library-regressions", ids)
        self.assertFalse(
            {
                "leaf.compose-validation",
                "leaf.compose-baseline-regressions",
                "leaf.infrastructure-hardening",
                "leaf.template-security-baseline",
                "leaf.quickwin-baseline",
            }
            & ids
        )
        self.assertEqual(
            runner.SelectedPrerequisites(node=False, docker=False),
            runner.selected_prerequisites(plan, paths),
        )

    def test_document_links_are_local_only_for_changed_and_full_plans(self) -> None:
        paths = ("docs/03.specs/0211-qa-delivery-rationalization/spec.md",)
        local_changed = build_public_plan(
            "changed", runner.ExecutionContext.LOCAL, paths
        )
        remote_changed = build_public_plan(
            "changed", runner.ExecutionContext.PULL_REQUEST, paths
        )
        local_full = build_public_plan("full", runner.ExecutionContext.LOCAL)
        hosted_full = build_public_plan(
            "full", runner.ExecutionContext.WORKFLOW_DISPATCH
        )

        self.assertIn(
            "leaf.docs-traceability", {item.gate_id for item in local_changed}
        )
        self.assertIn("leaf.docs-traceability", {item.gate_id for item in local_full})
        self.assertNotIn(
            "leaf.docs-traceability", {item.gate_id for item in remote_changed}
        )
        self.assertNotIn(
            "leaf.docs-traceability", {item.gate_id for item in hosted_full}
        )

    def test_implementation_regressions_are_local_only_with_remote_owners(
        self,
    ) -> None:
        cases = {
            "scripts/lib/document_governance/spec_packages.py": (
                "leaf.document-governance-library-regressions",
                "leaf.repo-document-metadata",
            ),
            ".github/workflow-contract.yml": (
                "leaf.workflow-contract-regressions",
                "leaf.workflow-contract",
            ),
            "scripts/hooks/hook_rules.py": (
                "leaf.local-hook-rule-tests",
                "leaf.local-agent-governance-contract",
            ),
            "scripts/validation/check-script-manifest.py": (
                "leaf.repository-integrity-regressions",
                "leaf.local-script-manifest",
            ),
        }
        for path, (local_only, remote_owner) in cases.items():
            with self.subTest(path=path):
                local_ids = {
                    item.gate_id
                    for item in build_public_plan(
                        "changed", runner.ExecutionContext.LOCAL, (path,)
                    )
                }
                remote_ids = {
                    item.gate_id
                    for item in build_public_plan(
                        "changed", runner.ExecutionContext.PULL_REQUEST, (path,)
                    )
                }
                self.assertIn(local_only, local_ids)
                self.assertNotIn(local_only, remote_ids)
                self.assertIn(remote_owner, remote_ids)

    def test_local_only_plan_intersects_normal_changed_selection(self) -> None:
        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document)

        document_plan = build_public_plan(
            "changed",
            runner.ExecutionContext.LOCAL,
            ("docs/03.specs/0211-qa-scope-and-delivery-rationalization/spec.md",),
        )
        self.assertEqual(
            ("leaf.docs-traceability",),
            tuple(
                invocation.gate_id
                for invocation in runner.build_local_only_validation_plan(
                    document_plan,
                    public,
                    runner.ExecutionContext.LOCAL,
                )
            ),
        )

        implementation_plan = build_public_plan(
            "changed",
            runner.ExecutionContext.LOCAL,
            (".github/workflow-contract.yml",),
        )
        local_only_ids = {
            invocation.gate_id
            for invocation in runner.build_local_only_validation_plan(
                implementation_plan,
                public,
                runner.ExecutionContext.LOCAL,
            )
        }
        self.assertIn("leaf.workflow-contract-regressions", local_only_ids)
        self.assertNotIn("leaf.workflow-contract", local_only_ids)
        self.assertNotIn("leaf.changed-style", local_only_ids)
        self.assertNotIn("leaf.commit-message-contract", local_only_ids)

    def test_local_only_cli_rejects_authenticated_hosted_context_before_execution(
        self,
    ) -> None:
        environment = {
            "HYHOME_CI_GATE_ROOT": str(ROOT),
            "PATH": os.defpath,
            "GITHUB_ACTIONS": "true",
            "EVENT_NAME": "pull_request",
            "PR_BASE_SHA": "a" * 40,
            "PR_HEAD_SHA": "b" * 40,
        }
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(runner, "collect_changed_paths", return_value=()),
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(
                1,
                runner.main(["--profile", "changed", "--local-only"]),
            )
        execute.assert_not_called()
        self.assertIn("ci-gate-local-only-context", stderr.getvalue())

    def test_local_only_cli_executes_and_explains_only_the_selected_local_slice(
        self,
    ) -> None:
        environment = {
            "HYHOME_CI_GATE_ROOT": str(ROOT),
            "PATH": os.defpath,
        }
        selected_plans: list[tuple[runner.GateInvocation, ...]] = []

        def capture_execution(
            root: pathlib.Path,
            plan: tuple[runner.GateInvocation, ...],
            environ: dict[str, str],
        ) -> int:
            self.assertEqual(ROOT, root)
            self.assertEqual(os.defpath, environ["PATH"])
            selected_plans.append(plan)
            return 0

        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(
                runner,
                "collect_changed_paths",
                return_value=(".github/workflow-contract.yml",),
            ),
            mock.patch.object(
                runner,
                "execute_execution_plan",
                side_effect=capture_execution,
            ),
        ):
            self.assertEqual(
                0,
                runner.main(["--profile", "changed", "--local-only"]),
            )

        self.assertEqual(1, len(selected_plans))
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        selected_ids = {invocation.gate_id for invocation in selected_plans[0]}
        self.assertLessEqual(selected_ids, set(public.local_only_gate_ids))
        self.assertIn("leaf.workflow-contract-regressions", selected_ids)
        self.assertNotIn("leaf.workflow-contract", selected_ids)

        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(
                runner,
                "collect_changed_paths",
                return_value=(".github/workflow-contract.yml",),
            ),
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
        ):
            self.assertEqual(
                0,
                runner.main(["--profile", "changed", "--local-only", "--explain"]),
            )
        execute.assert_not_called()
        lines = tuple(stdout.getvalue().splitlines())
        self.assertTrue(lines)
        self.assertTrue(all(line.startswith("local-only\t") for line in lines))
        self.assertTrue(
            any("leaf.workflow-contract-regressions" in line for line in lines)
        )

    def test_document_owner_changes_select_regressions(self) -> None:
        owners = (
            "scripts/lib/document_governance/metadata/reference.py",
            "scripts/validation/check-document-metadata.py",
            "tests/lib/document_governance/metadata/test_reference.py",
        )
        targets = {
            "leaf.local-document-metadata-tests",
            "leaf.document-governance-library-regressions",
        }
        for path in owners:
            with self.subTest(path=path):
                plan = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, (path,)
                )
                self.assertLessEqual(targets, {item.gate_id for item in plan})

    def test_gate_and_workflow_implementation_changes_omit_document_regressions(
        self,
    ) -> None:
        targets = {
            "leaf.local-document-metadata-tests",
            "leaf.document-governance-library-regressions",
        }
        for path in (
            ".github/workflow-contract.yml",
            "scripts/lib/gate/ci_gate_contract.py",
            "scripts/validation/ci_gate_runner.py",
            "tests/lib/gate/test_ci_gate_contract.py",
            "tests/validation/test_ci_gate_plan.py",
        ):
            with self.subTest(path=path):
                plan = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, (path,)
                )
                self.assertFalse(targets & {item.gate_id for item in plan})

    def test_release_owner_changes_select_release_regression_only_locally(self) -> None:
        release_inputs = (
            "scripts/operations/release.py",
            "tests/validation/test_release.py",
            ".github/workflows/generate-changelog.yml",
            ".cz.toml",
            "cliff.toml",
            "CHANGELOG.md",
        )
        for path in release_inputs:
            with self.subTest(path=path):
                hosted = build_public_plan(
                    "changed", runner.ExecutionContext.PULL_REQUEST, (path,)
                )
                local = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, (path,)
                )
                hosted_ids = {item.gate_id for item in hosted}
                local_ids = {item.gate_id for item in local}
                self.assertNotIn("leaf.release-regressions", hosted_ids)
                self.assertIn("leaf.release-regressions", local_ids)
                self.assertFalse(
                    {
                        "leaf.compose-validation",
                        "leaf.compose-baseline-regressions",
                        "leaf.infrastructure-hardening",
                        "leaf.template-security-baseline",
                        "leaf.quickwin-baseline",
                    }
                    & hosted_ids
                )
                self.assertFalse(runner.selected_prerequisites(hosted, (path,)).docker)

        ordinary_document = build_public_plan(
            "changed",
            runner.ExecutionContext.PULL_REQUEST,
            ("docs/03.specs/0211-qa-delivery-rationalization/spec.md",),
        )
        self.assertNotIn(
            "leaf.release-regressions",
            {item.gate_id for item in ordinary_document},
        )

    def test_changed_unit_owners_run_locally_while_conftest_corpus_stays_hosted(
        self,
    ) -> None:
        cases = {
            "tests/validation/test_compose_baseline_gates.py": (
                "leaf.compose-baseline-regressions",
                None,
            ),
            "tests/validation/test_supply_chain_wrapper.py": (
                "leaf.supply-chain-fixture-policy",
                None,
            ),
            "infra/11-quality/conftest/policy/compose.rego": (
                "leaf.conftest-policy-tests",
                "leaf.conftest-policy",
            ),
        }
        conftest_entrypoint = pathlib.PurePosixPath(
            "scripts/validation/check-conftest-policy.sh"
        )
        for path, (local_unit, hosted_corpus) in cases.items():
            with self.subTest(path=path):
                local = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, (path,)
                )
                hosted = build_public_plan(
                    "changed", runner.ExecutionContext.PULL_REQUEST, (path,)
                )
                local_ids = [item.gate_id for item in local]
                hosted_ids = [item.gate_id for item in hosted]
                self.assertEqual(1, local_ids.count(local_unit))
                self.assertNotIn(local_unit, hosted_ids)
                if hosted_corpus is not None:
                    self.assertEqual(1, hosted_ids.count(hosted_corpus))
                    self.assertEqual(
                        [
                            ("--mode", "corpus"),
                            ("--mode", "verify"),
                        ],
                        [
                            item.argv
                            for item in local
                            if item.entrypoint == conftest_entrypoint
                        ],
                    )
                    self.assertEqual(
                        [("--mode", "corpus")],
                        [
                            item.argv
                            for item in hosted
                            if item.entrypoint == conftest_entrypoint
                        ],
                    )
                    self.assertTrue(
                        runner.selected_prerequisites(local, (path,)).docker
                    )
                    self.assertTrue(
                        runner.selected_prerequisites(hosted, (path,)).docker
                    )

    def test_changed_implementation_owners_are_explicit_and_unknown_code_fails_closed(
        self,
    ) -> None:
        cases = {
            "scripts/hardening/check-all-hardening.sh": {
                "leaf.infrastructure-hardening"
            },
            "scripts/validation/check-template-security-baseline.sh": {
                "leaf.template-security-baseline"
            },
            "scripts/validation/check-quickwin-baseline.sh": {"leaf.quickwin-baseline"},
            "scripts/validation/check-supply-chain-policy.py": {
                "leaf.supply-chain-deterministic-policy"
            },
            "tests/validation/test_compose_baseline_gates.py": {
                "leaf.compose-baseline-regressions"
            },
            "scripts/lib/agent_governance/agent_governance_contract.py": {
                "leaf.local-agent-governance-contract"
            },
            "scripts/hooks/hook_rules.py": {"leaf.local-hook-rule-tests"},
            "scripts/operations/provider_surface_renderer.py": {
                "leaf.local-provider-surface-drift"
            },
            "scripts/operations/use-qa-ci-tools.sh": {
                "leaf.repo-contracts-control-plane-regressions"
            },
            "scripts/operations/sync-tech-stack-versions.sh": {
                "leaf.local-tech-stack-version-drift",
                "leaf.repository-integrity-regressions",
            },
            "scripts/validation/check-script-manifest.py": {
                "leaf.local-script-manifest",
                "leaf.repository-integrity-regressions",
            },
            "tests/validation/_script_manifest_support.py": {
                "leaf.local-script-manifest",
                "leaf.repository-integrity-regressions",
            },
        }
        for path, expected_gate_ids in cases.items():
            with self.subTest(path=path):
                local_plan = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, (path,)
                )
                remote_plan = build_public_plan(
                    "changed", runner.ExecutionContext.PULL_REQUEST, (path,)
                )
                local_ids = {item.gate_id for item in local_plan}
                remote_ids = {item.gate_id for item in remote_plan}
                self.assertLessEqual(expected_gate_ids, local_ids | remote_ids)
                if path == "scripts/operations/provider_surface_renderer.py":
                    self.assertNotIn("leaf.compose-validation", remote_ids)
                    self.assertNotIn("leaf.compose-baseline-regressions", remote_ids)
                    self.assertFalse(
                        runner.selected_prerequisites(remote_plan, (path,)).docker
                    )
                if path == "scripts/operations/use-qa-ci-tools.sh":
                    self.assertNotIn("leaf.compose-validation", remote_ids)
                    self.assertNotIn("leaf.compose-baseline-regressions", remote_ids)
                    self.assertFalse(
                        runner.selected_prerequisites(remote_plan, (path,)).docker
                    )

        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document)
        for path in (
            "scripts/future_domain/unmapped.py",
            "tests/validation/test_future_unmapped.py",
        ):
            with self.subTest(path=path):
                self.assertEqual(
                    public.suite_names,
                    contract.select_public_suites(public, "changed", (path,)),
                )

    def test_style_controller_inputs_select_their_harness_without_npm_audit(
        self,
    ) -> None:
        controller_inputs = (
            ".pre-commit-config.yaml",
            ".markdownlint-cli2.yaml",
            ".cz.toml",
            ".hadolint.yaml",
            ".shellcheckrc",
            ".yamllint",
            "ruff.toml",
            "scripts/requirements-pre-commit.txt",
            "scripts/requirements.txt",
            "tests/validation/test_agent_governance_ci_routing.py",
        )
        for path in controller_inputs:
            with self.subTest(path=path):
                ids = {
                    item.gate_id
                    for item in build_public_plan(
                        "changed", runner.ExecutionContext.LOCAL, (path,)
                    )
                }
                self.assertIn("leaf.ci-precommit-regressions", ids)
                self.assertIn("leaf.repo-contracts-control-plane-regressions", ids)
                if path.startswith("scripts/requirements"):
                    self.assertNotIn("leaf.dependency-vulnerability-audit", ids)

    def test_registered_test_sources_select_their_own_leaf(self) -> None:
        document = contract.load_contract_document(ROOT)
        registry = contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        expected_by_path: dict[str, set[str]] = {}
        for node in registry.nodes:
            if node.entrypoint is not None:
                entrypoint = node.entrypoint.as_posix()
                if entrypoint.startswith("tests/") and (ROOT / entrypoint).is_file():
                    expected_by_path.setdefault(entrypoint, set()).add(node.gate_id)
            if not node.argv or node.argv[0] != "run-unittest":
                continue
            for module in node.argv[1:]:
                if module.startswith("-"):
                    break
                source = f"{module.replace('.', '/')}.py"
                if (ROOT / source).is_file():
                    expected_by_path.setdefault(source, set()).add(node.gate_id)

        for path, expected_gate_ids in sorted(expected_by_path.items()):
            with self.subTest(path=path):
                actual_gate_ids = {
                    item.gate_id
                    for item in build_public_plan(
                        "changed", runner.ExecutionContext.LOCAL, (path,)
                    )
                }
                self.assertTrue(
                    expected_gate_ids & actual_gate_ids,
                    f"{path} does not select one of {sorted(expected_gate_ids)}",
                )

    def test_prerequisites_follow_the_selected_plan(self) -> None:
        document = contract.load_contract_document(ROOT)
        registry = contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        public = contract.parse_public_gate_contract(document)

        def requirements(paths: tuple[str, ...]):
            selected = contract.select_public_suites(public, "changed", paths)
            plan = runner.build_public_validation_plan(
                registry,
                contract.public_root_gate_ids(public, selected, changed_paths=paths),
                public,
                selected,
                runner.ExecutionContext.PULL_REQUEST,
                root=ROOT,
            )
            return runner.selected_prerequisites(plan, paths)

        self.assertEqual(
            runner.SelectedPrerequisites(node=False, docker=False),
            requirements(("docs/03.specs/0211-example/spec.md",)),
        )
        self.assertEqual(
            runner.SelectedPrerequisites(node=False, docker=False),
            requirements(("README.md",)),
        )
        self.assertEqual(
            runner.SelectedPrerequisites(node=True, docker=False),
            requirements(("projects/storybook/nextjs/package.json",)),
        )
        self.assertEqual(
            runner.SelectedPrerequisites(node=False, docker=True),
            requirements(("infra/01-gateway/docker-compose.yml",)),
        )

    def test_mixed_unknown_path_keeps_document_regressions(self) -> None:
        targets = {
            "leaf.local-document-metadata-tests",
            "leaf.document-governance-library-regressions",
        }
        for paths in (
            (
                "docs/03.specs/0200-path-aware-pr-regressions/spec.md",
                "unknown-root.txt",
            ),
            ("unknown-root.txt",),
        ):
            with self.subTest(paths=paths):
                plan = build_public_plan(
                    "changed", runner.ExecutionContext.LOCAL, paths
                )
                self.assertLessEqual(targets, {item.gate_id for item in plan})

    def test_full_plan_keeps_document_regressions_once(self) -> None:
        plan = build_public_plan("full", runner.ExecutionContext.LOCAL)
        ids = [item.gate_id for item in plan]
        self.assertEqual(1, ids.count("leaf.local-document-metadata-tests"))
        self.assertEqual(1, ids.count("leaf.document-governance-library-regressions"))

    def test_relevant_frontend_failure_propagates(self) -> None:
        document = contract.load_contract_document(ROOT)
        registry = contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        public = contract.parse_public_gate_contract(document)
        paths = ("projects/storybook/nextjs/package-lock.json",)
        selected = contract.select_public_suites(public, "changed", paths)
        plan = runner.build_public_validation_plan(
            registry,
            contract.public_root_gate_ids(public, selected, changed_paths=paths),
            public,
            selected,
            runner.ExecutionContext.PULL_REQUEST,
        )
        self.assertIn("leaf.frontend-quality", {item.gate_id for item in plan})
        self.assertEqual(
            23,
            runner.execute_execution_plan(
                ROOT,
                plan,
                {"PATH": os.defpath},
                executor=lambda invocation: (
                    23 if invocation.gate_id == "leaf.frontend-quality" else 0
                ),
            ),
        )

    def test_every_public_plan_has_unique_canonical_invocations(self) -> None:
        cases = (
            ("changed", runner.ExecutionContext.LOCAL),
            ("changed", runner.ExecutionContext.PULL_REQUEST),
            ("full", runner.ExecutionContext.LOCAL),
            ("full", runner.ExecutionContext.PUSH),
            ("full", runner.ExecutionContext.WORKFLOW_DISPATCH),
        )
        for profile, context in cases:
            with self.subTest(profile=profile, context=context):
                plan = build_public_plan(profile, context)
                keys = [
                    runner.canonical_invocation_key(
                        ROOT, item, profile=profile, context=context
                    )
                    for item in plan
                ]
                self.assertEqual(len(keys), len(set(keys)))

    def test_required_runner_interfaces_are_exact(self) -> None:
        self.assertEqual(
            (
                "gate_id",
                "entrypoint",
                "argv",
                "cwd",
                "allowed_env_keys",
                "timeout_seconds",
            ),
            tuple(field.name for field in dataclasses.fields(runner.GateInvocation)),
        )

    def test_fake_executor_receives_each_leaf_once_in_order(self) -> None:
        seen: list[str] = []
        plan = (
            _invocation("setup.frontend", "scripts/validation/setup.py"),
            _invocation("leaf.repository", "scripts/validation/leaf.py"),
        )
        result = runner.execute_execution_plan(
            pathlib.Path.cwd(),
            plan,
            environ={"PATH": "/usr/bin", "GIT_DIR": "/tmp/hostile"},
            executor=lambda invocation: seen.append(invocation.gate_id) or 0,
        )
        self.assertEqual(0, result)
        self.assertEqual(["setup.frontend", "leaf.repository"], seen)

    def test_nonzero_fake_child_is_propagated_and_stops_plan(self) -> None:
        seen: list[str] = []

        def execute(invocation: runner.GateInvocation) -> int:
            seen.append(invocation.gate_id)
            return 17

        self.assertEqual(
            17,
            runner.execute_execution_plan(
                pathlib.Path.cwd(),
                (
                    _invocation("leaf.first", "first.py"),
                    _invocation("leaf.second", "second.py"),
                ),
                {"PATH": "/usr/bin"},
                executor=execute,
            ),
        )
        self.assertEqual(["leaf.first"], seen)

    def test_cli_rejects_obsolete_and_unknown_arguments(self) -> None:
        for arguments in (
            ["--profile", "full", "--gate", "leaf.repo-contracts"],
            ["--profile", "full", "--all"],
            ["--profile", "full", "--list"],
            ["--profile", "full", "--dry-run"],
        ):
            with self.subTest(arguments=arguments):
                stderr = io.StringIO()
                with mock.patch("sys.stderr", stderr):
                    result = runner.main(arguments)
                self.assertEqual(2, result)
                self.assertIn("ci-gate-cli-arguments", stderr.getvalue())
        stderr = io.StringIO()
        root = pathlib.Path(__file__).resolve().parents[2]
        with (
            mock.patch("sys.stderr", stderr),
            mock.patch.dict(
                os.environ, {"HYHOME_CI_GATE_ROOT": str(root)}, clear=False
            ),
        ):
            self.assertEqual(1, runner.main(["--profile", "local-harness"]))
        self.assertIn("ci-gate-profile-unknown", stderr.getvalue())

    def test_full_explain_is_deterministic_and_does_not_execute(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = build_public_plan("full", runner.ExecutionContext.LOCAL)
        expected = runner.render_public_validation_plan(
            plan,
            public,
            public.suite_names,
            runner.ExecutionContext.LOCAL,
            profile="full",
        )
        with (
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
            mock.patch.dict(
                os.environ, {"HYHOME_CI_GATE_ROOT": str(root)}, clear=False
            ),
        ):
            self.assertEqual(0, runner.main(["--profile", "full", "--explain"]))
        execute.assert_not_called()
        self.assertEqual(expected, tuple(stdout.getvalue().splitlines()))

    def test_requirements_reports_prerequisites_without_executing(self) -> None:
        environment = {
            "HYHOME_CI_GATE_ROOT": str(ROOT),
            "PATH": os.defpath,
            "GITHUB_ACTIONS": "true",
            "EVENT_NAME": "pull_request",
            "PR_BASE_SHA": "a" * 40,
            "PR_HEAD_SHA": "b" * 40,
        }
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(
                runner,
                "collect_changed_paths",
                return_value=("docs/03.specs/example.md",),
            ),
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
        ):
            self.assertEqual(
                0,
                runner.main(["--profile", "changed", "--requirements"]),
            )
        execute.assert_not_called()
        self.assertEqual("node=false\ndocker=false\n", stdout.getvalue())

    def test_standalone_validator_explain_and_fake_execution_have_exact_parity(
        self,
    ) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        selected = ("agent-governance",)
        plan = _real_public_plan(selected, {})
        explained = runner.render_public_validation_plan(
            plan, suites, selected, runner.ExecutionContext.LOCAL
        )
        explained_identities = tuple(_explained_identity(line) for line in explained)
        executed: list[runner.GateInvocation] = []
        result = runner.execute_execution_plan(
            root,
            plan,
            {"PATH": os.defpath},
            executor=lambda invocation: executed.append(invocation) or 0,
        )
        validator_gate_ids = {
            item.gate_id
            for item in suites.validators
            if item.suite in selected and "local" in item.contexts
        }
        executed_validators = tuple(
            _invocation_identity(invocation)
            for invocation in executed
            if invocation.gate_id in validator_gate_ids
        )
        self.assertEqual(0, result)
        self.assertEqual(explained_identities, executed_validators)
        self.assertEqual(
            1,
            sum(
                identity[1] == "scripts/validation/check-agent-governance-contract.py"
                for identity in executed_validators
            ),
        )

    def test_public_validator_missing_or_duplicate_invocation_fails_closed(
        self,
    ) -> None:
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        selected = suites.suite_names
        plan = _real_public_plan(selected, {})
        validator_path = next(
            item.entrypoint for item in suites.validators if "local" in item.contexts
        )
        invocation = next(item for item in plan if item.entrypoint == validator_path)
        mutations = (
            tuple(item for item in plan if item is not invocation),
            (*plan, invocation),
        )
        for mutated in mutations:
            with (
                self.subTest(size=len(mutated)),
                self.assertRaises(contract.GateContractError) as raised,
            ):
                runner.validate_public_execution_parity(
                    suites,
                    selected,
                    mutated,
                    runner.ExecutionContext.LOCAL,
                )
            self.assertEqual("ci-gate-public-execution-parity", raised.exception.code)
        duplicate_ownership = dataclasses.replace(
            suites,
            validators=(*suites.validators, suites.validators[0]),
        )
        with self.assertRaises(contract.GateContractError) as raised:
            runner.validate_public_execution_parity(
                duplicate_ownership,
                selected,
                plan,
                runner.ExecutionContext.LOCAL,
            )
        self.assertEqual("ci-gate-public-execution-parity", raised.exception.code)

    def test_real_execution_contexts_filter_only_their_admitted_leaves(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        public = contract.parse_public_gate_contract(document)
        suites = public
        changed = contract.select_public_suites(
            public, "changed", ("scripts/validation/example.py",)
        )
        full = contract.select_public_suites(public, "full", ())
        contexts = {
            "local-changed": (changed, {}),
            "local-full": (full, {}),
            "pull_request": (
                changed,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "pull_request",
                    "PR_BASE_SHA": "a" * 40,
                    "PR_HEAD_SHA": "b" * 40,
                },
            ),
            "push": (
                full,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "b" * 40,
                },
            ),
            "initial_push": (
                full,
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "0" * 40,
                },
            ),
            "workflow_dispatch": (
                full,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "workflow_dispatch",
                },
            ),
        }
        plans = {
            name: _real_public_plan(selected, environ)
            for name, (selected, environ) in contexts.items()
        }
        for name, (selected, environ) in contexts.items():
            context = runner.derive_execution_context(environ)
            explained = runner.render_public_validation_plan(
                plans[name], suites, selected, context
            )
            executed: list[runner.GateInvocation] = []
            self.assertEqual(
                0,
                runner.execute_execution_plan(
                    root,
                    plans[name],
                    {"PATH": os.defpath},
                    executor=lambda invocation: executed.append(invocation) or 0,
                ),
            )
            explained_identities = tuple(
                _explained_identity(line) for line in explained
            )
            # Count every validator gate, not only eligible gates: otherwise a
            # hidden ineligible invocation can evade this explain comparison.
            validator_gate_ids = {item.gate_id for item in suites.validators}
            self.assertEqual(
                explained_identities,
                tuple(
                    _invocation_identity(invocation)
                    for invocation in executed
                    if invocation.gate_id in validator_gate_ids
                ),
            )
        # Parsed for its assertion that the registry is well formed; the result
        # is unused because the checks below read the plans, not the registry.
        contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        for name in ("local-changed", "local-full"):
            gate_ids = {item.gate_id for item in plans[name]}
            with self.subTest(context=name):
                self.assertFalse(any(item.startswith("setup.") for item in gate_ids))
                self.assertFalse(gate_ids & runner._LOCAL_EXCLUDED_GATE_IDS)
                self.assertNotIn(
                    pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh"),
                    {item.entrypoint for item in plans[name]},
                )
        self.assertIn(
            "leaf.commit-message-contract",
            {item.gate_id for item in plans["pull_request"]},
        )
        for name in ("push", "initial_push", "workflow_dispatch"):
            self.assertNotIn(
                "leaf.commit-message-contract",
                {item.gate_id for item in plans[name]},
            )

    def test_local_full_plan_excludes_ci_only_hardening(self) -> None:
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(public.suite_names, {})
        self.assertNotIn(
            pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh"),
            {item.entrypoint for item in plan},
        )

    def test_base_plan_rejects_runtime_validator_rebind(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        public_paths = {item.entrypoint for item in public.validators}
        manifest = yaml.safe_load(
            (root / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        manual_paths = tuple(
            pathlib.PurePosixPath(row["path"])
            for row in manifest["files"]
            if row.get("kind") == "validator"
            and pathlib.PurePosixPath(row["path"]) not in public_paths
        )
        self.assertTrue(manual_paths)
        forbidden_paths = (
            *manual_paths,
            pathlib.PurePosixPath(
                "scripts/operations/rehearse-sample-service-delivery.sh"
            ),
            pathlib.PurePosixPath("scripts/validation/run-ci-gate.py"),
            pathlib.PurePosixPath("scripts/validation/run-ci-precommit.sh"),
            pathlib.PurePosixPath(
                "scripts/validation/run-agent-precommit-all-files.sh"
            ),
        )
        # These exact pairs are registered internal gate invocations rather than
        # validator rebinds, so the parity check admits them by design. The
        # staged authoring mode remains outside the public gate; only the exact
        # authenticated PR mode is reachable here.
        admitted_pairs = {
            (runner._INTERNAL_ADAPTER_PATH, ("check-diff-hygiene",)),
            (
                pathlib.PurePosixPath(
                    "scripts/validation/check-github-workflow-contract.py"
                ),
                (),
            ),
            (
                pathlib.PurePosixPath("scripts/validation/check-operations-catalog.py"),
                (),
            ),
            (
                pathlib.PurePosixPath("scripts/validation/check-script-manifest.py"),
                (),
            ),
            (
                pathlib.PurePosixPath("scripts/validation/check-storybook-contract.sh"),
                (),
            ),
            (
                pathlib.PurePosixPath("scripts/validation/run-ci-precommit.sh"),
                ("--mode", "pr-merge"),
            ),
        }
        candidate_argv = (
            (),
            ("check-diff-hygiene",),
            ("--mode", "pr-merge"),
            ("--mode", "local-staged"),
            ("--mode", "unknown"),
        )
        self.assertTrue(
            admitted_pairs.issubset(
                {(path, argv) for path in forbidden_paths for argv in candidate_argv}
                | {(runner._INTERNAL_ADAPTER_PATH, ("check-diff-hygiene",))}
            )
        )
        for context in runner.ExecutionContext:
            for path in forbidden_paths:
                for argv in candidate_argv:
                    if (path, argv) in admitted_pairs and (
                        path
                        != pathlib.PurePosixPath(
                            "scripts/validation/run-ci-precommit.sh"
                        )
                        or context is runner.ExecutionContext.PULL_REQUEST
                    ):
                        continue
                    with self.subTest(context=context, path=path, argv=argv):
                        with self.assertRaises(contract.GateContractError) as raised:
                            runner.build_public_validation_plan(
                                _rebind_diff_gate(gates, path, argv),
                                contract.public_root_gate_ids(
                                    public, public.suite_names
                                ),
                                public,
                                public.suite_names,
                                context,
                            )
                        self.assertEqual(
                            "ci-gate-public-execution-parity", raised.exception.code
                        )

    def test_internal_adapters_require_exact_argv_and_context(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        roots = contract.public_root_gate_ids(public, public.suite_names)
        for context, argv in (
            (runner.ExecutionContext.LOCAL, ("check-diff-hygiene", "--write")),
            (runner.ExecutionContext.LOCAL, ("run-unittest", "tests.lib.ops", "-v")),
            (runner.ExecutionContext.LOCAL, ("run-unittest", "-v")),
            (runner.ExecutionContext.LOCAL, ("run-zizmor-sarif",)),
            (runner.ExecutionContext.LOCAL, ("install-playwright",)),
            (runner.ExecutionContext.PUSH, ("check-commit-range",)),
            (runner.ExecutionContext.WORKFLOW_DISPATCH, ("verify-metadata-base",)),
            (runner.ExecutionContext.PULL_REQUEST, ("publish-qa-recommendations",)),
        ):
            with self.subTest(context=context, argv=argv):
                with self.assertRaises(contract.GateContractError) as raised:
                    runner.build_public_validation_plan(
                        _rebind_diff_gate(gates, runner._INTERNAL_ADAPTER_PATH, argv),
                        roots,
                        public,
                        public.suite_names,
                        context,
                    )
                self.assertEqual(
                    "ci-gate-public-execution-parity", raised.exception.code
                )
        duplicate_invocations = (
            (runner.ExecutionContext.PULL_REQUEST, ("check-commit-range",)),
            (runner.ExecutionContext.PUSH, ("run-zizmor-sarif",)),
            (runner.ExecutionContext.WORKFLOW_DISPATCH, ("install-playwright",)),
        )
        for context, argv in duplicate_invocations:
            with self.subTest(context=context, argv=argv):
                with self.assertRaises(contract.GateContractError) as raised:
                    runner.build_public_validation_plan(
                        _rebind_diff_gate(gates, runner._INTERNAL_ADAPTER_PATH, argv),
                        roots,
                        public,
                        public.suite_names,
                        context,
                    )
                self.assertEqual("ci-gate-invocation-duplicate", raised.exception.code)

        unique_argv = (
            "run-unittest",
            "tests.validation.test_ci_gate_runner.UniqueAdmissionProbe",
            "-v",
        )
        plan = runner.build_public_validation_plan(
            _rebind_diff_gate(gates, runner._INTERNAL_ADAPTER_PATH, unique_argv),
            roots,
            public,
            public.suite_names,
            runner.ExecutionContext.LOCAL,
        )
        self.assertIn(
            ("leaf.local-diff-hygiene", runner._INTERNAL_ADAPTER_PATH, unique_argv),
            {(item.gate_id, item.entrypoint, item.argv) for item in plan},
        )

    def test_final_parity_and_explain_reject_hidden_or_mutated_invocations(
        self,
    ) -> None:
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(suites.suite_names, {})
        forbidden = [
            _invocation("leaf.injected", item.entrypoint.as_posix())
            for item in suites.validators
            if "local" not in item.contexts
        ]
        forbidden.extend(
            dataclasses.replace(_invocation("leaf.injected", path), argv=argv)
            for path, argv in (
                ("scripts/validation/run-ci-gate.py", ("--profile", "full")),
                (
                    "scripts/operations/rehearse-sample-service-delivery.sh",
                    ("rehearse",),
                ),
                ("scripts/knowledge/generate-llm-wiki.py", ("--write",)),
                ("scripts/validation/report-provider-hook-parity.sh", ()),
                ("scripts/lib/gate/ci_gate_adapters.py", ("run-zizmor-sarif",)),
            )
        )
        for invocation in forbidden:
            for validate in (
                lambda candidate: runner.validate_public_execution_parity(
                    suites,
                    suites.suite_names,
                    candidate,
                    runner.ExecutionContext.LOCAL,
                ),
                lambda candidate: runner.render_public_validation_plan(
                    candidate,
                    suites,
                    suites.suite_names,
                    runner.ExecutionContext.LOCAL,
                ),
            ):
                with self.subTest(invocation=invocation, validate=validate):
                    with self.assertRaises(contract.GateContractError) as raised:
                        validate((*plan, invocation))
                    self.assertEqual(
                        "ci-gate-public-execution-parity", raised.exception.code
                    )

    def test_runtime_rebind_fails_before_cli_execution(self) -> None:
        document = contract.load_contract_document(pathlib.Path.cwd())
        for node in document["gate_nodes"]:
            if node["gate_id"] == "leaf.local-diff-hygiene":
                node["entrypoint"] = (
                    "scripts/operations/check-compose-core-readiness.sh"
                )
                node["argv"] = []
        with (
            mock.patch.object(runner, "load_contract_document", return_value=document),
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch.dict(os.environ, {"PATH": os.defpath}, clear=True),
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(1, runner.main(["--profile", "full"]))
        execute.assert_not_called()
        self.assertIn("ci-gate-public-execution-parity", stderr.getvalue())

    def test_malformed_execution_context_fails_closed(self) -> None:
        invalid = (
            {"EVENT_NAME": "push"},
            {"GITHUB_ACTIONS": "true", "EVENT_NAME": "schedule"},
            {"GITHUB_ACTIONS": "true", "EVENT_NAME": "push"},
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "a" * 40,
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "0" * 40,
                "PR_HEAD_SHA": "b" * 40,
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "a" * 40,
                "PR_HEAD_SHA": "a" * 40,
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "push",
                "PUSH_BEFORE_SHA": "invalid",
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "workflow_dispatch",
                "PUSH_BEFORE_SHA": "a" * 40,
            },
        )
        for environ in invalid:
            with (
                self.subTest(environ=environ),
                self.assertRaises(contract.GateContractError) as raised,
            ):
                runner.derive_execution_context(environ)
            self.assertEqual("ci-gate-execution-context", raised.exception.code)

    def test_metadata_base_policy_reaches_the_real_adapter(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        for label, environ, expected_base in (
            (
                "pull_request",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "pull_request",
                    "PR_BASE_SHA": "a" * 40,
                    "PR_HEAD_SHA": "b" * 40,
                    "PATH": os.defpath,
                },
                "a" * 40,
            ),
            (
                "push",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "b" * 40,
                    "PATH": os.defpath,
                },
                "b" * 40,
            ),
        ):
            with self.subTest(label=label):
                plan = _real_public_plan(
                    runner.public_suite_names(),
                    environ,
                )
                invocation = next(
                    item for item in plan if item.gate_id == "leaf.repo-metadata-base"
                )
                with tempfile.TemporaryDirectory(dir="/tmp") as directory:
                    child = runner._child_environment(
                        root,
                        pathlib.Path(directory),
                        invocation,
                        "python",
                        environ,
                        python_bootstrap=pathlib.Path(directory),
                    )
                self.assertEqual(expected_base, child["TEMPLATE_GATE_BASE"])
                for name in (
                    "check-document-metadata.py",
                    "check-document-corpus-lifecycle.py",
                ):
                    validator = next(
                        item for item in plan if item.entrypoint.name == name
                    )
                    with tempfile.TemporaryDirectory(dir="/tmp") as directory:
                        validator_child = runner._child_environment(
                            root,
                            pathlib.Path(directory),
                            validator,
                            "python",
                            environ,
                            python_bootstrap=pathlib.Path(directory),
                        )
                    self.assertEqual(
                        expected_base, validator_child["TEMPLATE_GATE_BASE"]
                    )
                with mock.patch.object(
                    adapters,
                    "_run_child",
                    return_value=subprocess.CompletedProcess((), 0),
                ) as run_child:
                    self.assertEqual(
                        0,
                        adapters.run_adapter(root, ("verify-metadata-base",), child),
                    )
                self.assertEqual(2, run_child.call_count)

        for label, environ in (
            (
                "initial_push",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "0" * 40,
                },
            ),
            (
                "workflow_dispatch",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "workflow_dispatch",
                },
            ),
        ):
            with self.subTest(label=label):
                plan = _real_public_plan(
                    runner.public_suite_names(),
                    environ,
                )
                self.assertNotIn(
                    "leaf.repo-metadata-base",
                    {item.gate_id for item in plan},
                )
                metadata = next(
                    item
                    for item in plan
                    if item.entrypoint
                    == pathlib.PurePosixPath(
                        "scripts/validation/check-document-metadata.py"
                    )
                )
                self.assertEqual(("--mode", "check-active"), metadata.argv)
                self.assertEqual((), metadata.allowed_env_keys)
