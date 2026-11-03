"""The single default route must not lose a finding the four modes produced."""

from __future__ import annotations

import contextlib
import io
import unittest
from unittest import mock

from scripts.lib.document_governance.lifecycle.contract import Finding
from tests.validation.lifecycle._support import lifecycle

SPEC_FINDING = Finding("docs/03.specs/0000-fixture/spec.md", "spec-sentinel", "x")


class LifecycleRouteEquivalenceTests(unittest.TestCase):
    """The default route emits the Spec Package and occupancy finding sources.

    A clean tree produces no findings at all, so each source is stubbed with a
    distinct sentinel instead, which fails if the default drops one. Stage 98
    archive records are not validated by this route.
    """

    def _run_default(self) -> str:
        output = io.StringIO()
        with (
            mock.patch.object(
                lifecycle,
                "_spec_package_lifecycle_findings",
                return_value=[SPEC_FINDING],
            ),
            mock.patch.object(
                lifecycle,
                "run_occupancy",
                side_effect=lambda root: print("occupancy-sentinel: stub") or 1,
            ),
            contextlib.redirect_stdout(output),
        ):
            code = lifecycle.main([])
        self.assertNotEqual(0, code, "seeded findings must fail the route")
        return output.getvalue()

    def test_default_route_emits_every_finding_source(self) -> None:
        rendered = self._run_default()
        for code in ("spec-sentinel", "occupancy-sentinel"):
            with self.subTest(code=code):
                self.assertIn(code, rendered)

    def test_default_route_is_the_only_lifecycle_cli_shape(self) -> None:
        self.assertFalse(
            hasattr(lifecycle, "MODES") and lifecycle.MODES,
            "the lifecycle CLI must expose no mode inventory",
        )
        parser = lifecycle._parser()
        options = {
            option for action in parser._actions for option in action.option_strings
        }
        for removed in ("--mode", "--wave", "--manifest", "--exceptions", "--output"):
            with self.subTest(option=removed):
                self.assertNotIn(removed, options)
