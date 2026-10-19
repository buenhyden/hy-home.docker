"""Run only the separately approved synthetic quality-path-guard rehearsal.

The rehearsal runs two cycles from the same input bytes. Each cycle starts its
own project, runs the passing and the failing attempt, removes exactly what it
owns and writes a receipt. The second cycle starts only after the first left no
container or network with the run label, so nothing carries over between them.
"""

import argparse
import hashlib
import importlib
import ipaddress
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

CYCLES = 2
# Logical results that both cycles must reproduce. Point counts and timings
# are recorded but not compared: k6 samples its gauges once per second.
EXPECTED = (
    {"attempt": 1, "exit": 0, "verdict": "passed", "evidence_state": "complete"},
    {
        "attempt": 2,
        "exit": 99,
        "verdict": "failed_threshold",
        "evidence_state": "complete",
    },
)
INPUT_KEYS = ("run_id", "images", "inputs")


def require_result(code, final, expected_code, expected_verdict):
    if (
        code != expected_code
        or final.get("verdict") != expected_verdict
        or final.get("evidence_state") != "complete"
    ):
        raise RuntimeError("synthetic quality acceptance failed")


def compare_cycles(receipts):
    """Return the reasons the cycles differ; an empty list means they match."""
    if len(receipts) != CYCLES:
        return [f"expected {CYCLES} cycle receipts, got {len(receipts)}"]
    reasons = []
    first = receipts[0]
    for receipt in receipts:
        cycle = receipt.get("cycle")
        if receipt.get("error"):
            reasons.append(f"cycle {cycle} failed: {receipt['error']}")
        if receipt.get("cleanup") != {"containers": 0, "networks": 0}:
            reasons.append(f"cycle {cycle} left owned resources")
        logical = [
            {key: item.get(key) for key in EXPECTED[0]}
            for item in receipt.get("attempts", [])
        ]
        if logical != list(EXPECTED):
            reasons.append(f"cycle {cycle} attempts differ from the expected results")
        for key in INPUT_KEYS:
            if receipt.get(key) != first.get(key):
                reasons.append(f"cycle {cycle} {key} differs from cycle 1")
    return reasons


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(directory):
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(directory)).encode() + b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _owned(run_id):
    """Count containers and networks that still carry this run's label."""
    label = "label=hyhome.quality.run_id=" + run_id
    counts = {}
    for kind, args in (
        ("containers", ["ps", "--all", "--quiet"]),
        ("networks", ["network", "ls", "--quiet"]),
    ):
        output = subprocess.check_output(
            ["docker", "--context", "default", *args, "--filter", label], text=True
        )
        counts[kind] = len(output.split())
    return counts


def write_inputs(root, images, quality_run, http_guard):
    """Write the scenario, mappings, manifests and guard once for every cycle."""
    run_id = str(uuid.uuid4())
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
        "fixture_sha256": _sha256(source),
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
    # The second attempt forces a threshold failure from the same scenario.
    failing = {**manifest, "attempt": 2, "thresholds": {"checks": ["rate>1"]}}
    manifests = []
    for item in (manifest, failing):
        path = root / f"manifest-{item['attempt']}.json"
        path.write_bytes(quality_run._canonical(item))
        manifests.append((item, path))
    guard = root / "routes.yml"
    guard.write_bytes(quality_run._canonical(http_guard.configuration(manifest)))
    hashes = {
        "fixture_sha256": manifest["fixture_sha256"],
        "mappings_sha256": _tree_sha256(mappings),
        "guard_sha256": _sha256(guard),
        "manifest_sha256": [_sha256(path) for _, path in manifests],
    }
    return run_id, scenario, mappings, manifests, guard, hashes


def run_cycle(cycle, repo, images, inputs, modules, evidence):
    quality_run, container_executor = modules
    run_id, scenario, mappings, manifests, guard, hashes = inputs
    project = "hyhome-quality-guard-" + uuid.uuid4().hex[:12]
    receipt = {
        "cycle": cycle,
        "project": project,
        "run_id": run_id,
        "images": images,
        "inputs": hashes,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "attempts": [],
        "cleanup": None,
        "error": None,
    }
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
    attempts_root = pathlib.Path(tempfile.mkdtemp(prefix="hyhome-quality-attempts-"))
    attempts_root.chmod(0o755)
    created = False

    def command(args):
        result = subprocess.run(
            base + args, env=env, capture_output=True, text=True, check=False
        )
        if result.returncode:
            print(result.stderr)
            result.check_returncode()
        return result

    def name_of(container):
        return (
            subprocess.check_output(
                [
                    "docker",
                    "--context",
                    "default",
                    "inspect",
                    container,
                    "--format",
                    "{{.Name}}",
                ],
                text=True,
            )
            .strip()
            .lstrip("/")
        )

    try:
        if _owned(run_id) != {"containers": 0, "networks": 0}:
            raise RuntimeError(f"owned resources exist before cycle {cycle}")
        network_ids = subprocess.check_output(
            ["docker", "--context", "default", "network", "ls", "--quiet"], text=True
        ).split()
        if network_ids:
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
        print(f"CYCLE{cycle}_COMPOSE_RENDER_PASS")
        created = True
        command(["up", "--detach", "--pull", "never"])
        print(f"CYCLE{cycle}_ISOLATED_UP_PASS")
        time.sleep(15)
        peer_name = name_of(command(["ps", "--quiet", "path-guard"]).stdout.strip())
        backend_name = name_of(
            command(["ps", "--all", "--quiet", "mock-backend"]).stdout.strip()
        )
        from result_inspection import inspect_raw_points

        for (manifest, manifest_path), expected in zip(
            manifests, EXPECTED, strict=True
        ):
            attempt = attempts_root / f"attempt-{manifest['attempt']}"
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
            final = quality_run.finalize(attempt)
            points, issues = inspect_raw_points(attempt, manifest)
            receipt["attempts"].append(
                {
                    "attempt": manifest["attempt"],
                    "exit": code,
                    "verdict": final["verdict"],
                    "evidence_state": final["evidence_state"],
                    "import_allowed": final["import_allowed"],
                    "raw_points": points,
                    "raw_point_issues": len(issues),
                    "final_sha256": _sha256(attempt / "final.json"),
                }
            )
            # Keep the finalized evidence; the attempt directory is removed below.
            kept = evidence / f"cycle-{cycle}" / attempt.name
            kept.mkdir(parents=True)
            for name in ("final.json", "checksums.json"):
                shutil.copy2(attempt / name, kept / name)
            print(
                f"CYCLE{cycle}_ATTEMPT{manifest['attempt']}_EXIT",
                code,
                "VERDICT",
                final["verdict"],
                "EVIDENCE",
                final["evidence_state"],
            )
            require_result(code, final, expected["exit"], expected["verdict"])
            if expected["exit"] == 0 and (issues or not final["import_allowed"]):
                raise RuntimeError("native distribution acceptance failed")
        print(f"CYCLE{cycle}_EXACT_ALLOWED200_UNAPPROVED404_ADMIN404_PASS")
        print(f"CYCLE{cycle}_MANIFEST_THRESHOLD_OVERRIDE_FAILURE_PASS")
    except Exception as error:
        receipt["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        try:
            if created:
                command(["down", "--timeout", "10"])
            receipt["cleanup"] = _owned(run_id)
            if receipt["cleanup"] != {"containers": 0, "networks": 0}:
                receipt["error"] = receipt["error"] or "owned resources remain"
                print(f"CYCLE{cycle}_OWNED_CLEANUP_FAIL", receipt["cleanup"])
            else:
                print(f"CYCLE{cycle}_OWNED_CLEANUP_PASS")
            if receipt["error"]:
                # A failed attempt keeps its raw files for investigation.
                receipt["kept_attempts"] = str(attempts_root)
            else:
                shutil.rmtree(attempts_root)
        finally:
            receipt["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            path = evidence / f"cycle-{cycle}.json"
            path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    if receipt["error"]:
        raise RuntimeError(f"cycle {cycle} failed: {receipt['error']}")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guard-image", required=True)
    parser.add_argument("--mock-image", required=True)
    parser.add_argument("--k6-image", required=True)
    parser.add_argument(
        "--evidence-dir",
        required=True,
        type=pathlib.Path,
        help="new directory for the cycle receipts; it must not exist",
    )
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(repo / "infra/11-quality/k6"))
    quality_run = importlib.import_module("quality_run")
    container_executor = importlib.import_module("container_executor")
    http_guard = importlib.import_module("http_guard")

    images = {"guard": args.guard_image, "mock": args.mock_image, "k6": args.k6_image}
    if not http_guard.IMAGE.fullmatch(images["guard"]) or not all(
        "@sha256:" in value for value in images.values()
    ):
        raise ValueError("approved cached image digests are required")
    observed = subprocess.check_output(["docker", "context", "show"], text=True).strip()
    if observed != "default":
        raise ValueError("this rehearsal requires the approved default context")
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
    evidence = args.evidence_dir
    evidence.mkdir(parents=True, exist_ok=False)

    root = pathlib.Path(tempfile.mkdtemp(prefix="hyhome-quality-guard-"))
    root.chmod(0o755)
    receipts = []
    try:
        if shutil.disk_usage(root).free < 256 * 1024 * 1024:
            raise ValueError("insufficient fixture disk budget")
        inputs = write_inputs(root, images, quality_run, http_guard)
        modules = (quality_run, container_executor)
        for cycle in range(1, CYCLES + 1):
            receipts.append(run_cycle(cycle, repo, images, inputs, modules, evidence))
    finally:
        shutil.rmtree(root)
        for cycle in range(1, CYCLES + 1):
            if not (evidence / f"cycle-{cycle}.json").exists():
                print(f"CYCLE{cycle}_NOT_RUN")
    reasons = compare_cycles(receipts)
    (evidence / "comparison.json").write_text(
        json.dumps({"match": not reasons, "reasons": reasons}, indent=2) + "\n"
    )
    if reasons:
        raise RuntimeError("reload cycles differ: " + "; ".join(reasons))
    print("RELOAD_CYCLES_LOGICAL_MATCH_PASS")


if __name__ == "__main__":
    main()
