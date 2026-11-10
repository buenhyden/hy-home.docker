#!/usr/bin/env python3
"""Prepare the verified public material directory for the owned OpenBao build.

Writes a new mode-0700 ``/tmp/hyhome-p01-owned-build-<UTC>/`` tree (refuses an
existing one), fetches only approved public hosts, authenticates every input and
prints the new pins. It never builds, never touches HOME, never reads secrets.
Procedure and doc sources: infra/03-security/openbao/build/README.md.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
import zlib
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
BUILD = REPOSITORY / "infra/03-security/openbao/build"
ROOT_PREFIX = "/tmp/hyhome-p01-owned-build-"

# Approved one-time public fetch (infra/supply-chain.network-approvals.md).
HOSTS = {"github.com", "dl-cdn.alpinelinux.org", "alpinelinux.org"}
# GitHub serves release assets from its own CDN after a github.com redirect.
REDIRECT_SUFFIX = ".githubusercontent.com"
MIRROR = "https://dl-cdn.alpinelinux.org/alpine/v3.24"

# Pinned by tool-images.json (cosign v3.1.3 linux/amd64 digest).
COSIGN = "gcr.io/projectsigstore/cosign@sha256:9e5c2f2edc34351160407ca3416c61855bdf9403c3c5936e0f0be7fc261611b8"
GITHUB_ISSUER = "https://token.actions.githubusercontent.com"
# Official docs, not read from the certificate under test:
# https://openbao.org/docs/install/#cosign
#   (github.com/openbao/openbao website/content/docs/install.mdx @ v2.7.1)
OPENBAO_IDENTITY_REGEXP = "^https://github.com/openbao/openbao/.github/workflows/release.yml@refs/heads/(main|release/.+)$"
# https://edu.chainguard.dev/chainguard/containers/security-and-compliance/verifying-chainguard-images-and-metadata-signatures-with-cosign/
#   (github.com/chainguard-dev/edu, "Public registry" section)
CHAINGUARD_IDENTITY = "https://github.com/chainguard-images/images/.github/workflows/release.yaml@refs/heads/main"
DOCS = {
    "source_checksums": "https://openbao.org/docs/install/#cosign",
    "builder": "https://edu.chainguard.dev/chainguard/containers/security-and-compliance/verifying-chainguard-images-and-metadata-signatures-with-cosign/",
}
APPROVALS = REPOSITORY / "infra/supply-chain.network-approvals.md"
APPROVAL_LINE = "OpenBao material network approval: confirmed"
DOCKER = "/usr/bin/docker"
SOCKET = "unix:///var/run/docker.sock"
OUTPUT_LIMIT = 8 * 1024**2


class Blocked(Exception):
    """A material input could not be authenticated; nothing is worked around."""


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


# ---- bounded public fetch -------------------------------------------------


class _Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl, redirect=True)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check_url(url: str, *, redirect: bool = False) -> None:
    parts = urllib.parse.urlsplit(url)
    host = parts.hostname or ""
    if parts.scheme != "https" or parts.username or parts.password:
        raise Blocked("fetch-scheme")
    if host not in HOSTS and not (redirect and host.endswith(REDIRECT_SUFFIX)):
        raise Blocked(f"fetch-host-not-approved:{host}")


def fetch(url: str, target: Path, limit: int) -> str:
    """Download one https file with an exclusive create; return its sha256."""
    check_url(url)
    opener = urllib.request.build_opener(_Redirects)
    request = urllib.request.Request(
        url, headers={"User-Agent": "hy-home-material-prep"}
    )
    digest, size = hashlib.sha256(), 0
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "wb") as out, opener.open(request, timeout=120) as response:
        while block := response.read(1024**2):
            size += len(block)
            if size > limit:
                raise Blocked("fetch-over-bound")
            digest.update(block)
            out.write(block)
    return digest.hexdigest()


# ---- APK index, closure and RSA signatures --------------------------------


def gzip_members(raw: bytes) -> list[tuple[bytes, bytes]]:
    """Split concatenated gzip streams into (raw member, decompressed) pairs."""
    members = []
    while raw:
        stream = zlib.decompressobj(31)
        data = stream.decompress(raw)
        used = len(raw) - len(stream.unused_data)
        if not stream.eof or used == 0:
            raise Blocked("gzip-member-invalid")
        members.append((raw[:used], data))
        raw = stream.unused_data
    return members


def verify_datahash(segments: list) -> None:
    """Bind the data segment to the signed control: APK v2 signs only the control,
    whose .PKGINFO ``datahash`` is the sha256 of the compressed data stream."""
    if len(segments) != 3:
        raise Blocked("apk-segment-count")
    control = tarfile.open(fileobj=BytesIO(segments[1][1]))
    try:
        info = control.extractfile(".PKGINFO").read().decode()
    except (KeyError, AttributeError) as error:
        raise Blocked("apk-pkginfo-missing") from error
    values = [
        line.split("=", 1)[1].strip()
        for line in info.splitlines()
        if line.split("=", 1)[0].strip() == "datahash"
    ]
    if len(values) != 1 or values[0] != hashlib.sha256(segments[2][0]).hexdigest():
        raise Blocked("apk-datahash-mismatch")


def verify_rsa(
    scratch: Path, key: Path, key_name: str, segments: list, signed: int
) -> None:
    """Check the leading ``.SIGN.RSA[256].<key>`` member against segments[signed]."""
    tar = tarfile.open(fileobj=BytesIO(segments[0][1]))
    names = tar.getnames()
    algorithms = {".SIGN.RSA." + key_name: "sha1", ".SIGN.RSA256." + key_name: "sha256"}
    if len(names) != 1 or names[0] not in algorithms:
        raise Blocked("signature-key-name-mismatch")
    algorithm = algorithms[names[0]]
    (scratch / "sig").write_bytes(tar.extractfile(names[0]).read())
    (scratch / "signed").write_bytes(segments[signed][0])
    result = subprocess.run(
        [
            "openssl",
            "dgst",
            f"-{algorithm}",
            "-verify",
            str(key),
            "-signature",
            str(scratch / "sig"),
            str(scratch / "signed"),
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode or b"Verified OK" not in result.stdout:
        raise Blocked("rsa-signature-invalid")


def parse_index(text: str, repository: str) -> dict:
    packages = {}
    for block in text.strip().split("\n\n"):
        row = dict(line.split(":", 1) for line in block.splitlines() if ":" in line)
        row["repository"] = repository
        if row["P"] in packages:
            packages[row["P"]]["_duplicate"] = "1"  # refused only if actually selected
            continue
        packages[row["P"]] = row
    return packages


def _name(token: str) -> str:
    return re.split(r"[<>=~]", token, maxsplit=1)[0]


def resolve_closure(packages: dict, requested) -> list[dict]:
    """Transitive dependency closure; a provider choice must be unambiguous."""
    provides = {}
    for row in packages.values():
        for token in [row["P"], *row.get("p", "").split()]:
            provides.setdefault(_name(token), set()).add(row["P"])
    chosen, queue = {}, list(requested)
    while True:
        while queue:
            name = queue.pop()
            candidates = provides.get(_name(name), set())
            if _name(name) in packages:
                pick = _name(name)
            elif len(candidates) == 1:
                pick = next(iter(candidates))
            elif candidates & chosen.keys():
                pick = sorted(candidates & chosen.keys())[0]
            else:
                ranked = sorted(
                    candidates, key=lambda p: -int(packages[p].get("k", "0"))
                )
                if not ranked or (
                    len(ranked) > 1
                    and packages[ranked[0]].get("k") == packages[ranked[1]].get("k")
                ):
                    raise Blocked(f"dependency-provider-ambiguous:{name}")
                pick = ranked[0]
            if pick in chosen:
                continue
            if "_duplicate" in packages[pick]:
                raise Blocked(f"selected-package-has-several-versions:{pick}")
            chosen[pick] = packages[pick]
            queue += [
                t for t in packages[pick].get("D", "").split() if not t.startswith("!")
            ]
        have = {
            _name(t) for r in chosen.values() for t in [r["P"], *r.get("p", "").split()]
        }
        # apk also installs packages whose every install_if condition is already met
        queue = [
            n
            for n, r in packages.items()
            if n not in chosen
            and r.get("i")
            and all(_name(t) in have for t in r["i"].split())
        ]
        if not queue:
            break
    return [
        chosen[name]
        for name in sorted(chosen, key=lambda n: f"{n}-{chosen[n]['V']}.apk")
    ]


def closure_row(row: dict, raw: bytes, segments: list) -> dict:
    control = "Q1" + base64.b64encode(hashlib.sha1(segments[1][0]).digest()).decode()
    if (
        len(segments) != 3
        or control != row["C"]
        or len(raw) != int(row["S"])
        or row["A"] not in {"x86_64", "noarch"}
    ):
        raise Blocked(f"apk-index-mismatch:{row['P']}")
    return {
        "filename": f"{row['P']}-{row['V']}.apk",
        "name": row["P"],
        "version": row["V"],
        "architecture": row["A"],
        "repository": row["repository"],
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "index_control_checksum": row["C"],
    }


# ---- bounded cosign container ---------------------------------------------


class Docker:
    """Exact reviewed docker binary, new empty client config, minimal env."""

    def __init__(self, config: Path):
        config.mkdir(mode=0o700)
        self.base = [DOCKER, "--host", SOCKET, "--config", str(config)]
        self.environment = {"PATH": "/usr/bin:/bin", "HOME": str(config)}

    def run(self, args, timeout=30):
        return subprocess.run(
            self.base + args,
            env=self.environment,
            capture_output=True,
            timeout=timeout,
            check=False,
        )

    def container(self, image, command, mounts, *, env, network, limits, timeout):
        """create -> start --attach -> exact-id rm; returns (exit, stdout, stderr)."""
        args = [
            "create",
            "--pull",
            "never",
            "--network",
            network,
            *limits,
            "--tmpfs",
            "/tmp:rw,nosuid,nodev,noexec,size=16m,mode=1777",
        ]
        for source, target, readonly in mounts:
            args += [
                "--mount",
                f"type=bind,src={source},dst={target}"
                + (",readonly" if readonly else ""),
            ]
        for key, value in env.items():
            args += ["--env", f"{key}={value}"]
        created = self.run([*args, image, *command])
        cid = created.stdout.decode().strip()
        if created.returncode or not re.fullmatch("[0-9a-f]{64}", cid):
            raise Blocked("container-create-failed")
        try:
            inspect = json.loads(self.run(["inspect", cid]).stdout)[0]
            if {m["Destination"] for m in inspect["Mounts"]} != {
                t for _, t, _ in mounts
            } or (inspect["Config"].get("Volumes")):
                raise Blocked("container-unexpected-mount")
            try:
                result = self.run(["start", "--attach", cid], timeout=timeout)
            except subprocess.TimeoutExpired as error:
                raise Blocked("container-timeout") from error
            if len(result.stdout) + len(result.stderr) > OUTPUT_LIMIT:
                raise Blocked("container-output-over-bound")
            state = json.loads(
                self.run(["inspect", "--format", "{{json .State}}", cid]).stdout
            )
            if state["OOMKilled"]:
                raise Blocked("container-oom")
            return state["ExitCode"], result.stdout, result.stderr
        finally:
            self.run(["rm", "--force", cid])


COSIGN_LIMITS = [
    "--user",
    "65532:65532",
    "--read-only",
    "--cap-drop",
    "ALL",
    "--security-opt",
    "no-new-privileges",
    "--memory",
    "512m",
    "--memory-swap",
    "512m",
    "--cpus",
    "1",
    "--pids-limit",
    "32",
]


def cosign(docker: Docker, arguments, mounts=()):
    """One keyless cosign call on the default bridge: no socket/auth/HOME mounts."""
    code, out, _ = docker.container(
        COSIGN,
        arguments,
        mounts,
        env={"HOME": "/tmp"},
        network="bridge",
        limits=COSIGN_LIMITS,
        timeout=150,
    )
    if code:
        raise Blocked("cosign-verification-failed")
    return out


def write_receipt(proof: Path, label: str, document: dict) -> str:
    raw = (
        json.dumps(
            {"status": "PASS", "exit": 0, **document, "verified_at": utc_now()},
            indent=2,
            sort_keys=True,
        ).encode()
        + b"\n"
    )
    path = proof / f"{label}-receipt.json"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as out:
        out.write(raw)
    return hashlib.sha256(raw).hexdigest()


def source_receipt(docker: Docker, proof: Path, inputs: dict) -> str:
    # the pinned release assets
    release = inputs["source_archive_url"].rsplit("/", 1)[0]
    for name in ("checksums.txt", "checksums.txt.sigstore.json"):
        fetch(f"{release}/{name}", proof / name, 4 * 1024**2)
    arguments = [
        "verify-blob",
        "--bundle",
        "/in/checksums.txt.sigstore.json",
        f"--certificate-oidc-issuer={GITHUB_ISSUER}",
        f"--certificate-identity-regexp={OPENBAO_IDENTITY_REGEXP}",
        "/in/checksums.txt",
    ]
    cosign(docker, arguments, [(proof, "/in", True)])
    archive = inputs["source_archive_url"].rsplit("/", 1)[1]
    line = f"{inputs['source_archive_sha256']}  {archive}"
    if line not in (proof / "checksums.txt").read_text().splitlines():
        raise Blocked("checksums-do-not-list-pinned-archive")
    digests = {
        name: hashlib.sha256((proof / name).read_bytes()).hexdigest()
        for name in ("checksums.txt", "checksums.txt.sigstore.json", "source.tar.xz")
    }
    return write_receipt(
        proof,
        "source_checksums",
        {
            "command": ["cosign", *arguments],
            "cosign_image": COSIGN,
            "identity_regexp": OPENBAO_IDENTITY_REGEXP,
            "issuer": GITHUB_ISSUER,
            "documentation": DOCS["source_checksums"],
            "checksums_line": line,
            "subject_digests": digests,
        },
    )


def builder_receipt(docker: Docker, proof: Path, inputs: dict) -> str:
    repository = inputs["builder"].split("@")[0]
    seen = {}
    for role in ("builder_index", "builder"):
        digest = inputs[role] if role == "builder_index" else inputs[role].split("@")[1]
        reference = f"{repository}@{digest}"
        arguments = [
            "verify",
            f"--certificate-oidc-issuer={GITHUB_ISSUER}",
            f"--certificate-identity={CHAINGUARD_IDENTITY}",
            reference,
        ]
        payload = json.loads(cosign(docker, arguments).splitlines()[-1])
        signed = {row["critical"]["image"]["docker-manifest-digest"] for row in payload}
        if signed != {digest}:
            raise Blocked("builder-signed-digest-mismatch")
        seen[role] = {
            "reference": reference,
            "command": ["cosign", *arguments],
            "signed_digests": sorted(signed),
        }
    return write_receipt(
        proof,
        "builder",
        {
            "cosign_image": COSIGN,
            "identity": CHAINGUARD_IDENTITY,
            "issuer": GITHUB_ISSUER,
            "documentation": DOCS["builder"],
            "subject_digests": seen,
        },
    )


# ---- source tree, modules, manifests --------------------------------------


def extract_source(archive: Path, target: Path, patch: Path) -> dict:
    """Extract the dist (regular files/dirs only), apply the reviewed patch."""
    omitted = []
    target.mkdir(mode=0o755)
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        prefix = members[0].name.split("/", 1)[0]
        if (
            len({m.name for m in members}) != len(members)
            or sum(m.size for m in members) > 4 * 1024**3
        ):
            raise Blocked("source-archive-duplicate-or-size")
        for member in members:
            parts = Path(member.name).parts
            if parts[0] != prefix or ".." in parts or member.name.startswith("/"):
                raise Blocked("source-archive-path")
            if len(parts) == 1:
                continue
            path = target.joinpath(*parts[1:])
            if member.isdir():
                path.mkdir(mode=0o755, exist_ok=True)
            elif member.isfile():
                path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
                fd = os.open(
                    path,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o755 if member.mode & 0o111 else 0o644,
                )
                with os.fdopen(fd, "wb") as out:
                    shutil.copyfileobj(tar.extractfile(member), out)
            elif member.issym():
                omitted.append(
                    member.name.removeprefix(prefix + "/")
                )  # file_manifest refuses symlinks
            else:
                raise Blocked("source-archive-member-kind")
    subprocess.run(
        [
            "patch",
            "-p1",
            "--no-backup-if-mismatch",
            "-d",
            str(target),
            "-i",
            str(patch),
        ],
        check=True,
        capture_output=True,
    )
    return {"omitted_symlinks": sorted(omitted)}


GO_ENV = {
    "GOENV": "off",
    "GOWORK": "off",
    "GOTOOLCHAIN": "local",
    "CGO_ENABLED": "0",
    "GOFLAGS": "-mod=mod",
    "GOPATH": "/tmp/go",
    "GOMODCACHE": "/modules",
    "GOCACHE": "/tmp/gocache",
    "GOPRIVATE": "",
    "GONOSUMDB": "",
    "GONOPROXY": "",
    "GOINSECURE": "",
    "HOME": "/tmp",
    "GOSUMDB": "sum.golang.org",
}
GO_LIMITS = [
    "--user",
    "1000:1000",
    "--read-only",
    "--cap-drop",
    "ALL",
    "--security-opt",
    "no-new-privileges",
    "--memory",
    "2g",
    "--memory-swap",
    "2g",
    "--cpus",
    "1",
    "--pids-limit",
    "64",
    "--workdir",
    "/src",
    "--entrypoint",
    "/bin/sh",
]


def prepare_modules(docker: Docker, inputs: dict, material: Path) -> None:
    """Download the module cache (bridge), then prove it offline (network none)."""
    modules = material / "modules"
    modules.mkdir(mode=0o755)
    steps = (
        # only the download step may write the cache; go.sum must already be complete
        ("bridge", "https://proxy.golang.org", "go mod download", False),
        # the build mounts the cache read-only: extracted trees must already exist
        (
            "none",
            "off",
            "go mod verify && go list -mod=readonly -tags=ui -deps . >/dev/null",
            True,
        ),
    )
    for network, proxy, command, readonly in steps:
        code, _, _ = docker.container(
            inputs["builder"],
            ["-ec", command],
            [(material / "source", "/src", True), (modules, "/modules", readonly)],
            env={**GO_ENV, "GOPROXY": proxy},
            network=network,
            limits=GO_LIMITS,
            timeout=900,
        )
        if code:
            raise Blocked("module-step-failed:" + command.split()[1])


# ---- orchestration --------------------------------------------------------


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "owned_openbao_build",
        REPOSITORY / "infra/03-security/openbao/scripts/build-owned-image.py",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_materials(builder, material: Path, inputs: dict, extra: dict) -> str:
    """Write materials.json in the exact shape ``materials()`` accepts."""
    document = {
        "source_archive_sha256": inputs["source_archive_sha256"],
        "go_patch_sha256": inputs["go_patch_sha256"],
        "offline_module_verification": "PASS",
        "signed_apk_verification": "PASS",
        "go_mod_sha256": hashlib.sha256(
            (material / "source/go.mod").read_bytes()
        ).hexdigest(),
        "go_sum_sha256": hashlib.sha256(
            (material / "source/go.sum").read_bytes()
        ).hexdigest(),
        **extra,
    }
    for name in ("source", "modules", "apks", "keys", "proof"):
        document[name + "_files"] = builder.file_manifest(material / name)
    builder.exclusive_json(material / "materials.json", document)
    return hashlib.sha256((material / "materials.json").read_bytes()).hexdigest()


def require_approval(path: Path = APPROVALS) -> None:
    if APPROVAL_LINE not in path.read_text().splitlines():
        raise Blocked("network-approval-line-missing")


def prepare(root: Path, *, allow_go_proxy: bool) -> dict:
    require_approval()
    builder = load_builder()
    inputs = json.loads((BUILD / "build-inputs.json").read_text())
    if (
        hashlib.sha256((BUILD / "go-modules.patch").read_bytes()).hexdigest()
        != inputs["go_patch_sha256"]
    ):
        raise Blocked("go-patch-pin-mismatch")
    if not str(root).startswith(ROOT_PREFIX) or ".." in root.parts:
        raise Blocked("root-outside-owned-build-scratch")
    os.mkdir(root, 0o700)  # refuses an existing directory
    material, scratch = root / "materials", root / "scratch"
    for path in (material, scratch):
        path.mkdir(mode=0o700)
    for name in ("apks", "keys", "proof"):
        (material / name).mkdir(mode=0o755)
    proof = material / "proof"
    docker = Docker(scratch / "docker-config")

    # 1. independently pinned Alpine key, source archive, signed indexes
    key_name = inputs["alpine_key_url"].rsplit("/", 1)[1]
    key = material / "keys" / key_name
    if fetch(inputs["alpine_key_url"], key, 65536) != inputs["alpine_key_sha256"]:
        raise Blocked("alpine-key-pin-mismatch")
    if (
        fetch(inputs["source_archive_url"], proof / "source.tar.xz", 128 * 1024**2)
        != inputs["source_archive_sha256"]
    ):
        raise Blocked("source-archive-pin-mismatch")
    packages, indexes = {}, {}
    for repository in ("main", "community"):
        target = proof / f"{repository}-APKINDEX.tar.gz"
        indexes[repository] = fetch(
            f"{MIRROR}/{repository}/x86_64/APKINDEX.tar.gz", target, 8 * 1024**2
        )
        segments = gzip_members(target.read_bytes())
        verify_rsa(scratch, key, key_name, segments, 1)
        archive = tarfile.open(fileobj=BytesIO(segments[1][1]))
        text = archive.extractfile("APKINDEX").read().decode()
        for name, row in parse_index(text, repository).items():
            if name in packages:
                raise Blocked("index-package-in-both-repositories")
            packages[name] = row

    # 2. publisher receipts (cosign, bounded container)
    pins = {"apk_indexes": indexes}
    pins["publisher_receipts"] = {
        "builder": builder_receipt(docker, proof, inputs),
        "source_checksums": source_receipt(docker, proof, inputs),
    }

    # 3. APK closure: the same requested names against the current signed index
    requested = {name: packages[name]["V"] for name in inputs["apk_requested"]}
    rows = []
    for row in resolve_closure(packages, requested):
        filename = f"{row['P']}-{row['V']}.apk"
        target = material / "apks" / filename
        fetch(f"{MIRROR}/{row['repository']}/x86_64/{filename}", target, 64 * 1024**2)
        raw = target.read_bytes()
        segments = gzip_members(raw)
        verify_rsa(scratch, key, key_name, segments, 1)
        verify_datahash(segments)
        rows.append(closure_row(row, raw, segments))
    pins.update(apk_requested=requested, apk_closure=rows)

    # 4. source with the reviewed patch, then the Go module cache
    extra = extract_source(
        proof / "source.tar.xz", material / "source", BUILD / "go-modules.patch"
    )
    if not allow_go_proxy:
        return {
            "status": "BLOCKED",
            "reason": "go-module-proxy-not-approved",
            "root": str(root),
            "pins": pins,
            **extra,
        }
    prepare_modules(docker, inputs, material)

    sha = write_materials(builder, material, inputs, extra)
    shutil.rmtree(scratch)
    return {
        "status": "PASS",
        "materials_directory": str(material),
        "materials_sha256": sha,
        "pins": pins,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(ROOT_PREFIX + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")),
        help="new directory under /tmp/hyhome-p01-owned-build-*",
    )
    parser.add_argument(
        "--allow-go-proxy",
        action="store_true",
        help="permit proxy.golang.org module download (needs its own approval)",
    )
    args = parser.parse_args(argv)
    try:
        result = prepare(args.root, allow_go_proxy=args.allow_go_proxy)
    except (
        Blocked,
        OSError,
        ValueError,
        KeyError,
        subprocess.SubprocessError,
    ) as error:
        print(
            json.dumps({"status": "FAIL", "failure": f"{type(error).__name__}:{error}"})
        )
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
