---
title: "Infrastructure Tier Layout Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
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
automation and documentation. Use the existing root Compose application,
shared template, operations catalog and validation gates.

Technology: Docker Compose YAML, shell, Python unittest and the existing
Markdown/JSON document contracts. No new dependency or service registry.

Execution method is pending user selection: native execution in this session
with an independent final reviewer is recommended because the eighteen moves
and their cross-package paths must change together. If selected, invoke
`superpowers:executing-plans`. Subagent-driven execution instead invokes
`superpowers:subagent-driven-development`; serialize overlapping file owners.
Neither method begins before the user reviews this written plan.

## Dependencies

- The user approved the written specification on 2026-10-01. Its frontmatter
  remains draft for first registration; this does not negate the approval or
  invent a committed lifecycle transition. Apply normal transitions when
  registering subsequent lifecycle changes.
- Read the Spec and current repository instructions at execution start.
  Capture the actual base SHA and concurrent dirty paths; do not assume the
  research counts are still current. Preserve other work, especially SPEC-0182
  and SPEC-0193. Use an isolated execution branch/worktree if needed.
- Before implementation, create the package Task
  `tasks/tsk-0001-tier-layout-and-consistency.md` using the registered template.
  It owns baseline, RED/GREEN, acceptance receipts and review evidence.
- Runtime changes, remote publication and data operations are outside this
  plan's execution authorization. All Compose rendering uses `.env.example`.

### Global constraints

Keep service/project/container identities, images, commands, profiles,
healthchecks, ports, networks, secret references, resource settings and
persistent host/volume paths unchanged. Only the Spec's eighteen source-path
moves and Analytics tier labels may change in the resolved application model.
Keep dbt on PostgreSQL and SeaweedFS shared. Preserve frozen history.

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
4. W4: Run affected gates, independent review and evidence closure
   (acceptance 1 through 6).

### W1: Baseline and regression checks

Owner: implementation worker. Files: create
`tests/validation/test_infra_tier_layout.py`; read the eighteen Spec source
packages, root `docker-compose.yml`, `infra/common-optimizations.yml`,
POL-0078 and existing `tests/validation/test_compose_baseline_gates.py`.

Produces: the recorded baseline SHA, public model comparison inputs and a
small regression module consumed by W2. Temporary model files are not the
execution record; persist commands, comparison summaries and checksums in the
Task, never private rendered configuration.

- [ ] Capture full public model with
  `docker compose --env-file .env.example --profile '*' config --format json`.
  Capture HOME and affected profile selections using the exact POL-0078 HOME
  union and the profile names extracted from the eighteen source packages.
- [ ] Inventory Git-tracked package files and cross-package mount/build paths;
  record source contents/digests for moved configuration. Read path names only
  for private overrides; do not open their contents or silently migrate them.
- [ ] In the new test module define
  `compare_models(before: dict, after: dict, moves: dict[str, str]) -> list[str]`.
  It returns structural difference paths after applying the exact Spec move
  map only to source-path fields and the approved services' tier labels.
  Normalize JSON object ordering, not values, list contents or arbitrary text.
  Reuse existing parsing/model helpers where available.
- [ ] Add tests proving allowed relocations compare equal; changed volume
  device/name, removed helper service, changed profile/port and unknown path
  substitutions produce differences. Do not ignore the entire labels or
  volumes object. Keep this comparator test-local, not a new registry/gate.
- [ ] Add `TierLayoutTests` asserting the eighteen destinations, exact root
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

- [ ] Apply moves as one repository change. Update root includes, shared
  `extends.file` depths, build references and cross-package provisioning mounts
  (notably the shared mng-db runner used by Superset/dbt and other consumers).
- [ ] Set Analytics package labels to `hy-home.tier: analytics`. Preserve all
  other labels. Search `hy-home.tier`, its sanitized discovery form
  `hy_home_tier`, and old package paths in current tracked consumers; update
  only affected selectors, preserving their intended service membership.
- [ ] In `check-all-hardening.sh`, retain storage checks in `check_04_data`,
  move processing/BI/dbt checks into `check_12_analytics`, and add
  `12-analytics | analytics` to `run_tier`, help and all-tier execution.
  Update existing test paths; preserve every prior control and test assertion.
- [ ] Extend the regression module with the Analytics dispatch/failure fixture
  using the existing baseline-gate test pattern. Prove an intentionally broken
  Analytics control fails its tier check, then prove the actual tree passes.
- [ ] Update `.github/labeler.yml` path matching with the existing label scheme;
  this changes tracked configuration only and creates no remote label.
  Regenerate the existing projection with
  `bash scripts/operations/sync-tech-stack-versions.sh --write` after the
  renamed files are visible to its Git-tracked discovery. Review the index
  before staging; do not accidentally stage unrelated edits.
- [ ] Rerender the same public models/selections and call W1's comparator with
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

- [ ] Update tier tables/trees, storage versus processing roles and package
  links. Correct HOME count guidance, Observability selectors and
  `restic-offsite`; preserve classification and exact activation semantics.
- [ ] Align AD-0004's HOME/LAB and HA claims, AD-0012's old sub-tier wording and
  REQ-0005's current paths. Record the newly approved tier boundary in the ADR
  and maintain traceability without changing issued requirement identifiers.
- [ ] Update current Guide/Policy/Runbook files selected by references to the
  exact eighteen old package prefixes, including `implementation_services`
  fields. Existing subject IDs include 0017, 0019, 0022, 0024, 0025, 0026,
  0027, 0028, 0029, 0031, 0033, 0034, 0090, 0094 and 0097. Also update
  cross-package provisioning/backup references in subjects 0021 and 0032 and
  any current consumer discovered by the same bounded path search.
- [ ] Review residual hits with `git grep` across current tracked files.
  Keep dated research, frozen archives, test fixtures explicitly exercising
  retired routes and historical provenance unchanged. Record justified
  residuals in the Task; do not mass-replace every string in the repository.
- [ ] Run document/cross-reference and operations-catalog checks. Transfer
  category content before deleting indexes; no Stage 98 payload is created
  for these `infra/` navigation files.

### W4: Verification and closure

Owner: executor for checks and Task evidence, separate read-only reviewer for
semantic review. Consumes W1-W3 results and produces acceptance receipts.

- [ ] Run the commands below against the final diff; repair only scoped
  defects. Test new nontrivial logic and measure at least 80% of changed
  executable lines using existing coverage tooling, with exclusions explained.
- [ ] Have an author-independent reviewer compare the final diff to all six
  Spec criteria, the move map, label consumers and rollback boundary. Resolve
  material findings and rerun only affected checks after changes.
- [ ] Record each criterion's W unit, actual result and durable owner in
  `tasks/tsk-0001-tier-layout-and-consistency.md`. Mark runtime checks NOT_RUN;
  do not imply source validation proves mounted paths in running containers.
- [ ] Finish only after observed PASS for every source acceptance criterion.
  Prepare two coherent commit boundaries: package/config/test relocation and
  documentation alignment. Commit/push/merge only under applicable delivery
  authorization; do not mark this draft plan or implementation completed now.

## Risk and Rollback

Moving source mounts can affect future recreations even if current containers
continue running. Inventory source mounts and stop on a requirement for live
path reconciliation; arrange a separate approved operation rather than
restarting containers. Source-model equality permits only mapped paths and
Analytics tier labels; preserve all persistent storage identities.

Restore the relocation and its consumer references as one logical Git change.
Do not revert unrelated dirty paths, reset another worker's branch, remove
volumes or restore application data. If a review discovers a service-level
redesign need, return to Spec scope rather than hiding it in the migration.

## Verification

| Command/check | Expected result | Criteria |
| --- | --- | --- |
| W1 before/after model comparison and source-content checks | No unapproved delta | 1, 2 |
| `python3 -m unittest tests.validation.test_infra_tier_layout tests.validation.test_compose_baseline_gates` | Applicable tests PASS; opt-in runtime rehearsals remain explicit | 1, 2, 3 |
| `bash scripts/validation/validate-docker-compose.sh` | Public HOME/profile rendering and port checks PASS | 2, 3 |
| `bash scripts/hardening/check-all-hardening.sh 04-data 09-tooling 12-analytics` | Every retained/moved tier check PASS | 3 |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` | Projection matches source | 3 |
| `python3 scripts/validation/check-operations-catalog.py` | Existing global join PASS | 3, 4 |
| `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | No contract violations | 4 |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | Selected registered checks PASS | 3, 4, 5 |
| Independent read-only review and Task receipt | No unresolved material finding; criteria mapped to evidence | 5, 6 |

Do not enable `HYHOME_PG_REHEARSAL` or other live rehearsal flags. Run path-only
unit coverage for `test_mng_pg_init_sql.py` where available; its live database
rehearsal remains outside this scope. Hosted CI-only gates are NOT_RUN until a
separately authorized delivery supplies their results. A broad full-suite
rerun is not required unless changed-path routing or a new finding justifies it.

## Rulings

- Written Spec approval: user, 2026-10-01, including dbt's move from Tooling.
- Plan status: draft; user review and execution method selection pending.
- Default recommendation: native, serialized relocation with one independent
  final review. Documentation may be delegated once paths stabilize.
- Durable document rules and canonical package paths take precedence over
  generic skill output paths. No parallel plan/status ledger is introduced.
