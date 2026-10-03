---
title: "Runtime Compatibility and Security Task"
version: "0.1.1"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-10-03"
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
No generated projection or runtime condition is marked PASS from the initial draft.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft `0f67cb297`, review transition `2157e62c5`. Source commit pending.

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
