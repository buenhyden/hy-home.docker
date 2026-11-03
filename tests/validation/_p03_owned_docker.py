"""Exact-owner Docker boundary for isolated P03 synthetic fixtures."""

from __future__ import annotations

import fcntl
import json
import math
import os
import re
import stat
import subprocess
import tempfile
import time
from pathlib import Path

from tests.validation.test_datastore_rehearsal_boundary import DockerClientBoundary


class NativeFixtureError(RuntimeError):
    """A value-free native-fixture failure."""


class _PerCallDockerClient(DockerClientBoundary):
    """Retain the fixed client identity while honoring each stage's deadline."""

    def __init__(self, **kwargs) -> None:
        self._requested_timeout: float | None = None
        super().__init__(**kwargs)

    def _remaining_timeout(self) -> float:
        inherited = super()._remaining_timeout()
        if self._requested_timeout is None:
            return inherited
        return min(inherited, self._requested_timeout)

    def run_result_with_timeout(self, timeout: float, *arguments: str):
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or not 0 < timeout <= 300
            or self._requested_timeout is not None
        ):
            raise NativeFixtureError("docker_timeout_invalid")
        self._requested_timeout = float(timeout)
        try:
            return self.run_result(*arguments)
        finally:
            self._requested_timeout = None


class OwnedDocker:
    """Track pending and created resources by immutable identity and labels."""

    OWNER_KEY = "hyhome.p03.native-owner"
    ATTEMPT_KEY = "hyhome.p03.native-attempt"
    OWNER = "tests.validation.p03"

    def __init__(
        self,
        prefix: str,
    ) -> None:
        if not re.fullmatch(r"p03-[a-z0-9-]{1,80}", prefix):
            raise NativeFixtureError("native_prefix_invalid")
        self.prefix = prefix
        self.pending = {kind: set() for kind in ("container", "network", "volume")}
        self.records = {kind: {} for kind in ("container", "network", "volume")}
        self._config: Path | None = None
        self._config_identity: tuple[int, int, int] | None = None
        self._client: _PerCallDockerClient | None = None
        self._lock_fd = -1

    def command(self, *arguments: str, timeout: float = 30) -> str:
        if self._client is None:
            raise NativeFixtureError("docker_boundary_unverified")
        try:
            result = self._client.run_result_with_timeout(timeout, *arguments)
        except PermissionError:
            raise NativeFixtureError("docker_authority_changed") from None
        except (
            OSError,
            TimeoutError,
            subprocess.TimeoutExpired,
            AssertionError,
            RuntimeError,
        ):
            raise NativeFixtureError("docker_unavailable") from None
        if result.returncode != 0:
            detail = (result.stderr or "").casefold()
            code = (
                "docker_permission"
                if "permission denied" in detail
                else "docker_failed"
            )
            raise NativeFixtureError(code)
        return result.stdout.strip()

    def verify_local_engine(self) -> None:
        if any(
            os.environ.get(key)
            for key in (
                "DOCKER_HOST",
                "DOCKER_CONTEXT",
                "DOCKER_TLS_VERIFY",
                "DOCKER_CERT_PATH",
                "DOCKER_CONFIG",
            )
        ):
            raise NativeFixtureError("docker_environment_refused")
        self._acquire_lock()
        try:
            self._initialize_client()
        except BaseException:
            self._client = None
            try:
                self._cleanup_config()
            finally:
                self._release_lock()
            raise

    def _initialize_client(self) -> None:
        self._config = Path(tempfile.mkdtemp(prefix=self.prefix + "-docker-config-"))
        self._config.chmod(0o700)
        metadata = self._config.stat(follow_symlinks=False)
        self._config_identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
        try:
            self._client = _PerCallDockerClient(
                binary=Path("/usr/bin/docker"),
                socket_path=Path("/var/run/docker.sock"),
                config_dir=self._config,
                deadline_seconds=20 * 60,
            )
        except (
            OSError,
            PermissionError,
            AssertionError,
            RuntimeError,
            TimeoutError,
            subprocess.TimeoutExpired,
        ):
            raise NativeFixtureError("docker_unavailable") from None
        if self.command("context", "show", timeout=10) != "default":
            raise NativeFixtureError("docker_context_refused")
        engine = self.command(
            "info", "--format", "{{.ID}}|{{.ServerVersion}}", timeout=10
        )
        if not re.fullmatch(r"[^|\s]+\|[^|\s]+", engine):
            raise NativeFixtureError("docker_engine_identity_invalid")

    def image_cached(self, image: str) -> bool:
        if self._client is None:
            raise NativeFixtureError("docker_boundary_unverified")
        try:
            result = self._client.run_result_with_timeout(
                15, "image", "inspect", "--format", "{{.Id}}", image
            )
        except PermissionError:
            raise NativeFixtureError("docker_authority_changed") from None
        except (
            OSError,
            TimeoutError,
            subprocess.TimeoutExpired,
            AssertionError,
            RuntimeError,
        ):
            raise NativeFixtureError("docker_unavailable") from None
        if result.returncode == 0:
            return True
        detail = (result.stderr or "").casefold()
        if "no such image" in detail or "no such object" in detail:
            return False
        if "permission denied" in detail:
            raise NativeFixtureError("docker_permission")
        raise NativeFixtureError("docker_unavailable")

    def _labels(self) -> list[str]:
        return [
            "--label",
            f"{self.OWNER_KEY}={self.OWNER}",
            "--label",
            f"{self.ATTEMPT_KEY}={self.prefix}",
        ]

    def _validate_labels(self, labels: object) -> None:
        if (
            not isinstance(labels, dict)
            or labels.get(self.OWNER_KEY) != self.OWNER
            or labels.get(self.ATTEMPT_KEY) != self.prefix
        ):
            raise NativeFixtureError("owned_resource_labels_changed")

    def create_network(self, name: str) -> str:
        self.pending["network"].add(name)
        identity = self.command(
            "network", "create", "--internal", *self._labels(), name
        )
        item = self._inspect_json("network", identity)
        self._validate_labels(item.get("Labels"))
        if item.get("Name") != name or item.get("Id") != identity:
            raise NativeFixtureError("owned_network_identity_changed")
        self.records["network"][name] = identity
        self.pending["network"].discard(name)
        return identity

    def create_volume(self, name: str) -> str:
        self.pending["volume"].add(name)
        returned = self.command("volume", "create", *self._labels(), name)
        item = self._inspect_json("volume", name)
        self._validate_labels(item.get("Labels"))
        if returned != name or item.get("Name") != name:
            raise NativeFixtureError("owned_volume_identity_changed")
        self.records["volume"][name] = name
        self.pending["volume"].discard(name)
        return name

    def create_container(self, name: str, *arguments: str) -> str:
        if (
            arguments.count("--pull=never") != 1
            or "--pull" in arguments
            or any(
                argument.startswith("--pull=") and argument != "--pull=never"
                for argument in arguments
            )
        ):
            raise NativeFixtureError("container_pull_policy_refused")
        self.pending["container"].add(name)
        identity = self.command(
            "create",
            "--name",
            name,
            *self._labels(),
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges=true",
            "--memory",
            "768m",
            "--memory-swap",
            "768m",
            "--cpus",
            "0.50",
            "--pids-limit",
            "256",
            "--stop-timeout",
            "10",
            *arguments,
        )
        item = self._inspect_json("container", identity)
        labels = (item.get("Config") or {}).get("Labels")
        self._validate_labels(labels)
        if item.get("Name") != "/" + name or item.get("Id") != identity:
            raise NativeFixtureError("owned_container_identity_changed")
        self.records["container"][name] = identity
        self.pending["container"].discard(name)
        return identity

    def _inspect_json(self, kind: str, identity: str) -> dict:
        prefix = () if kind == "container" else (kind,)
        raw = self.command(*prefix, "inspect", identity, timeout=15)
        try:
            value = json.loads(raw)
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            if not isinstance(value, dict):
                raise ValueError
            return value
        except (TypeError, ValueError, json.JSONDecodeError):
            raise NativeFixtureError("owned_resource_metadata_invalid") from None

    def remove_container(self, name: str) -> None:
        identity = self.container_id(name)
        item = self._inspect_json("container", identity)
        self._validate_labels((item.get("Config") or {}).get("Labels"))
        if item.get("Name") != "/" + name or item.get("Id") != identity:
            raise NativeFixtureError("owned_container_identity_changed")
        self.command("rm", "--force", "--volumes", identity, timeout=30)
        self.records["container"].pop(name)

    def container_id(self, name: str) -> str:
        identity = self.records["container"].get(name)
        if identity is None:
            raise NativeFixtureError("owned_container_record_missing")
        item = self._inspect_json("container", identity)
        self._validate_labels((item.get("Config") or {}).get("Labels"))
        if item.get("Name") != "/" + name or item.get("Id") != identity:
            raise NativeFixtureError("owned_container_identity_changed")
        return identity

    def cleanup(self) -> None:
        failures: list[str] = []
        if self._client is None:
            if any(self.pending.values()) or any(self.records.values()):
                raise NativeFixtureError("docker_boundary_unverified")
            self._cleanup_config()
            self._release_lock()
            return
        self._client.begin_cleanup()
        deadline = time.monotonic() + 60
        while any(self.pending.values()) and time.monotonic() < deadline:
            for kind in ("container", "network", "volume"):
                for name in tuple(self.pending[kind]):
                    try:
                        if self._adopt_pending(kind, name):
                            self.pending[kind].discard(name)
                    except NativeFixtureError:
                        failures.append(kind + "_adoption")
            if any(self.pending.values()):
                time.sleep(1)
        for names in self.pending.values():
            names.clear()
        try:
            self._adopt_labeled_sweep()
        except NativeFixtureError:
            failures.append("label_sweep")
        self._remove_recorded(failures)
        try:
            self._adopt_labeled_sweep()
            self._remove_recorded(failures)
        except NativeFixtureError:
            failures.append("late_sweep")
        if any(self.pending.values()) or any(self.records.values()):
            failures.append("residual")
        try:
            if any(self._labeled_identities().values()):
                failures.append("late_residual")
        except NativeFixtureError:
            failures.append("final_sweep")
        if not failures:
            try:
                self._cleanup_config()
            except NativeFixtureError:
                failures.append("config")
        if not failures:
            self._release_lock()
        if failures:
            raise NativeFixtureError("native_cleanup_incomplete")

    def _remove_recorded(self, failures: list[str]) -> None:
        for name in tuple(reversed(self.records["container"])):
            try:
                self.remove_container(name)
            except NativeFixtureError:
                failures.append("container")
        for kind in ("network", "volume"):
            for name, identity in tuple(reversed(self.records[kind].items())):
                try:
                    item = self._inspect_json(kind, identity)
                    self._validate_labels(item.get("Labels"))
                    if item.get("Name") != name:
                        raise NativeFixtureError("owned_resource_identity_changed")
                    self.command(kind, "rm", identity, timeout=30)
                    self.records[kind].pop(name)
                except NativeFixtureError:
                    failures.append(kind)

    def _adopt_pending(self, kind: str, name: str) -> bool:
        if kind == "container":
            candidates = self.command(
                "ps",
                "-aq",
                "--no-trunc",
                "--filter",
                f"name=^/{name}$",
                "--filter",
                f"label={self.ATTEMPT_KEY}={self.prefix}",
            ).split()
        else:
            candidates = self.command(
                kind,
                "ls",
                "-q",
                "--filter",
                f"name=^{name}$",
                "--filter",
                f"label={self.ATTEMPT_KEY}={self.prefix}",
            ).split()
        if not candidates:
            return False
        if len(candidates) != 1:
            raise NativeFixtureError("pending_resource_identity_ambiguous")
        identity = name if kind == "volume" else candidates[0]
        item = self._inspect_json(kind, identity)
        labels = (
            (item.get("Config") or {}).get("Labels")
            if kind == "container"
            else item.get("Labels")
        )
        self._validate_labels(labels)
        expected_name = "/" + name if kind == "container" else name
        if item.get("Name") != expected_name:
            raise NativeFixtureError("pending_resource_identity_changed")
        self.records[kind][name] = identity
        return True

    def _labeled_identities(self) -> dict[str, list[str]]:
        result = {}
        for kind in ("container", "network", "volume"):
            command = (
                ("ps", "-aq", "--no-trunc")
                if kind == "container"
                else (kind, "ls", "-q")
            )
            result[kind] = self.command(
                *command,
                "--filter",
                f"label={self.ATTEMPT_KEY}={self.prefix}",
            ).split()
        return result

    def _adopt_labeled_sweep(self) -> None:
        for kind, identities in self._labeled_identities().items():
            for identity in identities:
                item = self._inspect_json(kind, identity)
                labels = (
                    (item.get("Config") or {}).get("Labels")
                    if kind == "container"
                    else item.get("Labels")
                )
                self._validate_labels(labels)
                raw_name = item.get("Name")
                name = raw_name.removeprefix("/") if isinstance(raw_name, str) else ""
                if not name.startswith(self.prefix):
                    raise NativeFixtureError("labeled_resource_name_invalid")
                stored = name if kind == "volume" else identity
                self.records[kind].setdefault(name, stored)

    def _cleanup_config(self) -> None:
        if self._config is None:
            return
        metadata = self._config.stat(follow_symlinks=False)
        identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
        if (
            not stat.S_ISDIR(metadata.st_mode)
            or identity != self._config_identity
            or any(self._config.iterdir())
        ):
            raise NativeFixtureError("docker_config_changed")
        self._config.rmdir()
        self._config = None
        self._config_identity = None

    def _acquire_lock(self) -> None:
        path = "/tmp/hyhome-opsflow-native-rehearsal.lock"
        try:
            descriptor = os.open(
                path,
                os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW,
                0o600,
            )
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_uid != os.geteuid()
                or stat.S_IMODE(metadata.st_mode) != 0o600
                or metadata.st_nlink != 1
            ):
                raise NativeFixtureError("native_lock_metadata_invalid")
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(descriptor)
            raise NativeFixtureError("native_lock_held") from None
        except (OSError, NativeFixtureError):
            if "descriptor" in locals():
                os.close(descriptor)
            raise
        self._lock_fd = descriptor

    def _release_lock(self) -> None:
        if self._lock_fd < 0:
            return
        fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
        os.close(self._lock_fd)
        self._lock_fd = -1
