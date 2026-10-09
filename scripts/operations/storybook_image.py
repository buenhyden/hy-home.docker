#!/usr/bin/env python3
"""Build and verify the Storybook images from one committed revision.

build   exports projects/storybook/nextjs at a commit with git archive, so the
        context holds committed files only, and builds the static origin
        hy-home/storybook:<commit> and the remote docs MCP
        hy-home/storybook-mcp:<commit> from that one context, with SBOM and max
        provenance attestations; --push also pushes both to the local registry.
verify  checks that both image labels, revision.json, lockfile, UI package and
        manifest hashes all match that commit and that the MCP image serves the
        same manifests, that the static output carries no environment or key
        files, and with --registry that the registry holds the same indexes
        with their SBOM and provenance.

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
# Dockerfile target per image; None is the final (static) stage.
IMAGES = {IMAGE: None, "hy-home/storybook-mcp": "mcp"}
HTML = "/usr/share/nginx/html"
MCP_STATIC = "/app/storybook-static"
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
    with tempfile.TemporaryDirectory(prefix="hy-storybook-") as tmp:
        context = export(revision, pathlib.Path(tmp))
        for image, target in IMAGES.items():
            command = ["docker", "buildx", "build", "--sbom=true", "--provenance=mode=max",
                       "--build-arg", f"STORYBOOK_SOURCE_REVISION={revision}", "--load",
                       "-t", f"{image}:{revision}"]  # fmt: skip
            if target:
                command += ["--target", target]
            if push:
                command += ["-t", f"{registry()}/{image}:{revision}"]
            subprocess.run([*command, str(context)], cwd=ROOT, check=True)
    if push:
        for image in IMAGES:
            subprocess.run(["docker", "push", f"{registry()}/{image}:{revision}"],
                           cwd=ROOT, check=True)  # fmt: skip


def inspect_remote(reference: str, field: str) -> dict:
    return json.loads(run("docker", "buildx", "imagetools", "inspect", reference,
                          "--format", f"{{{{json .{field}}}}}"))  # fmt: skip


def inspect_contents(image: str, static: str, listing: bool) -> tuple[dict, dict, list]:
    """revision.json, manifest hashes and (for the origin) the file list of an image."""
    script = (f"cat {static}/revision.json; echo; cd {static}/manifests && sha256sum "
              f"components.json docs.json; echo; cd {static} && "
              f"{'find . -type f' if listing else 'true'}")  # fmt: skip
    out = run("docker", "run", "--rm", "--pull=never", "--network", "none",
              "--entrypoint", "sh", image, "-c", script)  # fmt: skip
    record_text, sums, files = out.split("\n\n", 2)
    manifests = {
        name: digest for digest, name in (line.split() for line in sums.splitlines())
    }
    paths = sorted(line[2:] for line in files.splitlines() if line.startswith("./"))
    return json.loads(record_text), manifests, paths


def check_registry_image(image: str, revision: str, image_id: str) -> tuple[list, dict]:
    remote = f"{registry()}/{image}:{revision}"
    index = inspect_remote(remote, "Manifest")
    provenance = json.dumps(inspect_remote(remote, "Provenance"))
    packages = (inspect_remote(remote, "SBOM").get("SPDX") or {}).get("packages") or []
    attestations = [m for m in index.get("manifests", [])
                    if (m.get("annotations") or {}).get("vnd.docker.reference.type")
                    == "attestation-manifest"]  # fmt: skip
    findings = []
    if index["digest"] != image_id:
        findings.append(
            f"{image}: registry index {index['digest']} is not the local image"
        )
    if f'"build-arg:STORYBOOK_SOURCE_REVISION": "{revision}"' not in provenance:
        findings.append(f"{image}: provenance does not record the source revision")
    if not attestations or not packages:
        findings.append(
            f"{image}: registry index lacks SBOM or provenance attestations"
        )
    return findings, {"registryDigest": index["digest"],
                      "attestations": len(attestations), "sbomPackages": len(packages)}  # fmt: skip


def verify(revision: str, check_registry: bool) -> int:
    findings = []
    lockfile = subprocess.run(["git", "show", f"{revision}:{SOURCE}/package-lock.json"],
                              cwd=ROOT, check=True, capture_output=True).stdout  # fmt: skip
    ui = json.loads(run("git", "show", f"{revision}:{SOURCE}/packages/ui/package.json"))
    expected = {"lockfileSha256": hashlib.sha256(lockfile).hexdigest(),
                "uiPackage": {"name": ui["name"], "version": ui["version"]}}  # fmt: skip
    report = {"revision": revision,
              "sourceTree": run("git", "rev-parse", f"{revision}:{SOURCE}").strip(),
              **expected, "images": {}}  # fmt: skip
    for image, target in IMAGES.items():
        reference = f"{image}:{revision}"
        meta = json.loads(run("docker", "image", "inspect", reference))[0]
        label = (meta["Config"].get("Labels") or {}).get(
            "org.opencontainers.image.revision"
        )
        if label != revision:
            findings.append(f"{reference}: image label revision {label!r}")
        record, manifests, files = inspect_contents(
            reference, MCP_STATIC if target else HTML, listing=not target
        )
        findings += [f"{reference}: {f}" for f in
                     check_static(record, revision, expected, files, manifests)]  # fmt: skip
        entry = {"imageId": meta["Id"], "manifestSha256": manifests}
        if not target:
            entry["files"] = len(files)
        if check_registry:
            registry_findings, registry_report = check_registry_image(
                image, revision, meta["Id"]
            )
            findings += registry_findings
            entry.update(registry_report)
        report["images"][image] = entry
    hashes = {
        json.dumps(entry["manifestSha256"]) for entry in report["images"].values()
    }
    if len(hashes) != 1:
        findings.append(
            "the MCP image serves different manifests from the static origin"
        )
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
