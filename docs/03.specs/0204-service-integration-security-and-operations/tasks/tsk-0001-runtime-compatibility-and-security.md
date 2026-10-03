---
title: "Runtime Compatibility and Security Task"
version: "0.1.1"
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

The user explicitly requested resolution of PR351's six initial-status
findings. This docs-only delivery is based on protected main
`d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, on branch
`codex/spec-0204-registration`. It registers the original draft bodies of
Spec, Plan and Tasks 1-3 from `0f67cb297`, and Task4 from `d666b6f42`,
plus this receipt, the Stage 03 navigation row and the Registry spec counter.
Current implementation, approvals and completed evidence remain unchanged on
`codex/spec-0201-0205-closure` at
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`. This first registration is
not a reversal of that work or a runtime acceptance claim.

The validator correctly compares the PR's protected merge-base state.
Intermediate commits on a feature branch cannot register a document on main.
Use three preliminary docs-only protected PR merges: draft registration;
Spec review with Plan approved and Tasks ready; then Spec approved with
Plan active and Tasks in-progress. Merge that protected main into the closure
branch without rewriting named recovery/archive objects. PR351 supplies the
fourth lifecycle edge and the final reviewed bodies: Spec active, Task1
blocked, Tasks 2-4 completed, Plan remains active. Every round must pass the
normal required gate and keep actual execution approvals separate. No
transition override, validator edit or gate waiver is authorized. PR351's
independent security merge hold remains unchanged.

Registration verification: changed metadata against origin/main selected 7
Markdown documents, zero violations and zero transition overrides, exit 0.
The initial counter preparation failed its high-water/next-number relationship;
both were then updated together and validation passed. Document links mode all
exited 0 with zero failures and one pre-existing historical-source warning.
Corpus and archive recovery exited 0 with zero violations. Independent
read-only review approved the eight-file registration and the three-stage
route; `git diff --cached --check` exited 0. No runtime tests are needed for
this document-only registration.

Approved writer scope: these six package documents,
`docs/03.specs/README.md`, and the existing spec counter in
`docs/99.templates/registry.json`; no runtime or private inputs. Rollback is
a scoped revert of the registration delivery, with original source objects
retained; do not cancel a completed Task or delete archived bodies.


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
