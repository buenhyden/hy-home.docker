from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "scripts/manifest.yaml"
LEDGER = ROOT / "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"
MIGRATION_ROOTS = (
    "docs/01.requirements",
    "docs/02.architecture",
    "docs/03.specs",
    "docs/04.execution",
    "docs/05.operations",
    "docs/90.references",
    "docs/98.archive",
)
REQUIRED_FIELDS = frozenset(
    {
        "path",
        "kind",
        "authority",
        "lifecycle",
        "mutation",
        "consumers",
        "disposition",
        "successor",
        "tests",
    }
)
KINDS = frozenset(
    {
        "contract",
        "dependency-manifest",
        "generator",
        "hook",
        "library",
        "operations",
        "runner",
        "validator",
    }
)
LIFECYCLES = frozenset({"active", "transition"})
MUTATIONS = frozenset({"none", "check-write", "runtime"})
DISPOSITIONS = frozenset({"retain", "merge", "delete", "rewrite"})


def tracked_paths(pathspec: str) -> set[str]:
    return set(
        subprocess.run(
            ["git", "ls-files", pathspec],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout.splitlines()
    )


def local_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


class ScriptManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tracked = tracked_paths("scripts")
        cls.manifest_path = local_path(MANIFEST)
        cls.repository_paths = tracked_paths(":(top)")
        # Task 3 defines the script inventory itself.  Include the on-disk
        # record while this test runs before a controller can update the
        # protected shared Git index; at Task 3 HEAD it is tracked normally.
        cls.repository_paths.add(cls.manifest_path)
        cls.repository_paths.add(local_path(Path(__file__).resolve()))
        cls.manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.rows = cls.manifest["files"]

    def test_every_tracked_script_has_one_manifest_record(self) -> None:
        declared = [row["path"] for row in self.rows]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(self.tracked | {self.manifest_path}, set(declared))

    def test_records_are_sorted_and_use_the_complete_schema(self) -> None:
        paths = [row["path"] for row in self.rows]
        self.assertEqual(paths, sorted(paths))
        for row in self.rows:
            self.assertEqual(REQUIRED_FIELDS, set(row))
            self.assertIn(row["kind"], KINDS)
            self.assertIn(row["lifecycle"], LIFECYCLES)
            self.assertIn(row["mutation"], MUTATIONS)
            self.assertIn(row["disposition"], DISPOSITIONS)
            self.assertIsInstance(row["authority"], str)
            self.assertTrue(row["authority"])

    def test_consumer_successor_and_test_references_are_evidenced(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                self.assertIsInstance(row["consumers"], list)
                self.assertEqual(row["consumers"], sorted(set(row["consumers"])))
                self.assertIsInstance(row["tests"], list)
                self.assertEqual(row["tests"], sorted(set(row["tests"])))
                for reference in [*row["consumers"], *row["tests"]]:
                    self.assertIn(reference, self.repository_paths)
                    self.assertTrue((ROOT / reference).is_file())
                successor = row["successor"]
                if row["disposition"] == "retain":
                    self.assertIsNone(successor)
                else:
                    self.assertIsInstance(successor, str)
                    self.assertIn(successor, self.repository_paths)
                if row["disposition"] in {"retain", "rewrite"}:
                    self.assertTrue(row["consumers"])

    def test_ledger_has_one_complete_sorted_row_for_every_migration_document(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        ledger_text = text.split("```yaml\n", 1)[1].split("```", 1)[0]
        ledger = yaml.safe_load(ledger_text)
        rows = ledger["records"]
        expected = set().union(*(tracked_paths(root) for root in MIGRATION_ROOTS))
        expected.discard(LEDGER.relative_to(ROOT).as_posix())
        declared = [row["legacy_path"] for row in rows]
        self.assertEqual(declared, sorted(declared))
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(expected, set(declared))
        required = {
            "legacy_path",
            "stable_path",
            "artifact_id",
            "action",
            "replacement",
            "source_commit",
            "reason",
        }
        destructive = {"merge", "archive", "delete"}
        for row in rows:
            with self.subTest(path=row["legacy_path"]):
                self.assertEqual(required, set(row))
                self.assertIn(row["action"], {"archive", "delete", "merge", "move", "retain", "rewrite"})
                self.assertEqual(
                    "232effd9a5e00907bdbe30efc6665023fb2d07f4",
                    row["source_commit"],
                )
                self.assertTrue(row["reason"])
                if row["action"] == "delete":
                    self.assertIsNone(row["stable_path"])
                else:
                    self.assertIsInstance(row["stable_path"], str)
                    self.assertTrue(row["stable_path"])
                if row["action"] in destructive:
                    self.assertIsInstance(row["replacement"], str)
                    self.assertTrue(row["replacement"])
                else:
                    self.assertIsNone(row["replacement"])


if __name__ == "__main__":
    unittest.main()
