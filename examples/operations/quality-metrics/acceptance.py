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
    "prom": "prom/prometheus:v3.14.0",
    "probe": "python:3.13.15-alpine",
}


def metrics_config(source):
    """Use the actual bounded transform-to-remote-write source, not a parallel implementation."""
    start = source.index('otelcol.processor.transform "quality_metrics" {')
    end = source.index(
        "/*****************************************************************", start
    )
    return (
        source[start:end]
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


PROBE = """import json,sys,urllib.request,urllib.parse
op=json.load(sys.stdin)
if op["kind"]=="send":
 url="http://alloy:4318/v1/metrics"
 request=urllib.request.Request(url,json.dumps(op["body"]).encode(),{"Content-Type":"application/json"})
else:
 url="http://prometheus:9090/api/v1/query?"+urllib.parse.urlencode({"query":op["query"]})
 request=urllib.request.Request(url)
with urllib.request.urlopen(request,timeout=5) as response:
 print(response.read().decode())
"""


def payload(name, delta, value, timestamp, start, *, histogram=False, identity=True):
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
        data = {
            "sum": {
                "aggregationTemporality": 1 if delta else 2,
                "isMonotonic": True,
                "dataPoints": [point],
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
    args = parser.parse_args()
    images = {role: getattr(args, role + "_image") for role in TAGS}
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
    configs = {
        "ALLOY": metrics_config(SOURCE.read_text()),
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
