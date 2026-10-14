#!/usr/bin/env python3
"""Prepare one public owned OpenBao build; native phases need exact admission."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import resource
import shutil
import stat
import struct
import subprocess
import time
import types
from datetime import UTC, datetime
from pathlib import Path


class Blocked(Exception):
    """A public material or execution boundary could not be established."""


SELECTION = {
    "golang.org/x/crypto": ("v0.56.0", "v0.57.0"),
    "golang.org/x/mod": ("v0.38.0", "v0.41.0"),
    "golang.org/x/net": ("v0.58.0", "v0.60.0"),
    "golang.org/x/sync": ("v0.22.0", "v0.23.0"),
    "golang.org/x/sys": ("v0.47.0", "v0.48.0"),
    "golang.org/x/term": ("v0.45.0", "v0.46.0"),
    "golang.org/x/text": ("v0.41.0", "v0.42.0"),
    "golang.org/x/tools": ("v0.48.0", "v0.49.0"),
}


def read_regular(path: Path, limit: int, *, source: bool = False) -> bytes:
    """Hold every no-follow path component and reject aliased/changing inputs."""
    parts = path.absolute().parts
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in parts[1:-1]:
            following = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=directory,
            )
            os.close(directory)
            directory = following
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        try:
            before = os.fstat(fd)
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_nlink != 1
                or before.st_uid != os.getuid()
                or before.st_gid != os.getgid()
                or before.st_size > limit
                or before.st_mode & (0o002 if source else 0o022)
            ):
                raise Blocked("public-file-metadata")
            with os.fdopen(fd, "rb", closefd=False) as stream:
                payload = stream.read(limit + 1)
            after = os.fstat(fd)
            fields = (
                "st_dev",
                "st_ino",
                "st_mode",
                "st_nlink",
                "st_uid",
                "st_gid",
                "st_size",
                "st_mtime_ns",
                "st_ctime_ns",
            )
            if (
                any(getattr(before, name) != getattr(after, name) for name in fields)
                or len(payload) > limit
            ):
                raise Blocked("public-file-changed")
            return payload
        finally:
            os.close(fd)
    except OSError as error:
        raise Blocked("public-file-unavailable") from error
    finally:
        os.close(directory)


def require_hash(payload: bytes, expected: str) -> None:
    if hashlib.sha256(payload).hexdigest() != expected:
        raise Blocked("material-digest-mismatch")


def container_limits(phase: str) -> list[str]:
    if phase not in {"compile", "prefetch", "runtime"}:
        raise Blocked("unknown-container-phase")
    if phase == "runtime":
        return [
            "--user",
            "0:0",
            "--cap-drop",
            "ALL",
            "--cap-add",
            "CHOWN",
            "--security-opt",
            "no-new-privileges",
            "--memory",
            "1g",
            "--memory-swap",
            "1g",
            "--cpus",
            "1",
            "--pids-limit",
            "64",
        ]
    memory, cpus, pids = ("4g", "2", "128") if phase == "compile" else ("2g", "1", "64")
    return [
        "--user",
        "1000:1000",
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--memory",
        memory,
        "--memory-swap",
        memory,
        "--cpus",
        cpus,
        "--pids-limit",
        pids,
    ]


def go_environment(*, offline: bool) -> dict[str, str]:
    return {
        "GOENV": "off",
        "GOWORK": "off",
        "GOTOOLCHAIN": "local",
        "GOMAXPROCS": "2" if offline else "1",
        "CGO_ENABLED": "0",
        "GOOS": "linux",
        "GOARCH": "amd64",
        "GOFLAGS": "",
        "GOPROXY": "off" if offline else "https://proxy.golang.org",
        "GOSUMDB": "sum.golang.org",
        "GOPRIVATE": "",
        "GONOSUMDB": "",
        "GONOPROXY": "",
        "GOINSECURE": "",
        "GOPATH": "/tmp/go",
        "GOMODCACHE": "/modules",
        "GOCACHE": "/cache",
        "HOME": "/tmp",
    }


def admit_resources(memory: int, disk: int) -> None:
    if memory < 12 * 1024**3 or disk < 32 * 1024**3:
        raise Blocked("insufficient-memory-or-disk-headroom")


def require_reproducible(first: dict, second: dict) -> None:
    required = {"binary", "config", "layers", "manifest"}
    if set(first) != required or set(second) != required or first != second:
        raise Blocked("reproducibility-mismatch")


_OCI_CACHE = None


def load_oci(build: Path):
    """Execute the held bytes covered by the frozen build-inputs digest."""
    global _OCI_CACHE
    payload = read_regular(build / "owned_image_oci.py", 1024**2, source=True)
    inputs = json.loads(read_regular(build / "build-inputs.json", 65536, source=True))
    require_hash(payload, inputs["oci_helper_sha256"])
    digest = hashlib.sha256(payload).hexdigest()
    if _OCI_CACHE is None or _OCI_CACHE[0] != digest:
        module = types.ModuleType("owned_openbao_oci")
        exec(
            compile(payload, str(build / "owned_image_oci.py"), "exec"), module.__dict__
        )
        module.Blocked, module.read_regular = Blocked, read_regular
        module.SELECTION, module.require_hash = SELECTION, require_hash
        _OCI_CACHE = (digest, module)
    return _OCI_CACHE[1]


def module_delta(before, after):
    return _public_materials().module_delta(before, after)


def materials(directory, expected, inputs):
    return _public_materials().materials(directory, expected, inputs)


def _public_materials():
    return load_oci(Path(__file__).resolve().parents[1] / "build")


def archive_members(path, prefix, limit):
    return _public_materials().archive_members(path, prefix, limit)


def decode_json(payload):
    return _public_materials().decode_json(payload)


def private_directory(path, *, create=False):
    return _public_materials().private_directory(path, create=create)


def file_manifest(root):
    return _public_materials().file_manifest(root)


def exclusive_json(path, document):
    return _public_materials().exclusive_json(path, document)


def current_packet(repository: Path) -> str:
    package = "infra/03-security/openbao/"
    names = [package + "scripts/build-owned-image.py"] + [
        package + "build/" + name
        for name in (
            "Dockerfile",
            "build-inputs.json",
            "go-modules.patch",
            "owned_image_oci.py",
            "README.md",
        )
    ]
    names += ["tests/validation/test_openbao_owned_image_contract.py"]
    value = hashlib.sha256()
    for name in sorted(names):
        value.update(
            name.encode()
            + b"\0"
            + read_regular(repository / name, 1024**2, source=True)
            + b"\0"
        )
    return value.hexdigest()


class LocalDocker:
    """Explicit host orchestration; containers never receive its socket/config."""

    def __init__(self, directory: Path):
        self.directory = private_directory(directory)
        self.config = directory / "docker-config"
        self.config.mkdir(mode=0o700)
        self.base = [
            "/usr/bin/docker",
            "--host",
            "unix:///var/run/docker.sock",
            "--config",
            str(self.config),
        ]
        self.environment = {
            "PATH": "/usr/bin:/bin",
            "HOME": str(directory),
            "DOCKER_CONFIG": str(self.config),
        }

    def captured(self, args: list[str], timeout=30):
        result = subprocess.run(
            self.base + args,
            env=self.environment,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        if (
            result.returncode
            or len(result.stdout) > 1024**2
            or len(result.stderr) > 1024**2
        ):
            raise Blocked("docker-command-failed")
        return result.stdout

    def image(self, reference: str) -> dict:
        row = decode_json(self.captured(["image", "inspect", reference]))[0]
        if (
            row["Os"] != "linux"
            or row["Architecture"] != "amd64"
            or row["Config"].get("Volumes")
            or row["Id"] != reference.rsplit("@", 1)[1]
        ):
            raise Blocked("image-platform-or-volume")
        return row

    def created_boundary(self, cid, phase, mounts):
        row = decode_json(self.captured(["inspect", cid]))[0]
        _public_materials().validate_created_boundary(row, phase, mounts)

    def admitted_mounts(self, phase, mounts):
        permitted = (
            {"/src", "/modules", "/out", "/cache"}
            if phase == "compile"
            else {
                "/public/apks",
                "/public/keys",
                "/public/bao",
                "/public/docker-entrypoint.sh",
                "/public/LICENSE",
            }
        )
        for source, target, readonly in mounts:
            absolute = str(source.absolute())
            if (
                target not in permitted
                or any(char in absolute for char in (",", "\n", "\x00"))
                or not absolute.startswith("/tmp/hyhome-p01-")
                or source.is_symlink()
                or not source.exists()
                or (phase == "runtime" and not readonly)
            ):
                raise Blocked("unadmitted-container-mount")

    def container(
        self, label, phase, image, command, mounts, environment, *, export=None
    ):
        self.admitted_mounts(phase, mounts)
        cid = None
        record = {"phase": label, "status": "FAIL", "network": "none"}
        started = time.monotonic()
        timeout = 2700 if phase == "compile" else 300
        args = [
            "create",
            "--pull",
            "never",
            "--network",
            "none",
            "--label",
            "com.hyhome.operation=p01-owned-rebuild",
            *container_limits(phase),
        ]
        args += ["--ulimit", "fsize=402653184:402653184"]
        args += ["--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=128m,mode=1777"]
        for source, target, readonly in mounts:
            args += [
                "--mount",
                f"type=bind,src={source},dst={target}"
                + (",readonly" if readonly else ""),
            ]
        for key, value in environment.items():
            args += ["--env", f"{key}={value}"]
        args += [
            "--workdir",
            "/src" if phase == "compile" else "/",
            "--entrypoint",
            "/bin/sh",
            image,
            "-ec",
            command,
        ]
        try:
            cid = self.captured(args).decode().strip()
            if not re.fullmatch("[0-9a-f]{64}", cid):
                raise Blocked("created-id-invalid")
            record = {**record, "created_id": cid}
            self.created_boundary(cid, phase, mounts)
            with (
                (self.directory / f"{label}.stdout").open("xb") as out,
                (self.directory / f"{label}.stderr").open("xb") as err,
            ):
                result = self.attached(cid, out, err, timeout)
            state = decode_json(
                self.captured(["inspect", "--format", "{{json .State}}", cid])
            )
            record = {
                **record,
                "client_exit": result.returncode,
                "container_exit": state["ExitCode"],
                "oom_killed": state["OOMKilled"],
            }
            if result.returncode or state["ExitCode"] or state["OOMKilled"]:
                raise Blocked("bounded-container-failed")
            if export:
                self.streamed(["export", cid], export, 512 * 1024**2, 300)
            record = {**record, "status": "PASS"}
        finally:
            if cid and re.fullmatch("[0-9a-f]{64}", cid):
                try:
                    self.captured(["rm", "--force", cid])
                    record = {**record, "cleanup": "exact-created-id-removed"}
                except (Blocked, subprocess.SubprocessError):
                    record = {**record, "status": "FAIL", "cleanup": "FAILED"}
            exclusive_json(
                self.directory / f"{label}-receipt.json",
                {
                    **record,
                    "argv": self.base + args,
                    "seconds": round(time.monotonic() - started, 3),
                    "finished_at": datetime.now(UTC).isoformat(),
                },
            )
            if record.get("cleanup") == "FAILED":
                raise Blocked("owned-container-cleanup-failed")

    def attached(self, cid, out, err, timeout):
        started = time.monotonic()
        process = subprocess.Popen(
            [*self.base, "start", "--attach", cid],
            env=self.environment,
            stdout=out,
            stderr=err,
            preexec_fn=lambda: resource.setrlimit(
                resource.RLIMIT_FSIZE, (8 * 1024**2,) * 2
            ),
        )
        try:
            while process.poll() is None:
                used = sum(
                    path.lstat().st_size
                    for path in self.directory.rglob("*")
                    if path.is_file() and not path.is_symlink()
                )
                if (
                    time.monotonic() - started > timeout
                    or used > 16 * 1024**3
                    or shutil.disk_usage(self.directory).free < 16 * 1024**3
                ):
                    raise Blocked("compile-time-or-scratch-budget")
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    continue
            return process
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)

    def streamed(self, args, target, limit, timeout):
        with (
            target.open("xb") as out,
            (target.parent / (target.name + ".stderr")).open("xb") as err,
        ):
            result = subprocess.run(
                self.base + args,
                env=self.environment,
                stdout=out,
                stderr=err,
                timeout=timeout,
                check=False,
                preexec_fn=lambda: resource.setrlimit(
                    resource.RLIMIT_FSIZE, (limit,) * 2
                ),
            )
        if result.returncode or target.stat().st_size > limit:
            raise Blocked("bounded-docker-stream-failed")


def build_inputs(build: Path) -> dict:
    inputs = decode_json(read_regular(build / "build-inputs.json", 65536, source=True))
    expected = {
        "schema_version": 1,
        "builder_version": "go1.27.2",
        "version": "2.7.1+hyhome.go1.27.2.net0.60.0.r1",
        "upstream_commit": "a5db72cef75c24b920ade02065b18dd8eb666bac",
        "source_archive_sha256": "6da0c07e61d8dfd2ab72ad47cb96691fb7abfecd460a55272545346575c37711",
        "builder": "cgr.dev/chainguard/go@sha256:69e74b89b97ff9775b9e2f7d235e65273556c88b814d3178a13acff8780aa940",
        "runtime": "docker.io/library/alpine@sha256:d56c381f961d307a21b3ca004cf1e3910f106644aefb1f43e654c8a56c4fd395",
        "tag": "hy-home/openbao:2.7.1-go1.27.2-net0.60.0-r1",
        "commit_date": "2026-10-01T13:32:54Z",
        "source_date_epoch": 1790861574,
    }
    if any(inputs.get(key) != value for key, value in expected.items()):
        raise Blocked("unreviewed-build-input")
    if inputs.get("modules") != {key: value[1] for key, value in SELECTION.items()}:
        raise Blocked("unreviewed-module-input")
    require_hash(
        read_regular(build / "Dockerfile", 65536, source=True), inputs["recipe_sha256"]
    )
    require_hash(
        read_regular(build / "go-modules.patch", 65536, source=True),
        inputs["go_patch_sha256"],
    )
    return inputs


def compile_command(inputs: dict) -> str:
    namespace = "github.com/openbao/openbao/v2/internal/version."
    flags = " ".join(
        f"-X {namespace}{key}={value}"
        for key, value in (
            ("fullVersion", "2.7.1"),
            ("VersionMetadata", "hyhome.go1.27.2.net0.60.0.r1"),
            ("GitCommit", inputs["upstream_commit"]),
            ("CommitDate", inputs["commit_date"]),
        )
    )
    return (
        "go mod verify; go build -p=2 -mod=readonly -trimpath -buildvcs=false "
        f"-tags=ui -ldflags '{flags}' -o /out/bao .; "
        "go version -m /out/bao > /out/build-info.txt"
    )


def verify_binary(path: Path, information: Path, inputs: dict) -> str:
    raw = read_regular(path, 384 * 1024**2, source=True)
    if (
        len(raw) < 64
        or raw[:6] != b"\x7fELF\x02\x01"
        or struct.unpack_from("<H", raw, 18)[0] != 62
    ):
        raise Blocked("binary-not-elf64-amd64")
    offset = struct.unpack_from("<Q", raw, 32)[0]
    size, count = struct.unpack_from("<HH", raw, 54)
    if (
        size < 4
        or offset + size * count > len(raw)
        or any(
            struct.unpack_from("<I", raw, offset + number * size)[0] == 3
            for number in range(count)
        )
    ):
        raise Blocked("binary-interpreter-or-header")
    info = read_regular(information, 1024**2, source=True).decode()
    if not info.splitlines()[0].endswith("go1.27.2"):
        raise Blocked("binary-compiler-version")
    selected = {
        parts[1]: parts[2]
        for line in info.splitlines()
        if len(parts := line.split()) >= 3 and parts[0] == "dep"
    }
    if selected.get("golang.org/x/net") != "v0.60.0" or any(
        selected.get(name, value) != value for name, value in inputs["modules"].items()
    ):
        raise Blocked("binary-module-selection")
    return hashlib.sha256(raw).hexdigest()


def host_headroom(directory: Path) -> None:
    memory = next(
        int(line.split()[1]) * 1024
        for line in Path("/proc/meminfo").read_text().splitlines()
        if line.startswith("MemAvailable:")
    )
    admit_resources(memory, shutil.disk_usage(directory).free)


def compile_pass(
    docker: LocalDocker, material: Path, output: Path, inputs: dict, number: int
) -> dict:
    output.mkdir(mode=0o700)
    cache = output / "cache"
    cache.mkdir(mode=0o700)
    (cache / "tmp").mkdir(mode=0o700)
    mounts = [
        (material / "source", "/src", True),
        (material / "modules", "/modules", True),
        (output, "/out", False),
        (cache, "/cache", False),
    ]
    docker.container(
        f"compile-{number}",
        "compile",
        inputs["builder"],
        compile_command(inputs),
        mounts,
        {
            **go_environment(offline=True),
            "GOTMPDIR": "/cache/tmp",
            "SOURCE_DATE_EPOCH": str(inputs["source_date_epoch"]),
        },
    )
    return {"binary": verify_binary(output / "bao", output / "build-info.txt", inputs)}


def runtime_pass(
    docker: LocalDocker,
    material: Path,
    output: Path,
    inputs: dict,
    recipe: str,
    oci,
    number: int,
    labels: dict,
) -> dict:
    command, config = oci.runtime_recipe(recipe, inputs["runtime"])
    config = {**config, "Labels": {**config["Labels"], **labels}}
    mounts = [
        (material / "apks", "/public/apks", True),
        (material / "keys", "/public/keys", True),
        (output / "bao", "/public/bao", True),
        (
            material / "source/.release/docker/docker-entrypoint.sh",
            "/public/docker-entrypoint.sh",
            True,
        ),
        (material / "source/LICENSE", "/public/LICENSE", True),
    ]
    raw_export = output / "runtime.export.tar"
    docker.container(
        f"runtime-{number}",
        "runtime",
        inputs["runtime"],
        command,
        mounts,
        {
            "PATH": config["Env"][0][5:],
            "SOURCE_DATE_EPOCH": str(inputs["source_date_epoch"]),
        },
        export=raw_export,
    )
    layer = output / "runtime.layer.tar"
    try:
        oci.canonical_layer(
            raw_export, layer, inputs["source_date_epoch"], 512 * 1024**2
        )
    except oci.InvalidImage as error:
        raise Blocked("public-runtime-export-invalid") from error
    configuration = {
        "architecture": "amd64",
        "os": "linux",
        "created": inputs["commit_date"],
        "config": config,
        "history": [
            {
                "created": inputs["commit_date"],
                "created_by": "hy-home owned OpenBao: fixed authenticated public inputs",
            }
        ],
    }
    return oci.image_archive(
        layer, output / "oci", configuration, inputs["tag"], inputs["source_date_epoch"]
    )


def run_build(
    material: Path,
    material_hash: str,
    output: Path,
    build: Path,
    inputs: dict,
    packet: str,
) -> dict:
    initial = materials(material, material_hash, inputs)
    output = private_directory(output, create=True)
    lock = os.open(
        material / ".build.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600
    )
    try:
        metadata = os.fstat(lock)
        if (
            metadata.st_uid != os.getuid()
            or metadata.st_nlink != 1
            or metadata.st_mode & 0o077
        ):
            raise Blocked("concurrency-lock-owner-or-mode")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        docker, oci = LocalDocker(output), load_oci(build)
        recipe = read_regular(build / "Dockerfile", 65536, source=True)
        require_hash(recipe, inputs["recipe_sha256"])
        for image in (inputs["builder"], inputs["runtime"]):
            docker.image(image)
        labels = {
            "com.hyhome.openbao.recipe_packet": packet,
            "com.hyhome.openbao.materials_sha256": material_hash,
            "com.hyhome.openbao.patch_sha256": inputs["go_patch_sha256"],
        }
        results = []
        for number in (1, 2):
            host_headroom(output)
            stage = output / f"pass-{number}"
            binary = compile_pass(docker, material, stage, inputs, number)
            if materials(material, material_hash, inputs) != initial:
                raise Blocked("compile-materials-changed")
            image = runtime_pass(
                docker,
                material,
                stage,
                inputs,
                recipe.decode(),
                oci,
                number,
                labels,
            )
            if materials(material, material_hash, inputs) != initial:
                raise Blocked("runtime-materials-changed")
            if current_packet(build.parents[3]) != packet:
                raise Blocked("build-source-changed")
            results.append(
                {
                    **binary,
                    **{key: image[key] for key in ("config", "layers", "manifest")},
                }
            )
        require_reproducible(*results)
        return {
            "status": "PASS",
            "reproducibility": "binary-and-complete-oci-identities-match",
            "identity": results[0],
            "source_packet": packet,
            "materials_sha256": material_hash,
            "archive": str(output / "pass-1/oci/image.oci.tar"),
            "HOME": "NOT_RUN",
        }
    finally:
        os.close(lock)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("plan", "build"), default="plan")
    parser.add_argument("--materials-directory", type=Path, required=True)
    parser.add_argument("--materials-sha256", required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--packet-sha256", required=True)
    args = parser.parse_args(argv)
    repository, build = (
        Path(__file__).resolve().parents[4],
        Path(__file__).resolve().parents[1] / "build",
    )
    try:
        packet, inputs = current_packet(repository), build_inputs(build)
        if packet != args.packet_sha256:
            raise Blocked("source-packet-mismatch")
        materials(args.materials_directory, args.materials_sha256, inputs)
        if args.phase == "plan":
            result = {
                "source_packet": packet,
                "compile_command": compile_command(inputs),
                "compile_limits": container_limits("compile"),
                "runtime_limits": container_limits("runtime"),
                "network": "none",
                "compile": "NOT_RUN",
                "image_load": "NOT_RUN",
                "HOME": "NOT_RUN",
            }
        else:
            result = run_build(
                args.materials_directory,
                args.materials_sha256,
                args.output_directory,
                build,
                inputs,
                packet,
            )
            exclusive_json(args.output_directory / "build-receipt.json", result)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (
        Blocked,
        OSError,
        ValueError,
        KeyError,
        subprocess.SubprocessError,
    ) as error:
        print(
            json.dumps(
                {"status": "FAIL", "failure": type(error).__name__, "HOME": "NOT_RUN"}
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
