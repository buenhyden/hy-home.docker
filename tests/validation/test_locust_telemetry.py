"""Locust request-event evidence excludes private client metadata."""

import importlib.util
import unittest
from pathlib import Path

PATH = (
    Path(__file__).resolve().parents[2]
    / "examples/operations/locust-telemetry/locustfile.py"
)


class LocustTelemetryTests(unittest.TestCase):
    def test_request_event_contract_preserves_units_and_rejects_unknown_groups(self):
        spec = importlib.util.spec_from_file_location("locust_fixture", PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.record_event({}, "GET", "health", 12.5, None, 200)
        self.assertEqual(result["health:200"]["count"], 1)
        self.assertEqual(result["health:200"]["sum_ms"], 12.5)
        self.assertEqual(result["health:200"]["buckets_ms"]["25"], 1)
        with self.assertRaises(ValueError):
            module.record_event(
                {}, "GET", "http://private?token=synthetic", 12.5, None, 200
            )

    def test_invalid_time_and_unsafe_method_are_rejected(self):
        spec = importlib.util.spec_from_file_location("locust_fixture", PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for time in (float("nan"), float("inf"), -1):
            with self.assertRaises(ValueError):
                module.record_event({}, "GET", "health", time, None, 200)
        with self.assertRaises(ValueError):
            module.record_event({}, "authorization", "health", 1, None, 200)

    def test_lab_workers_and_expected_count_share_one_bounded_input(self):
        import yaml

        lab = yaml.safe_load((PATH.parents[3] / "labs/locust.yml").read_text())
        master = lab["services"]["lab-locust-master"]["command"]
        worker = lab["services"]["lab-locust-worker"]
        expected = master[master.index("--expect-workers") + 1]
        self.assertEqual("${LAB_LOCUST_EXPECT_WORKERS:-2}", expected)
        self.assertEqual(expected, worker["deploy"]["replicas"])
        self.assertEqual(
            "${LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT:-60}",
            master[master.index("--expect-workers-max-wait") + 1],
        )
        for key in ("--run-time", "--stop-timeout", "--exit-code-on-error"):
            self.assertIn(key, master)
        self.assertNotIn("--otel", master)

    def test_lab_readiness_uses_image_python_not_external_pgrep(self):
        import yaml

        lab = yaml.safe_load((PATH.parents[3] / "labs/locust.yml").read_text())
        for name in ("lab-locust-master", "lab-locust-worker"):
            self.assertEqual(
                lab["services"][name]["healthcheck"]["test"][:2], ["CMD", "python"]
            )

    def test_container_artifacts_reject_links_fifo_size_and_duplicate_sensitive_keys(
        self,
    ):
        import os
        import tempfile

        spec = importlib.util.spec_from_file_location(
            "locust_acceptance", PATH.with_name("acceptance.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "events.json"
            source.write_text('{"series":{},"series":{}}')
            with self.assertRaises(ValueError):
                module.read_evidence(source)
            link = root / "link.json"
            link.symlink_to(source)
            with self.assertRaises(ValueError):
                module.bounded_read(link, 100)
            fifo = root / "fifo"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                module.bounded_read(fifo, 100)
            source.write_bytes(b"x" * 101)
            with self.assertRaises(ValueError):
                module.bounded_read(source, 100)
            source.write_text('{"authorization":"synthetic"}')
            with self.assertRaises(ValueError):
                module.read_evidence(source)

    def test_docker_client_rejects_relative_binary_and_ambient_environment(self):
        import tempfile

        spec = importlib.util.spec_from_file_location(
            "locust_acceptance", PATH.with_name("acceptance.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                module.client_environment(Path(directory), "docker")
            env = module.client_environment(Path(directory), "/usr/bin/docker")
            self.assertEqual(set(env), {"PATH", "HOME", "DOCKER_CONFIG", "LANG"})
            self.assertTrue(Path(env["DOCKER_CONFIG"]).is_relative_to(Path(directory)))

    def test_early_preflight_failures_remove_owned_scratch(self):
        import tempfile
        from unittest import mock

        spec = importlib.util.spec_from_file_location(
            "locust_acceptance", PATH.with_name("acceptance.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for binary, locust in (
            ("docker", "locustio/locust@sha256:" + "1" * 64),
            ("/missing/docker", "locustio/locust@sha256:" + "1" * 64),
            ("/usr/bin/docker", "invalid-digest"),
        ):
            with (
                self.subTest(binary=binary, image=locust),
                tempfile.TemporaryDirectory() as parent,
            ):
                scratch = Path(parent) / "owned"
                scratch.mkdir()
                args = [
                    "acceptance",
                    "--docker-binary",
                    binary,
                    "--locust-image",
                    locust,
                    "--mock-image",
                    "wiremock/wiremock@sha256:" + "2" * 64,
                ]
                with (
                    mock.patch.object(
                        module.tempfile, "mkdtemp", return_value=str(scratch)
                    ),
                    mock.patch.object(module.sys, "argv", args),
                ):
                    with self.assertRaises((ValueError, OSError)):
                        module.main()
                self.assertFalse(scratch.exists())
