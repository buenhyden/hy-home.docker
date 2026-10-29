from __future__ import annotations

import fcntl
import json
import os
import re
import secrets
import stat
import time
from pathlib import Path

from tests.validation import _opsflow_native_evidence as native
from tests.validation._opsflow_native_inputs import (
    ALIASES,
    ATTEMPT_LABEL,
    IMAGE_IDS,
    MAILPIT_REF,
    N8N_ID,
    N8N_LABELS,
    N8N_REF,
    OWNER,
    OWNER_LABEL,
    PG_REF,
    RESOURCE_CAPS,
    ROLE_LABEL,
    RUNNER_REF,
    RUNNER_RUNTIME_IDS,
    TMPFS,
    VALKEY_REF,
    bind_mount,
    memory_bytes,
    precreate_headroom_failure,
)
from tests.validation._opsflow_native_ownership import (
    Container,
    Network,
    PendingContainer,
    PendingNetwork,
    adopt_container,
    adopt_network,
    consume_cidfile,
    discover_container,
    discover_network,
    inspect_container_identity,
    inspect_network_identity,
    inspect_none_network,
    main_readiness_failure_facts,
    mismatch_receipt,
    n8n_health_probe,
    network_attachment_matches,
    node_status_probe,
    request_container_removal,
    security_contract_matches,
    sweep_attempt,
    unique_identity,
    wait_container_absent,
)
from tests.validation._supabase_smtp_fixture_storage import write_exclusive
from tests.validation.test_datastore_rehearsal_boundary import DockerClientBoundary

# Generation 1 and the restore took about 660 s on 2026-10-20 (SPEC-0204
# TSK-0019), and a 13-minute limit expired during generation 2's main start.
# The first full pass took 864 s, about 0.58 of the former 25-minute limit.
# The criterion 22 scenarios add a scheduled-trigger wait of up to 150 s, a
# 70 s deactivated hold, three more n8n CLI/REST rounds and five credential
# probes (an estimate, not a measurement), so the limit moves to 40 minutes.
WORK_SECONDS = 40 * 60


class RehearsalFailure(AssertionError):
    pass


class NativeDockerBoundary(DockerClientBoundary):
    def _remaining_timeout(self) -> float:
        timeout = min(super()._remaining_timeout(), 60.0)
        if self.cleanup_deadline is None:
            return timeout
        # `docker rm -f -v` of a running container took 3.9 s (median) and
        # 6.1 s (max) on this host (2026-10-20), over the shared 2.4 s cleanup
        # call limit; every removal then read as unknown.
        return min(10.0, self.cleanup_deadline - time.monotonic())


class NativeFixture:
    def __init__(self) -> None:
        self.host_uid, self.host_gid = native.host_identity()
        self.started = time.monotonic()
        self.work_deadline = self.started + WORK_SECONDS
        self.final_deadline = self.started + WORK_SECONDS + 2 * 60
        self.attempt = "opsflow-native-" + secrets.token_hex(12)
        self.lock_path = Path("/tmp/hyhome-opsflow-native-rehearsal.lock")
        self.lock_fd = -1
        self.directory = Path("/tmp") / (
            "hyhome-opsflow-native-attempt-" + secrets.token_hex(12)
        )
        self.dir_identity: tuple[int, int] | None = None
        self.files: dict[Path, native.PrivateFile] = {}
        self.mailpit_dirs: dict[Path, tuple[int, int]] = {}
        self.dumps: dict[str, Path] = {}
        self.dump_receipts: dict[str, dict[str, object]] = {}
        self.runtime_images: dict[str, str] = {}
        self.none_network_id = ""
        self.containers: dict[str, Container] = {}
        self.networks: dict[str, Network] = {}
        self.pending_containers: dict[str, PendingContainer] = {}
        self.pending_networks: dict[str, PendingNetwork] = {}
        self.swept_cids: set[str] = set()
        self.swept_nids: set[str] = set()
        self.generation = 1
        self.receipt: dict[str, object] = {
            "attempt": self.attempt,
            "native": "NOT_RUN",
            "cleanup": "PENDING",
        }
        try:
            self._prepare_host_boundary()
            config = self.directory / "docker-config"
            config.mkdir(mode=0o700)
            self.client = NativeDockerBoundary(
                binary=Path("/usr/bin/docker"),
                socket_path=Path("/var/run/docker.sock"),
                config_dir=config,
                deadline_seconds=WORK_SECONDS,
            )
        except BaseException:
            try:
                self._cleanup_host()
            finally:
                if self.lock_fd >= 0:
                    fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                    os.close(self.lock_fd)
                    self.lock_fd = -1
            raise

    def _prepare_host_boundary(self) -> None:
        self.lock_fd = os.open(
            self.lock_path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600
        )
        lock = os.fstat(self.lock_fd)
        if (
            not stat.S_ISREG(lock.st_mode)
            or lock.st_uid != os.geteuid()
            or stat.S_IMODE(lock.st_mode) != 0o600
            or lock.st_nlink != 1
        ):
            raise RehearsalFailure("native rehearsal lock metadata rejected")
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RehearsalFailure("native rehearsal host lock is held") from None
        stale_dirs = list(Path("/tmp").glob("hyhome-opsflow-native-attempt-*"))
        stale_dirs += list(Path("/tmp").glob("hyhome-opsflow-airflow-native-attempt-*"))
        if stale_dirs:
            raise RehearsalFailure("stale native rehearsal host attempt exists")
        self.directory.mkdir(mode=0o700)
        metadata = self.directory.stat(follow_symlinks=False)
        self.dir_identity = (metadata.st_dev, metadata.st_ino)

    def private(self, name: str, content: str, *, mode: int = 0o600) -> Path:
        path = write_exclusive(self.directory, name, content, mode)
        metadata = path.stat(follow_symlinks=False)
        if (metadata.st_uid, metadata.st_gid) != (self.host_uid, self.host_gid):  # fmt: skip
            raise RehearsalFailure("private input owner metadata mismatch")
        identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid, metadata.st_gid)
        self.files[path] = native.PrivateFile(path, *identity, mode)
        return path

    def _remaining(self, cleanup: bool = False) -> None:
        limit = self.final_deadline if cleanup else self.work_deadline
        if time.monotonic() >= limit:
            raise RehearsalFailure("native rehearsal deadline expired")

    @staticmethod
    def _headroom() -> tuple[int, int, int, int]:
        memory = {
            line.split(":", 1)[0]: int(line.split()[1])
            for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines()
            if ":" in line and len(line.split()) >= 2
        }
        disk = os.statvfs("/tmp")
        return (
            memory.get("MemAvailable", 0),
            memory.get("SwapFree", 0),
            disk.f_bavail * disk.f_frsize,
            0 if not disk.f_files else disk.f_favail * 100 // disk.f_files,
        )

    def runtime_headroom(self) -> None:
        available, _, _, _ = self._headroom()
        if available < 3 * 1024**2:
            raise RehearsalFailure("runtime memory reserve crossed; cleanup required")

    @staticmethod
    def _object(payload: str) -> dict:
        try:
            value = json.loads(payload)
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            if not isinstance(value, dict):
                raise ValueError
            return value
        except (ValueError, TypeError):
            raise RehearsalFailure("Docker metadata shape rejected") from None

    def verify_prerequisites(self) -> None:
        self._remaining()
        if (
            os.environ.get("OPSFLOW_N8N_NATIVE_IMAGE") != N8N_ID
            or os.environ.get("OPSFLOW_N8N_NATIVE_CONTEXT") != "default"
        ):
            raise RehearsalFailure(
                "explicit exact native image/context selection required"
            )
        if any(
            os.environ.get(key)
            for key in (
                "DOCKER_HOST",
                "DOCKER_CONTEXT",
                "DOCKER_TLS_VERIFY",
                "DOCKER_CERT_PATH",
            )
        ):
            raise RehearsalFailure("Docker environment overrides are forbidden")
        active = self.client.run(
            "ps", "-aq", "--filter", f"label={OWNER_LABEL}"
        ).split()
        active_networks = self.client.run(
            "network", "ls", "-q", "--filter", f"label={OWNER_LABEL}"
        ).split()
        if active or active_networks:
            raise RehearsalFailure("an owned native attempt already exists")
        available, swap_free, disk_free, inode_percent = self._headroom()
        self.receipt["precreate_headroom"] = {
            "mem_available_kib": available,
            "swap_free_kib": swap_free,
            "disk_free_bytes": disk_free,
            "inode_free_percent": inode_percent,
        }
        headroom_failure = precreate_headroom_failure(available, swap_free, disk_free, inode_percent, os.cpu_count() or 0)  # fmt: skip
        if headroom_failure:
            raise RehearsalFailure(headroom_failure)
        try:
            self.none_network_id = inspect_none_network(self.client)
        except (ValueError, TypeError, json.JSONDecodeError):
            raise RehearsalFailure("built-in none network identity changed") from None
        for reference, expected in IMAGE_IDS.items():
            result = self.client.run_result("image", "inspect", reference)
            if result.returncode:
                raise RehearsalFailure("required exact native image is not cached")
            item = self._object(result.stdout)
            if (item.get("Id"), item.get("Os"), item.get("Architecture")) != (
                expected,
                "linux",
                "amd64",
            ):
                raise RehearsalFailure("native image identity/platform mismatch")
            if "@sha256:" in reference:
                tagged, digest = reference.rsplit("@", 1)
                repo_digest = tagged.rsplit(":", 1)[0] + "@" + digest
                if repo_digest not in (item.get("RepoDigests") or []):
                    raise RehearsalFailure("native image RepoDigest mismatch")
            if reference == N8N_REF:
                labels = (item.get("Config") or {}).get("Labels") or {}
                if any(labels.get(key) != value for key, value in N8N_LABELS.items()):
                    raise RehearsalFailure("n8n source binding labels mismatch")
            configured_user = (item.get("Config") or {}).get("User") or ""
            expected_user = {
                N8N_REF: "1000",
                RUNNER_REF: "runner",
                MAILPIT_REF: "",
                PG_REF: "",
                VALKEY_REF: "",
            }[reference]
            if configured_user != expected_user:
                raise RehearsalFailure("native image configured user changed")
            entrypoint = (item.get("Config") or {}).get("Entrypoint") or []
            if reference == MAILPIT_REF and entrypoint != ["/mailpit"]:
                raise RehearsalFailure("Mailpit native entrypoint changed")
            volumes = (item.get("Config") or {}).get("Volumes") or {}
            expected_volumes = (
                {"/var/lib/postgresql": {}} if reference == PG_REF else {}
            )
            if volumes != expected_volumes:
                raise RehearsalFailure("native image declared-volume contract changed")

    def create_networks(self) -> None:
        for role in ("ctl", "runner", "dev", "capture"):
            name = f"{self.attempt}-{role}"
            pending = PendingNetwork(name, role)
            self.pending_networks[role] = pending
            result = None
            failed = False
            try:
                result = self.client.run_result(
                    "network",
                    "create",
                    "--internal",
                    "--label",
                    f"{OWNER_LABEL}={OWNER}",
                    "--label",
                    f"{ATTEMPT_LABEL}={self.attempt}",
                    "--label",
                    f"{ROLE_LABEL}={role}",
                    name,
                )
            except BaseException:
                failed = True
            candidates = [] if result is None else [result.stdout.strip()]
            try:
                found = self.client.run(
                    "network",
                    "ls",
                    "-q",
                    "--no-trunc",
                    "--filter",
                    f"name=^{name}$",
                    "--filter",
                    f"label={ATTEMPT_LABEL}={self.attempt}",
                ).split()
            except BaseException:
                failed, found = True, []
            identity = unique_identity(candidates + found)
            if identity:
                self.networks[role] = adopt_network(pending, identity)
            if failed or result is None or result.returncode or role not in self.networks:  # fmt: skip
                raise RehearsalFailure("owned network creation failed")
            self._verify_network_owned(role, self.networks[role])

    def _verify_network_owned(self, role: str, record: Network) -> dict:
        try:
            return inspect_network_identity(self.client, record, role, self.attempt)
        except (ValueError, TypeError, json.JSONDecodeError):
            raise RehearsalFailure("owned network metadata changed") from None

    def _adopt_pending_container(self, role: str) -> None:
        pending = self.pending_containers[role]
        record = discover_container(self.client, pending, self.attempt)
        if record is None:
            self.pending_containers.pop(role)
            return
        self.containers[role] = record
        self._verify_owned(record)

    def _adopt_pending_network(self, role: str) -> None:
        pending = self.pending_networks[role]
        record = discover_network(self.client, pending, self.attempt)
        if record is None:
            self.pending_networks.pop(role)
            return
        self.networks[role] = record
        self._verify_network_owned(role, record)

    def create(
        self,
        role: str,
        image: str,
        user: str,
        networks: tuple[str, ...],
        *,
        env: tuple[str, ...] = (),
        mounts: tuple[str, ...] = (),
        command: tuple[str, ...] = (),
        entrypoint: str | None = None,
        cap_add: tuple[str, ...] = (),
    ) -> Container:
        self._remaining()
        self.runtime_headroom()
        memory, cpus, pids = RESOURCE_CAPS[role]
        name = f"{self.attempt}-g{self.generation}-{role}"
        cidfile = self.directory / f"cid-g{self.generation}-{role}"
        if cidfile.exists():
            raise RehearsalFailure("container identity file already exists")
        network_record = self.networks.get(networks[0]) if networks else None
        if networks and network_record is None:
            raise RehearsalFailure("unowned network requested")
        network = network_record.network_id if network_record else "none"
        args = [
            "create",
            "--cidfile",
            str(cidfile),
            "--name",
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
            f"hyhome.opsflow.native-generation={self.generation}",
            "--label",
            f"hyhome.opsflow.native-image-ref={image}",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges=true",
            "--memory",
            memory,
            "--memory-swap",
            memory,
            "--cpus",
            cpus,
            "--pids-limit",
            str(pids),
            "--stop-timeout",
            "10",
            "--user",
            user,
            "--network",
            network,
        ]
        if networks:
            args += ["--network-alias", ALIASES[role]]
        for capability in cap_add:
            args += ["--cap-add", capability]
        for value in TMPFS.get(role, ()):
            args += ["--tmpfs", value]
        for assignment in env:
            if (
                "PASSWORD=" in assignment
                or "TOKEN=" in assignment
                or "KEY=" in assignment
            ):
                raise RehearsalFailure("secret environment assignment rejected")
            args += ["--env", assignment]
        for mount in mounts:
            args += ["--mount", mount]
        if entrypoint:
            args += ["--entrypoint", entrypoint]
        args += [IMAGE_IDS[image], *command]
        pending = PendingContainer(
            name,
            role,
            self.generation,
            IMAGE_IDS[image],
            image,
            user,
            networks,
            mounts,
            cap_add,
        )
        self.pending_containers[role] = pending
        result = None
        failed = False
        candidates: list[str] = []
        try:
            result = self.client.run_result(*args)
            candidates.append(result.stdout.strip())
        except BaseException:
            failed = True
        try:
            identity = self._consume_cidfile(cidfile)
            if identity:
                candidates.append(identity)
        except BaseException:
            failed = True
        try:
            found = self.client.run(
                "ps",
                "-aq",
                "--no-trunc",
                "--filter",
                f"name=^/{name}$",
                "--filter",
                f"label={ATTEMPT_LABEL}={self.attempt}",
                "--filter",
                f"label={ROLE_LABEL}={role}",
            ).split()
        except BaseException:
            failed, found = True, []
        identity = unique_identity(candidates + found)
        if identity:
            self.containers[role] = adopt_container(pending, identity)
        if failed or result is None or result.returncode or role not in self.containers:
            raise RehearsalFailure("owned container identity is ambiguous")
        record = self.containers[role]
        for extra in networks[1:]:
            extra_record = self.networks.get(extra)
            if extra_record is None:
                raise RehearsalFailure("unowned network requested")
            self.client.run("network", "connect", "--alias", ALIASES[role], extra_record.network_id, record.cid)  # fmt: skip
        self._verify_container(record)
        return record

    def _consume_cidfile(self, path: Path) -> str | None:
        try:
            return consume_cidfile(path, os.geteuid())
        except (UnicodeDecodeError, OSError, ValueError):
            raise RehearsalFailure("container identity file rejected") from None

    def chown_secret(self, path: Path, uid: int) -> None:
        item = self.files[path]
        mount = f"type=bind,src={path},dst=/owned-secret"
        self.create(
            "secret-prep",
            VALKEY_REF,
            "0:0",
            (),
            mounts=(mount,),
            entrypoint="/bin/chown",
            cap_add=("CHOWN",),
            command=(f"{uid}:{item.gid}", "/owned-secret"),
        )
        self.start("secret-prep")
        record = self.containers["secret-prep"]
        self.runtime_headroom()
        self._verify_container(record)
        waited = self.client.run_result("wait", record.cid)
        if waited.returncode or waited.stdout.strip() != "0":
            raise RehearsalFailure("secret ownership preparation failed")
        self.remove("secret-prep")
        self.files[path] = item.with_uid(uid)
        metadata = path.stat(follow_symlinks=False)
        if (metadata.st_uid, metadata.st_gid) != (uid, item.gid) or stat.S_IMODE(metadata.st_mode) != item.mode:  # fmt: skip
            raise RehearsalFailure("secret ownership metadata mismatch")

    def _verify_owned(self, record: Container) -> dict:
        try:
            return inspect_container_identity(self.client, record, self.attempt)
        except (ValueError, TypeError, json.JSONDecodeError):
            raise RehearsalFailure("owned container metadata changed") from None

    # fmt: off
    def _verify_container(self, record: Container) -> None:
        item = self._verify_owned(record)
        config = item.get("Config") or {}
        host = item.get("HostConfig") or {}
        memory, cpus, pids = RESOURCE_CAPS[record.role]
        actual_tmpfs = {path: set(options.split(",")) for path, options in (host.get("Tmpfs") or {}).items()}
        expected_tmpfs = {value.split(":", 1)[0]: set(value.split(":", 1)[1].split(",")) for value in TMPFS.get(record.role, ())}
        actual_mounts = {(mount.get("Source"), mount.get("Destination"), not mount.get("RW", False)) for mount in item.get("Mounts") or [] if mount.get("Type") == "bind"}
        if any(mount.get("Type") == "volume" for mount in item.get("Mounts") or []):
            raise RehearsalFailure("anonymous Docker volume rejected")
        parsed_mounts = [(specification, dict(part.split("=", 1) for part in specification.split(",") if "=" in part)) for specification in record.mounts]
        expected_mounts = {(fields.get("src"), fields.get("dst"), "readonly" in specification.split(",")) for specification, fields in parsed_mounts}
        network_ok = network_attachment_matches(item, record, self.networks, ALIASES, self.none_network_id)
        runtime_image = item.get("Image")
        expected_runtime = RUNNER_RUNTIME_IDS if record.image_ref == RUNNER_REF else {self.runtime_images.get(record.image_ref, runtime_image)}
        image_ok = isinstance(runtime_image, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", runtime_image) and runtime_image in expected_runtime and config.get("Image") == record.image_id and config.get("User") == record.user
        resources_ok = host.get("ReadonlyRootfs") and host.get("Memory") == memory_bytes(memory) and host.get("MemorySwap") == memory_bytes(memory) and host.get("NanoCpus") == int(float(cpus) * 1_000_000_000) and host.get("PidsLimit") == pids
        security_ok = security_contract_matches(host, record.cap_add)
        storage_ok = actual_tmpfs == expected_tmpfs and actual_mounts == expected_mounts
        checks = {"image": image_ok, "resources": resources_ok, "security": security_ok, "storage": storage_ok, "network": network_ok}
        failures = sorted(name for name, passed in checks.items() if not passed)
        if failures:
            self.receipt.update(mismatch_receipt(failures, item, record, self.networks, ALIASES, self.none_network_id))
            raise RehearsalFailure("owned container metadata changed: " + ",".join(failures))
        self.runtime_images.setdefault(record.image_ref, runtime_image)
        self.receipt["runtime_image_configs"] = dict(sorted(self.runtime_images.items()))
    # fmt: on

    def start(self, role: str) -> None:
        self.runtime_headroom()
        record = self.containers[role]
        self._verify_container(record)
        self.client.run("start", record.cid)

    def stop(self, role: str) -> None:
        record = self.containers[role]
        self._verify_container(record)
        result = self.client.run_result("stop", "--time", "10", record.cid)
        if result.returncode:
            raise RehearsalFailure("owned container stop failed")
        if (self._verify_owned(record).get("State") or {}).get("Running") is not False:
            raise RehearsalFailure("owned container remained running after stop")

    def exec_result(self, role: str, *args: str, input_: str | None = None):
        self._remaining()
        self.runtime_headroom()
        record = self.containers[role]
        self._verify_container(record)
        return self.client.run_result("exec", "-i", record.cid, *args, input_=input_)

    def exec(self, role: str, *args: str, input_: str | None = None) -> str:
        result = self.exec_result(role, *args, input_=input_)
        if result.returncode:
            raise RehearsalFailure("owned container command failed (output withheld)")
        return result.stdout

    def wait_until(self, probe, message: str, seconds: int = 60, failure=None) -> None:
        deadline = min(time.monotonic() + seconds, self.work_deadline)
        while time.monotonic() < deadline:
            self.runtime_headroom()
            if probe():
                return
            time.sleep(0.25)
        if failure:
            failure()
        raise RehearsalFailure(message)

    def logs_contain(self, role: str, pattern: str) -> bool:
        self.runtime_headroom()
        record = self.containers[role]
        self._verify_container(record)
        result = self.client.run_result("logs", record.cid)
        return result.returncode == 0 and pattern in result.stdout + result.stderr

    def remove(self, role: str) -> None:
        record = self.containers[role]
        self._verify_owned(record)
        request_container_removal(self.client, record.cid)
        observed = wait_container_absent(self.client, record.cid, self.final_deadline)
        self.receipt.setdefault("container_removal_facts", {})[role] = {
            "present": observed.present,
            "exact_absent": observed.exact_absent,
            "unknown": observed.unknown,
        }
        if not observed.absent:
            raise RehearsalFailure("owned container removal failed")
        self.containers.pop(role)
        self.pending_containers.pop(role, None)

    # fmt: off
    def create_secrets(self) -> dict[str, tuple[str, Path]]:
        values = {"metadata_pg": secrets.token_urlsafe(32), "dev_pg": secrets.token_urlsafe(32), "valkey_server": secrets.token_urlsafe(32), "encryption": secrets.token_urlsafe(48), "runner": secrets.token_urlsafe(48), "owner": "Aa1!" + secrets.token_urlsafe(32), "migrator": secrets.token_urlsafe(32), "ingest": secrets.token_urlsafe(32), "notifier": secrets.token_urlsafe(32), "reader": secrets.token_urlsafe(32)}
        values |= {"metadata_n8n": values["metadata_pg"], "valkey_n8n": values["valkey_server"]}
        result = {}
        for key, value in values.items():
            uid = {"metadata_pg": 70, "dev_pg": 70, "valkey_server": 999}.get(key, self.host_uid)
            mode = 0o640 if uid != self.host_uid else 0o600
            path = self.private(key.replace("_", "-") + ".secret", value + "\n", mode=mode)
            if uid != self.host_uid:
                self.chown_secret(path, uid)
            result[key] = (value, path)
        for name in ("metadata.dump", "dev-roles.sql", "dev.dump"):
            path = self.private(name, "", mode=0o640)
            self.chown_secret(path, 70)
            self.dumps[name] = path
        return result
    def start_postgres(self, role: str, secret: Path) -> None:
        user, database = ("n8n", "n8n") if role == "metadata-pg" else ("p04_audit", "postgres")
        names = ("metadata.dump",) if role == "metadata-pg" else ("dev-roles.sql", "dev.dump")
        dump_mounts = tuple(bind_mount(self.dumps[name], "/fixture/" + name, readonly=self.generation == 2) for name in names)
        env = (f"POSTGRES_USER={user}", f"POSTGRES_DB={database}", "POSTGRES_PASSWORD_FILE=/run/secrets/postgres-password", "PGDATA=/var/lib/postgresql/18/docker")
        self.create(role, PG_REF, "70:70", ("ctl",) if role == "metadata-pg" else ("dev",), env=env, mounts=(bind_mount(secret, "/run/secrets/postgres-password"), *dump_mounts), command=("postgres", "-c", "max_connections=40", "-c", "shared_buffers=64MB"))
        self.start(role)
        self.wait_until(lambda: self.exec_result(role, "pg_isready", "-U", user, "-d", database).returncode == 0, f"{role} readiness expired")
    def psql(self, role: str, database: str, sql: str, *, check: bool = True, container: str = "dev-pg"):
        result = self.exec_result(container, "psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1", "-v", "VERBOSITY=verbose", "-U", role, "-d", database, input_=sql)
        if check and result.returncode:
            raise RehearsalFailure("PostgreSQL fixture command failed (output withheld)")
        return result
    def start_valkey(self, secret: Path) -> None:
        script = "set -eu; umask 077; password=$(cat /run/secrets/valkey-password); printf 'bind 0.0.0.0\\nprotected-mode yes\\nport 6379\\nsave \"\"\\nappendonly no\\nrequirepass %s\\n' \"$password\" >/run/valkey/valkey.conf; exec valkey-server /run/valkey/valkey.conf"
        self.create("valkey", VALKEY_REF, "999:999", ("ctl",), mounts=(bind_mount(secret, "/run/secrets/valkey-password"),), entrypoint="/bin/sh", command=("-ec", script))
        self.start("valkey")
        self.wait_until(lambda: self.exec_result("valkey", "/bin/sh", "-ec", 'valkey-cli -a "$(cat /run/secrets/valkey-password)" ping').returncode == 0, "Valkey readiness expired")
    def start_mailpit(self) -> None:
        # The scenario stops and restarts Mailpit and expects the earlier
        # capture, but Docker clears a tmpfs on stop. The store is a bind of an
        # owned directory, one per generation so each generation starts empty.
        if self.host_uid != 1000:
            raise RehearsalFailure("Mailpit store owner must match its container user")
        data = self.directory / f"mailpit-data-{self.generation}"
        data.mkdir(mode=0o700)
        created = data.stat(follow_symlinks=False)
        self.mailpit_dirs[data] = (created.st_dev, created.st_ino)
        self.create("mailpit", MAILPIT_REF, "1000:1000", ("capture",), env=("MP_DATABASE=/data/mailpit.db", "MP_UI_BIND_ADDR=0.0.0.0:8025", "MP_SMTP_BIND_ADDR=0.0.0.0:1025", "MP_MAX_MESSAGES=32"), mounts=(bind_mount(data, "/data", readonly=False),))
        self.start("mailpit")
    def _n8n_env(self) -> tuple[str, ...]:
        return ("DB_TYPE=postgresdb", "DB_POSTGRESDB_HOST=metadata-pg", "DB_POSTGRESDB_PORT=5432", "DB_POSTGRESDB_DATABASE=n8n", "DB_POSTGRESDB_USER=n8n", "DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/n8n_db_password", "EXECUTIONS_MODE=queue", "N8N_VALKEY_HOST=n8n-valkey", "N8N_VALKEY_SECRET=" + Path("/run/secrets/n8n_valkey_password").name, "QUEUE_BULL_REDIS_HOST=n8n-valkey", "QUEUE_BULL_REDIS_PORT=6379", "QUEUE_BULL_PREFIX=opsflow_native", "QUEUE_BULL_REDIS_PASSWORD_FILE=/run/secrets/n8n_valkey_password", "N8N_RUNNERS_MODE=external", "N8N_RUNNERS_BROKER_LISTEN_ADDRESS=0.0.0.0", "N8N_RUNNERS_AUTH_TOKEN_FILE=/run/secrets/n8n_runner_auth_token", "N8N_RUNNERS_TASK_TIMEOUT=60", "N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key", "OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true", "N8N_USER_FOLDER=/tmp", "N8N_PROTOCOL=http", "N8N_HOST=n8n", "N8N_PORT=5678", "N8N_LOG_LEVEL=debug", "N8N_SECURE_COOKIE=false", "N8N_DIAGNOSTICS_ENABLED=false", "N8N_VERSION_NOTIFICATIONS_ENABLED=false", "N8N_TEMPLATES_ENABLED=false", "N8N_PERSONALIZATION_ENABLED=false", "N8N_BLOCK_ENV_ACCESS_IN_NODE=true", "GENERIC_TIMEZONE=Asia/Seoul", "TZ=Asia/Seoul")
    def start_n8n(self, secrets_: dict[str, tuple[str, Path]]) -> None:
        mounts = tuple(bind_mount(secrets_[key][1], target) for key, target in (("metadata_n8n", "/run/secrets/n8n_db_password"), ("valkey_n8n", "/run/secrets/n8n_valkey_password"), ("encryption", "/run/secrets/n8n_encryption_key"), ("runner", "/run/secrets/n8n_runner_auth_token")))
        self.create("main", N8N_REF, "1000:1000", ("ctl",), env=self._n8n_env(), mounts=mounts)
        self.create("worker", N8N_REF, "1000:1000", ("ctl", "runner", "dev", "capture"), env=self._n8n_env(), mounts=mounts, command=("worker", "--concurrency=1"))
        self.start("main")
        def health():
            ready, facts = n8n_health_probe(lambda *args: self.exec_result("main", *args))
            self.receipt["main_health_probe"] = facts
            return ready
        # At these caps a fresh database reached readiness 200 in 118 s and
        # 208 s (2026-10-20, SPEC-0204 TSK-0019); V16's 90 s wait expired first.
        self.wait_until(health, "n8n main readiness expired", 300, lambda: self.receipt.__setitem__("main_readiness_failure", main_readiness_failure_facts(self.client, self.containers["main"], self.attempt, lambda result: native.retain_failure_output(self.directory, self.files, self.receipt, result))))  # fmt: skip
        self.start("worker")
        def worker_broker_health():
            ready, facts = node_status_probe(lambda *args: self.exec_result("worker", *args), "http://127.0.0.1:5679/healthz")
            self.receipt["worker_broker_health_probe"] = facts
            return ready
        # The worker broker answered after 80 s against a 90 s wait (same date).
        self.wait_until(worker_broker_health, "n8n worker broker readiness expired", 300)
        def mailpit_health():
            ready, facts = node_status_probe(lambda *args: self.exec_result("worker", *args), "http://mailpit:8025/readyz")
            self.receipt["mailpit_health_probe"] = facts
            return ready
        self.wait_until(mailpit_health, "Mailpit native readiness expired")

    def start_runner(self, token: Path) -> None:
        script = "set -eu; N8N_RUNNERS_AUTH_TOKEN=$(cat /run/secrets/n8n-runner-token); export N8N_RUNNERS_AUTH_TOKEN; exec /usr/local/bin/task-runner-launcher javascript python"
        self.create("runner", RUNNER_REF, "1000:1000", ("runner",), env=("N8N_RUNNERS_TASK_BROKER_URI=http://n8n-worker:5679", "N8N_RUNNERS_TASK_TIMEOUT=60"), mounts=(bind_mount(token, "/run/secrets/n8n-runner-token"),), entrypoint="/bin/sh", command=("-ec", script))
        self.start("runner")
        self.wait_until(lambda: self.logs_contain("worker", 'Registered runner "'), "external runner did not register with worker broker", 60)
    # fmt: on

    def receipt_json(self) -> str:
        safe = {
            **self.receipt,
            "image_id": N8N_ID,
            "source_binding": N8N_LABELS["hyhome.source-binding"],
        }
        return json.dumps(safe, sort_keys=True)

    def cleanup(self) -> None:
        failures: list[str] = []
        resources_clear = False
        cancellation: BaseException | None = None
        try:
            self.client.begin_cleanup()
            for role in tuple(self.pending_containers):
                if role not in self.containers:
                    try:
                        self._adopt_pending_container(role)
                    except Exception:
                        failures.append("container_adoption")
            for role in tuple(reversed(self.containers)):
                try:
                    self.remove(role)
                except Exception:
                    failures.append("container")
            for role in tuple(self.pending_networks):
                if role not in self.networks:
                    try:
                        self._adopt_pending_network(role)
                    except Exception:
                        failures.append("network_adoption")
            for role, record in tuple(reversed(self.networks.items())):
                removed = False
                for attempt in range(2):
                    try:
                        self._verify_network_owned(role, record)
                        if self.client.run_result(
                            "network", "rm", record.network_id
                        ).returncode:
                            raise RehearsalFailure("owned network removal failed")
                        if (
                            self.client.run_result(
                                "network", "inspect", record.network_id
                            ).returncode
                            == 0
                        ):
                            raise RehearsalFailure(
                                "owned network remained after removal"
                            )
                        removed = True
                        break
                    except Exception:
                        if attempt:
                            failures.append("network")
                if removed:
                    self.networks.pop(role, None)
                    self.pending_networks.pop(role, None)
            container_ids, network_ids = sweep_attempt(self.client, self.attempt)
            self.swept_cids.update(container_ids)
            self.swept_nids.update(network_ids)
            resources_clear = not container_ids and not network_ids
            if not resources_clear:
                failures.append("residual_owned_resource")
        except BaseException as error:
            if not isinstance(error, Exception):
                cancellation = error
            failures.append("cleanup_boundary")
        finally:
            tracked = (
                self.containers
                or self.networks
                or self.pending_containers
                or self.pending_networks
            )
            cleanup_host = None
            if tracked or not resources_clear:
                failures.append("host_held_for_owned_resource")
            elif "failure_evidence" in self.receipt:
                failures.append("failure_evidence_retained")
            else:
                cleanup_host = self._cleanup_host
            boundary = native.finalize_host_boundary(cleanup_host, self.lock_fd)
            self.lock_fd, boundary_failures, boundary_cancellation = boundary
            failures.extend(boundary_failures)
            if cancellation is None:
                cancellation = boundary_cancellation
        self.receipt.update(cleanup="PASS" if not failures else "FAIL", cleanup_failures=sorted(set(failures)), swept_container_ids=sorted(self.swept_cids), swept_network_ids=sorted(self.swept_nids))  # fmt: skip
        self.receipt["retained"] = {
            "container_ids": sorted(
                {item.cid for item in self.containers.values()} | self.swept_cids
            ),
            "network_ids": sorted(
                {item.network_id for item in self.networks.values()} | self.swept_nids
            ),
            "pending_container_roles": sorted(self.pending_containers),
            "pending_network_roles": sorted(self.pending_networks),
            "attempt_dir": self.directory.name if self.dir_identity else None,
        }
        if cancellation is not None:
            raise cancellation
        if failures:
            raise RehearsalFailure("owned native cleanup incomplete")

    def _cleanup_host(self) -> None:
        if self.dir_identity is None:
            return
        for path, expected in tuple(self.files.items()):
            if not path.exists():
                self.files.pop(path, None)
                continue
            metadata = path.stat(follow_symlinks=False)
            identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid, metadata.st_gid, stat.S_IMODE(metadata.st_mode), metadata.st_nlink)  # fmt: skip
            expected_identity = (expected.device, expected.inode, expected.uid, expected.gid, expected.mode, 1)  # fmt: skip
            if identity != expected_identity or not stat.S_ISREG(metadata.st_mode):
                raise RehearsalFailure("owned host file metadata changed")
            path.unlink()
            self.files.pop(path, None)
        for data, identity in tuple(self.mailpit_dirs.items()):
            if os.path.lexists(data):
                metadata = data.stat(follow_symlinks=False)
                if (
                    not stat.S_ISDIR(metadata.st_mode)
                    or (metadata.st_dev, metadata.st_ino) != identity
                ):
                    raise RehearsalFailure("owned Mailpit store metadata changed")
                for item in data.iterdir():
                    metadata = item.stat(follow_symlinks=False)
                    if (
                        not stat.S_ISREG(metadata.st_mode)
                        or metadata.st_uid != self.host_uid
                        or not item.name.startswith("mailpit.db")
                    ):
                        raise RehearsalFailure("owned Mailpit store metadata changed")
                    item.unlink()
                data.rmdir()
            self.mailpit_dirs.pop(data)
        config = self.directory / "docker-config"
        if config.exists() and not any(config.iterdir()):
            config.rmdir()
        metadata = self.directory.stat(follow_symlinks=False)
        if (
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_uid,
            stat.S_IMODE(metadata.st_mode),
        ) != (*self.dir_identity, os.geteuid(), 0o700) or any(self.directory.iterdir()):
            raise RehearsalFailure("owned host directory cleanup refused")
        self.directory.rmdir()
        self.dir_identity = None
