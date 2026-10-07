"""Repository-composition and compatibility-facade tests."""

from __future__ import annotations

import contextlib
import dataclasses
import io
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.lib.document_governance import archive as archive_authority
from scripts.lib.document_governance.lifecycle.recovery import (
    run as run_recovery,
)
from scripts.lib.document_governance.metadata import reference as reference_module
from scripts.lib.document_governance.metadata.heading import (
    extract_markdown_headings,
)
from scripts.lib.document_governance.metadata.profile import (
    classify_registered_path,
)
from scripts.lib.document_governance.registry import (
    PRESERVED_DISPOSITIONS,
    preserved_origin_path,
)
from tests.lib.document_governance.metadata._support import (
    ROOT,
    copy_registry_contract_fixture,
    current_profiles,
    metadata,
    run_checker,
)


class MetadataValidatorCompatibilityTests(unittest.TestCase):
    def test_generated_inventory_has_registered_audit_metadata(self) -> None:
        from scripts.lib.document_governance.registry import validate_frontmatter

        rendered = reference_module.render_report([], current_profiles(), {})
        values = metadata._parse_frontmatter_text(rendered)
        self.assertEqual((), validate_frontmatter(values))
        self.assertLessEqual(
            set(
                current_profiles()["_registry"].profiles["audit"][
                    "required_frontmatter"
                ]
            ),
            values.keys(),
        )
        self.assertEqual("reference/audit-pack", values["type"])
        self.assertEqual("AUD-0023", values["artifact_id"])
        self.assertEqual("published", values["status"])
        self.assertEqual("1.0.1", values["version"])
        self.assertEqual("2026-07-05", str(values["created"]))
        self.assertEqual("2026-09-06", str(values["observed_at"]))
        _, h2 = extract_markdown_headings(rendered)
        headings = {heading.removeprefix("## ") for heading in h2}
        self.assertLessEqual(
            set(current_profiles()["_registry"].profiles["audit"]["required_sections"]),
            headings,
        )

    def test_report_includes_new_managed_governance_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            relative = pathlib.Path(".agents/governance/bootstrap.md")
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / relative).read_bytes())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--profiles",
                        str(ROOT / "docs/99.templates/registry.json"),
                        "--mode",
                        "report",
                    ]
                )
            self.assertEqual(0, result)
            self.assertIn(relative.as_posix(), output.getvalue())
            path.write_text(
                '---\ntitle: Fixture\nversion: invalid-fixture-version\ntype: governance/policy\nstatus: active\nowner: "@fixture"\nupdated: "2026-09-06"\n---\n# Fixture\n'
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--profiles",
                        str(ROOT / "docs/99.templates/registry.json"),
                        "--mode",
                        "check-active",
                    ]
                )
            self.assertEqual(1, result)
            self.assertIn(relative.as_posix(), output.getvalue())

    def test_metadata_validator_declares_its_compatibility_api(self) -> None:
        """The split preserves live imports, not incidental module globals."""

        from scripts.lib.document_governance import metadata_validator

        self.assertTrue(metadata_validator.__all__)
        missing = [
            name
            for name in metadata_validator.__all__
            if not hasattr(metadata_validator, name)
        ]
        self.assertEqual([], missing)


class RepositoryContractIntegrationTests(unittest.TestCase):
    def test_generation_normalization_accepts_only_registered_named_edges(self) -> None:
        registered = frozenset(
            {
                ("navigation", "draft", "active"),
                ("publication", "review", "in-review"),
            }
        )
        self.assertTrue(
            reference_module._registered_generation_normalization(
                {"lifecycle_id": "navigation", "identity_relation": "none"},
                "draft",
                "active",
                registered,
            )
        )
        self.assertFalse(
            reference_module._registered_generation_normalization(
                {"lifecycle_id": "adr", "identity_relation": "direct"},
                "accepted",
                "rejected",
                registered,
            )
        )

    def fixture(self, directory: str) -> tuple[pathlib.Path, pathlib.Path]:
        root = pathlib.Path(directory)
        return root, copy_registry_contract_fixture(root)

    def run_contracts(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        return run_checker(root, "check-contracts", profiles=profiles)

    def test_changed_mode_retains_repository_contract_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, registry = self.fixture(directory)
            finding = reference_module.Finding(
                "docs/03.specs/README.md", "index-member-unlisted", "fixture"
            )
            transitions = frozenset(
                {
                    (
                        "docs/03.specs/0001-fixture/tasks/tsk-0001-work.md",
                        "draft",
                        "in-progress",
                    )
                }
            )
            normalizations = frozenset(
                {
                    (
                        "docs/03.specs/0001-fixture/spec.md",
                        "active",
                        "in-progress",
                    )
                }
            )
            output = io.StringIO()
            with (
                mock.patch.object(
                    reference_module,
                    "_validate_repository_contracts",
                    return_value=(
                        [finding],
                        transitions,
                        normalizations,
                        reference_module._GenerationBindings(),
                    ),
                ) as contracts,
                mock.patch.object(
                    reference_module, "collect_records_at_ref", return_value=[]
                ) as base_records,
                mock.patch.object(
                    reference_module,
                    "validate_record",
                    return_value=[],
                ) as validate_record,
                contextlib.redirect_stdout(output),
            ):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(registry),
                        "--mode",
                        "check-changed",
                        "--base-ref",
                        "HEAD",
                    ]
                )
            contracts.assert_called_once()
            base_records.assert_called_once()
            self.assertEqual({}, contracts.call_args.kwargs["previous_records"])
            self.assertTrue(
                any(
                    call.kwargs.get("actual_lifecycle_transitions") == transitions
                    for call in validate_record.call_args_list
                )
            )
            self.assertTrue(
                any(
                    call.kwargs.get("actual_lifecycle_normalizations") == normalizations
                    for call in validate_record.call_args_list
                )
            )
            self.assertEqual(1, result)
            self.assertIn("index-member-unlisted", output.getvalue())

    def test_contracts_share_exact_baseline_and_historical_input_context(self) -> None:
        profiles = current_profiles()
        previous = {
            "docs/03.specs/0001-fixture/spec.md": reference_module.Record(
                pathlib.Path("docs/03.specs/0001-fixture/spec.md"),
                {"status": "draft"},
                "spec",
            )
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "docs/03.specs").mkdir(parents=True)
            authority = (
                root
                / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
            )
            authority.parent.mkdir(parents=True)
            authority.write_text("synthetic authority presence")
            lifecycle = mock.Mock(
                findings=(),
                actual_transitions=frozenset(),
                actual_normalizations=frozenset(),
                generation_source=None,
            )
            with (
                mock.patch.object(
                    reference_module, "_tracked_repository_markdown", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_reference_delegation_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_index_membership_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_allocation_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_changed_paths", return_value=set()
                ),
                mock.patch.object(
                    reference_module,
                    "collect_records_at_ref",
                    side_effect=AssertionError("baseline was already parsed"),
                ),
                mock.patch.object(
                    reference_module, "collect_records", return_value=[]
                ) as current,
                mock.patch.object(
                    reference_module, "load_spec_packages", return_value=()
                ) as packages,
                mock.patch.object(
                    reference_module,
                    "validate_repository_spec_package_lifecycle_details",
                    return_value=lifecycle,
                ) as validate,
            ):
                findings, _, _, _ = reference_module._validate_repository_contracts(
                    root,
                    profiles,
                    base_ref="a" * 40,
                    transition_ref="a" * 40,
                    previous_records=previous,
                )
            self.assertEqual([], findings)
            self.assertIs(previous, current.call_args.kwargs["previous_records"])
            self.assertIs(
                packages.call_args.kwargs["_historical_context"],
                validate.call_args.kwargs["_historical_context"],
            )

    def test_historical_archive_alias_requires_identity_metadata_and_raw_bytes(
        self,
    ) -> None:
        profiles = current_profiles()
        relative = pathlib.Path("docs/98.archive/migrations/0001-example.md")
        text = (
            "---\nartifact_id: MIG-0001\ntype: archive/migration\n"
            "status: sealed\n---\n# Historical Migration\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(text.encode())
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "source",
                ],
                cwd=root,
                check=True,
            )
            revision = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            record = metadata._record_from_text(relative, text, profiles=profiles)
            expected = frozenset({relative.as_posix()})
            self.assertEqual(
                expected,
                reference_module._source_bound_legacy_archive_types(
                    root, (record,), profiles, revision
                ),
            )
            for key, value in (("artifact_id", "MIG-0002"), ("status", "draft")):
                with self.subTest(changed_metadata=key):
                    changed = dataclasses.replace(
                        record, metadata={**record.metadata, key: value}
                    )
                    self.assertEqual(
                        frozenset(),
                        reference_module._source_bound_legacy_archive_types(
                            root, (changed,), profiles, revision
                        ),
                    )
            with mock.patch.object(
                reference_module, "collect_selected_records_at_ref", return_value={}
            ):
                self.assertEqual(
                    frozenset(),
                    reference_module._source_bound_legacy_archive_types(
                        root, (record,), profiles, revision
                    ),
                )
            for payload in (
                (text + "Changed body.\n").encode(),
                text.replace("\n", "\r\n").encode(),
            ):
                path.write_bytes(payload)
                self.assertEqual(
                    frozenset(),
                    reference_module._source_bound_legacy_archive_types(
                        root, (record,), profiles, revision
                    ),
                )

    def test_terminal_task_body_baseline_requires_exact_generation_blob(self) -> None:
        profiles = current_profiles()
        relative = pathlib.Path("docs/03.specs/0001-example/tasks/tsk-0001-example.md")
        missing_relative = pathlib.Path(
            "docs/03.specs/0001-example/tasks/tsk-0002-missing-at-source.md"
        )
        text = (
            "---\nartifact_id: SPEC-0001-TSK-0001\ntype: sdlc/task\n"
            "status: completed\n---\n# Historical Task\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text(text, encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "source",
                ],
                cwd=root,
                check=True,
            )
            revision = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            record = metadata._record_from_text(relative, text, profiles=profiles)
            bindings = reference_module._GenerationBindings(
                revision,
                {relative.as_posix(): "completed"},
                frozenset({relative.as_posix()}),
            )

            exact_record, exact_text = reference_module._generation_task_body_baseline(
                root, record, text, profiles, bindings
            )

            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
            normalized_crlf_text = path.read_text(encoding="utf-8")
            self.assertEqual(text, normalized_crlf_text)
            crlf_only = reference_module._generation_task_body_baseline(
                root, record, normalized_crlf_text, profiles, bindings
            )

            changed_text = text + "changed\n"
            path.write_bytes(changed_text.encode("utf-8"))
            changed = reference_module._generation_task_body_baseline(
                root, record, path.read_text(encoding="utf-8"), profiles, bindings
            )

            symlink_target = path.with_name("same-content.md")
            symlink_target.write_text(text, encoding="utf-8")
            path.unlink()
            path.symlink_to(symlink_target.name)
            nonregular = reference_module._generation_task_body_baseline(
                root, record, text, profiles, bindings
            )

            path.unlink()
            path.write_text(text, encoding="utf-8")
            with mock.patch.object(
                reference_module,
                "MAX_SPEC_FILE_BYTES",
                len(text.encode("utf-8")) - 1,
                create=True,
            ):
                oversized = reference_module._generation_task_body_baseline(
                    root, record, text, profiles, bindings
                )

            missing_path = root / missing_relative
            missing_path.write_text(text, encoding="utf-8")
            missing_record = metadata._record_from_text(
                missing_relative, text, profiles=profiles
            )
            missing_bindings = reference_module._GenerationBindings(
                revision,
                {missing_relative.as_posix(): "completed"},
                frozenset({missing_relative.as_posix()}),
            )
            missing_source = reference_module._generation_task_body_baseline(
                root, missing_record, text, profiles, missing_bindings
            )

        self.assertIsNotNone(exact_record)
        self.assertEqual(text, exact_text)
        self.assertEqual((None, None), crlf_only)
        self.assertEqual((None, None), changed)
        self.assertEqual((None, None), nonregular)
        self.assertEqual((None, None), oversized)
        self.assertEqual((None, None), missing_source)

    def test_repository_contracts_validate_canonical_spec_packages(self) -> None:
        profiles = current_profiles()
        findings = metadata.validate_repository_contracts(ROOT, profiles)
        self.assertNotIn(
            "spec-package-invalid",
            {finding.code for finding in findings},
        )

    def test_repository_contracts_reject_fragmented_in_progress_task_evidence(
        self,
    ) -> None:
        from scripts.lib.document_governance.registry import load_registry
        from scripts.lib.document_governance.spec_packages import load_spec_packages

        def materialize_in_progress_package(
            root: pathlib.Path,
            package_relative: pathlib.Path,
            index_anchor: str,
            index_row: str,
        ) -> None:
            package = root / package_relative
            tasks = package / "tasks"
            tasks.mkdir(parents=True, exist_ok=True)
            package.joinpath("spec.md").write_text(
                """---
title: "Fixture Evidence Integrity Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-06"
---

# Fixture Evidence Integrity Specification

## Overview

Exercise the generation 5 Evidence contract.

## Scope

The fixture is local to this regression.

## Contracts

The Task Evidence table remains contiguous.

## Acceptance Criteria

1. Reject a detached Evidence row.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-task-evidence-table-integrity.md)
""",
                encoding="utf-8",
            )
            package.joinpath("plan.md").write_text(
                """---
title: "Fixture Evidence Integrity Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210-PLAN-0001"
parent_ids:
- "SPEC-0210"
created: "2026-10-06"
---

# Fixture Evidence Integrity Plan

## Overview

Exercise one controlled in-progress Task.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Validate detached Evidence. | None | TSK-0001 | Metadata contracts. |

## Verification Plan

Run the canonical metadata checker before and after the mutation.

## Risks and Rollback

The temporary repository is discarded after the test.

## Related Documents

- [Specification](spec.md)
- [Task](tasks/tsk-0001-task-evidence-table-integrity.md)
""",
                encoding="utf-8",
            )
            tasks.joinpath("tsk-0001-task-evidence-table-integrity.md").write_text(
                """---
title: "Fixture Evidence Integrity Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210-TSK-0001"
parent_ids:
- "SPEC-0210-PLAN-0001"
created: "2026-10-06"
---

# Fixture Evidence Integrity Task

## Objective

Exercise the public metadata path with an explicit in-progress Task.

## Inputs and Authorization

### Fixture Authorization

This synthetic fixture grants no operation or approval.

## Work Log

### Fixture Start

The controlled fixture is in progress.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0210 | draft | approved | #fixture-authorization |
| SPEC-0210 | approved | in-progress | #fixture-start |
| SPEC-0210-PLAN-0001 | draft | approved | #fixture-authorization |
| SPEC-0210-PLAN-0001 | approved | in-progress | #fixture-start |
| SPEC-0210-TSK-0001 | draft | ready | #fixture-authorization |
| SPEC-0210-TSK-0001 | ready | in-progress | #fixture-start |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 1 | W1 | Fixture control | synthetic | NOT_RUN | This Task | pending |

## Review and Completion

The fixture is intentionally in progress.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
""",
                encoding="utf-8",
            )
            index = root / "docs/03.specs/README.md"
            index_text = index.read_text(encoding="utf-8")
            row_count = index_text.count(index_row)
            if row_count == 0:
                self.assertEqual(1, index_text.count(index_anchor))
                index.write_text(
                    index_text.replace(
                        index_anchor,
                        f"{index_anchor}\n{index_row}",
                        1,
                    ),
                    encoding="utf-8",
                )
            else:
                self.assertEqual(1, row_count)
            self.assertEqual(1, index.read_text(encoding="utf-8").count(index_row))

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory) / "repository"
            cloned = subprocess.run(
                ("git", "clone", "--quiet", "--shared", str(ROOT), str(root)),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, cloned.returncode, cloned.stdout + cloned.stderr)
            package_relative = pathlib.Path(
                "docs/03.specs/0210-task-evidence-table-integrity"
            )
            index_anchor = (
                "| SPEC-0209 | [0209-common-document-contract-adoption/]"
                "(./0209-common-document-contract-adoption/) | 공통 문서 계약의 "
                "Registry, 현재 문서, 소비자 정합화 |"
            )
            index_row = (
                "| SPEC-0210 | [0210-task-evidence-table-integrity/]"
                "(./0210-task-evidence-table-integrity/) | generation 5 Plan과 "
                "Task 증거 표의 분절 누락 방지 |"
            )
            materialize_in_progress_package(
                root,
                package_relative,
                index_anchor,
                index_row,
            )
            materialize_in_progress_package(
                root,
                package_relative,
                index_anchor,
                index_row,
            )
            shutil.copy2(
                ROOT / "docs/99.templates/registry.json",
                root / "docs/99.templates/registry.json",
            )
            shutil.copy2(
                ROOT / "scripts/lib/document_governance/spec_packages.py",
                root / "scripts/lib/document_governance/spec_packages.py",
            )
            staged = subprocess.run(
                ("git", "-C", str(root), "add", "--all"),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, staged.returncode, staged.stdout + staged.stderr)
            committed = subprocess.run(
                (
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=P03 Fixture",
                    "-c",
                    "user.email=p03@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "p03 metadata fixture",
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                0, committed.returncode, committed.stdout + committed.stderr
            )
            registry_path = root / "docs/99.templates/registry.json"
            packages = load_spec_packages(
                root / "docs/03.specs",
                registry=load_registry(registry_path),
            )
            fixture_package = next(
                package
                for package in packages
                if package.spec.artifact_id == "SPEC-0210"
            )
            self.assertEqual("in-progress", fixture_package.spec.status)
            self.assertEqual("in-progress", fixture_package.plan.status)
            self.assertEqual(1, len(fixture_package.tasks))
            self.assertEqual("in-progress", fixture_package.tasks[0].status)
            control = self.run_contracts(root, registry_path)
            self.assertEqual(
                0,
                control.returncode,
                control.stdout + control.stderr,
            )

            task = (
                root
                / package_relative
                / ("tasks/tsk-0001-task-evidence-table-integrity.md")
            )
            marker = "\n## Review and Completion\n"
            source = task.read_text(encoding="utf-8")
            self.assertEqual(1, source.count(marker))
            task.write_text(
                source.replace(
                    marker,
                    "\nDetached evidence fragment.\n\n"
                    "| Hidden failure | 1 | W1 | Source check | fixture | FAIL | "
                    "detached | rejected |\n" + marker,
                    1,
                ),
                encoding="utf-8",
            )

            result = self.run_contracts(
                root,
                registry_path,
            )
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn("spec-package-invalid", rendered)
            self.assertIn("registered evidence table must be contiguous", rendered)

    def test_repository_contracts_enforce_machine_source_safety(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            path = root / relative_path
            path.write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "servers:\n"
                "  - url: https://api.example.com\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )

    def test_registry_contracts_parse_profile_and_section_contracts(self) -> None:
        relative_path = (
            "docs/99.templates/templates/requirements/requirement-package.template.md"
        )
        cases = (
            (
                "profile",
                'type: "sdlc/requirement"',
                'type: "sdlc/spec"',
                "template-artifact-type-mismatch",
            ),
            (
                "heading",
                "## Acceptance Criteria",
                "## Verification Contract",
                "template-section-missing",
            ),
        )
        for label, before, after, expected in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / relative_path
                path.write_text(
                    path.read_text(encoding="utf-8").replace(before, after, 1),
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"{expected}: {relative_path}", result.stdout)

    def test_repository_contracts_fail_closed_on_openapi_parse_boundaries_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        cases = (
            (
                "malformed",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npaths: [fixture-parse-leak\n",
                "fixture-parse-leak",
            ),
            (
                "duplicate-key",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\ninfo: fixture-first\ninfo: fixture-duplicate-leak\n",
                "fixture-duplicate-leak",
            ),
            (
                "constructor",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-value: !!python/object:fixture-constructor-leak {}\n",
                "fixture-constructor-leak",
            ),
            (
                "non-mapping-root",
                "- __API_TITLE__\n- fixture-root-leak\n",
                "fixture-root-leak",
            ),
        )
        for label, text, private_value in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-parse-error: {relative_path}: "
                    "machine template could not be parsed as a safe OpenAPI mapping",
                    result.stdout,
                )
                self.assertNotIn(private_value, rendered)
                self.assertNotRegex(rendered, r"(?i)(line|column) [0-9]+")

    def test_repository_contracts_bound_openapi_credential_value_keywords(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with (
                self.subTest(keyword=keyword),
                tempfile.TemporaryDirectory() as directory,
            ):
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          {keyword}: {value}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)
        with (
            self.subTest(keyword="direct-list"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "access_token: [__ACCESS_TOKEN__, fixture-direct-list-leak]\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )
            self.assertNotIn("fixture-direct-list-leak", rendered)

    def test_repository_contracts_reject_openapi_credential_plural_examples_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        cases = {
            "scalar": "fixture-scalar-cli-private",
            "list": "[__PASSWORD_PRIMARY__, fixture-list-cli-private]",
            "map": "{primary: __PASSWORD_PRIMARY__, secondary: fixture-map-cli-private}",
        }
        for label, examples in cases.items():
            with self.subTest(shape=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          examples: {examples}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)

    def test_repository_contracts_accept_exact_nested_openapi_credential_examples_tokens(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          examples:\n"
                "            primary: __PASSWORD_PRIMARY__\n"
                "            alternatives:\n"
                "              - __PASSWORD_SECONDARY__\n"
                "              - __PASSWORD_TERTIARY__\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_repository_contracts_accept_safe_openapi_credential_shapes(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        cases = (
            (
                "exact-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "x-api-key: __API_KEY__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          default: __PASSWORD_DEFAULT__\n"
                "          example: __PASSWORD_EXAMPLE__\n"
                "          const: __PASSWORD_CONST__\n"
                "          enum: [__PASSWORD_PRIMARY__, __PASSWORD_SECONDARY__]\n",
            ),
            (
                "schema-only-unrelated-default",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      required: [password]\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          format: password\n"
                "          description: caller-supplied credential\n"
                "        displayName:\n"
                "          type: string\n"
                "          default: fixture display name\n",
            ),
            (
                "standard-example-token",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          example: __PASSWORD_EXAMPLE__\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_workspace_cannot_become_a_docs_inventory_prefix(self) -> None:
        from scripts.lib.document_governance.metadata import reference

        profiles = current_profiles()
        original = reference.TARGET_MARKDOWN_PREFIXES
        try:
            reference.TARGET_MARKDOWN_PREFIXES = (*original, "_workspace/")
            findings = metadata.validate_repository_contracts(ROOT, profiles)
        finally:
            reference.TARGET_MARKDOWN_PREFIXES = original
        self.assertIn(
            "workspace-inventory-coupling",
            {finding.code for finding in findings},
        )


class IndexMembershipTests(unittest.TestCase):
    """The index rule must fire, and must not fire on a listed package."""

    def _findings(self, index_body: str) -> list[object]:
        registry = metadata.load_registry()
        member = "docs/90.references/research/0002-agentic-engineering-research-pack/README.md"
        self.assertEqual(
            "research",
            classify_registered_path(member, registry),
            "fixture path must classify as the indexed member profile",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            index = root / "docs/90.references/research/README.md"
            index.parent.mkdir(parents=True)
            index.write_text(index_body, encoding="utf-8")
            record = metadata.Record(pathlib.Path(member), {}, "research")
            findings = reference_module._index_membership_findings(
                root, registry, [record]
            )
        # The fixture root holds only the research index and one research
        # record, so the other registered indexes govern nothing and are
        # skipped. Scoping keeps this test about the research rule alone.
        return [
            finding
            for finding in findings
            if finding.path == "docs/90.references/research/README.md"
            and finding.code != "index-unreadable"
        ]

    def test_unlisted_package_is_reported(self) -> None:
        findings = self._findings("# Research Packages\n")
        self.assertEqual(
            ["index-member-unlisted"], [finding.code for finding in findings]
        )

    def test_listed_package_is_accepted(self) -> None:
        findings = self._findings(
            "# Research Packages\n\n"
            "| [RES-0002](./0002-agentic-engineering-research-pack/README.md) | x |\n"
        )
        self.assertEqual([], findings)

    def test_package_directory_link_is_membership(self) -> None:
        """SPEC-0184 rule 6: an index links a package, not its member file."""

        for target in (
            "./0002-agentic-engineering-research-pack/",
            "0002-agentic-engineering-research-pack",
        ):
            with self.subTest(target=target):
                findings = self._findings(
                    f"# Research Packages\n\n[RES-0002]({target})\n"
                )
                self.assertEqual([], findings)

    def test_every_registered_index_governs_at_least_one_package(self) -> None:
        """A rule that enumerates nothing passes without checking anything."""

        registry = metadata.load_registry()
        self.assertTrue(registry.indexes)
        for index_path, member_profile in registry.indexes.items():
            with self.subTest(index=index_path):
                self.assertTrue((ROOT / index_path).is_file())
                governed = [
                    path
                    for path in (ROOT / index_path).parent.rglob("*.md")
                    if classify_registered_path(
                        path.relative_to(ROOT).as_posix(), registry
                    )
                    == member_profile
                ]
                governed.extend(
                    self._preserved_members(registry, index_path, member_profile)
                )
                self.assertTrue(governed, f"{index_path} governs no document")

    @staticmethod
    def _preserved_members(
        registry: object, index_path: str, member_profile: str
    ) -> list[pathlib.Path]:
        """Members an index still governs after preservation moved their bodies.

        An active stage empties out when its last package completes, which is a
        real state and not a vacuous rule: Stage 03 holds no package exactly
        when no change is in flight. Preservation moves the body without ending
        the governance relation, so the index's own listing still routes to
        every one of them. Count them by the path they were moved from.
        """

        stage_dir = pathlib.PurePosixPath(index_path).parent
        found: list[pathlib.Path] = []
        for disposition in PRESERVED_DISPOSITIONS:
            root = ROOT / "docs/98.archive" / disposition
            if not root.is_dir():
                continue
            for path in root.rglob("*.md"):
                origin = preserved_origin_path(path.relative_to(ROOT).as_posix())
                if origin is None:
                    continue
                if not origin.startswith(f"{stage_dir}/"):
                    continue
                if classify_registered_path(origin, registry) == member_profile:
                    found.append(path)
        return found


class ReadmeSectionProfileTests(unittest.TestCase):
    """Sections come from the document's own profile, not from `readme`."""

    def test_every_readme_profile_that_declares_sections_is_satisfied(self) -> None:
        registry = metadata.load_registry()
        checked = 0
        for path in ROOT.glob("**/README.md"):
            relative = path.relative_to(ROOT).as_posix()
            if relative.startswith((".git/", ".worktrees/", "node_modules/")):
                continue
            profile_id = classify_registered_path(relative, registry)
            if profile_id is None:
                continue
            required = registry.profiles.get(profile_id, {}).get(
                "required_sections", ()
            )
            if not required:
                continue
            checked += 1
            _, h2 = extract_markdown_headings(path.read_text(encoding="utf-8"))
            for section in required:
                with self.subTest(path=relative, section=section):
                    self.assertIn(f"## {section}", h2)
        # A profile-driven check that inspects nothing passes vacuously.
        self.assertGreater(checked, 100, "too few READMEs carry a section contract")

    def test_profiles_beyond_readme_declare_sections(self) -> None:
        """The rule is only worth enforcing if other profiles use it."""

        registry = metadata.load_registry()
        with_sections = {
            profile_id
            for profile_id, profile in registry.profiles.items()
            if profile.get("required_sections")
        }
        self.assertIn("readme", with_sections)
        self.assertTrue(with_sections - {"readme"})


class GloballyForbiddenKeyTests(unittest.TestCase):
    """A retired key is reported as retired, not as an unknown typo."""

    def _codes(self, key: str) -> list[str]:
        registry = metadata.load_registry()
        profiles = metadata.build_registry_profiles(registry)
        record = metadata.Record(
            pathlib.Path(".agents/governance/providers/README.md"),
            {
                "title": "Providers",
                "version": "1.0.0",
                "type": "governance/provider-index",
                "status": "active",
                "owner": "@buenhyden",
                key: "x",
            },
            "governance-provider-index",
        )
        manifest = metadata.build_manifest([record])
        return [
            finding.code
            for finding in metadata.validate_record(record, profiles, manifest)
            if finding.code in {"forbidden-key", "type-inappropriate-key"}
        ]

    def test_every_globally_forbidden_key_is_reported_as_forbidden(self) -> None:
        registry = metadata.load_registry()
        forbidden = registry.common.get("globally_forbidden", ())
        self.assertTrue(forbidden, "the contract declares nothing to enforce")
        for key in forbidden:
            with self.subTest(key=key):
                self.assertIn("forbidden-key", self._codes(key))

    def test_an_undeclared_key_keeps_the_other_code(self) -> None:
        self.assertEqual(["type-inappropriate-key"], self._codes("bogus_key"))


class ArchiveContractDiagnosticTests(unittest.TestCase):
    """An archive contract violation must name the document, not be an error."""

    def _corrupted_root(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        shutil.copytree(ROOT / "docs/98.archive", root / "docs/98.archive")
        victim = next((root / "docs/98.archive/tombstones").rglob("*.md"))
        victim.write_text(
            victim.read_text(encoding="utf-8")
            + "\n## Original Body\n\nA retired body copied into the pointer.\n",
            encoding="utf-8",
        )
        self.relative = victim.relative_to(root).as_posix()
        return root

    def test_violation_is_reported_with_its_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._corrupted_root(directory)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = run_recovery(root)
        output = stream.getvalue()
        self.assertEqual(1, code, output)
        self.assertIn("archive-contract-invalid", output)
        self.assertIn(self.relative, output)

    def test_intact_archive_still_loads(self) -> None:
        inventory = archive_authority.load_archive(ROOT / "docs/98.archive")
        self.assertTrue(inventory.tombstones)
        self.assertTrue(inventory.migrations)


class TemplateRoutingTests(unittest.TestCase):
    """SPEC-0184 rule 7: `template_roles` alone maps a type to its template."""

    def test_registry_carries_no_template_catalog(self) -> None:
        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("template_catalog", raw)
        self.assertFalse(hasattr(metadata.load_registry(), "template_catalog"))
        self.assertFalse(hasattr(reference_module, "_template_catalog_findings"))

    def test_every_role_still_names_an_existing_source(self) -> None:
        registry = metadata.load_registry()
        self.assertGreater(len(registry.template_roles), 30)
        for role_id, role in registry.template_roles.items():
            with self.subTest(role=role_id):
                self.assertTrue((ROOT / str(role["source"])).is_file())

    def test_templates_readme_routes_only_to_category_directories(self) -> None:
        from scripts.lib.document_governance.links import (
            build_document_graph,
            check_navigation,
        )

        readme = ROOT / "docs/99.templates/templates/README.md"
        findings = check_navigation(build_document_graph([readme], repo_root=ROOT))
        self.assertEqual([], findings)
