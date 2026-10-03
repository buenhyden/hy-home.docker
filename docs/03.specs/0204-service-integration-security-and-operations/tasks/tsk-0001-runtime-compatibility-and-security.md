---
title: "Runtime Compatibility and Security Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
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
| Official n8n runner/release, Crawl4AI security release, OpenBao status and amd64 image manifest inspection on 2026-10-03 | PASS read-only | n8n image index digests `sha256:87e0bab2c93192e8dd885ff7b0697c22a1bd97489568a8c67cc140fd7dbb342d` and `sha256:443eaee69319997627e2129ed8d512c4f4ea2418a744393cf26e843237399299`; Crawl4AI `sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b`. No image pull or execution. |
| `python3 -m unittest tests.validation.test_service_runtime_compatibility tests.validation.test_tech_stack_version_contract -q` | PASS, exit 0, 58 tests | Includes synthetic missing/empty/valid runner token and broker guard shell execution, plus sealed rc0/1/2; no Code-node process or image execution. |
| `docker compose --env-file .env.example --profile workflow-n8n config --quiet`; default/dedicated broker secret render; `--profile crawl4ai config --quiet` | PASS, each exit 0 | Only static root model; selected n8n main/worker receive one Valkey secret. |
| `LAB_DATA_DIR=/tmp/hyhome-lab-cassandra-synthetic docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile cassandra config --quiet` | PASS, exit 0 | Initial render without required `LAB_DATA_DIR` exited 1; corrected with a synthetic path. No LAB service or volume created. |
| `bash scripts/operations/sync-tech-stack-versions.sh --write` then `--check`; `git diff --check`; shell syntax | PASS, each exit 0 | Generated projection and source syntax only. |
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

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft `0f67cb297`, review transition `2157e62c5`. Source commit pending; no remote merge or HOME execution.

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
