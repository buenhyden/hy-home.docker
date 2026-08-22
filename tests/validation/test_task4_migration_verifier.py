from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-task4-migration.py"
MIGRATION = ROOT / "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md"


def load_verifier():
    spec = importlib.util.spec_from_file_location("check_task4_migration", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def mutate_ledger(path: pathlib.Path, mutation) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^```(?:yaml|yml)[ \t]*\r?\n(.*?)^```[ \t]*$",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if match is None:
        raise RuntimeError("missing migration ledger")
    ledger = yaml.safe_load(match.group(1))
    mutation(ledger)
    replacement = yaml.safe_dump(ledger, sort_keys=False)
    path.write_text(text[: match.start(1)] + replacement + text[match.end(1) :], encoding="utf-8")


class Task4MigrationVerifierTests(unittest.TestCase):
    def test_exact_approved_task4_selection_and_edges(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/validation/check-task4-migration.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("rows=128 rename=81 delete=47 edges=1134", result.stdout)
        self.assertIn(
            "selection_sha256="
            "9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1",
            result.stdout,
        )
        self.assertIn(
            "edges_sha256="
            "2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139",
            result.stdout,
        )
        self.assertIn(
            "task4_rows_sha256="
            "2fd01449c78581374d37153175455ca0d08e2ca05e36812dcab8189a97208f95",
            result.stdout,
        )

    def test_negative_mutations_report_the_failed_integrity_layer(self) -> None:
        cases = {
            "identity": (
                lambda ledger: ledger["rows"][3].update({"row_id": "mig-0003-r9999"}),
                "Task 4 row identities changed",
            ),
            "action": (
                lambda ledger: ledger["rows"][3].update({"action": "invented"}),
                "Task 4 action counts changed",
            ),
            "target": (
                lambda ledger: ledger["rows"][3].update({"target_path": None}),
                "rename row lacks target",
            ),
            "totals": (
                lambda ledger: ledger["rows"][3].update({"owner_task": 5}),
                "Task 4 totals changed",
            ),
            "selection-digest": (
                lambda ledger: ledger.update({"baseline_commit": "0" * 40}),
                "approved selection digest changed",
            ),
            "edge-digest": (
                lambda ledger: ledger["rows"][3]["active_consumers"].append(
                    "invented/consumer.md"
                ),
                "derived consumer-edge digest changed",
            ),
            "task4-row-digest": (
                lambda ledger: ledger["rows"][3].update(
                    {"source_path": "invented/source.md"}
                ),
                "Task 4 source/target/action mapping changed",
            ),
        }
        verifier = load_verifier()
        for name, (mutation, message) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                migration = pathlib.Path(directory) / MIGRATION.name
                shutil.copy2(MIGRATION, migration)
                mutate_ledger(migration, mutation)
                verifier.MIGRATION = migration
                with self.assertRaisesRegex(verifier.VerificationError, message):
                    verifier._verify()


if __name__ == "__main__":
    unittest.main()
