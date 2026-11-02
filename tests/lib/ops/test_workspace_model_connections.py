"""P03 model, Runner, and exact tool connection projections."""

from __future__ import annotations

import json
import unittest

from scripts.lib.ops._workspace_connection_sources import candidate_kind
from scripts.lib.ops._workspace_model_connections import policy_rows
from tests.lib.ops.test_workspace_connections import WorkspaceConnectionFixture


class WorkspaceModelConnectionTests(WorkspaceConnectionFixture, unittest.TestCase):
    def test_p03_ai_compose_connections_remain_source_only_and_value_free(self):
        webui = self.put(
            "infra/08-ai/open-webui/docker-compose.yml",
            """
services:
  open-webui:
    environment:
      OLLAMA_BASE_URL: http://ollama:${OLLAMA_PORT:-11434}
""",
        )
        notebook = self.put(
            "infra/08-ai/open-notebook/docker-compose.yml",
            """
services:
  open_notebook:
    environment:
      SURREAL_URL: ws://surrealdb:8000/rpc
      OLLAMA_API_BASE: http://ollama:${OLLAMA_PORT:-11434}
      SURREAL_USER: PRIVATE_USER
    secrets:
      - surreal_db_password
      - open_notebook_encryption_key
""",
        )
        exporter = self.put(
            "infra/08-ai/ollama/docker-compose.yml",
            """
services:
  ollama-exporter:
    environment:
      OLLAMA_HOST: ollama:${OLLAMA_PORT:-11434}
""",
        )
        result = self.inspect(webui, notebook, exporter)
        p03 = [row for row in result["connections"] if row["owner"] == "P03"]
        self.assertEqual(len(p03), 3)
        self.assertEqual(
            {(row["caller_roles"][0], row["provider"]) for row in p03},
            {
                ("open-webui", "ollama"),
                ("open_notebook", "ollama"),
                ("open_notebook", "surrealdb"),
            },
        )
        fallback = next(
            row
            for row in p03
            if row["reason"] == "environment-fallback-not-registration"
        )
        self.assertEqual(fallback["disposition"], "deferred")
        self.assertEqual(fallback["registration"]["actual_state"], "UNKNOWN")
        database = next(row for row in p03 if row["provider"] == "surrealdb")
        self.assertEqual(database["secret_refs"], ["surreal_db_password"])
        exporter_row = next(
            row
            for row in result["connections"]
            if row["caller_roles"] == ["ollama-exporter"]
        )
        self.assertEqual(exporter_row["owner"], "P07")
        self.assertEqual(
            {
                row["port_contract"]["service_dns"]["port"]
                for row in result["connections"]
            },
            {8000, 11434},
        )
        self.assertNotIn("PRIVATE_USER", json.dumps(result))

    def test_p03_runner_brokers_and_local_model_overlay_are_bounded_candidates(self):
        runners = self.put(
            "infra/07-workflow/n8n/docker-compose.yml",
            """
services:
  n8n-task-runner:
    environment:
      N8N_RUNNERS_TASK_BROKER_URI: http://n8n:${N8N_BROKER_PORT:-5679}
    secrets: [n8n_runner_auth_token]
  n8n-task-runner-worker:
    environment:
      N8N_RUNNERS_TASK_BROKER_URI: http://n8n-worker:${N8N_BROKER_PORT:-5679}
    secrets: [n8n_runner_auth_token]
""",
        )
        overlay = self.put(
            "infra/07-workflow/n8n/docker-compose.ollama-local.yml",
            """
services:
  n8n-worker:
    networks: {n8n_ollama_net: {}}
  ollama:
    networks: {n8n_ollama_net: {}}
networks:
  n8n_ollama_net: {internal: true}
""",
        )
        result = self.inspect(runners, overlay)
        broker_rows = [
            row
            for row in result["connections"]
            if row["reason"] == "external-runner-broker-source"
        ]
        self.assertEqual(len(broker_rows), 2)
        self.assertEqual(
            {row["provider"] for row in broker_rows}, {"n8n", "n8n-worker"}
        )
        self.assertEqual(
            {tuple(row["secret_refs"]) for row in broker_rows},
            {("n8n_runner_auth_token",)},
        )
        self.assertEqual(
            {row["port_contract"]["service_dns"]["port"] for row in broker_rows},
            {5679},
        )
        overlay_row = next(
            row
            for row in result["connections"]
            if row["reason"] == "network-reachability-not-registration"
        )
        self.assertEqual(overlay_row["caller_roles"], ["n8n-worker"])
        self.assertEqual(overlay_row["provider"], "ollama")
        self.assertEqual(overlay_row["disposition"], "deferred")
        self.assertEqual(
            overlay_row["port_contract"]["service_dns"],
            {"state": "unknown", "port": None},
        )

    def test_p03_model_policy_fixture_is_a_reference_not_stored_registration(self):
        policy = self.put(
            "tests/fixtures/p03_models/notebook-model-policy.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "target": "owned-isolated",
                    "provider": {
                        "name": "ollama",
                        "credential_name": "P03 Local Ollama",
                        "base_url": "http://ollama:11434",
                        "modalities": ["language", "embedding"],
                    },
                    "models": [
                        {"name": "gemma4:e2b", "type": "language", "default": "chat"},
                        {
                            "name": "embeddinggemma-2:740m",
                            "type": "embedding",
                            "dimensions": 768,
                            "default": "embedding",
                        },
                    ],
                }
            ),
        )
        result = self.inspect(policy)
        self.assertEqual(candidate_kind(policy["path"]), "model-policy")
        self.assertEqual(len(result["connections"]), 2)
        self.assertEqual(
            {row["reason"] for row in result["connections"]},
            {
                "owned-isolated-chat-model-policy",
                "owned-isolated-embedding-model-policy",
            },
        )
        for row in result["connections"]:
            self.assertEqual(
                row["source"], {"path": policy["path"], "sha256": policy["sha256"]}
            )
            self.assertEqual(
                row["registration"], {"level": "fixture", "actual_state": "UNKNOWN"}
            )
            self.assertEqual(row["disposition"], "deferred")
            self.assertEqual(row["provider"], "ollama")
            self.assertEqual(row["auth_kind"], "credential-reference")
            self.assertEqual(row["secret_refs"], [])
            self.assertEqual(
                row["port_contract"]["service_dns"],
                {"state": "declared", "port": 11434},
            )

    def test_p03_model_policy_rejects_wrong_provider_and_credential_bearing_url(self):
        base = {
            "schema_version": 1,
            "target": "owned-isolated",
            "provider": {
                "name": "ollama",
                "credential_name": "P03 Local Ollama",
                "base_url": "http://other-provider:11434",
                "modalities": ["language", "embedding"],
            },
            "models": [
                {"name": "gemma4:e2b", "type": "language", "default": "chat"},
                {
                    "name": "embeddinggemma-2:740m",
                    "type": "embedding",
                    "dimensions": 768,
                    "default": "embedding",
                },
            ],
        }
        wrong_host = self.put(
            "tests/fixtures/p03_models/notebook-model-policy.json",
            json.dumps(base),
        )
        result = self.inspect(wrong_host)
        self.assertEqual(result["connections"], [])
        self.assertEqual(result["connection_gaps"][0]["code"], "source-invalid")

        base["provider"]["base_url"] = "http://user:PRIVATE@ollama:11434"
        credential_url = self.put(
            "tests/fixtures/p03_models/notebook-model-policy.json",
            json.dumps(base),
        )
        result = self.inspect(credential_url)
        self.assertEqual(result["connections"], [])
        self.assertEqual(
            result["connection_gaps"][0]["code"],
            "credential-bearing-endpoint-refused",
        )
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertIsNone(
            candidate_kind("tests/fixtures/p03_models/notebook-model-policy-copy.json")
        )

        for invalid_url in (
            "file://ollama:11434",
            "https://ollama:11434",
            "http://ollama:11434/path",
            "ollama:11434",
        ):
            with self.subTest(invalid_url=invalid_url):
                base["provider"]["base_url"] = invalid_url
                invalid = self.put(
                    "tests/fixtures/p03_models/notebook-model-policy.json",
                    json.dumps(base),
                )
                result = self.inspect(invalid)
                self.assertEqual([], result["connections"])
                self.assertEqual("source-invalid", result["connection_gaps"][0]["code"])

    def test_p03_model_policy_schema_is_closed_and_fail_closed(self):
        valid = {
            "schema_version": 1,
            "target": "owned-isolated",
            "provider": {
                "name": "ollama",
                "credential_name": "P03 Local Ollama",
                "base_url": "http://ollama:11434",
                "modalities": ["language", "embedding"],
            },
            "models": [
                {"name": "gemma4:e2b", "type": "language", "default": "chat"},
                {
                    "name": "embeddinggemma-2:740m",
                    "type": "embedding",
                    "dimensions": 768,
                    "default": "embedding",
                },
            ],
        }
        candidates = []
        extra = json.loads(json.dumps(valid))
        extra["unexpected"] = True
        candidates.append(extra)
        for invalid_version in (True, 1.0, "1"):
            versioned = json.loads(json.dumps(valid))
            versioned["schema_version"] = invalid_version
            candidates.append(versioned)
        wrong_target = json.loads(json.dumps(valid))
        wrong_target["target"] = "HOME"
        candidates.append(wrong_target)
        provider_shape = json.loads(json.dumps(valid))
        provider_shape["provider"] = []
        candidates.append(provider_shape)
        modality = json.loads(json.dumps(valid))
        modality["provider"]["modalities"] = ["language"]
        candidates.append(modality)
        credential = json.loads(json.dumps(valid))
        credential["provider"]["credential_name"] = ["PRIVATE"]
        candidates.append(credential)
        for invalid_name in ("", " leading", "trailing ", "line\nbreak", "x" * 81):
            invalid_credential = json.loads(json.dumps(valid))
            invalid_credential["provider"]["credential_name"] = invalid_name
            candidates.append(invalid_credential)
        models_shape = json.loads(json.dumps(valid))
        models_shape["models"] = []
        candidates.append(models_shape)
        model_shape = json.loads(json.dumps(valid))
        model_shape["models"][0] = "gemma4:e2b"
        candidates.append(model_shape)
        model_keys = json.loads(json.dumps(valid))
        model_keys["models"][0]["dimensions"] = 768
        candidates.append(model_keys)
        for invalid_dimensions in (768.0, True, "768"):
            dimensions = json.loads(json.dumps(valid))
            dimensions["models"][1]["dimensions"] = invalid_dimensions
            candidates.append(dimensions)
        model_value = json.loads(json.dumps(valid))
        model_value["models"][0]["name"] = "unapproved"
        candidates.append(model_value)

        for index, candidate in enumerate(candidates):
            with self.subTest(index=index):
                row = self.put(
                    "tests/fixtures/p03_models/notebook-model-policy.json",
                    json.dumps(candidate),
                )
                result = self.inspect(row)
                self.assertEqual(result["connections"], [])
                self.assertEqual(
                    result["connection_gaps"],
                    [{"source": row["path"], "code": "source-invalid"}],
                )

    def test_p03_model_policy_direct_projection_rejects_float_dimensions(self):
        document = {
            "schema_version": 1,
            "target": "owned-isolated",
            "provider": {
                "name": "ollama",
                "credential_name": "P03 Local Ollama",
                "base_url": "http://ollama:11434",
                "modalities": ["language", "embedding"],
            },
            "models": [
                {"name": "gemma4:e2b", "type": "language", "default": "chat"},
                {
                    "name": "embeddinggemma-2:740m",
                    "type": "embedding",
                    "dimensions": 768.0,
                    "default": "embedding",
                },
            ],
        }
        with self.assertRaisesRegex(ValueError, "invalid model policy"):
            policy_rows(
                document,
                {"path": "tests/fixtures/p03_models/notebook-model-policy.json"},
                [],
                [],
                endpoint=lambda _: ("ollama", 11434, None),
                row=lambda *_: {},
            )

    def test_p03_compose_credential_endpoint_is_a_gap_without_value_echo(self):
        row = self.put(
            "infra/08-ai/open-webui/docker-compose.yml",
            """
services:
  open-webui:
    environment:
      OLLAMA_BASE_URL: http://user:PRIVATE@ollama:11434
""",
        )
        result = self.inspect(row)
        self.assertEqual(result["connections"], [])
        self.assertEqual(
            result["connection_gaps"],
            [{"source": row["path"], "code": "credential-bearing-endpoint-refused"}],
        )
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_p03_approved_tool_destination_alias_is_source_only(self):
        source = self.put(
            "infra/07-workflow/n8n/workloads/demo/hermes-plugin/tools.py",
            """
APPROVED_WEBHOOK_URL = "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion"
WEBHOOK_URL_DEFAULT = APPROVED_WEBHOOK_URL
PRIVATE_TOKEN = "not-collected"
""",
        )
        result = self.inspect(source)
        self.assertEqual(len(result["connections"]), 1)
        row = result["connections"][0]
        self.assertEqual(row["provider"], "n8n.hy.home.arpa")
        self.assertEqual(
            row["port_contract"]["service_dns"],
            {"state": "declared", "port": 443},
        )
        self.assertEqual(row["owner"], "P03")
        self.assertEqual(row["reason"], "approved-tool-destination-source")
        self.assertEqual(row["registration"]["level"], "sdk-only")
        self.assertEqual(row["registration"]["actual_state"], "UNKNOWN")
        self.assertNotIn("not-collected", json.dumps(result))

    def test_p03_approved_tool_alias_rejects_any_other_destination(self):
        for value in (
            "http://n8n.hy.home.arpa/webhook/hermes-blog-ingestion",
            "https://other.hy.home.arpa/webhook/hermes-blog-ingestion",
            "https://n8n.hy.home.arpa/webhook/other",
            "https://n8n.hy.home.arpa:8443/webhook/hermes-blog-ingestion",
        ):
            with self.subTest(value=value):
                source = self.put(
                    "infra/07-workflow/n8n/workloads/demo/hermes-plugin/tools.py",
                    f'APPROVED_WEBHOOK_URL = "{value}"\n'
                    "WEBHOOK_URL_DEFAULT = APPROVED_WEBHOOK_URL\n",
                )
                result = self.inspect(source)
                self.assertEqual([], result["connections"])
                self.assertEqual(
                    [
                        {
                            "source": source["path"],
                            "code": "endpoint-unresolved",
                        }
                    ],
                    result["connection_gaps"],
                )
                self.assertNotIn(value, json.dumps(result))
