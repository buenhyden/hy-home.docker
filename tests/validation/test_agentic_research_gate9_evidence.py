from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/validation/agentic-research-gate9-evidence.py"
SCHEMA = "agentic-research-gate9/v1"
OLD_PACK = "docs/90.references/research/2026-07-05-agentic-research-pack-refresh"
NEW_PACK = "docs/90.references/research/2026-08-08-agentic-engineering-research-pack"
TASK = "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
SPEC = "docs/03.specs/137-agentic-research-pack-rebuild/spec.md"
PLAN = "docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md"
INDEX = "docs/90.references/llm-wiki/llm-wiki-index.md"
COVERAGE = (
    "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md"
)
ROLES = ("migration-specification", "quality")
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


def regular_file_snapshot(path: pathlib.Path) -> tuple[int, int, int, bytes]:
    metadata = path.lstat()
    return (
        stat.S_IFMT(metadata.st_mode),
        stat.S_IMODE(metadata.st_mode),
        metadata.st_nlink,
        path.read_bytes(),
    )


def blob_oid(root: pathlib.Path, value: bytes) -> str:
    return subprocess.run(
        ["git", "hash-object", "--stdin"],
        cwd=root,
        input=value,
        capture_output=True,
        check=True,
    ).stdout.decode().strip()


def marker(payload: dict[str, object]) -> str:
    return (
        "<!-- GATE9-EVIDENCE/v1\n"
        + canonical_json(payload).decode()
        + "-->"
    )


def git(root: pathlib.Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=check,
    )


def task_transition_patch(root: pathlib.Path, before: bytes, after: bytes) -> bytes:
    with tempfile.TemporaryDirectory(prefix="gate9-task-patch-") as temporary:
        environment = os.environ.copy()
        environment["GIT_INDEX_FILE"] = os.fspath(pathlib.Path(temporary) / "index")

        def raw_git(*args: str, input_bytes: bytes | None = None) -> bytes:
            return subprocess.run(
                ["git", *args],
                cwd=root,
                env=environment,
                input=input_bytes,
                capture_output=True,
                check=True,
            ).stdout

        raw_git("read-tree", "--empty")
        before_oid = raw_git("hash-object", "-w", "--stdin", input_bytes=before).decode().strip()
        raw_git("update-index", "--add", "--cacheinfo", "100644", before_oid, TASK)
        before_tree = raw_git("write-tree").decode().strip()
        after_oid = raw_git("hash-object", "-w", "--stdin", input_bytes=after).decode().strip()
        raw_git("update-index", "--cacheinfo", "100644", after_oid, TASK)
        return raw_git("diff", "--cached", "--binary", "--full-index", before_tree, "--", TASK)


class Gate9Fixture:
    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.wrapper_dirs: list[pathlib.Path] = []
        git(root, "init", "--quiet")
        git(root, "config", "user.name", "Gate Nine Test")
        git(root, "config", "user.email", "gate9@example.invalid")
        for ordinal in range(20):
            self.write(f"{OLD_PACK}/file-{ordinal:02d}.md", f"old {ordinal}\n")
            self.write(f"{NEW_PACK}/file-{ordinal:02d}.md", f"new {ordinal}\n")
        self.write(SPEC, "# Spec\n")
        self.write(PLAN, "# Plan\n")
        self.write(INDEX, "fixed index\n")
        self.write(COVERAGE, "fixed coverage\n")
        self.write(
            "scripts/knowledge/generate-llm-wiki-index.sh",
            "#!/usr/bin/env bash\nset -eu\n"
            + "if [[ ${1:-} == --stdout && $# == 1 ]]; then printf 'fixed index\\n'; "
            + "elif [[ $# == 0 ]]; then printf 'fixed index\\n' > "
            + INDEX
            + "; else exit 2; fi\n",
            executable=True,
        )
        self.write(
            "scripts/knowledge/generate-llm-wiki-coverage.sh",
            "#!/usr/bin/env bash\nset -eu\n"
            + "if [[ ${1:-} == --stdout && $# == 1 ]]; then printf 'fixed coverage\\n'; "
            + "elif [[ $# == 0 ]]; then printf 'fixed coverage\\n' > "
            + COVERAGE
            + "; else exit 2; fi\n",
            executable=True,
        )
        self.pending_payload: dict[str, object] = {
            "attempt": 1,
            "schema": SCHEMA,
            "state": "PACKAGE_REVIEW_PENDING",
        }
        self.write(TASK, "# Task\n\n" + marker(self.pending_payload) + "\n")
        helper_path = self.root / HELPER.relative_to(ROOT)
        helper_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HELPER, helper_path)
        git(root, "add", ".")
        git(root, "commit", "--quiet", "-m", "fixture reviewed code")
        self.reviewed_code_head = git(root, "rev-parse", "HEAD").stdout.strip()
        task_path = root / TASK
        task_path.write_text(
            task_path.read_text(encoding="utf-8")
            + f"\nGATE9_REVIEWED_CODE_HEAD: `{self.reviewed_code_head}`\n",
            encoding="utf-8",
        )
        git(root, "add", TASK)
        git(root, "commit", "--quiet", "-m", "fixture reviewed closure")
        self.head = git(root, "rev-parse", "HEAD").stdout.strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8") + "\nCandidate gate results.\n",
            encoding="utf-8",
        )

    def write(self, relative: str, value: str, *, executable: bool = False) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        if executable:
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def run(
        self,
        *args: str,
        check: bool = False,
        env: dict[str, str] | None = None,
        bind_live: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        command_env = os.environ.copy()
        if env:
            command_env.update(env)
        command_args = list(args)
        if bind_live and command_args and command_args[0] in AUTHORITY_MODES:
            command_args[1:1] = [
                "--require-live-head",
                "--live-reviewed-head",
                self.head,
                "--reviewed-code-head",
                self.reviewed_code_head,
            ]
        return subprocess.run(
            ["python3", os.fspath(HELPER), *command_args],
            cwd=self.root,
            env=command_env,
            capture_output=True,
            text=True,
            check=check,
        )

    def build(self, output: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return self.run(
            "build-package",
            "--attempt",
            "1",
            "--output",
            os.fspath(output),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
        )

    def repository_state(self) -> dict[str, object]:
        protected_paths = (
            *(f"{OLD_PACK}/file-{ordinal:02d}.md" for ordinal in range(20)),
            INDEX,
            COVERAGE,
        )
        return {
            "head": git(self.root, "rev-parse", "HEAD").stdout,
            "index": regular_file_snapshot(self.root / ".git/index"),
            "old_tree": git(
                self.root, "ls-tree", "-r", "--full-tree", "HEAD", OLD_PACK
            ).stdout,
            "protected": {
                path: regular_file_snapshot(self.root / path)
                for path in protected_paths
            },
            "refs": git(
                self.root,
                "for-each-ref",
                "--format=%(refname) %(objectname)",
                "refs/codex/review-evidence/agentic-research/gate9/v1/",
            ).stdout,
            "worktrees": git(self.root, "worktree", "list", "--porcelain").stdout,
        }

    def advance_reviewed_generator(self, relative: str, value: str) -> None:
        task_path = self.root / TASK
        committed_task = subprocess.run(
            ["git", "show", f"HEAD:{TASK}"],
            cwd=self.root,
            capture_output=True,
            check=True,
        ).stdout
        task_path.write_bytes(committed_task)
        self.write(relative, value, executable=True)
        git(self.root, "add", relative)
        git(self.root, "commit", "--quiet", "-m", "fixture reviewed generator")
        old_reviewed = self.reviewed_code_head
        self.reviewed_code_head = git(
            self.root, "rev-parse", "HEAD"
        ).stdout.strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8").replace(
                old_reviewed, self.reviewed_code_head
            ),
            encoding="utf-8",
        )
        git(self.root, "add", TASK)
        git(self.root, "commit", "--quiet", "-m", "fixture reviewed closure")
        self.head = git(self.root, "rev-parse", "HEAD").stdout.strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8") + "\nCandidate gate results.\n",
            encoding="utf-8",
        )

    def authorize_package(
        self, package: pathlib.Path
    ) -> tuple[dict[str, pathlib.Path], str]:
        materials = self.review_materials(package)
        self.backfill_task(package, materials)
        self.closure_materials(package, materials)
        terminal = self.root / "evidence/terminal.md"
        terminal.write_text("AUTHORIZED\n", encoding="utf-8")
        published = self.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "AUTHORIZED",
            "--terminal-report",
            os.fspath(terminal),
            "--migration-report",
            os.fspath(materials["migration-specification-report"]),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-report",
            os.fspath(materials["quality-report"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
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
        )
        if published.returncode != 0:
            raise AssertionError(published.stderr)
        return materials, json.loads(published.stdout)["evidence_ref"]

    def build_attempt_two(self, output: pathlib.Path) -> tuple[pathlib.Path, str]:
        package_one = self.root / "attempt-one-package"
        built = self.build(package_one)
        assert built.returncode == 0, built.stderr
        materials = self.review_materials(package_one)
        terminal = self.root / "attempt-one-terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        drift = self.write_json(
            "attempt-one-drift.json",
            {
                "kind": "drift-proof",
                "reason": "fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        published = self.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package_one),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        assert published.returncode == 0, published.stderr
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        evidence_tree = git(
            self.root, "show", "-s", "--format=%T", evidence_ref
        ).stdout.strip()
        package_id = sha256_bytes((package_one / "SHA256SUMS").read_bytes())
        attempt_two_marker = {
            "attempt": 2,
            "attempt_1": {
                "evidence_ref": evidence_ref,
                "evidence_tree": evidence_tree,
                "package_sha256": package_id,
                "reason": "fixture drift",
                "terminal_state": "INVALIDATED",
            },
            "schema": SCHEMA,
            "state": "ATTEMPT_2_PENDING",
        }
        task_path = self.root / TASK
        task_path.write_bytes(
            task_path.read_bytes().replace(
                marker(self.pending_payload).encode(),
                marker(attempt_two_marker).encode(),
                1,
            )
        )
        shutil.rmtree(package_one)
        shutil.rmtree(self.root / "evidence")
        terminal.unlink()
        drift.unlink()
        built_two = self.run(
            "build-package",
            "--attempt",
            "2",
            "--output",
            os.fspath(output),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
        )
        assert built_two.returncode == 0, built_two.stderr
        return output, evidence_ref

    def write_json(self, relative: str, value: object) -> pathlib.Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json(value))
        return path

    def reseal_package(self, package: pathlib.Path) -> None:
        (package / "package.json").chmod(0o644)
        (package / "SHA256SUMS").chmod(0o644)
        package_document = json.loads((package / "package.json").read_text())
        package_document["attachments"] = [
            {
                "bytes": len((package / name).read_bytes()),
                "path": name,
                "sha256": sha256_bytes((package / name).read_bytes()),
            }
            for name in sorted(
                set(path.name for path in package.iterdir())
                - {"SHA256SUMS", "package.json"}
            )
        ]
        (package / "package.json").write_bytes(canonical_json(package_document))
        checksum_paths = sorted(
            set(path.name for path in package.iterdir()) - {"SHA256SUMS"}
        )
        (package / "SHA256SUMS").write_bytes(
            b"".join(
                f"{sha256_bytes((package / name).read_bytes())}  {name}\n".encode()
                for name in checksum_paths
            )
        )
        for path in package.iterdir():
            path.chmod(0o444)

    def git_wrapper(
        self,
        name: str,
        body: str,
    ) -> dict[str, str]:
        bin_dir = pathlib.Path(tempfile.mkdtemp(prefix=f"gate9-wrapper-{name}-"))
        self.wrapper_dirs.append(bin_dir)
        wrapper = bin_dir / "git"
        marker_path = bin_dir / "executed"
        real_git = shutil.which("git")
        assert real_git is not None
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
            "PATH": os.fspath(bin_dir) + os.pathsep + os.environ["PATH"],
        }

    def cleanup(self) -> None:
        for path in self.wrapper_dirs:
            shutil.rmtree(path, ignore_errors=True)

    def review_materials(self, package: pathlib.Path) -> dict[str, pathlib.Path]:
        package_id = sha256_bytes((package / "SHA256SUMS").read_bytes())
        assignments = json.loads((package / "assignments.json").read_text())
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
            "controller_task": "/root",
            "kind": "assignment-attestation",
            "package_head": self.head,
            "package_sha256": package_id,
            "schema": SCHEMA,
            "source": "collaboration.spawn_agent/result",
        }
        materials: dict[str, pathlib.Path] = {}
        materials["attestation"] = self.write_json("evidence/assignment.json", attestation)
        attestation_hash = sha256_bytes(materials["attestation"].read_bytes())
        for role in ROLES:
            report = self.root / f"evidence/{role}-report.md"
            report.write_text(f"# {role} review\n\nApproved C0/I0/M0.\n", encoding="utf-8")
            identity = next(row for row in attestation["assignments"] if row["role"] == role)
            receipt = {
                "agent_id": identity["agent_id"],
                "assignment_attestation_sha256": attestation_hash,
                "attempt": assignments["attempt"],
                "findings": {"critical": 0, "important": 0, "minor": 0},
                "kind": "package-review-receipt",
                "package_head": self.head,
                "package_sha256": package_id,
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
                f"evidence/{role}-receipt.json", receipt
            )
        return materials

    def backfill_task(
        self, package: pathlib.Path, materials: dict[str, pathlib.Path]
    ) -> bytes:
        candidate = (package / "task-candidate.md").read_bytes()
        package_id = sha256_bytes((package / "SHA256SUMS").read_bytes())
        candidate_match = re.search(
            rb"<!-- GATE9-EVIDENCE/v1\n(?P<payload>\{[^\r\n]*\}\n)-->",
            candidate,
        )
        assert candidate_match is not None
        candidate_marker = json.loads(candidate_match.group("payload"))
        attempt = candidate_marker["attempt"]
        review_records: dict[str, object] = {}
        for role in ROLES:
            receipt_path = materials[f"{role}-receipt"]
            receipt = json.loads(receipt_path.read_text())
            review_records[role] = {
                "agent_id": receipt["agent_id"],
                "assignment_attestation_sha256": receipt[
                    "assignment_attestation_sha256"
                ],
                "findings": receipt["findings"],
                "receipt_sha256": sha256_bytes(receipt_path.read_bytes()),
                "role": role,
                "run_id": receipt["run_id"],
                "task_path": receipt["task_path"],
                "verdict": receipt["verdict"],
            }
        payload = {
            "actual_committed_deletion_review": "Not Run",
            "actual_staged_deletion_review": "Not Run",
            "attempt": attempt,
            "evidence_ref": (
                "refs/codex/review-evidence/agentic-research/gate9/v1/"
                f"attempt-{attempt}/{package_id}"
            ),
            "new_manifest_sha256": sha256_bytes((package / "new-manifest.tsv").read_bytes()),
            "old_manifest_sha256": sha256_bytes((package / "old-manifest.tsv").read_bytes()),
            "package_sha256": package_id,
            "proposed_deletion_patch_sha256": sha256_bytes(
                (package / "proposed-deletion.patch").read_bytes()
            ),
            "recovery_head": self.head,
            "reviews": review_records,
            "schema": SCHEMA,
            "state": "TASK_BACKFILLED",
        }
        updated = candidate.replace(
            marker(candidate_marker).encode(), marker(payload).encode(), 1
        )
        (self.root / TASK).write_bytes(updated)
        return updated

    def closure_materials(
        self, package: pathlib.Path, materials: dict[str, pathlib.Path]
    ) -> None:
        candidate = (package / "task-candidate.md").read_bytes()
        task_after = (self.root / TASK).read_bytes()
        task_diff = task_transition_patch(self.root, candidate, task_after)
        tuple_record = {
            "after": {
                "blob_oid": blob_oid(self.root, task_after),
                "bytes": len(task_after),
                "sha256": sha256_bytes(task_after),
            },
            "before": {
                "blob_oid": blob_oid(self.root, candidate),
                "bytes": len(candidate),
                "sha256": sha256_bytes(candidate),
            },
            "diff": {"bytes": len(task_diff), "sha256": sha256_bytes(task_diff)},
        }
        attestation_hash = sha256_bytes(materials["attestation"].read_bytes())
        for role in ROLES:
            report = self.root / f"evidence/{role}-closure-report.md"
            report.write_text(f"# {role} closure\n\nMarker matches; non-marker unchanged.\n")
            receipt_path = materials[f"{role}-receipt"]
            receipt = json.loads(receipt_path.read_text())
            closure = {
                "agent_id": receipt["agent_id"],
                "assignment_attestation_sha256": attestation_hash,
                "attempt": receipt["attempt"],
                "findings": {"critical": 0, "important": 0, "minor": 0},
                "kind": "closure",
                "marker_match": True,
                "non_marker_unchanged": True,
                "package_receipt_sha256": sha256_bytes(receipt_path.read_bytes()),
                "package_sha256": receipt["package_sha256"],
                "report": {
                    "bytes": len(report.read_bytes()),
                    "sha256": sha256_bytes(report.read_bytes()),
                },
                "role": role,
                "run_id": receipt["run_id"],
                "schema": SCHEMA,
                "task": tuple_record,
                "task_path": receipt["task_path"],
                "verdict": "Approved",
            }
            materials[f"{role}-closure-report"] = report
            materials[f"{role}-closure"] = self.write_json(
                f"evidence/{role}-closure.json", closure
            )


class AgenticResearchGate9EvidenceTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="gate9-evidence-test-")
        self.root = pathlib.Path(self.temporary.name)
        self.fixture = Gate9Fixture(self.root)

    def tearDown(self) -> None:
        self.fixture.cleanup()
        self.temporary.cleanup()

    def test_build_and_verify_canonical_package_without_repository_mutation(self) -> None:
        before_head = git(self.root, "rev-parse", "HEAD").stdout
        before_index = git(self.root, "diff", "--cached", "--binary").stdout
        before_index_bytes = (self.root / ".git/index").read_bytes()
        before_old = git(self.root, "ls-tree", "-r", "--name-only", "HEAD", OLD_PACK).stdout
        protected_paths = (
            *(f"{OLD_PACK}/file-{ordinal:02d}.md" for ordinal in range(20)),
            INDEX,
            COVERAGE,
        )
        before_protected = {
            path: regular_file_snapshot(self.root / path) for path in protected_paths
        }
        package = self.root / "outside-package"

        built = self.fixture.build(package)
        self.assertEqual(0, built.returncode, built.stderr)
        verified = self.fixture.run(
            "verify-package", "--package", os.fspath(package), "--require-live-head"
        )
        self.assertEqual(0, verified.returncode, verified.stderr)

        self.assertEqual(before_head, git(self.root, "rev-parse", "HEAD").stdout)
        self.assertEqual(before_index, git(self.root, "diff", "--cached", "--binary").stdout)
        self.assertEqual(before_index_bytes, (self.root / ".git/index").read_bytes())
        self.assertEqual(
            before_old,
            git(self.root, "ls-tree", "-r", "--name-only", "HEAD", OLD_PACK).stdout,
        )
        self.assertEqual(
            before_protected,
            {
                path: regular_file_snapshot(self.root / path)
                for path in protected_paths
            },
        )
        self.assertEqual(
            {
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
            },
            {path.name for path in package.iterdir()},
        )
        for attachment in package.iterdir():
            self.assertEqual(0, attachment.stat().st_mode & 0o222, attachment.name)

    def test_package_verification_rejects_stale_head_and_byte_or_mode_drift(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        self.fixture.write("advance.txt", "advance\n")
        git(self.root, "add", "advance.txt")
        git(self.root, "commit", "--quiet", "-m", "advance")
        stale = self.fixture.run(
            "verify-package", "--package", os.fspath(package), "--require-live-head"
        )
        self.assertNotEqual(0, stale.returncode)
        self.assertIn("UNTRUSTED_PACKAGE_HEAD", stale.stderr)

        shutil.rmtree(package)
        self.fixture.head = git(self.root, "rev-parse", "HEAD").stdout.strip()
        fresh_package = self.root / "fresh-package"
        fresh = self.fixture.build(fresh_package)
        self.assertEqual(0, fresh.returncode, fresh.stderr)
        attachment = fresh_package / "spec.md"
        attachment.chmod(0o644)
        attachment.write_text("drift\n", encoding="utf-8")
        drift = self.fixture.run(
            "verify-package", "--package", os.fspath(fresh_package)
        )
        self.assertNotEqual(0, drift.returncode)
        self.assertRegex(drift.stderr, "(CHECKSUM_DRIFT|ATTACHMENT_MODE_DRIFT)")

    def test_package_verification_rejects_noncanonical_json_and_unsorted_checksums(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)

        assignments = package / "assignments.json"
        assignments.chmod(0o644)
        parsed = json.loads(assignments.read_text(encoding="utf-8"))
        assignments.write_text(json.dumps(parsed, indent=2) + "\n", encoding="utf-8")
        assignments.chmod(0o444)
        result = self.fixture.run("verify-package", "--package", os.fspath(package))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("NON_CANONICAL_JSON", result.stderr)

        shutil.rmtree(package)
        self.assertEqual(0, self.fixture.build(package).returncode)
        sums = package / "SHA256SUMS"
        sums.chmod(0o644)
        lines = sums.read_text(encoding="utf-8").splitlines(keepends=True)
        sums.write_text("".join(reversed(lines)), encoding="utf-8")
        sums.chmod(0o444)
        result = self.fixture.run("verify-package", "--package", os.fspath(package))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("UNSORTED_ATTACHMENTS", result.stderr)

    def test_build_rejects_dirty_real_index(self) -> None:
        git(self.root, "add", TASK)
        result = self.fixture.build(self.root / "package")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("DIRTY_REAL_INDEX", result.stderr)

    def test_build_rejects_third_attempt(self) -> None:
        result = self.fixture.run(
            "build-package",
            "--attempt",
            "3",
            "--output",
            os.fspath(self.root / "package"),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("THIRD_ATTEMPT", result.stderr)

    def test_assignment_and_backfill_validation_reject_identity_or_finding_drift(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        valid_assignment = self.fixture.run(
            "verify-assignments",
            "--package",
            os.fspath(package),
            "--attestation",
            os.fspath(materials["attestation"]),
        )
        self.assertEqual(0, valid_assignment.returncode, valid_assignment.stderr)
        valid_review = self.fixture.run(
            "verify-backfill",
            "--package",
            os.fspath(package),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--task",
            TASK,
            "--expect-state",
            "PACKAGE_REVIEWED",
        )
        self.assertEqual(0, valid_review.returncode, valid_review.stderr)

        attestation = json.loads(materials["attestation"].read_text())
        attestation["assignments"][1]["agent_id"] = attestation["assignments"][0]["agent_id"]
        materials["attestation"].write_bytes(canonical_json(attestation))
        duplicate = self.fixture.run(
            "verify-assignments",
            "--package",
            os.fspath(package),
            "--attestation",
            os.fspath(materials["attestation"]),
        )
        self.assertNotEqual(0, duplicate.returncode)
        self.assertIn("IDENTITY_COLLISION", duplicate.stderr)

        materials = self.fixture.review_materials(package)
        receipt_path = materials["quality-receipt"]
        receipt = json.loads(receipt_path.read_text())
        receipt["findings"]["important"] = 1
        receipt_path.write_bytes(canonical_json(receipt))
        finding = self.fixture.run(
            "verify-backfill",
            "--package",
            os.fspath(package),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-receipt",
            os.fspath(receipt_path),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--task",
            TASK,
            "--expect-state",
            "PACKAGE_REVIEWED",
        )
        self.assertNotEqual(0, finding.returncode)
        self.assertIn("LOAD_BEARING_FINDING", finding.stderr)

    def test_task_backfill_accepts_marker_only_transition_and_rejects_other_edits(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        self.fixture.backfill_task(package, materials)
        valid = self.fixture.run(
            "verify-backfill",
            "--package",
            os.fspath(package),
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
        )
        self.assertEqual(0, valid.returncode, valid.stderr)
        with (self.root / TASK).open("ab") as stream:
            stream.write(b"outside marker drift\n")
        invalid = self.fixture.run(
            "verify-backfill",
            "--package",
            os.fspath(package),
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
        )
        self.assertNotEqual(0, invalid.returncode)
        self.assertIn("TASK_OUTSIDE_MARKER_DRIFT", invalid.stderr)

    def test_authorized_publication_is_create_only_idempotent_and_ref_replayable(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        self.fixture.backfill_task(package, materials)
        self.fixture.closure_materials(package, materials)
        terminal = self.root / "evidence/terminal.md"
        terminal.write_text("AUTHORIZED\n", encoding="utf-8")
        publish_args = [
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "AUTHORIZED",
            "--terminal-report",
            os.fspath(terminal),
            "--migration-report",
            os.fspath(materials["migration-specification-report"]),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-report",
            os.fspath(materials["quality-report"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
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
        first = self.fixture.run(*publish_args)
        self.assertEqual(0, first.returncode, first.stderr)
        first_ref_value = git(
            self.root,
            "rev-parse",
            json.loads(first.stdout)["evidence_ref"],
        ).stdout.strip()
        retry = self.fixture.run(*publish_args)
        self.assertEqual(0, retry.returncode, retry.stderr)
        self.assertEqual(first_ref_value, json.loads(retry.stdout)["evidence_commit"])

        shutil.rmtree(package)
        shutil.rmtree(self.root / "evidence")
        from_ref = self.fixture.run(
            "verify-authorized",
            "--package-from-ref",
            "--task",
            TASK,
            "--evidence-ref",
            "auto",
            "--require-live-head",
            "--require-clean-real-index",
            "--require-task-only-worktree",
        )
        self.assertEqual(0, from_ref.returncode, from_ref.stderr)
        self.assertEqual("AUTHORIZED", json.loads(from_ref.stdout)["state"])

    def test_publication_rejects_nonidentical_existing_ref(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        package_id = sha256_bytes((package / "SHA256SUMS").read_bytes())
        evidence_ref = (
            "refs/codex/review-evidence/agentic-research/gate9/v1/"
            f"attempt-1/{package_id}"
        )
        git(self.root, "update-ref", evidence_ref, self.fixture.head)
        terminal = self.root / "terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        materials = self.fixture.review_materials(package)
        attestation = materials["attestation"]
        drift = self.fixture.write_json(
            "drift.json",
            {
                "kind": "drift-proof",
                "reason": "fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        collision = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(attestation),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        self.assertNotEqual(0, collision.returncode)
        self.assertIn("FOREIGN_REF", collision.stderr)

    def test_rejected_terminal_requires_a_load_bearing_review_finding(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        terminal = self.root / "terminal.md"
        terminal.write_text("REJECTED: package-review-rejected\n")
        result = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "REJECTED",
            "--terminal-report",
            os.fspath(terminal),
            "--migration-report",
            os.fspath(materials["migration-specification-report"]),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-report",
            os.fspath(materials["quality-report"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--evidence-ref",
            "auto",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("REJECTED_WITHOUT_FINDING", result.stderr)

    def test_invalidated_attempt_one_authorizes_exactly_one_bound_attempt_two(self) -> None:
        package = self.root / "package-one"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        package_id = sha256_bytes((package / "SHA256SUMS").read_bytes())
        terminal = self.root / "terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        drift = self.fixture.write_json(
            "drift.json",
            {
                "kind": "drift-proof",
                "reason": "fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        published = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        self.assertEqual(0, published.returncode, published.stderr)
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        evidence_tree = git(self.root, "show", "-s", "--format=%T", evidence_ref).stdout.strip()
        attempt_two_marker = {
            "attempt": 2,
            "attempt_1": {
                "evidence_ref": evidence_ref,
                "evidence_tree": evidence_tree,
                "package_sha256": package_id,
                "reason": "fixture drift",
                "terminal_state": "INVALIDATED",
            },
            "schema": SCHEMA,
            "state": "ATTEMPT_2_PENDING",
        }
        task_path = self.root / TASK
        task_path.write_bytes(
            task_path.read_bytes().replace(
                marker(self.fixture.pending_payload).encode(),
                marker(attempt_two_marker).encode(),
                1,
            )
        )
        shutil.rmtree(self.root / "evidence")
        terminal.unlink()
        drift.unlink()
        shutil.rmtree(package)

        package_two = self.root / "package-two"
        built = self.fixture.run(
            "build-package",
            "--attempt",
            "2",
            "--output",
            os.fspath(package_two),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
        )
        self.assertEqual(0, built.returncode, built.stderr)
        self.assertEqual(2, json.loads((package_two / "package.json").read_text())["attempt"])

    def test_invalidated_evidence_requires_nonempty_bound_reason(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        terminal = self.root / "terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        drift = self.fixture.write_json(
            "drift-missing.json",
            {"kind": "drift-proof", "schema": SCHEMA, "state": "INVALIDATED"},
        )
        result = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("INVALIDATED_REASON_INVALID", result.stderr)

    def test_invalidated_evidence_rejects_empty_reason(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        terminal = self.root / "terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        drift = self.fixture.write_json(
            "drift-empty.json",
            {
                "kind": "drift-proof",
                "reason": "",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        result = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("INVALIDATED_REASON_INVALID", result.stderr)

    def test_package_requires_exact_regular_0444_attachments(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        same_spec = self.root / "same-spec.md"
        same_spec.write_bytes((package / "spec.md").read_bytes())
        same_spec.chmod(0o444)

        for name, mutation, expected in (
            ("0400", lambda path: path.chmod(0o400), "ATTACHMENT_MODE_DRIFT"),
            ("0440", lambda path: path.chmod(0o440), "ATTACHMENT_MODE_DRIFT"),
            ("executable", lambda path: path.chmod(0o555), "ATTACHMENT_MODE_DRIFT"),
            (
                "directory",
                lambda path: (path.unlink(), path.mkdir()),
                "ATTACHMENT_TYPE_DRIFT",
            ),
            (
                "symlink",
                lambda path: (path.unlink(), path.symlink_to(same_spec)),
                "ATTACHMENT_TYPE_DRIFT",
            ),
        ):
            with self.subTest(name=name):
                candidate = self.root / f"mode-{name}"
                shutil.copytree(package, candidate)
                target = candidate / "spec.md"
                mutation(target)
                result = self.fixture.run(
                    "verify-package", "--package", os.fspath(candidate)
                )
                self.assertNotEqual(0, result.returncode, name)
                self.assertIn(expected, result.stderr)

    def test_package_replay_rederives_every_semantic_attachment(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)

        def trailing_deletion_patch(candidate: pathlib.Path) -> None:
            path = candidate / "proposed-deletion.patch"
            path.chmod(0o644)
            path.write_bytes(path.read_bytes() + b"forged trailing bytes\n")

        def false_gate(candidate: pathlib.Path) -> None:
            path = candidate / "gate-results.json"
            path.chmod(0o644)
            value = json.loads(path.read_text())
            value["gates"][3]["result"] = "FAIL"
            path.write_bytes(canonical_json(value))

        def forged_task_before(candidate: pathlib.Path) -> None:
            path = candidate / "task-before.md"
            path.chmod(0o644)
            path.write_bytes(b"# forged Task before\n")

        def forged_task_patch(candidate: pathlib.Path) -> None:
            path = candidate / "task-before-to-candidate.patch"
            path.chmod(0o644)
            path.write_bytes(path.read_bytes() + b"forged trailing bytes\n")

        def extra_package_key(candidate: pathlib.Path) -> None:
            path = candidate / "package.json"
            path.chmod(0o644)
            value = json.loads(path.read_text())
            value["unexpected"] = True
            path.write_bytes(canonical_json(value))

        for name, mutation in (
            ("deletion-patch", trailing_deletion_patch),
            ("gate-results", false_gate),
            ("task-before", forged_task_before),
            ("task-transition", forged_task_patch),
            ("package-schema", extra_package_key),
        ):
            with self.subTest(name=name):
                candidate = self.root / f"semantic-{name}"
                shutil.copytree(package, candidate)
                mutation(candidate)
                self.fixture.reseal_package(candidate)
                result = self.fixture.run(
                    "verify-package", "--package", os.fspath(candidate)
                )
                self.assertNotEqual(0, result.returncode, name)
                self.assertIn("PACKAGE_SEMANTIC_DRIFT", result.stderr)

    def test_boolean_finding_counts_are_rejected(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        receipt_path = materials["quality-receipt"]
        receipt = json.loads(receipt_path.read_text())
        receipt["findings"]["minor"] = True
        receipt_path.write_bytes(canonical_json(receipt))
        result = self.fixture.run(
            "verify-backfill",
            "--package",
            os.fspath(package),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-receipt",
            os.fspath(receipt_path),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--task",
            TASK,
            "--expect-state",
            "PACKAGE_REVIEWED",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("INVALID_RECEIPT", result.stderr)

    def test_attempt_two_rejects_forged_terminal_commit_message(self) -> None:
        package = self.root / "package-one"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        package_id = sha256_bytes((package / "SHA256SUMS").read_bytes())
        terminal = self.root / "terminal.md"
        terminal.write_text("INVALIDATED: fixture drift\n")
        drift = self.fixture.write_json(
            "drift.json",
            {
                "kind": "drift-proof",
                "reason": "fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        published = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "INVALIDATED",
            "--terminal-report",
            os.fspath(terminal),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
            "--drift-proof",
            os.fspath(drift),
            "--evidence-ref",
            "auto",
        )
        self.assertEqual(0, published.returncode, published.stderr)
        evidence_ref = json.loads(published.stdout)["evidence_ref"]
        evidence_tree = git(self.root, "show", "-s", "--format=%T", evidence_ref).stdout.strip()
        forged = subprocess.run(
            ["git", "commit-tree", evidence_tree, "-p", self.fixture.head],
            cwd=self.root,
            input="forged terminal message\n",
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        git(self.root, "update-ref", evidence_ref, forged)
        attempt_two_marker = {
            "attempt": 2,
            "attempt_1": {
                "evidence_ref": evidence_ref,
                "evidence_tree": evidence_tree,
                "package_sha256": package_id,
                "reason": "fixture drift",
                "terminal_state": "INVALIDATED",
            },
            "schema": SCHEMA,
            "state": "ATTEMPT_2_PENDING",
        }
        task_path = self.root / TASK
        task_path.write_bytes(
            task_path.read_bytes().replace(
                marker(self.fixture.pending_payload).encode(),
                marker(attempt_two_marker).encode(),
                1,
            )
        )
        shutil.rmtree(self.root / "evidence")
        terminal.unlink()
        drift.unlink()
        shutil.rmtree(package)
        result = self.fixture.run(
            "build-package",
            "--attempt",
            "2",
            "--output",
            os.fspath(self.root / "package-two"),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("EVIDENCE_COMMIT_IDENTITY_DRIFT", result.stderr)

    def test_attempt_two_later_modes_require_durable_attempt_one_prehistory(self) -> None:
        package, attempt_one_ref = self.fixture.build_attempt_two(
            self.root / "attempt-two-package"
        )
        materials = self.fixture.review_materials(package)
        terminal = self.root / "attempt-two-terminal.md"
        terminal.write_text("INVALIDATED: second fixture drift\n")
        drift = self.fixture.write_json(
            "attempt-two-drift.json",
            {
                "kind": "drift-proof",
                "reason": "second fixture drift",
                "schema": SCHEMA,
                "state": "INVALIDATED",
            },
        )
        attempt_one_tree = git(
            self.root, "show", "-s", "--format=%T", attempt_one_ref
        ).stdout.strip()
        git(self.root, "update-ref", "-d", attempt_one_ref)
        commands = {
            "verify-package": (
                "verify-package",
                "--package",
                os.fspath(package),
            ),
            "verify-assignments": (
                "verify-assignments",
                "--package",
                os.fspath(package),
                "--attestation",
                os.fspath(materials["attestation"]),
            ),
            "verify-backfill": (
                "verify-backfill",
                "--package",
                os.fspath(package),
                "--migration-receipt",
                os.fspath(materials["migration-specification-receipt"]),
                "--quality-receipt",
                os.fspath(materials["quality-receipt"]),
                "--assignment-attestation",
                os.fspath(materials["attestation"]),
                "--task",
                TASK,
                "--expect-state",
                "PACKAGE_REVIEWED",
            ),
            "publish-evidence-ref": (
                "publish-evidence-ref",
                "--package",
                os.fspath(package),
                "--task",
                TASK,
                "--terminal-state",
                "INVALIDATED",
                "--terminal-report",
                os.fspath(terminal),
                "--assignment-attestation",
                os.fspath(materials["attestation"]),
                "--drift-proof",
                os.fspath(drift),
                "--evidence-ref",
                "auto",
            ),
        }
        for prehistory in ("missing", "forged"):
            if prehistory == "forged":
                forged = subprocess.run(
                    ["git", "commit-tree", attempt_one_tree, "-p", self.fixture.head],
                    cwd=self.root,
                    input="forged attempt-one terminal\n",
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
                git(self.root, "update-ref", attempt_one_ref, forged)
            for name, command in commands.items():
                with self.subTest(prehistory=prehistory, name=name):
                    result = self.fixture.run(*command)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("ATTEMPT_PREHISTORY_INVALID", result.stderr)

    def test_authorized_replay_requires_durable_attempt_one_prehistory(self) -> None:
        package, attempt_one_ref = self.fixture.build_attempt_two(
            self.root / "attempt-two-package"
        )
        materials = self.fixture.review_materials(package)
        self.fixture.backfill_task(package, materials)
        self.fixture.closure_materials(package, materials)
        terminal = self.root / "attempt-two-terminal.md"
        terminal.write_text("AUTHORIZED\n")
        published = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "AUTHORIZED",
            "--terminal-report",
            os.fspath(terminal),
            "--migration-report",
            os.fspath(materials["migration-specification-report"]),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-report",
            os.fspath(materials["quality-report"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
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
        )
        self.assertEqual(0, published.returncode, published.stderr)
        attempt_one_tree = git(
            self.root, "show", "-s", "--format=%T", attempt_one_ref
        ).stdout.strip()
        forged = subprocess.run(
            ["git", "commit-tree", attempt_one_tree, "-p", self.fixture.head],
            cwd=self.root,
            input="forged attempt-one terminal\n",
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        for prehistory in ("forged", "missing"):
            if prehistory == "forged":
                git(self.root, "update-ref", attempt_one_ref, forged)
            else:
                git(self.root, "update-ref", "-d", attempt_one_ref)
            with self.subTest(prehistory=prehistory):
                result = self.fixture.run(
                    "verify-authorized",
                    "--package-from-ref",
                    "--task",
                    TASK,
                    "--evidence-ref",
                    "auto",
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("ATTEMPT_PREHISTORY_INVALID", result.stderr)

    def test_projected_index_proves_exact_twenty_deletions_without_worktree_mutation(
        self,
    ) -> None:
        before = self.fixture.repository_state()
        package = self.root / "step0d-package"
        built = self.fixture.build(package)
        self.assertEqual(0, built.returncode, built.stderr)
        patch = (package / "proposed-deletion.patch").read_bytes()
        self.assertEqual(20, patch.count(b"deleted file mode 100644"))
        for ordinal in range(20):
            self.assertIn(
                f"{OLD_PACK}/file-{ordinal:02d}.md".encode(),
                patch,
            )
        self.assertNotIn(SPEC.encode(), patch)
        self.assertEqual(before, self.fixture.repository_state())

        module_spec = importlib.util.spec_from_file_location("gate9_helper", HELPER)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        projector = getattr(module, "authoritative_projection", None)
        self.assertIsNotNone(projector, "Step 0d authoritative projector is missing")
        if projector is None:
            return
        projection = projector(
            self.root,
            self.fixture.head,
            self.fixture.head,
            self.fixture.reviewed_code_head,
        )
        expected_tree = git(
            self.root, "rev-parse", f"{self.fixture.head}^{{tree}}"
        ).stdout.strip()
        self.assertEqual(expected_tree, projection.initial_tree_oid)
        self.assertNotEqual(projection.initial_tree_oid, projection.final_tree_oid)
        self.assertEqual(20, len(projection.old_paths))
        self.assertEqual(
            tuple(("D", path) for path in projection.old_paths),
            projection.deletion_statuses,
        )

    def test_production_generator_grandchild_git_reads_pinned_projected_index(
        self,
    ) -> None:
        task_path = self.root / TASK
        task_path.write_bytes(
            subprocess.run(
                ["git", "show", f"HEAD:{TASK}"],
                cwd=self.root,
                capture_output=True,
                check=True,
            ).stdout
        )
        generator_paths = (
            "scripts/knowledge/generate-llm-wiki-index.sh",
            "scripts/knowledge/generate-llm-wiki-coverage.sh",
        )
        required_paths = (
            ".claude/agents/doc-writer.md",
            "docs/00.agent-governance/agents/agents/doc-writer.md",
            "docs/00.agent-governance/agents/functions/knowledge-map-agent.md",
            "docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md",
            "docs/90.references/data/knowledge/README.md",
            "docs/03.specs/096-llm-wiki-agent-first-completion/spec.md",
            "docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md",
            "docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md",
            "docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md",
            "docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md",
            "docs/04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md",
        )
        for relative in generator_paths:
            shutil.copy2(ROOT / relative, self.root / relative)
        for relative in required_paths:
            if not (self.root / relative).exists():
                self.fixture.write(relative, "# Fixture required path\n")
        git(self.root, "add", *generator_paths, *required_paths)

        rendered: dict[str, bytes] = {}
        for relative, output in zip(generator_paths, (INDEX, COVERAGE), strict=True):
            result = subprocess.run(
                ["bash", relative, "--stdout"],
                cwd=self.root,
                capture_output=True,
                check=True,
            )
            rendered[output] = result.stdout
            (self.root / output).write_bytes(result.stdout)
        git(self.root, "add", INDEX, COVERAGE)
        git(self.root, "commit", "--quiet", "-m", "fixture production generators")

        prior_reviewed_code_head = self.fixture.reviewed_code_head
        self.fixture.reviewed_code_head = git(
            self.root, "rev-parse", "HEAD"
        ).stdout.strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8").replace(
                prior_reviewed_code_head,
                self.fixture.reviewed_code_head,
            ),
            encoding="utf-8",
        )
        git(self.root, "add", TASK)
        git(self.root, "commit", "--quiet", "-m", "fixture reviewed closure")
        self.fixture.head = git(self.root, "rev-parse", "HEAD").stdout.strip()
        task_path.write_text(
            task_path.read_text(encoding="utf-8") + "\nCandidate gate results.\n",
            encoding="utf-8",
        )

        before = self.fixture.repository_state()
        with tempfile.TemporaryDirectory(
            prefix="gate9-production-generator-package-"
        ) as package_parent:
            package = pathlib.Path(package_parent) / "package"
            built = self.fixture.build(package)
            self.assertEqual(0, built.returncode, built.stderr)
            self.assertEqual(rendered[INDEX], (package / "llm-wiki-index.md").read_bytes())
            self.assertEqual(
                rendered[COVERAGE],
                (package / "llm-wiki-stage-category-coverage.md").read_bytes(),
            )
        self.assertEqual(before, self.fixture.repository_state())

    def test_projected_index_rejects_outside_status_drift(self) -> None:
        before = self.fixture.repository_state()
        environment = self.fixture.git_wrapper(
            "step0d-outside-index",
            'if [[ "$1" == "update-index" && "$2" == "--force-remove" && "$3" == "-z" ]]; then\n'
            '  "$REAL_GIT" "$@"\n'
            '  "$REAL_GIT" update-index --force-remove -- ' + json.dumps(SPEC) + "\n"
            '  touch "$GATE9_WRAPPER_MARKER"\n'
            "  exit 0\n"
            "fi\n"
            'exec "$REAL_GIT" "$@"\n',
        )
        result = self.fixture.run(
            "build-package",
            "--attempt",
            "1",
            "--output",
            os.fspath(self.root / "outside-status-package"),
            "--spec",
            SPEC,
            "--plan",
            PLAN,
            "--task",
            TASK,
            env=environment,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("PROJECTED_DELETION_DRIFT", result.stderr)
        self.assertTrue(pathlib.Path(environment["GATE9_WRAPPER_MARKER"]).is_file())
        self.assertEqual(before, self.fixture.repository_state())

    def test_projector_rejects_empty_noisy_crlf_and_non_utf8_stdout_without_writes(
        self,
    ) -> None:
        variants = {
            "empty": "exit 0\n",
            "noisy": "printf 'fixed index\\nnoise\\n'\n",
            "crlf": "printf 'fixed index\\r\\n'\n",
            "non-utf8": "printf '\\377'\n",
        }
        for name, output_program in variants.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix=f"gate9-stdout-{name}-"
            ) as directory:
                fixture = Gate9Fixture(pathlib.Path(directory))
                try:
                    fixture.advance_reviewed_generator(
                        "scripts/knowledge/generate-llm-wiki-index.sh",
                        "#!/usr/bin/env bash\nset -eu\n"
                        "[[ ${1:-} == --stdout && $# == 1 ]] || exit 2\n"
                        + output_program,
                    )
                    before = fixture.repository_state()
                    result = fixture.build(pathlib.Path(directory) / "package")
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("GENERATOR_STDOUT_DRIFT", result.stderr)
                    self.assertEqual(before, fixture.repository_state())
                finally:
                    fixture.cleanup()

    def test_every_public_mode_reprojects_and_rejects_resealed_noop_generator(
        self,
    ) -> None:
        package = self.root / "resealed-package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        (package / "llm-wiki-index.md").chmod(0o644)
        (package / "llm-wiki-index.md").write_bytes(b"forged no-op output\n")
        self.fixture.reseal_package(package)
        marker_path = self.root / "generator-executed"
        generator_path = self.root / "scripts/knowledge/generate-llm-wiki-index.sh"
        generator_path.write_text(
            "#!/usr/bin/env bash\nset -eu\nprintf executed > "
            + os.fspath(marker_path)
            + "\nexit 0\n",
            encoding="utf-8",
        )
        dummy = self.root / "dummy"
        dummy.write_text("dummy\n", encoding="utf-8")
        commands = {
            "build-package": (
                "build-package", "--attempt", "1", "--output",
                os.fspath(self.root / "dirty-code-package"), "--spec", SPEC,
                "--plan", PLAN, "--task", TASK,
            ),
            "verify-package": ("verify-package", "--package", os.fspath(package)),
            "verify-assignments": (
                "verify-assignments", "--package", os.fspath(package),
                "--attestation", os.fspath(materials["attestation"]),
            ),
            "verify-backfill": (
                "verify-backfill", "--package", os.fspath(package),
                "--migration-receipt", os.fspath(materials["migration-specification-receipt"]),
                "--quality-receipt", os.fspath(materials["quality-receipt"]),
                "--assignment-attestation", os.fspath(materials["attestation"]),
                "--task", TASK, "--expect-state", "PACKAGE_REVIEWED",
            ),
            "publish-evidence-ref": (
                "publish-evidence-ref", "--package", os.fspath(package),
                "--task", TASK, "--terminal-state", "INVALIDATED",
                "--terminal-report", os.fspath(dummy),
                "--assignment-attestation", os.fspath(materials["attestation"]),
                "--drift-proof", os.fspath(dummy), "--evidence-ref", "auto",
            ),
            "verify-authorized": (
                "verify-authorized", "--package", os.fspath(package),
                "--task", TASK, "--evidence-ref", "auto",
            ),
        }
        for mode, command in commands.items():
            with self.subTest(mode=mode):
                result = self.fixture.run(*command)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("REVIEWED_CODE_DRIFT", result.stderr)
                self.assertFalse(marker_path.exists())

    def test_non_live_package_generator_is_rejected_before_shell_across_all_modes(
        self,
    ) -> None:
        package = self.root / "historical-package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        marker_path = self.root / "historical-generator-executed"
        self.fixture.advance_reviewed_generator(
            "scripts/knowledge/generate-llm-wiki-index.sh",
            "#!/usr/bin/env bash\nset -eu\nprintf executed > "
            + os.fspath(marker_path)
            + "\nexit 0\n",
        )
        historical_head = self.fixture.reviewed_code_head
        for name in ("HEAD.txt", "package.json", "assignments.json", "gate-results.json"):
            (package / name).chmod(0o644)
        (package / "HEAD.txt").write_text(f"{historical_head}\n", encoding="ascii")
        for name in ("package.json", "assignments.json", "gate-results.json"):
            value = json.loads((package / name).read_text(encoding="utf-8"))
            value["package_head"] = historical_head
            (package / name).write_bytes(canonical_json(value))
        self.fixture.reseal_package(package)
        materials = self.fixture.review_materials(package)
        dummy = self.root / "non-live-dummy"
        dummy.write_text("dummy\n", encoding="utf-8")
        commands = {
            "verify-package": ("verify-package", "--package", os.fspath(package)),
            "verify-assignments": (
                "verify-assignments", "--package", os.fspath(package),
                "--attestation", os.fspath(materials["attestation"]),
            ),
            "verify-backfill": (
                "verify-backfill", "--package", os.fspath(package),
                "--migration-receipt", os.fspath(materials["migration-specification-receipt"]),
                "--quality-receipt", os.fspath(materials["quality-receipt"]),
                "--assignment-attestation", os.fspath(materials["attestation"]),
                "--task", TASK, "--expect-state", "PACKAGE_REVIEWED",
            ),
            "publish-evidence-ref": (
                "publish-evidence-ref", "--package", os.fspath(package),
                "--task", TASK, "--terminal-state", "INVALIDATED",
                "--terminal-report", os.fspath(dummy),
                "--assignment-attestation", os.fspath(materials["attestation"]),
                "--drift-proof", os.fspath(dummy), "--evidence-ref", "auto",
            ),
            "verify-authorized": (
                "verify-authorized", "--package", os.fspath(package),
                "--task", TASK, "--evidence-ref", "auto",
            ),
        }
        for mode, command in commands.items():
            with self.subTest(mode=mode):
                result = self.fixture.run(*command)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("UNTRUSTED_PACKAGE_HEAD", result.stderr)
                self.assertFalse(marker_path.exists())

    def test_package_authority_requires_live_binding_and_unambiguous_history(
        self,
    ) -> None:
        missing = self.fixture.run(
            "build-package", "--attempt", "1", "--output",
            os.fspath(self.root / "missing-binding"), "--spec", SPEC,
            "--plan", PLAN, "--task", TASK, bind_live=False,
        )
        self.assertEqual(2, missing.returncode)
        self.assertIn("LIVE_HEAD_REQUIRED", missing.stderr)
        abbreviated = self.fixture.run(
            "build-package", "--require-live-head", "--live-reviewed-head",
            self.fixture.head[:12], "--reviewed-code-head",
            self.fixture.reviewed_code_head, "--attempt", "1", "--output",
            os.fspath(self.root / "abbreviated-binding"), "--spec", SPEC,
            "--plan", PLAN, "--task", TASK, bind_live=False,
        )
        self.assertEqual(2, abbreviated.returncode)
        self.assertIn("LIVE_HEAD_REQUIRED", abbreviated.stderr)

        common_dir = pathlib.Path(
            git(self.root, "rev-parse", "--path-format=absolute", "--git-common-dir")
            .stdout.strip()
        )
        ambiguous_cases = {
            "replace": common_dir / f"refs/replace/{self.fixture.head}",
            "grafts": common_dir / "info/grafts",
            "shallow": common_dir / "shallow",
        }
        for name, path in ambiguous_cases.items():
            with self.subTest(name=name):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    f"{self.fixture.head}\n" if name != "grafts" else f"{self.fixture.head} {self.fixture.reviewed_code_head}\n",
                    encoding="ascii",
                )
                try:
                    result = self.fixture.build(self.root / f"ambiguous-{name}")
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("AMBIGUOUS_GIT_HISTORY", result.stderr)
                finally:
                    path.unlink(missing_ok=True)

    def test_pinned_scratch_cleanup_preserves_victim_after_ancestor_substitution(
        self,
    ) -> None:
        module_spec = importlib.util.spec_from_file_location("gate9_scratch", HELPER)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        owner_class = getattr(module, "PinnedScratch", None)
        self.assertIsNotNone(owner_class, "Step 0d pinned scratch owner is missing")
        if owner_class is None:
            return
        victim_parent = pathlib.Path(tempfile.mkdtemp(prefix="gate9-victim-"))
        victim = victim_parent / "victim.txt"
        victim.write_bytes(b"outside victim\n")
        owner = owner_class("gate9-test-")
        holding = owner.holding_path
        relocated = holding.with_name(holding.name + "-relocated")
        try:
            owner.create_file("index", b"scratch\n")
            holding.rename(relocated)
            holding.symlink_to(victim_parent, target_is_directory=True)
            with self.assertRaises(module.Gate9Error) as caught:
                owner.close()
            self.assertIn(
                caught.exception.code,
                {"SCRATCH_SCOPE_DRIFT", "SCRATCH_CLEANUP_FAILURE"},
            )
            self.assertEqual(b"outside victim\n", victim.read_bytes())
            self.assertTrue(relocated.exists())
        finally:
            if holding.is_symlink():
                holding.unlink()
            shutil.rmtree(relocated, ignore_errors=True)
            shutil.rmtree(victim_parent, ignore_errors=True)

    def test_projection_never_invokes_worktree_or_drifts_registry(self) -> None:
        before_registry = git(self.root, "worktree", "list", "--porcelain").stdout
        environment = self.fixture.git_wrapper(
            "forbid-worktree",
            'if [[ "$1" == "worktree" ]]; then touch "$GATE9_WRAPPER_MARKER"; exit 97; fi\n'
            'exec "$REAL_GIT" "$@"\n',
        )
        result = self.fixture.run(
            "build-package", "--attempt", "1", "--output",
            os.fspath(self.root / "no-worktree-package"), "--spec", SPEC,
            "--plan", PLAN, "--task", TASK, env=environment,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(pathlib.Path(environment["GATE9_WRAPPER_MARKER"]).exists())
        self.assertEqual(
            before_registry,
            git(self.root, "worktree", "list", "--porcelain").stdout,
        )
        source = HELPER.read_text(encoding="utf-8")
        for forbidden in (
            '"worktree", "add"',
            '"worktree", "remove"',
            '"worktree", "prune"',
            "shutil.rmtree",
            "TemporaryDirectory",
            "mkdtemp",
        ):
            self.assertNotIn(forbidden, source)

    def test_valid_package_and_ref_replay_preserve_repository_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gate9-authorized-package-") as outside:
            package = pathlib.Path(outside) / "authorized-package"
            self.assertEqual(0, self.fixture.build(package).returncode)
            _, evidence_ref = self.fixture.authorize_package(package)
            shutil.rmtree(self.root / "evidence")
            before = self.fixture.repository_state()
            for source_args in (
                ("--package", os.fspath(package)),
                ("--package-from-ref",),
            ):
                with self.subTest(source=source_args[0]):
                    result = self.fixture.run(
                        "verify-authorized", *source_args, "--task", TASK,
                        "--evidence-ref", evidence_ref,
                        "--require-clean-real-index", "--require-task-only-worktree",
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual("AUTHORIZED", json.loads(result.stdout)["state"])
                    self.assertEqual(before, self.fixture.repository_state())

    def test_projection_rejects_live_head_advance_after_preflight(self) -> None:
        module_spec = importlib.util.spec_from_file_location("gate9_head_race", HELPER)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        original_capture = module.capture_repository_snapshot
        advanced = False

        def advance_before_capture(root: pathlib.Path, expected_head: str) -> object:
            nonlocal advanced
            if not advanced:
                git(root, "commit", "--quiet", "--allow-empty", "-m", "advance after preflight")
                advanced = True
            return original_capture(root, expected_head)

        module.capture_repository_snapshot = advance_before_capture
        with self.assertRaises(module.Gate9Error) as caught:
            module.authoritative_projection(
                self.root,
                self.fixture.head,
                self.fixture.head,
                self.fixture.reviewed_code_head,
            )
        self.assertIn(
            caught.exception.code,
            {"PROJECTED_INDEX_SCOPE_DRIFT", "UNTRUSTED_PACKAGE_HEAD"},
        )
        self.assertTrue(advanced)

    def test_authorized_ref_wrong_parent_rejects_before_generator_execution(
        self,
    ) -> None:
        marker_path = self.root / "wrong-parent-generator-executed"
        self.fixture.advance_reviewed_generator(
            "scripts/knowledge/generate-llm-wiki-index.sh",
            "#!/usr/bin/env bash\nset -eu\n"
            "if [[ ${1:-} == --stdout && $# == 1 ]]; then "
            "printf executed > "
            + json.dumps(os.fspath(marker_path))
            + "; printf 'fixed index\\n'; "
            "elif [[ $# == 0 ]]; then printf 'fixed index\\n' > "
            + INDEX
            + "; else exit 2; fi\n",
        )
        package = self.root / "wrong-parent-package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        _, evidence_ref = self.fixture.authorize_package(package)
        marker_path.unlink(missing_ok=True)

        evidence_commit = git(self.root, "rev-parse", evidence_ref).stdout.strip()
        tree = git(self.root, "show", "-s", "--format=%T", evidence_commit).stdout.strip()
        raw_commit = git(self.root, "cat-file", "commit", evidence_commit).stdout
        _, separator, message = raw_commit.partition("\n\n")
        self.assertEqual("\n\n", separator)
        forged = subprocess.run(
            [
                "git",
                "commit-tree",
                tree,
                "-p",
                self.fixture.reviewed_code_head,
            ],
            cwd=self.root,
            input=message,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        git(self.root, "update-ref", evidence_ref, forged, evidence_commit)

        result = self.fixture.run(
            "verify-authorized",
            "--package-from-ref",
            "--task",
            TASK,
            "--evidence-ref",
            evidence_ref,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("EVIDENCE_COMMIT_IDENTITY_DRIFT", result.stderr)
        self.assertFalse(marker_path.exists())

    def test_pinned_scratch_unregistered_index_lock_fails_closed(self) -> None:
        module_spec = importlib.util.spec_from_file_location("gate9_index_lock", HELPER)
        self.assertIsNotNone(module_spec)
        self.assertIsNotNone(module_spec.loader)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        owner = module.PinnedScratch("gate9-index-lock-")
        holding = owner.holding_path
        try:
            owner.create_file("index", b"scratch index\n")
            (owner.path / "index.lock").write_bytes(b"unregistered\n")
            with self.assertRaises(Exception) as caught:
                owner.close()
            self.assertIsInstance(caught.exception, module.Gate9Error)
            self.assertEqual("SCRATCH_CLEANUP_FAILURE", caught.exception.code)
            self.assertIn(os.fspath(holding), caught.exception.detail)
            self.assertEqual(
                b"unregistered\n",
                (holding / "scratch/index.lock").read_bytes(),
            )
        finally:
            shutil.rmtree(holding, ignore_errors=True)

    def test_concurrent_create_race_reuses_identical_tuple_without_drift(self) -> None:
        package = self.root / "package"
        self.assertEqual(0, self.fixture.build(package).returncode)
        materials = self.fixture.review_materials(package)
        self.fixture.backfill_task(package, materials)
        self.fixture.closure_materials(package, materials)
        terminal = self.root / "evidence/terminal.md"
        terminal.write_text("AUTHORIZED\n")
        before_head = git(self.root, "rev-parse", "HEAD").stdout
        before_index = git(self.root, "diff", "--cached", "--binary").stdout
        before_task = (self.root / TASK).read_bytes()
        race_flag = pathlib.Path(tempfile.gettempdir()) / f"gate9-race-{self.root.name}"
        race_flag.unlink(missing_ok=True)
        environment = self.fixture.git_wrapper(
            "update-ref-race",
            f'FLAG="{race_flag}"\n'
            'if [[ "$1" == "update-ref" && "${4:-}" == "0000000000000000000000000000000000000000" && ! -e "$FLAG" ]]; then\n'
            '  "$REAL_GIT" "$@"\n'
            '  touch "$FLAG"\n'
            "  exit 91\n"
            "fi\n"
            'exec "$REAL_GIT" "$@"\n',
        )
        before_status = git(self.root, "status", "--porcelain").stdout
        result = self.fixture.run(
            "publish-evidence-ref",
            "--package",
            os.fspath(package),
            "--task",
            TASK,
            "--terminal-state",
            "AUTHORIZED",
            "--terminal-report",
            os.fspath(terminal),
            "--migration-report",
            os.fspath(materials["migration-specification-report"]),
            "--migration-receipt",
            os.fspath(materials["migration-specification-receipt"]),
            "--quality-report",
            os.fspath(materials["quality-report"]),
            "--quality-receipt",
            os.fspath(materials["quality-receipt"]),
            "--assignment-attestation",
            os.fspath(materials["attestation"]),
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
            env=environment,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before_head, git(self.root, "rev-parse", "HEAD").stdout)
        self.assertEqual(before_index, git(self.root, "diff", "--cached", "--binary").stdout)
        self.assertEqual(before_task, (self.root / TASK).read_bytes())
        self.assertEqual(before_status, git(self.root, "status", "--porcelain").stdout)
        race_flag.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
