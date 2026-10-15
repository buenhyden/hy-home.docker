"""Required observations cannot be hidden by a separate successful check."""

from __future__ import annotations

import dataclasses
import json
import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance import spec_packages as module
from scripts.lib.document_governance.registry import load_registry
from tests.lib.document_governance.test_generation6 import (
    ACCEPT_BOTH,
    PASS_BOTH,
    PENDING_BOTH,
    PLAN,
    SPEC,
    generation6_registry,
    task,
)


def current_task(result: str, *, required: str = "required", resolves: str = "-"):
    source = task("", "")
    return dataclasses.replace(
        source,
        body=f"""## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Broken | 1 | W1 | Integration | candidate A | {result} | receipt | {required} | - |
| Good | 1 | W1 | Unit | candidate A | PASS | receipt | required | {resolves} |
| Other | 2 | W2 | Unit | candidate A | PASS | receipt | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Good | reviewed | [Owner](../spec.md) |
| 2 | accepted | Other | reviewed | [Owner](../spec.md) |
""",
    )


class Generation7EvidenceTests(unittest.TestCase):
    def contract(self, task):
        return module._v6_evidence_contract(SPEC, PLAN, (task,), load_registry())

    def test_required_nonpass_observation_blocks_acceptance(self):
        for result in ("FAIL", "ERROR", "NOT_RUN", "CANCELLED", "NOT_APPLICABLE"):
            with self.subTest(result=result):
                with self.assertRaisesRegex(
                    module.SpecPackageError, "unresolved required"
                ):
                    self.contract(current_task(result))

    def test_optional_observation_does_not_erase_a_valid_acceptance(self):
        self.contract(current_task("ERROR", required="optional"))

    def test_resolution_requires_the_same_check_and_work_unit(self):
        with self.assertRaisesRegex(
            module.SpecPackageError, "same Check and Work Unit"
        ):
            self.contract(current_task("ERROR", resolves="Broken"))
        fixed = current_task("ERROR", resolves="Broken")
        fixed = dataclasses.replace(
            fixed,
            body=fixed.body.replace(
                "| Good | 1 | W1 | Unit |", "| Good | 1 | W1 | Integration |"
            ),
        )
        self.assertFalse(self.contract(fixed).unresolved_failures)

    def test_acceptance_requires_a_current_owner(self):
        missing = current_task("PASS")
        missing = dataclasses.replace(
            missing, body=missing.body.replace("[Owner](../spec.md)", "-")
        )
        with self.assertRaisesRegex(module.SpecPackageError, "Current Owner"):
            self.contract(missing)

    def test_failed_observations_cannot_be_deleted_or_downgraded(self):
        registry = load_registry()
        before = current_task("ERROR")
        before = dataclasses.replace(
            before, body=before.body.replace("| accepted |", "| pending |")
        )
        package = module.SpecPackage(
            pathlib.Path(SPEC.path.parent), "0001", "example", SPEC, PLAN, (before,), ()
        )
        for changed in (
            before.body.replace(
                "| Broken | 1 | W1 | Integration | candidate A | ERROR | receipt | required | - |\n",
                "",
            ),
            before.body.replace(
                "| ERROR | receipt | required |", "| ERROR | receipt | optional |"
            ),
            before.body.replace("| ERROR | receipt |", "| PASS | receipt |"),
        ):
            with self.subTest(changed=changed):
                after = dataclasses.replace(
                    package, tasks=(dataclasses.replace(before, body=changed),)
                )
                self.assertTrue(
                    module._failed_observation_findings(
                        (package,), (after,), registry, registry
                    )
                )
        resolved = dataclasses.replace(
            before,
            body=before.body.replace(
                "\n\n## Criterion Acceptance",
                "\n| Fixed | 1 | W1 | Integration | candidate A | PASS | receipt | required | Broken |\n\n## Criterion Acceptance",
            ),
        )
        after = dataclasses.replace(package, tasks=(resolved,))
        self.assertEqual(
            (),
            module._failed_observation_findings(
                (package,), (after,), registry, registry
            ),
        )

    def test_legacy_failure_projection_preserves_every_observed_cell(self):
        legacy = task(
            "| Broken | 1 | W1 | Integration | candidate A | FAIL | receipt | - |\n",
            "| 1 | pending | - | - |\n| 2 | pending | - | - |\n",
        )
        before = module.SpecPackage(
            pathlib.Path(SPEC.path.parent), "0001", "example", SPEC, PLAN, (legacy,), ()
        )
        after = dataclasses.replace(before, tasks=(current_task("FAIL"),))
        self.assertEqual(
            (),
            module._failed_observation_findings(
                (before,), (after,), generation6_registry(), load_registry()
            ),
        )

    def test_multi_item_task_round_trips_through_a_committed_base(self):
        text = """---
title: "Items"
version: "0.1.0"
type: "sdlc/task"
owner: "@owner"
updated: "2026-10-15"
artifact_id: "SPEC-0001-TSK-0001"
parent_ids:
- "SPEC-0001-PLAN-0001"
---

# Items

## Work Log

### Execution Items

| Item | Work Unit | Scope | Owner | Status | Blocker |
| --- | --- | --- | --- | --- | --- |
| A | W1 | First | @owner | draft | - |
| B | W2 | Second | @owner | ready | - |
"""
        registry = load_registry()
        document = module._snapshot_document(
            SPEC.path.parent / "tasks/tsk-0001-items.md", text, registry=registry
        )
        self.assertEqual("ready", document.status)
        self.assertEqual(text, document.source_text)
        legacy = dataclasses.replace(
            registry, common={**registry.common, "lifecycle_generation": 5}
        )
        for invalid_text, profile, source_registry in (
            (text, "task", legacy),
            (
                text.replace("| B | W2 | Second | @owner | ready | - |\n", ""),
                "task",
                registry,
            ),
            (text.replace("SPEC-0001-TSK-0001", "SPEC-0001"), "spec", registry),
        ):
            path = (
                SPEC.path
                if profile == "spec"
                else SPEC.path.parent / "tasks/tsk-0001-items.md"
            )
            with self.subTest(
                profile=profile,
                generation=source_registry.common["lifecycle_generation"],
            ):
                with self.assertRaises(module.SpecPackageError):
                    module._snapshot_document(
                        path, invalid_text, registry=source_registry
                    )
        repository = pathlib.Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", "-C", str(root), *args],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            git("init", "-q")
            git("config", "core.hooksPath", "")
            git("config", "user.name", "Snapshot Fixture")
            git("config", "user.email", "fixture@example.invalid")
            for relative in (
                "docs/99.templates/registry.json",
                "docs/99.templates/contracts/document-profile.schema.json",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((repository / relative).read_bytes())
            task_path = root / SPEC.path.parent / "tasks/tsk-0001-items.md"
            task_path.parent.mkdir(parents=True)
            task_path.write_text(text)
            (root / SPEC.path).write_text(
                '---\nartifact_id: "SPEC-0001"\nstatus: "approved"\nparent_ids: []\n---\n\n# Spec\n'
            )
            git("add", ".")
            git("commit", "-qm", "multi-item source")
            packages = module._load_base_spec_packages(root, base_ref="HEAD")
            self.assertEqual("ready", packages[0].tasks[0].status)
            self.assertEqual(text, packages[0].tasks[0].source_text)

    def test_legacy_tables_allow_prose_correction_but_no_new_decision(self):
        original = task(PASS_BOTH, ACCEPT_BOTH)
        corrected = dataclasses.replace(
            original, body=original.body + "\nCurrent source handoff.\n"
        )
        admitted = module._bind_legacy_task_tables(
            corrected, original, generation6_registry()
        )
        self.contract(admitted)
        altered = dataclasses.replace(
            corrected, body=corrected.body.replace("| One | 1", "| Invented | 1")
        )
        for candidate, source in ((altered, original), (corrected, None)):
            with self.subTest(source=source is None):
                with self.assertRaisesRegex(module.SpecPackageError, "must match"):
                    module._bind_legacy_task_tables(
                        candidate, source, generation6_registry()
                    )

    def test_generation_source_exists_before_any_main_merge(self):
        repository = pathlib.Path(__file__).resolve().parents[3]
        registry_path = pathlib.Path("docs/99.templates/registry.json")
        schema_path = pathlib.Path(
            "docs/99.templates/contracts/document-profile.schema.json"
        )
        current = json.loads((repository / registry_path).read_text())
        earlier = json.loads(json.dumps(current))
        legacy = generation6_registry()
        for key in (
            "contract_id",
            "lifecycle_generation",
            "evidence_columns",
            "criterion_acceptance_columns",
            "result_domain",
        ):
            earlier["common"][key] = legacy.common[key]
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", "-C", str(root), *args],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            git("init", "-q")
            git("config", "core.hooksPath", "")
            git("config", "user.name", "Contract Fixture")
            git("config", "user.email", "fixture@example.invalid")
            for relative in (registry_path, schema_path):
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / schema_path).write_text((repository / schema_path).read_text())
            (root / registry_path).write_text(json.dumps(earlier))
            legacy_task = task(
                "| Broken | 1 | W1 | Integration | candidate A | FAIL | receipt | - |\n",
                PENDING_BOTH,
            )
            for document in (SPEC, PLAN, legacy_task):
                target = root / document.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "---\n"
                    + f"artifact_id: {document.artifact_id}\nstatus: {document.status}\n"
                    + f"parent_ids: {json.dumps(document.parent_ids)}\n---\n\n"
                    + document.body
                )
            git("add", ".")
            git("commit", "-qm", "source generation")
            source = git("rev-parse", "HEAD")
            self.assertEqual(source, module.previous_generation_revision(root, 7))
            (root / registry_path).write_text(json.dumps(current))
            git("add", ".")
            git("commit", "-qm", "local amendment")
            self.assertEqual(source, module.previous_generation_revision(root, 7))
            self.assertEqual("", git("rev-list", "--merges", "HEAD"))
            snapshots = module._load_base_spec_packages(root, base_ref="HEAD")
            bound = module._bind_legacy_evidence(snapshots, root)
            self.assertEqual(
                6, bound[0].tasks[0].evidence_registry.common["lifecycle_generation"]
            )
            self.assertEqual(
                (),
                module._failed_observation_findings(
                    bound, bound, load_registry(), load_registry()
                ),
            )


if __name__ == "__main__":
    unittest.main()
