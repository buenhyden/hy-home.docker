---
title: "Runtime Compatibility and Security Task"
version: "0.1.4"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0001"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Runtime Compatibility and Security Task

## Objective

After owner approval, correct the confirmed n8n compatibility and secret
consumer defects, check Crawl4AI's security pin, and separate OpenBao sealed
status from readiness. Verify Cassandra LAB's already changed official-image
contract without moving data or creating LAB credentials again.

## Inputs

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7` on 2026-10-03;
SPEC-0201 W5, SPEC-0204 criteria 1-4/8 and Plan W1/W2/W5. The user-supplied
Prompt 04 requests source implementation but requires an approved Task. This
Task is an approval draft: no source edits, image pull, HOME deployment or
credential action has been authorized by its existence.

## Work Log

| Service and source evidence | Proposed exact writer path and variable/consumer | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| n8n main/worker use one older build pin while both runners use a newer image; official n8n documentation requires matching versions. Proposed target is the 2026-10-02 stable `2.41.6`, subject to a fresh release/digest/compatibility check | `infra/07-workflow/n8n/docker-compose.yml`, `Dockerfile`, `dev.Dockerfile`, `renovate.json5`; `N8N_VERSION`, four image declarations; main, worker and two runners | Same-version/render assertion, queue/manual/scheduled/webhook/Code smoke on synthetic metadata; revert version declarations before HOME rollout. A live DB upgrade needs metadata plus encryption-key backup and its own operation approval | Source Task approval; HOME start/restart separately |
| n8n instance has singular timeout key; runner image `_FILE` support is not documented | `infra/07-workflow/n8n/docker-compose.yml`, `docker-entrypoint.sh`, `docker-entrypoint.dev.sh`; `N8N_RUNNERS_TASK_TIMEOUT`, broker token reference `n8n_runner_auth_token`, selected `N8N_VALKEY_SECRET` file; n8n and both runners. A new runner wrapper is excluded until an exact Task amendment | Empty/mismatched file rejection, supported variable render, no secret in argv/log/layer or JS/Python Code-task environment, bounded worker restart; revert scoped wrapper/Compose | Secret **reference** edits in approved source scope; no token reading/rotation |
| Crawl4AI is pinned before the official `0.9.4` security fixes, is opt-in and has no confirmed consumer | `infra/08-ai/crawl4ai/docker-compose.yml`, `renovate.json5` only if matching update rule, existing `docs/05.operations/{guides,policies,runbooks}/0091-crawl4ai.md`; URL/redirect/robots/link preview input | Official advisory and image digest/architecture review, synthetic DNS/redirect/private-destination denial, preserve separate bridge and verify real egress enforcement separately; revert image pin if behavior differs | No new consumer network, HOME activation or crawler payload collection |
| OpenBao health accepts sealed status as healthy | `infra/03-security/openbao/docker-compose.yml`, existing `docs/05.operations/{guides,policies,runbooks}/0085-openbao.md`; `bao status` result | Synthetic sealed/unsealed/Agent-template-current probes and dependency render; revert health semantics if dependency contract fails | No unseal, credential rotation or HOME restart |
| Cassandra official image move already lives in LAB | `labs/cassandra.yml`, `labs/cassandra.md`, existing GDE/POL/RUN-0025 read-only unless a confirmed defect appears; `/var/lib/cassandra` | LAB render, data/auth/UID limits recorded; no duplicate migration or fabricated auth | No old Bitnami data move, LAB up or secret issue |

Version projection `infra/tech-stack.versions.json` is generated from source;
run `bash scripts/operations/sync-tech-stack-versions.sh --check` and the
registered write route only when a declaration changes. Update Korean
`infra/07-workflow/n8n/README.md` and current Stage 05 n8n documents if their
consumer instructions change. Proposed focused regression owner is a single
new `tests/validation/test_service_runtime_compatibility.py` unless an existing
contract test already covers each changed invariant.

Official source evidence checked on 2026-10-03:
[n8n task runners](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners/),
[n8n queue mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode/),
[n8n runner environment](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/task-runners/),
[n8n releases](https://github.com/n8n-io/n8n/releases), and
[Crawl4AI security advisories](https://github.com/unclecode/crawl4ai/security),
and [OpenBao status exit codes](https://openbao.org/docs/commands/status/).
Recheck exact stable image, digest and compatibility at implementation time;
none of these links is a tested HOME deployment.

## Verification Evidence

### Protected registration repair — 2026-10-04

### Hosted fixture validation and document formatting — 2026-10-04

PR352 head `042b9db6d6e86025fc94af8105a18c63440ba071`, required
run `37154950211`, job `111296335212`, finished failure/exit1. Hosted
metadata selected2/violations0/legacy0/overrides0; corpus and archive recovery
violations0. The existing Storybook fixture test passed, retaining all five
negative mutations. The later pinned markdownlint-cli2 hook modified files
and stopped the required job; no later leaf is claimed PASS.

The exact approved Task1 document contained two redundant blank lines.
Direct invocation of cached, pinned markdownlint-cli2 0.22.1 on this one
approved document removed only those two blank lines and returned exit0.
This formatter reconciliation changes no source, fixture assertions,
threshold, workflow, lifecycle edge or frozen archive. Recheck formatting
idempotence, metadata and exact diff before the normal hosted retry. The
fixture implementation itself needs no second correction. Runtime holds
remain unchanged. Raw CI output was not copied into this record; an automatic
approval rejection of raw log printing was honored with bounded diagnostic
extraction of checker results and hook identity.

### Additional fixture scope proposal — 2026-10-04

PR352 head `b240f6150` hosted run `37154044478` returned failure, but
metadata selected2/violations0/overrides0 and links/corpus/recovery passed.
The five failures are the existing Storybook shell regression's baseline
fixture: main0460795's checker also reads `.storybook/main.ts` and the private
UI `package.json`, while the test copied only package.json/vitest.config.ts.
No initial-state finding remains in this registration candidate.

Proposed additional writer is only
`tests/lib/gate/test_github_workflow_contract.py`'s existing Storybook fixture
copy loop: add those two tracked configuration files and create their parent
directories before copying. Preserve all five mutation assertions, thresholds,
checker code, workflow routing and required protection. Exact proposed patch
is staged outside the repository as `/tmp/hyhome-storybook-fixture-proposed.patch`;
the tracked test was unchanged during scope review.
Existing targeted unittest reproduced RED exit1/five failed subcases. Loading
the proposed test source from scratch with the original repository ROOT
returned GREEN exit0/one test covering all five subcases. An initial scratch
loader exited1 because its temporary file depth could not resolve ROOT;
keeping the real repository `__file__` fixes the loader without altering the
proposed test or its assertions. The exact targeted regression and normal
hosted checks must run after approved application. Independent read-only
patch review returned PASS: only fixture completeness changes, all original
negative assertions and checker semantics remain intact. The user approved the exact fixture minimum and Task1 record on 2026-10-04.
`git apply` of the reviewed patch exited0. The same targeted existing unittest
then passed exit0/one test with all five original mutation cases; Ruff check,
Ruff format --check and git diff --check each exited0. No checker or threshold
changed. The scope now includes that single fixture loop in
`tests/lib/gate/test_github_workflow_contract.py` in addition to this Task record.

The package's exact-file approval rule was satisfied by that explicit owner
response. Push the scoped fixture and record to PR352, observe the normal
hosted gate, then resume the reviewed document sequence only after green.
Rollback is a scoped revert of the fixture addition, which returns the known
missing-input failure; it is not a gate bypass or an operational rollback.

The user requested resolution of PR351's six initial-status findings after
explicitly authorizing push, PR merge and cleanup. Original implementation
and completed evidence remain on `codex/spec-0201-0205-closure` at
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`; no final body or frozen
archive is rewound by this document registration.

Initial preparation used `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`
and six original draft bodies (five from `0f67cb297`, Task4 from `d666b6f42`).
Local metadata selected7/violations0/overrides0, links failures0 with one
pre-existing historical warning, and corpus/recovery violations0, each exit0;
independent review approved. The first counter relationship check failed
before correcting high_water and next_number together. Draft commit
`86f65973a6a762952e004994fb5e860d2b7dca8c` remains recoverable.

Authenticated PR readback then exposed concurrent protected main
`0460795abf6da9203e38f30291a8f20118c6ab88` from PR350, which already
registers Spec, Plan and Tasks1-3 as draft. No obsolete registration was
merged. The registration branch merges this latest main and preserves its
Storybook changes, navigation and SPEC high-water206/next207 exactly.
PR352 now adds only the missing original Task4 draft and this Task1 receipt.
Independent review approved the narrowed two-document diff; README and Registry
match the new main exactly. A check before finishing the main merge exited2:
allocation predecessor 0460795 did not yet precede branch HEAD. The normal
merge commit establishes that ancestry; validation must rerun afterward.
After normal main merge `21bf46fdd`, changed metadata against origin/main
0460795 selected2/violations0/overrides0, exit0. Refreshed links mode all
returned failures0/one pre-existing historical warning, exit0; corpus and
archive recovery returned violations0, exit0. `git diff --cached --check`
passed and independent review approved the exact two-document diff.
Registration document scope covers these two package documents; the approved
fixture-loop extension is recorded above. Final independent review approved
this exact three-file PR diff with zero standards/spec findings; normal hosted
checks still decide merge readiness. No runtime,
private values, validator, lifecycle registry rule or transition override changes.

Use three preliminary docs-only protected merges: finish Task4 draft
registration; Spec draft→review, Plan draft→approved and all Tasks draft→ready;
then Spec review→approved, Plan approved→active and Tasks ready→in-progress.
Merge that main into the closure branch without rewriting recovery objects.
PR351 then supplies the fourth edge and final reviewed bodies: Spec active,
Task1 blocked, Tasks2-4 completed, Plan stays active. Every merge requires
normal green protection. PR351's independent security hold remains unchanged;
this registration does not approve HOME, image pulls or service execution.
Rollback is a scoped PR revert with original sources preserved, never archive
rewriting or cancellation of already-completed work.

| Check | Result | Limit |
| --- | --- | --- |
| Current tracked-source and official-doc comparison | READ_ONLY | n8n version/timeout mismatch and Crawl4AI later advisory confirmed; no image execution |
| Draft package: `check-document-metadata.py --mode check-changed --base-ref main` | PASS (exit 0, selected 6, violations 0) | Documents only; no service validation |
| Draft package: `check-document-links.py --mode all` | PASS (exit 0, failures 0) | One pre-existing archive provenance warning |
| Draft package: `check-document-corpus-lifecycle.py --base-ref main`; registry JSON parse; `git diff --cached --check` | PASS (each exit 0) | Draft lifecycle and syntax only |
| Scoped Compose, secret consumer, URL allow/deny, OpenBao and LAB checks | NOT_RUN | Await approved source diff and synthetic fixture preflight |
| HOME n8n DB upgrade, crawler request, OpenBao unseal or service restart | NOT_RUN | Separate exact operational approval required |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1/W5 | DRAFT ledger; no source change | This Task and existing service READMEs |
| 2 | W2/W5 | NOT_RUN | GDE/POL/RUN-0053 and n8n source |
| 3 | W2/W5 | NOT_RUN | GDE/POL/RUN-0091 and LAB Cassandra documents |
| 4 | W2/W5 | PARTIAL design; auth routes belong also to TSK-0002 | GDE/POL/RUN-0085 and POL-0079 |
| 8 | W5 | NOT_RUN | This Task verification receipts |

## Review Evidence

Independent source/security review is pending the approved implementation diff.
No generated projection or runtime condition is marked PASS from this draft.

## Commit Ledger

No Prompt 04 commit. Baseline only: `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.

## Rulings

Do not shrink main runners without path evidence. Do not use a generic `_FILE`
assumption for `n8nio/runners`; verify its entrypoint first. If the pinned
runner lacks a safe supported file-consumption path, stop and amend this Task
with the exact wrapper/Dockerfile path before writing one. Existing LAB
Cassandra work is a verification item, not a repeat implementation.

## Deferred Items

Task source approval, image/digest acceptance, synthetic container preflight,
HOME version upgrade, management DB/encryption-key backup, real credential
handling and all service operations remain separate.
