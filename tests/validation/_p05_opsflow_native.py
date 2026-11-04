"""Current-artifact P05 fixture; historical v3 native sources remain unchanged."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

from tests.validation import _opsflow_native_evidence as evidence
from tests.validation import _opsflow_native_fixture as legacy
from tests.validation import _opsflow_native_inputs as inputs
from tests.validation import _p05_opsflow_recovery as recovery
from tests.validation import _p05_opsflow_registration as registration
from tests.validation import test_opsflow_native_rehearsal as historical
from tests.validation._opsflow_native_fixture import RehearsalFailure
from tests.validation.test_opsflow_database_rehearsal import migration_sql, publish_sql

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = (
    ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/nodes/OpsflowSmtp"
)
ANALYSIS = ROOT / "_workspace/repo-support/analysis/p05"
# The active-send hold replaces the stopped Mailpit under its alias and reuses
# the ephemeral capture-probe caps, so the reviewed aggregate does not grow.
HOLD = "smtp-hold"


def validate_artifact(value, expected_binding, expected_dist):
    fields = {"reference", "image_id", "base_id", "binding", "dist_sha256"}
    if (
        not isinstance(value, dict)
        or set(value) != fields
        or value["base_id"] != inputs.N8N_ID
        or value["binding"] != expected_binding
        or not isinstance(expected_binding, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_binding) is None
        or value["reference"] != "hy-home/p05-n8n-fixture:" + expected_binding[:12]
        or not isinstance(value["image_id"], str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", value["image_id"]) is None
        or value["dist_sha256"] != expected_dist
        or not {"OpsflowSmtp.node.js", "transport.js"} <= set(expected_dist)
        or any(
            not isinstance(name, str)
            or "/" in name
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            for name, digest in expected_dist.items()
        )
    ):
        raise RehearsalFailure("current fixture artifact binding rejected")
    return {**value, "dist_sha256": dict(expected_dist)}


def public_digest(path, *, read_bytes=False):
    """Read a stable regular public artifact without following any symlink."""
    absolute = path.absolute()
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in absolute.parts[1:-1]:
            selected = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=directory,
            )
            os.close(directory)
            directory = selected
        descriptor = os.open(
            absolute.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory
        )
    except OSError:
        raise RehearsalFailure("public artifact path rejected") from None
    finally:
        os.close(directory)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RehearsalFailure("public artifact identity rejected")
        digest = hashlib.sha256()
        chunks = []
        while block := os.read(descriptor, 65536):
            digest.update(block)
            if read_bytes:
                chunks.append(block)
        after = os.fstat(descriptor)
        observed = absolute.stat(follow_symlinks=False)

        def fields(item):
            return (
                item.st_dev,
                item.st_ino,
                item.st_size,
                item.st_mtime_ns,
                item.st_ctime_ns,
            )

        if fields(before) != fields(after) or fields(after) != fields(observed):
            raise RehearsalFailure("public artifact changed during collection")
        return b"".join(chunks) if read_bytes else digest.hexdigest()
    finally:
        os.close(descriptor)


def runtime_lock():
    value = json.loads(public_digest(PACKAGE / "package-lock.json", read_bytes=True))
    selected = {
        "name": value["name"],
        "version": value["version"],
        "lockfileVersion": 3,
        "requires": True,
        "packages": {
            "node_modules/nodemailer": value["packages"]["node_modules/nodemailer"]
        },
    }
    return (json.dumps(selected, sort_keys=True, indent=2) + "\n").encode()


def deployment_files():
    selected = {
        name: public_digest(PACKAGE / name)
        for name in ("package.json", "package-lock.json")
    }
    selected |= {
        "dist/" + path.name: public_digest(path)
        for path in (PACKAGE / "dist").iterdir()
        if path.is_file()
    }
    dependency = PACKAGE / "node_modules/nodemailer"
    selected |= {
        "node_modules/nodemailer/" + str(path.relative_to(dependency)): public_digest(
            path
        )
        for path in dependency.rglob("*")
        if path.is_file()
    }
    selected["node_modules/.package-lock.json"] = hashlib.sha256(
        runtime_lock()
    ).hexdigest()
    manifest = "".join(
        digest + "  " + name + "\n" for name, digest in sorted(selected.items())
    ).encode()
    return {**selected, "SHA256SUMS": hashlib.sha256(manifest).hexdigest()}


def validate_deployment(rows, expected):
    if not isinstance(rows, list) or not rows or len(rows) > 1024:
        raise RehearsalFailure("public deployment metadata rejected")
    observed, names, directories = {}, set(), 0
    for row in rows:
        if not isinstance(row, dict) or row.get("kind") not in {"file", "directory"}:
            raise RehearsalFailure("public deployment kind rejected")
        file = row["kind"] == "file"
        fields = {"name", "kind", "uid", "gid", "mode"} | (
            {"sha256"} if file else set()
        )
        name = row.get("name")
        if (
            set(row) != fields
            or not isinstance(name, str)
            or name in names
            or not (name == "opsflow" or name.startswith("opsflow/"))
            or any(part in {"", ".", ".."} for part in name.split("/"))
            or any(type(row[key]) is not int for key in ("uid", "gid", "mode"))
            or row["uid"] != 0
            or row["gid"] != 0
            or row["mode"] != (0o644 if file else 0o755)
        ):
            raise RehearsalFailure("public deployment identity rejected")
        names.add(name)
        if file:
            observed[name.removeprefix("opsflow/")] = row["sha256"]
        else:
            directories += 1
    if "opsflow" not in names or observed != expected:
        raise RehearsalFailure("public deployment content rejected")
    return {"files": len(observed), "directories": directories}


def current_binding():
    source = {path.name: public_digest(path) for path in sorted(PACKAGE.glob("*.ts"))}
    for name in ("package.json", "package-lock.json", "tsconfig.json"):
        source[name] = public_digest(PACKAGE / name)
    dist = {
        path.name: public_digest(path)
        for path in sorted((PACKAGE / "dist").iterdir())
        if path.is_file()
    }
    dependency = PACKAGE / "node_modules/nodemailer"
    dependencies = {
        "nodemailer/" + str(path.relative_to(dependency)): public_digest(path)
        for path in sorted(dependency.rglob("*"))
        if path.is_file()
    }
    binding = hashlib.sha256(
        json.dumps(
            {
                "base_id": inputs.N8N_ID,
                "source": source,
                "dist": dist,
                "dependencies": dependencies,
                "deployment_owner": {"uid": 0, "gid": 0},
                "runtime_lock_sha256": hashlib.sha256(runtime_lock()).hexdigest(),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return binding, dist


def local_artifact():
    value = json.loads((ANALYSIS / "candidate-artifact.json").read_text())
    binding, dist = current_binding()
    return validate_artifact(value, binding, dist)


class P05Fixture(legacy.NativeFixture):
    def __init__(self, artifact):
        binding, dist = current_binding()
        self.artifact = validate_artifact(artifact, binding, dist)
        super().__init__()
        self.receipt["task"] = "SPEC-0212-TSK-0044"
        self.receipt["candidate"] = {
            key: self.artifact[key]
            for key in ("reference", "image_id", "base_id", "binding")
        }
        self.smtp_epoch = 1

    def prepare_smtp(self):
        binary = shutil.which("openssl")
        if binary is None:
            raise RehearsalFailure("fixture TLS generator unavailable")
        commands = (
            (
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                "p05-ca.key",
                "-out",
                "p05-ca.pem",
                "-days",
                "1",
                "-subj",
                "/CN=P05 Synthetic CA",
                "-addext",
                "basicConstraints=critical,CA:TRUE",
            ),
            (
                "req",
                "-new",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                "p05-server.key",
                "-out",
                "p05-server.csr",
                "-subj",
                "/CN=mailpit",
            ),
            (
                "x509",
                "-req",
                "-in",
                "p05-server.csr",
                "-CA",
                "p05-ca.pem",
                "-CAkey",
                "p05-ca.key",
                "-CAcreateserial",
                "-out",
                "p05-server.pem",
                "-days",
                "1",
                "-extfile",
                "p05-server.ext",
            ),
        )
        self.private(
            "p05-server.ext",
            "subjectAltName=DNS:mailpit\nextendedKeyUsage=serverAuth\n",
        )
        for command in commands:
            subprocess.run(
                (binary, *command),
                cwd=self.directory,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
                check=True,
            )
        for name in (
            "p05-ca.key",
            "p05-ca.pem",
            "p05-server.key",
            "p05-server.csr",
            "p05-ca.srl",
            "p05-server.pem",
        ):
            path = self.directory / name
            path.chmod(0o600)
            item = path.stat(follow_symlinks=False)
            if (
                not stat.S_ISREG(item.st_mode)
                or item.st_nlink != 1
                or item.st_uid != self.host_uid
            ):
                raise RehearsalFailure("fixture TLS file identity rejected")
            self.files[path] = evidence.PrivateFile(
                path, item.st_dev, item.st_ino, item.st_uid, item.st_gid, 0o600
            )
        self.smtp_values = {epoch: secrets.token_urlsafe(32) for epoch in (1, 2)}
        self.smtp_files = {
            epoch: self.private(
                f"p05-smtp-{epoch}.secret", "p05-capture:" + value + "\n"
            )
            for epoch, value in self.smtp_values.items()
        }

    def _n8n_env(self):
        return (*super()._n8n_env(), "NODE_EXTRA_CA_CERTS=/run/secrets/p05-ca.pem")

    def start_n8n(self, values):
        # The historical raw-log custody schema admits exactly its old files.
        # This TLS fixture keeps only the existing closed readiness facts.
        def closed_diagnostic(_directory, _files, receipt, _result):
            receipt["p05_readiness_evidence"] = "CLOSED_FACTS_ONLY"

        with mock.patch.object(
            evidence, "retain_failure_output", side_effect=closed_diagnostic
        ):
            return super().start_n8n(values)

    @contextmanager
    def roles(self):
        with mock.patch.multiple(
            legacy,
            ALIASES={**inputs.ALIASES, HOLD: "mailpit"},
            RESOURCE_CAPS={
                **inputs.RESOURCE_CAPS,
                HOLD: inputs.RESOURCE_CAPS["capture-probe"],
            },
            TMPFS={**inputs.TMPFS, HOLD: inputs.TMPFS["capture-probe"]},
        ):
            yield

    def _verify_container(self, record):
        with self.roles():
            return super()._verify_container(record)

    @contextmanager
    def bindings(self):
        selected = {
            self.artifact["reference"]: self.artifact["image_id"],
            inputs.PG_ID: inputs.PG_ID,
            inputs.VALKEY_ID: inputs.VALKEY_ID,
            inputs.MAILPIT_ID: inputs.MAILPIT_ID,
            inputs.RUNNER_REF: inputs.RUNNER_ID,
        }
        with (
            mock.patch.multiple(
                legacy,
                IMAGE_IDS=selected,
                N8N_REF=self.artifact["reference"],
                N8N_ID=self.artifact["image_id"],
                N8N_LABELS={
                    "hyhome.source-binding": self.artifact["binding"],
                    "hyhome.p05.base-id": inputs.N8N_ID,
                    "hyhome.p05.fixture": "1",
                },
                PG_REF=inputs.PG_ID,
                VALKEY_REF=inputs.VALKEY_ID,
                MAILPIT_REF=inputs.MAILPIT_ID,
            ),
            self.roles(),
        ):
            yield

    def verify_prerequisites(self):
        with self.bindings():
            super().verify_prerequisites()

    def create(self, role, image, user, networks, **kwargs):
        translated = {
            inputs.N8N_REF: self.artifact["reference"],
            inputs.PG_REF: inputs.PG_ID,
            inputs.VALKEY_REF: inputs.VALKEY_ID,
            inputs.MAILPIT_REF: inputs.MAILPIT_ID,
        }.get(image, image)
        allowed = {
            "metadata-pg": inputs.PG_ID,
            "dev-pg": inputs.PG_ID,
            "valkey": inputs.VALKEY_ID,
            "secret-prep": inputs.VALKEY_ID,
            "main": self.artifact["reference"],
            "worker": self.artifact["reference"],
            "capture-probe": self.artifact["reference"],
            "runner": inputs.RUNNER_REF,
            "mailpit": inputs.MAILPIT_ID,
            HOLD: self.artifact["reference"],
        }
        if role not in allowed or translated != allowed[role]:
            raise RehearsalFailure("current fixture role/image combination rejected")
        if role in {"main", "worker"}:
            kwargs = {
                **kwargs,
                "mounts": (
                    *kwargs.get("mounts", ()),
                    inputs.bind_mount(
                        self.directory / "p05-ca.pem", "/run/secrets/p05-ca.pem"
                    ),
                ),
            }
        with self.bindings():
            return super().create(role, translated, user, networks, **kwargs)

    def start_mailpit(self):
        directory = self.directory / f"mailpit-data-{self.generation}"
        if not directory.exists():
            directory.mkdir(mode=0o700)
            item = directory.stat(follow_symlinks=False)
            self.mailpit_dirs[directory] = (item.st_dev, item.st_ino)
        item = directory.stat(follow_symlinks=False)
        if (
            self.mailpit_dirs.get(directory) != (item.st_dev, item.st_ino)
            or stat.S_IMODE(item.st_mode) != 0o700
            or item.st_uid != self.host_uid
        ):
            raise RehearsalFailure("owned SMTP store identity rejected")
        env = (
            "MP_DATABASE=/data/mailpit.db",
            "MP_UI_BIND_ADDR=0.0.0.0:8025",
            "MP_SMTP_BIND_ADDR=0.0.0.0:1025",
            "MP_MAX_MESSAGES=32",
            "MP_SMTP_AUTH_FILE=/run/secrets/smtp-auth",
            "MP_SMTP_TLS_CERT=/run/secrets/server.pem",
            "MP_SMTP_REQUIRE_STARTTLS=true",
            "MP_SMTP_AUTH_ALLOW_INSECURE=false",
            "MP_SMTP_DISABLE_RDNS=true",
            "MP_DISABLE_VERSION_CHECK=true",
        )
        mounts = (
            inputs.bind_mount(directory, "/data", readonly=False),
            inputs.bind_mount(
                self.smtp_files[self.smtp_epoch], "/run/secrets/smtp-auth"
            ),
            inputs.bind_mount(
                self.directory / "p05-server.pem", "/run/secrets/server.pem"
            ),
            inputs.bind_mount(
                self.directory / "p05-server.key", "/run/secrets/server.key"
            ),
        )
        self.create(
            "mailpit",
            inputs.MAILPIT_REF,
            "1000:1000",
            ("capture",),
            env=env,
            mounts=mounts,
            command=("--smtp-tls-key=/run/secrets/server.key",),
        )
        self.start("mailpit")

    def start_smtp_hold(self):
        state = self._verify_owned(self.containers["mailpit"]).get("State") or {}
        if state.get("Running") is not False:
            raise RehearsalFailure("SMTP hold requires the stopped capture")
        self.create(
            HOLD,
            self.artifact["reference"],
            "1000:1000",
            ("capture",),
            mounts=tuple(
                inputs.bind_mount(self.directory / name, "/run/secrets/" + target)
                for name, target in (
                    ("p05-server.pem", "server.pem"),
                    ("p05-server.key", "server.key"),
                )
            ),
            entrypoint="node",
            command=("-e", recovery.HOLD_JS),
        )
        self.start(HOLD)
        self.wait_until(
            lambda: self.logs_contain(HOLD, "P05_HOLD LISTENING"),
            "SMTP hold readiness expired",
            30,
        )

    def hold_facts(self):
        record = self.containers[HOLD]
        self._verify_container(record)
        result = self.client.run_result("logs", record.cid)
        if result.returncode:
            raise RehearsalFailure("SMTP hold log unavailable")
        return recovery.parse_hold(result.stdout)

    def kill(self, role):
        # SIGKILL, not `docker stop`: no graceful shutdown can let the node
        # finish or the transport's own socket timeout end the session.
        record = self.containers[role]
        self._verify_container(record)
        if self.client.run_result("kill", record.cid).returncode:
            raise RehearsalFailure("owned container kill failed")
        self.wait_until(
            lambda: (
                (self._verify_owned(record).get("State") or {}).get("Running") is False
            ),
            "owned container remained running after kill",
            10,
        )

    def receipt_json(self):
        value = json.loads(super().receipt_json())
        return json.dumps(
            {
                **value,
                "image_id": self.artifact["image_id"],
                "source_binding": self.artifact["binding"],
            },
            sort_keys=True,
        )


PROFILE_API = historical.API_JS.replace(
    "else if(input.action==='credential_update')",
    """else if(input.action==='profile'){const w=(await call('/rest/workflows/'+encodeURIComponent(input.workflowId),'GET',undefined,auth)).data;
const nodes=w.nodes.map(n=>n.type==='n8n-nodes-opsflow.opsflowSmtp'?{...n,parameters:{...n.parameters,captureProfile:'mailpit-starttls-auth-v1'}}:n);
if(!nodes.some(n=>n.parameters?.captureProfile==='mailpit-starttls-auth-v1'))throw new Error('profile_target_absent');
const r=await call('/rest/workflows/'+encodeURIComponent(input.workflowId),'PATCH',{name:w.name,nodes,connections:w.connections,settings:w.settings,versionId:w.versionId},auth);out={id:r.data.id};}
else if(input.action==='credential_update')""",
)
PROFILE_API = PROFILE_API.replace(
    "else if(input.action==='profile')", registration.CREATE_BRANCH
)
# n8n's own retry of a crashed execution (REST /executions/:id/retry, the
# editor's "Retry with original workflow"); it resolves on completion.
PROFILE_API = PROFILE_API.replace(
    "else if(input.action==='credential_update')",
    """else if(input.action==='retry'){const r=await call('/rest/executions/'+encodeURIComponent(input.executionId)+'/retry','POST',{loadWorkflow:false},auth);const d=r.data;
out={id:String(d.id),retryOf:String(d.retryOf),status:String(d.status)};}
else if(input.action==='trace'){const d=(await call('/rest/executions/'+encodeURIComponent(input.executionId),'GET',undefined,auth)).data;
const x=typeof d.data==='string'?require('flatted').parse(d.data):d.data;const nm=v=>/^[A-Za-z0-9 _.-]{1,64}$/.test(String(v))?String(v):'withheld';
const rd=x?.resultData||{};const e=rd.error;
out={stack:(x?.executionData?.nodeExecutionStack||[]).map(i=>nm(i?.node?.name)),runNodes:Object.keys(rd.runData||{}).map(nm),last:rd.lastNodeExecuted?nm(rd.lastNodeExecuted):'',error:e?{name:nm(e.name),node:e.node?nm(e.node.name):''}:null};}
else if(input.action==='credential_update')""",
)


class P05Scenario(historical.OpsflowN8nNativeRehearsal):
    def bind_and_import(self):
        return registration.register(self)

    def phase(self, name):
        self.fixture.receipt["phase"] = name
        print("P05_NATIVE_PHASE " + name, flush=True)

    def setUp(self):
        self.fixture = P05Fixture(local_artifact())
        self.secrets = {}
        self.email = f"owner-{self.fixture.attempt}@opsflow.invalid"
        self._finished = False
        self.credential_ids = {}
        self.execution_ids = []
        self.published = 0
        self.stale_notifier = ""
        self.inputs = []
        self.runs = []

    def api(self, action, **payload):
        with mock.patch.object(historical, "API_JS", PROFILE_API):
            return super().api(action, **payload)

    def provision(self):
        super().provision()
        sql = historical.PG_WORKLOAD / "sql"
        for name in ("005_data_version.sql", "007_notification_recovery.sql"):
            self.fixture.psql(
                "opsflow_migrator", "opsflow_dev", migration_sql(sql / name)
            )
        self.fixture.psql(
            "p04_audit",
            "opsflow_dev",
            "\\set migration_sha256 '"
            + hashlib.sha256(
                (sql / "007_notification_recovery.sql").read_bytes()
            ).hexdigest()
            + "'\n"
            + (sql / "008_checks.sql").read_text(),
        )

    def update_smtp(self, epoch):
        credential = {
            "name": "p05-native-smtp",
            "type": "smtp",
            "data": {
                "user": "p05-capture",
                "password": self.fixture.smtp_values[epoch],
                "host": "mailpit",
                "port": 1025,
                "secure": False,
                "disableStartTls": False,
                "hostName": "",
            },
        }
        identifier = self.credential_ids["smtp"]
        changed = self.api(
            "credential_update", credentialId=identifier, credential=credential
        )
        if str(changed.get("id")) != identifier:
            raise RehearsalFailure("same credential identity changed")

    def execute(self, workflow, state):
        execution = self.run_manual(workflow)
        self.execution_ids.append(execution)
        self.await_execution(
            execution, state, "acknowledged" if state == "success" else None
        )
        return execution

    def publish_input(self, label, captured):
        item = ("hy-home.k8s", hashlib.sha256(label).hexdigest(), captured)
        run = self.publish(*item)
        self.inputs.append(item)
        self.runs.append(run)
        return run

    def outbox_snapshot(self):
        return recovery.snapshot_lines(self.db_value(recovery.SNAPSHOT_SQL))

    def execution_status(self, execution):
        seen = {}

        def terminal():
            summary = self.api("execution", executionId=execution)
            if summary.get("terminal") is True:
                seen["status"] = str(summary.get("status"))
            return "status" in seen

        try:
            self.fixture.wait_until(
                terminal, "interrupted execution did not settle", 60
            )
        except RehearsalFailure:
            return "not_terminal"
        return seen["status"]

    def interrupt_active_send(self, workflow, label, captured, *, kill_main=False):
        f = self.fixture
        run = self.publish_input(label, captured)
        f.stop("mailpit")
        f.start_smtp_hold()
        execution = self.run_manual(workflow)
        self.execution_ids.append(execution)
        f.wait_until(
            lambda: f.hold_facts()["body_held_at_ms"] is not None,
            "SMTP session was not held mid-DATA",
            60,
        )
        held = f.hold_facts()
        f.kill("worker")
        self.killed_at = time.monotonic()
        # Host and container read the same kernel wall clock; measuring after
        # the kill returns is an upper bound on the interruption point.
        killed_ms = int(time.time() * 1000) - held["body_held_at_ms"]
        if kill_main:
            # Main dies with the worker: its in-memory wait for the job is lost.
            f.kill("main")
        f.wait_until(
            lambda: f.hold_facts()["closed_after_body_ms"] is not None,
            "held SMTP session did not close after the kill",
            10,
        )
        facts = {
            "data_started": held["data_started"],
            "session_open_at_kill": held["closed_after_body_ms"] is None,
            "body_to_kill_ms": killed_ms,
            "body_to_close_ms": f.hold_facts()["closed_after_body_ms"],
            "state_after_kill": self.db_value(
                f"SELECT state FROM ops_flow.outbox WHERE run_id='{run}';"
            ),
            "execution_status": "main_down"
            if kill_main
            else self.execution_status(execution),
        }
        key = "main_restart_interruption" if kill_main else "active_send_interruption"
        f.receipt[key] = facts
        f.remove(HOLD)
        f.receipt[key] = recovery.validate_interruption(facts)
        return run

    def broker_jobs(self, ids, role="main"):
        result = self.fixture.exec_result(
            role, "node", "-e", recovery.QUEUE_PROBE, input_=json.dumps({"ids": ids})
        )
        if result.returncode:
            raise RehearsalFailure("exact old broker job probe unavailable")
        return json.loads(result.stdout)

    def recover_interrupted(self, workflow, run):
        f = self.fixture
        interrupted = self.execution_ids[-1]
        f.receipt["interrupted_execution_id"] = interrupted
        # Closed count only: whether the interrupted job outlived its worker.
        before = recovery.broker_job_count(
            self.broker_jobs([interrupted]), [interrupted]
        )
        f.receipt["interrupted_broker_job_matching"] = before
        for role in ("mailpit", "worker", "runner"):
            f.start(role)
        self.await_worker_and_capture()
        # n8n's own recovery only: the restarted worker fails and deletes the
        # stalled job and main marks the execution crashed. The rehearsal
        # removes nothing from the queue.
        started = time.monotonic()
        after = self.settle_job(interrupted)
        f.receipt["interrupted_queue_recovery_seconds"] = round(
            time.monotonic() - started, 3
        )
        facts = {
            "jobs_before_restart": before,
            "jobs_after_recovery": after,
            "execution_status": self.execution_status(interrupted),
        }
        f.receipt["interrupted_queue_recovery"] = facts
        recovery.validate_queue_recovery(facts)
        f.receipt["interrupted_recovery"] = self.quarantine_interrupted(
            workflow, run, b"p05-after-interruption", "2026-11-28T00:00:00Z"
        )

    def await_worker_and_capture(self):
        f = self.fixture
        for target, seconds in (
            ("http://127.0.0.1:5679/healthz", 300),
            ("http://mailpit:8025/readyz", 60),
        ):
            f.wait_until(
                lambda target=target: legacy.node_status_probe(
                    lambda *args: f.exec_result("worker", *args), target
                )[0],
                "recovered worker or capture readiness expired",
                seconds,
            )
        f.wait_until(
            lambda: f.logs_contain("worker", 'Registered runner "'),
            "external runner did not re-register",
            60,
        )

    def settle_job(self, execution, role="main"):
        # Waits only for n8n itself to remove the job; returns the final count.
        f = self.fixture
        try:
            f.wait_until(
                lambda: (
                    recovery.broker_job_count(
                        self.broker_jobs([execution], role), [execution]
                    )
                    == 0
                ),
                "n8n did not settle the interrupted queue job",
                recovery.STALL_RECOVERY_SECONDS,
            )
        except RehearsalFailure as error:
            # Only the settle timeout is recorded and validated by the caller;
            # any other failure (probe, headroom) propagates unchanged.
            if str(error) != "n8n did not settle the interrupted queue job":
                raise
        return recovery.broker_job_count(
            self.broker_jobs([execution], role), [execution]
        )

    def quarantine_interrupted(self, workflow, run, label, captured):
        # Fixture-only time travel as the superuser (as fast_forward_sql does)
        # instead of waiting out the 10-minute lease; the notifier cannot.
        expired = self.db_value(
            "UPDATE ops_flow.outbox SET lease_until=clock_timestamp() "
            f"WHERE run_id='{run}' AND state='sending' RETURNING id;"
        )
        if not expired.isdecimal():
            raise RehearsalFailure("interrupted lease was not left sending")
        fresh = self.publish_input(label, captured)
        self.execute(workflow, "success")
        self.wait_state(fresh, "accepted_by_smtp")
        observed = (
            self.db_value(
                "SELECT state||'|'||attempts||'|'||coalesce(last_error_code,'') "
                f"FROM ops_flow.outbox WHERE run_id='{run}';"
            ),
            self.capture(run)["matched"],
            self.capture(fresh)["matched"],
        )
        # claim_notification turns the expired lease unknown without a send
        # or a new attempt; only the fresh row is claimed and delivered.
        if observed != ("unknown|1|lease_expired_delivery_unknown", False, True):
            raise RehearsalFailure("interrupted notification was resent or reclaimed")
        return {
            "state": "unknown",
            "last_error_code": "lease_expired_delivery_unknown",
            "attempts": 1,
            "resent": False,
            "fresh_after_recovery": "accepted_by_smtp",
        }

    def metadata_execution(self, execution):
        # Closed facts only: the status word and the count of its data rows.
        if not execution.isdecimal():
            raise RehearsalFailure("interrupted execution id rejected")
        value = self.fixture.psql(
            "n8n",
            "n8n",
            "SELECT coalesce((SELECT status FROM execution_entity WHERE "
            f"id={execution}),'absent')||'|'||(SELECT count(*) FROM execution_data "
            f'WHERE "executionId"={execution});',
            container="metadata-pg",
        ).stdout.strip()
        status, _, rows = value.partition("|")
        if not re.fullmatch(r"[a-z]{1,16}", status) or not rows.isdecimal():
            raise RehearsalFailure("metadata execution facts rejected")
        return status, int(rows)

    def recover_after_main_restart(self, workflow, run):
        f = self.fixture
        interrupted = self.execution_ids[-1]
        f.receipt["main_restart_execution_id"] = interrupted
        # Main is down, so the worker probes; it must run before the killed
        # worker's lock expires or the job could already be gone.
        f.start("worker")
        before = recovery.broker_job_count(
            self.broker_jobs([interrupted], "worker"), [interrupted]
        )
        probe_ms = int((time.monotonic() - self.killed_at) * 1000)
        for role in ("mailpit", "runner"):
            f.start(role)
        self.await_worker_and_capture()
        after = self.settle_job(interrupted, "worker")
        if not interrupted.isdecimal():
            raise RehearsalFailure("interrupted execution id rejected")
        status, data_before = self.metadata_execution(interrupted)
        started = time.monotonic()
        f.start("main")
        f.wait_until(
            lambda: legacy.node_status_probe(
                lambda *args: f.exec_result("main", *args),
                "http://127.0.0.1:5678/healthz",
            )[0],
            "restarted main readiness expired",
            300,
        )
        # The metadata DB is authoritative here: after a main restart the REST
        # read can answer 404 for the execution (native attempt 4).
        try:
            f.wait_until(
                lambda: (
                    self.metadata_execution(interrupted)[0] not in {"new", "running"}
                ),
                "restarted main did not settle the execution",
                60,
            )
        except RehearsalFailure as error:
            if str(error) != "restarted main did not settle the execution":
                raise
        settled, data_after = self.metadata_execution(interrupted)
        try:
            readable = self.api("execution", executionId=interrupted).get("status")
        except RehearsalFailure:
            readable = "unreadable"
        f.receipt["main_restart_metadata"] = {
            "execution_data_rows_before_main": data_before,
            "execution_data_rows_after_main": data_after,
            "rest_status": readable,
        }
        facts = {
            "jobs_before_restart": before,
            "kill_to_probe_ms": probe_ms,
            "jobs_after_worker_recovery": after,
            "status_while_main_down": status,
            "execution_status": settled,
        }
        f.receipt["main_restart_recovery_seconds"] = round(
            time.monotonic() - started, 3
        )
        f.receipt["main_restart_recovery"] = facts
        recovery.validate_main_restart_recovery(facts)
        f.receipt["main_restart_quarantine"] = self.quarantine_interrupted(
            workflow, run, b"p05-after-main-restart", "2026-11-30T00:00:00Z"
        )

    def retry_crashed(self, crashed, interrupted_runs):
        # n8n's own replay of each crashed execution. A fresh row is published
        # first so the retry must really run: it claims and delivers that row
        # while every interrupted row and its mail stay untouched.
        f = self.fixture
        baseline = self.outbox_snapshot()
        statuses, fresh = [], []
        for index, execution in enumerate(crashed):
            run = self.publish_input(
                b"p05-retry-" + str(index).encode(),
                f"2026-12-{1 + index:02d}T00:00:00Z",
            )
            fresh.append(run)
            # Closed node names only: where the retry starts from.
            crashed_trace = self.api("trace", executionId=execution)
            result = self.api("retry", executionId=execution)
            if result.get("retryOf") != execution:
                raise RehearsalFailure("retry was not bound to the crashed execution")
            statuses.append(str(result.get("status")))
            # Closed facts before any wait: the retry's own outcome and path.
            try:
                path = self.api("execution", executionId=str(result.get("id")))
                path = {
                    key: path.get(key)
                    for key in ("status", "mode", "acknowledged", "deliveryRedacted")
                }
                path["trace"] = self.api("trace", executionId=str(result.get("id")))
            except RehearsalFailure:
                path = "unreadable"
            f.receipt.setdefault("execution_retry_attempts", []).append(
                {
                    "status": statuses[-1],
                    "crashed_trace": crashed_trace,
                    "path": path,
                    "fresh_state": self.db_value(
                        f"SELECT state FROM ops_flow.outbox WHERE run_id='{run}';"
                    ),
                    "interrupted_resent": sum(
                        1 for old in interrupted_runs if self.capture(old)["matched"]
                    ),
                }
            )
            self.wait_state(run, "accepted_by_smtp")
        others = tuple(
            line
            for line in self.outbox_snapshot()
            if recovery.run_id_of(line) not in fresh
        )
        facts = {
            "retried": len(crashed),
            "statuses": statuses,
            "interrupted_rows_unchanged": others
            == tuple(
                line for line in baseline if recovery.run_id_of(line) not in fresh
            ),
            "interrupted_resent": sum(
                1 for run in interrupted_runs if self.capture(run)["matched"]
            ),
            "fresh_accepted_first_attempt": sum(
                1
                for run in fresh
                if self.db_value(
                    f"SELECT state||'|'||attempts FROM ops_flow.outbox WHERE run_id='{run}';"
                )
                == "accepted_by_smtp|1"
            ),
        }
        f.receipt["execution_retry"] = facts
        f.receipt["execution_retry"] = recovery.validate_execution_retry(facts)

    def ready_retry(self, run):
        self.fixture.wait_until(
            lambda: (
                self.db_value(
                    f"SELECT next_attempt_at<=clock_timestamp() FROM ops_flow.outbox WHERE run_id='{run}';"
                )
                == "t"
            ),
            "retry budget did not become ready",
            90,
        )

    def fence(self, workflow):
        self.fixture.stop("mailpit")
        row = next(
            item for item in self.api("workflows")["rows"] if item["id"] == workflow
        )
        if row.get("active") is True:
            self.api("deactivate", workflowId=workflow, versionId=row["versionId"])
        inactive = (
            next(
                item for item in self.api("workflows")["rows"] if item["id"] == workflow
            )["active"]
            is False
        )
        for role in ("runner", "worker"):
            self.fixture.stop(role)
        absent = all(
            (
                lambda state: (
                    state.get("Status") == "exited"
                    and state.get("Running") is False
                    and state.get("Pid") == 0
                )
            )(self.fixture._verify_owned(self.fixture.containers[role])["State"])
            for role in ("runner", "worker", "mailpit")
        )
        observed = self.broker_jobs(self.execution_ids)
        terminal = all(
            self.api("execution", executionId=execution).get("terminal") is True
            for execution in self.execution_ids
        )
        barrier = {
            "smtp_egress_held": absent,
            "workflow_inactive": inactive,
            "old_execution_ids": list(self.execution_ids),
            "old_processes_absent": absent,
            "old_sockets_absent": absent,
            "old_broker_jobs_absent": observed
            == {"scanned": True, "matching": 0, "ids": self.execution_ids},
            "old_executions_terminal": terminal,
            "owned_attempt": self.fixture.attempt,
        }
        self.fixture.receipt["recovery_barrier_facts"] = barrier
        self.fixture.receipt["recovery_barrier"] = recovery.validate_barrier(barrier)
        self.fixture.receipt["recovery_scope"] = "QUIESCED_ONLY"
        self.fixture.receipt["live_inflight_interruption"] = "TEST_RESIDUAL"

    def run_scenario(self):
        f = self.fixture
        self.phase("preflight")
        f.verify_prerequisites()
        self.secrets = f.create_secrets()
        f.prepare_smtp()
        f.create_networks()
        self.phase("postgres_provision")
        f.start_postgres("metadata-pg", self.secrets["metadata_pg"][1])
        self.start_dev_cluster()
        self.provision()
        self.phase("queue_tls_worker_startup")
        f.start_valkey(self.secrets["valkey_server"][1])
        f.start_mailpit()
        f.start_n8n(self.secrets)
        f.start_runner(self.secrets["runner"][1])
        self.phase("workflow_binding")
        workflow, _name = self.bind_and_import()
        self.api("profile", workflowId=workflow)
        self.update_smtp(1)
        first = self.publish_input(b"p05-first", "2026-11-20T00:00:00Z")
        self.phase("first_worker_starttls_delivery")
        self.execute(workflow, "success")
        self.wait_state(first, "accepted_by_smtp")
        self.assertEqual(
            (True, True, 1),
            (
                self.capture(first)["matched"],
                self.capture(first)["safe"],
                self.capture(first)["total"],
            ),
        )
        f.receipt["worker_queue_starttls_auth"] = "PASS"
        self.phase("same_id_credential_refresh")
        second = self.publish_input(b"p05-second", "2026-11-21T00:00:00Z")
        self.update_smtp(2)
        self.execute(workflow, "error")
        self.wait_state(second, "unknown")
        self.assertEqual(1, self.capture(first)["total"])
        f.receipt["wrong_new_material"] = "PASS"
        f.stop("mailpit")
        f.remove("mailpit")
        f.smtp_epoch = 2
        f.start_mailpit()
        refreshed = self.publish_input(b"p05-refreshed", "2026-11-22T00:00:00Z")
        self.execute(workflow, "success")
        self.wait_state(refreshed, "accepted_by_smtp")
        f.receipt["same_id_next_execution_refresh"] = "PASS"
        third = self.publish_input(b"p05-third", "2026-11-23T00:00:00Z")
        self.update_smtp(1)
        self.execute(workflow, "error")
        self.wait_state(third, "unknown")
        self.assertEqual(2, self.capture(refreshed)["total"])
        f.receipt["wrong_old_material"] = "PASS"
        self.update_smtp(2)
        corrected = self.publish_input(b"p05-corrected", "2026-11-24T00:00:00Z")
        self.execute(workflow, "success")
        self.wait_state(corrected, "accepted_by_smtp")
        # Interrupt before the barrier: restore must wait for n8n to settle
        # the orphaned job and execution, never ignore or delete them.
        self.phase("live_active_send_interruption")
        interrupted = self.interrupt_active_send(
            workflow, b"p05-interrupted", "2026-11-27T00:00:00Z"
        )
        self.recover_interrupted(workflow, interrupted)
        self.phase("main_and_worker_interruption")
        main_lost = self.interrupt_active_send(
            workflow, b"p05-main-restart", "2026-11-29T00:00:00Z", kill_main=True
        )
        crashed = [self.execution_ids[-1]]
        self.recover_after_main_restart(workflow, main_lost)
        self.phase("crashed_execution_retry")
        crashed.insert(0, f.receipt["interrupted_execution_id"])
        self.retry_crashed(crashed, [interrupted, main_lost])
        self.fence(workflow)
        before = self.outbox_snapshot()
        self.phase("owned_restore")
        self.restore_and_restart()
        self._session = None
        self.phase("restored_state_replay")
        f.receipt["restored_outbox_equivalence"] = recovery.validate_restored_state(
            before, self.outbox_snapshot()
        )
        baseline = self.outbox_snapshot()
        replays = [
            self.db_value(publish_sql(*item)[1], "opsflow_ingest")
            for item in self.inputs
        ]
        f.receipt["same_input_replay"] = recovery.validate_replay(
            replays,
            baseline,
            self.outbox_snapshot(),
            self.db_value(recovery.CLAIMABLE_SQL),
        )
        fourth = self.publish(
            "hy-home.k8s",
            hashlib.sha256(b"p05-restored").hexdigest(),
            # Newer than every pre-restore capture, or publish_manifest records
            # it as historical; SQL003 also allows one run per source per UTC
            # date, so every input in this scenario has its own date.
            "2026-12-31T00:00:00Z",
        )
        self.execute(workflow, "success")
        self.wait_state(fourth, "accepted_by_smtp")
        f.receipt["next_claim_after_restore"] = recovery.validate_next_claim(
            baseline, self.outbox_snapshot(), fourth
        )
        self.assertEqual(
            (True, 1), (self.capture(fourth)["matched"], self.capture(fourth)["total"])
        )
        # Generation 2 capture: no accepted or unknown pre-restore run resent.
        resent = [run for run in self.runs if self.capture(run)["matched"]]
        if resent:
            raise RehearsalFailure("a pre-restore notification was sent again")
        f.receipt["live_inflight_interruption"] = "PASS"
        f.receipt["same_encryption_key_restore"] = "PASS"
        f.receipt["native"] = "PASS"
        self.phase("complete")


def run_current_rehearsal():
    if os.environ.get("P05_OPSFLOW_NATIVE") != "1":
        raise RehearsalFailure("current native opt-in required")
    scenario = P05Scenario(
        "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
    )
    scenario.setUp()
    try:
        scenario.run_scenario()
    finally:
        scenario.finish()
