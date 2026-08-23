---
profile_id: task
status: active
artifact_id: task-0153-0008
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-23
---

# Task 0008: Operations

## Objective

Converge Stage 05 catalog/domain/subject documents, remove ops- path prefixes and Releases, and retain incident year packages.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Task 7 Spec lifecycle, Operations membership manifest, approved Migration owner_task 8 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Preflight authority freeze | Verified Migration 0003 rows `mig-0003-r0257` through `mig-0003-r0449`: 193 total, 192 renames, one delete; froze the bounded declared/live consumer union and exclusions in the ignored Task 8 report. |
| RED | Added focused Operations topology, identity, ownership, Release-absence, incident, bounded-reader, stale-authority, and semantic-witness tests. The 18-test run produced the single intended final-topology failure before mutation. |
| Structural execution | Executed exactly 192 literal native `git mv` source/target pairs from Migration 0003 after equality and precondition checks; removed the registered Release README and the Plan-authorized Release template/support authority. |
| Consumer convergence | Rewrote the frozen current-consumer union to prefixless four-digit subject routes. Immutable Stage 98 evidence, generated/historical Stage 90 material, and explicit negative fixtures were excluded. |
| Validator convergence | Made Registry plus Migration 0003 the current structural authority; retained Migration 0002 only for bounded body-derived semantic-witness checks. |
| Review-fix round 1 | Addressed independent specification `C0/I1/M0` and Python `C0/I6/M0` findings: removed remaining active generic predecessor routes; added a fail-closed active scan; bounded and descriptor-hardened Git/tracked-file reads; enforced the full frozen Migration 0003 row contract; made semantic witnesses and Operations Registry/topology relations exact; narrowed metadata baselines to verified source/target pairs; restored Migration 0001 tombstone expectations; and restored the checker execution contract. Re-review remains pending. |
| Review-fix round 2 | Addressed Python re-review `C0/I4/M0`: made the manifest declare Registry plus Migration 0003 as current authority and Migration 0002 as semantic witness only; enforced complete Operations profile, traceability, lifecycle, and `profile_id` contracts; narrowed Spec scan exclusions to exact frozen implementation evidence; and replaced Operations directory materialization with descriptor-anchored bounded streaming enumeration and identity revalidation. Re-review remains pending. |
| Review-fix round 3 | Addressed Python/specification re-review `C0/I2/M0`: pinned the complete approved Operations profile and lifecycle projections, switched current Operations documents to canonical duplicate-safe frontmatter parsing, corrected the two repo-contract comparison guides, and extended the active-route scan to scripts/config with exact historical/negative exclusions. Re-review remains pending. |
| Review-fix round 4 | Converged the controller gate on current per-service catalog Guide links, the exact incident packet role paths, and exact role-leaf links for Specs 0001/0002/0005/0095. Reproduced the script-reference unsafe-surface failure as the two authorized Task 8 Release deletions, exempted only those exact bounded Git-reported deletions, and retained fail-closed missing/symlink/type/race behavior. The remaining nine script-reference occurrences are exact inherited Spec 0135/0136/0137 evidence; re-review remains pending. |
| Review-fix round 5 | Addressed the four important round-4 review findings with strict mutation-first coverage: bounded script-reference Git discovery with process-group cleanup and one batched ignore query; shared CommonMark-aware rendered-link parsing; exact confined regular Spec-role targets; and bounded tracked service discovery plus descriptor-safe reads. Count, file, aggregate, timeout, partial-output, symlink, FIFO, race, false-link, and target-depth/type boundaries all fail closed. Re-review remains pending. |
| Review-fix round 6 | Addressed Python/shell re-review `C0/I2/M0` while specification review remained `C0/I0/M0`: inline-code comment openers no longer alter cross-line HTML-comment state, and angle-bracket Spec role destinations cannot bypass validation. `DocumentLink` now carries the parser-owned label alongside its existing line, raw destination, and normalized target; Spec and service gates consume that typed occurrence directly with no raw-regex rebinding. Final independent specification and Python reviews both approved the result at `C0/I0/M0`. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Focused Operations tests | `python3 -m unittest tests.validation.test_operations_catalog tests.validation.test_operations_taxonomy` | PASS — 64 tests, including bounded Git/output/deadline/process-group cleanup, batched ignore discovery, tracked input and directory race/type/count/file/aggregate limits, state-aware CommonMark exclusions, angle-bracket Spec-role target confinement/type, service Guide routing, embedded-section dependency integrity, complete Registry/lifecycle projection, Migration contract, semantic witness, active-reference, incident paths, and executable-usage mutations. |
| Metadata repository contract | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | PASS — zero violations. |
| Changed metadata transition | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS — 269 selected, zero violations, 206 proven base-existing exceptions, no overrides. |
| Focused Task 8 metadata tests | Six exact source/target baseline methods | PASS — exact-source/profile-only, extra-metadata rejection, missing-source, pre-existing-target, unregistered-target, and unrelated-README boundaries all green. |
| Final Operations topology | `python3 scripts/validation/check-operations-catalog.py --mode complete` | PASS — 13 domains, 75 subjects, 66 Guides, 64 Policies, 62 Runbooks, zero Releases. |
| Active consumer scan | `python3 scripts/validation/check-operations-catalog.py --mode consumers` plus focused Markdown/script/config mutations and live scan | PASS — the live scan is empty; exact historical evidence and negative fixtures remain excluded while active Specs, scripts, and configuration are scanned. |
| Repo-contract comparison drift | Focused current-path/existence method plus `bash -n scripts/validation/check-repo-contracts.sh` | PASS — both comparison variables resolve to existing prefixless catalog Guides, so their guarded drift checks no longer skip for a retired document path. |
| Round-4 repository-contract slices | Focused service, incident, Spec traceability, and script-reference sections | PASS for all Task 8-owned behavior. Only the two exact Task 8 Release deletions are exempted; arbitrary deletion, broken symlink, FIFO, and descriptor identity race fail closed. The live script section exposes nine inherited Spec 0135/0136/0137 missing references rather than an unsafe surface. |
| Round-5 repository-contract hardening | Focused real-section executions plus shared link-parser and bounded-reader regressions | PASS — partial-output Git timeout reaps its process group; ignored discovery is one bounded batch; fences, HTML comments, inline code, and images do not satisfy links; Spec targets must be exact confined existing nonsymlink regular leaves; compose symlinks, README FIFO/races, and count/file/aggregate overflow fail closed. Git byte ordering is accepted without weakening duplicate rejection. |
| Round-6 rendered-link authority | Exact parser/Spec mutations plus live Spec and service sections | PASS — `` `<!--` `` does not hide the next rendered link, real multiline comments still suppress links, and existing angle-bracket targets pass while missing angle-bracket targets fail. A normal Operations index link remains navigation rather than a Policy role link. |
| Full repository contract | Single bounded `bash scripts/validation/check-repo-contracts.sh` run | NOT A PASS — completed with `failures=13`; zero Task 8-owned sections remain failing. The 13 future/inherited sections and exact nine script references are recorded in the ignored Task 8 execution report. |
| Manifest authority | Focused live and mutation methods in `tests.validation.test_script_manifest` | PASS — two tests; active Operations implementation/gate rows cannot declare Migration 0002 as current authority. |
| Manifest diagnostics | Complete-schema ordering method and `check-script-manifest.py` under a 60-second bound | NOT A PASS — inherited row ordering places `check-task4-migration.py` before `check-target-surface-contract.py`; the complete checker produced no output before timeout. |
| Document registry tests | `python3 -m unittest tests.validation.test_document_registry` | PASS — 31 tests. |
| Focused CI leaf test | Operations current-authority CI leaf method in `tests.validation.test_ci_gate_contract` | PASS — one test. |
| Tombstone preservation diagnostic | Targeted Migration 0001 preservation method in `tests.validation.test_script_manifest` | NOT A PASS — exactly three inherited Airbyte Spec-path mismatches remain; Task 8-attributable tombstone failures are zero. |
| Static validation | Ruff, `bash -n`, and `git diff --check` for working tree and index | PASS. |
| Python syntax | `python3 -m py_compile` over the modified Operations and metadata validators, CLI, and focused tests | PASS. |
| Broad metadata diagnostic | `python3 -m unittest tests.validation.test_document_metadata` under a 240-second bound | NOT A PASS — completed 256 tests with inherited non-Task-8 failures; focused Task 8 contract tests are run separately. |
| Link alignment diagnostic | `python3 scripts/validation/check-document-links.py --mode alignment` | NOT A PASS — 44 inherited/current-plan findings, including Spec 0153 links to its frozen Migration authority; no missing prefixless Stage 05 target introduced by Task 8. |
| Shared document-link tests | `python3 -m unittest tests.validation.test_document_links` | NOT A PASS — 28 tests ran; all 15 `DocumentGraphTests`, including the cross-line comment-state regression, passed. Three pre-existing consumer methods still fail on 16 stale deleted-validator mentions, an oversized/nonregular Task 0137 traceability input, and known alignment findings. |
| Round-6 full repository snapshot | Single `timeout 280s bash scripts/validation/check-repo-contracts.sh` run on the final tree | NOT A PASS — completed with `failures=13`; all Task 8-owned sections passed. The remaining failures and nine script references are inherited or owned by Tasks 9–12. |
| Exact row inventory | Bounded Migration 0003 source/target scan | PASS — 193 rows, 192 rename targets present, all 192 sources absent, registered deletion absent. |
| Frozen authority | `sha256sum docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md` | PASS — `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Independent specification review | APPROVED — `C0/I0/M0` | All reported findings were reproduced, corrected, and accepted after round 6. The fail-closed current-consumer scan covers Markdown, scripts, and configuration with exact history/negative exclusions. |
| Independent Python review | APPROVED — `C0/I0/M0` | All six review rounds were closed with focused mutation coverage for bounded Git and filesystem discovery, descriptor-safe reads, complete authority projections, and shared rendered-link parsing. |
| Controller gate convergence | VERIFIED | A fresh bounded final-tree repository-contract run completed with `failures=13`; no Task 8-owned section failed. Residual failures remain visible for their later owners. |
| Round-5 important findings | CLOSED | Bounded Git/discovery, rendered-link semantics, exact Spec-target validation, and bounded tracked service/read findings all have real gate-level regressions. |
| Round-6 important findings | CLOSED | The shared parser is the sole rendered-link occurrence authority used by the Spec/service gates; exact inline-comment and angle-destination mutations are GREEN. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| None | Work remains uncommitted; no commit or review evidence is claimed. |

## Rulings

- Migration 0003 is the structural execution authority and remains byte-identical.
- Migration 0002 is a read-only semantic witness; its two merges are not re-executed.
- Incidents remain a sibling of `catalog/`; there is no guide-root alternative.
- Meaningful frontmatter artifact IDs remain stable while only `ops-` subject path prefixes are removed.
- A separate Release document role and route are unnecessary; delivery evidence remains with Tasks, `CHANGELOG.md`, Git tags, artifact attestations, and applicable Runbooks.

## Deferred Items

- The 13 full-gate residual sections and nine inherited script references are routed to their owning Tasks 9–12; Task 8 introduced no exception for them.
- Shared index state contains exactly 192 `R100` entries inherent to the required native `git mv` commands until the implementation commit is created.
