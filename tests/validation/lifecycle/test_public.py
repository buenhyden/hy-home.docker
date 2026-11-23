"""Current public lifecycle and CLI-shape tests."""

from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

# Imported for its side effect and as the script manifest's evidence that this
# test covers that module. The entrypoint re-exports its names, so the module
# must be loaded before those attributes resolve. Not dead code.
from scripts.lib.document_governance.lifecycle import (
    public as public_module,
)
from tests.validation.lifecycle._support import (
    REGISTRY,
    ROOT,
    SCRIPT,
    lifecycle,
    run,
)


class CurrentPublicContractTests(unittest.TestCase):
    def test_public_route_shares_one_snapshot_context_with_lifecycle(self) -> None:
        from scripts.lib.document_governance.registry import load_registry

        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            (root / "docs/03.specs").mkdir(parents=True)
            registry = load_registry(REGISTRY)
            with (
                mock.patch.object(
                    public_module, "load_spec_packages", return_value=()
                ) as load,
                mock.patch.object(
                    public_module,
                    "validate_repository_spec_package_lifecycle",
                    return_value=(),
                ) as validate,
            ):
                self.assertEqual(
                    [],
                    public_module._spec_package_lifecycle_findings(
                        root, {"_registry": registry}
                    ),
                )
            context = load.call_args.kwargs["_historical_context"]
            self.assertIs(context, validate.call_args.kwargs["_historical_context"])

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


class ReadinessReportTests(unittest.TestCase):
    """sdlc.md: readiness is derived on read and is never removal approval."""

    def test_readiness_flag_reports_every_package_without_gating(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, lifecycle.main(["--readiness"]))
        lines = [
            line
            for line in output.getvalue().splitlines()
            if line.startswith("readiness: ")
        ]
        self.assertTrue(any(" SPEC-0212 " in f"{line} " for line in lines), lines)
        for line in lines:
            self.assertRegex(
                line, r"^readiness: SPEC-[0-9]{4} (ready|not-ready: .+|unknown)$"
            )

    def test_readiness_reuses_the_packages_the_lifecycle_check_loaded(self):
        from unittest import mock

        from scripts.lib.document_governance import spec_packages

        with (
            mock.patch.object(
                public_module, "load_spec_packages", return_value=()
            ) as checked,
            mock.patch.object(
                public_module,
                "validate_repository_spec_package_lifecycle",
                return_value=(),
            ),
            mock.patch.object(spec_packages, "load_spec_packages") as reloaded,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(0, lifecycle.main(["--readiness"]))
        self.assertEqual(1, checked.call_count)
        reloaded.assert_not_called()

    def test_readiness_is_off_by_default(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            lifecycle.main([])
        self.assertNotIn("readiness: ", output.getvalue())

    def test_a_load_failure_reports_unavailable_without_a_traceback(self) -> None:
        from unittest import mock

        from scripts.lib.document_governance import spec_packages

        output = io.StringIO()
        with (
            mock.patch.object(
                spec_packages,
                "load_spec_packages",
                side_effect=spec_packages.SpecPackageError("broken"),
            ),
            contextlib.redirect_stdout(output),
        ):
            lifecycle._print_readiness(ROOT, None)
        self.assertEqual(
            "readiness: unavailable: Stage 03 packages did not load\n",
            output.getvalue(),
        )
