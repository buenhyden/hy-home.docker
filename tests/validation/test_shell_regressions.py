"""Run the shell regression suites that no gate reached on their own.

`scripts/manifest.yaml` names both scripts as the tests of their libraries,
but the shell-syntax gate only parses `scripts/**/*.sh`, so neither suite
ever ran. Each test executes one suite and requires its own exit status.
"""

from __future__ import annotations

import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class ShellRegressionSuiteTests(unittest.TestCase):
    def run_suite(self, relative: str) -> None:
        result = subprocess.run(
            ["bash", str(ROOT / relative)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
        self.assertEqual(
            0, result.returncode, result.stdout[-2000:] + result.stderr[-2000:]
        )

    def test_hardening_library_contract(self) -> None:
        self.run_suite("tests/validation/test_hardening_lib.sh")

    def test_agent_precommit_all_files_wrapper(self) -> None:
        self.run_suite("tests/validation/test_run_agent_precommit_all_files.sh")


if __name__ == "__main__":
    unittest.main()
