"""Repository-composition and compatibility-facade tests."""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import io
import json
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest
from datetime import date
from unittest import mock

from scripts.lib.document_governance import registry as registry_module
from scripts.lib.document_governance.metadata import reference as reference_module
from scripts.lib.document_governance.metadata.heading import (
    extract_markdown_headings,
)
from scripts.lib.document_governance.metadata.profile import (
    classify_registered_path,
)
from tests.lib.document_governance.metadata._support import (
    ROOT,
    copy_registry_contract_fixture,
    current_profiles,
    git,
    init_git,
    metadata,
    run_checker,
)


class MetadataValidatorCompatibilityTests(unittest.TestCase):
    def test_metadata_cli_reads_frontmatter_schema_once_per_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            paths = (
                pathlib.Path(".agents/governance/bootstrap.md"),
                pathlib.Path("docs/00.workspace/04.quality/quality-standards.md"),
            )
            for relative in paths:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            self.assertEqual(0, git(root, "add", "--", *map(str, paths)).returncode)
            argv = [
                "--root",
                str(root),
                "--registry",
                str(ROOT / "docs/99.templates/registry.json"),
            ]

            with mock.patch.object(
                registry_module, "_parse_json", wraps=registry_module._parse_json
            ) as parse_json:
                for _ in range(2):
                    parse_json.reset_mock()
                    stdout = io.StringIO()
                    with contextlib.redirect_stdout(stdout):
                        self.assertEqual(0, reference_module.main(argv))
                    for relative in paths:
                        self.assertIn(relative.as_posix(), stdout.getvalue())
                    schema_loads = [
                        call
                        for call in parse_json.call_args_list
                        if call.args[0] == registry_module.DEFAULT_FRONTMATTER_SCHEMA
                    ]
                    self.assertEqual(1, len(schema_loads))

    def test_frontmatter_schema_snapshot_is_not_shared_between_invocations(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            schema = pathlib.Path(directory) / "frontmatter.json"
            schema.write_text('{"type": "object"}', encoding="utf-8")
            snapshot = registry_module.FrontmatterValidator(schema)
            self.assertEqual((), snapshot({}))

            schema.write_text('{"required": ["title"]}', encoding="utf-8")
            self.assertEqual((), snapshot({}))
            self.assertEqual(
                ("frontmatter-schema-invalid",),
                tuple(
                    item.code
                    for item in registry_module.validate_frontmatter({}, schema)
                ),
            )

    def test_generated_inventory_has_registered_audit_metadata(self) -> None:
        from scripts.lib.document_governance.common_document import (
            common_metadata,
            load_contract,
            payload_text,
        )
        from scripts.lib.document_governance.registry import validate_frontmatter

        observed_on = date(2030, 6, 7)
        profiles = current_profiles()
        with mock.patch.object(reference_module, "date", create=True) as clock:
            clock.today.return_value = observed_on
            rendered = reference_module.render_report([], profiles, {})
        clock.today.assert_called_once_with()
        values = metadata._parse_frontmatter_text(rendered)
        self.assertEqual((), validate_frontmatter(values))
        self.assertLessEqual(
            set(
                current_profiles()["_registry"].profiles["audit"][
                    "required_frontmatter"
                ]
            ),
            values.keys(),
        )
        self.assertEqual("reference/audit-pack", values["type"])
        self.assertEqual("AUD-0023", values["artifact_id"])
        self.assertEqual("published", values["status"])
        self.assertEqual("2.0.0", values["version"])
        self.assertEqual("2026-07-05", str(values["created"]))
        self.assertEqual(observed_on.isoformat(), str(values["observed_at"]))
        self.assertEqual(observed_on.isoformat(), str(values["updated"]))
        registry = profiles["_registry"]
        audit_path = (
            registry.profiles["audit"]["path_pattern"]
            .replace("{number:4}", "0023")
            .replace("{slug}", "frontmatter-semantic-inventory")
        )
        self.assertNotIn("{", audit_path)
        common = common_metadata(registry, audit_path, values)
        self.assertEqual("reference-pack", common["kind"])
        self.assertEqual("active", common["lifecycle"])
        self.assertEqual(
            {"subject": "hy-home.docker", "layer": "reference"}, dict(common["scope"])
        )
        _, h2 = extract_markdown_headings(rendered)
        self.assertEqual(
            [f"## {title}" for title in load_contract()["headings"]], list(h2)
        )
        _, h2 = extract_markdown_headings(payload_text(rendered))
        headings = {heading.removeprefix("## ") for heading in h2}
        self.assertLessEqual(
            set(current_profiles()["_registry"].profiles["audit"]["required_sections"]),
            headings,
        )

    def test_generated_inventory_passes_current_profile_and_language_consumers(
        self,
    ) -> None:
        from scripts.lib.document_governance.language import language_mismatch

        profiles = current_profiles()
        rendered = reference_module.render_report([], profiles, {})
        path = pathlib.Path(
            "docs/90.references/02.audits/0023-frontmatter-semantic-inventory/README.md"
        )
        record = dataclasses.replace(
            reference_module._record_from_text(path, rendered), artifact_type="audit"
        )
        with self.subTest(consumer="metadata"):
            self.assertEqual([], reference_module.validate_record(record, profiles, {}))
        with self.subTest(consumer="body"):
            self.assertEqual(
                [],
                reference_module.validate_body_contract(
                    record, rendered, profiles, True
                ),
            )
        with self.subTest(consumer="language"):
            self.assertFalse(language_mismatch(rendered, "ko"))

    def test_report_includes_new_managed_governance_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            relative = pathlib.Path(".agents/governance/bootstrap.md")
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / relative).read_bytes())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(ROOT / "docs/99.templates/registry.json"),
                        "--mode",
                        "report",
                    ]
                )
            self.assertEqual(0, result)
            self.assertIn(relative.as_posix(), output.getvalue())
            path.write_text(
                '---\ntitle: Fixture\nversion: invalid-fixture-version\ntype: governance/policy\nstatus: active\nowner: "@fixture"\nupdated: "2026-09-06"\n---\n# Fixture\n'
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(ROOT / "docs/99.templates/registry.json"),
                        "--mode",
                        "check-active",
                    ]
                )
            self.assertEqual(1, result)
            self.assertIn(relative.as_posix(), output.getvalue())

    def test_metadata_validator_declares_its_compatibility_api(self) -> None:
        """The split preserves live imports, not incidental module globals."""

        from scripts.lib.document_governance import metadata_validator

        self.assertTrue(metadata_validator.__all__)
        missing = [
            name
            for name in metadata_validator.__all__
            if not hasattr(metadata_validator, name)
        ]
        self.assertEqual([], missing)


class FixtureGitTests(unittest.TestCase):
    def test_init_git_names_main_from_a_detached_clone(self) -> None:
        # Hosted CI checks out the PR merge ref detached; a clone of it is too.
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            git(root, "init", "-q")
            git(root, "config", "user.name", "Fixture")
            git(root, "config", "user.email", "fixture@example.invalid")
            git(root, "commit", "-q", "--allow-empty", "-m", "seed")
            git(root, "checkout", "-q", "--detach")
            init_git(root)
            self.assertEqual(
                "main", git(root, "branch", "--show-current").stdout.strip()
            )


class RepositoryContractIntegrationTests(unittest.TestCase):
    def common_fixture(self, root: pathlib.Path):
        registry = registry_module.load_registry()
        roles = {
            name: registry.template_roles[name]
            for name in ("sdlc/task", "governance/codex-agent")
        }
        profile_ids = {name for role in roles.values() for name in role["profiles"]}
        binding = registry.common["document_core"]
        common = {
            **registry.common,
            "document_core": {
                **binding,
                "profile_bindings": {
                    name: binding["profile_bindings"][name] for name in profile_ids
                },
                "path_bindings": {},
            },
        }
        for relative in {
            binding["source_path"],
            *(role["source"] for role in roles.values()),
            *(
                role["native_source"]
                for role in roles.values()
                if "native_source" in role
            ),
        }:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        return dataclasses.replace(
            registry,
            profiles={
                name: registry.profiles[name]
                for name in profile_ids | {"template-source"}
            },
            template_roles=roles,
            common=common,
        )

    def common_codes(self, root, registry):
        with mock.patch(
            "scripts.lib.document_governance.template_definition.role_design_contract_findings",
            return_value=[],
        ) as old_binding:
            result = reference_module._role_design_findings(
                root, {"_registry": registry}
            )
        old_binding.assert_called_once_with(registry, root=root)
        return {finding.code for finding in result}

    def test_common_core_checks_actual_pinned_sources_and_preserves_role_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            registry = self.common_fixture(root)
            self.assertEqual(set(), self.common_codes(root, registry))

    def test_common_core_missing_tampered_or_wrong_identity_fails_closed(self):
        for change, expected in (
            ("binding-missing", "document-core-binding-missing"),
            ("source-missing", "document-core-source-unreadable"),
            ("source-tampered", "document-core-source-changed"),
            ("invalid-json", "document-core-source-invalid"),
            ("invalid-payload", "document-core-source-invalid"),
            ("invalid-headings", "document-core-source-invalid"),
            ("missing-marker", "document-core-source-invalid"),
            ("wrong-id", "document-core-identity"),
            ("wrong-version", "document-core-identity"),
        ):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                registry = self.common_fixture(root)
                binding = registry.common["document_core"]
                source = root / binding["source_path"]
                if change == "binding-missing":
                    registry = dataclasses.replace(
                        registry,
                        common={
                            key: value
                            for key, value in registry.common.items()
                            if key != "document_core"
                        },
                    )
                elif change == "source-missing":
                    source.unlink()
                elif change == "source-tampered":
                    source.write_bytes(source.read_bytes() + b" ")
                elif change in {
                    "invalid-json",
                    "invalid-payload",
                    "invalid-headings",
                    "missing-marker",
                }:
                    document = json.loads(source.read_bytes())
                    if change == "invalid-payload":
                        document["payload_profiles"]["task"] = {}
                    elif change == "invalid-headings":
                        document["headings"] = {"invalid": 1}
                    elif change == "missing-marker":
                        document["payload_encoding"] = {}
                    raw = (
                        b"{"
                        if change == "invalid-json"
                        else json.dumps(document).encode()
                    )
                    source.write_bytes(raw)
                    registry = dataclasses.replace(
                        registry,
                        common={
                            **registry.common,
                            "document_core": {
                                **binding,
                                "source_sha256": hashlib.sha256(raw).hexdigest(),
                            },
                        },
                    )
                else:
                    field = (
                        "contract_id" if change == "wrong-id" else "contract_version"
                    )
                    registry = dataclasses.replace(
                        registry,
                        common={
                            **registry.common,
                            "document_core": {**binding, field: "other"},
                        },
                    )
                self.assertIn(expected, self.common_codes(root, registry))

    def test_common_core_requires_exact_profile_coverage_and_known_payload_kinds(self):
        for change in ("missing", "extra", "unknown-kind", "wrong-role"):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                registry = self.common_fixture(root)
                binding = registry.common["document_core"]
                profiles = dict(binding["profile_bindings"])
                if change == "missing":
                    del profiles["task"]
                elif change == "extra":
                    profiles["undeclared"] = profiles["task"]
                elif change == "unknown-kind":
                    profiles["task"] = {**profiles["task"], "kind": "unknown-kind"}
                else:
                    registry = dataclasses.replace(
                        registry,
                        profiles={
                            **registry.profiles,
                            "task": {
                                **registry.profiles["task"],
                                "template_id": "governance/codex-agent",
                            },
                        },
                    )
                registry = dataclasses.replace(
                    registry,
                    common={
                        **registry.common,
                        "document_core": {**binding, "profile_bindings": profiles},
                    },
                )
                self.assertIn(
                    "document-core-profile-binding", self.common_codes(root, registry)
                )

    def test_common_core_definition_sources_must_be_wrapped_and_bound_to_the_role(self):
        for change, expected in (
            ("unwrapped", "document-core-definition-envelope"),
            ("wrong-template", "document-core-definition-binding"),
        ):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                registry = self.common_fixture(root)
                name = (
                    "sdlc/task" if change == "unwrapped" else "governance/codex-agent"
                )
                source = root / registry.template_roles[name]["source"]
                if change == "unwrapped":
                    source.write_text("# Unwrapped\n\n## Scope\n\nExisting content.\n")
                else:
                    text = source.read_text()
                    self.assertIn("template_id: governance/codex-agent", text)
                    source.write_text(
                        text.replace(
                            "template_id: governance/codex-agent",
                            "template_id: sdlc/spec",
                        )
                    )
                self.assertIn(expected, self.common_codes(root, registry))

    def test_common_core_native_payload_is_separate_existing_and_owned(self):
        for change in ("missing", "alias", "unknown", "no-binding"):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                registry = self.common_fixture(root)
                name = "governance/codex-agent"
                role = registry.template_roles[name]
                if change == "missing":
                    (root / role["native_source"]).unlink()
                elif change == "alias":
                    role = {**role, "native_source": role["source"]}
                elif change == "unknown":
                    (root / "unowned.toml").write_text("name='unowned'\n")
                    role = {**role, "native_source": "unowned.toml"}
                else:
                    role = {
                        key: value
                        for key, value in role.items()
                        if key != "native_source"
                    }
                registry = dataclasses.replace(
                    registry, template_roles={**registry.template_roles, name: role}
                )
                self.assertIn(
                    "document-core-native-binding", self.common_codes(root, registry)
                )

    def test_common_core_sources_reject_symlinks_and_oversize_inputs(self):
        for subject in ("contract", "definition", "native"):
            for change in ("symlink", "parent-symlink", "oversize"):
                with (
                    self.subTest(subject=subject, change=change),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = pathlib.Path(directory)
                    registry = self.common_fixture(root)
                    role = registry.template_roles["governance/codex-agent"]
                    relative = (
                        registry.common["document_core"]["source_path"]
                        if subject == "contract"
                        else role[
                            "source" if subject == "definition" else "native_source"
                        ]
                    )
                    source = root / relative
                    if change == "symlink":
                        replacement = root / "replacement"
                        replacement.write_bytes(source.read_bytes())
                        source.unlink()
                        source.symlink_to(replacement)
                    elif change == "parent-symlink":
                        replacement = root / "relocated"
                        source.parent.rename(replacement)
                        source.parent.symlink_to(replacement, target_is_directory=True)
                    else:
                        source.write_bytes(b"x" * (256 * 1024 + 1))
                    expected = {
                        "contract": "document-core-source-unreadable",
                        "definition": "document-core-definition-unreadable",
                        "native": "document-core-native-binding",
                    }[subject]
                    self.assertIn(expected, self.common_codes(root, registry))

    def test_generation_byte_snapshot_keeps_exact_and_bounded_worktree_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = pathlib.Path("docs/task.md")
            (root / path).parent.mkdir()
            (root / path).write_bytes(b"# Fixture\r\n")
            with mock.patch.object(reference_module, "_bounded_git") as git_read:
                for source, expected in (
                    (b"# Fixture\r\n", True),
                    (b"# Fixture\n", False),
                ):
                    self.assertEqual(
                        expected,
                        reference_module._source_blob_matches_worktree(
                            root, path, "a" * 40, source_blob=source
                        ),
                    )
                (root / path).unlink()
                (root / "target.md").write_bytes(b"# Fixture\r\n")
                (root / path).symlink_to("../target.md")
                self.assertFalse(
                    reference_module._source_blob_matches_worktree(
                        root, path, "a" * 40, source_blob=b"# Fixture\r\n"
                    )
                )
            git_read.assert_not_called()

    def test_generation_normalization_accepts_only_registered_named_edges(self) -> None:
        registered = frozenset(
            {
                ("navigation", "draft", "active"),
                ("publication", "review", "in-review"),
            }
        )
        self.assertTrue(
            reference_module._registered_generation_normalization(
                {"lifecycle_id": "navigation", "identity_relation": "none"},
                "draft",
                "active",
                registered,
            )
        )
        self.assertFalse(
            reference_module._registered_generation_normalization(
                {"lifecycle_id": "adr", "identity_relation": "direct"},
                "accepted",
                "rejected",
                registered,
            )
        )

    def fixture(self, directory: str) -> tuple[pathlib.Path, pathlib.Path]:
        root = pathlib.Path(directory)
        return root, copy_registry_contract_fixture(root)

    def run_contracts(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        return run_checker(root, "check-contracts", profiles=profiles)

    def test_changed_mode_retains_repository_contract_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, registry = self.fixture(directory)
            finding = reference_module.Finding(
                "docs/03.specs/README.md", "index-member-unlisted", "fixture"
            )
            transitions = frozenset(
                {
                    (
                        "docs/03.specs/0001-fixture/01.tasks/tsk-0001-work.md",
                        "draft",
                        "in-progress",
                    )
                }
            )
            normalizations = frozenset(
                {
                    (
                        "docs/03.specs/0001-fixture/spec.md",
                        "active",
                        "in-progress",
                    )
                }
            )
            output = io.StringIO()
            with (
                mock.patch.object(
                    reference_module,
                    "_validate_repository_contracts",
                    return_value=(
                        [finding],
                        transitions,
                        normalizations,
                        reference_module._GenerationBindings(),
                    ),
                ) as contracts,
                mock.patch.object(
                    reference_module, "collect_records_at_ref", return_value=[]
                ) as base_records,
                mock.patch.object(
                    reference_module,
                    "validate_record",
                    return_value=[],
                ) as validate_record,
                contextlib.redirect_stdout(output),
            ):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(registry),
                        "--mode",
                        "check-changed",
                        "--base-ref",
                        "HEAD",
                    ]
                )
            contracts.assert_called_once()
            base_records.assert_called_once()
            self.assertEqual({}, contracts.call_args.kwargs["previous_records"])
            # Native contracts own record validation; main reuses those findings.
            validate_record.assert_not_called()
            self.assertEqual(1, result)
            self.assertIn("index-member-unlisted", output.getvalue())

    def test_changed_mode_reports_version_change_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, registry = self.fixture(directory)
            finding = reference_module.Finding(
                "docs/90.references/01.research/README.md",
                "version-unchanged",
                "fixture",
            )
            output = io.StringIO()
            with (
                mock.patch.object(
                    reference_module,
                    "_validate_repository_contracts",
                    return_value=(
                        [],
                        frozenset(),
                        frozenset(),
                        reference_module._GenerationBindings(),
                    ),
                ),
                mock.patch.object(
                    reference_module, "collect_records_at_ref", return_value=[]
                ),
                mock.patch.object(reference_module, "validate_record", return_value=[]),
                mock.patch.object(
                    reference_module,
                    "version_change_findings",
                    return_value=[finding],
                ) as changes,
                contextlib.redirect_stdout(output),
            ):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(registry),
                        "--mode",
                        "check-changed",
                        "--base-ref",
                        "HEAD",
                    ]
                )
            changes.assert_called_once()
            self.assertEqual(1, result)
            self.assertIn("version-unchanged", output.getvalue())
            self.assertFalse(hasattr(reference_module, "version_downgrade_findings"))

    def test_changed_mode_reports_product_version_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, registry = self.fixture(directory)
            finding = reference_module.Finding(
                "projects/storybook/nextjs/package.json",
                "version-downgrade",
                "fixture",
            )
            output = io.StringIO()
            with (
                mock.patch.object(
                    reference_module,
                    "_validate_repository_contracts",
                    return_value=(
                        [],
                        frozenset(),
                        frozenset(),
                        reference_module._GenerationBindings(),
                    ),
                ),
                mock.patch.object(
                    reference_module, "collect_records_at_ref", return_value=[]
                ),
                mock.patch.object(reference_module, "validate_record", return_value=[]),
                mock.patch.object(
                    reference_module,
                    "product_version_findings",
                    return_value=[finding],
                ) as changes,
                contextlib.redirect_stdout(output),
            ):
                result = reference_module.main(
                    [
                        "--root",
                        str(root),
                        "--registry",
                        str(registry),
                        "--mode",
                        "check-changed",
                        "--base-ref",
                        "HEAD",
                    ]
                )
            changes.assert_called_once()
            self.assertEqual(1, result)
            self.assertIn("version-downgrade", output.getvalue())

    def test_contracts_share_exact_baseline_and_historical_input_context(self) -> None:
        profiles = current_profiles()
        previous = {
            "docs/03.specs/0001-fixture/spec.md": reference_module.Record(
                pathlib.Path("docs/03.specs/0001-fixture/spec.md"),
                {"status": "draft"},
                "spec",
            )
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            # No Stage 98 migration ledger exists here: Spec Package validation
            # must run from the current tree alone (SPEC-0248).
            (root / "docs/03.specs").mkdir(parents=True)
            lifecycle = mock.Mock(
                findings=(),
                actual_transitions=frozenset(),
                actual_normalizations=frozenset(),
                generation_source=None,
            )
            with (
                mock.patch.object(
                    reference_module, "_tracked_repository_markdown", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_reference_delegation_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_index_membership_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_allocation_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_role_design_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_changed_paths", return_value=set()
                ),
                mock.patch.object(
                    reference_module,
                    "collect_records_at_ref",
                    side_effect=AssertionError("baseline was already parsed"),
                ),
                mock.patch.object(
                    reference_module, "collect_records", return_value=[]
                ) as current,
                mock.patch.object(
                    reference_module, "load_spec_packages", return_value=()
                ) as packages,
                mock.patch.object(
                    reference_module,
                    "validate_repository_spec_package_lifecycle_details",
                    return_value=lifecycle,
                ) as validate,
            ):
                findings, _, _, _ = reference_module._validate_repository_contracts(
                    root,
                    profiles,
                    base_ref="a" * 40,
                    transition_ref="a" * 40,
                    previous_records=previous,
                )
            self.assertEqual([], findings)
            self.assertTrue(packages.called)
            self.assertTrue(validate.called)
            self.assertIs(previous, current.call_args.kwargs["previous_records"])
            self.assertIs(
                packages.call_args.kwargs["_historical_context"],
                validate.call_args.kwargs["_historical_context"],
            )

    def test_terminal_task_body_baseline_requires_exact_generation_blob(self) -> None:
        profiles = current_profiles()
        relative = pathlib.Path(
            "docs/03.specs/0001-example/01.tasks/tsk-0001-example.md"
        )
        missing_relative = pathlib.Path(
            "docs/03.specs/0001-example/01.tasks/tsk-0002-missing-at-source.md"
        )
        text = (
            "---\nartifact_id: SPEC-0001-TSK-0001\ntype: sdlc/task\n"
            "status: completed\n---\n# Historical Task\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text(text, encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "source",
                ],
                cwd=root,
                check=True,
            )
            revision = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            record = metadata._record_from_text(relative, text, profiles=profiles)
            bindings = reference_module._GenerationBindings(
                revision,
                {relative.as_posix(): "completed"},
                frozenset({relative.as_posix()}),
            )

            exact_record, exact_text = reference_module._generation_task_body_baseline(
                root, record, text, profiles, bindings
            )

            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
            normalized_crlf_text = path.read_text(encoding="utf-8")
            self.assertEqual(text, normalized_crlf_text)
            crlf_only = reference_module._generation_task_body_baseline(
                root, record, normalized_crlf_text, profiles, bindings
            )

            changed_text = text + "changed\n"
            path.write_bytes(changed_text.encode("utf-8"))
            changed = reference_module._generation_task_body_baseline(
                root, record, path.read_text(encoding="utf-8"), profiles, bindings
            )

            symlink_target = path.with_name("same-content.md")
            symlink_target.write_text(text, encoding="utf-8")
            path.unlink()
            path.symlink_to(symlink_target.name)
            nonregular = reference_module._generation_task_body_baseline(
                root, record, text, profiles, bindings
            )

            path.unlink()
            path.write_text(text, encoding="utf-8")
            with mock.patch.object(
                reference_module,
                "MAX_SPEC_FILE_BYTES",
                len(text.encode("utf-8")) - 1,
                create=True,
            ):
                oversized = reference_module._generation_task_body_baseline(
                    root, record, text, profiles, bindings
                )

            missing_path = root / missing_relative
            missing_path.write_text(text, encoding="utf-8")
            missing_record = metadata._record_from_text(
                missing_relative, text, profiles=profiles
            )
            missing_bindings = reference_module._GenerationBindings(
                revision,
                {missing_relative.as_posix(): "completed"},
                frozenset({missing_relative.as_posix()}),
            )
            missing_source = reference_module._generation_task_body_baseline(
                root, missing_record, text, profiles, missing_bindings
            )

        self.assertIsNotNone(exact_record)
        self.assertEqual(text, exact_text)
        self.assertEqual((None, None), crlf_only)
        self.assertEqual((None, None), changed)
        self.assertEqual((None, None), nonregular)
        self.assertEqual((None, None), oversized)
        self.assertEqual((None, None), missing_source)

    def test_repository_contracts_reject_fragmented_in_progress_task_evidence(
        self,
    ) -> None:
        from scripts.lib.document_governance.registry import load_registry
        from scripts.lib.document_governance.spec_packages import load_spec_packages

        current_registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text()
        )
        fixture_number = current_registry["identity_spaces"]["spec"]["next_number"]
        fixture_id = f"SPEC-{fixture_number:04d}"

        def materialize_in_progress_package(
            root: pathlib.Path,
            package_relative: pathlib.Path,
            index_anchor: str,
            index_row: str,
        ) -> None:
            package = root / package_relative
            tasks = package / "01.tasks"
            tasks.mkdir(parents=True, exist_ok=True)
            package.joinpath("spec.md").write_text(
                """---
title: "Fixture Evidence Integrity Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-06"
---

# Fixture Evidence Integrity Specification

## Overview

### Intent

Exercise the current Evidence contract.

### Owning Requirements

The fixture parents are REQ-0024 and REQ-0026.

## Scope

### In Scope

The fixture is local to this regression.

### Non-goals

No other contract is exercised.

## Behavior Contract

### Normal Behavior

The Task Evidence table remains contiguous.

### Failure and Edge Cases

A detached Evidence row is rejected.

## Acceptance Criteria

### Criteria

1. Reject a detached Evidence row.

### Evidence Requirements

- The Task records the rejection as an Evidence row.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](01.tasks/tsk-0001-task-evidence-table-integrity.md)

### Historical and Navigation

No historical or navigation link applies.
""",
                encoding="utf-8",
            )
            package.joinpath("plan.md").write_text(
                """---
title: "Fixture Evidence Integrity Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210-PLAN-0001"
parent_ids:
- "SPEC-0210"
created: "2026-10-06"
---

# Fixture Evidence Integrity Plan

## Overview

Exercise one controlled in-progress Task.

## Work Breakdown

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| W1 | Validate detached Evidence. | None | TSK-0001 | docs/03.specs | 1 | Metadata contracts. |

## Verification Plan

Run the canonical metadata checker before and after the mutation.

## Risks and Rollback

The temporary repository is discarded after the test.

## Related Documents

- [Specification](spec.md)
- [Task](01.tasks/tsk-0001-task-evidence-table-integrity.md)
""",
                encoding="utf-8",
            )
            tasks.joinpath("tsk-0001-task-evidence-table-integrity.md").write_text(
                """---
title: "Fixture Evidence Integrity Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210-TSK-0001"
parent_ids:
- "SPEC-0210-PLAN-0001"
created: "2026-10-06"
---

# Fixture Evidence Integrity Task

## Scope

### Objective and Parent

Exercise the public metadata path with an explicit in-progress Task.

- [Specification](../spec.md)
- [Plan](../plan.md)

### Inputs and Authority

#### Fixture Authorization

This synthetic fixture grants no operation or approval.

## Execution Log

### Work Performed

#### Fixture Start

The controlled fixture is in progress.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0210 | draft | approved | #fixture-authorization |
| SPEC-0210-PLAN-0001 | draft | approved | #fixture-authorization |
| SPEC-0210-TSK-0001 | draft | ready | #fixture-authorization |
| SPEC-0210-TSK-0001 | ready | in-progress | #fixture-start |

### Blockers and Decisions

No blocker or decision is recorded.

## Verification Evidence

### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 1 | W1 | observation | synthetic | - | Fixture control | - | NOT_RUN | This Task | true | - |

### Resolution Links

No resolution is recorded.

## Acceptance Decision

### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | undecided | pending | - | - | - | [Spec](../spec.md) | - |

### Remaining Conditions

The fixture is intentionally in progress.

## Handoff

### Promotion Receipt

No promotion is recorded.

### Next Owner

This synthetic fixture names no next owner.
""",
                encoding="utf-8",
            )
            for member in (
                package / "spec.md",
                package / "plan.md",
                tasks / "tsk-0001-task-evidence-table-integrity.md",
            ):
                member.write_text(member.read_text().replace("SPEC-0210", fixture_id))
            index = root / "docs/03.specs/README.md"
            index_text = index.read_text(encoding="utf-8")
            row_count = index_text.count(index_row)
            if row_count == 0:
                self.assertEqual(1, index_text.count(index_anchor))
                index.write_text(
                    index_text.replace(
                        index_anchor,
                        f"{index_anchor}\n{index_row}",
                        1,
                    ),
                    encoding="utf-8",
                )
            else:
                self.assertEqual(1, row_count)
            self.assertEqual(1, index.read_text(encoding="utf-8").count(index_row))

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory) / "repository"
            cloned = subprocess.run(
                ("git", "clone", "--quiet", "--shared", str(ROOT), str(root)),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, cloned.returncode, cloned.stdout + cloned.stderr)
            copy_registry_contract_fixture(root)
            package_relative = pathlib.Path(
                f"docs/03.specs/{fixture_number:04d}-fixture-evidence-integrity"
            )
            index_anchor = (
                "| SPEC-0204 | [서비스 연동·보안·운영]"
                "(./0204-service-integration-security-and-operations/) | 공통 서비스 "
                "호환성·외부 연결·백업 경계의 승인용 계약 |"
            )
            index_row = (
                f"| {fixture_id} | [{fixture_number:04d}-fixture-evidence-integrity/]"
                f"(./{fixture_number:04d}-fixture-evidence-integrity/) | 현재 Plan과 "
                "Task 증거 표의 분절 누락 방지 |"
            )
            materialize_in_progress_package(
                root,
                package_relative,
                index_anchor,
                index_row,
            )
            materialize_in_progress_package(
                root,
                package_relative,
                index_anchor,
                index_row,
            )
            fixture_registry = json.loads(
                (root / "docs/99.templates/registry.json").read_text()
            )
            fixture_registry["identity_spaces"]["spec"].update(
                high_water=fixture_number, next_number=fixture_number + 1
            )
            (root / "docs/99.templates/registry.json").write_text(
                json.dumps(fixture_registry, ensure_ascii=False, indent=2) + "\n"
            )
            shutil.copy2(
                ROOT / "scripts/lib/document_governance/spec_packages.py",
                root / "scripts/lib/document_governance/spec_packages.py",
            )
            corrected_task = pathlib.Path(
                "docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/"
                "tsk-0040-workspace-inventory.md"
            )
            shutil.copy2(ROOT / corrected_task, root / corrected_task)
            staged = subprocess.run(
                ("git", "-C", str(root), "add", "--all"),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, staged.returncode, staged.stdout + staged.stderr)
            committed = subprocess.run(
                (
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=P03 Fixture",
                    "-c",
                    "user.email=p03@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "p03 metadata fixture",
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                0, committed.returncode, committed.stdout + committed.stderr
            )
            registry_path = root / "docs/99.templates/registry.json"
            packages = load_spec_packages(
                root / "docs/03.specs",
                registry=load_registry(registry_path),
            )
            fixture_package = next(
                package
                for package in packages
                if package.spec.artifact_id == fixture_id
            )
            self.assertEqual("approved", fixture_package.spec.status)
            self.assertEqual("approved", fixture_package.plan.status)
            self.assertEqual(1, len(fixture_package.tasks))
            self.assertEqual("in-progress", fixture_package.tasks[0].status)
            # The load above is the control: the package parses before the
            # fragment is added, and the asserted message attributes the
            # failure, so a second real-tree contract run adds no proof.

            task = (
                root
                / package_relative
                / ("01.tasks/tsk-0001-task-evidence-table-integrity.md")
            )
            marker = "\n### Resolution Links\n"
            source = task.read_text(encoding="utf-8")
            self.assertEqual(1, source.count(marker))
            task.write_text(
                source.replace(
                    marker,
                    "\nDetached evidence fragment.\n\n"
                    "| Hidden failure | 1 | W1 | automated | fixture | - | "
                    "Source check | 1 | FAIL | detached | true | - |\n" + marker,
                    1,
                ),
                encoding="utf-8",
            )

            result = self.run_contracts(
                root,
                registry_path,
            )
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn("spec-package-invalid", rendered)
            self.assertIn("registered evidence table must be contiguous", rendered)

    def test_repository_contracts_enforce_machine_source_safety(self) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            path = root / relative_path
            path.write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "servers:\n"
                "  - url: https://api.example.com\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )

    def test_registry_contracts_parse_profile_and_section_contracts(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            wrap_document,
        )

        relative_path = "docs/99.templates/02.templates/01.requirements/requirement-package.template.md"
        cases = (
            ("profile", "template-artifact-type-mismatch"),
            ("heading", "template-section-missing"),
        )
        for label, expected in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / relative_path
                original = path.read_text(encoding="utf-8")
                if label == "profile":
                    self.assertEqual(
                        "sdlc/requirement",
                        reference_module._parse_frontmatter_text(original)["type"],
                    )
                    changed, count = re.subn(
                        r"(?m)^type:[^\n]+$", "type: sdlc/spec", original, count=1
                    )
                    self.assertEqual(1, count)
                    self.assertEqual(
                        "sdlc/spec",
                        reference_module._parse_frontmatter_text(changed)["type"],
                    )
                else:
                    payload = compact_payload(original)
                    marker = "\n## Traceability\n"
                    self.assertEqual(1, payload.count(marker))
                    changed = wrap_document(
                        payload.replace(marker, "\n## Verification Contract\n", 1),
                        kind="requirement",
                    )
                self.assertNotEqual(original, changed)
                path.write_text(changed, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"{expected}: {relative_path}", result.stdout)

    def test_repository_contracts_fail_closed_on_openapi_parse_boundaries_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        cases = (
            (
                "malformed",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npaths: [fixture-parse-leak\n",
                "fixture-parse-leak",
            ),
            (
                "duplicate-key",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\ninfo: fixture-first\ninfo: fixture-duplicate-leak\n",
                "fixture-duplicate-leak",
            ),
            (
                "constructor",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-value: !!python/object:fixture-constructor-leak {}\n",
                "fixture-constructor-leak",
            ),
            (
                "non-mapping-root",
                "- __API_TITLE__\n- fixture-root-leak\n",
                "fixture-root-leak",
            ),
        )
        for label, text, private_value in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-parse-error: {relative_path}: "
                    "machine template could not be parsed as a safe OpenAPI mapping",
                    result.stdout,
                )
                self.assertNotIn(private_value, rendered)
                self.assertNotRegex(rendered, r"(?i)(line|column) [0-9]+")

    def test_repository_contracts_bound_openapi_credential_value_keywords(self) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with (
                self.subTest(keyword=keyword),
                tempfile.TemporaryDirectory() as directory,
            ):
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          {keyword}: {value}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)
        with (
            self.subTest(keyword="direct-list"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "access_token: [__ACCESS_TOKEN__, fixture-direct-list-leak]\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )
            self.assertNotIn("fixture-direct-list-leak", rendered)

    def test_repository_contracts_reject_openapi_credential_plural_examples_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        cases = {
            "scalar": "fixture-scalar-cli-private",
            "list": "[__PASSWORD_PRIMARY__, fixture-list-cli-private]",
            "map": "{primary: __PASSWORD_PRIMARY__, secondary: fixture-map-cli-private}",
        }
        for label, examples in cases.items():
            with self.subTest(shape=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          examples: {examples}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)

    def test_repository_contracts_accept_exact_nested_openapi_credential_examples_tokens(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          examples:\n"
                "            primary: __PASSWORD_PRIMARY__\n"
                "            alternatives:\n"
                "              - __PASSWORD_SECONDARY__\n"
                "              - __PASSWORD_TERTIARY__\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_repository_contracts_accept_safe_openapi_credential_shapes(self) -> None:
        relative_path = (
            "docs/99.templates/02.templates/03.specs/02.contracts/openapi.template.yaml"
        )
        cases = (
            (
                "exact-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "x-api-key: __API_KEY__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          default: __PASSWORD_DEFAULT__\n"
                "          example: __PASSWORD_EXAMPLE__\n"
                "          const: __PASSWORD_CONST__\n"
                "          enum: [__PASSWORD_PRIMARY__, __PASSWORD_SECONDARY__]\n",
            ),
            (
                "schema-only-unrelated-default",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      required: [password]\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          format: password\n"
                "          description: caller-supplied credential\n"
                "        displayName:\n"
                "          type: string\n"
                "          default: fixture display name\n",
            ),
            (
                "standard-example-token",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          example: __PASSWORD_EXAMPLE__\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_workspace_cannot_become_a_docs_inventory_prefix(self) -> None:
        from scripts.lib.document_governance.metadata import reference

        # The rule reads only module constants, so it is checked directly
        # rather than through a real-tree contract run.
        self.assertEqual([], reference._workspace_inventory_findings())
        original = reference.TARGET_MARKDOWN_PREFIXES
        try:
            reference.TARGET_MARKDOWN_PREFIXES = (*original, "_workspace/")
            findings = reference._workspace_inventory_findings()
        finally:
            reference.TARGET_MARKDOWN_PREFIXES = original
        self.assertIn(
            "workspace-inventory-coupling",
            {finding.code for finding in findings},
        )


class IndexMembershipTests(unittest.TestCase):
    """The index rule must fire, and must not fire on a listed package."""

    def _findings(self, index_body: str) -> list[object]:
        registry = metadata.load_registry()
        member = "docs/90.references/01.research/0002-agentic-engineering-research-pack/README.md"
        self.assertEqual(
            "research",
            classify_registered_path(member, registry),
            "fixture path must classify as the indexed member profile",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            index = root / "docs/90.references/01.research/README.md"
            index.parent.mkdir(parents=True)
            index.write_text(index_body, encoding="utf-8")
            record = metadata.Record(pathlib.Path(member), {}, "research")
            findings = reference_module._index_membership_findings(
                root, registry, [record]
            )
        # The fixture root holds only the research index and one research
        # record, so the other registered indexes govern nothing and are
        # skipped. Scoping keeps this test about the research rule alone.
        return [
            finding
            for finding in findings
            if finding.path == "docs/90.references/01.research/README.md"
            and finding.code != "index-unreadable"
        ]

    def test_unlisted_package_is_reported(self) -> None:
        findings = self._findings("# Research Packages\n")
        self.assertEqual(
            ["index-member-unlisted"], [finding.code for finding in findings]
        )

    def test_listed_package_is_accepted(self) -> None:
        findings = self._findings(
            "# Research Packages\n\n"
            "| [RES-0002](./0002-agentic-engineering-research-pack/README.md) | x |\n"
        )
        self.assertEqual([], findings)

    def test_package_directory_link_is_membership(self) -> None:
        """SPEC-0184 rule 6: an index links a package, not its member file."""

        for target in (
            "./0002-agentic-engineering-research-pack/",
            "0002-agentic-engineering-research-pack",
        ):
            with self.subTest(target=target):
                findings = self._findings(
                    f"# Research Packages\n\n[RES-0002]({target})\n"
                )
                self.assertEqual([], findings)

    def test_registered_indexes_govern_live_packages(self) -> None:
        """A rule that enumerates nothing passes without checking anything.

        An index may be empty once its last package is retired, so non-vacuity
        is asserted across the indexes, not per index. Stage 98 is not counted.
        """

        registry = metadata.load_registry()
        self.assertTrue(registry.indexes)
        governed_total = 0
        for index_path, member_profile in registry.indexes.items():
            with self.subTest(index=index_path):
                self.assertTrue((ROOT / index_path).is_file())
                governed_total += sum(
                    1
                    for path in (ROOT / index_path).parent.rglob("*.md")
                    if classify_registered_path(
                        path.relative_to(ROOT).as_posix(), registry
                    )
                    == member_profile
                )
        self.assertGreater(governed_total, 0)


class ReadmeSectionProfileTests(unittest.TestCase):
    """Sections come from the document's own profile, not from `readme`."""

    def _readme_findings(self, text: str):
        path = pathlib.Path("scripts/README.md")
        profiles = current_profiles()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            (root / path).parent.mkdir(parents=True)
            (root / path).write_text(text)
            with (
                mock.patch.object(
                    reference_module,
                    "_tracked_repository_markdown",
                    return_value=[path],
                ),
                mock.patch.object(reference_module, "collect_records", return_value=[]),
                mock.patch.object(
                    reference_module, "_allocation_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_role_design_findings", return_value=[]
                ),
                mock.patch.object(
                    reference_module, "_reference_delegation_findings", return_value=[]
                ),
            ):
                findings, *_ = reference_module._validate_repository_contracts(
                    root, profiles, validation_paths={path.as_posix()}
                )
        return [finding for finding in findings if finding.path == path.as_posix()]

    def _readme_body(self):
        registry = metadata.load_registry()
        profile = classify_registered_path("scripts/README.md", registry)
        sections = registry.profiles[profile]["required_sections"]
        return "# Fixture\n\n" + "\n\n".join(
            f"## {section}\n\nFilled." for section in sections
        ), sections

    def test_repository_readme_check_reads_legacy_and_common_role_sections(self):
        from scripts.lib.document_governance.common_document import wrap_document

        body, _ = self._readme_body()
        for text in (body, wrap_document(body, kind="readme")):
            with self.subTest(enveloped=text != body):
                self.assertEqual([], self._readme_findings(text))

    def test_repository_readme_check_still_rejects_a_missing_payload_heading(self):
        from scripts.lib.document_governance.common_document import wrap_document

        body, sections = self._readme_body()
        text = wrap_document(body, kind="readme").replace(
            f"#### {sections[0]}\n", "", 1
        )
        findings = self._readme_findings(text)
        self.assertEqual(
            ["readme-heading-missing"], [finding.code for finding in findings]
        )
        self.assertIn(f"## {sections[0]}", findings[0].message)

    def test_repository_readme_check_fails_closed_for_a_malformed_common_envelope(self):
        from scripts.lib.document_governance.common_document import (
            load_contract,
            wrap_document,
        )

        body, _ = self._readme_body()
        title = next(iter(load_contract()["headings"]))
        text = wrap_document(body, kind="readme").replace(f"## {title}\n", "", 1)
        self.assertEqual(
            ["readme-envelope-invalid"],
            [finding.code for finding in self._readme_findings(text)],
        )

    def test_profiles_beyond_readme_declare_sections(self) -> None:
        """The rule is only worth enforcing if other profiles use it."""

        registry = metadata.load_registry()
        with_sections = {
            profile_id
            for profile_id, profile in registry.profiles.items()
            if profile.get("required_sections")
        }
        self.assertIn("readme", with_sections)
        self.assertTrue(with_sections - {"readme"})


class GloballyForbiddenKeyTests(unittest.TestCase):
    """A retired key is reported as retired, not as an unknown typo."""

    def _codes(self, key: str) -> list[str]:
        registry = metadata.load_registry()
        profiles = metadata.build_registry_profiles(registry)
        record = metadata.Record(
            pathlib.Path(".agents/governance/providers/README.md"),
            {
                "title": "Providers",
                "version": "1.0.0",
                "type": "governance/provider-index",
                "status": "active",
                "owner": "@buenhyden",
                key: "x",
            },
            "governance-provider-index",
        )
        manifest = metadata.build_manifest([record])
        return [
            finding.code
            for finding in metadata.validate_record(record, profiles, manifest)
            if finding.code in {"forbidden-key", "type-inappropriate-key"}
        ]

    def test_every_globally_forbidden_key_is_reported_as_forbidden(self) -> None:
        registry = metadata.load_registry()
        forbidden = registry.common.get("globally_forbidden", ())
        self.assertTrue(forbidden, "the contract declares nothing to enforce")
        for key in forbidden:
            with self.subTest(key=key):
                self.assertIn("forbidden-key", self._codes(key))

    def test_an_undeclared_key_keeps_the_other_code(self) -> None:
        self.assertEqual(["type-inappropriate-key"], self._codes("bogus_key"))


class TemplateRoutingTests(unittest.TestCase):
    """SPEC-0184 rule 7: `template_roles` alone maps a type to its template."""

    def test_templates_readme_routes_only_to_category_directories(self) -> None:
        from scripts.lib.document_governance.links import (
            build_document_graph,
            check_navigation,
        )

        readme = ROOT / "docs/99.templates/02.templates/README.md"
        findings = check_navigation(build_document_graph([readme], repo_root=ROOT))
        self.assertEqual([], findings)
