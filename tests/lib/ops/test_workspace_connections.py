"""Value-minimizing public connection census; no runtime or private state."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops._workspace_connection_sources import (
    candidate_kind,
    public_source_path,
)
from scripts.lib.ops._workspace_connections import (
    ConnectionInventoryError,
    inspect_connections,
    validate_connections,
)
from scripts.lib.ops.port_inventory import project
from scripts.lib.ops.workspace_inventory import InventoryError, compare, scan


class WorkspaceConnectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="p02 connections ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, relative: str, body: str) -> dict:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        raw = body.encode()
        return {
            "path": relative,
            "state": "HASHED",
            "sha256": hashlib.sha256(raw).hexdigest(),
        }

    def inspect(self, *rows):
        return inspect_connections(self.root, list(rows), services=[])

    def test_source_handler_api_closes_candidate_and_public_path_boundaries(self):
        self.assertEqual(
            candidate_kind("infra/demo/docker-compose.yml"),
            "compose",
        )
        self.assertEqual(
            candidate_kind("infra/12-analytics/superset/docker-compose.yml"),
            "compose",
        )
        self.assertIsNone(candidate_kind("infra/demo/README.md"))
        self.assertTrue(public_source_path("infra/demo/docker-compose.yml"))
        self.assertFalse(public_source_path("secrets/docker-compose.yml"))
        self.assertFalse(public_source_path("../infra/demo/docker-compose.yml"))

    def test_compose_allowlist_extracts_redisinsight_and_kafbat_without_values(self):
        row = self.put(
            "infra/connections/docker-compose.yml",
            """
services:
  redisinsight:
    environment:
      RI_REDIS_HOST1: mng-valkey
      RI_REDIS_PORT1: '6381'
      RI_REDIS_USERNAME1: mnginspector
      RI_REDIS_PASSWORD1: PRIVATE_LITERAL_MARKER
    secrets: [mng_valkey_inspector_password]
  kafbat-ui:
    environment:
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: '${KAFKA_BOOTSTRAP_SERVERS:-kafka-1:19092}'
      KAFKA_CLUSTERS_0_SCHEMAREGISTRY: 'http://schema-registry:8081'
      KAFKA_CLUSTERS_0_KAFKACONNECT_0_ADDRESS: 'http://kafka-connect:8083'
""",
        )
        result = self.inspect(row)
        ids = {item["id"] for item in result["connections"]}
        self.assertEqual(len(ids), 4)
        redis = next(
            item for item in result["connections"] if item["provider"] == "mng-valkey"
        )
        self.assertEqual(
            redis["port_contract"]["service_dns"], {"state": "declared", "port": 6381}
        )
        self.assertEqual(redis["secret_refs"], ["mng_valkey_inspector_password"])
        self.assertEqual(redis["registration"]["actual_state"], "UNKNOWN")
        rendered = json.dumps(result)
        self.assertNotIn("PRIVATE_LITERAL_MARKER", rendered)
        self.assertNotIn("KAFKA_BOOTSTRAP_SERVERS", rendered)
        validate_connections(result, public_files=[row])

    def test_superset_metadata_and_provision_connections_use_declared_mng_port(self):
        row = self.put(
            "infra/12-analytics/superset/docker-compose.yml",
            """
services:
  superset:
    environment:
      SUPERSET_DB_HOST: mng-pg
      SUPERSET_DB_PORT: '${POSTGRES_PORT:-5544}'
      SUPERSET_DB_USER: PRIVATE_USER_VALUE
    secrets: [superset_db_password, superset_secret_key]
    command:
      - "superset set-database-uri --database_name lakehouse --uri 'trino://superset@trino:8080/lakehouse'"
  superset-db-provision:
    environment:
      PGHOST: mng-pg
      PGPORT: '${POSTGRES_PORT:-5544}'
      PGUSER: PRIVATE_ADMIN_VALUE
    secrets: [mng_postgres_password, superset_db_password]
  superset-refused:
    environment:
      SUPERSET_DB_HOST: 'user:PRIVATE_PASSWORD@mng-pg'
      SUPERSET_DB_PORT: '5544'
    secrets: [superset_db_password]
""",
        )
        result = self.inspect(row)
        superset_rows = [
            connection
            for connection in result["connections"]
            if connection["reason"].startswith("superset-")
        ]
        self.assertEqual(len(superset_rows), 3)
        self.assertEqual(
            {connection["caller_roles"][0] for connection in superset_rows},
            {"superset", "superset-db-provision"},
        )
        self.assertEqual(
            {
                connection["port_contract"]["service_dns"]["port"]
                for connection in superset_rows
            },
            {5544, 8080},
        )
        self.assertEqual(
            {tuple(connection["secret_refs"]) for connection in superset_rows},
            {(), ("superset_db_password",), ("mng_postgres_password",)},
        )
        self.assertEqual(
            {
                connection["registration"]["actual_state"]
                for connection in superset_rows
            },
            {"UNKNOWN"},
        )
        self.assertEqual(
            {connection["registration"]["level"] for connection in superset_rows},
            {"source-declared"},
        )
        self.assertEqual(
            {connection["provider"] for connection in superset_rows},
            {"mng-pg", "trino"},
        )
        self.assertIn(
            "credential-bearing-endpoint-refused",
            {gap["code"] for gap in result["connection_gaps"]},
        )
        rendered = json.dumps(result)
        for forbidden in (
            "PRIVATE_USER_VALUE",
            "PRIVATE_ADMIN_VALUE",
            "PRIVATE_PASSWORD",
        ):
            self.assertNotIn(forbidden, rendered)

    def test_grafana_provisioning_records_source_registration_and_secret_name_only(
        self,
    ):
        row = self.put(
            "infra/06-observability/grafana/provisioning/datasources/datasource.yml",
            """
apiVersion: 1
datasources:
  - name: Operations DB
    uid: operations-db
    type: grafana-postgresql-datasource
    access: proxy
    url: mng-pg:5544
    user: ${GRAFANA_DB_READER_USER}
    secureJsonData:
      password: $__file{/run/secrets/grafana_reader_password}
  - name: Metrics
    uid: metrics
    type: prometheus
    access: proxy
    url: http://prometheus:9090
  - name: Deferred Port
    uid: deferred-port
    type: postgres
    access: proxy
    url: mng-pg:${POSTGRES_PORT}
""",
        )
        result = self.inspect(row)
        database = next(
            item
            for item in result["connections"]
            if item["id"].endswith("grafana:operations-db")
        )
        self.assertEqual(database["secret_refs"], ["grafana_reader_password"])
        self.assertEqual(database["registration"]["level"], "provisioned-source")
        self.assertEqual(database["disposition"], "adopted")
        deferred = next(
            item
            for item in result["connections"]
            if item["id"].endswith("grafana:deferred-port")
        )
        self.assertEqual(deferred["provider"], "mng-pg")
        self.assertEqual(
            deferred["port_contract"]["service_dns"],
            {"state": "unknown", "port": None},
        )
        self.assertIn(
            "endpoint-unresolved", {gap["code"] for gap in result["connection_gaps"]}
        )
        self.assertNotIn("GRAFANA_DB_READER_USER", json.dumps(result))
        self.assertNotIn("POSTGRES_PORT", json.dumps(result))

    def test_airflow_examples_and_inactive_n8n_workflows_stay_deferred(self):
        airflow = self.put(
            "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json",
            json.dumps({"host": "dev-pg", "port": 5432, "password": "PRIVATE"}),
        )
        n8n = self.put(
            "infra/07-workflow/n8n/workloads/demo/workflow.json",
            json.dumps(
                {
                    "name": "Demo",
                    "active": False,
                    "nodes": [
                        {
                            "id": "send",
                            "type": "n8n-nodes-base.httpRequest",
                            "parameters": {
                                "url": "http://provider:8787/private-path",
                                "authentication": "genericCredentialType",
                            },
                            "credentials": {
                                "httpHeaderAuth": {
                                    "id": "PRIVATE_ID",
                                    "name": "PRIVATE_NAME",
                                }
                            },
                        }
                    ],
                }
            ),
        )
        result = self.inspect(airflow, n8n)
        self.assertEqual(
            {row["disposition"] for row in result["connections"]}, {"deferred"}
        )
        self.assertEqual(
            {row["registration"]["level"] for row in result["connections"]},
            {"fixture", "inactive-workflow-source"},
        )
        self.assertIn(
            "httpHeaderAuth",
            {r for row in result["connections"] for r in row["secret_refs"]},
        )
        rendered = json.dumps(result)
        for forbidden in ("PRIVATE", "private-path"):
            self.assertNotIn(forbidden, rendered)

    def test_malformed_duplicate_yaml_and_credential_endpoint_are_safe_gaps(self):
        duplicate = self.put(
            "infra/demo/docker-compose.yml",
            "services:\n  app: {image: one}\n  app: {image: two}\n",
        )
        credential = self.put(
            "infra/06-observability/grafana/provisioning/datasources/bad.yml",
            "datasources:\n  - {name: bad, uid: bad, type: prometheus, url: 'https://user:PRIVATE@host:9090/path?token=PRIVATE'}\n",
        )
        result = self.inspect(duplicate, credential)
        self.assertEqual(result["connections"], [])
        self.assertEqual(
            {gap["code"] for gap in result["connection_gaps"]},
            {"duplicate-key", "credential-bearing-endpoint-refused"},
        )
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_duplicate_json_key_is_a_fixed_gap_without_copying_values(self):
        row = self.put(
            "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json",
            '{"host":"dev-pg","host":"PRIVATE_MARKER","port":5432}',
        )
        result = self.inspect(row)
        self.assertEqual(result["connections"], [])
        self.assertEqual(result["connection_gaps"][0]["code"], "duplicate-key")
        self.assertNotIn("PRIVATE_MARKER", json.dumps(result))

    def test_list_environment_and_projected_four_port_locations_remain_distinct(self):
        row = self.put(
            "infra/demo/docker-compose.yml",
            """
services:
  redisinsight:
    environment:
      - RI_REDIS_HOST1=mng-valkey
      - RI_REDIS_PORT1=6379
      - RI_REDIS_USERNAME1=inspector
      - INVALID
    secrets:
      - {source: mng_valkey_inspector_password, target: password}
""",
        )
        projected = project(
            {
                "services": {
                    "mng-valkey": {
                        "ports": ["127.0.0.1:16379:6379"],
                        "labels": {
                            "traefik.enable": "true",
                            "traefik.http.services.mng.loadbalancer.server.port": "6379",
                        },
                    }
                }
            }
        )["services"][0]
        result = inspect_connections(
            self.root,
            [row],
            services=[{"service": "mng-valkey", "ports": projected}],
        )
        contract = result["connections"][0]["port_contract"]
        self.assertEqual(contract["listener"], {"state": "unknown", "port": None})
        self.assertEqual(contract["service_dns"], {"state": "declared", "port": 6379})
        self.assertEqual(
            contract["host_publication"], {"state": "declared", "port": 16379}
        )
        self.assertEqual(
            contract["gateway_backend"], {"state": "unknown", "port": 6379}
        )

    def test_bad_endpoint_shapes_are_counted_without_partial_rows_or_values(self):
        row = self.put(
            "infra/06-observability/grafana/provisioning/datasources/bad.yml",
            """
datasources:
  - {uid: query, url: 'http://provider:9090/path?token=PRIVATE'}
  - {uid: port, url: 'provider:99999'}
  - {uid: unresolved, url: '${NO_DEFAULT}'}
  - [not, a, datasource]
""",
        )
        result = self.inspect(row)
        self.assertEqual(result["connections"], [])
        self.assertEqual(
            {gap["code"] for gap in result["connection_gaps"]},
            {"endpoint-query-refused", "endpoint-port-invalid", "endpoint-unresolved"},
        )
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_active_n8n_source_is_never_promoted_to_stored_registration(self):
        row = self.put(
            "infra/07-workflow/n8n/workloads/demo/workflow.json",
            json.dumps(
                {
                    "active": True,
                    "nodes": [
                        "invalid",
                        {"type": "n8n-nodes-base.code", "parameters": {}},
                        {
                            "type": "n8n-nodes-base.httpRequest",
                            "parameters": {"url": "http://provider:8787/path"},
                        },
                    ],
                }
            ),
        )
        result = self.inspect(row)
        connection = result["connections"][0]
        self.assertEqual(connection["registration"]["level"], "source-declared")
        self.assertEqual(connection["registration"]["actual_state"], "UNKNOWN")
        self.assertEqual(connection["auth_kind"], "unknown")
        self.assertEqual(connection["disposition"], "deferred")

    def test_n8n_custom_node_policy_and_source_url_are_sdk_only_candidates(self):
        node = self.put(
            "infra/07-workflow/n8n/workloads/demo/nodes/Opsflow.node.ts",
            "credentials: [{ name: 'smtp', required: true }],\n",
        )
        policy = self.put(
            "infra/07-workflow/n8n/workloads/demo/nodes/transport.ts",
            "export const POLICY = Object.freeze({ host: 'mailpit', port: 1025 });\n",
        )
        source_url = self.put(
            "infra/07-workflow/n8n/workloads/demo/hermes-plugin/tools.py",
            'WEBHOOK_URL_DEFAULT = "https://n8n.local/webhook/private-path"\n',
        )
        result = self.inspect(node, policy, source_url)
        self.assertEqual(len(result["connections"]), 3)
        self.assertEqual(
            {row["registration"]["level"] for row in result["connections"]},
            {"sdk-only"},
        )
        self.assertEqual(
            {row["registration"]["actual_state"] for row in result["connections"]},
            {"UNKNOWN"},
        )
        self.assertIn(
            "smtp",
            {ref for row in result["connections"] for ref in row["secret_refs"]},
        )
        self.assertEqual(
            {row["provider"] for row in result["connections"]},
            {None, "mailpit", "n8n.local"},
        )
        self.assertNotIn("private-path", json.dumps(result))
        self.assertEqual(
            result["connection_coverage"],
            {
                "candidate_sources": 3,
                "parsed_sources": 3,
                "extracted_sources": 3,
                "unhandled_sources": 0,
                "connection_rows": 3,
            },
        )

    def test_external_symlink_and_changed_source_are_refused(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.write_text("datasources: []\n")
        self.addCleanup(outside.unlink)
        linked = (
            self.root
            / "infra/06-observability/grafana/provisioning/datasources/link.yml"
        )
        linked.parent.mkdir(parents=True)
        linked.symlink_to(outside)
        link_row = {
            "path": linked.relative_to(self.root).as_posix(),
            "state": "HASHED",
            "sha256": hashlib.sha256(outside.read_bytes()).hexdigest(),
        }
        with self.assertRaises(ConnectionInventoryError):
            self.inspect(link_row)

        row = self.put(
            "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json",
            '{"host":"dev-pg","port":5432}',
        )
        (self.root / row["path"]).write_text('{"host":"changed","port":5432}')
        with self.assertRaises(ConnectionInventoryError):
            self.inspect(row)

    def test_validator_rejects_open_rows_duplicates_and_false_registration(self):
        row = self.put(
            "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json",
            '{"host":"dev-pg","port":5432}',
        )
        document = self.inspect(row)
        mutations = []
        with_extra = json.loads(json.dumps(document))
        with_extra["connections"][0]["raw_url"] = "http://PRIVATE"
        mutations.append(with_extra)
        duplicate = json.loads(json.dumps(document))
        duplicate["connections"].append(duplicate["connections"][0])
        mutations.append(duplicate)
        claimed = json.loads(json.dumps(document))
        claimed["connections"][0]["registration"]["actual_state"] = "PASS"
        mutations.append(claimed)
        bad_source = json.loads(json.dumps(document))
        bad_source["connections"][0]["source"]["sha256"] = "bad"
        mutations.append(bad_source)
        bad_port = json.loads(json.dumps(document))
        bad_port["connections"][0]["port_contract"]["listener"]["port"] = 70000
        mutations.append(bad_port)
        bad_auth = json.loads(json.dumps(document))
        bad_auth["connections"][0]["auth_kind"] = "password-value"
        mutations.append(bad_auth)
        bad_caller = json.loads(json.dumps(document))
        bad_caller["connections"][0]["caller_roles"] = ["bad/value"]
        mutations.append(bad_caller)
        bad_provider = json.loads(json.dumps(document))
        bad_provider["connections"][0]["provider"] = "user@provider"
        mutations.append(bad_provider)
        bad_identity = json.loads(json.dumps(document))
        bad_identity["connections"][0]["id"] = ""
        mutations.append(bad_identity)
        bad_source_list = json.loads(json.dumps(document))
        bad_source_list["connection_sources"].append(
            bad_source_list["connection_sources"][0]
        )
        mutations.append(bad_source_list)
        bad_provenance = json.loads(json.dumps(document))
        bad_provenance["connections"][0]["source"]["path"] = "other.json"
        mutations.append(bad_provenance)
        bad_gap = json.loads(json.dumps(document))
        bad_gap["connection_gaps"] = [{"source": "x", "code": "PRIVATE_VALUE"}]
        mutations.append(bad_gap)
        bad_coverage = json.loads(json.dumps(document))
        bad_coverage["connection_coverage"]["connection_rows"] = 99
        mutations.append(bad_coverage)
        for candidate in mutations:
            with (
                self.subTest(candidate=candidate),
                self.assertRaises(ConnectionInventoryError),
            ):
                validate_connections(candidate, public_files=[row])

        forged = json.loads(json.dumps(document))
        forged_source = {
            "path": "secrets/docker-compose.yml",
            "sha256": "f" * 64,
            "state": "HASHED",
        }
        forged["connection_sources"] = [
            {
                "path": forged_source["path"],
                "sha256": forged_source["sha256"],
                "kind": "compose",
                "result": "extracted",
            }
        ]
        forged["connections"][0]["source"] = {
            "path": forged_source["path"],
            "sha256": forged_source["sha256"],
        }
        forged["connection_coverage"] = {
            "candidate_sources": 1,
            "parsed_sources": 1,
            "extracted_sources": 1,
            "unhandled_sources": 0,
            "connection_rows": 1,
        }
        with self.assertRaises(ConnectionInventoryError):
            validate_connections(forged, public_files=[forged_source])

        forged_gap = json.loads(json.dumps(document))
        forged_gap["connection_gaps"] = [
            {
                "source": "infra/forged/docker-compose.yml",
                "code": "endpoint-unresolved",
            }
        ]
        with self.assertRaises(ConnectionInventoryError):
            validate_connections(forged_gap, public_files=[row])

        inconsistent = json.loads(json.dumps(document))
        inconsistent["connection_sources"][0]["result"] = "partial"
        with self.assertRaises(ConnectionInventoryError):
            validate_connections(inconsistent, public_files=[row])

    def test_scan_flag_is_optional_and_compare_invalidates_only_dependent_rows(self):
        path = "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json"
        first = self.put(path, '{"host":"dev-pg","port":5432}')
        plain, _ = scan(self.root, public_paths=[path])
        self.assertNotIn("connections", plain)
        before, _ = scan(self.root, public_paths=[path], connections=True)
        self.assertEqual(before["connections"][0]["source"]["sha256"], first["sha256"])
        self.put(path, '{"host":"dev-pg","port":5544}')
        after, _ = scan(self.root, public_paths=[path], connections=True)
        difference = compare(before, after)
        self.assertEqual(
            difference["invalidated_connections"], [before["connections"][0]["id"]]
        )
        self.assertEqual(
            difference["changed_connections"], [before["connections"][0]["id"]]
        )

    def test_scan_translates_connection_race_to_fixed_inventory_error(self):
        path = "infra/07-workflow/airflow/workloads/demo/fixtures/pg-connection.example.json"
        self.put(path, '{"host":"dev-pg","port":5432}')
        with patch(
            "scripts.lib.ops._workspace_connections.inspect_connections",
            side_effect=ConnectionInventoryError("PRIVATE_DETAIL"),
        ):
            with self.assertRaisesRegex(
                InventoryError, r"^Connection inventory failed\.$"
            ):
                scan(self.root, public_paths=[path], connections=True)


if __name__ == "__main__":
    unittest.main()
