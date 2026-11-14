"""The CLI operates on isolated public fixtures, never the HOME configuration."""

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
)
from scripts.lib.ops._workspace_render import render_inventory

CLI = Path(__file__).resolve().parents[2] / "scripts/operations/workspace-inventory.py"


class WorkspaceCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="p01 cli ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "app.py").write_text("print('synthetic')\n")
        (self.root / ".env").write_text("MUST_NOT_APPEAR_IN_REPORT\n")

    def run_cli(self, command, *args):
        return subprocess.run(
            [sys.executable, str(CLI), command, "--root", str(self.root), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_scan_validate_compare_and_private_metadata_separation(self):
        private = "_workspace/repo-support/analysis/p01/private.yaml"
        result = self.run_cli(
            "scan",
            "--output",
            "before.yaml",
            "--private-output",
            private,
            "--public-path",
            "app.py",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        public = yaml.safe_load((self.root / "before.yaml").read_text())
        self.assertNotIn(".env", [r["path"] for r in public["files"]])
        self.assertTrue((self.root / private).exists())
        self.assertNotIn(
            "MUST_NOT_APPEAR", result.stdout + (self.root / private).read_text()
        )
        self.assertEqual(
            self.run_cli("validate", "--input", "before.yaml").returncode, 0
        )
        (self.root / "app.py").write_text("print('changed')\n")
        self.assertEqual(
            self.run_cli(
                "scan", "--output", "after.yaml", "--public-path", "app.py"
            ).returncode,
            0,
        )
        compared = self.run_cli(
            "compare", "--before", "before.yaml", "--after", "after.yaml"
        )
        self.assertEqual(compared.returncode, 0, compared.stderr)
        self.assertEqual(json.loads(compared.stdout)["changed"], ["app.py"])

    def test_invalid_curation_and_unsafe_paths_preserve_previous_output(self):
        (self.root / "out.yaml").write_text("previous")
        (self.root / "curation.yaml").write_text("workspace: {git: false}\n")
        for args in (
            ("--output", "out.yaml", "--curation", "curation.yaml"),
            ("--output", "../outside.yaml"),
            ("--output", "out.yaml", "--private-output", "public-private.yaml"),
        ):
            result = self.run_cli("scan", *args)
            self.assertEqual(result.returncode, 2)
            self.assertEqual((self.root / "out.yaml").read_text(), "previous")

    def test_scan_connections_is_opt_in_and_value_minimizing(self):
        relative = "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json"
        source = self.root / relative
        source.parent.mkdir(parents=True)
        source.write_text('{"host":"dev-pg","port":5432,"password":"PRIVATE_MARKER"}')
        plain = self.run_cli(
            "scan", "--output", "plain.yaml", "--public-path", relative
        )
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertNotIn(
            "connections", yaml.safe_load((self.root / "plain.yaml").read_text())
        )

        result = self.run_cli(
            "scan",
            "--output",
            "connections.yaml",
            "--connections",
            "--public-path",
            relative,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        document = yaml.safe_load((self.root / "connections.yaml").read_text())
        self.assertEqual(document["connections"][0]["provider"], "dev-pg")
        self.assertEqual(
            document["connections"][0]["registration"]["actual_state"], "UNKNOWN"
        )
        self.assertNotIn("PRIVATE_MARKER", (self.root / "connections.yaml").read_text())
        self.assertEqual(
            self.run_cli("validate", "--input", "connections.yaml").returncode, 0
        )

    def test_connection_read_boundary_failure_is_fixed_and_preserves_output(self):
        relative = "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json"
        source = self.root / relative
        source.parent.mkdir(parents=True)
        source.write_text('{"host":"dev-pg","port":5432}')
        (self.root / "connections.yaml").write_text("previous")
        spec = importlib.util.spec_from_file_location("workspace_inventory_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        stderr = io.StringIO()
        with (
            patch(
                "scripts.lib.ops._workspace_connections.read_bounded_regular",
                side_effect=OperationsAuthorityError(
                    "read-failed", "PRIVATE_SOURCE_PATH"
                ),
            ),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            result = module.main(
                [
                    "scan",
                    "--root",
                    str(self.root),
                    "--output",
                    "connections.yaml",
                    "--connections",
                    "--public-path",
                    relative,
                ]
            )
        self.assertEqual(result, 2)
        self.assertEqual((self.root / "connections.yaml").read_text(), "previous")
        self.assertNotIn("PRIVATE_SOURCE_PATH", stderr.getvalue())

    def test_bad_arguments_and_yaml_do_not_echo_input_values(self):
        bad = self.run_cli("validate", "--SENSITIVE_ARGUMENT")
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn("SENSITIVE_ARGUMENT", bad.stderr)
        (self.root / "bad.yaml").write_text("!!python/object:PRIVATE {}")
        failed = self.run_cli("validate", "--input", "bad.yaml")
        self.assertEqual(failed.returncode, 2)
        self.assertNotIn("PRIVATE", failed.stderr)

    def test_cli_main_in_process_exercises_results_and_cancellation(self):
        spec = importlib.util.spec_from_file_location("workspace_inventory_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        shared = ["--root", str(self.root)]
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(
                module.main(
                    ["scan", *shared, "--output", "one.yaml", "--public-path", "app.py"]
                ),
                0,
            )
            self.assertEqual(
                module.main(["validate", *shared, "--input", "one.yaml"]), 0
            )
            self.assertEqual(
                module.main(
                    ["compare", *shared, "--before", "one.yaml", "--after", "one.yaml"]
                ),
                0,
            )
            self.assertEqual(
                module.main(["validate", *shared, "--input", "missing.yaml"]), 2
            )
            with patch.object(module, "scan", side_effect=KeyboardInterrupt):
                self.assertEqual(
                    module.main(["scan", *shared, "--output", "one.yaml"]), 130
                )
            (self.root / "docker-compose.yml").write_text(
                "services: {app: {image: 'alpine:3'}}\n"
            )

            def render(root, doc):
                return render_inventory(
                    root,
                    doc,
                    run=lambda *a, **k: subprocess.CompletedProcess(
                        a, 0, b'{"services":{"app":{}}}'
                    ),
                )

            with patch.object(module, "render_inventory", side_effect=render):
                self.assertEqual(
                    module.main(
                        [
                            "scan",
                            *shared,
                            "--output",
                            "rendered.yaml",
                            "--render",
                            "--public-path",
                            "docker-compose.yml",
                        ]
                    ),
                    0,
                )

            inputs = [
                {
                    "source": "docker-compose.yml",
                    "selection": "all-profiles",
                    "variables": {},
                }
            ]
            (self.root / "inputs.yaml").write_text(yaml.safe_dump(inputs))
            with patch.object(
                module, "render_inventory", side_effect=lambda root, doc, **kwargs: doc
            ) as renderer:
                self.assertEqual(
                    module.main(
                        [
                            "scan",
                            *shared,
                            "--output",
                            "typed.yaml",
                            "--render",
                            "--render-inputs",
                            "inputs.yaml",
                            "--public-path",
                            "docker-compose.yml",
                        ]
                    ),
                    0,
                )
                self.assertEqual(renderer.call_args.kwargs["case_inputs"], inputs)


class CommittedLedgerTests(unittest.TestCase):
    def test_committed_ledger_passes_its_own_validator(self):
        # A moved connection source (e.g. 30d73680a) must not leave DATA-0096
        # unloadable by `compare`; regenerate the ledger when this fails.
        from scripts.lib.ops.workspace_inventory import validate

        ledger = (
            CLI.parents[2]
            / "docs/90.references/data/0096-workspace-inventory/data.yaml"
        )
        self.assertTrue(validate(yaml.safe_load(ledger.read_text())))


class PublishedSnapshotFreshnessTests(unittest.TestCase):
    """DATA-0096 is a dated scan the producer cannot replay offline.

    Its freshness contract is therefore provenance: the tracked bytes must be
    exactly the producer's serialization, valid, and dated like its README.
    """

    ROOT = CLI.parents[2]
    LEDGER = "docs/90.references/data/0096-workspace-inventory/data.yaml"
    README = "docs/90.references/data/0096-workspace-inventory/README.md"

    def staged(self, edit=None, readme_edit=None):
        tmp = tempfile.TemporaryDirectory(prefix="snapshot ")
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for relative, change in ((self.LEDGER, edit), (self.README, readme_edit)):
            text = (self.ROOT / relative).read_text()
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(change(text) if change else text)
        return root

    def check(self, root):
        from scripts.lib.ops.workspace_inventory import check_published

        return check_published(root, self.LEDGER, self.README)

    def test_committed_snapshot_is_current_with_its_producer_contract(self):
        self.assertTrue(self.check(self.ROOT))

    def test_stale_or_hand_edited_snapshot_is_rejected(self):
        from scripts.lib.ops.workspace_inventory import InventoryError

        cases = {
            "non-canonical bytes": lambda t: t.replace(
                "schema_version: 1\n", "schema_version:   1\n", 1
            ),
            "unparsed trailing hand edit": lambda t: t + "\n",
            "moved observation date": lambda t: t.replace(
                "observed_at: '2026-11-07", "observed_at: '2026-11-01", 1
            ),
            "forged head": lambda t: t.replace(
                "head: 52556b386d2dee1b5d06923354e69df8c04e1e1d", "head: nothex", 1
            ),
            "broken coverage": lambda t: t.replace(
                "coverage:\n", "coverage:\n  forged: true\n", 1
            ),
        }
        for name, edit in cases.items():
            with self.subTest(name):
                with self.assertRaises(InventoryError):
                    self.check(self.staged(edit))

    def test_readme_date_must_match_the_observation(self):
        from scripts.lib.ops.workspace_inventory import InventoryError

        root = self.staged(
            readme_edit=lambda t: t.replace(
                'observed_at: "2026-11-07"', 'observed_at: "2026-11-08"', 1
            )
        )
        with self.assertRaises(InventoryError):
            self.check(root)

    def test_cli_check_exits_nonzero_on_a_stale_snapshot(self):
        good = subprocess.run(
            [sys.executable, str(CLI), "check", "--root", str(self.ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(good.returncode, 0, good.stderr)
        root = self.staged(lambda t: t + "\n")
        bad = subprocess.run(
            [sys.executable, str(CLI), "check", "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main()
