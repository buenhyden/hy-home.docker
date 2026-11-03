"""Effect-integrity tests for the isolated Notebook native rehearsal."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.lib.ops._notebook_models_http import ApiError
from tests.validation._p03_notebook_effects import (
    measured_restore_counts,
    validate_completed_job,
    validate_embedding_events,
    validate_search,
)
from tests.validation._p03_notebook_native import DockerNotebookRuntime
from tests.validation._p03_owned_docker import NativeFixtureError


class NotebookEffectTests(unittest.TestCase):
    def test_job_is_terminal_and_bound_to_exact_source(self):
        job = {
            "id": "command:p03",
            "status": "completed",
            "command": "embed_source",
            "input": {"source_id": "source:p03"},
        }
        validate_completed_job(job, "command:p03", "source:p03")
        for changed in (
            {**job, "id": "command:other"},
            {**job, "status": "running"},
            {**job, "input": {"source_id": "source:other"}},
        ):
            with self.subTest(changed=changed), self.assertRaises(NativeFixtureError):
                validate_completed_job(changed, "command:p03", "source:p03")

    def test_search_requires_concrete_source_bound_result(self):
        result = {
            "total_count": 1,
            "results": [{"id": "source_embedding:p03", "source_id": "source:p03"}],
        }
        self.assertEqual(validate_search(result, "source:p03"), 1)
        for changed in (
            {"total_count": 1, "results": []},
            {"total_count": 1, "results": [{"id": "source_embedding:p03"}]},
            {"total_count": 1, "results": [{"source_id": "source:p03"}]},
        ):
            with self.subTest(changed=changed), self.assertRaises(NativeFixtureError):
                validate_search(changed, "source:p03")

    def test_embedding_event_requires_exact_model_dimension_and_shape(self):
        valid = json.dumps(
            {
                "kind": "embedding",
                "model": "embeddinggemma-2:740m",
                "dimension": 768,
            }
        )
        self.assertEqual(validate_embedding_events([valid]), 768)
        for changed in (
            valid.replace("768", "1024"),
            valid.replace("embeddinggemma-2:740m", "other"),
            valid[:-1] + ', "unexpected": true}',
        ):
            with self.subTest(changed=changed), self.assertRaises(NativeFixtureError):
                validate_embedding_events([changed])

    def test_restore_counts_require_exact_session_content_and_dimension(self):
        arguments = {
            "notebooks": [{"id": "notebook:p03"}],
            "sources": [{"id": "source:p03"}],
            "session": {
                "id": "chat_session:p03",
                "messages": [
                    {"role": "user", "content": "recovered"},
                    {"role": "assistant", "content": "P03 controlled reply"},
                ],
            },
            "session_id": "chat_session:p03",
            "expected_chat_tail": (
                ("user", "recovered"),
                ("assistant", "P03 controlled reply"),
            ),
            "text_results": 1,
            "vector_results": 1,
            "embedding_dimensions": 768,
        }
        self.assertEqual(measured_restore_counts(**arguments)["sessions"], 1)
        for key, value in (
            ("session_id", "chat_session:other"),
            ("embedding_dimensions", 0),
            ("expected_chat_tail", (("assistant", "wrong"),)),
        ):
            changed = {**arguments, key: value}
            with self.subTest(key=key), self.assertRaises(NativeFixtureError):
                measured_restore_counts(**changed)

    def test_runtime_measures_seed_recovery_restart_backup_and_restore_effects(self):
        class StatefulClient:
            def __init__(self, events):
                self.events = events
                self.available = True
                self.messages = []

            def embedding_event(self):
                row = {
                    "kind": "embedding",
                    "model": "embeddinggemma-2:740m",
                    "dimension": 768,
                }
                with self.events.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(row) + "\n")

            def post(self, path, payload):
                if path == "/api/notebooks":
                    return {"id": "notebook:p03"}
                if path == "/api/sources/json":
                    self.embedding_event()
                    return {"id": "source:p03", "command_id": "command:p03"}
                if path == "/api/chat/sessions":
                    return {"id": "chat_session:p03"}
                if path == "/api/chat/execute":
                    if not self.available:
                        raise ApiError("api_transport_error")
                    self.messages.extend(
                        [
                            {"role": "user", "content": payload["message"]},
                            {
                                "role": "assistant",
                                "content": "P03 controlled reply",
                            },
                        ]
                    )
                    return {"accepted": True}
                if path == "/api/search":
                    if payload["type"] == "vector":
                        self.embedding_event()
                    return {
                        "total_count": 1,
                        "results": [
                            {
                                "id": "source_embedding:p03",
                                "source_id": "source:p03",
                            }
                        ],
                    }
                raise AssertionError(path)

            def get(self, path):
                if path == "/api/commands/jobs/command:p03":
                    return {
                        "id": "command:p03",
                        "status": "completed",
                        "command": "embed_source",
                        "source_id": "source:p03",
                    }
                if path == "/api/notebooks":
                    return [{"id": "notebook:p03"}]
                if path == "/api/sources?notebook_id=notebook:p03":
                    return [{"id": "source:p03"}]
                if path == "/api/chat/sessions/chat_session:p03":
                    return {
                        "id": "chat_session:p03",
                        "messages": list(self.messages),
                    }
                raise AssertionError(path)

        class FakeOwned:
            @staticmethod
            def container_id(name):
                return "id-" + name

        with tempfile.TemporaryDirectory(prefix="p03 runtime effects ") as directory:
            runtime = DockerNotebookRuntime(sleep=lambda _seconds: None)
            runtime.root = Path(directory)
            events = runtime.root / "events"
            events.mkdir()
            (events / "events.jsonl").write_text("", encoding="utf-8")
            client = StatefulClient(runtime.events)
            runtime._client = lambda **_kwargs: client
            runtime._owned = FakeOwned()

            def docker(*arguments, timeout=30):
                del timeout
                if arguments[0] == "stop" and "ollama" in arguments[-1]:
                    client.available = False
                if arguments[0] == "start" and "ollama" in " ".join(arguments):
                    client.available = True
                return ""

            runtime._docker = docker
            counts = runtime.seed_and_query()
            runtime.interrupt_dependency_and_recover()
            runtime.verify_registered_models = Mock()
            runtime._wait_health = Mock(return_value="http://127.0.0.1:5055")
            restarted = runtime.restart_app_and_verify()

            def copy_volume(_volume, destination, *, restore=False):
                del restore
                destination.mkdir(parents=True, exist_ok=True)

            runtime._copy_volume = copy_volume
            backup = runtime.backup_consistent_set()
            runtime._create_primitives = Mock()
            runtime._create_stack = Mock(
                return_value=("restore-ollama", "restore-db", "restore-notebook")
            )
            restored = runtime.restore_isolated_and_verify(restarted)

        self.assertEqual(counts["embedding_dimensions"], 768)
        self.assertEqual(counts["chat_messages"], 2)
        self.assertEqual(restarted["chat_messages"], 4)
        self.assertEqual(restored, restarted)
        self.assertEqual(
            backup["components"],
            ("application_volume", "database_volume", "encryption_key"),
        )
        self.assertGreaterEqual(runtime.verify_registered_models.call_count, 2)

    def test_runtime_rejections_require_exact_http_status(self):
        class RefusingClient:
            def __init__(self, error):
                self.error = error

            def get(self, _path):
                raise self.error

            def post(self, _path, _payload):
                raise self.error

        runtime = DockerNotebookRuntime()
        for status in (401, 403):
            runtime._client = lambda *_args, status=status, **_kwargs: RefusingClient(
                ApiError("api_http_error", status=status)
            )
            runtime.verify_auth_rejection()
        runtime._client = lambda *_args, **_kwargs: RefusingClient(
            ApiError("api_http_error", status=404)
        )
        runtime.verify_protocol_rejections()

        for method, error in (
            ("verify_auth_rejection", ApiError("api_transport_error")),
            (
                "verify_protocol_rejections",
                ApiError("api_http_error", status=401),
            ),
        ):
            runtime._client = lambda *_args, error=error, **_kwargs: RefusingClient(
                error
            )
            with self.subTest(method=method), self.assertRaises(NativeFixtureError):
                getattr(runtime, method)()

    def test_volume_copy_helpers_are_owned_pull_free_and_read_only_at_source(self):
        class FakeOwned:
            def __init__(self):
                self.creates = []
                self.removed = []

            def create_container(self, name, *arguments):
                self.creates.append((name, arguments))

            @staticmethod
            def container_id(name):
                return "id-" + name

            def remove_container(self, name):
                self.removed.append(name)

        with tempfile.TemporaryDirectory(prefix="p03 copy effects ") as directory:
            runtime = DockerNotebookRuntime()
            runtime.root = Path(directory)
            owned = FakeOwned()
            runtime._owned = owned
            runtime._docker = lambda *arguments, **_kwargs: (
                "0" if arguments[0] == "wait" else ""
            )
            runtime._copy_volume("source-volume", runtime.root / "backup")
            runtime._copy_volume(
                "restore-volume", runtime.root / "backup", restore=True
            )

        self.assertEqual(len(owned.creates), 2)
        backup_arguments = owned.creates[0][1]
        restore_arguments = owned.creates[1][1]
        self.assertIn("--pull=never", backup_arguments)
        self.assertIn("none", backup_arguments)
        self.assertIn("--read-only", backup_arguments)
        self.assertIn("/tmp:rw,noexec,nosuid,nodev", backup_arguments)
        self.assertTrue(
            any(
                "src=source-volume" in item and item.endswith(",readonly")
                for item in backup_arguments
            )
        )
        self.assertTrue(
            any("dst=/backup,readonly" in item for item in restore_arguments)
        )
        self.assertEqual(owned.removed, [row[0] for row in owned.creates])
