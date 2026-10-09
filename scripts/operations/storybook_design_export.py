#!/usr/bin/env python3
"""Export the reviewed design system for Claude Design (SPEC-0219).

/design-sync uploads the repository it runs in, so it runs in this bundle and
never in the repository: the bundle holds only the committed files named in
projects/storybook/nextjs/design-export.allowlist.json plus a manifest of their
hashes. Story imports are rewritten to the bundle layout; nothing else changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ALLOWLIST = "projects/storybook/nextjs/design-export.allowlist.json"
FORBIDDEN_PATH = re.compile(r"(^|/)(\.env[^/]*|secrets?|[^/]*\.(pem|key|p12))(/|$)")
SECRET = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?i:password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"\s]{8,}"
    r"|Bearer\s+[A-Za-z0-9._~+/-]{20,}"
    r"|__Secure-[A-Za-z0-9_-]+=|_oauth2_proxy="
)
STORY_IMPORT = "../../packages/ui/src/"


def check_allowlist(files: dict[str, str]) -> list[str]:
    findings = []
    for target, source in files.items():
        for path in (target, source):
            if (
                "*" in path
                or ".." in pathlib.PurePosixPath(path).parts
                or path.startswith("/")
            ):
                findings.append(
                    f"{path}: globs, parent or absolute paths are not allowed"
                )
            elif FORBIDDEN_PATH.search(path):
                findings.append(
                    f"{path}: environment, secret or key files are never exported"
                )
    return findings


def scan(name: str, text: str) -> list[str]:
    return [f"{name}: secret-shaped content"] if SECRET.search(text) else []


def export(out: pathlib.Path, revision: str) -> dict:
    allowlist = json.loads((ROOT / ALLOWLIST).read_text(encoding="utf-8"))["files"]
    findings = check_allowlist(allowlist)
    if out.exists() and any(out.iterdir()):
        findings.append(f"{out} is not empty")
    contents = {}
    for target, source in sorted(allowlist.items()):
        if findings:
            break
        text = subprocess.run(["git", "show", f"{revision}:{source}"], cwd=ROOT,
                              check=True, capture_output=True, text=True).stdout  # fmt: skip
        if target.startswith("stories/"):
            text = text.replace(STORY_IMPORT, "../src/")
        findings += scan(target, text)
        contents[target] = text
    if findings:
        raise SystemExit("\n".join(f"FAIL {finding}" for finding in findings))
    manifest = {"revision": revision, "files": {}}
    for target, text in contents.items():
        path = out / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        manifest["files"][target] = hashlib.sha256(text.encode()).hexdigest()
    (out / "export-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=pathlib.Path)
    parser.add_argument("--revision", default="HEAD")
    args = parser.parse_args(argv)
    revision = subprocess.run(["git", "rev-parse", "--verify", f"{args.revision}^{{commit}}"],
                              cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()  # fmt: skip
    manifest = export(args.out, revision)
    print(
        f"design export: revision={revision} files={len(manifest['files'])} out={args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
