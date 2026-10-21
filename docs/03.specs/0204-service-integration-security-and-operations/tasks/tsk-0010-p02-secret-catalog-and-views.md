---
title: "P02 Secret Catalog and Value-Free Views Task"
version: "0.1.9"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-21"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0010"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P02 Secret Catalog and Value-Free Views Task

## Overview

### Objective

Own criterion 16 and W32: one value-free catalog, per-ID classification,
generated views and regeneration guards, reusing existing parsers and issued
identities. This Task authorizes a parallel source preparation slice; it does
not implement P06's real credential migration or claim production consumption.

## Inputs and Authorization

The current user requests a P02 prerequisite/conflict assessment and a concrete
worker handoff. The supplied P02 prompt is compared with clean local main
`2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`, rather than its historical
`860ac1c3` baseline. Remote main observed during assessment is
`a31a38ca29ee8e0683a29e61bf41347bfddc3d62`; a subsequent `ls-remote` and fetch
confirmed remote main at `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`.
ROOT did not push main in this assessment. These verified Git facts are separate
from session reports and operational acceptance. The earlier integration's
local-main/no-PR instruction is retained for SEC01/SMTP01/CLN01. The newly
supplied P02 execution prompt selects an owning-Spec PR after implementation
and latest-head CI/review; issuance itself makes no remote write. Dev is unused.

Read bootstrap/provider, SPEC-0204/0212, TSK-0005/0006/0007/0009, current root
declarations, public environment example, secret support matrix, generator,
public sensitive-reference example, and subject-0085 guide/policy/runbook.
Reconcile the complete reference code and tests with existing tools before
selecting canonical paths; never create a duplicate authority. Reference
heuristics are draft hints, not evidence of actual consumers or deletion safety.

### Worker Branch and Ownership

Create `codex/p02-secret-catalog` and
`/home/hyunyoun/data/hy-home.docker/.worktrees/p02-secret-catalog` from the
commit that issues this Task after it reaches local main. Record that exact
commit, worktree HEAD and clean status before writing. One existing or separately
assigned P02 worker owns the implementation; Task issuance starts no second
implementation session and does not touch foreign dirty worktrees.

The worker owns this Task and these source destinations, subject to a prior
NO_CHANGE/reuse check:

- `infra/03-security/openbao/secret-catalog.json` and
  `infra/03-security/openbao/secret-catalog.schema.json` as the single catalog
  and closed production metadata contract, not a second service inventory.
- `scripts/lib/ops/secret_catalog.py` for parsing, classification and view
  generation, with private `_secret_catalog_io.py` for fixed public-file and
  staging primitives, plus `scripts/operations/secret-catalog.py` as its narrow CLI.
  Reuse SMTP01 and existing metadata parsing rather than copying them.
- `tests/lib/ops/test_secret_catalog.py` and
  `tests/validation/test_secret_catalog_contract.py`, with synthetic fixtures
  in `tests/fixtures/secret-catalog/` and its Korean README if needed.
- Catalog-related additions to existing
  `docs/05.operations/{guides,policies,runbooks}/0085-openbao.md` and
  `infra/03-security/openbao/README.md` are proposals only. P01/TSK-0006 is
  the sole writer of these files during its active continuation; it integrates
  reviewed P02 paragraphs without replacing operational/auth/recovery text.

The worker prepares an ignored `.agent-work/integration-proposal/README.md` with exact
base blob IDs and patches for `scripts/operations/gen-secrets.sh`,
`secrets/SENSITIVE_ENV_VARS.md.example`, `infra/secret-file-support.json`,
`scripts/lib/ops/README.md`, test/fixture indexes and required manifest/workflow
regression registration. The integration coordinator is their sole final
writer. Any necessary public environment/schema amendment is also a proposal
for its P03/coordinator owner; it never sources or rewrites real dotenv state.
Root Compose, real/public environment, gateway, Alloy, backup, Registry,
Spec/Plan and other Tasks are read-only to the worker. A new shared need must be
added to the proposal before implementation and reviewed against current head.

### Parallel and Waiting Boundaries

Proceed now with public-source inventory, value-free catalog/schema, aliases,
classification, provisional destination plans, generated staging views,
regeneration guards, synthetic tests and subject-0085 documentation proposals. Preserve
COMM-002 at `secrets/communication/smtp/smtp_password.txt`; COMM-003 is an
alias/tombstone without another source/value/KV entry. Never renumber IDs.

The current public scanner consumes a ten-column source table and the SMTP
two-column alias table. The reference eight-column view is not a compatible
drop-in replacement. Preserve those consumers or submit a coherent parser,
generator and regression proposal with the SMTP01 owner; never change the
generated view alone. Image support is referenced from the existing support
matrix, not duplicated into a second mutable version authority.

Classify kv_static, stable_crypto, bootstrap_external, public configuration,
derived/runtime copies, UNUSED_DELETE and LAB exclusion separately. Preserve
encryption history and independent recovery custody. Keep unknown consumers
BLOCKED_FACTS and CLN01's positive rollback/init consumers retained. No profile
or lack of recent traffic proves absence. Published metadata must distinguish
declared, observed, imported, delivered, consumed, rotated, recovered and retired.

Wait for SEC01/P01's final image, auth, Agent and recovery contracts before
asserting final ACL/delivery/restart mappings or successful consumption. P06
owns selected real KV copy, credential delivery and migration acceptance.
CLN01 owns generic deletion eligibility; SMTP01 is the sole COMM-003 executor.
Reference migration code may be adapted and tested with mocks only in this
slice. It must not access production KV, tokens, secret payloads or source files.

No private sensitive table overwrite, credential read/copy/rotation/deletion,
HOME restart, LAB runtime, learning-app planning, actual Wiki or external
workspace creation occurs. Later private metadata inspection must first name
the exact host/path, output filter and recovery boundary in this Task and pass
independent review; only names, paths, modes and consumer metadata may leave it.

## Work Log

### Authorized Source Continuation

The user confirmed the existing source handoff and authorized correction of the
generator proposal's lock-lifetime defect. The issued draft is now ready for
this authorized continuation. This transition does not accept runtime lanes,
shared integration, hosted CI or delivery; the Task is not completed.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0010 | draft | ready | #authorized-source-continuation |
| SPEC-0204-TSK-0010 | ready | in-progress | #lock-lifetime-follow-up |

### Lock-Lifetime Follow-up

P09/TSK-0008 is an independently owned preparation-only Task. It consumes
value-free readiness plans and unresolved facts; it does not own OpenBao
migration or operational recovery. P01 and the owning backup/recovery Task
must establish actual custody and recovery acceptance, while P06 owns selected
migration, credential delivery and revocation. CLN01 owns deletion eligibility;
SMTP01 remains the sole COMM-003 executor. P10 owns end-to-end acceptance.

The worker reconciled its four logical commits onto local main
`f7543e0697e2473cbbbeb254792e7a1d5b4b8423` with `git rebase main`, exit 0;
the resulting pre-correction HEAD is
`e371e3ae344d3cdbc60e4bc1b2e0f3b194339aae`. The seven code/catalog/schema/test
files are byte-equivalent to the previous `ea927d004` source, verified with
`git diff --exit-code ea927d004 HEAD -- <seven-owned-source-paths>`, exit 0.
The initial sandboxed rebase failed with a namespace error, exit 1; the
approved retry succeeded. No reset, stash, clean or force push occurred.

The coordinator's independent receipt at the prior `ea927d004` input confirms
40 scoped tests, 13 generator synthetic tests and 147 affected regressions
passed. These tests did not detect the subsequently reproduced lock defect:
killing the Python parent released its lock while the Bash mutator continued.
The synthetic harness's exit 0 means successful defect reproduction, not
security acceptance. The ignored generator/helper proposal requires the same
held lock descriptor to reach the actual mutator, a parent-death regression
and independent code/security review before coordinator integration.

The ready bridge was committed as `b06b513c9` after the registered
local-staged gate and corpus lifecycle passed, exit 0. The first event-table
attempt used a noncanonical subsection and failed lifecycle and selected
metadata, exit 1; the canonical `Lifecycle Events` heading corrected the
chain. The Task is now in progress while shared integration and delivery
remain pending. ID, created date and prior issuance receipts are preserved.

The ignored helper proposal preserves the default root-identity API and adds
`with_fd=True` to yield that identity and the exact held descriptor. The
generator wrapper passes only that descriptor through `pass_fds`; there is
no explicit unlock or second lock. The synthetic parent-death test first
failed on the old wrapper, exit 1. After correction, eight lock tests,
13 generator proposal tests and 147 affected regressions passed, exit 0,
on input `e371e3ae` plus the exact ignored proposals. Ruff check and format
check passed after formatting the new regression, and its eight tests passed
again. The helper and generator functional source did not change during
formatting. Combined exact-main patch preflight and Bash syntax passed.

Independent security review of final helper patch SHA256
`ef791d3299de40f0233e9068bee33a7156768141afa0edcb601ec75ce3629019`
and generator patch SHA256
`5d4a487ebe119efade5ea2aff4635f682fbd26042803d908e3447fd4591891d1`
approved coordinator integration and independently passed eight lock tests.
This approval covers public source and synthetic subprocesses only. The
cooperative SMTP lock does not establish quiescence for the separate CLN01
lock or nonparticipating writers. No real generator, COMM-003 unlink or
private maintenance operation was performed.

On reconciled input `e371e3ae` plus this Task-only update, the source unit and
contract command passed 40 tests, exit 0. Branch coverage with appended CLI
render measured 91% total against an 80% threshold, exit 0. Ruff check and
format check on the five owned Python files passed; `check-views` returned
`P02_VIEWS_MATCH`, exit 0. The ignored receipt and integration handoff retain
exact commands, base blobs and patch hashes. The four P01 document proposals
now explicitly distinguish four tracked public inputs from four ignored
staging outputs; P01 remains their sole tracked writer. Actual Script Manifest
registration, combined-head review/CI and remote delivery remain pending.

### Worker Execution Plan

The user assigned this session as the single P02 implementation owner and then
required local `main` as the baseline for implementation and shared drafts.
The issued worker worktree was clean at `953a6c10e5ea7d7883b11f6d7f1a9f6f2104be2d`.
It was advanced with `git merge --ff-only main` to local main
`728ec6379f193256cee342550e38479cf3ebfc56`; exit 0. The two new helper/test files
were preserved. The subsequent SEC01 commit is baseline context, not a P02 edit.
A later local-main ownership update was reconciled at
`6da5e3bf380d5002e0e28181136fde8c016e49ce` with all owned drafts preserved.
OpenBao document drafts were saved as an ignored patch, following P01 sole
writer ownership. Before remote delivery, the coordinator must reconcile local-main publication
so an owning-Spec PR does not deliver unrelated baseline commits.

The worker remains on `codex/p02-secret-catalog` in the issued worktree.
The parent exclusively writes catalog/schema, the contract test, this Task and
ignored integration proposals. A bounded helper worker owns the library, CLI
and unit tests; a documentation worker prepares subject-0085 and OpenBao README
catalog proposals for the P01 sole writer. Inventory and independent review workers are read-only.
Request, token, elapsed-time, retry ceilings and shared-budget allocation are
UNKNOWN; no enforcement of an unspecified budget is claimed. Six concurrent
workers is a scheduling limit, not a runtime-provider guarantee.

W32 is implemented in three reviewable units: catalog/schema and per-ID source
contracts; tooling/staging views and regeneration refusal; subject-0085 usage
and verification evidence. Each new behavior gets a witnessed RED, focused
GREEN and negative boundary coverage. Shared generator/parser/view/index/gate
changes are proposed against local-main blob IDs before final integration;
the coordinator remains their sole final writer. No production values, source
secret files or real dotenv state are inspected. P01 delivery and recovery
contracts and P06 migration/consumption remain prerequisites for runtime lanes.
The user subsequently supplied the complete P02 execution input and reference
code/tests. All supplied file bodies were read before reconciliation. Existing
SMTP parsing and metadata consumers are reused. The reference migration HTTP
client and real value-copy lane belong to P06 and are not installed in this
public-source preparation slice. Its filename-only retirement heuristic does
not override CLN01 positive initialization and rollback consumers. The reference
eight-cell view is adapted to the existing ten-pipe-cell scanner contract, and
reference view/classification tests are mapped to canonical unittest guards rather than installing
a second `reference/` tool tree. The closed production schema is extended with
per-ID owner, action, public evidence and blocked mount/field/UID/GID/mode/rotation
plans; these fields are contracts, not observations or deployment evidence.

### Issuance and Worker Receipts

Task issuance has a measured RED probe on input `2b9f5ec82`: no Task 0010,
criterion 16 or W32 existed. This documentation-only unit supplies those
contracts; the matching availability probe passed after issuance. The first
metadata check failed on prose in W32's dependency cell and a non-draft initial
Task status. Correcting only those fields produced selected=3, violations=0,
exit 0; the resulting Task remains draft. Independent review and document
links confirmed the issuance boundaries and existing link targets. The worker
implementation, full per-ID acceptance and all runtime
lanes remain unexecuted at issuance. Do not mark this Task completed merely
because it is issued.

The helper parser RED used `/tmp/hy-home-p09-qa/bin/python -m unittest discover
-s tests/lib/ops -p test_secret_catalog.py -v` on input `953a6c10` plus the new
minimal test: exit 1, missing module. The minimal parser GREEN used the same
command plus the new library: one test, exit 0. These are historical focused
results; checks after reconciliation use `728ec637` plus owned changes.
A proposal-preparation invocation of `rtk proxy python` failed with exit 1
because this host provides `python3`; it made no edits. The corrected command
uses `rtk proxy python3`.

The worker subsequently fast-forwarded to local main
`74feff9429d302233d2475b31beed3dbf2ac07c9` with `git merge --ff-only main`,
exit 0. This includes P03 ownership issuance; no P03 files are worker edits.
The catalog derives the active issued IDs and alias from the existing public
source table, without a fixed service inventory. Original source dates use
`source_recorded_at`; they do not claim review, rotation or delivery dates.
Known Compose/environment grants and all nine `process_htpasswd` input/output
IDs record declared source/job consumers. Runtime, manual/external clients and
actual recovery remain UNKNOWN until P01/P06 receipts. Positive initialization,
rollback, independent backup custody, PG-020 and crypto history remain retained.
No proven UNUSED_DELETE target was identified in this public-source slice.
Unknown consumer facts must be reconciled by P01/P06 with CLN01 by 2026-10-18;
this review deadline authorizes no deletion or default migration.

The action contract binds DELETE bidirectionally to UNUSED_DELETE and
OUT_OF_SCOPE to LAB exclusion. UNKNOWN_BLOCKED requires BLOCKED_FACTS;
IMPLEMENT requires root kv_static ACTIVE_KEEP with declared source consumers.
VERIFY_RUNTIME preserves active/recovery rows with source consumers; NO_CHANGE
preserves known active or retained recovery rows. Only IMPLEMENT may enter the
initial generation guard, and all other crypto/custody/automation/lifecycle
conditions still apply. These actions never authorize a private operation.
The owner/evidence pointers and blocked mount/field/UID/GID/mode/ACL/delivery/
reload/restart/rotation plans are explicit metadata, not accepted runtime facts.

Independent code/security review found missing source/job consumers, action
contradictions and an earlier single-read I/O assumption. Bounded EOF reads now
validate size and identity. On input `74feff942` plus the owned RED tests,
`/tmp/hy-home-p09-qa/bin/python -m unittest
 tests.validation.test_secret_catalog_contract.SecretCatalogContractTests.test_generator_htpasswd_inputs_are_declared_consumers
 tests.validation.test_secret_catalog_contract.SecretCatalogContractTests.test_schema_rejects_contradictory_action_authority -q`
failed with 13 subtest failures, exit 1. After catalog/schema correction,
`/tmp/hy-home-p09-qa/bin/python -m unittest
 tests.validation.test_secret_catalog_contract -q` passed nine tests, exit 0.
The prior `6da5e3bf` helper/contract run passed 34 tests and branch coverage 91%;
it is superseded by final post-review results below, not reused as final-head proof.

Four generated files remain confined to `.agent-work/p02-views`: compatible
public example, value-free local staging table, summary and Korean README.
The actual private sensitive table and dotenv are neither read nor overwritten.
Reference view/classification boundaries use canonical unittest tests.
The reference HTTP/CAS copy tests are NOT_RUN and remain P06 work; no migration
mock or network result is claimed. The complete reference pytest command is
NOT_RUN because pytest is absent in the isolated QA environment.
Real HTTP/KV migration is NOT_RUN and belongs to P06; no mock equals delivery proof.

Shared generator, workflow/manifest/index and P01 documentation changes remain
ignored exact-base proposals. The final generator proposal has 13 synthetic tests, exit 0, on library
`89602c6d` SHA256. Its 147-test compatibility overlay passed, exit 0, on the
preceding `6382d9f3` library; this older input is explicitly retained and is not
claimed as latest-library evidence. The last correction only aligns malformed
LAB consumer validation with the unchanged schema. Its apply path performs
no COMM-003 unlink; SMTP01 owns its executor, proof and lock contract. Generic
CLN01 deletion still requires a writer-stop boundary because its lock is
separate. No claim of coordinated private maintenance is made.

A first selected metadata run failed on a forbidden level-two heading, exit 1.
The execution and receipt headings were nested under Work Log as required.
A search command with an unmatched shell glob failed before execution, exit 1;
explicit validator paths corrected discovery. Document gates run after the
final body update. SOURCE/UNIT/STATIC results are scoped public-source evidence;
ISOLATED denotes synthetic tests. HOME/MIGRATION/ROTATION/RECOVERY/DELIVERY remain
NOT_RUN pending their owning operational and coordinator integration gates.

### Final Source Receipts and Integration Handoff

All material independent code/security findings were closed against library
SHA256 `89602c6da2c48b341d913c7582780c29ca9bcd3b44f5d8946105551c62eeb52d`.
A declared active or recovery consumer must name at least one source path.
The sole empty-list exception is the exact unused_delete/UNUSED_DELETE/DELETE
metadata triple; this known-zero source declaration is not a CLN01 operational
five-axis absence receipt. No production row uses this exception. The library
and schema reject malformed LAB declarations consistently with and without the
schema. Positive LAB fixtures are synthetic source metadata only.

The final tooling unit passed 30 unittest cases, exit 0, on `74feff942` plus
owned source. It was committed as
`d82f6fc825e2b7e97c335dd4f49283c8a7428ea5`. While separating logical commits,
the production catalog/schema were temporarily absent from the Git index;
combined checks stopped with `public_input_not_tracked`, exit 1. This expected
fail-closed result was corrected by staging only the three owned public files.
The catalog/schema/production contract unit was committed as
`1148592d8e6152667a08bc90c02f7d9d960f2d04` after final 40-test GREEN, exit 0.
Both units passed `bash scripts/validation/run-ci-precommit.sh --mode local-staged`
on their actual indexes, exit 0. Unrelated file-type hooks were SKIP because
no matching staged files existed. No hook bypass was used.

Final commands used `/tmp/hy-home-p09-qa/bin/python` (QA) unless indicated:

- `-m coverage run --branch --include='*/scripts/lib/ops/*secret_catalog*.py,*/scripts/operations/secret-catalog.py' --data-file=/tmp/p02-secret-catalog-root-final.coverage -m unittest tests.lib.ops.test_secret_catalog tests.validation.test_secret_catalog_contract -q`: 40 PASS, exit 0, input `d82f6fc82` plus the staged catalog unit.
- `-m coverage run --append --branch --include='*/scripts/lib/ops/*secret_catalog*.py,*/scripts/operations/secret-catalog.py' --data-file=/tmp/p02-secret-catalog-root-final.coverage scripts/operations/secret-catalog.py --root <worker-worktree> render`: four staging files, exit 0.
- `-m coverage report --data-file=/tmp/p02-secret-catalog-root-final.coverage --fail-under=80`: total 91%, CLI 88%, library/I/O 91%, exit 0.
- `scripts/operations/secret-catalog.py --root <worker-worktree> check` and `check-views`: valid public metadata and matching views, exit 0.
- Ruff `check` and `format --check` on all five owned Python files: PASS, exit 0. `git diff --check HEAD` and staged diff checks: PASS, exit 0.
- `scripts/validation/check-document-metadata.py --mode check-changed --changed-path docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0010-p02-secret-catalog-and-views.md --base-ref main`: selected=1, violations=0, exit 0, input `74feff942` plus the prior Task body. Final evidence additions require the same gate again.
- `scripts/validation/check-document-corpus-lifecycle.py --base-ref main`: violations=0, exit 0. `scripts/validation/check-document-links.py --mode all`: failures=0, exit 0; one existing warning for unverified historical archive links.
- QA `-m pip_audit -r scripts/requirements.txt` failed, exit 1, because the module was absent. `uv tool run pip-audit -r scripts/requirements.txt` failed, exit 1, because ensurepip is unavailable. `uv pip compile scripts/requirements.txt --output-file /tmp/p02-validation-audit.lock`, followed by `uv tool run pip-audit --disable-pip --no-deps -r /tmp/p02-validation-audit.lock`, audited the fully resolved validator dependency graph and passed, exit 0. Repository dependency files were unchanged.
- `scripts/validation/check-script-manifest.py --check-generated`: FAIL, exit 1, exactly three missing registrations on `1148592d8`. The ignored manifest patch is required; its initial generator kind/order and proof declarations were corrected in the proposal. Existing short-read tests now import the actual private companion rather than its library re-export, to provide genuine manifest test-use evidence.

`<worker-worktree>` means the exact issued P02 worktree above. The fixed
public staging directory is ignored; there is no production deployment effect.
The previous unmodified-generator 147-case SOURCE/UNIT compatibility command
and the proposal's final synthetic command are recorded with their exact
inputs in `.agent-work/integration-proposal/generator/README.md`. Independent
document review confirmed proposal-only ownership and runtime boundaries;
its pending-receipt concern is resolved by these scoped final receipts.

The integration coordinator receives `.agent-work/integration-proposal/README.md`
and exact-base patches for manifest, workflow, indexes and generator/regressions;
P01 receives the preserved four-file catalog documentation patch. Shared
tracked files remain untouched. Apply each only after matching its recorded
blob to current local main, then run registered changed checks, script manifest,
40 P02 tests, affected generator regressions, metadata/links/lifecycle and
independent latest-head review. P01/P03/P06/P08/P10 receive schema version 1.0.0,
issued ID/alias mapping, provisional destination/recovery graph and all blocked
runtime facts from the committed catalog. Their final ACL, delivery, restart,
retention/RPO/RTO and migration receipts remain unresolved owning contracts.

`git ls-remote --heads origin main` confirmed remote main
`6da5e3bf380d5002e0e28181136fde8c016e49ce`, exit 0; that receipt used local main
`74feff9429d302233d2475b31beed3dbf2ac07c9`. No P02 remote push, PR or merge has
occurred. DELIVERY is NOT_RUN until shared integration and publication align;
an owning-Spec PR must exclude unrelated P03 baseline work. HOME, MIGRATION,
ROTATION and RECOVERY are NOT_RUN. No real values, source secret files, volumes,
services, credentials or LAB runtime were changed or deleted. Tracked source
commits support Git rollback; no nonexistent private recovery is promised.

Before handoff, local main advanced to
`4e26a5a8022a7307c7461af60337442912955df1` (P04 ownership issuance).
`git rebase main` preserved all four unpublished P02 logical units without
conflicts, exit 0; only upstream Spec/Plan/P04 Task changed. The original commit
SHAs above identify historical measured inputs, not the final delivery list.
The current four commits and latest-base receipts are in the ignored integration
handoff. Shared proposal base blob IDs are unchanged and are rechecked against
this local main. No force push, reset, stash or clean occurred.

### Coordinator Source Integration

On 2026-10-11 the coordinator reconciled worker head
`d32ef6354190181753816bf09215f397ed0122f1` with clean local main
`6f230c56eb97c3cd587d636ba6492b24de13e53d`. Merge
`1dfd203dc41bf49d0669db855143f72304bc43b6` preserves all six worker logical
commits and the existing P06 issuance. Common integration commit
`962e11be50260a3dce2e2700b22951fce1b3f4f7` changes exactly ten shared paths:
workflow contract, script manifest, SMTP helper, generator, three README indexes,
two existing generator/metadata regressions and the new inherited-lock test.
The eight previously committed P02-owned paths remain intact. No source file
was deleted. This current receipt supersedes earlier shared-registration-pending
statements only for the locally integrated SOURCE/UNIT/STATIC slice; historical
measurements and operational exclusions remain valid.

The CLI manifest consumer is the existing test that actually invokes it,
`tests/lib/ops/test_secret_catalog.py`. RUN-0085 remains its authority. The
unapplied P01 runbook proposal is not declared an active invocation consumer. P01 alone
reconciles its four OpenBao documents with the fixed public proposal
`p02-openbao-docs.patch`, SHA256
`71907ca6135cee7ad60df3868b92214967ef19822cf17b715810b3bb7419b7f4`.
After that prose contains the actual CLI invocation, the coordinator can add
it as a proven consumer. P03 must regenerate its manifest/workflow proposal
against this integrated base and retain both registration sets.

The old *proposed* Python lock wrapper, rather than the prior main generator,
failed the parent-death RED test: exit 1, one failure. The new wrapper passes the
same held file description to the child. It preserves the default helper API
and cooperative lock boundaries; CLN and nonparticipating writers still require
separate quiescence. COMM-002 canonical and COMM-003 alias generation remains
blocked; SMTP01 retains sole ownership of actual COMM-003 retirement.

Coordinator checks used `/tmp/hy-home-p09-qa/bin/python` with its directory first
in PATH for child interpreters. The source candidate began at `1dfd203d` plus
the exact shared diff; final functional input is commit `962e11be`. Actual
commands and fixed file hashes are retained in the ignored, value-free
`.agent-work/p02-coordinator-integration.json` receipt:

- Initial combined catalog, SMTP, metadata, retirement and runtime-compatibility
  `-m unittest` selection: 195 PASS, 34.349 seconds, exit 0.
- Final generator/metadata/inherited-lock selection after ShellCheck correction:
  39 PASS, 24.573 seconds, exit 0. The synthetic generator harness bound to the
  actual final generator: 13 PASS, 13.211 seconds, exit 0.
- `check-script-manifest.py --check-generated`,
  `check-github-workflow-contract.py`, `bash -n scripts/operations/gen-secrets.sh`,
  Ruff `check` and `format --check`, diff checks and registered
  `run-ci-precommit.sh --mode local-staged`: PASS, exit 0.
- Public CLI `check`, `render` and `check-views`: 145 entries, one alias,
  four ignored staging views matching the catalog, exit 0. No private metadata
  or credential input is read by these commands.
- `check-document-links.py --mode all`: 1,195 documents, 11,607 links,
  failures 0, exit 0; one pre-existing historical archive warning.

Failures were kept as failures: the initial manifest referenced unapplied P01
prose, two proposal test imports/formatting failed Ruff, and the staged gate
reported ShellCheck SC2066 for a single-item environment-file loop. Registration
now references the real CLI test, formatting is corrected and the unchanged
root-only parser reads the quoted root environment file directly. A retry
without the QA child PATH failed 14 of 39 tests; the fixed PATH run passed all
39. Initial public rendering was blocked by a missing ignored parent README;
the coordinator prepared that public README and render/check then passed.
Final generator SHA256 is
`1aeadbb428dc7efbd6f38b36720a8a485baae42e4b29383590aa231f7385bee5`;
the earlier proposal generator hash is a historical input only. Independent
code and security reviews accepted the exact combined source and this final
loop correction without remaining Critical/Important or P1/P2 findings.

The registered default changed profile contains all 17 local SOURCE leaves
once among its 33 invocations. A read-only plan comparison confirmed identical
IDs, arguments, environment boundaries and timeouts. Full plan SHA256 is
`712364150d828e205a778920f9e2cdb9baae2caf008d5c4f9158a9b3858e6700`.
The redundant standalone local-only run was interrupted with exit 130, rather
than labelled PASS. The first default aggregate failed with exit 1: two public
checkout entrypoints had mode 0775 despite Git mode 100755. After verifying
regular files, owner, single link and unchanged content, the coordinator
restricted those two checkout files to 0755. Their 19 focused tests passed,
exit 0. This metadata correction did not change production files or Git bytes.

The existing executor then ran the exact registered suffix at index 18 with
all original arguments, optional-runtime skips, environment limits and timeouts.
Its first 14 leaves passed, including 525 Compose tests with 69 skips; the last
integrity leaf failed, exit 1, with three failures among 365 tests. The test-owned
mutation expectations omitted the three new catalog writers. Commit
`b13e379efe954270e1f76458a74d1b0d93f39459` adds only those exact `check-write`
expectations, preserving the default `none` and equality assertion. Focused
Manifest regressions then passed: 48 tests, 12.183 seconds, exit 0.

During verification, both local and remote main advanced to accepted P01 source
`6d1d6960e59c316fad2c6d168d853989da565faa`. Pure merge
`ab346b2c9a329731af3fff74be651531d87067cc` preserves its ten P01 paths byte for
byte. The final diff against that main contains exactly 19 P02 paths, including
the separate mutation-expectation correction; all six worker commits remain
ancestors. The regenerated 33-invocation plan is identical to the frozen plan.
On this merged SOURCE input, the existing executor reran the exact registered
Compose baseline, diff hygiene and repository integrity leaves: exit 0.
Compose ran 544 tests in 128.949 seconds with 71 optional-native skips and no
failure; integrity ran 365 tests in 82.085 seconds with no failure. Independent
code and security reviews accepted this merged SOURCE with no remaining findings.
The original aggregate and first suffix remain FAIL records. Acceptance uses
their unchanged successful leaves plus these corrected, affected-leaf receipts;
it does not relabel either aggregate or claim fresh hosted CI/native acceptance.

The result-only record initially introduced a disallowed H2; the coordinator
moved it under the existing Work Log and selected metadata passed with one
selected document and zero violations, exit 0. The finalized merged-tree metadata,
links and lifecycle checks and exact staged Task gate must pass before the receipt
commit and local main fast-forward. Their exact Task hash, commands and actual
exit codes are retained in the coordinator receipt.

Fresh `git ls-remote --heads origin main` observed
`6d1d6960e59c316fad2c6d168d853989da565faa`, exit 0. GitHub readback confirmed
P01 PR #421 merged with candidate-quality SUCCESS on head
`d3ae5587d7e3376bed22bbef82badf3875d8fb95`; its PR main-security job was SKIPPED.
That source delivery does not accept P02 prose or actual HOME recovery. P01's
four current document blobs differ from the preserved proposal bases, so P01
must reconcile the proposal against this accepted main; the coordinator has not
applied it. P05/P06 issuance is already in the current remote baseline and is
absent from the 19-path P02 diff. No remote P02 push, PR, latest-head hosted CI
or merge occurred. P01 document acceptance, future latest-head CI and independent
review remain delivery prerequisites. Keep this Task in progress.

HOME, MIGRATION, ROTATION, RECOVERY, native SMTP and private generator execution
remain NOT_RUN. No production credential, database, application service, LAB
runtime or secret file was created, changed or deleted. ISOLATED includes
synthetic temporary fixtures and ephemeral Conftest policy-tool containers,
whose name-scoped readback found zero remaining containers, exit 0. These tools
are not application deployment or recovery evidence. Existing foreign dirty
checkout drafts were preserved.
P01/P03/P06/P08/P10 receive schema version 1.0.0, the 145 issued entries and
COMM-003-to-COMM-002 alias, regeneration/retirement exclusions and this source
commit. P06 can use the integrated guard API for source/synthetic binding work;
actual pilot still needs issued consumer IDs/destinations/ACL/delivery from the
catalog and P01/P03/P04 operational acceptance. The closed catalog is not
permission to invent opsflow entries or issue credentials.

### Current Public-Source Reconciliation — 2026-10-13

The current user authorizes P02 reconciliation, scoped logical commit and its
owning-Spec PR/merge after current checks and independent review. This receipt
supersedes historical pending-source statements only where fresh evidence below
supports it. It preserves issued identities, dates, lifecycle and prior receipts.
Criterion 16 / W32 remains owned by SPEC-0204-TSK-0010; P06 / TSK-0014 owns real
copy and delivery. Completed Tasks are not rewritten.

`git fetch origin main` returned exit 0. Both current HEAD and fetched
`origin/main` were `62556dc63b66c828c27e9c33017d26cdf70b8542`; the supplied
investigation SHA was `23e37362b72e98028a4675f282819c0346ae59dc`.
`git status --short` was empty. `git worktree list --porcelain` and individual
`git -C <worktree> status --short` inspected the existing worktrees; all inspected
statuses were empty and no foreign index or checkout was modified. GitHub
`gh pr list --repo buenhyden/hy-home.docker --state open` returned an empty list,
exit 0. The sole current writer uses `codex/p02-current-reconciliation` in
`.worktrees/p02-current-reconciliation`, created from that fetched main.

| Source / consumer | Acceptance owner and classification | Target and recovery boundary |
| --- | --- | --- |
| Catalog/schema, public example/support, CLI and generator | TSK-0010 criterion 16/W32; SOURCE_APPLIED / NO_CHANGE; byte-identical to the investigation SHA | Fixed tracked public inputs; preserve existing source and generation contracts |
| View I/O/library and focused unit tests | TSK-0010 criterion 16/W32; CONFIRMED_GAP | Existing `check-views` accepted mode 0644; enforce exact 0600 for generated targets and preserve the parent README compatibility |
| Current 0085 guide/policy/runbook and OpenBao README | P01/TSK-0006; SOURCE_APPLIED / NO_CHANGE | Existing Korean catalog instructions are applied; preserve that sole writer; Stage05 paths moved under `04-security-and-secrets` since the investigation SHA |
| Current Task | TSK-0010; CONFIRMED_GAP in current-SHA evidence and explicit handoff | Add only this receipt; revert this logical documentation commit to restore prior text |
| Consumer metadata and proposed destinations | P01/P03/P06; CONSUMER_DEPENDENT / RUNTIME_UNVERIFIED | Source declarations do not establish actual UID, ACL, reload, custody or RTO; no KV provisioning |
| COMM-002 / COMM-003 | SMTP01; SOURCE_APPLIED / NO_CHANGE | One canonical source and one value-free source-retired alias; actual old-file deletion is NOT_RUN in this execution |
| PG-020, stable crypto, bootstrap and recovery materials | P01/P06/CLN01; SOURCE_APPLIED / NO_CHANGE | Retain independent/consumer-owned custody and history; no automatic reissue or deletion |
| LAB runtime, learning apps, actual Wiki, image/scanner edits | OUT_OF_SCOPE | LAB metadata classification only; no current-image warning investigated or asserted here |

Catalog schema version is `1.0.0`; fresh public validation reports 145 entries
and one alias. Observed classifications are 66 kv_static, 10 stable_crypto,
9 bootstrap_external, 23 public_configuration, 3 derived_runtime and
34 lab_excluded; unused_delete has no current row. These counts are observations,
not new inventory invariants. UNKNOWN_BLOCKED/BLOCKED_FACTS remains a fail-closed
contract, not proof of consumer absence. `source_recorded_at` remains the first
public source date, not a current observation or rotation date.

#### Value-Free P06 Handoff

The existing catalog and P01 renderer name the following source identities.
The renderer paths below are already declared source, not new approved catalog
destinations or evidence of successful delivery. The catalog retains its blocked
proposals pending exact consumer authorization, failure and recovery facts.
All catalog mount/field/UID/GID/mode bindings remain null; ACL, delivery,
reload/restart and rotation remain BLOCKED_P01. No second mapping authority or
catalog copy is created.

| ID | Catalog proposed KV / existing renderer source | Consumer role / file target | Rotation / recovery / blocked facts |
| --- | --- | --- | --- |
| IAM-002 | `secret/planned/root/iam-002`; existing `secret/data/hy-home/02-auth/keycloak` | Keycloak admin; renderer `/openbao/out/auth/keycloak_admin_password.txt`; declared consumer `infra/02-auth/keycloak/docker-compose.yml` | P01 renderer reads `admin_password` with 0600 output; actual delivery, consumer UID, restart, custody and RTO unresolved; history retained |
| OBS-002 | `secret/planned/root/obs-002`; existing `secret/data/hy-home/06-observability/grafana` | Grafana admin; renderer `/openbao/out/observability/grafana_admin_password.txt`; declared consumer `infra/06-observability/docker-compose.yml` | Same P01/P06 boundaries; read-only renderer ACL covers only the two declared data and corresponding metadata paths |
| COMM-002 | `secret/planned/root/comm-002`; no renderer binding | ROOT observability source consumer; `secrets/communication/smtp/smtp_password.txt`; LAB declaration is metadata only | Generation guard refuses canonical SMTP; destination/rotation/recovery remain unaccepted; no SMTP delivery operation |
| COMM-003 | Alias to COMM-002; no KV destination or generator | No independent consumer/value/file target approved by P02 | Source tombstone does not prove private old-file deletion; SMTP01 owns that operation |
| PG-020 | No KV destination | Retained recovery reference; no inferred live consumer | NO_CHANGE / RETAINED_FOR_RECOVERY; custody UNKNOWN; no reissue/delete |

P06 consumes the catalog's existing issued IDs through the integrated validation
API. Neither a planned path nor renderer source authorizes copying a value.
The next actual approval must name the selected ID, HOME target/consumer,
KV mount/path/key, actor/ACL, delivery target and UID/mode, restart/rotation,
independent recovery materials and rollback before the dependent lane runs.

#### Fresh Verification Inputs and Outcomes

The initial checks below bind to clean source `62556dc63` in the worker worktree.
The first system-Python run of the three requested modules ran 90 tests and
failed with 15 failures and 10 errors, exit 1, including missing `referencing`.
That environment failure is retained, not reclassified as PASS. Historical
`/tmp/hy-home-p09-qa` is absent on this host; `python3 -m venv` also failed
because ensurepip is absent. The current writer used uv to create its own
`/tmp/p02-current-qa` and install the unchanged registered
`scripts/requirements.txt` and `scripts/requirements-pre-commit.txt`, plus
coverage. No system Python, repository dependency contract or private config
was changed. Some initial commands did not start because the sandbox reported
a namespace error; scoped native escalation allowed the recorded retries.

With `/tmp/p02-current-qa/bin` first in PATH for synthetic child interpreters:

- `python -m unittest tests.lib.ops.test_secret_catalog tests.validation.test_secret_catalog_contract tests.validation.test_secret_metadata_sync -q`:
  90 PASS, 65.321 seconds, exit 0.
- `python -m unittest tests.validation.test_smtp_generator tests.validation.test_smtp_lock_inheritance -q`:
  18 PASS, 3.184 seconds, exit 0; all private inputs are synthetic.
- `python scripts/operations/secret-catalog.py --root <worker-root> check`:
  P02_METADATA_VALID, 145 entries / one alias, exit 0.

Independent security inspection reproduced one source gap: after chmod 0644,
`check_views` returned true on the original source. New synthetic tests
`SyntheticRepositoryTests.test_generated_views_require_exact_private_mode`
and `test_generated_views_are_private_under_restrictive_umask` first failed
with missing refusal and mode 000 instead of 0600, exit 1. The same focused
command passed two tests after the minimum fix, exit 0. Every generated target
now requires exact 0600 in render and check; the opened temporary inode receives
fchmod inside its managed stream before writing. The ordinary parent README
retains compatibility. No new dependency, CLI option or source mapping is added.

Final functional source is commit
`8e46188bd665292abd7d2ecb22ca9df3f189a2d1`, exactly three files, +36/-4:
`_secret_catalog_io.py`, `secret_catalog.py` and `test_secret_catalog.py`.
Both independent code and security reviewers approved those exact bytes with
no remaining findings; independent unit review passed 35 tests, and the security
reviewer independently passed the two permission regressions, exit 0.
Public catalog/schema/support/example blobs remain unchanged from the baseline.

On that exact source candidate, with the same QA environment:

- `python -m coverage run --branch --include='*/scripts/lib/ops/*secret_catalog*.py' --data-file=/tmp/p02-final.coverage -m unittest tests.lib.ops.test_secret_catalog tests.validation.test_secret_catalog_contract tests.validation.test_secret_metadata_sync tests.validation.test_smtp_generator tests.validation.test_smtp_lock_inheritance tests.lib.ops.test_openbao_consumer_migration.PublicCatalogBindingTests -q`:
  116 PASS, 108.720 seconds, exit 0. P06's six public-binding checks are synthetic,
  not KV import or delivery.
- `python -m coverage report --data-file=/tmp/p02-final.coverage --fail-under=80`:
  total 90% branch-aware coverage, exit 0.
- Public CLI `render` / `check-views`: STAGING_RENDERED / P02_VIEWS_MATCH,
  exit 0; all four newly rendered staging files were observed at 0600.
- Ruff check and format check on the three source/test files, `git diff --check`,
  Commitizen message check and
  `bash scripts/validation/run-ci-precommit.sh --mode local-staged` on the exact
  three-file index: PASS, exit 0; unmatched file-type hooks were explicitly SKIP.
- `docker compose --env-file .env.example config --no-env-resolution --no-interpolate --quiet`:
  static render PASS, exit 0; no dotenv/secret payload or daemon mutation.
- Initial Task selected metadata: one selected / zero violations, exit 0.
  `check-document-links.py --mode all`: 1,272 documents / 11,440 links,
  failures 0, exit 0; one existing historical-capture warning is retained.

The source-only commit passed the staged gate and preserves its recovery object.
The current Task receipt is a separate documentation unit. Remote main protection
read-back has zero required status contexts and zero required approvals, with
CODEOWNERS review unenforced and no rulesets. This is a point-in-time observation;
the request still requires actual candidate-quality success and independent review
before the P02 PR merges, without bypass or protection changes. Remote delivery
is pending at receipt authoring and must be reported from actual PR read-back.

Final `python scripts/validation/run-ci-gate.py --profile changed --local-only`
passed, exit 0, on `8e46188b` plus this result-only Task receipt. Its selected
leaves were local-candidate-preflight, docs-traceability and
repository-integrity-regressions; the last ran 559 tests in 149.379 seconds,
all PASS. Final selected Task metadata again returned selected=1 / violations=0,
exit 0. This last result-only addition introduces no link or lifecycle change;
its independent delta review, diff hygiene and exact staged documentation gate
precede the documentation commit. Hosted CI and merge remain separate receipts.

HOME, KV IMPORT/CONSUMPTION, MIGRATION, ROTATION and RECOVERY are NOT_RUN.
This run never opens private dotenv/table/auth inputs, real secret files, raw
logs or application data. `secrets/` and unknown local rows are preserved.
Source rollback uses `git revert 8e46188bd665292abd7d2ecb22ca9df3f189a2d1`
for the permission fix, and reverts the separate documentation commit for this
receipt. The code revert restores the known 0600 validation gap; neither action
rolls back a data format, credential rotation or deployed service. The Task stays in progress while
its separately owned operational dependencies remain unresolved.

### Single-owner draft for the public contract — 2026-10-21

v22 §10 asks for one owner of generation, reference and validation. Today three
statements name different owners:

| Statement | Location | Claims |
| --- | --- | --- |
| Guide concepts | GDE-0010 `## Concepts` | `SENSITIVE_ENV_VARS.md.example` owns the public ID, env key, path and purpose contract |
| Guide related link | GDE-0010 `## Related Documents` | `scripts/operations/gen-secrets.sh` is the metadata synchronization owner |
| Catalog | `infra/03-security/openbao/secret-catalog.json` `metadata_source`; `scripts/lib/ops/secret_catalog.py` `VIEW_NAMES`; `tests/validation/test_secret_catalog_contract.py` | The catalog renders `.example` and the value-free views, and the test pins the rendered `.example` to the tracked file |

The test makes the catalog the effective source: an edit to `.example` alone
fails it. The only writers of the private `secrets/SENSITIVE_ENV_VARS.md` are
`gen-secrets.sh` (it reads `.example` as `EXAMPLE_FILE`) and
`scripts/lib/ops/smtp_contract.py`.

Draft for the owner, not applied: the catalog is the single source;
`.example` is a rendered public view; `secret_catalog.py check-views` is the
validation; `gen-secrets.sh` and `smtp_contract.py` are the only writers of the
private file and consume `.example` as a view. GDE-0010 `## Concepts` and its
related link would then say so, and `metadata_source` would stop pointing at the
view.

Retention classes for `secrets/` subtrees, from directory names only (no file
opened, no value read):

| Class | Subtrees | Disposal |
| --- | --- | --- |
| Rendered or generated | private `SENSITIVE_ENV_VARS.md`; generated credentials under `auth/`, `db/`, `data/`, `communication/`, `observability/`, `automation/`, `storage/`, `tools/` | Regenerate from the catalog and the generator; never hand-edit |
| Bootstrap or independent custody | `security/`, `certs/` | Keep; retire only through the OpenBao/CLN01 retirement records |
| Recovery | `backup/` | Keep while the backup chain references it |
| Historical | `.backup-20261002-prompt02`, `.backup-20261003`, `.backup-20261003-layout`, `.retired` | Owner review, then CLN01 disposal; none is read here |
| Excluded | `labs/` | LAB scope, not assessed |

Which owner to choose, and any move or deletion, is the owner's decision. S10b
status: PARTIAL, draft recorded.

Owner decision — 2026-10-21 ("S10b secret 단일 owner 검토후 진행"): the draft's
single owner is adopted. GDE-0010 now names `secret-catalog.json` as the one
source, `.example` as its rendered public view, the catalog check plus
`test_secret_catalog_contract.py` as validation, and `gen-secrets.sh` and
`smtp_contract.py` as the only writers of the private registry. The catalog's
`metadata_source` field stays as it is (the code pins it, and renaming it would
change the schema); GDE-0010 says it records where the catalog was first
migrated from. Checks on 2026-10-21: the contract module passes in a Python
with jsonschema (the host `python3` lacks `referencing`, so it errors there);
`secret-catalog.py --root <absolute path> check` reports 145 entries and 1
alias, and a relative `--root .` returns `P02_METADATA_BLOCKED`. No other
operations, requirements, architecture or `.agents` document claims `.example`
as the owner; `secrets/README.md` was not read. The retention classes stay a
draft, and no file under `secrets/` was moved or deleted. S10b status: PARTIAL,
ownership decided; retention classes and P06 consumption remain.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Issuance baseline | 16, 8 | W32 | Task/criterion/work-unit availability probe | 2b9f5ec82 | FAIL | Coordinator private issuance RED receipt; no values | - |
| Issuance source contract | 16, 8 | W32 | Availability GREEN and selected metadata after dependency/status correction | 2b9f5ec82 plus three issuance documents | PASS | Coordinator GREEN and metadata retry receipts; exit 0 | Issuance baseline |
| P02 source implementation | 16 | W32 | Catalog, closed schema, four staging views and source consumer regression | 74feff942 plus owned changes | PASS | Tooling d82f6fc82 and catalog 1148592d8; 40 scoped tests and coverage 91%, exit 0; shared integration pending | - |
| Private migration and consumption | 16 | W32 | Selected P06 runtime contract and actual receipt | Final P01/SEC01 contract pending | NOT_RUN | P06 owner | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 16 | pending | - | - |

## Review and Completion

Before each unit, record actual input SHA and a meaningful RED/GREEN test.
Cover malformed IDs/fields/paths, sensitive-field rejection, canonical and
alias uniqueness/cycles, SMTP one-source behavior, migrated/retired reissuance
refusal, crypto/recovery retention, staging-only output and private/env
noninterference. Do not equate schema fields or mock KV equality with actual
security, migration or recovery evidence. Scan free text and outputs for secret
leaks and independently review the generator/custody boundaries.

Run focused unit and contract tests, Ruff, schema/view drift and existing secret
metadata/support/SMTP/retirement regressions affected by the proposal. Run
metadata/links/lifecycle for changed documents, exact changed/staged registered
checks, and independent security/code/document review at the final head.
Preserve logical catalog/schema, tooling/guards, and documentation commits.
The coordinator integrates common proposals once and reruns affected checks.
Preserve those logical commits in one SPEC-0204 P02 PR, compare its diff against
fresh remote main, require actual latest-head CI and independent review, and
merge without admin bypass. Then fast-forward local main and remove only the
merged clean worker branch/worktree after preserving its evidence. If the
current remote baseline changes, rebase/reconcile and rerun affected gates
before delivery. Never include unrelated preceding integration or SEC01 HOME
units in the P02 PR; dev is unused.

Hand P01/P03/P06/P08/P10 the catalog SHA/schema version, ID/alias mapping,
planned path/ACL/delivery/reload/recovery graph, blocked consumers, exact test
receipts and final local main SHA. Report SOURCE/UNIT/STATIC/ISOLATED/HOME/
MIGRATION/ROTATION/RECOVERY/DELIVERY separately, with real commands and exits.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [SMTP01 contract](tsk-0005-cross-tier-contracts-second-round.md)
- [OpenBao trust and recovery](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [CLN01 retirement](tsk-0007-cln01-material-retirement.md)
- [P09 preparation](tsk-0008-llm-wiki-preparation.md)
- [SEC01 continuation](tsk-0009-sec01-stable-security-integration.md)
- [OpenBao guide](../../../05.operations/guides/04-security-and-secrets/0085-openbao.md)
- [OpenBao policy](../../../05.operations/policies/04-security-and-secrets/0085-openbao.md)
- [OpenBao runbook](../../../05.operations/runbooks/04-security-and-secrets/0085-openbao.md)
