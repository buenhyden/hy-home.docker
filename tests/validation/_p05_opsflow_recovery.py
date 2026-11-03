"""Closed P05 recovery barrier facts; an SQL transition is not SMTP fencing."""

import re

from tests.validation._opsflow_native_fixture import RehearsalFailure


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
