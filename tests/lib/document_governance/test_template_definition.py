from __future__ import annotations

import copy
import importlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator

from scripts.lib.document_governance.registry import (
    ROOT,
    RegistryError,
    _registry_from_document,
    load_registry,
    load_registry_document,
    validate_registry,
)
from scripts.lib.document_governance.template_definition import template_definition

SCHEMA_PATH = ROOT / "docs/99.templates/01.contracts/template-definition.schema.json"
GLOSSARY = ROOT / ".agents/knowledge/glossary.md"
LOCAL_GLOSSARY = ROOT / "docs/00.workspace/01.project/glossary.md"


class CommonDocumentContractTests(unittest.TestCase):
    def test_payload_and_language_readers_ignore_metadata_root_environment(
        self,
    ) -> None:
        program = """import sys
from scripts.lib.document_governance.common_document import compact_payload, payload_text, wrap_document
from scripts.lib.document_governance.language import language_mismatch
source = '# Example\\n\\n## Rules\\n\\nThis policy explains the actual rule and its full scope in English.\\n'
wrapped = wrap_document(source, kind='policy')
assert compact_payload(wrapped) == source
assert '## Rules' in payload_text(wrapped)
assert language_mismatch(wrapped, 'en') is None
assert 'scripts.lib.document_governance.metadata.profile' not in sys.modules
"""
        result = subprocess.run(
            [sys.executable, "-c", program],
            cwd=ROOT,
            env={**os.environ, "HYHOME_CI_GATE_ROOT": "/proc/self/fd/2147483647"},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_common_contract_load_is_stdlib_only_before_dependency_installation(
        self,
    ) -> None:
        program = """import sys
from scripts.lib.document_governance.common_document import load_contract
core = load_contract()
assert core['contract_id'] == 'WORKSPACE-DOCUMENT-CORE'
assert not {'yaml', 'markdown_it', 'jsonschema'} & sys.modules.keys()
assert isinstance(core['headings']['문서 개요'], tuple)
try:
    core['headings']['문서 개요'] = ()
except TypeError:
    pass
else:
    raise AssertionError('the JSON contract must be deeply immutable')
from scripts.lib.document_governance.common_document import _markdown_unfenced_lines
assert _markdown_unfenced_lines('# Actual\\n```md\\n# Example\\n```\\n') == ['# Actual']
assert not {'yaml', 'markdown_it', 'jsonschema'} & sys.modules.keys()
"""
        result = subprocess.run(
            [sys.executable, "-ES", "-c", program],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_existing_unfenced_reader_is_reexported_without_a_second_implementation(
        self,
    ) -> None:
        from scripts.lib.document_governance import common_document
        from scripts.lib.document_governance.metadata import heading

        self.assertIs(
            common_document._markdown_unfenced_lines, heading._markdown_unfenced_lines
        )
        self.assertIs(
            common_document._markdown_form_lines, heading._markdown_form_lines
        )

    def test_deep_encoding_keeps_annotations_out_of_actual_heading_titles(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            payload_text,
            wrap_document,
        )

        source = "# Sample\n\n## Rules\n\n##### Deep rule\n\n###### Deepest rule\n\nActual evidence.\n"
        wrapped = wrap_document(source, kind="policy")
        self.assertIn("###### Deep rule\n<!-- core-payload-level:5 -->\n", wrapped)
        self.assertIn("###### Deepest rule\n<!-- core-payload-level:6 -->\n", wrapped)
        for line in wrapped.splitlines():
            if line.startswith("#"):
                self.assertNotIn("core-payload-level", line)
        viewed = payload_text(wrapped)
        self.assertEqual(len(wrapped.splitlines()), len(viewed.splitlines()))
        for index, line in enumerate(wrapped.splitlines()):
            if re.fullmatch(r"<!-- core-payload-level:[456] -->", line):
                self.assertEqual("", viewed.splitlines()[index])
        evidence_line = wrapped.splitlines().index("Actual evidence.")
        self.assertEqual("Actual evidence.", viewed.splitlines()[evidence_line])
        self.assertEqual(source, compact_payload(wrapped))

    def test_only_structurally_associated_depth_annotations_are_removed(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            wrap_document,
        )

        source = (
            "# Sample\n\n## Rules\n\nA literal comment follows.\n"
            "<!-- core-payload-level:5 -->\n\n"
            "#### Actual fourth-level title\n<!-- core-payload-level:5 -->\n\n"
            "###### Actual deep title\n<!-- core-payload-level:5 -->\n\n"
            "```markdown\n###### Literal example\n<!-- core-payload-level:6 -->\n"
            "<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->\n\n\nLiteral spacing.\n```\n"
        )
        self.assertEqual(source, compact_payload(wrap_document(source, kind="policy")))

    def test_wrap_preserves_metadata_and_comment_preamble_above_h1(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            payload_text,
            wrap_document,
        )

        prefix = '---\ntitle: "Literal <!--"\ndescription: |\n  Metadata bytes remain.\n---\n\n'
        preamble = "<!-- Author prompt: Keep this preamble. -->\n<!-- Generated by a real producer. -->\n\n"
        source = (
            prefix + preamble + "# Sample\n\n## Rules\n\n```text\nOne.\n\n\nTwo.\n```\n"
        )
        wrapped = wrap_document(source, kind="policy")
        self.assertTrue(wrapped.startswith(prefix + preamble + "# Sample\n\n"))
        self.assertNotIn("\n\n\n# Sample", wrapped)
        self.assertTrue(
            payload_text(wrapped).startswith(prefix + preamble + "# Sample\n")
        )
        self.assertEqual(source, compact_payload(wrapped))

    def test_common_contract_rejects_duplicate_json_meanings(self) -> None:
        from scripts.lib.document_governance.common_document import (
            CORE_PATH,
            CommonDocumentError,
            load_contract,
        )

        original = (ROOT / CORE_PATH).read_text(encoding="utf-8")
        duplicated = original.replace(
            '"version": "1.0.0"', '"version": "0.9.0", "version": "1.0.0"', 1
        )
        self.assertNotEqual(original, duplicated)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / CORE_PATH
            source.parent.mkdir(parents=True)
            source.write_text(duplicated, encoding="utf-8")
            with self.assertRaises(CommonDocumentError):
                load_contract(root=root)

    def test_structural_marker_inside_fenced_payload_is_preserved(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            wrap_document,
        )

        marker = "<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->"
        source = "# Example\n\n## Rules\n\n```markdown\n" + marker + "\n```\n"
        wrapped = wrap_document(source, kind="policy")
        self.assertEqual(source, compact_payload(wrapped))
        with_metadata = "---\ndescription: |\n  " + marker + "\n---\n\n" + source
        self.assertEqual(
            with_metadata, compact_payload(wrap_document(with_metadata, kind="policy"))
        )

    def test_current_normative_source_cannot_drop_envelope_and_scope(self) -> None:
        import dataclasses

        from scripts.lib.document_governance.common_document import compact_payload
        from scripts.lib.document_governance.metadata.heading import (
            validate_body_contract,
        )
        from scripts.lib.document_governance.metadata.lifecycle import (
            _record_from_text,
            validate_record,
        )
        from scripts.lib.document_governance.metadata.profile import (
            build_registry_profiles,
        )
        from scripts.lib.document_governance.registry import classify_path

        profiles = build_registry_profiles(load_registry())
        path = pathlib.Path(".agents/governance/bootstrap.md")
        source = compact_payload((ROOT / path).read_text())
        source = re.sub(r"(?m)^document_scope:\n(?:  .*\n)+", "", source)
        record = dataclasses.replace(
            _record_from_text(path, source),
            artifact_type=classify_path(path.as_posix(), load_registry()),
        )
        self.assertIn(
            "missing-required-key",
            {item.code for item in validate_record(record, profiles, {})},
        )
        codes = {
            item.code for item in validate_body_contract(record, source, profiles, True)
        }
        self.assertIn("common-envelope-missing", codes)

    def test_formal_contract_is_bound_by_identity_version_and_content(self) -> None:
        import hashlib

        registry = load_registry()
        binding = registry.common["document_core"]
        source = ROOT / binding["source_path"]
        core = json.loads(source.read_text(encoding="utf-8"))
        self.assertEqual("WORKSPACE-DOCUMENT-CORE", core["contract_id"])
        self.assertEqual(core["contract_id"], binding["contract_id"])
        self.assertEqual(core["version"], binding["contract_version"])
        self.assertEqual(
            hashlib.sha256(source.read_bytes()).hexdigest(), binding["source_sha256"]
        )

    def test_envelope_keeps_role_payload_and_rejects_a_missing_outer_section(
        self,
    ) -> None:
        from scripts.lib.document_governance.common_document import (
            CommonDocumentError,
            load_contract,
            payload_text,
            wrap_document,
        )

        original = "# Sample\n\n## Rules\n\n### Boundary\n\nOne actual rule.\n"
        wrapped = wrap_document(original, kind="policy")
        for title, children in load_contract()["headings"].items():
            self.assertIn(f"## {title}\n", wrapped)
            for child in children:
                self.assertIn(f"### {child}\n", wrapped)
        viewed = payload_text(wrapped)
        self.assertIn("## Rules\n", viewed)
        self.assertIn("### Boundary\n", viewed)
        self.assertIn("One actual rule.", viewed)
        broken = wrapped.replace("## 적용과 확인\n", "", 1)
        with self.assertRaises(CommonDocumentError):
            payload_text(broken)

    def test_task_implementation_state_cannot_supply_normative_active(self) -> None:
        from scripts.lib.document_governance.common_document import (
            CommonDocumentError,
            common_metadata,
        )

        path = "docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0102-p04-templates.md"
        metadata = {
            "title": "A completed execution",
            "version": "1.0.0",
            "type": "sdlc/task",
            "status": "completed",
            "owner": "@buenhyden",
            "document_scope": {"subject": "document governance", "layer": "workspace"},
        }
        with self.assertRaises(CommonDocumentError):
            common_metadata(load_registry(), path, metadata)
        actual = common_metadata(
            load_registry(), path, {**metadata, "document_lifecycle": "draft"}
        )
        self.assertEqual("draft", actual["lifecycle"])
        self.assertEqual("task", actual["kind"])

    def test_every_definition_has_common_outer_and_a_typed_payload(self) -> None:
        from scripts.lib.document_governance.common_document import load_contract

        registry = load_registry()
        expected = load_contract()["headings"]
        for template_id in registry.template_roles:
            with self.subTest(template=template_id):
                definition = template_definition(registry, template_id)
                self.assertEqual(
                    list(expected), [h["title"] for h in definition["headings"]]
                )
                self.assertIn(
                    definition["payload"]["kind"], load_contract()["payload_profiles"]
                )
                self.assertTrue(definition["payload"]["headings"])

    def test_payload_roundtrip_preserves_deep_headings_fences_and_source_lines(
        self,
    ) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            payload_text,
            wrap_document,
        )

        original = (
            '---\ntitle: "Literal <!--"\n---\n\n# Sample\n\n'
            "## Rules\n\n### Boundary\n\n#### Detail\n\n"
            "##### Deep rule\n\n###### Deepest rule\n\nActual evidence.\n\n"
            "```md\n## Example\n###### Example depth\n```\n"
        )
        wrapped = wrap_document(original, kind="policy")
        self.assertEqual(wrapped, wrap_document(wrapped, kind="policy"))
        viewed = payload_text(wrapped)
        self.assertEqual(len(wrapped.splitlines()), len(viewed.splitlines()))
        evidence_line = wrapped.splitlines().index("Actual evidence.")
        self.assertEqual("Actual evidence.", viewed.splitlines()[evidence_line])
        self.assertIn("##### Deep rule\n", viewed)
        self.assertIn("###### Deepest rule\n", viewed)
        self.assertIn("```md\n## Example\n###### Example depth\n```", viewed)
        self.assertEqual(
            [line for line in original.splitlines() if line],
            [line for line in compact_payload(wrapped).splitlines() if line],
        )
        self.assertEqual(original, payload_text(original))

    def test_common_metadata_refuses_invented_lifecycle_scope_and_numeric_versions(
        self,
    ) -> None:
        from scripts.lib.document_governance.common_document import (
            CommonDocumentError,
            common_metadata,
        )

        registry = load_registry()
        path = "docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0102-p04-templates.md"
        valid = {
            "title": "Task",
            "version": "1.0.0",
            "owner": "@buenhyden",
            "status": "completed",
            "document_lifecycle": "draft",
            "document_scope": {"subject": "document governance", "layer": "workspace"},
        }
        self.assertEqual("draft", common_metadata(registry, path, valid)["lifecycle"])
        for changes in (
            {"title": ""},
            {"owner": None},
            {"version": "1.0.0-rc.1"},
            {"version": "01.0.0"},
            {"document_lifecycle": "completed"},
            {"document_scope": {"subject": "", "layer": "workspace"}},
            {"document_scope": {"subject": "Task", "layer": "application"}},
            {
                "document_scope": {
                    "subject": "Task",
                    "layer": "workspace",
                    "extra": "value",
                }
            },
        ):
            with self.subTest(changes=changes), self.assertRaises(CommonDocumentError):
                common_metadata(registry, path, {**valid, **changes})


def _errors(definition: object) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return sorted(
        "/".join(map(str, error.absolute_path)) + ": " + error.validator
        for error in validator.iter_errors(definition)
    )


def _slug(value: str) -> str:
    text = re.sub(r"[`*_~]", "", value.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"[ -]+", "-", text).strip("-")


def _reference_failures(definition: dict) -> list[str]:
    """Return every authored reference that does not resolve."""

    failures = []
    glossary = GLOSSARY.read_text(encoding="utf-8") + LOCAL_GLOSSARY.read_text(
        encoding="utf-8"
    )
    for path in definition["consumer_paths"]:
        if not (ROOT / path).is_file():
            failures.append(path)
    for ref in definition["policy_refs"]:
        path, _, anchor = ref.partition("#")
        target = ROOT / path
        if (
            not re.fullmatch(
                r"(?:\.agents/governance|docs/00\.workspace/(?:01\.project|03\.process|04\.quality))/[a-z-]+\.md",
                path,
            )
            or not target.is_file()
        ):
            failures.append(ref)
            continue
        text = target.read_text(encoding="utf-8")
        if anchor not in {_slug(h) for h in re.findall(r"^#{1,6} +(.+)$", text, re.M)}:
            failures.append(ref)
    for term in definition["vocabulary_refs"]:
        if f"| {term.removeprefix('local:')} |" not in glossary:
            failures.append(term)
    for kind in ("positive", "negative", "regression"):
        for name in definition["validation"][kind]:
            if name.startswith("scripts/"):
                if not (ROOT / name.split()[0]).is_file():
                    failures.append(name)
                continue
            module, _, attribute = name.partition(":")
            try:
                loaded = importlib.import_module(module)
                for part in filter(None, attribute.split(".")):
                    loaded = getattr(loaded, part)
            except (ImportError, AttributeError):
                failures.append(name)
    return failures


def _template_headings(text: str) -> list[tuple[int, str]]:
    from scripts.lib.document_governance.metadata.heading import (
        _HEADING_LINE,
        _markdown_unfenced_lines,
    )

    found = []
    for line in _markdown_unfenced_lines(text):
        match = _HEADING_LINE.match(line)
        if match and len(match.group(1)) in (2, 3):
            found.append((len(match.group(1)), match.group(2)))
    return found


class TemplateDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()
        cls.definitions = {
            role: template_definition(cls.registry, role)
            for role in cls.registry.template_roles
        }

    def _profile(self, role: str):
        return self.registry.profiles[self.registry.template_roles[role]["profiles"][0]]

    def test_schema_rejects_a_combined_contract_version(self) -> None:
        definition = dict(self.definitions["sdlc/task"])
        definition["contract_version"] = "COMMON-DOC-FORM-1/1.0.0"
        del definition["contract_id"]
        errors = _errors(definition)
        self.assertIn(": required", errors)
        self.assertIn("contract_version: pattern", errors)

    def test_every_definition_validates_against_the_schema(self) -> None:
        Draft202012Validator.check_schema(
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        )
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                self.assertEqual([], _errors(definition))

    def test_section_ids_are_unique(self) -> None:
        for role, definition in self.definitions.items():
            headings = [*definition["headings"], *definition["payload"]["headings"]]
            ids = [h["section_id"] for h in headings] + [
                c["section_id"] for h in headings for c in h["children"]
            ]
            with self.subTest(role=role):
                self.assertEqual(len(ids), len(set(ids)))

    def test_headings_equal_the_profile_sections(self) -> None:
        for role, definition in self.definitions.items():
            profile = self._profile(role)
            if not (
                profile.get("required_sections") or profile.get("optional_sections")
            ):
                continue
            with self.subTest(role=role):
                self.assertEqual(
                    [
                        *profile.get("required_sections", ()),
                        *profile.get("optional_sections", ()),
                    ],
                    [heading["title"] for heading in definition["payload"]["headings"]],
                )
                for heading in definition["payload"]["headings"]:
                    title = heading["title"]
                    # Order is the template's; see the declared-order test.
                    self.assertCountEqual(
                        [
                            *profile.get("required_subsections", {}).get(title, ()),
                            *profile.get("optional_subsections", {}).get(title, ()),
                        ],
                        [child["title"] for child in heading["children"]],
                    )

    def test_headings_match_the_template_file(self) -> None:
        from scripts.lib.document_governance.common_document import template_payload

        for role, definition in self.definitions.items():
            source = self.registry.template_roles[role]["source"]
            if not source.endswith(".md") or not self._profile(role).get(
                "required_sections"
            ):
                continue
            text = (ROOT / source).read_text(encoding="utf-8")
            found = _template_headings(template_payload(self.registry, role))
            h2 = [title for level, title in found if level == 2]
            with self.subTest(role=role):
                self.assertEqual(
                    [
                        (item["level"], item["title"])
                        for heading in definition["headings"]
                        for item in (heading, *heading["children"])
                    ],
                    _template_headings(text),
                )
                payload_headings = definition["payload"]["headings"]
                derived = [h["title"] for h in payload_headings]
                required = [
                    h["title"]
                    for h in payload_headings
                    if h["requiredness"] == "required"
                ]
                # The template shows every required H2 in order; any other
                # H2 it shows is a registered optional section.
                self.assertEqual(required, [t for t in h2 if t in required])
                self.assertLessEqual(set(h2), set(derived))
                if self._profile(role).get("required_subsections"):
                    h3 = [title for level, title in found if level == 3]
                    children = [c for h in payload_headings for c in h["children"]]
                    required_children = [
                        c["title"] for c in children if c["requiredness"] == "required"
                    ]
                    # The validator orders required subsections only; an
                    # optional one may sit anywhere under its parent.
                    self.assertEqual(
                        required_children, [t for t in h3 if t in required_children]
                    )
                    self.assertLessEqual(set(h3), {c["title"] for c in children})

    def test_conditional_subsections_carry_the_contract_condition(self) -> None:
        # COMMON-DOC-FORM-1 1.0.0 marked the requirement Quality Requirements
        # and the ADR Supersession H3s conditional; both roles moved to the
        # role design core, where every H3 is required, so none is left.
        expected: dict[tuple[str, str], str] = {}
        found = {}
        for role, definition in self.definitions.items():
            for heading in definition["payload"]["headings"]:
                for child in heading["children"]:
                    if child["requiredness"] != "required":
                        found[(role, child["title"])] = (
                            child["requiredness"],
                            child["condition"],
                            child["empty_policy"],
                        )
        self.assertEqual(
            {
                key: ("conditional", text, "omit_when_condition_false")
                for key, text in expected.items()
            },
            found,
        )

    def test_subsections_keep_the_declared_order(self) -> None:
        recovery = next(
            h
            for h in self.definitions["operation/runbook"]["payload"]["headings"]
            if h["title"] == "Escalation"
        )
        self.assertEqual(
            [("Next Owner", 1), ("Recovery or Forward Repair", 2)],
            [(c["title"], c["order"]) for c in recovery["children"]],
        )
        for role, definition in self.definitions.items():
            if not self._profile(role).get("required_subsections"):
                continue
            from scripts.lib.document_governance.common_document import template_payload

            found = _template_headings(template_payload(self.registry, role))
            h3 = [title for level, title in found if level == 3]
            with self.subTest(role=role):
                children = [
                    c["title"]
                    for h in definition["payload"]["headings"]
                    for c in h["children"]
                ]
                self.assertEqual([t for t in h3 if t in children], children)

    def test_prohibited_content_keys_name_template_roles(self) -> None:
        # A misspelled key would otherwise be ignored silently.
        keys = set(self.registry.common["section_prohibited_content"])
        self.assertLessEqual(keys, set(self.registry.template_roles))

    def test_sections_carry_their_role_prohibited_content(self) -> None:
        # COMMON-DOC-FORM-1 1.0.0: an H2 carries the role rule and one empty
        # rule that includes a guidance-comment-only body; an H3 carries the
        # role rule and the stand-in rule, and no empty rule.
        role_rule = {
            "sdlc/requirement": "Implementation detail or Task status, which "
            "the Requirement does not own.",
            "operation/runbook": "Procedure guidance presented as execution "
            "approval, or a stored secret value.",
            "governance/policy": "A rule weakened to suit a test.",
        }
        stand_in = (
            "A same-named heading inside a code fence, quote or comment "
            "standing in for the real section."
        )
        empty = (
            "A heading with no body, or a body that is only an unexplained "
            "TODO, TBD, N/A, - or a template guidance comment."
        )
        for role, definition in self.definitions.items():
            if not self._profile(role).get("required_subsections"):
                continue
            with self.subTest(role=role):
                for heading in definition["payload"]["headings"]:
                    rules = heading["prohibited_content"]
                    self.assertEqual(2, len(rules), heading["title"])
                    self.assertEqual(empty, rules[1])
                    if role in role_rule:
                        self.assertEqual(role_rule[role], rules[0])
                    for child in heading["children"]:
                        self.assertEqual(
                            [rules[0], stand_in], child["prohibited_content"]
                        )

    def test_headingless_templates_use_their_real_top_level_units(self) -> None:
        expected = {
            "sdlc/openapi": ["openapi", "info", "paths", "components"],
            "sdlc/graphql": ["schema", "type Query", "type __OBJECT_TYPE__"],
            "sdlc/proto": [
                'syntax = "proto3"',
                "package __PACKAGE_NAME__",
                "service __SERVICE_NAME__",
                "message HealthRequest",
                "message HealthResponse",
            ],
            "governance/codex-agent": [
                "name",
                "description",
                "developer_instructions",
                "model",
                "model_reasoning_effort",
                "sandbox_mode",
            ],
            "governance/claude-agent": [
                "frontmatter name",
                "frontmatter description",
                "frontmatter tools",
                "frontmatter model",
                "frontmatter effort",
                "frontmatter permissionMode",
                "frontmatter skills",
                "Generated-by marker comment",
                "Body {{AGENT_BODY}}",
            ],
        }
        for role, titles in expected.items():
            with self.subTest(role=role):
                self.assertEqual(
                    titles,
                    [h["title"] for h in self.definitions[role]["payload"]["headings"]],
                )
        proto = {
            h["title"]: h["requiredness"]
            for h in self.definitions["sdlc/proto"]["payload"]["headings"]
        }
        self.assertEqual("conditional", proto["message HealthRequest"])
        self.assertEqual("required", proto["service __SERVICE_NAME__"])
        codex = self.definitions["governance/codex-agent"]
        self.assertEqual(
            expected["governance/codex-agent"], [m["name"] for m in codex["metadata"]]
        )

    def test_a_codex_projection_carries_only_the_rendered_keys(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        profile = self.registry.profiles["runtime-projection-codex"]
        rendered = {
            m["name"] for m in self.definitions["governance/codex-agent"]["metadata"]
        }
        self.assertLessEqual(
            {*profile["required_frontmatter"], *profile["optional_frontmatter"]},
            rendered,
        )
        projection = (ROOT / ".codex/agents/doc-writer.toml").read_bytes()
        self.assertTrue(renderer._is_codex_agent_projection(projection))
        self.assertFalse(
            renderer._is_codex_agent_projection(
                projection + b'permissionMode = "plan"\n'
            )
        )

    def test_a_claude_projection_carries_only_the_rendered_keys(self) -> None:
        from scripts.lib.document_governance.frontmatter import parse_frontmatter_text
        from scripts.lib.document_governance.metadata.heading import (
            _markdown_form_lines,
        )
        from scripts.operations import provider_surface_renderer as renderer

        expected = {
            path.as_posix(): content
            for path, content in renderer.expected_projection(ROOT, "claude").items()
            if path.as_posix().startswith(".claude/agents/")
        }
        self.assertTrue(expected)
        written: set[str] = set()
        for content in expected.values():
            text = content.decode("utf-8")
            written |= set(parse_frontmatter_text(text))
            # AGENT_BODY owns the canonical role H1; the native envelope
            # must not duplicate it or omit the only actual title.
            self.assertEqual(
                1,
                sum(
                    heading is not None and heading[0] == 1
                    for _, _, heading in _markdown_form_lines(text)
                ),
            )
        self.assertTrue({"model_reasoning_effort", "version"}.isdisjoint(written))
        profile = self.registry.profiles["runtime-projection-claude"]
        self.assertLessEqual(
            {*profile["required_frontmatter"], *profile["optional_frontmatter"]},
            written,
        )
        # The renderer --check compares each tracked projection with these
        # bytes, so a projection carrying a Codex-only key is drift.
        path = ".claude/agents/doc-writer.md"
        self.assertEqual(expected[path], (ROOT / path).read_bytes())
        tampered = expected[path].replace(
            b"\n---\n", b'\nmodel_reasoning_effort: "high"\n---\n', 1
        )
        self.assertIn(b"model_reasoning_effort", tampered)
        self.assertNotEqual(expected[path], tampered)

    def test_authored_references_resolve(self) -> None:
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                self.assertEqual([], _reference_failures(definition))

    def test_dangling_authored_references_are_reported(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/task"])
        definition["consumer_paths"] = ["scripts/does-not-exist.py"]
        definition["policy_refs"] = [
            "docs/00.workspace/03.process/sdlc.md#no-such-anchor"
        ]
        definition["vocabulary_refs"] = ["TERM-NOT-A-TERM"]
        definition["validation"]["positive"] = [
            "tests.lib.document_governance.test_registry:NoSuchTests"
        ]
        self.assertEqual(4, len(_reference_failures(definition)))

    def test_a_missing_required_field_is_rejected(self) -> None:
        for role, definition in self.definitions.items():
            changed = copy.deepcopy(definition)
            del changed["purpose"]
            with self.subTest(role=role):
                self.assertIn(": required", _errors(changed))

    def test_empty_headings_are_rejected(self) -> None:
        for role, definition in self.definitions.items():
            changed = copy.deepcopy(definition)
            changed["headings"] = []
            with self.subTest(role=role):
                self.assertIn("headings: minItems", _errors(changed))

    def test_a_release_role_is_rejected(self) -> None:
        for role in ("Release", "release", "operations/release"):
            definition = copy.deepcopy(self.definitions["sdlc/task"])
            definition["role"] = role
            with self.subTest(role=role):
                self.assertIn("role: not", _errors(definition))

    def test_an_unknown_key_is_rejected(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/task"])
        definition["owner"] = "@someone"
        self.assertIn(": additionalProperties", _errors(definition))
        raw = copy.deepcopy(dict(load_registry_document()))
        raw["template_roles"]["sdlc/task"]["owner"] = "@someone"
        findings = validate_registry(raw)
        self.assertIn(
            ("schema-invalid", "template_roles.sdlc/task"),
            {(finding.code, finding.path) for finding in findings},
        )

    def test_a_duplicate_key_is_rejected(self) -> None:
        text = (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        duplicated = text.replace(
            '"purpose": ', '"purpose": "first",\n      "purpose": ', 1
        )
        self.assertNotEqual(text, duplicated)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "registry.json"
            path.write_text(duplicated, encoding="utf-8")
            with self.assertRaisesRegex(RegistryError, "duplicate JSON member"):
                load_registry_document(path)

    def test_a_missing_dictionary_entry_is_rejected(self) -> None:
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["frontmatter_key_definitions"]["artifact_id"]
        del raw["common"]["table_column_definitions"]["Resolves"]
        codes = {(f.code, f.message) for f in validate_registry(raw)}
        self.assertIn(("template-key-undefined", "artifact_id"), codes)
        self.assertIn(("template-column-undefined", "Resolves"), codes)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "registry.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(
                RegistryError, "template-(key|column)-undefined"
            ):
                load_registry(path)
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["table_column_definitions"]["Definition"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        # An unbound (domain) role reads its columns from the dictionary.
        with self.assertRaisesRegex(RegistryError, "Definition"):
            template_definition(registry, "governance/vocabulary")

    def _common_form_roles(self, registry) -> list[str]:
        return [
            role
            for role, entry in registry.template_roles.items()
            if registry.profiles[entry["profiles"][0]].get("required_subsections")
            and not entry.get("core_role")
        ]

    def test_the_common_form_revision_is_read_from_the_registry(self) -> None:
        """H-W01-2: the consumer reads the adopted revision, not a constant."""

        pinned = self.registry.common["common_form_contract"]
        roles = self._common_form_roles(self.registry)
        self.assertTrue(roles)
        for role in roles:
            self.assertEqual(
                pinned["contract_id"], self.definitions[role]["payload"]["contract_id"]
            )
            self.assertEqual(
                pinned["contract_version"],
                self.definitions[role]["payload"]["contract_version"],
            )
        raw = copy.deepcopy(dict(load_registry_document()))
        raw["common"]["common_form_contract"]["contract_version"] = "9.9.9"
        moved = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        for role in roles:
            with self.subTest(role=role):
                self.assertEqual(
                    "9.9.9",
                    template_definition(moved, role)["payload"]["contract_version"],
                )
        legacy = next(
            role
            for role, entry in moved.template_roles.items()
            if role not in set(roles) and not entry.get("core_role")
        )
        self.assertEqual(
            moved.common["contract_id"],
            template_definition(moved, legacy)["payload"]["contract_id"],
        )
        self.assertEqual(
            moved.common["contract_version"],
            template_definition(moved, legacy)["payload"]["contract_version"],
        )

    def test_template_outline_ignores_commented_headings_and_tables(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        guidance, tables = _template_outline(
            "## Parent\n\n### Child\n\nWrite the reason.\n\n"
            "<!-- An example\n## Fake\n| False header |\n-->\n\n"
            "Write the result.\n"
        )
        self.assertEqual(
            {
                ("Parent", None): "",
                ("Parent", "Child"): "Write the reason. Write the result.",
            },
            guidance,
        )
        self.assertEqual([], tables)

    def test_template_outline_ignores_list_nested_tables(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        _, tables = _template_outline(
            "## Parent\n\n- Example\n\n  | False | Header |\n"
            "  | --- | --- |\n  | a | b |\n\n"
            "| Real | Header |\n| --- | --- |\n| c | d |\n"
        )
        self.assertEqual([("Parent", None, "| Real | Header |")], tables)

    def test_template_outline_refuses_an_invalid_table_delimiter(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        for rows in ("", "| :--- |\n", "| --- | invalid |\n", "| \u00a0--- | --- |\n"):
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(RegistryError, "table delimiter"):
                    _template_outline(f"## Parent\n\n| Left | Right |\n{rows}")

    def test_template_outline_accepts_delimiter_without_outer_pipes(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        guidance, tables = _template_outline(
            "## Parent\n\n| Left | Right |\n:--- | ---:\n| a | b |\n"
        )
        self.assertEqual({("Parent", None): ""}, guidance)
        self.assertEqual([("Parent", None, "| Left | Right |")], tables)

    def test_a_registry_without_the_pin_fails_for_a_common_form_role(self) -> None:
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["common_form_contract"]
        self.assertIn("schema-invalid", {f.code for f in validate_registry(raw)})
        bare = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        role = self._common_form_roles(bare)[0]
        with self.assertRaisesRegex(RegistryError, "common_form_contract"):
            template_definition(bare, role)

    def test_a_malformed_common_form_pin_is_rejected(self) -> None:
        for value in (
            "1.0.0",
            "COMMON-DOC-FORM-1",
            "COMMON-DOC-FORM-1/1.0",
            "COMMON-DOC-FORM-1 1.0.0",
            1,
            {"contract_id": "COMMON-DOC-FORM-1", "contract_version": "1.0.0\n"},
            {"contract_id": "COMMON-DOC-FORM-1", "contract_version": "1.0.0-rc.1"},
        ):
            raw = copy.deepcopy(dict(load_registry_document()))
            raw["common"]["common_form_contract"] = value
            with self.subTest(value=value):
                self.assertIn(
                    "schema-invalid", {f.code for f in validate_registry(raw)}
                )

    def test_unknown_role_and_missing_field_raise_registry_error(self) -> None:
        with self.assertRaises(RegistryError):
            template_definition(self.registry, "operations/release")
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["template_roles"]["sdlc/task"]["purpose"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        with self.assertRaisesRegex(RegistryError, "purpose"):
            template_definition(registry, "sdlc/task")


def _core_from(definition: dict) -> dict:
    """Build a core role with the exact structure of one projection."""

    def required(item: dict) -> str:
        return "always" if item["requiredness"] == "required" else "when applicable"

    sections = []
    for h2 in definition["payload"]["headings"]:
        subsections = [
            {
                "section_id": h3["section_id"],
                "title_en": h3["title"],
                "required_when": required(h3),
            }
            for h3 in h2["children"]
        ]
        sections.append(
            {
                "section_id": h2["section_id"],
                "title_en": h2["title"],
                "required_when": required(h2),
                "subsections": subsections,
            }
        )
    tables = [
        {
            "table_id": table["name"],
            "section_id": table["section"],
            "columns": [
                {"label": column["key"], "required": column["required"]}
                for column in table["columns"]
            ],
        }
        for table in definition["tables"]
    ]
    return {"role": "fixture", "sections": sections, "tables": tables}


def _pending_role(raw: dict) -> str:
    """A pending-migration template role whose core target no other role names,
    so the fixtures below can change its exception. Once every role is bound,
    the first such bound role is turned back into a pending one in this copy of
    the Registry only."""

    roles = raw["template_roles"]
    targets = [
        role.get("core_role") or role.get("core_exception", {}).get("core_role")
        for role in roles.values()
    ]
    unique = [
        template_id
        for template_id, role in sorted(roles.items())
        if targets.count(
            role.get("core_role") or role.get("core_exception", {}).get("core_role")
        )
        == 1
    ]
    for template_id in unique:
        if roles[template_id].get("core_exception", {}).get("kind") == (
            "pending-migration"
        ):
            return template_id
    template_id = next(
        template_id for template_id in unique if roles[template_id].get("core_role")
    )
    role = roles[template_id]
    role["core_exception"] = {
        "kind": "pending-migration",
        "reason": "Fixture: a bound role returned to pending for this test",
        "core_role": role.pop("core_role"),
    }
    return template_id


class RoleDesignConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_findings,
        )

        cls.findings = staticmethod(role_design_findings)
        cls.registry = load_registry()
        cls.task = template_definition(cls.registry, "sdlc/task")

    def _codes(self, core_role: dict, definition: dict) -> set[str]:
        return {
            code
            for code, _, _ in self.findings(
                {"fixture": core_role},
                {"sdlc/task": "fixture"},
                {"sdlc/task": definition},
            )
        }

    def test_an_identical_projection_conforms(self) -> None:
        self.assertEqual(set(), self._codes(_core_from(self.task), self.task))

    def test_same_titles_with_a_different_table_do_not_conform(self) -> None:
        core = _core_from(self.task)
        core["tables"][0]["columns"][3]["label"] = "Method"
        self.assertIn("role-design-table-mismatch", self._codes(core, self.task))

    def test_a_different_subsection_does_not_conform(self) -> None:
        core = _core_from(self.task)
        core["sections"][0]["subsections"][0]["title_en"] = "Problem"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def test_requiredness_is_part_of_the_core(self) -> None:
        core = _core_from(self.task)
        core["sections"][1]["required_when"] = "when applicable"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def test_a_table_may_sit_in_an_h3_of_its_core_owned_h2(self) -> None:
        core = _core_from(self.task)
        owner = next(
            h2["section_id"]
            for h2 in self.task["payload"]["headings"]
            if any(
                h3["section_id"] == self.task["tables"][0]["section"]
                for h3 in h2["children"]
            )
        )
        core["tables"][0]["section_id"] = owner
        self.assertEqual(set(), self._codes(core, self.task))

    def test_an_extra_or_missing_table_does_not_conform(self) -> None:
        extra = _core_from(self.task)
        extra["tables"].append(copy.deepcopy(extra["tables"][0]))
        missing = _core_from(self.task)
        missing["tables"].pop()
        for core in (extra, missing):
            with self.subTest(tables=len(core["tables"])):
                self.assertIn(
                    "role-design-table-mismatch", self._codes(core, self.task)
                )

    def test_h3_requiredness_is_part_of_the_core(self) -> None:
        core = _core_from(self.task)
        core["sections"][0]["subsections"][0]["required_when"] = "when applicable"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def _registry_with(self, edit) -> object:
        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        edit(raw)
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "registry.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            return load_registry(path)

    def test_an_unknown_or_unmapped_core_role_is_reported(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        def rename(raw: dict) -> None:
            exception = raw["template_roles"][_pending_role(raw)]["core_exception"]
            exception["core_role"] = "no-such-role"

        codes = {
            code
            for code, _, _ in role_design_contract_findings(self._registry_with(rename))
        }
        self.assertEqual(
            {"role-design-unknown-role", "role-design-core-unmapped"}, codes
        )

    def test_the_schema_owns_the_exception_shape(self) -> None:
        from scripts.lib.document_governance.registry import validate_registry

        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        cases = {
            "pending without a core role": lambda role: role["core_exception"].pop(
                "core_role"
            ),
            "domain with a core role": lambda role: role["core_exception"].update(
                kind="domain"
            ),
            "both fields": lambda role: role.update(core_role="decision"),
            "neither field": lambda role: role.pop("core_exception"),
        }
        for name, edit in cases.items():
            with self.subTest(case=name):
                changed = copy.deepcopy(raw)
                edit(changed["template_roles"][_pending_role(changed)])
                self.assertIn(
                    "schema-invalid",
                    {finding.code for finding in validate_registry(changed)},
                )

    def test_a_different_core_identity_is_rejected(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        def bump(raw: dict) -> None:
            raw["common"]["role_design_contract"]["contract_version"] = "4.0.1"

        codes = {
            code
            for code, _, _ in role_design_contract_findings(self._registry_with(bump))
        }
        self.assertEqual({"role-design-identity"}, codes)

    def test_the_incident_and_postmortem_forms_are_bound_and_conform(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        bound = {
            template_id: role.get("core_role")
            for template_id, role in self.registry.template_roles.items()
            if role.get("core_role")
        }
        self.assertEqual("incident", bound.get("operation/incident"))
        self.assertEqual("postmortem", bound.get("operation/postmortem"))
        self.assertEqual("runbook", bound.get("operation/runbook"))
        self.assertEqual("guide", bound.get("operation/guide"))
        self.assertEqual("policy", bound.get("operation/policy"))
        self.assertEqual("policy", bound.get("governance/policy"))
        self.assertEqual("research", bound.get("reference/research"))
        self.assertEqual("audit", bound.get("reference/audit"))
        self.assertEqual("data-reference", bound.get("reference/data"))
        self.assertEqual("agent-instructions", bound.get("common/agent-guide"))
        self.assertEqual("skill", bound.get("governance/skill"))
        self.assertEqual("requirement", bound.get("sdlc/requirement"))
        self.assertEqual("architecture", bound.get("sdlc/architecture-description"))
        self.assertEqual("decision", bound.get("sdlc/architecture-decision"))
        for template_id, core_role in (
            ("common/readme", "stage-readme"),
            ("common/documentation-readme", "stage-readme"),
            ("reference/category-readme", "stage-readme"),
            ("reference/research-pack", "stage-readme"),
            ("reference/audit-pack", "stage-readme"),
            ("reference/data-pack", "stage-readme"),
            ("common/package-readme", "service-readme"),
            ("common/repository-readme", "root-readme"),
            ("common/runtime-governance-readme", "root-readme"),
            ("common/incident-year-readme", "stage-readme"),
            ("governance/knowledge-index", "stage-readme"),
            ("governance/prompt-index", "stage-readme"),
            ("governance/provider-index", "stage-readme"),
        ):
            self.assertEqual(core_role, bound.get(template_id), template_id)
        self.assertEqual("spec", bound.get("sdlc/spec"))
        self.assertEqual("plan", bound.get("sdlc/plan"))
        self.assertEqual("task", bound.get("sdlc/task"))
        self.assertEqual([], role_design_contract_findings(self.registry))

    def test_a_runbook_steps_table_reads_the_core_columns(self) -> None:
        definition = template_definition(self.registry, "operation/runbook")
        self.assertEqual(
            "workspace-document-role-design", definition["payload"]["contract_id"]
        )
        self.assertEqual(
            [
                ("Step", "integer"),
                ("Action", "string"),
                ("Expected Result", "string"),
                ("On Failure", "string"),
            ],
            [
                (column["key"], column["data_type"])
                for column in definition["tables"][0]["columns"]
            ],
        )

    def test_a_bound_table_reads_its_columns_from_the_core(self) -> None:
        definition = template_definition(self.registry, "operation/postmortem")
        self.assertEqual(
            "workspace-document-role-design", definition["payload"]["contract_id"]
        )
        self.assertEqual(
            [
                ("Action", "string"),
                ("Owner", "string"),
                ("Condition", "string"),
                ("Evidence", "reference-or-none"),
            ],
            [
                (column["key"], column["data_type"])
                for column in definition["tables"][0]["columns"]
            ],
        )

    def test_a_core_table_under_another_h2_is_rejected(self) -> None:
        from scripts.lib.document_governance.common_document import (
            compact_payload,
            wrap_document,
        )

        role = self.registry.template_roles["operation/postmortem"]
        contract = self.registry.common["role_design_contract"]
        source = ROOT / str(role["source"])
        text = source.read_text(encoding="utf-8")
        table = "\n".join(line for line in text.split("\n") if line.startswith("|"))
        moved = (
            compact_payload(text)
            .replace(table + "\n", "")
            .replace(
                "### Contributing Factors\n",
                "### Contributing Factors\n\n" + table + "\n",
                1,
            )
        )
        moved = wrap_document(moved, kind="postmortem")
        self.assertNotEqual(text, moved)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for relative in (
                str(contract["source_path"]),
                str(role["source"]),
                "docs/99.templates/01.contracts/document-frontmatter.schema.json",
                "docs/99.templates/01.contracts/common-document-contract.json",
            ):
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).write_bytes((ROOT / relative).read_bytes())
            (root / str(role["source"])).write_text(moved, encoding="utf-8")
            with self.assertRaisesRegex(RegistryError, "not in the core role"):
                template_definition(self.registry, "operation/postmortem", root=root)

    def test_the_registry_pins_the_tracked_core(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        contract = self.registry.common["role_design_contract"]
        self.assertEqual("workspace-document-role-design", contract["contract_id"])
        self.assertEqual([], role_design_contract_findings(self.registry))

    def test_a_changed_core_or_schema_file_is_rejected(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        contract = self.registry.common["role_design_contract"]
        for changed in ("source_path", "schema_path"):
            with (
                self.subTest(changed=changed),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                for key in ("source_path", "schema_path"):
                    target = root / contract[key]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes((ROOT / contract[key]).read_bytes())
                target = root / contract[changed]
                target.write_bytes(target.read_bytes() + b"\n")
                findings = role_design_contract_findings(self.registry, root=root)
                self.assertEqual(
                    [("role-design-source-changed", contract[changed])],
                    [(code, location) for code, location, _ in findings],
                )


if __name__ == "__main__":
    unittest.main()
