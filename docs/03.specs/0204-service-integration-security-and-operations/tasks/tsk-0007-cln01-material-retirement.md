---
title: "CLN01 Material Retirement Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0007"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# CLN01 Material Retirement Task

## Objective

Implement the narrow, audited retirement path for material that another owner
has retired in source. A candidate is deletable only after source, runtime,
jobs, backup/restore and external consumers are all confirmed absent; a
candidate list alone is not completion.

## Inputs and Authorization

The user authorizes this implementation, its tests, scoped validation, logical
commit and owning-Spec delivery after checks and independent review. The target
checkout is `/home/hyunyoun/data/hy-home.docker`; any host Docker observation
must still prove its mapping to that checkout. Private apply requires an
operator-owned `/tmp/cln01-<run>/` directory with mode 0700 and a mode-0600,
single-link regular manifest. No secret value, raw log, credential material or
private manifest is tracked or printed.

`COMM-002` is the protected canonical SMTP source. SMTP01, not CLN01, owns its
canonical cutover and generator work. `COMM-003` remains pending until SMTP01
has merged and source and operational cutover evidence exists; its dependent
PR is TBD. GoTrue SMTP `_FILE` support is not inferred. `PG-020` is retained
for rollback because its observed nlink is 2. Supabase, Nginx, SurrealDB and
Open Notebook optional materials are `UNKNOWN_BLOCKED`, not unused;
`owner@buenhyden` must re-review them by 2026-10-17. LAB runtime, Compose,
secrets, data and images are excluded. OpenBao/CA/backup keys, current
cryptographic identities, archives and history are protected from the helper.

## Work Log

### Initial issuance

This is the initial draft issuance, held for coordinated integration. Public
implementation results below are source evidence, not authority for private
apply or package completion. No Task lifecycle transition is claimed.

### W24 execution contract

The implementation writer owns only `scripts/operations/retire-materials.py`,
`scripts/lib/ops/retire_materials.py`, and their focused tests. SMTP01 owns
SMTP declarations and generator references. The public generator handoff at
`/tmp/cln01-public-handoff` is unverified and outside this Task's PR. Root
Compose, public environment contracts, Registry, catalog, gateway, Alloy and
backup changes remain serialized with their respective owner.

The helper defaults to inspection and requires explicit `--apply`. It accepts
only reviewed root-scope regular-file entries beneath `secrets`, `infra` or
`docs`; it rejects tracked files, protected paths, symlink traversal, non-file
nodes, shared inodes, stale review records and changed identities. It uses
dir-fd no-follow traversal, whole-manifest preflight and final identity checks.
Partial results distinguish `deleted`, `already-absent`, `failed`,
`not-attempted`, `deleted-durability-unknown` and
`deleted-identity-unconfirmed`; partial failure returns exit
2 without misrepresenting prior unlinks. Generator non-recreation remains an
SMTP01 acceptance concern, not a CLN01 implementation claim.

Before any private apply, stop or establish all known concurrent writers and
hold the shared generator lock. A hostile or uncooperative writer is a hard
precondition failure because the lock cannot stop it. The supervisor must
designate one executor, confirm the SMTP01 candidate executor and CLN01 assessment route, and confirm
fresh receipts; current user-integration holds remain in force. SMTP01's
metadata proof has distinct fields and no required timestamp/private-proof
mode, so it cannot be translated automatically into CLN01 manifest truth.
Recheck parent symlinks and file identity at apply time. Exact tracked targets
use `git rm -- PATH...`; private targets use the helper; an empty directory may
use `rmdir` only after inspection. No recursive removal, glob, prune, volume
deletion, credential API or broad environment evaluation is permitted.

### Input, ownership and observation receipt

Start `main`, `origin/main`, remote `main` and HEAD were all
`a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; worktree was clean. Relative to
`860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`, only the subsequent OpenBao
receipt and regression alignment changed. Those sources remain untouched.
The actual root include/service set equals the existing marked current
inventory in m0021; no new inventory or fixed service count is introduced.
The first comparison failed because plain PyYAML does not understand
`!override`; rerunning with the existing `_ComposeLoader` succeeded.

SEC01, SMTP01 and CLN01 were discovered concurrently authoring the original
checkout. CLN01 moved its ongoing public implementation by copying its own
files to `/tmp/hy-home-cln01`, branch `codex/cln01-material-retirement`, at the
same input revision. The original checkout was not reset, stashed or cleaned.
An automatic approval review rejected a proposed move/rewrite of shared Task
and Spec/Plan files because it could corrupt another session's uncommitted
work. That action did not execute; the safer copy-only isolation succeeded.
The original shared CLN01 contract drafts and generator edits remain for the
integration owner to reconcile. In particular the two uncommitted SPEC-0212
TSK-0004 filenames collide. No CLN01 SPEC-0212 Task is issued by this branch.
The scoped generator draft was written before its worker received the user's
SMTP01 ownership steering; it is preserved as a public handoff outside this
PR and is not GREEN or accepted. No private input was changed by that draft.

The user subsequently assigned common-file integration, actual deletion and
HOME rollout ordering to a separate supervisor. Default sequence is SEC01,
SMTP01, then CLN01, subject to the actual prerequisite PRs. This Task's source
commit/PR does not grant permission to merge shared edits independently.

Read-only Docker metadata confirmed Traefik's Compose working-directory label
matches `/home/hyunyoun/data/hy-home.docker`. No stopped or running containers
were found for the candidate service labels `auth`, `nginx`, `surrealdb` and
`open_notebook`. This is presence context only, not proof of consumer absence,
functional readiness or a current declaration/runtime digest match. The
canonical and duplicate SMTP paths remain present regular files with nlink 1;
PG-020 remains present with nlink 2. No file contents or secret hashes were
read, compared or recorded. Equality of SMTP values is user-supplied input.

### Candidate dispositions and missing facts

| Public material | Action / disposition | Five-axis evidence and residual |
| --- | --- | --- |
| COMM-002 canonical SMTP | NO_CHANGE / ACTIVE_KEEP | Source: Alertmanager and canonical SMTP owner. One exact bind is observed; current functional consumption is unverified. Jobs, recovery and external ownership are not re-certified. Unconditionally protected. |
| COMM-003 duplicate SMTP at `secrets/communication/supabase/supabase_smtp_password.txt` | BLOCKED_FACTS / pending ALIAS_REPLACED | SMTP01 owns source/generator cutover. The dependent PR and operational receipt are not yet available. No exact bind is observed, but two read-only ancestor mounts belong to node-exporter and cAdvisor; file-specific access purpose remains UNKNOWN; jobs, backup/restore and external consumers remain UNKNOWN. No delete decision. |
| PG-020 legacy app password | NO_CHANGE / RETAINED_FOR_RECOVERY | Public registry and prior Task explicitly preserve rollback use; current nlink 2 confirms an additional link. Runtime/jobs/external ownership and both link paths remain unclosed. Protected ID and exact path in the general helper. |
| Supabase, Nginx, SurrealDB/Open Notebook material | BLOCKED_FACTS / UNKNOWN_BLOCKED | Intentional optional/manual operating roles remain in source and existing inventory. Candidate containers absent; jobs, restore and external consumers unverified. Service/data removal is not approved by this observation. |
| LAB runtime/config/secret/data | OUT_OF_SCOPE / LAB_EXCLUDED | No new LAB operation or deletion. Document moves are a separate owner follow-up. |

There is no proven-unused actual private target at this input. No manifest of
fabricated true checks is created. @buenhyden and the integration supervisor
must resolve the named missing consumer/recovery facts by 2026-10-17 or record
a fresh bounded follow-up. A protected hold does not prevent any independently
proven UNUSED_DELETE item from being processed in its owning unit.

### Read-only host observations

The corrected COMM-003 path is a regular file with nlink 1; no alternate
duplicate location was observed. The canonical path has nlink 1 and PG-020 has
nlink 2. An all-container mount-only query found zero
COMM-003 exact binds, two read-only ancestor mounts and zero writable ancestor
mounts. The two ancestor roles are node-exporter and cAdvisor with read-only host-root
mounts; their file-specific access purpose remains UNKNOWN. This is not
consumer-zero evidence. The canonical file has one exact bind.

`hyhome-backup.timer` is enabled and active. Its installed service has the
exact original checkout as WorkingDirectory and its ExecStart contains the
registered `hyhome-backup.sh`. Declared host backup covers whole `secrets` with
an empty host-exclude setting. Encrypted restorability, snapshot retention,
RPO and RTO remain UNKNOWN; no private snapshot was listed or compared, and no
runtime state changed.

### Read-only command receipt

Observation input is the original operator checkout
`/home/hyunyoun/data/hy-home.docker` on 2026-10-10 KST. Git base is
`a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; its working tree has concurrent
SMTP01/SEC01 drafts, so the runtime query does not prove source/runtime parity.
The re-run wrapper below returned exit 0. Every Docker/systemd subprocess used
`check=True` and returned 0; raw mounts, container identifiers, service property
text and credential bytes were captured without printing. Only booleans and
public-ID counters were emitted. The file observations use lstat only.

```python
import json
import stat
import subprocess
from pathlib import Path

root = Path('/home/hyunyoun/data/hy-home.docker')
targets = {
    'COMM-002': root / 'secrets/communication/smtp/smtp_password.txt',
    'COMM-003': root / 'secrets/communication/supabase/supabase_smtp_password.txt',
    'PG-020': root / 'secrets/db/legacy-app/service_password.txt',
    'incorrect-COMM-003': root / 'secrets/communication/smtp/supabase_smtp_password.txt',
}
for identifier, path in targets.items():
    try:
        info = path.lstat()
        result = {'present': True, 'regular': stat.S_ISREG(info.st_mode), 'nlink': info.st_nlink}
    except FileNotFoundError:
        result = {'present': False}
    print(json.dumps({'id': identifier, 'file_state': result}))
identifiers = subprocess.run(['docker', 'ps', '-aq'], capture_output=True, text=True, check=True).stdout.split()
mounts = []
if identifiers:
    raw = subprocess.run(['docker', 'inspect', '--format', '{{json .Mounts}}', *identifiers], capture_output=True, text=True, check=True).stdout
    mounts = [mount for line in raw.splitlines() for mount in json.loads(line)]
for identifier in ('COMM-002', 'COMM-003', 'PG-020'):
    path = targets[identifier]
    exact = [mount for mount in mounts if mount.get('Type') == 'bind' and Path(mount.get('Source', '')) == path]
    ancestors = [mount for mount in mounts if mount.get('Type') == 'bind' and Path(mount.get('Source', '')) in path.parents]
    print(json.dumps({'id': identifier, 'all_container_mounts': {'exact': len(exact), 'ancestor_readonly': sum(not mount.get('RW') for mount in ancestors), 'ancestor_writable': sum(bool(mount.get('RW')) for mount in ancestors)}}))
for mode in ('is-enabled', 'is-active'):
    result = subprocess.run(['systemctl', mode, 'hyhome-backup.timer'], capture_output=True, text=True, check=True)
    allowed = {'enabled', 'active'}
    print(json.dumps({'timer_check': mode, 'state': result.stdout.strip() if result.stdout.strip() in allowed else 'UNKNOWN', 'exit': result.returncode}))
result = subprocess.run(['systemctl', 'show', 'hyhome-backup.service', '--property=WorkingDirectory', '--property=ExecStart'], capture_output=True, text=True, check=True)
print(json.dumps({'installed_backup_unit_exit': result.returncode, 'checkout_matches': f'WorkingDirectory={root}' in result.stdout.splitlines(), 'registered_script_matches': str(root / 'infra/09-platform-ops/restic/bin/hyhome-backup.sh') in result.stdout}))
```

The separate label-only wrapper also returned exit 0; its two Docker
subprocesses returned 0. It emits only candidate service counts and a checkout
match boolean, not container identifiers or raw label values.

```python
import json
import subprocess

identifiers = subprocess.run(['docker', 'ps', '-aq'], capture_output=True, text=True, check=True).stdout.split()
services = ('auth', 'nginx', 'surrealdb', 'open_notebook')
counts = dict.fromkeys(services, 0)
checkout_match = False
if identifiers:
    query = '{{index .Config.Labels "com.docker.compose.service"}}|{{index .Config.Labels "com.docker.compose.project.working_dir"}}'
    raw = subprocess.run(['docker', 'inspect', '--format', query, *identifiers], capture_output=True, text=True, check=True).stdout
    for line in raw.splitlines():
        service, _, checkout = line.partition('|')
        if service in counts:
            counts[service] += 1
        if service == 'traefik' and checkout == '/home/hyunyoun/data/hy-home.docker':
            checkout_match = True
print(json.dumps({'candidate_service_counts': counts, 'traefik_checkout_match': checkout_match}))
```

Actual label results: all four candidate counts are 0 and Traefik checkout
match is true. This does not establish external consumer absence or readiness.

Actual public results: COMM-002 present/regular/nlink 1, exact bind 1; COMM-003
present/regular/nlink 1, exact bind 0; PG-020 present/regular/nlink 2, exact bind
0. Each has two read-only ancestor binds and zero writable ancestor binds.
The incorrect COMM-003 path is absent. Timer enabled/active and installed unit
checkout/script match all returned exit 0/true. These facts do not certify
external consumers or a selected encrypted restore point.

Source commands were `rtk proxy rg -n 'SERVICE_POSTGRES|supabase_smtp_password|smtp_password' docker-compose.yml infra scripts .github .env.example secrets/SENSITIVE_ENV_VARS.md.example --glob '!scripts/lib/ops/retire_materials.py'`
and scoped reads of `infra/09-platform-ops/restic/{backup.sh,docker-compose.yml,sets/host-exclude.txt}`;
all succeeded (exit 0). The tracked host-exclude file contains only a comment
and the entrypoint includes `/src/host`, so source declares whole-secrets
backup. Actual backup success, snapshots and restore remain UNKNOWN/NOT_RUN.

### Five-axis continuation and P09 handoff

All candidates below are root-scope and owned by @buenhyden; the public catalog
remains the identity/path owner. Source at the current main still declares
COMM-003 for Supabase auth. SMTP01's unmerged work is not operational cutover.
The public source scan covers Compose, entrypoints, scripts and runbooks;
read-only host probes cover running and stopped Docker bind mounts and the
exact installed backup timer/service. None reads secret values or raw logs.

| Axis | COMM-003 | PG-020 / optional materials |
| --- | --- | --- |
| source | Current main root secret and auth grant still refer to the corrected file; SMTP01 transition pending | PG-020 catalog retains rollback; optional source/manual operations remain declared |
| runtime | No exact bind; node-exporter/cAdvisor read-only host-root mounts remain accessible; file-specific consumption UNKNOWN | PG-020 nlink 2; candidate service absence is only presence evidence |
| jobs | Installed backup timer active/enabled; registration maps to original checkout | Other scheduled/manual consumers are UNKNOWN |
| backup_restore | Declared host set includes all secrets, with no excludes; actual restore mapping/retention UNKNOWN | PG-020 rollback and Open Notebook encrypted credential recovery are retained |
| external | Client owners, cold-start/re-auth and rollback users are UNKNOWN | External clients and required HOME functions are UNKNOWN |

Specific retained optional inputs include AI-003 at
`secrets/db/surrealdb/surreal_db_password.txt`, AI-004 at
`secrets/tools/open-notebook/open_notebook_password.txt`, and protected AI-005
at `secrets/tools/open-notebook/open_notebook_encryption_key.txt`. Their
explicit Compose consumers and RUN-0073/0080 recovery contracts prevent an
unused classification. `infra/01-gateway/nginx/config/nginx.conf` is tracked
and mounted by the optional gateway; its manual RUN-0011 contract remains a
consumer. Supabase init/config and tracked runbooks are likewise not deletion
candidates merely because their profile is inactive.

P09 remains another owner's preparation task. The earlier read-only plan
review found retention, backup/RPO/RTO, source ACL revocation and deletion-first
recovery reconciliation listed as future contracts. No standalone implemented
P09 artifact was available at that earlier observation; the subsequent
preparation-contract review below records the later public artifacts. Concrete retention periods, backup
custody, restore targets, measured RPO/RTO, deletion coverage of cache/old
generations and consumer revocation acknowledgments are UNKNOWN/NOT_RUN.
Preparation schemas and synthetic fixtures have a development acceptance
consumer and must not be retired as unused. No P09 file is authored here.
The integration owner must reconcile inherited active Wiki-implementation and
LAB-document-move exclusions against the current 11–30 request in its common
contract unit; completed P00 history is preserved.

SMTP01's inspected source has a distinct `--retire` path that rewrites private
metadata and unlinks COMM-003; the general CLN01 helper refuses that candidate.
At the earlier comparison its executor did not call `retirement_lock`; the
latest inspected SMTP source now calls an SMTP-local lock. Its public source
SHA-256 was `d6b8c9c1089d00bf4de2cf0558743324421403eb8a0daa6b9592f26c9f62b505`.
CLN01 locks `/tmp/cln01-retirement-<uid>-<root-dev-ino-digest>/lock`, whereas
SMTP01 locks `secrets/.smtp01-retirement.lock`. A synthetic one-root probe
acquired both concurrently: command exit 0, shared-lock compatibility FAIL.
The SMTP source claim that the lock is shared is not yet true. The proposed
integration order is canonical CLN root lock first, then SMTP-local lock;
the generator and sole SMTP executor must honor that order and pass a real
cross-process contention test. SMTP01 owns this correction. The original
shared generator draft remains unverified and outside this branch.

A synthetic `verify_proof` probe with a read-only host-root bind returned the
expected `old_runtime_parent_mount` refusal (command exit 0). The actual
node-exporter/cAdvisor ancestor mounts therefore remain an operational blocker;
their role names alone cannot authorize a broad exception. Maintenance must
narrow or quiesce their access, or the owner must prove an exact capability
exception with negative tests. No such runtime mutation was performed.

The proof schemas remain different. Do not translate SMTP boolean fields into
CLN five-axis truth; require fresh operator-owned host/root/source evidence,
writer/job quiescence and a selected restore or reissue path. Independent
security follow-up accepts the unchanged CLN source for logical commit/draft
PR, but private apply remains BLOCKED. Neither CLI is invoked against private
material by this Task.

### Execution and correction record

The source test-authoring route witnessed missing-helper RED (exit 1), then
basic actual-delete/idempotence GREEN (one synthetic test, exit 0). Expanded
boundary tests exposed missing protection, missing-parent retry and recreated
absent-target/post-unlink replacement handling; those cases were corrected.
The SMTP draft probe first had a test JSON-key error and was corrected before
its meaningful source RED (two expected failures, exit 1); it belongs to the
preserved handoff, not CLN01 SMTP acceptance. Scoped generator CLI RED was
observed (exit 1), and `bash -n` passed (exit 0); generator GREEN is NOT_RUN.

The first QA venv failed (exit 1) because host `ensurepip` is unavailable.
`uv venv /tmp/cln01-qa-uv --system-site-packages` and isolated installation of
coverage 7.16.2 succeeded without system package changes. The version was
verified on [PyPI](https://pypi.org/project/coverage/). Commitizen 4.15.1 uses
the existing repository pin. The Node `cz` command is not the Python checker;
no commit was produced by its failed version probe.

Script Manifest initially rejected unstaged new paths, then rejected the
existing draft backup runbook as runtime authority. After exact index
registration, the helper uses the same active local-secret/delivery Runbook
RUN-0009 that owns the existing generator. Draft RUN-0021 was not activated
or changed to bypass the gate. Manifest validation then passed.

Independent review found root alias/lock separation, Git environment injection,
missing hard protection for PG-020, and optional maintenance freshness, plus a
malformed-entry CLI traceback. Regression fixes and fresh independent code/security re-reviews resolved all
findings on the frozen input below. Earlier unit/coverage results remain bounded
to their older inputs.

The frozen helper input `956536c08ff0f6a8986cccae03f72d0e6dd61a3a46d4fc68acfbceb83289a337`
passed 50 focused tests (exit 0), fresh branch coverage 98% (exit 0, 328
statements and 114 branches), Ruff check and format-check (exit 0), and independent
code/security re-review PASS. The library/CLI plus Manifest/surface ownership
suites passed 105 tests (exit 0). These are SOURCE/UNIT/ISOLATED results, not
private deletion or HOME evidence. Unicode control/format paths are rejected
and receipt output uses ASCII escaping. COMM-003 is hard-held by both ID and
corrected exact path, including relabeled receipts, so this generic helper
cannot be a second SMTP deletion executor. The proposed sole unlink executor
is SMTP01's `smtp_contract --retire` after supervisor release; CLN01 owns the
assessment/hold. The generator draft's `inspect_plan` import cannot accept
COMM-003 under this hard hold and must not be repurposed as a second metadata
or file retirement route.

Lifecycle initially failed because W24 Dependencies contained text rather than
a Work Unit ID, and Evidence Acceptance used an unregistered value. Those
contract cells were corrected without validator changes. A later root edit
used `PASS, exit 0` in Evidence Result; the exact registered value `PASS`
resolved that parser error and its cascading metadata diagnostics. One root
API probe used a nonexistent metadata loader and failed with AttributeError;
the corrected registry loader exposed the real parser error. Full lifecycle
then passed (exit 0). The first staged controller failed (exit 2) because an
extra Runbook blank line was reformatted inside its isolated check; the line
was explicitly corrected and the controller then passed (exit 0). Unrelated
archive payloads and shared checkout files were not rewritten.

The local static command set is: `check-script-manifest.py`,
`check-github-workflow-contract.py`, metadata `--mode check-active` and the
four owning paths with `--mode check-changed`, document links `--mode all`,
corpus lifecycle `--base-ref a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`, and
`git diff --check`. Each passed (exit 0) after the parser fix. Full links retain
one pre-existing warning for historical source capture; archive recovery has
zero violations. `run-ci-gate.py --profile changed --explain` passed (exit 0)
and selected the existing local prerequisite route; aggregate candidate QA
belongs to the remote PR, not a second local full-suite run. The staged
controller's no-file checks are SKIPPED rather than evidence of those tools
examining changed Dockerfiles, shell, TOML or workflow YAML.

The registered local prerequisite command
`rtk proxy python3 scripts/validation/run-ci-gate.py --profile changed --local-only`
on staged tree `5299d401e324b0784418efefa8469f1ee517a41e` returned exit 1.
Its document-governance library run passed 644 of 645 tests; the remaining
historical-generation test rejected the premature parent `blocked` to
`in-progress` transition. Spec and Plan retain their original `blocked` status,
and the premature Lifecycle Events table was removed. A focused rerun first
rejected the header-only table (exit 1), so the entire empty table was removed;
the intervening four-path metadata run also returned exit 1 for that empty
table. It completed before a scoped stop attempt; no process was stopped. The new Task stays
draft; W24, AC12, IDs, created times and historical Task payloads are preserved.
No Registry, lifecycle validator or regression assertion was weakened. The
focused failing test then passed (1 test, 23.469 seconds, exit 0) after the
entire table removal. The final local prerequisite result is separate.

### Executed source commands

All commands below use HEAD `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` plus
the public working changes. Python source checks use the frozen helper SHA
above; the index and final delivery revision will be recorded independently.
The focused unit command and diff check passed (exit 0). Final metadata/link
results are recorded with the STATIC evidence after all Task edits.

```text
rtk proxy python3 -m unittest tests.lib.ops.test_retirement tests.validation.test_retirement_cli -q
python3 scripts/validation/check-document-metadata.py --mode check-changed --changed-path docs/03.specs/0204-service-integration-security-and-operations/spec.md --changed-path docs/03.specs/0204-service-integration-security-and-operations/plan.md --changed-path docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0007-cln01-material-retirement.md
python3 scripts/validation/check-document-links.py --root . --mode all
git diff --check
rtk proxy python3 -m unittest tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_current_repository_spec_packages_cover_spec_directories -v
```

### Reproducible dependency probes

The following public-only probe was run from `/tmp/hy-home-cln01` against
`/tmp/hy-home-smtp01/scripts/lib/ops/smtp_contract.py` at worktree HEAD
`7bb0d850742d1865ff904c857e6a9a8d42bb558e`. It is cross-worktree dependency
evidence, not CLN01 delivery acceptance. Save the exact Python below to
`/tmp/cln01-dependency-probes.py`, then run
`rtk proxy env PYTHONPATH=/tmp/hy-home-cln01 python3 /tmp/cln01-dependency-probes.py`.
The actual command returned exit 0; the semantic lock result is FAIL because
both locks acquired. Parent-mount refusal is the expected safe result. All
receipt booleans and Docker replies are synthetic; no operator proof, private
file, actual Docker command or retire/apply function is used.

```python
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch
from scripts.lib.ops.retire_materials import retirement_lock

source = Path('/tmp/hy-home-smtp01/scripts/lib/ops/smtp_contract.py')
expected = 'd6b8c9c1089d00bf4de2cf0558743324421403eb8a0daa6b9592f26c9f62b505'
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
print('smtp_source_sha256=' + expected)
revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=source.parents[3], capture_output=True, text=True, check=True).stdout.strip()
print('smtp_worktree_head=' + revision)
spec = importlib.util.spec_from_file_location('cln01_synthetic_smtp_probe', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='cln01-synthetic-interop-') as directory:
    root = Path(directory) / 'synthetic-root'
    (root / 'secrets').mkdir(parents=True)
    with retirement_lock(root), module.retirement_lock(root):
        print('lock_compatibility=FAIL:both_locks_acquired')
    fake_revision = 'a' * 40
    hashes = {'synthetic': 'synthetic-public-source'}
    proof = Path(directory) / 'synthetic-proof.json'
    proof.write_text(json.dumps({
        'host': 'synthetic-host', 'git_sha': fake_revision, 'source_sha256': hashes,
        'old_mount_consumers': [], 'job_backup_external_verified': True,
        'canonical_restore_mapping_verified': True, 'consumer_creation_quiesced': True,
        'source_private_mutation_quiesced': True, 'root_identity': module.root_identity(root)}))
    def fake_run(arguments, root=None):
        if arguments[0] == 'git':
            return (fake_revision + '\n').encode()
        if arguments[:2] == ['docker', 'ps']:
            return b'synthetic-container\n'
        return (json.dumps([{'Type': 'bind', 'Source': '/', 'Destination': '/host/root', 'RW': False}]) + '\n').encode()
    with patch.object(module, '_run', side_effect=fake_run), patch.object(module, 'source_hashes', return_value=hashes), patch.object(module.socket, 'gethostname', return_value='synthetic-host'):
        try:
            module.verify_proof(root, proof)
        except module.ContractError as error:
            assert str(error) == 'old_runtime_parent_mount'
            print('parent_mount_probe=EXPECTED_REFUSAL:old_runtime_parent_mount')
        else:
            raise AssertionError('read-only ancestor was not refused')
print('private_input_or_runtime_mutation=False')
```

Bounded actual output:

```text
smtp_source_sha256=d6b8c9c1089d00bf4de2cf0558743324421403eb8a0daa6b9592f26c9f62b505
smtp_worktree_head=7bb0d850742d1865ff904c857e6a9a8d42bb558e
lock_compatibility=FAIL:both_locks_acquired
parent_mount_probe=EXPECTED_REFUSAL:old_runtime_parent_mount
private_input_or_runtime_mutation=False
```

### Preparation-contract review follow-up

P09 artifacts subsequently appeared in `/tmp/hy-home-p09`; they remain owned
by that session. Read-only review examined the consumer policy, artifact
revocation/surface-watermark model and job/generation recovery contract.
The synthetic examples bind retention to 30 days, RPO to 3600 seconds and RTO
to 7200 seconds, with restore drill NOT_RUN; these are preparation inputs,
not actual retention authority or measured recovery performance. Deletion and
revocation must be replayed before generation publication; access/cache/old
surface declarations must cover the event watermark. Physical cleanup and
real access denial remain NOT_RUN. Actual retention/custody, restore targets,
measured RPO/RTO and revocation acknowledgments remain UNKNOWN.

The public helper input was
`51044ec43592c8eccf40774d821016784e562bb0d30a59bd66d38685b3ecc0af`,
and the public test input was
`48e1c70d218ddd951ae845e65325c0d6d9ec02712de0dfa351e45e13bce0e7d1`.
Both were unchanged before/after the following five selected synthetic tests
(2.140 seconds, exit 0, PASS), run from `/tmp/hy-home-p09`:

```text
rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest tests.lib.ops.test_wiki_preparation.PreparationTests.test_policy_binds_consumer_artifact_and_job_authority tests.lib.ops.test_wiki_preparation.PreparationTests.test_artifact_hash_acl_revocation_and_provenance tests.lib.ops.test_wiki_preparation.PreparationTests.test_job_state_retry_generation_and_delete_priority tests.lib.ops.test_wiki_preparation.PreparationTests.test_revocation_delete_priority_and_public_dead_state_rejection tests.lib.ops.test_wiki_preparation.PreparationTests.test_canonical_paths_surface_watermarks_and_retry_history -v
```

This is bounded source/synthetic review, not the complete P09 acceptance suite.
P09 schemas/fixtures have an explicit development-acceptance consumer and
remain ACTIVE_KEEP. No P09 source/doc file is created, moved or modified here.

### Final local verification and logical delivery receipt

Source commit `3048c31fe2e1a53d4b481df3fda5ce587cae80c5` has tree
`61457438a65d3eb73ed56e10d1a2b2251cb06d85` and unchanged frozen helper SHA.
The ordinary commit hook and Commitizen check returned exit 0. It contains
only the 11 CLN01 files listed in the source increment; the original mixed
checkout and SMTP01/P09 files remain untouched.

Exact source increment (A = created, M = modified; no tracked deletion):

```text
M .github/workflow-contract.yml
M docs/03.specs/0204-service-integration-security-and-operations/plan.md
M docs/03.specs/0204-service-integration-security-and-operations/spec.md
A docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0007-cln01-material-retirement.md
M docs/05.operations/runbooks/0009-release-management.md
A scripts/lib/ops/retire_materials.py
M scripts/manifest.yaml
A scripts/operations/retire-materials.py
A tests/lib/ops/test_retirement.py
M tests/validation/_script_manifest_support.py
A tests/validation/test_retirement_cli.py
```

The final Task-only metadata check passed (selected 1, zero violations, exit
0) and its staged controller passed (exit 0). The later prose/file-list correction also passed metadata (selected 1, zero
violations, exit 0). Its first staged style run caught tabs from Git name-status
output (exit 2); these were explicitly replaced with spaces before a fresh
staged controller rerun. No style or metadata policy was weakened.

On that tree, the second registered local prerequisite command returned exit
1 due to two pre-existing worktree permission mismatches: Open WebUI and
Gatus entrypoints were mode 0775 while their tests prohibit group/world
writing. The two exact local files were adjusted with
`rtk proxy chmod go-w -- infra/08-ai/open-webui/docker-entrypoint.sh infra/06-observability/gatus/docker-entrypoint.sh`.
Their contents and Git tree were unchanged; no operator checkout or service
was modified. The focused two-test command below then passed (exit 0):

```text
rtk proxy python3 -m unittest tests.validation.test_openwebui_oidc_entrypoint.OpenWebUiOidcEntrypointTests.test_script_is_executable_and_not_group_or_world_writable tests.validation.test_gatus_oidc.GatusOidcEntrypointTests.test_script_is_not_group_or_world_writable -v
```

The original aggregate is still FAIL, not retroactively PASS. Its completed
prefix passed hook tests 15, lifecycle tests 15, metadata tests 142, document
library tests 645, supply-chain fixtures 239, candidate preflight and full
links, plus isolated conftest 18/18. The failed Compose batch had 421 tests,
two failures and 59 native opt-in SKIPs. Permission correction is a local QA
repair, not a tracked deployment change. An exploratory `--profile operations`
explain command returned exit 1 because that profile is unregistered; the
registered contract was not changed to accept it.

To avoid rerunning the unchanged successful prefix, the registered runner was
used for the failed leaf and all remaining selected leaves. The exact script
below was saved to `/tmp/cln01-resume-local-leaves.py` and executed using
`rtk proxy env PYTHONPATH=/tmp/hy-home-cln01 python3 /tmp/cln01-resume-local-leaves.py`.
It verified the frozen tree, parsed the original contract, constructed and
validated the complete normal local plan, then resumed at the failed Compose
leaf using the original descriptor/environment/timeout executor. No bypass
flag, fixture expectation or runner source was changed. The resumption
returned exit 0; this is bounded leaf evidence, not a successful rerun of the
whole aggregate command.

```python
import os
import subprocess
from pathlib import Path
from scripts.validation import ci_gate_runner as runner

root = Path('/tmp/hy-home-cln01')
expected = '61457438a65d3eb73ed56e10d1a2b2251cb06d85'
actual = subprocess.run(['git', 'write-tree'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
assert actual == expected
raw = runner.load_contract_document(root)
registry = runner.parse_gate_registry(raw, '.github/workflow-contract.yml')
assert not runner.validate_gate_registry(root, registry)
contract = runner.parse_public_gate_contract(raw)
context = runner.derive_execution_context(os.environ)
assert context is runner.ExecutionContext.LOCAL
paths = runner.collect_changed_paths(root, os.environ)
suites = runner.select_public_suites(contract, 'changed', paths)
roots = runner.public_root_gate_ids(contract, suites, changed_paths=paths)
plan = runner.build_public_validation_plan(registry, roots, contract, suites, context, profile='changed', root=root)
local = runner.build_local_only_validation_plan(plan, contract, context)
index = next(i for i, gate in enumerate(local) if gate.gate_id == 'leaf.compose-baseline-regressions')
remaining = local[index:]
print('Verification resumption only; original aggregate remains FAIL.', flush=True)
for gate in remaining:
    print('registered_remaining_leaf=' + gate.gate_id, flush=True)
raise SystemExit(runner.execute_execution_plan(root, remaining, os.environ))
```

The resumed results were Compose 421 (59 native opt-in SKIP), gate contract 27,
runner 60, adapters 42, workflow 36, control-plane 51, staged-controller shell
regressions PASS, release 18 and repository integrity 214. All resumed leaves
returned exit 0. Original/final logs are QA source-output artifacts outside Git,
not operator logs; public batch summaries and commands are retained here.
Latest lstat-only observation also returned exit 0: COMM-002 and COMM-003 are
still present regular files with nlink 1; PG-020 is present with nlink 2.
Actual private apply, HOME, migration, rotation and recovery remain NOT_RUN.
Remote PR candidate and coordinated merge remain pending.

### Latest main reconciliation

The evidence-only commit is `c015c1ee5ef21d44299e5a7b34f24cd8077f39d0`.
Read-only remote inspection found main
`cac9e10fa584754706598d624654e07e8d6531f4` (P09 issuance PR #414).
Local merge commit `a5d1447b96bc3a25ad145bd750cbb262f264162e`, tree
`4a1b6de6e5a4e28dccb3400fb4ffdd2ed175a003`, preserves both parents.
Spec/Plan conflicts were limited to versions and adjacent AC12/AC13,
W24/W25 and Task links. Both owners' additions remain; Spec is 1.4.1,
Plan is 1.5.1, both remain blocked. P09 Task 0008 is byte-identical to
main, with its ID, created time and body preserved; no P09 implementation
artifact was authored. Independent merge review found no additional defect.

On the resolved tree, three-path metadata passed (exit 0), the historical
Spec Package regression passed (1 test, exit 0), staged controller passed
(exit 0), full links passed (exit 0, one existing historical-capture warning),
and `git diff --cached --check` passed (exit 0). Lifecycle with explicit
latest-main base initially returned exit 1 during the uncommitted merge:
archive assessment requires that base to be an ancestor of HEAD. The source
of this refusal was verified in `archive_assessments._history`; no validator
or archive file was changed. The original a03c base passed (exit 0).
The latest-main-base rerun after the merge commit passed (exit 0):
corpus violations 0 and archive recovery violations 0. Remote main was rechecked and still matched cac9e10.
This is candidate-branch reconciliation, not a CLN01 PR merge into main.

```text
rtk git fetch origin main
rtk git merge --no-commit origin/main
rtk proxy python3 scripts/validation/check-document-metadata.py --mode check-changed --changed-path docs/03.specs/0204-service-integration-security-and-operations/spec.md --changed-path docs/03.specs/0204-service-integration-security-and-operations/plan.md --changed-path docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0008-llm-wiki-preparation.md
rtk proxy python3 -m unittest tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_current_repository_spec_packages_cover_spec_directories -v
rtk proxy bash scripts/validation/run-ci-precommit.sh --mode local-staged
rtk proxy python3 scripts/validation/check-document-links.py --root . --mode all
rtk proxy python3 scripts/validation/check-document-corpus-lifecycle.py --base-ref cac9e10fa584754706598d624654e07e8d6531f4
```

A later public-only SMTP dependency recheck found worktree HEAD
`e7bff9149f29a4bbb23d977dadf01f5988ee12fc`. Its helper SHA remained
`d6b8c9c1089d00bf4de2cf0558743324421403eb8a0daa6b9592f26c9f62b505`;
the distinct `secrets/.smtp01-retirement.lock` therefore remains an
interoperability blocker. CLN01 has not edited that source or generator.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SMTP01 dependency | 12 | W24 | merged delivery plus source and operational cutover evidence | SMTP01 delivery, dependent PR TBD | NOT_RUN | SMTP01 owner evidence | pending |
| Helper source acceptance | 12 | W24 | 50 focused tests, 98% branch coverage, Ruff and independent code/security review | frozen helper input `956536c08ff0f6a8986cccae03f72d0e6dd61a3a46d4fc68acfbceb83289a337` | PASS | CLN01 implementation patch | pending |
| Candidate classification | 12 | W24 | partial five-axis assessment; BLOCKED_FACTS until missing ownership/recovery facts close | current source and read-only observations on named host | DEFER | #read-only-host-observations | pending |
| Private deletion acceptance | 12 | W24 | manifest preflight and idempotent reinspection | operator manifest under `/tmp/cln01-<run>/` | NOT_RUN | operator host | pending |

## Review and Completion

SOURCE and UNIT passed on the frozen helper input; ISOLATED passed using only
synthetic fixtures. STATIC includes Manifest/workflow validation, active metadata, full links and
corpus lifecycle PASS (exit 0); the registered staged controller passed after
explicit blank-line corrections. Final staged input and delivery are separate. HOME, MIGRATION,
ROTATION and RECOVERY remain NOT_RUN. DELIVERY has the logical source commit
above; remote PR acceptance and coordinated merge remain pending. Private
apply, functional runtime proof and recovery remain NOT_RUN; the limited
checkout-to-host label observation above does not satisfy those criteria.
A Git logical revert can restore tracked source; it cannot restore private
material. Private recovery is limited to a pre-existing encrypted recovery
artifact or a reissue path proved before deletion. No service health, actual
secret migration, native SMTP delivery, runtime consumer absence, actual deletion or recovery is claimed by this draft.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Current request reconciliation](../../0212-request-baseline-and-reconciliation/spec.md)
- [Historical P00 Task](../../0212-request-baseline-and-reconciliation/tasks/tsk-0003-active-contract-and-exclusions.md)
- [OpenBao trust Task](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
