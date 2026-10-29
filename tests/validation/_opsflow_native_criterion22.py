"""SPEC-0204 criterion 22 native scenario contract, free of Docker and secrets.

Holds the receipt fields, the scenario order, the SQL and shell scripts the
opt-in n8n native rehearsal runs, and the parsers for their closed outputs, so
Docker-free guards can pin them. Secrets never appear here: a script reads a
password or key from stdin and prints only booleans, counts and safe IDs.
"""

from __future__ import annotations

import json
import re

# Receipt fields, flat like the existing ones (`native`, `queue_runner`,
# `restore`). Each starts `NOT_RUN`, becomes `PASS` when its scenario's
# assertions hold, and becomes `FAIL` if they raise.
GENERATION_1_STEPS = (
    "scheduled_execution",
    "concurrent_claims",
    "retry_dead_letter",
    "empty_queue",
    "credential_rotation",
)
RESTORE_STEPS = ("paired_restore_decrypt", "wrong_key_fail_closed")
RECEIPT_FIELDS = GENERATION_1_STEPS + RESTORE_STEPS

# ops_flow.outbox CHECK(attempts BETWEEN 0 AND 5) and claim_notification().
MAX_ATTEMPTS = 5
# One scheduled tick is at most 60 s away; the rest covers activation and a
# worker that is busy with the previous minute.
SCHEDULE_WAIT_SECONDS = 150
# More than one full minute with the trigger deactivated.
DEACTIVATED_HOLD_SECONDS = 70
RACE_HOLD_SECONDS = 3

UUID_NIL = "00000000-0000-0000-0000-000000000000"
EXECUTION_STATUSES_OPEN = {"new", "running", "waiting", "unknown"}


def initial_receipt() -> dict[str, str]:
    return {field: "NOT_RUN" for field in RECEIPT_FIELDS}


# --- Closed diagnostics when a queued execution never turns terminal: the last
# status seen and whether known n8n log lines exist. No log text is kept.
EXECUTION_STATUSES_SEEN = frozenset(
    {"none", "new", "running", "waiting", "success", "error", "canceled", "crashed"}
)
TIMEOUT_LOG_MARKERS = {
    "main": {"enqueued": "Enqueued execution"},
    "worker": {
        "started": "Worker started execution",
        "finished": "Worker finished execution",
        "unknown_node": "Unrecognized node type",
        "runner_timeout": "Task request timed out",
        "runner_registered": 'Registered runner "',
    },
}


def execution_timeout_facts(last_status: str, logs_contain) -> dict[str, object]:
    facts: dict[str, object] = {
        "last_status": last_status
        if last_status in EXECUTION_STATUSES_SEEN
        else "other"
    }
    for role, markers in TIMEOUT_LOG_MARKERS.items():
        try:
            facts[f"{role}_log"] = {
                key: bool(logs_contain(role, text)) for key, text in markers.items()
            }
        except Exception:  # diagnostics must not mask the timeout itself
            facts[f"{role}_log"] = "unavailable"
    return facts


def backoff_seconds(attempts: int) -> int:
    """retry_not_sent_notification(): least(900, 30 * 2^attempts) seconds."""
    return min(900, 30 * 2**attempts)


# --- SQL, run through psql over the container socket (see NativeFixture.psql)

CLAIMABLE_SQL = (
    "SELECT count(*) FROM ops_flow.outbox WHERE state IN ('pending','retry') "
    "AND attempts<5;"
)
CLAIM_PROBE_SQL = "SELECT coalesce(max(id),0) FROM ops_flow.claim_notification();"

# One notifier session: claim (token stays inside psql), then reject a wrong
# token, ack once, and refuse a replay. A loser claims nothing (`cid`=0).
# The transaction is held open so concurrent claimers overlap deterministically
# (FOR UPDATE SKIP LOCKED skips the row the winner has locked).
RACE_SQL = f"""BEGIN;
SELECT coalesce(max(id),0) AS cid, coalesce(max(lease_token::text),'') AS ctok FROM ops_flow.claim_notification() \\gset
SELECT pg_sleep({RACE_HOLD_SECONDS});
COMMIT;
SELECT 'claim|'||:cid;
SELECT 'stale|'||ops_flow.ack_notification(:cid,'{UUID_NIL}'::uuid);
SELECT 'ack|'||ops_flow.ack_notification(:cid,nullif(:'ctok','')::uuid);
SELECT 'again|'||ops_flow.ack_notification(:cid,nullif(:'ctok','')::uuid);
"""

# stdin: the session SQL. argv: job count. All jobs sleep to one barrier first.
RACE_SCRIPT = r"""set -eu
SQL=$(cat)
T=$(psql -X -qAt -U p04_audit -d opsflow_dev -c "SELECT clock_timestamp()+interval '4 seconds'")
i=0
while [ "$i" -lt "$1" ]; do
 i=$((i+1))
 (out=$(printf '%s\n' "SELECT pg_sleep(greatest(0,extract(epoch from '$T'::timestamptz-clock_timestamp())));" "$SQL" | psql -X -qAt -v ON_ERROR_STOP=1 -U opsflow_notifier -d opsflow_dev | tr '\n' ','); printf 'job%s:%s\n' "$i" "$out") &
done
wait
"""

# One claim then retry_not_sent for the same lease, token inside psql.
RETRY_CYCLE_SQL = """SELECT coalesce(max(id),0) AS cid, coalesce(max(lease_token::text),'') AS ctok FROM ops_flow.claim_notification() \\gset
SELECT 'claimed|'||:cid;
SELECT 'retried|'||ops_flow.retry_not_sent_notification(:cid,nullif(:'ctok','')::uuid);
"""


def outbox_row_sql(outbox_id: str, columns: str) -> str:
    if not outbox_id.isdecimal():
        raise ValueError("outbox id must be decimal")
    return f"SELECT {columns} FROM ops_flow.outbox WHERE id={outbox_id};"


def retry_expected(attempt: int) -> str:
    if not 1 <= attempt <= MAX_ATTEMPTS:
        raise ValueError("attempt outside the configured range")
    if attempt == MAX_ATTEMPTS:
        return f"dead|{attempt}|smtp_not_started|n/a"
    return f"retry|{attempt}|smtp_not_started|true"


def retry_row_sql(outbox_id: str, attempt: int) -> str:
    """Row shape matching retry_expected(); the backoff window is exact."""
    if not 1 <= attempt <= MAX_ATTEMPTS:
        raise ValueError("attempt outside the configured range")
    head = "state||'|'||attempts||'|'||coalesce(last_error_code,'')||'|'||"
    if attempt == MAX_ATTEMPTS:
        return outbox_row_sql(outbox_id, head + "'n/a'")
    delay = backoff_seconds(attempt)
    return outbox_row_sql(
        outbox_id,
        head
        + f"(next_attempt_at BETWEEN clock_timestamp()+interval '{delay - 30} seconds' "
        f"AND clock_timestamp()+interval '{delay + 1} seconds')::text",
    )


def fast_forward_sql(outbox_id: str) -> str:
    # Fixture-only time travel as the superuser; the notifier cannot do this.
    if not outbox_id.isdecimal():
        raise ValueError("outbox id must be decimal")
    return (
        "UPDATE ops_flow.outbox SET next_attempt_at=clock_timestamp() "
        f"WHERE id={outbox_id} AND state='retry' RETURNING id;"
    )


def exhaust_sql(outbox_id: str) -> str:
    if not outbox_id.isdecimal():
        raise ValueError("outbox id must be decimal")
    return (
        f"UPDATE ops_flow.outbox SET attempts={MAX_ATTEMPTS},state='retry' "
        f"WHERE id={outbox_id} AND state='pending' RETURNING id;"
    )


def rotate_role_sql(role: str, password: str) -> str:
    if not re.fullmatch(r"opsflow_[a-z]+", role) or not re.fullmatch(
        r"[A-Za-z0-9_-]{32,128}", password
    ):
        raise ValueError("rotation input shape rejected")
    return f"ALTER ROLE {role} WITH PASSWORD '{password}';"


def terminate_role_sql(role: str) -> str:
    if not re.fullmatch(r"opsflow_[a-z]+", role):
        raise ValueError("rotation role shape rejected")
    return (
        # The 5 s timeout waits for each backend to exit (PostgreSQL 14+).
        "SELECT count(pg_terminate_backend(pid, 5000)) FROM pg_stat_activity "
        f"WHERE datname='opsflow_dev' AND usename='{role}';"
    )


def role_sessions_sql(role: str) -> str:
    if not re.fullmatch(r"opsflow_[a-z]+", role):
        raise ValueError("rotation role shape rejected")
    return (
        "SELECT count(*) FROM pg_stat_activity "
        f"WHERE datname='opsflow_dev' AND usename='{role}';"
    )


# --- Password check over TCP. The unix socket is `trust`, so a password is
# only enforced on a non-loopback host path: the container's own alias.
# stdin: the password. argv: role.
PASSWORD_PROBE_SCRIPT = r"""set -eu
IFS= read -r PGPASSWORD || PGPASSWORD=
export PGPASSWORD
exec psql -X -qAt -v VERBOSITY=verbose -h dev-pg -U "$1" -d opsflow_dev -c 'SELECT 1'
"""

# --- Credential decrypt check with the n8n CLI inside the main container.
# stdin: an optional replacement N8N_ENCRYPTION_KEY (empty line = the mounted
# key). argv: credential id, data field, expected SHA-256 of that field.
# Output: closed booleans only; the plaintext never leaves the container.
CREDENTIAL_PROBE_SCRIPT = r"""set -eu
umask 077
IFS= read -r key || key=
out=${TMPDIR:-/tmp}/credential-probe.json
rm -f "$out"
trap 'rm -f "$out"' EXIT
if [ -n "$key" ]; then unset N8N_ENCRYPTION_KEY_FILE; N8N_ENCRYPTION_KEY=$key; export N8N_ENCRYPTION_KEY; fi
if n8n export:credentials --id="$1" --decrypted --output="$out" >/dev/null 2>&1; then exported=true; else exported=false; fi
node -e '
const fs=require("fs"),crypto=require("crypto");
const [file,field,expected,exported]=process.argv.slice(1);
let present=false,match=false;
if(exported==="true"){try{const j=JSON.parse(fs.readFileSync(file,"utf8"));const c=Array.isArray(j)?j[0]:j;const v=c&&c.data&&c.data[field];present=typeof v==="string";match=present&&crypto.createHash("sha256").update(v).digest("hex")===expected;}catch(e){}}
process.stdout.write(JSON.stringify({exported:exported==="true",present,match}));
' "$out" "$2" "$3" "$exported"
"""


# --- Parsers for the closed outputs above.

_JOB = re.compile(r"job(\d+):(.*)\Z")


def parse_race(output: str, jobs: int) -> list[dict[str, object]]:
    """Parse RACE_SCRIPT output into one closed record per job."""
    rows: dict[int, dict[str, object]] = {}
    for line in output.splitlines():
        match = _JOB.fullmatch(line.strip())
        if match is None:
            raise ValueError("race output line rejected")
        index = int(match[1])
        fields = [part for part in match[2].split(",") if part]
        if index in rows or len(fields) != 4:
            raise ValueError("race job shape rejected")
        values = {}
        for field, label in zip(
            fields, ("claim", "stale", "ack", "again"), strict=True
        ):
            key, _, value = field.partition("|")
            if key != label:
                raise ValueError("race job field order rejected")
            values[key] = value
        if not values["claim"].isdecimal() or any(
            # `'text'||boolean` renders through boolean::text: true/false.
            values[key] not in {"true", "false"}
            for key in ("stale", "ack", "again")
        ):
            raise ValueError("race job value rejected")
        rows[index] = {
            "claim": int(values["claim"]),
            **{key: values[key] == "true" for key in ("stale", "ack", "again")},
        }
    if sorted(rows) != list(range(1, jobs + 1)):
        raise ValueError("race job set rejected")
    return [rows[index] for index in sorted(rows)]


def race_winners(rows: list[dict[str, object]], expected_ids: set[int]) -> None:
    """Exactly one winner per row; losers claim nothing; tokens are exclusive."""
    claimed = [row["claim"] for row in rows if row["claim"]]
    if sorted(claimed) != sorted(expected_ids) or len(set(claimed)) != len(claimed):
        raise ValueError("a row was claimed zero or several times")
    for row in rows:
        won = bool(row["claim"])
        if (row["stale"], row["ack"], row["again"]) != (False, won, False):
            raise ValueError("lease token exclusivity rejected")


def parse_probe(output: str) -> dict[str, bool]:
    value = json.loads(output)
    if set(value) != {"exported", "present", "match"} or not all(
        isinstance(item, bool) for item in value.values()
    ):
        raise ValueError("credential probe summary rejected")
    return value
