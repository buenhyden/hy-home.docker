from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import json
import pathlib
import re
import shutil
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _requirements_module():
    module_name = "scripts.lib.document_governance.requirements"
    if importlib.util.find_spec(module_name) is None:
        raise AssertionError(f"missing production module: {module_name}")
    return importlib.import_module(module_name)


def _registry_module():
    return importlib.import_module("scripts.lib.document_governance.registry")


def _package_text(
    *,
    number: str = "0001",
    functional: str | None = None,
    non_functional: str | None = None,
    interface: str | None = None,
) -> str:
    functional = functional or (
        f"- **REQ-{number}-FR-0001**: The package provides behavior one.\n"
        f"- **REQ-{number}-FR-0002**: The package provides behavior two.\n"
        f"- **REQ-{number}-FR-0003**: The package provides behavior three.\n"
        f"- **REQ-{number}-FR-0004**: The package provides behavior four."
    )
    non_functional = "" if non_functional is None else non_functional
    interface = "" if interface is None else interface
    return f"""---
title: Fixture Requirement Package
type: sdlc/requirement
layer: requirements
status: active
owner: "@buenhyden"
artifact_id: REQ-{number}
parent_ids: []
created: 2026-08-22
updated: 2026-08-22
---

# Fixture Requirement Package

## Problem and Goals

One bounded problem and goal.

## Stakeholders and User Needs

One stakeholder need.

## Functional Requirements

{functional}

## Non-functional Requirements

{non_functional}

## Interface Requirements

{interface}

## Constraints

One constraint.

## Acceptance Criteria

- The declared requirements are independently verifiable.

## Traceability

- Architecture and Spec links are added when their packages exist.
"""


class RequirementPackageTests(unittest.TestCase):
    def _write_package(
        self,
        directory: pathlib.Path,
        *,
        name: str = "0001-example.md",
        text: str | None = None,
    ) -> pathlib.Path:
        path = directory / name
        path.write_text(text or _package_text(), encoding="utf-8")
        return path

    def test_requirement_package_identity_is_owned_by_path(self) -> None:
        requirements = _requirements_module()
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory))
            package = requirements.parse_requirement_package(path)

        self.assertEqual("REQ-0001", package.artifact_id)
        self.assertEqual(("FR", "FR", "FR", "FR"), tuple(i.kind for i in package.items))
        self.assertTrue(
            all(item.identity.startswith("REQ-0001-") for item in package.items)
        )
        self.assertTrue(dataclasses.is_dataclass(package))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            package.artifact_id = "REQ-9999"

    def test_path_package_mismatch_fails_closed(self) -> None:
        requirements = _requirements_module()
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(
                pathlib.Path(directory),
                name="0002-example.md",
                text=_package_text(number="0001"),
            )
            with self.assertRaisesRegex(
                requirements.RequirementPackageError, "path.*REQ-0002"
            ):
                requirements.parse_requirement_package(path)

    def test_legacy_bare_and_malformed_declarations_fail_closed(self) -> None:
        requirements = _requirements_module()
        mutations = {
            "legacy-package": _package_text().replace(
                "REQ-0001-FR-0001", "PRD-0001-R0001", 1
            ),
            "bare-child": _package_text().replace("REQ-0001-FR-0001", "FR-0001", 1),
            "retired-interface": _package_text().replace(
                "REQ-0001-FR-0001", "interface-0001", 1
            ),
            "wrong-kind": _package_text().replace(
                "REQ-0001-FR-0001", "REQ-0001-NFR-0001", 1
            ),
            "malformed-list": _package_text().replace(
                "- **REQ-0001-FR-0001**:", "- REQ-0001-FR-0001:", 1
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for label, text in mutations.items():
                with self.subTest(label=label):
                    path = self._write_package(root, text=text)
                    with self.assertRaises(requirements.RequirementPackageError):
                        requirements.parse_requirement_package(path)

    def test_parser_rejects_retired_interface_identifier_anywhere(self) -> None:
        requirements = _requirements_module()
        text = _package_text().replace(
            "- Architecture and Spec links are added when their packages exist.",
            "- Retired reference: interface-0001.",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory), text=text)
            with self.assertRaisesRegex(
                requirements.RequirementPackageError, "retired identity"
            ):
                requirements.parse_requirement_package(path)

    def test_duplicate_or_reused_child_identity_fails_closed(self) -> None:
        requirements = _requirements_module()
        duplicated = _package_text(
            functional=(
                "- **REQ-0001-FR-0001**: The package provides one behavior.\n"
                "- **REQ-0001-FR-0001**: The package repeats that behavior."
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory), text=duplicated)
            with self.assertRaisesRegex(
                requirements.RequirementPackageError, "duplicate|reused"
            ):
                requirements.parse_requirement_package(path)

    def test_child_declarations_follow_registry_allocation_state(self) -> None:
        requirements = _requirements_module()
        mutations = {
            "above-high-water": _package_text().replace(
                "REQ-0001-FR-0004", "REQ-0001-FR-9999", 1
            ),
            "reserved-if-reintroduction": _package_text(
                interface=(
                    "- **REQ-0001-IF-0001**: A retired interface identity must "
                    "not be reintroduced."
                )
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for label, text in mutations.items():
                with self.subTest(label=label):
                    path = self._write_package(root, text=text)
                    with self.assertRaisesRegex(
                        requirements.RequirementPackageError,
                        "allocation|high-water|reserved|issued",
                    ):
                        requirements.parse_requirement_package(path)

    def test_public_parser_requires_exact_current_issued_declarations(self) -> None:
        requirements = _requirements_module()
        source = ROOT / "docs/01.requirements/0001-gateway.md"
        incomplete = source.read_text(encoding="utf-8").replace(
            (
                "- **REQ-0001-FR-0004**: OAuth2 Proxy와 연동하여 특정 경로에 "
                "대한 인증(SSO) 미들웨어를 제공해야 함.\n"
            ),
            "",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory), text=incomplete)
            with self.assertRaisesRegex(
                requirements.RequirementPackageError,
                "current_issued|declarations|allocation",
            ):
                requirements.parse_requirement_package(path)

    def test_document_and_registry_cannot_reintroduce_reserved_history(self) -> None:
        requirements = _requirements_module()
        source = ROOT / "docs/01.requirements/0003-security.md"
        reintroduced = source.read_text(encoding="utf-8").replace(
            "\n## Non-functional Requirements\n",
            (
                "\n| REQ-0003-FR-0005 | Reintroduced History | A retired "
                "number must remain unavailable. |\n\n"
                "## Non-functional Requirements\n"
            ),
            1,
        )
        registry = requirements.load_registry()
        requirement = registry.identity_spaces["requirement"]
        child_spaces = dict(requirement.child_spaces)
        allocation = child_spaces["REQ-0003.FR"]
        child_spaces["REQ-0003.FR"] = dataclasses.replace(
            allocation, current_issued=(*allocation.current_issued, 5)
        )
        identity_spaces = dict(registry.identity_spaces)
        identity_spaces["requirement"] = dataclasses.replace(
            requirement, child_spaces=child_spaces
        )
        paired_registry = dataclasses.replace(registry, identity_spaces=identity_spaces)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            package_path = self._write_package(
                root, name="0003-security.md", text=reintroduced
            )
            with self.assertRaisesRegex(
                ValueError,
                "history|reserved|issued|allocation",
            ):
                requirements.parse_requirement_package(
                    package_path, registry=paired_registry
                )

    def test_honestly_new_id_requires_coherent_atomic_registry_advance(self) -> None:
        requirements = _requirements_module()
        baseline = _registry_module().load_trusted_requirement_allocation_baseline(":")
        raw_registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        allocation = raw_registry["identity_spaces"]["requirement"]["child_spaces"][
            "REQ-0001.FR"
        ]
        allocation.update(
            {
                "high_water": 5,
                "next_number": 6,
                "current_issued": [1, 2, 3, 4, 5],
            }
        )
        advanced = _package_text(
            functional=(
                "- **REQ-0001-FR-0001**: The package provides behavior one.\n"
                "- **REQ-0001-FR-0002**: The package provides behavior two.\n"
                "- **REQ-0001-FR-0003**: The package provides behavior three.\n"
                "- **REQ-0001-FR-0004**: The package provides behavior four.\n"
                "- **REQ-0001-FR-0005**: The package provides newly allocated behavior."
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            registry_path = root / "registry.json"
            registry_path.write_text(json.dumps(raw_registry), encoding="utf-8")
            registry = requirements.load_registry(
                registry_path,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            )
            package_path = self._write_package(root, text=advanced)

            package = requirements.parse_requirement_package(
                package_path,
                registry=registry,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            )

        self.assertEqual("REQ-0001-FR-0005", package.items[-1].identity)

    def test_coherent_reclassification_fails_public_parse_and_stage_load(self) -> None:
        requirements = _requirements_module()
        registry_module = _registry_module()
        baseline = registry_module.load_trusted_requirement_allocation_baseline(":")
        raw_registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        allocation = raw_registry["identity_spaces"]["requirement"]["child_spaces"][
            "REQ-0003.FR"
        ]
        allocation["reserved_history"].remove(5)
        allocation["current_issued"].append(5)
        source = ROOT / "docs/01.requirements/0003-security.md"
        reintroduced = source.read_text(encoding="utf-8").replace(
            "\n## Non-functional Requirements\n",
            (
                "\n| REQ-0003-FR-0005 | Reintroduced History | A retired "
                "number must remain unavailable. |\n\n"
                "## Non-functional Requirements\n"
            ),
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            registry_path = root / "registry.json"
            registry_path.write_text(json.dumps(raw_registry), encoding="utf-8")
            candidate_registry = requirements.load_registry(registry_path)
            package_path = self._write_package(
                root, name="0003-security.md", text=reintroduced
            )
            with self.subTest(surface="public-parse"):
                with self.assertRaisesRegex(
                    ValueError, "history|reserved|baseline|transition"
                ):
                    requirements.parse_requirement_package(
                        package_path,
                        registry=candidate_registry,
                        trusted_requirement_baseline=baseline,
                        allow_requirement_allocation_transition=True,
                    )

            stage = root / "stage"
            stage.mkdir()
            for source_path in (ROOT / "docs/01.requirements").glob("*.md"):
                if source_path.name == "README.md":
                    continue
                shutil.copyfile(source_path, stage / source_path.name)
            (stage / "0003-security.md").write_text(reintroduced, encoding="utf-8")
            with self.subTest(surface="stage-load"):
                with self.assertRaisesRegex(
                    ValueError, "history|reserved|baseline|transition"
                ):
                    requirements.load_requirement_packages(
                        stage,
                        registry=candidate_registry,
                        trusted_requirement_baseline=baseline,
                        allow_requirement_allocation_transition=True,
                    )

    def test_candidate_allocation_transition_requires_trusted_baseline(self) -> None:
        requirements = _requirements_module()
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory))

            with self.assertRaisesRegex(ValueError, "trusted.*baseline"):
                requirements.parse_requirement_package(
                    path,
                    registry=requirements.load_registry(),
                    allow_requirement_allocation_transition=True,
                )

    def test_root_high_water_regression_fails_public_parse_and_stage_load(self) -> None:
        requirements = _requirements_module()
        registry_module = _registry_module()
        baseline = registry_module.load_trusted_requirement_allocation_baseline(":")
        registry = requirements.load_registry()
        requirement = registry.identity_spaces["requirement"]
        current = requirement.high_water
        regressed = dataclasses.replace(
            requirement, high_water=current - 1, next_number=current
        )
        identity_spaces = dict(registry.identity_spaces)
        identity_spaces["requirement"] = regressed
        candidate_registry = dataclasses.replace(
            registry, identity_spaces=identity_spaces
        )

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            package_path = self._write_package(root)
            with self.subTest(surface="public-parse"):
                with self.assertRaisesRegex(ValueError, "package.*high-water|regress"):
                    requirements.parse_requirement_package(
                        package_path,
                        registry=candidate_registry,
                        trusted_requirement_baseline=baseline,
                        allow_requirement_allocation_transition=True,
                    )

            stage = root / "stage"
            stage.mkdir()
            for source_path in (ROOT / "docs/01.requirements").glob("*.md"):
                if source_path.name != "README.md":
                    shutil.copyfile(source_path, stage / source_path.name)
            with self.subTest(surface="stage-load"):
                with self.assertRaisesRegex(ValueError, "package.*high-water|regress"):
                    requirements.load_requirement_packages(
                        stage,
                        registry=candidate_registry,
                        trusted_requirement_baseline=baseline,
                        allow_requirement_allocation_transition=True,
                    )

            child_spaces = dict(requirement.child_spaces)
            for kind in ("FR", "NFR", "IF"):
                source_space = child_spaces[f"REQ-0001.{kind}"]
                child_spaces[f"REQ-{current + 1:04d}.{kind}"] = dataclasses.replace(
                    source_space, prefix=f"REQ-{current + 1:04d}-{kind}-"
                )
            advanced_requirement = dataclasses.replace(
                requirement,
                high_water=current + 1,
                next_number=current + 2,
                child_spaces=child_spaces,
            )
            identity_spaces["requirement"] = advanced_requirement
            advanced_registry = dataclasses.replace(
                registry, identity_spaces=dict(identity_spaces)
            )
            with self.subTest(surface="stage-missing-new-package"):
                with self.assertRaisesRegex(ValueError, "package.*coverage|missing"):
                    requirements.load_requirement_packages(
                        stage,
                        registry=advanced_registry,
                        trusted_requirement_baseline=baseline,
                        allow_requirement_allocation_transition=True,
                    )
            self._write_package(
                stage,
                name=f"{current + 1:04d}-new.md",
                text=_package_text(number=f"{current + 1:04d}"),
            )
            packages = requirements.load_requirement_packages(
                stage,
                registry=advanced_registry,
                trusted_requirement_baseline=baseline,
                allow_requirement_allocation_transition=True,
            )
            self.assertEqual(f"REQ-{current + 1:04d}", packages[-1].artifact_id)

    def test_parser_rejects_unbounded_non_utf8_and_symlink_inputs(self) -> None:
        requirements = _requirements_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            oversized = root / "0001-oversized.md"
            oversized.write_bytes(b"x" * (requirements.MAX_REQUIREMENT_BYTES + 1))
            invalid_utf8 = root / "0001-invalid.md"
            invalid_utf8.write_bytes(b"\xff")
            target = self._write_package(root, name="0001-target.md")
            linked = root / "0001-linked.md"
            linked.symlink_to(target)
            for label, path in (
                ("oversized", oversized),
                ("invalid-utf8", invalid_utf8),
                ("symlink", linked),
            ):
                with self.subTest(label=label):
                    with self.assertRaises(requirements.RequirementPackageError):
                        requirements.parse_requirement_package(path)

    def test_stage_rejects_executable_interface_payloads(self) -> None:
        requirements = _requirements_module()
        payloads = {
            "openapi.yaml": "openapi: 3.1.0\n",
            "schema.graphql": "type Query { health: String! }\n",
            "service.proto": 'syntax = "proto3";\n',
        }
        with tempfile.TemporaryDirectory() as directory:
            stage = pathlib.Path(directory) / "docs/01.requirements"
            stage.mkdir(parents=True)
            self._write_package(stage)
            for name, body in payloads.items():
                with self.subTest(name=name):
                    payload = stage / name
                    payload.write_text(body, encoding="utf-8")
                    with self.assertRaisesRegex(
                        requirements.RequirementPackageError,
                        "Stage 03|executable interface",
                    ):
                        requirements.load_requirement_packages(stage)
                    payload.unlink()

    def test_parser_rejects_embedded_executable_interface_families(self) -> None:
        requirements = _requirements_module()
        payloads = {
            "openapi-2-json": '```json\n{"swagger": "2.0", "paths": {}}\n```',
            "openapi-3-json": '```json\n{"openapi": "3.1.0", "paths": {}}\n```',
            "openapi-2-yaml-indented": '    swagger: "2.0"\n    paths: {}',
            "openapi-3-yaml-indented": "    openapi: 3.0.3\n    paths: {}",
            "openapi-3-yaml-comment": (
                "    openapi: 3.1.0 # trailing YAML comment\n    paths: {}"
            ),
            "openapi-3-yaml-flow": "{openapi: 3.1.0, paths: {}}",
            "openapi-3-json-escaped-key": (
                '```json\n{"\\u006fpenapi": "3.1.0", "paths": {}}\n```'
            ),
            "openapi-json-multiline-flow": (
                '```json\n{ "\\u006fpenapi"\n:\n"3.1.0", "paths": {} }\n```'
            ),
            "openapi-yaml-quoted-key-tag-anchor": (
                "```yaml\n{ 'openapi': !!str &oas\n  '3.1.0', paths: {} }\n```"
            ),
            "openapi-yaml-anchor-alias": (
                "```yaml\nversion: &oas 3.1.0\n{ openapi: *oas, paths: {} }\n```"
            ),
            "openapi-yaml-folded-block-scalar": (
                "```yaml\nopenapi: >-\n  3.1.0\npaths: {}\n```"
            ),
            "openapi-yaml-literal-block-scalar": (
                "```yaml\nopenapi: |-\n  3.1.0\npaths: {}\n```"
            ),
            "graphql-non-query": "```graphql\ntype Mutation { rotate: Boolean! }\n```",
            "graphql-schema-directive": (
                "```graphql\nschema @auth { mutation: Mutation }\n```"
            ),
            "graphql-extended-mutation-directive": (
                "```graphql\nextend type Mutation @auth { rotate: Boolean! }\n```"
            ),
            "graphql-subscription-directive": (
                "```graphql\ntype Subscription @auth { events: String! }\n```"
            ),
            "graphql-next-line-brace": (
                "```graphql\nextend type Mutation @auth\n{\n  rotate: Boolean!\n}\n```"
            ),
            "graphql-blank-multiline-directive": (
                "```graphql\nextend\n\n type\n Mutation\n"
                "@auth(\n role: ADMIN\n)\n\n{\n rotate: Boolean!\n}\n```"
            ),
            "graphql-schema-multiline-directive": (
                '```graphql\nschema\n@link(\n url: "urn:fixture"\n)\n\n'
                "{\n query: Query\n}\n```"
            ),
            "graphql-comments-and-nested-directive-input": (
                "```graphql\nextend # extension comment\n"
                "type # kind comment\nMutation\n"
                "@auth(rule: { any: [{ nested: true }] }, "
                'note: "parenthesis ( stays literal )")\n'
                "# brace comment\n{\n rotate: Boolean!\n}\n```"
            ),
            "proto2-indented": '    syntax = "proto2";\n    message Health {}',
            "proto3-indented": '    syntax = "proto3";\n    message Health {}',
            "proto2-implicit": (
                "```proto\nmessage Legacy {\n"
                "  required string name = 1;\n"
                "  optional int32 count = 2;\n}\n```"
            ),
            "proto2-implicit-one-line-service": (
                "```proto\nmessage Legacy { required string name = 1; } "
                "service LegacyApi { rpc Get (Legacy) returns (Legacy); }\n```"
            ),
            "proto-imported-type-service": (
                "```proto\nservice Health {\n rpc Check (\n"
                "  google.protobuf.Empty\n ) returns (\n"
                "  acme.v1.Health\n );\n}\n```"
            ),
            "proto-service-option-aggregate-before-rpc": (
                "```proto\nservice Health {\n"
                " option (google.api.default_host) = {\n"
                '  value: { nested: "fixture } literal" }\n };\n'
                " rpc Check (google.protobuf.Empty) "
                "returns (acme.v1.Health);\n}\n```"
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for label, payload in payloads.items():
                with self.subTest(label=label):
                    path = self._write_package(
                        root, text=f"{_package_text()}\n{payload}\n"
                    )
                    with self.assertRaisesRegex(
                        requirements.RequirementPackageError,
                        "Stage 03|executable interface",
                    ):
                        requirements.parse_requirement_package(path)

    def test_executable_detector_does_not_reject_requirement_prose(self) -> None:
        requirements = _requirements_module()
        prose_examples = (
            "The service message should remain optional and versioned.",
            "A GraphQL type Mutation may be discussed without source braces.",
            "OpenAPI 3.1 compatibility is a product constraint, not a schema.",
            "A GraphQL type Mutation with an auth directive may place a brace later.",
            "An imported protobuf type may be used by an RPC in a future service.",
            "OpenAPI anchors and YAML tags are implementation details, not requirements.",
            "The invalid pair openapi: 2.0 is not an executable OpenAPI declaration.",
            "GraphQL comments and nested inputs are discussed without a declaration.",
            "A Proto service option may use an aggregate before an RPC is designed.",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for index, prose in enumerate(prose_examples):
                with self.subTest(prose=prose):
                    path = self._write_package(
                        root,
                        name=f"0001-prose-{index}.md",
                        text=f"{_package_text()}\n{prose}\n",
                    )
                    package = requirements.parse_requirement_package(path)
                    self.assertEqual("REQ-0001", package.artifact_id)

    def test_reader_rejects_valid_prefix_short_read(self) -> None:
        requirements = _requirements_module()
        registry = requirements.load_registry()
        valid_prefix = _package_text().encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(
                pathlib.Path(directory),
                text=_package_text() + "\ntrailing content that must be read\n",
            )
            with mock.patch.object(
                requirements.os, "read", side_effect=(valid_prefix, b"")
            ):
                with self.assertRaisesRegex(
                    requirements.RequirementPackageError,
                    "short read|changed while reading",
                ):
                    requirements.parse_requirement_package(path, registry=registry)

    def test_reader_rejects_concurrent_growth(self) -> None:
        requirements = _requirements_module()
        registry = requirements.load_registry()
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_package(pathlib.Path(directory))
            opened = path.stat()
            grown_values = list(opened)
            grown_values[6] += 1
            grown = type(opened)(grown_values)
            with mock.patch.object(
                requirements.os, "fstat", side_effect=(opened, grown)
            ):
                with self.assertRaisesRegex(
                    requirements.RequirementPackageError, "changed while reading"
                ):
                    requirements.parse_requirement_package(path, registry=registry)

    def test_current_stage_holds_the_canonical_package_run(self) -> None:
        from scripts.lib.document_governance.registry import load_registry

        requirements = _requirements_module()
        stage = ROOT / "docs/01.requirements"
        packages = requirements.load_requirement_packages(stage)
        high_water = load_registry().identity_spaces["requirement"].high_water
        self.assertEqual(
            [f"REQ-{number:04d}" for number in range(1, high_water + 1)],
            [package.artifact_id for package in packages],
        )
        self.assertFalse(tuple(stage.glob("prd-*.md")))

    def test_current_specs_reference_declared_requirement_child_ids(self) -> None:
        requirements = _requirements_module()
        packages = requirements.load_requirement_packages(ROOT / "docs/01.requirements")
        declared = {item.identity for package in packages for item in package.items}
        spec_packages = importlib.import_module(
            "scripts.lib.document_governance.spec_packages"
        ).load_spec_packages(ROOT / "docs/03.specs")
        consumers = tuple(
            ROOT / package.spec.path
            for package in spec_packages
            if package.spec.status == "active"
        )
        referenced = {
            identity
            for path in consumers
            for identity in re.findall(
                r"REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4}",
                path.read_text(encoding="utf-8"),
            )
        }

        self.assertEqual([], sorted(referenced - declared))
        for path in consumers:
            self.assertFalse(
                requirements._contains_retired_requirement_reference(  # type: ignore[attr-defined]
                    path.read_text(encoding="utf-8")
                ),
                path,
            )

        retired_injections = (
            "prd-0001",
            "srs-0001",
            "ifr-0001",
            "interface-0001",
            "docs/01.requirements/prd-0001-example.md",
            "FR-0001",
            "NFR-0001",
            "IF-0001",
        )
        for injected in retired_injections:
            with self.subTest(injected=injected):
                self.assertTrue(
                    requirements._contains_retired_requirement_reference(  # type: ignore[attr-defined]
                        f"Current consumer accidentally references {injected}."
                    )
                )


if __name__ == "__main__":
    unittest.main()
