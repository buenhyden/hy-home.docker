from __future__ import annotations

import ast
import dataclasses
import importlib.util
import io
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[3]
CLI = ROOT / "scripts/validation/check-document-links.py"
METADATA_CLI = ROOT / "scripts/validation/check-document-metadata.py"
LIFECYCLE_CLI = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
SCRIPT_MANIFEST_CLI = ROOT / "scripts/validation/check-script-manifest.py"


def load_metadata_cli():
    spec = importlib.util.spec_from_file_location("task10_document_metadata", METADATA_CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("metadata validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_script_manifest_cli():
    spec = importlib.util.spec_from_file_location(
        "task10_script_manifest", SCRIPT_MANIFEST_CLI
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("script manifest validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SharedDocumentGovernanceTests(unittest.TestCase):
    def test_exited_git_process_requires_complete_successful_drains(self) -> None:
        from scripts.lib.document_governance import git_provenance

        class DeferredDrain:
            def __init__(self, *, target, args=(), daemon=True):
                self.target, self.args = target, args

            def start(self):
                pass

            def join(self, timeout=None):
                self.target(*self.args)

            def is_alive(self):
                return False

        class BrokenStream(io.BytesIO):
            def read(self, size=-1):
                raise OSError("drain failed")

        for channel in ("stdout", "stderr"):
            for case in ("overflow", "error", "exact"):
                with self.subTest(channel=channel, case=case):
                    streams = {"stdout": io.BytesIO(), "stderr": io.BytesIO()}
                    streams[channel] = (
                        BrokenStream() if case == "error" else io.BytesIO(
                            b"x" * (git_provenance._GIT_OUTPUT_BYTES + (case == "overflow"))
                        )
                    )
                    process = mock.Mock(**streams, stdin=None, returncode=0)
                    process.poll.return_value = 0
                    with mock.patch.object(git_provenance.subprocess, "Popen", return_value=process), mock.patch.object(
                        git_provenance.threading, "Thread", DeferredDrain
                    ):
                        result = git_provenance._run_git(ROOT, ["cat-file", "blob", "object"])
                    if case == "exact":
                        self.assertEqual(result.returncode, 0)
                        self.assertEqual(len(getattr(result, channel)), git_provenance._GIT_OUTPUT_BYTES)
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertEqual(result.stdout, b"")

    def test_historical_document_requires_exact_regular_blob_recovery(self) -> None:
        from scripts.lib.document_governance.git_provenance import HistoricalDocument

        commit = "494065806794980080b081439298d7b534d10803"
        document = HistoricalDocument(ROOT, commit, "docs/99.templates/support/README.md")
        self.assertIn("#", document.read_text())
        for invalid_commit, invalid_path in (
            ("HEAD", "README.md"),
            (None, "README.md"),
            (commit, "../README.md"),
            (commit, "docs"),
            (commit, "missing.md"),
        ):
            with self.subTest(commit=invalid_commit, path=invalid_path):
                with self.assertRaises(ValueError):
                    HistoricalDocument(ROOT, invalid_commit, invalid_path).read_text()

    def test_graph_reads_large_task_evidence_and_keeps_a_finite_byte_limit(self) -> None:
        from scripts.lib.document_governance import links

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "source.md"
            target = root / "task.md"
            source.write_text("# Source\n[Evidence](task.md#evidence)\n", encoding="utf-8")
            target.write_text("# Evidence\n" + ("bounded evidence\n" * 140_000), encoding="utf-8")
            graph = links.build_document_graph((source, target), repo_root=root)
            self.assertEqual((), graph.input_findings)
            self.assertEqual(2, len(graph.nodes))
            target.write_text("x" * (4 * 1024 * 1024 + 1), encoding="utf-8")
            oversized = links.build_document_graph((target,), repo_root=root)
            self.assertEqual((), oversized.nodes)
            self.assertEqual("document-too-large", oversized.input_findings[0].code)

    def test_frontmatter_record_is_frozen_and_rejects_duplicate_keys(self) -> None:
        from scripts.lib.document_governance.frontmatter import (
            FrontmatterError,
            FrontmatterRecord,
            read_frontmatter,
        )

        self.assertTrue(dataclasses.is_dataclass(FrontmatterRecord))
        self.assertTrue(FrontmatterRecord.__dataclass_params__.frozen)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "record.md"
            path.write_text("---\nstatus: active\nstatus: draft\n---\n# Body\n")
            with self.assertRaises(FrontmatterError) as raised:
                read_frontmatter(path)
        self.assertEqual("duplicate-key", raised.exception.code)

    def test_frontmatter_record_metadata_is_deeply_immutable_and_copy_isolated(self) -> None:
        from scripts.lib.document_governance.frontmatter import (
            read_frontmatter,
            read_frontmatter_values,
        )

        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "record.md"
            path.write_text(
                "---\nlabels: [one, two]\nnested:\n  key: value\n---\n# Body\n",
                encoding="utf-8",
            )
            record = read_frontmatter(path)
            first = read_frontmatter_values(path)
            first["labels"].append("changed")
            second = read_frontmatter_values(path)
        with self.assertRaises(TypeError):
            record.metadata["new"] = "value"
        self.assertEqual(("one", "two"), record.metadata["labels"])
        self.assertEqual(["one", "two"], second["labels"])

    def test_frontmatter_rejects_cyclic_aliases_during_deep_freeze(self) -> None:
        from scripts.lib.document_governance.frontmatter import (
            FrontmatterError,
            frontmatter_record_from_text,
        )

        source = "---\ncycle: &cycle\n  - *cycle\n---\n# Body\n"
        with self.assertRaises(FrontmatterError) as raised:
            frontmatter_record_from_text(pathlib.Path("cycle.md"), source)
        self.assertEqual("cyclic-value", raised.exception.code)

    def test_metadata_cli_uses_the_shared_frontmatter_parser(self) -> None:
        from scripts.lib.document_governance import frontmatter

        metadata = load_metadata_cli()
        self.assertIs(frontmatter.read_frontmatter_values, metadata.parse_frontmatter)
        self.assertIs(frontmatter.parse_frontmatter_text, metadata._parse_frontmatter_text)

    def test_git_provenance_is_frozen_and_proves_regular_blob(self) -> None:
        from scripts.lib.document_governance.git_provenance import (
            Provenance,
            resolve_git_provenance,
        )

        self.assertTrue(dataclasses.is_dataclass(Provenance))
        self.assertTrue(Provenance.__dataclass_params__.frozen)
        proven = resolve_git_provenance(
            pathlib.PurePosixPath("README.md"), "HEAD", repo_root=ROOT
        )
        self.assertTrue(proven.is_regular_blob)
        self.assertEqual("blob", proven.object_type)
        missing = resolve_git_provenance(
            pathlib.PurePosixPath("docs/does-not-exist.md"), "HEAD", repo_root=ROOT
        )
        self.assertFalse(missing.exists)
        self.assertFalse(missing.is_regular_blob)

    def test_git_provenance_rejects_nul_tree_and_missing_objects(self) -> None:
        from scripts.lib.document_governance import git_provenance
        from scripts.lib.document_governance.git_provenance import resolve_git_provenance

        nul = resolve_git_provenance("README.md\x00other", "HEAD", repo_root=ROOT)
        nul_commit = resolve_git_provenance("README.md", "HEAD\x00other", repo_root=ROOT)
        tree = resolve_git_provenance("docs", "HEAD", repo_root=ROOT)
        missing_object = resolve_git_provenance(
            "README.md", "f" * 40, repo_root=ROOT
        )
        self.assertFalse(nul.exists)
        self.assertFalse(nul_commit.exists)
        self.assertFalse(tree.is_regular_blob)
        self.assertFalse(missing_object.exists)

        completed = subprocess.CompletedProcess
        responses = iter(
            (
                completed([], 0, stdout=("a" * 40 + "\n").encode(), stderr=b""),
                completed(
                    [],
                    0,
                    stdout=(f"100644 blob {'b' * 40}\tREADME.md\0").encode(),
                    stderr=b"",
                ),
                completed([], 1, stdout=b"", stderr=b"missing"),
            )
        )
        with mock.patch.object(
            git_provenance, "_run_git", side_effect=lambda *_: next(responses)
        ):
            missing_blob = resolve_git_provenance(
                "README.md", "HEAD", repo_root=ROOT
            )
        self.assertTrue(missing_blob.exists)
        self.assertFalse(missing_blob.is_regular_blob)

    def test_git_provenance_rejects_ambiguous_ls_tree_records(self) -> None:
        from scripts.lib.document_governance import git_provenance

        completed = subprocess.CompletedProcess
        row = f"100644 blob {'b' * 40}\tREADME.md\0".encode()
        responses = iter(
            (
                completed([], 0, stdout=("a" * 40 + "\n").encode(), stderr=b""),
                completed([], 0, stdout=row + row, stderr=b""),
            )
        )
        with mock.patch.object(
            git_provenance, "_run_git", side_effect=lambda *_: next(responses)
        ):
            provenance = git_provenance.resolve_git_provenance(
                "README.md", "HEAD", repo_root=ROOT
            )
        self.assertFalse(provenance.exists)
        self.assertFalse(provenance.is_regular_blob)

    def test_lifecycle_imports_shared_governance_instead_of_metadata_cli(self) -> None:
        source = LIFECYCLE_CLI.read_text()
        tree = ast.parse(source)
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertNotIn("check-document-metadata", imported)
        self.assertNotIn("check_document_metadata", imported)
        self.assertNotIn("_load_metadata_module", source)
        self.assertIn("metadata_contract", source)

    def test_manifest_yaml_evidence_requires_an_exact_typed_entry(self) -> None:
        checker = load_script_manifest_cli()
        target = "scripts/example.py"
        self.assertTrue(
            checker._reference_proves_use(
                ".pre-commit-config.yaml",
                "entry: python3 scripts/example.py --check\n",
                target,
                is_test=False,
            )
        )
        for invalid in (
            "# entry: python3 scripts/example.py --check\n",
            "entry: python3 scripts/example.py-extra --check\n",
        ):
            self.assertFalse(
                checker._reference_proves_use(
                    ".pre-commit-config.yaml", invalid, target, is_test=False
                )
            )

    def test_manifest_yaml_cycle_is_an_explicit_finding(self) -> None:
        checker = load_script_manifest_cli()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / ".pre-commit-config.yaml").write_text(
                "entry: &loop\n  - *loop\n", encoding="utf-8"
            )
            codes = {
                finding.code
                for finding in checker._semantic_findings(
                    root,
                    {
                        "files": [
                            {
                                "path": "scripts/example.py",
                                "consumers": [".pre-commit-config.yaml"],
                                "tests": [],
                            }
                        ]
                    },
                )
            }
        self.assertIn("consumers-invalid", codes)


class DocumentGraphTests(unittest.TestCase):
    def test_fence_info_comment_opener_does_not_hide_later_rendered_links(self) -> None:
        from scripts.lib.document_governance.links import parse_local_markdown_links

        links = parse_local_markdown_links(
            pathlib.PurePosixPath("docs/source.md"),
            """```text <!--
[hidden](hidden.md)
```
[visible](visible.md)
""",
        )

        self.assertEqual(
            ("docs/visible.md",),
            tuple(link.target.as_posix() for link in links),
        )

    def test_inline_code_comment_opener_does_not_hide_later_rendered_links(self) -> None:
        from scripts.lib.document_governance.links import parse_local_markdown_links

        links = parse_local_markdown_links(
            pathlib.PurePosixPath("docs/source.md"),
            """`<!--`
[visible](visible.md)
<!--
[hidden](hidden.md)
-->
[after](after.md)
""",
        )

        self.assertEqual(
            ("docs/visible.md", "docs/after.md"),
            tuple(link.target.as_posix() for link in links),
        )
        self.assertEqual(("visible", "after"), tuple(link.label for link in links))

    def test_local_markdown_link_parser_ignores_nonrendered_links(self) -> None:
        from scripts.lib.document_governance.links import parse_local_markdown_links

        links = parse_local_markdown_links(
            pathlib.PurePosixPath("docs/source.md"),
            """[rendered](rendered.md)
`[inline](inline.md)`
![image](image.md)
```markdown
[fenced](fenced.md)
```
<!-- [single-comment](single-comment.md) -->
<!--
[multi-comment](multi-comment.md)
-->
""",
        )

        self.assertEqual(
            ("docs/rendered.md",),
            tuple(link.target.as_posix() for link in links),
        )

    def test_local_markdown_link_parser_is_immutable_and_normalizes_without_io(
        self,
    ) -> None:
        from scripts.lib.document_governance.links import parse_local_markdown_links

        source = pathlib.PurePosixPath("docs/05.operations/README.md")
        links = parse_local_markdown_links(
            source,
            """[angle](<catalog/>)
[query](incidents/?view=all)
[fragment](releases/#latest)
[encoded](%63atalog/)
[nested](incidents/(current)/../)
`[inline](inline-fake/)`
```markdown
[fenced](fenced-fake/)
```
[external](https://example.com/reference/)
[absolute](/docs/05.operations/catalog/)
[outside](%2e%2e/%2e%2e/%2e%2e/escape/)
[self](#top)
[file](history.md)
[query-control](catalog/?bad=%00)
[fragment-control](catalog/#bad=%1F)
""",
        )

        self.assertIsInstance(links, tuple)
        self.assertEqual(
            (
                "docs/05.operations/catalog",
                "docs/05.operations/incidents",
                "docs/05.operations/releases",
                "docs/05.operations/catalog",
                "docs/05.operations/incidents",
                "docs/05.operations/catalog",
                "../escape",
                "docs/05.operations/README.md",
                "docs/05.operations/history.md",
                "docs/05.operations/catalog",
                "docs/05.operations/catalog",
            ),
            tuple(link.target.as_posix() for link in links),
        )
        self.assertEqual(
            (False, False, False, False, False, True, False, False, False, False, False),
            tuple(link.absolute for link in links),
        )
        self.assertEqual(
            (False, False, False, False, False, False, True, False, False, False, False),
            tuple(link.outside_repository for link in links),
        )
        self.assertEqual(
            (True, True, True, True, True, True, True, False, False, True, True),
            tuple(link.is_directory_route for link in links),
        )
        self.assertEqual(
            (False, False, False, False, False, True, True, False, False, True, True),
            tuple(link.has_unsafe_target for link in links),
        )
        self.assertIn("\x00", links[-2].decoded_target)
        self.assertIn("\x1f", links[-1].decoded_target)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            links[0].line = 99  # type: ignore[misc]

    def test_retired_role_root_implementation_selector_has_no_current_inputs(self) -> None:
        selected: list[str] = []
        operations = ROOT / "docs/05.operations"
        for role_root in ("guides", "policies", "runbooks"):
            bucket = operations / role_root
            if bucket.is_dir():
                selected.extend(
                    path.relative_to(ROOT).as_posix()
                    for path in bucket.rglob("*.md")
                    if path.name != "README.md"
                )

        self.assertEqual([], selected)

    def test_graph_ignores_fences_and_resolves_relative_links_and_anchors(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/source.md"
            target = root / "docs/target.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "# Source\n\n[ok](target.md#target)\n\n"
                "```markdown\n[example](missing.md)\n```\n",
                encoding="utf-8",
            )
            target.write_text("# Target\n", encoding="utf-8")
            graph = build_document_graph([source, target], repo_root=root)
        self.assertEqual(2, len(graph.nodes))
        self.assertEqual(1, len(graph.links))
        self.assertEqual("docs/target.md", graph.links[0].target.as_posix())
        self.assertEqual("target", graph.links[0].fragment)

    def test_graph_ignores_inline_code_and_parses_angle_and_nested_destinations(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/source.md"
            target = root / "docs/target_(one).md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "`[example](missing.md)` [angle](<target_(one).md>) "
                "[nested](target_(one).md)\n",
                encoding="utf-8",
            )
            target.write_text("# Target\n", encoding="utf-8")
            graph = build_document_graph([source, target], repo_root=root)
        self.assertEqual(2, len(graph.links))
        self.assertEqual(
            {"docs/target_(one).md"}, {link.target.as_posix() for link in graph.links}
        )

    def test_graph_reports_unreadable_invalid_utf8_and_symlink_escape_inputs(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            invalid = root / "docs/invalid.md"
            invalid.parent.mkdir(parents=True)
            invalid.write_bytes(b"\xff")
            outside = root.parent / f"{root.name}-outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            escaped = root / "docs/escaped.md"
            escaped.symlink_to(outside)
            try:
                graph = build_document_graph([invalid, escaped, outside], repo_root=root)
                codes = {finding.code for finding in check_alignment(graph)}
            finally:
                outside.unlink(missing_ok=True)
        self.assertIn("document-invalid-utf8", codes)
        self.assertIn("document-symlink", codes)
        self.assertIn("document-outside-repository", codes)

    def test_graph_rejects_source_symlink_ancestors_and_lexical_parent_escape(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp) / "repo"
            outside = pathlib.Path(temp) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "source.md").write_text("# Outside\n", encoding="utf-8")
            (root / "linked").symlink_to(outside, target_is_directory=True)
            graph = build_document_graph(
                [root / "linked/source.md", root / "../outside/source.md"],
                repo_root=root,
            )
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertIn("document-symlink-ancestor", codes)
        self.assertIn("document-outside-repository", codes)

    def test_malformed_frontmatter_is_immutable_and_reported(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/source.md"
            source.parent.mkdir(parents=True)
            source.write_text("---\nstatus: [\n---\n# Source\n", encoding="utf-8")
            graph = build_document_graph([source], repo_root=root)
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertIn("document-frontmatter-invalid", codes)
        with self.assertRaises(TypeError):
            graph.nodes[0].metadata["status"] = "active"

    def test_alignment_rejects_missing_and_current_to_tombstone_links(self) -> None:
        from scripts.lib.document_governance.links import (
            build_document_graph,
            check_alignment,
        )

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/03.specs/spec-0001/example.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "# Source\n\n[missing](missing.md)\n"
                "[archive](../../98.archive/tombstones/example.md)\n",
                encoding="utf-8",
            )
            graph = build_document_graph([source], repo_root=root)
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertIn("missing-link-target", codes)
        self.assertIn("active-archive-link", codes)

    def test_alignment_allows_current_to_archive_index_and_migration_links(self) -> None:
        from scripts.lib.document_governance.links import (
            archive_direct_link_total,
            build_document_graph,
            check_alignment,
        )

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/03.specs/0001-current/spec.md"
            readme = root / "docs/98.archive/README.md"
            migration = root / "docs/98.archive/migrations/0001-map.md"
            source.parent.mkdir(parents=True)
            readme.parent.mkdir(parents=True)
            migration.parent.mkdir(parents=True)
            source.write_text(
                "# Source\n\n[archive](../../98.archive/README.md)\n"
                "[migration](../../98.archive/migrations/0001-map.md)\n",
                encoding="utf-8",
            )
            readme.write_text("# Archive\n", encoding="utf-8")
            migration.write_text("# Migration\n", encoding="utf-8")
            graph = build_document_graph([source, readme, migration], repo_root=root)
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertNotIn("active-archive-link", codes)
        self.assertEqual(0, archive_direct_link_total(graph))

    def test_alignment_preserves_removed_template_detection(self) -> None:
        from scripts.lib.document_governance.links import (
            build_document_graph,
            check_alignment,
        )

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/03.specs/spec-0001/example.md"
            source.parent.mkdir(parents=True)
            source.write_text("Use operation.template.md.\n", encoding="utf-8")
            graph = build_document_graph([source], repo_root=root)
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertIn("removed-template-name", codes)

    def test_alignment_validates_same_document_and_unselected_markdown_anchors(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/source.md"
            target = root / "other/target.md"
            source.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            source.write_text(
                "# Source\n[same](#missing) [other](../other/target.md#missing)\n",
                encoding="utf-8",
            )
            target.write_text("# Present\n", encoding="utf-8")
            graph = build_document_graph([source], repo_root=root)
            findings = check_alignment(graph)
        self.assertEqual(2, sum(item.code == "missing-link-anchor" for item in findings))

    def test_alignment_rejects_symlink_and_non_regular_targets(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "docs/source.md"
            target_dir = root / "docs/directory"
            outside = root.parent / f"{root.name}-target.md"
            source.parent.mkdir(parents=True)
            target_dir.mkdir()
            outside.write_text("# Outside\n", encoding="utf-8")
            escaped = root / "docs/escaped.md"
            escaped.symlink_to(outside)
            source.write_text(
                "[dir](directory) [escape](escaped.md)\n", encoding="utf-8"
            )
            try:
                graph = build_document_graph([source], repo_root=root)
                codes = {finding.code for finding in check_alignment(graph)}
            finally:
                outside.unlink(missing_ok=True)
        self.assertIn("link-target-not-regular", codes)
        self.assertIn("link-target-symlink", codes)

    def test_alignment_rejects_target_symlink_ancestors(self) -> None:
        from scripts.lib.document_governance.links import build_document_graph, check_alignment

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp) / "repo"
            outside = pathlib.Path(temp) / "outside"
            source = root / "docs/source.md"
            root.mkdir()
            outside.mkdir()
            source.parent.mkdir()
            (outside / "target.md").write_text("# Target\n", encoding="utf-8")
            (root / "linked").symlink_to(outside, target_is_directory=True)
            source.write_text("[escape](../linked/target.md)\n", encoding="utf-8")
            graph = build_document_graph([source], repo_root=root)
            codes = {finding.code for finding in check_alignment(graph)}
        self.assertIn("link-target-symlink-ancestor", codes)

    def test_traceability_fixture_accepts_reciprocal_indexes_and_catalog_pairs(self) -> None:
        from scripts.lib.document_governance.links import (
            build_document_graph,
            check_traceability,
        )

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            specs = root / "docs/03.specs/README.md"
            ops = root / "docs/05.operations/README.md"
            catalog = (
                root
                / "docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md"
            )
            guide = catalog.parent / "subject/guide.md"
            runbook = catalog.parent / "subject/runbook.md"
            for path in (specs, ops, catalog, guide, runbook):
                path.parent.mkdir(parents=True, exist_ok=True)
            specs.write_text("[Operations](../05.operations/README.md)\n")
            ops.write_text("[Specs](../03.specs/README.md)\n")
            catalog.write_text("[OPER](subject/guide.md), [RUN](subject/runbook.md)\n")
            guide.write_text("# Guide\n")
            runbook.write_text("# Runbook\n")
            graph = build_document_graph(
                [specs, ops, catalog, guide, runbook], repo_root=root
            )
            findings = check_traceability(graph)
        self.assertEqual([], findings)


class DocumentLinksCliTests(unittest.TestCase):
    def test_transition_shells_delegate_exact_modes_direct_and_held(self) -> None:
        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        env["PYTHONSAFEPATH"] = "1"
        for name, mode in (
            ("check-doc-traceability.sh", "traceability"),
            ("check-doc-implementation-alignment.sh", "alignment"),
        ):
            script = ROOT / "scripts/validation" / name
            with script.open("rb") as held:
                for path in (str(script), f"/proc/self/fd/{held.fileno()}"):
                    with self.subTest(mode=mode, path=path):
                        result = subprocess.run(
                            ["bash", path], cwd=ROOT, env=env,
                            pass_fds=(held.fileno(),), capture_output=True,
                            text=True, check=False,
                        )
                        self.assertEqual(0, result.returncode, result.stderr)
                        self.assertIn(f"mode={mode}", result.stdout)

    def test_transition_shells_preserve_canonical_failures_and_reject_extra_argv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "scripts/validation").mkdir(parents=True)
            shutil.copy2(CLI, root / "scripts/validation" / CLI.name)
            shutil.copytree(ROOT / "scripts/lib", root / "scripts/lib")
            source = root / "docs/03.specs/README.md"
            source.parent.mkdir(parents=True)
            source.write_text("[missing](missing.md)\n", encoding="utf-8")
            for name, expected in (
                ("check-doc-traceability.sh", "traceability-file-missing"),
                ("check-doc-implementation-alignment.sh", "missing-link-target"),
            ):
                script = ROOT / "scripts/validation" / name
                with self.subTest(name=name):
                    result = subprocess.run(
                        ["bash", str(script)], cwd=root,
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertIn(expected, result.stderr)
                    rejected = subprocess.run(
                        ["bash", str(script), "--mode", "all"], cwd=ROOT,
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(2, rejected.returncode)

    def test_historical_command_evidence_does_not_hide_current_commands(self) -> None:
        from scripts.validation.agent_governance_contract import HISTORICAL_TABLE_MARKER, current_markdown_authority

        command = "bash scripts/validation/check-doc-traceability.sh"
        table = f"{HISTORICAL_TABLE_MARKER}\n| Command | Result |\n| --- | --- |\n| `{command}` | observed PASS |\n"
        self.assertNotIn(command, current_markdown_authority(table))
        self.assertIn(command, current_markdown_authority(table + f"\n{command}\n"))
        self.assertIn(command, current_markdown_authority(table.replace("| --- | --- |", "invalid separator")))

    def test_active_publications_do_not_instruct_deleted_shell_validators(self) -> None:
        from scripts.lib.document_governance.frontmatter import read_frontmatter_values
        from scripts.validation.agent_governance_contract import current_markdown_authority

        candidates = [ROOT / "README.md"]
        for root in (
            ROOT / "docs/00.agent-governance/policies",
            ROOT / "docs/00.agent-governance/roles",
            ROOT / "docs/01.requirements",
            ROOT / "docs/02.architecture",
            ROOT / "docs/03.specs",
            ROOT / "docs/05.operations",
            ROOT / "infra",
        ):
            candidates.extend(root.rglob("*.md"))
        failures: list[str] = []
        for path in sorted(set(candidates)):
            if path.name in {"plan.md", "task.md"}:
                continue
            metadata = read_frontmatter_values(path)
            if metadata.get("status") in {"completed", "archived", "deprecated", "retired"}:
                continue
            text = current_markdown_authority(path.read_text(encoding="utf-8"))
            if "check-doc-traceability.sh" in text or "check-doc-implementation-alignment.sh" in text:
                failures.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], failures)

    def test_repository_modes_are_deterministic_and_non_mutating(self) -> None:
        before = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        for mode in ("traceability", "alignment"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    [sys.executable, str(CLI), "--mode", mode],
                    cwd=ROOT,
                    text=True,
                    check=False,
                    capture_output=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(f"mode={mode}", result.stdout)
        after = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(before, after)

    def test_cli_rejects_unknown_mode(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CLI), "--mode", "unknown"],
            cwd=ROOT,
            text=True,
            check=False,
            capture_output=True,
        )
        self.assertNotEqual(0, result.returncode)


def load_links_cli():
    spec = importlib.util.spec_from_file_location("task10_document_links", CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("link validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LinkSelectionScopeTests(unittest.TestCase):
    """The gate must read the corpus it is supposed to protect."""

    def _tree(self, root: pathlib.Path, *relatives: str) -> None:
        for relative in relatives:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# x\n", encoding="utf-8")

    def test_selection_covers_every_tracked_documentation_root(self) -> None:
        module = load_links_cli()
        expected = (
            "docs/00.agent-governance/policies/x.md",
            "docs/01.requirements/0001-a.md",
            "docs/02.architecture/decisions/0001-a.md",
            "docs/03.specs/0001-a/spec.md",
            "docs/05.operations/catalog/00-workspace/0001-a/guide.md",
            "docs/90.references/audits/0001-a/README.md",
            "docs/98.archive/migrations/0001-a.md",
            "docs/99.templates/README.md",
        )
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, *expected)
            selected = {
                path.relative_to(root).as_posix() for path in module._paths(root)
            }
            for relative in expected:
                self.assertIn(relative, selected)

    def test_selection_skips_superseded_and_retired_documents(self) -> None:
        module = load_links_cli()
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            for name, status in (("a", "superseded"), ("b", "retired"), ("c", "active")):
                target = root / f"docs/90.references/audits/0001-{name}/README.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    f"---\nstatus: {status}\n---\n\n# {name}\n", encoding="utf-8"
                )
            selected = {
                path.relative_to(root).as_posix() for path in module._paths(root)
            }
            self.assertNotIn("docs/90.references/audits/0001-a/README.md", selected)
            self.assertNotIn("docs/90.references/audits/0001-b/README.md", selected)
            self.assertIn("docs/90.references/audits/0001-c/README.md", selected)

    def test_selection_has_no_path_exemption(self) -> None:
        """Nothing is skipped for where it lives, only for what it claims.

        The two agentic research packs were exempted by path while SPEC-0137's
        disposition was undecided. That Spec Package is now `completed` and the
        exemption is gone: a research document is read like any other, and a
        superseded one is skipped by its own status, not by its directory.
        """

        module = load_links_cli()
        self.assertFalse(hasattr(module, "DEFERRED_PREFIXES"))
        self.assertFalse(hasattr(module, "_deferred"))
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(
                root,
                "docs/90.references/research/0001-agentic-research-pack-refresh/x.md",
                "docs/90.references/research/0002-agentic-engineering-research-pack/x.md",
                "docs/90.references/research/0084-github-actions-platform/README.md",
            )
            selected = {
                path.relative_to(root).as_posix() for path in module._paths(root)
            }
            for relative in (
                "docs/90.references/research/0001-agentic-research-pack-refresh/x.md",
                "docs/90.references/research/0002-agentic-engineering-research-pack/x.md",
                "docs/90.references/research/0084-github-actions-platform/README.md",
            ):
                self.assertIn(relative, selected)


if __name__ == "__main__":
    unittest.main()
