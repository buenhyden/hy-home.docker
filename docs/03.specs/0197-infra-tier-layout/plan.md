---
title: "Infrastructure Tier Layout Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0197-PLAN-0001"
parent_ids:
- "SPEC-0197"
created: "2026-10-01"
---

# Infrastructure Tier Layout Implementation Plan

## Objective

Implement the user-approved [SPEC-0197](spec.md): twelve flat Data packages,
six flat Analytics packages including dbt, and consistent configuration,
automation and documentation. The subsequent user-requested Tooling/Communication/Laboratory extension
is tracked in W5 below; the user approved its written C move map on 2026-10-01.
The user approved the additional implementation sequence on 2026-10-01,
preserving native execution plus independent review. Use the existing root Compose application,
shared template, operations catalog and validation gates.

Technology: Docker Compose YAML, shell, Python unittest and the existing
Markdown/JSON document contracts. No new dependency or service registry.

The user approved the original W1–W4 Plan on 2026-10-01 and selected native execution in
this session with an independent final reviewer. `superpowers:executing-plans`
is the selected procedure; the eighteen moves and their cross-package paths
are implemented together. The Task owns observed execution and review results.

## Dependencies

- The user approved the written specification on 2026-10-01. Its frontmatter
  used draft for first registration; this did not negate the approval or
  invent a committed lifecycle transition. Apply normal transitions when
  registering subsequent lifecycle changes.
- Read the Spec and current repository instructions at execution start.
  Capture the actual base SHA and concurrent dirty paths; do not assume the
  research counts are still current. Preserve other work, especially SPEC-0182
  and SPEC-0193. Use an isolated execution branch/worktree if needed.
- Before implementation, create the package Task
  `tasks/tsk-0001-tier-layout-and-consistency.md` using the registered template.
  It owns baseline, RED/GREEN, acceptance receipts and review evidence.
- Original W1–W6 authorization excluded runtime changes, remote publication
  and data operations; W7 records the separately approved bounded delivery.
  W1–W6 Compose rendering uses `.env.example`.

### Global constraints

Keep service/project/container identities, images, profiles, healthchecks,
ports, networks, secret references, resource settings and persistent host/volume
paths unchanged. W1-W4 permit only the original eighteen source-path moves and
Analytics tier labels. W5 may use the amended Spec's exact additional path/label
allowlists and sole Conftest entrypoint token exception under the user-approved
amended implementation Plan. W6 adds its exact five source mappings and nine
platform-ops labels; only the tracked backup unit source-prefix token changes
outside Compose. Every other command/entrypoint token remains unchanged. Keep dbt on
PostgreSQL and SeaweedFS shared. Preserve frozen history.

### Review focus

1. A relative path resolves to the wrong existing file: W1/W2 compare mapped
   bind/build/config sources and file contents, not only syntax.
2. A tier label filter hides Analytics: W2 traces consumers and compares the
   selected service set before and after the approved label substitution.
3. The new tier bypasses hardening: W1/W2 test dispatch and failure when an
   Analytics control is deliberately violated in a temporary fixture.
4. A helper/provisioning service or opt-in selector disappears: W1/W2 compare
   complete service sets, dependencies, profiles and HOME selection.
5. A historical path is treated as a live reference: W3 reviews each residual
   path hit by ownership; archive/source-history references remain unchanged.

## Execution Sequence

1. W1: Capture the public baseline and establish focused regression checks
   (acceptance 1, 2, 3, 6).
2. W2: Move packages and update executable consumers atomically
   (acceptance 1, 2, 3).
3. W3: Align current documentation and navigation
   (acceptance 4, 6).
4. W4: Run affected gates and independent review for the original scope
   (acceptance 1 through 6); final package closure also requires W5.
5. W5: Investigate the three-tier extension, amend the concrete destination map
   and implementation sequence, then verify the approved additional relocation
   (acceptance 7 plus the applicable preservation and validation criteria).
6. W6: Rename the approved platform capability and reconcile all active consumers
   (acceptance8 plus preservation/validation criteria2–6); written Plan review approved.
7. W7: Deliver through protected main, reconcile the authorized runtime targets,
   and record actual operational completion separately from source acceptance.

### W1: Baseline and regression checks

Owner: implementation worker. Files: create
`tests/validation/test_infra_tier_layout.py`; read the eighteen Spec source
packages, root `docker-compose.yml`, `infra/common-optimizations.yml`,
POL-0078 and existing `tests/validation/test_compose_baseline_gates.py`.

Produces: the recorded baseline SHA, public model comparison inputs and a
small regression module consumed by W2. Temporary model files are not the
execution record; persist commands, comparison summaries and checksums in the
Task, never private rendered configuration.

- [x] Capture full public model with
  `docker compose --env-file .env.example --profile '*' config --format json`.
  Capture HOME and affected profile selections using the exact POL-0078 HOME
  union and the profile names extracted from the eighteen source packages.
- [x] Inventory Git-tracked package files and cross-package mount/build paths;
  record source contents/digests for moved configuration. Read path names only
  for private overrides; do not open their contents or silently migrate them.
- [x] In the new test module define
  `compare_models(before: dict, after: dict, moves: dict[str, str]) -> list[str]`.
  It returns structural difference paths after applying the exact Spec move
  map only to source-path fields and the approved services' tier labels.
  Normalize JSON object ordering, not values, list contents or arbitrary text.
  Reuse existing parsing/model helpers where available.
- [x] Add tests proving allowed relocations compare equal; changed volume
  device/name, removed helper service, changed profile/port and unknown path
  substitutions produce differences. Do not ignore the entire labels or
  volumes object. Keep this comparator test-local, not a new registry/gate.
- [x] Add `TierLayoutTests` asserting the eighteen destinations, exact root
  include coverage, package-local README presence and tier labels. Run
  `python3 -m unittest tests.validation.test_infra_tier_layout` before moving
  files: comparator cases pass; destination/layout cases fail for old paths.
  Record that RED result, with no intentionally failing delivery commit.

### W2: Atomic relocation and executable consumers

Owner: the same implementation worker; serialize changes to root Compose and
hardening. Consumes W1's baseline and move map. Produces a renderable new tree
with the same execution behavior.

Files: move the exact eighteen package directories listed in Spec; modify
`docker-compose.yml`, `scripts/hardening/check-all-hardening.sh`,
`.github/labeler.yml`, `infra/tech-stack.versions.json`,
`tests/validation/test_compose_baseline_gates.py`,
`tests/validation/test_mng_pg_init_sql.py`, and the W1 regression module.
Inspect the existing Observability label consumers before any scoped edit.

- [x] Apply moves as one repository change. Update root includes, shared
  `extends.file` depths, build references and cross-package provisioning mounts
  (notably the shared mng-db runner used by Superset/dbt and other consumers).
- [x] Set Analytics package labels to `hy-home.tier: analytics`. Preserve all
  other labels. Search `hy-home.tier`, its sanitized discovery form
  `hy_home_tier`, and old package paths in current tracked consumers; update
  only affected selectors, preserving their intended service membership.
- [x] In `check-all-hardening.sh`, retain storage checks in `check_04_data`,
  move processing/BI/dbt checks into `check_12_analytics`, and add
  `12-analytics | analytics` to `run_tier`, help and all-tier execution.
  Update existing test paths; preserve every prior control and test assertion.
- [x] Extend the regression module with the Analytics dispatch/failure fixture
  using the existing baseline-gate test pattern. Prove an intentionally broken
  Analytics control fails its tier check, then prove the actual tree passes.
- [x] Update `.github/labeler.yml` path matching with the existing label scheme;
  this changes tracked configuration only and creates no remote label.
  Regenerate the existing projection with
  `bash scripts/operations/sync-tech-stack-versions.sh --write` after the
  renamed files are visible to its Git-tracked discovery. Review the index
  before staging; do not accidentally stage unrelated edits.
- [x] Rerender the same public models/selections and call W1's comparator with
  the exact map. Require no unexpected difference and verify mapped source
  file contents; path-only edits are reviewed separately. Run the W1 tests
  and existing baseline tests: all applicable tests must pass.

### W3: Documentation and durable boundary

Owner: documentation worker after W2 paths stabilize. Consumes the verified
new layout; produces current navigation and architecture without old live
routes. Do not edit implementation files owned by W2 concurrently.

Files: `infra/README.md`, `infra/04-data/README.md`, new
`infra/12-analytics/README.md`, `infra/09-tooling/README.md`,
`infra/06-observability/README.md`, and each moved package's README.
Remove the seven old category indexes only after transferring their useful
content: analytics, cache-and-kv, lake-and-object, nosql, operational,
relational and specialized. The old lakehouse category has no README.

Durable files: `docs/01.requirements/0005-data-analytics.md`,
`docs/02.architecture/descriptions/0004-data-architecture.md`,
`docs/02.architecture/descriptions/0012-data-analytics-architecture.md` and
`docs/02.architecture/descriptions/0031-home-development-host.md`.
Allocate the next available ADR identity through the existing registry at
execution time for `data-storage-and-analytics-tier-boundary.md`; do not
reserve a guessed number or modify ADR-0039's retained engine decision.

- [x] Update tier tables/trees, storage versus processing roles and package
  links. Correct HOME count guidance, Observability selectors and
  `restic-offsite`; preserve classification and exact activation semantics.
- [x] Align AD-0004's HOME/LAB and HA claims, AD-0012's old sub-tier wording and
  REQ-0005's current paths. Record the newly approved tier boundary in the ADR
  and maintain traceability without changing issued requirement identifiers.
- [x] Update current Guide/Policy/Runbook files selected by references to the
  exact eighteen old package prefixes, including `implementation_services`
  fields. Existing subject IDs include 0017, 0019, 0022, 0024, 0025, 0026,
  0027, 0028, 0029, 0031, 0033, 0034, 0090, 0094 and 0097. Also update
  cross-package provisioning/backup references in subjects 0021 and 0032 and
  any current consumer discovered by the same bounded path search.
- [x] Review residual hits with `git grep` across current tracked files.
  Keep dated research, frozen archives, test fixtures explicitly exercising
  retired routes and historical provenance unchanged. Record justified
  residuals in the Task; do not mass-replace every string in the repository.
- [x] Run document/cross-reference and operations-catalog checks. Transfer
  category content before deleting indexes; no Stage 98 payload is created
  for these `infra/` navigation files.

### W4: Verification and closure

Owner: executor for checks and Task evidence, separate read-only reviewer for
semantic review. Consumes W1-W3 results and produces acceptance receipts.

- [x] Run the commands below against the final diff; repair only scoped
  defects. Test new nontrivial logic and measure at least 80% of changed
  executable lines using existing coverage tooling, with exclusions explained.
- [x] Have an author-independent reviewer compare the final diff to all six
  Spec criteria, the move map, label consumers and rollback boundary. Resolve
  material findings and rerun only affected checks after changes.
- [x] Record each criterion's W unit, actual result and durable owner in
  `tasks/tsk-0001-tier-layout-and-consistency.md`. Mark runtime checks NOT_RUN;
  do not imply source validation proves mounted paths in running containers.
- [x] Finish only after observed PASS for every source acceptance criterion.
  Prepare two coherent commit boundaries: package/config/test relocation and
  documentation alignment. Commit/push/merge only under applicable delivery
  authorization. Initial draft registration and subsequent formal lifecycle
  transitions remain distinct from the recorded source acceptance results.

### W5: Tooling, Communication and Laboratory extension

Owner: the same native executor; preserve the user's selected same-session
implementation plus independent final review. Evidence:
`tasks/tsk-0002-tooling-tier-reclassification.md`. The written C Spec amendment
was approved on 2026-10-01; the user then approved this concrete Plan extension
and preserved the existing execution method.
The approved twelve new moves and sixteen service labels are exactly the Spec's
additional placement tables, not another inferred inventory.

- [x] Inventory eighteen packages/twenty-seven identities, seven selected build
  definitions/eight built identities; record retain/move reasons and official roles.
- [x] Compare A/B/C; resolve independent draft findings; record user approval of C.

#### W5.1: Public baseline and regression contract

Files: `tests/validation/test_infra_tier_layout.py`; read all twelve moved
packages and the six retained packages, their selected Dockerfiles and root
Compose. Reuse `compare_models(before: dict, after: dict, moves: dict[str, str])
-> list[str]`; keep its signature and input-immutability guarantee. Replace the
Analytics-only label normalization with a fixed exact service-to-tier mapping
containing the original ten assignments and the sixteen approved additions.
The only non-path-field substitution is Conftest's complete expected entrypoint
`['/bin/sh', '/project/infra/09-tooling/conftest/run.sh']` to the same list with
`/project/infra/11-quality/conftest/run.sh`. Do not normalize arbitrary strings.

- [x] After SPEC-0198 W5 author/review and the already-requested W2-W5 Korean
  corrections finish, freeze all Operations writers for the relocation window.
  Keep their corrected bytes; do not restore original documents from Git.
- [x] Record current public full/HOME/affected-profile models using
  `docker compose --env-file .env.example --profile '*' config --format json`
  and the original W1 selection procedure. Record tracked source hashes and
  selected build context/Dockerfile/args/target/COPY/entrypoint inputs. List
  untracked/ignored names only; do not read or move private content. Stop on a
  source/destination collision rather than overwriting or deleting it.
- [x] Add `test_approved_reclassification_labels_and_conftest_entrypoint`:
  all sixteen exact new assignments and the exact Conftest token compare equal;
  inputs remain byte-equivalent. Add negative cases to the existing semantic
  drift test: unknown-service tier change, extra/changed Conftest argv token,
  changed non-Conftest entrypoint, profile/host-volume/image/build-arg drift.
- [x] Extend layout assertions for all twelve approved new destinations and six
  retained packages, absence of retired source directories, seven Quality
  packages, and exact root include coverage without duplicates. Retain the
  original Data/Analytics checks and certificate-script regression.
- [x] Run `python3 -m unittest tests.validation.test_infra_tier_layout` before
  implementing the moves: record intended new-case RED; existing cases remain
  passing. Implement only the bounded comparator extension and confirm its
  positive/negative tests pass while destination checks remain RED.

#### W5.2: Relocation and executable consumers

Files: twelve package directories in the approved Spec map;
`docker-compose.yml`, `scripts/hardening/check-all-hardening.sh`,
`scripts/validation/check-conftest-policy.sh`, `.github/labeler.yml`,
`infra/tech-stack.versions.json`, `tests/validation/test_infra_tier_layout.py`,
`tests/validation/test_compose_baseline_gates.py`,
`tests/validation/test_tech_stack_version_contract.py`.
Inside moved Conftest, update only the approved entrypoint in
`infra/11-quality/conftest/docker-compose.yml` and policy prefix in `run.sh`.
All other executable source edits require a demonstrated mapped-path need.

- [x] Move tracked source packages intact; keep nested SurrealDB and all helper
  jobs. Update root includes and exactly sixteen tier labels. Verify relative
  extends/build/bind/provisioning paths; preserve host paths, environment keys,
  profile names, network/volume/service identities and image/package pins.
- [x] Transfer existing hardening checks without loss: RedisInsight to
  `check_04_data`, Dozzle to `check_06_observability`, Open Notebook/SurrealDB to
  `check_08_ai`; SonarQube/WireMock/Pact plus Mailpit to `check_11_quality`.
  Keep Stalwart checks in10, all existing Analytics checks in12. Retained
  `check_09_tooling` checks existence of its five retained Compose packages;
  do not return vacuous success after moving every previous assertion away.
- [x] Replace retired `11-laboratory|laboratory|lab` hardening routes/help/default
  dispatch with `11-quality|quality`. These are hardening CLI names, not Compose
  profile changes. Change labeler area11 to `area/infra/quality`; do not create
  remote labels or modify unrelated area rules.
- [x] Extend fixture regression coverage before changing dispatch: Quality must
  reject non-loopback WireMock, public-read Pact, and missing/non-native Mailpit
  health. Reuse `MailpitHealthContractTests` for its existing bad-health cases,
  moving its fixture and invocation to Quality. Destination-tier fixtures must
  reject missing Dozzle OIDC, removed RedisInsight SSO and missing Open Notebook
  password-file controls; keep unrelated template/control checks passing.
  Add these bounded checks to the existing tier-layout test module, not a new
  framework or registry. Verify the old hardening alias fails explicitly.
- [x] Update existing test source paths for moved MLflow/Pact/Conftest/Dozzle
  and Mailpit. Keep opt-in runtime rehearsal switches off. Source-only test
  fixtures may move, but retained-route/history fixtures remain unchanged.
- [x] Make only owned moved files Git-visible and run the existing version
  projection writer `bash scripts/operations/sync-tech-stack-versions.sh --write`.
  Re-render the same public selections; require zero unexpected comparator
  differences. Verify tracked file membership/content against baseline, with
  exact path/label/document changes separately explained.

#### W5.3: Durable owners and Operations handoff

Files: `infra/README.md`; tier indexes04/06/08/09/10/12 and new
`infra/11-quality/README.md`; each moved package README. Transfer useful content
from `infra/11-laboratory/README.md` before removing that navigation file.
Current requirements: `docs/01.requirements/0010-tooling.md`,
`0011-communication.md`, `0012-laboratory.md` in that directory; preserve their
issued obligation identities. Current descriptions under
`docs/02.architecture/descriptions/`: `0004-data-architecture.md`,
`0006-observability-architecture.md`, `0008-ai-architecture.md`,
`0009-tooling-architecture.md`, `0010-communication-architecture.md`,
`0011-laboratory-architecture.md`, `0012-data-analytics-architecture.md`,
`0024-tooling-optimization-hardening-architecture.md`,
`0025-laboratory-optimization-hardening-architecture.md`,
`0031-home-development-host.md`.

- [x] Record the new capability boundary in
  `docs/02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md`,
  parent `AD-0009`. ADR allocation is currently high-water45/next46; recheck at
  creation rather than overwriting a concurrent allocation. Update only the
  corresponding registry cursor, decision index and exact ADR expectation in
  `tests/lib/document_governance/test_taxonomy.py`. Preserve ADR0045's original
  Data/Analytics decision and every accepted historical ADR body.
- [x] Align current descriptions/requirements and package indexes to approved
  capability ownership. AD0009 remains the logical platform/verification owner;
  AD0011 and REQ0012 retain their optional administration/research obligations
  across destination tiers, rather than silently losing those requirements.
  Clarify data-quality versus software-quality, Dozzle's leaf Compose, shared
  profiles across tiers, and existing internal-only Stalwart operation.
- [x] Reconcile current Stage05 implementation bindings/links and tier references
  selected by the exact twelve old prefixes, including subjects0061/0062/0063/
  0064/0066/0070/0072/0073/0074/0076/0080/0084/0088/0089/0092/0093/0095 and all
  discovered current consumers. Update four Operations indexes and system0099
  Guide/Runbook where affected. Preserve every reviewed body correction, ID and
  role. Operations prose and all READMEs are Korean; structural tokens remain
  unchanged. Do not rename role files or weaken their registered templates.
- [x] Refresh only the marked `current-service-inventory` projection in
  `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`
  using existing `scripts.lib.document_governance.operations_catalog.render_service_inventory`.
  Preserve surrounding dated research and recorded operating classifications.
- [x] Classify residual old-path hits: update active consumers; retain explicit
  history/retired-route fixtures/frozen archives. Record old→new path crosswalk
  in Task0002 and SPEC-0198's integration Task so dated W1 manifests are not
  rewritten as though the relocation preceded their observations.
- [x] Hand off stable new paths to SPEC-0198 W6/W7 authors only after native
  relocation/source checks and independent review. They resume full semantic
  body audits on the new paths; a path update does not replace those audits.

#### W5.4: Verification, review and integrated closure

- [x] Run the existing focused tests:
  `python3 -m unittest tests.validation.test_infra_tier_layout tests.validation.test_compose_baseline_gates tests.validation.test_tech_stack_version_contract`.
  Require all static tests PASS; explicitly retain runtime rehearsals as SKIPPED.
  Run affected hardening04/06/08/09/10/11-quality/12 and the original baseline
  suite. Record any existing unsupported static helper separately, not as PASS.
- [x] Run the existing Compose public-input validator, version-projection
  `--check`, operations catalog, metadata, links/language and taxonomy tests.
  Measure at least80% changed executable-line coverage for comparator/hardening
  additions using the original stdlib/Bash trace approach. Pure relocation,
  comments and prose do not justify synthetic tests or denominator manipulation.
- [x] Have an independent read-only reviewer compare exact source hashes,
  approved maps, negative regressions, retained controls and document ownership.
  Resolve material findings with scoped rechecks; no live acceptance inference.
- [x] After all SPEC-0198 writers and language fixes finish, stage owned final
  bytes and freeze repository/index mutation before the combined
  `python3 scripts/validation/run-ci-gate.py --profile changed`. Do not rerun
  the20-minute gate against a changing snapshot. Record source acceptance1–7
  across Task0001/Task0002; runtime/build/deploy/recovery/remote work remains
  NOT_RUN. No package completion until every required source criterion passes.

### W6: Platform Operations naming amendment

Owner: the same native executor, followed by independent read-only review.
The user approved the written naming amendment on2026-10-01. This additional
Plan was approved on2026-10-01; preserve the selected execution method.
Evidence stays in Task0002. SPEC0198 W6/W7 body writers remain paused until the
new paths pass scoped source validation and review. No new Task or registry.
Acceptance:8, with preservation/validation criteria2–6. The approved Spec's
five destinations and nine identities are the exact mapping, not a wildcard
permission to rename generic tooling references.

W6 reuses the five existing review-focus classes: mapped source/content equality,
exact label membership, retained hardening, unchanged helpers/profiles, and
historical-reference preservation. Its additional backup-unit risk is pinned by
`test_platform_ops_layout_and_backup_unit` plus whole-unit baseline comparison.

#### W6.1: Baseline and naming regressions

Files: `tests/validation/test_infra_tier_layout.py`; read the five source package
trees, root Compose, `infra/common-optimizations.yml`, POL0078 and the tracked
Restic unit `infra/09-tooling/restic/systemd/hyhome-backup.service`.
Interface: reuse `compare_models(before: dict, after: dict, moves: dict[str, str])
-> list[str]` and the existing `TIER_ASSIGNMENTS`; no new production helper.

- [x] Snapshot current public all-profile model and HOME plus the union of the
  five packages' profiles with inherited configuration variables excluded.
  Record tracked file names/hashes and source inputs; inspect untracked/ignored
  names only and stop on collisions. Reconfirm OpenTofu's inline Dockerfile,
  context/args/target and credential/workspace mount declarations without reads
  of private mounted files. Preserve the previously reviewed C source state.
- [x] Add `test_platform_ops_labels_preserve_profiles`: create the exact nine
  Spec identities with old `tooling` labels and preserved profiles; expected
  copies differ only by `platform-ops`. Assert equality and input immutability;
  assert a changed `tooling` profile or an unknown service label produces a
  nonempty difference. Run `python3 -m unittest
  tests.validation.test_infra_tier_layout.ModelComparisonTests` and record the
  new positive case failing before extending the exact label map.
- [x] Add `test_platform_ops_layout_and_backup_unit`: assert five packages at
  `infra/09-platform-ops`, nine expected labels, no old09 directory, and unique
  root include coverage. Assert the tracked backup unit's exact ExecStart is
  `/home/hyunyoun/data/hy-home.docker/infra/09-platform-ops/restic/bin/hyhome-backup.sh`
  and that its mapped repository target exists. Do not execute the unit.
- [x] Add `test_platform_ops_hardening_dispatch`: temporary source fixture copies
  the existing hardening script/library, image projection and five package
  Compose files. Both `09-platform-ops` and `platform-ops` must pass; removing
  Registry Compose must fail. Old `09-tooling` and `tooling` hardening aliases
  must exit2. Existing Compose `tooling` activation must remain valid.
  Run the existing module to witness new naming cases RED before relocation.

#### W6.2: Atomic naming change and executable consumers

Files: rename `infra/09-tooling` to `infra/09-platform-ops` with all five packages;
`docker-compose.yml`, `.github/labeler.yml`,
`scripts/hardening/check-all-hardening.sh`, `infra/tech-stack.versions.json`,
`tests/validation/test_infra_tier_layout.py`,
`tests/validation/test_compose_baseline_gates.py`,
`tests/validation/test_tech_stack_version_contract.py`,
`tests/lib/document_governance/metadata/test_heading.py`.

- [x] Extend the existing comparator label map for exactly `opentofu`,
  `terrakube-api`, `terrakube-ui`, `terrakube-executor`, `registry`, `renovate`,
  `restic`, `restic-offsite`, `backup-sqlite-export` -> `platform-ops`. Preserve
  all previous mappings and the sole Conftest whole-entrypoint exception.
  Confirm comparator GREEN while physical naming cases still fail.
- [x] Move tracked packages/index intact, update five Compose label anchors and
  root include prefixes. Preserve all profile/identity/image/network/volume/
  secret/host-path fields. Only change the tracked backup unit's exact old
  ExecStart source prefix; compare the remainder with its baseline byte-for-byte.
  Preserve Renovate unit bytes, timer names/schedules and all command arguments.
- [x] Rename hardening function to `check_09_platform_ops`, tier text/default
  dispatch to09-platform-ops, accepted aliases to `09-platform-ops|platform-ops`,
  and its five existence-check prefixes. Change labeler key to
  `area/infra/platform-ops` and glob to `infra/09-platform-ops/**/*`.
  Update current path fixtures in the listed tests; preserve retired-route
  strings in metadata/profile.py and frozen archive/retention fixtures.
- [x] Stage only owned moved paths so existing Git-driven projections see them.
  Run `bash scripts/operations/sync-tech-stack-versions.sh --write`, then
  `--check`. Re-render full/HOME/affected public models: zero unexpected model
  differences, identical service selections and unchanged image tags.
  Compare every tracked source file against its mapped baseline; outside
  README/Compose, only the exact backup-unit path token may differ.
- [x] Run `python3 -m unittest tests.validation.test_infra_tier_layout
  tests.validation.test_compose_baseline_gates
  tests.validation.test_tech_stack_version_contract
  tests.lib.document_governance.metadata.test_heading` as one command.
  Require static cases PASS and keep opt-in runtime tests explicitly SKIPPED.

#### W6.3: Naming owners, historical preservation and operational handoff

Files: `infra/README.md`, new tier and five package READMEs,
`infra/11-quality/README.md`, `infra/06-observability/grafana/README.md`,
`scripts/README.md`; REQ0010; AD0004/0009/0024/0031; existing uncommitted ADR0046;
all four Stage05 indexes and GDE0099; current Stage05 subject paths0021,0060,
0061,0062,0063,0064,0065,0066,0068,0069,0082,0083,0086,0092,0093,0095,0098
where existing files actually reference the old capability/path. Also inspect
POL0006 and the marked current inventory in Stage90 research m0021. Preserve
all issued IDs, filenames and body corrections from SPEC0198.

- [x] Explain Platform Operations' IaC/artifact/dependency/backup scope and
  exclusions in the existing owners; preserve REQ0010's Quality obligations.
  Update active path, title, tier and hardening references selectively. Keep
  generic tooling terms and the `tooling` Compose profile. Stage05/README prose
  is Korean; Spec/Plan/Task and architecture/requirements prose is English.
- [x] Document the backup unit refresh requirement in the existing backup
  Runbook/README: a copied/installed unit can still reference the old path.
  Require a separately approved exact unit refresh/daemon-reload handoff before
  relying on the next scheduled backup after delivery. Do not execute host
  unit/timer commands, trigger catch-up jobs or claim installed state is fixed.
- [x] Coordinate RUN0098 with SPEC0182: recheck the scoped worktree/main status
  and diff immediately before any path-only edit/staging; stop on concurrent
  owner changes. Preserve its dated rehearsal payload and do not edit SPEC0182.
  SPEC0198 W7 retains ownership of separate semantic corrections.
- [x] Update only the existing current inventory via
  `render_service_inventory(root: pathlib.Path) -> str` after mapping authored
  identity paths. Snapshot prefix/suffix around the two exact marker strings,
  replace only their enclosed projection, and verify outside bytes unchanged.
  Recompute boundaries after any path replacement; never reuse stale offsets.
  Treat any historical link repair as a separate exact source-revision change.
- [x] Trace all old-prefix hits with Git searches that include hidden files and
  extensionless/systemd sources. Classify active consumers versus accepted ADRs,
  retired routes, archives and dated evidence. Preserve historical decisions;
  pin broken historical links to their actual source revisions, not new paths.
  Record the exact five-prefix crosswalk in Task0002 and reference it from the
  SPEC0198 integration Task without rewriting dated W1 audit manifests.

#### W6.4: Scoped review and combined completion

- [x] Run hardening with `09-platform-ops` and the already affected tiers;
  `bash scripts/validation/validate-docker-compose.sh`; version `--check`;
  `python3 scripts/validation/check-operations-catalog.py`; scoped metadata,
  document links/language and `git diff --check`. Preserve known historical-link
  warnings and unsupported infra-helper evidence rather than calling them PASS.
- [x] Reuse existing stdlib/Bash trace coverage for any new executable checker
  logic; require at least80% changed executable-line coverage. Pure relocation
  and prose do not create synthetic coverage obligations.
- [x] Independent read-only reviewer checks five mapped package inventories,
  nine label assignments, unchanged selectors/data, backup-unit token exception,
  old-alias rejection, retained checks, historical bytes and all current owners.
  Resolve material findings with scoped rechecks before final-path handoff to
  SPEC0198 W6/W7 authors. No live/runtime acceptance is inferred.
- [x] After remaining SPEC0198 writers/review finish, stage owned final bytes and
  freeze repository/index mutation before the single combined
  `python3 scripts/validation/run-ci-gate.py --profile changed`. Map acceptance8
  to this evidence in Task0002; criteria1–7 retain prior receipts and final checks.
  Commit boundaries remain coherent source/test relocation and documentation/
  projection alignment; actual commits/publication require delivery authority.
  Do not reset other work, clean worktrees, push or merge as part of W6
  source implementation; W7 owns the later authorized delivery.

### W7: Authorized delivery and operational application

The user's subsequent2026-10-01 instruction authorizes this follow-on work;
it supersedes the original no-publication/no-runtime limits only here.
Task0002 owns actual receipts. Existing source acceptance remains unchanged.

- [x] Record independent source/security review, frozen changed-gate PASS,
  remote protection, live identities/images/mounts and old-source config hashes.
- [ ] Register legal lifecycle transitions, publish the reviewed branch through
  a main PR, require hosted checks, and preserve the original planning drafts
  through their exact recovery commit before synchronizing the main checkout.
- [ ] Preserve public old bind-source bytes for target-only rollback. After
  main integration, recreate master, volume, filer and S3 in that order, then
  Registry, Dozzle and RedisInsight individually with no dependencies, build,
  pull, volume renewal or optional-profile startup. Wait for existing health
  checks and stop on failure. Match captured image IDs and every persistent
  mount, including S3's anonymous data volume; verify the other five moved
  running containers remain unchanged. Dozzle retains its observed v11.1.0
  through an explicit temporary image override; its prior v11.1.1 source gap
  is not an upgrade authorization. Independent runtime review accepted this
  seven-target scope and preservation contract.
- [ ] Apply only the installed Restic ExecStart source-prefix change after
  confirming the new main target exists and the captured unit hash matches.
  Preserve host-specific unit settings and timer state; validate the unit and
  daemon-reload without starting backup. Root authentication is currently
  unavailable; do not bypass it or claim this step passed without observation.
- [ ] Record container health, exact image/mount preservation, installed-unit
  verification and hosted delivery evidence. Complete SPEC0197/0198 only when
  required work is actually done; verify SPEC0194 is already completed.
  Commit final receipts through the same protected PR process, synchronize
  main/origin/main, and remove only the fully delivered clean branch/worktree.

Rollback is target-only: use the captured image, previous tier and preserved
public source bindings if a recreation fails; retain all existing volumes and
secret references. No data restore or broad stack restart. Before changing the
installed unit preserve its original bytes; restore only that unit on validation
failure, reload systemd and preserve the timer. Task0002 records exact prepared
paths/hashes and outcomes. A missing host privilege blocks that step only.

## Risk and Rollback

For W1–W6 source implementation, moving source mounts can affect future
recreations even if current containers continue running. Inventory source mounts
and stop on a requirement for live
path reconciliation; arrange a separate approved operation rather than
restarting containers. Source-model equality permits only the exact approved
Spec path/label allowlists and its sole Conftest entrypoint token exception.
The C destination design and amended implementation Plan are approved. Preserve all persistent
storage identities and other command/entrypoint tokens.

Restore the relocation and its consumer references as one logical Git change.
Do not revert unrelated dirty paths, reset another worker's branch, remove
volumes or restore application data. If a review discovers a service-level
redesign need, return to Spec scope rather than hiding it in the migration.

## Verification

| Command/check | Expected result | Criteria |
| --- | --- | --- |
| W1/W5 before/after model comparison and source-content checks | No unapproved delta | 1, 2, 7 |
| `python3 -m unittest tests.validation.test_infra_tier_layout tests.validation.test_compose_baseline_gates` | Applicable tests PASS; opt-in runtime rehearsals remain explicit | 1, 2, 3 |
| `bash scripts/validation/validate-docker-compose.sh` | Public HOME/profile rendering and port checks PASS | 2, 3 |
| `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 09-platform-ops 10-communication 11-quality 12-analytics` | Every retained/moved tier check PASS | 3, 7 |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` | Projection matches source | 3 |
| `python3 scripts/validation/check-operations-catalog.py` | Existing global join PASS | 3, 4, 7 |
| `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | No contract violations | 4 |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | Selected registered checks PASS | 3, 4, 5, 7 |
| Independent read-only review and Task receipt | No unresolved material finding; criteria mapped to evidence | 5, 6, 7 |

Do not enable `HYHOME_PG_REHEARSAL` or other live rehearsal flags. Run path-only
unit coverage for `test_mng_pg_init_sql.py` where available; its live database
rehearsal remains outside this scope. Hosted CI-only gates are NOT_RUN until a
separately authorized delivery supplies their results. A broad full-suite
rerun is not required unless changed-path routing or a new finding justifies it.

Source acceptance checkpoint, 2026-10-01: all source/document work units and independent reviews accepted; final `python3 scripts/validation/run-ci-gate.py --profile changed` exit0. At that checkpoint the reviewable packet was staged but uncommitted. Later authorized delivery and runtime reconciliation are tracked in SPEC0197 Plan W7 and Task0002; source acceptance does not substitute for those observations. Detailed outcomes, earlier failed attempts and remaining implementation limits are preserved in the canonical Tasks.

## Rulings

- Written Spec approval: user, 2026-10-01, including dbt's move from Tooling.
- Initial Plan registration used draft; original W1–W4 native execution approved on
  2026-10-01. C Spec and W5 Plan approved on the same date, preserving the selected method.
- Selected method: native, serialized relocation with one independent final
  review. Original implementation and documentation were performed in this
  session; the additional W5 source migration is implemented and independently accepted.
  Naming W6 implementation, scoped checks and independent review are complete;
  combined integration evidence remains tracked in Task0002.
- Durable document rules and canonical package paths take precedence over
  generic skill output paths. No parallel plan/status ledger is introduced.
