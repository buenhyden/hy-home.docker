"""Public binding, synthetic decisions and generated loopback review regressions."""

import contextlib
import copy
import hashlib
import io
import json
import subprocess
import unittest
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import openbao_consumer_migration as migration
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


class SyntheticKvDecisionTests(unittest.TestCase):
    """Declared public observations only; no byte comparison or KV executor."""

    def test_prewrite_not_found_needs_never_created_metadata(self):
        observation = migration.SyntheticKvObservation("not_found", "unknown", None)
        decision = migration.decide_synthetic_copy(observation, phase="pre_write")
        self.assertEqual("UNRESOLVED", decision.status)
        self.assertIsNone(decision.kv_version)
        self.assertIsNone(decision.cas)

    def test_genuine_absence_is_only_a_prewrite_cas_zero_candidate(self):
        observation = migration.SyntheticKvObservation(
            "not_found", "never_created", None
        )
        decision = migration.decide_synthetic_copy(observation, phase="pre_write")
        self.assertEqual("WOULD_CREATE", decision.status)
        self.assertIsNone(decision.kv_version)
        self.assertEqual(0, decision.cas)
        for phase in ("ambiguous_write", "cas_race"):
            decision = migration.decide_synthetic_copy(observation, phase=phase)
            self.assertEqual(("UNRESOLVED", None, None), self.outcome(decision))

    @staticmethod
    def outcome(decision):
        return decision.status, decision.kv_version, decision.cas

    def test_equal_and_different_observations_require_a_live_positive_version(self):
        expected = {
            ("pre_write", "equal"): "WOULD_NOOP",
            ("ambiguous_write", "equal"): "RECONCILED_EQUAL",
            ("cas_race", "equal"): "RECONCILED_EQUAL",
            ("pre_write", "different"): "CONFLICT",
            ("ambiguous_write", "different"): "CONFLICT",
            ("cas_race", "different"): "CONFLICT",
        }
        for (phase, data), status in expected.items():
            with self.subTest(phase=phase, data=data):
                observation = migration.SyntheticKvObservation(data, "present", 7)
                decision = migration.decide_synthetic_copy(observation, phase=phase)
                self.assertEqual((status, 7, None), self.outcome(decision))

    def test_deleted_denied_missing_and_inconsistent_states_never_authorize_write(self):
        expected = {
            ("pre_write", "not_found", "never_created", None): (
                "WOULD_CREATE",
                None,
                0,
            ),
            ("pre_write", "equal", "present", 1): ("WOULD_NOOP", 1, None),
            ("ambiguous_write", "equal", "present", 1): ("RECONCILED_EQUAL", 1, None),
            ("cas_race", "equal", "present", 1): ("RECONCILED_EQUAL", 1, None),
            ("pre_write", "different", "present", 1): ("CONFLICT", 1, None),
            ("ambiguous_write", "different", "present", 1): ("CONFLICT", 1, None),
            ("cas_race", "different", "present", 1): ("CONFLICT", 1, None),
        }
        combinations = product(
            ("pre_write", "ambiguous_write", "cas_race"),
            ("not_found", "equal", "different", "unknown"),
            (
                "never_created",
                "present",
                "soft_deleted",
                "destroyed",
                "unknown",
                "forbidden",
                "mount_missing",
            ),
            (None, 1),
        )
        for phase, data, metadata, version in combinations:
            with self.subTest(
                phase=phase, data=data, metadata=metadata, version=version
            ):
                observation = migration.SyntheticKvObservation(data, metadata, version)
                decision = migration.decide_synthetic_copy(observation, phase=phase)
                self.assertEqual(
                    expected.get(
                        (phase, data, metadata, version), ("UNRESOLVED", None, None)
                    ),
                    self.outcome(decision),
                )

    def test_invalid_observations_have_fixed_non_disclosing_diagnostics(self):
        valid = migration.SyntheticKvObservation("equal", "present", 1)
        invalid = [
            None,
            {},
            [],
            "private-marker",
            object(),
            {"token": "private-marker"},
        ]
        for field in ("data_state", "metadata_state"):
            for value in (None, [], {}, True, "private-marker", object()):
                invalid.append(replace(valid, **{field: value}))
        for version in (True, False, 0, -1, 1.5, "1", [], {}, float("nan")):
            invalid.append(replace(valid, kv_version=version))
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            for observation in invalid:
                with self.assertRaises(MigrationError) as caught:
                    migration.decide_synthetic_copy(observation, phase="pre_write")
                self.assertEqual("synthetic_observation_invalid", str(caught.exception))
        self.assertEqual("", output.getvalue())

    def test_invalid_phases_cannot_become_retry_or_copy_commands(self):
        observation = migration.SyntheticKvObservation(
            "not_found", "never_created", None
        )
        for phase in (None, [], {}, True, "private-marker", "retry", "copy"):
            with self.assertRaises(MigrationError) as caught:
                migration.decide_synthetic_copy(observation, phase=phase)
            self.assertEqual("synthetic_copy_phase_invalid", str(caught.exception))

    def test_inputs_and_decisions_are_frozen(self):
        observation = migration.SyntheticKvObservation("equal", "present", 1)
        before = replace(observation)
        decision = migration.decide_synthetic_copy(observation, phase="pre_write")
        self.assertEqual(before, observation)
        with self.assertRaises(AttributeError):
            observation.data_state = "not_found"
        with self.assertRaises(AttributeError):
            decision.status = "COPIED"

    def test_public_decision_performs_no_io_selection_or_schema_read(self):
        observation = migration.SyntheticKvObservation("equal", "present", 1)
        with (
            patch("builtins.open", side_effect=AssertionError("unexpected_io")),
            patch.object(
                Path, "read_bytes", side_effect=AssertionError("unexpected_io")
            ),
            patch.object(
                migration, "select_wave", side_effect=AssertionError("selection")
            ),
            patch.object(
                migration, "_schema", side_effect=AssertionError("schema_read")
            ),
        ):
            decision = migration.decide_synthetic_copy(observation, phase="cas_race")
        self.assertEqual(("RECONCILED_EQUAL", 1, None), self.outcome(decision))

    def test_decision_states_cannot_be_promoted_to_current_receipts(self):
        for status in (
            "WOULD_CREATE",
            "WOULD_NOOP",
            "RECONCILED_EQUAL",
            "CONFLICT",
            "UNRESOLVED",
        ):
            candidate = receipt()
            candidate["items"][0]["state"] = status
            with self.assertRaises(MigrationError):
                validate_public("receipt", candidate)


class RuntimeReviewRegressionTests(unittest.TestCase):
    """Review-found safety failures exercised through synthetic loopback resources."""

    def setUp(self):
        from tests.lib.ops.test_openbao_copy_runtime import RuntimeCopyTests

        self.runtime = RuntimeCopyTests()
        self.runtime.setUp()
        self.addCleanup(self.runtime.doCleanups)

    def test_input_roles_and_alternate_root_path_cannot_alias_source(self):
        import os

        candidate = self.runtime.plan()
        source = candidate.sources[0]
        nested = self.runtime.folder / "secrets"
        info = nested.stat()
        alternate = replace(
            source,
            root=str(nested),
            root_dev=info.st_dev,
            root_ino=info.st_ino,
            relative="db/dev-pg/synthetic.txt",
        )
        for field, reference in (
            ("copy_token", source),
            ("metadata_token", source),
            ("ca", source),
            ("copy_token", alternate),
            ("metadata_token", candidate.copy_token),
            ("ca", candidate.copy_token),
        ):
            with self.subTest(field=field, root=reference.root):
                self.runtime.server.version = 0
                self.runtime.server.calls.clear()
                with patch("os.open", wraps=os.open) as opened:
                    result = self.runtime.execute(
                        replace(candidate, **{field: reference})
                    )
                self.assertEqual("BLOCKED", result.status)
                self.assertEqual([], self.runtime.server.calls)
                self.assertFalse(opened.called)

    def test_actual_held_inode_role_alias_is_refused_before_http(self):
        from scripts.lib.ops._openbao_copy_io import hold_input

        candidate = self.runtime.plan()
        for field in ("copy_token", "metadata_token", "ca"):
            with self.subTest(field=field):
                reference = getattr(candidate, field)

                def mounted_alias(selected, stack, *, ca=False, reference=reference):
                    # An injected bind-mount seam returns a real held source FD.
                    chosen = candidate.sources[0] if selected == reference else selected
                    return hold_input(chosen, stack, ca=ca)

                with patch.object(migration, "hold_input", side_effect=mounted_alias):
                    result = self.runtime.execute(candidate)
                self.assertEqual("BLOCKED", result.status)
                self.assertEqual("copy_input_role_alias", result.diagnostic)
                self.assertEqual([], self.runtime.server.calls)

    def test_lost_post_and_unverifiable_readback_preserve_possible_write(self):
        from scripts.lib.ops._openbao_copy_transport import CopyTransport

        self.runtime.server.mode = "lost_write"
        request = CopyTransport.request
        metadata = "/v1/secret/metadata/" + row().kv_path

        def lost_readback(client, method, path, token, payload=None):
            try:
                return request(client, method, path, token, payload)
            finally:
                if method == "POST":
                    self.runtime.server.responses = {
                        ("GET", metadata): (403, {"errors": []})
                    }

        with patch.object(CopyTransport, "request", new=lost_readback):
            result = self.runtime.execute()
        self.assertEqual("PARTIAL", result.status)
        self.assertEqual("UNRESOLVED", result.items[0].status)
        self.assertTrue(result.items[0].write_attempted)
        self.assertIsNone(result.items[0].accepted_version)
        self.assertIsNone(result.items[0].kv_version)
        self.assertEqual(
            1, sum(method == "POST" for method, *_ in self.runtime.server.calls)
        )

    def test_acknowledged_version_one_and_conflicting_version_two_both_survive(self):
        from scripts.lib.ops._openbao_copy_transport import CopyTransport

        request = CopyTransport.request

        def concurrent_change(client, method, path, token, payload=None):
            response = request(client, method, path, token, payload)
            if method == "POST":
                self.runtime.server.version, self.runtime.server.value = 2, "different"
            return response

        with patch.object(CopyTransport, "request", new=concurrent_change):
            result = self.runtime.execute()
        self.assertEqual("PARTIAL", result.status)
        self.assertEqual("CONFLICT", result.items[0].status)
        self.assertTrue(result.items[0].write_attempted)
        self.assertEqual(1, result.items[0].accepted_version)
        self.assertEqual(2, result.items[0].kv_version)
        self.assertEqual(
            1, sum(method == "POST" for method, *_ in self.runtime.server.calls)
        )
        self.assertEqual(
            b"synthetic-private-marker\n", self.runtime.source.read_bytes()
        )

    def test_origin_requires_dns_labels_and_separate_numeric_connect_address(self):
        candidate = self.runtime.plan()
        for hostname in (
            "127.0.0.1",
            "[::1]",
            "x-",
            "a..b",
            "-bad.example",
            "a" * 64 + ".example",
            ".example",
            "a." * 126 + "ab",
        ):
            with self.subTest(hostname=hostname), patch("os.open") as opened:
                result = self.runtime.execute(
                    replace(candidate, origin="https://" + hostname)
                )
                self.assertEqual("BLOCKED", result.status)
                self.assertEqual("copy_endpoint_invalid", result.diagnostic)
                self.assertEqual([], self.runtime.server.calls)
                self.assertFalse(opened.called)

    def test_unexpected_post_transport_failure_is_partial_and_redacted(self):
        from scripts.lib.ops._openbao_copy_transport import CopyTransport

        request = CopyTransport.request

        def unexpected(client, method, path, token, payload=None):
            if method == "POST":
                request(client, method, path, token, payload)
                raise RuntimeError("synthetic-private-marker")
            if self.runtime.server.version:
                raise RuntimeError("synthetic-private-marker")
            return request(client, method, path, token, payload)

        with patch.object(CopyTransport, "request", new=unexpected):
            result = self.runtime.execute()
        self.assertEqual("PARTIAL", result.status)
        self.assertTrue(result.items[0].write_attempted)
        self.assertIsNone(result.items[0].accepted_version)
        self.assertIsNone(result.items[0].kv_version)
        self.assertNotIn("synthetic-private-marker", repr(result))
        self.assertEqual(
            1, sum(method == "POST" for method, *_ in self.runtime.server.calls)
        )

    def test_post_cleanup_failure_preserves_ack_observation_and_attempt(self):
        import os

        close = os.close
        closed = []

        def failing_close(descriptor):
            close(descriptor)
            closed.append(descriptor)
            if self.runtime.server.version:
                raise OSError("synthetic-private-marker")

        with patch("os.close", new=failing_close):
            result = self.runtime.execute()
        self.assertEqual("PARTIAL", result.status)
        self.assertEqual("copy_cleanup_failed", result.diagnostic)
        self.assertEqual(1, len(result.items))
        item = result.items[0]
        self.assertEqual("CREATED", item.status)
        self.assertTrue(item.write_attempted)
        self.assertEqual((1, 1), (item.accepted_version, item.kv_version))
        self.assertNotIn("synthetic-private-marker", repr(result))
        self.assertTrue(closed)
        for descriptor in closed:
            with self.assertRaises(OSError):
                os.fstat(descriptor)

    def test_noop_cleanup_failure_retains_observation_without_write_claim(self):
        import os

        self.runtime.server.version = 3
        self.runtime.server.value = "synthetic-private-marker\n"
        close = os.close

        def failing_close(descriptor):
            close(descriptor)
            raise OSError("synthetic-private-marker")

        with patch("os.close", new=failing_close):
            result = self.runtime.execute()
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("copy_cleanup_failed", result.diagnostic)
        self.assertEqual(1, len(result.items))
        item = result.items[0]
        self.assertEqual(("NOOP", 3), (item.status, item.kv_version))
        self.assertFalse(item.write_attempted)
        self.assertIsNone(item.accepted_version)
        self.assertNotIn("synthetic-private-marker", repr(result))
