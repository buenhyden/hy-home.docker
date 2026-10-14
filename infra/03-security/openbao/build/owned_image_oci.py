"""Deterministically package only an admitted public OpenBao runtime export."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import shlex
import stat
import tarfile
from pathlib import Path, PurePosixPath


class InvalidImage(Exception):
    """The selected public image boundary failed; payloads stay private."""


# Safe defaults refuse material access outside the selected verified loader.
Blocked = InvalidImage
SELECTION = {}


def read_regular(*args, **kwargs):
    raise InvalidImage("selected-loader-required")


def require_hash(*args, **kwargs):
    raise InvalidImage("selected-loader-required")


# Docker reconstructs these transient files for every running container.
TRANSIENT = {".dockerenv", "etc/hosts", "etc/hostname", "etc/resolv.conf"}
TOPS = {
    "bin",
    "dev",
    "etc",
    "home",
    "lib",
    "licenses",
    "media",
    "mnt",
    "lib64",
    "openbao",
    "opt",
    "proc",
    "root",
    "run",
    "sbin",
    "srv",
    "sys",
    "tmp",
    "usr",
    "var",
    "public",
}


def copy_command(value: str) -> str:
    fields = shlex.split(value)
    permitted = {
        ("--chmod=555", "bao", "/usr/bin/bao"),
        ("--chmod=755", "docker-entrypoint.sh", "/usr/local/bin/docker-entrypoint.sh"),
        ("--chmod=644", "LICENSE", "/licenses/mozilla.txt"),
    }
    if tuple(fields) not in permitted:
        raise InvalidImage("unsupported-copy")
    mode, source, target = fields
    return (
        f"mkdir -p {shlex.quote(posixpath.dirname(target))}; "
        f"cp /public/{source} {target}; chmod {mode[8:]} {target}"
    )


def runtime_recipe(text: str, image: str) -> tuple[str, dict]:
    """Only this OpenBao recipe's opcodes and public mounts are supported."""
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    ops = [
        (line.split(" ", 1)[0], line.split(" ", 1)[1]) for line in lines if " " in line
    ]
    if len(ops) != len(lines) or not ops or ops[0] != ("FROM", image):
        raise InvalidImage("recipe-base-or-syntax")
    commands, config = [], {"Labels": {}}
    copies = set()
    counts = {}
    for opcode, value in ops[1:]:
        counts[opcode] = counts.get(opcode, 0) + 1
        if opcode == "COPY":
            command = copy_command(value)
            if command in copies:
                raise InvalidImage("duplicate-recipe-copy")
            copies.add(command)
            commands.append(command)
        elif opcode == "RUN":
            mount = "--mount=type=bind,source=apks,target=/public/apks,readonly "
            if not value.startswith(mount) or "--allow-untrusted" in value:
                raise InvalidImage("unsupported-run-mount-or-trust")
            commands.append(value[len(mount) :])
        elif opcode == "LABEL":
            for entry in shlex.split(value):
                key, separator, label = entry.partition("=")
                if not separator or not key.startswith(
                    ("org.opencontainers.image.", "com.hyhome.")
                ):
                    raise InvalidImage("recipe-label")
                config["Labels"] = {**config["Labels"], key: label}
        elif opcode in {"ENTRYPOINT", "CMD"}:
            config[{"ENTRYPOINT": "Entrypoint", "CMD": "Cmd"}[opcode]] = json.loads(
                value
            )
        elif opcode == "ENV" and value.startswith("PATH="):
            config["Env"] = [value]
        elif opcode == "USER" and value == "openbao":
            config["User"] = value
        elif opcode == "EXPOSE" and value == "8200":
            config["ExposedPorts"] = {"8200/tcp": {}}
        else:
            raise InvalidImage("unsupported-recipe-opcode")
    expected = {
        "COPY": 3,
        "RUN": 1,
        "ENV": 1,
        "EXPOSE": 1,
        "USER": 1,
        "ENTRYPOINT": 1,
        "CMD": 1,
        "LABEL": 4,
    }
    if (
        counts != expected
        or config.get("Entrypoint") != ["docker-entrypoint.sh"]
        or config.get("Cmd") != ["server", "-dev", "-dev-no-store-token"]
    ):
        raise InvalidImage("recipe-configuration")
    return "; ".join(commands), {**config, "WorkingDir": "/"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024**2):
            value.update(block)
    return "sha256:" + value.hexdigest()


def normalized_name(raw: str) -> str:
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "\x00" in raw
        or "\\" in raw
        or any(ord(char) < 32 or ord(char) == 127 for char in raw)
        or not path.parts
    ):
        raise InvalidImage("export-path")
    return str(path)


def export_rows(archive: tarfile.TarFile, limit: int):
    members = archive.getmembers()
    if len(members) > 10000 or sum(m.size for m in members) > limit:
        raise InvalidImage("export-size-or-count")
    names = [normalized_name(m.name) for m in members]
    if len(names) != len(set(names)):
        raise InvalidImage("export-duplicate")
    rows = []
    for member, name in zip(members, names, strict=True):
        top = name.split("/", 1)[0]
        if top not in TOPS and name not in TRANSIENT:
            raise InvalidImage("export-unexpected-root")
        if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
            raise InvalidImage("export-special-member")
        if member.issym() or member.islnk():
            link = member.linkname
            if "\\\\" in link or any(
                ord(char) < 32 or ord(char) == 127 for char in link
            ):
                raise InvalidImage("export-link-escape")
            stack = (
                [] if link.startswith("/") or member.islnk() else name.split("/")[:-1]
            )
            for component in link.split("/"):
                if component in {"", "."}:
                    continue
                if component == "..":
                    if not stack:
                        raise InvalidImage("export-link-escape")
                    stack.pop()
                else:
                    stack.append(component)
        if any("security.capability" in key for key in member.pax_headers):
            raise InvalidImage("unexpected-file-capability")
        if (
            name.startswith("public/")
            and member.isfile()
            and member.size == 0
            and name in {"public/bao", "public/LICENSE", "public/docker-entrypoint.sh"}
        ):
            continue
        if name.startswith(("root/", "public/")) and not member.isdir():
            raise InvalidImage("export-private-or-mounted-content")
        if name in TRANSIENT or top == "public":
            continue
        rows.append((name, member))
    return tuple(sorted(rows, key=lambda pair: pair[0]))


def canonical_layer(source: Path, target: Path, epoch: int, limit: int) -> str:
    """One held export, sorted headers, fixed times; preserve actual numeric modes."""
    try:
        fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, "rb") as held:
            before = os.fstat(held.fileno())
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_uid != os.getuid()
                or before.st_nlink != 1
                or before.st_size > limit
            ):
                raise InvalidImage("export-file-metadata")
            with tarfile.open(fileobj=held, mode="r:*") as incoming:
                rows = export_rows(incoming, limit)
                output = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(output, "wb") as stream:
                    with tarfile.open(
                        fileobj=stream, mode="w", format=tarfile.PAX_FORMAT
                    ) as out:
                        for name, member in rows:
                            item = tarfile.TarInfo(name)
                            for field in (
                                "mode",
                                "uid",
                                "gid",
                                "size",
                                "type",
                                "linkname",
                            ):
                                setattr(item, field, getattr(member, field))
                            item.mtime = epoch
                            out.addfile(
                                item,
                                incoming.extractfile(member)
                                if member.isfile()
                                else None,
                            )
            after = os.fstat(held.fileno())
            fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
            if any(getattr(before, key) != getattr(after, key) for key in fields):
                raise InvalidImage("export-changed")
        if target.stat().st_size > limit:
            raise InvalidImage("canonical-layer-over-bound")
        return digest(target)
    except (OSError, tarfile.TarError, ValueError) as error:
        raise InvalidImage("export-or-exclusive-output-invalid") from error


def json_bytes(document: dict) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def write_bytes(directory: Path, payload: bytes) -> dict:
    value = "sha256:" + hashlib.sha256(payload).hexdigest()
    with (directory / value[7:]).open("xb") as stream:
        stream.write(payload)
    return {"digest": value, "size": len(payload)}


def image_archive(
    layer: Path, directory: Path, configuration: dict, tag: str, epoch: int
) -> dict:
    """One uncompressed OCI layer; no arbitrary filesystem/context/provider API."""
    if not tag.startswith("hy-home/openbao:") or any(c.isspace() for c in tag):
        raise InvalidImage("owned-tag")
    directory.mkdir(mode=0o700)
    blobs = directory / "blobs/sha256"
    blobs.mkdir(parents=True, mode=0o700)
    layer_hash = digest(layer)
    destination = blobs / layer_hash[7:]
    with layer.open("rb") as source, destination.open("xb") as target:
        while block := source.read(1024**2):
            target.write(block)
    config = {**configuration, "rootfs": {"type": "layers", "diff_ids": [layer_hash]}}
    descriptor = write_bytes(blobs, json_bytes(config))
    manifest = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "config": {
            **descriptor,
            "mediaType": "application/vnd.oci.image.config.v1+json",
        },
        "layers": [
            {
                "digest": layer_hash,
                "size": layer.stat().st_size,
                "mediaType": "application/vnd.oci.image.layer.v1.tar",
            }
        ],
    }
    subject = write_bytes(blobs, json_bytes(manifest))
    index = {
        "schemaVersion": 2,
        "manifests": [
            {
                **subject,
                "mediaType": manifest["mediaType"],
                "platform": {"os": "linux", "architecture": "amd64"},
                "annotations": {
                    "org.opencontainers.image.ref.name": "docker.io/" + tag,
                    "io.containerd.image.name": "docker.io/"
                    + tag.split(":", 1)[0]
                    + "@"
                    + subject["digest"],
                },
            }
        ],
    }
    (directory / "index.json").write_bytes(json_bytes(index))
    (directory / "oci-layout").write_bytes(json_bytes({"imageLayoutVersion": "1.0.0"}))
    output = directory / "image.oci.tar"
    with output.open("xb") as stream, tarfile.open(fileobj=stream, mode="w") as archive:
        for path in sorted(
            p for p in directory.rglob("*") if p.is_file() and p != output
        ):
            item = tarfile.TarInfo(str(path.relative_to(directory)))
            item.size, item.mtime, item.mode = path.stat().st_size, epoch, 0o644
            with path.open("rb") as content:
                archive.addfile(item, content)
    return {
        "config": descriptor["digest"],
        "layers": [layer_hash],
        "manifest": subject["digest"],
        "archive": str(output),
    }


# Public source/cache ownership routines used only by the selected build.
def archive_members(path: Path, prefix: str, limit: int):
    """Inspect the whole authenticated archive before any extraction."""
    with tarfile.open(path) as archive:
        members = archive.getmembers()
    names = [member.name for member in members]
    if len(names) != len(set(names)) or len(names) > 100000:
        raise Blocked("archive-duplicate-or-count")
    if sum(member.size for member in members if member.isfile()) > limit:
        raise Blocked("archive-size")
    for member in members:
        name = PurePosixPath(member.name)
        if (
            name.is_absolute()
            or ".." in name.parts
            or not name.parts
            or name.parts[0] != prefix
            or "\x00" in member.name
            or not (member.isfile() or member.isdir())
        ):
            raise Blocked("archive-path-or-kind")
    return tuple(members)


def decode_json(payload: bytes):
    def pairs(items):
        result = dict(items)
        if len(result) != len(items):
            raise Blocked("duplicate-json-key")
        return result

    try:
        return json.loads(
            payload,
            object_pairs_hook=pairs,
            parse_constant=lambda _: (_ for _ in ()).throw(Blocked("nonfinite-json")),
        )
    except (ValueError, UnicodeError) as error:
        raise Blocked("invalid-json") from error


def private_directory(path: Path, *, create=False) -> Path:
    path = path.absolute()
    if ".." in path.parts or not (
        str(path).startswith("/tmp/hyhome-p01-selected-image-security-20261014/")
        or str(path).startswith("/tmp/hyhome-p01-owned-build-")
    ):
        raise Blocked("outside-owned-public-scratch")
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[1:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_fd
            if component.startswith("hyhome-p01-"):
                metadata = os.fstat(descriptor)
                if (
                    metadata.st_uid != os.getuid()
                    or metadata.st_gid != os.getgid()
                    or metadata.st_mode & 0o022
                ):
                    raise Blocked("scratch-parent-owner-or-mode")
        if create:
            os.mkdir(path.parts[-1], mode=0o700, dir_fd=descriptor)
        following = os.open(
            path.parts[-1],
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=descriptor,
        )
        os.close(descriptor)
        descriptor = following
        metadata = os.fstat(descriptor)
        if (
            metadata.st_uid != os.getuid()
            or metadata.st_gid != os.getgid()
            or metadata.st_mode & 0o077
        ):
            raise Blocked("scratch-owner-or-mode")
    except OSError as error:
        raise Blocked("scratch-unavailable") from error
    finally:
        os.close(descriptor)
    return path


def file_manifest(root: Path) -> list[dict]:
    if root.is_symlink() or not root.is_dir():
        raise Blocked("material-root-not-directory")
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise Blocked("material-symlink")
        if path.is_file():
            raw = read_regular(path, 256 * 1024**2, source=True)
            rows.append(
                {
                    "path": str(path.relative_to(root)),
                    "size": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
    if len(rows) > 100000 or sum(row["size"] for row in rows) > 6 * 1024**3:
        raise Blocked("material-count-or-size")
    return rows


def exclusive_json(path: Path, document: dict) -> None:
    raw = json.dumps(document, indent=2, sort_keys=True).encode() + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())
    path.chmod(0o400)


def module_delta(before: dict, after: dict) -> dict:
    """Only eight authenticated MVS version edges may change in the root module."""
    if {k: v for k, v in before.items() if k != "Require"} != {
        k: v for k, v in after.items() if k != "Require"
    }:
        raise Blocked("module-authority-changed")
    old, new = (
        {r["Path"]: r for r in document["Require"]} for document in (before, after)
    )
    if (
        len(old) != len(before["Require"])
        or len(new) != len(after["Require"])
        or set(old) != set(new)
    ):
        raise Blocked("module-rows-changed-or-duplicate")
    changed = {name for name in old if old[name] != new[name]}
    if changed != set(SELECTION):
        raise Blocked("unexpected-module-selection")
    for name in changed:
        if (old[name]["Version"], new[name]["Version"]) != SELECTION[name] or {
            k: v for k, v in old[name].items() if k != "Version"
        } != {k: v for k, v in new[name].items() if k != "Version"}:
            raise Blocked("unexpected-module-edge")
    return {name: new[name]["Version"] for name in sorted(changed)}


def materials(directory: Path, expected: str, inputs: dict) -> dict:
    directory = private_directory(directory)
    raw = read_regular(directory / "materials.json", 64 * 1024**2)
    require_hash(raw, expected)
    document = decode_json(raw)
    if (
        document.get("source_archive_sha256") != inputs["source_archive_sha256"]
        or document.get("go_patch_sha256") != inputs["go_patch_sha256"]
        or document.get("offline_module_verification") != "PASS"
        or document.get("signed_apk_verification") != "PASS"
    ):
        raise Blocked("material-provenance-incomplete")
    for name in ("source", "modules", "apks", "keys", "proof"):
        if file_manifest(directory / name) != document[name + "_files"]:
            raise Blocked("material-snapshot-mismatch")
    expected_apks = [
        {"path": row["filename"], "size": row["size"], "sha256": row["sha256"]}
        for row in inputs["apk_closure"]
    ]
    if document["apks_files"] != sorted(expected_apks, key=lambda row: row["path"]):
        raise Blocked("apk-closure-mismatch")
    key_rows = document["keys_files"]
    if len(key_rows) != 1 or key_rows[0]["sha256"] != inputs["alpine_key_sha256"]:
        raise Blocked("independent-alpine-key-mismatch")
    for label, expected_hash in inputs["publisher_receipts"].items():
        receipt = read_regular(directory / "proof" / (label + "-receipt.json"), 65536)
        require_hash(receipt, expected_hash)
        observed = decode_json(receipt)
        if observed.get("status") != "PASS" or observed.get("exit") != 0:
            raise Blocked("publisher-verification-not-pass")
    for label, expected_hash in inputs["apk_indexes"].items():
        require_hash(
            read_regular(
                directory / "proof" / (label + "-APKINDEX.tar.gz"), 8 * 1024**2
            ),
            expected_hash,
        )
    require_hash(
        read_regular(directory / "proof/source.tar.xz", 64 * 1024**2),
        inputs["source_archive_sha256"],
    )
    source = directory / "source"
    require_hash(
        read_regular(source / "go.mod", 1024**2, source=True), document["go_mod_sha256"]
    )
    require_hash(
        read_regular(source / "go.sum", 1024**2, source=True), document["go_sum_sha256"]
    )
    return document


def permitted_tmpfs_view(mounts):
    """Docker 29 prestart omits --tmpfs from Mounts; allow only its /tmp row."""
    other = [row for row in mounts if row["Type"] != "bind"]
    return not other or (
        len(other) == 1
        and other[0]["Type"] == "tmpfs"
        and other[0].get("Destination") == "/tmp"
        and other[0].get("Source", "") == ""
        and other[0].get("RW") is True
        and other[0].get("Mode", "")
        in {"", "rw,nosuid,nodev,noexec,size=128m,mode=1777"}
    )


def validate_created_boundary(row, phase, mounts):
    config = row["HostConfig"]
    memory, cpu, pids, user = (
        (4 * 1024**3, 2000000000, 128, "1000:1000")
        if phase == "compile"
        else (1024**3, 1000000000, 64, "0:0")
    )
    expected = {
        "Memory": memory,
        "MemorySwap": memory,
        "NanoCpus": cpu,
        "PidsLimit": pids,
        "NetworkMode": "none",
        "Privileged": False,
        "ReadonlyRootfs": phase == "compile",
        "Tmpfs": {"/tmp": "rw,nosuid,nodev,noexec,size=128m,mode=1777"},
    }
    caps = {str(value).removeprefix("CAP_") for value in config.get("CapAdd") or []}
    actual_mounts = {
        (value["Source"], value["Destination"], not value["RW"])
        for value in row["Mounts"]
        if value["Type"] == "bind"
    }
    if (
        any(config.get(key) != value for key, value in expected.items())
        or config.get("CapDrop") != ["ALL"]
        or caps != ({"CHOWN"} if phase == "runtime" else set())
        or row["Config"]["User"] != user
        or config.get("SecurityOpt")
        not in (["no-new-privileges"], ["no-new-privileges=true"])
        or actual_mounts
        != {(str(source), target, readonly) for source, target, readonly in mounts}
        or not permitted_tmpfs_view(row["Mounts"])
    ):
        raise Blocked("created-container-boundary-mismatch")
