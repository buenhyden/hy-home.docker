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

    def test_quality_metrics_use_only_the_authenticated_receiver(self) -> None:
        receiver = self.config.index('otelcol.receiver.otlp "quality" {')
        block = self.config[receiver : self.config.index("\n}\n", receiver)]
        self.assertIn("auth     = otelcol.auth.bearer.quality.handler", block)
        self.assertIn('endpoint = "0.0.0.0:4319"', block)
        self.assertIn(
            "metrics = [otelcol.processor.transform.quality_metrics.input]", block
        )
        self.assertEqual(
            1,
            self.config.count(
                "metrics = [otelcol.processor.transform.quality_metrics.input]"
            ),
        )
        self.assertIn('filename  = "/run/secrets/quality_otlp_token"', self.config)
        default = self.config.index('otelcol.receiver.otlp "default" {')
        default_block = self.config[default : self.config.index("\n}\n", default)]
        self.assertNotIn("metrics", default_block.split("output {")[1])
        self.assertIn("traces = [otelcol.processor.batch.default.input]", default_block)
        self.assertIn("traces = [otelcol.exporter.otlp.tempo.input]", self.config)
        compose = (ROOT / "infra/06-observability/docker-compose.yml").read_text()
        self.assertNotIn(
            "4319", compose.split("    ports:")[1].split("    depends_on:")[0]
        )

    def test_metric_labels_are_allowlisted_and_required(self) -> None:
        # Rate condition, response class and producer instance must reach
        # delta-to-cumulative; unbounded names and URLs must not (SPEC-0214).
        self.assertIn(
            'keep_keys(attributes, ["project_id", "environment", "service_name", '
            '"condition", "expected_response", "method", "status", "scenario"])',
            self.config,
        )
        self.assertIn('"service.instance.id"])', self.config)
        for unbounded in ('"name"', '"url"', '"user_id"'):
            self.assertNotIn(unbounded + ",", self.config.split("keep_keys")[2])
        self.assertIn(
            'source_labels = ["project_id", "environment", "service_name"]',
            self.config,
        )
        self.assertIn(
            'regex  = "__name__|project_id|environment|service_name|instance|'
            'condition|expected_response|method|status|scenario|le|quantile"',
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

    def k6_expressions(self):
        stack = list(self.dashboard["panels"])
        while stack:
            panel = stack.pop()
            stack.extend(panel.get("panels", []))
            for target in panel.get("targets", []) or []:
                if "k6_" in target.get("expr", ""):
                    yield panel, target["expr"]

    def test_k6_dashboard_filters_every_query_by_run_identity(self) -> None:
        # The OTLP path carries the run as instance "<run_id>-a<attempt>"
        # (executor resource attributes); run_id/attempt/testid tags are
        # dropped by the bounded label allowlist (SPEC-0214).
        variables = {
            item["name"]: item
            for item in self.dashboard["templating"]["list"]
            if "name" in item
        }
        self.assertTrue({"project_id", "instance", "quantile"} <= variables.keys())
        self.assertFalse({"run_id", "attempt", "testid"} & variables.keys())
        self.assertEqual(".*", variables["instance"].get("allValue"))
        expressions = [expression for _, expression in self.k6_expressions()]
        self.assertTrue(expressions)
        for expression in expressions:
            with self.subTest(expression=expression):
                self.assertIn('project_id=~"$project_id"', expression)
                self.assertIn('instance=~"$instance"', expression)
                self.assertNotIn("run_id", expression)

    def test_k6_dashboard_shows_millisecond_trends_with_live_variables(self) -> None:
        # OTLP trends arrive as *_milliseconds histograms, so a seconds unit
        # would mislabel every latency panel by 1000x.
        text = json.dumps(self.dashboard)
        self.assertNotIn("$quantile_stat", text)
        self.assertNotRegex(text, r'"(unit|value)": "s"')

    def test_k6_dashboard_does_not_average_reported_percentiles(self) -> None:
        for _, expression in self.k6_expressions():
            with self.subTest(expression=expression):
                self.assertNotIn("avg(k6_http_req_duration_", expression)
                self.assertNotIn("_$quantile_stat", expression)
                if "_milliseconds_bucket" in expression:
                    self.assertTrue(expression.startswith("histogram_quantile("))
                    self.assertIn("sum by (le", expression)
        failed = [
            expression
            for _, expression in self.k6_expressions()
            if "k6_http_req_failed_total" in expression
        ]
        self.assertTrue(failed)
        for expression in failed:
            self.assertIn('condition="nonzero"', expression)
        requests_panel = next(
            panel
            for panel, _ in self.k6_expressions()
            if panel.get("title") == "Requests by method and status"
        )
        group_by = next(
            item
            for item in requests_panel["transformations"]
            if item["id"] == "groupBy"
        )
        fields = group_by["options"]["fields"]
        self.assertNotIn("name", fields)
        for field in ("Value #B", "Value #C", "Value #D", "Value #E"):
            self.assertEqual(["lastNotNull"], fields[field]["aggregations"])

    def test_relay_egress_network_reaches_only_alloy_internally(self) -> None:
        # A per-run relay joins this network and its run network only; being
        # internal, it gives the relay no route beyond HOME Alloy.
        root = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        block = root[root.index("  quality_otlp_net:") :].split("\n  project_net:")[0]
        self.assertIn("internal: true", block)
        self.assertIn("subnet: 10.250.17.0/24", block)
        observability = (ROOT / "infra/06-observability/docker-compose.yml").read_text(
            encoding="utf-8"
        )
        alloy = observability[observability.index("\n  alloy:") :].split(
            "\n  grafana:"
        )[0]
        self.assertIn("quality_otlp_net: {}", alloy)
        self.assertEqual(1, observability.count("quality_otlp_net: {}"))

    def test_k6_dashboard_separates_absent_from_zero(self) -> None:
        # k6 sends dropped_iterations and checks only once one occurs or a
        # check exists, so "no series" must not read as 0 or as 0% passing.
        panels = {panel["title"]: panel for panel, _ in self.k6_expressions()}
        dropped = [
            expression
            for _, expression in self.k6_expressions()
            if "k6_dropped_iterations_total" in expression
        ]
        self.assertEqual(1, len(dropped))
        self.assertIn("or (0 * sum(k6_iterations_total{", dropped[0])
        checks = panels["Checks Success Rate (aggregate individual checks)"]
        self.assertEqual(
            "No checks reported", checks["fieldConfig"]["defaults"]["noValue"]
        )

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
            "evidence_state",
            "official_verdict",
            "object_ref",
            "baseline_values",
            "baseline_run_id:sqlstring",
        ):
            self.assertIn(required, queries)

    def test_perf_datasource_example_is_not_automatically_provisioned(self) -> None:
        import yaml

        contract = (
            ROOT
            / "infra/06-observability/grafana/provisioning/contracts"
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
        spec = importlib.util.spec_from_file_location(
            "metrics_acceptance", fixture / "acceptance.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        extracted = module.metrics_config(self.config)
        start = self.config.index('otelcol.processor.transform "quality_metrics" {')
        end = self.config.index(
            "/*****************************************************************", start
        )
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


HERMES_DASHBOARD = (
    ROOT / "infra/06-observability/grafana/dashboards/Applications/hermes-research.json"
)
HERMES_SECRET = "hermes_otlp_token"


class HermesObservabilityContractTest(unittest.TestCase):
    """Host-run Hermes exports OTLP over an authenticated, loopback-only path."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = ALLOY.read_text(encoding="utf-8")
        cls.compose = (ROOT / "infra/06-observability/docker-compose.yml").read_text(
            encoding="utf-8"
        )

    def block(self, header: str) -> str:
        start = self.config.index(header)
        return self.config[start : self.config.index("\n}\n", start)]

    def test_receiver_requires_the_bearer_token_and_fans_out_by_signal(self) -> None:
        self.assertIn('filename  = "/run/secrets/hermes_otlp_token"', self.config)
        self.assertIn(
            "token = local.file.hermes_otlp_token.content",
            self.block('otelcol.auth.bearer "hermes" {'),
        )
        receiver = self.block('otelcol.receiver.otlp "hermes" {')
        self.assertIn("auth     = otelcol.auth.bearer.hermes.handler", receiver)
        self.assertIn('endpoint = "0.0.0.0:4320"', receiver)
        self.assertNotIn("grpc", receiver)
        self.assertIn("traces  = [otelcol.processor.batch.default.input]", receiver)
        self.assertIn(
            "logs    = [otelcol.processor.transform.hermes_logs.input]", receiver
        )
        self.assertIn(
            "metrics = [otelcol.processor.transform.hermes_metrics.input]", receiver
        )
        # The unauthenticated 4317/4318 receiver still carries traces only.
        default = self.block('otelcol.receiver.otlp "default" {')
        self.assertNotIn("hermes", default)
        self.assertNotIn("logs", default.split("output {")[1])

    def test_logs_reach_loki_and_metrics_are_bounded_and_identity_checked(self) -> None:
        self.assertIn(
            'set(attributes["loki.resource.labels"], "service.name")',
            self.block('otelcol.processor.transform "hermes_logs" {'),
        )
        self.assertIn(
            "forward_to = [loki.write.local_loki.receiver]",
            self.block('otelcol.exporter.loki "hermes" {'),
        )
        transform = self.block('otelcol.processor.transform "hermes_metrics" {')
        self.assertIn(
            'keep_keys(attributes, ["service_name", "status", "outcome", "job_kind"])',
            transform,
        )
        self.assertIn("otelcol.processor.batch.hermes_metrics.input", transform)
        self.assertIn(
            "otelcol.exporter.prometheus.hermes_metrics.input",
            self.block('otelcol.processor.batch "hermes_metrics" {'),
        )
        self.assertIn(
            "prometheus.relabel.hermes_metrics.receiver",
            self.block('otelcol.exporter.prometheus "hermes_metrics" {'),
        )
        relabel = self.block('prometheus.relabel "hermes_metrics" {')
        self.assertIn('source_labels = ["service_name"]', relabel)
        self.assertIn('regex         = "hermes"', relabel)
        self.assertIn('action = "labelkeep"', relabel)
        self.assertIn("max_cache_size = 2048", relabel)
        self.assertIn(
            "forward_to     = [prometheus.remote_write.local_prometheus.receiver]",
            relabel,
        )
        for unbounded in ("trace_id", "span_id", "session", "user"):
            self.assertNotIn(unbounded, relabel)

    def test_compose_publishes_only_on_loopback_with_the_secret(self) -> None:
        self.assertIn(
            "'127.0.0.1:${ALLOY_HERMES_OTLP_HOST_PORT:-4320}:4320'", self.compose
        )
        self.assertIn(f"      - {HERMES_SECRET}\n", self.compose)
        root = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn(
            f"  {HERMES_SECRET}:\n    file: ./secrets/observability/alloy/"
            f"{HERMES_SECRET}.txt\n",
            root,
        )

    def test_secret_is_catalogued(self) -> None:
        catalog = json.loads(
            (ROOT / "infra/03-security/openbao/secret-catalog.json").read_text()
        )
        rows = [
            entry
            for entry in catalog["entries"]
            if entry.get("source_path")
            == f"secrets/observability/alloy/{HERMES_SECRET}.txt"
        ]
        self.assertEqual(["OBS-016"], [row["id"] for row in rows])
        self.assertEqual("Token", rows[0]["value_type"])

    def test_dashboard_has_loki_logs_and_tempo_trace_panels(self) -> None:
        panels = json.loads(HERMES_DASHBOARD.read_text(encoding="utf-8"))["panels"]
        logs = [p for p in panels if p["type"] == "logs"]
        traces = [p for p in panels if p["datasource"]["uid"] == "Tempo"]
        self.assertEqual(1, len(logs))
        self.assertEqual({"type": "loki", "uid": "Loki"}, logs[0]["datasource"])
        self.assertEqual('{service_name="hermes"}', logs[0]["targets"][0]["expr"])
        self.assertEqual(1, len(traces))
        target = traces[0]["targets"][0]
        self.assertEqual({"type": "tempo", "uid": "Tempo"}, target["datasource"])
        self.assertEqual("traceql", target["queryType"])
        self.assertIn('resource.service.name = "hermes"', target["query"])


if __name__ == "__main__":
    unittest.main()
