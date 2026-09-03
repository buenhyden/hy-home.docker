from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import scripts.lib.document_governance.registry as registry_module
from scripts.lib.document_governance.registry import (
    document_type,
    DEFAULT_REGISTRY,
    RegistryError,
    _path_patterns_overlap,
    classify_path,
    load_registry,
    _declares_provider_binding,
    resolve_template_placeholders,
    validate_frontmatter,
    validate_registry,
)
from scripts.lib.document_governance.metadata_validator import (
    Record,
    _parse_frontmatter_text,
    build_registry_profiles,
    build_manifest,
    infer_artifact_type,
    load_profiles,
    validate_body_contract,
    validate_record,
)
from scripts.lib.document_governance import metadata_validator
from scripts.lib.document_governance.taxonomy import validate_stable_identity


def _child_env() -> dict[str, str]:
    """Environment for a CLI this test spawns itself.

    The CI gate exports `HYHOME_CI_GATE_ROOT` pointing at its sealed
    `/proc/self/fd/N` root. A child started here is not a gate invocation, and
    the CLIs reject that root as invalid and exit 1 instead of the status the
    test asserts. The variable is therefore dropped for children this test owns.
    It surfaced on 2026-08-29, the first time these suites were executed by a
    gate at all; standalone runs never set it.
    """

    environment = dict(os.environ)
    environment.pop("HYHOME_CI_GATE_ROOT", None)
    return environment


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _fixture_git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _allocation_git_fixture(root: pathlib.Path) -> str:
    registry = root / "docs/99.templates/registry.json"
    registry.parent.mkdir(parents=True)
    shutil.copyfile(DEFAULT_REGISTRY, registry)
    stage = root / "docs/01.requirements"
    stage.mkdir(parents=True)
    for source in (ROOT / "docs/01.requirements").glob("*.md"):
        if source.name != "README.md":
            shutil.copyfile(source, stage / source.name)
    for args in (
        ("init", "-q"),
        ("config", "user.name", "Registry Fixture"),
        ("config", "user.email", "registry@example.invalid"),
        ("add", "."),
        ("commit", "-qm", "baseline"),
    ):
        result = _fixture_git(root, *args)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
    return _fixture_git(root, "rev-parse", "HEAD").stdout.strip()


def _reclassify_fixture_allocation(root: pathlib.Path) -> None:
    registry_path = root / "docs/99.templates/registry.json"
    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    allocation = raw["identity_spaces"]["requirement"]["child_spaces"]["REQ-0003.FR"]
    allocation["reserved_history"].remove(5)
    allocation["current_issued"].append(5)
    registry_path.write_text(json.dumps(raw), encoding="utf-8")
    package_path = root / "docs/01.requirements/0003-security.md"
    package_path.write_text(
        package_path.read_text(encoding="utf-8").replace(
            "\n## Non-functional Requirements\n",
            (
                "\n| REQ-0003-FR-0005 | Reintroduced History | A retired "
                "number must remain unavailable. |\n\n"
                "## Non-functional Requirements\n"
            ),
            1,
        ),
        encoding="utf-8",
    )


class DocumentRegistryTests(unittest.TestCase):
    def test_changed_generated_body_requires_exact_manifest_owner_and_output(
        self,
    ) -> None:
        from scripts.lib.document_governance.metadata_validator import (
            build_registry_profiles,
        )
        from scripts.lib.document_governance.references import (
            generated_reference_owners,
        )

        profiles = build_registry_profiles(load_registry())
        profiles["common"]["generated_outputs"] = generated_reference_owners(ROOT)
        path = pathlib.Path(
            "docs/90.references/data/0065-audit-implementation-matrix/README.md"
        )
        owner = "scripts/validation/generate-audit-implementation-matrix.sh"
        for candidate, generated_by, allowed in (
            (path, owner, True),
            (path, "scripts/forged.py", False),
            (path.with_name("undeclared.md"), owner, False),
        ):
            with self.subTest(path=candidate, owner=generated_by):
                record = Record(
                    candidate,
                    {"profile_id": "data", "generated_by": generated_by},
                    "data",
                )
                findings = validate_body_contract(
                    record, "# Generated\n", profiles, changed_boundary=True
                )
                self.assertEqual(allowed, not findings)

    def test_exact_additional_readme_paths_preserve_profile_validation(self) -> None:
        from scripts.lib.document_governance.metadata_validator import (
            build_registry_profiles,
        )

        registry = load_registry()
        for path in (
            "docs/02.architecture/decisions/README.md",
            "docs/02.architecture/descriptions/README.md",
            "docs/99.templates/README.md",
            "docs/99.templates/templates/README.md",
        ):
            with self.subTest(path=path):
                self.assertEqual("readme", classify_path(path, registry))
                record = Record(
                    pathlib.Path(path),
                    {"status": "active", "type": "sdlc/spec"},
                    "readme",
                )
                self.assertIn(
                    "type-mismatch",
                    {
                        item.code
                        for item in validate_record(
                            record,
                            build_registry_profiles(registry),
                            build_manifest([record]),
                        )
                    },
                )
                self.assertIn(
                    "body-heading-missing",
                    {
                        item.code
                        for item in validate_body_contract(
                            record,
                            "# Navigation\n",
                            build_registry_profiles(registry),
                            changed_boundary=True,
                        )
                    },
                )
        self.assertIsNone(
            classify_path("docs/02.architecture/unknown/README.md", registry)
        )
        for path in ("../outside.md", "docs/03.specs/0104-collision/spec.md"):
            raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
            next(item for item in raw["profiles"] if item["profile_id"] == "readme")[
                "additional_paths"
            ] = [path]
            self.assertTrue(validate_registry(raw))

    def test_bounded_readers_reject_regular_to_fifo_swaps_without_blocking(
        self,
    ) -> None:
        from scripts.lib.document_governance import (
            architecture,
            archive,
            identity_history,
            requirements,
            spec_packages,
        )

        def read_spec(path):
            descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                return spec_packages._read_regular_utf8_at(
                    descriptor, path.name, str(path), spec_packages._LoadBudget()
                )
            finally:
                os.close(descriptor)

        readers = (
            lambda path: registry_module._read_regular_file(path, 1024),
            architecture._read_regular_utf8,
            archive._read_regular,
            identity_history._read_identity_source,
            requirements._read_regular_utf8,
            read_spec,
        )
        real_open = os.open
        for reader in readers:
            with (
                self.subTest(reader=reader.__name__),
                tempfile.TemporaryDirectory() as directory,
            ):
                path = pathlib.Path(directory) / "input.md"
                path.write_text("safe\n", encoding="utf-8")

                def swap(name, flags, *args, **kwargs):
                    if pathlib.Path(name).name == path.name:
                        path.unlink()
                        os.mkfifo(path)
                        self.assertTrue(
                            flags & os.O_NONBLOCK, "FIFO open must not block"
                        )
                    return real_open(name, flags, *args, **kwargs)

                with mock.patch.object(os, "open", side_effect=swap):
                    with self.assertRaises(
                        (ValueError, identity_history.IdentityHistoryError)
                    ):
                        reader(path)

    def test_default_authority_is_registry_json(self) -> None:
        registry = load_registry()

        self.assertEqual(registry.source.as_posix(), "docs/99.templates/registry.json")
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
        self.assertEqual(
            (1, 2, 3, 4), requirement.child_spaces["REQ-0001.FR"].current_issued
        )
        self.assertEqual((), requirement.child_spaces["REQ-0001.IF"].current_issued)
        self.assertEqual((1,), requirement.child_spaces["REQ-0001.IF"].reserved_history)

    def test_spec_0153_package_uses_registered_paths_and_identities(self) -> None:
        registry = load_registry()
        package = pathlib.Path("docs/03.specs/0153-workspace-governance-simplification")
        expected_profiles = {
            ".github/repository-surface.md": "repository-readme",
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

        self.assertEqual(
            "SPEC-0153",
            registry.profiles["spec"]["artifact_id_pattern"].replace(
                "{number:4}", "0153"
            ),
        )
        self.assertEqual(
            "SPEC-0153-PLAN-0001",
            registry.profiles["plan"]["artifact_id_pattern"]
            .replace("{package_number:4}", "0153")
            .replace("{member_number:4}", "0001"),
        )

    def test_specific_profile_wins_over_unsupported_fallback(self) -> None:
        registry = load_registry()

        self.assertEqual(
            "requirements-package",
            classify_path("docs/01.requirements/0001-example.md", registry),
        )

    def test_package_indexes_and_machine_contracts_are_registered(self) -> None:
        registry = load_registry()

        expected = {
            "docs/90.references/audits/README.md": "reference-category-readme",
            "docs/03.specs/0153-example/contracts/openapi.yaml": "openapi-contract",
            "docs/03.specs/0153-example/contracts/schema.graphql": "graphql-contract",
            "docs/03.specs/0153-example/contracts/service.proto": "proto-contract",
            "docs/05.operations/catalog/04-data/README.md": "operations-domain-readme",
        }
        for path, profile_id in expected.items():
            with self.subTest(path=path):
                self.assertEqual(profile_id, classify_path(path, registry))

        guide = registry.profiles["guide"]
        self.assertEqual("GDE-{number:4}", guide["artifact_id_pattern"])
        self.assertEqual("subject-member", guide["identity_relation"])
        self.assertEqual(
            [],
            validate_stable_identity(
                pathlib.PurePosixPath(
                    "docs/05.operations/catalog/04-data/0051-example/guide.md"
                ),
                {"type": "operation/guide", "artifact_id": "GDE-0052"},
                registry.profiles,
            ),
        )

    def test_operations_subject_readme_profile_is_absent(self) -> None:
        registry = load_registry()

        self.assertNotIn("operations-subject-readme", registry.profiles)
        self.assertNotIn("operations-subject-readme", registry.transitions)
        self.assertIsNone(
            classify_path(
                "docs/05.operations/catalog/04-data/0051-example/README.md",
                registry,
            )
        )

    def test_registered_numeric_identities_do_not_use_substring_matches(self) -> None:
        profiles = load_registry().profiles
        examples = (
            (
                pathlib.PurePosixPath(
                    "docs/05.operations/catalog/data/10012-wrong/guide.md"
                ),
                {"type": "operation/guide", "artifact_id": "GDE-0012"},
            ),
            (
                pathlib.PurePosixPath("docs/03.specs/9999-contains-0015/plan.md"),
                {"type": "sdlc/plan", "artifact_id": "SPEC-0015-PLAN-0001"},
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

    def test_every_markdown_template_references_a_profile_not_a_target_path(
        self,
    ) -> None:
        registry = load_registry()

        for role, template in registry.template_roles.items():
            source = template["source"]
            if not str(source).endswith(".md"):
                continue
            with self.subTest(role=role):
                text = (ROOT / str(source)).read_text(encoding="utf-8")
                values = _parse_frontmatter_text(text)
                profile = registry.profiles[str(template["profile_id"])]
                if _declares_provider_binding(profile):
                    # A provider runtime owns this binding, so it declares no type.
                    self.assertIn("name:", text)
                    self.assertNotIn("type:", text)
                else:
                    self.assertIn("type:", text)
                self.assertEqual(
                    (), validate_frontmatter(resolve_template_placeholders(values))
                )
                self.assertNotIn("docs/01.requirements/", text)
                self.assertNotIn("docs/02.architecture/", text)
                self.assertNotIn("docs/03.specs/", text)
                self.assertNotIn("docs/05.operations/", text)
                self.assertNotIn("docs/90.references/", text)
                self.assertNotIn("docs/98.archive/", text)

    def test_operations_profiles_do_not_delegate_current_membership_to_archive(
        self,
    ) -> None:
        from scripts.lib.document_governance.metadata_validator import (
            build_registry_profiles,
        )

        registry = load_registry()
        profiles = build_registry_profiles(registry)["profiles"]

        for profile_id in ("guide", "policy", "runbook"):
            with self.subTest(profile_id=profile_id):
                traceability = registry.profiles[profile_id]["traceability"]
                self.assertNotIn("membership_authority", traceability)
                self.assertTrue(profiles[profile_id]["allow_empty_parents"])

    def test_every_copy_template_is_registered(self) -> None:
        registry = load_registry()
        registered = {
            pathlib.Path(str(value["source"]))
            for value in registry.template_roles.values()
        }
        actual = {
            path.relative_to(ROOT)
            for path in (ROOT / "docs/99.templates/templates").rglob("*")
            if path.is_file()
            and ".template." in path.name
            # Runtime projections are provider-owned bindings, not copy sources.
            and not path.name.endswith("-projection.template.md")
        }

        self.assertEqual(actual, registered)

    def test_invalid_registry_mutations_fail_closed(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        mutations: dict[str, object] = {
            "duplicate-profile-id": lambda value: value["profiles"].append(
                dict(value["profiles"][0])
            ),
            "non-monotonic-identity": lambda value: value["identity_spaces"][
                "requirement"
            ].update(
                {"next_number": value["identity_spaces"]["requirement"]["high_water"]}
            ),
            "reserved-history-reissue": lambda value: value["identity_spaces"][
                "requirement"
            ]["child_spaces"]["REQ-0003.FR"]["current_issued"].append(5),
            "incomplete-allocation-history": lambda value: value["identity_spaces"][
                "requirement"
            ]["child_spaces"]["REQ-0003.FR"]["reserved_history"].remove(5),
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
                "sdlc/requirement"
            ].update({"target_path": "docs/01.requirements/0001-example.md"}),
            "profile-transition-mismatch": lambda value: value["transitions"].update(
                {"spec": "execution"}
            ),
            "index-profile-unknown": lambda value: value["indexes"].update(
                {"docs/03.specs/README.md": "typo-profile"}
            ),
            "template-source-traversal": lambda value: value["template_roles"][
                "sdlc/requirement"
            ].update(
                {"source": ("docs/99.templates/templates/../../outside.template.md")}
            ),
            "artifact-token-unknown": lambda value: value["profiles"][0].update(
                {"artifact_id_pattern": "REQ-{bogus:4}"}
            ),
            "traceability-profile-unknown": lambda value: value["profiles"][0][
                "traceability"
            ].update({"allowed_parent_profiles": ["typo-profile"]}),
            "template-id-mismatch": lambda value: value["profiles"][0].update(
                {"template_id": "sdlc/architecture-decision"}
            ),
            "frontmatter-overlap": lambda value: value["profiles"][0][
                "optional_frontmatter"
            ].append(value["profiles"][0]["required_frontmatter"][0]),
            "flattened-requirement-child-space": lambda value: value["identity_spaces"][
                "requirement"
            ]["child_spaces"].update(
                {
                    "FR": value["identity_spaces"]["requirement"]["child_spaces"].pop(
                        "REQ-0001.FR"
                    )
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

    def test_requirement_allocation_transition_rejects_coherent_reclassification(
        self,
    ) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        allocation = raw["identity_spaces"]["requirement"]["child_spaces"][
            "REQ-0003.FR"
        ]
        allocation["reserved_history"].remove(5)
        allocation["current_issued"].append(5)
        baseline = registry_module.load_trusted_requirement_allocation_baseline(":")

        self.assertEqual((), validate_registry(raw))
        findings = validate_registry(
            raw,
            trusted_requirement_baseline=baseline,
            allow_requirement_allocation_transition=True,
        )

        self.assertIn(
            "requirement-reserved-history-reclassified",
            {finding.code for finding in findings},
        )

    def test_sibling_space_may_advance_by_reservation_but_not_by_a_gap(
        self,
    ) -> None:
        """FR, NFR, and IF share one sequence: the non-issuing siblings advance
        their high-water by recording the same numbers as reservations."""

        baseline = registry_module.load_trusted_requirement_allocation_baseline(":")

        allocated = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        spaces = allocated["identity_spaces"]["requirement"]["child_spaces"]
        issuing = spaces["REQ-0023.FR"]
        allocation = issuing["high_water"] + 1
        issuing["current_issued"].append(allocation)
        issuing["high_water"] = allocation
        issuing["next_number"] = allocation + 1
        for sibling in ("REQ-0023.NFR", "REQ-0023.IF"):
            space = spaces[sibling]
            space["reserved_history"] = sorted(
                set(space["reserved_history"])
                | set(range(1, allocation + 1)) - set(space["current_issued"])
            )
            space["high_water"] = allocation
            space["next_number"] = allocation + 1

        self.assertEqual(
            (),
            validate_registry(
                allocated,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            ),
        )

        gapped = json.loads(json.dumps(allocated))
        gapped_space = gapped["identity_spaces"]["requirement"]["child_spaces"][
            "REQ-0023.NFR"
        ]
        gapped_space["reserved_history"].remove(allocation)
        gapped_space["high_water"] = allocation + 1
        gapped_space["next_number"] = allocation + 2

        self.assertIn(
            "requirement-allocation-transition-invalid",
            {
                finding.code
                for finding in validate_registry(
                    gapped,
                    trusted_requirement_baseline=baseline,
                    allow_requirement_allocation_transition=True,
                )
            },
        )

    def test_requirement_allocation_transition_requires_trusted_baseline(
        self,
    ) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))

        findings = validate_registry(
            raw,
            allow_requirement_allocation_transition=True,
        )

        self.assertIn(
            "requirement-allocation-baseline-required",
            {finding.code for finding in findings},
        )

    def test_requirement_root_high_water_cannot_regress_or_orphan_child_spaces(
        self,
    ) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        requirement = raw["identity_spaces"]["requirement"]
        requirement["high_water"] = 24
        requirement["next_number"] = 25
        baseline = registry_module.load_trusted_requirement_allocation_baseline(":")

        snapshot_codes = {finding.code for finding in validate_registry(raw)}
        transition_codes = {
            finding.code
            for finding in validate_registry(
                raw,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            )
        }

        self.assertIn(
            "requirement-child-space-above-package-high-water", snapshot_codes
        )
        self.assertIn("requirement-package-high-water-regressed", transition_codes)

        advanced = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        advanced_requirement = advanced["identity_spaces"]["requirement"]
        allocated = advanced_requirement["high_water"] + 1
        advanced_requirement["high_water"] = allocated
        advanced_requirement["next_number"] = allocated + 1
        for kind in ("FR", "NFR", "IF"):
            child = json.loads(
                json.dumps(advanced_requirement["child_spaces"][f"REQ-0001.{kind}"])
            )
            child["prefix"] = f"REQ-{allocated:04d}-{kind}-"
            advanced_requirement["child_spaces"][f"REQ-{allocated:04d}.{kind}"] = child
        self.assertEqual(
            (),
            validate_registry(
                advanced,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            ),
        )

    def test_candidate_allocation_bounds_fail_without_finding_expansion(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        requirement = raw["identity_spaces"]["requirement"]
        requirement["high_water"] = 10_000
        requirement["next_number"] = 10_001

        started = time.monotonic()
        findings = validate_registry(raw)
        elapsed = time.monotonic() - started

        self.assertLess(elapsed, 1.0)
        self.assertLessEqual(len(findings), 6)
        self.assertIn(
            "identity-allocation-bound-exceeded",
            {finding.code for finding in findings},
        )
        self.assertNotIn(
            "requirement-package-space-missing",
            {finding.code for finding in findings},
        )

        schema = json.loads(
            registry_module.DEFAULT_PROFILE_SCHEMA.read_text(encoding="utf-8")
        )["$defs"]["identitySpace"]["properties"]
        self.assertEqual(9_999, schema["high_water"]["maximum"])
        self.assertEqual(9_999, schema["next_number"]["maximum"])
        for field in ("current_issued", "reserved_history"):
            self.assertEqual(9_999, schema[field]["maxItems"])
            self.assertEqual(9_999, schema[field]["items"]["maximum"])
        self.assertEqual(9_999, schema["child_spaces"]["maxProperties"])

    def test_trusted_commit_ref_is_resolved_once_before_blob_reads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            baseline_oid = _allocation_git_fixture(root)
            self.assertEqual(
                0, _fixture_git(root, "branch", "moving", baseline_oid).returncode
            )
            _reclassify_fixture_allocation(root)
            self.assertEqual(0, _fixture_git(root, "add", ".").returncode)
            self.assertEqual(
                0,
                _fixture_git(root, "commit", "-qm", "candidate").returncode,
            )
            candidate_oid = _fixture_git(root, "rev-parse", "HEAD").stdout.strip()
            original = registry_module._git_read
            calls: list[tuple[str, ...]] = []
            moved = False

            def moving_ref(args, *, root):  # type: ignore[no-untyped-def]
                nonlocal moved
                calls.append(tuple(args))
                result = original(args, root=root)
                if args[:2] == ["rev-parse", "--verify"]:
                    self.assertEqual(
                        0,
                        _fixture_git(
                            root, "branch", "-f", "moving", candidate_oid
                        ).returncode,
                    )
                    moved = True
                return result

            with mock.patch.object(
                registry_module, "_git_read", side_effect=moving_ref
            ):
                baseline = registry_module.load_trusted_requirement_allocation_baseline(
                    "moving", root=root
                )

            self.assertTrue(moved)
            self.assertEqual(baseline_oid, baseline.source)
            self.assertNotIn(5, baseline.child_spaces["REQ-0003.FR"].current_issued)
            self.assertEqual(
                1,
                sum(any("moving" in argument for argument in call) for call in calls),
            )

    def test_trusted_index_snapshot_reads_captured_blob_oids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _allocation_git_fixture(root)
            original = registry_module._git_read
            index_changed = False

            def moving_index(args, *, root):  # type: ignore[no-untyped-def]
                nonlocal index_changed
                result = original(args, root=root)
                if args[:2] == ["ls-files", "--stage"]:
                    _reclassify_fixture_allocation(root)
                    self.assertEqual(0, _fixture_git(root, "add", ".").returncode)
                    index_changed = True
                return result

            with mock.patch.object(
                registry_module, "_git_read", side_effect=moving_index
            ):
                baseline = registry_module.load_trusted_requirement_allocation_baseline(
                    ":", root=root
                )

            self.assertTrue(index_changed)
            self.assertNotIn(5, baseline.child_spaces["REQ-0003.FR"].current_issued)

    def test_bounded_process_caps_stdout_and_stderr_before_buffering(self) -> None:
        cases = {
            "stdout": "import sys; sys.stdout.write('x' * 4096)",
            "stderr": "import sys; sys.stderr.write('x' * 4096)",
        }
        for channel, source in cases.items():
            with self.subTest(channel=channel):
                with self.assertRaisesRegex(RegistryError, f"{channel}.*byte limit"):
                    registry_module._run_bounded_process(  # type: ignore[attr-defined]
                        [sys.executable, "-c", source],
                        stdout_limit=64,
                        stderr_limit=64,
                    )

    def test_explicit_pinned_commit_allocation_baseline_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            oid = _allocation_git_fixture(root)

            baseline = registry_module.load_trusted_requirement_allocation_baseline(
                oid, root=root
            )

            self.assertEqual(oid, baseline.source)
            self.assertEqual(
                load_registry().identity_spaces["requirement"].high_water,
                baseline.package_high_water,
            )

    def test_every_canonical_markdown_profile_has_a_satisfiable_profile_id_contract(
        self,
    ) -> None:
        registry = load_registry()
        adapted = build_registry_profiles(registry)
        profile_map = adapted["profiles"]

        def render(value: str) -> str:
            replacements = {
                "{number:4}": "0001",
                "{package_number:4}": "0001",
                "{task_number:4}": "0001",
                "{member_number:4}": "0001",
                "{retired_artifact_id}": "SPEC-0001",
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
            "title": "Example",
            "owner": "@buenhyden",
            "version": "0.1.0",
            "type": "",
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
            "agent_id": "rules-engineer",
            "tier": "worker",
            "work_profile": "routine-validation",
            "permission_profile": "read-only",
            "skill_ids": ["policy-gate-agent"],
            "generated_by": "scripts/validation/check-document-metadata.py",
        }
        markdown_profiles = {
            profile_id: profile
            for profile_id, profile in registry.profiles.items()
            if profile.get("frontmatter_policy") == "required"
            and not any(
                item.get("kind") == "provider-owned-binding"
                for item in profile.get("exceptions", ())
            )
        }
        self.assertTrue(
            {
                "reference-category-readme",
                "operations-domain-readme",
                "readme",
                "governance-policy",
                "governance-hook-policy",
                "governance-role",
                "governance-skill",
                "governance-provider",
                "governance-sdlc",
                "generated",
                "documentation-readme",
            }
            <= set(markdown_profiles)
        )
        for profile_id, profile in markdown_profiles.items():
            with self.subTest(profile_id=profile_id):
                required = set(profile["required_frontmatter"])
                optional = set(profile["optional_frontmatter"])
                self.assertIn("type", required)
                self.assertNotIn("type", optional)
                adapted_profile = profile_map[profile_id]
                self.assertIn("type", adapted_profile["required"])
                self.assertNotIn("type", adapted_profile["optional"])

                unordered_values = {
                    key: values_by_key[key]
                    for key in required
                    if key not in {"type", "artifact_id"}
                }
                unordered_values["type"] = document_type(profile_id)
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
                "docs/90.references/data/{number:4}-{slug}/m{member_number:4}-report.md"
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
                "docs/90.references/data/{number:4}-{slug}/m{member_number:4}-{slug}.md",
                "docs/90.references/data/{number:4}-{slug}/m{member_number:4}-report.md",
            )
        )
        self.assertFalse(
            _path_patterns_overlap(
                "docs/90.references/data/{number:4}-{slug}/m{member_number:4}-report.md",
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
                env=_child_env(),
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
            shutil.copy2(DEFAULT_REGISTRY, root / "docs/99.templates/registry.json")
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
                    "registry baseline",
                ],
                cwd=root,
                check=True,
                capture_output=True,
            )
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
                env=_child_env(),
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
                env=_child_env(),
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("regular non-symlink", result.stderr)

    def test_transition_adapter_preserves_profile_lifecycle_graphs(self) -> None:
        adapted = build_registry_profiles(load_registry())
        profile_map = adapted["profiles"]
        self.assertIsInstance(profile_map, dict)
        spec = profile_map["spec"]
        self.assertIn("superseded", spec["transitions"]["active"])
        self.assertEqual([], spec["transitions"]["superseded"])

    def test_adapter_rejects_every_unregistered_target_route(self) -> None:
        """A route the Registry does not own is unsupported, with no fallback.

        The retired legacy envelope classified `prd-####-*.md` as `prd`. That
        profile owned no document, so the route now fails closed like any other
        unregistered path.
        """

        adapted = build_registry_profiles(load_registry())

        for unregistered in (
            "docs/01.requirements/prd-0001-legacy.md",
            "docs/01.requirements/not-numbered.md",
        ):
            with self.subTest(path=unregistered):
                self.assertEqual(
                    "unsupported",
                    infer_artifact_type(pathlib.Path(unregistered), adapted),
                )

    def test_transition_adapter_projects_registry_body_roles(self) -> None:
        registry = load_registry()
        adapted = build_registry_profiles(registry)
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
        missing = body.replace("## Acceptance Criteria\n\nContract content.\n\n", "", 1)
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
        adapted = build_registry_profiles(registry)
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
            {"missing-required-key"}
            <= {
                finding.code
                for finding in validate_record(
                    invalid, adapted, build_manifest([invalid])
                )
            }
        )

    def test_canonical_target_profile_id_must_equal_inferred_profile(self) -> None:
        adapted = build_registry_profiles(load_registry())
        record = Record(
            pathlib.Path("docs/01.requirements/0001-example.md"),
            {
                "title": "Example",
                "type": "sdlc/spec",
                "layer": "requirements",
                "status": "draft",
                "owner": "@buenhyden",
                "artifact_id": "REQ-0001",
                "parent_ids": [],
                "created": "2026-08-20",
                "updated": "2026-08-20",
            },
            "requirements-package",
        )

        self.assertIn(
            "type-mismatch",
            {finding.code for finding in validate_record(record, adapted, {})},
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


class FreeFormProfileTests(unittest.TestCase):
    """A profile with no shared heading vocabulary declares itself free-form.

    `governance-policy` spans 16 documents with 51 distinct H2 headings, of
    which only `Related Documents` appears in more than one. Registering the
    other 50 would state a contract nothing shares; leaving them unregistered
    makes every edit to any of those documents a violation while the corpus
    itself passes, because only headings a change introduces are counted.
    """

    def _adapted(self):
        return build_registry_profiles(load_registry())

    def _codes(self, profile_id: str, path: str, headings: tuple[str, ...]):
        record = Record(
            path=pathlib.Path(path),
            metadata={"profile_id": profile_id, "status": "active"},
            artifact_type=profile_id,
        )
        body = "# Title\n\n" + "".join(f"## {h}\n\ncontent\n\n" for h in headings)
        return {
            finding.code
            for finding in validate_body_contract(record, body, self._adapted(), True)
        }

    def test_free_form_profile_permits_an_unregistered_heading(self) -> None:
        codes = self._codes(
            "governance-policy",
            "docs/00.agent-governance/policies/quality-standards.md",
            ("Anything At All", "Related Documents"),
        )
        self.assertNotIn("body-heading-forbidden", codes)

    def test_free_form_profile_still_requires_related_documents(self) -> None:
        codes = self._codes(
            "governance-policy",
            "docs/00.agent-governance/policies/quality-standards.md",
            ("Anything At All",),
        )
        self.assertIn("body-heading-missing", codes)

    def test_a_contracted_profile_still_rejects_an_unregistered_heading(self) -> None:
        codes = self._codes(
            "governance-role",
            "docs/00.agent-governance/roles/qa-engineer.md",
            (
                "Purpose",
                "Use When",
                "Inputs",
                "Outputs",
                "Permissions",
                "Success Criteria",
                "Failure and Escalation",
                "Related Documents",
                "Anything At All",
            ),
        )
        self.assertIn("body-heading-forbidden", codes)

    def test_every_governance_policy_document_satisfies_its_own_contract(self) -> None:
        policies = sorted(
            path
            for path in (ROOT / "docs/00.agent-governance").rglob("*.md")
            if re.search(
                r"^type:\s*governance/policy\s*$",
                path.read_text(encoding="utf-8"),
                re.M,
            )
        )
        self.assertGreaterEqual(len(policies), 16)
        adapted = self._adapted()
        offenders: list[str] = []
        for path in policies:
            record = Record(
                path=path.relative_to(ROOT),
                metadata={"profile_id": "governance-policy", "status": "active"},
                artifact_type="governance-policy",
            )
            findings = validate_body_contract(
                record, path.read_text(encoding="utf-8"), adapted, True
            )
            offenders.extend(
                f"{path.relative_to(ROOT)}: {finding.message}"
                for finding in findings
                if finding.code == "body-heading-forbidden"
            )
        self.assertEqual([], offenders)


class ExecutionLifecycleTests(unittest.TestCase):
    """A Task drafted and finished inside one change is the normal case.

    `check-changed` compares the status at the merge base with the status at
    HEAD. It does not walk the commits between them, so an intermediate
    `active` commit is invisible to it: SPEC-0154's own spec.md passed through
    draft, active, and completed in three commits and still reported
    `draft -> completed`. Requiring `active` at the change boundary therefore
    does not record that work was tracked; it forbids completing any document
    that was drafted before the merge base, which is every Task an agent
    writes and finishes in one branch.
    """

    def _transitions(self, profile_id: str) -> dict[str, list[str]]:
        registry = load_registry()
        return {
            key: list(value)
            for key, value in dict(registry.transitions[profile_id]).items()
        }

    def test_execution_lifecycle_completes_from_draft(self) -> None:
        for profile_id in ("task", "plan"):
            with self.subTest(profile_id=profile_id):
                self.assertIn("completed", self._transitions(profile_id)["draft"])

    def test_execution_lifecycle_keeps_active_reachable(self) -> None:
        transitions = self._transitions("task")
        self.assertIn("active", transitions["draft"])
        self.assertIn("completed", transitions["active"])

    def test_execution_lifecycle_still_refuses_to_reopen(self) -> None:
        self.assertEqual([], self._transitions("task")["completed"])

    def test_spec_package_lifecycle_stays_strict(self) -> None:
        # A Spec Package is reviewed as `active` before it can complete. Only
        # the Task lifecycle relaxes, because only a Task is routinely drafted
        # and finished inside one change.
        self.assertNotIn("completed", self._transitions("spec")["draft"])


class InvalidPreviousStatusTests(unittest.TestCase):
    """A status the lifecycle never defined is repaired, not transitioned.

    `docs/98.archive/migrations/0001` and `0002` carried `archived`, which is
    not a member of any lifecycle in the registry. The transition check reads
    `transitions[previous_status]`, finds nothing, and demands an override for
    every move out of that state. The override is unreachable twice over: its
    `evidence_task` contract matches no path in this repository, and no gate
    or workflow passes an override file at all. The effect is that an invalid
    status is cheaper to keep than to correct.
    """

    def _profiles(self):
        return build_registry_profiles(load_registry())

    def _codes(self, previous_status: str, status: str) -> set[str]:
        record = Record(
            path=pathlib.Path("docs/98.archive/migrations/0001-fixture.md"),
            metadata={
                "profile_id": "migration",
                "status": status,
                "artifact_id": "MIG-0001",
                "artifact_type": "migration",
                "parent_ids": ["SPEC-0136"],
                "created": "2026-08-29",
                "updated": "2026-08-30",
            },
            artifact_type="migration",
            previous_status=previous_status,
        )
        return {
            finding.code for finding in validate_record(record, self._profiles(), {})
        }

    def test_repair_from_an_undefined_status_is_not_a_transition(self) -> None:
        self.assertNotIn("invalid-transition", self._codes("archived", "completed"))

    def test_move_between_defined_statuses_still_follows_the_lifecycle(self) -> None:
        self.assertIn("invalid-transition", self._codes("superseded", "completed"))

    def test_repair_must_land_on_a_defined_status(self) -> None:
        self.assertIn("invalid-transition", self._codes("archived", "archived-too"))


class ResurrectedMigrationContractTests(unittest.TestCase):
    """A completed migration's contract is not resurrected on every load.

    `DEFAULT_MIGRATION_CONTRACT` was a `HistoricalDocument`, not a path: every
    `load_profiles()` read `docs/99.templates/support/document-corpus-migration-contract.yaml`
    out of the pinned commit `49406580` and validated its 384-line shape,
    including eight named migration waves whose source document, SPEC-0153, was
    deleted. The file is absent from the working tree. The only caller that
    consumed the result, `load_promoted_transition_witnesses`, returned `{}` on
    every CLI route because the profiles the CLI builds always carry
    `_registry`; the other caller discarded the value.
    """

    def test_the_migration_contract_loader_is_gone(self) -> None:
        for name in (
            "load_migration_contract",
            "DEFAULT_MIGRATION_CONTRACT",
            "SDLC_TAXONOMY_BASELINE",
            "SDLC_TAXONOMY_MANIFEST_PATH",
            "SDLC_TAXONOMY_SOURCE_ROOTS",
            "load_promoted_transition_witnesses",
            "PromotedTransitionWitness",
        ):
            with self.subTest(name=name):
                self.assertFalse(
                    hasattr(metadata_validator, name),
                    f"{name} still resurrects a completed migration's contract",
                )

    def test_no_stage_04_route_is_pinned_in_the_validator(self) -> None:
        facade = pathlib.Path(metadata_validator.__file__)
        sources = (facade, *sorted((facade.parent / "metadata").glob("*.py")))
        for path in sources:
            with self.subTest(path=path.name):
                self.assertNotIn(
                    "docs/04.execution",
                    path.read_text(encoding="utf-8"),
                )

    def test_profiles_still_load_without_the_resurrected_contract(self) -> None:
        """`load_profiles()` no longer takes a contract path and still works.

        It used to accept `migration_contract_path` and call the loader purely
        for its side effect, discarding the result, so every profile load in
        the repository paid for a Git read of a deleted file.
        """

        import inspect

        signature = inspect.signature(metadata_validator.load_profiles)
        self.assertNotIn("migration_contract_path", signature.parameters)
        profiles = metadata_validator.load_profiles()
        self.assertIn("governance-policy", profiles)


class RegistryIndexContractTests(unittest.TestCase):
    """The index binding is a Registry fact, not a path hardcoded in Python."""

    def test_unknown_member_profile_is_named_exactly(self) -> None:
        raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        raw["indexes"]["docs/03.specs/README.md"] = "typo-profile"
        self.assertEqual(
            ["index-profile-unknown"],
            [finding.code for finding in validate_registry(raw)],
        )

    def test_every_index_binds_a_registered_profile(self) -> None:
        registry = load_registry()
        self.assertTrue(registry.indexes)
        for index_path, member_profile in registry.indexes.items():
            with self.subTest(index=index_path):
                self.assertIn(member_profile, registry.profiles)
