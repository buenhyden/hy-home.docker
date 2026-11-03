"""Pull-free n8n Worker-image to controlled Ollama protocol rehearsal."""

from __future__ import annotations

import json
import os
import secrets
import shutil
import stat
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tests.validation._opsflow_native_inputs import N8N_ID
from tests.validation._p03_notebook_native import NOTEBOOK_IMAGE
from tests.validation._p03_notebook_protocol import OLLAMA_PROTOCOL_SERVER
from tests.validation._p03_owned_docker import NativeFixtureError, OwnedDocker

_WORKER_PROBE = r"""const expected = new Set(["gemma4:e2b", "embeddinggemma-2:740m"]);
const base = process.env.OLLAMA_HOST;
if (base !== "http://ollama:11434") process.exit(2);
async function json(path, body) {
  const response = await fetch(base + path, body ? {
    method: "POST", headers: {"content-type": "application/json"},
    body: JSON.stringify(body), signal: AbortSignal.timeout(5000)
  } : {signal: AbortSignal.timeout(5000)});
  if (!response.ok) process.exit(3);
  return response.json();
}
(async () => {
  const tags = await json("/api/tags");
  const names = new Set(tags.models.map(row => row.name));
  if (expected.size !== names.size || [...expected].some(name => !names.has(name))) process.exit(4);
  const chat = await json("/api/chat", {model: "gemma4:e2b", stream: false,
    messages: [{role: "user", content: "P03 controlled probe"}]});
  const embedded = await json("/api/embed", {model: "embeddinggemma-2:740m",
    input: "P03 controlled probe"});
  const dimension = embedded.embeddings?.[0]?.length;
  if (chat.message?.content !== "P03 controlled reply" || dimension !== 768) process.exit(5);
  process.stdout.write(JSON.stringify({actor: "n8n-worker-image-protocol-probe",
    chat_model: "gemma4:e2b", embedding_model: "embeddinggemma-2:740m",
    embedding_dimensions: dimension, queue_workflow_claimed: false,
    live_model_inference_claimed: false}));
})().catch(() => process.exit(6));
"""


class WorkerOllamaFixture:
    """Exercise the Worker image as a client without claiming a queue execution."""

    def __init__(
        self,
    ) -> None:
        self.prefix = "p03-worker-ollama-" + secrets.token_hex(6)
        self._owned = OwnedDocker(self.prefix)
        self.root: Path | None = None
        self._root_identity: tuple[int, int, int] | None = None

    def _docker(self, *arguments: str, timeout: float = 30) -> str:
        return self._owned.command(*arguments, timeout=timeout)

    def _require_cached(self, image: str) -> None:
        if not self._owned.image_cached(image):
            raise NativeFixtureError("worker_probe_image_missing")

    @staticmethod
    def _selection(environ: Mapping[str, str]) -> None:
        if (
            environ.get("P03_WORKER_OLLAMA_NATIVE_REHEARSAL") != "1"
            or environ.get("P03_WORKER_OLLAMA_NATIVE_CONTEXT") != "default"
            or any(
                environ.get(key)
                for key in (
                    "DOCKER_HOST",
                    "DOCKER_CONTEXT",
                    "DOCKER_TLS_VERIFY",
                    "DOCKER_CERT_PATH",
                    "DOCKER_CONFIG",
                )
            )
        ):
            raise NativeFixtureError("worker_probe_selection_refused")

    def run(self) -> Mapping[str, Any]:
        self._selection(os.environ)
        try:
            return self._run_selected()
        finally:
            self.cleanup()

    def _run_selected(self) -> Mapping[str, Any]:
        self._owned.verify_local_engine()
        self._require_cached(N8N_ID)
        self._require_cached(NOTEBOOK_IMAGE)
        self.root = Path(tempfile.mkdtemp(prefix=self.prefix + "-"))
        metadata = self.root.stat(follow_symlinks=False)
        self._root_identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
        server = self.root / "ollama_protocol.py"
        server.write_text(OLLAMA_PROTOCOL_SERVER, encoding="utf-8")
        server.chmod(0o400)
        events = self.root / "events"
        events.mkdir(mode=0o700)
        network = self.prefix + "-net"
        server_name = self.prefix + "-server"
        probe_name = self.prefix + "-probe"
        try:
            network_id = self._owned.create_network(network)
            self._owned.create_container(
                server_name,
                "--pull=never",
                "--network",
                network_id,
                "--network-alias",
                "ollama",
                "--read-only",
                "--tmpfs",
                "/tmp:rw,noexec,nosuid,nodev",
                "--mount",
                f"type=bind,src={server.resolve()},dst=/fixture/ollama_protocol.py,readonly",
                "--mount",
                f"type=bind,src={events.resolve()},dst=/events",
                "--entrypoint",
                "python",
                NOTEBOOK_IMAGE,
                "/fixture/ollama_protocol.py",
            )
            self._docker("start", self._owned.container_id(server_name))
            self._owned.create_container(
                probe_name,
                "--pull=never",
                "--network",
                network_id,
                "--read-only",
                "--tmpfs",
                "/tmp:rw,noexec,nosuid,nodev",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges:true",
                "--env",
                "OLLAMA_HOST=http://ollama:11434",
                "--entrypoint",
                "node",
                N8N_ID,
                "-e",
                _WORKER_PROBE,
            )
            probe_id = self._owned.container_id(probe_name)
            self._docker("start", "--attach", probe_id, timeout=20)
            raw = self._docker("logs", probe_id, timeout=10)
            receipt = json.loads(raw)
            if receipt != {
                "actor": "n8n-worker-image-protocol-probe",
                "chat_model": "gemma4:e2b",
                "embedding_model": "embeddinggemma-2:740m",
                "embedding_dimensions": 768,
                "queue_workflow_claimed": False,
                "live_model_inference_claimed": False,
            }:
                raise NativeFixtureError("worker_probe_receipt_invalid")
            return receipt
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            raise NativeFixtureError("worker_probe_receipt_invalid") from error

    def cleanup(self) -> None:
        failures = []
        try:
            self._owned.cleanup()
        except NativeFixtureError:
            failures.append("docker_resources")
        if self.root is not None:
            try:
                metadata = self.root.stat(follow_symlinks=False)
                identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
                if (
                    not stat.S_ISDIR(metadata.st_mode)
                    or identity != self._root_identity
                ):
                    raise NativeFixtureError("worker_probe_root_changed")
                shutil.rmtree(self.root)
                self.root = None
                self._root_identity = None
            except (NativeFixtureError, OSError):
                failures.append("host")
        if failures:
            raise NativeFixtureError("worker_probe_cleanup_incomplete")
