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
    def test_k6_delivery_rehearsal_consumes_the_current_candidate(self):
        spec = importlib.util.spec_from_file_location(
            "sec01_quality_delivery_candidate",
            ROOT / "examples/operations/quality-metrics/acceptance.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(K6.split("@", 1)[0], module.STAGE_TAGS["k6"])

    def test_current_public_refresh_keeps_followups_and_pending_evidence_exact(self):
        updates = json.loads(
            (
                ROOT / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        releases = json.loads(
            (
                ROOT / "infra/09-platform-ops/security-updates/release-lookups.json"
            ).read_text()
        )["coordinator_current_public_refresh"]
        images = json.loads(
            (
                ROOT
                / "infra/09-platform-ops/security-updates/image-source-lookups.json"
            ).read_text()
        )["coordinator_current_public_refresh"]
        receipt = releases["receipt_sha256"]
        refresh = updates["source_refreshes"][-1]
        self.assertEqual(refresh["public_metadata_receipt_sha256"], receipt)
        self.assertEqual(images["receipt_sha256"], receipt)
        self.assertEqual(images["source_revision"], refresh["source_revision"])
        self.assertEqual(releases["source_revision"], refresh["source_revision"])
        self.assertIn("signatures not verified", images["trust"])

        selected = set(refresh["updated_services"])
        selected_rows = [
            row for row in updates["entries"] if row["service"] in selected
        ]
        self.assertEqual(len(selected_rows), len(selected))
        rows = {row["service"]: row for row in selected_rows}
        self.assertEqual(set(rows), selected)
        for service, row in rows.items():
            with self.subTest(service=service, field="pending_evidence"):
                self.assertEqual(row["source_refreshed_at"], refresh["refreshed_at"])
                self.assertEqual(row["signature"], "NOT_RUN")
                self.assertEqual(row["sbom_scan"], "NOT_RUN")
                self.assertEqual(row["deployment"], "NOT_RUN")
                self.assertIn("does not prove HOME rollout", row["runtime_refresh"])
        self.assertEqual(updates["delivery_preconditions"]["home_rollout"], "NOT_RUN")

        custom_services = {
            "great-expectations",
            "k6",
            "oauth2-proxy",
            "opentofu",
            "tempo",
        }
        self.assertLessEqual(custom_services, selected)
        for service in custom_services:
            with self.subTest(service=service, field="custom_digest"):
                row = rows[service]
                self.assertEqual(row["target_index_digest"], "UNKNOWN")
                self.assertEqual(row["target_manifest_digest"], "UNKNOWN")
                self.assertEqual(row["target_config_digest"], "UNKNOWN")
                self.assertTrue(row["target_declared_digest"].startswith("UNKNOWN:"))

        exporters = [
            record
            for record in images["records"]
            if record["repository"] == "oliver006/redis_exporter"
        ]
        self.assertEqual(len(exporters), 1)
        exporter = exporters[0]
        for service in selected - custom_services:
            with self.subTest(service=service, field="exporter_digests"):
                row = rows[service]
                self.assertEqual(row["target_index_digest"], exporter["index_digest"])
                self.assertEqual(
                    row["target_manifest_digest"],
                    exporter["platform_manifest_digest"],
                )
                self.assertEqual(row["target_config_digest"], exporter["config_digest"])
                self.assertEqual(
                    len(
                        {
                            row["target_index_digest"],
                            row["target_manifest_digest"],
                            row["target_config_digest"],
                        }
                    ),
                    3,
                )

        for service in ("great-expectations", "opentofu"):
            with self.subTest(service=service, field="followup_image"):
                row = rows[service]
                self.assertEqual(
                    row["next_fact_command"],
                    [
                        "docker",
                        "image",
                        "inspect",
                        "--platform",
                        "linux/amd64",
                        row["target_source_image"],
                        "--format",
                        "{{.Id}} {{.Architecture}}",
                    ],
                )
        self.assertEqual(
            rows["k6"]["next_fact_command"],
            [
                "git",
                "show",
                refresh["source_revision"] + ":infra/11-quality/k6/Dockerfile",
            ],
        )

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
