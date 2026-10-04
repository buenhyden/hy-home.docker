---
title: "Runtime Compatibility and Security Task"
version: "1.0.2"
type: "sdlc/task"
status: "ready"
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

### Storybook blocker and alternative assessment — 2026-10-04

The user requested investigation and alternatives if no immediate fix exists,
then prioritized main integration and eligible package preservation. This is
read-only research recorded by this Task's protected-delivery owner; npm
implementation remains owned by SPEC-0205 and shared UI/MCP by SPEC-0206.
No package, lint configuration, audit threshold, workflow or archive body is
changed. The earlier braces hold is not withdrawn by a request to integrate.

At protected main `7f939ae802afc1d23f96b8eca4100abfcc2bf629`, the tracked
lockfile contains the dev-only path `eslint-config-next@16.3.8 →
@next/eslint-plugin-next@16.3.8 → fast-glob@3.3.1 → micromatch@4.0.8 →
braces@3.0.3`. Only micromatch directly declares braces in this lockfile.
The ESLint configuration imports both Next core-web-vitals and TypeScript
presets. Removing Storybook alone leaves that Next lint dependency in place.
This is a source-graph finding, not a claim that static assets expose braces.

Read-only official registry JSON queries exited 0 on 2026-10-04: stable
`storybook` is 10.6.1, `eslint-config-next` and `@next/eslint-plugin-next` are
16.3.8, and braces is 3.0.3. The latest Next plugin still declares fast-glob
3.3.1. The [official advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm)
reports affected braces through 3.0.3 with no patched release. Therefore a
supported stable upgrade that removes this path was not found. A handwritten
fork, package alias, lint-rule removal or production-only audit would require
new validation and would not satisfy the existing complete high/critical
check. None is applied or reported as an immediate solution.

| Candidate | Official functional basis and current registry tag | Replacement limits and security finding | Disposition |
| --- | --- | --- | --- |
| Keep Storybook | Existing 10.6.1 source, package exports, isolated static/browser receipts, revision manifests and local documentation MCP | Keep failed audit visible; wait for a patched braces release or upstream Next lint dependency replacement proven with the current rules | Preferred current architecture; merge remains blocked |
| Ladle | [React/Vite workshop](https://ladle.dev/docs/), [static build CLI](https://ladle.dev/docs/cli/) and [meta.json](https://ladle.dev/docs/meta/); @ladle/react latest 5.1.1, MIT, React peer >=18, Vite ^6.0.5 | Declares globby ^14.0.2; compatible globby14.1.0 declares fast-glob ^3.3.3, which declares micromatch ^4.0.8 and hence braces ^3.0.3. meta.json is not the current components/docs manifest contract. React19/Vite8, Next mocks, stories/addons, coverage and MCP need a separate consumer trial | First functional alternative to evaluate after product/contract approval; not a demonstrated audit fix |
| React Styleguidist | [React component documentation/playground](https://react-styleguidist.js.org/); latest13.1.4, MIT, React peer >=18 | Different Markdown/webpack contract; declares react-dev-utils ^12.0.0, whose compatible12.0.1 declares globby ^11.0.4; globby11.1.0 declares fast-glob ^3.2.9. Current story/MCP/test contracts require migration | Secondary documentation alternative; no security-clean graph claimed |
| Histoire | [Official Vite playground](https://histoire.dev/) lists Vue/Svelte; npm latest is1.0.0-beta.1, MIT | No official current React replacement was established; that beta directly declares micromatch ^4.0.8 and is not a stable candidate | Reject for this React workspace |

Candidate dependency paths are declared-range evidence from official registry
metadata, not installed lockfiles or complete security audits. No replacement
was installed, built, benchmarked or connected to HOME. Free self-hosting and
MIT upstream licenses do not grant a distribution license to the existing
private UNLICENSED UI package. Existing Traefik origin/auth/network contracts
would be preserved by an approved alternative; no second gateway is proposed.

Main integration must pass the required protected check before disposition.
PR353 run37162825263 and PR354 run37163965061 have failed required
validation-changed checks while the independent braces hold remains unresolved.
Sanitized `gh run view --log-failed` readbacks report the braces advisory and
five high findings; PR354 metadata selected6/violations0 and corpus/archive
recovery violations0. PR355 run37164906030 also failed, with metadata
selected1/violations0 and corpus/archive recovery violations0 before the same
five-high audit result. These observed failures are not converted into PASS.
PR352 is already merged; PR351 was closed without merge. Closed PR351's
recovery commit `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` preserves14
completed members for SPEC-0201/0202/0203/0205. Their frozen bodies are not
rewritten or presented as completed current-main packages. Once the security
hold clears, deliver the remaining registered protected lifecycle edges,
reconcile the divergent current SPEC-0205 through the existing immutable
handoff contract, integrate source, then prioritize those four whole-package
archives. SPEC-0182 recovery/offline custody, SPEC-0193 live resource/alert
acceptance, SPEC-0204 exact-image synthetic acceptance and SPEC-0206 HOME
TLS/OIDC remain separate uncompleted conditions; never archive individual
completed Tasks from their unfinished packages.

The inspected source inputs were only tracked JSON/ESLint/gate declarations
and public vendor metadata. Output is this assessment and a prioritized
handoff; no runtime, secret or data operation occurred. Rollback is a scoped
documentation revert preserving source recovery commits. Focused metadata `check-document-metadata.py --mode check-changed --base-ref
origin/main --changed-path` on this Task exited0, selected1/violations0/legacy0/
overrides0. Markdownlint-cli2 0.22.1 and `git diff --check` exited0. A Python
comparison proved only the dated research receipt and patch version changed,
exit0; the existing body, lifecycle and acceptance entries are preserved.
Independent review requested precise CI-failure evidence wording, corrected
above; final independent policy/document review returned PASS. Candidate install,
consumer/build/audit, HOME changes and data migration are NOT_RUN.

### OpenDesign assessment — 2026-10-04

The user's named candidate is assessed as [nexu-io/open-design](https://github.com/nexu-io/open-design),
not the separate opendesign.cc design-system catalog or similarly named forks.
Authenticated public-source readback exited0 at main revision
`53231d40b778d88eba23f35547bf99485d3ae9fc`; latest release is
`open-design-v0.24.1` while that source manifest declares0.23.1. These are
separate artifacts, not a verified runtime pin. Upstream Apache-2.0 permits
self-hosting; BYOK/provider or cloud usage is not thereby free, and imported
brand assets keep their own rights.

Official source describes design/prototype generation, design-system files,
export and Codex/Claude adapters. It is a Claude Design workflow candidate,
not a demonstrated replacement for existing Storybook component interaction,
accessibility/coverage, package consumer and revision-manifest acceptance.
The inspected [live-artifacts MCP source](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/apps/daemon/src/mcp-live-artifacts-server.ts)
exposes create/update/refresh as well as list and connector tools; this is not
the currently approved shared read-only documentation toolset. A supported
read-only subset with audience/reader authorization is not established here.

[Deployment documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/deploy/README.md)
explicitly distinguishes its single-tenant bearer token from per-user access
control. [Adapter documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/docs/agent-adapters.md)
uses non-interactive permission modes, including Claude bypassPermissions;
therefore a preview sandbox is not proof that the agent cannot write or run
code. [Privacy documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/PRIVACY.md)
describes product analytics enabled by default and separately configured
safety/reliability telemetry not disabled by the general toggle. Local-first
must not be reported as offline or zero outbound data.

Recommendation: keep Storybook's approved package/testing/docs contract;
evaluate OpenDesign only as a separate design-workflow companion using
approved UI tokens and synthetic screens in an isolated external workspace.
Before any trial, review exact release/dependency audit, model destinations,
telemetry configuration, file-write/command authority and the client config
changes. No installer, agent credential import, global MCP registration,
Docker service, model request, repo upload or HOME activation was performed.
Replacing the design tool does not remove the current Next ESLint/braces
path. Main integration and whole-package archival still require the earlier
protected prerequisites and terminal completion evidence; they are not
unblocked by this candidate research. This Task's focused metadata check
exited0, selected1/violations0/legacy0/overrides0; Markdownlint-cli2 0.22.1,
`git diff --check` and exact prior-body preservation comparison exited0.
Independent read-only source/policy review returned PASS. The preceding PR354
head `ed2600286e12d16349345f080244c6966321f273` run37165579521 failed:
metadata selected6/violations0 and corpus violations0, followed by five high
braces findings in sanitized diagnostics. This does not prove the new head's
hosted result. Actual candidate execution remains NOT_RUN.

### Protected review edge — 2026-10-04

Protected `origin/main` now contains PR352 at
`7f939ae802afc1d23f96b8eca4100abfcc2bf629`, registering all six draft
members. The preceding gate and hold receipts remain dated evidence; their
unmerged PR352 descriptions are historical. The owner closed PR351 without
merging its source. The latest owner request keeps braces on hold and asks
for the remaining Spec/Plan/Task work to proceed.

Existing Prompt 04 design/package/Plan/Task source approvals are carried
forward for this source-only lifecycle edge: Spec draft→review, Plan
draft→approved, Tasks1–4 draft→ready. Only these six package documents
change. No implementation completion, hosted gate waiver, source merge,
image pull, HOME action, secret operation or deployment is approved or
reported by this edge. Runtime checks remain NOT_RUN. A later source
integration must separately reconcile the closed PR351's preserved work;
this receipt does not reopen it or discard its recovery objects.

Local `check-document-metadata.py --mode check-changed --base-ref origin/main`
selected6/violations0/legacy0/overrides0 against the protected baseline above.
Cached installed markdownlint-cli2 0.22.1 and `git diff --check` returned exit0;
all six original bodies are preserved apart from this dated Task1 receipt.
The first formatter attempt used its cache source entrypoint and exited1 for
missing `globby`; the installed package entrypoint resolves that environment
issue without modifying tools or rules. Independent read-only review returned
PASS; hosted checks remain pending for this edge. Domain tests and container
execution are N/A for this edge.

The separate backlog PR353 head `7cfd890dbcd4b262a39ada1b45b5efc51ca332da`
ran hosted CI `37162825263`: metadata selected8/violations0, operations catalog
PASS and formatting hooks PASS, but the gate exited1 with five high findings
under `GHSA-vfj7-8cjw-p6xm`. The owner's braces hold remains; this document
edge adds no security exception and does not merge that PR.

### Protected registration repair — 2026-10-04

### Required gate result and existing security hold — 2026-10-04

PR352 head `0ef17a4a58d0d53f7249f3b0eef7939457e5cb72`, hosted
run `37158568358`, finished failure/exit1. Metadata selected2/violations0/
legacy0/overrides0; the approved fixture and both pinned formatters passed.
The later npm audit reported five high findings in the dependency graph,
including `GHSA-vfj7-8cjw-p6xm`. This is an independent security block,
not a recurrence of the missing fixture or document registration finding.

Authenticated GitHub advisory readback on 2026-10-04 confirms braces
`<= 3.0.3`, severity high, first_patched_version null; official source:
[GitHub Advisory Database](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
The owner previously chose to wait for a patch rather than grant a security
exception. That decision remains binding. No security exception, dependency
substitution, threshold reduction, manual workflow rerun or protected merge
is authorized by this receipt. No further hosted execution is dispatched.

The registration candidate's metadata has zero findings, but PR352 is not
merged. The original closure PR351 has not received the three protected
prerequisites and is not claimed repaired or merge-ready. The reviewed next
six-document edge remains uncommitted in its owned review worktree. Existing
source and recovery objects remain on their named branches; do not delete
those branches or dirty pending worktrees. Local main and origin/main were
last observed equal at `0460795abf6da9203e38f30291a8f20118c6ab88`.
Resume normal protected delivery only after the approved security hold clears.
HOME/isolated execution/data migration remain NOT_RUN for this repair.

### Pinned Python formatter scope amendment — 2026-10-04

PR352 head `a959826519c77402133bb197c7335747faa3e9bf`, required
run `37156755186`, finished failure/exit1. Metadata selected2/violations0/
legacy0/overrides0 and the markdownlint hook passed. The next ruff-format
hook modified one file and stopped the job; later leaves remain unverified.
Local Ruff 0.16.10 had accepted the approved fixture, but the CI hook pins
0.15.12. The pinned formatter accepts the approved fixture unchanged. Its
read-only check of 152 tracked Python files identifies only the existing
`tests/validation/test_compose_baseline_gates.py` from protected main PR350.

The four-hunk proposal changes only line wrapping, has identical Python AST,
and is idempotent under pinned Ruff 0.15.12. Independent read-only review
returned PASS on neutrality and required exact-path scope approval. The owner
explicitly approved those four formatting hunks and this Task1 record on
2026-10-04. The amended writer ledger adds only that one test file. Applying
pinned formatting modifies those same four hunks; no assertion, validation
condition, threshold, workflow or runtime behavior changes. Revert this
format-only commit for recovery, preserving all prior objects. Required
hosted CI must still pass before protected registration and later edges.

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
