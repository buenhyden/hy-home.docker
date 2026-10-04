"""Run only synthetic Locust LAB peers with exact owned cleanup."""

import argparse
import csv
import io
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def client_environment(scratch, binary):
    path = Path(binary)
    if not path.is_absolute() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("untrusted Docker binary")
    info = path.stat()
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != 0
        or info.st_mode & 0o022
        or not os.access(path, os.X_OK)
    ):
        raise ValueError("untrusted Docker binary")
    home = scratch / "client-home"
    config = scratch / "docker-config"
    home.mkdir(mode=0o700)
    config.mkdir(mode=0o700)
    return {
        "PATH": "/usr/bin:/bin",
        "HOME": str(home),
        "DOCKER_CONFIG": str(config),
        "LANG": "C.UTF-8",
    }


def bounded_read(path, limit):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("unsafe artifact path")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC)
        with os.fdopen(fd, "rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
                raise ValueError("invalid artifact type or size")
            content = stream.read(limit + 1)
            after = os.fstat(stream.fileno())
            if len(content) > limit or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
                before.st_ctime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ):
                raise ValueError("artifact changed or exceeded quota")
            return content
    except OSError:
        raise ValueError("artifact unavailable") from None


def regular_present(path):
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def read_evidence(path):
    sys.path.insert(0, str(ROOT / "infra/11-quality/k6"))
    from quality_run import _pairs, _reject_nonfinite

    try:
        evidence = json.loads(bounded_read(path, 65536), object_pairs_hook=_pairs)
        _reject_nonfinite(evidence)
    except (ValueError, TypeError, OverflowError, RecursionError):
        raise ValueError("invalid bounded event artifact") from None
    required = {
        "schema_version",
        "project_id",
        "client",
        "counter_unit",
        "histogram_unit",
        "timeout_seconds",
        "invalid_events",
        "read_timeouts",
        "series",
    }
    if not isinstance(evidence, dict) or set(evidence) != required:
        raise ValueError("unexpected event schema")
    if (
        evidence["schema_version"] != "hyhome.locust-event/v1"
        or evidence["project_id"] != "synthetic-locust"
        or evidence["client"] != "HttpUser.requests"
        or evidence["counter_unit"] != "requests"
        or evidence["histogram_unit"] != "ms"
        or evidence["timeout_seconds"] != 0.05
    ):
        raise ValueError("unexpected event constants")
    if not isinstance(evidence["series"], dict) or set(evidence["series"]) != {
        "health:200",
        "timeout:timeout",
    }:
        raise ValueError("unapproved event series")
    for count in (evidence["invalid_events"], evidence["read_timeouts"]):
        if type(count) is not int or not 0 <= count <= 1000:
            raise ValueError("invalid bounded event count")
    for value in evidence["series"].values():
        if (
            not isinstance(value, dict)
            or set(value) != {"count", "sum_ms", "buckets_ms", "infinity"}
            or not isinstance(value["buckets_ms"], dict)
            or set(value["buckets_ms"]) != {"25", "50", "100", "250", "1000"}
        ):
            raise ValueError("unexpected histogram schema")
        if (
            any(
                type(c) is not int or not 0 <= c <= 1000
                for c in (
                    value["count"],
                    value["infinity"],
                    *value["buckets_ms"].values(),
                )
            )
            or isinstance(value["sum_ms"], bool)
            or not isinstance(value["sum_ms"], (int, float))
        ):
            raise ValueError("invalid histogram scalar")
    return evidence


def read_csv(path):
    stream = io.StringIO(bounded_read(path, 65536).decode("utf-8"))
    reader = csv.DictReader(stream)
    required = {
        "Type",
        "Name",
        "Request Count",
        "Failure Count",
        "Median Response Time",
        "Average Response Time",
        "Min Response Time",
        "Max Response Time",
        "Average Content Size",
        "Requests/s",
        "Failures/s",
        "50%",
        "66%",
        "75%",
        "80%",
        "90%",
        "95%",
        "98%",
        "99%",
        "99.9%",
        "99.99%",
        "100%",
    }
    if (
        reader.fieldnames is None
        or len(reader.fieldnames) != len(required)
        or set(reader.fieldnames) != required
    ):
        raise ValueError("unexpected CSV schema")
    rows = list(reader)
    if len(rows) != 3 or {r.get("Name") for r in rows} != {
        "health",
        "timeout",
        "Aggregated",
    }:
        raise ValueError("unexpected CSV groups")
    for row in rows:
        if set(row) != required or row["Type"] not in {"GET", ""}:
            raise ValueError("unexpected CSV record")
        for key, value in row.items():
            if key not in {"Type", "Name"} and (
                len(value) > 64
                or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value)
                or not math.isfinite(float(value))
            ):
                raise ValueError("unsafe CSV value")
    return next(r for r in rows if r["Name"] == "Aggregated")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locust-image", required=True)
    parser.add_argument("--mock-image", required=True)
    parser.add_argument("--docker-binary", default="/usr/bin/docker")
    args = parser.parse_args()
    project = "locust-telemetry-" + uuid.uuid4().hex[:12]
    scratch = Path(tempfile.mkdtemp(prefix=project + "-"))
    created = False
    results = None
    try:
        for image, repository in (
            (args.locust_image, "locustio/locust"),
            (args.mock_image, "wiremock/wiremock"),
        ):
            if not re.fullmatch(re.escape(repository) + r"@sha256:[0-9a-f]{64}", image):
                raise ValueError("only approved immutable fixture images accepted")
        env = client_environment(scratch, args.docker_binary)

        def docker(*arguments, timeout=30):
            result = subprocess.run(
                [args.docker_binary, "--context", "default", *arguments],
                env=env,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout,
            )
            if result.returncode:
                raise RuntimeError(
                    "fixture Docker command failed with exit " + str(result.returncode)
                )
            return result

        context = json.loads(docker("context", "inspect", "default").stdout)[0]
        if not context["Endpoints"]["docker"]["Host"].startswith("unix://"):
            raise ValueError("local default Unix context required")
        for image in (args.locust_image, args.mock_image):
            info = json.loads(docker("image", "inspect", image).stdout)[0]
            if info["Os"] != "linux" or info["Architecture"] != "amd64":
                raise ValueError("approved architecture differs")
        if shutil.disk_usage("/tmp").free < 512 * 1024 * 1024:
            raise ValueError("insufficient scratch space")
        scenario, results, mappings = (
            scratch / name for name in ("scenario", "results", "mappings")
        )
        for path in (scenario, results, mappings):
            path.mkdir()
        shutil.copyfile(HERE / "locustfile.py", scenario / "locustfile.py")
        for name, path, delay in (("health", "/health", 0), ("timeout", "/slow", 250)):
            (mappings / (name + ".json")).write_text(
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
        env.update(
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
            LAB_LOCUST_EXPECT_WORKERS="1",
            LAB_LOCUST_USERS="1",
            LAB_LOCUST_SPAWN_RATE="1",
            LAB_LOCUST_RUN_TIME="4s",
            LAB_LOCUST_STOP_TIMEOUT="1",
            LAB_LOCUST_EXIT_CODE_ON_ERROR="1",
        )

        def compose(*arguments, timeout=30):
            return docker(
                "compose",
                "--env-file",
                str(empty_env),
                "--project-name",
                project,
                "-f",
                str(ROOT / "labs/locust.yml"),
                "-f",
                str(HERE / "compose.override.yml"),
                "--profile",
                "lab-locust",
                *arguments,
                timeout=timeout,
            )

        def resources_remain():
            return bool(
                docker(
                    "ps",
                    "--all",
                    "--quiet",
                    "--filter",
                    "label=com.docker.compose.project=" + project,
                ).stdout.strip()
                or docker(
                    "network",
                    "ls",
                    "--quiet",
                    "--filter",
                    "label=com.docker.compose.project=" + project,
                ).stdout.strip()
            )

        if resources_remain():
            raise ValueError("fixture project already exists")
        model = json.loads(compose("config", "--format", "json").stdout)
        if model.get("volumes") or model.get("secrets") or len(model["services"]) != 3:
            raise ValueError("unexpected fixture resources")
        for service in model["services"].values():
            if (
                service.get("ports")
                or service.get("privileged")
                or not service.get("read_only")
            ):
                raise ValueError("fixture isolation missing")
            for mount in service.get("volumes", []):
                if mount["type"] != "bind" or not Path(mount["source"]).is_relative_to(
                    scratch
                ):
                    raise ValueError("foreign fixture mount")
        if not model["networks"]["lab_locust_net"]["internal"]:
            raise ValueError("internal fixture network required")
        print(
            "PREFLIGHT",
            project,
            "CPU1.5 MEMORY1024MiB PORTS0 VOLUMES0 SECRETS0",
            flush=True,
        )
        created = True
        compose("up", "--detach", "--no-build", "--pull", "never", "mock-backend")
        # No request log/body is read: only the disposable backend readiness exit.
        mock = compose("ps", "--quiet", "mock-backend").stdout.strip()
        for _ in range(20):
            probe = subprocess.run(
                [
                    args.docker_binary,
                    "--context",
                    "default",
                    "exec",
                    mock,
                    "wget",
                    "-q",
                    "-O",
                    "/dev/null",
                    "http://localhost:8080/health",
                ],
                env=env,
                capture_output=True,
                check=False,
                timeout=5,
            )
            if probe.returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError("synthetic backend not ready")
        compose(
            "up",
            "--detach",
            "--no-build",
            "--pull",
            "never",
            "lab-locust-master",
            "lab-locust-worker",
        )
        master = compose("ps", "--all", "--quiet", "lab-locust-master").stdout.strip()
        exit_code = int(docker("wait", master, timeout=60).stdout.strip())
        deadline = time.monotonic() + 10
        while not list(results.glob("events-*.json")) and time.monotonic() < deadline:
            time.sleep(0.2)
        event_files = list(results.glob("events-*.json"))
        if exit_code != 1 or len(event_files) != 1:
            raise RuntimeError("bounded expected timeout evidence incomplete")
        evidence = read_evidence(event_files[0])
        if (
            evidence["invalid_events"]
            or evidence["read_timeouts"] < 1
            or evidence["client"] != "HttpUser.requests"
            or evidence["histogram_unit"] != "ms"
        ):
            raise RuntimeError("client-specific telemetry invalid")
        if set(evidence["series"]) != {"health:200", "timeout:timeout"}:
            raise RuntimeError("unexpected status/group cardinality")
        total = 0
        for record in evidence["series"].values():
            count = record["count"]
            if (
                count < 1
                or record["infinity"] != count
                or not math.isfinite(record["sum_ms"])
                or record["sum_ms"] < 0
            ):
                raise RuntimeError("counter histogram reconciliation failed")
            buckets = [record["buckets_ms"][str(b)] for b in (25, 50, 100, 250, 1000)]
            if buckets != sorted(buckets) or buckets[-1] > count:
                raise RuntimeError("invalid cumulative buckets")
            total += count
        aggregate = read_csv(results / "locust_stats.csv")
        if (
            int(aggregate["Request Count"]) != total
            or int(aggregate["Failure Count"]) != evidence["read_timeouts"]
        ):
            raise RuntimeError("master/worker event CSV reconciliation failed")
        print(
            "HEADLESS_EXIT1_EXPECTED_TIMEOUT_PASS",
            "COUNTER",
            total,
            "READ_TIMEOUTS",
            evidence["read_timeouts"],
            "HISTOGRAM_MS_STATUS_GROUP_PRIVACY_PASS",
            flush=True,
        )
    except Exception:
        print(
            "FIXTURE_FAILURE",
            "event_files",
            len(list(results.glob("events-*.json"))) if results is not None else 0,
            "csv_present",
            regular_present(results / "locust_stats.csv")
            if results is not None
            else False,
            flush=True,
        )
        raise
    finally:
        if created:
            compose("down", "--timeout", "10")
            if resources_remain():
                raise RuntimeError(
                    "owned fixture cleanup incomplete; scratch preserved"
                )
            print("OWNED_CLEANUP_PASS", project, flush=True)
        shutil.rmtree(scratch)


if __name__ == "__main__":
    main()
