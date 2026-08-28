from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts.lib.document_governance.frontmatter import read_frontmatter_values


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _architecture_module():
    module_name = "scripts.lib.document_governance.architecture"
    if importlib.util.find_spec(module_name) is None:
        raise AssertionError(f"missing production module: {module_name}")
    return importlib.import_module(module_name)


def _document_text(
    profile_id: str,
    number: str,
    *,
    artifact_id: str | None = None,
    status: str = "active",
    parent_ids: tuple[str, ...] | None = None,
    supersedes: tuple[str, ...] = (),
    superseded_by: str | None = None,
) -> str:
    prefix = "AD" if profile_id == "architecture-description" else "ADR"
    artifact_id = artifact_id or f"{prefix}-{number}"
    if parent_ids is None:
        parent_ids = (
            ("REQ-0001",)
            if profile_id == "architecture-description"
            else ("AD-0001",)
        )
    parent_lines = "\n".join(f"  - {item}" for item in parent_ids)
    supersedes_lines = (
        "supersedes: []"
        if not supersedes
        else "supersedes:\n" + "\n".join(f"  - {item}" for item in supersedes)
    )
    superseded_by_value = "null" if superseded_by is None else superseded_by
    return f"""---
profile_id: {profile_id}
status: {status}
artifact_id: {artifact_id}
artifact_type: {profile_id if profile_id == "architecture-description" else "adr"}
parent_ids:
{parent_lines}
created: 2026-08-22
updated: 2026-08-22
{supersedes_lines}
superseded_by: {superseded_by_value}
---

# Fixture {artifact_id}

Bounded fixture body.
"""


def _write_document(
    stage_root: pathlib.Path,
    directory: str,
    name: str,
    text: str,
) -> pathlib.Path:
    target = stage_root / directory / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def _write_minimal_corpus(stage_root: pathlib.Path) -> None:
    stage_root.mkdir(parents=True, exist_ok=True)
    (stage_root / "README.md").write_text("# Architecture\n", encoding="utf-8")
    for directory in ("descriptions", "decisions"):
        child = stage_root / directory
        child.mkdir()
        (child / "README.md").write_text(f"# {directory}\n", encoding="utf-8")
    _write_document(
        stage_root,
        "descriptions",
        "0001-example.md",
        _document_text("architecture-description", "0001"),
    )
    _write_document(
        stage_root,
        "decisions",
        "0001-example.md",
        _document_text("adr", "0001"),
    )


class ArchitectureDocumentTests(unittest.TestCase):
    def test_current_architecture_corpus_is_prefixless_and_uppercase(self) -> None:
        stage_root = ROOT / "docs/02.architecture"
        paths = tuple(
            sorted(
                path
                for directory in ("descriptions", "decisions")
                for path in stage_root.joinpath(directory).glob("*.md")
                if path.name != "README.md"
            )
        )
        problems: list[str] = []
        for path in paths:
            metadata = read_frontmatter_values(path)
            artifact_id = metadata.get("artifact_id")
            if path.name.startswith(("ad-", "adr-")):
                problems.append(f"prefixed path: {path.relative_to(ROOT)}")
            if not isinstance(artifact_id, str) or not artifact_id.startswith(
                ("AD-", "ADR-")
            ):
                problems.append(
                    f"noncanonical artifact_id: {path.relative_to(ROOT)}: {artifact_id!r}"
                )
        self.assertEqual(51, len(paths))
        self.assertFalse(stage_root.joinpath("requirements").exists())
        self.assertEqual([], problems)

    def test_loads_frozen_canonical_documents_and_validates_graph(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            predecessor = _write_document(
                stage_root,
                "decisions",
                "0027-predecessor.md",
                _document_text(
                    "adr",
                    "0027",
                    status="superseded",
                    superseded_by="ADR-0029",
                ),
            )
            _write_document(
                stage_root,
                "decisions",
                "0029-successor.md",
                _document_text(
                    "adr",
                    "0029",
                    supersedes=("ADR-0027",),
                ),
            )
            corpus = architecture.load_architecture_documents(stage_root)

        by_id = {document.artifact_id: document for document in corpus}
        self.assertEqual((), architecture.validate_supersession_graph(corpus))
        self.assertEqual(("ADR-0027",), by_id["ADR-0029"].supersedes)
        self.assertEqual("ADR-0029", by_id["ADR-0027"].superseded_by)
        self.assertEqual(predecessor.name, by_id["ADR-0027"].path.name)
        self.assertIsInstance(by_id["ADR-0027"].parent_ids, tuple)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            by_id["ADR-0027"].status = "active"

    def test_lowercase_stable_id_fails_closed(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            target = stage_root / "descriptions/0001-example.md"
            target.write_text(
                _document_text(
                    "architecture-description", "0001", artifact_id="ad-0001"
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                architecture.ArchitectureDocumentError, "AD-0001|uppercase|artifact"
            ):
                architecture.load_architecture_documents(stage_root)

    def test_path_number_mismatch_fails_closed(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            target = stage_root / "decisions/0001-example.md"
            target.write_text(_document_text("adr", "0002"), encoding="utf-8")
            with self.assertRaisesRegex(
                architecture.ArchitectureDocumentError, "path|ADR-0001|mismatch"
            ):
                architecture.load_architecture_documents(stage_root)

    def test_duplicate_identity_fails_closed(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            _write_document(
                stage_root,
                "decisions",
                "0001-duplicate.md",
                _document_text("adr", "0001"),
            )
            with self.assertRaisesRegex(
                architecture.ArchitectureDocumentError, "duplicate.*ADR-0001"
            ):
                architecture.load_architecture_documents(stage_root)

    def test_symlink_non_regular_oversized_and_non_utf8_inputs_fail_closed(self) -> None:
        architecture = _architecture_module()
        mutations = ("symlink", "non-regular", "oversized", "non-utf8")
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                stage_root = pathlib.Path(directory) / "docs/02.architecture"
                _write_minimal_corpus(stage_root)
                target = stage_root / "decisions/0001-example.md"
                if mutation == "symlink":
                    source = stage_root / "outside.md"
                    source.write_text(_document_text("adr", "0001"), encoding="utf-8")
                    target.unlink()
                    target.symlink_to(source)
                elif mutation == "non-regular":
                    target.unlink()
                    target.mkdir()
                elif mutation == "oversized":
                    target.write_bytes(b"x" * (architecture.MAX_ARCHITECTURE_BYTES + 1))
                else:
                    target.write_bytes(b"\xff\xfe\xfa")
                with self.assertRaises(architecture.ArchitectureDocumentError):
                    architecture.load_architecture_documents(stage_root)

    def test_same_inode_mutation_during_read_fails_closed(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "mixed.md"
            target.write_bytes(b"a" * (70 * 1024))
            initial = target.stat()
            real_read = architecture.os.read
            mutated = False

            def mutate_after_first_chunk(descriptor: int, count: int) -> bytes:
                nonlocal mutated
                chunk = real_read(descriptor, count)
                if chunk and not mutated:
                    with target.open("r+b") as stream:
                        stream.seek(64 * 1024)
                        stream.write(b"b" * (6 * 1024))
                        stream.flush()
                        architecture.os.fsync(stream.fileno())
                    mutated = True
                return chunk

            with mock.patch.object(
                architecture.os,
                "read",
                side_effect=mutate_after_first_chunk,
            ), self.assertRaisesRegex(
                architecture.ArchitectureDocumentError,
                "changed|read",
            ):
                architecture._read_regular_utf8(target)

            final = target.stat()
            self.assertTrue(mutated)
            self.assertEqual((initial.st_dev, initial.st_ino, initial.st_size), (final.st_dev, final.st_ino, final.st_size))

    def test_dangling_and_asymmetric_supersession_are_reported(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            _write_document(
                stage_root,
                "decisions",
                "0029-successor.md",
                _document_text("adr", "0029", supersedes=("ADR-0027",)),
            )
            corpus = architecture.load_architecture_documents(stage_root)
            dangling = architecture.validate_supersession_graph(corpus)
            self.assertIn("supersession-dangling", {item.code for item in dangling})

            _write_document(
                stage_root,
                "decisions",
                "0027-predecessor.md",
                _document_text("adr", "0027", status="superseded"),
            )
            corpus = architecture.load_architecture_documents(stage_root)
            asymmetric = architecture.validate_supersession_graph(corpus)
            self.assertIn(
                "supersession-asymmetric", {item.code for item in asymmetric}
            )

    def test_cyclic_supersession_is_reported(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            _write_document(
                stage_root,
                "decisions",
                "0027-cycle-a.md",
                _document_text(
                    "adr",
                    "0027",
                    status="superseded",
                    supersedes=("ADR-0029",),
                    superseded_by="ADR-0029",
                ),
            )
            _write_document(
                stage_root,
                "decisions",
                "0029-cycle-b.md",
                _document_text(
                    "adr",
                    "0029",
                    status="superseded",
                    supersedes=("ADR-0027",),
                    superseded_by="ADR-0027",
                ),
            )
            corpus = architecture.load_architecture_documents(stage_root)
            findings = architecture.validate_supersession_graph(corpus)
        self.assertIn("supersession-cycle", {item.code for item in findings})

    def test_supersession_edges_require_effective_successor_and_superseded_predecessor(self) -> None:
        architecture = _architecture_module()
        predecessor = architecture.ArchitectureDocument(
            pathlib.PurePosixPath("docs/02.architecture/decisions/0027-predecessor.md"),
            "ADR-0027",
            "adr",
            "superseded",
            ("AD-0001",),
            (),
            "ADR-0029",
        )
        for status in ("rejected", "draft", "retired"):
            with self.subTest(status=status):
                successor = architecture.ArchitectureDocument(
                    pathlib.PurePosixPath("docs/02.architecture/decisions/0029-successor.md"),
                    "ADR-0029",
                    "adr",
                    status,
                    ("AD-0001",),
                    ("ADR-0027",),
                    None,
                )
                findings = architecture.validate_supersession_graph(
                    (predecessor, successor)
                )
                self.assertIn(
                    "supersession-successor-not-effective",
                    {item.code for item in findings},
                )

        active_predecessor = dataclasses.replace(predecessor, status="active")
        active_successor = architecture.ArchitectureDocument(
            pathlib.PurePosixPath("docs/02.architecture/decisions/0029-successor.md"),
            "ADR-0029",
            "adr",
            "active",
            ("AD-0001",),
            ("ADR-0027",),
            None,
        )
        findings = architecture.validate_supersession_graph(
            (active_predecessor, active_successor)
        )
        self.assertIn(
            "supersession-predecessor-not-superseded",
            {item.code for item in findings},
        )

    def test_superseded_successor_remains_effective_in_a_reciprocal_chain(self) -> None:
        architecture = _architecture_module()
        documents = (
            architecture.ArchitectureDocument(
                pathlib.PurePosixPath("docs/02.architecture/decisions/0027-first.md"),
                "ADR-0027",
                "adr",
                "superseded",
                ("AD-0001",),
                (),
                "ADR-0028",
            ),
            architecture.ArchitectureDocument(
                pathlib.PurePosixPath("docs/02.architecture/decisions/0028-middle.md"),
                "ADR-0028",
                "adr",
                "superseded",
                ("AD-0001",),
                ("ADR-0027",),
                "ADR-0029",
            ),
            architecture.ArchitectureDocument(
                pathlib.PurePosixPath("docs/02.architecture/decisions/0029-current.md"),
                "ADR-0029",
                "adr",
                "active",
                ("AD-0001",),
                ("ADR-0028",),
                None,
            ),
        )
        self.assertEqual((), architecture.validate_supersession_graph(documents))

    def test_metadata_cli_rejects_ineffective_supersession_successor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            _write_document(
                stage_root,
                "decisions",
                "0027-predecessor.md",
                _document_text(
                    "adr",
                    "0027",
                    status="superseded",
                    superseded_by="ADR-0029",
                ),
            )
            _write_document(
                stage_root,
                "decisions",
                "0029-successor.md",
                _document_text(
                    "adr",
                    "0029",
                    status="retired",
                    supersedes=("ADR-0027",),
                ),
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/validation/check-document-metadata.py"),
                    "--root",
                    directory,
                    "--profiles",
                    str(ROOT / "docs/99.templates/registry.json"),
                    "--mode",
                    "report",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("configuration-error:", result.stderr)
        self.assertIn("supersession-successor-not-effective", result.stderr)

    def test_archived_superseded_adr_is_reported(self) -> None:
        architecture = _architecture_module()
        predecessor = architecture.ArchitectureDocument(
            pathlib.PurePosixPath("docs/98.archive/decisions/0027-predecessor.md"),
            "ADR-0027",
            "adr",
            "superseded",
            ("AD-0001",),
            (),
            "ADR-0029",
        )
        successor = architecture.ArchitectureDocument(
            pathlib.PurePosixPath("docs/02.architecture/decisions/0029-successor.md"),
            "ADR-0029",
            "adr",
            "active",
            ("AD-0001",),
            ("ADR-0027",),
            None,
        )
        findings = architecture.validate_supersession_graph((predecessor, successor))
        self.assertIn("superseded-adr-archived", {item.code for item in findings})

    def test_restored_requirements_root_is_forbidden(self) -> None:
        architecture = _architecture_module()
        with tempfile.TemporaryDirectory() as directory:
            stage_root = pathlib.Path(directory) / "docs/02.architecture"
            _write_minimal_corpus(stage_root)
            stage_root.joinpath("requirements").mkdir()
            with self.assertRaisesRegex(
                architecture.ArchitectureDocumentError, "requirements"
            ):
                architecture.load_architecture_documents(stage_root)


if __name__ == "__main__":
    unittest.main()
