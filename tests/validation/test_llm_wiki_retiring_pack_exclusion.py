from __future__ import annotations

import fcntl
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
INDEX_GENERATOR = Path("scripts/knowledge/generate-llm-wiki-index.sh")
COVERAGE_GENERATOR = Path("scripts/knowledge/generate-llm-wiki-coverage.sh")
INDEX_OUTPUT = Path("docs/90.references/llm-wiki/llm-wiki-index.md")
COVERAGE_OUTPUT = Path(
    "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md"
)
RETIRING_PREFIX = (
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/"
)
NEW_PREFIX = (
    "docs/90.references/research/"
    "2026-08-08-agentic-engineering-research-pack/"
)
SIBLING_PATH = (
    "docs/90.references/research/"
    "2026-07-05-agentic-research-pack-refresh-notes/README.md"
)
PLAN_PATH = "docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md"
TASK_PATH = "docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md"

RETIRING_PACK_FILES = (
    "README.md",
    "agent-instructions-vibe-coding.md",
    "agent-model-selection.md",
    "ai-agent-catalogs.md",
    "automation-pipeline-workflow.md",
    "docker-compose-infrastructure.md",
    "document-metadata-lifecycle.md",
    "documentation-architecture.md",
    "harness-engineering.md",
    "llm-wiki-system.md",
    "loop-engineering.md",
    "memory-hierarchy.md",
    "provider-implementation-comparison.md",
    "provider-model-landscape.md",
    "quality-ci-formatting.md",
    "scope-application-matrix.md",
    "sdlc-document-roles.md",
    "security-governance.md",
    "spec-driven-sdlc.md",
    "workspace-baseline.md",
)
NEW_PACK_FILES = tuple(
    sorted((*RETIRING_PACK_FILES, "verification-validation.md"))
)


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def write_fixture_file(root: Path, relative_path: str) -> None:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"# Fixture: {relative_path}\n")


def coverage_metrics(content: str) -> dict[str, int]:
    patterns = {
        "safe paths": r"^- Safe tracked source paths: `(\d+)`$",
        "docs/90.references": r"^\| `docs/90\.references` \| (\d+) \|",
        "Reference and template docs": (
            r"^\| Reference and template docs \| (\d+) \|"
        ),
        "folder index": r"^\| folder index \| (\d+) \|",
        "Markdown reference": r"^\| Markdown reference \| (\d+) \|",
    }
    metrics: dict[str, int] = {}
    for label, pattern in patterns.items():
        match = re.search(pattern, content, re.MULTILINE)
        if match is None:
            raise AssertionError(f"coverage metric is missing: {label}")
        metrics[label] = int(match.group(1))
    return metrics


def output_snapshot(path: Path) -> tuple[int, int, int, int, bytes]:
    metadata = path.lstat()
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        path.read_bytes(),
    )


def gate9_manifest(root: Path = REPOSITORY_ROOT) -> bytes:
    object_format = run(
        ["git", "rev-parse", "--show-object-format"], cwd=root
    ).stdout.strip()
    live_commit = run(
        ["git", "rev-parse", "HEAD"], cwd=root
    ).stdout.strip()
    projected_tree = run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=root
    ).stdout.strip()
    paths = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).split(b"\0")
    if paths[-1] == b"":
        paths.pop()
    paths.sort()
    records = [
        b"schema=agentic-research-llm-wiki-manifest/v1",
        f"object-format={object_format}".encode(),
        f"live-commit={live_commit}".encode(),
        f"projected-tree={projected_tree}".encode(),
        f"count={len(paths)}".encode(),
        *paths,
    ]
    return b"\0".join(records) + b"\0"


def memfd_with_seals(payload: bytes, seals: int) -> int:
    descriptor = os.memfd_create(
        "gate9-llm-wiki-manifest",
        os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING,
    )
    remaining = memoryview(payload)
    while remaining:
        written = os.write(descriptor, remaining)
        if written == 0:
            raise RuntimeError("memfd write made no progress")
        remaining = remaining[written:]
    os.lseek(descriptor, 0, os.SEEK_SET)
    if seals:
        fcntl.fcntl(descriptor, fcntl.F_ADD_SEALS, seals)
    return descriptor


def sealed_memfd(payload: bytes) -> int:
    return memfd_with_seals(
        payload,
        fcntl.F_SEAL_SEAL
        | fcntl.F_SEAL_SHRINK
        | fcntl.F_SEAL_GROW
        | fcntl.F_SEAL_WRITE,
    )


def internal_manifest_environment(descriptor: int, payload: bytes) -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "GATE9_LLM_MANIFEST_FD": str(descriptor),
            "GATE9_LLM_MANIFEST_SIZE": str(len(payload)),
            "GATE9_LLM_MANIFEST_SHA256": hashlib.sha256(payload).hexdigest(),
        }
    )
    return environment


class LlmWikiRetiringPackExclusionTest(unittest.TestCase):
    def create_repository(self, root: Path) -> None:
        run(["git", "init", "--quiet"], cwd=root)

        for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR):
            target = root / generator
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPOSITORY_ROOT / generator, target)

        for filename in RETIRING_PACK_FILES:
            write_fixture_file(root, f"{RETIRING_PREFIX}{filename}")

        for filename in NEW_PACK_FILES:
            write_fixture_file(root, f"{NEW_PREFIX}{filename}")

        for retained_path in (SIBLING_PATH, PLAN_PATH, TASK_PATH):
            write_fixture_file(root, retained_path)

        run(["git", "add", "."], cwd=root)

    def generate(self, root: Path) -> tuple[bytes, bytes]:
        run(["bash", str(INDEX_GENERATOR)], cwd=root)
        run(["bash", str(COVERAGE_GENERATOR)], cwd=root)
        return (
            (root / INDEX_OUTPUT).read_bytes(),
            (root / COVERAGE_OUTPUT).read_bytes(),
        )

    def test_retiring_pack_is_projection_invariant_until_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_repository(root)

            coexisting_index, coexisting_coverage = self.generate(root)

            run(
                ["git", "rm", "--cached", "--quiet", "-r", RETIRING_PREFIX],
                cwd=root,
            )
            post_delete_index, post_delete_coverage = self.generate(root)

            coexisting_metrics = coverage_metrics(coexisting_coverage.decode())
            post_delete_metrics = coverage_metrics(post_delete_coverage.decode())
            observed_deltas = {
                label: post_delete_metrics[label] - coexisting_metrics[label]
                for label in coexisting_metrics
            }
            if coexisting_coverage != post_delete_coverage:
                self.assertEqual(
                    observed_deltas,
                    {
                        "safe paths": -20,
                        "docs/90.references": -20,
                        "Reference and template docs": -20,
                        "folder index": -1,
                        "Markdown reference": -19,
                    },
                )

            delta_evidence = f"temporary-index deletion deltas: {observed_deltas}"
            self.assertEqual(
                coexisting_index,
                post_delete_index,
                msg=delta_evidence,
            )
            self.assertEqual(
                coexisting_coverage,
                post_delete_coverage,
                msg=delta_evidence,
            )

            decoded_index = coexisting_index.decode()
            decoded_coverage = coexisting_coverage.decode()
            for filename in RETIRING_PACK_FILES:
                self.assertNotIn(f"{RETIRING_PREFIX}{filename}", decoded_index)
                self.assertNotIn(f"{RETIRING_PREFIX}{filename}", decoded_coverage)

            for filename in NEW_PACK_FILES:
                self.assertIn(f"{NEW_PREFIX}{filename}", decoded_index)

            for retained_path in (SIBLING_PATH, PLAN_PATH, TASK_PATH):
                self.assertIn(retained_path, decoded_index)
                self.assertIn(retained_path, decoded_coverage)

            for filename in NEW_PACK_FILES:
                retained_path = f"{NEW_PREFIX}{filename}"
                run(
                    ["git", "rm", "--cached", "--quiet", retained_path],
                    cwd=root,
                )
                run(["bash", str(COVERAGE_GENERATOR)], cwd=root)
                without_path_metrics = coverage_metrics(
                    (root / COVERAGE_OUTPUT).read_text(encoding="utf-8")
                )
                expected_delta = {
                    "safe paths": -1,
                    "docs/90.references": -1,
                    "Reference and template docs": -1,
                    "folder index": -1 if filename == "README.md" else 0,
                    "Markdown reference": 0 if filename == "README.md" else -1,
                }
                self.assertEqual(
                    expected_delta,
                    {
                        label: without_path_metrics[label] - coexisting_metrics[label]
                        for label in coexisting_metrics
                    },
                    msg=f"new-pack coverage projection omitted {retained_path}",
                )
                run(["git", "add", retained_path], cwd=root)

    def test_verification_validation_leaf_changes_only_new_pack_cardinality(
        self,
    ) -> None:
        self.assertEqual(20, len(RETIRING_PACK_FILES))
        self.assertEqual(21, len(NEW_PACK_FILES))
        self.assertEqual(
            set(RETIRING_PACK_FILES) | {"verification-validation.md"},
            set(NEW_PACK_FILES),
        )

        production_pack = REPOSITORY_ROOT / NEW_PREFIX
        production_files = sorted(
            path.name for path in production_pack.iterdir() if path.is_file()
        )
        self.assertEqual(list(NEW_PACK_FILES), production_files)
        self.assertIn(
            "(./verification-validation.md)",
            (production_pack / "README.md").read_text(encoding="utf-8"),
        )

    def test_stdout_mode_is_byte_exact_and_write_free(self) -> None:
        for generator, output in (
            (INDEX_GENERATOR, INDEX_OUTPUT),
            (COVERAGE_GENERATOR, COVERAGE_OUTPUT),
        ):
            with self.subTest(generator=generator):
                output_path = REPOSITORY_ROOT / output
                before = output_snapshot(output_path)
                result = subprocess.run(
                    ["bash", str(generator), "--stdout"],
                    cwd=REPOSITORY_ROOT,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr.decode())
                self.assertEqual(before[-1], result.stdout)
                self.assertEqual(b"", result.stderr)
                self.assertEqual(before, output_snapshot(output_path))

    def test_generator_cli_rejects_conflicting_and_extra_arguments_without_writes(
        self,
    ) -> None:
        invalid_arguments = (
            ("--check", "--stdout"),
            ("--stdout", "--check"),
            ("--stdout", "extra"),
            ("--unknown",),
        )
        for generator, output in (
            (INDEX_GENERATOR, INDEX_OUTPUT),
            (COVERAGE_GENERATOR, COVERAGE_OUTPUT),
        ):
            output_path = REPOSITORY_ROOT / output
            for arguments in invalid_arguments:
                with self.subTest(generator=generator, arguments=arguments):
                    before = output_snapshot(output_path)
                    result = subprocess.run(
                        ["bash", str(generator), *arguments],
                        cwd=REPOSITORY_ROOT,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode)
                    self.assertEqual(b"", result.stdout)
                    self.assertNotEqual(b"", result.stderr)
                    self.assertEqual(before, output_snapshot(output_path))

    def test_internal_manifest_mode_is_byte_exact_for_both_generators(self) -> None:
        manifest_only = "docs/fixture/manifest-only.md"
        tracked_only = "docs/fixture/tracked-only.md"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run(["git", "init", "--quiet"], cwd=root)
            for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR):
                target = root / generator
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPOSITORY_ROOT / generator, target)
            write_fixture_file(root, manifest_only)
            run(["git", "add", "."], cwd=root)
            run(
                [
                    "git",
                    "-c",
                    "user.name=Gate 9 Test",
                    "-c",
                    "user.email=gate9@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "fixture manifest tree",
                ],
                cwd=root,
            )

            payload = gate9_manifest(root)
            expected_outputs = {
                generator: subprocess.run(
                    ["bash", str(generator), "--stdout"],
                    cwd=root,
                    capture_output=True,
                    check=True,
                ).stdout
                for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR)
            }

            run(["git", "rm", "--quiet", manifest_only], cwd=root)
            write_fixture_file(root, tracked_only)
            run(["git", "add", tracked_only], cwd=root)

            for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR):
                with self.subTest(generator=generator):
                    current_public = subprocess.run(
                        ["bash", str(generator), "--stdout"],
                        cwd=root,
                        capture_output=True,
                        check=False,
                    )
                    descriptor = sealed_memfd(payload)
                    try:
                        internal_result = subprocess.run(
                            ["bash", str(generator), "--stdout"],
                            cwd=root,
                            capture_output=True,
                            check=False,
                            env=internal_manifest_environment(descriptor, payload),
                            pass_fds=(descriptor,),
                        )
                    finally:
                        os.close(descriptor)
                    self.assertEqual(0, current_public.returncode, current_public.stderr)
                    self.assertNotEqual(
                        expected_outputs[generator], current_public.stdout
                    )
                    self.assertEqual(0, internal_result.returncode, internal_result.stderr)
                    self.assertEqual(b"", internal_result.stderr)
                    self.assertEqual(
                        expected_outputs[generator], internal_result.stdout
                    )

    def test_internal_manifest_rejects_partial_malformed_unsealed_wrong_type_oversize_and_offset(
        self,
    ) -> None:
        payload = gate9_manifest()
        records = payload.split(b"\0")[:-1]
        required_seals = (
            fcntl.F_SEAL_SEAL
            | fcntl.F_SEAL_SHRINK
            | fcntl.F_SEAL_GROW
            | fcntl.F_SEAL_WRITE
        )

        def payload_with_records(new_records: list[bytes]) -> bytes:
            return b"\0".join(new_records) + b"\0"

        def payload_with_paths(paths: list[bytes]) -> bytes:
            return payload_with_records(
                [*records[:4], f"count={len(paths)}".encode(), *paths]
            )

        for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR):
            cases: list[tuple[str, int | None, dict[str, str]]] = []

            def add_sealed_case(
                label: str,
                case_payload: bytes,
                environment_update: dict[str, str] | None = None,
                offset: int = 0,
            ) -> None:
                descriptor = sealed_memfd(case_payload)
                if offset:
                    os.lseek(descriptor, offset, os.SEEK_SET)
                environment = internal_manifest_environment(
                    descriptor, case_payload
                )
                if environment_update:
                    environment.update(environment_update)
                cases.append((label, descriptor, environment))

            partial_environment = os.environ.copy()
            partial_environment["GATE9_LLM_MANIFEST_FD"] = "0"
            cases.append(("partial", None, partial_environment))

            add_sealed_case(
                "extra-variable",
                payload,
                {"GATE9_LLM_MANIFEST_INDEX": "0"},
            )

            malformed_payload = b"malformed\0"
            add_sealed_case("malformed", malformed_payload)

            schema_records = list(records)
            schema_records[0] = b"schema=agentic-research-llm-wiki-manifest/v2"
            add_sealed_case("schema", payload_with_records(schema_records))

            oid_records = list(records)
            oid_records[2] = b"live-commit=" + b"g" + oid_records[2][len(b"live-commit=") + 1 :]
            add_sealed_case("oid", payload_with_records(oid_records))

            count_records = list(records)
            count_records[4] = f"count={len(records[5:]) + 1}".encode()
            add_sealed_case("count", payload_with_records(count_records))

            add_sealed_case("unsafe-path", payload_with_paths([b"../unsafe.md"]))
            add_sealed_case("non-utf8-path", payload_with_paths([b"docs/\xff.md"]))
            add_sealed_case(
                "duplicate-path",
                payload_with_paths([b"docs/a.md", b"docs/a.md"]),
            )
            add_sealed_case(
                "unsorted-path",
                payload_with_paths([b"docs/b.md", b"docs/a.md"]),
            )
            add_sealed_case(
                "prefix-collision",
                payload_with_paths([b"docs/a", b"docs/a/file.md"]),
            )

            add_sealed_case(
                "size",
                payload,
                {"GATE9_LLM_MANIFEST_SIZE": str(len(payload) + 1)},
            )
            add_sealed_case(
                "digest",
                payload,
                {"GATE9_LLM_MANIFEST_SHA256": "0" * 64},
            )

            unsealed_descriptor = memfd_with_seals(payload, 0)
            cases.append(
                (
                    "unsealed",
                    unsealed_descriptor,
                    internal_manifest_environment(unsealed_descriptor, payload),
                )
            )

            partial_seal_descriptor = memfd_with_seals(
                payload,
                required_seals & ~fcntl.F_SEAL_WRITE,
            )
            cases.append(
                (
                    "partial-seals",
                    partial_seal_descriptor,
                    internal_manifest_environment(partial_seal_descriptor, payload),
                )
            )

            directory_descriptor = os.open(
                REPOSITORY_ROOT,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC,
            )
            cases.append(
                (
                    "directory-fd",
                    directory_descriptor,
                    internal_manifest_environment(directory_descriptor, payload),
                )
            )

            pipe_read, pipe_write = os.pipe()
            os.close(pipe_write)
            cases.append(
                (
                    "pipe-fd",
                    pipe_read,
                    internal_manifest_environment(pipe_read, payload),
                )
            )

            oversize = 8 * 1024 * 1024 + 1
            oversize_descriptor = os.memfd_create(
                "gate9-oversize-manifest",
                os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING,
            )
            os.ftruncate(oversize_descriptor, oversize)
            os.lseek(oversize_descriptor, 0, os.SEEK_SET)
            fcntl.fcntl(
                oversize_descriptor,
                fcntl.F_ADD_SEALS,
                fcntl.F_SEAL_SEAL
                | fcntl.F_SEAL_SHRINK
                | fcntl.F_SEAL_GROW
                | fcntl.F_SEAL_WRITE,
            )
            oversize_environment = os.environ.copy()
            oversize_environment.update(
                {
                    "GATE9_LLM_MANIFEST_FD": str(oversize_descriptor),
                    "GATE9_LLM_MANIFEST_SIZE": str(oversize),
                    "GATE9_LLM_MANIFEST_SHA256": "0" * 64,
                }
            )
            cases.append(
                (
                    "oversize",
                    oversize_descriptor,
                    oversize_environment,
                )
            )

            add_sealed_case("offset", payload, offset=1)

            for case, descriptor, environment in cases:
                with self.subTest(generator=generator, case=case):
                    pass_fds = () if descriptor is None else (descriptor,)
                    try:
                        result = subprocess.run(
                            ["bash", str(generator), "--stdout"],
                            cwd=REPOSITORY_ROOT,
                            capture_output=True,
                            check=False,
                            env=environment,
                            pass_fds=pass_fds,
                        )
                    finally:
                        if descriptor is not None:
                            os.close(descriptor)
                    self.assertNotEqual(0, result.returncode)
                    self.assertEqual(b"", result.stdout)
                    self.assertNotEqual(b"", result.stderr)

        reused_descriptor = sealed_memfd(payload)
        try:
            first_environment = internal_manifest_environment(
                reused_descriptor, payload
            )
            first_result = subprocess.run(
                ["bash", str(INDEX_GENERATOR), "--stdout"],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                check=False,
                env=first_environment,
                pass_fds=(reused_descriptor,),
            )
            second_result = subprocess.run(
                ["bash", str(COVERAGE_GENERATOR), "--stdout"],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                check=False,
                env=internal_manifest_environment(reused_descriptor, payload),
                pass_fds=(reused_descriptor,),
            )
        finally:
            os.close(reused_descriptor)
        self.assertEqual(0, first_result.returncode, first_result.stderr)
        self.assertNotEqual(b"", first_result.stdout)
        self.assertNotEqual(0, second_result.returncode)
        self.assertEqual(b"", second_result.stdout)
        self.assertNotEqual(b"", second_result.stderr)


if __name__ == "__main__":
    unittest.main()
