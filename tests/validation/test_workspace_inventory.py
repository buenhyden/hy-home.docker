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


if __name__ == "__main__":
    unittest.main()
