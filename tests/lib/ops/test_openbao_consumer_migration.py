"""W47 synthetic selection and public P02 API binding; no private I/O."""

import copy
import hashlib
import json
import subprocess
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.lib.ops.openbao_consumer_migration import (
    CatalogBinding,
    CatalogSelection,
    FrozenAuthority,
    MigrationError,
    parse_public_json,
    select_wave,
    validate_public,
)
from scripts.lib.ops.secret_catalog import load_catalog, validate_catalog

ROOT = Path(__file__).resolve().parents[3]


def binding():
    return CatalogBinding("a" * 40, "1.0.0", "b" * 64, "c" * 64, "d" * 64)


def wave():
    return {
        "schema_version": "1.0.0",
        "wave_id": "p06-synthetic-pilot",
        "consumer": "synthetic-consumer",
        "evidence_kind": "synthetic",
        "catalog": binding().as_dict(),
        "secret_ids": ["PG-033"],
    }


def row(identifier="PG-033"):
    return CatalogSelection(
        identifier,
        "root",
        "kv_static",
        "IMPLEMENT",
        "ACTIVE_KEEP",
        "DECLARED",
        ("synthetic-consumer",),
        None,
        "secrets/db/dev-pg/synthetic.txt",
        "APPROVED",
        "secret",
        "hy-home/dev/synthetic/connection",
        "value",
    )


def receipt():
    return {
        **{key: value for key, value in wave().items() if key != "secret_ids"},
        "result": "PASS",
        "items": [{"id": "PG-033", "state": "classified", "kv_version": None}],
    }


class PublicMigrationTests(unittest.TestCase):
    def test_selection_is_immutable_and_performs_only_public_lookup(self):
        calls = []

        def lookup(identifier):
            calls.append(identifier)
            return row(identifier)

        candidate = wave()
        before = copy.deepcopy(candidate)
        selected = select_wave(candidate, FrozenAuthority(binding(), lookup))
        self.assertEqual(["PG-033"], calls)
        self.assertEqual(before, candidate)
        self.assertEqual((row(),), selected)
        with self.assertRaises(AttributeError):
            selected[0].id = "PG-034"

    def test_candidate_cannot_choose_catalog_or_source_hash(self):
        for field in binding().as_dict():
            candidate = wave()
            candidate["catalog"][field] = (
                "2.0.0"
                if field.endswith("version")
                else "e" * len(candidate["catalog"][field])
            )
            calls = []
            with self.subTest(field=field), self.assertRaises(MigrationError):
                select_wave(candidate, FrozenAuthority(binding(), calls.append))
            self.assertEqual([], calls)

    def test_all_candidate_guards_precede_adapter_access(self):
        candidates = []
        for key, value in (
            ("secret_ids", []),
            ("secret_ids", ["PG-033", "PG-033"]),
            ("secret_ids", ["*"]),
            ("consumer", "../private"),
            ("wave_id", "private-marker"),
            ("evidence_kind", "native"),
            ("schema_version", True),
            ("token", "private-marker"),
        ):
            candidate = wave()
            candidate[key] = value
            candidates.append(candidate)
        for candidate in candidates:
            calls = []
            with self.subTest(candidate=candidate), self.assertRaises(MigrationError):
                select_wave(candidate, FrozenAuthority(binding(), calls.append))
            self.assertEqual([], calls)

    def test_unknown_alias_unresolved_and_ineligible_rows_are_rejected(self):
        variants = [None, replace(row(), id="PG-034")]
        for key, value in (
            ("alias_of", "PG-034"),
            ("scope", "lab"),
            ("scope", "home"),
            ("scope", None),
            ("classification", "bootstrap_external"),
            ("classification", "stable_crypto"),
            ("classification", "unused_delete"),
            ("action", "VERIFY_RUNTIME"),
            ("disposition", "RETAINED_FOR_RECOVERY"),
            ("consumer_status", "BLOCKED_FACTS"),
            ("consumers", ()),
            ("consumers", ("other-consumer",)),
            ("destination_status", "BLOCKED_P01"),
            ("field", "admin_password"),
        ):
            variants.append(replace(row(), **{key: value}))
        for candidate in variants:
            with self.subTest(row=candidate), self.assertRaises(MigrationError):
                select_wave(
                    wave(), FrozenAuthority(binding(), lambda _, item=candidate: item)
                )

    def test_paths_and_mounts_reject_traversal_hidden_wildcard_and_lab(self):
        for key, value in (
            ("source_path", "/etc/private"),
            ("source_path", "secrets/../private"),
            ("source_path", "secrets/.hidden/file"),
            ("source_path", "secrets/labs/file.txt"),
            ("source_path", "secrets/a/*"),
            ("source_path", "secrets/a/%2e%2e"),
            ("kv_path", "hy-home/../admin"),
            ("kv_path", "sys/admin"),
            ("mount", "secret/other"),
            ("mount", "*"),
            ("mount", "sys"),
            ("mount", "auth"),
        ):
            candidate = replace(row(), **{key: value})
            with (
                self.subTest(field=key, value=value),
                self.assertRaises(MigrationError),
            ):
                select_wave(
                    wave(), FrozenAuthority(binding(), lambda _, item=candidate: item)
                )

    def test_destinations_are_unique_across_entire_wave(self):
        candidate = wave()
        candidate["secret_ids"] = ["PG-033", "PG-034"]
        with self.assertRaisesRegex(MigrationError, "duplicate_destination"):
            select_wave(candidate, FrozenAuthority(binding(), row))
        selected = select_wave(
            candidate,
            FrozenAuthority(
                binding(),
                lambda identifier: replace(
                    row(identifier),
                    kv_path="hy-home/dev/synthetic/" + identifier.lower(),
                ),
            ),
        )
        self.assertEqual(2, len(selected))

    def test_adapter_failures_never_disclose_exception_payload(self):
        def broken(_):
            raise RuntimeError("private-marker")

        with self.assertRaises(MigrationError) as caught:
            select_wave(wave(), FrozenAuthority(binding(), broken))
        self.assertEqual("catalog_adapter_failed", str(caught.exception))

    def test_invalid_authority_and_projection_types_are_rejected(self):
        for authority in (
            None,
            FrozenAuthority(replace(binding(), revision="bad"), row),
            FrozenAuthority(binding(), None),
        ):
            with self.subTest(authority=authority), self.assertRaises(MigrationError):
                select_wave(wave(), authority)
        for candidate in (
            {},
            replace(row(), consumers=["synthetic-consumer"]),
            replace(row(), source_path=None),
            replace(row(), mount=None),
        ):
            with self.subTest(row=candidate), self.assertRaises(MigrationError):
                select_wave(
                    wave(), FrozenAuthority(binding(), lambda _, item=candidate: item)
                )

    def test_public_parser_is_bounded_and_has_fixed_diagnostics(self):
        self.assertEqual(wave(), parse_public_json(json.dumps(wave()).encode()))
        for raw in (
            b'{"a":1,"a":2}',
            b'{"a":NaN}',
            b'{"a":Infinity}',
            b"private-marker",
            b"\xff",
            b"[]",
            b"{" + b" " * 131072,
            b'{"a":' + b"[" * 30 + b"0" + b"]" * 30 + b"}",
            "text",
        ):
            with (
                self.subTest(size=len(raw)),
                self.assertRaises(MigrationError) as caught,
            ):
                parse_public_json(raw)
            self.assertNotIn("private-marker", str(caught.exception))

    def test_receipts_reject_false_promotion_and_arbitrary_private_fields(self):
        validate_public("receipt", receipt())
        for state in (
            "copied",
            "rendered",
            "consumed",
            "authoritative",
            "recoverable",
            "local-plaintext-removed",
        ):
            candidate = receipt()
            candidate["items"][0].update(state=state, kv_version=1)
            with self.subTest(state=state), self.assertRaises(MigrationError):
                validate_public("receipt", candidate)
        for key, value in (
            ("evidence_kind", "native"),
            ("value", "private-marker"),
            ("value_sha256", "a" * 64),
            ("result", "PARTIAL"),
        ):
            candidate = receipt()
            candidate[key] = value
            with self.subTest(field=key), self.assertRaises(MigrationError):
                validate_public("receipt", candidate)
        candidate = receipt()
        candidate["items"] *= 2
        with self.assertRaises(MigrationError):
            validate_public("receipt", candidate)

    def test_receipt_version_and_status_are_coherent(self):
        for version in (0, True, 1):
            candidate = receipt()
            candidate["items"][0]["kv_version"] = version
            with self.subTest(version=version), self.assertRaises(MigrationError):
                validate_public("receipt", candidate)
        for result in ("NOT_RUN", "FAIL", "PASS"):
            candidate = receipt()
            candidate["result"] = result
            self.assertIsNone(validate_public("receipt", candidate))
        with self.assertRaises(MigrationError):
            validate_public("unknown", wave())
        with self.assertRaises(MigrationError):
            validate_public("wave", [])


class PublicCatalogBindingTests(unittest.TestCase):
    """Test-only projection; P02 owns validation and all approval decisions."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        inputs = (
            "infra/03-security/openbao/secret-catalog.json",
            "infra/03-security/openbao/secret-catalog.schema.json",
            "scripts/lib/ops/secret_catalog.py",
        )
        hashes = tuple(
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in inputs
        )
        if json.loads((ROOT / inputs[0]).read_bytes()) != cls.catalog:
            raise AssertionError("public catalog changed after API validation")
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        cls.public_binding = CatalogBinding(
            revision, cls.catalog["schema_version"], *hashes
        )
        cls.rows = tuple(
            CatalogSelection(
                entry["id"],
                entry["scope"],
                entry["classification"],
                entry["action"],
                entry["disposition"],
                entry["consumer_status"],
                tuple(entry["consumers"]),
                None,
                entry["source_path"],
                entry["destination_plan"]["status"],
                entry["destination_plan"]["mount"],
                entry["destination_plan"]["kv_path"],
                entry["destination_plan"]["field"],
            )
            for entry in cls.catalog["entries"]
        )

    def candidate(self, identifier):
        return {
            **wave(),
            "catalog": self.public_binding.as_dict(),
            "secret_ids": [identifier],
        }

    def lookup(self, identifier):
        return next((item for item in self.rows if item.id == identifier), None)

    def test_public_api_metadata_is_preserved_by_refused_selection(self):
        before = copy.deepcopy(self.catalog)
        self.assertEqual(
            {entry["id"] for entry in self.catalog["entries"]},
            {item.id for item in self.rows},
        )
        authority = FrozenAuthority(self.public_binding, self.lookup)
        for item in self.rows:
            with self.subTest(identifier=item.id), self.assertRaises(MigrationError):
                select_wave(self.candidate(item.id), authority)
        self.assertEqual(before, self.catalog)

    def test_implement_action_is_not_a_destination_approval(self):
        item = next(
            item
            for item in self.rows
            if item.scope == "root"
            and item.classification == "kv_static"
            and item.action == "IMPLEMENT"
        )
        self.assertNotEqual("APPROVED", item.destination_status)
        with self.assertRaisesRegex(MigrationError, "catalog_copy_not_approved"):
            select_wave(
                self.candidate(item.id),
                FrozenAuthority(self.public_binding, self.lookup),
            )

    def test_alias_is_not_resolved_into_its_canonical_copy(self):
        self.assertIn(
            {"id": "COMM-003", "canonical_id": "COMM-002", "state": "source_retired"},
            self.catalog["aliases"],
        )
        authority = FrozenAuthority(self.public_binding, self.lookup)
        with self.assertRaisesRegex(MigrationError, "unknown_catalog_id"):
            select_wave(self.candidate("COMM-003"), authority)
        with self.assertRaises(MigrationError):
            select_wave(self.candidate("COMM-002"), authority)

    def test_recovery_hold_is_not_reclassified_for_a_pilot(self):
        held = self.lookup("PG-020")
        self.assertEqual("RETAINED_FOR_RECOVERY", held.disposition)
        with self.assertRaisesRegex(MigrationError, "catalog_copy_not_approved"):
            select_wave(
                self.candidate(held.id),
                FrozenAuthority(self.public_binding, self.lookup),
            )
        self.assertEqual("RETAINED_FOR_RECOVERY", self.lookup("PG-020").disposition)

    def test_public_input_binding_drift_stops_before_lookup(self):
        for field in ("revision", "catalog_sha256", "schema_sha256", "source_sha256"):
            candidate = self.candidate("PG-020")
            candidate["catalog"][field] = "e" * len(candidate["catalog"][field])
            if candidate["catalog"][field] == getattr(self.public_binding, field):
                candidate["catalog"][field] = "f" * len(candidate["catalog"][field])
            calls = []
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(MigrationError, "catalog_binding_mismatch"),
            ):
                select_wave(
                    candidate, FrozenAuthority(self.public_binding, calls.append)
                )
            self.assertEqual([], calls)

    def test_invented_delivery_approval_is_rejected_by_the_p02_api(self):
        candidate = copy.deepcopy(self.catalog)
        entry = next(item for item in candidate["entries"] if item["id"] == "PG-020")
        entry["destination_plan"] = {**entry["destination_plan"], "status": "APPROVED"}
        with self.assertRaises(ValueError):
            validate_catalog(candidate)
        self.assertEqual("RETAINED_FOR_RECOVERY", self.lookup("PG-020").disposition)
