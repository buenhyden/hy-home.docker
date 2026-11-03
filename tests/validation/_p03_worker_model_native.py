"""Owned n8n queue-worker to controlled Ollama protocol rehearsal.

The controlled endpoint binds only inside the worker's loopback namespace.  A
successful persisted execution therefore proves that Main dispatched the
manual run to the queue Worker; it does not claim live model inference.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from collections.abc import Mapping

from tests.validation._opsflow_native_fixture import NativeFixture, RehearsalFailure
from tests.validation._opsflow_native_inputs import N8N_ID
from tests.validation._p03_runner_native_fixture import p03_api_script
from tests.validation.test_opsflow_native_rehearsal import API_JS

SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")
P03_API_JS = p03_api_script(API_JS)

_WORKER_OLLAMA_SERVER = r"""
const http = require('http');
const fs = require('fs');
const events = '/tmp/p03-worker-ollama-events.jsonl';
function reply(res, status, value) {
  const body = JSON.stringify(value);
  res.writeHead(status, {'content-type':'application/json','content-length':Buffer.byteLength(body)});
  res.end(body);
}
http.createServer((req,res) => {
  if (req.method === 'GET' && req.url === '/health') return reply(res,200,{ready:true});
  if (req.method !== 'POST' || req.url !== '/api/chat') return reply(res,404,{error:'not found'});
  if (req.headers.authorization) return reply(res,400,{error:'unexpected authorization'});
  const executionId = req.headers['x-p03-execution-id'];
  if (typeof executionId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(executionId)) {
    return reply(res,400,{error:'invalid execution id'});
  }
  let size = 0; const chunks = [];
  req.on('data', chunk => { size += chunk.length; if (size <= 8192) chunks.push(chunk); });
  req.on('end', () => {
    if (size > 8192) return reply(res,413,{error:'request too large'});
    let body; try { body=JSON.parse(Buffer.concat(chunks).toString('utf8')); }
    catch (_) { return reply(res,400,{error:'invalid json'}); }
    const keys=Object.keys(body).sort();
    const message=Array.isArray(body.messages) && body.messages.length === 1 ? body.messages[0] : null;
    if (JSON.stringify(keys) !== JSON.stringify(['messages','model','stream']) ||
        body.model !== 'gemma4:e2b' || body.stream !== false ||
        !message || message.role !== 'user' || message.content !== 'P03 synthetic worker request') {
      return reply(res,400,{error:'invalid model request'});
    }
    fs.appendFileSync(events, JSON.stringify({execution_id:executionId,model:body.model,actor:'worker-loopback'})+'\n', {encoding:'utf8',mode:0o600});
    reply(res,200,{model:body.model,created_at:'synthetic',message:{role:'assistant',content:'P03 controlled reply'},done:true,done_reason:'stop'});
  });
}).listen(11434,'127.0.0.1');
"""


def normalize_execution_id(value: object) -> str:
    """Normalize the n8n numeric-or-string execution ID without coercion."""

    if isinstance(value, bool):
        raise ValueError("Worker model execution safe ID rejected")
    if isinstance(value, int):
        if value < 1:
            raise ValueError("Worker model execution safe ID rejected")
        normalized = str(value)
    elif isinstance(value, str):
        normalized = value
    else:
        raise ValueError("Worker model execution safe ID rejected")
    if not SAFE_ID.fullmatch(normalized):
        raise ValueError("Worker model execution safe ID rejected")
    return normalized


def worker_model_native_selection(environ: Mapping[str, str]) -> str:
    """Require an explicit local/default exact-image selection."""

    if (
        environ.get("P03_WORKER_MODEL_NATIVE_REHEARSAL") != "1"
        or environ.get("OPSFLOW_N8N_NATIVE_IMAGE") != N8N_ID
        or environ.get("OPSFLOW_N8N_NATIVE_CONTEXT") != "default"
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
        raise ValueError("exact isolated Worker model native selection required")
    return "default"


def build_worker_model_workflow(name: str) -> dict[str, object]:
    """Return one bounded manual queue workflow with an active HTTP model call."""

    if (
        not isinstance(name, str)
        or not 1 <= len(name) <= 128
        or name.strip() != name
        or any(ord(character) < 0x20 or ord(character) == 0x7F for character in name)
    ):
        raise ValueError("bounded workflow name required")
    manual = {
        "parameters": {},
        "id": str(uuid.uuid4()),
        "name": "Manual",
        "type": "n8n-nodes-base.manualTrigger",
        "typeVersion": 1,
        "position": [0, 0],
    }
    request = {
        "parameters": {
            "method": "POST",
            "url": "http://127.0.0.1:11434/api/chat",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "X-P03-Execution-Id",
                        "value": "={{ $execution.id }}",
                    }
                ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": (
                "={{ JSON.stringify({model:'gemma4:e2b',stream:false,"
                "messages:[{role:'user',content:'P03 synthetic worker request'}]}) }}"
            ),
            "options": {
                "redirect": {"redirect": {"followRedirects": False}},
                "response": {
                    "response": {
                        "fullResponse": True,
                        "neverError": False,
                        "responseFormat": "json",
                    }
                },
                "timeout": 10000,
            },
        },
        "id": str(uuid.uuid4()),
        "name": "Controlled Ollama Chat",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.4,
        "position": [240, 0],
    }
    return {
        "name": name,
        "nodes": [manual, request],
        "connections": {
            "Manual": {
                "main": [
                    [{"node": "Controlled Ollama Chat", "type": "main", "index": 0}]
                ]
            }
        },
        "active": False,
        "settings": {
            "executionOrder": "v1",
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
            "executionTimeout": 30,
        },
    }


class WorkerModelNativeRehearsal:
    """Run one pull-free Main→Valkey→Worker→loopback model request."""

    def __init__(self, fixture: NativeFixture | None = None) -> None:
        self.fixture = fixture
        self.email = ""
        self.session: str | None = None
        self.secrets: dict[str, tuple[str, object]] = {}

    def _api(self, action: str, **payload: object) -> dict[str, object]:
        body = {
            "action": action,
            "email": self.email,
            "password": self.secrets["owner"][0],
            **({"cookie": self.session} if self.session else {}),
            **payload,
        }
        result = self.fixture.exec_result(
            "main",
            "node",
            "-e",
            P03_API_JS,
            input_=json.dumps(body, separators=(",", ":")),
        )
        if result.returncode:
            raise RehearsalFailure("n8n model REST operation failed (output withheld)")
        try:
            value = json.loads(result.stdout)
        except (TypeError, ValueError):
            raise RehearsalFailure("n8n model REST summary rejected") from None
        if not isinstance(value, dict):
            raise RehearsalFailure("n8n model REST summary rejected")
        session = value.pop("_session", None)
        if session is not None:
            if not isinstance(session, str) or not session:
                raise RehearsalFailure("n8n model session summary rejected")
            self.session = session
        return value

    def _start_controlled_worker_endpoint(self) -> None:
        transferred = self.fixture.exec_result(
            "worker",
            "/bin/sh",
            "-ec",
            "umask 077; cat >/tmp/p03-worker-ollama.js",
            input_=_WORKER_OLLAMA_SERVER,
        )
        if transferred.returncode:
            raise RehearsalFailure("controlled Worker endpoint transfer failed")
        started = self.fixture.exec_result(
            "worker",
            "/bin/sh",
            "-ec",
            "node /tmp/p03-worker-ollama.js >/tmp/p03-worker-ollama.log 2>&1 </dev/null & echo $! >/tmp/p03-worker-ollama.pid",
        )
        if started.returncode:
            raise RehearsalFailure("controlled Worker endpoint start failed")
        probe = (
            "fetch('http://127.0.0.1:11434/health')"
            ".then(async r=>{const j=await r.json();process.exit(r.status===200&&j.ready===true?0:1)})"
            ".catch(()=>process.exit(1))"
        )
        self.fixture.wait_until(
            lambda: (
                self.fixture.exec_result("worker", "node", "-e", probe).returncode == 0
            ),
            "controlled Worker endpoint readiness expired",
            20,
        )
        main_isolated = self.fixture.exec_result(
            "main",
            "node",
            "-e",
            "fetch('http://127.0.0.1:11434/health').then(()=>process.exit(2)).catch(()=>process.exit(0))",
        )
        if main_isolated.returncode != 0:
            raise RehearsalFailure(
                "controlled endpoint was reachable from Main loopback"
            )

    def _import_workflow(self, workflow: Mapping[str, object], owner_id: str) -> str:
        private = self.fixture.private(
            "p03-worker-model-workflow.json",
            json.dumps(workflow, separators=(",", ":")) + "\n",
        )
        transfer = self.fixture.exec_result(
            "main",
            "/bin/sh",
            "-ec",
            "umask 077; cat >/tmp/p03-worker-model-workflow.json",
            input_=private.read_text(encoding="utf-8"),
        )
        if transfer.returncode:
            raise RehearsalFailure("Worker model workflow transfer failed")
        imported = self.fixture.exec_result(
            "main",
            "n8n",
            "import:workflow",
            "--input=/tmp/p03-worker-model-workflow.json",
            f"--userId={owner_id}",
            "--activeState=false",
        )
        if imported.returncode:
            raise RehearsalFailure("Worker model workflow import failed")
        rows = self._api("workflows").get("rows")
        matches = (
            [row for row in rows if row.get("name") == workflow["name"]]
            if isinstance(rows, list)
            else []
        )
        if len(matches) != 1 or not SAFE_ID.fullmatch(matches[0].get("id", "")):
            raise RehearsalFailure("Worker model workflow lookup failed")
        return matches[0]["id"]

    def _await_execution(self, execution_id: str) -> dict[str, object]:
        terminal: dict[str, object] = {}

        def finished() -> bool:
            summary = self._api("execution", executionId=execution_id)
            if summary.get("id") != execution_id:
                raise RehearsalFailure("Worker model execution identity changed")
            if summary.get("status") in {"success", "error", "canceled", "crashed"}:
                terminal.update(summary)
                return True
            return False

        self.fixture.wait_until(
            finished, "Worker model execution did not terminate", 60
        )
        if (
            terminal.get("status") != "success"
            or terminal.get("terminal") is not True
            or terminal.get("finished") is not True
        ):
            raise RehearsalFailure("Worker model execution result rejected")
        return terminal

    def _worker_event(self, execution_id: str) -> dict[str, str]:
        result = self.fixture.exec_result(
            "worker", "/bin/cat", "/tmp/p03-worker-ollama-events.jsonl"
        )
        try:
            rows = [json.loads(line) for line in result.stdout.splitlines()]
        except (TypeError, ValueError):
            raise RehearsalFailure("controlled Worker event summary rejected") from None
        expected = {
            "execution_id": execution_id,
            "model": "gemma4:e2b",
            "actor": "worker-loopback",
        }
        if result.returncode or rows != [expected]:
            raise RehearsalFailure("controlled Worker event did not match execution")
        return expected

    def run(self) -> dict[str, object]:
        worker_model_native_selection(os.environ)
        receipt: dict[str, object] = {
            "native": "ERROR",
            "cleanup": "PENDING",
            "live_model_inference_claimed": False,
        }
        try:
            if self.fixture is None:
                self.fixture = NativeFixture()
            self.email = f"p03-model-{self.fixture.attempt}@opsflow.invalid"
            self.fixture.verify_prerequisites()
            self.fixture.create_networks()
            self.secrets = self.fixture.create_secrets()
            self.fixture.start_postgres("metadata-pg", self.secrets["metadata_pg"][1])
            self.fixture.start_valkey(self.secrets["valkey_server"][1])
            self.fixture.start_mailpit()
            self.fixture.start_n8n(self.secrets)
            self._start_controlled_worker_endpoint()
            setup = self._api("setup")
            owner_id = setup.get("id")
            if not isinstance(owner_id, str) or not SAFE_ID.fullmatch(owner_id):
                raise RehearsalFailure("Worker model owner safe ID rejected")
            workflow = build_worker_model_workflow(
                f"P03 Worker model {self.fixture.attempt}"
            )
            workflow_id = self._import_workflow(workflow, owner_id)
            try:
                execution_id = normalize_execution_id(
                    self._api("run", workflowId=workflow_id).get("executionId")
                )
            except ValueError as error:
                raise RehearsalFailure(str(error)) from None
            terminal = self._await_execution(execution_id)
            event = self._worker_event(execution_id)
            self.fixture.stop("worker")
            persisted = self._api("execution", executionId=execution_id)
            if persisted != terminal:
                raise RehearsalFailure(
                    "persisted execution readback changed after Worker stop"
                )
            receipt.update(
                native="PASS",
                queue_execution="PASS",
                worker_actor="PASS",
                persisted_readback="PASS",
                execution_id=execution_id,
                workflow_id=workflow_id,
                model=event["model"],
                protocol="controlled-ollama-chat",
            )
            self.fixture.receipt["p03_worker_model"] = dict(receipt)
            self.fixture.receipt["native"] = "PASS"
            return receipt
        finally:
            if self.fixture is not None:
                self.fixture.cleanup()
                receipt["cleanup"] = self.fixture.receipt.get("cleanup", "FAIL")
