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
    def test_registry_binds_five_relations_and_is_valid(self) -> None:
        raw = _registry()
        relations = raw["common"]["document_relations"]
        self.assertEqual(
            {
                "authority",
                "ownership",
                "reference",
                "traceability",
                "change_propagation",
            },
            set(relations),
        )
        self.assertEqual(
            [{"kind": "frontmatter", "ref": "parent_ids"}],
            relations["traceability"]["writers"][:1],
        )
        self.assertEqual("child-to-parent", relations["traceability"]["direction"])
        self.assertEqual((), validate_registry(raw))

    def test_manual_reverse_lookup_is_rejected(self) -> None:
        raw = _registry()
        raw["common"]["document_relations"]["traceability"]["reverse_lookup"] = "manual"
        self.assertIn("schema-invalid", _codes(raw))

    def test_duplicate_relation_id_is_rejected(self) -> None:
        raw = _registry()
        relations = raw["common"]["document_relations"]
        relations["reference"]["id"] = relations["authority"]["id"]
        self.assertIn("relation-contract-invalid", _codes(raw))

    def test_unknown_writer_references_are_rejected(self) -> None:
        cases = (
            ("ownership", {"kind": "frontmatter", "ref": "not_a_key"}),
            ("reference", {"kind": "link", "ref": "not_a_link_type"}),
            ("change_propagation", {"kind": "derived", "ref": "rel.missing"}),
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
        raw["common"]["document_relations"]["traceability"][
            "retained_reverse_fields"
        ] = ["not_a_key"]
        self.assertIn("relation-contract-invalid", _codes(raw))


if __name__ == "__main__":
    unittest.main()
