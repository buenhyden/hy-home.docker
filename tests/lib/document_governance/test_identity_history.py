from __future__ import annotations

import dataclasses
import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest
from types import MappingProxyType
from unittest import mock

from scripts.lib.document_governance import identity_history
from scripts.lib.document_governance.identity_history import (
    IdentityHistoryError,
    IssuedIdentities,
    collect_issued_identities,
    validate_identity_history,
)
from scripts.lib.document_governance.registry import load_registry


class IdentityHistoryTests(unittest.TestCase):
    def test_identity_scan_does_not_read_patch_text(self) -> None:
        """Identity history cost must not grow with every historical diff."""

        source = (
            pathlib.Path(__file__).resolve().parents[3]
            / "scripts/lib/document_governance/identity_history.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn('"-p"', source)
        self.assertNotIn('"--patch"', source)
        self.assertNotIn('"-G"', source)
        self.assertNotIn("_record_history_patch", source)
        self.assertIn("MAX_GIT_OUTPUT_BYTES = 8 * 1024 * 1024", source)
        self.assertNotIn(
            "MAX_GIT_OUTPUT_BYTES = 64 * 1024 * 1024",
            source,
        )

    def test_approved_pre_introduction_base_preserves_existing_identity(self) -> None:
        from scripts.lib.document_governance.archive import _approved_migration_document

        root = pathlib.Path(__file__).resolve().parents[3]
        approved = _approved_migration_document(root)
        base = approved["baseline_commit"]
        self.assertEqual(
            "",
            self._git(root, "ls-tree", base, "--", "docs/99.templates/registry.json"),
        )
        current = {"docs/03.specs/0008-workflow/spec.md": "SPEC-0008"}
        self.assertEqual(
            (),
            identity_history.validate_allocation_transition(
                root, load_registry(), current, base
            ),
        )
        with self.assertRaises(IdentityHistoryError):
            identity_history.validate_allocation_transition(
                root, load_registry(), current, "0" * 40
            )

    def test_generic_allocation_rejects_retired_reuse_and_requires_atomic_advance(
        self,
    ) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            spec = root / "docs/03.specs/0104-original/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text("---\nartifact_id: SPEC-0104\n---\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue identity")
            previous = self._git(root, "rev-parse", "HEAD").strip()
            registry = load_registry()
            current = {"docs/03.specs/0104-moved/spec.md": "SPEC-0104"}
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, registry, current, previous
                ),
            )
            spec.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "retire identity")
            retired = self._git(root, "rev-parse", "HEAD").strip()
            findings = identity_history.validate_allocation_transition(
                root, registry, current, retired
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})
            # Derive the unallocated number rather than pin one. A literal here
            # is consumed the moment real work issues that identity, and the
            # test then asserts that a legitimately allocated number is not
            # allocated. `SPEC-0154` was the pin and SPEC-0154 was issued.
            unallocated = registry.identity_spaces["spec"].high_water + 1
            introduced = {
                f"docs/03.specs/{unallocated:04d}-new/spec.md": f"SPEC-{unallocated:04d}"
            }
            findings = identity_history.validate_allocation_transition(
                root, registry, introduced, retired
            )
            self.assertIn(
                "identity-allocation-not-advanced", {item.code for item in findings}
            )
            spaces = dict(registry.identity_spaces)
            spaces["spec"] = dataclasses.replace(
                spaces["spec"], high_water=unallocated, next_number=unallocated + 1
            )
            advanced = dataclasses.replace(
                registry, identity_spaces=MappingProxyType(spaces)
            )
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, advanced, introduced, retired
                ),
            )

    def test_deleted_package_identity_requires_exact_git_recovery(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            registry_path = root / "docs/99.templates/registry.json"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            decision = root / "docs/03.specs/0104-decision/tasks/tsk-0001-recovery.md"
            decision.parent.mkdir(parents=True)
            decision.write_text(
                "---\nartifact_id: SPEC-0104-TSK-0001\n---\n", encoding="utf-8"
            )
            source = (
                root / "docs/90.references/research/0085-workspace/REQUEST-SCOPE.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nartifact_id: RES-0085-SCOPE\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue incomplete package")
            source_commit = self._git(root, "rev-parse", "HEAD").strip()
            source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete incomplete package")
            base = self._git(root, "rev-parse", "HEAD").strip()
            target_path = (
                "docs/90.references/research/0085-workspace/m0001-request-scope.md"
            )
            decision_path = decision.relative_to(root).as_posix()
            current = {
                target_path: "RES-0085-m0001",
                decision_path: "SPEC-0104-TSK-0001",
            }

            findings = identity_history.validate_allocation_transition(
                root, load_registry(), current, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            recovery = {
                target_path: {
                    "source_commit": source_commit,
                    "source_path": source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                    "decision_path": decision_path,
                    "decision_artifact_id": "SPEC-0104-TSK-0001",
                    "disposition": "consolidated",
                }
            }
            decision_evidence = {
                decision_path: [
                    {
                        "source_commit": source_commit,
                        "source_path": source.relative_to(root).as_posix(),
                        "source_artifact_id": "RES-0085-SCOPE",
                        "target_path": target_path,
                        "target_artifact_id": "RES-0085-m0001",
                        "disposition": "consolidated",
                    }
                ]
            }
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root,
                    load_registry(),
                    current,
                    base,
                    recovery_evidence=recovery,
                    decision_evidence=decision_evidence,
                ),
            )

            target = root / target_path
            target.write_text(
                "---\nartifact_id: RES-0085-m0001\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "introduce recovered package")
            target_base = self._git(root, "rev-parse", "HEAD").strip()
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root,
                    load_registry(),
                    current,
                    target_base,
                    recovery_evidence=recovery,
                    decision_evidence=decision_evidence,
                ),
            )

            recovery[target_path]["source_artifact_id"] = "RES-0084-SCOPE"
            findings = identity_history.validate_allocation_transition(
                root,
                load_registry(),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            recovery[target_path]["source_artifact_id"] = "RES-0085-SCOPE"
            findings = identity_history.validate_allocation_transition(
                root,
                load_registry(),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence={},
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

            untyped_decision_path = "docs/03.specs/0104-decision/tasks/tsk-0001.md"
            recovery[target_path]["decision_path"] = untyped_decision_path
            current[untyped_decision_path] = "SPEC-0104-TSK-0001"
            decision_evidence[untyped_decision_path] = decision_evidence[decision_path]
            findings = identity_history.validate_allocation_transition(
                root,
                load_registry(),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})
            recovery[target_path]["decision_path"] = decision_path
            current.pop(untyped_decision_path)
            decision_evidence.pop(untyped_decision_path)

            canonical_source = (
                root / "docs/90.references/research/0085-workspace/README.md"
            )
            canonical_source.write_text(
                "---\nartifact_id: RES-0085\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue canonical package")
            canonical_commit = self._git(root, "rev-parse", "HEAD").strip()
            canonical_source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete canonical package")
            canonical_base = self._git(root, "rev-parse", "HEAD").strip()
            recovery[target_path].update(
                {
                    "source_commit": canonical_commit,
                    "source_path": canonical_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085",
                }
            )
            decision_evidence[decision_path][0].update(
                {
                    "source_commit": canonical_commit,
                    "source_path": canonical_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085",
                }
            )
            findings = identity_history.validate_allocation_transition(
                root,
                load_registry(),
                current,
                canonical_base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

            foreign_source = (
                root / "docs/90.references/research/0084-other/REQUEST-SCOPE.md"
            )
            foreign_source.parent.mkdir(parents=True)
            foreign_source.write_text(
                "---\nartifact_id: RES-0085-SCOPE\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue foreign legacy member")
            foreign_commit = self._git(root, "rev-parse", "HEAD").strip()
            foreign_source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete foreign legacy member")
            foreign_base = self._git(root, "rev-parse", "HEAD").strip()
            recovery[target_path].update(
                {
                    "source_commit": foreign_commit,
                    "source_path": foreign_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                }
            )
            decision_evidence[decision_path][0].update(
                {
                    "source_commit": foreign_commit,
                    "source_path": foreign_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                }
            )
            findings = identity_history.validate_allocation_transition(
                root,
                load_registry(),
                current,
                foreign_base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

    def test_missing_predecessor_registry_is_not_a_generic_bootstrap_exception(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps({}), encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "introduce registry")
            source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete registry")
            previous = self._git(root, "rev-parse", "HEAD").strip()
            with self.assertRaises(IdentityHistoryError):
                identity_history.validate_allocation_transition(
                    root, load_registry(), {}, previous
                )

    def _git(self, root: pathlib.Path, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout

    def test_deleted_lowercase_package_and_child_ids_remain_reserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            requirement = root / "docs/01.requirements/prd-0042-example.md"
            requirement.parent.mkdir(parents=True)
            requirement.write_text(
                "---\nartifact_id: prd-0042\n---\n\n"
                "**PRD-0042-R0043**: old functional requirement\n"
                "**PRD-0042-NFR-0044**: old non-functional requirement\n"
                "**IFR-0042-R0045**: old interface requirement\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add deleted requirement")
            second = root / "docs/01.requirements/req-0043-example.md"
            second.write_text(
                "---\nartifact_id: REQ-0043\n---\n\n"
                "REQ-0043-FR-0043\nREQ-0043-NFR-0044\nREQ-0043-IF-0045\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add second requirement")
            requirement.unlink()
            second.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete requirement")

            issued = collect_issued_identities(root)

        self.assertGreaterEqual(issued.high_water("requirement"), 42)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.FR"), 43)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.NFR"), 44)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.IF"), 45)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.FR"), 43)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.NFR"), 44)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.IF"), 45)

    def test_stage90_category_not_legacy_ref_filename_owns_identity_space(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            audit = root / "docs/90.references/audits/ref-0023-fixture.md"
            data = root / "docs/90.references/data/history/ref-0061-fixture.md"
            audit.parent.mkdir(parents=True)
            data.parent.mkdir(parents=True)
            audit.write_text("---\nartifact_id: AUD-0023\n---\n", encoding="utf-8")
            data.write_text("---\nartifact_id: DATA-0061\n---\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add Stage 90 fixtures")

            issued = collect_issued_identities(root)

        self.assertIn(23, issued.numbers["audit"])
        self.assertIn(61, issued.numbers["data"])
        self.assertNotIn(23, issued.numbers.get("research", frozenset()))
        self.assertNotIn(61, issued.numbers.get("research", frozenset()))

    def test_tombstone_identity_comes_from_frontmatter_not_target_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            tombstone = root / (
                "docs/98.archive/tombstones/03.specs/0153-retired-target.md"
            )
            tombstone.parent.mkdir(parents=True)
            tombstone.write_text(
                "---\nartifact_id: TOMBSTONE-0131\n---\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add Tombstone fixture")

            issued = collect_issued_identities(root)

        self.assertIn(131, issued.numbers["tombstone"])
        self.assertNotIn(153, issued.numbers["tombstone"])

    def test_registry_high_water_is_not_below_repository_history(self) -> None:
        registry = load_registry()
        started = time.monotonic()
        issued = collect_issued_identities(
            pathlib.Path(__file__).resolve().parents[3], refs=("--all",)
        )
        self.assertGreater(issued.high_water("spec"), 0)

        self.assertEqual((), validate_identity_history(registry, issued))
        self.assertLessEqual(
            time.monotonic() - started,
            identity_history.MAX_GIT_SCAN_SECONDS + 5,
        )

    def test_history_uses_only_bounded_object_name_scans(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[3]
        commands: list[tuple[str, ...]] = []
        real_run_git = identity_history._run_git

        def recording_run_git(
            repo: pathlib.Path,
            arguments: tuple[str, ...],
            **kwargs: object,
        ) -> str:
            commands.append(arguments)
            return real_run_git(repo, arguments, **kwargs)

        with mock.patch.object(
            identity_history,
            "_run_git",
            side_effect=recording_run_git,
        ):
            collect_issued_identities(root, refs=("HEAD",))

        history_commands = [
            command for command in commands if command[:2] == ("rev-list", "--objects")
        ]
        self.assertEqual(
            [
                ("rev-list", "--objects", "HEAD", "--", pathspec)
                for pathspec in identity_history.GIT_HISTORY_QUERIES
            ],
            history_commands,
        )
        grep_commands = [
            command for command in commands if command[:2] == ("grep", "-h")
        ]
        self.assertTrue(grep_commands)
        self.assertTrue(
            all(
                len(command) <= identity_history._GIT_GREP_BATCH_SIZE + 12
                for command in grep_commands
            )
        )
        self.assertTrue(
            all(
                token not in command
                for command in commands
                for token in ("-p", "--patch", "-G", "-S")
            )
        )

    def test_git_output_cap_terminates_stdout_and_stderr_producers_early(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            executable = root / "git"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import os, pathlib, signal, sys, time\n"
                "marker = pathlib.Path(os.environ['FAKE_GIT_MARKER'])\n"
                "def stop(*_):\n"
                "    marker.write_text('terminated', encoding='utf-8')\n"
                "    raise SystemExit(0)\n"
                "signal.signal(signal.SIGTERM, stop)\n"
                "target = int(os.environ['FAKE_GIT_FD'])\n"
                "chunk = b'x' * 4096\n"
                "while True:\n"
                "    os.write(target, chunk)\n"
                "    time.sleep(0.001)\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)

            for stream_name, descriptor in (("stdout", "1"), ("stderr", "2")):
                with self.subTest(stream=stream_name):
                    marker = root / f"{stream_name}.marker"
                    environment = {
                        "PATH": f"{root}{os.pathsep}{os.environ.get('PATH', '')}",
                        "FAKE_GIT_MARKER": str(marker),
                        "FAKE_GIT_FD": descriptor,
                    }
                    started = time.monotonic()
                    with (
                        mock.patch.dict(os.environ, environment),
                        self.assertRaisesRegex(
                            IdentityHistoryError,
                            "Git identity scan exceeded its output bound",
                        ),
                    ):
                        identity_history._run_git(
                            root,
                            ("adversarial",),
                            max_output_bytes=1024,
                            timeout_seconds=4,
                        )
                    self.assertLess(time.monotonic() - started, 2)
                    self.assertEqual("terminated", marker.read_text(encoding="utf-8"))

    def test_terminate_and_reap_waits_for_killed_child_and_surfaces_reap_failure(
        self,
    ) -> None:
        alive = True
        process = mock.Mock()
        process.poll.side_effect = lambda: None if alive else -9

        def wait(timeout: float | None = None) -> int:
            nonlocal alive
            if timeout is not None:
                raise subprocess.TimeoutExpired("fake-git", timeout)
            alive = False
            return -9

        process.wait.side_effect = wait
        identity_history._terminate_and_reap(process, None)

        self.assertIsNotNone(process.poll())
        process.kill.assert_called_once_with()
        process.wait.assert_called_once_with()

        failed = mock.Mock()
        failed.poll.return_value = None
        failed.wait.side_effect = OSError("wait failed")
        with self.assertRaisesRegex(
            IdentityHistoryError, "failed to reap bounded Git identity scan"
        ):
            identity_history._terminate_and_reap(failed, None)

    def test_history_rejects_an_issued_but_unregistered_package_child_space(
        self,
    ) -> None:
        registry = load_registry()
        requirement = registry.identity_spaces["requirement"]
        children = {
            key: value
            for key, value in requirement.child_spaces.items()
            if key != "REQ-0001.FR"
        }
        broken_requirement = dataclasses.replace(
            requirement, child_spaces=MappingProxyType(children)
        )
        broken_registry = dataclasses.replace(
            registry,
            identity_spaces=MappingProxyType(
                {
                    **registry.identity_spaces,
                    "requirement": broken_requirement,
                }
            ),
        )
        issued = IssuedIdentities(
            MappingProxyType({"requirement.REQ-0001.FR": frozenset({4})})
        )

        self.assertIn(
            "identity-history-space-missing",
            {
                finding.code
                for finding in validate_identity_history(broken_registry, issued)
            },
        )

    def test_rename_into_docs_uses_the_destination_path_for_added_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            source = root / "notes.md"
            source.write_text("artifact_id: note-0001\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add note")
            target = root / "docs/01.requirements/0099-example.md"
            target.parent.mkdir(parents=True)
            source.rename(target)
            target.write_text("artifact_id: REQ-0099\n", encoding="utf-8")
            self._git(root, "add", "-A")
            self._git(root, "commit", "-qm", "promote requirement")
            target.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete requirement")

            issued = collect_issued_identities(root)

        self.assertGreaterEqual(issued.high_water("requirement"), 99)

    def test_deleted_worktree_source_is_history_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            source = root / "docs/90.references/research/0099-example/README.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nartifact_id: RES-0099\n---\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add identity source")
            source.unlink()

            issued = collect_issued_identities(root)

        self.assertIn(99, issued.numbers["research"])

    def test_tracked_identity_source_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            target = root / "target.md"
            target.write_text("artifact_id: REQ-0001\n", encoding="utf-8")
            link = root / "docs/01.requirements/0001-example.md"
            link.parent.mkdir(parents=True)
            link.symlink_to(target)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add unsafe identity source")

            with self.assertRaises(IdentityHistoryError):
                collect_issued_identities(root)


if __name__ == "__main__":
    unittest.main()


class GitPredicateTests(unittest.TestCase):
    """`git merge-base --is-ancestor` exits 1 to answer `false`, not to fail."""

    def _repo_with_two_unrelated_commits(self, root: pathlib.Path) -> tuple[str, str]:
        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True,
                text=True,
                check=True,
            )

        run("init", "-q")
        run("config", "core.hooksPath", "")
        run("config", "user.name", "Predicate Fixture")
        run("config", "user.email", "predicate@example.invalid")
        (root / "a.txt").write_text("a", encoding="utf-8")
        run("add", ".")
        run("commit", "-qm", "one")
        first = run("rev-parse", "HEAD").stdout.strip()
        run("checkout", "-q", "--orphan", "unrelated")
        (root / "b.txt").write_text("b", encoding="utf-8")
        run("add", ".")
        run("commit", "-qm", "two")
        second = run("rev-parse", "HEAD").stdout.strip()
        return first, second

    def test_false_predicate_is_an_answer_not_a_scan_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first, _ = self._repo_with_two_unrelated_commits(root)
            self.assertFalse(
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", first, "HEAD")
                )
            )

    def test_true_predicate_is_reported_as_true(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _, second = self._repo_with_two_unrelated_commits(root)
            self.assertTrue(
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", second, "HEAD")
                )
            )

    def test_scan_failure_names_the_command_and_carries_git_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._repo_with_two_unrelated_commits(root)
            with self.assertRaises(IdentityHistoryError) as caught:
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", "not-a-commit", "HEAD")
                )
            message = str(caught.exception)
            self.assertIn("merge-base --is-ancestor not-a-commit HEAD", message)
            self.assertNotEqual("bounded Git identity scan failed", message)
