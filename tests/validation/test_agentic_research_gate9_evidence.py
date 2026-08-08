from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
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


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
            "#!/usr/bin/env bash\nset -eu\nprintf 'fixed index\\n' > " + INDEX + "\n",
            executable=True,
        )
        self.write(
            "scripts/knowledge/generate-llm-wiki-coverage.sh",
            "#!/usr/bin/env bash\nset -eu\nprintf 'fixed coverage\\n' > "
            + COVERAGE
            + "\n",
            executable=True,
        )
        self.pending_payload: dict[str, object] = {
            "attempt": 1,
            "schema": SCHEMA,
            "state": "PACKAGE_REVIEW_PENDING",
        }
        self.write(TASK, "# Task\n\n" + marker(self.pending_payload) + "\n")
        git(root, "add", ".")
        git(root, "commit", "--quiet", "-m", "fixture baseline")
        self.head = git(root, "rev-parse", "HEAD").stdout.strip()
        task_path = root / TASK
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
    ) -> subprocess.CompletedProcess[str]:
        command_env = os.environ.copy()
        if env:
            command_env.update(env)
        return subprocess.run(
            ["python3", os.fspath(HELPER), *args],
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
        before_old = git(self.root, "ls-tree", "-r", "--name-only", "HEAD", OLD_PACK).stdout
        package = self.root / "outside-package"

        built = self.fixture.build(package)
        self.assertEqual(0, built.returncode, built.stderr)
        verified = self.fixture.run(
            "verify-package", "--package", os.fspath(package), "--require-live-head"
        )
        self.assertEqual(0, verified.returncode, verified.stderr)

        self.assertEqual(before_head, git(self.root, "rev-parse", "HEAD").stdout)
        self.assertEqual(before_index, git(self.root, "diff", "--cached", "--binary").stdout)
        self.assertEqual(
            before_old,
            git(self.root, "ls-tree", "-r", "--name-only", "HEAD", OLD_PACK).stdout,
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
        self.assertIn("STALE_HEAD", stale.stderr)

        attachment = package / "spec.md"
        attachment.chmod(0o644)
        attachment.write_text("drift\n", encoding="utf-8")
        drift = self.fixture.run("verify-package", "--package", os.fspath(package))
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

    def test_detached_worktree_cleanup_handles_partial_add_and_failed_remove(self) -> None:
        before = git(self.root, "worktree", "list", "--porcelain").stdout
        wrappers = {
            "partial-add": self.fixture.git_wrapper(
                "partial-add",
                'if [[ "$1" == "worktree" && "$2" == "add" ]]; then\n'
                '  "$REAL_GIT" "$@"\n'
                '  touch "$GATE9_WRAPPER_MARKER"\n'
                "  exit 91\n"
                "fi\n"
                'exec "$REAL_GIT" "$@"\n',
            ),
            "failed-remove": self.fixture.git_wrapper(
                "failed-remove",
                'if [[ "$1" == "worktree" && "$2" == "remove" ]]; then\n'
                '  touch "$GATE9_WRAPPER_MARKER"\n'
                "  exit 91\n"
                "fi\n"
                'exec "$REAL_GIT" "$@"\n',
            ),
        }
        for name, environment in wrappers.items():
            with self.subTest(name=name):
                if name == "partial-add":
                    result = self.fixture.run(
                        "build-package",
                        "--attempt",
                        "1",
                        "--output",
                        os.fspath(self.root / f"package-{name}"),
                        "--spec",
                        SPEC,
                        "--plan",
                        PLAN,
                        "--task",
                        TASK,
                        env=environment,
                    )
                else:
                    result = self.fixture.run(
                        "build-package",
                        "--attempt",
                        "1",
                        "--output",
                        os.fspath(self.root / f"package-{name}"),
                        "--spec",
                        SPEC,
                        "--plan",
                        PLAN,
                        "--task",
                        TASK,
                        env=environment,
                    )
                self.assertNotEqual(0, result.returncode, name)
                self.assertTrue(
                    pathlib.Path(environment["GATE9_WRAPPER_MARKER"]).is_file(),
                    name,
                )
                expected = (
                    "GIT_FAILURE: git worktree add"
                    if name == "partial-add"
                    else "WORKTREE_CLEANUP_FAILURE"
                )
                self.assertIn(expected, result.stderr, name)
                self.assertEqual(
                    before,
                    git(self.root, "worktree", "list", "--porcelain").stdout,
                    name,
                )

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
