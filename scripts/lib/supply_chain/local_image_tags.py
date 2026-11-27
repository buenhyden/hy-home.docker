"""Keep the version in a locally built image tag equal to its Dockerfile base.

A locally built service such as ``hy/loki:3.7.8-seaweedfs`` names the upstream
version it wraps, but Renovate only bumps the Dockerfile ``FROM`` line, so the
tag kept naming a past release. For every SEC01 ledger row with a build source
whose Compose tag starts with a version, the Dockerfile ``FROM`` image with the
same name as the tag's repository sets the expected version. Rows without such
a ``FROM`` (an unversioned tag, an unresolved build variable, a differently
named base) are not covered.

--check exits 1 on a stale tag; --write rewrites the Compose ``image:`` lines.
Standard library only, so the Renovate post-upgrade step can run it as is.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEDGER = "infra/09-platform-ops/security-updates/update-ledger.json"
TAG_VERSION = re.compile(r"^v?(\d+(?:\.\d+)+)")
FROM = re.compile(r"^FROM\s+(?:--\S+\s+)*(\S+)", re.M)
ARG = re.compile(r"^ARG\s+(\w+)=(\S+)", re.M)


def _name(ref):
    return ref.split("@", 1)[0].rsplit(":", 1)[0].rsplit("/", 1)[-1]


def expected_image(root, row):
    """Return the Compose image the row should declare, or None if not covered."""
    image, build = row.get("current_declared"), row.get("build_source")
    if not isinstance(image, str) or ":" not in image or not build:
        return None
    build = build if isinstance(build, dict) else {"context": build}
    dockerfile = build.get("dockerfile", "Dockerfile")
    if "$" in dockerfile or "$" in build.get("context", ""):
        return None
    repo, tag = image.rsplit(":", 1)
    current = TAG_VERSION.match(tag)
    path = Path(root, row["compose_file"]).parent / build["context"] / dockerfile
    if not current or not path.is_file():
        return None
    text = path.read_text()
    args = dict(ARG.findall(text))
    for ref in FROM.findall(text):
        ref = re.sub(r"\$\{?(\w+)\}?", lambda m: args.get(m[1], m[0]), ref)
        base = ref.split("@", 1)[0]
        if ":" in base and _name(base) == _name(image):
            version = TAG_VERSION.match(base.rsplit(":", 1)[1])
            if version:
                return f"{repo}:{version[1]}{tag[current.end() :]}"
    return None


def _image_line(old):
    return re.compile(rf"(?m)^(\s*image:\s*){re.escape(old)}\s*$")


def stale(root, ledger):
    """Return {compose_file: {old image: new image}} for every stale tag.

    Only a tag still present in its Compose file counts; a ledger row that
    lags an already renamed tag is ledger_rebind's drift, not a stale tag.
    """
    result = {}
    for row in ledger["entries"]:
        old, new = row["current_declared"], expected_image(root, row)
        text = (root / row["compose_file"]).read_text()
        if new and new != old and _image_line(old).search(text):
            result.setdefault(row["compose_file"], {})[old] = new
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    changes = stale(root, json.loads((root / LEDGER).read_text()))
    for compose, images in sorted(changes.items()):
        for old, new in sorted(images.items()):
            print(f"{compose}: {old} -> {new}")
        if args.write:
            path = root / compose
            text = path.read_text()
            for old, new in images.items():
                text = _image_line(old).sub(lambda m, new=new: m[1] + new, text)
            path.write_text(text)
    if changes and args.check:
        print("stale local image tags; run with --write", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
