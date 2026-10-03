"""Static contract checks for SPEC-0203 quality telemetry."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOY = ROOT / "infra/06-observability/alloy/config/config.home.alloy"
K6_DASHBOARD = ROOT / "infra/06-observability/grafana/dashboards/Infrastructure/k6.json"
GRAFANA_README = ROOT / "infra/06-observability/grafana/README.md"


class QualityObservabilityContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = ALLOY.read_text(encoding="utf-8")
        cls.dashboard = json.loads(K6_DASHBOARD.read_text(encoding="utf-8"))

    def test_otlp_metrics_reuse_receiver_without_changing_trace_path(self) -> None:
        self.assertIn(
            "metrics = [otelcol.processor.transform.quality_metrics.input]",
            self.config,
        )
        self.assertIn("traces  = [otelcol.processor.batch.default.input]", self.config)
        self.assertIn("traces = [otelcol.exporter.otlp.tempo.input]", self.config)

    def test_metric_labels_are_allowlisted_and_required(self) -> None:
        self.assertIn(
            'keep_keys(attributes, ["project_id", "environment", "service_name"])',
            self.config,
        )
        self.assertIn(
            'source_labels = ["project_id", "environment", "service_name"]',
            self.config,
        )
        self.assertIn(
            'regex  = "__name__|project_id|environment|service_name|le|quantile"',
            self.config,
        )
        self.assertNotIn("resource_to_telemetry_conversion = true", self.config)

    def test_batches_and_remote_write_queue_are_bounded(self) -> None:
        for setting in (
            'max_stale   = "5m"',
            "max_streams = 10000",
            "send_batch_max_size = 1024",
            "max_cache_size = 2048",
            "capacity             = 5000",
            "max_shards           = 2",
            'sample_age_limit     = "5m"',
        ):
            self.assertIn(setting, self.config)
        self.assertIn('url = "http://prometheus:9090/api/v1/write"', self.config)

    def test_delta_temporality_conversion_is_explicitly_enabled(self) -> None:
        compose = (ROOT / "infra/06-observability/docker-compose.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "metrics = [otelcol.processor.deltatocumulative.quality_metrics.input]",
            self.config,
        )
        self.assertIn(
            "metrics = [otelcol.processor.batch.quality_metrics.input]",
            self.config,
        )
        self.assertIn("--stability.level=experimental", compose)

    def test_k6_dashboard_filters_every_query_by_run_identity(self) -> None:
        variables = {
            item["name"]: item
            for item in self.dashboard["templating"]["list"]
            if "name" in item
        }
        self.assertTrue(
            {"project_id", "run_id", "attempt", "testid"} <= variables.keys()
        )
        for name in ("project_id", "run_id", "attempt", "testid"):
            self.assertEqual(".*", variables[name].get("allValue"))

        expressions = [
            target["expr"]
            for panel in self.dashboard["panels"]
            for target in panel.get("targets", [])
            if "k6_" in target.get("expr", "")
        ]
        self.assertTrue(expressions)
        for expression in expressions:
            with self.subTest(expression=expression):
                self.assertIn('project_id=~"$project_id"', expression)
                self.assertIn('run_id=~"$run_id"', expression)
                self.assertIn('attempt=~"$attempt"', expression)
                self.assertIn('testid=~"$testid"', expression)

    def test_k6_dashboard_does_not_average_reported_percentiles(self) -> None:
        expressions = [
            target["expr"]
            for panel in self.dashboard["panels"]
            for target in panel.get("targets", [])
            if "k6_" in target.get("expr", "")
        ]

        for expression in expressions:
            with self.subTest(expression=expression):
                self.assertNotIn("avg(k6_http_req_duration_", expression)
                self.assertNotIn("avg by(name, method, status)", expression)

        requests_panel = next(
            panel
            for panel in self.dashboard["panels"]
            if panel.get("title") == "Requests by URL"
        )
        group_by = next(
            item
            for item in requests_panel["transformations"]
            if item["id"] == "groupBy"
        )
        fields = group_by["options"]["fields"]
        for field in ("Value #D", "Value #E"):
            self.assertEqual(["lastNotNull"], fields[field]["aggregations"])

        organize = next(
            item
            for item in requests_panel["transformations"]
            if item["id"] == "organize"
        )
        renames = organize["options"]["renameByName"]
        self.assertNotIn("Value #D (mean)", renames)
        self.assertNotIn("Value #E (mean)", renames)
        self.assertEqual("p95", renames["Value #D (lastNotNull)"])
        self.assertEqual("p99", renames["Value #E (lastNotNull)"])

    def test_perf_results_use_rls_view_and_sql_literal_filters(self) -> None:
        dashboard = json.loads((K6_DASHBOARD.parent / "perf-results.json").read_text())
        variables = {v["name"]: v for v in dashboard["templating"]["list"]}
        self.assertEqual("datasource", variables["DS_PERF_DB"]["type"])
        self.assertEqual({}, variables["DS_PERF_DB"]["current"])
        self.assertEqual("", variables["project_id"]["current"]["value"])
        for panel in dashboard["panels"]:
            sql = panel["targets"][0]["rawSql"]
            self.assertIn("quality.run_results", sql)
            self.assertIn("LIMIT 500", sql)
            self.assertNotIn("*' IN (${project_id", sql)
            for name in ("project_id", "run_id", "attempt"):
                self.assertIn("${" + name + ":sqlstring}", sql)
            self.assertNotIn("${project_id:raw}", sql)
        queries = "\n".join(p["targets"][0]["rawSql"] for p in dashboard["panels"])
        for required in (
            "evidence_state", "official_verdict", "object_ref",
            "baseline_values", "baseline_run_id:sqlstring",
        ):
            self.assertIn(required, queries)

    def test_perf_datasource_example_is_not_automatically_provisioned(self) -> None:
        import yaml
        contract = (
            ROOT / "infra/06-observability/grafana/provisioning/contracts"
            / "perf-db.datasource.yml.example"
        )
        datasource = yaml.safe_load(contract.read_text())["datasources"][0]
        self.assertEqual("perf_db", datasource["jsonData"]["database"])
        self.assertEqual(2, datasource["jsonData"]["maxOpenConns"])
        self.assertNotEqual("datasources", contract.parent.name)
        self.assertTrue(contract.name.endswith(".example"))
        self.assertIn("PERF_DB_READER_LOGIN", datasource["user"])
        self.assertNotIn("perf_owner", contract.read_text())
        active = (contract.parent.parent / "datasources/datasource.yml").read_text()
        self.assertNotIn("perf_db", active)

    def test_synthetic_metrics_fixture_reuses_exact_bounded_source(self) -> None:
        import importlib.util
        fixture = ROOT / "examples/operations/quality-metrics"
        spec = importlib.util.spec_from_file_location("metrics_acceptance", fixture / "acceptance.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        extracted = module.metrics_config(self.config)
        start = self.config.index('otelcol.processor.transform "quality_metrics" {')
        end = self.config.index('/*****************************************************************', start)
        self.assertTrue(extracted.startswith(self.config[start:end]))
        self.assertNotIn("discovery.docker", extracted)
        self.assertNotIn("tempo", extracted)
        import yaml
        model = yaml.safe_load((fixture / "docker-compose.yml").read_text())
        self.assertTrue(model["networks"]["metrics"]["internal"])
        self.assertNotIn("volumes", model)
        self.assertNotIn("secrets", model)
        for service in model["services"].values():
            self.assertNotIn("ports", service)
            self.assertNotIn("container_name", service)
            self.assertTrue(service["read_only"])
            self.assertEqual(["ALL"], service["cap_drop"])
            self.assertIn("mem_limit", service)
            self.assertIn("cpus", service)

    def test_locust_lab_is_not_claimed_as_root_observability_coverage(self) -> None:
        readme = GRAFANA_README.read_text(encoding="utf-8")
        self.assertNotIn("| 11-quality | `locust-master` |", readme)
        self.assertNotIn("| 11-quality | `locust-worker` |", readme)
        self.assertIn("`lab-locust-master`", readme)
        self.assertIn("`lab-locust-worker`", readme)
        self.assertIn("`hy-home-infra`만 유지", readme)


if __name__ == "__main__":
    unittest.main()
