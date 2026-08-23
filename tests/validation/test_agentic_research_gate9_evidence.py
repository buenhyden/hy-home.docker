from __future__ import annotations

import ast
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import types
import unittest
from collections.abc import Mapping, Sequence
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/validation/agentic-research-gate9-evidence.py"
SCHEMA = "agentic-research-gate9/v1"
BUNDLE_SCHEMA = "agentic-research-gate9-bundle/v1"
BUILD_RECEIPT_SCHEMA = "agentic-research-gate9-build-receipt/v1"
OLD_PACK = "docs/90.references/research/2026-07-05-agentic-research-pack-refresh"
NEW_PACK = "docs/90.references/research/2026-08-08-agentic-engineering-research-pack"
TASK = "docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"
SPEC = "docs/03.specs/0137-agentic-research-pack-rebuild/spec.md"
PLAN = "docs/03.specs/0137-agentic-research-pack-rebuild/plan.md"
INDEX = "docs/90.references/data/0082-llm-wiki-index/README.md"
COVERAGE = "docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md"
ROLES = ("migration-specification", "quality")
PACKAGE_ATTACHMENTS = (
    "HEAD.txt",
    "SHA256SUMS",
    "assignments.json",
    "gate-results.json",
    "llm-wiki-index.md",
    "llm-wiki-stage-category-coverage.md",
    "new-manifest.tsv",
    "old-manifest.tsv",
    "package.json",
    "plan.md",
    "proposed-deletion.patch",
    "spec.md",
    "task-before.md",
    "task-before-to-candidate.patch",
    "task-candidate.md",
)
AUTHORITY_MODES = {
    "build-package",
    "verify-package",
    "verify-assignments",
    "verify-backfill",
    "publish-evidence-ref",
    "verify-authorized",
}


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def expected_transport(receipt: Mapping[str, object]) -> list[str]:
    """The mandatory all-or-none external-bundle transport group."""
    return [
        "--bundle",
        os.fspath(receipt["bundle_path"]),
        "--expected-bundle-sha256",
        str(receipt["bundle_sha256"]),
        "--expected-package-sha256",
        str(receipt["package_sha256"]),
    ]


def logical_package_fixture() -> dict[str, bytes]:
    payloads = {
        name: f"fixture:{name}\n".encode()
        for name in PACKAGE_ATTACHMENTS
        if name != "SHA256SUMS"
    }
    payloads["SHA256SUMS"] = b"".join(
        f"{sha256_bytes(payloads[name])}  {name}\n".encode()
        for name in sorted(payloads)
    )
    return payloads


def git(
    root: pathlib.Path,
    *args: str,
    check: bool = True,
    input_bytes: bytes | None = None,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    return subprocess.run(
        ["git", *args],
        cwd=root,
        env=command_env,
        input=input_bytes,
        capture_output=True,
        check=check,
    )


def marker(payload: Mapping[str, object]) -> bytes:
    return b"<!-- GATE9-EVIDENCE/v1\n" + canonical_json(payload) + b"-->"


def parse_marker(value: bytes) -> dict[str, object]:
    matched = re.search(
        rb"<!-- GATE9-EVIDENCE/v1\n(?P<payload>\{[^\r\n]*\}\n)-->", value
    )
    if matched is None:
        raise AssertionError("fixture Task marker is missing")
    return json.loads(matched.group("payload"))


def regular_file_snapshot(path: pathlib.Path) -> tuple[int, int, int, bytes]:
    metadata = path.lstat()
    return (
        stat.S_IFMT(metadata.st_mode),
        stat.S_IMODE(metadata.st_mode),
        metadata.st_nlink,
        path.read_bytes(),
    )


def _mapping_tree(root: pathlib.Path, files: Mapping[str, bytes]) -> str:
    trie: dict[bytes, object] = {}
    for raw_path, value in files.items():
        parts = [os.fsencode(part) for part in pathlib.PurePosixPath(raw_path).parts]
        node = trie
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            if not isinstance(child, dict):
                raise AssertionError("fixture prefix collision")
            node = child
        if parts[-1] in node:
            raise AssertionError("fixture duplicate path")
        blob = git(root, "hash-object", "-w", "--stdin", input_bytes=value).stdout.strip()
        node[parts[-1]] = blob

    def emit(node: dict[bytes, object]) -> bytes:
        rows = bytearray()
        for name in sorted(node):
            value = node[name]
            if isinstance(value, dict):
                object_type = b"tree"
                mode = b"040000"
                oid = emit(value)
            else:
                object_type = b"blob"
                mode = b"100644"
                oid = value
            rows.extend(mode + b" " + object_type + b" " + oid + b"\t" + name + b"\0")
        return git(root, "mktree", "-z", input_bytes=bytes(rows)).stdout.strip()

    return emit(trie).decode("ascii")


def task_transition_patch(root: pathlib.Path, before: bytes, after: bytes) -> bytes:
    before_tree = _mapping_tree(root, {TASK: before})
    after_tree = _mapping_tree(root, {TASK: after})
    return git(
        root,
        "diff-tree",
        "-r",
        "--no-commit-id",
        "--binary",
        "--full-index",
        before_tree,
        after_tree,
        "--",
        TASK,
    ).stdout


def load_helper(name: str = "gate9_evidence_test") -> object:
    spec = importlib.util.spec_from_file_location(name, HELPER)
    if spec is None or spec.loader is None:
        raise AssertionError("Gate 9 helper module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Gate9Fixture:
    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.bundle_paths: list[pathlib.Path] = []
        self.wrapper_dirs: list[pathlib.Path] = []
        self.generator_log = pathlib.Path(
            f"/tmp/gate9-generator-calls-{secrets.token_hex(16)}.log"
        )
        git(root, "init", "--quiet")
        git(root, "config", "user.name", "Gate Nine Test")
        git(root, "config", "user.email", "gate9@example.invalid")

        self.write(f"{OLD_PACK}/README.md", "# retiring pack\n")
        self.write(f"{OLD_PACK}/.gitattributes", "*.md diff=hostile\n")
        for ordinal in range(18):
            self.write(f"{OLD_PACK}/file-{ordinal:02d}.md", f"old {ordinal}\n")
        self.write(f"{NEW_PACK}/README.md", "# canonical pack\n")
        for ordinal in range(20):
            self.write(f"{NEW_PACK}/leaf-{ordinal:02d}.md", f"new {ordinal}\n")
        self.weird_siblings = (
            "docs/90.references/research/sibling\tname.md",
            "docs/90.references/research/sibling\nname.md",
        )
        for sibling in self.weird_siblings:
            self.write(sibling, "preserved sibling\n")

        requirements = "\n".join(
            f"- REQ-{ordinal:02d}: fixture requirement {ordinal}"
            for ordinal in range(1, 37)
        )
        self.write(SPEC, f"# Spec\n\n{requirements}\n")
        self.write(PLAN, "# Plan\n\nApproved Step 0e fixture.\n")
        self.write(INDEX, "fixed index\n")
        self.write(COVERAGE, "fixed coverage\n")
        self._write_generator(
            "scripts/knowledge/generate-llm-wiki-index.sh", "fixed index\n", INDEX
        )
        self._write_generator(
            "scripts/knowledge/generate-llm-wiki-coverage.sh",
            "fixed coverage\n",
            COVERAGE,
        )
        self.pending_payload: dict[str, object] = {
            "attempt": 1,
            "schema": SCHEMA,
            "state": "PACKAGE_REVIEW_PENDING",
        }
        self.write(
            TASK,
            "# Task\n\n"
            + "36/36 requirements verified.\n\n"
            + requirements
            + "\n\n"
            + marker(self.pending_payload).decode()
            + "\n",
        )
        helper_path = self.root / HELPER.relative_to(ROOT)
        helper_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HELPER, helper_path)
        git(root, "add", ".")
        git(root, "commit", "--quiet", "-m", "fixture reviewed code")
        self.reviewed_code_head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
        task_path = root / TASK
        task_path.write_text(
            task_path.read_text(encoding="utf-8")
            + f"\nGATE9_REVIEWED_CODE_HEAD: `{self.reviewed_code_head}`\n",
            encoding="utf-8",
        )
        git(root, "add", TASK)
        git(root, "commit", "--quiet", "-m", "fixture reviewed closure")
        self.head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8") + "\nCandidate gate results.\n",
            encoding="utf-8",
        )

    def _write_generator(self, relative: str, output: str, tracked_output: str) -> None:
        script = f"""#!/usr/bin/env bash
set -euo pipefail
mode=${{1:-}}
if [[ -n ${{GATE9_LLM_MANIFEST_FD:-}} || -n ${{GATE9_LLM_MANIFEST_SIZE:-}} || -n ${{GATE9_LLM_MANIFEST_SHA256:-}} ]]; then
  [[ $# -eq 1 && $mode == --stdout ]]
  [[ -n ${{GATE9_LLM_MANIFEST_FD:-}} && -n ${{GATE9_LLM_MANIFEST_SIZE:-}} && -n ${{GATE9_LLM_MANIFEST_SHA256:-}} ]]
  python3 - "$GATE9_LLM_MANIFEST_FD" "$GATE9_LLM_MANIFEST_SIZE" "$GATE9_LLM_MANIFEST_SHA256" <<'PY'
import hashlib, os, sys
fd, size, expected = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
value = os.read(fd, size)
assert len(value) == size and hashlib.sha256(value).hexdigest() == expected
assert os.read(fd, 1) == b""
PY
  printf '%b' {json.dumps(output)}
  printf x >> {json.dumps(os.fspath(self.generator_log))}
elif [[ $# -eq 1 && $mode == --stdout ]]; then
  printf '%b' {json.dumps(output)}
elif [[ $# -eq 1 && $mode == --check ]]; then
  cmp -s <(printf '%b' {json.dumps(output)}) {tracked_output}
elif [[ $# -eq 0 ]]; then
  printf '%b' {json.dumps(output)} > {tracked_output}
else
  exit 2
fi
"""
        self.write(relative, script, executable=True)

    def write(self, relative: str, value: str, *, executable: bool = False) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        if executable:
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def run(
        self,
        *args: str,
        env: Mapping[str, str] | None = None,
        bind_live: bool = True,
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command_env = os.environ.copy()
        if env:
            command_env.update(env)
        command = list(args)
        if bind_live and command and command[0] in AUTHORITY_MODES:
            command[1:1] = [
                "--require-live-head",
                "--live-reviewed-head",
                self.head,
                "--reviewed-code-head",
                self.reviewed_code_head,
            ]
        return subprocess.run(
            ["python3", os.fspath(HELPER), *command],
            cwd=self.root,
            env=command_env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def build_process(
        self,
        attempt: int = 1,
        *,
        env: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self.run(
            "build-package",
            "--attempt",
            str(attempt),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
            env=env,
            timeout=timeout,
        )

    def build(self, attempt: int = 1) -> dict[str, object]:
        result = self.build_process(attempt)
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        receipt = json.loads(result.stdout)
        path = pathlib.Path(receipt["bundle_path"])
        self.bundle_paths.append(path)
        return receipt

    def read_bundle(self, bundle: pathlib.Path | Mapping[str, object]) -> dict[str, object]:
        path = (
            pathlib.Path(bundle["bundle_path"])
            if isinstance(bundle, Mapping)
            else bundle
        )
        return json.loads(path.read_bytes())

    def attachments(self, bundle: pathlib.Path | Mapping[str, object]) -> dict[str, bytes]:
        document = self.read_bundle(bundle)
        return {
            record["path"]: base64.b64decode(record["base64"], validate=True)
            for record in document["attachments"]
        }

    def write_bundle(self, document: Mapping[str, object]) -> pathlib.Path:
        for _ in range(128):
            path = pathlib.Path(
                "/tmp/agentic-research-gate9-attempt-1-"
                + secrets.token_hex(16)
                + ".bundle.json"
            )
            try:
                descriptor = os.open(
                    path,
                    os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                    0o600,
                )
            except FileExistsError:
                continue
            break
        else:
            raise AssertionError("fixture bundle allocation exhausted")
        value = canonical_json(document)
        try:
            view = memoryview(value)
            while view:
                count = os.write(descriptor, view)
                if count <= 0:
                    raise AssertionError("fixture bundle short write")
                view = view[count:]
            os.fsync(descriptor)
            os.fchmod(descriptor, 0o444)
        finally:
            os.close(descriptor)
        self.bundle_paths.append(path)
        return path

    def canonical_bundle(self, attachments: Mapping[str, bytes]) -> tuple[bytes, str]:
        package_sha256 = sha256_bytes(attachments["SHA256SUMS"])
        document = {
            "attachments": [
                {
                    "base64": base64.b64encode(attachments[path]).decode("ascii"),
                    "bytes": len(attachments[path]),
                    "mode": "0444",
                    "path": path,
                    "sha256": sha256_bytes(attachments[path]),
                }
                for path in sorted(attachments)
            ],
            "kind": "gate9-package-bundle",
            "package_sha256": package_sha256,
            "schema": BUNDLE_SCHEMA,
        }
        value = canonical_json(document)
        return value, sha256_bytes(value)

    def rewritten_bundle(
        self,
        original: Mapping[str, object],
        attachments: Mapping[str, bytes],
    ) -> tuple[pathlib.Path, dict[str, object]]:
        value, digest = self.canonical_bundle(attachments)
        document = json.loads(value)
        path = self.write_bundle(document)
        return path, {
            "bundle_path": os.fspath(path),
            "bundle_sha256": digest,
            "package_sha256": document["package_sha256"],
            "schema": BUILD_RECEIPT_SCHEMA,
            "state": "BUILT",
        }

    def repository_state(self) -> dict[str, object]:
        return {
            "head": git(self.root, "rev-parse", "HEAD").stdout,
            "index": regular_file_snapshot(self.root / ".git/index"),
            "old_tree": git(
                self.root, "ls-tree", "-r", "-z", "--full-tree", "HEAD", OLD_PACK
            ).stdout,
            "protected": {
                path: regular_file_snapshot(self.root / path)
                for path in (*self.weird_siblings, INDEX, COVERAGE)
            },
            "refs": git(
                self.root,
                "for-each-ref",
                "--format=%(refname) %(objectname)",
                "refs/codex/review-evidence/agentic-research/gate9/v1/",
            ).stdout,
            "worktrees": git(self.root, "worktree", "list", "--porcelain").stdout,
        }

    def generator_calls(self) -> int:
        return len(self.generator_log.read_bytes()) if self.generator_log.exists() else 0

    def git_wrapper(self, name: str, body: str) -> dict[str, str]:
        directory = pathlib.Path(tempfile.mkdtemp(prefix=f"gate9-git-{name}-"))
        self.wrapper_dirs.append(directory)
        wrapper = directory / "git"
        marker_path = directory / "executed"
        real_git = shutil.which("git")
        if real_git is None:
            raise AssertionError("git is unavailable")
        wrapper.write_text(
            "#!/usr/bin/env bash\nset -eu\nREAL_GIT="
            + json.dumps(real_git)
            + "\n"
            + body,
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        return {
            "GATE9_WRAPPER_MARKER": os.fspath(marker_path),
            "PATH": os.fspath(directory) + os.pathsep + os.environ["PATH"],
        }

    def write_json(self, relative: str, value: object) -> pathlib.Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json(value))
        return path

    def review_materials(
        self, receipt: Mapping[str, object]
    ) -> dict[str, pathlib.Path]:
        attachments = self.attachments(receipt)
        assignments = json.loads(attachments["assignments.json"])
        identities = {
            "migration-specification": ("agent-migration", "/root/gate9-migration"),
            "quality": ("agent-quality", "/root/gate9-quality"),
        }
        attestation = {
            "assignments": [
                {
                    "agent_id": identities[row["role"]][0],
                    "role": row["role"],
                    "run_id": row["run_id"],
                    "task_path": identities[row["role"]][1],
                }
                for row in assignments["assignments"]
            ],
            "attempt": assignments["attempt"],
            "bundle_sha256": receipt["bundle_sha256"],
            "controller_task": "/root",
            "kind": "assignment-attestation",
            "package_head": self.head,
            "package_sha256": receipt["package_sha256"],
            "schema": SCHEMA,
            "source": "collaboration.spawn_agent/result",
        }
        materials: dict[str, pathlib.Path] = {}
        materials["attestation"] = self.write_json(
            "evidence/assignment.json", attestation
        )
        attestation_hash = sha256_bytes(materials["attestation"].read_bytes())
        for role in ROLES:
            report = self.root / f"evidence/{role}-report.md"
            report.write_text(
                f"# {role} review\n\nApproved C0/I0/M0.\n", encoding="utf-8"
            )
            identity = next(
                row for row in attestation["assignments"] if row["role"] == role
            )
            review_receipt = {
                "agent_id": identity["agent_id"],
                "assignment_attestation_sha256": attestation_hash,
                "attempt": assignments["attempt"],
                "bundle_sha256": receipt["bundle_sha256"],
                "findings": {"critical": 0, "important": 0, "minor": 0},
                "kind": "package-review-receipt",
                "package_head": self.head,
                "package_sha256": receipt["package_sha256"],
                "report": {
                    "bytes": len(report.read_bytes()),
                    "sha256": sha256_bytes(report.read_bytes()),
                },
                "role": role,
                "run_id": identity["run_id"],
                "schema": SCHEMA,
                "task_path": identity["task_path"],
                "verdict": "Approved",
            }
            materials[f"{role}-report"] = report
            materials[f"{role}-receipt"] = self.write_json(
                f"evidence/{role}-receipt.json", review_receipt
            )
        return materials

    def backfill_task(
        self,
        receipt: Mapping[str, object],
        materials: Mapping[str, pathlib.Path],
    ) -> bytes:
        attachments = self.attachments(receipt)
        candidate = attachments["task-candidate.md"]
        candidate_marker = parse_marker(candidate)
        attempt = candidate_marker["attempt"]
        reviews: dict[str, object] = {}
        for role in ROLES:
            path = materials[f"{role}-receipt"]
            value = json.loads(path.read_bytes())
            reviews[role] = {
                "agent_id": value["agent_id"],
                "assignment_attestation_sha256": value[
                    "assignment_attestation_sha256"
                ],
                "findings": value["findings"],
                "receipt_sha256": sha256_bytes(path.read_bytes()),
                "role": role,
                "run_id": value["run_id"],
                "task_path": value["task_path"],
                "verdict": value["verdict"],
            }
        payload = {
            "actual_committed_deletion_review": "Not Run",
            "actual_staged_deletion_review": "Not Run",
            "attempt": attempt,
            "bundle_sha256": receipt["bundle_sha256"],
            "evidence_ref": (
                "refs/codex/review-evidence/agentic-research/gate9/v1/"
                f"attempt-{attempt}/{receipt['package_sha256']}"
            ),
            "new_manifest_sha256": sha256_bytes(attachments["new-manifest.tsv"]),
            "old_manifest_sha256": sha256_bytes(attachments["old-manifest.tsv"]),
            "package_sha256": receipt["package_sha256"],
            "proposed_deletion_patch_sha256": sha256_bytes(
                attachments["proposed-deletion.patch"]
            ),
            "recovery_head": self.head,
            "reviews": reviews,
            "schema": SCHEMA,
            "state": "TASK_BACKFILLED",
        }
        updated = candidate.replace(marker(candidate_marker), marker(payload), 1)
        (self.root / TASK).write_bytes(updated)
        return updated

    def closure_materials(
        self,
        receipt: Mapping[str, object],
        materials: dict[str, pathlib.Path],
    ) -> None:
        candidate = self.attachments(receipt)["task-candidate.md"]
        task_after = (self.root / TASK).read_bytes()
        task_diff = task_transition_patch(self.root, candidate, task_after)
        task_tuple = {
            "after": {
                "blob_oid": git(
                    self.root, "hash-object", "--stdin", input_bytes=task_after
                ).stdout.decode().strip(),
                "bytes": len(task_after),
                "sha256": sha256_bytes(task_after),
            },
            "before": {
                "blob_oid": git(
                    self.root, "hash-object", "--stdin", input_bytes=candidate
                ).stdout.decode().strip(),
                "bytes": len(candidate),
                "sha256": sha256_bytes(candidate),
            },
            "diff": {"bytes": len(task_diff), "sha256": sha256_bytes(task_diff)},
        }
        attestation_hash = sha256_bytes(materials["attestation"].read_bytes())
        for role in ROLES:
            report = self.root / f"evidence/{role}-closure-report.md"
            report.write_text(
                f"# {role} closure\n\nMarker matches; non-marker unchanged.\n",
                encoding="utf-8",
            )
            review_path = materials[f"{role}-receipt"]
            review = json.loads(review_path.read_bytes())
            closure = {
                "agent_id": review["agent_id"],
                "assignment_attestation_sha256": attestation_hash,
                "attempt": review["attempt"],
                "bundle_sha256": receipt["bundle_sha256"],
                "findings": {"critical": 0, "important": 0, "minor": 0},
                "kind": "closure",
                "marker_match": True,
                "non_marker_unchanged": True,
                "package_receipt_sha256": sha256_bytes(review_path.read_bytes()),
                "package_sha256": receipt["package_sha256"],
                "report": {
                    "bytes": len(report.read_bytes()),
                    "sha256": sha256_bytes(report.read_bytes()),
                },
                "role": role,
                "run_id": review["run_id"],
                "schema": SCHEMA,
                "task": task_tuple,
                "task_path": review["task_path"],
                "verdict": "Approved",
            }
            materials[f"{role}-closure-report"] = report
            materials[f"{role}-closure"] = self.write_json(
                f"evidence/{role}-closure.json", closure
            )

    def publish(
        self,
        receipt: Mapping[str, object],
        materials: Mapping[str, pathlib.Path],
        *,
        state: str = "AUTHORIZED",
        drift_proof: pathlib.Path | None = None,
        env: Mapping[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        terminal = self.root / "evidence/terminal.md"
        terminal_text = f"{state}\n"
        if state == "REJECTED":
            terminal_text = "REJECTED: package-review-rejected\n"
        elif state == "INVALIDATED":
            if drift_proof is None:
                raise AssertionError("INVALIDATED fixture requires drift proof")
            reason = json.loads(drift_proof.read_bytes())["reason"]
            terminal_text = f"INVALIDATED: {reason}\n"
        terminal.write_text(terminal_text, encoding="utf-8")
        arguments = [
            "publish-evidence-ref",
            *expected_transport(receipt),
            "--task",
            TASK,
            "--terminal-state",
            state,
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--evidence-ref",
            "auto",
        ]
        if state in {"AUTHORIZED", "REJECTED"}:
            for role, cli_role in (
                ("migration-specification", "migration"),
                ("quality", "quality"),
            ):
                arguments.extend(
                    [
                        f"--{cli_role}-report",
                        os.fspath(materials[f"{role}-report"]),
                        f"--{cli_role}-receipt",
                        os.fspath(materials[f"{role}-receipt"]),
                    ]
                )
                if state == "AUTHORIZED":
                    arguments.extend(
                        [
                            f"--{cli_role}-closure-report",
                            os.fspath(materials[f"{role}-closure-report"]),
                            f"--{cli_role}-closure",
                            os.fspath(materials[f"{role}-closure"]),
                        ]
                    )
        elif state == "INVALIDATED":
            if drift_proof is None:
                raise AssertionError("INVALIDATED fixture requires drift proof")
            arguments.extend(["--drift-proof", os.fspath(drift_proof)])
        return self.run(*arguments, env=env)

    def authorize(
        self, receipt: Mapping[str, object]
    ) -> tuple[dict[str, pathlib.Path], str]:
        materials = self.review_materials(receipt)
        self.backfill_task(receipt, materials)
        self.closure_materials(receipt, materials)
        published = self.publish(receipt, materials)
        if published.returncode != 0:
            raise AssertionError(published.stderr)
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        self.hide_control_files()
        return materials, evidence_ref

    def build_attempt_two(self) -> tuple[dict[str, object], str]:
        first = self.build(1)
        materials = self.review_materials(first)
        drift = self.write_json(
            "evidence/attempt-one-drift.json",
            {
                "kind": "drift-proof",
                "reason": "fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        published = self.publish(first, materials, state="INVALIDATED", drift_proof=drift)
        if published.returncode != 0:
            raise AssertionError(published.stderr)
        evidence = json.loads(published.stdout)
        evidence_ref = evidence["evidence_ref"]
        evidence_tree = git(
            self.root, "show", "-s", "--format=%T", evidence_ref
        ).stdout.decode().strip()
        attempt_two = {
            "attempt": 2,
            "attempt_1": {
                "bundle_sha256": first["bundle_sha256"],
                "evidence_ref": evidence_ref,
                "evidence_tree": evidence_tree,
                "package_sha256": first["package_sha256"],
                "reason": "fixture drift",
                "terminal_state": "INVALIDATED",
            },
            "schema": SCHEMA,
            "state": "ATTEMPT_2_PENDING",
        }
        task_path = self.root / TASK
        task_path.write_bytes(
            task_path.read_bytes().replace(
                marker(self.pending_payload), marker(attempt_two), 1
            )
        )
        self.hide_control_files()
        return self.build(2), evidence_ref

    def hide_control_files(self) -> None:
        shutil.rmtree(self.root / "evidence", ignore_errors=True)

    def cleanup(self) -> None:
        for path in self.bundle_paths:
            try:
                path.chmod(0o600)
                path.unlink(missing_ok=True)
            except OSError:
                pass
        self.generator_log.unlink(missing_ok=True)
        for path in self.wrapper_dirs:
            shutil.rmtree(path, ignore_errors=True)


class AgenticResearchGate9EvidenceTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="gate9-evidence-test-")
        self.root = pathlib.Path(self.temporary.name)
        self.fixture = Gate9Fixture(self.root)

    def tearDown(self) -> None:
        self.fixture.cleanup()
        self.temporary.cleanup()

    def verify_bundle(
        self, receipt: Mapping[str, object]
    ) -> subprocess.CompletedProcess[str]:
        return self.fixture.run("verify-package", *expected_transport(receipt))

    def verify_assignments(
        self,
        receipt: Mapping[str, object],
        materials: Mapping[str, pathlib.Path],
    ) -> subprocess.CompletedProcess[str]:
        return self.fixture.run(
            "verify-assignments",
            *expected_transport(receipt),
            "--attestation",
            os.fspath(materials["attestation"]),
        )

    def verify_backfill(
        self,
        receipt: Mapping[str, object],
        materials: Mapping[str, pathlib.Path],
        state: str,
    ) -> subprocess.CompletedProcess[str]:
        return self.fixture.run(
            "verify-backfill",
            *expected_transport(receipt),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--task",
            TASK,
            "--expect-state",
            state,
        )

    def verify_authorized(
        self,
        evidence_ref: str,
        *,
        receipt: Mapping[str, object] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        source = (
            list(expected_transport(receipt))
            if receipt is not None
            else ["--bundle-from-ref"]
        )
        return self.fixture.run(
            "verify-authorized",
            *source,
            "--task",
            TASK,
            "--evidence-ref",
            evidence_ref,
            "--require-clean-real-index",
            "--require-task-only-worktree",
        )

    def assert_fails(
        self, result: subprocess.CompletedProcess[str], code: str
    ) -> None:
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn(code, result.stderr)

    def test_helper_has_no_scratch_index_directory_or_forbidden_git_verbs(
        self,
    ) -> None:
        source = HELPER.read_text(encoding="utf-8")
        syntax = ast.parse(source)
        guarded_functions = {
            node.name: ast.get_source_segment(source, node)
            for node in syntax.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in {"tree_manifest", "tracked_blob_oid", "read_ref_leaves"}
        }
        self.assertEqual(
            {"tree_manifest", "tracked_blob_oid", "read_ref_leaves"},
            set(guarded_functions),
        )
        for function_source in guarded_functions.values():
            self.assertIsNotNone(function_source)
            self.assertIn('"-z"', function_source)
        ref_source = guarded_functions["read_ref_leaves"]
        assert ref_source is not None
        self.assertIn('["cat-file", "blob",', ref_source)
        self.assertNotIn('"show"', ref_source)
        self.assertNotIn(".splitlines(", ref_source)
        self.assertNotIn("open(", ref_source)
        self.assertLess(
            ref_source.index("if path in leaves:"),
            ref_source.index("leaves[path] = blob.stdout"),
        )
        forbidden = (
            "PinnedScratch",
            "ScratchOwnership",
            "GIT_INDEX_FILE",
            '"read-tree"',
            '"update-index"',
            '"write-tree"',
            "TemporaryDirectory",
            "mkdtemp",
            "os.mkdir",
            "os.rmdir",
            "os.unlink",
            "shutil.rmtree",
            '"worktree", "add"',
            '"worktree", "remove"',
            '"worktree", "prune"',
        )
        self.assertEqual([], [token for token in forbidden if token in source])
        self.assertNotIn('"0" * 40', source)
        self.assertIn('"0" * width', source)
        self.assertIn("width = object_format_width(root)", source)
        before = self.fixture.repository_state()
        receipt = self.fixture.build()
        self.assertEqual(before, self.fixture.repository_state())
        self.assertRegex(
            os.fspath(receipt["bundle_path"]),
            r"^/tmp/agentic-research-gate9-attempt-1-[0-9a-f]{32}\.bundle\.json$",
        )

    def test_projected_tree_removes_exact_subtree_and_preserves_raw_siblings(
        self,
    ) -> None:
        module = load_helper("gate9_project_root")
        before = self.fixture.repository_state()
        with mock.patch.object(module, "run_git", wraps=module.run_git) as observed_git:
            projection = module.project_root_tree(self.root, self.fixture.head)
        mktree_calls = [
            call
            for call in observed_git.call_args_list
            if len(call.args) > 1 and call.args[1] == ["mktree", "-z"]
        ]
        self.assertEqual(4, len(mktree_calls))
        patch = projection.proposed_deletion_patch
        self.assertEqual(20, patch.count(b"deleted file mode 100644"))
        self.assertEqual(20, len(projection.old_paths))
        for ordinal in range(18):
            self.assertIn(f"{OLD_PACK}/file-{ordinal:02d}.md".encode(), patch)
        self.assertIn(f"{OLD_PACK}/README.md".encode(), patch)
        self.assertIn(f"{OLD_PACK}/.gitattributes".encode(), patch)
        for sibling in self.fixture.weird_siblings:
            self.assertNotIn(os.fsencode(sibling), patch)
            initial = git(
                self.root,
                "ls-tree",
                "-z",
                "--full-tree",
                projection.initial_tree_oid,
                "--",
                sibling,
            ).stdout
            projected = git(
                self.root,
                "ls-tree",
                "-z",
                "--full-tree",
                projection.final_tree_oid,
                "--",
                sibling,
            ).stdout
            self.assertEqual(initial, projected)
        self.assertEqual(
            b"",
            git(
                self.root,
                "ls-tree",
                "-r",
                "-z",
                "--full-tree",
                projection.final_tree_oid,
                "--",
                OLD_PACK,
            ).stdout,
        )
        self.assertEqual(before, self.fixture.repository_state())

    def test_projected_tree_rejects_malformed_nul_paths_types_and_object_width(
        self,
    ) -> None:
        module = load_helper("gate9_raw_tree_parser")
        parser = getattr(module, "parse_raw_tree_records")
        width = len(self.fixture.head)
        oid = b"a" * width
        valid = b"100644 blob " + oid + b"\tsafe\nname\0"
        records = parser(valid, width)
        self.assertEqual(1, len(records))
        git_ordered = b"".join(
            (
                b"100644 blob " + oid + b"\tfoo.bar\0",
                b"040000 tree " + oid + b"\tfoo\0",
                b"100644 blob " + oid + b"\tfoo0\0",
            )
        )
        ordered = parser(git_ordered, width)
        self.assertEqual([b"foo.bar", b"foo", b"foo0"], [row.name for row in ordered])
        invalid = {
            "unterminated": valid[:-1],
            "slash": valid.replace(b"safe\nname", b"unsafe/name"),
            "dot": valid.replace(b"safe\nname", b".."),
            "width": valid.replace(oid, b"a" * (width - 1)),
            "type": valid.replace(b"100644 blob", b"100644 tree"),
            "duplicate": valid + valid,
            "plain-name-order": b"".join(
                (
                    b"040000 tree " + oid + b"\tfoo\0",
                    b"100644 blob " + oid + b"\tfoo.bar\0",
                )
            ),
        }
        for name, raw in invalid.items():
            with self.subTest(name=name), self.assertRaises(module.Gate9Error) as caught:
                parser(raw, width)
            self.assertEqual("PROJECTED_TREE_SCOPE_DRIFT", caught.exception.code)
        missing = module.RawTreeEntry(
            b"100644", b"blob", b"f" * width, b"missing-object"
        )
        with self.assertRaises(module.Gate9Error) as caught:
            module._emit_verified_tree(
                self.root, [missing], code="PROJECTED_TREE_SCOPE_DRIFT"
            )
        self.assertEqual("PROJECTED_TREE_SCOPE_DRIFT", caught.exception.code)

    def test_tree_diff_is_exact_under_hostile_config_and_initial_tree_attributes(
        self,
    ) -> None:
        module = load_helper("gate9_hostile_tree_diff")
        baseline = module.project_root_tree(
            self.root, self.fixture.head
        ).proposed_deletion_patch
        malicious_attributes = self.root / "malicious-attributes"
        malicious_attributes.write_text("*.md diff=hostile\n", encoding="utf-8")
        git(self.root, "config", "diff.external", "/bin/false")
        git(self.root, "config", "diff.hostile.textconv", "/bin/false")
        git(self.root, "config", "core.attributesFile", os.fspath(malicious_attributes))
        environment = {
            "GIT_EXTERNAL_DIFF": "/bin/false",
            "GIT_DIFF_OPTS": "--ext-diff",
        }
        with mock.patch.dict(os.environ, environment):
            hostile = module.project_root_tree(self.root, self.fixture.head)
        self.assertEqual(
            baseline,
            hostile.proposed_deletion_patch,
        )

    def test_task_patches_and_evidence_tree_use_one_in_memory_trie(self) -> None:
        module = load_helper("gate9_mapping_tree")
        build_tree = getattr(module, "build_tree_from_mapping")
        mapping = {
            "alpha/report.md": ("100644", b"alpha\n"),
            "beta/nested/receipt.json": ("100644", canonical_json({"ok": True})),
        }
        tree = build_tree(self.root, mapping)
        tree_oid = tree.tree_oid if hasattr(tree, "tree_oid") else tree
        listing = git(
            self.root, "ls-tree", "-r", "-z", "--full-tree", str(tree_oid)
        ).stdout
        self.assertIn(b"100644 blob ", listing)
        self.assertIn(b"\talpha/report.md\0", listing)
        self.assertIn(b"\tbeta/nested/receipt.json\0", listing)
        for invalid in (
            {"same": ("100644", b"a"), "same/child": ("100644", b"b")},
            {"../escape": ("100644", b"a")},
            {"/absolute": ("100644", b"a")},
        ):
            with self.assertRaises(module.Gate9Error):
                build_tree(self.root, invalid)
        source = HELPER.read_text(encoding="utf-8")
        self.assertNotIn("def write_task_patch(", source)
        self.assertNotIn("def write_evidence_tree(", source)

    def test_bundle_build_is_atomic_read_only_canonical_and_collision_safe(
        self,
    ) -> None:
        before = self.fixture.repository_state()
        process = self.fixture.build_process()
        self.assertEqual(0, process.returncode, process.stderr)
        receipt = json.loads(process.stdout)
        path = pathlib.Path(receipt["bundle_path"])
        self.fixture.bundle_paths.append(path)
        self.assertEqual(canonical_json(receipt), process.stdout.encode())
        self.assertEqual(
            {
                "bundle_path",
                "bundle_sha256",
                "package_sha256",
                "schema",
                "state",
            },
            set(receipt),
        )
        self.assertEqual(BUILD_RECEIPT_SCHEMA, receipt["schema"])
        self.assertEqual("BUILT", receipt["state"])
        metadata = path.lstat()
        self.assertTrue(stat.S_ISREG(metadata.st_mode))
        self.assertEqual(1, metadata.st_nlink)
        self.assertEqual(0o444, stat.S_IMODE(metadata.st_mode))
        value = path.read_bytes()
        self.assertEqual(receipt["bundle_sha256"], sha256_bytes(value))
        self.assertEqual(canonical_json(json.loads(value)), value)
        document = json.loads(value)
        self.assertEqual(BUNDLE_SCHEMA, document["schema"])
        self.assertEqual(sorted(PACKAGE_ATTACHMENTS), [row["path"] for row in document["attachments"]])
        self.assertEqual(before, self.fixture.repository_state())

    def test_bundle_build_rejects_symlink_collision_traversal_and_partial_write_without_receipt(
        self,
    ) -> None:
        module = load_helper("gate9_atomic_bundle")
        reader = getattr(module, "read_bundle_once")
        victim = pathlib.Path(f"/tmp/gate9-victim-{secrets.token_hex(16)}")
        victim.write_bytes(b"victim\n")
        symlink = pathlib.Path(
            "/tmp/agentic-research-gate9-attempt-1-"
            + secrets.token_hex(16)
            + ".bundle.json"
        )
        symlink.symlink_to(victim)
        try:
            for supplied in (symlink, self.root / "outside.bundle.json"):
                with self.assertRaises(module.Gate9Error) as caught:
                    reader(supplied)
                self.assertEqual("BUNDLE_READ_FAILURE", caught.exception.code)
                self.assertEqual(b"victim\n", victim.read_bytes())
        finally:
            symlink.unlink(missing_ok=True)
            victim.unlink(missing_ok=True)

        writer = getattr(module, "write_atomic_bundle")
        payloads = logical_package_fixture()
        collision_token = secrets.token_hex(16)
        collision = pathlib.Path(
            "/tmp/agentic-research-gate9-attempt-1-"
            + collision_token
            + ".bundle.json"
        )
        collision_fd = os.open(
            collision,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
        )
        os.write(collision_fd, b"collision victim\n")
        os.fchmod(collision_fd, 0o444)
        os.close(collision_fd)
        try:
            with mock.patch.object(module.secrets, "token_hex", return_value=collision_token):
                with self.assertRaises(module.Gate9Error) as caught:
                    writer(1, payloads)
            self.assertEqual("BUNDLE_CREATE_FAILURE", caught.exception.code)
            self.assertEqual(b"collision victim\n", collision.read_bytes())
        finally:
            collision.chmod(0o600)
            collision.unlink(missing_ok=True)

        with mock.patch.object(module.secrets, "token_hex", return_value="../escape"):
            with self.assertRaises(module.Gate9Error) as caught:
                writer(1, payloads)
        self.assertEqual("BUNDLE_CREATE_FAILURE", caught.exception.code)
        short_token = secrets.token_hex(16)
        short_path = pathlib.Path(
            f"/tmp/agentic-research-gate9-attempt-1-{short_token}.bundle.json"
        )
        with mock.patch.object(module.secrets, "token_hex", return_value=short_token), mock.patch.object(
            module.os, "write", return_value=0
        ):
            with self.assertRaises(module.Gate9Error) as caught:
                writer(1, payloads)
        self.assertEqual("BUNDLE_CREATE_FAILURE", caught.exception.code)
        self.assertTrue(short_path.exists())
        short_path.chmod(0o600)
        short_path.unlink()

    def test_atomic_bundle_writer_rejects_directory_entry_substitution(
        self,
    ) -> None:
        module = load_helper("gate9_bundle_entry_substitution")
        payloads = logical_package_fixture()
        for attack in ("rename-replacement", "hardlink-unlink-replacement"):
            with self.subTest(attack=attack):
                token = secrets.token_hex(16)
                path = pathlib.Path(
                    f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
                )
                displaced = pathlib.Path(f"{path}.displaced")
                anchor = pathlib.Path(f"{path}.anchor")
                victim = pathlib.Path(f"{path}.victim")
                victim_bytes = b"unrelated victim must remain unchanged\n"
                victim.write_bytes(victim_bytes)
                real_fsync = module.os.fsync
                attacked = False

                def substitute_on_file_fsync(descriptor: int) -> None:
                    nonlocal attacked
                    real_fsync(descriptor)
                    if attacked or not stat.S_ISREG(module.os.fstat(descriptor).st_mode):
                        return
                    attacked = True
                    if attack == "rename-replacement":
                        path.rename(displaced)
                    else:
                        os.link(path, anchor)
                        path.unlink()
                    os.link(victim, path)

                output = io.StringIO()
                caught: object | None = None
                try:
                    with mock.patch.object(
                        module.secrets, "token_hex", return_value=token
                    ), mock.patch.object(
                        module.os, "fsync", side_effect=substitute_on_file_fsync
                    ), contextlib.redirect_stdout(output):
                        try:
                            module.write_atomic_bundle(1, payloads)
                        except module.Gate9Error as error:
                            caught = error
                    self.assertTrue(attacked)
                    self.assertEqual(victim_bytes, victim.read_bytes())
                    self.assertNotIn("BUILT", output.getvalue())
                    self.assertIsNotNone(caught, "path replacement was accepted")
                    self.assertEqual("BUNDLE_CREATE_FAILURE", caught.code)
                finally:
                    for artifact in (path, displaced, anchor, victim):
                        if artifact.exists():
                            artifact.chmod(0o600)
                            artifact.unlink()

    def test_atomic_bundle_writer_rejects_io_metadata_and_size_faults(
        self,
    ) -> None:
        module = load_helper("gate9_bundle_writer_faults")
        payloads = logical_package_fixture()

        for fault in (
            "midstream-write",
            "file-fsync",
            "directory-fsync",
            "chmod",
            "readback-eof",
            "readback-digest",
        ):
            with self.subTest(fault=fault):
                token = secrets.token_hex(16)
                path = pathlib.Path(
                    f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
                )
                real_write = module.os.write
                real_fsync = module.os.fsync
                real_read = module.os.read
                write_calls = 0
                fsync_calls = 0
                read_calls = 0

                def injected_write(descriptor: int, value: bytes) -> int:
                    nonlocal write_calls
                    write_calls += 1
                    if write_calls == 1:
                        midpoint = max(1, len(value) // 2)
                        return real_write(descriptor, value[:midpoint])
                    raise OSError("injected midstream write failure")

                def injected_fsync(descriptor: int) -> None:
                    nonlocal fsync_calls
                    fsync_calls += 1
                    target = 1 if fault == "file-fsync" else 2
                    if fsync_calls == target:
                        raise OSError("injected fsync failure")
                    real_fsync(descriptor)

                def injected_read(descriptor: int, size: int) -> bytes:
                    nonlocal read_calls
                    read_calls += 1
                    if fault == "readback-eof" and read_calls == 1:
                        return b""
                    value = real_read(descriptor, size)
                    if fault == "readback-digest" and value and read_calls == 1:
                        return bytes((value[0] ^ 1,)) + value[1:]
                    return value

                output = io.StringIO()
                caught: object | None = None
                try:
                    with contextlib.ExitStack() as stack:
                        stack.enter_context(
                            mock.patch.object(
                                module.secrets, "token_hex", return_value=token
                            )
                        )
                        if fault == "midstream-write":
                            stack.enter_context(
                                mock.patch.object(
                                    module.os, "write", side_effect=injected_write
                                )
                            )
                        elif fault in {"file-fsync", "directory-fsync"}:
                            stack.enter_context(
                                mock.patch.object(
                                    module.os, "fsync", side_effect=injected_fsync
                                )
                            )
                        elif fault == "chmod":
                            stack.enter_context(
                                mock.patch.object(
                                    module.os,
                                    "fchmod",
                                    side_effect=OSError("injected chmod failure"),
                                )
                            )
                        else:
                            stack.enter_context(
                                mock.patch.object(
                                    module.os, "read", side_effect=injected_read
                                )
                            )
                        with contextlib.redirect_stdout(output):
                            try:
                                module.write_atomic_bundle(1, payloads)
                            except module.Gate9Error as error:
                                caught = error
                    self.assertIsNotNone(caught)
                    self.assertEqual("BUNDLE_CREATE_FAILURE", caught.code)
                    self.assertNotIn("BUILT", output.getvalue())
                finally:
                    if path.exists():
                        path.chmod(0o600)
                        path.unlink()

        for field, replacement in (
            ("st_nlink", 2),
            ("st_mode", stat.S_IFREG | 0o600),
            ("st_size", 1),
            ("st_dev", -1),
            ("st_ino", -1),
        ):
            with self.subTest(metadata=field):
                token = secrets.token_hex(16)
                path = pathlib.Path(
                    f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
                )
                real_fstat = module.os.fstat
                regular_calls = 0

                def drifted_fstat(descriptor: int) -> object:
                    nonlocal regular_calls
                    observed = real_fstat(descriptor)
                    if not stat.S_ISREG(observed.st_mode):
                        return observed
                    regular_calls += 1
                    if regular_calls != 2:
                        return observed
                    values = {
                        name: getattr(observed, name)
                        for name in dir(observed)
                        if name.startswith("st_")
                    }
                    values[field] = replacement
                    return types.SimpleNamespace(**values)

                try:
                    with mock.patch.object(
                        module.secrets, "token_hex", return_value=token
                    ), mock.patch.object(
                        module.os, "fstat", side_effect=drifted_fstat
                    ), self.assertRaises(module.Gate9Error) as caught:
                        module.write_atomic_bundle(1, payloads)
                    self.assertEqual("BUNDLE_CREATE_FAILURE", caught.exception.code)
                finally:
                    if path.exists():
                        path.chmod(0o600)
                        path.unlink()

        with self.subTest(fault="oversize-before-create"):
            outer, _ = module._bundle_bytes(payloads)
            token = secrets.token_hex(16)
            path = pathlib.Path(
                f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
            )
            caught: object | None = None
            try:
                with mock.patch.object(
                    module.secrets, "token_hex", return_value=token
                ), mock.patch.object(
                    module, "BUNDLE_MAX_BYTES", len(outer) - 1
                ):
                    try:
                        module.write_atomic_bundle(1, payloads)
                    except module.Gate9Error as error:
                        caught = error
                self.assertIsNotNone(caught, "oversize bundle was created")
                self.assertEqual("BUNDLE_SIZE_DRIFT", caught.code)
                self.assertFalse(path.exists(), "oversize failure left a bundle path")
            finally:
                if path.exists():
                    path.chmod(0o600)
                    path.unlink()

    def _run_bundle_publication_window(
        self,
        module: object,
        payloads: Mapping[str, bytes],
        window: str | None,
        replacement_bytes: bytes,
    ) -> dict[str, object]:
        token = secrets.token_hex(16)
        path = pathlib.Path(
            f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
        )
        displaced = pathlib.Path(f"{path}.displaced")
        victim = pathlib.Path(f"{path}.victim")
        victim.write_bytes(replacement_bytes)
        victim.chmod(0o444)
        counters = {
            "entry_stat": 0,
            "final_fstat": 0,
            "final_read": 0,
            "parent_fsync": 0,
        }
        state: dict[str, object] = {
            "parent": None,
            "final": None,
            "attacked": False,
        }
        real_open = module.os.open
        real_fstat = module.os.fstat
        real_stat = module.os.stat
        real_read = module.os.read
        real_fsync = module.os.fsync

        def substitute() -> None:
            if state["attacked"]:
                return
            state["attacked"] = True
            path.rename(displaced)
            victim.rename(path)

        def hooked_open(
            name: object, flags: int, *args: object, **kwargs: object
        ) -> int:
            descriptor = real_open(name, flags, *args, **kwargs)
            if name == "/tmp" and kwargs.get("dir_fd") is None:
                state["parent"] = descriptor
            elif kwargs.get("dir_fd") == state["parent"] and not flags & os.O_CREAT:
                state["final"] = descriptor
            return descriptor

        def hooked_fstat(descriptor: int) -> os.stat_result:
            if descriptor == state["final"]:
                counters["final_fstat"] += 1
            observed = real_fstat(descriptor)
            if (
                descriptor == state["final"]
                and window == "after-final-open-fstat"
                and counters["final_fstat"] == 1
            ):
                substitute()
            return observed

        def hooked_stat(*args: object, **kwargs: object) -> object:
            if kwargs.get("dir_fd") is not None:
                counters["entry_stat"] += 1
                if window == "during-final-pair" and counters["entry_stat"] == 2:
                    substitute()
            observed = real_stat(*args, **kwargs)
            if kwargs.get("dir_fd") is not None:
                if window == "after-first-entry-stat" and counters["entry_stat"] == 1:
                    substitute()
                elif window == "after-final-pair" and counters["entry_stat"] == 2:
                    substitute()
            return observed

        def hooked_read(descriptor: int, size: int) -> bytes:
            value = real_read(descriptor, size)
            if descriptor == state["final"]:
                counters["final_read"] += 1
                if window == "during-final-read" and counters["final_read"] == 1:
                    substitute()
            return value

        def hooked_fsync(descriptor: int) -> None:
            if descriptor == state["parent"]:
                counters["parent_fsync"] += 1
                if (
                    window == "before-final-parent-fsync"
                    and counters["parent_fsync"] == 2
                ):
                    substitute()
            real_fsync(descriptor)
            if descriptor == state["parent"]:
                if (
                    window == "after-first-parent-fsync"
                    and counters["parent_fsync"] == 1
                ):
                    substitute()
                elif window == "before-final-pair" and counters["parent_fsync"] == 2:
                    substitute()

        output = io.StringIO()
        caught: object | None = None
        result: object | None = None
        try:
            with (
                mock.patch.object(module.secrets, "token_hex", return_value=token),
                mock.patch.object(module.os, "open", side_effect=hooked_open),
                mock.patch.object(module.os, "fstat", side_effect=hooked_fstat),
                mock.patch.object(module.os, "stat", side_effect=hooked_stat),
                mock.patch.object(module.os, "read", side_effect=hooked_read),
                mock.patch.object(module.os, "fsync", side_effect=hooked_fsync),
                contextlib.redirect_stdout(output),
            ):
                try:
                    result = module.write_atomic_bundle(1, payloads)
                except module.Gate9Error as error:
                    caught = error
            observed_bytes = path.read_bytes() if path.exists() else None
        finally:
            for artifact in (path, displaced, victim):
                if artifact.exists():
                    artifact.chmod(0o600)
                    artifact.unlink()
        return {
            "attacked": bool(state["attacked"]),
            "caught": caught,
            "counters": dict(counters),
            "observed_bytes": observed_bytes,
            "path": path,
            "result": result,
            "stdout": output.getvalue(),
        }

    def test_atomic_bundle_publication_linearizes_at_final_post_fsync_pair(
        self,
    ) -> None:
        module = load_helper("gate9_bundle_publication_linearization")
        payloads = logical_package_fixture()
        outer, _ = module._bundle_bytes(payloads)

        with self.subTest(contract="one-final-pair-after-the-final-parent-fsync"):
            clean = self._run_bundle_publication_window(
                module, payloads, None, b"unused replacement\n"
            )
            self.assertIsNone(clean["caught"])
            self.assertIsNotNone(clean["result"])
            self.assertEqual(
                2,
                clean["counters"]["entry_stat"],
                "publication must probe the literal direct-child entry exactly "
                "twice: once before the final parent fsync and once as the "
                "second member of the single final post-fsync pair",
            )
            self.assertEqual(2, clean["counters"]["parent_fsync"])
            self.assertGreaterEqual(clean["counters"]["final_fstat"], 2)

        for window in (
            "after-first-entry-stat",
            "after-first-parent-fsync",
            "after-final-open-fstat",
            "during-final-read",
            "before-final-parent-fsync",
            "before-final-pair",
            "during-final-pair",
        ):
            with self.subTest(window=window):
                observed = self._run_bundle_publication_window(
                    module, payloads, window, outer
                )
                self.assertTrue(
                    observed["attacked"], f"attack hook was not reached: {window}"
                )
                self.assertEqual(outer, observed["observed_bytes"])
                self.assertEqual("", observed["stdout"])
                self.assertIsNotNone(
                    observed["caught"],
                    f"substitution before or during the final pair was accepted: {window}",
                )
                self.assertEqual("BUNDLE_CREATE_FAILURE", observed["caught"].code)
                self.assertIsNone(
                    observed["result"],
                    f"substitution before or during the final pair produced a receipt: {window}",
                )

        with self.subTest(window="after-final-pair"):
            replacement = b"non-identical post-publication drift\n"
            observed = self._run_bundle_publication_window(
                module, payloads, "after-final-pair", replacement
            )
            self.assertTrue(observed["attacked"])
            self.assertEqual(replacement, observed["observed_bytes"])
            self.assertEqual("", observed["stdout"])
            self.assertIsNone(
                observed["caught"],
                "a substitution after the linearization point must not revoke "
                "the already published receipt",
            )
            self.assertIsNotNone(observed["result"])
            self.assertEqual(
                (
                    sha256_bytes(outer),
                    os.fspath(observed["path"]),
                ),
                (
                    observed["result"].bundle_sha256,
                    os.fspath(observed["result"].path),
                ),
            )
            self.assertEqual(outer, observed["result"].outer_bytes)

        with self.subTest(contract="entry-check-before-directory-fsync"):
            token = secrets.token_hex(16)
            path = pathlib.Path(
                f"/tmp/agentic-research-gate9-attempt-1-{token}.bundle.json"
            )
            events: list[str] = []
            real_fsync = module.os.fsync
            real_fchmod = module.os.fchmod
            real_read = module.os.read
            real_open = module.os.open
            real_fstat = module.os.fstat
            real_stat = module.os.stat
            final_descriptor: int | None = None

            def ordered_open(
                name: object, flags: int, *args: object, **kwargs: object
            ) -> int:
                nonlocal final_descriptor
                descriptor = real_open(name, flags, *args, **kwargs)
                if kwargs.get("dir_fd") is not None:
                    if flags & os.O_CREAT:
                        events.append("entry-create")
                    else:
                        events.append("final-reopen")
                        final_descriptor = descriptor
                return descriptor

            def ordered_fstat(descriptor: int) -> os.stat_result:
                observed = real_fstat(descriptor)
                if descriptor == final_descriptor:
                    events.append("final-fstat")
                return observed

            def ordered_fsync(descriptor: int) -> None:
                kind = (
                    "directory-fsync"
                    if stat.S_ISDIR(real_fstat(descriptor).st_mode)
                    else "file-fsync"
                )
                events.append(kind)
                real_fsync(descriptor)

            def ordered_fchmod(descriptor: int, mode: int) -> None:
                events.append("chmod")
                real_fchmod(descriptor, mode)

            def ordered_read(descriptor: int, size: int) -> bytes:
                events.append("readback")
                return real_read(descriptor, size)

            def ordered_stat(*args: object, **kwargs: object) -> object:
                if kwargs.get("dir_fd") is not None:
                    events.append("entry-stat")
                return real_stat(*args, **kwargs)

            try:
                with mock.patch.object(
                    module.secrets, "token_hex", return_value=token
                ), mock.patch.object(
                    module.os, "fsync", side_effect=ordered_fsync
                ), mock.patch.object(
                    module.os, "fchmod", side_effect=ordered_fchmod
                ), mock.patch.object(
                    module.os, "read", side_effect=ordered_read
                ), mock.patch.object(
                    module.os, "open", side_effect=ordered_open
                ), mock.patch.object(
                    module.os, "fstat", side_effect=ordered_fstat
                ), mock.patch.object(
                    module.os, "stat", side_effect=ordered_stat
                ):
                    module.write_atomic_bundle(1, payloads)
                self.assertIn("entry-stat", events)
                self.assertIn("final-reopen", events)
                self.assertIn("final-fstat", events)
                self.assertLess(events.index("file-fsync"), events.index("chmod"))
                self.assertLess(events.index("chmod"), events.index("readback"))
                self.assertLess(events.index("readback"), events.index("entry-stat"))
                self.assertLess(
                    events.index("entry-stat"), events.index("directory-fsync")
                )
                self.assertLess(
                    events.index("directory-fsync"), events.index("final-reopen")
                )
                self.assertLess(
                    events.index("final-reopen"), events.index("final-fstat")
                )
                self.assertEqual("entry-stat", events[-1])
                self.assertEqual("directory-fsync", events[-3])
            finally:
                if path.exists():
                    path.chmod(0o600)
                    path.unlink()

    def test_bundle_verification_reads_once_without_extraction(self) -> None:
        module = load_helper("gate9_bundle_read_once")
        payloads = logical_package_fixture()
        bundle = module.write_atomic_bundle(1, payloads)
        path = bundle.path
        self.assertIsNotNone(path)
        if path is None:
            return
        self.fixture.bundle_paths.append(path)
        hardlink = pathlib.Path(f"/tmp/gate9-hardlink-{secrets.token_hex(16)}.bundle.json")
        os.link(path, hardlink)
        self.fixture.bundle_paths.append(hardlink)
        with self.assertRaises(module.Gate9Error) as caught:
            module.read_bundle_once(path)
        self.assertEqual("BUNDLE_READ_FAILURE", caught.exception.code)

        hardlink.chmod(0o600)
        hardlink.unlink()
        self.fixture.bundle_paths.remove(hardlink)
        path.chmod(0o444)
        before_directories = {
            entry.relative_to(self.root)
            for entry in self.root.rglob("*")
            if entry.is_dir() and ".git" not in entry.relative_to(self.root).parts
        }
        real_open = module.os.open
        child_opens = 0

        def open_once(*args: object, **kwargs: object) -> int:
            nonlocal child_opens
            if args and args[0] == path.name:
                child_opens += 1
                if child_opens > 1:
                    raise AssertionError("bundle direct child reopened")
            return real_open(*args, **kwargs)

        with mock.patch.object(module.os, "open", side_effect=open_once):
            verified = module.read_bundle_once(path)
        self.assertEqual(1, child_opens)
        self.assertEqual(payloads, dict(verified.attachments))
        self.assertEqual(bundle.bundle_sha256, verified.bundle_sha256)
        after_directories = {
            entry.relative_to(self.root)
            for entry in self.root.rglob("*")
            if entry.is_dir() and ".git" not in entry.relative_to(self.root).parts
        }
        self.assertEqual(before_directories, after_directories)
        source = HELPER.read_text(encoding="utf-8")
        self.assertNotIn("materialize_evidence", source)

    def test_every_public_mode_freshly_replays_tree_and_memfd_projection(
        self,
    ) -> None:
        receipt = self.fixture.build()
        self.assertEqual(2, self.fixture.generator_calls())

        before = self.fixture.generator_calls()
        verified = self.verify_bundle(receipt)
        self.assertEqual(0, verified.returncode, verified.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())

        materials = self.fixture.review_materials(receipt)
        before = self.fixture.generator_calls()
        assigned = self.verify_assignments(receipt, materials)
        self.assertEqual(0, assigned.returncode, assigned.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())

        before = self.fixture.generator_calls()
        reviewed = self.verify_backfill(receipt, materials, "PACKAGE_REVIEWED")
        self.assertEqual(0, reviewed.returncode, reviewed.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())

        self.fixture.backfill_task(receipt, materials)
        self.fixture.closure_materials(receipt, materials)
        before = self.fixture.generator_calls()
        published = self.fixture.publish(receipt, materials)
        self.assertEqual(0, published.returncode, published.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        self.fixture.hide_control_files()

        evidence_commit = git(
            self.root, "show-ref", "--verify", "--hash", evidence_ref
        ).stdout.decode().strip()
        evidence_tree = git(
            self.root, "rev-parse", f"{evidence_commit}^{{tree}}"
        ).stdout.decode().strip()
        wrong_parent_commit = git(
            self.root,
            "commit-tree",
            evidence_tree,
            "-p",
            evidence_commit,
            input_bytes=b"wrong-parent evidence fixture\n",
        ).stdout.decode().strip()
        git(
            self.root,
            "update-ref",
            evidence_ref,
            wrong_parent_commit,
            evidence_commit,
        )
        # The external bundle is now the first untrusted-input operation, so it
        # must remain present for the later evidence-commit identity check to
        # be the observed failure.
        try:
            before = self.fixture.generator_calls()
            wrong_parent = self.verify_authorized(evidence_ref, receipt=receipt)
            self.assert_fails(wrong_parent, "EVIDENCE_COMMIT_IDENTITY_DRIFT")
            self.assertEqual(before, self.fixture.generator_calls())
        finally:
            git(
                self.root,
                "update-ref",
                evidence_ref,
                evidence_commit,
                wrong_parent_commit,
            )

        mismatched_attachments = self.fixture.attachments(receipt)
        mismatched_attachments["plan.md"] += b"external mismatch\n"
        mismatched_attachments["SHA256SUMS"] = b"".join(
            f"{sha256_bytes(mismatched_attachments[path])}  {path}\n".encode()
            for path in sorted(mismatched_attachments)
            if path != "SHA256SUMS"
        )
        _, mismatched_receipt = self.fixture.rewritten_bundle(
            receipt, mismatched_attachments
        )
        before = self.fixture.generator_calls()
        mismatched = self.verify_authorized(
            evidence_ref, receipt=mismatched_receipt
        )
        self.assert_fails(mismatched, "BUNDLE_TRANSPORT_DRIFT")
        self.assertEqual(before, self.fixture.generator_calls())

        before = self.fixture.generator_calls()
        authorized = self.verify_authorized(evidence_ref, receipt=receipt)
        self.assertEqual(0, authorized.returncode, authorized.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())

        before = self.fixture.generator_calls()
        ref_only = self.verify_authorized(evidence_ref)
        self.assertEqual(0, ref_only.returncode, ref_only.stderr)
        self.assertEqual(before + 2, self.fixture.generator_calls())

    def test_full_ref_only_replay_uses_in_memory_package_attachments(self) -> None:
        receipt = self.fixture.build()
        materials, evidence_ref = self.fixture.authorize(receipt)
        del materials
        bundle_path = pathlib.Path(receipt["bundle_path"])
        bundle_path.chmod(0o000)
        try:
            before = self.fixture.repository_state()
            replay = self.verify_authorized(evidence_ref)
            self.assertEqual(0, replay.returncode, replay.stderr)
            self.assertEqual("AUTHORIZED", json.loads(replay.stdout)["state"])
            self.assertEqual(before, self.fixture.repository_state())
        finally:
            bundle_path.chmod(0o444)
        source = HELPER.read_text(encoding="utf-8")
        self.assertNotIn("materialize_evidence", source)
        self.assertNotIn("TemporaryDirectory", source)

    def test_bundle_binds_twenty_one_file_pack_and_thirty_six_requirements(
        self,
    ) -> None:
        receipt = self.fixture.build()
        attachments = self.fixture.attachments(receipt)
        old_rows = attachments["old-manifest.tsv"].splitlines()
        new_rows = attachments["new-manifest.tsv"].splitlines()
        self.assertEqual(20, len(old_rows))
        self.assertEqual(21, len(new_rows))
        self.assertEqual(20, attachments["proposed-deletion.patch"].count(b"deleted file mode 100644"))
        spec = attachments["spec.md"].decode("utf-8")
        task = attachments["task-candidate.md"].decode("utf-8")
        for ordinal in range(1, 37):
            requirement = f"REQ-{ordinal:02d}"
            self.assertIn(requirement, spec)
            self.assertIn(requirement, task)
        document = self.fixture.read_bundle(receipt)
        self.assertEqual(sorted(PACKAGE_ATTACHMENTS), [row["path"] for row in document["attachments"]])
        self.assertTrue(all(row["mode"] == "0444" for row in document["attachments"]))

    def test_pack_semantic_validator_rejects_exact_requirement_and_manifest_shape_drift(
        self,
    ) -> None:
        module = load_helper("gate9_pack_semantic_table")
        spec = (self.root / SPEC).read_bytes()
        task = (self.root / TASK).read_bytes()
        manifest = module.tree_manifest(self.root, self.fixture.head, module.NEW_PACK)
        cases = {
            "spec-missing-requirement": (
                spec.replace(b"- REQ-36: fixture requirement 36\n", b""),
                task,
                manifest,
            ),
            "spec-extra-requirement": (
                spec + b"- REQ-37: forbidden extra requirement\n",
                task,
                manifest,
            ),
            "task-missing-requirement": (
                spec,
                task.replace(b"- REQ-36: fixture requirement 36\n", b""),
                manifest,
            ),
            "task-extra-requirement": (
                spec,
                task + b"\n- REQ-37: forbidden extra requirement\n",
                manifest,
            ),
            "task-not-36-of-36": (
                spec,
                task.replace(
                    b"36/36 requirements verified.",
                    b"35/36 requirements verified.",
                ),
                manifest,
            ),
            "renamed-readme": (
                spec,
                task,
                manifest.replace(
                    f"{NEW_PACK}/README.md".encode(),
                    f"{NEW_PACK}/OVERVIEW.md".encode(),
                ),
            ),
            "twenty-one-leaves-without-readme": (
                spec,
                task,
                manifest.replace(
                    f"{NEW_PACK}/README.md".encode(),
                    f"{NEW_PACK}/leaf-20.md".encode(),
                ),
            ),
        }
        validator = getattr(module, "validate_pack_semantics", lambda *_: None)
        for case, arguments in cases.items():
            with self.subTest(drift=case):
                caught: object | None = None
                try:
                    validator(*arguments)
                except module.Gate9Error as error:
                    caught = error
                self.assertIsNotNone(caught, f"semantic validator accepted {case}")
                expected = (
                    "PACK_CARDINALITY"
                    if case in {"renamed-readme", "twenty-one-leaves-without-readme"}
                    else "PACKAGE_SEMANTIC_DRIFT"
                )
                self.assertEqual(expected, caught.code)

    def test_shared_semantic_validation_rejects_requirement_task_and_pack_shape_drift(
        self,
    ) -> None:
        def commit_fixture_change(fixture: Gate9Fixture, *paths: str) -> None:
            git(fixture.root, "add", "-A", *paths)
            git(fixture.root, "commit", "--quiet", "-m", "semantic drift fixture")
            fixture.head = (
                git(fixture.root, "rev-parse", "HEAD").stdout.decode().strip()
            )

        def mutate(fixture: Gate9Fixture, case: str) -> None:
            if case == "spec-missing-requirement":
                path = fixture.root / SPEC
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        "- REQ-36: fixture requirement 36\n", ""
                    ),
                    encoding="utf-8",
                )
                commit_fixture_change(fixture, SPEC)
            elif case == "spec-extra-requirement":
                path = fixture.root / SPEC
                path.write_text(
                    path.read_text(encoding="utf-8")
                    + "- REQ-37: forbidden extra requirement\n",
                    encoding="utf-8",
                )
                commit_fixture_change(fixture, SPEC)
            elif case == "task-missing-requirement":
                path = fixture.root / TASK
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        "- REQ-36: fixture requirement 36\n", ""
                    ),
                    encoding="utf-8",
                )
            elif case == "task-extra-requirement":
                path = fixture.root / TASK
                path.write_text(
                    path.read_text(encoding="utf-8")
                    + "\n- REQ-37: forbidden extra requirement\n",
                    encoding="utf-8",
                )
            elif case == "task-not-36-of-36":
                path = fixture.root / TASK
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        "36/36 requirements verified.",
                        "35/36 requirements verified.",
                    ),
                    encoding="utf-8",
                )
            elif case == "renamed-readme":
                (fixture.root / NEW_PACK / "README.md").rename(
                    fixture.root / NEW_PACK / "OVERVIEW.md"
                )
                commit_fixture_change(fixture, NEW_PACK)
            elif case == "twenty-one-leaves-without-readme-file":
                readme = fixture.root / NEW_PACK / "README.md"
                holding = fixture.root / NEW_PACK / ".readme-fixture"
                readme.rename(holding)
                readme.mkdir()
                holding.rename(readme / "content.md")
                commit_fixture_change(fixture, NEW_PACK)
            else:
                raise AssertionError(case)

        for case in (
            "spec-missing-requirement",
            "spec-extra-requirement",
            "task-missing-requirement",
            "task-extra-requirement",
            "task-not-36-of-36",
            "renamed-readme",
            "twenty-one-leaves-without-readme-file",
        ):
            with self.subTest(mode="build", drift=case):
                with tempfile.TemporaryDirectory(
                    prefix="gate9-semantic-build-"
                ) as temporary:
                    fixture = Gate9Fixture(pathlib.Path(temporary))
                    try:
                        mutate(fixture, case)
                        result = fixture.build_process()
                        if result.returncode == 0:
                            fixture.bundle_paths.append(
                                pathlib.Path(json.loads(result.stdout)["bundle_path"])
                            )
                        self.assertNotEqual(
                            0,
                            result.returncode,
                            f"build accepted {case}: {result.stdout}",
                        )
                        expected = (
                            "PACK_CARDINALITY"
                            if case
                            in {
                                "renamed-readme",
                                "twenty-one-leaves-without-readme-file",
                            }
                            else "PACKAGE_SEMANTIC_DRIFT"
                        )
                        self.assertIn(expected, result.stderr)
                    finally:
                        fixture.cleanup()

        module = load_helper("gate9_shared_semantic_replay")
        receipt = self.fixture.build()
        attachments = self.fixture.attachments(receipt)
        candidate = attachments["task-candidate.md"].replace(
            b"36/36 requirements verified.", b"35/36 requirements verified."
        )
        self.assertNotEqual(attachments["task-candidate.md"], candidate)
        attachments["task-candidate.md"] = candidate
        attachments["task-before-to-candidate.patch"] = task_transition_patch(
            self.root, attachments["task-before.md"], candidate
        )
        package_payloads = {
            name: value
            for name, value in attachments.items()
            if name not in {"SHA256SUMS", "package.json"}
        }
        package_document = json.loads(attachments["package.json"])
        package_document["attachments"] = module.package_records(package_payloads)
        attachments["package.json"] = canonical_json(package_document)
        attachments["SHA256SUMS"] = module.checksum_manifest(
            {
                name: value
                for name, value in attachments.items()
                if name != "SHA256SUMS"
            }
        )
        _, malformed_receipt = self.fixture.rewritten_bundle(receipt, attachments)

        with self.subTest(mode="bundle-replay", drift="task-not-36-of-36"):
            replay = self.verify_bundle(malformed_receipt)
            self.assertNotEqual(0, replay.returncode, replay.stdout)
            self.assertIn("PACKAGE_SEMANTIC_DRIFT", replay.stderr)

        _, evidence_ref = self.fixture.authorize(receipt)
        evidence_commit, leaves = module.read_ref_leaves(self.root, evidence_ref)
        forged_leaves = dict(leaves)
        for name, value in attachments.items():
            forged_leaves[f"package/{name}"] = value
        forged_leaves["SHA256SUMS"] = module.checksum_manifest(
            {
                name: value
                for name, value in forged_leaves.items()
                if name != "SHA256SUMS"
            }
        )
        parent, _, message = module.commit_identity(self.root, evidence_commit)
        forged_tree = module._evidence_tree(self.root, forged_leaves)
        forged_commit = git(
            self.root,
            "commit-tree",
            forged_tree,
            "-p",
            parent,
            input_bytes=message,
        ).stdout.decode().strip()
        git(
            self.root,
            "update-ref",
            evidence_ref,
            forged_commit,
            evidence_commit,
        )
        with self.subTest(mode="ref-replay", drift="task-not-36-of-36"):
            replay = self.verify_authorized(evidence_ref)
            self.assertNotEqual(0, replay.returncode, replay.stdout)
            self.assertIn("PACKAGE_SEMANTIC_DRIFT", replay.stderr)

    def test_all_public_modes_preserve_repository_and_lifecycle_invariants(
        self,
    ) -> None:
        module = load_helper("gate9_control_file_once")
        control = self.root / "control-once.json"
        moved = self.root / "control-original.json"
        original = canonical_json({"schema": SCHEMA, "value": "original"})
        forged = canonical_json({"schema": SCHEMA, "value": "forged"})
        control.write_bytes(original)
        real_open = module.os.open
        real_read = module.os.read
        control_opens = 0
        substituted = False

        def observed_open(*args: object, **kwargs: object) -> int:
            nonlocal control_opens
            if args and pathlib.Path(args[0]) == control:
                control_opens += 1
                if control_opens > 1:
                    raise AssertionError("control path reopened")
            return real_open(*args, **kwargs)

        def substitute_after_open(descriptor: int, count: int) -> bytes:
            nonlocal substituted
            if not substituted:
                control.rename(moved)
                control.write_bytes(forged)
                substituted = True
            return real_read(descriptor, count)

        with mock.patch.object(module.os, "open", side_effect=observed_open), mock.patch.object(
            module.os, "read", side_effect=substitute_after_open
        ):
            frozen = module.read_control_file_once(control, "test control")
        self.assertEqual(1, control_opens)
        self.assertEqual(original, frozen.value)
        self.assertEqual(forged, control.read_bytes())
        control.unlink()
        moved.unlink()

        initial = self.fixture.repository_state()
        receipt = self.fixture.build()
        self.assertEqual(initial, self.fixture.repository_state())
        self.assertEqual(0, self.verify_bundle(receipt).returncode)
        self.assertEqual(initial, self.fixture.repository_state())

        materials = self.fixture.review_materials(receipt)
        linked_attestation = self.root / "evidence/assignment-hardlink.json"
        os.link(materials["attestation"], linked_attestation)
        rejected_control = self.verify_assignments(receipt, materials)
        self.assert_fails(rejected_control, "CONTROL_FILE_DRIFT")
        linked_attestation.unlink()
        self.assertEqual(0, self.verify_assignments(receipt, materials).returncode)
        self.assertEqual(initial, self.fixture.repository_state())
        self.assertEqual(
            0,
            self.verify_backfill(receipt, materials, "PACKAGE_REVIEWED").returncode,
        )
        self.assertEqual(initial, self.fixture.repository_state())

        self.fixture.backfill_task(receipt, materials)
        task_only = self.fixture.repository_state()
        self.assertEqual(initial["head"], task_only["head"])
        self.assertEqual(initial["index"], task_only["index"])
        self.assertEqual(initial["old_tree"], task_only["old_tree"])
        self.assertEqual(initial["protected"], task_only["protected"])
        self.assertEqual(initial["worktrees"], task_only["worktrees"])
        self.fixture.closure_materials(receipt, materials)
        published = self.fixture.publish(receipt, materials)
        self.assertEqual(0, published.returncode, published.stderr)
        after_publish = self.fixture.repository_state()
        for key in ("head", "index", "old_tree", "protected", "worktrees"):
            self.assertEqual(task_only[key], after_publish[key])
        self.assertNotEqual(task_only["refs"], after_publish["refs"])
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        self.fixture.hide_control_files()
        self.assertEqual(0, self.verify_authorized(evidence_ref, receipt=receipt).returncode)
        self.assertEqual(0, self.verify_authorized(evidence_ref).returncode)
        self.assertEqual(after_publish, self.fixture.repository_state())

    def test_build_and_verify_canonical_bundle_without_repository_mutation(self) -> None:
        before = self.fixture.repository_state()
        receipt = self.fixture.build()
        self.assertEqual(before, self.fixture.repository_state())
        result = self.verify_bundle(receipt)
        self.assertEqual(0, result.returncode, result.stderr)
        verified = json.loads(result.stdout)
        self.assertEqual("VERIFIED", verified["state"])
        self.assertEqual(receipt["package_sha256"], verified["package_sha256"])
        self.assertEqual(receipt["bundle_sha256"], verified["bundle_sha256"])
        self.assertEqual(before, self.fixture.repository_state())

    def test_bundle_verification_rejects_byte_schema_and_mode_drift(self) -> None:
        receipt = self.fixture.build()
        attachments = self.fixture.attachments(receipt)
        attachments["plan.md"] += b"forged\n"
        forged_path, forged_receipt = self.fixture.rewritten_bundle(
            receipt, attachments
        )
        del forged_path
        result = self.fixture.run(
            "verify-package", *expected_transport(forged_receipt)
        )
        self.assertNotEqual(0, result.returncode)
        self.assertRegex(result.stderr, r"BUNDLE_SCHEMA_DRIFT|CHECKSUM_DRIFT|PACKAGE_SEMANTIC_DRIFT")

        path = pathlib.Path(receipt["bundle_path"])
        path.chmod(0o644)
        try:
            result = self.verify_bundle(receipt)
            self.assert_fails(result, "BUNDLE_READ_FAILURE")
        finally:
            path.chmod(0o444)

        document = self.fixture.read_bundle(receipt)
        document["attachments"][0]["base64"] = document["attachments"][0]["base64"].rstrip("=")
        noncanonical = self.fixture.write_bundle(document)
        result = self.fixture.run(
            "verify-package",
            "--bundle",
            os.fspath(noncanonical),
            "--expected-bundle-sha256",
            sha256_bytes(noncanonical.read_bytes()),
            "--expected-package-sha256",
            str(document["package_sha256"]),
        )
        self.assert_fails(result, "BUNDLE_SCHEMA_DRIFT")

    def test_build_rejects_dirty_real_index_and_third_attempt(self) -> None:
        git(self.root, "add", TASK)
        dirty = self.fixture.build_process()
        self.assertNotEqual(0, dirty.returncode)
        self.assertRegex(dirty.stderr, r"DIRTY_REAL_INDEX|REAL_INDEX_DRIFT")
        git(self.root, "reset", "--quiet", "HEAD", "--", TASK)
        third = self.fixture.build_process(3)
        self.assert_fails(third, "THIRD_ATTEMPT")

    def test_assignment_and_backfill_reject_identity_bundle_and_finding_drift(
        self,
    ) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        attestation = json.loads(materials["attestation"].read_bytes())
        attestation["assignments"][1]["agent_id"] = attestation["assignments"][0]["agent_id"]
        materials["attestation"].write_bytes(canonical_json(attestation))
        self.assert_fails(self.verify_assignments(receipt, materials), "INVALID_ATTESTATION")

        materials = self.fixture.review_materials(receipt)
        review_path = materials["quality-receipt"]
        review = json.loads(review_path.read_bytes())
        review["bundle_sha256"] = "0" * 64
        review_path.write_bytes(canonical_json(review))
        result = self.verify_backfill(receipt, materials, "PACKAGE_REVIEWED")
        self.assertNotEqual(0, result.returncode)
        self.assertRegex(
            result.stderr,
            r"BUNDLE_TRANSPORT_DRIFT|INVALID_RECEIPT|RECEIPT_BINDING_DRIFT",
        )

        materials = self.fixture.review_materials(receipt)
        review_path = materials["quality-receipt"]
        review = json.loads(review_path.read_bytes())
        review["findings"]["critical"] = True
        review_path.write_bytes(canonical_json(review))
        result = self.verify_backfill(receipt, materials, "PACKAGE_REVIEWED")
        self.assertNotEqual(0, result.returncode)
        self.assertRegex(result.stderr, r"INVALID_FINDING_COUNT|INVALID_RECEIPT")

    def test_task_backfill_accepts_marker_only_transition_and_rejects_other_edits(
        self,
    ) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        self.assertEqual(
            0,
            self.verify_backfill(receipt, materials, "PACKAGE_REVIEWED").returncode,
        )
        self.fixture.backfill_task(receipt, materials)
        accepted = self.verify_backfill(receipt, materials, "TASK_BACKFILLED")
        self.assertEqual(0, accepted.returncode, accepted.stderr)
        task_path = self.root / TASK
        task_path.write_bytes(task_path.read_bytes() + b"outside-marker drift\n")
        rejected = self.verify_backfill(receipt, materials, "TASK_BACKFILLED")
        self.assertNotEqual(0, rejected.returncode)
        self.assertRegex(
            rejected.stderr,
            r"TASK_PATCH_DRIFT|INVALID_TASK_MARKER|TASK_OUTSIDE_MARKER_DRIFT",
        )

    def test_authorized_publication_is_create_only_idempotent_and_ref_replayable(
        self,
    ) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        self.fixture.backfill_task(receipt, materials)
        self.fixture.closure_materials(receipt, materials)
        before = self.fixture.repository_state()
        first = self.fixture.publish(receipt, materials)
        self.assertEqual(0, first.returncode, first.stderr)
        first_record = json.loads(first.stdout)
        second = self.fixture.publish(receipt, materials)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(first_record, json.loads(second.stdout))
        after = self.fixture.repository_state()
        for key in ("head", "index", "old_tree", "protected", "worktrees"):
            self.assertEqual(before[key], after[key])
        self.fixture.hide_control_files()
        self.assertEqual(
            0,
            self.verify_authorized(first_record["evidence_ref"], receipt=receipt).returncode,
        )
        self.assertEqual(0, self.verify_authorized(first_record["evidence_ref"]).returncode)

    def test_concurrent_create_race_reuses_identical_tuple_without_drift(self) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        self.fixture.backfill_task(receipt, materials)
        self.fixture.closure_materials(receipt, materials)
        environment = self.fixture.git_wrapper(
            "create-race",
            'if [[ "$1" == update-ref && "${2:-}" == --no-deref && "${5:-}" == 0000000000000000000000000000000000000000 ]]; then\n'
            '  "$REAL_GIT" "$@"\n'
            '  touch "$GATE9_WRAPPER_MARKER"\n'
            "  exit 73\n"
            "fi\n"
            'exec "$REAL_GIT" "$@"\n',
        )
        before = self.fixture.repository_state()
        result = self.fixture.publish(receipt, materials, env=environment)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(pathlib.Path(environment["GATE9_WRAPPER_MARKER"]).is_file())
        after = self.fixture.repository_state()
        for key in ("head", "index", "old_tree", "protected", "worktrees"):
            self.assertEqual(before[key], after[key])
        self.assertNotEqual(before["refs"], after["refs"])

    def test_publication_rejects_nonidentical_existing_ref(self) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        self.fixture.backfill_task(receipt, materials)
        self.fixture.closure_materials(receipt, materials)
        package_id = receipt["package_sha256"]
        evidence_ref = (
            "refs/codex/review-evidence/agentic-research/gate9/v1/"
            f"attempt-1/{package_id}"
        )
        git(self.root, "update-ref", evidence_ref, self.fixture.head)
        before = self.fixture.repository_state()
        result = self.fixture.publish(receipt, materials)
        self.assert_fails(result, "FOREIGN_REF")
        self.assertEqual(before, self.fixture.repository_state())

    def test_rejected_terminal_requires_a_load_bearing_review_finding(self) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        no_finding = self.fixture.publish(receipt, materials, state="REJECTED")
        self.assertNotEqual(0, no_finding.returncode)
        self.assertRegex(no_finding.stderr, r"REJECTED_WITHOUT_FINDING|INVALID_TERMINAL_STATE")

        quality_path = materials["quality-receipt"]
        quality = json.loads(quality_path.read_bytes())
        quality["findings"]["important"] = 1
        quality["verdict"] = "Needs fixes"
        quality_path.write_bytes(canonical_json(quality))
        rejected = self.fixture.publish(receipt, materials, state="REJECTED")
        self.assertEqual(0, rejected.returncode, rejected.stderr)
        record = json.loads(rejected.stdout)
        self.assertEqual("REJECTED", record["state"])
        self.assertIn("/attempt-1/", record["evidence_ref"])

    def test_invalidated_evidence_requires_nonempty_bound_reason(self) -> None:
        receipt = self.fixture.build()
        materials = self.fixture.review_materials(receipt)
        drift = self.fixture.write_json(
            "evidence/empty-drift.json",
            {
                "kind": "drift-proof",
                "reason": "",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        result = self.fixture.publish(
            receipt, materials, state="INVALIDATED", drift_proof=drift
        )
        self.assertNotEqual(0, result.returncode)
        self.assertRegex(
            result.stderr,
            r"INVALID_DRIFT_PROOF|INVALIDATED_REASON_INVALID|EMPTY_TERMINAL_REASON",
        )

    def test_invalidated_attempt_one_authorizes_exactly_one_bound_attempt_two(
        self,
    ) -> None:
        second, first_ref = self.fixture.build_attempt_two()
        self.assertIn("/attempt-1/", first_ref)
        self.assertEqual("BUILT", second["state"])
        self.assertNotEqual(second["package_sha256"], first_ref.rsplit("/", 1)[-1])
        wrong = self.fixture.build_process(1)
        self.assertNotEqual(0, wrong.returncode)
        self.assertRegex(wrong.stderr, r"ATTEMPT_STATE_MISMATCH|ATTEMPT_PREHISTORY_DRIFT")
        third = self.fixture.build_process(3)
        self.assert_fails(third, "THIRD_ATTEMPT")

    def test_package_authority_requires_live_binding_and_unambiguous_history(self) -> None:
        missing = self.fixture.run(
            "build-package",
            "--attempt",
            "1",
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
            bind_live=False,
        )
        self.assert_fails(missing, "LIVE_HEAD_REQUIRED")
        abbreviated = self.fixture.run(
            "build-package",
            "--require-live-head",
            "--live-reviewed-head",
            self.fixture.head[:12],
            "--reviewed-code-head",
            self.fixture.reviewed_code_head,
            "--attempt",
            "1",
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
            bind_live=False,
        )
        self.assert_fails(abbreviated, "LIVE_HEAD_REQUIRED")

        common_dir = pathlib.Path(
            git(
                self.root, "rev-parse", "--path-format=absolute", "--git-common-dir"
            ).stdout.decode().strip()
        )
        replace = common_dir / f"refs/replace/{self.fixture.head}"
        replace.parent.mkdir(parents=True, exist_ok=True)
        replace.write_text(f"{self.fixture.reviewed_code_head}\n", encoding="ascii")
        try:
            result = self.fixture.build_process()
            self.assert_fails(result, "AMBIGUOUS_GIT_HISTORY")
        finally:
            replace.unlink(missing_ok=True)

    def test_evidence_ref_replay_and_discovery_reject_symbolic_and_substituted_refs(
        self,
    ) -> None:
        module = load_helper("gate9_replay_ref_identity")
        for malformed in (
            f"{module.REF_PREFIX}/attempt-1/{'a' * 63}",
            f"{module.REF_PREFIX}/attempt-1/{'a' * 64}/suffix",
            f"{module.REF_PREFIX}/attempt-3/{'a' * 64}",
            f"{module.REF_PREFIX}/attempt-1/{'A' * 64}",
        ):
            with self.subTest(case="resolve-pattern", evidence_ref=malformed):
                caught: object | None = None
                try:
                    module.resolve_evidence_ref(
                        {"evidence_ref": malformed}, "auto"
                    )
                except module.Gate9Error as error:
                    caught = error
                self.assertIsNotNone(caught, "noncanonical marker ref was accepted")
                self.assertEqual("INVALID_TASK_MARKER", caught.code)

        with tempfile.TemporaryDirectory(
            prefix="gate9-ref-replay-identity-"
        ) as temporary:
            fixture = Gate9Fixture(pathlib.Path(temporary))
            try:
                receipt = fixture.build()
                _, evidence_ref = fixture.authorize(receipt)
                evidence_commit = (
                    git(
                        fixture.root,
                        "show-ref",
                        "--verify",
                        "--hash",
                        evidence_ref,
                    )
                    .stdout.decode()
                    .strip()
                )

                with self.subTest(case="read-ref-leaves-symbolic-outside"):
                    outside = "refs/heads/gate9-outside-replay"
                    git(fixture.root, "update-ref", outside, evidence_commit)
                    git(fixture.root, "update-ref", "-d", evidence_ref)
                    git(fixture.root, "symbolic-ref", evidence_ref, outside)
                    resolve_caught: object | None = None
                    caught = None
                    try:
                        with mock.patch.object(
                            module, "repository_root", return_value=fixture.root
                        ):
                            try:
                                module.resolve_evidence_ref(
                                    {"evidence_ref": evidence_ref}, "auto"
                                )
                            except module.Gate9Error as error:
                                resolve_caught = error
                        self.assertIsNotNone(
                            resolve_caught,
                            "marker resolution accepted an outside symbolic target",
                        )
                        self.assertEqual("FOREIGN_REF", resolve_caught.code)
                        try:
                            module.read_ref_leaves(fixture.root, evidence_ref)
                        except module.Gate9Error as error:
                            caught = error
                        self.assertIsNotNone(
                            caught, "ref leaf load accepted an outside symbolic target"
                        )
                        self.assertEqual("FOREIGN_REF", caught.code)
                        self.assertEqual(
                            evidence_commit,
                            git(fixture.root, "rev-parse", outside)
                            .stdout.decode()
                            .strip(),
                        )
                    finally:
                        git(
                            fixture.root,
                            "symbolic-ref",
                            "--delete",
                            evidence_ref,
                            check=False,
                        )
                        git(fixture.root, "update-ref", evidence_ref, evidence_commit)
                        git(fixture.root, "update-ref", "-d", outside, check=False)

                with self.subTest(case="read-ref-leaves-substitution"):
                    parent, tree, message = module.commit_identity(
                        fixture.root, evidence_commit
                    )
                    del parent
                    replacement = (
                        git(
                            fixture.root,
                            "commit-tree",
                            tree,
                            "-p",
                            evidence_commit,
                            input_bytes=message,
                        )
                        .stdout.decode()
                        .strip()
                    )
                    real_run_git = module.run_git
                    substituted = False

                    def substitute_during_leaf_load(
                        root: pathlib.Path,
                        arguments: list[str],
                        **kwargs: object,
                    ) -> subprocess.CompletedProcess[bytes]:
                        nonlocal substituted
                        if (
                            not substituted
                            and arguments
                            and arguments[0] == "ls-tree"
                            and evidence_commit in arguments
                        ):
                            substituted = True
                            real_run_git(
                                root,
                                [
                                    "update-ref",
                                    "--no-deref",
                                    evidence_ref,
                                    replacement,
                                    evidence_commit,
                                ],
                            )
                        return real_run_git(root, arguments, **kwargs)

                    caught = None
                    try:
                        with mock.patch.object(
                            module,
                            "run_git",
                            side_effect=substitute_during_leaf_load,
                        ):
                            try:
                                module.read_ref_leaves(fixture.root, evidence_ref)
                            except module.Gate9Error as error:
                                caught = error
                        self.assertTrue(substituted)
                        self.assertIsNotNone(
                            caught, "ref identity changed during leaf load"
                        )
                        self.assertEqual("FOREIGN_REF", caught.code)
                    finally:
                        git(
                            fixture.root,
                            "update-ref",
                            "--no-deref",
                            evidence_ref,
                            evidence_commit,
                            replacement,
                            check=False,
                        )

                with self.subTest(case="existing-ref-discovery-symbolic-outside"):
                    outside = "refs/heads/gate9-outside-discovery"
                    symbolic = f"{module.REF_PREFIX}/attempt-1/{'c' * 64}"
                    git(fixture.root, "update-ref", outside, evidence_commit)
                    git(fixture.root, "symbolic-ref", symbolic, outside)
                    caught = None
                    try:
                        try:
                            module.existing_evidence_refs(fixture.root)
                        except module.Gate9Error as error:
                            caught = error
                        self.assertIsNotNone(
                            caught, "evidence discovery accepted a symbolic ref"
                        )
                        self.assertEqual("FOREIGN_REF", caught.code)
                        self.assertEqual(
                            outside,
                            git(fixture.root, "symbolic-ref", "-q", symbolic)
                            .stdout.decode()
                            .strip(),
                        )
                    finally:
                        git(
                            fixture.root,
                            "symbolic-ref",
                            "--delete",
                            symbolic,
                            check=False,
                        )
                        git(fixture.root, "update-ref", "-d", outside, check=False)
            finally:
                fixture.cleanup()

    def test_evidence_ref_creation_rejects_symbolic_and_outside_namespace_refs(
        self,
    ) -> None:
        module = load_helper("gate9_symbolic_ref_contract")
        tree = module.build_tree_from_mapping(
            self.root, {"evidence.json": ("100644", b"{}\n")}
        )
        message = module.evidence_commit_message(1, "a" * 64, "AUTHORIZED")
        desired = git(
            self.root,
            "commit-tree",
            tree,
            "-p",
            self.fixture.head,
            input_bytes=message,
        ).stdout.decode().strip()

        with self.subTest(case="preexisting-symbolic-ref"):
            target = "refs/heads/gate9-symbolic-target"
            evidence_ref = f"{module.REF_PREFIX}/attempt-1/{'a' * 64}"
            git(self.root, "update-ref", target, desired)
            git(self.root, "symbolic-ref", evidence_ref, target)
            caught: object | None = None
            try:
                try:
                    module.create_or_reuse_ref(
                        self.root,
                        evidence_ref,
                        self.fixture.head,
                        tree,
                        message,
                    )
                except module.Gate9Error as error:
                    caught = error
                self.assertIsNotNone(caught, "symbolic evidence ref was reused")
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(
                    target,
                    git(self.root, "symbolic-ref", "-q", evidence_ref)
                    .stdout.decode()
                    .strip(),
                )
            finally:
                git(self.root, "symbolic-ref", "--delete", evidence_ref, check=False)
                git(self.root, "update-ref", "-d", target, check=False)

        with self.subTest(case="dangling-symbolic-ref-does-not-create-target"):
            target = "refs/heads/gate9-dangling-target"
            evidence_ref = f"{module.REF_PREFIX}/attempt-1/{'c' * 64}"
            git(self.root, "symbolic-ref", evidence_ref, target)
            caught = None
            try:
                try:
                    module.create_or_reuse_ref(
                        self.root,
                        evidence_ref,
                        self.fixture.head,
                        tree,
                        message,
                    )
                except module.Gate9Error as error:
                    caught = error
                self.assertIsNotNone(caught, "dangling symbolic ref was dereferenced")
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertNotEqual(
                    0,
                    git(self.root, "show-ref", "--verify", target, check=False).returncode,
                    "symbolic update created an outside-namespace target",
                )
            finally:
                git(self.root, "symbolic-ref", "--delete", evidence_ref, check=False)
                git(self.root, "update-ref", "-d", target, check=False)

        with self.subTest(case="symbolic-update-ref-race"):
            target = "refs/heads/gate9-race-target"
            evidence_ref = f"{module.REF_PREFIX}/attempt-1/{'b' * 64}"
            git(self.root, "update-ref", target, desired)
            real_run_git = module.run_git
            raced = False

            def symbolic_race(
                root: pathlib.Path,
                arguments: list[str],
                **kwargs: object,
            ) -> subprocess.CompletedProcess[bytes]:
                nonlocal raced
                if (
                    not raced
                    and arguments
                    and arguments[0] == "update-ref"
                    and evidence_ref in arguments
                ):
                    raced = True
                    real_run_git(root, ["symbolic-ref", evidence_ref, target])
                    return subprocess.CompletedProcess(
                        ["git", *arguments], 1, b"", b"injected symbolic race\n"
                    )
                return real_run_git(root, arguments, **kwargs)

            caught = None
            try:
                with mock.patch.object(module, "run_git", side_effect=symbolic_race):
                    try:
                        module.create_or_reuse_ref(
                            self.root,
                            evidence_ref,
                            self.fixture.head,
                            tree,
                            message,
                        )
                    except module.Gate9Error as error:
                        caught = error
                self.assertTrue(raced)
                self.assertIsNotNone(caught, "symbolic CAS race was reused")
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(
                    target,
                    git(self.root, "symbolic-ref", "-q", evidence_ref)
                    .stdout.decode()
                    .strip(),
                )
            finally:
                git(self.root, "symbolic-ref", "--delete", evidence_ref, check=False)
                git(self.root, "update-ref", "-d", target, check=False)

        with self.subTest(case="outside-namespace"):
            outside_ref = "refs/heads/gate9-outside-namespace"
            caught = None
            try:
                try:
                    module.create_or_reuse_ref(
                        self.root,
                        outside_ref,
                        self.fixture.head,
                        tree,
                        message,
                    )
                except module.Gate9Error as error:
                    caught = error
                self.assertIsNotNone(caught, "outside-namespace ref was created")
                self.assertEqual("FOREIGN_REF", caught.code)
            finally:
                git(self.root, "update-ref", "-d", outside_ref, check=False)

        source = HELPER.read_text(encoding="utf-8")
        syntax = ast.parse(source)
        create_source = next(
            ast.get_source_segment(source, node)
            for node in syntax.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "create_or_reuse_ref"
        )
        assert create_source is not None
        with self.subTest(case="no-deref-zero-oid-cas"):
            self.assertIn('"--no-deref"', create_source)
            self.assertIn('"0" * width', create_source)
            self.assertNotIn('"update-ref", evidence_ref, commit', create_source)

    def test_create_only_ref_uses_repository_object_width(self) -> None:
        module = load_helper("gate9_sha256_ref")
        sha256_root = self.root / "sha256-repository"
        sha256_root.mkdir()
        initialized = git(
            sha256_root,
            "init",
            "--quiet",
            "--object-format=sha256",
            check=False,
        )
        if initialized.returncode != 0:
            self.skipTest("installed Git does not support SHA-256 repositories")
        git(sha256_root, "config", "user.name", "Gate Nine SHA256")
        git(sha256_root, "config", "user.email", "gate9-sha256@example.invalid")
        (sha256_root / "root.txt").write_text("root\n", encoding="utf-8")
        git(sha256_root, "add", "root.txt")
        git(sha256_root, "commit", "--quiet", "-m", "sha256 root")
        parent = git(sha256_root, "rev-parse", "HEAD").stdout.decode().strip()
        tree = module.build_tree_from_mapping(
            sha256_root, {"evidence.txt": ("100644", b"evidence\n")}
        )
        evidence_ref = (
            "refs/codex/review-evidence/agentic-research/gate9/v1/"
            f"attempt-1/{'d' * 64}"
        )
        message = b"test-sha256-evidence\n"
        commit = module.create_or_reuse_ref(
            sha256_root, evidence_ref, parent, tree, message
        )
        self.assertEqual(64, len(commit))
        self.assertEqual(
            commit,
            git(sha256_root, "rev-parse", evidence_ref).stdout.decode().strip(),
        )
        self.assertEqual(
            commit,
            module.create_or_reuse_ref(
                sha256_root, evidence_ref, parent, tree, message
            ),
        )

    def _external_consumer_invocations(
        self,
        materials: Mapping[str, pathlib.Path],
        transport: list[str],
    ) -> dict[str, list[str]]:
        terminal = self.root / "evidence/terminal.md"
        terminal.parent.mkdir(parents=True, exist_ok=True)
        terminal.write_text("AUTHORIZED\n", encoding="utf-8")
        return {
            "verify-package": ["verify-package", *transport],
            "verify-assignments": [
                "verify-assignments",
                *transport,
                "--attestation",
                os.fspath(materials["attestation"]),
            ],
            "verify-backfill": [
                "verify-backfill",
                *transport,
                "--migration-receipt",
                os.fspath(materials["migration-specification-receipt"]),
                "--quality-receipt",
                os.fspath(materials["quality-receipt"]),
                "--assignment-attestation",
                os.fspath(materials["attestation"]),
                "--task",
                TASK,
                "--expect-state",
                "TASK_BACKFILLED",
            ],
            "publish-evidence-ref": [
                "publish-evidence-ref",
                *transport,
                "--task",
                TASK,
                "--terminal-state",
                "AUTHORIZED",
                "--terminal-report",
                os.fspath(terminal),
                "--assignment-attestation",
                os.fspath(materials["attestation"]),
                "--migration-report",
                os.fspath(materials["migration-specification-report"]),
                "--migration-receipt",
                os.fspath(materials["migration-specification-receipt"]),
                "--quality-report",
                os.fspath(materials["quality-report"]),
                "--quality-receipt",
                os.fspath(materials["quality-receipt"]),
                "--migration-closure-report",
                os.fspath(materials["migration-specification-closure-report"]),
                "--migration-closure",
                os.fspath(materials["migration-specification-closure"]),
                "--quality-closure-report",
                os.fspath(materials["quality-closure-report"]),
                "--quality-closure",
                os.fspath(materials["quality-closure"]),
                "--evidence-ref",
                "auto",
            ],
            "verify-authorized": [
                "verify-authorized",
                *transport,
                "--task",
                TASK,
                "--evidence-ref",
                "auto",
            ],
        }

    def test_all_external_bundle_consumers_reject_post_publication_transport_drift_before_authority(
        self,
    ) -> None:
        fixture = self.fixture
        receipt = fixture.build()
        materials = fixture.review_materials(receipt)
        fixture.backfill_task(receipt, materials)
        fixture.closure_materials(receipt, materials)
        first_path = pathlib.Path(os.fspath(receipt["bundle_path"]))

        attachments = dict(fixture.attachments(receipt))
        attachments["plan.md"] = attachments["plan.md"] + b"second canonical bundle\n"
        attachments["SHA256SUMS"] = b"".join(
            f"{sha256_bytes(attachments[name])}  {name}\n".encode()
            for name in sorted(attachments)
            if name != "SHA256SUMS"
        )
        second_value, second_digest = fixture.canonical_bundle(attachments)
        second_document = json.loads(second_value)
        second_path = fixture.write_bundle(second_document)
        self.assertNotEqual(receipt["bundle_sha256"], second_digest)
        self.assertNotEqual(
            receipt["package_sha256"], second_document["package_sha256"]
        )
        os.rename(second_path, first_path)
        self.assertEqual(second_value, first_path.read_bytes())

        transport = [
            "--bundle",
            os.fspath(first_path),
            "--expected-bundle-sha256",
            str(receipt["bundle_sha256"]),
            "--expected-package-sha256",
            str(receipt["package_sha256"]),
        ]
        forbidden = {
            "cat-file",
            "commit-tree",
            "diff",
            "for-each-ref",
            "hash-object",
            "ls-tree",
            "merge-base",
            "mktree",
            "symbolic-ref",
            "update-ref",
        }
        invocations = self._external_consumer_invocations(materials, transport)
        before = fixture.repository_state()
        for mode, arguments in invocations.items():
            with self.subTest(consumer=mode):
                environment = fixture.git_wrapper(
                    f"transport-{mode}",
                    'printf "%s\\n" "$1" >> "$GATE9_WRAPPER_MARKER"\n'
                    'exec "$REAL_GIT" "$@"\n',
                )
                log = pathlib.Path(environment["GATE9_WRAPPER_MARKER"])
                calls_before = fixture.generator_calls()
                result = fixture.run(*arguments, env=environment, timeout=120)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertTrue(
                    result.stderr.splitlines()[0].startswith(
                        "BUNDLE_TRANSPORT_DRIFT: "
                    ),
                    result.stderr,
                )
                observed = (
                    [line.strip() for line in log.read_text().splitlines()]
                    if log.exists()
                    else []
                )
                self.assertFalse(
                    forbidden.intersection(observed),
                    f"{mode} reached {sorted(forbidden.intersection(observed))} "
                    "before the transport check",
                )
                self.assertEqual(calls_before, fixture.generator_calls())
                after = fixture.repository_state()
                self.assertEqual(before, after)

        with self.subTest(parser="transport-group"):
            base = os.fspath(first_path)
            good_bundle = str(receipt["bundle_sha256"])
            good_package = str(receipt["package_sha256"])
            cases = {
                "both-missing": ["--bundle", base],
                "bundle-hash-missing": [
                    "--bundle",
                    base,
                    "--expected-package-sha256",
                    good_package,
                ],
                "package-hash-missing": [
                    "--bundle",
                    base,
                    "--expected-bundle-sha256",
                    good_bundle,
                ],
                "duplicate-bundle-hash": [
                    "--bundle",
                    base,
                    "--expected-bundle-sha256",
                    good_bundle,
                    "--expected-bundle-sha256",
                    good_bundle,
                    "--expected-package-sha256",
                    good_package,
                ],
                "uppercase-hex": [
                    "--bundle",
                    base,
                    "--expected-bundle-sha256",
                    good_bundle.upper(),
                    "--expected-package-sha256",
                    good_package,
                ],
                "short-hex": [
                    "--bundle",
                    base,
                    "--expected-bundle-sha256",
                    good_bundle[:63],
                    "--expected-package-sha256",
                    good_package,
                ],
                "nonhex": [
                    "--bundle",
                    base,
                    "--expected-bundle-sha256",
                    "z" * 64,
                    "--expected-package-sha256",
                    good_package,
                ],
            }
            for label, source in cases.items():
                for mode in (
                    "verify-package",
                    "verify-assignments",
                    "verify-backfill",
                    "publish-evidence-ref",
                    "verify-authorized",
                ):
                    with self.subTest(parser=label, consumer=mode):
                        arguments = list(invocations[mode])
                        head = arguments[0]
                        tail = arguments[1 + len(transport) :]
                        result = fixture.run(head, *source, *tail, timeout=120)
                        self.assertEqual(1, result.returncode, result.stdout)
                        self.assertEqual("", result.stdout)
                        self.assertTrue(
                            result.stderr.splitlines()[0].startswith(
                                "BUNDLE_TRANSPORT_USAGE: "
                            ),
                            result.stderr,
                        )
            for label, source in (
                (
                    "ref-source-with-bundle-hash",
                    [
                        "--bundle-from-ref",
                        "--expected-bundle-sha256",
                        good_bundle,
                    ],
                ),
                (
                    "ref-source-with-package-hash",
                    [
                        "--bundle-from-ref",
                        "--expected-package-sha256",
                        good_package,
                    ],
                ),
            ):
                with self.subTest(parser=label):
                    result = fixture.run(
                        "verify-authorized",
                        *source,
                        "--task",
                        TASK,
                        "--evidence-ref",
                        "auto",
                        timeout=120,
                    )
                    self.assertEqual(1, result.returncode, result.stdout)
                    self.assertEqual("", result.stdout)
                    self.assertTrue(
                        result.stderr.splitlines()[0].startswith(
                            "BUNDLE_TRANSPORT_USAGE: "
                        ),
                        result.stderr,
                    )

    def _gate9_namespace(self, attempt: int = 1) -> pathlib.Path:
        return (
            self.root
            / ".git/refs/codex/review-evidence/agentic-research/gate9/v1"
            / f"attempt-{attempt}"
        )

    def _namespace_inventory(self) -> dict[str, object]:
        prefix = b"refs/codex/review-evidence/agentic-research/gate9/v1/"
        rows = git(
            self.root,
            "for-each-ref",
            "--format=%(refname) %(objectname) %(symref)",
        ).stdout.splitlines()
        return {
            "objects": sorted(
                git(
                    self.root,
                    "cat-file",
                    "--batch-all-objects",
                    "--batch-check=%(objectname) %(objecttype)",
                ).stdout.splitlines()
            ),
            "outside_refs": sorted(
                row for row in rows if not row.startswith(prefix)
            ),
        }

    def _plant_victim(self) -> tuple[pathlib.Path, bytes]:
        victim = pathlib.Path(
            f"/tmp/gate9-discovery-victim-{secrets.token_hex(16)}.txt"
        )
        payload = b"discovery victim must remain byte-identical\n"
        victim.write_bytes(payload)
        self.addCleanup(victim.unlink, missing_ok=True)
        return victim, payload

    def test_evidence_ref_discovery_finds_dangling_loose_symbolic_refs_and_stays_stable(
        self,
    ) -> None:
        module = load_helper("gate9_raw_evidence_ref_discovery")
        fixture = self.fixture
        namespace = self._gate9_namespace()
        namespace.mkdir(parents=True, exist_ok=True)
        canonical = "a" * 64
        victim, victim_bytes = self._plant_victim()
        blob = (
            git(fixture.root, "hash-object", "-w", "--stdin", input_bytes=b"blob\n")
            .stdout.decode()
            .strip()
        )

        def clear_namespace() -> None:
            if namespace.exists():
                for child in sorted(namespace.rglob("*"), reverse=True):
                    if child.is_dir() and not child.is_symlink():
                        child.rmdir()
                    else:
                        child.unlink()
            namespace.mkdir(parents=True, exist_ok=True)

        def discovery_error() -> object | None:
            try:
                module.existing_evidence_refs(fixture.root)
            except module.Gate9Error as error:
                return error
            return None

        with self.subTest(case="dangling-loose-symbolic-ref"):
            leaf = namespace / canonical
            leaf.write_bytes(b"ref: refs/heads/gate9-absent-target\n")
            try:
                listed = git(
                    fixture.root,
                    "for-each-ref",
                    "--format=%(refname)",
                    f"{module.REF_PREFIX}/",
                )
                self.assertEqual(b"", listed.stdout)
                self.assertEqual(b"", listed.stderr)
                before = self._namespace_inventory()
                caught = discovery_error()
                self.assertIsNotNone(
                    caught,
                    "for-each-ref omits a dangling loose symbolic ref, so raw "
                    "discovery must reject it",
                )
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(before, self._namespace_inventory())
                self.assertEqual(victim_bytes, victim.read_bytes())
            finally:
                clear_namespace()

        for label, relative, payload in (
            ("malformed-name", "NOT-SIXTY-FOUR-HEX", f"{fixture.head}\n"),
            ("uppercase-name", "A" * 64, f"{fixture.head}\n"),
            ("extra-depth", f"{canonical}/suffix", f"{fixture.head}\n"),
            ("short-oid", canonical, f"{fixture.head[:-1]}\n"),
            ("noncommit-oid", canonical, f"{blob}\n"),
            ("missing-terminator", canonical, fixture.head),
        ):
            with self.subTest(case=label):
                target = namespace / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(payload, encoding="ascii")
                try:
                    caught = discovery_error()
                    self.assertIsNotNone(caught, f"{label} was admitted")
                    self.assertEqual("FOREIGN_REF", caught.code)
                finally:
                    clear_namespace()

        with self.subTest(case="filesystem-symlink-leaf"):
            leaf = namespace / canonical
            os.symlink(os.fspath(victim), leaf)
            try:
                caught = discovery_error()
                self.assertIsNotNone(caught, "a symlink leaf was admitted")
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(victim_bytes, victim.read_bytes())
            finally:
                clear_namespace()

        with self.subTest(case="fifo-leaf-before-open"):
            leaf = namespace / canonical
            os.mkfifo(leaf)
            environment = fixture.git_wrapper(
                "discovery-fifo",
                'printf "%s\\n" "$*" >> "$GATE9_WRAPPER_MARKER"\n'
                'exec "$REAL_GIT" "$@"\n',
            )
            log = pathlib.Path(environment["GATE9_WRAPPER_MARKER"])
            try:
                result = fixture.build_process(env=environment, timeout=20)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertTrue(
                    result.stderr.splitlines()[0].startswith("FOREIGN_REF: "),
                    result.stderr,
                )
                lines = log.read_text().splitlines() if log.exists() else []
                reopened = [
                    line
                    for line in lines
                    if canonical in line
                    or (
                        module.REF_PREFIX in line
                        and line.split(" ", 1)[0]
                        in {"for-each-ref", "symbolic-ref", "update-ref"}
                    )
                ]
                self.assertEqual(
                    [], reopened, "discovery reopened the FIFO evidence leaf"
                )
            finally:
                clear_namespace()

        with self.subTest(case="substitution-between-snapshots"):
            leaf = namespace / canonical
            leaf.write_text(f"{fixture.head}\n", encoding="ascii")
            replacement = (
                git(
                    fixture.root,
                    "commit-tree",
                    git(fixture.root, "rev-parse", "HEAD^{tree}")
                    .stdout.decode()
                    .strip(),
                    "-p",
                    fixture.head,
                    input_bytes=b"substituted evidence commit\n",
                )
                .stdout.decode()
                .strip()
            )
            git(fixture.root, "update-ref", "refs/heads/gate9-substitute", replacement)
            before = self._namespace_inventory()
            real_run_git = module.run_git
            snapshots = {"count": 0}

            def substitute_between_snapshots(
                root: pathlib.Path,
                arguments: Sequence[str],
                **kwargs: object,
            ) -> subprocess.CompletedProcess[bytes]:
                result = real_run_git(root, arguments, **kwargs)
                if (
                    arguments
                    and arguments[0] == "for-each-ref"
                    and any(module.REF_PREFIX in value for value in arguments)
                ):
                    snapshots["count"] += 1
                    if snapshots["count"] == 1:
                        leaf.write_text(f"{replacement}\n", encoding="ascii")
                return result

            try:
                with mock.patch.object(
                    module, "run_git", side_effect=substitute_between_snapshots
                ):
                    caught = discovery_error()
                self.assertGreaterEqual(snapshots["count"], 1)
                self.assertIsNotNone(
                    caught, "a leaf substituted between snapshots was admitted"
                )
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(victim_bytes, victim.read_bytes())
                after = self._namespace_inventory()
                self.assertEqual(before["objects"], after["objects"])
            finally:
                git(
                    fixture.root,
                    "update-ref",
                    "-d",
                    "refs/heads/gate9-substitute",
                    check=False,
                )
                clear_namespace()

        with self.subTest(case="raw-union-omission-clause"):
            leaf = namespace / canonical
            leaf.write_text(f"{fixture.head}\n", encoding="ascii")
            before = self._namespace_inventory()
            real_run_git = module.run_git
            observed: dict[str, object] = {"unlinked": False, "boundary": None}

            def unlink_before_for_each_ref(
                root: pathlib.Path,
                arguments: Sequence[str],
                **kwargs: object,
            ) -> subprocess.CompletedProcess[bytes]:
                if (
                    not observed["unlinked"]
                    and arguments
                    and arguments[0] == "for-each-ref"
                    and any(module.REF_PREFIX in value for value in arguments)
                ):
                    observed["unlinked"] = True
                    leaf.unlink()
                    result = real_run_git(root, arguments, **kwargs)
                    observed["boundary"] = (
                        result.returncode,
                        result.stdout,
                        result.stderr,
                    )
                    return result
                return real_run_git(root, arguments, **kwargs)

            try:
                with mock.patch.object(
                    module, "run_git", side_effect=unlink_before_for_each_ref
                ):
                    caught = discovery_error()
                self.assertTrue(observed["unlinked"])
                self.assertEqual(
                    (0, b"", b""),
                    observed["boundary"],
                    "the omission boundary invocation must exit zero with empty "
                    "stdout and stderr so no preserved guard can fire",
                )
                self.assertIsNotNone(
                    caught, "a one-sided raw membership was admitted"
                )
                self.assertEqual("FOREIGN_REF", caught.code)
                self.assertEqual(victim_bytes, victim.read_bytes())
                self.assertEqual(before, self._namespace_inventory())
            finally:
                clear_namespace()

    def test_evidence_ref_hazard_funnels_are_bounded_reaped_and_fail_closed(
        self,
    ) -> None:
        module = load_helper("gate9_hazard_funnels")
        fixture = self.fixture
        namespace = self._gate9_namespace()
        namespace.mkdir(parents=True, exist_ok=True)
        canonical = "b" * 64
        victim, victim_bytes = self._plant_victim()

        def clear_namespace() -> None:
            if namespace.exists():
                for child in sorted(namespace.rglob("*"), reverse=True):
                    if child.is_dir() and not child.is_symlink():
                        child.rmdir()
                    else:
                        child.unlink()
            namespace.mkdir(parents=True, exist_ok=True)

        with self.subTest(case="regular-raw-direct-snapshot-succeeds"):
            leaf = namespace / canonical
            leaf.write_text(f"{fixture.head}\n", encoding="ascii")
            git(
                fixture.root,
                "update-ref",
                f"{module.REF_PREFIX}/attempt-1/{canonical}",
                fixture.head,
            )
            try:
                self.assertEqual(
                    [f"{module.REF_PREFIX}/attempt-1/{canonical}"],
                    module.existing_evidence_refs(fixture.root),
                )
            finally:
                git(
                    fixture.root,
                    "update-ref",
                    "-d",
                    f"{module.REF_PREFIX}/attempt-1/{canonical}",
                    check=False,
                )
                clear_namespace()

        with self.subTest(case="measured-for-each-ref-baseline"):
            namespace.mkdir(parents=True, exist_ok=True)
            leaf = namespace / canonical
            os.mkfifo(leaf)
            try:
                started = time.monotonic()
                baseline = git(
                    fixture.root,
                    "for-each-ref",
                    "--format=%(refname)",
                    f"{module.REF_PREFIX}/attempt-1/{canonical}",
                    check=False,
                )
                elapsed = time.monotonic() - started
                self.assertEqual(0, baseline.returncode)
                self.assertEqual(b"", baseline.stdout)
                self.assertEqual(b"", baseline.stderr)
                self.assertLess(elapsed, 2.0)
            finally:
                clear_namespace()

        with self.subTest(case="sub-case-1-pre-snapshot-fifo"):
            namespace.mkdir(parents=True, exist_ok=True)
            leaf = namespace / canonical
            os.mkfifo(leaf)
            environment = fixture.git_wrapper(
                "pre-snapshot-fifo",
                'printf "%s\\n" "$*" >> "$GATE9_WRAPPER_MARKER"\n'
                'exec "$REAL_GIT" "$@"\n',
            )
            log = pathlib.Path(environment["GATE9_WRAPPER_MARKER"])
            try:
                started = time.monotonic()
                result = fixture.build_process(env=environment, timeout=60)
                elapsed = time.monotonic() - started
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertTrue(
                    result.stderr.splitlines()[0].startswith("FOREIGN_REF: "),
                    result.stderr,
                )
                lines = log.read_text().splitlines() if log.exists() else []
                namespace_calls = [
                    line
                    for line in lines
                    if module.REF_PREFIX in line
                    and line.split(" ", 1)[0]
                    in {"for-each-ref", "symbolic-ref", "update-ref"}
                ]
                self.assertEqual([], namespace_calls)
                self.assertEqual([], sorted(namespace.glob("*.lock")))
                self.assertLess(
                    elapsed,
                    30.0,
                    "the pre-snapshot FIFO must be rejected without a funnel bound",
                )
            finally:
                clear_namespace()

        with self.subTest(case="sub-case-3-create-only-cas-funnel"):
            task_before_publish = (self.root / TASK).read_bytes()
            receipt = fixture.build()
            materials = fixture.review_materials(receipt)
            fixture.backfill_task(receipt, materials)
            fixture.closure_materials(receipt, materials)
            namespace.mkdir(parents=True, exist_ok=True)
            leaf_name = str(receipt["package_sha256"])
            leaf = namespace / leaf_name
            before = self._namespace_inventory()
            spawned: list[int] = []
            real_popen = module.subprocess.Popen
            real_run_git = module.run_git

            def recording_popen(*args: object, **kwargs: object) -> object:
                process = real_popen(*args, **kwargs)
                spawned.append(process.pid)
                return process

            def inject_fifo_at_commit_tree(
                root: pathlib.Path,
                arguments: Sequence[str],
                **kwargs: object,
            ) -> subprocess.CompletedProcess[bytes]:
                if arguments and arguments[0] == "commit-tree" and not leaf.exists():
                    leaf.parent.mkdir(parents=True, exist_ok=True)
                    os.mkfifo(leaf)
                return real_run_git(root, arguments, **kwargs)

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            previous = os.getcwd()
            terminal = self.root / "evidence/terminal.md"
            terminal.parent.mkdir(parents=True, exist_ok=True)
            terminal.write_text("AUTHORIZED\n", encoding="utf-8")
            argv = [
                os.fspath(HELPER),
                "publish-evidence-ref",
                "--require-live-head",
                "--live-reviewed-head",
                fixture.head,
                "--reviewed-code-head",
                fixture.reviewed_code_head,
                "--bundle",
                os.fspath(receipt["bundle_path"]),
                "--expected-bundle-sha256",
                str(receipt["bundle_sha256"]),
                "--expected-package-sha256",
                str(receipt["package_sha256"]),
                "--task",
                TASK,
                "--terminal-state",
                "AUTHORIZED",
                "--terminal-report",
                os.fspath(terminal),
                "--assignment-attestation",
                os.fspath(materials["attestation"]),
                "--migration-report",
                os.fspath(materials["migration-specification-report"]),
                "--migration-receipt",
                os.fspath(materials["migration-specification-receipt"]),
                "--quality-report",
                os.fspath(materials["quality-report"]),
                "--quality-receipt",
                os.fspath(materials["quality-receipt"]),
                "--migration-closure-report",
                os.fspath(materials["migration-specification-closure-report"]),
                "--migration-closure",
                os.fspath(materials["migration-specification-closure"]),
                "--quality-closure-report",
                os.fspath(materials["quality-closure-report"]),
                "--quality-closure",
                os.fspath(materials["quality-closure"]),
                "--evidence-ref",
                "auto",
            ]
            try:
                os.chdir(fixture.root)
                started = time.monotonic()
                with mock.patch.object(
                    module.subprocess, "Popen", side_effect=recording_popen
                ), mock.patch.object(
                    module, "run_git", side_effect=inject_fifo_at_commit_tree
                ), mock.patch.object(
                    module.sys, "argv", argv
                ), contextlib.redirect_stdout(
                    stdout_buffer
                ), contextlib.redirect_stderr(
                    stderr_buffer
                ):
                    status = module.main()
                elapsed = time.monotonic() - started
            finally:
                os.chdir(previous)
                fixture.hide_control_files()
                (self.root / TASK).write_bytes(task_before_publish)
            self.assertTrue(leaf.is_fifo(), "the mid-flight FIFO was not injected")
            self.assertEqual(1, status)
            self.assertEqual("", stdout_buffer.getvalue())
            first_line = stderr_buffer.getvalue().splitlines()[0]
            self.assertRegex(first_line, r"^[A-Z][A-Z0-9_]*: .+")
            self.assertGreaterEqual(
                elapsed, 2.0, "funnel 1 returned before its 2.0-second bound expired"
            )
            self.assertLess(elapsed, 30.0)
            self.assertTrue(spawned, "no funnel-1 child was recorded")
            blocked_pid = spawned[-1]
            self.assertFalse(
                pathlib.Path(f"/proc/{blocked_pid}").exists(),
                "the blocked funnel-1 child is still present",
            )
            with self.assertRaises(ChildProcessError):
                os.waitpid(blocked_pid, os.WNOHANG)
            after = self._namespace_inventory()
            self.assertEqual(before["outside_refs"], after["outside_refs"])
            self.assertEqual(victim_bytes, victim.read_bytes())
            leaf.unlink()
            clear_namespace()
            fixture.hide_control_files()

        for variant, payload in (
            ("empty", b""),
            ("full-width-oid", f"{fixture.head}\n".encode()),
        ):
            with self.subTest(case="sub-case-4-lock-residue", variant=variant):
                namespace.mkdir(parents=True, exist_ok=True)
                lock = namespace / f"{canonical}.lock"
                lock.write_bytes(payload)
                lock_before = (
                    lock.lstat().st_mode,
                    lock.lstat().st_size,
                    lock.lstat().st_mtime_ns,
                    lock.read_bytes(),
                )
                before = self._namespace_inventory()
                state_before = fixture.repository_state()
                try:
                    result = fixture.build_process(timeout=60)
                    self.assertEqual(1, result.returncode, result.stdout)
                    self.assertEqual("", result.stdout)
                    first_line = result.stderr.splitlines()[0]
                    self.assertTrue(
                        first_line.startswith("STALE_REF_LOCK: "), result.stderr
                    )
                    self.assertIn(os.fspath(lock), result.stderr)
                    self.assertTrue(lock.exists(), "the lock residue was removed")
                    self.assertEqual(
                        lock_before,
                        (
                            lock.lstat().st_mode,
                            lock.lstat().st_size,
                            lock.lstat().st_mtime_ns,
                            lock.read_bytes(),
                        ),
                    )
                    self.assertFalse((namespace / canonical).exists())
                    self.assertEqual(before, self._namespace_inventory())
                    self.assertEqual(state_before, fixture.repository_state())
                    self.assertEqual(victim_bytes, victim.read_bytes())
                finally:
                    clear_namespace()

        with self.subTest(case="sub-case-5-control-file-fifo"):
            receipt = fixture.build()
            control = self.root / "evidence/fifo-attestation.json"
            control.parent.mkdir(parents=True, exist_ok=True)
            os.mkfifo(control)
            try:
                started = time.monotonic()
                result = fixture.run(
                    "verify-assignments",
                    "--bundle",
                    os.fspath(receipt["bundle_path"]),
                    "--expected-bundle-sha256",
                    str(receipt["bundle_sha256"]),
                    "--expected-package-sha256",
                    str(receipt["package_sha256"]),
                    "--attestation",
                    os.fspath(control),
                    timeout=60,
                )
                elapsed = time.monotonic() - started
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertRegex(
                    result.stderr.splitlines()[0], r"^[A-Z][A-Z0-9_]*: .+"
                )
                self.assertLess(elapsed, 30.0)
            finally:
                control.unlink()
                fixture.hide_control_files()

        with self.subTest(case="sub-case-5-whole-file-fifo"):
            fifo_task = self.root / "docs/04.execution/tasks/gate9-fifo-task.md"
            fifo_task.parent.mkdir(parents=True, exist_ok=True)
            os.mkfifo(fifo_task)
            try:
                started = time.monotonic()
                result = fixture.run(
                    "verify-authorized",
                    "--bundle-from-ref",
                    "--task",
                    "docs/04.execution/tasks/gate9-fifo-task.md",
                    "--evidence-ref",
                    "auto",
                    timeout=60,
                )
                elapsed = time.monotonic() - started
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertRegex(
                    result.stderr.splitlines()[0], r"^[A-Z][A-Z0-9_]*: .+"
                )
                self.assertLess(elapsed, 30.0)
            finally:
                fifo_task.unlink()

        for variant in ("fifo", "dangling-symlink"):
            with self.subTest(case="sub-case-5-non-regular-index", variant=variant):
                receipt = fixture.build()
                index_path = self.root / ".git/index"
                saved = index_path.read_bytes()
                index_path.unlink()
                if variant == "fifo":
                    os.mkfifo(index_path)
                else:
                    os.symlink(
                        os.fspath(self.root / ".git/gate9-absent-index"), index_path
                    )
                environment = fixture.git_wrapper(
                    f"index-guard-{variant}",
                    'printf "%s\\n" "$*" >> "$GATE9_WRAPPER_MARKER"\n'
                    'exec "$REAL_GIT" "$@"\n',
                )
                log = pathlib.Path(environment["GATE9_WRAPPER_MARKER"])
                try:
                    started = time.monotonic()
                    result = fixture.run(
                        "verify-package",
                        "--bundle",
                        os.fspath(receipt["bundle_path"]),
                        "--expected-bundle-sha256",
                        str(receipt["bundle_sha256"]),
                        "--expected-package-sha256",
                        str(receipt["package_sha256"]),
                        env=environment,
                        timeout=60,
                    )
                    elapsed = time.monotonic() - started
                    self.assertEqual(1, result.returncode, result.stdout)
                    self.assertEqual("", result.stdout)
                    self.assertRegex(
                        result.stderr.splitlines()[0], r"^[A-Z][A-Z0-9_]*: .+"
                    )
                    lines = log.read_text().splitlines() if log.exists() else []
                    index_readers = [
                        line
                        for line in lines
                        if line.split(" ", 1)[0] in {"diff", "status"}
                    ]
                    self.assertEqual(
                        [],
                        index_readers,
                        "the index guard must run before the first index-reading "
                        "Git invocation in the authority preflight",
                    )
                    self.assertLess(elapsed, 30.0)
                finally:
                    index_path.unlink()
                    index_path.write_bytes(saved)

        for injection, body in (
            (
                "nonzero-exit",
                'if [[ "$1" == for-each-ref && "$*" == *'
                "codex/review-evidence/agentic-research/gate9"
                '* ]]; then\n'
                '  "$REAL_GIT" "$@" || true\n'
                "  exit 41\n"
                "fi\n"
                'exec "$REAL_GIT" "$@"\n',
            ),
            (
                "stderr-with-zero-exit",
                'if [[ "$1" == for-each-ref && "$*" == *'
                "codex/review-evidence/agentic-research/gate9"
                '* ]]; then\n'
                '  "$REAL_GIT" "$@"\n'
                '  printf "advisory\\n" >&2\n'
                "  exit 0\n"
                "fi\n"
                'exec "$REAL_GIT" "$@"\n',
            ),
        ):
            with self.subTest(case="sub-case-6-injected-git-output", injection=injection):
                environment = fixture.git_wrapper(f"injected-{injection}", body)
                before = self._namespace_inventory()
                state_before = fixture.repository_state()
                result = fixture.build_process(env=environment, timeout=60)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertEqual("", result.stdout)
                self.assertTrue(
                    result.stderr.splitlines()[0].startswith("FOREIGN_REF: "),
                    result.stderr,
                )
                self.assertEqual(before, self._namespace_inventory())
                self.assertEqual(state_before, fixture.repository_state())
                self.assertEqual(victim_bytes, victim.read_bytes())
