---
title: "Shared Experience Integration Task"
version: "1.0.4"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0206-TSK-0002"
parent_ids:
- "SPEC-0206"
- "SPEC-0206-PLAN-0001"
created: "2026-10-03"
---

# Shared Experience Integration Task

## Objective

Register the tested Storybook static origin in root Compose with restricted browser access, coherent operations contracts and generated metadata.

## Inputs

Approved SPEC-0206 and Plan W3-W4; TSK-0001 artifacts are required before integration; current root/Traefik/OAuth2 Proxy source; admin-only decision from the user; no remote MCP audience/client.

## Work Log

| Current -> target | Exact writer files | Regression / rollback |
| --- | --- | --- |
| No shared experience tier -> optional Storybook static origin | NEW `infra/13-experience/README.md`, `infra/13-experience/storybook/README.md`, `infra/13-experience/storybook/docker-compose.yml`; `docker-compose.yml`, `infra/README.md` | Root/profile render, no host 80/443, network/health/resource checks; revert only new tier and root include. |
| Browser route unavailable -> admin-only Traefik HTTPS on dedicated ingress | New leaf Compose labels; `infra/01-gateway/traefik/docker-compose.yml` joins the new internal `experience_ingress_net` declared in root `docker-compose.yml`; read-only existing `infra/01-gateway/traefik/dynamic/middleware.yml` and `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg` | RouteAuth, asset auth, TLS/render and deny checks; assert only Traefik and Storybook join this network and Storybook is absent from shared `edge_net`; no OAuth2 Proxy group widening. |
| Profile/public metadata absent -> registered optional profile and source projection | `docs/05.operations/policies/0078-compose-profile-vocabulary.md`; generated `infra/tech-stack.versions.json`; `docs/99.templates/registry.json`; `docs/03.specs/README.md` | Profile vocabulary, image projection generator/check, registry and document contracts; revert logical metadata commit. No new public or secret environment key is required for the static origin; existing `DEFAULT_URL` is consumed without reading its value. The real `.env` is untouched. |
| No current operating contract -> Storybook subject 0101 | NEW `docs/05.operations/guides/0101-storybook.md`, `docs/05.operations/policies/0101-storybook.md`, `docs/05.operations/runbooks/0101-storybook.md`; `docs/05.operations/README.md`, `docs/05.operations/guides/README.md`, `docs/05.operations/policies/README.md`, `docs/05.operations/runbooks/README.md` | Operations catalog, links, metadata, exact service binding; revert only this subject/index rows. |
| Codex/Claude Design usage -> verified instructions | `projects/storybook/nextjs/README.md` is TSK-0001 writer; this Task writes the new GDE-0101 usage section and reads that README | Official-source URL and installed-client availability review; revert guide section. |
| Existing baseline gates assume every routed service uses `edge_net` and every service has a Docker secret -> precise Storybook contract | `tests/validation/test_compose_baseline_gates.py`; `infra/common-optimizations.exceptions.json` | Reuse the canonical Compose-aware loader for `!override`, accept only an explicitly selected network also joined by Traefik, retain the Storybook dedicated-network assertion, register a single no-secret exception with owner/risk/exit/review; run focused tests and quickwin gate; revert only these two files if the service is removed. |
| Grafana service coverage inventory omits the new root service -> one truthful row | `infra/06-observability/grafana/README.md` Service Coverage table only; user approved this exact extra writer on 2026-10-03 | Add Storybook once with metrics source `none` and no new dashboard/scrape claim; `test_readme_covers_every_service_every_job_and_every_dashboard`; revert the row if service is removed. |
| Storybook leaf README still routes future evidence to frozen SPEC-0206 Task -> current operations handoff | `infra/13-experience/storybook/README.md`; user approved this exact current-consumer cutover on 2026-10-04 | Route future evidence to the approved operations Task plus RUN-0101; preserve historical source evidence and revert only this README row if the operational handoff changes. |

The root Compose, Traefik Compose network attachment, profile policy, Stage 99 Registry and image projection have exactly one writer: this Task. The user approved the Traefik writer addition on 2026-10-03 after independent security review identified direct origin access from shared `edge_net` as High risk. TSK-0001 consumes their planned contracts and does not edit them. The user approved the two current-service projection cells in `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md` on 2026-10-03: add the Storybook service row and update Traefik’s Network cell through the inventory generator. On 2026-10-03 the user additionally approved the Storybook middleware projection cell after independent review required rate limit and shared retry/circuit controls. Preserve all historical judgment prose; this Task is the sole writer of those three current-service cells.

## Verification Evidence

TSK-0001 source handoff is `e811e159afa2dc7245bb2d6b562a91cf931283fe`; its exact-SHA image and local isolated browser evidence are recorded in TSK-0001. This Task changed source declarations, focused validators and operator contracts; HOME was not restarted or deployed.

| Command / assertion | Exit / evidence |
| --- | --- |
| `HYHOME_COMPOSE_PROFILES='core experience' bash scripts/validation/validate-docker-compose.sh` | 0; 9 selected services, synthetic `.env` removed. Focused JSON assertion also exited 0: Storybook only on internal `experience_ingress_net`, Traefik on that and `edge_net`, no host port/volume/secret/env, image tag exact SHA, `pull_policy: never`, UID/GID 101:101, read-only 256 MiB / 0.5 CPU and SSO router. Core/dev/local selections exclude Storybook. |
| `bash scripts/hardening/check-all-hardening.sh 01-gateway` | 0; shared checker covers tiers 01–12, so tier 13 hardening was verified by the focused rendered JSON assertion above. |
| `python3 scripts/validation/check-operations-catalog.py` | 0 after generated current-service projection changed exactly the approved Storybook row, Traefik Network cell and Storybook middleware cell. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates`; `HYHOME_COMPOSE_PROFILES='core experience' bash scripts/validation/check-quickwin-baseline.sh` | 0 each; 93 tests (21 skipped), and 9 rendered services with all six QuickWin violation counters zero. Canonical Compose-aware loader reads `!override`; the dedicated-network/middleware assertion and one documented Storybook no-secret exception preserve the baseline. |
| `bash scripts/operations/sync-tech-stack-versions.sh --write`; `bash scripts/operations/sync-tech-stack-versions.sh --check` | 0 each; generated local-custom `hy-home/storybook` image entry (`repositories=92 external=74 local_custom=18`). |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` for the six new/changed 0101 and profile files; same checker for two README frontmatters; `python3 scripts/validation/check-document-links.py --mode navigation`; `--mode entrypoint`; `git diff --check` | 0 each; metadata selected 6 and 2 respectively with zero violations; 33 new local links and repository navigation/entrypoint routes resolve. Earlier metadata run returned 1 for two duplicated Compose version literals; corrected to official docs links. |
| 2026-10-04 fresh source/static batch: Storybook contract, core/experience render, version92 and combined 25 unittests | PASS; source/static only. No Docker exec/run, HOME deployment, DNS/TLS or OIDC session observation is claimed by this row. |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 3 | W3 | PASS: source/static Compose profile, dedicated network, admin-only router and no host ports render safely; HOME TLS/OIDC/session remains operational follow-up | [Storybook Compose](../../../../infra/13-experience/storybook/docker-compose.yml) |
| 6 | W4 | PASS: official-source Codex/Claude guide and local config examples distinguish unexecuted external actions | [GDE-0101](../../../05.operations/guides/0101-storybook.md) |
| 7 | W3 | PASS: operations subject, Registry, Grafana service row, version/inventory projections and focused gates reached active source/static state | [POL-0101](../../../05.operations/policies/0101-storybook.md) |
| 7 | W4 | PASS: Guide/Policy/Runbook, README handoff, independent review and rollback boundaries agree with source/static completion | [RUN-0101](../../../05.operations/runbooks/0101-storybook.md) |

## Review Evidence

Independent integration code, security and rules-engineer reviews found no Critical/High issue in the dedicated internal ingress topology, then identified the missing per-route gateway controls, Compose tag test parsing, routed-network test assumption, quickwin no-secret exception, document links and Grafana service row. The user approved each out-of-scope correction. The corrected static gates above pass. Final independent source and security re-reviews returned APPROVED/PASS with no blocking issue; the policy review returned PASS with one documentation-evidence minor, corrected here. ForwardAuth Cookie minimization remains a minor follow-up; neither HOME behavior nor claim delivery was observed.

## Commit Ledger

Baseline main/origin-main `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; dependent source base `fbbea9123751c13588022cdb76213fd8b5a14b6e`; Storybook source `e811e159afa2dc7245bb2d6b562a91cf931283fe`; source evidence `d208109d38371d41f6888bd1b76538754396d4b5`; TSK-0001-owned README entrypoint link correction `90452d6484e7528caa2bc661baa1b8c3bc13971c`. Integration source `519b2fd40e9ad98b429e05a1c932ceec10893e81`; operations draft-to-review `4019dd1f314f137a550f08489fbe74469ed04186`, review-to-active/approved `ecd4dd89a47a359ff2c9e2e6617ca4e8b04ba46e`, and policy approved-to-active `a4e1723523928011365f76cb7fcf46a2e930d6f0`. This Task closure commit records the source/static outcome. HOME TLS/OIDC observation is handed off to Stage 05 operations and is not required for SPEC-0206 source/static completion. On 2026-10-03 the user separately requested commit, push, merge, branch/worktree cleanup and main synchronization. The clean feature tip `890c54fbad49dfd77008bcb48953d7ccf5ac56df` was pushed to `origin/feat/0206-storybook-sharing`, and Draft PR #350 was opened against `main`. Authenticated main protection requires `validation-changed` and zero approvals; CODEOWNERS review is not enforced. Hosted run `37121382053` failed `validation-changed` with 12 `invalid-initial-status` findings on new documents that were introduced at draft and transitioned in separate commits. The official GHSA-vfj7-8cjw-p6xm still lists no patched `braces` release, and local `npm audit --json` exits 1 with five high findings from the dev ESLint chain. At that observation, merge and branch deletion were blocked and local `main`/`origin/main` remained `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`. This historical failure is not a current delivery state. Read-only authenticated inspection on 2026-10-04 confirmed [PR #350](https://github.com/buenhyden/hy-home.docker/pull/350) merged at `2026-10-03T20:52:27Z` as `0460795abf6da9203e38f30291a8f20118c6ab88`, which is an ancestor of the then-observed local `main` and `origin/main` `7f939ae802afc1d23f96b8eca4100abfcc2bf629`. The observed merge does not turn the failed required run into PASS or authorize another bypass. At that observation, the unresolved advisory and user hold remained applicable to subsequent delivery. Current audit handling follows the separately approved bounded acceptance in the quality policy. No HOME rollout or authentication observation is inferred from the merge.

## Rulings

Use existing `/admins` ForwardAuth for browser traffic with `sso-auth@file` and a manual OAuth2 Proxy start entrypoint; real 401/403 and session behavior remain untested. MCP is a task-local process outside root Compose until approved machine authentication exists. Reconcile already issued operations subject 0100 before reserving 0101; do not reuse or relabel 0100.

## Deferred Items

Reviewer group, remote MCP OIDC, HOME activation, DNS/TLS observations, external design account use and data migration remain deferred to GDE/POL/RUN-0101. PR #350 is merged; feature-branch deletion is not established by that receipt. SPEC-0206 is now source/static completed: criterion 3 has accepted source/static evidence, while HOME TLS/OIDC/session evidence remains a Stage 05 operational follow-up. The completion request does not waive those operational approvals or alter the separately owned audit policy.

Delivery receipt review, 2026-10-04.

This correction changes delivery metadata, current deferred-work routing and completion disposition only. Historical command results, failure diagnostics, source SHAs, acceptance criteria, completed Task status and runtime boundaries are preserved. The user requested review and completion of SPEC-0206 and authorized commit/push delivery in this conversation; the target is `buenhyden/hy-home.docker`, a task-owned `codex/spec-0206-delivery-receipt` branch and a documentation-only Draft PR. No protected-main push, merge bypass, credential or operational action is included. Rollback is a follow-up correction or revert of this documentation commit; the historical source objects remain reachable.

Focused verification: `markdownlint-cli2` 0.22.1 on this file exited 0; `git diff --check` exited 0; `git merge-base --is-ancestor 0460795abf6da9203e38f30291a8f20118c6ab88 origin/main` exited 0. A Python comparison against the base confirmed Verification Evidence, Review Evidence, Rulings and completed status unchanged (exit 0). Independent read-only policy/document review returned PASS. The first `check-document-metadata.py --mode check-changed --base-ref origin/main --changed-path` attempt exited 1 for one forbidden extra heading; the receipt was moved under the existing Deferred Items section without changing the body contract. The corrected metadata run exited 0 (`selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`); the final independent review returned PASS. No source/runtime test is newly claimed by this documentation-only correction.

Final source delivery checks: changed metadata14/0 violations, corpus/archive recovery341/0 violations, links0 failures/1 legacy provenance warning, authored Markdown14 and diff checks each exited0. The first policy review found the parent-ID omission; the single-field retry changed POL-0101 parent to AD-0031 with no status/authority promotion, followed by independent re-review. Required hosted checks and protected completion merge remain distinct pending delivery gates; no new container/HOME evidence is claimed.
