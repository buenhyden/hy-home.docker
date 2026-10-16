"""Build an inactive draft consumer; never connect, import or provision anything."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

CLAIM_KEYS = frozenset(
    {"id", "run_id", "source", "row_count", "lease_token", "lease_until"}
)
SOURCES = frozenset({"hy-home.docker", "hy-home.k8s", "Project-Template", "blog-data"})
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
CLAIM_VALIDATOR_JS = r"""(rows) => {
  if (!Array.isArray(rows) || rows.length !== 1) return false;
  const r = rows[0];
  if (!r || typeof r !== 'object' || Array.isArray(r)) return false;
  const keys = ['id','run_id','source','row_count','lease_token','lease_until'];
  if (Object.keys(r).length !== keys.length || !keys.every(k => Object.hasOwn(r,k))) return false;
  const full = (pattern, value) => typeof value === 'string' && new RegExp('^(?:'+pattern+')(?![\\s\\S])').test(value);
  const id = typeof r.id === 'number' ? Number.isSafeInteger(r.id) && r.id > 0 :
    full('[1-9][0-9]{0,18}',r.id) && BigInt(r.id) <= 9223372036854775807n;
  return id && full('[0-9a-f]{64}',r.run_id) &&
    ['hy-home.docker','hy-home.k8s','Project-Template','blog-data'].includes(r.source) &&
    Number.isSafeInteger(r.row_count) && r.row_count >= 1 && r.row_count <= 5000 &&
    full('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',r.lease_token) &&
    full('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3}Z',r.lease_until) &&
    Number.isFinite(Date.parse(r.lease_until)) && new Date(r.lease_until).toISOString() === r.lease_until;
}"""


def _lease_timestamp(value):
    if (
        not isinstance(value, str)
        or re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", value
        )
        is None
    ):
        return False
    try:
        return (
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
            == value
        )
    except ValueError:
        return False


def validate_claim(rows):
    """Validate the supplied-reference draft; return a fresh, closed claim."""
    if not isinstance(rows, list) or len(rows) != 1:
        raise ValueError("invalid_claim")
    row = rows[0]
    if not isinstance(row, dict) or set(row) != CLAIM_KEYS:
        raise ValueError("invalid_claim")
    value = row["id"]
    valid_id = (type(value) is int and 0 < value <= 2**53 - 1) or (
        isinstance(value, str)
        and re.fullmatch(r"[1-9][0-9]{0,18}", value) is not None
        and int(value) <= 9223372036854775807
    )
    if not (
        valid_id
        and isinstance(row["run_id"], str)
        and re.fullmatch(r"[0-9a-f]{64}", row["run_id"]) is not None
        and isinstance(row["source"], str)
        and row["source"] in SOURCES
        and type(row["row_count"]) is int
        and 1 <= row["row_count"] <= 5000
        and isinstance(row["lease_token"], str)
        and re.fullmatch(UUID, row["lease_token"]) is not None
        and _lease_timestamp(row["lease_until"])
    ):
        raise ValueError("invalid_claim")
    return dict(row)


def evaluate_outcome(rows, receipt, ack, retry, quarantine=None):
    """Synthetic transition oracle; this never performs claim/send/ack/retry."""
    if rows == []:
        return "empty"
    try:
        row = validate_claim(rows)
    except ValueError:
        return "invalid_claim"
    if (
        not isinstance(receipt, dict)
        or set(receipt) != {"run_id", "state"}
        or receipt["run_id"] != row["run_id"]
    ):
        return "delivery_uncertain"
    if receipt["state"] == "accepted_by_smtp":
        return (
            "acknowledged"
            if ack is True
            else ("quarantined" if quarantine is True else "quarantine_uncertain")
        )
    if receipt["state"] == "cancelled":
        return (
            "retry_recorded_not_sent"
            if retry is True
            else ("quarantined" if quarantine is True else "quarantine_uncertain")
        )
    if receipt["state"] == "uncertain":
        return "quarantined" if quarantine is True else "quarantine_uncertain"
    return "delivery_uncertain"


def node(name, kind, version, parameters, *, position=(0, 0), **extras):
    return {
        "id": name.lower().replace(" ", "-"),
        "name": name,
        "type": kind,
        "typeVersion": version,
        "position": list(position),
        "parameters": parameters,
        **extras,
    }


def boolean_node(name, expression, position):
    return node(
        name,
        "n8n-nodes-base.if",
        2.2,
        {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 2,
                },
                "conditions": [
                    {
                        "id": name.lower().replace(" ", "-"),
                        "leftValue": expression,
                        "rightValue": "",
                        "operator": {
                            "type": "boolean",
                            "operation": "true",
                            "singleValue": True,
                        },
                    }
                ],
                "combinator": "and",
            },
            "options": {},
        },
        position=position,
    )


def _entry_nodes(pg, smtp):
    return [
        node("Manual", "n8n-nodes-base.manualTrigger", 1, {}, position=(0, -80)),
        node(
            "Every Minute",
            "n8n-nodes-base.scheduleTrigger",
            1.2,
            {
                "rule": {"interval": [{"field": "minutes", "minutesInterval": 1}]},
            },
            position=(0, 100),
        ),
        node(
            "Claim",
            "n8n-nodes-base.postgres",
            2.6,
            {
                "operation": "executeQuery",
                "query": "SELECT id,run_id,source,row_count,lease_token, "
                "to_char(lease_until AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.MS\"Z\"') AS lease_until "
                "FROM ops_flow.claim_notification();",
                "options": {"queryBatching": "independently"},
            },
            position=(240, 0),
            credentials=pg,
            alwaysOutputData=False,
            onError="continueErrorOutput",
        ),
        boolean_node(
            "Valid Claim",
            "={{ (" + CLAIM_VALIDATOR_JS + ")($input.all().map(i => i.json)) }}",
            (450, 0),
        ),
        node(
            "Capture Mail",
            "n8n-nodes-opsflow.opsflowSmtp",
            1,
            {"claim": "={{ $json }}"},
            position=(680, -100),
            credentials=smtp,
            onError="continueErrorOutput",
        ),
        boolean_node(
            "SMTP Accepted",
            '={{ Object.keys($json).length === 2 && $json.run_id === $("Claim").first().json.run_id && $json.state === "accepted_by_smtp" }}',
            (910, -100),
        ),
        boolean_node(
            "Retryable Receipt",
            '={{ Object.keys($json).length === 2 && $json.run_id === $("Claim").first().json.run_id && $json.state === "cancelled" }}',
            (1120, 180),
        ),
    ]


def _database_nodes(pg):
    parameters = (
        '={{ [$("Claim").first().json.id, $("Claim").first().json.lease_token] }}'
    )
    nodes = []
    for name, function, result, position in (
        ("Ack", "ack_notification", "acknowledged", (1140, -250)),
        ("Retry Not Sent", "retry_not_sent_notification", "requeued", (1350, 150)),
        ("Mark Unknown", "unknown_notification", "quarantined", (1350, 400)),
    ):
        nodes.append(
            node(
                name,
                "n8n-nodes-base.postgres",
                2.6,
                {
                    "operation": "executeQuery",
                    "query": f"SELECT ops_flow.{function}($1::bigint,$2::uuid) AS {result};",
                    "options": {
                        "queryReplacement": parameters,
                        "queryBatching": "independently",
                    },
                },
                position=position,
                credentials={"postgres": dict(pg["postgres"])},
                onError="continueErrorOutput",
            )
        )
    return nodes


def _confirmation_nodes():
    return [
        boolean_node(
            "Verify Ack",
            "={{ $input.all().length === 1 && $json.acknowledged === true }}",
            (1380, -250),
        ),
        boolean_node(
            "Verify Retry",
            "={{ $input.all().length === 1 && $json.requeued === true }}",
            (1580, 150),
        ),
        node(
            "Acknowledged",
            "n8n-nodes-base.code",
            2,
            {
                "mode": "runOnceForAllItems",
                "jsCode": 'return [{json:{run_id:$("Claim").first().json.run_id,state:"accepted_by_smtp"}}];',
            },
            position=(1600, -350),
        ),
    ]


def _failure_nodes():
    nodes = []
    for name, code, position in (
        ("DB Uncertain", "db_unavailable_or_lease_uncertain", (1350, 550)),
        ("Invalid Claim", "invalid_claim", (680, 350)),
        ("Ack Uncertain", "ack_lost_or_lease_expired", (1600, -150)),
        ("Lost Lease", "retry_lost_or_lease_expired", (1800, 300)),
        ("Retry Recorded", "retry_recorded_not_sent", (1800, -20)),
        ("Delivery Uncertain", "delivery_uncertain_fresh_claim_required", (1800, 80)),
    ):
        nodes.extend(
            [
                node(
                    "Redact " + name,
                    "n8n-nodes-base.code",
                    2,
                    {
                        "mode": "runOnceForAllItems",
                        "jsCode": f'return [{{json:{{state:"{code}"}}}}];',
                    },
                    position=position,
                ),
                node(
                    name,
                    "n8n-nodes-base.stopAndError",
                    1,
                    {"errorMessage": code},
                    position=(position[0] + 220, position[1]),
                ),
            ]
        )
    return nodes


def _connections():
    def edge(target):
        return {"node": target, "type": "main", "index": 0}

    def branches(*targets):
        return {"main": [[edge(target)] for target in targets]}

    return {
        "Manual": branches("Claim"),
        "Every Minute": branches("Claim"),
        "Claim": branches("Valid Claim", "Redact DB Uncertain"),
        "Valid Claim": branches("Capture Mail", "Redact Invalid Claim"),
        "Capture Mail": branches("SMTP Accepted", "Mark Unknown"),
        "SMTP Accepted": branches("Ack", "Retryable Receipt"),
        "Retryable Receipt": branches("Retry Not Sent", "Mark Unknown"),
        "Ack": branches("Verify Ack", "Mark Unknown"),
        "Retry Not Sent": branches("Verify Retry", "Mark Unknown"),
        "Mark Unknown": branches("Redact Delivery Uncertain", "Redact DB Uncertain"),
        "Verify Ack": branches("Acknowledged", "Mark Unknown"),
        "Verify Retry": branches("Redact Retry Recorded", "Mark Unknown"),
        **{
            "Redact " + name: branches(name)
            for name in (
                "DB Uncertain",
                "Invalid Claim",
                "Ack Uncertain",
                "Lost Lease",
                "Retry Recorded",
                "Delivery Uncertain",
            )
        },
    }


def build_workflow():
    """Return fresh deterministic public objects, with every trigger inactive."""
    pg = {
        "postgres": {
            "id": "REPLACE_WITH_LOCAL_CREDENTIAL_ID",
            "name": "opsflow-dev-notifier",
        }
    }
    smtp = {
        "smtp": {
            "id": "REPLACE_WITH_LOCAL_CREDENTIAL_ID",
            "name": "mailpit-internal-only",
        }
    }
    nodes = (
        _entry_nodes(pg, smtp)
        + _database_nodes(pg)
        + _confirmation_nodes()
        + _failure_nodes()
    )
    return {
        "name": "Operations manifest outbox to Mailpit (DEV draft)",
        "nodes": nodes,
        "connections": _connections(),
        "active": False,
        "pinData": {},
        "tags": [],
        "settings": {
            "executionOrder": "v1",
            "timezone": "Asia/Seoul",
            "executionTimeout": 120,
            "saveDataSuccessExecution": "none",
            "saveDataErrorExecution": "none",
            "saveManualExecutions": False,
            "saveExecutionProgress": False,
        },
    }


def render_workflow():
    return (
        json.dumps(build_workflow(), ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    expected = render_workflow()
    if args.check:
        return (
            0
            if args.output.is_file()
            and args.output.read_text(encoding="utf-8") == expected
            else 1
        )
    args.output.write_text(expected, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
