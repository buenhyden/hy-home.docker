"""Synthetic metadata only; P02 never reads private values or production KV."""

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import _secret_catalog_io as catalog_io
from scripts.lib.ops import secret_catalog as catalog

PUBLIC = """| ID | Automation | Type | Value | Env | Path | Recorded | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **COMM-002** | `O` | `Pass` | `(비어있음)` | `-` | `secrets/communication/smtp/smtp_password.txt` | 2026-10-03 | Shared SMTP password |

| Retired ID | Canonical ID |
| --- | --- |
| COMM-003 | COMM-002 |
""".encode()
EVIDENCE = "docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0010-p02-secret-catalog-and-views.md"
CLI = Path(__file__).resolve().parents[3] / "scripts/operations/secret-catalog.py"


def model():
    metadata = catalog.parse_public_table(PUBLIC)
    entry = {
        **metadata["entries"][0],
        "scope": "root",
        "classification": "kv_static",
        "consumers": ["infra/06-observability/docker-compose.yml"],
        "consumer_status": "DECLARED",
        "disposition": "ACTIVE_KEEP",
        "owner": "@buenhyden",
        "action": "NO_CHANGE",
        "evidence_ref": EVIDENCE,
        "runtime_evidence": {
            lane: None for lane in catalog.LIFECYCLE_FIELDS - {"declared"}
        },
        "destination_plan": {
            "status": "BLOCKED_P01",
            "acl": "BLOCKED_P01",
            "kv_path": "secret/root/smtp",
            "delivery": "BLOCKED_P01",
            "reload": "BLOCKED_P01",
            "restart": "BLOCKED_P01",
            "rotation": "BLOCKED_P01",
            "mount": None,
            "field": None,
            "uid": None,
            "gid": None,
            "mode": None,
        },
        "recovery": {
            "history": "retain",
            "custody": "consumer_owned",
            "status": "UNKNOWN",
        },
        "lifecycle": {
            "declared": "CONFIRMED",
            "observed": "UNKNOWN",
            "imported": "NOT_RUN",
            "delivered": "NOT_RUN",
            "consumed": "UNKNOWN",
            "rotated": "NOT_RUN",
            "recovered": "NOT_RUN",
            "retired": "NOT_RUN",
        },
    }
    return {
        "schema_version": "1.0.0",
        "owner_task": "SPEC-0204-TSK-0010",
        "metadata_source": catalog.METADATA_PATH,
        "support_matrix": catalog.SUPPORT_PATH,
        "entries": [entry],
        "aliases": metadata["aliases"],
    }


def generation_model():
    document = model()
    entry = deepcopy(document["entries"][0])
    entry.update(
        id="TEST-001", source_path="secrets/db/example/password.txt", action="IMPLEMENT"
    )
    entry["destination_plan"]["kv_path"] = "secret/root/test"
    document["entries"].append(entry)
    return document


class SecretCatalogTests(unittest.TestCase):
    def setUp(self):
        self.document = model()
        self.entry = self.document["entries"][0]

    def assert_invalid(self, document):
        with self.assertRaises(catalog.CatalogError):
            catalog.validate_catalog(document)

    def test_parse_public_metadata_and_smtp_alias_without_values(self):
        parsed = catalog.parse_public_table(PUBLIC)
        self.assertEqual(parsed["entries"][0]["id"], "COMM-002")
        self.assertEqual(parsed["entries"][0]["source_path"], catalog.CANONICAL_PATH)
        self.assertEqual(
            parsed["aliases"],
            [{"id": "COMM-003", "canonical_id": "COMM-002", "state": "source_retired"}],
        )
        self.assertNotIn("value", parsed["entries"][0])

    def test_source_date_preserved_without_review_or_rotation_claim(self):
        entry = catalog.parse_public_table(PUBLIC)["entries"][0]
        self.assertEqual(entry["source_recorded_at"], "2026-10-03")
        self.assertNotIn("reviewed_at", entry)
        views = catalog.render_views(self.document)
        self.assertIn("원본기록일".encode(), views[catalog.VIEW_NAMES[0]])

    def test_observed_and_consumed_confirmation_blocks_reissuance(self):
        for lane in ("observed", "consumed"):
            document = generation_model()
            document["entries"][1]["lifecycle"][lane] = "CONFIRMED"
            document["entries"][1]["runtime_evidence"][lane] = EVIDENCE
            catalog.validate_catalog(document)
            with self.subTest(lane=lane):
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))

    def test_deployed_destination_needs_a_delivered_full_binding(self):
        def deployed(field="client_secret"):
            document = generation_model()
            entry = document["entries"][1]
            entry["lifecycle"]["delivered"] = "CONFIRMED"
            entry["runtime_evidence"]["delivered"] = EVIDENCE
            entry["destination_plan"].update(
                status="DEPLOYED",
                delivery="openbao_agent",
                mount="secret",
                kv_path="hy-home/test/app",
                field=field,
                uid=100,
                gid=1000,
                mode="0640",
            )
            return document

        catalog.validate_catalog(deployed())
        twin = deployed()
        sibling = deepcopy(twin["entries"][1])
        sibling.update(id="TEST-002", source_path="secrets/db/example/other.txt")
        sibling["destination_plan"]["field"] = "admin_password"
        twin["entries"].append(sibling)
        catalog.validate_catalog(twin)
        sibling["destination_plan"]["field"] = "client_secret"
        with self.subTest(case="duplicate_binding"):
            self.assert_invalid(twin)
        for case, change in [
            ("not_delivered", ("lifecycle", "delivered", "NOT_RUN")),
            ("other_mount", ("destination_plan", "mount", "kv")),
            ("outside_prefix", ("destination_plan", "kv_path", "secret/x")),
            ("bad_field", ("destination_plan", "field", "Value")),
            ("bool_uid", ("destination_plan", "uid", True)),
            ("open_mode", ("destination_plan", "mode", "0644")),
            ("other_delivery", ("destination_plan", "delivery", "BLOCKED_P01")),
            ("rotation_claim", ("destination_plan", "rotation", "openbao_agent")),
        ]:
            document = deployed()
            section, key, value = change
            document["entries"][1][section][key] = value
            with self.subTest(case=case):
                self.assert_invalid(document)
        document = generation_model()
        document["entries"][1]["destination_plan"]["field"] = "client_secret"
        with self.subTest(case="blocked_with_binding"):
            self.assert_invalid(document)

    def test_secret_source_prefix_and_planned_destinations_are_unique(self):
        document = generation_model()
        document["entries"][1]["source_path"] = "infra/public.txt"
        with self.subTest(case="source_prefix"):
            self.assert_invalid(document)
        document = generation_model()
        document["entries"][1]["destination_plan"]["kv_path"] = document["entries"][0][
            "destination_plan"
        ]["kv_path"]
        with self.subTest(case="duplicate_kv_path"):
            self.assert_invalid(document)
        for field, value in [
            ("classification", "bootstrap_external"),
            ("disposition", "RETAINED_FOR_RECOVERY"),
        ]:
            document = generation_model()
            document["entries"][1][field] = value
            with self.subTest(case=field):
                self.assert_invalid(document)

    def test_unused_delete_metadata_cannot_claim_consumers_or_crypto_custody(self):
        for classification in ("kv_static", "stable_crypto"):
            document = generation_model()
            entry = document["entries"][1]
            entry["classification"] = classification
            entry["disposition"] = "UNUSED_DELETE"
            with self.subTest(classification=classification):
                self.assert_invalid(document)
        document = generation_model()
        entry = document["entries"][1]
        entry.update(
            classification="unused_delete",
            disposition="UNUSED_DELETE",
            action="DELETE",
            consumer_status="DECLARED",
        )
        entry["destination_plan"]["kv_path"] = None
        with self.subTest(case="positive_consumers"):
            self.assert_invalid(document)
        entry["consumers"] = []
        with self.subTest(case="recovery_custody"):
            self.assert_invalid(document)
        entry["recovery"]["custody"] = "not_applicable"
        catalog.validate_catalog(document)
        self.assertFalse(catalog.generation_allowed(document, "TEST-001"))
        entry["source_path"] = "secrets/automation/example/fernet_key.txt"
        self.assert_invalid(document)

    def test_validate_and_render_preserve_input_and_table_shape(self):
        original = deepcopy(self.document)
        catalog.validate_catalog(self.document)
        views = catalog.render_views(self.document)
        self.assertEqual(set(views), set(catalog.VIEW_NAMES))
        self.assertIn("README.md", views)
        parsed = catalog.parse_public_table(views[catalog.VIEW_NAMES[0]])
        self.assertEqual(
            parsed["entries"], catalog.parse_public_table(PUBLIC)["entries"]
        )
        self.assertEqual(self.document, original)
        for raw in views.values():
            self.assertNotIn(b'"value":', raw)

    def test_staging_local_view_has_governance_without_value_column(self):
        views = catalog.render_views(self.document)
        self.assertIn("SENSITIVE_ENV_VARS.md", views)
        local = views["SENSITIVE_ENV_VARS.md"].decode()
        for field in (
            "분류",
            "원본 경로",
            "계획 KV",
            "작업",
            "소유자",
            "수명주기",
            "근거",
        ):
            self.assertIn(field, local)
        self.assertNotIn("| 값 |", local)
        self.assertNotIn("(비어있음)", local)
        self.assertIn(EVIDENCE, local)

    def test_runtime_confirmation_requires_corresponding_evidence_and_consumer(self):
        for lane in catalog.LIFECYCLE_FIELDS - {"declared"}:
            document = generation_model()
            entry = document["entries"][1]
            entry["lifecycle"][lane] = "CONFIRMED"
            with self.subTest(lane=lane):
                self.assert_invalid(document)
                entry["runtime_evidence"][lane] = EVIDENCE
                catalog.validate_catalog(document)
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))
        entry["lifecycle"]["consumed"] = "CONFIRMED"
        entry["runtime_evidence"]["consumed"] = EVIDENCE
        entry["consumers"] = []
        self.assert_invalid(document)
        document = model()
        document["entries"][0]["runtime_evidence"]["observed"] = "infra/public.json"
        self.assert_invalid(document)

    def test_public_parser_rejects_values_and_retired_source_conversion(self):
        cases = [
            PUBLIC.replace("(비어있음)".encode(), b"synthetic-private-value"),
            PUBLIC.replace(b"| COMM-003 | COMM-002 |", b""),
            PUBLIC.replace(b"| COMM-003 | COMM-002 |", b"| COMM-003 | UNKNOWN-001 |"),
            PUBLIC.replace(b"COMM-002", b"COMM-099"),
            PUBLIC.replace(b"| **COMM-002**", b"| invalid"),
            PUBLIC.replace(b"`O`", b"`Y`"),
            PUBLIC.replace(b"`Pass`", b"`Unexpected`"),
            PUBLIC.replace(b"2026-10-03", b"2026-99-03"),
            PUBLIC.replace(b"Shared SMTP password", b"password=synthetic-value"),
            PUBLIC.replace(b"| ID | Automation", b"| ID | Extra | Automation"),
        ]
        for raw in cases:
            with self.subTest(case_length=len(raw)), self.assertRaises(ValueError):
                catalog.parse_public_table(raw)
        retired = b"| **COMM-003** | `O` | `Pass` | `(\xeb\xb9\x84\xec\x96\xb4\xec\x9e\x88\xec\x9d\x8c)` | `-` | `secrets/communication/supabase/supabase_smtp_password.txt` | 2026-10-03 | Old SMTP |\n"
        with self.assertRaises(ValueError):
            catalog.parse_public_table(PUBLIC + retired)
        with self.assertRaises(ValueError):
            catalog.parse_public_table(b"\xff")
        with self.assertRaises(ValueError):
            catalog.parse_public_table("not bytes")

    def test_closed_fields_and_malformed_types(self):
        for target in [
            self.document,
            self.entry,
            self.entry["destination_plan"],
            self.entry["recovery"],
            self.entry["lifecycle"],
        ]:
            target["password"] = "synthetic-value"
            self.assert_invalid(self.document)
            del target["password"]
        for field in catalog.ENTRY_FIELDS:
            document = deepcopy(self.document)
            del document["entries"][0][field]
            self.assert_invalid(document)
        for field, value in [
            ("classification", []),
            ("consumers", [{}]),
            ("automation", {}),
            ("value_type", None),
            ("source_recorded_at", False),
            ("scope", []),
            ("purpose", "password: synthetic-value"),
            ("id", "invalid"),
        ]:
            with self.subTest(field=field):
                document = deepcopy(self.document)
                document["entries"][0][field] = value
                self.assert_invalid(document)

    def test_public_paths_and_unicode_are_bounded(self):
        for path in [
            "/etc/passwd",
            "../outside",
            "secrets/../outside",
            "secrets//x",
            "secrets/./x",
            "secrets/a\\b",
            "secrets/*",
            "secrets/a\u202eb",
            "secrets/a\x7fb",
        ]:
            document = deepcopy(self.document)
            document["entries"][0]["source_path"] = path
            with self.subTest(path_repr=repr(path)):
                self.assert_invalid(document)
        for value in [
            "token=synthetic-value",
            "-----BEGIN PRIVATE KEY-----",
            "eyJabc.def.ghi",
            "purpose\u200bspoof",
            "a" * 1001,
            "text|column",
        ]:
            document = deepcopy(self.document)
            document["entries"][0]["purpose"] = value
            self.assert_invalid(document)

    def test_duplicates_alias_cycles_and_smtp_invariants(self):
        document = deepcopy(self.document)
        document["entries"].append(deepcopy(self.entry))
        self.assert_invalid(document)
        document["entries"][1]["id"] = "TEST-001"
        self.assert_invalid(document)
        for aliases in [
            [],
            [self.document["aliases"][0]] * 2,
            [{"id": "COMM-002", "canonical_id": "COMM-002", "state": "source_retired"}],
            [
                {
                    "id": "COMM-003",
                    "canonical_id": "MISSING-001",
                    "state": "source_retired",
                }
            ],
            [
                {
                    "id": "COMM-003",
                    "canonical_id": "ALIAS-001",
                    "state": "source_retired",
                },
                {
                    "id": "ALIAS-001",
                    "canonical_id": "COMM-003",
                    "state": "source_retired",
                },
            ],
        ]:
            self.assert_invalid({**self.document, "aliases": aliases})
        document = deepcopy(self.document)
        document["entries"][0]["source_path"] = (
            "secrets/communication/supabase/supabase_smtp_password.txt"
        )
        self.assert_invalid(document)

    def test_generation_guard_for_every_classification_and_lifecycle(self):
        self.assertTrue(catalog.generation_allowed(generation_model(), "TEST-001"))
        self.assertFalse(catalog.generation_allowed(self.document, "COMM-002"))
        self.assertFalse(catalog.generation_allowed(self.document, "COMM-003"))
        self.assertFalse(catalog.generation_allowed(self.document, "UNKNOWN-001"))
        for field, value in [
            ("classification", "stable_crypto"),
            ("classification", "bootstrap_external"),
            ("classification", "public_configuration"),
            ("classification", "derived_runtime"),
            ("classification", "unused_delete"),
            ("classification", "lab_excluded"),
            ("scope", "lab"),
            ("automation", "X"),
            ("disposition", "RETAINED_FOR_RECOVERY"),
            ("consumer_status", "BLOCKED_FACTS"),
            ("consumers", []),
        ]:
            document = generation_model()
            document["entries"][1][field] = value
            with self.subTest(field=field, value=value):
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))
        for lane in ("imported", "delivered", "rotated", "recovered", "retired"):
            document = generation_model()
            document["entries"][1]["lifecycle"][lane] = "CONFIRMED"
            document["entries"][1]["runtime_evidence"][lane] = EVIDENCE
            catalog.validate_catalog(document)
            self.assertFalse(catalog.generation_allowed(document, "TEST-001"))

    def test_action_disposition_policy_blocks_unauthorized_interpretations(self):
        for action in ("DELETE", "OUT_OF_SCOPE", "BLOCKED_FACTS"):
            document = generation_model()
            document["entries"][1]["action"] = action
            with self.subTest(action=action):
                self.assert_invalid(document)
        for action in ("NO_CHANGE", "VERIFY_RUNTIME"):
            document = generation_model()
            document["entries"][1]["action"] = action
            catalog.validate_catalog(document)
            with self.subTest(generation_action=action):
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))
        document = generation_model()
        entry = document["entries"][1]
        entry.update(
            classification="unused_delete",
            disposition="UNUSED_DELETE",
            consumers=[],
            consumer_status="DECLARED",
        )
        entry["destination_plan"]["kv_path"] = None
        entry["recovery"]["custody"] = "not_applicable"
        with self.subTest(case="unused_requires_delete"):
            self.assert_invalid(document)
        entry["action"] = "DELETE"
        catalog.validate_catalog(document)
        entry.update(
            scope="lab",
            classification="lab_excluded",
            disposition="LAB_EXCLUDED",
            action="NO_CHANGE",
        )
        with self.subTest(case="lab_requires_out_of_scope"):
            self.assert_invalid(document)
        entry["action"] = "OUT_OF_SCOPE"
        entry["consumers"] = ["infra/labs/docker-compose.yml"]
        catalog.validate_catalog(document)
        entry.update(
            scope="root",
            classification="kv_static",
            disposition="UNKNOWN_BLOCKED",
            consumer_status="BLOCKED_FACTS",
            action="NO_CHANGE",
        )
        with self.subTest(case="unknown_requires_blocked"):
            self.assert_invalid(document)
        entry["action"] = "BLOCKED_FACTS"
        catalog.validate_catalog(document)
        entry.update(disposition="RETAINED_FOR_RECOVERY", action="NO_CHANGE")
        catalog.validate_catalog(document)
        entry["action"] = "VERIFY_RUNTIME"
        with self.subTest(case="verify_requires_known_source"):
            self.assert_invalid(document)
        entry["consumer_status"] = "DECLARED"
        entry["consumers"] = ["infra/06-observability/docker-compose.yml"]
        catalog.validate_catalog(document)

    def test_declared_active_actions_require_nonempty_consumer_references(self):
        for action in ("IMPLEMENT", "VERIFY_RUNTIME", "NO_CHANGE"):
            document = generation_model()
            entry = document["entries"][1]
            entry.update(action=action, consumers=[])
            with self.subTest(action=action):
                self.assert_invalid(document)
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))

    def test_declared_empty_consumers_schema_and_library_parity(self):
        schema_path = CLI.parents[2] / catalog.SCHEMA_PATH
        schema = json.loads(schema_path.read_bytes())
        document = generation_model()
        entry = document["entries"][1]
        entry.update(
            scope="lab",
            classification="lab_excluded",
            disposition="LAB_EXCLUDED",
            action="OUT_OF_SCOPE",
            consumers=[],
        )
        entry["destination_plan"]["kv_path"] = None
        for validation_schema in (None, schema):
            with self.subTest(
                case="lab_declared_empty", schema=validation_schema is not None
            ):
                with self.assertRaises(catalog.CatalogError):
                    catalog.validate_catalog(document, validation_schema)
        entry.update(
            scope="root",
            classification="unused_delete",
            disposition="UNUSED_DELETE",
            action="DELETE",
        )
        entry["recovery"]["custody"] = "not_applicable"
        for validation_schema in (None, schema):
            with self.subTest(
                case="exact_unused_exception", schema=validation_schema is not None
            ):
                catalog.validate_catalog(document, validation_schema)
                self.assertFalse(catalog.generation_allowed(document, "TEST-001"))

    def test_generation_binding_matches_every_catalog_metadata_field(self):
        document = generation_model()
        source = "secrets/db/example/password.txt"
        self.assertTrue(
            catalog.generation_binding_allowed(document, "TEST-001", source, None, "O")
        )
        for args in [
            ("TEST-001", source, None, "X"),
            ("TEST-001", "secrets/db/other/password.txt", None, "O"),
            ("TEST-001", source, "UNAPPROVED_ENV", "O"),
            ("COMM-003", source, None, "O"),
            ("TEST-001", [], None, "O"),
            ([], source, None, "O"),
        ]:
            with self.subTest(
                argument_types=tuple(type(item).__name__ for item in args)
            ):
                self.assertFalse(catalog.generation_binding_allowed(document, *args))

    def test_recovery_lab_and_planned_contracts_fail_closed(self):
        document = deepcopy(self.document)
        extra = deepcopy(self.entry)
        extra.update(
            id="PG-020", source_path="secrets/db/legacy-app/service_password.txt"
        )
        document["entries"].append(extra)
        self.assert_invalid(document)
        extra["disposition"] = "RETAINED_FOR_RECOVERY"
        extra["destination_plan"]["kv_path"] = None
        catalog.validate_catalog(document)
        self.assertFalse(catalog.generation_allowed(document, "PG-020"))
        for field, value in [
            ("delivery", "READY"),
            ("kv_path", "../outside"),
            ("status", "FINAL"),
        ]:
            document = deepcopy(self.document)
            document["entries"][0]["destination_plan"][field] = value
            self.assert_invalid(document)
        for field, value in [
            ("history", "discard"),
            ("custody", []),
            ("status", "CONFIRMED"),
        ]:
            document = deepcopy(self.document)
            document["entries"][0]["recovery"][field] = value
            self.assert_invalid(document)
        document = deepcopy(self.document)
        document["entries"][0]["lifecycle"]["imported"] = []
        self.assert_invalid(document)

    def test_external_schema_reference_is_rejected_without_resolution(self):
        from jsonschema import Draft202012Validator

        with patch.object(
            Draft202012Validator,
            "iter_errors",
            side_effect=ValueError("synthetic-reference"),
        ) as resolver:
            with self.assertRaises(catalog.CatalogError):
                catalog.validate_catalog(
                    self.document, {"$ref": "https://example.invalid/unapproved"}
                )
            resolver.assert_not_called()

    def test_schema_failure_is_sanitized(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.validate_catalog(
                self.document, {"type": "object", "required": ["missing"]}
            )
        with self.assertRaises(catalog.CatalogError):
            catalog.validate_catalog(
                self.document, {"type": "invalid-sensitive-schema"}
            )


class SyntheticRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.document = model()
        family = self.root / ".agent-work"
        family.mkdir(mode=0o700)
        (family / "README.md").write_text("# 합성 작업 산출물\n")
        self.write_json(catalog.CATALOG_PATH, self.document)
        self.write_json(catalog.SCHEMA_PATH, {})
        self.write_json(catalog.SUPPORT_PATH, {})
        metadata = self.root / catalog.METADATA_PATH
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_bytes(PUBLIC)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "add",
                "--",
                catalog.CATALOG_PATH,
                catalog.SCHEMA_PATH,
                catalog.SUPPORT_PATH,
                catalog.METADATA_PATH,
            ],
            check=True,
        )

    def write_json(self, relative, value):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value))

    def cli(self, command, *arguments):
        result = subprocess.run(
            [sys.executable, str(CLI), "--root", str(self.root), command, *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertNotIn("synthetic-private-value", result.stdout + result.stderr)
        return result

    def test_load_and_stage_roundtrip_preserve_synthetic_private_state(self):
        private = self.root / "secrets/SENSITIVE_ENV_VARS.md"
        private.write_text("synthetic-private-value")
        environment = self.root / ".env"
        environment.write_text("NO_TOUCH=synthetic-private-value\n")
        before = (private.read_bytes(), environment.read_bytes())
        self.assertEqual(catalog.load_catalog(self.root), self.document)
        self.assertFalse(catalog.check_views(self.root))
        self.assertEqual(catalog.write_views(self.root), catalog.VIEW_NAMES)
        self.assertTrue(catalog.check_views(self.root))
        self.assertEqual((private.read_bytes(), environment.read_bytes()), before)
        view = self.root / catalog.OUTPUT_PATH / catalog.VIEW_NAMES[0]
        view.write_bytes(view.read_bytes() + b"drift\n")
        self.assertFalse(catalog.check_views(self.root))

    def test_generated_views_require_exact_private_mode(self):
        (self.root / ".agent-work/README.md").chmod(0o644)
        catalog.write_views(self.root)
        staging = self.root / catalog.OUTPUT_PATH
        for name in catalog.VIEW_NAMES:
            with self.subTest(name=name):
                view = staging / name
                view.chmod(0o644)
                try:
                    with self.assertRaises(catalog.CatalogError):
                        catalog.check_views(self.root)
                    with self.assertRaises(catalog.CatalogError):
                        catalog.write_views(self.root)
                finally:
                    view.chmod(0o600)

    def test_generated_views_are_private_under_restrictive_umask(self):
        catalog.write_views(self.root)
        staging = self.root / catalog.OUTPUT_PATH
        for name in catalog.VIEW_NAMES:
            (staging / name).unlink()
        previous = os.umask(0o777)
        try:
            catalog.write_views(self.root)
        finally:
            os.umask(previous)
        for name in catalog.VIEW_NAMES:
            self.assertEqual(stat.S_IMODE((staging / name).stat().st_mode), 0o600)

    def test_staging_requires_operator_owned_family_readme(self):
        readme = self.root / ".agent-work/README.md"
        readme.unlink()
        with self.assertRaises((ValueError, OSError)):
            catalog.write_views(self.root)
        self.assertFalse((self.root / catalog.OUTPUT_PATH).exists())
        readme.write_text("# 합성 작업 산출물\n")
        (self.root / ".agent-work").rename(self.root / "saved-family")
        with self.assertRaises((ValueError, OSError)):
            catalog.write_views(self.root)
        self.assertFalse((self.root / ".agent-work").exists())

    def test_cli_check_render_guard_and_drift(self):
        self.assertEqual(self.cli("check").returncode, 0)
        self.assertEqual(self.cli("check-views").returncode, 2)
        self.assertEqual(self.cli("render").returncode, 0)
        self.assertEqual(self.cli("check-views").returncode, 0)
        self.assertEqual(self.cli("check-generation", "COMM-002").returncode, 2)
        self.assertEqual(self.cli("check-generation", "COMM-003").returncode, 2)

    def test_load_rejects_public_source_drift_and_untracked_inputs(self):
        self.document["entries"][0]["purpose"] = "Different metadata purpose"
        self.write_json(catalog.CATALOG_PATH, self.document)
        with self.assertRaises(catalog.CatalogError):
            catalog.load_catalog(self.root)
        self.write_json(catalog.CATALOG_PATH, model())
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "rm",
                "--cached",
                "-q",
                "--",
                catalog.CATALOG_PATH,
            ],
            check=True,
        )
        with self.assertRaises(catalog.CatalogError):
            catalog.load_catalog(self.root)

    def test_load_rejects_duplicate_json_and_malformed_schema_without_leak(self):
        target = self.root / catalog.CATALOG_PATH
        target.write_text('{"entries": [], "entries": ["synthetic-private-value"]}')
        self.assertEqual(self.cli("check").returncode, 2)
        self.write_json(catalog.CATALOG_PATH, self.document)
        self.write_json(catalog.SCHEMA_PATH, {"type": "invalid-sensitive-schema"})
        self.assertEqual(self.cli("check").returncode, 2)

    def test_root_and_public_input_symlink_and_hardlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            alias = Path(tmp) / "alias"
            alias.symlink_to(self.root, target_is_directory=True)
            with self.assertRaises(ValueError):
                catalog.load_catalog(alias)
            target = self.root / catalog.CATALOG_PATH
            target.unlink()
            outside = Path(tmp) / "outside.json"
            outside.write_text("synthetic-private-value")
            target.symlink_to(outside)
            with self.assertRaises(OSError):
                catalog.load_catalog(self.root)
            target.unlink()
            self.write_json(catalog.CATALOG_PATH, self.document)
            os.link(target, outside.with_name("shared.json"))
            with self.assertRaises(ValueError):
                catalog.load_catalog(self.root)

    def test_staging_escape_symlinks_and_shared_inode_are_refused(self):
        with self.assertRaises(ValueError):
            catalog.write_views(self.root, self.root / "secrets")
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp)
            agent = self.root / ".agent-work"
            (agent / "README.md").unlink()
            agent.rmdir()
            agent.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(OSError):
                catalog.write_views(self.root)
            agent.unlink()
            agent.mkdir()
            (agent / "README.md").write_text("# 합성 작업 산출물\n")
            catalog.write_views(self.root)
            target = self.root / catalog.OUTPUT_PATH / catalog.VIEW_NAMES[0]
            target.unlink()
            untouched = outside / "private.txt"
            untouched.write_text("synthetic-private-value")
            target.symlink_to(untouched)
            with self.assertRaises(ValueError):
                catalog.write_views(self.root)
            with self.assertRaises(ValueError):
                catalog.check_views(self.root)
            self.assertEqual(untouched.read_text(), "synthetic-private-value")
            target.unlink()
            catalog.write_views(self.root)
            os.link(target, outside / "shared.md")
            with self.assertRaises(ValueError):
                catalog.write_views(self.root)

    def test_git_environment_override_does_not_change_catalog_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            overrides = {
                "GIT_DIR": str(Path(tmp) / ".git"),
                "GIT_INDEX_FILE": str(Path(tmp) / "index"),
            }
            with patch.dict(os.environ, overrides):
                self.assertEqual(catalog.load_catalog(self.root), self.document)

    def test_borrowed_root_fd_loads_catalog_from_held_inode(self):
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            fd_root = f"/proc/self/fd/{fd}"
            with patch.dict(os.environ, {"HYHOME_GENERATOR_HELD_ROOT": fd_root}):
                self.assertEqual(catalog.load_catalog(Path(fd_root)), self.document)
        finally:
            os.close(fd)

    def test_borrowed_root_fd_rejects_unmatched_held_root(self):
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                other_fd = os.open(tmp, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    with patch.dict(
                        os.environ,
                        {"HYHOME_GENERATOR_HELD_ROOT": f"/proc/self/fd/{other_fd}"},
                    ):
                        with self.assertRaises(catalog.CatalogError):
                            catalog.load_catalog(Path(f"/proc/self/fd/{fd}"))
                finally:
                    os.close(other_fd)
        finally:
            os.close(fd)

    def test_borrowed_root_fd_rejects_untracked_public_input(self):
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "rm",
                "--cached",
                "-q",
                "--",
                catalog.CATALOG_PATH,
            ],
            check=True,
        )
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            fd_root = f"/proc/self/fd/{fd}"
            with patch.dict(os.environ, {"HYHOME_GENERATOR_HELD_ROOT": fd_root}):
                with self.assertRaises(catalog.CatalogError):
                    catalog.load_catalog(Path(fd_root))
        finally:
            os.close(fd)

    def test_public_read_accepts_complete_short_chunks_and_rejects_short_eof(self):
        target = self.root / catalog.CATALOG_PATH
        expected = target.read_bytes()
        fd = os.open(target.parent, catalog.DIR_FLAGS)
        read = os.read
        try:
            with patch.object(
                catalog.os,
                "read",
                side_effect=lambda opened, length: read(opened, min(length, 2)),
            ):
                with self.subTest(case="complete_short_chunks"):
                    self.assertEqual(catalog_io._read_file(fd, target.name), expected)
            calls = 0

            def truncated(opened, length):
                nonlocal calls
                calls += 1
                return read(opened, 2) if calls == 1 else b""

            with patch.object(catalog.os, "read", side_effect=truncated):
                with (
                    self.subTest(case="premature_eof"),
                    self.assertRaises(catalog.CatalogError),
                ):
                    catalog_io._read_file(fd, target.name)
        finally:
            os.close(fd)

    def test_cli_generic_errors_do_not_expose_input(self):
        stdout, stderr = StringIO(), StringIO()
        with patch.object(
            catalog, "load_catalog", side_effect=OSError("synthetic-private-value")
        ):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = catalog.main(["--root", str(self.root), "check"])
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "P02_METADATA_BLOCKED\n")


if __name__ == "__main__":
    unittest.main()
