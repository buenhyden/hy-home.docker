"""Next SEC01 CLI candidates: source and synthetic checks, never runtime proof."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
GX = ROOT / "infra/12-analytics/great-expectations"
TOFU = "ghcr.io/opentofu/opentofu:1.13.1-minimal@sha256:dfbc3f0a8bed0adfa2cf49ff418f158afe24080eea6d6e748db8799fc4553db6"
K6 = "grafana/k6:2.3.0@sha256:9c2dee7f8ed74d317e4027c06a10f169b625638189de8d4555d0b3486a5aeb34"


def services(path):
    return yaml.safe_load((ROOT / path).read_text())["services"]


def gx_wrapper():
    spec = importlib.util.spec_from_file_location(
        "sec01_gx_fixture", GX / "hyhome-gx.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NextToolCandidates(unittest.TestCase):
    def test_tofu_effective_inline_build_and_local_tag_agree(self):
        service = services("infra/09-platform-ops/opentofu/docker-compose.yml")[
            "opentofu"
        ]
        self.assertEqual(
            service["build"]["dockerfile_inline"].splitlines()[0],
            "FROM " + TOFU + " AS tofu",
        )
        self.assertEqual(service["image"], "hy-home/opentofu:1.13.1-local")
        self.assertIn(
            "COPY --from=tofu /usr/local/bin/tofu /usr/local/bin/tofu",
            service["build"]["dockerfile_inline"],
        )
        self.assertEqual(service["entrypoint"], ["tofu"])
        self.assertEqual(service["restart"], "no")
        self.assertEqual(service["working_dir"], "/workspace")
        self.assertEqual(
            service["volumes"],
            [
                "./workspace:/workspace:rw",
                "$HOME/.aws:/root/.aws:ro",
                "$HOME/.azure:/root/.azure:ro",
            ],
        )
        self.assertNotIn("command", service)

    def test_gx_requirements_and_local_image_share_candidate(self):
        lines = (GX / "requirements.txt").read_text().splitlines()
        self.assertEqual(
            lines, ["great-expectations==1.24.0", "trino[sqlalchemy]==0.340.0"]
        )
        service = services("infra/12-analytics/great-expectations/docker-compose.yml")[
            "great-expectations"
        ]
        self.assertEqual(service["image"], "hy-home/great-expectations:1.24.0-local")
        self.assertEqual(service["command"], ["list"])
        self.assertEqual(service["environment"]["GX_ANALYTICS_ENABLED"], "false")
        self.assertEqual(service["environment"]["HOME"], "/tmp")
        self.assertEqual(service["volumes"], ["./suites:/opt/hyhome/suites:ro"])
        dockerfile = (GX / "Dockerfile").read_text()
        self.assertIn("COPY requirements.txt /tmp/requirements.txt", dockerfile)
        self.assertIn("pip install --no-cache-dir -r /tmp/requirements.txt", dockerfile)
        self.assertIn("USER 1000:1000", dockerfile)
        self.assertIn('ENTRYPOINT ["python3", "/usr/local/bin/hyhome-gx"]', dockerfile)

    def test_k6_immutable_source_keeps_inventory_only_job(self):
        self.assertIn(
            "FROM " + K6,
            (ROOT / "infra/11-quality/k6/Dockerfile").read_text().splitlines(),
        )
        service = services("infra/11-quality/k6/docker-compose.yml")["k6"]
        self.assertEqual(service["command"], ["version"])
        self.assertEqual(service["restart"], "no")
        self.assertIs(service["read_only"], True)
        self.assertEqual(service["volumes"], ["k6-data:/scripts:ro"])
        self.assertNotIn("ports", service)
        self.assertNotIn("environment", service)

    def test_gx_list_does_not_import_engine_or_connect(self):
        wrapper = gx_wrapper()
        with tempfile.TemporaryDirectory(prefix="sec01-gx-fixture-") as raw:
            root = Path(raw)
            (root / "synthetic.json").write_text(
                json.dumps({"table": "fixture.rows", "expectations": [{}]})
            )
            output = io.StringIO()
            with (
                patch.object(wrapper, "SUITES", root),
                patch.object(
                    wrapper,
                    "validate",
                    side_effect=AssertionError("inventory must not validate"),
                ),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(wrapper.main(["list"]), 0)
            self.assertEqual(output.getvalue(), "synthetic\n")

    def test_gx_bad_suite_and_empty_inventory_fail_before_engine(self):
        wrapper = gx_wrapper()
        with tempfile.TemporaryDirectory(prefix="sec01-gx-fixture-") as raw:
            root = Path(raw)
            for contents in (
                None,
                {"table": "missing-schema", "expectations": [{}]},
                {"table": "fixture.rows", "expectations": []},
            ):
                if contents is not None:
                    (root / "synthetic.json").write_text(json.dumps(contents))
                with (
                    patch.object(wrapper, "SUITES", root),
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit) as caught,
                ):
                    if contents is None:
                        wrapper.main(["list"])
                    else:
                        wrapper.load("synthetic")
                self.assertEqual(caught.exception.code, 2)

    def test_gx_validation_exit_classification_and_selected_suite(self):
        wrapper = gx_wrapper()
        with tempfile.TemporaryDirectory(prefix="sec01-gx-fixture-") as raw:
            root = Path(raw)
            (root / "synthetic.json").write_text("{}")
            for outcome in (0, 1):
                with (
                    patch.object(wrapper, "SUITES", root),
                    patch.object(wrapper, "validate", return_value=outcome) as validate,
                ):
                    self.assertEqual(wrapper.main(["validate", "synthetic"]), outcome)
                    validate.assert_called_once_with(["synthetic"])
            with (
                patch.object(wrapper, "SUITES", root),
                patch.object(
                    wrapper, "validate", side_effect=RuntimeError("synthetic failure")
                ),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as caught,
            ):
                wrapper.main(["validate"])
            self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
