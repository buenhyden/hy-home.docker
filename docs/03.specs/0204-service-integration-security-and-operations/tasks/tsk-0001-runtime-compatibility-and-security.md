---
title: "Runtime Compatibility and Security Task"
version: "0.1.6"
type: "sdlc/task"
status: "blocked"
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
Task source scope was approved by the user on 2026-10-03. Image pull, HOME
deployment and credential action remain separate.

## Work Log

| Service and source evidence | Proposed exact writer path and variable/consumer | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| n8n main/worker use one older build pin while both runners use a newer image; official n8n documentation requires matching versions. Proposed target is the 2026-10-02 stable `2.41.6`, subject to a fresh release/digest/compatibility check | `infra/07-workflow/n8n/docker-compose.yml`, `Dockerfile`, `dev.Dockerfile`, `renovate.json5`; `N8N_VERSION`, four image declarations; main, worker and two runners | Same-version/render assertion, queue/manual/scheduled/webhook/Code smoke on synthetic metadata; revert version declarations before HOME rollout. A live DB upgrade needs metadata plus encryption-key backup and its own operation approval | Task source approved 2026-10-03; HOME start/restart separately |
| n8n instance has singular timeout key; runner image `_FILE` support is explicitly absent | `infra/07-workflow/n8n/docker-compose.yml`, `docker-entrypoint.sh`, `docker-entrypoint.dev.sh`; `N8N_RUNNERS_TASK_TIMEOUT`, broker token reference `n8n_runner_auth_token`, selected `N8N_VALKEY_SECRET` file; n8n and both runners. Use only a bounded inline Compose launcher entrypoint in this existing file; no new runner image or wrapper file is authorized | Empty/mismatched file rejection, supported variable render, no secret in argv/log/layer or JS/Python Code-task environment, bounded worker restart; revert scoped wrapper/Compose | Secret **reference** edits in approved source scope; no token reading/rotation |
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

| Check | Result | Limit |
| --- | --- | --- |
| Official n8n runner/release, Crawl4AI security release, OpenBao status and amd64 image manifest inspection on 2026-10-03 | PASS read-only | n8n image index digests `sha256:87e0bab2c93192e8dd885ff7b0697c22a1bd97489568a8c67cc140fd7dbb342d` and `sha256:443eaee69319997627e2129ed8d512c4f4ea2418a744393cf26e843237399299`; Crawl4AI `sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b`. No image pull or execution. |
| `python3 -m unittest tests.validation.test_service_runtime_compatibility tests.validation.test_tech_stack_version_contract -q` | PASS, exit 0, 58 tests | Includes synthetic missing/empty/valid runner token and broker guard shell execution, plus sealed rc0/1/2; no Code-node process or image execution. |
| `docker compose --env-file .env.example --profile workflow-n8n config --quiet`; default/dedicated broker secret render; `--profile crawl4ai config --quiet` | PASS, each exit 0 | Only static root model; selected n8n main/worker receive one Valkey secret. |
| `LAB_DATA_DIR=/tmp/hyhome-lab-cassandra-synthetic docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile cassandra config --quiet` | PASS, exit 0 | Initial render without required `LAB_DATA_DIR` exited 1; corrected with a synthetic path. No LAB service or volume created. |
| `bash scripts/operations/sync-tech-stack-versions.sh --write` then `--check`; `git diff --check`; shell syntax | PASS, each exit 0 | Generated projection and source syntax only. |
| `python3 scripts/validation/check-operations-catalog.py` after approved `render_service_inventory` refresh | PASS, exit 0 | Only eight n8n current-service projection cells changed; historical rationale retained. First run identified those eight stale cells (exit 1). |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS, exit 0 | Current Stage 05 prose; not runtime proof. |
| JS/Python Code-node token isolation, private/redirect URL denial, OpenBao Agent fresh render, n8n DB migration, Cassandra data/auth | NOT_RUN | Isolated image execution requires full Docker preflight and source controls; HOME and credentials remain out of scope. |
| HOME service start/restart, crawler request, OpenBao unseal or secret rotation | NOT_RUN | Separate exact operational approval required. |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1/W5 | Source defects corrected; runtime inventory remains unobserved | This Task and service READMEs |
| 2 | W2/W5 | Static PASS; Code-node and upgrade NOT_RUN | GDE/POL/RUN-0053 and n8n source |
| 3 | W2/W5 | Security pin/LAB render PASS; URL/egress and LAB runtime NOT_RUN | GDE/POL/RUN-0091 and LAB Cassandra documents |
| 4 | W2/W5 | Sealed synthetic PASS; Agent freshness NOT_RUN | GDE/POL/RUN-0085 and POL-0079 |
| 8 | W5 | Focused regression PASS; isolated execution NOT_RUN | This Task verification receipts |

### Completion recheck on 2026-10-04

Source baseline `ce001be7af93aebe6430f586b56a5c443fa9f386`. The focused
runtime/version contract command above was rerun: 58 tests, exit 0. Both
`workflow-n8n` and `crawl4ai` public-example Compose renders exited 0;
Cassandra LAB render with the synthetic path
`/tmp/hyhome-cassandra-0204-synthetic` also exited 0. These are static/synthetic
checks and do not replace the acceptance contract's isolated functional proof.

Read-only Docker preflight returned context `default`. Exact target images
`n8nio/n8n:2.41.6`, `n8nio/runners:2.41.6`, and `unclecode/crawl4ai:0.9.4`
were not available locally. The older cached versions cannot prove target
behavior. `BLOCKED_IMAGE_NOT_AVAILABLE` names the exact-image n8n Code,
queue, scheduled/webhook and crawler request tests. No images were pulled and
no containers, networks, mounts or volumes were created in this recheck.

Current official sources were reviewed on 2026-10-04. The Crawl4AI
[link-preview advisory](https://github.com/unclecode/crawl4ai/security/advisories/GHSA-wh5w-hmj3-vgg7),
[robots advisory](https://github.com/unclecode/crawl4ai/security/advisories/GHSA-f77g-77vp-r96v), and
[untrusted-wrapper advisory](https://github.com/unclecode/crawl4ai/security/advisories/GHSA-5w5p-vcv6-mm3f)
identify 0.9.4 as patched. The official tagged
[egress broker source](https://github.com/unclecode/crawl4ai/blob/v0.9.4/deploy/docker/egress_broker.py)
rejects non-global resolution answers and pins the approved address while
revalidating redirects. This source inspection is not execution evidence.

`BLOCKED_EGRESS_ENFORCEMENT` remains: the repository's dedicated bridge has
no demonstrated host/LAN/link-local egress enforcement. Setting a Docker
network `internal` would also require proving host bridge-gateway denial;
that single property alone cannot satisfy private-destination acceptance.
No consumer, proxy, firewall rule or crawler activation was inferred.

`BLOCKED_CODE_SECRET_ISOLATION` remains: mounted runner authentication and
launcher process environment have not been proven unreadable to Code tasks.
The current official
[n8n hardening guide](https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/harden-task-runners/)
recommends denying sensitive per-process `/proc` reads through AppArmor.
No host AppArmor policy was installed or presumed available here.
`BLOCKED_OPENBAO_AGENT_FRESHNESS` and `BLOCKED_CASSANDRA_AUTH_DATA` remain
named runtime gaps; sealed-status synthetic checks and LAB render do not
establish renewal/freshness, old-data migration, authentication, or safe UID.

The next approval must name the image pulls for the exact n8n server/runner
and Crawl4AI targets and authorize their unique synthetic test project. The
existing image digests above must be rechecked before pull. The runtime
fixture must be reviewed before execution: no published host ports, no HOME
networks/volumes, no actual credentials, explicit aggregate CPU/memory/disk
limits alongside concurrent rehearsals, and cleanup limited to the created
container/network/volume identities. n8n needs the matching broker/runner
Code path, synthetic metadata/queue, and both JavaScript/Python token-read
denial; a launcher shell probe is insufficient. Crawl4AI needs its actual
DNS/redirect/robots/link-preview/untrusted-config paths plus a reviewed egress
boundary, including host bridge-gateway and metadata denial. Installing host
AppArmor or firewall rules is a separate operation and is not authorized by
image-pull approval. HOME rollout and real metadata migration remain separate.

### Protected delivery attempt — 2026-10-04

The user explicitly requested Commit, Push, Merge and cleanup after the local
closure report. This authorizes delivery of the reviewed source to
`buenhyden/hy-home.docker`, source branch `codex/spec-0201-0205-closure`, base
`main`, through a pull request and merge commit if required checks pass.
It does not authorize an audit exception, bypass, direct main push, force push,
HOME operation or deletion of another worker's state.

Before-state: fetched `origin/main` and owner local `main` both point to
`d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; reviewed local closure source is
`68a461c18e548a835a3abc37ecf27c12489c39b4`, clean worktree. Authenticated
branch-protection readback requires strict `validation-changed`, zero approving
reviews, and no required CODEOWNER review. Existing draft PR350 belongs to
SPEC-0206 and is not this delivery target. The official braces advisory was
rechecked: no patched version; no security waiver is applied.

Command classes: push this feature branch with upstream, create a Draft PR
with exact scope/evidence, inspect its hosted checks, and merge only after all
required checks pass. Merge must preserve the archive source objects and named
recovery commits. After merge, fetch and fast-forward owner main; remove only
clean task-owned worktrees and branches whose commits are reachable from main.
If checks fail, preserve the feature branch/worktree and report BLOCKED.
Rollback before merge closes the delivery PR only with owner approval; it
never removes the protected main history or private runtime state.
Delivery after-state: `git push -u origin codex/spec-0201-0205-closure`
exited 0 and Draft [PR351](https://github.com/buenhyden/hy-home.docker/pull/351)
was created for source `df2705c193456ea459a6b4e8b70516935914208e`.
Hosted [CI run 37138415020](https://github.com/buenhyden/hy-home.docker/actions/runs/37138415020)
failed required `validation-changed`: six `invalid-initial-status` findings
for this package's new Spec, Plan and Tasks 1-4. This is the actual hosted
failure; the separate unpatched braces advisory remains a security hold.
CodeQL and GitGuardian passed but do not replace the required gate.

Independent lifecycle review confirmed that the changed-document validator
uses the protected merge-base state, not intermediate feature commits.
Registered initial `draft` delivery and one permitted edge per subsequent
protected delivery are required for these six documents. No validator change,
transition override, false rewind of completed work, or archive of incomplete
SPEC-0204 is applied. Staged registration is deferred while the independent
security merge hold persists; this receipt does not approve a waiver.

Merge result: BLOCKED, no merge or direct main push. Owner local main and
fetched origin/main remain `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.
The closure branch and its clean worktree remain available for review and
subsequent compliant delivery. Cleanup is restricted to clean obsolete
worktrees with preserved branch references and feature branches already
reachable from protected main. No runtime state or private files are removed.

Cleanup receipt: `git worktree remove /tmp/hyhome-spec-0204-integration`
exited 0 after checking clean status, absence of private environment/registry
and untracked secret files, and source reachability from the preserved closure
branch. Its `feat/0204-common-integration-ops` reference remains. `git branch -d`
removed only `feat/0202-development-data-lab`,
`feat/spec-0201-home-infra-diagnosis`, and `feat/spec-0203-quality-results`,
each with confirmed ancestry to origin/main. The exact unchanged remote 0203
head was also reachable from main and had no open PR; its deletion exited 0.
The already-absent remote 0202 branch's stale tracking reference was removed.
Fetch and `git merge --ff-only origin/main` exited 0; owner main and origin/main
both remain at the baseline SHA above. The main owner worktree and closure
worktree are retained. Receipt metadata validation selected one document,
zero violations/overrides, exit 0; independent read-only review confirmed the
hosted failure and absence of a false success claim.

### Package reassessment — 2026-10-04

The renewed completion request does not grant the separately scoped image
pulls, host isolation policy or HOME actions. This Task transitions from
`in-progress` to `blocked` because its existing acceptance criteria 2 and 3
still require exact-image functional execution and demonstrated secret/egress
boundaries. Criteria 1/8 have source and focused static evidence; criterion 4
retains named runtime blockers. Completed Tasks 2-4 stay within the active
package under the registered package occupancy rule; neither this Plan nor
Spec can transition to completed while these acceptance gaps remain.

Reassessment corrected active Spec/Plan descriptions that still called
SPEC-0203 source-only, all metrics unverified and dev-pg recovery absent.
The current evidence is synthetic importer/metrics and selected-set Restic
recovery PASS, with real target/store/Grafana, HOME/offsite/PITR and measured
operational capacity still NOT_RUN. Frozen SPEC-0201/0202/0203/0205 bodies
are preserved. Their completion does not satisfy this Task's service-specific
security criteria or the independent protected delivery gates.

Reassessment verification against `b1c325cc0d256d30b1cef8325fe336f8b7679ca0`:
`python3 scripts/validation/check-document-metadata.py --mode check-changed
--base-ref HEAD` exited 0, selected 3 documents, zero violations/overrides.
`python3 scripts/validation/check-document-corpus-lifecycle.py --base-ref HEAD`
exited 0, zero corpus/recovery violations, 327 preserved units. Independent
archive review matched SPEC-0201/0202/0203/0205 to their catalog source objects:
4/4, 4/4, 3/3 and 3/3 members respectively, exact modes/types/blobs; navigation
and scoped completion receipts passed. No frozen body was changed. The new
[hosted run 37140139679](https://github.com/buenhyden/hy-home.docker/actions/runs/37140139679)
for that source completed with failure; it is not a local-validation PASS.
This three-document correction changes no runtime code, interface, source
links or resource state, so previous implementation tests were not rerun.
Recovery is a scoped revert of this document correction; it must not rewrite
frozen records or imply a runtime rollback. Two independent read-only
reviewers approved the final three-document diff with no blocking findings;
they confirmed the registered blocked transition, evidence limits and pending
Phase A/B approval boundary. Neither reviewer ran runtime actions or changed
source/private state.

### Prepared next execution boundary

Phase A proposal is limited to read-only Docker context/daemon architecture,
image-cache and aggregate host-capacity preflight, followed by separately
approved pulls of `n8nio/n8n:2.41.6`, `n8nio/runners:2.41.6`, and
`unclecode/crawl4ai:0.9.4`. Resolve the current official manifest before each
pull, compare it to this Task's recorded digest and stop on mismatch until
reconciled. Record digest/platform and image compatibility metadata only;
never dump image/container environment, private Docker config or secrets.
No service starts, mounts, networks or volumes are authorized by Phase A.
Image-cache removal also needs its own exact disposition.

Phase B remains unapproved until the actual synthetic controller and security
boundary have independent review. Prepare it within the already approved
runtime test file or this Task; a new fixture, proxy or host-policy file needs
an exact writer amendment. The proposed serial fixture ceiling is 4 CPU,
6 GiB memory, 8 GiB writable scratch and 20 minutes per service phase, subject
to verified spare capacity before execution; these are proposed caps, not
measurements. Use a unique Task-labeled project, no published host ports,
no HOME networks/volumes, no real credentials and explicit created-resource
identities for cleanup. A network name or `internal` flag alone is insufficient.
If effective Code-token denial or host/LAN/metadata egress denial cannot be
proven without a new host policy, stop before the corresponding request and
seek that specific scope. Do not substitute shell stubs or cached older images
for the required actual broker/Code and crawler behavior.

## Review Evidence

Independent code and security review found three actionable gaps. The
unused Valkey secret mount was removed; default/dedicated render now exposes
only the selected password reference to main and worker. n8n Renovate image
updates were disabled because automatic Dockerfile/runner updates would leave
Compose build arguments and local tags stale; matching pins now require one
manual reviewed change. RUN-0098 and OpenBao guides distinguish Compose
`depends_on` gating from Docker daemon auto-restart, which can start an existing
Agent while the server is sealed.

The runner launcher still needs its auth token in a process environment. A
same-container Code task may read `/proc/*/environ` or the mounted secret
without an effective isolation control. Crawl4AI's dedicated bridge limits
Compose DNS discovery but does not deny host/LAN/link-local egress. Both are
HOME acceptance blockers; no Code-task `/proc` denial or synthetic URL/redirect
policy test is claimed. Official runner `_FILE` support descriptions differ
between the general n8n environment documentation and launcher setup text;
the approved inline secret-file adapter remains the reviewed source path.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft `0f67cb297`, review transition `2157e62c5`. Source commit `a51014aab597cd95bf5db19f00348e1d487ce642`; approved current-service projection eight-cell refresh is included in the follow-up documentation commit. No remote merge or HOME execution.

## Rulings

Do not shrink main runners without path evidence. Official documentation
says `n8nio/runners` does not support `_FILE`. The approved inline Compose
entrypoint must read the mounted secret, reject empty input without printing
it, export only the launcher variable, and retain official tini/launcher
behavior. A separate wrapper or image requires another exact Task amendment. Existing LAB
Cassandra work is a verification item, not a repeat implementation.

## Deferred Items

Image/digest acceptance, synthetic container preflight,
HOME version upgrade, management DB/encryption-key backup, real credential
handling and all service operations remain separate.
