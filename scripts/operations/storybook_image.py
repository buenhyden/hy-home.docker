#!/usr/bin/env python3
"""Build and verify the Storybook static image from one committed revision.

build   exports projects/storybook/nextjs at a commit with git archive, so the
        context holds committed files only, builds hy-home/storybook:<commit>
        with SBOM and max provenance attestations, and with --push also pushes
        it to the local registry.
verify  checks that the image label, revision.json, lockfile, UI package and
        manifest hashes all match that commit, that the static output carries
        no environment or key files, and with --registry that the registry
        holds the same index with its SBOM and provenance.

The default revision is the last commit that changed the Storybook source,
so an unrelated commit never changes the image a revision names.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = "projects/storybook/nextjs"
IMAGE = "hy-home/storybook"
HTML = "/usr/share/nginx/html"
SHA = re.compile(r"[0-9a-f]{40}")
# Names that must never reach the static output.
FORBIDDEN = re.compile(
    r"(^|/)(\.env[^/]*|[^/]*\.pem|[^/]*\.key|[^/]*\.map|node_modules)(/|$)"
)


def run(*args: str) -> str:
    return subprocess.run(
        args, cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def registry() -> str:
    return f"127.0.0.1:{os.environ.get('REGISTRY_PORT', '5000')}"


def resolve_revision(value: str | None) -> str:
    revision = value or run("git", "log", "-1", "--format=%H", "--", SOURCE).strip()
    revision = run("git", "rev-parse", "--verify", f"{revision}^{{commit}}").strip()
    run("git", "cat-file", "-e", f"{revision}:{SOURCE}/Dockerfile")
    return revision


def export(revision: str, destination: pathlib.Path) -> pathlib.Path:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", revision, SOURCE],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout  # fmt: skip
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(destination, filter="data")
    return destination / SOURCE


def check_static(record: dict, revision: str, expected: dict, files: list[str],
                 manifests: dict[str, str]) -> list[str]:  # fmt: skip
    """Compare the image's revision.json and file list with the commit."""
    findings = []
    if record.get("sourceRevision") != revision:
        findings.append(
            f"revision.json sourceRevision {record.get('sourceRevision')!r}"
        )
    if record.get("lockfileSha256") != expected["lockfileSha256"]:
        findings.append("revision.json lockfileSha256 differs from the commit")
    if record.get("uiPackage") != expected["uiPackage"]:
        findings.append(f"revision.json uiPackage {record.get('uiPackage')!r}")
    if record.get("manifestSha256") != manifests or len(manifests) != 2:
        findings.append("manifest hashes differ from revision.json")
    findings += [f"forbidden file {name}" for name in files if FORBIDDEN.search(name)]
    return findings


def build(revision: str, push: bool) -> None:
    tags = [f"{IMAGE}:{revision}"] + (
        [f"{registry()}/{IMAGE}:{revision}"] if push else []
    )
    with tempfile.TemporaryDirectory(prefix="hy-storybook-") as tmp:
        context = export(revision, pathlib.Path(tmp))
        command = ["docker", "buildx", "build", "--sbom=true", "--provenance=mode=max",
                   "--build-arg", f"STORYBOOK_SOURCE_REVISION={revision}", "--load"]  # fmt: skip
        for tag in tags:
            command += ["-t", tag]
        subprocess.run([*command, str(context)], cwd=ROOT, check=True)
    if push:
        subprocess.run(["docker", "push", tags[1]], cwd=ROOT, check=True)


def inspect_remote(reference: str, field: str) -> dict:
    return json.loads(run("docker", "buildx", "imagetools", "inspect", reference,
                          "--format", f"{{{{json .{field}}}}}"))  # fmt: skip


def verify(revision: str, check_registry: bool) -> int:
    image = f"{IMAGE}:{revision}"
    meta = json.loads(run("docker", "image", "inspect", image))[0]
    findings = []
    label = (meta["Config"].get("Labels") or {}).get(
        "org.opencontainers.image.revision"
    )
    if label != revision:
        findings.append(f"image label revision {label!r}")
    script = (f"cat {HTML}/revision.json; echo; cd {HTML}/manifests && sha256sum "
              f"components.json docs.json; echo; cd {HTML} && find . -type f")  # fmt: skip
    out = run("docker", "run", "--rm", "--pull=never", "--network", "none",
              "--entrypoint", "sh", image, "-c", script)  # fmt: skip
    record_text, sums, listing = out.split("\n\n", 2)
    manifests = {
        name: digest for digest, name in (line.split() for line in sums.splitlines())
    }
    lockfile = subprocess.run(["git", "show", f"{revision}:{SOURCE}/package-lock.json"],
                              cwd=ROOT, check=True, capture_output=True).stdout  # fmt: skip
    ui = json.loads(run("git", "show", f"{revision}:{SOURCE}/packages/ui/package.json"))
    expected = {"lockfileSha256": hashlib.sha256(lockfile).hexdigest(),
                "uiPackage": {"name": ui["name"], "version": ui["version"]}}  # fmt: skip
    files = sorted(line[2:] for line in listing.splitlines() if line.startswith("./"))
    findings += check_static(
        json.loads(record_text), revision, expected, files, manifests
    )
    report = {"revision": revision, "image": image, "imageId": meta["Id"],
              "sourceTree": run("git", "rev-parse", f"{revision}:{SOURCE}").strip(),
              **expected, "manifestSha256": manifests, "files": len(files)}  # fmt: skip
    if check_registry:
        remote = f"{registry()}/{IMAGE}:{revision}"
        index = inspect_remote(remote, "Manifest")
        provenance = json.dumps(inspect_remote(remote, "Provenance"))
        packages = (inspect_remote(remote, "SBOM").get("SPDX") or {}).get(
            "packages"
        ) or []
        attestations = [m for m in index.get("manifests", [])
                        if (m.get("annotations") or {}).get("vnd.docker.reference.type")
                        == "attestation-manifest"]  # fmt: skip
        if index["digest"] != meta["Id"]:
            findings.append(f"registry index {index['digest']} is not the local image")
        if f'"build-arg:STORYBOOK_SOURCE_REVISION": "{revision}"' not in provenance:
            findings.append("provenance does not record the source revision")
        if not attestations or not packages:
            findings.append("registry index lacks SBOM or provenance attestations")
        report.update(registryDigest=index["digest"], attestations=len(attestations),
                      sbomPackages=len(packages))  # fmt: skip
    print(json.dumps(report, indent=2))
    for finding in findings:
        print(f"FAIL {finding}", file=sys.stderr)
    return 1 if findings else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name, flag in (("build", "--push"), ("verify", "--registry")):
        command = sub.add_parser(name)
        command.add_argument("--revision")
        command.add_argument(flag, action="store_true")
    args = parser.parse_args(argv)
    revision = resolve_revision(args.revision)
    if not SHA.fullmatch(revision):
        raise SystemExit(f"not a full commit: {revision}")
    if args.command == "build":
        build(revision, args.push)
        return verify(revision, args.push)
    return verify(revision, args.registry)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
