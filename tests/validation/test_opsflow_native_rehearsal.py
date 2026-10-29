"""Default guards and opt-in actual n8n queue/runner/SMTP/restore rehearsal."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import stat
import subprocess
import time
import unittest
from copy import deepcopy
from pathlib import Path

from tests.validation._opsflow_native_criterion22 import (
    CLAIM_PROBE_SQL,
    CLAIMABLE_SQL,
    CREDENTIAL_PROBE_SCRIPT,
    DEACTIVATED_HOLD_SECONDS,
    EXECUTION_STATUSES_OPEN,
    EXECUTION_STATUSES_SEEN,
    MAX_ATTEMPTS,
    PASSWORD_PROBE_SCRIPT,
    RACE_SCRIPT,
    RACE_SQL,
    RECEIPT_FIELDS,
    RETRY_CYCLE_SQL,
    SCHEDULE_WAIT_SECONDS,
    execution_timeout_facts,
    exhaust_sql,
    fast_forward_sql,
    initial_receipt,
    outbox_row_sql,
    parse_probe,
    parse_race,
    race_winners,
    retry_expected,
    retry_row_sql,
    role_sessions_sql,
    rotate_role_sql,
    terminate_role_sql,
)
from tests.validation._opsflow_native_evidence import (
    BODY_FETCH_FAILURE_JS,
    body_fetch_failure_facts,
)
from tests.validation._opsflow_native_fixture import (
    NativeFixture,
    RehearsalFailure,
)
from tests.validation._opsflow_native_inputs import (
    N8N_ID,
    N8N_REF,
)
from tests.validation.test_opsflow_database_rehearsal import (
    CLUSTER_CONNECT,
    MIGRATION_1,
    MIGRATION_2,
    migration_sql,
    provision_sql,
    publish_sql,
    roles_restore_error_is_expected,
)
from tests.validation.test_opsflow_database_rehearsal import (
    WORKLOAD as PG_WORKLOAD,
)

FLAG = "OPSFLOW_N8N_NATIVE_REHEARSAL"
IMAGE_ENV = "OPSFLOW_N8N_NATIVE_IMAGE"
CONTEXT_ENV = "OPSFLOW_N8N_NATIVE_CONTEXT"
EXPLICIT = any(
    os.environ.get(key) is not None for key in (FLAG, IMAGE_ENV, CONTEXT_ENV)
)
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z")
SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")
API_JS = (
    BODY_FETCH_FAILURE_JS
    + "\n"
    + r"""
const fs=require('fs'); const input=JSON.parse(fs.readFileSync(0,'utf8'));
const base='http://127.0.0.1:5678';
async function call(path,method='GET',body,headers={}) {
 const r=await opsflowFetch(base+path,{method,headers:{'content-type':'application/json',...headers},body:body===undefined?undefined:JSON.stringify(body)});
 opsflowRequireOk(r); const j=await opsflowJson(r);
 return {data:j.data===undefined?j:j.data,cookie:(r.headers.get('set-cookie')||'').split(';',1)[0]};
}
async function toggle(id,on,versionId,auth){
 try{return await call('/rest/workflows/'+encodeURIComponent(id)+'/'+(on?'activate':'deactivate'),'POST',{versionId},auth);}
 catch(e){if(![404,405].includes(e.opsflowStatus))throw e;
  return await call('/rest/workflows/'+encodeURIComponent(id),'PATCH',{active:on,versionId},auth);}
}
async function login(){return (await call('/rest/login','POST',{emailOrLdapLoginId:input.email,password:input.password})).cookie;}
(async()=>{let out;
 if(input.action==='setup'){const r=await call('/rest/owner/setup','POST',{email:input.email,firstName:'Opsflow',lastName:'Fixture',password:input.password});out={id:r.data.id};}
 else {const fresh=!input.cookie; const cookie=input.cookie||await login(); const auth={cookie};
  if(input.action==='credential'){const r=await call('/rest/credentials','POST',input.credential,auth);out={id:r.data.id};}
  else if(input.action==='workflows'){const r=await call('/rest/workflows?take=100','GET',undefined,auth);const rows=r.data.results||r.data.data||r.data;out={rows:rows.map(x=>({id:x.id,name:x.name,active:x.active!==undefined?Boolean(x.active):Boolean(x.activeVersionId),versionId:x.versionId}))};}
  else if(input.action==='executions'){const r=await call('/rest/executions?limit=50&filter='+encodeURIComponent(JSON.stringify({workflowId:input.workflowId})),'GET',undefined,auth);const rows=r.data.results||r.data.data||r.data;out={rows:rows.map(x=>({id:String(x.id),mode:String(x.mode),status:String(x.status)}))};}
  else if(input.action==='activate'||input.action==='deactivate'){await toggle(input.workflowId,input.action==='activate',input.versionId,auth);out={ok:true};}
  else if(input.action==='credential_update'){const r=await call('/rest/credentials/'+encodeURIComponent(input.credentialId),'PATCH',input.credential,auth);out={id:String(r.data.id)};}
  else if(input.action==='run'){const r=await call('/rest/workflows/'+encodeURIComponent(input.workflowId)+'/run','POST',{triggerToStartFrom:{name:'Manual'}},auth);out={executionId:r.data.executionId};}
  else if(input.action==='execution'){const r=await call('/rest/executions/'+encodeURIComponent(input.executionId),'GET',undefined,auth);const d=r.data;
   const parsed=typeof d.data==='string'?require('flatted').parse(d.data):d.data;const rd=parsed?.resultData?.runData||{};
   const ns=n=>{const rows=rd[n]||[];return rows.length?String(rows[rows.length-1].executionStatus||'unknown'):'absent';};
   out={id:String(d.id),mode:String(d.mode),status:String(d.status),finished:Boolean(d.finished),terminal:Boolean(d.stoppedAt),acknowledged:ns('Acknowledged'),deliveryRedacted:ns('Redact Delivery Uncertain')};}
  else throw new Error('unknown_action');
  if(fresh) out._session=cookie;
 }
 process.stdout.write(JSON.stringify(out));
})().catch(opsflowExit);
"""
)
MAILPIT_JS = (
    BODY_FETCH_FAILURE_JS
    + "\n"
    + r"""
const crypto=require('crypto');
(async()=>{const run=process.argv[1];const r=await opsflowFetch('http://mailpit:8025/api/v1/messages');opsflowRequireOk(r);
const j=await opsflowJson(r);const rows=j.messages||j.Messages||[];const expected='opsflow.'+run+'@opsflow.invalid';
const m=rows.find(x=>(x.MessageID||x.MessageId||'').replace(/[<>]/g,'')===expected);let safe=false;
if(m){const id=m.ID||m.Id||m.id;const q=await opsflowFetch('http://mailpit:8025/api/v1/message/'+encodeURIComponent(id));opsflowRequireOk(q);const d=await opsflowJson(q);
 const text=d.Text||d.text||'';const raw=JSON.stringify(d);safe=text.includes('run='+run)&&text.includes('source=')&&!/lease_token|password|credential/i.test(raw);}
process.stdout.write(JSON.stringify({total:j.total??j.Total??rows.length,matched:Boolean(m),safe,digest:crypto.createHash('sha256').update(expected).digest('hex')}));
})().catch(opsflowExit);
"""
)


def native_selection(environ: dict[str, str] | None = None) -> tuple[str, str] | None:
    env = os.environ if environ is None else environ
    values = tuple(env.get(key) for key in (FLAG, IMAGE_ENV, CONTEXT_ENV))
    if values == (None, None, None):
        return None
    if values != ("1", N8N_ID, "default"):
        raise RehearsalFailure(
            "native opt-in must select the exact reviewed image and context"
        )
    if any(
        env.get(key)
        for key in (
            "DOCKER_HOST",
            "DOCKER_CONTEXT",
            "DOCKER_TLS_VERIFY",
            "DOCKER_CERT_PATH",
        )
    ):
        raise RehearsalFailure("Docker environment overrides are forbidden")
    return N8N_ID, "default"


@unittest.skipUnless(EXPLICIT, "exact isolated n8n native opt-in required")
class OpsflowN8nNativeRehearsal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        native_selection()

    def setUp(self):
        self.fixture = NativeFixture()
        self.secrets: dict[str, tuple[str, Path]] = {}
        self.email = f"owner-{self.fixture.attempt}@opsflow.invalid"
        self._finished = False
        self.credential_ids: dict[str, str] = {}
        self.published = 0
        self.stale_notifier = ""

    def tearDown(self):
        pass

    def finish(self):
        if self._finished:
            return
        self._finished = True
        if self.fixture.receipt.get("native") != "PASS":
            self.fixture.receipt["native"] = "ERROR"
        try:
            self.fixture.cleanup()
        finally:
            print("OPSFLOW_N8N_NATIVE_RECEIPT " + self.fixture.receipt_json())

    def api(self, action: str, **payload):
        # One login per session: n8n limits /rest/login to 5 per minute per
        # email, and polling an execution logged in every 0.25 s (429).
        session = getattr(self, "_session", None)
        body = {
            "action": action,
            "email": self.email,
            "password": self.secrets["owner"][0],
            **({"cookie": session} if session else {}),
            **payload,
        }
        result = self.fixture.exec_result(
            "main", "node", "-e", API_JS, input_=json.dumps(body, separators=(",", ":"))
        )
        failure = (
            body_fetch_failure_facts(result, "n8n_api") if result.returncode else None
        )
        if (
            session
            and failure
            and failure["kind"] == "http_status"
            and failure["status"] == 401
        ):
            # Only an ended session (for example after a main restart) logs in
            # again; any other failure is raised, never retried.
            self._session = None
            receipt = self.fixture.receipt
            receipt["n8n_session_relogins"] = receipt.get("n8n_session_relogins", 0) + 1
            return self.api(action, **payload)
        if failure:
            self.fixture.receipt["last_body_fetch_failure"] = failure
            raise RehearsalFailure("n8n REST operation failed (payload withheld)")
        try:
            out = json.loads(result.stdout)
        except (ValueError, TypeError):
            raise RehearsalFailure("n8n REST safe summary rejected") from None
        if isinstance(out, dict) and "_session" in out:
            self._session = out.pop("_session")
        return out

    def db_value(self, sql: str, role: str = "p04_audit") -> str:
        return self.fixture.psql(role, "opsflow_dev", sql).stdout.strip()

    def wait_state(self, run_id: str, state: str, seconds: int = 45) -> None:
        self.fixture.wait_until(
            lambda: (
                self.db_value(
                    f"SELECT state FROM ops_flow.delivery_status WHERE run_id='{run_id}';",
                    "opsflow_reader",
                )
                == state
            ),
            f"outbox did not reach {state}",
            seconds,
        )

    def capture(self, run_id: str, role: str = "worker") -> dict:
        result = self.fixture.exec_result(role, "node", "-e", MAILPIT_JS, run_id)
        if result.returncode:
            self.fixture.receipt["last_body_fetch_failure"] = body_fetch_failure_facts(
                result, "mailpit_capture"
            )
            raise RehearsalFailure("Mailpit safe capture summary failed")
        try:
            value = json.loads(result.stdout)
            if set(value) != {"total", "matched", "safe", "digest"}:
                raise ValueError
            return value
        except (ValueError, TypeError):
            raise RehearsalFailure("Mailpit safe capture summary rejected") from None

    def validate_dump(
        self, role: str, name: str, *, max_bytes: int = 32 * 1024 * 1024
    ) -> None:
        fixture = self.fixture
        fixture.runtime_headroom()
        _, _, disk_free, inode_percent = fixture._headroom()
        if disk_free < 10 * 1024**3 or inode_percent < 10:
            raise RehearsalFailure("dump disk/inode reserve is insufficient")
        path = fixture.dumps[name]
        metadata = path.stat(follow_symlinks=False)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_uid != 70
            # Foreign-owned fixture files are exactly 0640 (create_secrets);
            # pg_dump writes into the file and keeps that mode.
            or stat.S_IMODE(metadata.st_mode) != 0o640
            or metadata.st_nlink != 1
            or not 0 < metadata.st_size <= max_bytes
        ):
            raise RehearsalFailure("bounded dump metadata rejected")
        summary = fixture.exec(
            role,
            "/bin/sh",
            "-ec",
            'set -eu; bytes=$(wc -c <"$1"); digest=$(sha256sum "$1" | cut -d\' \' -f1); printf \'%s|%s\' "$bytes" "$digest"',
            "dump-check",
            "/fixture/" + name,
        )
        try:
            size_text, digest = summary.strip().split("|", 1)
            if int(size_text) != metadata.st_size or not re.fullmatch(
                r"[0-9a-f]{64}", digest
            ):
                raise ValueError
        except (ValueError, TypeError):
            raise RehearsalFailure("dump integrity summary rejected") from None
        receipt = {"size": metadata.st_size, "sha256": digest}
        if fixture.dump_receipts.get(name, receipt) != receipt:
            raise RehearsalFailure("dump content changed before restore")
        fixture.dump_receipts[name] = receipt
        fixture.receipt["dump_artifacts"] = dict(sorted(fixture.dump_receipts.items()))
        total = sum(
            item.path.stat(follow_symlinks=False).st_size
            for item in fixture.files.values()
            if item.path.exists()
        )
        if total > 96 * 1024 * 1024 or len(fixture.files) > 64:
            raise RehearsalFailure("host fixture file budget exceeded")

    def provision(self) -> None:
        sql = provision_sql()
        for role in ("migrator", "ingest", "notifier", "reader"):
            value = self.secrets[role][0]
            if not re.fullmatch(r"[A-Za-z0-9_-]{32,128}", value):
                raise RehearsalFailure("synthetic role secret shape rejected")
            public = f"p04-{role}-synthetic-only"
            if sql.count(public) != 1:
                raise RehearsalFailure("reviewed role password placeholder changed")
            sql = sql.replace(public, value)
        self.fixture.psql("p04_audit", "postgres", sql)
        for path in (
            MIGRATION_1,
            MIGRATION_2,
            PG_WORKLOAD / "sql/004_notification_quarantine.sql",
        ):
            self.fixture.psql("opsflow_migrator", "opsflow_dev", migration_sql(path))

    def start_dev_cluster(self) -> None:
        self.fixture.start_postgres("dev-pg", self.secrets["dev_pg"][1])
        self.fixture.psql(
            "p04_audit",
            "postgres",
            "\\set reviewed_connect_consumers 'reviewed'\n"
            + CLUSTER_CONNECT.read_text(),
        )

    def publish(self, source: str, digest: str, captured: str) -> str:
        run_id, sql = publish_sql(source, digest, captured)
        if self.db_value(sql, "opsflow_ingest") not in {"published", "replayed"}:
            raise RehearsalFailure("synthetic publication failed")
        return run_id

    @staticmethod
    def postgres_credential(password: str) -> dict:
        return {
            "name": "opsflow-native-postgres",
            "type": "postgres",
            "data": {
                "host": "dev-pg",
                "database": "opsflow_dev",
                "user": "opsflow_notifier",
                "password": password,
                "maxConnections": 2,
                "ssl": "disable",
                "port": 5432,
            },
        }

    def bind_and_import(self) -> tuple[str, str]:
        setup = self.api("setup")
        owner_id = setup.get("id")
        if not isinstance(owner_id, str) or not UUID.fullmatch(owner_id):
            raise RehearsalFailure("owner setup safe ID rejected")
        postgres = self.api(
            "credential",
            credential=self.postgres_credential(self.secrets["notifier"][0]),
        ).get("id")
        smtp = self.api(
            "credential",
            credential={
                "name": "opsflow-native-smtp",
                "type": "smtp",
                "data": {
                    "user": "",
                    "password": "",
                    "host": "mailpit",
                    "port": 1025,
                    "secure": False,
                    "disableStartTls": True,
                    "hostName": "",
                },
            },
        ).get("id")
        if not all(
            isinstance(value, str) and SAFE_ID.fullmatch(value)
            for value in (postgres, smtp)
        ):
            raise RehearsalFailure("credential safe IDs rejected")
        self.credential_ids = {"postgres": postgres, "smtp": smtp}
        workflow_path = (
            Path(__file__).resolve().parents[2]
            / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/workflows/manifest-outbox-mailpit.json"
        )
        tracked_bytes = workflow_path.read_bytes()
        tracked = json.loads(tracked_bytes)
        if tracked.get("active") is not False:
            raise RehearsalFailure("tracked workflow is not inactive")
        name = "Opsflow native " + self.fixture.attempt
        bound = deepcopy(tracked)
        bound["name"] = name
        overrides = {
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
        }
        expected = {
            "saveDataErrorExecution": "none",
            "saveDataSuccessExecution": "none",
            "saveExecutionProgress": False,
            "saveManualExecutions": False,
        }
        if any(
            bound.get("settings", {}).get(key) != value
            for key, value in expected.items()
        ):
            raise RehearsalFailure("tracked execution retention contract changed")
        bound["settings"] = {**bound["settings"], **overrides}
        for node in bound["nodes"]:
            for kind, credential in (node.get("credentials") or {}).items():
                if credential.get(
                    "id"
                ) != "REPLACE_WITH_LOCAL_CREDENTIAL_ID" or kind not in {
                    "postgres",
                    "smtp",
                }:
                    raise RehearsalFailure(
                        "workflow credential placeholder contract changed"
                    )
                credential["id"] = postgres if kind == "postgres" else smtp
        content = json.dumps(bound, separators=(",", ":")) + "\n"
        private = self.fixture.private("workflow.private.json", content)
        self.fixture.receipt["workflow_fixture"] = {
            "tracked_sha256": hashlib.sha256(tracked_bytes).hexdigest(),
            "bound_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "settings_delta": overrides,
        }
        transfer = self.fixture.exec_result(
            "main",
            "/bin/sh",
            "-ec",
            'umask 077; cat >/tmp/workflow.private.json; test "$(id -u)" = 1000; test "$(stat -c %a /tmp/workflow.private.json)" = 600',
            input_=private.read_text(),
        )
        if transfer.returncode:
            raise RehearsalFailure("private workflow transfer failed")
        imported = self.fixture.exec_result(
            "main",
            "n8n",
            "import:workflow",
            "--input=/tmp/workflow.private.json",
            f"--userId={owner_id}",
            "--activeState=false",
        )
        if imported.returncode:
            raise RehearsalFailure("inactive workflow import failed (output withheld)")
        rows = self.api("workflows").get("rows")
        matches = (
            [row for row in rows if row.get("name") == name]
            if isinstance(rows, list)
            else []
        )
        if (
            len(matches) != 1
            or matches[0].get("active") is not False
            or not SAFE_ID.fullmatch(matches[0].get("id", ""))
        ):
            raise RehearsalFailure("inactive imported workflow lookup failed")
        return matches[0]["id"], name

    def run_manual(self, workflow_id: str) -> str:
        execution = self.api("run", workflowId=workflow_id).get("executionId")
        if not isinstance(execution, str) or not SAFE_ID.fullmatch(execution):
            raise RehearsalFailure("manual execution safe ID rejected")
        return execution

    def await_execution(
        self, execution_id: str, status: str, code_node: str | None = None
    ) -> dict:
        terminal: dict[str, object] = {}
        seen = {"status": "none"}

        def probe() -> bool:
            summary = self.api("execution", executionId=execution_id)
            if summary.get("id") != execution_id:
                raise RehearsalFailure("execution safe ID changed")
            status_seen = summary.get("status")
            seen["status"] = (
                status_seen if status_seen in EXECUTION_STATUSES_SEEN else "other"
            )
            if status_seen in {"success", "error", "canceled", "crashed"}:
                terminal.update(summary)
                return True
            return False

        def timed_out() -> None:
            self.fixture.receipt["execution_timeout_facts"] = execution_timeout_facts(
                seen["status"], self.fixture.logs_contain
            )

        self.fixture.wait_until(
            probe, "queued execution did not become terminal", 60, timed_out
        )
        if terminal.get("status") != status or terminal.get("terminal") is not True:
            raise RehearsalFailure("queued execution terminal status rejected")
        if status == "success" and terminal.get("finished") is not True:
            raise RehearsalFailure("successful execution did not finish")
        if code_node and terminal.get(code_node) != "success":
            raise RehearsalFailure("external runner Code node did not complete")
        ids = self.fixture.receipt.setdefault("terminal_execution_ids", [])
        if isinstance(ids, list):
            ids.append(execution_id)
        return terminal

    # --- SPEC-0204 criterion 22 scenarios (see _opsflow_native_criterion22).

    def step(self, name: str, action) -> None:
        receipt = self.fixture.receipt
        try:
            action()
        except BaseException:
            receipt[name] = "FAIL"
            raise
        receipt[name] = "PASS"

    def generation_1_scenarios(self, workflow_id: str) -> tuple:
        # Order matters: each leaves the claimable queue empty for the next, and
        # none leaves a pending row for the later restore checks.
        return (
            (
                "scheduled_execution",
                lambda: self.scenario_scheduled_execution(workflow_id),
            ),
            ("concurrent_claims", self.scenario_concurrent_claims),
            ("retry_dead_letter", self.scenario_retry_dead_letter),
            ("empty_queue", lambda: self.scenario_empty_queue(workflow_id)),
            (
                "credential_rotation",
                lambda: self.scenario_credential_rotation(workflow_id),
            ),
        )

    def restore_scenarios(self) -> tuple:
        # The wrong-key probe runs last: it is the only step that starts a
        # second n8n process with another key.
        return (
            ("paired_restore_decrypt", self.scenario_paired_restore_decrypt),
            ("wrong_key_fail_closed", self.scenario_wrong_key_fail_closed),
        )

    def require_criterion_22_pass(self) -> None:
        if any(self.fixture.receipt.get(field) != "PASS" for field in RECEIPT_FIELDS):
            raise RehearsalFailure("criterion 22 scenarios did not all pass")

    def publish_next(self, source: str) -> tuple[str, str]:
        # Capture times only rise, so every row is `published` with an outbox
        # row. Each takes its own UTC day after the earlier steps' 2026-10-16,
        # since V2 allows one run per source and business date.
        self.published += 1
        digest = hashlib.sha256(f"criterion-22-{self.published}".encode()).hexdigest()
        captured = f"2026-10-{16 + self.published:02d}T00:00:00Z"
        run_id = self.publish(source, digest, captured)
        outbox_id = self.db_value(
            f"SELECT id FROM ops_flow.outbox WHERE run_id='{run_id}';"
        )
        if not outbox_id.isdecimal():
            raise RehearsalFailure("outbox safe ID rejected")
        return run_id, outbox_id

    def notifier(self, sql: str) -> str:
        return self.fixture.psql("opsflow_notifier", "opsflow_dev", sql).stdout.strip()

    def assert_claimable(self, expected: int) -> None:
        if self.db_value(CLAIMABLE_SQL) != str(expected):
            raise RehearsalFailure("claimable outbox row count rejected")

    def row(self, outbox_id: str, columns: str) -> str:
        return self.db_value(outbox_row_sql(outbox_id, columns))

    def workflow_row(self, workflow_id: str) -> dict:
        rows = self.api("workflows").get("rows")
        matches = (
            [row for row in rows if row.get("id") == workflow_id]
            if isinstance(rows, list)
            else []
        )
        if len(matches) != 1 or not SAFE_ID.fullmatch(matches[0].get("versionId", "")):
            raise RehearsalFailure("workflow lookup failed")
        return matches[0]

    def set_active(self, workflow_id: str, active: bool) -> None:
        version = self.workflow_row(workflow_id)["versionId"]
        self.api(
            "activate" if active else "deactivate",
            workflowId=workflow_id,
            versionId=version,
        )
        if self.workflow_row(workflow_id).get("active") is not active:
            raise RehearsalFailure("workflow activation state rejected")

    def executions(self, workflow_id: str) -> list[dict]:
        rows = self.api("executions", workflowId=workflow_id).get("rows")
        if not isinstance(rows, list) or not all(
            isinstance(row, dict)
            and SAFE_ID.fullmatch(row.get("id", ""))
            and isinstance(row.get("mode"), str)
            and isinstance(row.get("status"), str)
            for row in rows
        ):
            raise RehearsalFailure("execution list safe summary rejected")
        return rows

    def mail_total(self) -> int:
        # Mailpit counts every message in the generation, whatever the run.
        return self.capture("0" * 64)["total"]

    def drain_manual(self, workflow_id: str, run_id: str) -> None:
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success", "acknowledged")
        self.wait_state(run_id, "accepted_by_smtp")

    def scenario_scheduled_execution(self, workflow_id: str) -> None:
        containers = self.fixture.containers
        # Only the worker is on the dev network, so a claim that reaches the
        # DEV database can only have run on the actual queue worker.
        if "dev" in containers["main"].networks or (
            "dev" not in containers["worker"].networks
        ):
            raise RehearsalFailure("main/worker network roles changed")
        self.assert_claimable(0)
        run_id, _ = self.publish_next("blog-data")
        self.assert_claimable(1)
        before = {row["id"] for row in self.executions(workflow_id)}
        total = self.mail_total()
        self.set_active(workflow_id, True)
        started = time.monotonic()

        def delivered() -> bool:
            time.sleep(2)
            return (
                self.db_value(
                    f"SELECT state FROM ops_flow.delivery_status WHERE run_id='{run_id}';",
                    "opsflow_reader",
                )
                == "accepted_by_smtp"
            )

        self.fixture.wait_until(
            delivered, "scheduled execution did not deliver", SCHEDULE_WAIT_SECONDS
        )
        waited = round(time.monotonic() - started)
        self.set_active(workflow_id, False)
        self.fixture.wait_until(
            lambda: (
                not {row["status"] for row in self.executions(workflow_id)}
                & EXECUTION_STATUSES_OPEN
            ),
            "scheduled executions did not settle",
            60,
        )
        new = [row for row in self.executions(workflow_id) if row["id"] not in before]
        if not new or {row["mode"] for row in new} != {"trigger"}:
            raise RehearsalFailure("scheduled executions were not trigger-mode")
        summaries = [self.api("execution", executionId=row["id"]) for row in new]
        if any(
            summary.get("status") != "success" or summary.get("mode") != "trigger"
            for summary in summaries
        ) or not any(summary.get("acknowledged") == "success" for summary in summaries):
            raise RehearsalFailure("scheduled execution outcome rejected")
        capture = self.capture(run_id)
        if (capture["matched"], capture["safe"], capture["total"]) != (
            True,
            True,
            total + 1,
        ):
            raise RehearsalFailure("scheduled delivery was not exactly one message")
        self.fixture.receipt["scheduled_execution_facts"] = {
            "wait_seconds": waited,
            "trigger_executions": len(new),
            "worker_only_dev_network": True,
        }
        # Deactivated: more than one full minute passes and the row stays put.
        held, _ = self.publish_next("hy-home.docker")
        deadline = time.monotonic() + DEACTIVATED_HOLD_SECONDS
        while time.monotonic() < deadline:
            self.fixture.runtime_headroom()
            if (
                self.db_value(
                    f"SELECT state||'|'||attempts FROM ops_flow.outbox WHERE run_id='{held}';"
                )
                != "pending|0"
            ):
                raise RehearsalFailure("deactivated workflow still claimed a row")
            time.sleep(5)
        self.drain_manual(workflow_id, held)

    def race(self, jobs: int) -> list[dict]:
        result = self.fixture.exec_result(
            "dev-pg",
            "/bin/sh",
            "-ec",
            RACE_SCRIPT,
            "race",
            str(jobs),
            input_=RACE_SQL,
        )
        if result.returncode:
            raise RehearsalFailure("concurrent claim session failed (output withheld)")
        try:
            return parse_race(result.stdout, jobs)
        except ValueError:
            raise RehearsalFailure("concurrent claim summary rejected") from None

    def scenario_concurrent_claims(self) -> None:
        self.assert_claimable(0)
        _, single = self.publish_next("hy-home.k8s")
        self.assert_claimable(1)
        try:
            race_winners(self.race(4), {int(single)})
        except ValueError as error:
            raise RehearsalFailure(f"one row, four claimers: {error}") from None
        ids = [self.publish_next(source)[1] for source in ("hy-home.docker", "hy-home.k8s", "blog-data")]  # fmt: skip
        self.assert_claimable(3)
        try:
            race_winners(self.race(6), {int(item) for item in ids})
        except ValueError as error:
            raise RehearsalFailure(f"three rows, six claimers: {error}") from None
        listed = ",".join([single, *ids])
        self.assertEqual(
            "4",
            self.db_value(
                "SELECT count(*) FROM ops_flow.outbox WHERE id IN ("
                f"{listed}) AND state='accepted_by_smtp' AND attempts=1;"
            ),
        )
        self.assert_claimable(0)
        # The database claim contract, driven as the notifier role in psql;
        # the workflow itself runs one worker at concurrency 1.
        self.fixture.receipt["concurrent_claims_facts"] = {
            "driver": "psql_notifier_role"
        }

    def scenario_retry_dead_letter(self) -> None:
        self.assert_claimable(0)
        run_id, outbox_id = self.publish_next("hy-home.docker")
        for attempt in range(1, MAX_ATTEMPTS + 1):
            self.assertEqual(
                f"claimed|{outbox_id}\nretried|true", self.notifier(RETRY_CYCLE_SQL)
            )
            self.assertEqual(
                retry_expected(attempt),
                self.db_value(retry_row_sql(outbox_id, attempt)),
            )
            self.assertEqual("0", self.notifier(CLAIM_PROBE_SQL))
            if attempt < MAX_ATTEMPTS:
                # The backoff (60..480 s) is fast-forwarded as the superuser;
                # the notifier role cannot do that.
                self.assertEqual(outbox_id, self.db_value(fast_forward_sql(outbox_id)))
        self.assertEqual(
            f"dead|{MAX_ATTEMPTS}|true",
            self.row(
                outbox_id, "state||'|'||attempts||'|'||(lease_token IS NULL)::text"
            ),
        )
        self.assertEqual(
            "dead",
            self.db_value(
                f"SELECT state FROM ops_flow.delivery_status WHERE run_id='{run_id}';",
                "opsflow_reader",
            ),
        )
        # An exhausted row that never reached `sending` is dead-lettered too.
        _, exhausted = self.publish_next("hy-home.k8s")
        self.assertEqual(exhausted, self.db_value(exhaust_sql(exhausted)))
        self.assertEqual("0", self.notifier(CLAIM_PROBE_SQL))
        self.assertEqual(
            f"dead|{MAX_ATTEMPTS}|retry_exhausted",
            self.row(
                exhausted, "state||'|'||attempts||'|'||coalesce(last_error_code,'')"
            ),
        )
        self.fixture.receipt["retry_dead_letter_facts"] = {
            "driver": "psql_notifier_role",
            "backoff": "fast_forwarded",
        }

    def scenario_empty_queue(self, workflow_id: str) -> None:
        self.assert_claimable(0)
        self.assertEqual(
            "2",
            self.db_value("SELECT count(*) FROM ops_flow.outbox WHERE state='dead';"),
        )
        fingerprint = (
            "SELECT md5(string_agg(id||state||attempts||coalesce(last_error_code,'')"
            "||coalesce(accepted_at::text,''),',' ORDER BY id)) FROM ops_flow.outbox;"
        )
        before, total = self.db_value(fingerprint), self.mail_total()
        execution = self.run_manual(workflow_id)
        terminal = self.await_execution(execution, "success")
        self.assertEqual("absent", terminal.get("acknowledged"))
        self.assertEqual(total, self.mail_total())
        self.assertEqual(before, self.db_value(fingerprint))
        self.assert_claimable(0)

    def password_probe(self, role: str, password: str) -> subprocess.CompletedProcess:
        return self.fixture.exec_result(
            "dev-pg",
            "/bin/sh",
            "-ec",
            PASSWORD_PROBE_SCRIPT,
            "password-probe",
            role,
            input_=password + "\n",
        )

    def assert_password(self, role: str, password: str, accepted: bool) -> None:
        result = self.password_probe(role, password)
        if accepted and (result.returncode or result.stdout.strip() != "1"):
            raise RehearsalFailure("current notifier password was refused")
        denied = (
            "28P01" in result.stderr
            or "password authentication failed" in result.stderr
        )
        if not accepted and (result.returncode == 0 or not denied):
            raise RehearsalFailure("stale notifier password was not denied")

    def rewrite_secret_file(self, key: str, value: str) -> None:
        # Same inode, so the retained-evidence registry redacts the live value.
        path = self.secrets[key][1]
        expected = self.fixture.files[path]
        descriptor = os.open(path, os.O_WRONLY | os.O_NOFOLLOW)
        try:
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) != (expected.device, expected.inode):
                raise RehearsalFailure("rotated secret file identity changed")
            os.ftruncate(descriptor, 0)
            os.write(descriptor, (value + "\n").encode())
        finally:
            os.close(descriptor)
        self.secrets[key] = (value, path)

    def scenario_credential_rotation(self, workflow_id: str) -> None:
        old = self.secrets["notifier"][0]
        # Control: a wrong password is refused on this path, so a pass below
        # is not a `trust` rule accepting anything.
        self.assert_password("opsflow_notifier", secrets.token_urlsafe(32), False)
        self.assert_password("opsflow_notifier", old, True)
        run_id, outbox_id = self.publish_next("blog-data")
        total = self.mail_total()
        new = secrets.token_urlsafe(32)
        self.fixture.psql(
            "p04_audit", "postgres", rotate_role_sql("opsflow_notifier", new)
        )
        self.db_value(terminate_role_sql("opsflow_notifier"))
        self.assertEqual("0", self.db_value(role_sessions_sql("opsflow_notifier")))
        self.assert_password("opsflow_notifier", old, False)
        self.assert_password("opsflow_notifier", new, True)
        # n8n still holds the stale password: the claim is denied, nothing sent.
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "error")
        self.assertEqual("pending|0", self.row(outbox_id, "state||'|'||attempts"))
        self.assertEqual(total, self.mail_total())
        self.api(
            "credential_update",
            credentialId=self.credential_ids["postgres"],
            credential=self.postgres_credential(new),
        )
        self.drain_manual(workflow_id, run_id)
        capture = self.capture(run_id)
        self.assertEqual(
            (total + 1, True, True),
            (capture["total"], capture["matched"], capture["safe"]),
        )
        self.stale_notifier = old
        # Restore re-applies role passwords from this registry after the dump.
        self.rewrite_secret_file("notifier", new)
        self.fixture.receipt["credential_rotation_facts"] = {
            "stale_password_denied": True,
            "new_password_accepted": True,
            "stale_workflow_status": "error",
            "rotated_workflow_status": "success",
            "smtp_rotation": "NOT_RUN",
        }

    def credential_probe(
        self, credential_id: str, field: str, value: str, key: str = ""
    ) -> dict:
        digest = hashlib.sha256(value.encode()).hexdigest()
        result = self.fixture.exec_result(
            "main",
            "/bin/sh",
            "-ec",
            CREDENTIAL_PROBE_SCRIPT,
            "credential-probe",
            credential_id,
            field,
            digest,
            input_=key + "\n",
        )
        if result.returncode:
            raise RehearsalFailure("credential probe failed (output withheld)")
        try:
            return parse_probe(result.stdout)
        except (ValueError, TypeError):
            raise RehearsalFailure("credential probe summary rejected") from None

    def scenario_paired_restore_decrypt(self) -> None:
        if self.fixture.generation != 2:
            raise RehearsalFailure("paired restore must run in the fresh generation")
        postgres, smtp = (self.credential_ids[key] for key in ("postgres", "smtp"))
        rotated = self.secrets["notifier"][0]
        decrypted = self.credential_probe(postgres, "password", rotated)
        if decrypted != {"exported": True, "present": True, "match": True}:
            raise RehearsalFailure("restored credential did not decrypt")
        stale = self.credential_probe(postgres, "password", self.stale_notifier)
        if stale != {"exported": True, "present": True, "match": False}:
            raise RehearsalFailure("restored metadata lost the rotated credential")
        mail = self.credential_probe(smtp, "host", "mailpit")
        if mail != {"exported": True, "present": True, "match": True}:
            raise RehearsalFailure("restored SMTP credential did not decrypt")

    def scenario_wrong_key_fail_closed(self) -> None:
        # Positive control: the explicit-key path must decrypt with the right
        # key, so a refusal below is about the key and not a broken path.
        args = (
            self.credential_ids["postgres"],
            "password",
            self.secrets["notifier"][0],
        )
        right = self.credential_probe(*args, self.secrets["encryption"][0])
        if right != {"exported": True, "present": True, "match": True}:
            raise RehearsalFailure("the explicit-key path did not decrypt")
        wrong = self.credential_probe(*args, secrets.token_urlsafe(48))
        if wrong["match"]:
            raise RehearsalFailure("a mismatched encryption key decrypted the secret")
        self.fixture.receipt["wrong_key_facts"] = {"exported": wrong["exported"]}

    def test_actual_queue_runner_capture_unknown_reconcile_and_restore(self):
        scenario_error = finish_error = None
        scenario_traceback = finish_traceback = None
        try:
            self.run_scenario()
        except BaseException as error:
            scenario_error, scenario_traceback = error, error.__traceback__
        try:
            self.finish()
        except BaseException as error:
            finish_error, finish_traceback = error, error.__traceback__
        if scenario_error is not None:
            raise scenario_error.with_traceback(scenario_traceback)
        if finish_error is not None:
            raise finish_error.with_traceback(finish_traceback)

    def run_scenario(self):
        self.fixture.verify_prerequisites()
        self.secrets = self.fixture.create_secrets()
        self.fixture.create_networks()
        self.fixture.start_postgres("metadata-pg", self.secrets["metadata_pg"][1])
        self.start_dev_cluster()
        self.provision()
        self.fixture.start_valkey(self.secrets["valkey_server"][1])
        self.fixture.start_mailpit()
        self.fixture.start_n8n(self.secrets)
        self.fixture.start_runner(self.secrets["runner"][1])
        workflow_id, workflow_name = self.bind_and_import()

        first = self.publish("hy-home.docker", "1" * 64, "2026-10-16T01:00:00Z")
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success", "acknowledged")
        self.wait_state(first, "accepted_by_smtp")
        first_capture = self.capture(first)
        self.assertEqual(
            (1, True, True),
            (first_capture["total"], first_capture["matched"], first_capture["safe"]),
        )
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success")
        self.assertEqual(1, self.capture(first)["total"])

        second = self.publish("hy-home.k8s", "2" * 64, "2026-10-16T02:00:00Z")
        self.fixture.stop("mailpit")
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "error", "deliveryRedacted")
        self.wait_state(second, "unknown")
        self.fixture.stop("worker")
        self.fixture.stop("runner")
        # The lease columns exist only on ops_flow.outbox, which
        # opsflow_reader may not read (it sees delivery_status); audit as the
        # fixture superuser instead of widening the reader.
        self.assertEqual(
            "unknown|true|true|true|smtp_outcome_unknown",
            self.db_value(
                f"SELECT state||'|'||(accepted_at IS NULL)::text||'|'||(lease_token IS NULL)::text||'|'||(lease_until IS NULL)::text||'|'||coalesce(last_error_code,'') FROM ops_flow.outbox WHERE run_id='{second}';"
            ),
        )
        self.assertEqual(
            "0",
            self.db_value(
                "SELECT count(*) FROM pg_stat_activity WHERE datname='opsflow_dev' AND usename='opsflow_notifier';"
            ),
        )
        self.fixture.start("mailpit")
        self.fixture.create(
            "capture-probe",
            N8N_REF,
            "1000:1000",
            ("capture",),
            entrypoint="/bin/sh",
            command=("-ec", "exec sleep 60"),
        )
        self.fixture.start("capture-probe")
        self.assertEqual(1, self.capture(first, "capture-probe")["total"])
        self.fixture.remove("capture-probe")
        self.fixture.start("worker")
        self.fixture.start("runner")
        self.fixture.wait_until(
            lambda: self.fixture.logs_contain("worker", 'Registered runner "'),
            "external runner did not re-register",
            60,
        )
        unchanged_capture = self.capture(second)
        self.assertEqual(
            (1, False), (unchanged_capture["total"], unchanged_capture["matched"])
        )
        self.assertEqual(
            "unknown",
            self.db_value(
                f"SELECT state FROM ops_flow.delivery_status WHERE run_id='{second}';",
                "opsflow_reader",
            ),
        )
        self.assertEqual(
            "",
            self.db_value(
                "SELECT id FROM ops_flow.claim_notification();", "opsflow_notifier"
            ),
        )
        self.fixture.stop("worker")
        self.fixture.stop("runner")
        evidence = hashlib.sha256(
            ("smtp_connect_failure_before_acceptance:" + second).encode()
        ).hexdigest()
        outbox_id = self.db_value(
            f"SELECT id FROM ops_flow.outbox WHERE run_id='{second}';"
        )
        if not outbox_id.isdecimal():
            raise RehearsalFailure("outbox safe ID rejected")
        denied = self.fixture.psql(
            "opsflow_notifier",
            "opsflow_dev",
            f"SELECT ops_flow.reconcile_notification({outbox_id},'not_sent','{evidence}');",
            check=False,
        )
        self.assertNotEqual(0, denied.returncode)
        self.assertIn("42501", denied.stderr)
        self.assertEqual(
            "t",
            self.db_value(
                f"SET ROLE opsflow_owner;SELECT ops_flow.reconcile_notification({outbox_id},'not_sent','{evidence}');",
                "opsflow_migrator",
            ),
        )
        self.assertEqual(
            f"1|not_sent|{evidence}",
            self.db_value(
                f"SELECT attempt||'|'||result||'|'||evidence_sha256 FROM ops_flow.notification_reconciliations WHERE outbox_id={outbox_id} AND attempt=1;"
            ),
        )
        self.fixture.start("worker")
        self.fixture.start("runner")
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success", "acknowledged")
        self.wait_state(second, "accepted_by_smtp")
        second_capture = self.capture(second)
        self.assertEqual(
            (2, True, True),
            (
                second_capture["total"],
                second_capture["matched"],
                second_capture["safe"],
            ),
        )

        self.fixture.receipt.update(initial_receipt())
        for name, action in self.generation_1_scenarios(workflow_id):
            self.step(name, action)

        self.restore_and_restart()
        restored = self.api("workflows").get("rows")
        self.assertEqual(
            1,
            len(
                [
                    row
                    for row in restored
                    if row.get("name") == workflow_name and row.get("active") is False
                ]
            ),
        )
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success")
        self.assertEqual(0, self.capture(first)["total"])
        third = self.publish("Project-Template", "3" * 64, "2026-10-16T03:00:00Z")
        execution = self.run_manual(workflow_id)
        self.await_execution(execution, "success", "acknowledged")
        self.wait_state(third, "accepted_by_smtp")
        self.assertEqual(
            (1, True, True),
            tuple(self.capture(third)[key] for key in ("total", "matched", "safe")),
        )
        self.assertEqual(
            evidence,
            self.db_value(
                f"SELECT evidence_sha256 FROM ops_flow.notification_reconciliations WHERE outbox_id={outbox_id} AND attempt=1;"
            ),
        )
        for name, action in self.restore_scenarios():
            self.step(name, action)
        self.require_criterion_22_pass()
        self.fixture.receipt.update(
            {
                "native": "PASS",
                "queue_runner": "PASS",
                "smtp_connect_failure_before_acceptance": "PASS",
                "restore": "PASS",
                "response_loss_after_acceptance": "NOT_RUN",
                "exactly_once": "NOT_CLAIMED",
            }
        )

    def restore_and_restart(self) -> None:
        for role in ("runner", "worker", "main", "mailpit", "valkey"):
            self.fixture.stop(role)
        self.assertEqual(
            "0",
            self.db_value(
                "SELECT count(*) FROM pg_stat_activity WHERE datname='opsflow_dev' AND pid<>pg_backend_pid();"
            ),
        )
        self.assertEqual(
            "0",
            self.fixture.psql(
                "n8n",
                "n8n",
                "SELECT count(*) FROM pg_stat_activity WHERE datname='n8n' AND pid<>pg_backend_pid();",
                container="metadata-pg",
            ).stdout.strip(),
        )
        self.fixture.exec(
            "metadata-pg",
            "pg_dump",
            "-Fc",
            "--create",
            "-U",
            "n8n",
            "-d",
            "n8n",
            "-f",
            "/fixture/metadata.dump",
        )
        self.fixture.exec(
            "dev-pg",
            "pg_dumpall",
            "--roles-only",
            "--no-role-passwords",
            "-U",
            "p04_audit",
            "-f",
            "/fixture/dev-roles.sql",
        )
        self.fixture.exec(
            "dev-pg",
            "pg_dump",
            "-Fc",
            "--create",
            "-U",
            "p04_audit",
            "-d",
            "opsflow_dev",
            "-f",
            "/fixture/dev.dump",
        )
        self.validate_dump("metadata-pg", "metadata.dump")
        self.validate_dump("dev-pg", "dev-roles.sql", max_bytes=2 * 1024 * 1024)
        self.validate_dump("dev-pg", "dev.dump")
        for role in tuple(reversed(self.fixture.containers)):
            self.fixture.remove(role)
        self.fixture.generation = 2
        self.fixture.start_postgres("metadata-pg", self.secrets["metadata_pg"][1])
        self.start_dev_cluster()
        self.validate_dump("metadata-pg", "metadata.dump")
        self.validate_dump("dev-pg", "dev-roles.sql", max_bytes=2 * 1024 * 1024)
        self.validate_dump("dev-pg", "dev.dump")
        self.fixture.exec(
            "metadata-pg",
            "pg_restore",
            "--exit-on-error",
            "--clean",
            "--if-exists",
            "--create",
            "-U",
            "n8n",
            "-d",
            "postgres",
            "/fixture/metadata.dump",
        )
        roles_bytes = self.fixture.exec(
            "dev-pg", "cat", "/fixture/dev-roles.sql"
        ).encode()
        # roles_restore_error_is_expected reads `psql:<stdin>:N:` locations,
        # which psql prints for `-f -`; the database rehearsal does the same.
        role_restore = self.fixture.exec_result(
            "dev-pg",
            "psql",
            "-X",
            "-qAt",
            "-v",
            "ON_ERROR_STOP=0",
            "-v",
            "VERBOSITY=verbose",
            "-U",
            "p04_audit",
            "-d",
            "postgres",
            "-f",
            "-",
            input_=roles_bytes.decode(),
        )
        if not roles_restore_error_is_expected(
            roles_bytes, role_restore.stderr.encode(), role_restore.returncode
        ):
            raise RehearsalFailure("DEV roles restore errors rejected")
        self.fixture.exec(
            "dev-pg",
            "pg_restore",
            "--exit-on-error",
            "--create",
            "-U",
            "p04_audit",
            "-d",
            "postgres",
            "/fixture/dev.dump",
        )
        password_sql = ""
        for role in ("migrator", "ingest", "notifier", "reader"):
            value = self.secrets[role][0]
            if not re.fullmatch(r"[A-Za-z0-9_-]{32,128}", value):
                raise RehearsalFailure("synthetic restore secret shape rejected")
            password_sql += f"ALTER ROLE opsflow_{role} PASSWORD '{value}';"
        self.fixture.psql(
            "p04_audit",
            "postgres",
            password_sql,
        )
        self.fixture.start_valkey(self.secrets["valkey_server"][1])
        self.fixture.start_mailpit()
        self.fixture.start_n8n(self.secrets)
        self.fixture.start_runner(self.secrets["runner"][1])
