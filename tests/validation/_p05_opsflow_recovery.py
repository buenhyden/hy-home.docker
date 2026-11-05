"""Closed P05 recovery barrier facts; an SQL transition is not SMTP fencing."""

import hashlib
import re
from collections import Counter

from tests.validation._opsflow_native_fixture import RehearsalFailure

# transport.ts POLICY.socketTimeout: past it the transport ends a held session
# itself, so a worker stop issued later would not interrupt an active send.
SOCKET_TIMEOUT_SECONDS = 5.0

# n8n 2.43.6 queue defaults (@n8n/config scaling-mode.config.js): a killed
# worker's job lock expires after QUEUE_WORKER_LOCK_DURATION, and a running
# worker checks for stalled jobs every QUEUE_WORKER_STALLED_INTERVAL. Bull
# needs a marking pass and a failing pass, so a restarted worker settles the
# orphan within lock + 2 intervals; the bound adds one more interval of margin.
N8N_LOCK_DURATION_SECONDS = 60
N8N_STALLED_INTERVAL_SECONDS = 30
STALL_RECOVERY_SECONDS = N8N_LOCK_DURATION_SECONDS + 3 * N8N_STALLED_INTERVAL_SECONDS

# Every outbox, attempt-reconciliation, recovery-audit and run row, sorted.
# Lease tokens are capabilities: only their presence is compared.
SNAPSHOT_SQL = """SELECT line FROM (
 SELECT 'outbox|'||id||'|'||run_id||'|'||state||'|'||attempts||'|'||attempt_limit||'|'||coalesce(last_error_code,'')||'|'||coalesce(accepted_at::text,'')||'|'||(lease_token IS NULL)::text||'|'||coalesce(lease_until::text,'')||'|'||next_attempt_at::text||'|'||created_at::text AS line FROM ops_flow.outbox
 UNION ALL SELECT 'reconciliation|'||outbox_id||'|'||attempt||'|'||result||'|'||evidence_sha256||'|'||reconciled_at::text FROM ops_flow.notification_reconciliations
 UNION ALL SELECT 'audit|'||request_id||'|'||outbox_id||'|'||attempt||'|'||action||'|'||evidence_sha256||'|'||recorded_at::text FROM ops_flow.notification_recovery_audit
 UNION ALL SELECT 'run|'||run_id||'|'||source||'|'||status||'|'||captured_at::text FROM ops_flow.runs
) s ORDER BY line;"""
# claim_notification() candidates under the v5 per-row attempt_limit.
CLAIMABLE_SQL = (
    "SELECT count(*) FROM ops_flow.outbox WHERE state IN ('pending','retry') "
    "AND attempts<attempt_limit;"
)
_KINDS = {"outbox", "reconciliation", "audit", "run"}


def snapshot_lines(text):
    lines = tuple(line for line in str(text).splitlines() if line)
    if (
        not lines
        or len(lines) > 512
        or any(line.split("|", 1)[0] not in _KINDS for line in lines)
        or not any(line.startswith("outbox|") for line in lines)
    ):
        raise RehearsalFailure("outbox snapshot rejected")
    return lines


def _outbox(lines):
    rows = (line.split("|") for line in lines if line.startswith("outbox|"))
    return {fields[2]: fields for fields in rows if len(fields) > 4}


def validate_restored_state(before, after):
    if tuple(before) != tuple(after):
        raise RehearsalFailure("restored outbox, attempt or audit state differs")
    states = Counter(fields[3] for fields in _outbox(after).values())
    return {
        "rows": len(after),
        "outbox": len(_outbox(after)),
        "states": dict(sorted(states.items())),
        "sha256": hashlib.sha256("\n".join(after).encode()).hexdigest(),
    }


def validate_replay(results, before, after, claimable):
    # publish_manifest returns 'replayed' for an identical run without a new
    # outbox row; claim_notification never selects accepted or unknown rows.
    if (
        not results
        or any(result != "replayed" for result in results)
        or tuple(after) != tuple(before)
        or claimable != "0"
    ):
        raise RehearsalFailure("same-input replay changed notification state")
    return {"replayed": len(results), "claimable": 0}


def run_id_of(line):
    fields = line.split("|")
    if fields[0] == "outbox" and len(fields) > 2:
        return fields[2]
    if fields[0] == "run" and len(fields) > 1:
        return fields[1]
    return None


def validate_next_claim(before, after, fresh):
    row = _outbox(after).get(fresh)
    if (
        tuple(line for line in after if run_id_of(line) != fresh) != tuple(before)
        or row is None
        or row[3] != "accepted_by_smtp"
        or row[4] != "1"
    ):
        raise RehearsalFailure("next claim touched restored notification rows")
    return {"old_rows_unchanged": True, "fresh_accepted_first_attempt": True}


_HOLD_LINE = re.compile(
    r"P05_HOLD (?:(DATA_STARTED)|BODY_HELD at=([0-9]{1,16})"
    r"|CLIENT_CLOSED (?:after_body_ms=([0-9]{1,9})|before_body))"
)


def parse_hold(text):
    """Closed facts from the hold endpoint's own log lines only."""
    facts = {
        "data_started": False,
        "body_held_at_ms": None,
        "closed_after_body_ms": None,
    }
    for line in str(text).splitlines():
        if not line.startswith("P05_HOLD ") or line in {
            "P05_HOLD LISTENING",
        }:
            continue
        match = _HOLD_LINE.fullmatch(line)
        if match is None:
            raise RehearsalFailure("hold log line rejected")
        started, held, closed = match.groups()
        if (held and facts["body_held_at_ms"] is not None) or (
            closed and facts["closed_after_body_ms"] is not None
        ):
            raise RehearsalFailure("hold saw more than one session")
        if started:
            facts["data_started"] = True
        if held:
            facts["body_held_at_ms"] = int(held)
        if closed:
            facts["closed_after_body_ms"] = int(closed)
    return facts


def validate_interruption(facts):
    limit = int(SOCKET_TIMEOUT_SECONDS * 1000)
    fields = {
        "data_started",
        "session_open_at_kill",
        "body_to_kill_ms",
        "body_to_close_ms",
        "state_after_kill",
        "execution_status",
    }
    if (
        not isinstance(facts, dict)
        or set(facts) != fields
        or facts["data_started"] is not True
        or facts["session_open_at_kill"] is not True
        or any(
            type(facts[key]) is not int or not 0 <= facts[key] < limit
            for key in ("body_to_kill_ms", "body_to_close_ms")
        )
        # A SIGKILLed worker records nothing: the lease stays sending. An
        # unknown row here would mean the transport's own timeout ended the
        # session, which is not an interruption; success/retry never apply.
        or facts["state_after_kill"] != "sending"
        or facts["execution_status"] == "success"
    ):
        raise RehearsalFailure("active-send interruption outcome rejected")
    return dict(facts)


def broker_job_count(observed, ids):
    # Accept only a complete probe of exactly the requested ids, as the barrier
    # does; a partial scan or another id set is never read as a count.
    count = observed.get("matching") if isinstance(observed, dict) else None
    if type(count) is not int or observed != {
        "scanned": True,
        "matching": count,
        "ids": list(ids),
    }:
        raise RehearsalFailure("exact old broker job probe unavailable")
    return count


def validate_queue_recovery(facts):
    # n8n's own route, read from the 2.43.6 image: ScalingService forces Bull
    # maxStalledCount 0, so the restarted worker's stall check fails the
    # orphaned job ("job stalled more than maxStalledCount") and, with
    # keepLastFailed 0, deletes it. Main's WorkflowRunner then marks that
    # execution crashed. The job must have survived the kill (1) or nothing
    # was recovered; no job may be deleted by the rehearsal itself.
    if facts != {
        "jobs_before_restart": 1,
        "jobs_after_recovery": 0,
        "execution_status": "crashed",
    } or any(
        type(facts[key]) is not int
        for key in ("jobs_before_restart", "jobs_after_recovery")
    ):
        raise RehearsalFailure("interrupted queue job was not recovered by n8n")
    return dict(facts)


def validate_main_restart_recovery(facts):
    # Main killed too: the restarted worker still deletes the stalled job, but
    # no WorkflowRunner awaits it, so the execution stays running. The leader
    # main's ScalingService.setupQueue runs scheduleQueueRecovery(0) at start:
    # an in-progress execution with no active or waiting job becomes crashed.
    # The probe must precede lock expiry, or the job may already be gone.
    probe_ms = facts.get("kill_to_probe_ms") if isinstance(facts, dict) else None
    if (
        facts
        != {
            "jobs_before_restart": 1,
            "kill_to_probe_ms": probe_ms,
            "jobs_after_worker_recovery": 0,
            "status_while_main_down": "running",
            "execution_status": "crashed",
        }
        or type(probe_ms) is not int
        or not 0 <= probe_ms < N8N_LOCK_DURATION_SECONDS * 1000
        or type(facts["jobs_before_restart"]) is not int
        or type(facts["jobs_after_worker_recovery"]) is not int
    ):
        raise RehearsalFailure("main-restart queue recovery rejected")
    return dict(facts)


def validate_execution_retry(facts):
    # n8n 2.43.6 records a worker-killed execution with an empty start stack
    # and only the stall error; ExecutionService.retry copies that data, so
    # the retry runs no node, claims nothing and ends error (native attempt 8).
    # Replay is a new execution: it claims only claimable rows, while each
    # interrupted row stays unknown for reconciliation.
    # A run that ends before n8n attaches its result promise makes retry
    # throw "The retry did not start" (HTTP 500, native attempt 11): the same
    # no-op, recorded as not_started.
    count = facts.get("retried") if isinstance(facts, dict) else None
    statuses = facts.get("statuses") if isinstance(facts, dict) else None
    if (
        type(count) is not int
        or count < 1
        or not isinstance(statuses, list)
        or len(statuses) != count
        or any(status not in {"error", "not_started"} for status in statuses)
        or facts
        != {
            "retried": count,
            "statuses": statuses,
            "start_stacks_empty": True,
            "claimed_by_retry": 0,
            "interrupted_resent": 0,
            "rows_unchanged_by_retry": True,
            "retry_executions_terminal": True,
            "fresh_execution_delivered": True,
        }
        or type(facts["claimed_by_retry"]) is not int
        or type(facts["interrupted_resent"]) is not int
        or any(
            type(facts[key]) is not bool
            for key in (
                "start_stacks_empty",
                "rows_unchanged_by_retry",
                "retry_executions_terminal",
                "fresh_execution_delivered",
            )
        )
    ):
        raise RehearsalFailure("n8n execution retry outcome rejected")
    return dict(facts)


# Fixture-only STARTTLS endpoint under the capture alias with the owned
# synthetic certificate. It answers up to DATA, then never replies, so the
# client's session stays mid-DATA. It stores nothing and prints closed facts.
HOLD_JS = r"""const net=require('net'),tls=require('tls'),fs=require('fs');
const context=tls.createSecureContext({cert:fs.readFileSync('/run/secrets/server.pem'),key:fs.readFileSync('/run/secrets/server.key')});
const fact=name=>process.stdout.write('P05_HOLD '+name+'\n');
net.createServer(raw=>{
 let socket=raw,secure=false,data=false,pending='',bodyAt=0;
 const reply=text=>socket.write(text+'\r\n');
 const command=line=>{const verb=line.slice(0,4).toUpperCase();
  if(verb==='EHLO')reply(secure?'250-mailpit\r\n250 AUTH PLAIN':'250-mailpit\r\n250 STARTTLS');
  else if(verb==='STAR'&&!secure){reply('220 ready');raw.removeListener('data',feed);secure=true;pending='';
   socket=new tls.TLSSocket(raw,{isServer:true,secureContext:context});socket.on('data',feed);socket.on('error',()=>{});}
  else if(verb==='AUTH'&&secure)reply('235 synthetic');
  else if((verb==='MAIL'||verb==='RCPT')&&secure)reply('250 synthetic');
  else if(verb==='DATA'&&secure){data=true;reply('354 synthetic');fact('DATA_STARTED');}
  else reply('503 synthetic');};
 const body=()=>{if(!bodyAt){bodyAt=Date.now();fact('BODY_HELD at='+bodyAt);}};
 function feed(chunk){if(data){body();return;}
  pending+=chunk.toString('latin1');let at;
  while(!data&&(at=pending.indexOf('\r\n'))>=0){const line=pending.slice(0,at);pending=pending.slice(at+2);command(line);}
  if(data&&pending){pending='';body();}}
 raw.on('data',feed);raw.on('error',()=>{});raw.on('close',()=>fact(bodyAt?'CLIENT_CLOSED after_body_ms='+(Date.now()-bodyAt):'CLIENT_CLOSED before_body'));
 reply('220 mailpit ESMTP synthetic hold');
}).listen(1025,'0.0.0.0',()=>fact('LISTENING'));
"""


def validate_barrier(value):
    booleans = {
        "smtp_egress_held",
        "workflow_inactive",
        "old_processes_absent",
        "old_sockets_absent",
        "old_broker_jobs_absent",
        "old_executions_terminal",
    }
    if not isinstance(value, dict) or set(value) != booleans | {
        "old_execution_ids",
        "owned_attempt",
    }:
        raise RehearsalFailure("recovery barrier schema rejected")
    ids = value["old_execution_ids"]
    if (
        any(value[key] is not True for key in booleans)
        or not isinstance(ids, list)
        or not ids
        or len(ids) > 32
        or any(
            not isinstance(item, str) or re.fullmatch(r"[1-9][0-9]{0,18}", item) is None
            for item in ids
        )
        or len(set(ids)) != len(ids)
        or not isinstance(value["owned_attempt"], str)
        or re.fullmatch(r"opsflow-native-[0-9a-f]{24}", value["owned_attempt"]) is None
    ):
        raise RehearsalFailure("recovery barrier incomplete")
    return {**value, "old_execution_ids": list(ids)}


# Bull getJobs lists ids, then reads each hash: a job n8n removes in between
# is null. A null is an absent job, never a match, and must not fail the probe.
QUEUE_PROBE = r"""const fs=require('fs');
const data=JSON.parse(fs.readFileSync(0,'utf8'));
const Bull=require('/usr/local/lib/node_modules/n8n/node_modules/bull');
const password=fs.readFileSync('/run/secrets/n8n_valkey_password','utf8').replace(/\n$/,'');
(async()=>{
const q=new Bull('jobs',{prefix:'opsflow_native',redis:{host:'n8n-valkey',port:6379,password}});
try {
 const jobs=await q.getJobs(['waiting','active','delayed','paused','completed','failed']);
 const found=jobs.filter(j=>j!==null&&data.ids.includes(String(j.data?.executionId)));
 process.stdout.write(JSON.stringify({scanned:true,matching:found.length,ids:data.ids}));
} finally {await q.close();}
})().catch(()=>{process.stderr.write('owned queue inspection failed');process.exitCode=1});
"""
