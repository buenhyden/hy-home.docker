"""Offline contracts for the ancillary probe and actual n8n Worker model flow."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.validation._opsflow_native_inputs import N8N_ID
from tests.validation._p03_notebook_native import NOTEBOOK_IMAGE
from tests.validation._p03_worker_model_native import (
    WorkerModelNativeRehearsal,
    build_worker_model_workflow,
    normalize_execution_id,
    worker_model_native_selection,
)
from tests.validation._p03_worker_ollama_fixture import WorkerOllamaFixture


class WorkerModelSourceTests(unittest.TestCase):
    def test_worker_image_probe_is_truthful_internal_and_pull_free(self):
        expected = {
            "actor": "n8n-worker-image-protocol-probe",
            "chat_model": "gemma4:e2b",
            "embedding_model": "embeddinggemma-2:740m",
            "embedding_dimensions": 768,
            "queue_workflow_claimed": False,
            "live_model_inference_claimed": False,
        }

        class FakeOwned:
            def __init__(self):
                self.calls = []
                self.identities = {}

            def verify_local_engine(self):
                self.calls.append(("engine",))

            def image_cached(self, image):
                self.calls.append(("image", image))
                return True

            def create_network(self, name):
                self.calls.append(("network", name))
                return "network-id"

            def create_container(self, name, *arguments):
                self.calls.append(("container", name, arguments))
                self.identities[name] = "id-" + name

            def container_id(self, name):
                return self.identities[name]

            def command(self, *arguments, timeout=30):
                self.calls.append(("command", arguments, timeout))
                return json.dumps(expected) if arguments[0] == "logs" else ""

            def cleanup(self):
                self.calls.append(("cleanup",))

        fixture = WorkerOllamaFixture()
        owned = FakeOwned()
        fixture._owned = owned
        selected = {
            "P03_WORKER_OLLAMA_NATIVE_REHEARSAL": "1",
            "P03_WORKER_OLLAMA_NATIVE_CONTEXT": "default",
        }
        with patch.dict(os.environ, selected, clear=True):
            receipt = fixture.run()

        self.assertEqual(receipt, expected)
        self.assertIn(("image", N8N_ID), owned.calls)
        self.assertIn(("image", NOTEBOOK_IMAGE), owned.calls)
        probe_create = next(
            call for call in owned.calls if call[0] == "container" and N8N_ID in call[2]
        )
        self.assertIn("no-new-privileges:true", probe_create[2])
        self.assertIn("OLLAMA_HOST=http://ollama:11434", probe_create[2])

    def test_worker_queue_workflow_is_active_http_model_work_not_a_probe(self):
        workflow = build_worker_model_workflow("P03 worker model synthetic")
        self.assertEqual(workflow["active"], False)
        self.assertEqual(workflow["settings"]["saveManualExecutions"], True)
        nodes = {node["name"]: node for node in workflow["nodes"]}
        request = nodes["Controlled Ollama Chat"]
        self.assertEqual(request["type"], "n8n-nodes-base.httpRequest")
        self.assertEqual(
            request["parameters"]["url"], "http://127.0.0.1:11434/api/chat"
        )
        self.assertIn("gemma4:e2b", request["parameters"]["jsonBody"])
        self.assertNotIn("embeddinggemma", request["parameters"]["jsonBody"])
        headers = request["parameters"]["headerParameters"]["parameters"]
        self.assertEqual(
            headers,
            [{"name": "X-P03-Execution-Id", "value": "={{ $execution.id }}"}],
        )
        self.assertNotIn("credentials", request)

    def test_worker_queue_workflow_rejects_unbounded_or_controlled_names(self):
        for name in ("", "x" * 129, "bad\nname"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                build_worker_model_workflow(name)

    def test_worker_queue_native_selection_is_explicit_and_exact(self):
        selected = {
            "P03_WORKER_MODEL_NATIVE_REHEARSAL": "1",
            "OPSFLOW_N8N_NATIVE_IMAGE": N8N_ID,
            "OPSFLOW_N8N_NATIVE_CONTEXT": "default",
        }
        self.assertEqual(worker_model_native_selection(selected), "default")
        for rejected in (
            {},
            {**selected, "DOCKER_HOST": "tcp://external.invalid"},
            {**selected, "OPSFLOW_N8N_NATIVE_IMAGE": "sha256:" + "0" * 64},
        ):
            with self.subTest(rejected=rejected), self.assertRaises(ValueError):
                worker_model_native_selection(rejected)

    def test_worker_queue_execution_id_normalizes_only_bounded_safe_values(self):
        self.assertEqual(normalize_execution_id(42), "42")
        self.assertEqual(normalize_execution_id("abc_42"), "abc_42")
        for rejected in (True, 0, -1, "", "bad/id", "x" * 129):
            with self.subTest(rejected=rejected), self.assertRaises(ValueError):
                normalize_execution_id(rejected)

    def test_worker_queue_rehearsal_proves_worker_event_and_persisted_readback(self):
        class FakeFixture:
            attempt = "p03-worker-test"

            def __init__(self, root):
                self.root = root
                self.receipt = {}
                self.workflow_name = ""
                self.calls = []

            def verify_prerequisites(self):
                self.calls.append("verify_prerequisites")

            def create_networks(self):
                self.calls.append("create_networks")

            def create_secrets(self):
                self.calls.append("create_secrets")
                return {
                    "owner": ("synthetic-owner-password", object()),
                    "metadata_pg": ("synthetic-db-password", object()),
                    "valkey_server": ("synthetic-valkey-password", object()),
                }

            def start_postgres(self, *_args):
                self.calls.append("start_postgres")

            def start_valkey(self, *_args):
                self.calls.append("start_valkey")

            def start_mailpit(self):
                self.calls.append("start_mailpit")

            def start_n8n(self, _secrets):
                self.calls.append("start_n8n")

            def private(self, name, content):
                self.workflow_name = json.loads(content)["name"]
                target = self.root / name
                target.write_text(content, encoding="utf-8")
                return target

            @staticmethod
            def wait_until(callback, message, _seconds):
                if not callback():
                    raise AssertionError(message)

            def exec_result(self, actor, *arguments, input_=None):
                if actor == "main" and arguments[:2] == ("node", "-e"):
                    if input_ is None:
                        return subprocess.CompletedProcess(arguments, 0, "", "")
                    request = json.loads(input_)
                    action = request["action"]
                    values = {
                        "setup": {"id": "owner_1", "_session": "session"},
                        "workflows": {
                            "rows": [{"id": "workflow_1", "name": self.workflow_name}]
                        },
                        "run": {"executionId": 42},
                        "execution": {
                            "id": "42",
                            "status": "success",
                            "terminal": True,
                            "finished": True,
                        },
                    }
                    return subprocess.CompletedProcess(
                        arguments, 0, json.dumps(values[action]), ""
                    )
                if arguments[:2] == ("/bin/cat", "/tmp/p03-worker-ollama-events.jsonl"):
                    event = {
                        "execution_id": "42",
                        "model": "gemma4:e2b",
                        "actor": "worker-loopback",
                    }
                    return subprocess.CompletedProcess(
                        arguments, 0, json.dumps(event) + "\n", ""
                    )
                return subprocess.CompletedProcess(arguments, 0, "", "")

            def stop(self, actor):
                self.calls.append(("stop", actor))

            def cleanup(self):
                self.calls.append("cleanup")
                self.receipt["cleanup"] = "PASS"

        with tempfile.TemporaryDirectory() as directory:
            fixture = FakeFixture(Path(directory))
            rehearsal = WorkerModelNativeRehearsal(fixture)
            selected = {
                "P03_WORKER_MODEL_NATIVE_REHEARSAL": "1",
                "OPSFLOW_N8N_NATIVE_IMAGE": N8N_ID,
                "OPSFLOW_N8N_NATIVE_CONTEXT": "default",
            }
            with patch.dict(os.environ, selected, clear=True):
                receipt = rehearsal.run()

        self.assertEqual(receipt["native"], "PASS")
        self.assertEqual(receipt["queue_execution"], "PASS")
        self.assertEqual(receipt["worker_actor"], "PASS")
        self.assertEqual(receipt["persisted_readback"], "PASS")
        self.assertEqual(receipt["execution_id"], "42")
        self.assertEqual(receipt["cleanup"], "PASS")
        self.assertIn(("stop", "worker"), fixture.calls)
