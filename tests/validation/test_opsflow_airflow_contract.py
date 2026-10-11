"""Synthetic registration and overlay contracts; native acceptance is separate."""

import builtins
import io
import socket
import sys
import types
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

import yaml

WORKLOAD = (
    Path(__file__).resolve().parents[2]
    / "infra/07-workflow/airflow/workloads/manifest-pipeline"
)


class OverlayLoader(yaml.SafeLoader):
    pass


OverlayLoader.add_constructor("!reset", lambda loader, node: None)


class AirflowContractTests(unittest.TestCase):
    def register(self):
        source = (WORKLOAD / "dags/source_manifest_ingest.py").read_text()
        declarations = {"tasks": []}
        sdk = types.ModuleType("airflow.sdk")
        sdk.Param = lambda default, **rules: {"default": default, **rules}
        sdk.get_current_context = lambda: (_ for _ in ()).throw(
            AssertionError("parse_context_io")
        )

        def dag(**settings):
            declarations["dag"] = settings
            return lambda function: function

        def task(**settings):
            def decorate(function):
                declarations["tasks"].append((settings, function))
                return lambda: None

            return decorate

        sdk.dag, sdk.task = dag, task
        airflow = types.ModuleType("airflow")
        airflow.sdk = sdk
        # Preserve the source filename for coverage while the SDK remains a double.
        code = compile(source, str(WORKLOAD / "dags/source_manifest_ingest.py"), "exec")
        with patch.dict(sys.modules, {"airflow": airflow, "airflow.sdk": sdk}):
            with (
                patch.object(
                    builtins, "open", side_effect=AssertionError("parse_file_io")
                ),
                patch.object(io, "open", side_effect=AssertionError("parse_file_io")),
            ):
                with patch("os.open", side_effect=AssertionError("parse_file_io")):
                    with patch.object(
                        socket,
                        "create_connection",
                        side_effect=AssertionError("parse_network_io"),
                    ):
                        exec(code, {})
        return source, declarations

    def test_registration_is_io_free_manual_paused_and_bounded(self):
        _, value = self.register()
        settings = value["dag"]
        self.assertEqual(settings["dag_id"], "source_manifest_ingest")
        self.assertIsNone(settings["schedule"])
        self.assertTrue(settings["is_paused_upon_creation"])
        self.assertFalse(settings["catchup"])
        self.assertEqual(settings["max_active_runs"], 1)
        self.assertEqual(settings["max_active_tasks"], 1)
        self.assertEqual(len(value["tasks"]), 1)
        task_settings = value["tasks"][0][0]
        self.assertEqual(task_settings["pool"], "manifest_ingest")
        self.assertEqual(task_settings["pool_slots"], 1)
        self.assertEqual(task_settings["execution_timeout"], timedelta(minutes=3))
        self.assertFalse(task_settings["show_return_value_in_logs"])
        self.assertFalse(task_settings["multiple_outputs"])
        defaults = settings["default_args"]
        self.assertEqual(defaults["retries"], 2)
        self.assertTrue(defaults["retry_exponential_backoff"])
        self.assertLessEqual(defaults["max_retry_delay"], timedelta(minutes=5))

    def test_public_sdk_and_lazy_adapters(self):
        source, _ = self.register()
        self.assertIn("from airflow.sdk import", source)
        self.assertNotIn("airflow.models", source)
        self.assertNotIn("sqlalchemy", source)
        self.assertNotIn("smtp", source.lower())
        task_line = source.index("def validate_store_publish")
        self.assertGreater(source.index("from workflow_lib.adapters import"), task_line)

    def run_task(self, failure=None):
        _, value = self.register()
        function = value["tasks"][0][1]
        function.__globals__["get_current_context"] = lambda: {
            "params": {"source": "hy-home.docker", "business_date": "2026-10-10"}
        }
        calls = []
        adapters = types.ModuleType("workflow_lib.adapters")
        manifest = types.ModuleType("workflow_lib.manifest")

        def read_config(path, *, schema):
            calls.append(("file", path, schema))
            if failure:
                raise ValueError(failure)
            return {"synthetic": schema}

        adapters.read_private_json = read_config
        adapters.S3Store = lambda config: "synthetic_store"
        adapters.PgPublisher = lambda config: "synthetic_publisher"
        manifest.ingest = lambda store, publisher, source, day: {
            "run_id": "a" * 64,
            "status": "published",
            "records": 1,
        }
        package = types.ModuleType("workflow_lib")
        package.__path__ = []
        with patch.dict(
            sys.modules,
            {
                "workflow_lib": package,
                "workflow_lib.adapters": adapters,
                "workflow_lib.manifest": manifest,
            },
        ):
            return function(), calls

    def test_task_reads_only_two_ingest_configs_and_returns_bounded_metadata(self):
        result, calls = self.run_task()
        self.assertEqual(
            calls,
            [
                ("file", "/run/opsflow/s3.json", "s3"),
                ("file", "/run/opsflow/pg.json", "pg"),
            ],
        )
        self.assertEqual(set(result), {"run_id", "status", "records"})

    def test_task_sanitizes_driver_failure_before_airflow_records_it(self):
        with self.assertRaises(RuntimeError) as caught:
            self.run_task("synthetic-private-error")
        self.assertEqual(str(caught.exception), "manifest_task_failed")
        self.assertTrue(caught.exception.__suppress_context__)

    def test_overlay_preserves_roles_and_worker_only_access(self):
        overlay = yaml.load(
            (WORKLOAD / "compose.workflow.override.yml").read_text(),
            Loader=OverlayLoader,
        )
        roles = {
            "airflow-apiserver",
            "airflow-scheduler",
            "airflow-dag-processor",
            "airflow-worker",
            "airflow-triggerer",
            "airflow-init",
            "flower",
        }
        self.assertEqual(set(overlay["services"]), roles)
        for role, model in overlay["services"].items():
            self.assertEqual(model["image"], "${OPSFLOW_AIRFLOW_IMAGE:?}")
            self.assertIsNone(model["build"])
            self.assertEqual(model["pull_policy"], "never")
            for key in ("user", "command", "entrypoint"):
                self.assertNotIn(key, model)
            mounts = model.get("volumes", [])
            self.assertEqual(
                sum(mount["target"] == "/run/opsflow" for mount in mounts),
                int(role == "airflow-worker"),
            )
            for mount in mounts:
                self.assertTrue(mount["read_only"])
                self.assertFalse(mount["bind"]["create_host_path"])
            if role == "airflow-worker":
                self.assertEqual(set(model["networks"]), {"dev_data_net", "object_net"})
                self.assertNotIn("secrets", model)
            else:
                self.assertNotIn("networks", model)
        self.assertNotIn("networks", overlay)
        self.assertNotIn("secrets", overlay)


if __name__ == "__main__":
    unittest.main()
