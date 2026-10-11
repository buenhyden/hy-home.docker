"""W47 synthetic authority/selection tests; no actual catalog or private I/O."""

import copy
import json
import unittest
from dataclasses import replace

from scripts.lib.ops.openbao_consumer_migration import (
    CatalogBinding,
    CatalogSelection,
    FrozenAuthority,
    MigrationError,
    parse_public_json,
    select_wave,
    validate_public,
)


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
