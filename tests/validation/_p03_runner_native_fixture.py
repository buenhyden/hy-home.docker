"""Bounded synthetic native fixture for the P03 n8n runner contract."""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from pathlib import Path

from tests.validation._opsflow_native_fixture import RehearsalFailure
from tests.validation._opsflow_native_inputs import (
    N8N_ID,
)
from tests.validation._p03_runner_outcomes import (
    ERROR_CATEGORY_NEEDLES as ERROR_CATEGORY_NEEDLES,
)
from tests.validation._p03_runner_outcomes import (
    SAFE_ERROR_CLASSES as SAFE_ERROR_CLASSES,
)
from tests.validation._p03_runner_outcomes import (
    indeterminate_error_facts as indeterminate_error_facts,
)
from tests.validation._p03_runner_outcomes import (
    safe_error_facts as safe_error_facts,
)
from tests.validation._p03_runner_outcomes import (
    safe_terminal_error_facts as safe_terminal_error_facts,
)

ROOT = Path(__file__).resolve().parents[2]
RUNNER_CONFIG = ROOT / "infra/07-workflow/n8n/n8n-task-runners.json"
NATIVE_FLAG = "P03_RUNNER_NATIVE_REHEARSAL"
NATIVE_IMAGE_ENV = "OPSFLOW_N8N_NATIVE_IMAGE"
NATIVE_CONTEXT_ENV = "OPSFLOW_N8N_NATIVE_CONTEXT"
FULL_TASK_TIMEOUT = 300
FULL_REQUEST_TIMEOUT = 330
CONTROLLED_EXECUTION_TIMEOUT = 2
FULL_REHEARSAL_SCOPE = "synthetic_main_broker_application_controls"
NATIVE_EXPLICIT = any(
    os.environ.get(key) is not None
    for key in (NATIVE_FLAG, NATIVE_IMAGE_ENV, NATIVE_CONTEXT_ENV)
)
CANCEL_JS = r"""
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const id = String(input.executionId || '');
const cookie = String(input.cookie || '');
if (!/^[A-Za-z0-9_-]+$/.test(id) || !cookie || cookie.includes('\n')) process.exit(2);
fetch('http://127.0.0.1:5678/rest/executions/' + encodeURIComponent(id) + '/stop', {
  method: 'POST', headers: {cookie}
}).then(response => {
  process.stdout.write(JSON.stringify({status: response.status, accepted: [200, 204].includes(response.status)}));
}).catch(() => process.exit(3));
""".strip()

RUNNER_SCENARIOS = (
    (
        "javascript_ok",
        "javaScript",
        "return [{json:{runner:'javascript'}}];",
        "success",
        None,
    ),
    (
        "python_ok",
        "pythonNative",
        "return [{'json': {'runner': 'python'}}]",
        "success",
        None,
    ),
    (
        "javascript_module_denied",
        "javaScript",
        "require('node:fs'); return [{json:{unexpected:true}}];",
        "error",
        None,
    ),
    (
        "javascript_environment_denied",
        "javaScript",
        "return [{json:{value:process.env.N8N_RUNNERS_AUTH_TOKEN}}];",
        "error",
        None,
    ),
    (
        "python_module_denied",
        "pythonNative",
        "import os\nreturn [{'json': {'unexpected': True}}]",
        "error",
        None,
    ),
    (
        "python_fixture_secret_file_denied",
        "pythonNative",
        "data=open('/run/secrets/n8n-runner-token','rb').read(1)\nreturn [{'json': {'secret_file_readable': bool(data)}}]",
        "error",
        None,
    ),
    (
        "python_candidate_secret_file_denied",
        "pythonNative",
        "data=open('/run/secrets/n8n_runner_auth_token','rb').read(1)\nreturn [{'json': {'secret_file_readable': bool(data)}}]",
        "error",
        None,
    ),
    (
        "javascript_candidate_secret_file_denied",
        "javaScript",
        "const fs=require('node:fs'); const b=fs.readFileSync('/run/secrets/n8n_runner_auth_token'); return [{json:{secret_file_readable:b.length>0}}];",
        "error",
        None,
    ),
    (
        "python_host_path_denied",
        "pythonNative",
        "data=open('/host/etc/passwd','rb').read(1)\nreturn [{'json': {'host_path_visible': bool(data)}}]",
        "error",
        None,
    ),
    (
        "python_docker_socket_denied",
        "pythonNative",
        "data=open('/var/run/docker.sock','rb').read(1)\nreturn [{'json': {'docker_socket_visible': bool(data)}}]",
        "error",
        None,
    ),
    (
        "timeout",
        "javaScript",
        "await new Promise(resolve=>setTimeout(resolve,15000)); return [{json:{unexpected:true}}];",
        "error",
        CONTROLLED_EXECUTION_TIMEOUT,
    ),
)
FILE_DENIAL_CATEGORIES = frozenset(
    {"filesystem_access_denied", "filesystem_not_mounted"}
)
# Owner decision 2026-11-08: the pinned runners refuse a file probe one layer
# early (Python removes `open`, JS denies `node:fs`); that denial counts.
PYTHON_FILE_DENIAL_CATEGORIES = FILE_DENIAL_CATEGORIES | {"builtin_denied"}
ANCESTOR_ALLOWED_CATEGORIES = PYTHON_FILE_DENIAL_CATEGORIES
SCENARIO_ALLOWED_CATEGORIES = {
    "javascript_module_denied": frozenset({"module_access_denied"}),
    "javascript_environment_denied": frozenset({"environment_access_denied"}),
    "python_module_denied": frozenset({"module_access_denied"}),
    "python_fixture_secret_file_denied": PYTHON_FILE_DENIAL_CATEGORIES,
    "python_candidate_secret_file_denied": PYTHON_FILE_DENIAL_CATEGORIES,
    "javascript_candidate_secret_file_denied": FILE_DENIAL_CATEGORIES
    | {"module_access_denied"},
    "python_host_path_denied": PYTHON_FILE_DENIAL_CATEGORIES,
    "python_docker_socket_denied": PYTHON_FILE_DENIAL_CATEGORIES,
    "timeout": frozenset({"task_timeout"}),
}
REHEARSAL_RECEIPT_STAGES = (
    "wrong_token_registration",
    *(name for name, *_rest in RUNNER_SCENARIOS),
    "ancestor_environment_probe",
    "peer_nonbroker_port",
    "cancellation",
    "restart_next_good_task",
    "manual_worker_actor",
    "paired_candidate_network_runtime",
    "private_workflow_compatibility",
    "candidate_compose_runtime",
    "fixture_equivalence",
)


def safe_execution_id(value: object) -> str:
    """Normalize n8n's numeric or string execution ID without widening it."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise RehearsalFailure("execution safe ID rejected")
    normalized = str(value)
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", normalized):
        raise RehearsalFailure("execution safe ID rejected")
    return normalized


def execution_entity_id(payload: object, requested: str) -> str:
    """Accept the raw entity or one exact HTTP data envelope, never its flatted field."""
    if not isinstance(payload, dict):
        raise RehearsalFailure("execution entity shape rejected")
    entity = payload
    if payload.get("id") is None and isinstance(payload.get("data"), dict):
        entity = payload["data"]
    returned = safe_execution_id(entity.get("id"))
    if returned != safe_execution_id(requested) or not isinstance(
        entity.get("data"), str
    ):
        raise RehearsalFailure("execution entity shape rejected")
    return returned


def runner_timing_environment(
    task_timeout: int, request_timeout: int
) -> tuple[str, str, str]:
    """Return the bounded broker timing contract used by the synthetic fixture."""
    if (
        isinstance(task_timeout, bool)
        or isinstance(request_timeout, bool)
        or not isinstance(task_timeout, int)
        or not isinstance(request_timeout, int)
        or not 1 <= task_timeout <= 600
        or not task_timeout <= request_timeout <= 600
    ):
        raise ValueError("runner timing contract rejected")
    return (
        f"N8N_RUNNERS_TASK_TIMEOUT={task_timeout}",
        f"N8N_RUNNERS_TASK_REQUEST_TIMEOUT={request_timeout}",
        "N8N_RUNNERS_GRANT_TOKEN_TTL=120",
    )


def full_rehearsal_contract() -> dict[str, object]:
    """Return a fresh receipt scope for the bounded full application rehearsal."""
    return {
        "scope": FULL_REHEARSAL_SCOPE,
        "candidate_timing": {
            "task_timeout_seconds": FULL_TASK_TIMEOUT,
            "request_timeout_seconds": FULL_REQUEST_TIMEOUT,
            "grant_token_ttl_seconds": 120,
            "auto_shutdown_timeout_seconds": 0,
        },
        "controlled_workflow_timeout_seconds": CONTROLLED_EXECUTION_TIMEOUT,
    }


def initial_rehearsal_scenarios() -> dict[str, dict[str, str]]:
    """Return a fresh, explicit NOT_RUN denominator for the full rehearsal."""
    return {name: {"status": "NOT_RUN"} for name in REHEARSAL_RECEIPT_STAGES}


def persist_scenarios(case, receipt: dict, changes: dict) -> dict:
    """Persist a new receipt copy so a later failure cannot erase prior stages."""
    updated = {**receipt, **changes}
    case.fixture.receipt["p03_runner_scenarios"] = updated
    return updated


def error_classifier_js() -> str:
    """Render the value-free classifier used inside the owned n8n API probe."""
    classes = json.dumps(sorted(SAFE_ERROR_CLASSES), separators=(",", ":"))
    categories = json.dumps(ERROR_CATEGORY_NEEDLES, separators=(",", ":"))
    return (
        "const classifyExecutionError=e=>{"
        f"const allowed=new Set({classes}),categories={categories};"
        "let cursor=e,errorClass='unknown',observedName=false,values=[];"
        "for(let depth=0;depth<4&&cursor&&typeof cursor==='object'&&!Array.isArray(cursor);depth++){"
        "const name=typeof cursor.name==='string'?cursor.name:'';"
        "if(name){observedName=true;if(errorClass==='unknown'&&allowed.has(name))errorClass=name;}"
        "for(const key of ['name','message','description','stack'])if(typeof cursor[key]==='string')values.push(cursor[key].slice(0,2048));"
        "cursor=cursor.cause;}"
        "if(errorClass==='unknown'&&observedName)errorClass='other';"
        "let errorCategory=e&&typeof e==='object'&&!Array.isArray(e)?'unclassified':'absent';"
        "const sample=values.join(' ').toLowerCase().slice(0,8192);"
        "for(const [candidate,needles] of categories)if(needles.some(needle=>sample.includes(needle))){errorCategory=candidate;break;}"
        "return {errorClass,errorCategory};};"
    )


def kernel_confinement_facts(status: str, apparmor: str) -> dict[str, bool]:
    """Return value-free facts from the owned runner's kernel status files."""
    fields = {}
    for line in status.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return {
        "no_new_privileges_enforced": fields.get("NoNewPrivs") == "1",
        "seccomp_filter_enforced": fields.get("Seccomp") == "2",
        "apparmor_profile_enforced": apparmor.strip().endswith(" (enforce)"),
    }


def p03_api_script(base: str) -> str:
    """Read one execution entity without confusing its flatted data field for an envelope."""
    start_marker = "else if(input.action==='execution'){"
    end_marker = "  else throw new Error('unknown_action');"
    if base.count(start_marker) != 1 or base.count(end_marker) != 1:
        raise ValueError("execution API script markers changed")
    start = base.index(start_marker)
    end = base.index(end_marker, start)
    branch = (
        r"""else if(input.action==='execution'){
   """
        + error_classifier_js()
        + r"""
   const response=await opsflowFetch(base+'/rest/executions/'+encodeURIComponent(input.executionId),{headers:auth});
   opsflowRequireOk(response); const raw=await opsflowJson(response);
   const rawEntity=raw&&typeof raw==='object'&&!Array.isArray(raw)&&raw.id!==undefined;
   const d=rawEntity?raw:raw?.data;const responseShape=rawEntity?'raw':'data_envelope';
   if(!d||typeof d!=='object'||Array.isArray(d)||d.id===undefined||typeof d.data!=='string')throw new Error('execution_shape');
   const parsed=require('flatted').parse(d.data);const rd=parsed?.resultData?.runData||{};
   const ns=n=>{const rows=rd[n]||[];return rows.length?String(rows[rows.length-1].executionStatus||'unknown'):'absent';};
   const codeRows=rd.Code||[];const codeJson=codeRows.at(-1)?.data?.main?.[0]?.[0]?.json||{};
   const runnerResult=['javascript','python'].includes(codeJson.runner)?codeJson.runner:null;
   const recoveredResult=codeJson.recovered===true?true:null;
   const tokenNameVisible=typeof codeJson.token_name_visible==='boolean'?codeJson.token_name_visible:null;
   const ancestorEnvironmentReadable=typeof codeJson.ancestor_environment_readable==='boolean'?codeJson.ancestor_environment_readable:null;
   const executionError=parsed?.resultData?.error||codeRows.at(-1)?.error||null;
   const {errorClass,errorCategory}=classifyExecutionError(executionError);
   out={id:String(d.id),mode:String(d.mode),status:String(d.status),finished:Boolean(d.finished),terminal:Boolean(d.stoppedAt),responseShape,dataType:typeof d.data,errorClass,errorCategory,runnerResult,recoveredResult,tokenNameVisible,ancestorEnvironmentReadable,acknowledged:ns('Acknowledged'),deliveryRedacted:ns('Redact Delivery Uncertain')};}
"""
    )
    return base[:start] + branch + base[end:]


def native_selection(environ: dict[str, str] | None = None) -> tuple[str, str] | None:
    env = os.environ if environ is None else environ
    values = tuple(
        env.get(key) for key in (NATIVE_FLAG, NATIVE_IMAGE_ENV, NATIVE_CONTEXT_ENV)
    )
    if values == (None, None, None):
        return None
    if values != ("1", N8N_ID, "default"):
        raise RehearsalFailure(
            "runner native opt-in must select the reviewed image and default context"
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


def code_workflow(
    name: str,
    language: str,
    code: str,
    *,
    execution_timeout: int | None = None,
) -> dict:
    if language not in {"javaScript", "pythonNative"}:
        raise ValueError("unsupported Code language")
    if not name or not code or len(code) > 4096:
        raise ValueError("bounded workflow name and code are required")
    if execution_timeout is not None and (
        isinstance(execution_timeout, bool)
        or not isinstance(execution_timeout, int)
        or not 1 <= execution_timeout <= 30
    ):
        raise ValueError("bounded workflow execution timeout required")
    code_key = "jsCode" if language == "javaScript" else "pythonCode"
    settings = {
        "executionOrder": "v1",
        "saveDataErrorExecution": "all",
        "saveDataSuccessExecution": "all",
        "saveManualExecutions": True,
    }
    if execution_timeout is not None:
        settings = {**settings, "executionTimeout": execution_timeout}
    return {
        "name": name,
        "nodes": [
            {
                "parameters": {},
                "id": str(uuid.uuid4()),
                "name": "Manual",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [0, 0],
            },
            {
                "parameters": {
                    "mode": "runOnceForAllItems",
                    "language": language,
                    code_key: code,
                },
                "id": str(uuid.uuid4()),
                "name": "Code",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [240, 0],
            },
        ],
        "connections": {
            "Manual": {"main": [[{"node": "Code", "type": "main", "index": 0}]]}
        },
        "active": False,
        "settings": settings,
    }


def run_normal_javascript_diagnostic(case) -> None:
    """Run one candidate-budget JS execution through a prepared rehearsal case."""
    case.fixture.receipt["scope"] = "normal_js_diagnostic_only"
    case.fixture.receipt["candidate_timing"] = {
        "task_timeout_seconds": FULL_TASK_TIMEOUT,
        "request_timeout_seconds": FULL_REQUEST_TIMEOUT,
        "grant_token_ttl_seconds": 120,
        "auto_shutdown_timeout_seconds": 0,
    }
    case.fixture.verify_prerequisites()
    case.fixture.create_networks()
    case.secrets = case.fixture.create_secrets()
    case.fixture.start_postgres("metadata-pg", case.secrets["metadata_pg"][1])
    case.start_main(
        task_timeout=FULL_TASK_TIMEOUT, request_timeout=FULL_REQUEST_TIMEOUT
    )
    case.start_runner(case.secrets["runner"][1], task_timeout=FULL_TASK_TIMEOUT)
    case.fixture.wait_until(
        lambda: case.fixture.logs_contain("main", 'Registered runner "'),
        "external runner did not register with main broker",
        120,
    )
    setup = case.api("setup")
    case.owner_id = setup.get("id")
    if not isinstance(case.owner_id, str):
        raise RehearsalFailure("owner safe ID rejected")
    workflow_id = case.import_workflow(
        code_workflow(
            f"P03 normal JS diagnostic {case.fixture.attempt}",
            "javaScript",
            "return [{json:{runner:'javascript'}}];",
        )
    )
    _, terminal = case.run_workflow(
        workflow_id,
        frozenset({"success", "error"}),
        wait_seconds=FULL_REQUEST_TIMEOUT,
    )
    case.fixture.receipt["diagnostic_result"] = terminal["status"].upper()
    if terminal["status"] != "success":
        raise RehearsalFailure("normal JS diagnostic returned a safe error category")
    case.fixture.receipt["native"] = "PARTIAL"


def run_full_rehearsal(case) -> None:
    """Run the bounded Main-broker application controls in one owned fixture."""
    case.fixture.receipt.update(full_rehearsal_contract())
    case.fixture.verify_prerequisites()
    case.fixture.create_networks()
    case.secrets = case.fixture.create_secrets()
    case.fixture.start_postgres("metadata-pg", case.secrets["metadata_pg"][1])
    case.start_main()
    receipt = initial_rehearsal_scenarios()
    case.fixture.receipt["p03_runner_scenarios"] = dict(receipt)
    wrong = case.fixture.private("wrong-runner.secret", "synthetic-wrong-token\n")
    case.start_runner(wrong)
    time.sleep(3)
    if case.fixture.logs_contain("main", 'Registered runner "'):
        raise RehearsalFailure("wrong broker token registered a runner")
    receipt = persist_scenarios(
        case,
        receipt,
        {
            "wrong_token_registration": {
                "observation": "NOT_OBSERVED_WITHIN_3S",
                "status": "TEST_RESIDUAL",
            }
        },
    )
    case.fixture.remove("runner")
    case.start_runner(case.secrets["runner"][1])
    case.fixture.wait_until(
        lambda: case.fixture.logs_contain("main", 'Registered runner "'),
        "external runner did not register with main broker",
        60,
    )
    case.fixture.receipt["runner_kernel_confinement"] = kernel_confinement_facts(
        case.fixture.exec(
            "runner",
            "/bin/sh",
            "-ec",
            "grep -E '^(NoNewPrivs|Seccomp):' /proc/1/status",
        ),
        case.fixture.exec("runner", "/bin/sh", "-ec", "cat /proc/1/attr/current"),
    )
    if not all(case.fixture.receipt["runner_kernel_confinement"].values()):
        raise RehearsalFailure("runner kernel confinement was not enforced")
    setup = case.api("setup")
    case.owner_id = setup.get("id")
    if not isinstance(case.owner_id, str):
        raise RehearsalFailure("owner safe ID rejected")
    for name, language, code, expected, execution_timeout in RUNNER_SCENARIOS:
        workflow_id = case.import_workflow(
            code_workflow(
                f"P03 runner {name} {case.fixture.attempt}",
                language,
                code,
                execution_timeout=execution_timeout,
            )
        )
        accepted = (
            "success"
            if expected == "success"
            else frozenset({"success", "error", "canceled"})
            if name == "timeout"
            else frozenset({"success", "error"})
        )
        execution_id, terminal = case.run_workflow(
            workflow_id, accepted, wait_seconds=FULL_REQUEST_TIMEOUT
        )
        execution_id = safe_execution_id(execution_id)
        if expected == "success":
            expected_result = "javascript" if language == "javaScript" else "python"
            if terminal.get("runnerResult") != expected_result:
                raise RehearsalFailure(f"{name} functional result rejected")
            receipt = persist_scenarios(
                case,
                receipt,
                {
                    name: {
                        "execution_id": execution_id,
                        "functional_result": expected_result,
                        "status": "PASS",
                        "terminal_status": "success",
                    }
                },
            )
        elif terminal["status"] == "success":
            receipt = persist_scenarios(
                case,
                receipt,
                {
                    name: {
                        "denied": False,
                        "execution_id": execution_id,
                        "status": "FAIL",
                        "terminal_status": "success",
                    }
                },
            )
            raise RehearsalFailure(f"{name} access unexpectedly succeeded")
        elif terminal["status"] == "canceled":
            receipt = persist_scenarios(
                case,
                receipt,
                {
                    name: {
                        "attributed": name == "timeout",
                        "error_category": "controlled_workflow_timeout",
                        "execution_id": execution_id,
                        "status": "PASS" if name == "timeout" else "FAIL",
                        "terminal_status": "canceled",
                    }
                },
            )
        else:
            try:
                facts = safe_terminal_error_facts(
                    terminal, SCENARIO_ALLOWED_CATEGORIES[name]
                )
            except RehearsalFailure:
                failure = {
                    **indeterminate_error_facts(terminal),
                    "execution_id": execution_id,
                    "status": "FAIL",
                    "terminal_status": "error",
                }
                persist_scenarios(case, receipt, {name: failure})
                raise
            receipt = persist_scenarios(
                case,
                receipt,
                {
                    name: {
                        **facts,
                        "execution_id": execution_id,
                        "status": "PASS",
                        "terminal_status": "error",
                    }
                },
            )
    ancestor_probe = case.import_workflow(
        code_workflow(
            f"P03 runner ancestor environment probe {case.fixture.attempt}",
            "pythonNative",
            "pid=int(open('/proc/self/status').read().split('PPid:',1)[1].split()[0]); readable=False; visible=False\nfor _ in range(8):\n if pid<=1: break\n try:\n  data=open(f'/proc/{pid}/environ','rb').read(); readable=True\n  status=open(f'/proc/{pid}/status').read(); pid=int(status.split('PPid:',1)[1].split()[0])\n except OSError:\n  break\n visible=visible or b'N8N_RUNNERS_AUTH_TOKEN=' in data\nreturn [{'json': {'ancestor_environment_readable': readable, 'token_name_visible': visible}}]",
        )
    )
    ancestor_id, ancestor_terminal = case.run_workflow(
        ancestor_probe,
        frozenset({"success", "error"}),
        wait_seconds=FULL_REQUEST_TIMEOUT,
    )
    ancestor_id = safe_execution_id(ancestor_id)
    if ancestor_terminal["status"] == "success":
        visible = ancestor_terminal.get("tokenNameVisible")
        readable = ancestor_terminal.get("ancestorEnvironmentReadable")
        receipt = persist_scenarios(
            case,
            receipt,
            {
                "ancestor_environment_probe": {
                    "ancestor_environment_readable": readable is True,
                    "execution_id": ancestor_id,
                    "status": "FAIL" if readable is True or visible is True else "PASS",
                    "terminal_status": "success",
                    "token_name_visible": visible is True,
                }
            },
        )
        if readable is True or visible is True:
            raise RehearsalFailure("runner ancestor environment access succeeded")
    else:
        if ancestor_terminal.get("errorCategory") in ANCESTOR_ALLOWED_CATEGORIES:
            ancestor_facts = safe_terminal_error_facts(
                ancestor_terminal, ANCESTOR_ALLOWED_CATEGORIES
            )
        else:
            ancestor_facts = indeterminate_error_facts(ancestor_terminal)
        receipt = persist_scenarios(
            case,
            receipt,
            {
                "ancestor_environment_probe": {
                    **ancestor_facts,
                    "execution_id": ancestor_id,
                    "status": "PASS"
                    if ancestor_facts["attributed"] is True
                    else "TEST_RESIDUAL",
                    "terminal_status": "error",
                }
            },
        )
    peer_probe = case.import_workflow(
        code_workflow(
            f"P03 runner peer port probe {case.fixture.attempt}",
            "javaScript",
            "const r=await fetch('http://n8n:5678/healthz'); return [{json:{status:r.status}}];",
        )
    )
    peer_id, peer_terminal = case.run_workflow(
        peer_probe,
        frozenset({"success", "error"}),
        wait_seconds=FULL_REQUEST_TIMEOUT,
    )
    peer_id = safe_execution_id(peer_id)
    if peer_terminal["status"] == "success":
        persist_scenarios(
            case,
            receipt,
            {
                "peer_nonbroker_port": {
                    "execution_id": peer_id,
                    "observation": "REACHABLE",
                    "status": "FAIL",
                    "terminal_status": "success",
                }
            },
        )
        raise RehearsalFailure("Code reached the non-broker peer port")
    receipt = persist_scenarios(
        case,
        receipt,
        {
            "peer_nonbroker_port": {
                **indeterminate_error_facts(peer_terminal),
                "execution_id": peer_id,
                "status": "TEST_RESIDUAL",
                "terminal_status": "error",
            }
        },
    )
    cancellable = case.import_workflow(
        code_workflow(
            f"P03 runner cancellation {case.fixture.attempt}",
            "javaScript",
            "await new Promise(resolve=>setTimeout(resolve,15000)); return [{json:{unexpected:true}}];",
        )
    )
    cancellation_id = case.start_workflow(cancellable)
    case.cancel_execution(cancellation_id)
    case.await_execution(cancellation_id, "canceled", wait_seconds=FULL_REQUEST_TIMEOUT)
    receipt = persist_scenarios(
        case,
        receipt,
        {
            "cancellation": {
                "execution_id": safe_execution_id(cancellation_id),
                "execution_identity": "same",
                "post_stop_accepted": True,
                "status": "PASS",
                "terminal_status": "canceled",
            }
        },
    )
    case.fixture.stop("runner")
    case.fixture.start("runner")
    recovered = case.import_workflow(
        code_workflow(
            f"P03 runner recovered {case.fixture.attempt}",
            "javaScript",
            "return [{json:{recovered:true}}];",
        )
    )
    recovery_id, recovery_terminal = case.run_workflow(
        recovered, "success", wait_seconds=FULL_REQUEST_TIMEOUT
    )
    if recovery_terminal.get("recoveredResult") is not True:
        raise RehearsalFailure("restart next-good functional result rejected")
    receipt = persist_scenarios(
        case,
        receipt,
        {
            "restart_next_good_task": {
                "execution_id": safe_execution_id(recovery_id),
                "status": "PASS",
                "terminal_status": "success",
            },
            "manual_worker_actor": {"status": "NOT_RUN"},
            "paired_candidate_network_runtime": {"status": "NOT_RUN"},
            "private_workflow_compatibility": {"status": "NOT_RUN"},
            "candidate_compose_runtime": {"status": "NOT_RUN"},
            "fixture_equivalence": {
                "status": "NON_EQUIVALENT",
            },
            "fixture_differences": [
                "shared_internal_ctl_network",
                "fixture_specific_tmpfs",
                "fixture_specific_resource_caps",
            ],
        },
    )
    case.fixture.receipt["native_scope"] = full_rehearsal_contract()["scope"]
    case.fixture.receipt["native"] = "PARTIAL"
