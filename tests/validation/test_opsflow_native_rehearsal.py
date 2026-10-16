"""Default guards and opt-in actual n8n queue/runner/SMTP/restore rehearsal."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import unittest
from copy import deepcopy
from pathlib import Path

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
async function login(){return (await call('/rest/login','POST',{emailOrLdapLoginId:input.email,password:input.password})).cookie;}
(async()=>{let out;
 if(input.action==='setup'){const r=await call('/rest/owner/setup','POST',{email:input.email,firstName:'Opsflow',lastName:'Fixture',password:input.password});out={id:r.data.id};}
 else {const cookie=await login(); const auth={cookie};
  if(input.action==='credential'){const r=await call('/rest/credentials','POST',input.credential,auth);out={id:r.data.id};}
  else if(input.action==='workflows'){const r=await call('/rest/workflows?take=100','GET',undefined,auth);const rows=r.data.results||r.data.data||r.data;out={rows:rows.map(x=>({id:x.id,name:x.name,active:x.active,versionId:x.versionId}))};}
  else if(input.action==='run'){const r=await call('/rest/workflows/'+encodeURIComponent(input.workflowId)+'/run','POST',{triggerToStartFrom:{name:'Manual'}},auth);out={executionId:r.data.executionId};}
  else if(input.action==='execution'){const r=await call('/rest/executions/'+encodeURIComponent(input.executionId),'GET',undefined,auth);const d=r.data;
   const parsed=typeof d.data==='string'?require('flatted').parse(d.data):d.data;const rd=parsed?.resultData?.runData||{};
   const ns=n=>{const rows=rd[n]||[];return rows.length?String(rows[rows.length-1].executionStatus||'unknown'):'absent';};
   out={id:String(d.id),status:String(d.status),finished:Boolean(d.finished),terminal:Boolean(d.stoppedAt),acknowledged:ns('Acknowledged'),deliveryRedacted:ns('Redact Delivery Uncertain')};}
  else throw new Error('unknown_action');
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
        body = {
            "action": action,
            "email": self.email,
            "password": self.secrets["owner"][0],
            **payload,
        }
        result = self.fixture.exec_result(
            "main", "node", "-e", API_JS, input_=json.dumps(body, separators=(",", ":"))
        )
        if result.returncode:
            self.fixture.receipt["last_body_fetch_failure"] = body_fetch_failure_facts(
                result, "n8n_api"
            )
            raise RehearsalFailure("n8n REST operation failed (payload withheld)")
        try:
            return json.loads(result.stdout)
        except (ValueError, TypeError):
            raise RehearsalFailure("n8n REST safe summary rejected") from None

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
            or stat.S_IMODE(metadata.st_mode) != 0o600
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

    def bind_and_import(self) -> tuple[str, str]:
        setup = self.api("setup")
        owner_id = setup.get("id")
        if not isinstance(owner_id, str) or not UUID.fullmatch(owner_id):
            raise RehearsalFailure("owner setup safe ID rejected")
        postgres = self.api(
            "credential",
            credential={
                "name": "opsflow-native-postgres",
                "type": "postgres",
                "data": {
                    "host": "dev-pg",
                    "database": "opsflow_dev",
                    "user": "opsflow_notifier",
                    "password": self.secrets["notifier"][0],
                    "maxConnections": 2,
                    "ssl": "disable",
                    "port": 5432,
                },
            },
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

        def probe() -> bool:
            summary = self.api("execution", executionId=execution_id)
            if summary.get("id") != execution_id:
                raise RehearsalFailure("execution safe ID changed")
            if summary.get("status") in {"success", "error", "canceled", "crashed"}:
                terminal.update(summary)
                return True
            return False

        self.fixture.wait_until(probe, "queued execution did not become terminal", 60)
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
        self.assertEqual(
            "unknown|true|true|true|smtp_outcome_unknown",
            self.db_value(
                f"SELECT state||'|'||(accepted_at IS NULL)::text||'|'||(lease_token IS NULL)::text||'|'||(lease_until IS NULL)::text||'|'||coalesce(last_error_code,'') FROM ops_flow.outbox WHERE run_id='{second}';",
                "opsflow_reader",
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
            "/fixture/dev-roles.sql",
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
