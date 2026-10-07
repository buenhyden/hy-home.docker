#!/usr/bin/env python3
"""Validate main changelogs and publish a new SemVer draft with complete assets.

The publish subcommand mutates GitHub and requires separate release authority.
Failures retain any newly created tag/draft for an explicitly approved recovery;
this producer never moves tags, overwrites assets or republishes versions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from datetime import date
from pathlib import Path

SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
RELEASE_HEADING = re.compile(r"## \[([^\]]+)\] - ([0-9]{4}-[0-9]{2}-[0-9]{2})")
CATEGORIES = frozenset(
    {"Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"}
)
Runner = Callable[[list[str]], str]


class ReleaseError(ValueError):
    """A fail-closed validation or publication error with safe output."""


def release_tag(version: str) -> str:
    if SEMVER.fullmatch(version) is None:
        raise ReleaseError(
            "version must be a complete SemVer 2.0 version without v prefix"
        )
    return "v" + version


def validate_changelog(text: str) -> dict[str, str]:
    lines = text.splitlines()
    headers = [(i, line) for i, line in enumerate(lines) if line.startswith("## ")]
    if not headers or headers[0][1] != "## [Unreleased]":
        raise ReleaseError("CHANGELOG must start with the [Unreleased] section")
    releases: dict[str, str] = {}
    for position, (start, heading) in enumerate(headers):
        end = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
        body = lines[start + 1 : end]
        if any(line.startswith("### ") and line[4:] not in CATEGORIES for line in body):
            raise ReleaseError("CHANGELOG categories must follow Keep a Changelog")
        if heading == "## [Unreleased]" and position == 0:
            continue
        match = RELEASE_HEADING.fullmatch(heading)
        if match is None:
            raise ReleaseError("release heading must be exactly [SemVer] - YYYY-MM-DD")
        version, released_on = match.groups()
        release_tag(version)
        try:
            date.fromisoformat(released_on)
        except ValueError as error:
            raise ReleaseError(
                "release heading contains an invalid calendar date"
            ) from error
        if version in releases:
            raise ReleaseError("duplicate CHANGELOG version")
        if not any(line.startswith("### ") for line in body) or not any(
            line.startswith("- ") and line[2:].strip() for line in body
        ):
            raise ReleaseError("dated release must contain categorized changes")
        releases[version] = "\n".join(lines[start:end]).strip() + "\n"
    return releases


def release_notes(text: str, version: str) -> str:
    release_tag(version)
    notes = validate_changelog(text).get(version)
    if notes is None:
        raise ReleaseError("exact dated CHANGELOG version is missing")
    return notes


def run_command(argv: list[str]) -> str:
    try:
        result = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReleaseError("release command could not complete") from error
    if result.returncode:
        raise ReleaseError("release command failed")
    return result.stdout.strip()


def _json(run: Runner, argv: list[str]):
    try:
        return json.loads(run(argv))
    except (json.JSONDecodeError, TypeError) as error:
        raise ReleaseError("invalid GitHub response") from error


def _ref_sha(run: Runner, repository: str, ref: str) -> str:
    response = _json(run, ["gh", "api", f"repos/{repository}/git/ref/{ref}"])
    if not isinstance(response, dict) or not isinstance(response.get("object"), dict):
        raise ReleaseError("invalid GitHub reference response")
    sha = response["object"].get("sha")
    if response["object"].get("type") != "commit":
        raise ReleaseError("release reference must identify a commit directly")
    if not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{40}", sha) is None:
        raise ReleaseError("invalid GitHub reference SHA")
    return sha


def _new_version(run: Runner, repository: str, tag: str) -> None:
    pages = _json(
        run, ["gh", "api", f"repos/{repository}/releases", "--paginate", "--slurp"]
    )
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise ReleaseError("invalid GitHub release listing")
    for page in pages:
        for existing in page:
            if not isinstance(existing, dict) or not isinstance(
                existing.get("tag_name"), str
            ):
                raise ReleaseError("invalid GitHub release record")
            if existing["tag_name"] in {tag, tag[1:]}:
                raise ReleaseError(
                    "version already has a release or draft; recovery requires review"
                )
    tags = run(
        [
            "git",
            "ls-remote",
            "--tags",
            f"https://github.com/{repository}.git",
            f"refs/tags/{tag}",
            f"refs/tags/{tag[1:]}",
        ]
    )
    if tags:
        raise ReleaseError("tag already exists; it will not be moved or reused")


def _assets(directory: Path, changelog: str, tag: str, sha: str) -> list[Path]:
    payloads = {
        "CHANGELOG.md": changelog,
        "SOURCE_REVISION.txt": f"tag={tag}\ncommit={sha}\n",
    }
    paths = [directory / name for name in payloads]
    for name, content in payloads.items():
        (directory / name).write_text(content, encoding="utf-8")
    sums = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in paths
    )
    checksum = directory / "SHA256SUMS"
    checksum.write_text(sums, encoding="utf-8")
    return [*paths, checksum]


def _verify_release(
    run: Runner, repository: str, tag: str, paths: list[Path], *, expected_draft: bool
) -> dict:
    draft = _json(
        run,
        [
            "gh",
            "api",
            f"repos/{repository}/releases/tags/{tag}",
            "--header",
            "X-GitHub-Api-Version: 2026-03-10",
        ],
    )
    if (
        not isinstance(draft, dict)
        or draft.get("draft") is not expected_draft
        or draft.get("tag_name") != tag
    ):
        raise ReleaseError(
            "release state or tag differs from the expected publication stage"
        )
    assets = draft.get("assets")
    if not isinstance(assets, list) or any(
        not isinstance(asset, dict) for asset in assets
    ):
        raise ReleaseError("invalid release asset response")
    actual = [
        (asset.get("name"), asset.get("size"), asset.get("state"), asset.get("digest"))
        for asset in assets
    ]
    if any(
        not isinstance(name, str)
        or type(size) is not int
        or size <= 0
        or state != "uploaded"
        or not isinstance(digest, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is None
        for name, size, state, digest in actual
    ):
        raise ReleaseError("invalid release asset metadata")
    expected = [
        (
            path.name,
            path.stat().st_size,
            "uploaded",
            "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in paths
    ]
    if len(actual) != len(expected) or set(actual) != set(expected):
        raise ReleaseError(
            "draft assets are incomplete or differ from the prepared manifest"
        )
    return draft


def publish(
    version: str, sha: str, repository: str, *, run: Runner = run_command
) -> dict[str, str | bool]:
    tag = release_tag(version)
    if re.fullmatch(r"[0-9a-f]{40}", sha) is None:
        raise ReleaseError("release target must be a full commit SHA")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is None:
        raise ReleaseError("repository must be owner/name")
    if run(["git", "rev-parse", "HEAD"]) != sha:
        raise ReleaseError("checkout HEAD must match the release target")
    remote_main = _ref_sha(run, repository, "heads/main")
    run(["git", "merge-base", "--is-ancestor", sha, remote_main])
    changelog = run(["git", "show", f"{sha}:CHANGELOG.md"]) + "\n"
    notes = release_notes(changelog, version)
    _new_version(run, repository, tag)
    _json(
        run,
        [
            "gh",
            "api",
            f"repos/{repository}/git/refs",
            "--method",
            "POST",
            "-f",
            f"ref=refs/tags/{tag}",
            "-f",
            f"sha={sha}",
        ],
    )
    if _ref_sha(run, repository, f"tags/{tag}") != sha:
        raise ReleaseError("created tag does not identify the release target")
    with tempfile.TemporaryDirectory(prefix="hy-home-release-") as temporary:
        directory = Path(temporary)
        notes_file = directory / "notes.md"
        notes_file.write_text(notes, encoding="utf-8")
        paths = _assets(directory, changelog, tag, sha)
        create = [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            repository,
            "--draft",
            "--verify-tag",
            "--target",
            sha,
            "--title",
            tag,
            "--notes-file",
            str(notes_file),
        ]
        if SEMVER.fullmatch(version).group(4) is not None:
            create.append("--prerelease")
        run(create)
        run(
            [
                "gh",
                "release",
                "upload",
                tag,
                *(str(path) for path in paths),
                "--repo",
                repository,
            ]
        )
        _verify_release(run, repository, tag, paths, expected_draft=True)
        if _ref_sha(run, repository, f"tags/{tag}") != sha:
            raise ReleaseError("tag changed before publication")
        try:
            run(["gh", "release", "edit", tag, "--repo", repository, "--draft=false"])
            if _ref_sha(run, repository, f"tags/{tag}") != sha:
                raise ReleaseError("published tag differs from the target")
            published = _verify_release(
                run, repository, tag, paths, expected_draft=False
            )
            if type(published.get("immutable")) is not bool:
                raise ReleaseError("published immutability state is unobserved")
        except ReleaseError as error:
            raise ReleaseError(
                "publication readback failed; release may exist, manual recovery required"
            ) from error
    return {
        "tag": tag,
        "commit": sha,
        "published": not published["draft"],
        "immutable": published["immutable"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="read-only changelog validation")
    validate.add_argument("--changelog", type=Path, default=Path("CHANGELOG.md"))
    production = commands.add_parser(
        "publish", help="authorized main release publication"
    )
    production.add_argument("--version", required=True)
    production.add_argument("--sha", required=True)
    production.add_argument("--repository", required=True)
    arguments = parser.parse_args()
    try:
        if arguments.command == "validate":
            validate_changelog(arguments.changelog.read_text(encoding="utf-8"))
            print("PASS: main changelog format")
        else:
            receipt = publish(arguments.version, arguments.sha, arguments.repository)
            print(json.dumps(receipt))
    except (ReleaseError, OSError, UnicodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
