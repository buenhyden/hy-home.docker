"""Closed P05 recovery barrier facts; an SQL transition is not SMTP fencing."""

import hashlib
import re
from collections import Counter

from tests.validation._opsflow_native_fixture import RehearsalFailure

# transport.ts POLICY.socketTimeout: past it the transport ends a held session
# itself, so a worker stop issued later would not interrupt an active send.
SOCKET_TIMEOUT_SECONDS = 5.0

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


def validate_next_claim(before, after, fresh):
    row = _outbox(after).get(fresh)
    if (
        tuple(line for line in after if fresh not in line) != tuple(before)
        or row is None
        or row[3] != "accepted_by_smtp"
        or row[4] != "1"
    ):
        raise RehearsalFailure("next claim touched restored notification rows")
    return {"old_rows_unchanged": True, "fresh_accepted_first_attempt": True}


_HELD = (
    "data_started",
    "body_held",
    "session_open_at_stop",
    "client_closed_after_stop",
)


def validate_interruption(facts):
    latency = facts.get("detect_to_stop_seconds") if isinstance(facts, dict) else None
    if (
        not isinstance(facts, dict)
        or set(facts)
        != {*_HELD, "detect_to_stop_seconds", "state_after_stop", "execution_status"}
        or any(facts[key] is not True for key in _HELD)
        or type(latency) not in {int, float}
        or not 0 <= latency < SOCKET_TIMEOUT_SECONDS
        # The conservative transport rule: a started send is never success
        # or retry; it is uncertain (unknown) or still leased (sending).
        or facts["state_after_stop"] not in {"unknown", "sending"}
        or facts["execution_status"] == "success"
    ):
        raise RehearsalFailure("active-send interruption outcome rejected")
    return dict(facts)


# Fixture-only STARTTLS endpoint under the capture alias with the owned
# synthetic certificate. It answers up to DATA, then never replies, so the
# client's session stays mid-DATA. It stores nothing and prints closed facts.
HOLD_JS = r"""const net=require('net'),tls=require('tls'),fs=require('fs');
const context=tls.createSecureContext({cert:fs.readFileSync('/run/secrets/server.pem'),key:fs.readFileSync('/run/secrets/server.key')});
const fact=name=>process.stdout.write('P05_HOLD '+name+'\n');
net.createServer(raw=>{
 let socket=raw,secure=false,data=false,pending='';
 const reply=text=>socket.write(text+'\r\n');
 const command=line=>{const verb=line.slice(0,4).toUpperCase();
  if(verb==='EHLO')reply(secure?'250-mailpit\r\n250 AUTH PLAIN':'250-mailpit\r\n250 STARTTLS');
  else if(verb==='STAR'&&!secure){reply('220 ready');raw.removeListener('data',feed);secure=true;pending='';
   socket=new tls.TLSSocket(raw,{isServer:true,secureContext:context});socket.on('data',feed);socket.on('error',()=>{});}
  else if(verb==='AUTH'&&secure)reply('235 synthetic');
  else if((verb==='MAIL'||verb==='RCPT')&&secure)reply('250 synthetic');
  else if(verb==='DATA'&&secure){data=true;reply('354 synthetic');fact('DATA_STARTED');}
  else reply('503 synthetic');};
 function feed(chunk){if(data){fact('BODY_HELD');return;}
  pending+=chunk.toString('latin1');let at;
  while(!data&&(at=pending.indexOf('\r\n'))>=0){const line=pending.slice(0,at);pending=pending.slice(at+2);command(line);}
  if(data&&pending){pending='';fact('BODY_HELD');}}
 raw.on('data',feed);raw.on('error',()=>{});raw.on('close',()=>fact('CLIENT_CLOSED'));
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


QUEUE_PROBE = r"""const fs=require('fs');
const data=JSON.parse(fs.readFileSync(0,'utf8'));
const Bull=require('/usr/local/lib/node_modules/n8n/node_modules/bull');
const password=fs.readFileSync('/run/secrets/n8n_valkey_password','utf8').replace(/\n$/,'');
(async()=>{
const q=new Bull('jobs',{prefix:'opsflow_native',redis:{host:'n8n-valkey',port:6379,password}});
try {
 const jobs=await q.getJobs(['waiting','active','delayed','paused','completed','failed']);
 const found=jobs.filter(j=>data.ids.includes(String(j.data?.executionId)));
 process.stdout.write(JSON.stringify({scanned:true,matching:found.length,ids:data.ids}));
} finally {await q.close();}
})().catch(()=>{process.stderr.write('owned queue inspection failed');process.exitCode=1});
"""
