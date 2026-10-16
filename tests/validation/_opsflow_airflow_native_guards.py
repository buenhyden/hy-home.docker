"""Pure Airflow admission checks and host resource observations; no Docker calls."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
from pathlib import Path

AIRFLOW_ID = "sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2"
AIRFLOW_MANIFEST_ID = (
    "sha256:c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e"
)
AIRFLOW_CONFIG_ID = (
    "sha256:4644ae58fef15a94f8c82d3b27a5e7c60942262a43ec1640757a5f5dcbf39b04"
)


class RehearsalFailure(AssertionError):
    """Static diagnostic; no raw Docker or dependency payload."""


def postgres_command(role):
    rules = {
        "metadata-pg": "host airflow airflow samenet scram-sha-256",
        "dev-pg": "host opsflow_dev opsflow_ingest samenet scram-sha-256",
    }
    if role not in rules:
        raise RehearsalFailure("PostgreSQL fixture role rejected")
    return (
        "sh",
        "-ceu",
        "initdb -D /var/lib/postgresql/18/docker --auth-local=trust --auth-host=scram-sha-256 --username=p04_audit; "
        "printf '%s\\n' '"
        + rules[role]
        + "' >> /var/lib/postgresql/18/docker/pg_hba.conf; "
        "exec postgres -D /var/lib/postgresql/18/docker -c listen_addresses='*' -c unix_socket_directories=/var/run/postgresql -c max_connections=40 -c shared_buffers=32MB",
    )


def exact_container_absent(result, cid):
    if (
        result.returncode == 0
        and result.stdout.strip() == cid
        and not result.stderr.strip()
    ):
        return False
    if (
        result.returncode == 1
        and not result.stdout.strip()
        and result.stderr.strip().casefold() == "error: no such object: " + cid
    ):
        return True
    raise RehearsalFailure("exact container absence unknown")


S3_SERVER_COMMAND = tuple(
    (
        "weed -config_dir=/data server -filer -s3 -dir=/data -ip=seaweedfs-s3 -ip.bind=0.0.0.0 "
        "-volume.max=2 -master.volumeSizeLimitMB=64 -master.telemetry=false "
        "-s3.port=8333 -s3.config=/data/s3.json -s3.iam=false"
    ).split()
)


def validate_s3_policy(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate policy field")
            result[key] = value
        return result

    if (
        not isinstance(raw, str)
        or len(raw.encode()) > 65536
        or "simulation" in raw.casefold()
    ):
        raise RehearsalFailure("S3 policy readback rejected")
    try:
        value, _ = json.JSONDecoder(object_pairs_hook=unique).raw_decode(
            raw[raw.index("{") :]
        )
        locations = value["locations"]
        if not isinstance(locations, list) or len(locations) != 1:
            raise ValueError("exact policy rule required")
        rule = locations[0]
        if (
            not isinstance(rule, dict)
            or rule.get("locationPrefix") != "/buckets/opsflow-dev"
            or type(rule.get("volumeGrowthCount")) is not int
            or rule["volumeGrowthCount"] != 1
        ):
            raise ValueError("exact policy scope and count required")
    except (ValueError, TypeError, KeyError):
        raise RehearsalFailure("S3 policy readback rejected") from None


def validate_target(environment):
    if (
        environment.get("OPSFLOW_AIRFLOW_NATIVE_IMAGE"),
        environment.get("OPSFLOW_AIRFLOW_NATIVE_CONTEXT"),
    ) != (AIRFLOW_ID, "default"):
        raise RehearsalFailure("exact cached Airflow image/context required")
    if any(
        environment.get(k)
        for k in "DOCKER_HOST DOCKER_CONTEXT DOCKER_TLS_VERIFY DOCKER_CERT_PATH".split()
    ):
        raise RehearsalFailure("Docker environment overrides rejected")


def validate_probe(value):
    if (
        type(value.get("uid")) is not int
        or value["uid"] <= 0
        or type(value.get("gid")) is not int
        or value["gid"] < 0
        or value.get("airflow") != "3.3.2"
        or value.get("celery") != "3.24.1"
        or any(value.get(k) is not True for k in ("boto3", "psycopg2", "sdk"))
        or value.get("forbidden_env") != []
    ):
        raise RehearsalFailure("Airflow UID/driver/provider preflight rejected")
    return value["uid"], value["gid"]


def probe_observations(value):
    primitives = {
        k: value.get(k) if type(value.get(k)) is kind else None
        for kind, keys in ((int, "uid gid"), (bool, "boto3 psycopg2 sdk"))
        for k in keys.split()
    }
    versions = {
        k: value.get(k)
        if isinstance(value.get(k), str)
        and re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value[k])
        else None
        for k in "airflow celery".split()
    }
    known = "PGPASSWORD PGHOST PGPORT PGUSER PGDATABASE PGSERVICE PGSERVICEFILE PGPASSFILE SSL_CERT_DIR SSL_CERT_FILE".split()
    raw = value.get("forbidden_env")
    names = (
        [name for name in raw if isinstance(name, str) and name in known]
        if isinstance(raw, list)
        else []
    )
    return {
        **primitives,
        **versions,
        "forbidden_env": names,
        "forbidden_environment_present": raw != [],
    }


def host_resources():
    memory = dict(
        line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines()
    )
    disk = os.statvfs("/tmp")
    return {
        "memory": int(memory["MemAvailable"].split()[0]) * 1024,
        "swap": int(memory["SwapFree"].split()[0]) * 1024,
        "disk": shutil.disk_usage("/tmp").free,
        "inode_ratio": disk.f_favail / disk.f_files if disk.f_files else 0,
    }


def validate_resources(value, prestart=False):
    if value["memory"] < (7 if prestart else 3) * 1024**3 or (
        prestart and (value["disk"] < 10 * 1024**3 or value["inode_ratio"] < 0.1)
    ):
        raise RehearsalFailure("host resource reserve insufficient")


def validate_airflow_platform(descriptor):
    platform = descriptor.get("platform") or {}
    if (
        descriptor.get("digest"),
        descriptor.get("mediaType"),
        platform.get("os"),
        platform.get("architecture"),
    ) != (
        AIRFLOW_MANIFEST_ID,
        "application/vnd.oci.image.manifest.v1+json",
        "linux",
        "amd64",
    ):
        raise RehearsalFailure("Airflow platform manifest binding rejected")


def airflow_runtime_identity(value):
    identities = {
        AIRFLOW_ID: "OCI index",
        AIRFLOW_MANIFEST_ID: "linux/amd64 manifest",
        AIRFLOW_CONFIG_ID: "image config",
    }
    if value not in identities:
        raise RehearsalFailure("Airflow runtime digest binding rejected")
    return identities[value]


def network_alias(role):
    return {"api": "airflow-apiserver", "s3": "seaweedfs-s3"}.get(role, role)


def ordinary_networks_match(state, actual, expected):
    if (
        state not in {"created", "running", "exited"}
        or not isinstance(actual, dict)
        or set(actual) != set(expected)
    ):
        return False
    for name, (network_id, aliases) in expected.items():
        endpoint = actual[name]
        if not isinstance(endpoint, dict) or endpoint.get("Aliases") != aliases:
            return False
        if state == "created":
            if endpoint.get("NetworkID") != "" or endpoint.get("EndpointID") != "":
                return False
        elif endpoint.get("NetworkID") != network_id or (
            state == "running" and not isinstance(endpoint.get("EndpointID"), str)
        ):
            return False
        elif state == "running":
            if not re.fullmatch(r"[0-9a-f]{64}", endpoint["EndpointID"]):
                return False
        elif endpoint.get("EndpointID") != "":
            return False
    return True


CAPS = {
    "metadata-pg": (256, 150, 128),
    "dev-pg": (384, 200, 128),
    "valkey": (64, 50, 64),
    "s3": (384, 150, 128),
    "api": (512, 250, 256),
    "scheduler": (512, 300, 256),
    "processor": (512, 250, 256),
    "worker": (1024, 650, 256),
}


def private_identity(path):
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        try:
            value = os.fstat(descriptor)
            if (
                not stat.S_ISREG(value.st_mode)
                or value.st_nlink != 1
                or value.st_uid != os.geteuid()
                or stat.S_IMODE(value.st_mode) != 0o600
                or value.st_size > 2 * 1024**2
            ):
                raise RehearsalFailure("private file identity rejected")
            digest = hashlib.sha256()
            while block := os.read(descriptor, 65536):
                digest.update(block)
            after = os.fstat(descriptor)
            stable = "st_dev st_ino st_uid st_mode st_nlink st_size st_mtime_ns st_ctime_ns".split()
            identity = tuple(getattr(value, key) for key in stable)
            if any(getattr(value, key) != getattr(after, key) for key in stable):
                raise RehearsalFailure("private file changed while reading")
            return (*identity, digest.hexdigest())
        finally:
            os.close(descriptor)
    except OSError:
        raise RehearsalFailure("private file identity rejected") from None


def create_options(role, user):
    memory, milli_cpu, pids = CAPS.get(role, (512, 250, 128))
    args = [
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges=true",
        "--memory",
        f"{memory}m",
        "--memory-swap",
        f"{memory}m",
        "--cpus",
        str(milli_cpu / 1000),
        "--pids-limit",
        str(pids),
        "--stop-timeout",
        "5",
        "--tmpfs",
        "/tmp:rw,nosuid,nodev,noexec,mode=1777,size=64m",
    ]
    if role == "probe":
        return args
    args += ["--user", user]
    uid, gid = map(int, user.split(":"))
    locations = {
        "metadata-pg": (("/var/lib/postgresql", 128), ("/var/run/postgresql", 16)),
        "dev-pg": (("/var/lib/postgresql", 192), ("/var/run/postgresql", 16)),
        "valkey": (("/data", 16),),
        "s3": (("/data", 192),),
    }.get(role, ())
    if role in ("api", "scheduler", "processor", "worker", "probe"):
        locations = (
            ("/opt/airflow/dags", 8),
            ("/opt/airflow/logs", 32),
            ("/run/opsflow", 1),
            ("/run/airflow-fixture", 1),
        )
    for target, size in locations:
        args += [
            "--tmpfs",
            f"{target}:rw,nosuid,nodev,noexec,mode=0700,uid={uid},gid={gid},size={size}m",
        ]
    return args


def validate_airflow_environment(assignment):
    if assignment == "AIRFLOW_CONFIG=/tmp/airflow.cfg":
        return
    key, _, _value = assignment.partition("=")
    if not key.startswith("AIRFLOW__") or key.endswith(("_PASSWORD", "_TOKEN", "_KEY")):
        raise RehearsalFailure("unreviewed Airflow environment")


def safe_exception(error):
    name = type(error).__name__
    known = {
        "RehearsalFailure",
        "AssertionError",
        "PermissionError",
        "OSError",
        "TimeoutError",
        "ValueError",
        "KeyError",
        "JSONDecodeError",
        "RuntimeError",
        "FileNotFoundError",
        "KeyboardInterrupt",
        "SystemExit",
    }
    return name if name in known else "OtherException"


def cleanup_observation(stage, role, error=None):
    stages = {
        "verify",
        "rm",
        "absence",
        "removed",
        "container-remove",
        "pending-container",
        "pending-network",
        "network-verify",
        "network-rm",
        "network-absence",
        "network-removed",
        "begin",
        "final-sweeps",
        "host",
        "unlock",
    }
    return {
        "stage": stage if stage in stages else "unknown",
        "role": role if role in (*CAPS, "probe", "control", "data") else None,
        "exception": safe_exception(error) if error is not None else None,
        "absent": None,
    }


def failure_evidence(role, args, result):
    commands = {
        ("airflow", "db", "migrate"): "airflow-db-migrate",
        ("airflow", "db", "check"): "airflow-db-check",
    }
    command = commands.get(tuple(args[:3]), "owned-command")
    if args and args[0] in {"psql", "python", "sh", "pg_dumpall", "pg_dump"}:
        command = args[0]
    code = result.returncode
    if role not in (*CAPS, "probe") or type(code) is not int or not -255 <= code <= 255:
        raise RehearsalFailure("failure evidence identity rejected")
    fact = {
        "role": role,
        "command": command,
        "exit_code": code,
        "exit_class": "signal" if code < 0 else "nonzero" if code else "success",
    }
    streams = {}
    for name in ("stdout", "stderr"):
        raw = getattr(result, name, "").encode("utf-8")
        truncated = len(raw) > 256 * 1024
        parts = (raw[: 128 * 1024], raw[-128 * 1024 :]) if truncated else (raw,)
        text = "".join(part.decode("utf-8", errors="ignore") for part in parts)
        encoded = text.encode("utf-8")
        streams[name] = text
        fact[name] = {
            "bytes": len(encoded),
            "source_bytes": len(raw),
            "retention": "head-tail" if truncated else "complete",
            "truncated": truncated,
            "sha256": hashlib.sha256(encoded).hexdigest(),
        }
    return fact, streams


def airflow_environment():
    values = {
        "CORE__EXECUTOR": "CeleryExecutor",
        "CORE__LOAD_EXAMPLES": "false",
        "CORE__DAGS_ARE_PAUSED_AT_CREATION": "true",
        "CORE__AUTH_MANAGER": "airflow.api_fastapi.auth.managers.simple.simple_auth_manager.SimpleAuthManager",
        "CORE__EXECUTION_API_SERVER_URL": "http://airflow-apiserver:8080/execution/",
        "CORE__FERNET_KEY_CMD": "cat /run/airflow-fixture/fernet",
        "API_AUTH__JWT_SECRET_CMD": "cat /run/airflow-fixture/jwt",
        "API_AUTH__JWT_ISSUER": "airflow",
        "DATABASE__SQL_ALCHEMY_CONN_CMD": "cat /run/airflow-fixture/database",
        "CELERY__RESULT_BACKEND_CMD": "cat /run/airflow-fixture/result",
        "CELERY__BROKER_URL_CMD": "cat /run/airflow-fixture/broker",
        "CELERY__WORKER_CONCURRENCY": "1",
        "SCHEDULER__PARSING_PROCESSES": "1",
        "DAG_PROCESSOR__PARSING_PROCESSES": "1",
        "DAG_PROCESSOR__REFRESH_INTERVAL": "5",
        "DAG_PROCESSOR__MIN_FILE_PROCESS_INTERVAL": "5",
        "LOGGING__LOGGING_LEVEL": "WARNING",
        "CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE": "/run/airflow-fixture/simple-passwords.json",
    }
    return (
        "AIRFLOW_CONFIG=/tmp/airflow.cfg",
        *("AIRFLOW__" + key + "=" + value for key, value in values.items()),
    )


_RETAINED_FILES = frozenset(
    {
        "synthetic-input.json",
        "synthetic-secrets.json",
        "failure-stdout.txt",
        "failure-stderr.txt",
        "metadata-pg-snapshot",
        "dev-pg-snapshot",
        "metadata-pg-roles",
        "dev-pg-roles",
        "s3-snapshot.json",
    }
)
_IDENTITY_FIELDS = (
    "st_dev st_ino st_uid st_mode st_nlink st_size st_mtime_ns st_ctime_ns".split()
)


def _directory_identity(descriptor):
    item = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(item.st_mode)
        or item.st_uid != os.geteuid()
        or stat.S_IMODE(item.st_mode) != 0o700
    ):
        raise RehearsalFailure("retained evidence directory rejected")
    return [item.st_dev, item.st_ino, item.st_uid, item.st_mode, item.st_nlink]


def _bound_evidence_file(directory_fd, name, expected, metadata=False):
    if (
        not isinstance(expected, (list, tuple))
        or len(expected) != 9
        or any(type(v) is not int or v < 0 for v in expected[:8])
        or not isinstance(expected[-1], str)
        or not re.fullmatch(r"[0-9a-f]{64}", expected[-1])
    ):
        raise RehearsalFailure("retained file identity shape rejected")
    descriptor = os.open(
        name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory_fd
    )
    try:
        before = os.fstat(descriptor)
        maximum = 32 * 1024 if metadata else 2 * 1024**2
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_uid != os.geteuid()
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_nlink != 1
            or before.st_size > maximum
        ):
            raise RehearsalFailure("retained file metadata rejected")
        digest, content, total = hashlib.sha256(), bytearray(), 0
        while block := os.read(descriptor, 65536):
            total += len(block)
            if total > before.st_size:
                raise RehearsalFailure("retained evidence grew while reading")
            digest.update(block)
            if metadata:
                content.extend(block)
        identity = [getattr(before, key) for key in _IDENTITY_FIELDS]
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if (
            any(
                getattr(after, key) != getattr(before, key)
                or getattr(named, key) != getattr(before, key)
                for key in _IDENTITY_FIELDS
            )
            or total != before.st_size
            or [*identity, digest.hexdigest()] != list(expected)
        ):
            raise RehearsalFailure("retained file identity changed")
        return bytes(content) if metadata else None
    finally:
        os.close(descriptor)


def retained_metadata(directory, expected_directory, files, command):
    descriptor = os.open(
        directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    try:
        parent = _directory_identity(descriptor)
        if parent[:2] != list(expected_directory):
            raise RehearsalFailure("owned evidence directory changed")
        identities = {path.name: list(identity) for path, identity in files.items()}
        if not set(identities) <= _RETAINED_FILES or not {
            "failure-stdout.txt",
            "failure-stderr.txt",
        } <= set(identities):
            raise RehearsalFailure("retained authored file set rejected")
        if set(os.listdir(descriptor)) != {*identities, "docker-config"}:
            raise RehearsalFailure("unexpected retained host entry")
        for name, identity in identities.items():
            _bound_evidence_file(descriptor, name, identity)
        config = os.open(
            "docker-config",
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=descriptor,
        )
        try:
            config_identity = [
                *_directory_identity(config),
                os.fstat(config).st_ctime_ns,
            ]
            if os.listdir(config):
                raise RehearsalFailure("retained Docker config is not empty")
        finally:
            os.close(config)
        return {
            "directory_identity": parent,
            "config_directory_identity": config_identity,
            "file_identities": identities,
            "command": command,
        }
    finally:
        os.close(descriptor)


def retained_failure_evidence(directory, metadata_identity):
    descriptor = os.open(
        directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    try:
        body = _bound_evidence_file(
            descriptor, "failure-metadata.json", metadata_identity, metadata=True
        )
        value = json.loads(body)
        if set(value) != {
            "directory_identity",
            "config_directory_identity",
            "file_identities",
            "command",
        }:
            raise RehearsalFailure("retained metadata fields rejected")
        files = value["file_identities"]
        if (
            not isinstance(files, dict)
            or not set(files) <= _RETAINED_FILES
            or not {"failure-stdout.txt", "failure-stderr.txt"} <= set(files)
        ):
            raise RehearsalFailure("retained authored file set rejected")
        if _directory_identity(descriptor) != value["directory_identity"] or set(
            os.listdir(descriptor)
        ) != {*files, "failure-metadata.json", "docker-config"}:
            raise RehearsalFailure("retained directory identity or entries changed")
        for name, identity in files.items():
            _bound_evidence_file(descriptor, name, identity)
        config = os.open(
            "docker-config",
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=descriptor,
        )
        try:
            if [*_directory_identity(config), os.fstat(config).st_ctime_ns] != value[
                "config_directory_identity"
            ] or os.listdir(config):
                raise RehearsalFailure("retained Docker config changed")
        finally:
            os.close(config)
        named_config = os.stat(
            "docker-config", dir_fd=descriptor, follow_symlinks=False
        )
        config_fields = [
            named_config.st_dev,
            named_config.st_ino,
            named_config.st_uid,
            named_config.st_mode,
            named_config.st_nlink,
            named_config.st_ctime_ns,
        ]
        if config_fields != value["config_directory_identity"]:
            raise RehearsalFailure("retained Docker config path changed")
        named = directory.stat(follow_symlinks=False)
        if [named.st_dev, named.st_ino] != value["directory_identity"][:2] or set(
            os.listdir(descriptor)
        ) != {*files, "failure-metadata.json", "docker-config"}:
            raise RehearsalFailure("retained directory path changed")
        return value
    finally:
        os.close(descriptor)
