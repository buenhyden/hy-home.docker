from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from scripts.lib.document_governance.registry import (
    DEFAULT_REGISTRY,
    RegistryError,
    _path_patterns_overlap,
    classify_path,
    load_registry,
    validate_frontmatter,
    validate_registry,
)
from scripts.lib.document_governance.metadata_validator import (
    LEGACY_TRANSITION_PROFILES,
    Record,
    _parse_frontmatter_text,
    build_registry_transition_profiles,
    build_manifest,
    infer_artifact_type,
    load_profiles,
    validate_body_contract,
    validate_record,
)
from scripts.lib.document_governance.frontmatter import read_frontmatter_values
from scripts.lib.document_governance.taxonomy import validate_stable_identity


ROOT = pathlib.Path(__file__).resolve().parents[2]


class DocumentRegistryTests(unittest.TestCase):
    def test_default_authority_is_registry_json(self) -> None:
        registry = load_registry()

        self.assertEqual(
            registry.source.as_posix(), "docs/99.templates/registry.json"
        )
        self.assertEqual(DEFAULT_REGISTRY, ROOT / registry.source)
        self.assertNotIn("release", registry.profiles)
        self.assertGreater(registry.identity_spaces["requirement"].next_number, 0)

    def test_registry_is_deeply_immutable(self) -> None:
        registry = load_registry()

        with self.assertRaises(TypeError):
            registry.profiles["spec"] = {}  # type: ignore[index]
        with self.assertRaises(TypeError):
            registry.profiles["spec"]["statuses"] = ()  # type: ignore[index]

    def test_prefixless_profiles_and_full_requirement_ids(self) -> None:
        registry = load_registry()

        self.assertEqual(
            classify_path(
                pathlib.PurePosixPath("docs/03.specs/0153-example/spec.md"),
                registry,
            ),
            "spec",
        )
        requirement = registry.identity_spaces["requirement"]
        self.assertEqual("REQ-", requirement.prefix)
        self.assertTrue(
            {"REQ-0001.FR", "REQ-0001.NFR", "REQ-0001.IF"}
            <= set(requirement.child_spaces)
        )

    def test_spec_0153_package_uses_registered_paths_and_identities(self) -> None:
        registry = load_registry()
        package = pathlib.Path(
            "docs/03.specs/0153-workspace-governance-simplification"
        )
        expected_profiles = {
            ".github/INDEX.md": "github-navigation-index",
            package / "README.md": "spec-package-readme",
            package / "spec.md": "spec",
            package / "plan.md": "plan",
            **{
                package / "tasks" / f"tsk-{number:04d}-example.md": "task"
                for number in range(1, 14)
            },
        }

        for path, profile_id in expected_profiles.items():
            with self.subTest(path=path):
                self.assertEqual(profile_id, classify_path(path, registry))

        self.assertTrue((ROOT / package / "spec.md").is_file())
        self.assertTrue((ROOT / package / "plan.md").is_file())
        spec_values = read_frontmatter_values(ROOT / package / "spec.md")
        plan_values = read_frontmatter_values(ROOT / package / "plan.md")
        self.assertEqual("SPEC-0153", spec_values["artifact_id"])
        self.assertEqual("plan-0153", plan_values["artifact_id"])

    def test_specific_profile_wins_over_unsupported_fallback(self) -> None:
        registry = load_registry()

        self.assertEqual(
            "requirements-package",
            classify_path("docs/01.requirements/0001-example.md", registry),
        )

    def test_package_indexes_machine_contracts_and_operation_subjects_are_registered(self) -> None:
        registry = load_registry()

        expected = {
            "docs/03.specs/0153-example/README.md": "spec-package-readme",
            "docs/03.specs/0153-example/contracts/openapi.yaml": "openapi-contract",
            "docs/03.specs/0153-example/contracts/schema.graphql": "graphql-contract",
            "docs/03.specs/0153-example/contracts/service.proto": "proto-contract",
            "docs/05.operations/catalog/04-data/README.md": "operations-domain-readme",
            "docs/05.operations/catalog/04-data/0051-example/README.md": "operations-subject-readme",
        }
        for path, profile_id in expected.items():
            with self.subTest(path=path):
                self.assertEqual(profile_id, classify_path(path, registry))

        guide = registry.profiles["guide"]
        self.assertEqual("guide-{number:4}", guide["artifact_id_pattern"])
        self.assertEqual("subject-member", guide["identity_relation"])
        self.assertEqual(
            [],
            validate_stable_identity(
                pathlib.PurePosixPath(
                    "docs/05.operations/catalog/04-data/0051-example/guide.md"
                ),
                {"artifact_type": "guide", "artifact_id": "guide-0052"},
                registry.profiles,
            ),
        )

    def test_registered_numeric_identities_do_not_use_substring_matches(self) -> None:
        profiles = load_registry().profiles
        examples = (
            (
                pathlib.PurePosixPath(
                    "docs/05.operations/catalog/data/10012-wrong/guide.md"
                ),
                {"artifact_type": "guide", "artifact_id": "guide-0012"},
            ),
            (
                pathlib.PurePosixPath(
                    "docs/03.specs/9999-contains-0015/plan.md"
                ),
                {"artifact_type": "plan", "artifact_id": "plan-0015"},
            ),
        )
        for path, metadata in examples:
            with self.subTest(path=path):
                self.assertIn(
                    "path-id-mismatch",
                    {
                        finding.code
                        for finding in validate_stable_identity(
                            path, metadata, profiles
                        )
                    },
                )

    def test_every_markdown_template_references_a_profile_not_a_target_path(self) -> None:
        registry = load_registry()

        for role, template in registry.template_roles.items():
            source = template["source"]
            if not str(source).endswith(".md"):
                continue
            with self.subTest(role=role):
                text = (ROOT / str(source)).read_text(encoding="utf-8")
                self.assertIn("profile_id:", text)
                values = _parse_frontmatter_text(text)
                normalized = {
                    key: (
                        "2000-01-01T00:00:00Z"
                        if value == "YYYY-MM-DDTHH:MM:SSZ"
                        else "2000-01-01"
                        if value == "YYYY-MM-DD"
                        else value
                    )
                    for key, value in values.items()
                }
                self.assertEqual(
                    (), validate_frontmatter(normalized)
                )
                self.assertNotIn("docs/01.requirements/", text)
                self.assertNotIn("docs/02.architecture/", text)
                self.assertNotIn("docs/03.specs/", text)
                self.assertNotIn("docs/05.operations/", text)
                self.assertNotIn("docs/90.references/", text)
                self.assertNotIn("docs/98.archive/", text)

    def test_invalid_registry_mutations_fail_closed(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        mutations: dict[str, object] = {
            "duplicate-profile-id": lambda value: value["profiles"].append(
                dict(value["profiles"][0])
            ),
            "non-monotonic-identity": lambda value: value["identity_spaces"][
                "requirement"
            ].update({"next_number": value["identity_spaces"]["requirement"]["high_water"]}),
            "unknown-transition": lambda value: value["lifecycles"]["living"][
                "transitions"
            ]["draft"].append("completed"),
            "release-profile": lambda value: value["profiles"].append(
                {
                    **value["profiles"][0],
                    "profile_id": "release",
                    "path_pattern": "docs/05.operations/releases/{number:4}-{slug}.md",
                }
            ),
            "concrete-template-target": lambda value: value["template_roles"][
                "requirements/package"
            ].update({"target_path": "docs/01.requirements/0001-example.md"}),
            "profile-transition-mismatch": lambda value: value["transitions"].update(
                {"spec": "execution"}
            ),
            "template-source-traversal": lambda value: value["template_roles"][
                "requirements/package"
            ].update(
                {
                    "source": (
                        "docs/99.templates/templates/../../outside.template.md"
                    )
                }
            ),
            "artifact-token-unknown": lambda value: value["profiles"][0].update(
                {"artifact_id_pattern": "REQ-{bogus:4}"}
            ),
            "traceability-profile-unknown": lambda value: value["profiles"][0][
                "traceability"
            ].update({"allowed_parent_profiles": ["typo-profile"]}),
            "template-id-mismatch": lambda value: value["profiles"][0].update(
                {"template_id": "architecture/decision"}
            ),
            "frontmatter-overlap": lambda value: value["profiles"][0][
                "optional_frontmatter"
            ].append(value["profiles"][0]["required_frontmatter"][0]),
            "flattened-requirement-child-space": lambda value: value[
                "identity_spaces"
            ]["requirement"]["child_spaces"].update(
                {
                    "FR": value["identity_spaces"]["requirement"][
                        "child_spaces"
                    ].pop("REQ-0001.FR")
                }
            ),
            "missing-requirement-package-spaces": lambda value: [
                value["identity_spaces"]["requirement"]["child_spaces"].pop(
                    f"REQ-0001.{kind}"
                )
                for kind in ("FR", "NFR", "IF")
            ],
            "repeated-path-separator": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs//01.requirements/{number:4}-{slug}.md"}
            ),
            "dot-path-segment": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/./01.requirements/{number:4}-{slug}.md"}
            ),
            "parent-path-segment": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/../01.requirements/{number:4}-{slug}.md"}
            ),
            "backslash-path-separator": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs\\01.requirements\\{number:4}-{slug}.md"}
            ),
            "unmatched-opening-brace": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/01.requirements/{number:4}-{slug.md"}
            ),
            "unmatched-closing-brace": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/01.requirements/number:4}-{slug}.md"}
            ),
            "path-control-character": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/01.requirements/\n{number:4}-{slug}.md"}
            ),
            "path-unicode-control": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/01.requirements/\u0085{number:4}-{slug}.md"}
            ),
            "path-unicode-format": lambda value: value["profiles"][0].update(
                {"path_pattern": "docs/01.requirements/\u200b{number:4}-{slug}.md"}
            ),
            "markdown-frontmatter-policy-bypass": lambda value: next(
                profile
                for profile in value["profiles"]
                if profile["profile_id"] == "guide"
            ).update(
                {
                    "frontmatter_policy": "absent",
                    "required_frontmatter": [],
                    "optional_frontmatter": [],
                }
            ),
        }

        for name, mutate in mutations.items():
            candidate = json.loads(json.dumps(raw))
            mutate(candidate)  # type: ignore[operator]
            with self.subTest(name=name):
                self.assertTrue(validate_registry(candidate))

    def test_every_canonical_markdown_profile_has_a_satisfiable_profile_id_contract(self) -> None:
        registry = load_registry()
        adapted = build_registry_transition_profiles(
            registry, load_profiles(LEGACY_TRANSITION_PROFILES)
        )
        profile_map = adapted["profiles"]

        def render(value: str) -> str:
            replacements = {
                "{number:4}": "0001",
                "{package_number:4}": "0001",
                "{task_number:4}": "0001",
                "{subject_number:4}": "0001",
                "{year:4}": "2026",
                "{slug}": "example",
                "{domain}": "04-data",
                "{stage}": "01.requirements",
            }
            for token, replacement in replacements.items():
                value = value.replace(token, replacement)
            return value

        values_by_key: dict[str, object] = {
            "status": "draft",
            "artifact_id": "EXAMPLE-0001",
            "artifact_type": "",
            "parent_ids": [],
            "created": "2026-08-20",
            "updated": "2026-08-20",
            "observed_at": "2026-08-20",
            "reviewed_at": "2026-08-20",
            "occurred_at": "2026-08-20T00:00:00Z",
            "layer": "governance",
            "scope": "common",
            "function_id": "example",
            "owner_agent": "rules-engineer",
            "generated_by": "scripts/validation/check-document-metadata.py",
        }
        markdown_profiles = {
            profile_id: profile
            for profile_id, profile in registry.profiles.items()
            if profile.get("frontmatter_policy") == "required"
        }
        self.assertTrue(
            {
                "spec-package-readme",
                "operations-domain-readme",
                "operations-subject-readme",
                "readme",
                "governance-policy",
                "governance-hook-policy",
                "governance-role",
                "governance-skill",
                "governance-provider",
                "governance-sdlc",
                "generated",
                "repo-support",
            }
            <= set(markdown_profiles)
        )
        for profile_id, profile in markdown_profiles.items():
            with self.subTest(profile_id=profile_id):
                required = set(profile["required_frontmatter"])
                optional = set(profile["optional_frontmatter"])
                self.assertIn("profile_id", required)
                self.assertNotIn("profile_id", optional)
                adapted_profile = profile_map[profile_id]
                self.assertIn("profile_id", adapted_profile["required"])
                self.assertNotIn("profile_id", adapted_profile["optional"])

                unordered_values = {
                    key: values_by_key[key]
                    for key in required
                    if key not in {"profile_id", "artifact_id", "artifact_type"}
                }
                unordered_values["profile_id"] = profile_id
                if "artifact_type" in required:
                    unordered_values["artifact_type"] = profile_id
                artifact_pattern = profile.get("artifact_id_pattern")
                if "artifact_id" in required and isinstance(artifact_pattern, str):
                    unordered_values["artifact_id"] = render(artifact_pattern)
                allowed_parents = profile.get("traceability", {}).get(
                    "allowed_parent_profiles", ()
                )
                if "parent_ids" in required and allowed_parents:
                    unordered_values["parent_ids"] = ["PARENT-0001"]
                statuses = (
                    registry.lifecycles.get(str(profile.get("lifecycle_id")), ())
                    if profile.get("lifecycle_id") is not None
                    else ()
                )
                if "status" in required and statuses:
                    unordered_values["status"] = statuses[0]
                frontmatter_order = adapted["common"]["frontmatter_order"]
                metadata_values = {
                    key: unordered_values[key]
                    for key in frontmatter_order
                    if key in unordered_values
                }
                metadata_values.update(
                    {
                        key: value
                        for key, value in unordered_values.items()
                        if key not in metadata_values
                    }
                )
                path = pathlib.Path(render(str(profile["path_pattern"])))
                record = Record(
                    path,
                    metadata_values,
                    profile_id,
                    frontmatter_present=True,
                )
                findings = validate_record(
                    record,
                    adapted,
                    {"PARENT-0001": pathlib.Path("docs/parent.md")},
                )
                self.assertEqual([], findings)

    def test_registry_rejects_duplicate_path_authority(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        duplicate = dict(raw["profiles"][0])
        duplicate.update(
            {
                "profile_id": "requirements-duplicate",
                "template_id": None,
            }
        )
        raw["profiles"].append(duplicate)
        raw["transitions"]["requirements-duplicate"] = "living"

        self.assertIn(
            "profile-path-overlap",
            {finding.code for finding in validate_registry(raw)},
        )

    def test_registry_rejects_nonidentical_path_language_overlap(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        generated = next(
            profile
            for profile in raw["profiles"]
            if profile["profile_id"] == "generated"
        )
        specialized = {
            **generated,
            "profile_id": "generated-report",
            "path_pattern": (
                "docs/90.references/data/{number:4}-{slug}/report.md"
            ),
            "template_id": None,
        }
        raw["profiles"].append(specialized)
        raw["transitions"]["generated-report"] = generated["lifecycle_id"]

        self.assertIn(
            "profile-path-overlap",
            {finding.code for finding in validate_registry(raw)},
        )
        self.assertTrue(
            _path_patterns_overlap(
                "docs/90.references/data/{number:4}-{slug}/{slug}.md",
                "docs/90.references/data/{number:4}-{slug}/report.md",
            )
        )
        self.assertFalse(
            _path_patterns_overlap(
                "docs/90.references/data/{number:4}-{slug}/report.md",
                "docs/90.references/data/{number:4}-{slug}/summary.md",
            )
        )

    def test_loader_rejects_malformed_oversized_deep_and_symlink_sources(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            malformed = root / "malformed.json"
            malformed.write_text("{", encoding="utf-8")
            with self.assertRaises(RegistryError):
                load_registry(malformed)

            deep = root / "deep.json"
            nested: object = "leaf"
            for _ in range(80):
                nested = [nested]
            deep.write_text(json.dumps(nested), encoding="utf-8")
            with self.assertRaises(RegistryError):
                load_registry(deep)

            oversized = root / "oversized.json"
            oversized.write_bytes(b" " * (2 * 1024 * 1024))
            with self.assertRaises(RegistryError):
                load_registry(oversized)

            valid = root / "valid.json"
            valid.write_text(json.dumps(raw), encoding="utf-8")
            linked = root / "linked.json"
            linked.symlink_to(valid)
            with self.assertRaises(RegistryError):
                load_registry(linked)

    def test_default_report_uses_the_bounded_corpus_transition_adapter(self) -> None:
        checker = ROOT / "scripts/validation/check-document-metadata.py"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "docs/01.requirements/0001-example.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "---\nstatus: active\nartifact_id: REQ-0001\n"
                "artifact_type: requirements-package\nparent_ids: []\n"
                "created: 2026-08-20\nupdated: 2026-08-20\n---\n\n"
                "# Example\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--root",
                    str(root),
                    "--mode",
                    "report",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("unknown-profile", result.stdout)

    def test_default_registry_contract_includes_repository_body_findings(self) -> None:
        checker = ROOT / "scripts/validation/check-document-metadata.py"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            readme = root / "docs/99.templates/README.md"
            readme.parent.mkdir(parents=True)
            readme.write_text("# Incomplete Index\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            result = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--root",
                    str(root),
                    "--mode",
                    "check-contracts",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        findings = [
            line
            for line in result.stdout.splitlines()
            if not line.startswith("metadata repository contracts:")
        ]
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertTrue(
            any(
                "readme-heading-missing: docs/99.templates/README.md:" in line
                for line in findings
            ),
            result.stdout,
        )
        self.assertEqual(len(findings), len(set(findings)))
        self.assertNotIn("release-template-cardinality", result.stdout)
        self.assertNotIn("release-route-incomplete", result.stdout)
        self.assertNotIn("registry-array-duplicated", result.stdout)

    def test_cli_rejects_registry_symlink_before_path_resolution(self) -> None:
        checker = ROOT / "scripts/validation/check-document-metadata.py"
        with tempfile.TemporaryDirectory() as directory:
            linked = pathlib.Path(directory) / "registry.json"
            linked.symlink_to(DEFAULT_REGISTRY)
            result = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--mode",
                    "check-contracts",
                    "--registry",
                    str(linked),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("regular non-symlink", result.stderr)

    def test_transition_adapter_preserves_profile_lifecycle_graphs(self) -> None:
        adapted = build_registry_transition_profiles(
            load_registry(), load_profiles(LEGACY_TRANSITION_PROFILES)
        )
        profile_map = adapted["profiles"]
        self.assertIsInstance(profile_map, dict)
        spec = profile_map["spec"]
        self.assertIn("superseded", spec["transitions"]["active"])
        self.assertEqual([], spec["transitions"]["superseded"])

    def test_transition_adapter_rejects_unregistered_new_target_routes(self) -> None:
        adapted = build_registry_transition_profiles(
            load_registry(), load_profiles(LEGACY_TRANSITION_PROFILES)
        )

        self.assertEqual(
            "prd",
            infer_artifact_type(
                pathlib.Path("docs/01.requirements/prd-0001-legacy.md"), adapted
            ),
        )
        self.assertEqual(
            "unsupported",
            infer_artifact_type(
                pathlib.Path("docs/01.requirements/not-numbered.md"), adapted
            ),
        )

    def test_transition_adapter_projects_registry_body_roles(self) -> None:
        registry = load_registry()
        adapted = build_registry_transition_profiles(
            registry, load_profiles(LEGACY_TRANSITION_PROFILES)
        )
        sections = list(registry.profiles["requirements-package"]["required_sections"])
        body = "# Example\n\n" + "\n\n".join(
            f"## {section}\n\nContract content." for section in sections
        )
        record = Record(
            pathlib.Path("docs/01.requirements/0001-example.md"),
            {},
            "requirements-package",
        )

        self.assertEqual(
            [], validate_body_contract(record, body, adapted, changed_boundary=True)
        )
        missing = body.replace(
            "## Acceptance Criteria\n\nContract content.\n\n", "", 1
        )
        self.assertIn(
            "body-heading-missing",
            {
                finding.code
                for finding in validate_body_contract(
                    record, missing, adapted, changed_boundary=True
                )
            },
        )

    def test_null_template_profile_enforces_registry_native_body_sections(self) -> None:
        registry = load_registry()
        adapted = build_registry_transition_profiles(
            registry, load_profiles(LEGACY_TRANSITION_PROFILES)
        )
        path = pathlib.Path("docs/00.agent-governance/sdlc.md")
        valid = Record(
            path,
            {"profile_id": "governance-sdlc"},
            "governance-sdlc",
            frontmatter_present=True,
        )
        body = (
            "# Lifecycle\n\n## Purpose\n\nPurpose.\n\n## Lifecycle\n\nLifecycle.\n\n"
            "## Authority Boundaries\n\nBoundaries.\n\n## Related Documents\n\nLinks.\n"
        )
        self.assertEqual(
            [],
            validate_body_contract(
                valid,
                body,
                adapted,
                changed_boundary=True,
            ),
        )
        findings = validate_body_contract(
            valid,
            body.replace("## Authority Boundaries\n\nBoundaries.\n\n", ""),
            adapted,
            changed_boundary=True,
        )
        self.assertIn("body-heading-missing", {item.code for item in findings})
        invalid = Record(
            path,
            {},
            "governance-sdlc",
            frontmatter_present=True,
        )
        self.assertTrue(
            {"missing-required-key", "profile-id-mismatch"}
            <= {
                finding.code
                for finding in validate_record(
                    invalid, adapted, build_manifest([invalid])
                )
            }
        )

    def test_transition_adapter_allows_legacy_spec_reciprocal_link_only(self) -> None:
        adapted = build_registry_transition_profiles(
            load_registry(), load_profiles(LEGACY_TRANSITION_PROFILES)
        )

        self.assertIn(
            "superseded_by",
            adapted["_legacy_profiles"]["spec"]["optional"],
        )

    def test_canonical_target_profile_id_must_equal_inferred_profile(self) -> None:
        adapted = build_registry_transition_profiles(
            load_registry(), load_profiles(LEGACY_TRANSITION_PROFILES)
        )
        record = Record(
            pathlib.Path("docs/01.requirements/0001-example.md"),
            {
                "profile_id": "spec",
                "status": "draft",
                "artifact_id": "REQ-0001",
                "artifact_type": "requirements-package",
                "parent_ids": [],
                "created": "2026-08-20",
                "updated": "2026-08-20",
            },
            "requirements-package",
        )

        self.assertIn(
            "profile-id-mismatch",
            {
                finding.code
                for finding in validate_record(record, adapted, {})
            },
        )

    def test_frontmatter_schema_enforces_date_formats(self) -> None:
        findings = validate_frontmatter(
            {"created": "not-a-date", "updated": "2026-99-99"}
        )

        self.assertEqual(
            ["frontmatter-schema-invalid", "frontmatter-schema-invalid"],
            sorted(finding.code for finding in findings),
        )


if __name__ == "__main__":
    unittest.main()
