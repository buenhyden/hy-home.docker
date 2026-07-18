---
status: active
artifact_id: plan:2026-07-18-target-surface-contract-convergence
artifact_type: plan
parent_ids:
  - spec:133-target-surface-contract-convergence
---

# Target Surface Contract Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to execute this Plan task by task.
> Use `superpowers:executing-plans` for controller-side progress tracking.
> Every implementation step uses checkbox (`- [ ]`) syntax.

**Goal:** Converge the tracked `.github`, `archive`, `examples`, `infra`,
`projects`, `scripts`, `secrets`, and `tests` corpus on explicit native,
README, typed-document, archive, runtime, CI, and QA contracts; retire the
approved deprecated InfluxDB 2 implementation and unconsumed duplicates; and
close the work with independently reviewed evidence.

**Architecture:** Stage 99 remains the document-family and migration-contract
owner. A pinned corpus manifest classifies the 422 baseline target paths plus
direct-impact paths before mutation. Existing metadata and corpus-lifecycle
validators gain path-selected content-archive and SDLC-archive profiles,
binary-safe manifest generation, and reviewed-wave enforcement. A focused
target-surface validator owns only cross-surface invariants that do not belong
to those general validators. Existing repository-contract, local-QA,
pre-commit, Compose, and GitHub workflow owners call the focused checks.

**Tech Stack:** YAML 1.2, Markdown/CommonMark, Python 3.12, PyYAML, unittest,
Bash, Docker Compose, GitHub Actions, actionlint, yamllint, ShellCheck,
Hadolint, pre-commit, Graphify, and Git.

## Global Constraints

- After the planning commit, keep the primary checkout on `main`. Execute only
  in `.worktrees/target-surface-contract-convergence` on branch
  `codex/target-surface-contract-convergence`.
- The immutable classification baseline is
  `32c40e11747bc0bd03789c24861d2e5d60c0e999`. The target wave covers every
  tracked path under the eight target roots plus direct consumers named here.
- Use manifest-first classification. No delete, archive, merge, or replacement
  occurs until its row records consumers, preservation, rollback, and reviews.
- Preserve topic-specific README prose. The 75 baseline READMEs already match
  exactly one profile and contain the six core headings; do not bulk-rewrite
  compliant files or invent optional sections.
- Keep GitHub-native Markdown, workflow YAML, MDX, Compose, JSON, TOML, shell,
  Python, binary, and static assets in native schemas. Do not inject repository
  frontmatter into unsupported/native files.
- Keep `artifact_type: archive` as the semantic type while selecting
  `content-archive` for root `archive/**` and `sdlc-archive` for
  `docs/98.archive/**`.
- Git commit/blob provenance is the default preservation route. Only approved
  audit, legal, or evidence-preserve snapshots carry checksum metadata.
- Remove current deprecated implementations and active compatibility claims
  only after consumer proof. Preserve truthful historical evidence, standards
  prose, migration tests, and negative fixtures.
- The runtime-definition change is limited to removing the InfluxDB 2 server
  and unused v2-only consumers. Retain InfluxDB 3 Core. Do not start services,
  migrate live data, deploy, release, or change remote resources.
- Never inspect, render, log, or record secret values. Under `secrets/**`, use
  tracked path and metadata evidence only. Persist no rendered Compose output.
- Tracked workflow definitions may change. Remote branch protection, required
  contexts, environments, releases, secrets, and Actions state are read-only.
- Use TDD for every parser, selector, validator, generator, and QA-routing
  behavior. Record the exact RED failure before the minimal GREEN change.
- Execute T-TSC-001 through T-TSC-006 serially. Each task gets a fresh
  implementer, fresh specification reviewer, and distinct quality reviewer.
  Fix Critical and Important findings in separate commits and re-review.
- Create at least one logical Conventional Commit per task. Keep material
  review remediation separately reviewable.
- Never run `pre-commit run --all-files` directly. T-TSC-006 alone may call the
  approved wrapper from an initially clean linked worktree with explicit paths.
- Refresh Graphify after code changes when available. Its `f8a72211` report is
  advisory; corroborate against tracked Stage 00/03/04/90 owners.

## Overview

Task 1 creates the archive/profile/wave foundation and exact manifest. Task 2
fixes the copyable sample Service and phantom Storybook gitlink claims without
rewriting compliant READMEs. Task 3 converts the root content file into a
verified tombstone. Task 4 removes InfluxDB 2 and direct consumers and two
proven duplicates. Task 5 activates regression, QA, Compose, and workflow
contracts. Task 6 reconciles canonical research/audit/generated evidence,
performs whole-branch reviews and controlled QA, and closes the chain.

Actual commands, results, reviews, commits, deviations, and deferrals belong
in `docs/04.execution/tasks/2026-07-18-target-surface-contract-convergence.md`.

## Context and Inputs

At baseline, the target corpus has 422 tracked paths and 75 READMEs. Automated
profile/heading validation covered all 75; manual topic-content inspection
covered 74 and Task 2 explicitly inspects the remaining file before any README
claim is promoted. All 75 currently match one profile and the common navigation
envelope, but the sample Service uses stale headings. Two Storybook READMEs,
two scripts, and `.prettierignore` special-case a nonexistent
`projects/storybook/mcp` gitlink.
The root archive file lacks a typed profile/provenance envelope. The lifecycle
generator decodes every selected blob as UTF-8, which cannot safely classify
the target's binary/native files.

InfluxDB 3 Core is current, but an InfluxDB 2 definition, v2-only example
variables, unconsumed client dependency, unused k6/Locust org/bucket wiring,
and dual-generation active documentation remain. OpenSearch and SeaweedFS each
have one byte-identical duplicate with different consumer reality. CI has 15
local jobs; the last separately observed remote state had 12 required contexts.
Local and remote evidence remain explicitly separate.

Canonical inputs:

- `docs/03.specs/133-target-surface-contract-convergence/spec.md`
- `docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md`
- `docs/99.templates/support/document-metadata-profiles.yaml`
- `docs/99.templates/support/document-corpus-migration-contract.yaml`
- `docs/99.templates/support/frontmatter-contract.md`
- `docs/99.templates/support/readme-profile-contract.md`
- `docs/99.templates/support/archive-retention-contract.md`
- `docs/99.templates/support/corpus-migration-contract.md`
- `scripts/validation/check-document-metadata.py`
- `scripts/validation/check-document-corpus-lifecycle.py`
- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/validate-docker-compose.sh`
- `.github/workflows/ci-quality.yml`
- the canonical July 5 research and audit packs.

Official evidence and retrieval dates remain owned by Spec 133 and the
canonical research pack. Implementation uses the cited official InfluxDB 3,
Docker Compose, GitHub Actions, CommonMark, YAML, JSON Schema, pre-commit,
NIST retention, Git object, and OWASP secret/logging contracts.

## Goals and Non-goals

### Goals

- Register distinct content/SDLC archive profiles, templates, fields, and
  provenance validation under one semantic archive type.
- Pin and classify the complete corpus through a deterministic binary-safe
  manifest before mutation.
- Bind frontmatter and README sections to current profiles/consumers without
  flattening topic prose.
- Make the sample Service instantiate the current Service contract and remove
  false Storybook gitlink exceptions.
- Remove InfluxDB 2 and all unused v2-only active consumers while preserving
  one source-only InfluxDB 3 Core contract.
- Remove only the unreferenced OpenSearch `.example` and unmounted SeaweedFS
  active copy, retaining the mounted file/scaffold.
- Add deterministic target-surface and static workflow/QA regressions.
- Reconcile research, audit, generated inventories, Stage 04 evidence,
  reviews, and logical commits with final observed state.

### Non-goals

- Live data/query migration, service startup, deployment, backup, or release.
- Activating SeaweedFS security or changing unrelated Compose runtime.
- Reading secret values or changing remote GitHub resources.
- Rewriting compliant READMEs, native files, or historical evidence outside
  direct current-truth conflicts.
- Treating Graphify, remote observations, or static render as live proof.

## Work Breakdown

| Task | Logical unit | Acceptance | Primary gate |
| --- | --- | --- | --- |
| T-TSC-001 | Archive, metadata, wave, and manifest foundation | VAL-133-001/002 | focused metadata/lifecycle tests |
| T-TSC-002 | README, typed example, and Storybook cleanup | VAL-133-003 | README/profile/target fixtures |
| T-TSC-003 | Root content archive provenance migration | VAL-133-004 | archive/provenance validation |
| T-TSC-004 | Deprecated runtime and duplicate disposition | VAL-133-005/006 | absence scans and static Compose |
| T-TSC-005 | Validator, QA routing, and static CI enforcement | VAL-133-007 | unit/lint/repository gates |
| T-TSC-006 | Research, audit, generated evidence, and closure | VAL-133-008 | freshness, reviews, wrapper |

### Acceptance Map

| ID | Required outcome |
| --- | --- |
| VAL-133-001 | The pinned target manifest covers each selected baseline path exactly once and remains binary-safe and deterministic. |
| VAL-133-002 | Content and SDLC archive paths select distinct profiles/templates while preserving semantic `artifact_type: archive` and valid provenance. |
| VAL-133-003 | All retained target READMEs remain exact-one and the sample Service and Storybook surfaces match current consumer reality. |
| VAL-133-004 | The root Windows note is a valid Git-history content tombstone with no stale active command body. |
| VAL-133-005 | InfluxDB 2 source and active direct consumers are absent and InfluxDB 3 source/docs render consistently. |
| VAL-133-006 | Only the consumer-proven OpenSearch and SeaweedFS duplicates are removed; retained files/scaffold remain honest. |
| VAL-133-007 | Focused target, workflow, changed-path QA, repository, and static Compose regressions fail closed with safe diagnostics. |
| VAL-133-008 | Canonical research/audit/generated evidence, Task ledger, controlled QA, and independent task/branch reviews agree with final state. |

### Subagent-Driven Protocol

For each task, a fresh implementer receives its exact base, allowed/prohibited
paths, RED and GREEN commands, commit message, rollback, and evidence fields.
The implementer self-reviews and commits. A new specification reviewer examines
`BASE..HEAD` against Spec 133 and this Plan; a different quality reviewer then
examines correctness, security, maintainability, tests, and scope. Findings get
a bounded remediation commit and both reviews repeat. Task 6 ends with fresh
whole-branch reviews over
`32c40e11747bc0bd03789c24861d2e5d60c0e999..FINAL_HEAD`.

### T-TSC-001: Archive, Metadata, Wave, and Manifest Foundation

**Files:** modify
`docs/99.templates/support/{document-metadata-profiles.yaml,document-corpus-migration-contract.yaml,frontmatter-contract.md,common-document-contract.md,readme-profile-contract.md,archive-retention-contract.md,corpus-migration-contract.md,README.md}`;
`docs/99.templates/templates/common/{archive.template.md,README.md}`;
`docs/99.templates/templates/README.md`;
`docs/00.agent-governance/rules/{documentation-protocol.md,stage-authoring-matrix.md,task-checklists.md}`;
`scripts/validation/{check-document-metadata.py,check-document-corpus-lifecycle.py}`;
and `tests/validation/{test_document_metadata.py,test_document_corpus_lifecycle.py}`.
Create `docs/99.templates/templates/common/content-archive.template.md`,
`docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml`
and its generated summary; update
`docs/90.references/data/governance/document-corpus-lifecycle/README.md`.

The wave registry uses baseline `32c40e11747bc0bd03789c24861d2e5d60c0e999`,
the eight `source_roots`, an exact `direct_source_paths` list, and advisory
enforcement. Manifest schema v2 keeps the v1 top-level fields
`schema_version`, `wave`, `baseline_commit`, `generated_by`, `enforcement`, and
`entries`. Each v2 row has the existing fields except that `artifact_type` is
replaced by nullable `artifact_type_before` and `artifact_type_after`, and the
required `surface_class` enum is `native-platform`, `generated-output`,
`readme`, `typed-example`, `runtime`, `configuration`, `executable-script`,
`test-fixture`, `secret-metadata`, `content-archive`, or
`unsupported-static`. All other dispositions, evidence fields, verdict values,
ordering, and destructive gates remain v1-compatible. Foundation v1 remains
valid. Binary/native rows use Git mode/blob metadata without UTF-8 body decode;
their artifact types may be null. The Windows row transitions
`artifact_type_before: null` to `artifact_type_after: archive`.

`generate-manifest`, `check-manifest`, `generate-summary`, `check-summary`,
`check-promoted`, and `check-archive` accept `--wave
target-surface-convergence`. `generate-manifest` expands `source_roots` with
`git ls-tree -r` at the pinned baseline, unions the exact direct paths,
deduplicates and sorts by `source_path`, and writes only with explicit
`--output`. The wave registry requires exact `manifest_path` and `summary_path`.
When `--wave` is present and `--manifest` or `--output` is omitted, read-only
`check-manifest`, `check-summary`, `check-promoted`, and `check-archive` resolve
those paths from the wave registry. Write modes still require explicit
`--output`. `check-archive --wave` validates only archive rows selected by that
wave. Omitting `--wave` preserves current whole-corpus behavior.

- [ ] Add RED metadata fixtures for root archive collection, exact-one archive
  selectors, key order, content-tombstone forbidden fields, and unchanged
  Stage 98 behavior.
- [ ] Add RED lifecycle fixtures for root expansion, exact 422 coverage,
  binary-safe generation, `unsupported -> archive`, review fields, and focused
  `--wave` archive checking.
- [ ] Implement the minimum selector, scanner, wave loader, binary-safe row
  generator, transition, and focused validation changes.
- [ ] Generate/inspect every row; keep the wave advisory through Task 5.
- [ ] Run GREEN, contract, explicit-base metadata, compile, and diff gates.
- [ ] Commit `feat(docs): establish target corpus migration contracts`.

```bash
python3 -m unittest \
  tests.validation.test_document_metadata.ProfileSchemaTests \
  tests.validation.test_document_metadata.ArtifactInferenceTests \
  tests.validation.test_document_metadata.MetadataValidationTests \
  tests.validation.test_document_metadata.ReadmeProfileTests -v
python3 -m unittest \
  tests.validation.test_document_corpus_lifecycle.PublicContractTests \
  tests.validation.test_document_corpus_lifecycle.HumanContractRoutingTests \
  tests.validation.test_document_corpus_lifecycle.ManifestValidationTests \
  tests.validation.test_document_corpus_lifecycle.ArchiveProvenanceTests -v
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 32c40e11747bc0bd03789c24861d2e5d60c0e999
python3 -m py_compile scripts/validation/check-document-metadata.py \
  scripts/validation/check-document-corpus-lifecycle.py
git diff --check
```

### T-TSC-002: README, Typed Example, and Storybook Cleanup

**Files:** create `tests/validation/test_target_surface_contracts.py`; modify
`examples/sample-web-service/{README.md,service.md}`;
`projects/storybook/{README.md,nextjs/README.md}`;
`scripts/knowledge/report-graphify-health.sh`;
`scripts/hooks/agent-event-hook.sh`; `.prettierignore`; and only matching
manifest/Task/generated rows.

- [ ] RED-test canonical Service metadata/order/sections and absence of copied
  template instructions.
- [ ] RED-test exact-one README profiles and native exclusions.
- [ ] Identify and manually inspect the one README not covered by the prior
  74-file content inspection; record its path and disposition in the Task.
- [ ] RED-test active phantom `projects/storybook/mcp` references while
  permitting historical Stage 03/04 evidence.
- [ ] Rewrite only sample-specific Service content and remove the five live
  phantom exceptions after confirming no Git `160000` entry.
- [ ] Run shell syntax, metadata, links, focused regression, and diff checks.
- [ ] Commit `docs(examples): align sample and storybook contracts`.

```bash
TASK_BASE="$(git rev-parse HEAD)"
python3 -m unittest tests.validation.test_document_metadata.ReadmeProfileTests -v
python3 -m unittest discover -s tests/validation \
  -p 'test_target_surface_contracts.py' -v
bash -n scripts/hooks/agent-event-hook.sh \
  scripts/knowledge/report-graphify-health.sh
git ls-files --stage -- projects/storybook
if git grep -n -F 'projects/storybook/mcp' -- \
  .prettierignore projects/storybook scripts; then
  echo 'ERROR: active Storybook MCP phantom reference remains' >&2
  exit 1
else
  grep_status=$?
  if [ "$grep_status" -ne 1 ]; then
    echo 'ERROR: Storybook MCP absence scan failed' >&2
    exit "$grep_status"
  fi
fi
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref "$TASK_BASE"
git diff --check
```

### T-TSC-003: Root Content Archive Provenance Migration

**Files:** rewrite `archive/Windows-Network-IP.md` in place and update only its
manifest row, generated summary, Task, and directly required archive owner.
Pinned source commit is the Plan baseline, source blob is
`b1faa418b9e0bb91bc93137e6e97236e75967f21`, disposition is `withdrawn`,
preservation is `git-history`, and replacement is absent.

- [ ] RED-test stale body, unresolved commit/blob, SDLC parents/replacement,
  and snapshot-only fields.
- [ ] Resolve commit:path to the expected blob without printing the body.
- [ ] Apply the content-archive template, provenance, reason, and current-use
  warning; remove the two active `netsh` commands.
- [ ] Run focused archive, consumer, metadata, link, and diff gates.
- [ ] Commit `docs(archive): preserve Windows network note provenance`.

```bash
TASK_BASE="$(git rev-parse HEAD)"
test "$(git rev-parse \
  32c40e11747bc0bd03789c24861d2e5d60c0e999:archive/Windows-Network-IP.md)" \
  = b1faa418b9e0bb91bc93137e6e97236e75967f21
python3 -m unittest \
  tests.validation.test_document_corpus_lifecycle.ArchiveProvenanceTests -v
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-archive --wave target-surface-convergence
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref "$TASK_BASE"
if git grep -n -E 'netsh (interface|wlan)' -- archive; then
  echo 'ERROR: archived command body remains active' >&2
  exit 1
else
  grep_status=$?
  if [ "$grep_status" -ne 1 ]; then
    echo 'ERROR: archived command absence scan failed' >&2
    exit "$grep_status"
  fi
fi
git diff --check
```

### T-TSC-004: Deprecated Runtime and Duplicate Disposition

**Delete:**

- `infra/04-data/analytics/influxdb/docker-compose.v2.yml`;
- `infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example`;
- `infra/04-data/lake-and-object/seaweedfs/config/security.toml`.

**Direct consumers:** modify `.env.example`, metadata-only
`secrets/SENSITIVE_ENV_VARS.md.example`, and these exact files:

- `infra/04-data/analytics/influxdb/README.md`;
- `docs/01.requirements/005-data-analytics.md`;
- `docs/02.architecture/requirements/0012-data-analytics-architecture.md`;
- `docs/02.architecture/decisions/0015-analytics-engine-selection.md`;
- `docs/03.specs/005-data-analytics/{README.md,spec.md}`;
- `docs/05.operations/guides/04-data/analytics/{README.md,influxdb.md}`;
- `docs/05.operations/policies/04-data/analytics/influxdb.md`;
- `docs/05.operations/runbooks/04-data/analytics/influxdb.md`;
- `infra/09-tooling/k6/{README.md,docker-compose.yml}`;
- `infra/09-tooling/locust/{Dockerfile,README.md,docker-compose.yml}`;
- `docs/05.operations/{guides,policies,runbooks}/09-tooling/{k6.md,locust.md,performance-testing.md}`;
- `infra/04-data/lake-and-object/seaweedfs/README.md`;
- `docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md`;
- `docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md`; and
- the stale analytics-family section of
  `scripts/validation/check-repo-contracts.sh`; and
- `tests/validation/test_target_surface_contracts.py`.

- [ ] RED-test the v2 Compose path, v2-only example keys, `influxdb-client`,
  k6/Locust v2 wiring, active v2 docs, and both duplicate paths. Permit truthful
  historical and negative-test use.
- [ ] Confirm no tracked executable v2 query/data consumer. Stop for a separate
  runtime/data design if one exists.
- [ ] Remove the v2 server, keys/metadata, client dependency, and unused
  k6/Locust dependencies/secret grants.
- [ ] Normalize active truth on InfluxDB 3 Core database/token, port 8181,
  `/api/v3/write_lp`, current health, and source-only verification.
- [ ] Delete only the unreferenced OpenSearch `.example`; retain mounted
  `userdict_ko.txt`.
- [ ] Delete only unmounted SeaweedFS `security.toml`; retain and document the
  unmounted `.example` scaffold without activating it.
- [ ] Run regressions, Dockerfile lint, leaf/all-profile static Compose,
  metadata, traceability, alignment, consumer, and diff gates.
- [ ] Commit the runtime unit as
  `refactor(infra): retire InfluxDB 2 compatibility` and the duplicate unit as
  `chore(infra): remove unconsumed duplicate scaffolds`.

```bash
TASK_BASE="$(git rev-parse HEAD)"
python3 -m unittest discover -s tests/validation \
  -p 'test_target_surface_contracts.py' -v
docker compose --env-file .env.example \
  -f infra/04-data/analytics/influxdb/docker-compose.yml config --quiet
docker compose --env-file .env.example \
  -f infra/09-tooling/k6/docker-compose.yml config --quiet
docker compose --env-file .env.example \
  -f infra/09-tooling/locust/docker-compose.yml config --quiet
bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='core data obs workflow ai tooling messaging security communication service storage admin iac registry sast sync testing graph mng ksql nginx' \
  bash scripts/validation/validate-docker-compose.sh
hadolint infra/09-tooling/locust/Dockerfile
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref "$TASK_BASE"
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

### T-TSC-005: Validator, QA Routing, and Static CI Enforcement

**Files:** create `scripts/validation/target_surface_contract.py` and its thin
`check-target-surface-contract.py` CLI; extend the Task 2/4 regression owner
`tests/validation/test_target_surface_contracts.py`; modify repository
contracts, QA recommender/runner, QA tool bootstrap, scripts README,
`.pre-commit-config.yaml`, and CI routing tests. Keep GitHub workflow semantics
in `scripts/validation/check-repo-contracts.sh` and their mutations in
`tests/validation/test_agent_governance_ci_routing.py`. Modify
`ci-quality.yml` only to route through the existing quality taxonomy, never to
duplicate a job.

The target validator exposes immutable `Finding(code, path, message)`, loads
exact paths from the manifest, and owns only manifest coverage, removed active
paths/claims, phantom gitlink exceptions, sample Service instantiation,
and duplicate disposition. It delegates metadata/archive/Compose rules to their
current owners and workflow artifact-upload prohibition exclusively to
`check-repo-contracts.sh`; it never renders file bodies or values in
diagnostics.

- [ ] RED-test each target finding code, changed-path QA selection, and workflow
  permissions, concurrency, timeout, full-SHA actions, untrusted-input, and the
  existing repository-wide `actions/upload-artifact` prohibition.
- [ ] Implement the smallest deterministic target validator; keep workflow
  semantics in `check-repo-contracts.sh` and mutation coverage in
  `test_agent_governance_ci_routing.py`. Integrate repository aggregate, QA
  selection, pre-commit, and the existing CI job.
- [ ] Lint all workflow YAML and changed shell/Python/Dockerfile code.
- [ ] Record 15 local job names and the dated 12-context remote observation as
  distinct scopes; do not claim remote convergence.
- [ ] Commit `feat(qa): enforce target surface contracts`.

```bash
python3 -m unittest tests.validation.test_agent_governance_ci_routing -v
python3 -m unittest tests.validation.test_target_surface_contracts -v
bash tests/validation/test_run_agent_precommit_all_files.sh
python3 -m py_compile scripts/validation/target_surface_contract.py \
  scripts/validation/check-target-surface-contract.py
bash -n scripts/validation/check-repo-contracts.sh \
  scripts/validation/recommend-qa-gates.sh \
  scripts/validation/run-local-qa-gates.sh \
  scripts/validation/run-agent-precommit-all-files.sh \
  scripts/operations/use-qa-ci-tools.sh
actionlint .github/workflows/*.yml
yamllint -c .yamllint .github/workflows/*.yml
shellcheck --severity=warning scripts/validation/check-repo-contracts.sh \
  scripts/validation/recommend-qa-gates.sh \
  scripts/validation/run-local-qa-gates.sh \
  scripts/operations/use-qa-ci-tools.sh
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

This Plan deliberately does not create a second GitHub workflow validator or
test module. Existing workflow policy remains in `check-repo-contracts.sh`,
with deterministic mutation coverage in
`tests/validation/test_agent_governance_ci_routing.py`.

### T-TSC-006: Research, Audit, Generated Evidence, and Closure

**Authored evidence:** update the canonical research pack `README.md`,
`quality-ci-formatting.md`, `docker-compose-infrastructure.md`,
`document-metadata-lifecycle.md`, `security-governance.md`,
`automation-pipeline-workflow.md`, and `workspace-baseline.md`; update the
canonical audit pack `README.md`, `implementation-overview.md`,
`frontmatter-template-readme-implementation.md`,
`sdlc-document-contracts-implementation.md`,
`sdlc-quality-formatting-implementation.md`, `automation-candidates.md`,
`compose-infrastructure-operations-readiness.md`, and
`security-framework-maturity.md`. Update Spec 133, its index, this Plan/Task,
both Stage 04 indexes, and progress memory only for observed closure.

Generated owner order is target corpus summary, Compose coverage, tech-stack
provenance, security readiness, audit matrix, LLM Wiki index/coverage, then
frontmatter inventory.

- [ ] Revalidate official sources/dates and separate external fact, repository
  implementation, static verification, live runtime, and remote state.
- [ ] Reconcile only current-truth changes; preserve historical observations
  and superseded-pack routing.
- [ ] Regenerate each applicable owner in fixed order, run its freshness check,
  inspect exact fallout, and restore unrelated graph/generated noise.
- [ ] Run the full verification ladder.
- [ ] Obtain fresh Task 6 reviews and whole-branch reviews over the exact final
  range.
- [ ] From an initially clean linked worktree, run the controlled wrapper with
  only actual changed prefixes and record every required bounded path set.
- [ ] Validate and separately commit any allowed formatter mutation; re-review
  after it. Promote the manifest and close lifecycle docs only after all gates.
- [ ] Commit `docs(execution): close target surface convergence`.

```bash
python3 -m unittest discover -s tests/validation -v
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-manifest --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-summary --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-promoted --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-impacted \
  --base-ref 32c40e11747bc0bd03789c24861d2e5d60c0e999
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 32c40e11747bc0bd03789c24861d2e5d60c0e999
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/validate-docker-compose.sh
actionlint .github/workflows/*.yml
yamllint -c .yamllint .github/workflows/*.yml
bash scripts/validation/report-audit-pack-coverage.sh --check
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
graphify update .
bash scripts/knowledge/report-graphify-health.sh
git diff --check
```

The final wrapper is:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/2026-07-18-target-surface-contract-convergence.md \
  --allow-prefix .env.example \
  --allow-prefix .github \
  --allow-prefix .pre-commit-config.yaml \
  --allow-prefix .prettierignore \
  --allow-prefix archive \
  --allow-prefix docs \
  --allow-prefix examples \
  --allow-prefix infra \
  --allow-prefix projects \
  --allow-prefix scripts \
  --allow-prefix secrets \
  --allow-prefix tests
```

Remove any unused prefix before execution; add no broader prefix than the
actual final diff requires.

## Verification Plan

Each RED command must fail for the named missing behavior, not an environment
or fixture error. GREEN requires the focused suite and smallest affected
aggregate owner. Task 4 requires static leaf/all-profile Compose render but no
`up`, `run`, `start`, `exec`, or persisted output. Task 5 requires workflow
lint and semantic mutations. Task 6 requires fresh generated owners,
exact-range reviews, a clean linked worktree, and controlled QA.

Expected final evidence:

- exactly 422 pinned baseline target rows plus declared direct-impact rows,
  with no duplicate or unclassified selection;
- exact-one content and SDLC archive profiles;
- all retained target READMEs exact-one with no compliant bulk rewrite;
- no active phantom gitlink, InfluxDB 2 server, v2-only example variable,
  unused client dependency, or removed duplicate;
- source and active docs agree for InfluxDB/k6/Locust/OpenSearch/SeaweedFS;
- workflow, Python, shell, Dockerfile, metadata, traceability, alignment,
  repository, Compose, audit-freshness, generated, and diff gates pass;
- fresh reviewers have no unresolved finding; and
- wrapper exit 0, snapshot PASS, and no unexpected Git-visible path.

## Risks and Rollback

| Risk | Guardrail | Rollback |
| --- | --- | --- |
| Manifest schema breaks Foundation | Keep Foundation v1 fixtures passing. | Revert T1 and regenerate target summary only. |
| Binary/native normalization | Use Git mode/blob; parse only declared text. | Revert manifest; no target mutation proceeds. |
| Archive provenance mismatch | Resolve commit:path/blob before rewrite. | Revert tombstone; pinned source remains. |
| README content loss | Exact-one tests and diff-size review. | Revert T2 authored files. |
| Hidden Influx v2 consumer | Scan before deletion and stop on executable use. | Route a new runtime/data plan. |
| Unrelated Compose change | Leaf/all-profile config and exact service diff. | Revert T4 commits in reverse. |
| Secret disclosure | Paths/keys only; fail closed without echo. | Stop, remove evidence, escalate rotation if needed. |
| Local/remote CI confusion | Separate dated evidence scopes. | Revert local workflow only. |
| Generated spill | Inspect exact owner diff. | Revert inputs and regenerate owner only. |
| Wrapper unexpected path | Wrapper exits 20 and preserves diff. | Stop and assign bounded remediation. |

Use ordinary `git revert` in reverse dependency order. Do not use
`git reset --hard`, history rewriting, or manual generated reconstruction.

## Approval Gates

- Existing user approval covers Stage 99 governance/contracts, protected local
  surfaces, reviewed destructive cleanup, InfluxDB 2 source/direct-consumer
  removal, static CI/QA, external research, local commits, and Subagent-Driven
  execution.
- Secret values, live data migration, service startup, deployment, release,
  remote mutation, push, PR, merge, and worktree deletion require separate
  authority and are excluded.
- An executable v2 query consumer, data-migration need, unsafe archive payload,
  unresolved destructive consumer, or runtime-only dependency blocks its task.
- Promote the target wave only after all rows, reviews, and Task evidence pass.

## Completion Criteria

- [ ] All six tasks have logical commits, specification PASS, quality APPROVED,
  and no unresolved finding.
- [ ] The pinned manifest covers its selection once and is promoted only after
  complete evidence.
- [ ] Archive, README, native, example, deprecated, duplicate, workflow, and QA
  contracts are executable and regression-tested.
- [ ] Every deletion has consumer, preservation, rollback, and review evidence.
- [ ] All direct service/tooling documents agree with final static source.
- [ ] Canonical research/audit and generated owners are current.
- [ ] Full verification and controlled wrapper pass in the clean worktree.
- [ ] Fresh whole-branch reviews pass on the exact final range.
- [ ] Spec/Plan/Task/indexes/memory close with runtime/remote limits explicit.
- [ ] Worktree is clean and commits are logical Conventional Commits.

## Related Documents

- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Spec 131](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Execution Task](../tasks/2026-07-18-target-surface-contract-convergence.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Corpus migration contract](../../99.templates/support/corpus-migration-contract.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
