"""DOC-07 R08 link types and DOC-09 R07 document relations in the Registry."""

from __future__ import annotations

import json
import unittest

from scripts.lib.document_governance.registry import (
    DEFAULT_REGISTRY,
    validate_registry,
)


def _registry() -> dict:
    return json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))


def _codes(raw: dict) -> set[str]:
    return {finding.code for finding in validate_registry(raw)}


class LinkTypeContractTests(unittest.TestCase):
    def test_registry_binds_four_forward_link_types(self) -> None:
        common = _registry()["common"]
        types = common["link_types"]
        self.assertEqual(
            {"normative", "evidence", "historical", "navigation"}, set(types)
        )
        for name, link_type in types.items():
            with self.subTest(name=name):
                self.assertEqual("forward", link_type["direction"])
                self.assertEqual(
                    {
                        "direction",
                        "required",
                        "authority",
                        "pinned_version",
                        "on_target_removal",
                    },
                    set(link_type),
                )
        self.assertEqual({"markdown", "vault-wiki"}, set(common["link_profiles"]))

    def test_reverse_link_direction_is_rejected(self) -> None:
        raw = _registry()
        raw["common"]["link_types"]["evidence"]["direction"] = "reverse"
        self.assertIn("schema-invalid", _codes(raw))

    def test_missing_link_type_is_rejected(self) -> None:
        raw = _registry()
        del raw["common"]["link_types"]["historical"]
        self.assertIn("schema-invalid", _codes(raw))

    def test_missing_link_contract_is_rejected(self) -> None:
        raw = _registry()
        del raw["common"]["link_types"]
        self.assertIn("relation-contract-missing", _codes(raw))


class DocumentRelationContractTests(unittest.TestCase):
    def test_registry_binds_the_seven_common_relations_and_is_valid(self) -> None:
        raw = _registry()
        relations = raw["common"]["document_relations"]
        self.assertEqual(
            {
                "authority",
                "structural_ownership",
                "constraint",
                "traceability",
                "promotion",
                "supersession",
                "change_impact",
            },
            set(relations),
        )
        self.assertEqual(
            [{"kind": "frontmatter", "ref": "parent_ids"}],
            relations["structural_ownership"]["writers"],
        )
        self.assertEqual(
            [{"kind": "frontmatter", "ref": "supersedes"}],
            relations["supersession"]["writers"],
        )
        self.assertEqual(
            [{"kind": "section", "ref": "plan:Promotion Map/Owner and Receipt"}],
            relations["promotion"]["writers"],
        )
        self.assertEqual((), validate_registry(raw))

    def test_manual_reverse_lookup_is_rejected(self) -> None:
        raw = _registry()
        raw["common"]["document_relations"]["supersession"]["reverse_lookup"] = "manual"
        self.assertIn("schema-invalid", _codes(raw))

    def test_duplicate_relation_id_is_rejected(self) -> None:
        raw = _registry()
        relations = raw["common"]["document_relations"]
        relations["constraint"]["id"] = relations["authority"]["id"]
        self.assertIn("schema-invalid", _codes(raw))

    def test_unknown_writer_references_are_rejected(self) -> None:
        cases = (
            ("structural_ownership", {"kind": "frontmatter", "ref": "not_a_key"}),
            ("authority", {"kind": "link", "ref": "not_a_link_type"}),
            ("change_impact", {"kind": "derived", "ref": "rel.missing"}),
            ("promotion", {"kind": "section", "ref": "plan:Promotion Map/Nope"}),
            (
                "promotion",
                {"kind": "section", "ref": "nope:Promotion Map/Owner and Receipt"},
            ),
            (
                "constraint",
                {"kind": "section", "ref": "spec:Scope/Owning Requirements"},
            ),
        )
        for name, writer in cases:
            with self.subTest(name=name):
                raw = _registry()
                raw["common"]["document_relations"][name]["writers"] = [writer]
                self.assertIn("relation-contract-invalid", _codes(raw))

    def test_missing_owner_path_is_rejected(self) -> None:
        raw = _registry()
        raw["common"]["document_relations"]["authority"]["owner"] = (
            "scripts/validation/does-not-exist.py"
        )
        self.assertIn("relation-contract-invalid", _codes(raw))

    def test_retained_reverse_field_must_be_a_frontmatter_key(self) -> None:
        raw = _registry()
        raw["common"]["document_relations"]["supersession"][
            "retained_reverse_fields"
        ] = ["not_a_key"]
        self.assertIn("relation-contract-invalid", _codes(raw))

    def test_derived_writer_cannot_name_its_own_relation(self) -> None:
        raw = _registry()
        relation = raw["common"]["document_relations"]["change_impact"]
        relation["writers"] = [{"kind": "derived", "ref": relation["id"]}]
        self.assertIn("relation-contract-invalid", _codes(raw))

    def test_missing_relations_alone_is_rejected(self) -> None:
        raw = _registry()
        del raw["common"]["document_relations"]
        self.assertIn("relation-contract-missing", _codes(raw))


class PinnedContractValueTests(unittest.TestCase):
    """Every value the policy tables fix is pinned: a mutation fails closed."""

    MUTATIONS = (
        ("document_relations", "structural_ownership", "direction", "parent-to-child"),
        ("document_relations", "authority", "direction", "owner-to-consumer"),
        ("document_relations", "promotion", "id", "rel.other"),
        ("document_relations", "supersession", "direction", "predecessor-to-successor"),
        ("link_types", "normative", "authority", "none"),
        ("link_types", "normative", "required", False),
        ("link_types", "evidence", "pinned_version", "current"),
        ("link_types", "historical", "on_target_removal", "update-consumer"),
        ("link_types", "navigation", "authority", "binding"),
        ("link_profiles", "vault-wiki", "link_types", True),
        ("link_profiles", "vault-wiki", "syntax", "relative-markdown"),
        ("link_profiles", "markdown", "link_types", False),
    )

    def test_each_mutated_value_is_rejected(self) -> None:
        for section, entry, key, value in self.MUTATIONS:
            with self.subTest(section=section, entry=entry, key=key):
                raw = _registry()
                raw["common"][section][entry][key] = value
                self.assertIn("schema-invalid", _codes(raw))


if __name__ == "__main__":
    unittest.main()
