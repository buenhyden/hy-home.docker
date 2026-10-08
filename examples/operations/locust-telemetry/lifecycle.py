"""Locust LAB lifecycle under `lab.py` supervision; synthetic peers only.

Each case starts the authored LAB with the isolated overlay, lets
`lab.supervise` wait for the master, and checks the outcome, the propagated
exit code, the flushed CSV and the exact cleanup (SPEC-0214).
"""

import argparse
import csv
import importlib.util
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fixture = load("locust_acceptance", HERE / "acceptance.py")

# name, workers, run time, exit code on error, deadline s, action, expected
CASES = (
    ("propagated", 2, "6s", "1", 60, None, ("failed", 1)),
    ("completed", 2, "6s", "0", 60, None, ("completed", 0)),
    ("deadline", 2, "120s", "0", 12, None, ("deadline_exceeded", 124)),
    ("cancelled", 2, "120s", "0", 120, "sigterm", ("cancelled", 130)),
    ("master-crash", 2, "120s", "0", 120, "kill-master", ("failed", 137)),
    ("worker-drop", 2, "15s", "0", 60, "kill-worker", ("completed", 0)),
)
GRACE = 10
CHILD = """import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("lab", sys.argv[1])
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)
print(json.dumps(lab.supervise(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))))
"""


def csv_state(results):
    """complete: Aggregated row with requests; partial: file without it."""
    path = results / "locust_stats.csv"
    if not path.exists():
        return {"stats": "absent", "requests": 0, "history_rows": 0}
    rows = list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))
    aggregate = next((r for r in rows if r.get("Name") == "Aggregated"), None)
    history = results / "locust_stats_history.csv"
    count = int(aggregate["Request Count"]) if aggregate else 0
    return {
        "stats": "complete" if aggregate and count > 0 else "partial",
        "requests": count,
        "history_rows": max(
            0, len(history.read_text(encoding="utf-8").splitlines()) - 1
        )
        if history.exists()
        else 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locust-image", required=True)
    parser.add_argument("--mock-image", required=True)
    parser.add_argument("--docker-binary", default="/usr/bin/docker")
    args = parser.parse_args()
    scratch = Path(tempfile.mkdtemp(prefix="locust-lifecycle-"))
    env = fixture.client_environment(scratch, args.docker_binary)
    docker = [args.docker_binary, "--context", "default"]

    def call(*arguments, timeout=60, check=True):
        result = subprocess.run(
            [*docker, *arguments],
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        if check and result.returncode:
            raise RuntimeError(f"Docker command failed with exit {result.returncode}")
        return result

    scenario, mappings = scratch / "scenario", scratch / "mappings"
    for path in (scenario, mappings):
        path.mkdir()
    shutil.copyfile(HERE / "locustfile.py", scenario / "locustfile.py")
    for name, path, delay in (("health", "/health", 0), ("timeout", "/slow", 250)):
        (mappings / f"{name}.json").write_text(
            json.dumps(
                {
                    "request": {"method": "GET", "urlPath": path},
                    "response": {
                        "status": 200,
                        "body": "synthetic",
                        "fixedDelayMilliseconds": delay,
                    },
                }
            )
        )
    empty_env = scratch / "synthetic.env"
    empty_env.write_text("")
    failures = []
    for name, workers, run_time, on_error, deadline, action, expected in CASES:
        project = f"locust-life-{name}-{uuid.uuid4().hex[:8]}"
        results = scratch / f"results-{name}"
        results.mkdir()
        case_env = dict(
            env,
            QUALITY_LOCUST_IMAGE=args.locust_image,
            QUALITY_MOCK_IMAGE=args.mock_image,
            QUALITY_UID=str(os.getuid()),
            QUALITY_GID=str(os.getgid()),
            QUALITY_SCENARIO_DIR=str(scenario),
            QUALITY_RESULTS_DIR=str(results),
            QUALITY_MAPPINGS_DIR=str(mappings),
            LAB_LOCUST_SCENARIO_DIR=str(scenario),
            LAB_LOCUST_RESULT_DIR=str(results),
            LAB_LOCUST_NETWORK_NAME=project + "-isolated",
            LAB_LOCUST_EXPECT_WORKERS=str(workers),
            LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT="30",
            LAB_LOCUST_USERS="4",
            LAB_LOCUST_SPAWN_RATE="4",
            LAB_LOCUST_RUN_TIME=run_time,
            LAB_LOCUST_STOP_TIMEOUT="2",
            LAB_LOCUST_EXIT_CODE_ON_ERROR=on_error,
        )
        compose = [
            *docker, "compose", "--env-file", str(empty_env), "--project-name",
            project, "-f", str(ROOT / "labs/locust.yml"), "-f",
            str(HERE / "compose.override.yml"), "--profile", "lab-locust",
        ]  # fmt: skip

        def run_compose(*arguments, timeout=90, _env=case_env, _compose=compose):
            result = subprocess.run(
                [*_compose, *arguments],
                env=_env,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout,
            )
            if result.returncode:
                raise RuntimeError(f"compose failed with exit {result.returncode}")
            return result.stdout

        record = {"case": name}
        try:
            run_compose(
                "up", "--detach", "--no-build", "--pull", "never", "mock-backend"
            )
            mock = run_compose("ps", "--quiet", "mock-backend").strip()
            for _ in range(30):
                probe = call(
                    "exec", mock, "wget", "-q", "-O", "/dev/null",
                    "http://localhost:8080/health", check=False,
                )  # fmt: skip
                if probe.returncode == 0:
                    break
                time.sleep(1)
            run_compose(
                "up", "--detach", "--no-build", "--pull", "never", "--scale",
                f"lab-locust-worker={workers}", "lab-locust-master", "lab-locust-worker",
            )  # fmt: skip
            child = subprocess.Popen(
                [sys.executable, "-c", CHILD, str(ROOT / "scripts/operations/lab.py"),
                 args.docker_binary, project, str(deadline), str(GRACE)],
                stdout=subprocess.PIPE, text=True,
            )  # fmt: skip
            if action:
                time.sleep(8)
                master = run_compose("ps", "--quiet", "lab-locust-master").strip()
                worker = run_compose("ps", "--quiet", "lab-locust-worker").split()[0]
                if action == "sigterm":
                    child.send_signal(signal.SIGTERM)
                elif action == "kill-master":
                    call("kill", "--signal", "KILL", master)
                else:
                    call("kill", "--signal", "KILL", worker)
            stdout, _ = child.communicate(timeout=deadline + GRACE + 60)
            outcome = tuple(json.loads(stdout.strip().splitlines()[-1]))
            master_id = run_compose(
                "ps", "--all", "--quiet", "lab-locust-master"
            ).strip()
            record.update(
                outcome=outcome[0],
                controller_code=outcome[1],
                master_exit=int(
                    call(
                        "inspect", "--format", "{{.State.ExitCode}}", master_id
                    ).stdout.strip()
                ),
                workers_running=len(
                    run_compose(
                        "ps", "--quiet", "--status", "running", "lab-locust-worker"
                    ).split()
                ),
                **csv_state(results),
            )
            if outcome != expected:
                failures.append(f"{name}: outcome {outcome} != {expected}")
            # Every case except the crash must leave a flushed, complete CSV.
            if name != "master-crash" and record["stats"] != "complete":
                failures.append(f"{name}: CSV {record['stats']}")
        except Exception as exc:  # recorded, then cleanup still runs
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
        finally:
            subprocess.run(
                [*compose, "down", "--timeout", "10"],
                env=case_env,
                capture_output=True,
                check=False,
                timeout=120,
            )
            left = call(
                "ps", "--all", "--quiet", "--filter",
                f"label=com.docker.compose.project={project}",
            ).stdout.strip()  # fmt: skip
            record["leftovers"] = len(left.split())
            if left:
                failures.append(f"{name}: owned containers remain")
            print(json.dumps(record), flush=True)
    if failures:
        print("FAIL", json.dumps(failures), flush=True)
        print("scratch preserved:", scratch, flush=True)
        raise SystemExit(1)
    shutil.rmtree(scratch)
    print("PASS locust lifecycle; exact owned cleanup", flush=True)


if __name__ == "__main__":
    main()
