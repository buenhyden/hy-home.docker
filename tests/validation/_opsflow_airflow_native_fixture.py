"""Owned serial Airflow fixture; no runtime work occurs at import."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import secrets
import stat
import time
from dataclasses import dataclass
from pathlib import Path

from tests.validation._opsflow_airflow_native_evidence import (
    capture_failure,
    capture_s3_upload_failure,
)
from tests.validation._opsflow_airflow_native_guards import (
    AIRFLOW_CONFIG_ID,
    AIRFLOW_ID,
    AIRFLOW_MANIFEST_ID,
    CAPS,
    RehearsalFailure,
    airflow_runtime_identity,
    cleanup_observation,
    create_options,
    exact_container_absent,
    host_resources,
    network_alias,
    ordinary_networks_match,
    private_identity,
    probe_observations,
    safe_exception,
    validate_airflow_environment,
    validate_airflow_platform,
    validate_probe,
    validate_resources,
    validate_s3_policy,
    validate_target,
)
from tests.validation._opsflow_airflow_native_guards import (
    S3_SERVER_COMMAND as S3_SERVER_COMMAND,
)
from tests.validation._opsflow_airflow_native_guards import (
    airflow_environment as airflow_environment,
)
from tests.validation._opsflow_airflow_native_guards import (
    failure_evidence as failure_evidence,
)
from tests.validation._opsflow_airflow_native_guards import (
    postgres_command as postgres_command,
)
from tests.validation._opsflow_airflow_native_guards import (
    retained_failure_evidence as retained_failure_evidence,
)
from tests.validation._opsflow_airflow_native_guards import (
    retained_metadata as retained_metadata,
)
from tests.validation._supabase_smtp_fixture_storage import write_exclusive
from tests.validation.test_datastore_rehearsal_boundary import DockerClientBoundary

ROOT = Path(__file__).resolve().parents[2]
WORKLOAD = ROOT / "infra/07-workflow/airflow/workloads/manifest-pipeline"
PG_ID = "sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873"
VALKEY_ID = "sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b"
S3_ID = "sha256:4e61d15fd35994cb1e43e1e553dff106794841fd9a99ade2fc8c8bfce4d7872d"
IMAGES = frozenset((AIRFLOW_ID, PG_ID, VALKEY_ID, S3_ID))
OWNER_LABEL = "hyhome.opsflow.native-owner"
ATTEMPT_LABEL = "hyhome.opsflow.native-attempt"
ROLE_LABEL = "hyhome.opsflow.native-role"
OWNER = "test_opsflow_airflow_native_rehearsal"
PREFIX = "hyhome-opsflow-airflow-native-attempt-"
LOCK = Path("/tmp/hyhome-opsflow-native-rehearsal.lock")
CID = re.compile(r"[0-9a-f]{64}\Z")
PROBE = """import json,os
from importlib.metadata import version
import boto3,psycopg2,airflow.sdk
forbidden=[k for k in os.environ if k.startswith('PG') or k in ('SSL_CERT_DIR','SSL_CERT_FILE')]
print(json.dumps(dict(uid=os.getuid(),gid=os.getgid(),airflow=version('apache-airflow'),celery=version('apache-airflow-providers-celery'),boto3=True,psycopg2=True,sdk=True,forbidden_env=[k for k in forbidden if os.environ.get(k)])))
"""
WRITE_FILES = """import json,os,pathlib,sys
os.umask(0o077)
for path,body in json.load(sys.stdin).items():
 p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 with p.open('x') as stream:stream.write(body)
"""


@dataclass(frozen=True)
class Container:
    cid: str
    name: str
    role: str
    image: str
    generation: int
    user: str
    networks: tuple[str, ...]


class AirflowFixture:
    def __init__(self):
        validate_target(os.environ)
        self.started = time.monotonic()
        self.work_deadline = self.started + 780
        self.deadline = self.started + 900
        self.attempt = "p04-airflow-" + secrets.token_hex(12)
        self.directory = Path("/tmp") / (PREFIX + secrets.token_hex(12))
        self.files, self.containers, self.networks = {}, {}, {}
        self.pending_containers, self.pending_networks = {}, {}
        self.runtime_images = {}
        self.generation = 1
        self.lock_fd, self.dir_identity = -1, None
        self.receipt = {
            "attempt": self.attempt,
            "publication": "NOT_RUN",
            "recovery": "NOT_RUN",
            "cleanup": "PENDING",
        }
        self._prepare_host()
        try:
            config = self.directory / "docker-config"
            config.mkdir(mode=0o700)
            self.client = DockerClientBoundary(
                binary=Path("/usr/bin/docker"),
                socket_path=Path("/var/run/docker.sock"),
                config_dir=config,
                deadline_seconds=780,
            )
            self.client.deadline = self.work_deadline
        except Exception:
            self._cleanup_host()
            self._unlock()
            raise

    def _prepare_host(self):
        self.lock_fd = os.open(
            LOCK, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600
        )
        item = os.fstat(self.lock_fd)
        if (
            not stat.S_ISREG(item.st_mode)
            or item.st_uid != os.geteuid()
            or item.st_nlink != 1
            or stat.S_IMODE(item.st_mode) != 0o600
        ):
            self._unlock()
            raise RehearsalFailure("shared native lock rejected")
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._unlock()
            raise RehearsalFailure("another native rehearsal owns the host") from None
        if any(Path("/tmp").glob(PREFIX + "*")) or any(
            Path("/tmp").glob("hyhome-opsflow-native-attempt-*")
        ):
            self._unlock()
            raise RehearsalFailure("stale native attempt blocks execution")
        try:
            self.directory.mkdir(mode=0o700)
            metadata = self.directory.stat(follow_symlinks=False)
            self.dir_identity = metadata.st_dev, metadata.st_ino
        except Exception:
            self._unlock()
            raise

    def remaining(self):
        validate_resources(host_resources())
        if time.monotonic() >= self.work_deadline:
            raise RehearsalFailure("Airflow workload deadline reached")

    def private(self, name, body):
        path = write_exclusive(self.directory, name, body, 0o600)
        self.files[path] = private_identity(path)
        return path

    def prerequisites(self):
        self.remaining()
        if (
            self.client.run("ps", "-aq", "--filter", "label=" + OWNER_LABEL).split()
            or self.client.run(
                "network", "ls", "-q", "--filter", "label=" + OWNER_LABEL
            ).split()
        ):
            raise RehearsalFailure("another owned native resource exists")
        validate_resources(host_resources(), prestart=True)
        for image in IMAGES:
            item = json.loads(
                self.client.run(
                    "image",
                    "inspect",
                    "--format",
                    '{"Id":{{json .Id}},"Os":{{json .Os}},"Architecture":{{json .Architecture}}}',
                    image,
                )
            )
            if (item.get("Id"), item.get("Os"), item.get("Architecture")) != (
                image,
                "linux",
                "amd64",
            ):
                raise RehearsalFailure("cached image/platform mismatch")

        descriptor = json.loads(
            self.client.run(
                "image",
                "inspect",
                "--platform",
                "linux/amd64",
                "--format",
                "{{json .Descriptor}}",
                AIRFLOW_ID,
            )
        )
        validate_airflow_platform(descriptor)

    def probe(self):
        record = self.create(
            "probe", AIRFLOW_ID, "airflow", (), ("python", "-c", PROBE)
        )
        self.start("probe")
        self.remaining()
        result = self.client.run("wait", record.cid).strip()
        if result != "0":
            raise RehearsalFailure("cached Airflow driver probe failed")
        payload = json.loads(self.client.run("logs", record.cid))
        self.receipt["probe"] = {"image": AIRFLOW_ID, **probe_observations(payload)}
        self.uid, self.gid = validate_probe(payload)
        self.remove("probe")

    def create_networks(self):
        validate_resources(host_resources(), prestart=True)
        for role in ("control", "data"):
            self.remaining()
            name = f"{self.attempt}-{role}"
            self.pending_networks[role] = name
            result = self.client.run_result(
                "network",
                "create",
                "--internal",
                "--label",
                f"{OWNER_LABEL}={OWNER}",
                "--label",
                f"{ATTEMPT_LABEL}={self.attempt}",
                name,
            )
            self.adopt_network(role, name)
            if result.returncode or role not in self.networks:
                raise RehearsalFailure("owned network create failed")

    def adopt_network(self, role, name):
        found = self.client.run(
            "network",
            "ls",
            "-q",
            "--no-trunc",
            "--filter",
            "name=^" + name + "$",
            "--filter",
            f"label={ATTEMPT_LABEL}={self.attempt}",
        ).split()
        if not found:
            return
        if len(found) != 1 or not CID.fullmatch(found[0]):
            raise RehearsalFailure("network identity ambiguous")
        self.networks[role] = (found[0], name)
        self.pending_networks.pop(role, None)

    def adopt_container(self, role, name, image, user, networks):
        found = self.client.run(
            "ps",
            "-aq",
            "--no-trunc",
            "--filter",
            "name=^/" + name + "$",
            "--filter",
            f"label={ATTEMPT_LABEL}={self.attempt}",
        ).split()
        if not found:
            return
        if len(found) != 1 or not CID.fullmatch(found[0]):
            raise RehearsalFailure("container identity ambiguous")
        self.containers[role] = Container(
            found[0], name, role, image, self.generation, user, tuple(networks)
        )
        self.pending_containers.pop(role, None)

    def create(self, role, image, user, networks, command, *, alias=None, env=()):
        self.remaining()
        if alias not in (None, network_alias(role)):
            raise RehearsalFailure("unreviewed network alias")
        if (
            image not in IMAGES
            or role in self.containers
            or role not in (*CAPS, "probe")
        ):
            raise RehearsalFailure("unreviewed container target")
        if role == "probe" and self.containers:
            raise RehearsalFailure("probe must precede the stack")
        name = f"{self.attempt}-g{self.generation}-{role}"
        args = [
            "create",
            "--name",
            name,
            "--hostname",
            name,
            "--pull",
            "never",
            "--label",
            f"{OWNER_LABEL}={OWNER}",
            "--label",
            f"{ATTEMPT_LABEL}={self.attempt}",
            "--label",
            f"{ROLE_LABEL}={role}",
            "--label",
            f"hyhome.opsflow.native-image={image}",
            "--label",
            f"hyhome.opsflow.airflow-generation={self.generation}",
            *create_options(role, user),
        ]
        if networks:
            args += [
                "--network",
                self.networks[networks[0]][0],
                "--network-alias",
                alias or network_alias(role),
            ]
        else:
            args += ["--network", "none"]
        for assignment in env:
            key, _, value = assignment.partition("=")
            validate_airflow_environment(assignment)
            args += ["--env", key + "=" + value]
        args += ["--entrypoint", command[0], image, *command[1:]]
        self.pending_containers[role] = (name, image, user, tuple(networks))
        failure = None
        try:
            result = self.client.run_result(*args)
        except Exception as error:
            result = None
            failure = error
        found = self.client.run(
            "ps",
            "-aq",
            "--no-trunc",
            "--filter",
            "name=^/" + name + "$",
            "--filter",
            f"label={ATTEMPT_LABEL}={self.attempt}",
        ).split()
        candidates = {
            value
            for value in [result.stdout.strip() if result else "", *found]
            if CID.fullmatch(value)
        }
        if len(candidates) != 1:
            raise RehearsalFailure("container identity ambiguous")
        record = Container(
            candidates.pop(), name, role, image, self.generation, user, tuple(networks)
        )
        self.containers[role] = record
        self.pending_containers.pop(role, None)
        if failure or result.returncode:
            raise RehearsalFailure("owned container create failed") from None
        for network in networks[1:]:
            self.client.run(
                "network",
                "connect",
                "--alias",
                network_alias(role),
                self.networks[network][0],
                record.cid,
            )
        self.verify(record)
        return record

    def verify(self, record, full=True):
        fmt = '{"Status":{{json .State.Status}},"Id":{{json .Id}},"Name":{{json .Name}},"Image":{{json .Image}},"ImageRef":{{json .Config.Image}},"Labels":{{json .Config.Labels}},"User":{{json .Config.User}},"Hostname":{{json .Config.Hostname}},"Readonly":{{json .HostConfig.ReadonlyRootfs}},"Memory":{{json .HostConfig.Memory}},"MemorySwap":{{json .HostConfig.MemorySwap}},"NanoCpus":{{json .HostConfig.NanoCpus}},"PortBindings":{{json .HostConfig.PortBindings}},"Binds":{{json .HostConfig.Binds}},"PidsLimit":{{json .HostConfig.PidsLimit}},"CapDrop":{{json .HostConfig.CapDrop}},"SecurityOpt":{{json .HostConfig.SecurityOpt}},"Tmpfs":{{json .HostConfig.Tmpfs}},"Mounts":{{json .Mounts}},"Networks":{{json .NetworkSettings.Networks}}}'
        value = json.loads(self.client.run("inspect", "--format", fmt, record.cid))
        labels = value.get("Labels") or {}
        if (
            value.get("Id") != record.cid
            or value.get("Name") != "/" + record.name
            or value.get("ImageRef") != record.image
            or labels.get(OWNER_LABEL) != OWNER
            or labels.get(ATTEMPT_LABEL) != self.attempt
            or labels.get(ROLE_LABEL) != record.role
            or labels.get("hyhome.opsflow.airflow-generation") != str(record.generation)
            or labels.get("hyhome.opsflow.native-image") != record.image
        ):
            raise RehearsalFailure("owned container identity changed")
        if not full:
            return
        actual_image = value.get("Image", "")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", actual_image):
            raise RehearsalFailure("runtime image identity rejected")
        if record.image == AIRFLOW_ID:
            kind = airflow_runtime_identity(actual_image)
            self.receipt["airflow_artifact_binding"] = {
                "index": AIRFLOW_ID,
                "manifest": AIRFLOW_MANIFEST_ID,
                "config": AIRFLOW_CONFIG_ID,
                "runtime_image_type": kind,
            }
        previous = self.runtime_images.setdefault(record.image, actual_image)
        if previous != actual_image:
            raise RehearsalFailure("runtime platform image changed")
        memory, cpu, pids = CAPS.get(record.role, (512, 250, 128))
        networks = value.get("Networks", {})
        if record.role == "probe":
            if set(networks) != {"none"}:
                raise RehearsalFailure("probe network changed")
        elif not ordinary_networks_match(
            value.get("Status"),
            networks,
            {
                self.networks[n][1]: (self.networks[n][0], [network_alias(record.role)])
                for n in record.networks
            },
        ):
            raise RehearsalFailure("owned network boundary changed")
        options = create_options(record.role, record.user)
        expected_tmpfs = dict(
            part.split(":", 1)
            for i, part in enumerate(options)
            if i and options[i - 1] == "--tmpfs"
        )
        safe_mounts = all(m.get("Type") == "tmpfs" for m in value.get("Mounts", []))
        if (
            value.get("PidsLimit") != pids
            or value.get("CapDrop") != ["ALL"]
            or value.get("SecurityOpt") != ["no-new-privileges=true"]
            or value.get("Tmpfs") != expected_tmpfs
            or not safe_mounts
        ):
            raise RehearsalFailure("owned container hardening changed")
        if (
            value.get("User") != record.user
            or value.get("Hostname") != record.name
            or value.get("Readonly") is not True
            or value.get("Memory") != memory * 1024**2
            or value.get("MemorySwap") != memory * 1024**2
            or value.get("NanoCpus") != cpu * 1000000
            or value.get("PortBindings")
            or value.get("Binds")
        ):
            raise RehearsalFailure("owned container boundary changed")

    def start(self, role):
        self.remaining()
        item = self.containers[role]
        self.verify(item)
        self.client.run("start", item.cid)

    def exec_result(self, role, *args, input_=None):
        self.remaining()
        record = self.containers[role]
        self.verify(record)
        return self.client.run_result("exec", "-i", record.cid, *args, input_=input_)

    def execute(self, role, *args, input_=None, s3_failure_logs=False):
        result = self.exec_result(role, *args, input_=input_)
        if result.returncode:
            if s3_failure_logs:
                capture_s3_upload_failure(self, role, args, result)
            else:
                self.capture_failure(role, args, result)
            raise RehearsalFailure("owned command failed; private evidence retained")
        return result.stdout

    def put(self, role, files):
        self.execute(role, "python", "-c", WRITE_FILES, input_=json.dumps(files))

    def configure_s3(self):
        shell = " | weed shell -master=seaweedfs-s3:9333 -filer=seaweedfs-s3:8888"
        self.execute(
            "s3",
            "sh",
            "-ceu",
            "printf 'fs.configure -locationPrefix=/buckets/opsflow-dev -volumeGrowthCount=1 -apply\\n'"
            + shell,
        )
        raw = self.execute("s3", "sh", "-ceu", "printf 'fs.configure\\n'" + shell)
        validate_s3_policy(raw)

    def wait(self, probe, message, seconds=90):
        limit = min(self.work_deadline, time.monotonic() + seconds)
        while time.monotonic() < limit:
            self.remaining()
            if probe():
                return
            time.sleep(0.5)
        raise RehearsalFailure(message)

    def psql(self, role, sql, database="opsflow_dev", user="p04_audit", check=True):
        result = self.exec_result(
            role,
            "psql",
            "-X",
            "-qAt",
            "-v",
            "ON_ERROR_STOP=1",
            "-U",
            user,
            "-d",
            database,
            input_=sql,
        )
        if check and result.returncode:
            self.capture_failure(role, ("psql",), result)
            raise RehearsalFailure("owned SQL failed; private evidence retained")
        return result

    def stop(self, role):
        self.verify(self.containers[role])
        self.client.run("stop", "--time", "5", self.containers[role].cid)

    def capture_failure(self, role, args, result):
        return capture_failure(self, role, args, result)

    def observe_cleanup(self, stage, role, error=None):
        observed = cleanup_observation(stage, role, error)
        self.receipt.setdefault("cleanup_observations", []).append(observed)
        return observed

    def remove(self, role):
        record = self.containers[role]
        observed = self.observe_cleanup("verify", role)
        try:
            self.verify(record, full=False)
            observed["stage"] = "rm"
            try:
                self.client.run("rm", "-f", "-v", record.cid)
            except Exception as error:
                observed["rm_exception"] = safe_exception(error)
            observed["stage"] = "absence"
            self._await_absence(record.cid, observed)
            self.containers.pop(role)
            observed["stage"] = "removed"
        except BaseException as error:
            observed["exception"] = safe_exception(error)
            raise

    def _await_absence(self, cid, observed):
        field = (
            "cleanup_deadline"
            if self.client.cleanup_deadline is not None
            else "deadline"
        )
        previous = getattr(self.client, field)
        limit = min(previous, time.monotonic() + 5)
        setattr(self.client, field, limit)
        try:
            while time.monotonic() < limit:
                result = self.client.run_result("inspect", "--format", "{{.Id}}", cid)
                observed["inspect_exit"] = result.returncode
                observed["absent"] = exact_container_absent(result, cid)
                if observed["absent"]:
                    return
                time.sleep(min(0.1, max(0, limit - time.monotonic())))
            raise RehearsalFailure("owned container removal not confirmed")
        finally:
            setattr(self.client, field, previous)

    def dump(self, role, database):
        raw = self.execute(
            role,
            "sh",
            "-ceu",
            "pg_dump -Fc --create -U p04_audit -d "
            + database
            + " > /tmp/dump; base64 /tmp/dump",
        )
        if not 0 < len(raw) <= 1024 * 1024:
            raise RehearsalFailure("snapshot size rejected")
        return self.private(role + "-snapshot", raw)

    def dump_roles(self, role):
        raw = self.execute(
            role, "pg_dumpall", "--roles-only", "--no-role-passwords", "-U", "p04_audit"
        )
        expected = (
            {"p04_audit", "airflow"}
            if role == "metadata-pg"
            else {
                "p04_audit",
                "opsflow_owner",
                "opsflow_migrator",
                "opsflow_ingest",
                "opsflow_notifier",
                "opsflow_reader",
            }
        )
        found = set(re.findall(r"^CREATE ROLE ([a-z_][a-z0-9_]*);$", raw, re.MULTILINE))
        if found != expected or len(
            re.findall(r"\bCREATE\s+ROLE\b", raw, re.IGNORECASE)
        ) != len(expected):
            raise RehearsalFailure("role snapshot scope changed")
        return self.private(role + "-roles", raw.replace("CREATE ROLE p04_audit;", ""))

    def restore_roles(self, role, path):
        if private_identity(path) != self.files[path]:
            raise RehearsalFailure("role snapshot identity changed")
        self.psql(role, path.read_text(), database="postgres")

    def restore(self, role, path):
        if private_identity(path) != self.files[path]:
            raise RehearsalFailure("snapshot identity changed")
        self.execute(
            role,
            "sh",
            "-ceu",
            "base64 -d > /tmp/restore; pg_restore --exit-on-error --create -U p04_audit -d postgres /tmp/restore",
            input_=path.read_text(),
        )

    def _unlock(self):
        if self.lock_fd >= 0:
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            os.close(self.lock_fd)
            self.lock_fd = -1

    def _cleanup_host(self):
        if self.dir_identity is None:
            return
        for path, identity in self.files.items():
            if private_identity(path) != identity:
                raise RehearsalFailure("owned host file changed")
            path.unlink()
        config = self.directory / "docker-config"
        if config.exists():
            config.rmdir()
        item = self.directory.stat(follow_symlinks=False)
        if (
            (item.st_dev, item.st_ino) != self.dir_identity
            or stat.S_IMODE(item.st_mode) != 0o700
            or item.st_uid != os.geteuid()
            or any(self.directory.iterdir())
        ):
            raise RehearsalFailure("owned host directory changed")
        self.directory.rmdir()
        self.dir_identity = None

    def cleanup(self):
        failures, swept_containers, swept_networks = [], None, None
        phase, active_role, cancellation = "begin", None, None
        try:
            self.client.begin_cleanup()
            self.client.cleanup_deadline = min(
                self.deadline, self.client.cleanup_deadline
            )
            for role, values in tuple(self.pending_containers.items()):
                phase, active_role = "pending-container", role
                try:
                    self.adopt_container(role, *values)
                    if role not in self.containers:
                        self.pending_containers.pop(role, None)
                except Exception as error:
                    self.observe_cleanup("pending-container", role, error)
                    failures.append("pending container")
            for role, name in tuple(self.pending_networks.items()):
                phase, active_role = "pending-network", role
                try:
                    self.adopt_network(role, name)
                    if role not in self.networks:
                        self.pending_networks.pop(role, None)
                except Exception as error:
                    self.observe_cleanup("pending-network", role, error)
                    failures.append("pending network")
            for role in tuple(reversed(self.containers)):
                phase, active_role = "container-remove", role
                try:
                    self.remove(role)
                except Exception:
                    failures.append("container")
            for role, (network_id, name) in reversed(tuple(self.networks.items())):
                phase, active_role = "network-verify", role
                observed = self.observe_cleanup(phase, role)
                try:
                    item = json.loads(
                        self.client.run(
                            "network",
                            "inspect",
                            "--format",
                            '{"Id":{{json .Id}},"Name":{{json .Name}},"Labels":{{json .Labels}},"Internal":{{json .Internal}}}',
                            network_id,
                        )
                    )
                    if (
                        item.get("Id") != network_id
                        or item.get("Name") != name
                        or item.get("Internal") is not True
                        or (item.get("Labels") or {}).get(OWNER_LABEL) != OWNER
                        or (item.get("Labels") or {}).get(ATTEMPT_LABEL) != self.attempt
                    ):
                        raise RehearsalFailure("owned network changed")
                    phase = observed["stage"] = "network-rm"
                    self.client.run("network", "rm", network_id)
                    phase = observed["stage"] = "network-absence"
                    result = self.client.run_result(
                        "network", "inspect", "--format", "{{.Id}}", network_id
                    )
                    observed.update(
                        inspect_exit=result.returncode, absent=result.returncode != 0
                    )
                    if not observed["absent"]:
                        raise RehearsalFailure("owned network removal not confirmed")
                    self.networks.pop(role)
                    observed["stage"] = "network-removed"
                except Exception as error:
                    observed["exception"] = safe_exception(error)
                    failures.append("network")
            phase, active_role = "final-sweeps", None
            swept_containers = self.client.run(
                "ps",
                "-aq",
                "--no-trunc",
                "--filter",
                f"label={ATTEMPT_LABEL}={self.attempt}",
            ).split()
            swept_networks = self.client.run(
                "network",
                "ls",
                "-q",
                "--no-trunc",
                "--filter",
                f"label={ATTEMPT_LABEL}={self.attempt}",
            ).split()
            if (
                swept_containers
                or swept_networks
                or self.containers
                or self.networks
                or self.pending_containers
                or self.pending_networks
            ):
                failures.append("retained Docker state")
            if self.receipt.get("command_failure"):
                failures.append("protected failure evidence retained")
            if not failures:
                phase, active_role = "host", None
                self._cleanup_host()
        except BaseException as error:
            self.observe_cleanup(phase, active_role, error)
            if not isinstance(error, Exception):
                cancellation = error
            failures.append("unexpected cleanup failure")
        finally:
            try:
                self._unlock()
            except BaseException as error:
                self.observe_cleanup("unlock", None, error)
                if cancellation is None and not isinstance(error, Exception):
                    cancellation = error
                failures.append("lock cleanup failure")
            self.receipt.update(
                image_identities=self.runtime_images,
                cleanup="FAIL" if failures else "PASS",
                retained={
                    "container_ids": sorted(x.cid for x in self.containers.values()),
                    "network_ids": sorted(x[0] for x in self.networks.values()),
                    "swept_container_ids": swept_containers,
                    "swept_network_ids": swept_networks,
                    "pending_container_roles": sorted(self.pending_containers),
                    "pending_network_roles": sorted(self.pending_networks),
                    "attempt_directory": str(self.directory)
                    if self.dir_identity
                    else None,
                },
                cleanup_failures=failures,
            )
        if cancellation is not None:
            raise cancellation
        if failures:
            raise RehearsalFailure("Airflow native cleanup incomplete")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


WAIT = """import os,time
while not os.path.isfile('/tmp/fixture-ready'):time.sleep(.2)
os.execvp({command}[0],{command})
"""
S3_CLIENT = """import base64,hashlib,json,sys
import boto3
from botocore.config import Config
c=json.load(open('/run/opsflow/s3.json'))
s=boto3.client('s3',endpoint_url=c['endpoint_url'],aws_access_key_id=c['access_key_id'],aws_secret_access_key=c['secret_access_key'],region_name=c['region'],config=Config(connect_timeout=2,read_timeout=3,retries={'max_attempts':1},s3={'addressing_style':'path'}))
b=c['bucket']
"""
FUNCTION = "ops_flow.publish_manifest(text,text,text,timestamptz,jsonb,text)"
AF_ROLES = ("api", "scheduler", "processor", "worker")


def stage_file_backend(
    f, role, image, user, networks, path, contents, command, alias=None
):
    launch = 'while [ ! -f /data/ready ]; do sleep .2; done; exec "$@"'
    f.create(
        role,
        image,
        user,
        networks,
        ("sh", "-ceu", launch, "fixture", *command),
        alias=alias,
    )
    f.start(role)
    master = (
        "printf '[master.volume_growth]\\ncopy_1 = 1\\n' > /data/master.toml; "
        if role == "s3"
        else ""
    )
    f.execute(
        role,
        "sh",
        "-ceu",
        "umask 077; cat > " + path + "; " + master + "touch /data/ready",
        input_=contents,
    )
