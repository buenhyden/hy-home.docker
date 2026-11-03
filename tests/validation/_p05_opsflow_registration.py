"""Version-pinned authenticated editor registration; not a stable public API."""

import copy
import hashlib
import json
from pathlib import Path

from tests.validation import test_opsflow_native_rehearsal as historical
from tests.validation._opsflow_native_fixture import RehearsalFailure

WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/workflows/manifest-outbox-mailpit.json"
)
CREATE_BRANCH = r"""else if(input.action==='workflow_create'){
const p=(await call('/rest/projects/personal','GET',undefined,auth)).data;
if(p.type!=='personal'||typeof p.id!=='string')throw new Error('personal_project_rejected');
const w=input.workflow;
const body={name:w.name,nodes:w.nodes,connections:w.connections,settings:w.settings,projectId:p.id};
const r=await call('/rest/workflows','POST',body,auth);const d=r.data;
out={id:String(d.id),active:d.active!==undefined?Boolean(d.active):Boolean(d.activeVersionId),
project_id:d.homeProject?.id,personal_project_id:p.id,personal:d.homeProject?.type==='personal'};
}
else if(input.action==='profile')"""


def payload(tracked, attempt, credentials):
    expected = {
        "saveDataErrorExecution": "none",
        "saveDataSuccessExecution": "none",
        "saveExecutionProgress": False,
        "saveManualExecutions": False,
    }
    if tracked.get("active") is not False or any(
        tracked.get("settings", {}).get(key) != value for key, value in expected.items()
    ):
        raise RehearsalFailure(
            "tracked registration retention/inactive contract changed"
        )
    nodes = copy.deepcopy(tracked["nodes"])
    for node in nodes:
        for kind, credential in (node.get("credentials") or {}).items():
            if (
                kind not in credentials
                or credential.get("id") != "REPLACE_WITH_LOCAL_CREDENTIAL_ID"
            ):
                raise RehearsalFailure(
                    "workflow credential placeholder contract changed"
                )
            credential["id"] = credentials[kind]
    return {
        "name": "Opsflow native " + attempt,
        "nodes": nodes,
        "connections": copy.deepcopy(tracked["connections"]),
        "settings": {
            **tracked["settings"],
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
        },
    }


def validate_created(value):
    fields = {"id", "active", "project_id", "personal_project_id", "personal"}
    if (
        not isinstance(value, dict)
        or set(value) != fields
        or value["active"] is not False
        or value["personal"] is not True
        or any(
            not isinstance(value[key], str)
            or not historical.SAFE_ID.fullmatch(value[key])
            for key in ("id", "project_id", "personal_project_id")
        )
        or value["project_id"] != value["personal_project_id"]
    ):
        raise RehearsalFailure("created workflow ownership/inactive contract rejected")
    return value["id"]


def register(scenario):
    owner = scenario.api("setup").get("id")
    if not isinstance(owner, str) or not historical.UUID.fullmatch(owner):
        raise RehearsalFailure("owner setup safe ID rejected")
    postgres = scenario.api(
        "credential",
        credential=scenario.postgres_credential(scenario.secrets["notifier"][0]),
    ).get("id")
    smtp = scenario.api(
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
        isinstance(value, str) and historical.SAFE_ID.fullmatch(value)
        for value in (postgres, smtp)
    ):
        raise RehearsalFailure("credential safe IDs rejected")
    scenario.credential_ids = {"postgres": postgres, "smtp": smtp}
    original = WORKFLOW.read_bytes()
    body = payload(
        json.loads(original), scenario.fixture.attempt, scenario.credential_ids
    )
    content = json.dumps(body, separators=(",", ":")) + "\n"
    scenario.fixture.private("workflow.private.json", content)
    identifier = validate_created(scenario.api("workflow_create", workflow=body))
    rows = scenario.api("workflows").get("rows")
    matches = (
        [row for row in rows if row.get("name") == body["name"]]
        if isinstance(rows, list)
        else []
    )
    if (
        len(matches) != 1
        or matches[0].get("id") != identifier
        or matches[0].get("active") is not False
    ):
        raise RehearsalFailure("inactive owned workflow readback rejected")
    scenario.fixture.receipt["workflow_fixture"] = {
        "tracked_sha256": hashlib.sha256(original).hexdigest(),
        "bound_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "settings_delta": {
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
        },
    }
    scenario.fixture.receipt["workflow_registration"] = {
        "transport": "EDITOR_REST_PINNED_2_43_6",
        "inactive": True,
        "personal_project": True,
        "cold_cli_import": "NOT_RUN",
    }
    return identifier, body["name"]
