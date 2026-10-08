"""k6 through the real executor and relay controller, isolated or on HOME.

Target (Traefik path guard + WireMock) -> k6 (quality_run.py run) -> per-run
relay created by metrics_relay.py -> authenticated Alloy -> Prometheus ->
k6 dashboard queries. `acceptance.py` calls `run` against its own isolated
Alloy and Prometheus, adding the negative cases: forged OTLP identity, a
relay that breaks the peer contract, unapproved paths, cancel and run-scoped
cleanup. `--home` runs one canary against HOME Alloy on `quality_otlp_net`
and reads the live Grafana dashboard through the Grafana API.
"""

import argparse
import hashlib
import ipaddress
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
K6 = ROOT / "infra/11-quality/k6"
GUARD_COMPOSE = ROOT / "examples/operations/quality-path-guard/docker-compose.yml"
SUBNETS = ("10.251.211.0/24", "10.251.212.0/24")
FORGED = "forged-project"
SCENARIO = """import http from 'k6/http';
import { check } from 'k6';
// Approved paths pass through the guard; others must stop there (404).
export default function () {
  check(http.get('http://wiremock:8080/health'), {'approved 200': (r) => r.status === 200});
  check(http.get('http://wiremock:8080/unapproved'), {'unapproved 404': (r) => r.status === 404});
  check(http.get('http://wiremock:8080/__admin/requests'), {'admin 404': (r) => r.status === 404});
  http.get('http://wiremock:8080/slow');
  if (__VU === 1 && __ITER === 0) {
    // A scenario posting its own OTLP may not claim another project or run.
    const body = JSON.stringify({resourceMetrics: [{resource: {attributes: [
      {key: 'project.id', value: {stringValue: 'FORGED_PROJECT'}},
      {key: 'service.instance.id', value: {stringValue: 'forged'}}]},
      scopeMetrics: [{metrics: [{name: 'forged_counter', sum: {
        aggregationTemporality: 2, isMonotonic: true,
        dataPoints: [{asInt: '1', timeUnixNano: String(Date.now() * 1e6)}]}}]}]}]});
    http.post('http://metrics-ingress:4318/v1/metrics', body,
      {headers: {'Content-Type': 'application/json'}});
  }
}
""".replace("FORGED_PROJECT", FORGED)


def docker(*arguments, check=True, timeout=60, stdin=None):
    result = subprocess.run(
        ["docker", "--context", "default", *arguments],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
        input=stdin,
        env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]},
    )
    if check and result.returncode:
        raise RuntimeError(f"docker {arguments[:2]} failed: {result.stderr[-400:]}")
    return result.stdout


def quality_run(*arguments, timeout=180):
    return subprocess.run(
        [sys.executable, str(K6 / "quality_run.py"), *arguments],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def exists(name):
    return bool(docker("ps", "--all", "--quiet", "--filter", f"name=^{name}$").strip())


class Fixture:
    """One path-guarded WireMock target and the manifests of one run ID."""

    def __init__(self, images, network, token, scratch, project):
        sys.path.insert(0, str(K6))
        import http_guard
        import metrics_relay

        self.relay_module = metrics_relay
        self.images, self.network, self.token = images, network, token
        self.scratch, self.project = scratch, project
        self.run_id = str(uuid.uuid4())
        self.guard_project = "quality-relay-" + self.run_id[:8]
        self.scenarios = scratch / "scenarios"
        mappings = scratch / "mappings"
        for path in (self.scenarios, mappings):
            path.mkdir(mode=0o755)
        (self.scenarios / "relay.js").write_text(SCENARIO)
        (mappings / "catchall.json").write_text(
            json.dumps({"request": {"method": "GET", "urlPattern": ".*"},
                        "response": {"status": 200, "jsonBody": {"synthetic": True}}})
        )  # fmt: skip
        (mappings / "slow.json").write_text(
            json.dumps({"priority": 1, "request": {"method": "GET", "urlPath": "/slow"},
                        "response": {"status": 200, "fixedDelayMilliseconds": 300}})
        )  # fmt: skip
        for path in (*self.scenarios.iterdir(), *mappings.iterdir()):
            path.chmod(0o644)
        self.revision = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
        ).strip()
        first, _ = self.manifest(1, 20, 100000)
        self.routes = scratch / "routes.yml"
        self.routes.write_bytes(
            (json.dumps(http_guard.configuration(first), sort_keys=True,
                        separators=(",", ":")) + "\n").encode()
        )  # fmt: skip
        self.routes.chmod(0o644)
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": os.environ["HOME"],
            "QUALITY_GUARD_IMAGE": images["guard"],
            "QUALITY_MOCK_IMAGE": images["mock"],
            "QUALITY_GUARD_CONFIG": str(self.routes),
            "QUALITY_MOCK_MAPPINGS": str(mappings),
            "QUALITY_RUN_ID": self.run_id,
            "QUALITY_RUNNER_NETWORK": self.guard_project + "-runner",
            "QUALITY_RUNNER_SUBNET": SUBNETS[0],
            "QUALITY_BACKEND_NETWORK": self.guard_project + "-backend",
            "QUALITY_BACKEND_SUBNET": SUBNETS[1],
        }
        self.compose = ["docker", "--context", "default", "compose", "--env-file",
                        "/dev/null", "--project-name", self.guard_project, "-f",
                        str(GUARD_COMPOSE)]  # fmt: skip
        self.relay = [
            "--relay-image",
            images["alloy"],
            "--relay-token-file",
            str(token),
        ]

    def manifest(self, attempt, duration, iterations):
        value = {
            "schema_version": "hyhome.quality-run/v2",
            "telemetry": {"mode": "otlp"},
            "run_id": self.run_id,
            "attempt": attempt,
            "project_id": self.project,
            "environment": "test",
            "generator": "k6",
            "source_revision": self.revision,
            "tool_image": self.images["k6"],
            "fixture_sha256": hashlib.sha256(
                (self.scenarios / "relay.js").read_bytes()
            ).hexdigest(),
            "scenario_path": "relay.js",
            "mock_mode": "load",
            "target": {
                "origin": "http://wiremock:8080",
                "allowed_origins": ["http://wiremock:8080"],
                "allowed_networks": [SUBNETS[0]],
                "paths": ["/health", "/slow"],
            },
            "redirects": {"policy": "deny", "max_redirects": 0},
            "budget": {
                "users": 2,
                "rate_per_second": 20,
                "duration_seconds": duration,
                "max_iterations": iterations,
                "cpu_millis": 500,
                "memory_mib": 256,
            },
            "thresholds": {"checks": ["rate==1"]},
        }
        path = self.scratch / f"manifest-a{attempt}.json"
        path.write_text(json.dumps(value, sort_keys=True))
        return value, path

    def __enter__(self):
        taken = [
            ipaddress.ip_network(config["Subnet"])
            for item in json.loads(
                docker("network", "inspect", *docker("network", "ls", "-q").split())
            )
            for config in (item.get("IPAM", {}).get("Config") or [])
            if "Subnet" in config
        ]
        if any(ipaddress.ip_network(s).overlaps(t) for s in SUBNETS for t in taken):
            raise RuntimeError("guard fixture subnet overlaps an existing network")
        subprocess.run([*self.compose, "up", "--detach", "--pull", "never"],
                       env=self.env, check=True, capture_output=True, timeout=120)  # fmt: skip
        time.sleep(10)

        def name_of(service):
            ident = subprocess.check_output(
                [*self.compose, "ps", "--quiet", service], env=self.env, text=True
            ).strip()
            return docker("inspect", ident, "--format", "{{.Name}}").strip().lstrip("/")

        self.common = [
            "--scenario-root", str(self.scenarios), "--docker-context", "default",
            "--network", self.env["QUALITY_RUNNER_NETWORK"],
            "--wiremock-container", name_of("path-guard"),
            "--guard-config", str(self.routes),
            "--backend-network", self.env["QUALITY_BACKEND_NETWORK"],
            "--backend-container", name_of("mock-backend"),
            "--metrics-egress-network", self.network,
        ]  # fmt: skip
        return self

    def __exit__(self, *exc):
        subprocess.run([*self.compose, "down", "--timeout", "10"], env=self.env,
                       capture_output=True, check=False, timeout=120)  # fmt: skip
        quality_run("cleanup", "--run-id", self.run_id, "--docker-context", "default")
        if docker("ps", "--all", "--quiet", "--filter",
                  f"label=com.docker.compose.project={self.guard_project}").strip():  # fmt: skip
            raise RuntimeError("guard fixture containers remain")
        print("PASS guard fixture and run containers removed", flush=True)

    def runner(self, attempt):
        return f"hyhome-k6-{self.run_id.replace('-', '')}-a{attempt}"

    def passed_run(self, attempt, duration, iterations, query, expect_value):
        """Run, finalize and check that Prometheus holds exactly k6's counts."""
        manifest, path = self.manifest(attempt, duration, iterations)
        directory = self.scratch / f"a{attempt}"
        done = quality_run("run", "--manifest", str(path), "--attempt-dir",
                           str(directory), *self.common, *self.relay)  # fmt: skip
        if done.returncode != 0:
            raise AssertionError(
                f"executor run exited {done.returncode}: {done.stderr[-600:]}"
            )
        quality_run("finalize", "--attempt-dir", str(directory))
        final = json.loads((directory / "final.json").read_text())
        if (final["verdict"], final["evidence_state"]) != ("passed", "complete"):
            raise AssertionError(
                f"verdict {final['verdict']}/{final['evidence_state']}"
            )
        print(f"PASS a{attempt} through guard and controller relay: passed/complete",
              flush=True)  # fmt: skip
        if exists(self.relay_module.relay_name(manifest)) or exists(
            self.runner(attempt)
        ):
            raise AssertionError("relay or runner remained after the run")
        print(f"PASS a{attempt} relay and runner removed after the run", flush=True)
        summary = json.loads((directory / "raw-summary.json").read_text())["metrics"]
        instance = f"{self.run_id}-a{attempt}"
        selector = f'project_id="{self.project}",instance="{instance}"'
        expected = [
            (f"sum(k6_http_reqs_total{{{selector}}})", summary["http_reqs"]["values"]["count"]),
            (f'sum(k6_checks_total{{{selector},condition="nonzero"}})', summary["checks"]["values"]["passes"]),
            (f"sum(forged_counter_total{{{selector}}})", 1),
        ]  # fmt: skip
        if "dropped_iterations" in summary:
            expected.append(
                (f"sum(k6_dropped_iterations_total{{{selector}}})",
                 summary["dropped_iterations"]["values"]["count"])
            )  # fmt: skip
        for expression, value in expected:
            expect_value(expression, value, timeout=60)
        for forged in (f'{{project_id="{FORGED}"}}', '{instance="forged"}'):
            if query(forged):
                raise AssertionError(f"forged identity reached Prometheus: {forged}")
        print("PASS relay replaced the forged project and instance", flush=True)
        return manifest, instance


def run(images, network, token, scratch, query, expect_value, dashboard_check):
    """Isolated stage of acceptance.py, with the negative cases."""
    with Fixture(images, network, token, scratch, "metrics-rehearsal") as fixture:
        _, instance = fixture.passed_run(1, 20, 100000, query, expect_value)
        dashboard_check(
            instance, require=("k6_checks_total", "k6_dropped_iterations_total")
        )

        # A run without drops: the dashboard shows 0, an absent run nothing.
        _, instance = fixture.passed_run(2, 10, 3, query, expect_value)
        dropped = (
            'sum(k6_dropped_iterations_total{project_id="%s", instance=~"%s"}) or '
            '(0 * sum(k6_iterations_total{project_id="%s", instance=~"%s"}))'
        )
        project = fixture.project
        expect_value(dropped % (project, instance, project, instance), 0, timeout=60)
        if query(dropped % (project, "absent-run", project, "absent-run")):
            raise AssertionError("absent run reported a dropped-iteration value")
        print("PASS dropped iterations: 0 for a run without drops, no data for an "
              "absent run", flush=True)  # fmt: skip

        # A relay that breaks the contract (writable rootfs) is refused before
        # k6 starts; no runner container and no metrics appear.
        third, third_path = fixture.manifest(3, 10, 3)
        decoy = fixture.relay_module.relay_name(third)
        docker("create", "--name", decoy, "--label",
               f"hyhome.quality.run_id={fixture.run_id}", "--label",
               "hyhome.quality.attempt=3", "--label", "hyhome.quality.role=metrics-ingress",
               "--network", fixture.env["QUALITY_RUNNER_NETWORK"], "--network-alias",
               "metrics-ingress", images["alloy"], *fixture.relay_module.COMMAND)  # fmt: skip
        docker("network", "connect", network, decoy)
        docker("start", decoy, check=False)
        directory = scratch / "a3"
        refused = quality_run("run", "--manifest", str(third_path), "--attempt-dir",
                              str(directory), *fixture.common,
                              "--metrics-ingress-container", decoy)  # fmt: skip
        record = json.loads((directory / "exit.json").read_text())
        if (
            refused.returncode != 2
            or record["error_class"] != "isolation_preflight_failed"
        ):
            raise AssertionError("non-conforming relay was not refused before traffic")
        if exists(fixture.runner(3)):
            raise AssertionError("k6 started beside a non-conforming relay")
        docker("rm", "--force", decoy)
        print("PASS non-conforming relay refused before traffic", flush=True)

        # Cancel: SIGTERM mid-run removes this attempt's runner and relay,
        # never another run's container.
        foreign = "hyhome-k6relay-foreign-" + fixture.run_id[:8]
        docker("create", "--name", foreign, "--label",
               "hyhome.quality.run_id=00000000-0000-4000-8000-00000000f0f0",
               "--label", "hyhome.quality.role=metrics-ingress", images["alloy"])  # fmt: skip
        try:
            fourth, fourth_path = fixture.manifest(4, 60, 100000)
            directory = scratch / "a4"
            process = subprocess.Popen(
                [sys.executable, str(K6 / "quality_run.py"), "run", "--manifest",
                 str(fourth_path), "--attempt-dir", str(directory), *fixture.common,
                 *fixture.relay],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )  # fmt: skip
            deadline = time.monotonic() + 60
            while not exists(fixture.runner(4)) and time.monotonic() < deadline:
                time.sleep(1)
            time.sleep(3)
            process.send_signal(signal.SIGTERM)
            code = process.wait(timeout=90)
            record = json.loads((directory / "exit.json").read_text())
            if (
                code != 130
                or record["error_class"] != "runner_cancelled"
                or exists(fixture.runner(4))
                or exists(fixture.relay_module.relay_name(fourth))
                or not exists(foreign)
            ):
                raise AssertionError(
                    "cancel did not remove exactly this attempt's containers"
                )
            print("PASS SIGTERM: exit 130, runner_cancelled, own runner and relay "
                  "removed, another run untouched", flush=True)  # fmt: skip

            # Run-scoped cleanup after a crash removes only that run's leftovers.
            leftover = fixture.relay_module.relay_name(dict(fourth, attempt=5))
            docker("create", "--name", leftover, "--label",
                   f"hyhome.quality.run_id={fixture.run_id}", "--label",
                   "hyhome.quality.role=metrics-ingress", images["alloy"])  # fmt: skip
            cleaned = quality_run("cleanup", "--run-id", fixture.run_id,
                                  "--docker-context", "default")  # fmt: skip
            if cleaned.returncode != 0 or exists(leftover) or not exists(foreign):
                raise AssertionError("cleanup removed the wrong containers")
            print("PASS cleanup --run-id removed only that run's leftover", flush=True)
        finally:
            docker("rm", "--force", foreign, check=False)


PROBE = """import base64, json, sys, urllib.request, urllib.parse, urllib.error
op = json.load(sys.stdin)
if op["kind"] == "prometheus":
    request = urllib.request.Request("http://prometheus:9090/api/v1/query?" + urllib.parse.urlencode({"query": op["query"]}))
else:
    secret = open("/run/secrets/grafana_admin_password").read().strip()
    auth = base64.b64encode((op["user"] + ":" + secret).encode()).decode()
    body = json.dumps(op["body"]).encode() if "body" in op else None
    request = urllib.request.Request("http://grafana:3000" + op["path"], body,
        {"Authorization": "Basic " + auth, "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(request, timeout=15) as response:
        print(response.read().decode())
except urllib.error.HTTPError as error:
    print(json.dumps({"http_status": error.code}))
"""


def home():
    """One canary on HOME: HOME Alloy, HOME Prometheus and live Grafana."""
    parser = argparse.ArgumentParser(description=home.__doc__)
    for role in ("k6", "guard", "mock", "alloy", "probe"):
        parser.add_argument(f"--{role}-image", required=True)
    parser.add_argument("--home", action="store_true", required=True)
    parser.add_argument("--project-id", default="hyhome-quality-canary")
    args = parser.parse_args()
    images = {
        role: getattr(args, role + "_image")
        for role in ("k6", "guard", "mock", "alloy")
    }
    token = ROOT / "secrets/observability/alloy/quality_otlp_token.txt"
    grafana_secret = ROOT / "secrets/observability/grafana/grafana_admin_password.txt"
    user = docker("exec", "grafana", "printenv", "GF_SECURITY_ADMIN_USER").strip()
    scratch = Path(tempfile.mkdtemp(prefix="quality-home-canary-"))
    scratch.chmod(0o755)
    probe = "quality-home-probe-" + uuid.uuid4().hex[:8]
    docker("run", "--detach", "--rm", "--name", probe, "--network", "obs_net",
           "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
           "--memory", "64m", "--cpus", "0.25", "--user", f"{os.getuid()}:{os.getgid()}",
           "--mount", f"type=bind,src={grafana_secret},dst=/run/secrets/grafana_admin_password,readonly",
           args.probe_image, "python", "-c", "import time; time.sleep(900)")  # fmt: skip

    def ask(op):
        return json.loads(docker("exec", "-i", probe, "python", "-c", PROBE,
                                 stdin=json.dumps(op)))  # fmt: skip

    def query(expression):
        return ask({"kind": "prometheus", "query": expression})["data"]["result"]

    def expect_value(expression, expected, timeout=60):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            rows = query(expression)
            if rows and float(rows[0]["value"][1]) == expected:
                print(f"PASS {expression}={expected}", flush=True)
                return
            time.sleep(2)
        raise AssertionError(f"Mismatch: {expression} expected {expected}")

    try:
        with Fixture(
            images, "quality_otlp_net", token, scratch, args.project_id
        ) as fixture:
            _, instance = fixture.passed_run(1, 20, 100000, query, expect_value)
            series = query(f'count({{instance="{instance}"}})')
            print("INFO series for one attempt:", series[0]["value"][1], flush=True)
            found = ask({"kind": "grafana", "user": user,
                         "path": "/api/search?query=k6&type=dash-db"})  # fmt: skip
            uid = next(item["uid"] for item in found if item["title"].lower() == "k6")
            dashboard = ask({"kind": "grafana", "user": user,
                             "path": f"/api/dashboards/uid/{uid}"})["dashboard"]  # fmt: skip
            stack, targets = list(dashboard["panels"]), []
            while stack:
                panel = stack.pop()
                stack.extend(panel.get("panels", []))
                targets += [
                    t
                    for t in panel.get("targets", []) or []
                    if "k6_" in t.get("expr", "")
                ]
            empty = []
            for target in targets:
                expression = (
                    target["expr"].replace("$project_id", args.project_id)
                    .replace("$instance", instance).replace("$quantile", "0.95")
                    .replace("$__rate_interval", "5m").replace("$__range", "5m")
                )  # fmt: skip
                answer = ask({"kind": "grafana", "user": user, "path": "/api/ds/query",
                              "body": {"from": "now-30m", "to": "now", "queries": [
                                  {"refId": "A", "datasource": target["datasource"],
                                   "expr": expression, "instant": True}]}})  # fmt: skip
                frames = answer.get("results", {}).get("A", {}).get("frames", [])
                if not any(frame.get("data", {}).get("values") for frame in frames):
                    empty.append(expression[:100])
            print(f"PASS live Grafana dashboard {uid}: {len(targets) - len(empty)}/"
                  f"{len(targets)} queries return data", flush=True)  # fmt: skip
            for expression in empty:
                print("INFO empty live query:", expression, flush=True)
            if len(empty) == len(targets):
                raise AssertionError("live Grafana returned no data")
    finally:
        docker("rm", "--force", probe, check=False)
    import shutil

    shutil.rmtree(scratch)
    print("PASS HOME canary; probe and scratch removed", flush=True)


if __name__ == "__main__":
    home()
