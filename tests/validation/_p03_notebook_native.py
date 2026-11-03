"""Pull-free prerequisite census for the owned-isolated Notebook native test."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
import stat
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Protocol

from scripts.lib.ops._notebook_models_http import ApiError, OpenNotebookClient
from scripts.lib.ops.notebook_models import ModelPolicy, apply_policy, verify_policy
from tests.validation._p03_notebook_effects import (
    measured_restore_counts,
    validate_chat_session,
    validate_completed_job,
    validate_embedding_events,
    validate_search,
)
from tests.validation._p03_notebook_protocol import OLLAMA_PROTOCOL_SERVER
from tests.validation._p03_notebook_readiness import (
    NOTEBOOK_IMAGE,
    SURREALDB_IMAGE,
    native_selection,
)
from tests.validation._p03_owned_docker import NativeFixtureError, OwnedDocker

ROOT = Path(__file__).resolve().parents[2]
POLICY_FILE = ROOT / "infra/08-ai/open-notebook/config/notebook-model-policy.json"


class DockerNotebookRuntime:
    """Own and clean one pull-free Notebook/SDB/controlled-Ollama fixture."""

    def __init__(
        self,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._clock = clock
        self._sleep = sleep
        self.prefix = "p03-notebook-" + secrets.token_hex(6)
        self._owned = OwnedDocker(self.prefix)
        self.network = self.prefix + "-net"
        self.app_volume = self.prefix + "-app"
        self.db_volume = self.prefix + "-db"
        self.root: Path | None = None
        self.endpoint: str | None = None
        self.password = secrets.token_urlsafe(24)
        self.db_password = secrets.token_urlsafe(24)
        self.encryption_key = secrets.token_urlsafe(32)
        self.notebook_id: str | None = None
        self.source_id: str | None = None
        self.session_id: str | None = None
        self._root_identity: tuple[int, int, int] | None = None

    def _docker(self, *arguments: str, timeout: float = 30) -> str:
        return self._owned.command(*arguments, timeout=timeout)

    @property
    def events(self) -> Path:
        if self.root is None:
            raise NativeFixtureError("fixture_not_prepared")
        return self.root / "events" / "events.jsonl"

    def prepare(self) -> None:
        native_selection(os.environ)
        self._owned.verify_local_engine()
        if not self._owned.image_cached(NOTEBOOK_IMAGE) or not self._owned.image_cached(
            SURREALDB_IMAGE
        ):
            raise NativeFixtureError("native_image_missing")
        self.root = Path(tempfile.mkdtemp(prefix=self.prefix + "-"))
        root_metadata = self.root.stat(follow_symlinks=False)
        self._root_identity = (
            root_metadata.st_dev,
            root_metadata.st_ino,
            root_metadata.st_uid,
        )
        events = self.root / "events"
        events.mkdir(mode=0o700)
        (events / "events.jsonl").write_text("", encoding="utf-8")
        server = self.root / "ollama_protocol.py"
        server.write_text(OLLAMA_PROTOCOL_SERVER, encoding="utf-8")
        server.chmod(0o400)

    def _create_primitives(self, app_volume: str, db_volume: str, network: str) -> None:
        self._owned.create_network(network)
        for volume in (app_volume, db_volume):
            self._owned.create_volume(volume)

    def _create_stack(
        self,
        suffix: str,
        app_volume: str,
        db_volume: str,
        network: str,
        *,
        encryption_key: str | None = None,
    ) -> tuple[str, str, str]:
        if self.root is None:
            raise NativeFixtureError("fixture_not_prepared")
        ollama = self.prefix + f"-{suffix}-ollama"
        database = self.prefix + f"-{suffix}-surrealdb"
        notebook = self.prefix + f"-{suffix}-notebook"
        events = str((self.root / "events").resolve())
        server = str((self.root / "ollama_protocol.py").resolve())
        self._owned.create_container(
            ollama,
            "--pull=never",
            "--network",
            network,
            "--network-alias",
            "ollama",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev",
            "--mount",
            f"type=bind,src={server},dst=/fixture/ollama_protocol.py,readonly",
            "--mount",
            f"type=bind,src={events},dst=/events",
            "--entrypoint",
            "python",
            NOTEBOOK_IMAGE,
            "/fixture/ollama_protocol.py",
        )
        self._owned.create_container(
            database,
            "--pull=never",
            "--network",
            network,
            "--network-alias",
            "surrealdb",
            "--mount",
            f"type=volume,src={db_volume},dst=/mydata",
            "--entrypoint",
            "/surreal",
            SURREALDB_IMAGE,
            "start",
            "--bind",
            "0.0.0.0:8000",
            "--user",
            "root",
            "--pass",
            self.db_password,
            "rocksdb:/mydata/db.db",
        )
        self._owned.create_container(
            notebook,
            "--pull=never",
            "--network",
            network,
            "--publish",
            "127.0.0.1::5055",
            "--mount",
            f"type=volume,src={app_volume},dst=/app/data",
            "--env",
            "SURREAL_URL=ws://surrealdb:8000/rpc",
            "--env",
            "SURREAL_USER=root",
            "--env",
            f"SURREAL_PASSWORD={self.db_password}",
            "--env",
            "SURREAL_NAMESPACE=p03",
            "--env",
            "SURREAL_DATABASE=p03",
            "--env",
            f"OPEN_NOTEBOOK_PASSWORD={self.password}",
            "--env",
            f"OPEN_NOTEBOOK_ENCRYPTION_KEY={encryption_key or self.encryption_key}",
            "--env",
            "OLLAMA_API_BASE=http://ollama:11434",
            "--env",
            "OPEN_NOTEBOOK_WORKER_MAX_TASKS=1",
            NOTEBOOK_IMAGE,
        )
        return ollama, database, notebook

    def _wait_health(self, notebook: str, seconds: float = 120) -> str:
        port = self._docker("port", self._owned.container_id(notebook), "5055/tcp")
        if not port.startswith("127.0.0.1:") or not port[10:].isdigit():
            raise NativeFixtureError("notebook_loopback_port_invalid")
        endpoint = "http://" + port
        deadline = self._clock() + seconds
        while self._clock() < deadline:
            try:
                with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                    endpoint + "/health", timeout=2
                ) as response:
                    if response.status == 200:
                        return endpoint
            except (OSError, urllib.error.URLError):
                pass
            self._sleep(0.5)
        raise NativeFixtureError("notebook_start_timeout")

    def start_primary(self) -> None:
        self._create_primitives(self.app_volume, self.db_volume, self.network)
        ollama, database, notebook = self._create_stack(
            "primary", self.app_volume, self.db_volume, self.network
        )
        self._docker(
            "start",
            self._owned.container_id(ollama),
            self._owned.container_id(database),
        )
        self._sleep(1)
        self._docker("start", self._owned.container_id(notebook))
        self.endpoint = self._wait_health(notebook)

    def _client(
        self, password: str | None = None, seconds: float = 60
    ) -> OpenNotebookClient:
        if self.endpoint is None:
            raise NativeFixtureError("notebook_not_started")
        return OpenNotebookClient(
            self.endpoint, password or self.password, total_seconds=seconds
        )

    @staticmethod
    def _record_id(value: Any, prefix: str) -> str:
        if not isinstance(value, str) or not value.startswith(prefix + ":"):
            raise NativeFixtureError("native_api_shape_invalid")
        return value

    def verify_auth_rejection(self) -> None:
        try:
            self._client("wrong-synthetic-password", 10).get("/api/models")
        except ApiError as error:
            if error.code == "api_http_error" and error.status in {401, 403}:
                return
            raise NativeFixtureError("notebook_auth_rejection_type_invalid") from None
        raise NativeFixtureError("notebook_auth_rejection_missing")

    def register_models(self) -> None:
        document = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
        policy = ModelPolicy.from_document(document)
        fingerprint = hashlib.sha256(POLICY_FILE.read_bytes()).hexdigest()
        result = apply_policy(
            policy, self._client(seconds=60), fingerprint, owned_isolated=True
        )
        if result.get("result") != "PASS":
            raise NativeFixtureError("model_registration_failed")

    def verify_registered_models(self) -> None:
        document = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
        policy = ModelPolicy.from_document(document)
        fingerprint = hashlib.sha256(POLICY_FILE.read_bytes()).hexdigest()
        result = verify_policy(policy, self._client(seconds=60), fingerprint)
        if result.get("result") != "PASS":
            raise NativeFixtureError("model_registration_readback_failed")

    def verify_protocol_rejections(self) -> None:
        try:
            self._client(seconds=10).post(
                "/api/search",
                {"query": "scope", "type": "text", "notebook_id": "notebook:missing"},
            )
        except ApiError as error:
            if error.code == "api_http_error" and error.status == 404:
                return
            raise NativeFixtureError("invalid_scope_rejection_type_invalid") from None
        raise NativeFixtureError("invalid_scope_accepted")

    def _poll_job(self, job_id: str, source_id: str, seconds: float = 90) -> None:
        deadline = self._clock() + seconds
        while self._clock() < deadline:
            value = self._client(seconds=10).get(f"/api/commands/jobs/{job_id}")
            if not isinstance(value, Mapping):
                raise NativeFixtureError("job_shape_invalid")
            status = value.get("status")
            if status == "completed":
                validate_completed_job(value, job_id, source_id)
                return
            if status in {"failed", "cancelled"}:
                raise NativeFixtureError("job_terminal_failure")
            self._sleep(0.5)
        raise NativeFixtureError("job_poll_timeout")

    def _search_count(self, kind: str) -> int:
        result = self._client(seconds=30).post(
            "/api/search",
            {
                "query": "p03_unique_evidence",
                "type": kind,
                "limit": 5,
                "search_sources": True,
                "search_notes": False,
                "notebook_id": self.notebook_id,
            },
        )
        return validate_search(result, self.source_id)

    def _embedding_events_after(self, line_offset: int) -> int:
        try:
            lines = self.events.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            raise NativeFixtureError("embedding_event_shape_invalid") from error
        return validate_embedding_events(lines, line_offset)

    def seed_and_query(self) -> Mapping[str, int]:
        client = self._client(seconds=60)
        notebook = client.post(
            "/api/notebooks", {"name": "P03 isolated", "description": "synthetic"}
        )
        if not isinstance(notebook, Mapping):
            raise NativeFixtureError("native_api_shape_invalid")
        self.notebook_id = self._record_id(notebook.get("id"), "notebook")
        event_offset = len(self.events.read_text(encoding="utf-8").splitlines())
        source = client.post(
            "/api/sources/json",
            {
                "type": "text",
                "title": "P03 source",
                "content": "p03_unique_evidence",
                "notebooks": [self.notebook_id],
                "transformations": [],
                "embed": True,
                "delete_source": False,
                "async_processing": True,
            },
        )
        if not isinstance(source, Mapping):
            raise NativeFixtureError("native_api_shape_invalid")
        self.source_id = self._record_id(source.get("id"), "source")
        self._poll_job(
            self._record_id(source.get("command_id"), "command"), self.source_id
        )
        dimension = self._embedding_events_after(event_offset)
        session = self._client(seconds=30).post(
            "/api/chat/sessions", {"notebook_id": self.notebook_id, "title": "P03 chat"}
        )
        if not isinstance(session, Mapping):
            raise NativeFixtureError("native_api_shape_invalid")
        self.session_id = self._record_id(session.get("id"), "chat_session")
        self._client(seconds=60).post(
            "/api/chat/execute",
            {
                "session_id": self.session_id,
                "message": "Return P03 controlled reply",
                "context": {"sources": [], "notes": []},
            },
        )
        session_readback = self._client(seconds=30).get(
            f"/api/chat/sessions/{self.session_id}"
        )
        message_count = validate_chat_session(
            session_readback,
            self.session_id,
            (
                ("user", "Return P03 controlled reply"),
                ("assistant", "P03 controlled reply"),
            ),
        )
        return {
            "notebooks": 1,
            "sources": 1,
            "sessions": 1,
            "chat_messages": message_count,
            "text_results": self._search_count("text"),
            "vector_results": self._search_count("vector"),
            "embedding_dimensions": dimension,
        }

    def interrupt_dependency_and_recover(self) -> None:
        ollama = self.prefix + "-primary-ollama"
        self._docker("stop", "--time", "2", self._owned.container_id(ollama))
        try:
            self._client(seconds=10).post(
                "/api/chat/execute",
                {
                    "session_id": self.session_id,
                    "message": "expected dependency failure",
                    "context": {"sources": [], "notes": []},
                },
            )
        except ApiError as error:
            if str(error) not in {"api_http_error", "api_transport_error"}:
                raise NativeFixtureError("dependency_failure_type_invalid") from None
        else:
            raise NativeFixtureError("dependency_interruption_not_observed")
        self._docker("start", self._owned.container_id(ollama))
        self._sleep(1)
        self._client(seconds=30).post(
            "/api/chat/execute",
            {
                "session_id": self.session_id,
                "message": "recovered",
                "context": {"sources": [], "notes": []},
            },
        )
        recovered = self._client(seconds=30).get(
            f"/api/chat/sessions/{self.session_id}"
        )
        validate_chat_session(
            recovered,
            self.session_id,
            (("user", "recovered"), ("assistant", "P03 controlled reply")),
        )

    def _dataset_counts(
        self, expected_chat_tail: tuple[tuple[str, str], ...], event_offset: int = 0
    ) -> Mapping[str, int]:
        notebooks = self._client(seconds=30).get("/api/notebooks")
        sources = self._client(seconds=30).get(
            f"/api/sources?notebook_id={self.notebook_id}"
        )
        session = self._client(seconds=30).get(f"/api/chat/sessions/{self.session_id}")
        text_results = self._search_count("text")
        vector_results = self._search_count("vector")
        dimension = self._embedding_events_after(event_offset)
        return measured_restore_counts(
            notebooks,
            sources,
            session,
            session_id=self.session_id,
            expected_chat_tail=expected_chat_tail,
            text_results=text_results,
            vector_results=vector_results,
            embedding_dimensions=dimension,
        )

    def restart_app_and_verify(self) -> Mapping[str, int]:
        notebook = self.prefix + "-primary-notebook"
        self._docker(
            "restart",
            "--time",
            "3",
            self._owned.container_id(notebook),
            timeout=30,
        )
        self.endpoint = self._wait_health(notebook)
        self.verify_registered_models()
        return self._dataset_counts(
            (
                ("user", "Return P03 controlled reply"),
                ("assistant", "P03 controlled reply"),
                ("user", "recovered"),
                ("assistant", "P03 controlled reply"),
            )
        )

    def _copy_volume(
        self, volume: str, destination: Path, *, restore: bool = False
    ) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        script = (
            "import pathlib,shutil; s=pathlib.Path('/backup'); d=pathlib.Path('/data'); "
            "[shutil.copytree(p,d/p.name,dirs_exist_ok=True) if p.is_dir() else shutil.copy2(p,d/p.name) for p in s.iterdir()]"
            if restore
            else "import pathlib,shutil; s=pathlib.Path('/data'); d=pathlib.Path('/backup'); "
            "[shutil.copytree(p,d/p.name,dirs_exist_ok=True) if p.is_dir() else shutil.copy2(p,d/p.name) for p in s.iterdir()]"
        )
        data_mount = f"type=volume,src={volume},dst=/data"
        backup_mount = f"type=bind,src={destination.resolve()},dst=/backup"
        if restore:
            backup_mount += ",readonly"
        else:
            data_mount += ",readonly"
        mounts = ["--mount", data_mount, "--mount", backup_mount]
        helper = self.prefix + "-copy-" + secrets.token_hex(4)
        self._owned.create_container(
            helper,
            "--pull=never",
            "--network",
            "none",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev",
            *mounts,
            "--entrypoint",
            "python",
            NOTEBOOK_IMAGE,
            "-c",
            script,
        )
        identity = self._owned.container_id(helper)
        self._docker("start", identity, timeout=30)
        if self._docker("wait", identity, timeout=90) != "0":
            raise NativeFixtureError("volume_copy_failed")
        self._owned.remove_container(helper)

    def backup_consistent_set(self) -> Mapping[str, object]:
        if self.root is None:
            raise NativeFixtureError("fixture_not_prepared")
        self._docker(
            "stop",
            "--time",
            "5",
            self._owned.container_id(self.prefix + "-primary-notebook"),
        )
        self._docker(
            "stop",
            "--time",
            "5",
            self._owned.container_id(self.prefix + "-primary-surrealdb"),
        )
        backup = self.root / "backup"
        self._copy_volume(self.app_volume, backup / "app")
        self._copy_volume(self.db_volume, backup / "database")
        key = backup / "encryption-key"
        key.write_text(self.encryption_key, encoding="utf-8")
        key.chmod(0o600)
        return {
            "components": (
                "application_volume",
                "database_volume",
                "encryption_key",
            )
        }

    def _backup_encryption_key(self) -> str:
        if self.root is None:
            raise NativeFixtureError("fixture_not_prepared")
        path = self.root / "backup" / "encryption-key"
        try:
            metadata = path.stat(follow_symlinks=False)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_uid != os.geteuid()
                or metadata.st_nlink != 1
                or (metadata.st_mode & 0o777) != 0o600
                or metadata.st_size > 4096
            ):
                raise NativeFixtureError("backup_key_metadata_invalid")
            value = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise NativeFixtureError("backup_key_unreadable") from error
        if value != self.encryption_key:
            raise NativeFixtureError("backup_key_mismatch")
        return value

    def restore_isolated_and_verify(
        self, expected: Mapping[str, int]
    ) -> Mapping[str, int]:
        if self.root is None:
            raise NativeFixtureError("fixture_not_prepared")
        app_volume = self.prefix + "-restore-app"
        db_volume = self.prefix + "-restore-db"
        network = self.prefix + "-restore-net"
        self._create_primitives(app_volume, db_volume, network)
        self._copy_volume(app_volume, self.root / "backup" / "app", restore=True)
        self._copy_volume(db_volume, self.root / "backup" / "database", restore=True)
        restore_encryption_key = self._backup_encryption_key()
        ollama, database, notebook = self._create_stack(
            "restore",
            app_volume,
            db_volume,
            network,
            encryption_key=restore_encryption_key,
        )
        self._docker(
            "start",
            self._owned.container_id(ollama),
            self._owned.container_id(database),
        )
        self._sleep(1)
        self._docker("start", self._owned.container_id(notebook))
        self.endpoint = self._wait_health(notebook)
        self.verify_registered_models()
        event_offset = len(self.events.read_text(encoding="utf-8").splitlines())
        return self._dataset_counts(
            (
                ("user", "Return P03 controlled reply"),
                ("assistant", "P03 controlled reply"),
                ("user", "recovered"),
                ("assistant", "P03 controlled reply"),
            ),
            event_offset,
        )

    def cleanup(self) -> None:
        failures: list[str] = []
        try:
            self._owned.cleanup()
        except NativeFixtureError:
            failures.append("docker_resources")
        if self.root is not None:
            try:
                metadata = self.root.stat(follow_symlinks=False)
                identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
                if not self.root.is_dir() or identity != self._root_identity:
                    raise NativeFixtureError("fixture_root_identity_changed")
                shutil.rmtree(self.root)
                self.root = None
                self._root_identity = None
            except (NativeFixtureError, OSError):
                failures.append("host")
        if failures:
            raise NativeFixtureError("native_cleanup_incomplete")


class NotebookNativeBackend(Protocol):
    def prepare(self) -> None: ...

    def start_primary(self) -> None: ...

    def verify_auth_rejection(self) -> None: ...

    def register_models(self) -> None: ...

    def verify_protocol_rejections(self) -> None: ...

    def seed_and_query(self) -> Mapping[str, int]: ...

    def interrupt_dependency_and_recover(self) -> None: ...

    def restart_app_and_verify(self) -> Mapping[str, int]: ...

    def backup_consistent_set(self) -> Mapping[str, object]: ...

    def restore_isolated_and_verify(
        self, expected: Mapping[str, int]
    ) -> Mapping[str, int]: ...

    def cleanup(self) -> None: ...


class NotebookNativeLifecycle:
    """Run each app, worker, database, protocol, restart, and restore stage."""

    _COUNT_KEYS = (
        "notebooks",
        "sources",
        "sessions",
        "chat_messages",
        "text_results",
        "vector_results",
        "embedding_dimensions",
    )

    def __init__(self, backend: NotebookNativeBackend) -> None:
        self.backend = backend

    @classmethod
    def _counts(cls, value: Mapping[str, Any]) -> dict[str, int]:
        if set(value) != set(cls._COUNT_KEYS):
            raise AssertionError("native dataset summary shape rejected")
        counts = {key: value[key] for key in cls._COUNT_KEYS}
        if any(not isinstance(item, int) or item < 1 for item in counts.values()):
            raise AssertionError("native dataset summary value rejected")
        if counts["embedding_dimensions"] != 768:
            raise AssertionError("native embedding dimension rejected")
        return counts

    def run(self) -> dict[str, Any]:
        receipt: dict[str, Any] = {"native": "ERROR", "cleanup": "PENDING"}
        try:
            self.backend.prepare()
            self.backend.start_primary()
            self.backend.verify_auth_rejection()
            self.backend.register_models()
            self.backend.verify_protocol_rejections()
            source = self._counts(self.backend.seed_and_query())
            self.backend.interrupt_dependency_and_recover()
            source = self._counts(self.backend.restart_app_and_verify())
            backup = dict(self.backend.backup_consistent_set())
            components = backup.get("components")
            if not isinstance(components, (list, tuple)) or tuple(components) != (
                "application_volume",
                "database_volume",
                "encryption_key",
            ):
                raise AssertionError("native backup summary rejected")
            restored = self._counts(self.backend.restore_isolated_and_verify(source))
            if restored != source:
                raise AssertionError("restored dataset does not match source")
            receipt = {
                "native": "PASS",
                "cleanup": "PENDING",
                "source_counts": source,
                "backup_components": list(components),
                "embedding_dimensions": source["embedding_dimensions"],
                "restore_matches_source": True,
                "live_inference_claimed": False,
            }
            return receipt
        finally:
            self.backend.cleanup()
            receipt["cleanup"] = "PASS"
