"""P02 catalog acceptance against the issued public metadata and source boundaries."""

import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tests.validation.test_secret_metadata_sync import (
    compose_sources,
    interpolation_references,
    registry_rows,
)

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "infra/03-security/openbao/secret-catalog.json"
SCHEMA = ROOT / "infra/03-security/openbao/secret-catalog.schema.json"


class SecretCatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text())
        self.schema = json.loads(SCHEMA.read_text())

    def test_shared_n8n_account_keeps_its_own_identity_and_optional_consumers(self):
        entries = {row["id"]: row for row in self.catalog["entries"]}
        named = entries["CACHE-027"]
        self.assertEqual("secrets/db/mng-valkey/n8n_password.txt", named["source_path"])
        self.assertEqual("ACTIVE_KEEP", named["disposition"])
        self.assertIn(
            "infra/04-data/mng-db/docker-compose.n8n-acl.yml", named["consumers"]
        )
        self.assertIn("infra/07-workflow/n8n/docker-compose.yml", named["consumers"])
        self.assertEqual(
            "secrets/db/n8n-valkey/n8n_password.txt",
            entries["CACHE-009"]["source_path"],
        )
        self.assertNotEqual(entries["CACHE-007"]["source_path"], named["source_path"])
        self.assertIn(
            "infra/07-workflow/n8n/docker-compose.yml",
            entries["CACHE-007"]["consumers"],
        )

    def test_dedicated_monitors_have_three_distinct_optional_declared_identities(self):
        entries = {row["id"]: row for row in self.catalog["entries"]}
        for identifier, directory, leaf in (
            ("CACHE-028", "airflow-valkey", "07-workflow/airflow"),
            ("CACHE-029", "n8n-valkey", "07-workflow/n8n"),
            ("CACHE-030", "oauth2-valkey", "02-auth/oauth2-proxy"),
        ):
            with self.subTest(identifier=identifier):
                row = entries[identifier]
                self.assertEqual(
                    f"secrets/db/{directory}/monitor_password.txt", row["source_path"]
                )
                self.assertEqual(
                    [f"infra/{leaf}/docker-compose.monitor-acl.yml"],
                    row["consumers"],
                )
                self.assertEqual("DECLARED", row["consumer_status"])
                self.assertEqual("CONFIRMED", row["lifecycle"]["declared"])
                self.assertEqual("UNKNOWN", row["lifecycle"]["consumed"])
                self.assertEqual("BLOCKED_P01", row["destination_plan"]["delivery"])
        self.assertEqual(
            3, len({entries[f"CACHE-{n:03}"]["source_path"] for n in range(28, 31)})
        )

    def test_catalog_covers_issued_ids_without_renumbering_or_an_alias_value(self):
        issued = registry_rows(
            (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()
        )
        entries = {row["id"]: row for row in self.catalog["entries"]}
        self.assertEqual(set(issued), set(entries))
        self.assertEqual(len(entries), len(self.catalog["entries"]))
        for identifier, row in issued.items():
            self.assertEqual(
                row["path"] if row["path"] not in ("", "-") else None,
                entries[identifier]["source_path"],
            )
            self.assertEqual(
                row["env"] if row["env"] not in ("", "-") else None,
                entries[identifier]["env_key"],
            )
        self.assertNotIn("COMM-003", entries)
        self.assertEqual(
            entries["COMM-002"]["source_path"],
            "secrets/communication/smtp/smtp_password.txt",
        )
        self.assertIn(
            {"id": "COMM-003", "canonical_id": "COMM-002", "state": "source_retired"},
            self.catalog["aliases"],
        )

    def test_declared_public_environment_consumers_are_recorded(self):
        sources = compose_sources(ROOT)
        sources[".env.example"] = (ROOT / ".env.example").read_text()
        references = {
            path: {name for name, _ in interpolation_references(text)}
            for path, text in sources.items()
        }
        for entry in self.catalog["entries"]:
            if entry["scope"] == "lab" or entry["env_key"] is None:
                continue
            expected = {
                path for path, names in references.items() if entry["env_key"] in names
            }
            with self.subTest(identifier=entry["id"]):
                self.assertTrue(expected.issubset(set(entry["consumers"])))
                if expected:
                    self.assertEqual(entry["consumer_status"], "DECLARED")

    def test_generator_htpasswd_inputs_are_declared_consumers(self):
        generator = ROOT / "scripts/operations/gen-secrets.sh"
        calls = re.findall(
            r'^    process_htpasswd "([^"\n]+)" "([^"\n]+)" "([^"\n]+)"',
            generator.read_text(),
            re.MULTILINE,
        )
        self.assertTrue(calls)
        entries = {row["id"]: row for row in self.catalog["entries"]}
        for identifier in {identifier for call in calls for identifier in call}:
            with self.subTest(identifier=identifier):
                self.assertIn(
                    "scripts/operations/gen-secrets.sh",
                    entries[identifier]["consumers"],
                )
                self.assertEqual(entries[identifier]["consumer_status"], "DECLARED")

    def test_schema_rejects_contradictory_action_authority(self):
        validator = Draft202012Validator(self.schema)
        for scenario in (
            "active_delete",
            "root_out_of_scope",
            "unused_no_change",
            "lab_implement",
        ):
            candidate = copy.deepcopy(self.catalog)
            row = next(item for item in candidate["entries"] if item["id"] == "PG-001")
            if scenario == "active_delete":
                row["action"] = "DELETE"
            elif scenario == "root_out_of_scope":
                row["action"] = "OUT_OF_SCOPE"
            elif scenario == "lab_implement":
                row = next(
                    item for item in candidate["entries"] if item["scope"] == "lab"
                )
                row["action"] = "IMPLEMENT"
            else:
                row.update(
                    classification="unused_delete",
                    disposition="UNUSED_DELETE",
                    consumers=[],
                    consumer_status="BLOCKED_FACTS",
                    action="NO_CHANGE",
                )
                row["destination_plan"]["kv_path"] = None
            with self.subTest(scenario=scenario):
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_schema_requires_a_named_declared_consumer(self):
        validator = Draft202012Validator(self.schema)
        for action in ("IMPLEMENT", "VERIFY_RUNTIME", "NO_CHANGE"):
            candidate = copy.deepcopy(self.catalog)
            row = next(item for item in candidate["entries"] if item["id"] == "PG-001")
            row.update(action=action, consumers=[], consumer_status="DECLARED")
            with self.subTest(action=action):
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_production_library_schema_and_view_roundtrip_agree(self):
        from scripts.lib.ops.secret_catalog import (
            load_catalog,
            parse_public_table,
            render_views,
        )

        loaded = load_catalog(ROOT)
        self.assertEqual(loaded, self.catalog)
        rendered = render_views(loaded)
        original = parse_public_table(
            (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_bytes()
        )
        self.assertEqual(
            parse_public_table(rendered["SENSITIVE_ENV_VARS.md.example"]), original
        )
        self.assertIn("README.md", rendered)

    def test_closed_schema_rejects_sensitive_fields_at_every_metadata_boundary(self):
        Draft202012Validator.check_schema(self.schema)
        validator = Draft202012Validator(self.schema)
        validator.validate(self.catalog)
        for target in (
            "top",
            "entry",
            "destination_plan",
            "recovery",
            "lifecycle",
            "alias",
        ):
            with self.subTest(target=target):
                candidate = copy.deepcopy(self.catalog)
                if target == "top":
                    item = candidate
                elif target == "entry":
                    item = candidate["entries"][0]
                elif target == "alias":
                    item = candidate["aliases"][0]
                else:
                    item = candidate["entries"][0][target]
                item["value"] = "synthetic-forbidden"
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_full_reference_metadata_is_present_without_runtime_authority(self):
        for row in self.catalog["entries"]:
            self.assertEqual(row["owner"], "@buenhyden")
            self.assertIn(
                row["action"],
                {
                    "NO_CHANGE",
                    "IMPLEMENT",
                    "VERIFY_RUNTIME",
                    "DELETE",
                    "BLOCKED_FACTS",
                    "OUT_OF_SCOPE",
                },
            )
            self.assertTrue(row["evidence_ref"].startswith("docs/03.specs/0204-"))
            for field in ("mount", "field", "uid", "gid", "mode"):
                self.assertIsNone(row["destination_plan"][field])
            for field in ("restart", "rotation"):
                self.assertEqual(row["destination_plan"][field], "BLOCKED_P01")
            self.assertTrue(
                all(value is None for value in row["runtime_evidence"].values())
            )

    def test_schema_refuses_crypto_delete_and_nonstatic_or_recovery_kv_plans(self):
        validator = Draft202012Validator(self.schema)
        for scenario in ("crypto_delete", "recovery_kv", "nonstatic_kv"):
            candidate = copy.deepcopy(self.catalog)
            if scenario == "crypto_delete":
                row = next(
                    item for item in candidate["entries"] if item["id"] == "AUTO-003"
                )
                row["disposition"] = "UNUSED_DELETE"
                row["consumers"] = []
            elif scenario == "recovery_kv":
                row = next(
                    item for item in candidate["entries"] if item["id"] == "PG-020"
                )
                row["destination_plan"]["kv_path"] = "secret/planned/forbidden"
            else:
                row = next(
                    item for item in candidate["entries"] if item["id"] == "INFRA-003"
                )
                row["destination_plan"]["kv_path"] = "secret/planned/forbidden"
            with self.subTest(scenario=scenario):
                self.assertTrue(list(validator.iter_errors(candidate)))

    def test_catalog_preserves_recovery_and_lab_without_runtime_acceptance_claims(self):
        for entry in self.catalog["entries"]:
            self.assertIn("source_recorded_at", entry)
            self.assertNotIn("reviewed_at", entry)
            self.assertEqual(entry["destination_plan"]["status"], "BLOCKED_P01")
            self.assertEqual(entry["destination_plan"]["acl"], "BLOCKED_P01")
            for lane in ("observed", "consumed"):
                self.assertEqual(entry["lifecycle"][lane], "UNKNOWN")
            for lane in ("imported", "delivered", "rotated", "recovered", "retired"):
                self.assertEqual(entry["lifecycle"][lane], "NOT_RUN")
            if entry["id"].startswith("LAB-"):
                self.assertEqual(entry["classification"], "lab_excluded")
                self.assertEqual(entry["disposition"], "LAB_EXCLUDED")
                self.assertIsNone(entry["destination_plan"]["kv_path"])
            if entry["id"].startswith("BKP-") or entry["id"] == "SEC-003":
                self.assertEqual(entry["recovery"]["custody"], "independent_required")
                self.assertEqual(entry["disposition"], "RETAINED_FOR_RECOVERY")
                self.assertIsNone(entry["destination_plan"]["kv_path"])
            if entry["id"] == "PG-020":
                self.assertEqual(entry["disposition"], "RETAINED_FOR_RECOVERY")


if __name__ == "__main__":
    unittest.main()
