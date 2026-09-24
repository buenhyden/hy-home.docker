"""Commit-pinned recovery never relaxes ordinary allocation validation."""

import copy
import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

from scripts.lib.document_governance.registry import (
    RegistryError,
    load_trusted_requirement_allocation_baseline,
)

PATH = "docs/01.requirements/0012-laboratory.md"
TASK = "docs/98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0001-home-dev-convergence.md"
REG = "docs/99.templates/registry.json"
FIELD = "requirement_allocation_recovery_decisions"


class PinnedAllocationRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        children = {
            f"REQ-{n:04d}.{kind}": {
                "prefix": f"REQ-{n:04d}-{kind}-",
                "width": 4,
                "child_spaces": {},
                "high_water": 4 if n == 12 and kind == "FR" else 0,
                "next_number": 5 if n == 12 and kind == "FR" else 1,
                "current_issued": [1, 2, 3, 4] if n == 12 and kind == "FR" else [],
                "reserved_history": [],
            }
            for n in range(1, 13)
            for kind in ("FR", "NFR", "IF")
        }
        self.registry = {
            "identity_spaces": {
                "requirement": {
                    "high_water": 12,
                    "next_number": 13,
                    "child_spaces": children,
                }
            }
        }
        self.write(REG, json.dumps(self.registry))
        self.valid_text = (
            '---\nartifact_id: "REQ-0012"\n---\n## Functional Requirements\n'
            + "".join(f"- **REQ-0012-FR-{n:04d}**: body {n}\n" for n in (1, 2, 3, 4))
            + "\n## Non-functional Requirements\n"
        )
        self.write(PATH, self.valid_text)
        self.predecessor = self.commit("valid")
        self.corrupt_text = self.valid_text.replace(
            "- **REQ-0012-FR-0003**: body 3\n", ""
        ).replace("REQ-0012-FR-0004", "REQ-0012-FR-0003")
        self.write(PATH, self.corrupt_text)
        self.defect = self.commit("defect")
        self.write("unrelated.txt", "later base")
        self.base = self.commit("base")
        self.repaired = self.corrupt_text.replace(
            "REQ-0012-FR-0003", "REQ-0012-FR-0004"
        )
        self.write(PATH, self.repaired)
        self.registry["identity_spaces"]["requirement"]["child_spaces"][
            "REQ-0012.FR"
        ].update(current_issued=[1, 2, 4], reserved_history=[3])
        self.write(REG, json.dumps(self.registry))
        self.decision = dict(
            comparison_base_commit=self.base,
            defect_commit=self.defect,
            valid_predecessor_commit=self.predecessor,
            requirement_path=PATH,
            allocation_name="REQ-0012.FR",
            predecessor_current_issued=[1, 2, 3, 4],
            corrupt_declared=[1, 2, 3],
            repaired_current_issued=[1, 2, 4],
            repaired_reserved_history=[3],
            repaired_requirement_sha256=hashlib.sha256(
                self.repaired.encode()
            ).hexdigest(),
            disposition="stable-identity-restoration",
        )
        self.pin_patch = patch(
            "scripts.lib.document_governance.requirement_recovery.EXPECTED_PINS",
            {
                key: self.decision[key]
                for key in (
                    "comparison_base_commit",
                    "defect_commit",
                    "valid_predecessor_commit",
                )
            },
        )
        self.pin_patch.start()
        self.addCleanup(self.pin_patch.stop)
        self.task()
        self.git("add", TASK)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def task(self, rows=None):
        metadata = {
            "type": "sdlc/task",
            "status": "draft",
            "artifact_id": "SPEC-0180-TSK-0001",
            FIELD: [self.decision] if rows is None else rows,
        }
        self.write(
            TASK, "---\n" + yaml.safe_dump(metadata) + "---\n# Recovery decision\n"
        )

    def load(self):
        return load_trusted_requirement_allocation_baseline(
            self.base, root=self.root, allow_pinned_recovery=True
        )

    def test_strict_default_rejects_known_corruption(self):
        with self.assertRaises(RegistryError):
            load_trusted_requirement_allocation_baseline(self.base, root=self.root)

    def test_valid_repair_retains_original_history(self):
        baseline = self.load()
        self.assertEqual(
            (1, 2, 3, 4), baseline.child_spaces["REQ-0012.FR"].current_issued
        )
        self.assertEqual(self.base, baseline.source)

    def test_decision_schema_and_pins_fail_closed(self):
        for key, value in [
            ("extra", True),
            ("comparison_base_commit", self.predecessor),
            ("defect_commit", "70aaeff"),
            ("valid_predecessor_commit", self.base),
            ("requirement_path", "../escape"),
            ("allocation_name", "REQ-0013.FR"),
            ("predecessor_current_issued", [1, 2, 3]),
            ("corrupt_declared", [1, 2, 4]),
            ("repaired_current_issued", [1, 2, 3]),
            ("repaired_reserved_history", []),
            ("repaired_requirement_sha256", "0" * 64),
            ("disposition", "ignore"),
        ]:
            with self.subTest(key=key):
                original = copy.deepcopy(self.decision)
                self.decision[key] = value
                self.task()
                with self.assertRaises(RegistryError):
                    self.load()
                self.decision = original
        del self.decision["defect_commit"]
        self.task()
        with self.assertRaises(RegistryError):
            self.load()

    def test_missing_duplicate_untracked_and_symlink_decisions_rejected(self):
        for rows in ([], [self.decision, self.decision]):
            self.task(rows)
            with self.assertRaises(RegistryError):
                self.load()
        self.task()
        self.git("rm", "--cached", TASK)
        with self.assertRaises(RegistryError):
            self.load()
        self.git("add", TASK)
        target = self.root / TASK
        body = target.read_text()
        target.unlink()
        self.write("other.md", body)
        target.symlink_to(self.root / "other.md")
        with self.assertRaises(RegistryError):
            self.load()

    def test_candidate_body_and_history_must_match_exact_repair(self):
        for text in (
            self.corrupt_text,
            self.repaired + "changed",
            self.repaired.replace("body 4", "different"),
        ):
            self.write(PATH, text)
            with self.assertRaises(RegistryError):
                self.load()
        self.write(PATH, self.repaired)
        for field, value in (
            ("current_issued", [1, 2, 3, 4]),
            ("reserved_history", []),
            ("high_water", 5),
            ("next_number", 6),
            ("current_issued", [True, 2, 4]),
        ):
            original = copy.deepcopy(self.registry)
            self.registry["identity_spaces"]["requirement"]["child_spaces"][
                "REQ-0012.FR"
            ][field] = value
            self.write(REG, json.dumps(self.registry))
            with self.assertRaises(RegistryError):
                self.load()
            self.registry = original

    def test_committed_repair_uses_strict_loader_without_recovery(self):
        repaired_commit = self.commit("repair")
        with patch(
            "scripts.lib.document_governance.requirement_recovery.recover_pinned_requirement_baseline",
            side_effect=AssertionError("must not recover"),
        ):
            baseline = load_trusted_requirement_allocation_baseline(
                repaired_commit, root=self.root, allow_pinned_recovery=True
            )
        self.assertEqual((1, 2, 4), baseline.child_spaces["REQ-0012.FR"].current_issued)

    def test_historical_base_drift_is_not_recovered(self):
        self.git("checkout", "--", PATH, REG)
        self.write(PATH, self.corrupt_text + "unrelated historical edit\n")
        self.base = self.commit("later drift")
        self.decision["comparison_base_commit"] = self.base
        self.write(PATH, self.repaired)
        self.write(REG, json.dumps(self.registry))
        self.task()
        from scripts.lib.document_governance import requirement_recovery

        with patch.dict(
            requirement_recovery.EXPECTED_PINS, {"comparison_base_commit": self.base}
        ):
            with self.assertRaisesRegex(
                RegistryError, "historical declarations differ"
            ):
                self.load()

    def test_other_allocation_mismatch_is_not_recovered(self):
        self.git("checkout", "--", PATH, REG)
        other = json.loads((self.root / REG).read_text())
        other["identity_spaces"]["requirement"]["child_spaces"]["REQ-0001.FR"].update(
            high_water=1, next_number=2, current_issued=[1]
        )
        self.write(REG, json.dumps(other))
        self.base = self.commit("unrelated allocation corruption")
        self.decision["comparison_base_commit"] = self.base
        self.write(PATH, self.repaired)
        self.write(REG, json.dumps(self.registry))
        self.task()
        with self.assertRaises(RegistryError):
            self.load()

    def test_oversized_decision_owner_rejected(self):
        self.write(TASK, (self.root / TASK).read_text() + "x" * (4 * 1024 * 1024))
        with self.assertRaises(RegistryError):
            self.load()

    def test_duplicate_task_owner_rejected(self):
        extra = TASK.replace("tsk-0001-", "tsk-0002-")
        self.write(
            extra,
            (self.root / TASK)
            .read_text()
            .replace("SPEC-0180-TSK-0001", "SPEC-0180-TSK-0002"),
        )
        self.git("add", extra)
        with self.assertRaises(RegistryError):
            self.load()

    def test_parent_task_symlink_rejected(self):
        task_dir = (self.root / TASK).parent
        target = self.root / "elsewhere"
        task_dir.rename(target)
        task_dir.symlink_to(target, target_is_directory=True)
        with self.assertRaises(RegistryError):
            self.load()

    def test_valid_looking_alternate_commit_pins_rejected_before_git(self):
        for key in (
            "comparison_base_commit",
            "defect_commit",
            "valid_predecessor_commit",
        ):
            original = self.decision[key]
            self.decision[key] = "a" * 40
            self.task()
            with self.assertRaisesRegex(RegistryError, "registered incident"):
                self.load()
            self.decision[key] = original


class RecoveryContractParityTests(unittest.TestCase):
    def test_implementation_incident_pins_match_stage99_constants(self):
        from scripts.lib.document_governance import requirement_recovery

        root = pathlib.Path(__file__).resolve().parents[3]
        schema = json.loads(
            (
                root / "docs/99.templates/contracts/document-frontmatter.schema.json"
            ).read_text()
        )
        properties = schema["$defs"]["requirementAllocationRecoveryDecisions"]["items"][
            "properties"
        ]
        for key, value in requirement_recovery.EXPECTED_PINS.items():
            self.assertEqual(value, properties[key]["const"])
        for key, value in requirement_recovery.FIXED.items():
            self.assertEqual(value, properties[key]["const"])
