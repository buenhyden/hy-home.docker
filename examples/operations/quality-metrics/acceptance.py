"""Synthetic public-HTTP metrics delivery rehearsal; no HOME state or credentials."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "infra/06-observability/alloy/config/config.home.alloy"
COMPOSE = Path(__file__).with_name("docker-compose.yml")
TAGS = {
    "alloy": "grafana/alloy:v1.19.2",
    "prom": "prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e",
    "probe": "python:3.13.15-alpine",
}


TOKEN_PATH = "/run/secrets/quality_otlp_token"
# The k6 stage runs the real executor, relay controller and path guard.
STAGE_TAGS = {
    "k6": "grafana/k6:2.3.0",
    "guard": "traefik:v3.7.13",
    "mock": "wiremock/wiremock:3.13.2-alpine",
}
DASHBOARD = ROOT / "infra/06-observability/grafana/dashboards/Infrastructure/k6.json"


def dashboard_expressions(dashboard):
    stack = list(dashboard["panels"])
    while stack:
        panel = stack.pop()
        stack.extend(panel.get("panels", []))
        for target in panel.get("targets", []) or []:
            if "k6_" in target.get("expr", ""):
                yield target["expr"]


def metrics_config(source):
    """Use the actual bounded receiver-to-remote-write source, not a parallel implementation."""
    start = source.index('otelcol.processor.transform "quality_metrics" {')
    end = source.index(
        "/*****************************************************************", start
    )
    block = source[start:end]
    if 'otelcol.receiver.otlp "quality"' in block:
        return block
    # Pre-SPEC-0214 sources had no authenticated receiver; keep them runnable
    # so the same harness can show the previous behaviour (RED).
    return (
        block
        + """
otelcol.receiver.otlp "synthetic" {
  http { endpoint = "0.0.0.0:4318" }
  output { metrics = [otelcol.processor.transform.quality_metrics.input] }
}
"""
    )


def command(args, **kwargs):
    kwargs.setdefault("env", {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
    result = subprocess.run(
        args, capture_output=True, text=True, timeout=60, check=False, **kwargs
    )
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {args[:4]}: {result.stderr[-1500:]}"
        )
    return result.stdout


PROBE = """import json,sys,urllib.request,urllib.parse,urllib.error
op=json.load(sys.stdin)
if op["kind"]=="send":
 url=op["url"]
 headers={"Content-Type":"application/json"}
 if op.get("token"):
  headers["Authorization"]="Bearer "+op["token"]
 request=urllib.request.Request(url,json.dumps(op["body"]).encode(),headers)
else:
 url="http://prometheus:9090/api/v1/query?"+urllib.parse.urlencode({"query":op["query"]})
 request=urllib.request.Request(url)
try:
 with urllib.request.urlopen(request,timeout=5) as response:
  body=response.read().decode()
  print(body if op["kind"]!="send" else json.dumps({"status":response.status}))
except urllib.error.HTTPError as error:
 print(json.dumps({"status":error.code}))
"""


def payload(
    name,
    delta,
    value,
    timestamp,
    start,
    *,
    histogram=False,
    identity=True,
    instance=None,
    points=None,
):
    """Build one OTLP/JSON metric; `points` gives extra (attributes, value) pairs."""
    point = {
        "startTimeUnixNano": str(start),
        "timeUnixNano": str(timestamp),
        "attributes": [{"key": "discard_me", "value": {"stringValue": "synthetic"}}],
    }
    if histogram:
        point.update(
            count=str(value),
            sum=value * 25,
            explicitBounds=[10, 100],
            bucketCounts=["0", str(value), "0"],
        )
        data = {
            "histogram": {
                "aggregationTemporality": 1 if delta else 2,
                "dataPoints": [point],
            }
        }
    else:
        point["asInt"] = str(value)
        series = [point]
        for attributes, extra in points or ():
            series.append(
                {
                    "startTimeUnixNano": str(start),
                    "timeUnixNano": str(timestamp),
                    "asInt": str(extra),
                    "attributes": [
                        {"key": key, "value": {"stringValue": item}}
                        for key, item in attributes.items()
                    ],
                }
            )
        if points:
            series = series[1:]
        data = {
            "sum": {
                "aggregationTemporality": 1 if delta else 2,
                "isMonotonic": True,
                "dataPoints": series,
            }
        }
    attrs = [
        {"key": "service.name", "value": {"stringValue": "synthetic-metrics"}},
        {"key": "deployment.environment.name", "value": {"stringValue": "test"}},
    ]
    if identity:
        attrs.append(
            {"key": "project.id", "value": {"stringValue": "metrics-rehearsal"}}
        )
    if instance:
        attrs.append({"key": "service.instance.id", "value": {"stringValue": instance}})
    return {
        "resourceMetrics": [
            {
                "resource": {"attributes": attrs},
                "scopeMetrics": [
                    {
                        "scope": {"name": "synthetic"},
                        "metrics": [{"name": name, **data}],
                    }
                ],
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    for role in TAGS:
        parser.add_argument(f"--{role}-image", required=True)
    parser.add_argument("--source", type=Path, default=SOURCE)
    for role in STAGE_TAGS:
        parser.add_argument(
            f"--{role}-image", help="cached digest; all three enable the k6 stage"
        )
    args = parser.parse_args()
    images = {role: getattr(args, role + "_image") for role in TAGS}
    stage = [role for role in STAGE_TAGS if getattr(args, role + "_image")]
    if stage and len(stage) != len(STAGE_TAGS):
        raise RuntimeError(
            "the k6 stage needs --k6-image, --guard-image and --mock-image"
        )
    for role in stage:
        TAGS[role] = STAGE_TAGS[role]
        images[role] = getattr(args, role + "_image")
    context = command(["docker", "context", "show"]).strip()
    endpoint = json.loads(command(["docker", "context", "inspect", context]))[0][
        "Endpoints"
    ]["docker"]["Host"]
    if context != "default" or endpoint != "unix:///var/run/docker.sock":
        raise RuntimeError("Only the approved local default context is supported")
    for role, image in images.items():
        if "@sha256:" not in image:
            raise RuntimeError("Immutable cached digest required")
        actual = json.loads(command(["docker", "image", "inspect", image]))[0]
        declared = json.loads(command(["docker", "image", "inspect", TAGS[role]]))[0]
        if actual["Id"] != declared["Id"] or actual["Architecture"] != "amd64":
            raise RuntimeError("Cached digest/tag/architecture mismatch")
    if shutil.disk_usage("/tmp").free < 512 * 1024 * 1024:
        raise RuntimeError("Insufficient scratch capacity")
    available = next(
        int(line.split()[1])
        for line in Path("/proc/meminfo").read_text().splitlines()
        if line.startswith("MemAvailable:")
    )
    if available < 1024 * 1024:
        raise RuntimeError("Insufficient memory headroom")
    project = "quality-metrics-" + uuid.uuid4().hex[:12]
    network = project + "-isolated"
    if command(
        [
            "docker",
            "ps",
            "-aq",
            "--filter",
            f"label=com.docker.compose.project={project}",
        ]
    ).strip():
        raise RuntimeError("Project identity collision")
    if command(
        ["docker", "network", "ls", "-q", "--filter", f"name=^{network}$"]
    ).strip():
        raise RuntimeError("Network identity collision")
    scratch = Path(tempfile.mkdtemp(prefix=project + "-"))
    # Container UIDs may traverse only this controller-owned synthetic scratch.
    scratch.chmod(0o755)
    env = {
        "PATH": os.environ["PATH"],
        "HOME": os.environ["HOME"],
        "METRICS_NETWORK": network,
    }
    for role, image in images.items():
        env[f"METRICS_{role.upper()}_IMAGE"] = image
    alloy_config = metrics_config(args.source.read_text())
    authenticated = 'otelcol.receiver.otlp "quality"' in alloy_config
    endpoint = (
        "http://alloy:4319/v1/metrics"
        if authenticated
        else "http://alloy:4318/v1/metrics"
    )
    token = uuid.uuid4().hex
    token_file = scratch / "quality_otlp_token"
    token_file.write_text(token)
    # The relay controller refuses a token other users can read.
    token_file.chmod(0o640)
    env["METRICS_ALLOY_TOKEN"] = str(token_file)
    configs = {
        "ALLOY": alloy_config,
        "PROM": "global:\n  scrape_interval: 1s\nscrape_configs: []\n",
    }
    for role, text in configs.items():
        path = scratch / (role.lower() + ".config")
        path.write_text(text)
        path.chmod(0o644)
        env[f"METRICS_{role}_CONFIG"] = str(path)
    empty_env = scratch / "empty.env"
    empty_env.touch()
    base = [
        "docker",
        "--context",
        context,
        "compose",
        "--env-file",
        str(empty_env),
        "-p",
        project,
        "-f",
        str(COMPOSE),
    ]

    def compose(*arguments):
        return command(base + list(arguments), env=env)

    try:
        model = json.loads(compose("config", "--format", "json"))
        if model.get("volumes") or model.get("secrets"):
            raise RuntimeError("No volume/secret allowed")
        for service in model["services"].values():
            if (
                service.get("ports")
                or service.get("privileged")
                or not service.get("read_only")
            ):
                raise RuntimeError("Unsafe rehearsal service")
        print(
            json.dumps(
                {
                    "preflight": "PASS",
                    "context": context,
                    "project": project,
                    "network": network,
                    "ports": 0,
                    "volumes": 0,
                    "memory_limit_mib": 832,
                    "scratch": str(scratch),
                    "images": images,
                }
            ),
            flush=True,
        )
        compose("up", "-d", "--pull", "never")
        probe = compose("ps", "-q", "probe").strip()

        def request(op):
            if op["kind"] == "send":
                op = {"url": endpoint, "token": token if authenticated else "", **op}
            return json.loads(
                command(
                    ["docker", "exec", "-i", probe, "python", "-c", PROBE],
                    input=json.dumps(op),
                )
            )

        def query(name):
            return request({"kind": "query", "query": name})["data"]["result"]

        def expect(name, expected, timeout=35):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                try:
                    rows = query(name)
                    if rows and float(rows[0]["value"][1]) == expected:
                        labels = rows[0]["metric"]
                        if (
                            "discard_me" in labels
                            or labels.get("project_id") != "metrics-rehearsal"
                        ):
                            raise AssertionError("Resource/label filtering failed")
                        print(f"PASS {name}={expected}", flush=True)
                        return
                except RuntimeError:
                    pass
                time.sleep(1)
            raise AssertionError(
                f"Metric delivery mismatch: {name} expected {expected}"
            )

        time.sleep(3)
        start = time.time_ns() - 2_000_000_000
        timestamp = start + 1_000_000_000
        cases = [
            ("synthetic_delta_counter", True, False),
            ("synthetic_cumulative_counter", False, False),
            ("synthetic_delta_histogram", True, True),
            ("synthetic_cumulative_histogram", False, True),
        ]
        for name, delta, histogram in cases:
            request(
                {
                    "kind": "send",
                    "body": payload(
                        name, delta, 2, timestamp, start, histogram=histogram
                    ),
                }
            )
        for name, delta, histogram in cases:
            request(
                {
                    "kind": "send",
                    "body": payload(
                        name,
                        delta,
                        3 if delta else 5,
                        timestamp + 1_000_000_000,
                        timestamp if delta else start,
                        histogram=histogram,
                    ),
                }
            )
            expect(name + ("_count" if histogram else "_total"), 5)
            if histogram:
                expect(name + "_sum", 125)
                expect(name + '_bucket{le="100"}', 5)

        def expect_value(expression, expected, timeout=35):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                rows = query(expression)
                if rows and float(rows[0]["value"][1]) == expected:
                    print(f"PASS {expression}={expected}", flush=True)
                    return
                time.sleep(1)
            raise AssertionError(f"Mismatch: {expression} expected {expected}")

        # SPEC-0214: a k6 Rate exports one counter split by `condition`, and
        # several runners share metric names; neither identity may collapse.
        request(
            {
                "kind": "send",
                "body": payload(
                    "synthetic_rate",
                    False,
                    0,
                    timestamp,
                    start,
                    points=[({"condition": "zero"}, 3), ({"condition": "nonzero"}, 2)],
                ),
            }
        )
        expect('synthetic_rate_total{condition="zero"}', 3)
        expect('synthetic_rate_total{condition="nonzero"}', 2)
        for instance, value in (("runner-a", 4), ("runner-b", 6)):
            request(
                {
                    "kind": "send",
                    "body": payload(
                        "synthetic_instances",
                        False,
                        value,
                        timestamp,
                        start,
                        instance=instance,
                    ),
                }
            )
        expect_value("count(synthetic_instances_total)", 2)
        expect_value("sum(synthetic_instances_total)", 10)
        if authenticated:
            status = request(
                {
                    "kind": "send",
                    "token": "",
                    "body": payload(
                        "synthetic_unauthenticated", False, 1, time.time_ns(), start
                    ),
                }
            )["status"]
            if status != 401:
                raise AssertionError(f"Unauthenticated producer got HTTP {status}")
            time.sleep(3)
            if query("synthetic_unauthenticated_total"):
                raise AssertionError("Unauthenticated metric was stored")
            print("PASS unauthenticated producer rejected with 401", flush=True)
        else:
            print("NOT_RUN authentication: source has no quality receiver", flush=True)

        def dashboard_check(instance, require=()):
            """Every k6 dashboard query, on the real OTLP shape, for one run."""
            dashboard = json.loads(DASHBOARD.read_text())
            expressions = list(dashboard_expressions(dashboard))
            empty = []
            for expression in expressions:
                concrete = (
                    expression.replace("$project_id", "metrics-rehearsal")
                    .replace("$instance", instance)
                    .replace("$quantile", "0.95")
                    .replace("$__rate_interval", "5m")
                    .replace("$__range", "5m")
                )
                if not query(concrete):
                    empty.append(expression)
            missing = [
                name
                for name in (
                    "k6_http_reqs_total",
                    "k6_http_req_failed_total",
                    "k6_http_req_duration_milliseconds_bucket",
                    *require,
                )
                if not any(name in item for item in expressions if item not in empty)
            ]
            if missing:
                raise AssertionError(f"Dashboard returns no data for {missing}")
            print(
                f"PASS k6 dashboard queries: {len(expressions) - len(empty)}/"
                f"{len(expressions)} return data",
                flush=True,
            )
            for expression in empty:
                print("INFO empty dashboard query:", expression[:120], flush=True)

        if stage:
            import executor_stage

            executor_stage.run(
                images,
                network,
                token_file,
                scratch,
                query,
                expect_value,
                dashboard_check,
            )

        # Exact transport replay must not double count a delta stream.
        duplicate = payload(
            "synthetic_delta_counter", True, 3, timestamp + 1_000_000_000, timestamp
        )
        request({"kind": "send", "body": duplicate})
        time.sleep(3)
        expect("synthetic_delta_counter_total", 5)
        request(
            {
                "kind": "send",
                "body": payload(
                    "synthetic_missing_identity",
                    False,
                    9,
                    time.time_ns(),
                    start,
                    identity=False,
                ),
            }
        )
        time.sleep(3)
        if query("synthetic_missing_identity_total"):
            raise AssertionError("Missing project identity was accepted")
        print("PASS missing identity dropped", flush=True)
        compose("stop", "prometheus")
        request(
            {
                "kind": "send",
                "body": payload(
                    "synthetic_retry_counter", False, 7, time.time_ns(), start
                ),
            }
        )
        time.sleep(7)
        compose("start", "prometheus")
        expect("synthetic_retry_counter_total", 7)
        compose("restart", "alloy")
        time.sleep(3)
        restart_start = time.time_ns() - 1_000_000_000
        restart_timestamp = time.time_ns()
        # A new source epoch resets the same identity; this is not state recovery.
        request(
            {
                "kind": "send",
                "body": payload(
                    "synthetic_delta_counter", True, 4, restart_timestamp, restart_start
                ),
            }
        )
        expect("synthetic_delta_counter_total", 4)
        next_timestamp = time.time_ns()
        request(
            {
                "kind": "send",
                "body": payload(
                    "synthetic_delta_counter",
                    True,
                    2,
                    next_timestamp,
                    restart_timestamp,
                ),
            }
        )
        expect("synthetic_delta_counter_total", 6)
        print(
            "PASS same identity new epoch reset 4 then accumulated 6; prior state recovery NOT_PROVEN",
            flush=True,
        )
        print(
            "PASS synthetic metrics delivery; live Grafana/project datasource NOT_RUN",
            flush=True,
        )
    finally:
        compose("down", "--timeout", "10")
        if command(
            [
                "docker",
                "ps",
                "-aq",
                "--filter",
                f"label=com.docker.compose.project={project}",
            ]
        ).strip():
            raise RuntimeError("Owned project containers remain; scratch preserved")
        if command(
            ["docker", "network", "ls", "-q", "--filter", f"name=^{network}$"]
        ).strip():
            raise RuntimeError("Owned network remains; scratch preserved")
        shutil.rmtree(scratch)
        print("PASS exact owned cleanup; no volume deletion/prune", flush=True)


if __name__ == "__main__":
    main()
