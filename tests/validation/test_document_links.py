from __future__ import annotations

import ast
import dataclasses
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
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

    def test_alignment_rejects_missing_and_current_to_archive_links(self) -> None:
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
                / "docs/05.operations/catalog/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md"
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
    def test_active_publications_do_not_instruct_deleted_shell_validators(self) -> None:
        from scripts.lib.document_governance.frontmatter import read_frontmatter_values

        candidates = [ROOT / "README.md"]
        for root in (
            ROOT / "docs/00.agent-governance/rules",
            ROOT / "docs/00.agent-governance/scopes",
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
            if metadata.get("status") in {"completed", "archived", "deprecated"}:
                continue
            text = path.read_text(encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
