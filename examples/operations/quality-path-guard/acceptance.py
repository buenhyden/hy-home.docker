"""Run only the separately approved synthetic quality-path-guard rehearsal."""

import argparse
import hashlib
import importlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import uuid


def require_result(code, final, expected_code, expected_verdict):
    if (
        code != expected_code
        or final.get("verdict") != expected_verdict
        or final.get("evidence_state") != "complete"
    ):
        raise RuntimeError("synthetic quality acceptance failed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guard-image", required=True)
    parser.add_argument("--mock-image", required=True)
    parser.add_argument("--k6-image", required=True)
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(repo / "infra/11-quality/k6"))
    quality_run = importlib.import_module("quality_run")
    container_executor = importlib.import_module("container_executor")
    http_guard = importlib.import_module("http_guard")

    project = "hyhome-quality-guard-" + uuid.uuid4().hex[:12]
    run_id = str(uuid.uuid4())
    images = {"guard": args.guard_image, "mock": args.mock_image, "k6": args.k6_image}
    if not http_guard.IMAGE.fullmatch(images["guard"]) or not all(
        "@sha256:" in value for value in images.values()
    ):
        raise ValueError("approved cached image digests are required")

    root = pathlib.Path(tempfile.mkdtemp(prefix="hyhome-quality-guard-"))
    root.chmod(0o755)

    scenario = root / "scenarios"
    scenario.mkdir()
    mappings = root / "mappings"
    mappings.mkdir()
    (mappings / "catchall.json").write_text(
        json.dumps(
            {
                "request": {"method": "GET", "urlPattern": ".*"},
                "response": {"status": 200, "jsonBody": {"synthetic": True}},
            }
        )
    )
    source = scenario / "smoke.js"
    source.write_text(
        """import http from 'k6/http'; import {check} from 'k6'; export const options={thresholds:{checks:['rate==1']}}; export default function(){ for(const [path,status] of [['/health',200],['/unapproved',404],['/__admin/requests',404]]) { const r=http.get('http://wiremock:8080'+path); check(r,{'guard response':x=>x.status===status}); } }"""
    )
    manifest = {
        "schema_version": "hyhome.quality-run/v1",
        "run_id": run_id,
        "attempt": 1,
        "project_id": "synthetic-guard",
        "environment": "test",
        "generator": "k6",
        "source_revision": "a" * 40,
        "tool_image": images["k6"],
        "fixture_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "scenario_path": "smoke.js",
        "mock_mode": "load",
        "target": {
            "origin": "http://wiremock:8080",
            "allowed_origins": ["http://wiremock:8080"],
            "allowed_networks": ["10.251.211.0/24"],
            "paths": ["/health"],
        },
        "redirects": {"policy": "deny", "max_redirects": 0},
        "budget": {
            "users": 1,
            "rate_per_second": 10,
            "duration_seconds": 5,
            "max_iterations": 1,
            "cpu_millis": 250,
            "memory_mib": 128,
        },
        "thresholds": {"checks": ["rate==1"]},
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_bytes(quality_run._canonical(manifest))
    guard = root / "routes.yml"
    guard.write_bytes(quality_run._canonical(http_guard.configuration(manifest)))
    env = {
        **container_executor._docker_environment(),
        "QUALITY_GUARD_IMAGE": images["guard"],
        "QUALITY_MOCK_IMAGE": images["mock"],
        "QUALITY_GUARD_CONFIG": str(guard),
        "QUALITY_MOCK_MAPPINGS": str(mappings),
        "QUALITY_RUN_ID": run_id,
        "QUALITY_RUNNER_NETWORK": project + "-runner",
        "QUALITY_RUNNER_SUBNET": "10.251.211.0/24",
        "QUALITY_BACKEND_NETWORK": project + "-backend",
        "QUALITY_BACKEND_SUBNET": "10.251.212.0/24",
    }
    base = [
        "docker",
        "--context",
        "default",
        "compose",
        "--env-file",
        "/dev/null",
        "--project-name",
        project,
        "-f",
        str(repo / "examples/operations/quality-path-guard/docker-compose.yml"),
    ]
    created = False

    def command(args):
        result = subprocess.run(
            base + args, env=env, capture_output=True, text=True, check=False
        )
        if result.returncode:
            print(result.stderr)
            result.check_returncode()
        return result

    try:
        observed = subprocess.check_output(
            ["docker", "context", "show"], text=True
        ).strip()
        if observed != "default":
            raise ValueError("this rehearsal requires the approved default context")
        if shutil.disk_usage(root).free < 256 * 1024 * 1024:
            raise ValueError("insufficient fixture disk budget")
        for image in images.values():
            subprocess.run(
                [
                    "docker",
                    "--context",
                    "default",
                    "image",
                    "inspect",
                    image,
                    "--format",
                    "{{.Os}}/{{.Architecture}}",
                ],
                check=True,
            )
        network_ids = subprocess.check_output(
            ["docker", "--context", "default", "network", "ls", "--quiet"], text=True
        ).split()
        if network_ids:
            import ipaddress

            networks = json.loads(
                subprocess.check_output(
                    [
                        "docker",
                        "--context",
                        "default",
                        "network",
                        "inspect",
                        *network_ids,
                    ]
                )
            )
            wanted = [
                ipaddress.ip_network(env["QUALITY_RUNNER_SUBNET"]),
                ipaddress.ip_network(env["QUALITY_BACKEND_SUBNET"]),
            ]
            for network in networks:
                for config in network.get("IPAM", {}).get("Config") or []:
                    if "Subnet" in config:
                        existing = ipaddress.ip_network(config["Subnet"])
                        if any(
                            item.version == existing.version and item.overlaps(existing)
                            for item in wanted
                        ):
                            raise ValueError(
                                "fixture subnet overlaps an existing network"
                            )
        command(["config", "--quiet"])
        print("COMPOSE_RENDER_PASS")
        created = True
        command(["up", "--detach", "--pull", "never"])
        print("ISOLATED_UP_PASS")
        time.sleep(15)
        peer = command(["ps", "--quiet", "path-guard"]).stdout.strip()
        backend = command(["ps", "--all", "--quiet", "mock-backend"]).stdout.strip()

        peer_name = (
            subprocess.check_output(
                [
                    "docker",
                    "--context",
                    "default",
                    "inspect",
                    peer,
                    "--format",
                    "{{.Name}}",
                ],
                text=True,
            )
            .strip()
            .lstrip("/")
        )
        backend_name = (
            subprocess.check_output(
                [
                    "docker",
                    "--context",
                    "default",
                    "inspect",
                    backend,
                    "--format",
                    "{{.Name}}",
                ],
                text=True,
            )
            .strip()
            .lstrip("/")
        )
        attempt = root / "attempt"
        quality_run.prepare(manifest_path, scenario, attempt)
        code = container_executor.execute(
            manifest,
            scenario,
            attempt,
            env["QUALITY_RUNNER_NETWORK"],
            peer_name,
            guard_config=guard,
            backend_network=env["QUALITY_BACKEND_NETWORK"],
            backend_peer=backend_name,
        )
        print("RUN_EXIT", code)
        final = quality_run.finalize(attempt)
        print("FINAL_VERDICT", final["verdict"], "EVIDENCE", final["evidence_state"])
        require_result(code, final, 0, "passed")
        from result_inspection import inspect_raw_points

        points, issues = inspect_raw_points(attempt, manifest)
        if issues or not final["import_allowed"]:
            raise RuntimeError("native distribution acceptance failed")
        print("NATIVE_FINITE_IDENTITY_SAFE_POINTS_PASS", points)
        print("EXACT_ALLOWED200_UNAPPROVED404_ADMIN404_PASS")
        manifest["attempt"] = 2
        manifest["thresholds"] = {"checks": ["rate>1"]}
        manifest_path.write_bytes(quality_run._canonical(manifest))
        second = root / "attempt-2"
        quality_run.prepare(manifest_path, scenario, second)
        code = container_executor.execute(
            manifest,
            scenario,
            second,
            env["QUALITY_RUNNER_NETWORK"],
            peer_name,
            guard_config=guard,
            backend_network=env["QUALITY_BACKEND_NETWORK"],
            backend_peer=backend_name,
        )
        final = quality_run.finalize(second)
        print(
            "THRESHOLD_EXIT",
            code,
            "VERDICT",
            final["verdict"],
            "EVIDENCE",
            final["evidence_state"],
        )
        require_result(code, final, 99, "failed_threshold")
        print("MANIFEST_THRESHOLD_OVERRIDE_FAILURE_PASS")
    finally:
        if created:
            command(["down", "--timeout", "10"])
            print("OWNED_CLEANUP_PASS")
        shutil.rmtree(root)


if __name__ == "__main__":
    main()
