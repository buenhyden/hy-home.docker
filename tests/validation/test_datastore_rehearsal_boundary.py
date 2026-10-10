from __future__ import annotations

import json
import os
import re
import secrets
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple
from unittest import mock

from tests.validation._supabase_smtp_fixture_storage import write_exclusive

ROOT = Path(__file__).resolve().parents[2]
ATTEMPT_LABEL = "hyhome.rehearsal.attempt"
INVOCATION_LABEL = "hyhome.rehearsal.invocation"
IMAGE_LABEL = "hyhome.rehearsal.image"
IMAGE_ID_LABEL = "hyhome.rehearsal.image-id"
MAX_OUTPUT_BYTES = 2 * 1024 * 1024
CLEANUP_SECONDS = 2 * 60
CLEANUP_CALL_SECONDS = 2.4
PROCESS_REAP_SECONDS = 0.25
RUN_FLAGS = frozenset(("-d", "-i", "--rm", "--read-only"))
RUN_VALUE_OPTIONS = frozenset(
    (
        "--name",
        "--network",
        "--network-alias",
        "-e",
        "--env",
        "-v",
        "--volume",
        "--user",
        "--tmpfs",
        "--entrypoint",
        "--cap-drop",
        "--security-opt",
        "-w",
        "--workdir",
    )
)


@dataclass(frozen=True)
class ImageBinding:
    reference: str
    image_id: str
    repo_digests: tuple[str, ...]


@dataclass(frozen=True)
class OwnedContainer:
    container_id: str
    name: str
    invocation: str
    image: str
    image_id: str
    auto_remove: bool


class OwnedNetwork(NamedTuple):
    network_id: str
    name: str


@dataclass(frozen=True)
class CleanupIssue:
    kind: str
    resource_id: str
    category: str


class CleanupFailure(AssertionError):
    def __init__(
        self,
        issues: list[CleanupIssue],
        container_ids: set[str],
        network_ids: set[str],
    ) -> None:
        self.issues = tuple(issues)
        self.container_ids = tuple(sorted(container_ids))
        self.network_ids = tuple(sorted(network_ids))
        categories = ",".join(sorted({issue.category for issue in issues}))
        super().__init__(
            "cleanup incomplete "
            f"categories={categories} containers={self.container_ids} "
            f"networks={self.network_ids}"
        )


def new_attempt_prefix() -> str:
    return f"obs-rehearsal-{secrets.token_hex(12)}"


def write_private_fixture(directory: Path, name: str, content: str) -> Path:
    target = write_exclusive(directory, name, content, 0o640)
    metadata = target.stat(follow_symlinks=False)
    if metadata.st_gid != os.getegid():
        raise PermissionError("synthetic fixture group does not match the runner")
    return target


class DockerClientBoundary:
    def __init__(
        self,
        *,
        binary: Path,
        socket_path: Path,
        config_dir: Path,
        deadline_seconds: int,
        max_output_bytes: int = MAX_OUTPUT_BYTES,
    ) -> None:
        self.binary = binary
        self.socket_path = socket_path
        self.config_dir = config_dir
        self.deadline = time.monotonic() + deadline_seconds
        self.cleanup_deadline: float | None = None
        self.cleanup_identity_verified = False
        self.max_output_bytes = max_output_bytes
        self._binary_identity = self._validate_binary()
        self._socket_identity = self._validate_socket()
        self._validate_config()
        self.environment = {
            "DOCKER_CONFIG": str(config_dir),
            "DOCKER_HOST": f"unix://{socket_path}",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
        }
        self._daemon_identity = self._query_daemon_identity()

    @staticmethod
    def _identity(
        metadata: os.stat_result,
    ) -> tuple[int, int, int, int, int, int, int, int]:
        return (
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_uid,
            metadata.st_gid,
            metadata.st_mode,
            metadata.st_nlink,
            metadata.st_size,
            metadata.st_ctime_ns,
        )

    def _validate_binary(self) -> tuple[int, int, int, int, int, int, int, int]:
        metadata = self.binary.stat(follow_symlinks=False)
        if not stat.S_ISREG(metadata.st_mode) or not metadata.st_mode & 0o111:
            raise PermissionError("Docker client is not a fixed executable file")
        return self._identity(metadata)

    def _validate_socket(self) -> tuple[int, int, int, int, int, int, int, int]:
        metadata = self.socket_path.stat(follow_symlinks=False)
        if not stat.S_ISSOCK(metadata.st_mode):
            raise PermissionError("Docker endpoint is not the fixed local socket")
        return self._identity(metadata)

    def _validate_config(self) -> None:
        metadata = self.config_dir.stat(follow_symlinks=False)
        if (
            not stat.S_ISDIR(metadata.st_mode)
            or metadata.st_uid != os.geteuid()
            or stat.S_IMODE(metadata.st_mode) != 0o700
            or any(self.config_dir.iterdir())
        ):
            raise PermissionError("Docker client config must be new, empty and private")

    def _remaining_timeout(self) -> float:
        deadline = self.cleanup_deadline or self.deadline
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("datastore rehearsal deadline expired")
        per_call = CLEANUP_CALL_SECONDS if self.cleanup_deadline else 240.0
        return min(per_call, remaining)

    @staticmethod
    def _terminate_process_group(process: subprocess.Popen[bytes], deadline: float) -> None:  # fmt: skip
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            process.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("bounded Docker client process did not terminate") from error  # fmt: skip

    def _bounded_process(
        self,
        command: list[str],
        input_: str | None,
    ) -> subprocess.CompletedProcess[str]:
        call_timeout = self._remaining_timeout()
        call_deadline = time.monotonic() + call_timeout
        work_deadline = call_deadline - min(PROCESS_REAP_SECONDS, call_timeout / 2)
        with (
            tempfile.TemporaryFile() as stdin_file,
            tempfile.TemporaryFile() as stdout_file,
            tempfile.TemporaryFile() as stderr_file,
        ):
            if input_ is not None:
                stdin_file.write(input_.encode())
                stdin_file.seek(0)
            process = subprocess.Popen(
                command,
                stdin=stdin_file,
                stdout=stdout_file,
                stderr=stderr_file,
                env=self.environment,
                cwd=ROOT,
                start_new_session=True,
            )
            while process.poll() is None:
                stdout_size = os.fstat(stdout_file.fileno()).st_size
                stderr_size = os.fstat(stderr_file.fileno()).st_size
                if stdout_size > self.max_output_bytes:
                    self._terminate_process_group(process, call_deadline)
                    raise AssertionError("Docker stdout exceeded the rehearsal bound")
                if stderr_size > self.max_output_bytes:
                    self._terminate_process_group(process, call_deadline)
                    raise AssertionError("Docker stderr exceeded the rehearsal bound")
                if time.monotonic() >= work_deadline:
                    self._terminate_process_group(process, call_deadline)
                    raise subprocess.TimeoutExpired(command, call_timeout)
                time.sleep(0.01)
            stdout_size = os.fstat(stdout_file.fileno()).st_size
            stderr_size = os.fstat(stderr_file.fileno()).st_size
            if stdout_size > self.max_output_bytes:
                raise AssertionError("Docker stdout exceeded the rehearsal bound")
            if stderr_size > self.max_output_bytes:
                raise AssertionError("Docker stderr exceeded the rehearsal bound")
            stdout_file.seek(0)
            stderr_file.seek(0)
            return subprocess.CompletedProcess(
                command,
                process.returncode,
                stdout_file.read().decode(errors="replace"),
                stderr_file.read().decode(errors="replace"),
            )

    def _raw_result(
        self,
        *args: str,
        input_: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self._bounded_process([str(self.binary), *args], input_)

    def _raw(
        self,
        *args: str,
        check: bool = True,
        input_: str | None = None,
    ) -> str:
        result = self._raw_result(*args, input_=input_)
        if check and result.returncode != 0:
            raise AssertionError(f"Docker {args[0]} failed (exit {result.returncode})")
        return result.stdout

    def _query_daemon_identity(self) -> str:
        identity = self._raw(
            "info",
            "--format",
            "{{.ID}}|{{.ServerVersion}}|{{.OperatingSystem}}|{{.Architecture}}|"
            "{{.DockerRootDir}}",
        ).strip()
        if not identity:
            raise AssertionError("Docker daemon identity is empty")
        return identity

    def run(
        self,
        *args: str,
        check: bool = True,
        input_: str | None = None,
    ) -> str:
        self._validate_context()
        return self._raw(*args, check=check, input_=input_)

    def run_result(
        self, *args: str, input_: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        self._validate_context()
        return self._raw_result(*args, input_=input_)

    def _validate_context(self) -> None:
        if self._validate_binary() != self._binary_identity:
            raise PermissionError("Docker client identity changed")
        if self._validate_socket() != self._socket_identity:
            raise PermissionError("Docker socket identity changed")
        if (
            not self.cleanup_identity_verified
            and self._query_daemon_identity() != self._daemon_identity
        ):
            raise PermissionError("Docker daemon identity changed")  # fmt: skip

    def begin_cleanup(self) -> None:
        if self.cleanup_deadline is None:
            self.cleanup_deadline = time.monotonic() + CLEANUP_SECONDS
            self._validate_context()
            self.cleanup_identity_verified = True


class AttemptResources:
    def __init__(
        self,
        attempt: str,
        client: DockerClientBoundary,
        state_dir: Path | None = None,
    ) -> None:
        self.attempt = attempt
        self.client = client
        self.state_dir = state_dir
        self.container_ids: set[str] = set()
        self.network_ids: set[str] = set()
        self.container_names: dict[str, str] = {}
        self.network_names: dict[str, str] = {}
        self.container_records: dict[str, OwnedContainer] = {}
        self.network_records: dict[str, OwnedNetwork] = {}
        self.image_bindings: dict[str, ImageBinding] = {}
        self._invocation = 0

    def register_images(
        self,
        images: set[str],
        *,
        require_repo_digests: set[str] | None = None,
    ) -> None:
        if not images or any(
            not isinstance(image, str) or not image for image in images
        ):
            raise ValueError("rehearsal images must be non-empty strings")
        required = require_repo_digests or set()
        if not required.issubset(images):
            raise ValueError("required digest images must be registered together")
        bindings: dict[str, ImageBinding] = {}
        for image in sorted(images):
            result = self.client.run_result("image", "inspect", image)
            if result.returncode != 0:
                raise AssertionError(f"rehearsal image is not cached: {image}")
            payload = self._object(result.stdout)
            image_id = payload.get("Id")
            repo_digests = payload.get("RepoDigests") or []
            if not isinstance(image_id, str) or not re.fullmatch(
                r"sha256:[0-9a-f]{64}", image_id
            ):
                raise AssertionError("cached image ID is invalid")
            if not isinstance(repo_digests, list) or any(
                not isinstance(digest, str)
                or not re.search(r"@sha256:[0-9a-f]{64}\Z", digest)
                for digest in repo_digests
            ):
                raise AssertionError("cached RepoDigests are invalid")
            if image in required and not repo_digests:
                raise AssertionError(f"cached image has no RepoDigest: {image}")
            repository = image.rsplit(":", 1)[0]
            if image in required and not any(
                digest.partition("@")[0] == repository for digest in repo_digests
            ):
                raise AssertionError(f"cached RepoDigest does not match: {image}")
            bindings[image] = ImageBinding(image, image_id, tuple(sorted(repo_digests)))
        self.image_bindings = {**self.image_bindings, **bindings}

    @staticmethod
    def _object(payload: str) -> dict:
        decoded = json.loads(payload)
        if isinstance(decoded, list):
            if len(decoded) != 1:
                raise AssertionError("Docker inspect returned an unexpected count")
            decoded = decoded[0]
        if not isinstance(decoded, dict):
            raise AssertionError("Docker inspect did not return an object")
        return decoded

    def create_network(self, logical_name: str) -> str:
        name = f"{self.attempt}-{logical_name}"
        try:
            output = self.client.run(
                "network",
                "create",
                "--internal",
                "--label",
                f"{ATTEMPT_LABEL}={self.attempt}",
                name,
            ).strip()
        except AssertionError:
            output = self._recover_network(name)
            if output is None:
                raise
        if not re.fullmatch(r"[0-9a-f]{64}", output):
            output = self._recover_network(name) or ""
        if not re.fullmatch(r"[0-9a-f]{64}", output):
            raise AssertionError("Docker did not return an exact network ID")
        self.network_ids.add(output)
        self.network_names[name] = output
        self.network_records[output] = OwnedNetwork(output, name)
        if not self._network_present(self.network_records[output]):
            raise AssertionError("created network disappeared before validation")
        return name

    def _recover_network(self, name: str) -> str | None:
        candidates = self.client.run(
            "network",
            "ls",
            "-q",
            "--filter",
            f"label={ATTEMPT_LABEL}={self.attempt}",
            "--filter",
            f"name=^{name}$",
            check=False,
        ).split()
        if not candidates:
            return None
        if len(candidates) != 1 or not re.fullmatch(r"[0-9a-f]{64}", candidates[0]):
            raise AssertionError("network recovery did not resolve one exact ID")
        network_id = candidates[0]
        inspected = self._object(
            self.client.run("network", "inspect", network_id, check=False)
        )
        if (
            inspected.get("Id") != network_id
            or inspected.get("Name") != name
            or not inspected.get("Internal")
            or (inspected.get("Labels") or {}).get(ATTEMPT_LABEL) != self.attempt
        ):
            raise AssertionError("recovered network creation input does not match")
        return network_id

    def _container_input(
        self, args: tuple[str, ...]
    ) -> tuple[str, ImageBinding, int, str, dict[str, list[str]]]:
        parsed: dict[str, list[str]] = {}
        index = 0
        while index < len(args):
            option = args[index]
            if option in RUN_FLAGS:
                parsed.setdefault(option, []).append("")
                index += 1
                continue
            if option in RUN_VALUE_OPTIONS:
                if index + 1 >= len(args):
                    raise AssertionError("container option is incomplete")
                parsed.setdefault(option, []).append(args[index + 1])
                index += 2
                continue
            if option.startswith("-") or option not in self.image_bindings:
                raise AssertionError(
                    "container invocation has an unsupported option or image"
                )
            return (
                option,
                self.image_bindings[option],
                index,
                secrets.token_hex(16),
                parsed,
            )
        raise AssertionError("container invocation must contain one bound image")

    def _private_environment_args(
        self, args: tuple[str, ...], invocation_number: int
    ) -> list[str]:
        if self.state_dir is None:
            raise AssertionError(
                "environment storage requires a private state directory"
            )
        rewritten: list[str] = []
        index = 0
        environment_index = 0
        while index < len(args):
            value = args[index]
            if value not in ("-e", "--env"):
                rewritten.append(value)
                index += 1
                continue
            if index + 1 >= len(args):
                raise AssertionError("container environment option is incomplete")
            assignment = args[index + 1]
            key, separator, _ = assignment.partition("=")
            if (
                not separator
                or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key)
                or "\n" in assignment
                or "\x00" in assignment
            ):
                raise AssertionError("container environment assignment is invalid")
            environment_index += 1
            filename = f"env-{invocation_number}-{environment_index}"
            path = write_private_fixture(self.state_dir, filename, assignment + "\n")
            rewritten.extend(("--env-file", str(path)))
            index += 2
        return rewritten

    def _run_container(
        self,
        *args: str,
        check: bool = True,
        input_: str | None = None,
        return_result: bool = False,
    ) -> str | subprocess.CompletedProcess[str]:
        if self.state_dir is None:
            raise AssertionError(
                "container tracking requires a private state directory"
            )
        image, binding, image_index, invocation, parsed = self._container_input(args)
        self._invocation += 1
        singletons = (
            "--name",
            "--network",
            "--user",
            "--entrypoint",
            "--cap-drop",
            "--security-opt",
            "-w",
            "--workdir",
        )
        if any(len(parsed.get(option, ())) > 1 for option in singletons):
            raise AssertionError("container option must not be repeated")
        if parsed.get("--cap-drop", ["ALL"]) != ["ALL"]:
            raise AssertionError("container capabilities must be dropped")
        if parsed.get("--security-opt", ["no-new-privileges:true"]) != [
            "no-new-privileges:true"
        ]:
            raise AssertionError("container security option is unsupported")
        if parsed.get("--user", ["999:999"]) != ["999:999"]:
            raise AssertionError("container user is unsupported")
        name = (parsed.get("--name") or [f"{self.attempt}-job-{self._invocation}"])[0]
        if not name.startswith(f"{self.attempt}-"):
            raise AssertionError("container name escapes the attempt namespace")
        for volume in parsed.get("-v", []) + parsed.get("--volume", []):
            if "docker.sock" in volume:
                raise AssertionError("Docker socket mounts are forbidden")
            source, separator, _ = volume.partition(":")
            mode_separator = volume.rfind(":")
            modes = set(volume[mode_separator + 1 :].split(","))
            if (
                not separator
                or mode_separator <= len(source)
                or "ro" not in modes
                or "rw" in modes
            ):
                raise AssertionError("host bind mounts must be read-only")
            resolved = Path(source).resolve(strict=True)
            roots = (ROOT.resolve(), self.state_dir.resolve())
            if not any(
                resolved == root or resolved.is_relative_to(root) for root in roots
            ):
                raise AssertionError("host bind mount is outside the rehearsal inputs")
            if resolved in roots or ".git" in resolved.parts:
                raise AssertionError("broad repository or state mounts are forbidden")
            if resolved.is_relative_to(ROOT.resolve()) and resolved.relative_to(
                ROOT.resolve()
            ).parts[:1] == ("secrets",):
                raise AssertionError("repository secret mounts are forbidden")
        network = (parsed.get("--network") or [None])[0]
        owned_network = None
        if network is not None:
            network_id = self.network_names.get(network)
            owned_network = self.network_records.get(network_id) if network_id else None
            if owned_network is None or not self._network_present(owned_network):
                raise AssertionError("container network is not owned by this attempt")
        cidfile = self.state_dir / f"cid-{self._invocation}"
        if cidfile.exists():
            raise FileExistsError(cidfile)
        common = [
            "--name",
            name,
            "--label",
            f"{ATTEMPT_LABEL}={self.attempt}",
            "--label",
            f"{INVOCATION_LABEL}={invocation}",
            "--label",
            f"{IMAGE_LABEL}={image}",
            "--label",
            f"{IMAGE_ID_LABEL}={binding.image_id}",
            "--cidfile",
            str(cidfile),
            "--pull",
            "never",
            "--cpus",
            "1",
            "--memory",
            "512m",
            "--pids-limit",
            "128",
            "--group-add",
            str(os.getegid()),
        ]
        if network is None:
            common += ["--network", "none"]
        supplied_name = "--name" in args
        bound_args = list(args)
        bound_args[image_index] = binding.image_id
        if owned_network is not None:
            network_index = bound_args.index("--network")
            bound_args[network_index + 1] = owned_network.network_id
        command = (
            self._private_environment_args(
                tuple(bound_args[:image_index]), self._invocation
            )
            + bound_args[image_index:]
        )
        if supplied_name:
            name_index = command.index("--name")
            del command[name_index : name_index + 2]
        try:
            if return_result:
                output = self.client.run_result("run", *common, *command, input_=input_)
            else:
                output = self.client.run(
                    "run", *common, *command, check=check, input_=input_
                )
        finally:
            captured = False
            try:
                container_id = self._consume_cidfile(cidfile)
                if not re.fullmatch(r"[0-9a-f]{64}", container_id):
                    raise AssertionError("Docker cidfile did not contain an exact ID")
                candidate = OwnedContainer(
                    container_id,
                    name,
                    invocation,
                    image,
                    binding.image_id,
                    "--rm" in args,
                )
                if self._container_present(candidate):
                    self._track_container(candidate)
                    captured = True
            except (
                AssertionError,
                OSError,
                UnicodeError,
                ValueError,
                subprocess.SubprocessError,
            ):
                captured = False
            if not captured:
                self._recover_container(invocation, binding, name, "--rm" in args)
            record = self._record_for_name(name)
            if record is not None and record.auto_remove:
                self._retire_auto_removed(record)
        return output

    def _track_container(self, record: OwnedContainer) -> None:
        self.container_ids.add(record.container_id)
        self.container_names[record.name] = record.container_id
        self.container_records[record.container_id] = record

    def _forget_container(self, record: OwnedContainer) -> None:
        self.container_ids.discard(record.container_id)
        if self.container_names.get(record.name) == record.container_id:
            self.container_names.pop(record.name, None)
        self.container_records.pop(record.container_id, None)

    def _record_for_name(self, name: str) -> OwnedContainer | None:
        container_id = self.container_names.get(name)
        return self.container_records.get(container_id) if container_id else None

    def _retire_auto_removed(self, record: OwnedContainer) -> None:
        if not self._container_present(record):
            self._forget_container(record)

    def _consume_cidfile(self, cidfile: Path) -> str:
        directory_fd = os.open(
            self.state_dir,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        descriptor = -1
        try:
            descriptor = os.open(
                cidfile.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
                dir_fd=directory_fd,
            )
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_uid != os.geteuid()
                or metadata.st_nlink != 1
            ):
                raise PermissionError("Docker cidfile metadata is invalid")
            payload = os.read(descriptor, 130)
            if len(payload) > 129 or os.read(descriptor, 1):
                raise AssertionError("Docker cidfile exceeded the input bound")
            os.unlink(cidfile.name, dir_fd=directory_fd)
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            os.close(directory_fd)
        return payload.decode("ascii").strip()

    def run_container(
        self,
        *args: str,
        check: bool = True,
        input_: str | None = None,
    ) -> str:
        result = self._run_container(*args, check=check, input_=input_)
        if not isinstance(result, str):
            raise AssertionError("Docker container invocation returned invalid output")
        return result

    def run_container_result(
        self, *args: str, input_: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        result = self._run_container(*args, input_=input_, return_result=True)
        if isinstance(result, str):
            raise AssertionError("Docker container invocation returned invalid result")
        return result

    def _recover_container(
        self,
        invocation: str,
        binding: ImageBinding,
        name: str,
        auto_remove: bool,
    ) -> None:
        candidates = self.client.run(
            "ps",
            "-aq",
            "--filter",
            f"label={ATTEMPT_LABEL}={self.attempt}",
            "--filter",
            f"label={INVOCATION_LABEL}={invocation}",
            check=False,
        ).split()
        if not candidates:
            if auto_remove:
                return
            raise AssertionError("persistent container creation cannot be recovered")
        if len(candidates) != 1:
            raise AssertionError("container recovery did not resolve one exact ID")
        container_id = candidates[0]
        if not re.fullmatch(r"[0-9a-f]{64}", container_id):
            raise AssertionError("recovered container ID is invalid")
        payload = self.client.run("inspect", container_id, check=False)
        inspected = self._object(payload)
        config = inspected.get("Config") or {}
        labels = config.get("Labels") or {}
        if (
            inspected.get("Id") != container_id
            or inspected.get("Name", "").removeprefix("/") != name
            or labels.get(ATTEMPT_LABEL) != self.attempt
            or labels.get(INVOCATION_LABEL) != invocation
            or labels.get(IMAGE_LABEL) != binding.reference
            or labels.get(IMAGE_ID_LABEL) != binding.image_id
            or config.get("Image") != binding.image_id
            or inspected.get("Image") != binding.image_id
        ):
            raise AssertionError("recovered container creation input does not match")
        self._track_container(
            OwnedContainer(
                container_id,
                name,
                invocation,
                binding.reference,
                binding.image_id,
                auto_remove,
            )
        )

    def remove_container(self, name: str) -> None:
        record = self._record_for_name(name)
        if record is None:
            raise AssertionError("container name is not owned by this attempt")
        if not self._container_present(record):
            self._forget_container(record)
            return
        removed = self.client.run_result("rm", "-f", record.container_id)
        issues: list[CleanupIssue] = []
        if removed.returncode != 0:
            issues.append(CleanupIssue("container", record.container_id, "rm_failed"))
        if self._container_present(record):
            issues.append(
                CleanupIssue("container", record.container_id, "post_remove_present")
            )
        else:
            self._forget_container(record)
        if issues:
            raise CleanupFailure(issues, self.container_ids, self.network_ids)

    def _container_present(self, record: OwnedContainer) -> bool:
        result = self.client.run_result("inspect", record.container_id)
        if result.returncode != 0:
            missing = (f"Error: No such object: {record.container_id}", f"Error response from daemon: No such container: {record.container_id}")  # fmt: skip
            if (
                result.returncode == 1
                and not result.stdout
                and result.stderr.strip() in missing
            ):
                return False  # fmt: skip
            raise AssertionError("container absence check failed closed")
        inspected = self._object(result.stdout)
        config = inspected.get("Config") or {}
        labels = config.get("Labels") or {}
        if (
            inspected.get("Id") != record.container_id
            or inspected.get("Name", "").removeprefix("/") != record.name
            or inspected.get("Image") != record.image_id
            or config.get("Image") != record.image_id
            or labels.get(ATTEMPT_LABEL) != self.attempt
            or labels.get(INVOCATION_LABEL) != record.invocation
            or labels.get(IMAGE_LABEL) != record.image
            or labels.get(IMAGE_ID_LABEL) != record.image_id
        ):
            raise AssertionError("container ownership record does not match")
        return True

    def _network_present(self, record: OwnedNetwork) -> bool:
        result = self.client.run_result("network", "inspect", record.network_id)
        if result.returncode != 0:
            listed = self.client.run_result(
                "network",
                "ls",
                "-q",
                "--no-trunc",
                "--filter",
                f"id={record.network_id}",
            )
            if listed.returncode != 0:
                raise AssertionError("network absence check failed")
            candidates = listed.stdout.split()
            if candidates:
                raise AssertionError("network inspect failed while exact ID exists")
            return False
        inspected = self._object(result.stdout)
        if (
            inspected.get("Id") != record.network_id
            or inspected.get("Name") != record.name
            or not inspected.get("Internal")
            or (inspected.get("Labels") or {}).get(ATTEMPT_LABEL) != self.attempt
        ):
            raise AssertionError("network ownership record does not match")
        return True

    def _forget_network(self, record: OwnedNetwork) -> None:
        self.network_ids.discard(record.network_id)
        if self.network_names.get(record.name) == record.network_id:
            self.network_names.pop(record.name, None)
        self.network_records.pop(record.network_id, None)

    def run_owned(self, *args: str, check: bool = True) -> str:
        if not args:
            raise AssertionError("raw Docker operation is forbidden")
        action = args[0]
        if action in {"logs", "stop", "start", "restart"}:
            if len(args) != 2:
                raise AssertionError("owned container operation shape is invalid")
            record = self._record_for_name(args[1])
            if record is None or not self._container_present(record):
                raise AssertionError("container name is not currently owned")
            return self.client.run(action, record.container_id, check=check)
        if action == "exec":
            if len(args) < 3:
                raise AssertionError("owned exec operation shape is invalid")
            record = self._record_for_name(args[1])
            if record is None or not self._container_present(record):
                raise AssertionError("container name is not currently owned")
            return self.client.run("exec", record.container_id, *args[2:], check=check)
        if args[:2] == ("network", "connect"):
            tail = list(args[2:])
            aliases: list[str] = []
            while tail[:1] == ["--alias"] and len(tail) >= 2:
                aliases += tail[:2]
                del tail[:2]
            if len(tail) != 2:
                raise AssertionError("owned network connect shape is invalid")
            network_id = self.network_names.get(tail[0])
            container = self._record_for_name(tail[1])
            network = self.network_records.get(network_id) if network_id else None
            if (
                network is None
                or container is None
                or not self._network_present(network)
                or not self._container_present(container)
            ):
                raise AssertionError("network connect target is not currently owned")
            return self.client.run(
                "network",
                "connect",
                *aliases,
                network.network_id,
                container.container_id,
                check=check,
            )
        raise AssertionError("raw Docker operation is forbidden")

    def cleanup(self) -> None:
        begin_cleanup = getattr(self.client, "begin_cleanup", None)
        if callable(begin_cleanup):
            begin_cleanup()
        issues: list[CleanupIssue] = []
        records = sorted(
            self.container_records.values(),
            key=lambda record: (record.auto_remove, record.container_id),
        )
        for record in records:
            try:
                if not self._container_present(record):
                    self._forget_container(record)
                    continue
                result = self.client.run_result("rm", "-f", record.container_id)
                if result.returncode != 0:
                    issues.append(
                        CleanupIssue("container", record.container_id, "rm_failed")
                    )
                if self._container_present(record):
                    issues.append(
                        CleanupIssue(
                            "container", record.container_id, "post_remove_present"
                        )
                    )
                else:
                    self._forget_container(record)
            except (
                AssertionError,
                OSError,
                RuntimeError,
                ValueError,
                subprocess.TimeoutExpired,
            ) as error:
                issues.append(
                    CleanupIssue(
                        "container",
                        record.container_id,
                        f"verification_failed:{type(error).__name__}",
                    )
                )
        for record in sorted(
            self.network_records.values(), key=lambda item: item.network_id
        ):
            try:
                if not self._network_present(record):
                    self._forget_network(record)
                    continue
                result = self.client.run_result("network", "rm", record.network_id)
                if result.returncode != 0:
                    issues.append(
                        CleanupIssue("network", record.network_id, "rm_failed")
                    )
                if self._network_present(record):
                    issues.append(
                        CleanupIssue(
                            "network", record.network_id, "post_remove_present"
                        )
                    )
                else:
                    self._forget_network(record)
            except (
                AssertionError,
                OSError,
                RuntimeError,
                ValueError,
                subprocess.TimeoutExpired,
            ) as error:
                issues.append(
                    CleanupIssue(
                        "network",
                        record.network_id,
                        f"verification_failed:{type(error).__name__}",
                    )
                )
        recorded_container_ids = set(self.container_records)
        recorded_network_ids = set(self.network_records)
        for resource_id in sorted(self.container_ids - recorded_container_ids):
            issues.append(CleanupIssue("container", resource_id, "record_missing"))
        for resource_id in sorted(self.network_ids - recorded_network_ids):
            issues.append(CleanupIssue("network", resource_id, "record_missing"))
        if issues or self.container_ids or self.network_ids:
            raise CleanupFailure(
                issues,
                self.container_ids,
                self.network_ids,
            )


class DatastoreRehearsalBoundaryTests(unittest.TestCase):
    IMAGE = "postgres:18.6-alpine"
    IMAGE_ID = "sha256:" + "1" * 64
    DIGEST = "postgres@sha256:" + "2" * 64

    @staticmethod
    def completed(returncode: int, stdout: str = "", stderr: str = ""):
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    def bind(self, resources: AttemptResources) -> None:
        payload = json.dumps({"Id": self.IMAGE_ID, "RepoDigests": [self.DIGEST]})
        resources.client.run_result.return_value = self.completed(0, payload)
        resources.register_images({self.IMAGE}, require_repo_digests={self.IMAGE})
        resources.client.reset_mock()

    def test_attempt_prefix_and_private_fixture_contract(self) -> None:
        first, second = new_attempt_prefix(), new_attempt_prefix()
        self.assertRegex(first, r"\Aobs-rehearsal-[0-9a-f]{24}\Z")
        self.assertNotEqual(first, second)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            target = write_private_fixture(directory, "secret", "synthetic\n")
            metadata = target.stat()
            self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o640)
            self.assertEqual(
                (metadata.st_uid, metadata.st_gid), (os.geteuid(), os.getegid())
            )
            with self.assertRaises(FileExistsError):
                write_private_fixture(directory, "secret", "replacement\n")

    def test_image_binding_requires_cached_id_and_repodigest(self) -> None:
        client = mock.Mock()
        resources = AttemptResources("attempt", client)
        client.run_result.return_value = self.completed(
            0, json.dumps({"Id": self.IMAGE_ID, "RepoDigests": []})
        )
        with self.assertRaisesRegex(AssertionError, "no RepoDigest"):
            resources.register_images({self.IMAGE}, require_repo_digests={self.IMAGE})
        client.run_result.return_value = self.completed(
            0, json.dumps({"Id": self.IMAGE_ID, "RepoDigests": [self.DIGEST]})
        )
        resources.register_images({self.IMAGE}, require_repo_digests={self.IMAGE})
        self.assertEqual(resources.image_bindings[self.IMAGE].image_id, self.IMAGE_ID)

    def test_dev_provisioning_shape_accepts_stdin_flag(self) -> None:
        resources = AttemptResources("attempt", mock.Mock())
        self.bind(resources)
        args = ("--rm", "-i", "--network", "attempt-dev", "-e", "PGPASSWORD=x", self.IMAGE, "psql", "-X")  # fmt: skip
        self.assertEqual(resources._container_input(args)[0], self.IMAGE)

    def test_lost_create_recovery_binds_all_container_inputs(self) -> None:
        container_id = "a" * 64
        client = mock.Mock()
        resources = AttemptResources("attempt", client)
        self.bind(resources)
        binding = resources.image_bindings[self.IMAGE]
        labels = {ATTEMPT_LABEL: "attempt", INVOCATION_LABEL: "invocation", IMAGE_LABEL: self.IMAGE, IMAGE_ID_LABEL: self.IMAGE_ID}  # fmt: skip
        payload = {"Id": container_id, "Name": "/attempt-job", "Image": self.IMAGE_ID, "Config": {"Image": self.IMAGE_ID, "Labels": labels}}  # fmt: skip
        client.run.side_effect = [container_id + "\n", json.dumps(payload)]
        resources._recover_container("invocation", binding, "attempt-job", False)
        self.assertEqual(resources.container_names["attempt-job"], container_id)

    def test_bounded_capture_terminates_at_output_cap(self) -> None:
        client = object.__new__(DockerClientBoundary)
        client.binary = Path(sys.executable)
        client.environment = {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
        }
        client.deadline = time.monotonic() + 30
        client.cleanup_deadline = None
        client.max_output_bytes = 1024
        script = "import os,time;os.write(1,b'x'*8192);time.sleep(30)"
        with self.assertRaisesRegex(AssertionError, "stdout exceeded"):
            client._raw_result("-c", script)
        stuck = mock.Mock(pid=42)
        stuck.poll.return_value = None
        stuck.wait.side_effect = subprocess.TimeoutExpired([], 1)
        with mock.patch("os.killpg"), self.assertRaises(RuntimeError):
            client._terminate_process_group(stuck, time.monotonic() + 0.01)
        self.assertLessEqual(stuck.wait.call_args.kwargs["timeout"], 0.01)

    def test_fixed_client_rechecks_binary_socket_daemon_and_minimal_env(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            binary = root / "docker"
            endpoint = root / "docker.sock"
            config = root / "config"
            binary.write_bytes(b"fixture")
            binary.chmod(0o755)
            config.mkdir(mode=0o700)
            results = [self.completed(0, value) for value in ("daemon", "daemon", "items", "daemon")] + [self.completed(7), self.completed(0, "daemon"), self.completed(8), self.completed(9)]  # fmt: skip
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(str(endpoint))
                with mock.patch.object(
                    DockerClientBoundary, "_raw_result", side_effect=results
                ):
                    client = DockerClientBoundary(
                        binary=binary,
                        socket_path=endpoint,
                        config_dir=config,
                        deadline_seconds=30,
                    )
                    self.assertEqual(client.run("ps"), "items")
                    self.assertEqual(client.run_result("inspect").returncode, 7)
                    client.begin_cleanup()
                    self.assertEqual((client.run_result("one").returncode, client.run_result("two").returncode), (8, 9))  # fmt: skip
        self.assertEqual(
            set(client.environment),
            {"DOCKER_CONFIG", "DOCKER_HOST", "LANG", "LC_ALL", "PATH"},
        )
        self.assertLessEqual(client._remaining_timeout(), CLEANUP_CALL_SECONDS)
