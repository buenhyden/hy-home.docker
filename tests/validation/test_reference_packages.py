from __future__ import annotations

import pathlib
import os
import shutil
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]


def reference_api():
    try:
        from scripts.lib.document_governance import references
    except ImportError as exc:  # RED: the Task 9 authority does not exist yet.
        raise AssertionError("Task 9 reference authority is missing") from exc
    return references


class ReferencePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.references = reference_api()

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        for source in (
            "docs/90.references",
            "docs/99.templates/registry.json",
            "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md",
        ):
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            if (ROOT / source).is_dir():
                shutil.copytree(ROOT / source, target)
            else:
                shutil.copy2(ROOT / source, target)
        return directory, root

    def finding_codes(self, root: pathlib.Path = ROOT) -> set[str]:
        return {
            finding.code
            for finding in self.references.validate_current_references(root)
        }

    def test_current_reference_topology_matches_the_frozen_migration(self) -> None:
        migration = self.references.load_task9_migration(ROOT)
        self.assertEqual(tuple(f"mig-0003-r{n:04d}" for n in range(450, 566)), migration.row_ids)
        self.assertEqual(105, sum(row.action == "rename" for row in migration.rows))
        self.assertEqual(11, sum(row.action == "delete" for row in migration.rows))
        self.assertEqual(set(), self.finding_codes())

    def test_reference_roots_and_package_paths_are_exact(self) -> None:
        corpus = self.references.load_reference_packages(ROOT / "docs/90.references")
        self.assertEqual(("audits", "data", "research"), corpus.category_names)
        self.assertEqual(
            {"AUD-", "DATA-", "RES-"},
            {item.artifact_id.rsplit("-", 1)[0] + "-" for item in corpus.packages},
        )
        self.assertTrue(all(self.references.PACKAGE_PATH.fullmatch(item.relative_package) for item in corpus.packages))
        self.assertFalse(any(item.overrides_normative_stage for item in corpus.packages))

    def test_dated_or_prefixed_package_is_rejected(self) -> None:
        for invalid in ("2026-08-08-dated", "res-0099-prefixed", "aud-0099-prefixed"):
            with self.subTest(invalid=invalid):
                context, root = self._fixture()
                with context:
                    source = next((root / "docs/90.references/research").glob("[0-9][0-9][0-9][0-9]-*"))
                    source.rename(source.with_name(invalid))
                    self.assertIn("package-path-invalid", self.finding_codes(root))

        context, root = self._fixture()
        with context:
            (root / "docs/90.references/data/2026-08-23-empty").mkdir()
            self.assertTrue(
                {"package-path-invalid", "reference-corpus-invalid"}
                & self.finding_codes(root)
            )

    def test_retired_root_and_redirect_document_are_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            retired = root / "docs/90.references/learning"
            retired.mkdir()
            (retired / "README.md").write_text("# Moved\n\nSee ../research/.\n", encoding="utf-8")
            self.assertIn("retired-root-present", self.finding_codes(root))

        context, root = self._fixture()
        with context:
            redirect = next(
                (root / "docs/90.references/research").glob(
                    "[0-9][0-9][0-9][0-9]-*/README.md"
                )
            )
            metadata, separator, _ = redirect.read_text(encoding="utf-8").partition(
                "\n---\n"
            )
            self.assertEqual("\n---\n", separator)
            redirect.write_text(
                metadata
                + separator
                + "# Redirect\n\nMoved to ../0002-agentic-engineering-research-pack/.\n",
                encoding="utf-8",
            )
            self.assertIn("redirect-document-present", self.finding_codes(root))

        context, root = self._fixture()
        with context:
            unregistered = root / "docs/90.references/data/legacy/nested.md"
            unregistered.parent.mkdir()
            unregistered.write_text("# Legacy inventory\n", encoding="utf-8")
            self.assertTrue(
                {"unregistered-reference-file", "reference-corpus-invalid"}
                & self.finding_codes(root)
            )

    def test_package_identity_must_match_category_and_directory(self) -> None:
        context, root = self._fixture()
        with context:
            package = next((root / "docs/90.references/audits").glob("[0-9][0-9][0-9][0-9]-*/README.md"))
            package.write_text(
                package.read_text(encoding="utf-8").replace("artifact_id: AUD-", "artifact_id: RES-", 1),
                encoding="utf-8",
            )
            self.assertIn("package-identity-invalid", self.finding_codes(root))

    def test_stage90_cannot_override_normative_stages(self) -> None:
        context, root = self._fixture()
        with context:
            package = next((root / "docs/90.references/research").glob("[0-9][0-9][0-9][0-9]-*/README.md"))
            package.write_text(
                package.read_text(encoding="utf-8")
                + "\nStage 90 overrides Stage 00 policy and takes precedence over Stage 03.\n",
                encoding="utf-8",
            )
            self.assertIn("normative-authority-override", self.finding_codes(root))

    def test_current_clickable_link_to_retired_root_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            readme = root / "docs/90.references/README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "\n[retired learning](./learning/README.md)\n",
                encoding="utf-8",
            )
            self.assertIn("retired-link-present", self.finding_codes(root))

    def test_every_markdown_payload_uses_normalized_retired_link_targets(self) -> None:
        context, root = self._fixture()
        with context:
            package = next(
                (root / "docs/90.references/research").glob(
                    "[0-9][0-9][0-9][0-9]-*"
                )
            )
            payload = package / "payload.md"
            payload.write_text(
                "\n".join(
                    (
                        "[relative](../../%6clm-wiki/README.md?view=1#top)",
                        "[root](</docs/90.references/learning/README.md#top>)",
                        "![image](../../learning/asset.png)",
                        "[nested](../../data/%73ecurity/ref-0078.md)",
                        "[angle](<../../data/governance/ref-0071.yaml>)",
                        "![nested image](../../data/docker/asset.png)",
                        "<!-- [comment](../../llm-wiki/README.md) -->",
                        "<!-- [old data](../../data/security/ref.md) -->",
                        "`[code](../../llm-wiki/README.md)`",
                        "`[old data](../../data/governance/ref.yaml)`",
                        "```markdown",
                        "[fenced](../../llm-wiki/README.md)",
                        "[old data](../../data/docker/ref.md)",
                        "```",
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            findings = self.references.validate_current_references(root)
            retired = [item for item in findings if item.code == "retired-link-present"]
            self.assertEqual(6, len(retired))
            self.assertTrue(all(item.path.name == "payload.md" for item in retired))

    def test_generated_repository_map_rejects_missing_local_links(self) -> None:
        context, root = self._fixture()
        with context:
            repository_map = (
                root / "docs/90.references/data/0083-repository-map/README.md"
            )
            repository_map.write_text(
                repository_map.read_text(encoding="utf-8")
                + "\n[removed](../data/docker/README.md)\n",
                encoding="utf-8",
            )
            self.assertIn("generated-data-link-missing", self.finding_codes(root))

    def test_reference_traversal_rejects_symlinks_fifos_and_budget_overflow(self) -> None:
        for unsafe in ("broken-symlink", "live-symlink", "fifo"):
            with self.subTest(unsafe=unsafe):
                context, root = self._fixture()
                with context:
                    data = root / "docs/90.references/data"
                    if unsafe == "broken-symlink":
                        (data / "0099-broken").symlink_to(
                            data / "missing", target_is_directory=True
                        )
                    elif unsafe == "live-symlink":
                        target = next(data.glob("[0-9][0-9][0-9][0-9]-*"))
                        (data / "0099-live").symlink_to(target, target_is_directory=True)
                    else:
                        os.mkfifo(data / "unregistered.pipe")
                    self.assertIn("reference-corpus-invalid", self.finding_codes(root))

        context, root = self._fixture()
        with context, mock.patch.object(self.references, "MAX_CATEGORY_ENTRIES", 1):
            self.assertIn("reference-corpus-invalid", self.finding_codes(root))

        context, root = self._fixture()
        with context, mock.patch.object(self.references, "MAX_REFERENCE_FILE_BYTES", 32):
            self.assertIn("reference-corpus-invalid", self.finding_codes(root))

        context, root = self._fixture()
        with context, mock.patch.object(self.references, "MAX_TOTAL_REFERENCE_BYTES", 64):
            self.assertIn("reference-corpus-invalid", self.finding_codes(root))

    def test_descriptor_reader_rejects_missing_and_swapped_leaf_races(self) -> None:
        for mutation in ("missing", "swap"):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as directory:
                    parent = pathlib.Path(directory)
                    (parent / "README.md").write_text("original\n", encoding="utf-8")
                    descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
                    original_stat = os.stat
                    calls = 0

                    def racing_stat(path, *args, **kwargs):
                        nonlocal calls
                        if path == "README.md" and kwargs.get("dir_fd") == descriptor:
                            calls += 1
                            if calls == 2:
                                os.unlink(path, dir_fd=descriptor)
                                if mutation == "swap":
                                    replacement = os.open(
                                        path,
                                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                                        0o600,
                                        dir_fd=descriptor,
                                    )
                                    os.write(replacement, b"replacement\n")
                                    os.close(replacement)
                        return original_stat(path, *args, **kwargs)

                    try:
                        with mock.patch.object(self.references.os, "stat", racing_stat):
                            with self.assertRaises(self.references.ReferenceCorpusError):
                                self.references._read_regular_utf8(
                                    descriptor,
                                    "README.md",
                                    "race fixture",
                                    self.references._LoadBudget(),
                                )
                    finally:
                        os.close(descriptor)

    def test_authority_and_redirect_classification_is_semantic_and_padding_independent(self) -> None:
        context, root = self._fixture()
        with context:
            package = next(
                (root / "docs/90.references/research").glob(
                    "[0-9][0-9][0-9][0-9]-*/README.md"
                )
            )
            original = package.read_text(encoding="utf-8")
            package.write_text(
                original
                + "\nStage 90 should not override Stage 00 policy.\n"
                + "Stage 90 is not authoritative over Stage 03.\n",
                encoding="utf-8",
            )
            self.assertNotIn("normative-authority-override", self.finding_codes(root))
            package.write_text(
                original
                + "\nStage 00 is overridden by Stage 90 policy.\n"
                + "Stage 90 policy\nsupersedes Stage 05 and should not be ignored.\n",
                encoding="utf-8",
            )
            self.assertIn("normative-authority-override", self.finding_codes(root))

        context, root = self._fixture()
        with context:
            package = next(
                (root / "docs/90.references/research").glob(
                    "[0-9][0-9][0-9][0-9]-*/README.md"
                )
            )
            package.write_text(
                "# Redirect\n\nMoved to [current](../0084-github-actions-platform/).\n"
                + (" " * 8192)
                + "\n",
                encoding="utf-8",
            )
            self.assertIn("redirect-document-present", self.finding_codes(root))

            package.write_text(
                "# Deprecated algorithms\n\n## Findings\n\nThis research compares retired algorithms.\n",
                encoding="utf-8",
            )
            self.assertNotIn("redirect-document-present", self.finding_codes(root))

    def test_rendered_body_lexer_clauses_and_redirect_grammar_are_exact(self) -> None:
        authority = self.references._asserts_normative_authority
        redirect = self.references._is_redirect_only

        self.assertTrue(authority("`<!--`\n\nStage 90 overrides Stage 00 policy."))
        self.assertTrue(
            authority("```markdown\n<!--\n```\n\nStage 90 supersedes Stage 01 policy.")
        )
        self.assertTrue(
            authority(
                "```text <!--\nexample\n```\n\nStage 90 overrides Stage 00 policy."
            )
        )
        self.assertTrue(
            authority("Stage 90 is not descriptive but overrides Stage 00 policy.")
        )
        self.assertTrue(
            authority("Stage 90 is not descriptive and overrides Stage 00 policy.")
        )
        self.assertTrue(
            authority("Stage 00 is not descriptive but is overridden by Stage 90.")
        )
        self.assertTrue(
            authority("Stage 90 is not descriptive but takes precedence over Stage 02.")
        )
        self.assertFalse(authority("Stage 90 is non-normative relative to Stage 00."))
        self.assertFalse(authority("<!-- Stage 90 overrides Stage 00. -->"))
        self.assertFalse(authority("```text\nStage 90 overrides Stage 00.\n```"))
        self.assertFalse(authority("`Stage 90 overrides Stage 00.`"))

        self.assertTrue(redirect("# Deprecated\n\nUse [current](../current/).\n"))
        self.assertTrue(
            redirect(
                "# Redirect\n\nMoved to "
                "[current](docs/90.references/research/0002-agentic-engineering-research-pack/).\n"
            )
        )
        self.assertTrue(
            redirect(
                "# Redirect\n\nMoved to ../0002-agentic-engineering-research-pack/.\n"
            )
        )
        self.assertTrue(
            redirect(
                "# Moved\n\nReplaced by "
                "docs/90.references/research/0002-agentic-engineering-research-pack/!\n"
            )
        )
        self.assertFalse(
            redirect(
                "# Deprecated\n\n## Findings\n\nSubstantive historical analysis.\n\n"
                "## Sources\n\nUse [current](../current/) for current policy.\n"
            )
        )
        self.assertFalse(
            redirect(
                "# Deprecated\n\nUse [current](../current/). This paragraph also contains "
                "substantive historical analysis, evidence, and conclusions.\n"
            )
        )
        for unsafe_or_substantive in (
            "# Redirect\n\nMoved to ../0002-agentic-engineering-research-pack/. Use it now.\n",
            "# Redirect\n\nMoved to /docs/90.references/research/0002-agentic-engineering-research-pack/.\n",
            "# Redirect\n\nMoved to ../../../../outside/.\n",
            "# Redirect\n\nMoved to %68%74%74%70%73%3A%2F%2Fexample.invalid/.\n",
            "# Redirect\n\nMoved to [current](/docs/90.references/research/0002-agentic-engineering-research-pack/).\n",
            "# Redirect\n\nMoved to [current](../../../../outside/).\n",
            "# Redirect\n\nMoved to [current](%68%74%74%70%73%3A%2F%2Fexample.invalid/).\n",
            "# Redirect\n\nMoved to ../0002-agentic-engineering-research-pack/ and ../0084-github-actions-platform/.\n",
            "# Redirect\n\nMoved to [current](../0002-agentic-engineering-research-pack/) or ../0084-github-actions-platform/.\n",
            "# Redirect\n\nMoved to [first](../0002-agentic-engineering-research-pack/) [second](../0084-github-actions-platform/).\n",
        ):
            with self.subTest(unsafe_or_substantive=unsafe_or_substantive):
                self.assertFalse(redirect(unsafe_or_substantive))

    def test_active_consumer_scan_rejects_retired_runtime_routes(self) -> None:
        context, root = self._fixture()
        with context:
            consumer = root / "scripts/validation/current.py"
            consumer.parent.mkdir(parents=True)
            consumer.write_text(
                'CURRENT = "docs/90.references/data/governance/current.yaml"\n',
                encoding="utf-8",
            )
            findings = self.references.validate_active_reference_consumers(
                root,
                (pathlib.PurePosixPath("scripts/validation/current.py"),),
            )
            self.assertEqual({"retired-active-reference-path"}, {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
