"""Current public lifecycle and CLI-shape tests."""

from __future__ import annotations

import contextlib
import io
import sys
import unittest

# Imported for its side effect and as the script manifest's evidence that this
# test covers that module. The entrypoint re-exports its names, so the module
# must be loaded before those attributes resolve. Not dead code.
from scripts.lib.document_governance.lifecycle import (
    public as public_module,  # noqa: F401
)
from tests.validation.lifecycle._support import (
    REGISTRY,
    ROOT,
    SCRIPT,
    lifecycle,
    run,
)


class CurrentPublicContractTests(unittest.TestCase):
    def test_cli_defaults_to_the_registry_and_has_no_mode_inventory(self) -> None:
        parser = lifecycle._parser()
        self.assertEqual(REGISTRY.resolve(), parser.parse_args([]).profiles.resolve())
        self.assertFalse(hasattr(parser.parse_args([]), "mode"))
        self.assertFalse(hasattr(lifecycle, "MODES"))

    def test_cli_misuse_fails_before_opening_repository_files(self) -> None:
        result = run(
            sys.executable,
            str(SCRIPT),
            "--mode",
            "check-contract",
            "--wave",
            "forbidden",
            "--registry",
            "/missing/profiles.yaml",
            "--contract",
            "/missing/contract.yaml",
            cwd=ROOT,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("--wave", result.stderr)
        self.assertNotIn("configuration-error", result.stderr)

    def test_default_route_reports_lifecycle_and_occupancy(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, lifecycle.main([]))
        rendered = output.getvalue()
        self.assertIn("document corpus lifecycle:", rendered)
        self.assertIn("active stage occupancy:", rendered)
