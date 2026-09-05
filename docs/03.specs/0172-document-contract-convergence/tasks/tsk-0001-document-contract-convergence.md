---
title: "Document Contract Convergence Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0172-TSK-0001"
parent_ids:
- "SPEC-0172"
- "SPEC-0172-PLAN-0001"
created: "2026-09-04"
identity_recovery_decisions:
- source_commit: "db21aebf079fcc4e867779861b49c2283b7f8f01"
  source_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/REQUEST-SCOPE.md"
  source_artifact_id: "RES-0085-SCOPE"
  target_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md"
  target_artifact_id: "RES-0085-m0001"
  disposition: "consolidated"
---

# Document Contract Convergence Task

## Objective

Execute SPEC-0172 as a reviewed repository change, integrate it through a
feature branch and pull request, and retain exact local, hosted, provider,
runtime, protection, review, deferral, and Git evidence.

## Inputs

- Initial authorization covered local documents and validators. Follow-up user
  instructions on 2026-09-04 authorized the previously deferred RES-0085,
  Hosted CI, provider entitlement, runtime/deployment, branch protection,
  independent review, commit, push, PR, tag, and release categories.
- Feature-branch commit, push, PR, Hosted CI observation, provider entitlement,
  and branch-protection mutation have exact targets and rollback boundaries.
  Deployment, tag/release, and merge still require an exact target state,
  eligible merged commit, version, or explicit merge authority before execution.
- REQ-0024, REQ-0026, AD-0027, AD-0030, ADR-0029, and ADR-0031.
- Stage 00 policies, Stage 99 contracts, validators, formatter configuration,
  tests, and the current authored corpus.
- Protected surfaces: `docs/00.agent-governance/**`, `docs/99.templates/**`,
  and `scripts/**`.

## Work Log

### Safety and baseline (2026-09-04)

- Repository: `/home/hy/projects/hy-home.docker`.
- Origin: `https://github.com/buenhyden/hy-home.docker.git`.
- Branch: `main`; initial worktree: clean.
- Initial commit: `8a0a8ae4 docs(references): Give four compose defects a current owner-facing route`.
- Changed gate: PASS, exit 0.
- Traceability: PASS, 677 documents, 5,652 links, 0 failures.
- Prompt-listed lifecycle `--mode check-recovery`: CLI misuse, exit 2. The
  current no-mode route is the union of lifecycle, promoted, and recovery checks.
- Full gate: PASS, exit 0 on the clean baseline.

### Concurrent baseline change and integration boundary (2026-09-04)

- While the local worktree was in progress, PR #138 merged the RES-0085 request
  scope into `main` as `db21aebf`; this agent did not create that merge.
- The candidate moved to `codex/0172-document-contract-convergence`, committed
  the contract migration as `be7e1388`, and opened PR #139.
- `main` then advanced through `741eb90b` and `47cadba8`. The candidate merged
  those changes as `787cafd2` without rewriting their research routing or
  deterministic fixture behavior.
- The current candidate preserves the request as canonical member
  `RES-0085-m0001` beside the new package `README.md`. Its recovery evidence
  resolves the exact deleted blob at `db21aebf`, requires a reciprocal typed
  Task tuple, and rejects canonical, foreign-package, or untyped substitutes.
- PR #138 Hosted CI observation: CodeQL passed, `validation-changed` failed,
  `validation-full` was skipped, and the greeting job failed. This is baseline
  evidence only, not acceptance of the current candidate.
- Current `main` protection was observed as strict with one approving review,
  code-owner review, conversation resolution, and force-push/deletion disabled.
  Its 12 stale required contexts do not match the current CI Quality Gates job
  names; no setting was changed before a replacement target and rollback were
  proved.
- The current Codex task had direct account access. A bounded Claude CLI probe
  from `/tmp`, with safe/restricted mode, no tools, no session persistence, and
  a USD 0.05 ceiling, returned exactly `ENTITLEMENT_OK` with exit 0. This proves
  direct entitlement only, not model equivalence, performance, or acceptance.
- Docker Engine and Compose were reachable with zero active Compose projects.
  Five `k3d-hyhome` containers were present but do not prove this repository's
  Compose deployment. No runtime mutation was performed.

### Hosted CI and remote protection boundary (2026-09-04)

- PR #139 run `33866474442`, job `101002368891`, executed against candidate
  `401615481678bfedcbc3abbe64705e5a3cf40978`. `validation-changed` failed at
  the hardening leaf after 15m31s; `validation-full` job `101002370024` was
  skipped by the PR-event contract.
- The failing leaf exposed pre-existing drift on `main`: stale Valkey,
  redis-exporter, and RedisInsight image assertions; a retired Security Spec
  path still treated as active; and a Dozzle Registry lookup with no Registry
  entry. Fixes retain exact checks, point Security trace validation at active
  REQ-0003, and add the missing Dozzle source tuple.
- Regenerating DATA-0061 then exposed its generator's pre-migration
  frontmatter. The generator now emits the ordered common six and the
  `publication` lifecycle's `published` state before regenerating 19 components
  and 22 images.
- The corrected local `changed` profile passed with exit 0, including two
  every-declared Compose passes at 28 selections and 232 services, 11-tier
  hardening, 372 active metadata records, and 0 lifecycle/recovery violations.
- Follow-up PR run `33869471269`, job `101011775275`, executed against exact
  candidate `38e6b35a9990e736b34f04f42d90f387750d0013`. It passed the corrected
  hardening path and then failed after 15m45s at the scoped Storybook npm audit;
  `validation-full` job `101011776577` remained skipped by the PR-event
  contract.
- The audit failure resolved through
  `@storybook/nextjs-vite@10.5.10 -> vite-plugin-storybook-nextjs@3.3.0 ->
  image-size@2.0.2`. The lock now selects the compatible Storybook 10.6.0
  family, whose adapter replaces `image-size` with `probe-image-size`; the
  exact high-severity audit reports zero vulnerabilities.
- Advancing past audit exposed the pre-existing TypeScript 7.0.2 and
  `typescript-eslint@8.65.0` incompatibility. TypeScript is pinned to 5.9.3,
  inside both the declared `<6.1.0` and `tsconfck@3.1.6` `^5.0.0` peer ranges,
  and Next explicitly uses the compiler API because its CLI output capture
  returns empty in the local sandbox. The complete npm peer graph, lint,
  typecheck, Storybook production build, and Next webpack production build
  pass. Default Turbopack and browser coverage require local port binding and
  therefore remain Hosted-run evidence.
- Tracked policy `.github/rulesets/main-protection.md` defines the exact target:
  strict `main` checks `validation-changed` and `validation-full`, both bound to
  GitHub Actions app ID 15368. Reviews, CODEOWNERS, conversation resolution,
  force-push, deletion, and admin settings remain unchanged.
- The exact rollback is the observed strict 12-context set:
  `docs-traceability`, `repo-contracts`, `git-flow-contract`,
  `compose-validation`, `compose-all-profiles-validation`,
  `infrastructure-hardening`, `template-security-baseline`,
  `quickwin-baseline`, `pre-commit`, `zizmor`, `frontend-quality`, and
  `storybook-coverage`; restore app ID 15368 except the observed unbound
  `frontend-quality` context.
- PR run `33873742953`, job `101025625795`, executed against exact candidate
  `c9c09f1fff050f4a01b0220b86aab67902179b04`. The corrected dependency,
  peer, lint, typecheck, build, and Storybook browser coverage paths passed,
  including 9 tests and 100% reported code coverage. The final registered
  `zizmor` leaf then failed with `ci-gate-adapter-child-exec` because the PR job
  did not provision `uvx`; the full job `101025627829` was correctly skipped.
- The workflow already registered immutable `astral-sh/setup-uv` commit
  `20cfd1bf945f4377ade1205e4dbc17946fc9a30d` for the full job. The same action
  now provisions `uvx` in the changed job before dependencies and the public
  gate. No permission, event, validator, tool version, or SARIF upload behavior
  changes; removing that one step is the workflow rollback.
- PR run `33876647221`, job `101035112333`, executed against exact candidate
  `2aefde23d5853ca6a0e0de4e4dd1dbb72b06667f`. Both `Install uv` and dependency
  bootstrap passed, proving the previous executable-availability failure was
  removed. The public gate then failed after 17m52s when pinned
  markdownlint-cli2 0.22.1 rewrote one duplicate blank line in the Stage 99
  template README despite reporting zero lint errors, and Ruff 0.15.12 reported
  12 Python files requiring deterministic formatting; 94 Python files were
  already formatted. The full job `101035114121` was correctly skipped.
- A write-free local `ruff format --check --diff .` reproduced the exact same
  12-file set. Ruff mechanically normalized only those named Python files, and
  the exact CI pre-commit path reproduced markdownlint-cli2's one Stage 99
  README normalization. Validator and test behavior, hook versions, and all
  other non-evidence surfaces remain unchanged.
- Follow-up PR #140 run `33882334540`, job `101053733629`, executed against exact
  candidate `8f0a34320a0a8598939dbb5ecab1dfb73c298d9b`. The formatter hooks passed,
  proving their correction, and the public gate advanced through Storybook's
  9 browser tests with 100% reported code coverage. It then failed after
  18m15s at Hadolint v2.14.0 because
  `examples/sample-web-service/Dockerfile` used shell-form `HEALTHCHECK CMD`,
  producing exact finding `DL3025`; the full job `101053734881` was correctly
  skipped for the PR event.
- The sample healthcheck now uses Docker exec-form with the same `wget` command,
  arguments, URL, and nonzero failure semantics. This removes the unnecessary
  shell and redundant `|| exit 1` without changing the image, endpoint,
  interval, timeout, start period, retries, port, service, or deployment state.
  Reverting that one instruction is the correction rollback.
- Follow-up PR #140 run `33886343534`, job `101066935299`, executed against exact
  candidate `5ad8f0c094d50fba0e50b3f0e9a2c2fa632a50a0`. The sample healthcheck and
  every preceding hook passed. Hadolint v2.14.0 then reported only five
  `DL3066` findings: two n8n `USER` instructions, one OAuth2 Proxy instruction,
  and two OpenSearch instructions. The full job `101066936793` was correctly
  skipped for the PR event.
- OpenSearch 3.7.0 image history declares UID/GID 1000 and final `USER 1000`.
  Reproducing the OAuth2 Proxy account creation on exact Alpine 3.24.1 yielded
  UID 100/GID 101. The Dockerfiles now use those numeric user identities; n8n
  and OpenSearch assert their named account maps to UID 1000 and primary GID
  1000 before switching by UID only, preserving group-resolution semantics.
  Root is expressed as UID 0. The added commands are build-time identity guards;
  no effective user identity, ownership target, base-image reference, runtime
  command, service definition, hook, threshold, ignore, or deployed state
  changes. The custom image config, history, and digest necessarily change.
  The OAuth2 Proxy production identity is synchronized with the canonical
  hardening consumer, its focused regression, and the active operator guide;
  the root-active dev image retains its named-user contract. Reverting those
  three consumer updates and the three Dockerfile patches is the correction
  rollback.
- Exact affected Dockerfiles are `infra/07-workflow/n8n/Dockerfile`,
  `infra/02-auth/oauth2-proxy/Dockerfile`, and
  `infra/04-data/analytics/opensearch/Dockerfile`. Repository-wide
  `pre-commit run hadolint-docker --all-files`, BuildKit `--check` for all three
  exact build contexts, all 11 hardening tiers, and the 19 focused tech-stack
  contract tests pass. The OAuth-specific regression is
  `test_oauth2_proxy_production_numeric_identity_contract`.
- Follow-up PR #140 run `33890830204`, job `101081789784`, executed against
  exact candidate `1a5de646224c51f9caa33219bfbbb825338617c1` and passed the
  changed public suite in 13m0s. This proves the numeric-user correction reaches
  and passes every Hosted leaf, including Hadolint v2.14.0. The full job
  `101081791407` was correctly skipped for the PR event.
- Final candidate PR run `33892413865`, changed job `101087013309`, executed
  against `fe4e26bbe4cc699d678832f68bd765901e028fb7` and passed in 19m55s.
  Workflow-dispatch run `33894450241` then executed full job `101093684400`
  against that same SHA and failed after 12m25s. A local CI-context reproduction
  proved the full job combined 21 mutually exclusive profiles into one named
  selection, producing exact host-port conflicts on 80/443 and 8000. The full
  job now leaves `HYHOME_COMPOSE_PROFILES` unset so the existing validator checks
  all 28 declared selections and 232 services independently. Reintroducing the
  workflow-level or job-level override is rejected by the semantic contract;
  reverting the correction restores the known failure. The exact local CI-context
  run passed both Compose validations, hardening, tests, frontend build, and
  Storybook, then exited 1 only when Playwright's browser installer required an
  unavailable interactive `sudo` password; Hosted full remains the authority for
  that runner-specific final segment.
- Corrected candidate PR run `33899619212`, changed job `101110351847`, executed
  against `17a5564ca8527944b0da50a53e611e2093dbedc6` and passed in 12m51s.
  Workflow-dispatch run `33899635117`, full job `101110407893`, executed against
  the same SHA and passed in 19m57s, including the public suites and SARIF upload.
  These two runs close the Hosted retry without bypassing or removing a gate.
- On 2026-09-05 the user explicitly approved the remote mutation for
  `buenhyden/hy-home.docker` `main` required status checks. The audited command
  class was PATCH of `branches/main/protection/required_status_checks` only.
  Before-state was `strict=true` with the exact 12 observed leaf checks; the
  applied and read-back after-state is `strict=true` with only
  `validation-changed` and `validation-full`, both bound to app ID 15368.
  Pull-request review, CODEOWNERS, conversation resolution, admin, signature,
  linear-history, force-push, deletion, creation, lock, and fork-sync settings
  were read back unchanged. Rollback remains the exact captured 12-check state,
  including unbound `frontend-quality`; no rollback was required.

### Research architecture renewal (2026-09-05)

- Started from clean `main@4c6d211129615eab372d720ebd209b6c27618c86`
  on feature branch `codex/0002-agentic-research-renewal`; repository and
  external-source observation date is 2026-09-05.
- Inventoried the existing Stage 90 research roots before editing. RES-0002,
  RES-0084, and RES-0085 already own the requested questions, so no competing
  research package or package identity was created.
- Rebuilt the RES-0002 package README as the question, scope, method, summary,
  navigation, traceability, and limitation owner; preserved its exact README
  plus 20-member protection set, every member identity and `created` value, and
  mapped all 93 A1-G11 requested categories to one owning member each.
- Split the detailed GitHub Actions analysis out of the RES-0084 package README
  into new draft member `RES-0084-m0001`, retained the historical analysis with
  explicit 2026-07-05 initial-observation and 2026-08-10 source-refresh dates,
  and kept the package README as a concise router.
- Normalized the RES-0085 package and request-scope member around the current
  baseline and evidence classes without changing its approved identity-recovery
  tuple. Updated the research index and tracked main-protection record to the
  approved aggregate-check read-back.
- Re-opened official provider, GitHub, Docker Compose, Diátaxis, C4, arc42,
  Spec Kit, ISO/IEC/IEEE 29148, NIST SSDF, SLSA, and agency-agents sources. No
  secret, user-global setting, raw log, deployment, release, tag, or new remote
  mutation was used as research evidence.
- The first staged metadata check correctly rejected the new member at
  `published`; it was repaired to the registered `draft` initial state and
  `0.1.0` initial version. Independent review also found generated-index
  staleness and a historical cutoff ambiguity; both were corrected without
  weakening a validator.
- The owner generator refreshed only DATA-0076 and DATA-0082. Focused reference
  tests passed 24/24, metadata changed selected 28 paths with zero violations,
  all-link validation covered 683 documents and 5,705 links with zero failures,
  and the staged candidate full profile exited 0. Independent policy review
  returned final PASS with no actionable finding after revalidation.

### Research baseline consolidation (2026-09-05)

- Reassessed RES-0002, RES-0084, and RES-0085 by question, scope, lifecycle,
  inbound links, and canonical ownership before editing. RES-0084 remains the
  independent GitHub Actions platform-mechanics authority because its external
  observation cadence differs from repository adoption evidence in RES-0002.
- Consolidated mutable workspace-baseline ownership into `RES-0002-m0020` at
  `main@a89c600c05c0b61f5cbd592e196ac3673f9eeb4b`. RES-0085 now preserves the
  dated `main@4c6d211129615eab372d720ebd209b6c27618c86` assessment, approved
  request boundary, and recovery provenance without competing current-state
  conclusions.
- Preserved the RES-0085 package and member paths, artifact identifiers,
  `created` values, and exact `identity_recovery` tuple. The package and member
  each make only the registered publication-lifecycle transition from `draft`
  to `review`; `review -> published` and any later terminal transition would
  require separate approval and validation units if pursued.
- The RES-0002 protected path set did not change, so its exact README plus
  20-member Preservation Declaration remains unchanged. No generated document
  was edited because LLM Wiki freshness remained valid after the ownership-only
  consolidation.
- Pre-edit focused reference tests passed 24/24, traceability covered 683
  documents and 5,705 links with zero failures, LLM Wiki freshness passed, and
  `git diff --check` passed. Post-edit metadata selected eight paths with zero
  violations; lifecycle and recovery checks reported zero violations; and
  traceability covered 683 documents and 5,712 links with zero failures.
- After the independent review findings were corrected, the `changed` and
  canonical local `full` public profiles each exited 0. The final independent
  spec-compliance and quality verdicts were PASS with no actionable finding.

### Gap matrix

| Current state | Target state | Affected files | Migration | Validator | Test |
| --- | --- | --- | --- | --- | --- |
| Registry uses `profile_id` beside `type` | Internal `id` maps 1:1 to unique `family/kind` `type` | Registry, schema, consumers | migrate active prose | exact ID/type mapping | duplicate/mismatch |
| Schema admits arbitrary properties | closed Registry-driven keys | schema, metadata validator | retain declared provenance | forbidden/order | negative fixtures |
| Templates mix token forms | uppercase values and author prompts | templates, catalog | template-aware only | residue/source | orphan/token fixtures |
| Stage 01/02 teach legacy classifiers | `type` plus Registry selection | Stage README files | prose only | active scan | frozen boundary |
| Lifecycle roles are compressed | profile-specific graphs | Registry, Stage 00 | semantic mapping | entry/edge | invalid transition |
| Release evidence mode is implicit | consumer-backed explicit mode | Stage 00/05 | document mode | authority check | absent/adopted |
| Archive citation and authority blur | immutable history, no current dependency | REQ/AD/Stage 00/98 | policy only | frozen/dependency | boundary fixtures |

## Verification Evidence

| Check | Outcome | Evidence |
| --- | --- | --- |
| Registry, operations, and placeholder unit tests | PASS | 107 tests, exit 0 |
| Focused placeholder/type/catalog regressions | PASS | 11 tests, exit 0 |
| Generated LLM Wiki freshness | PASS | both tracked outputs fresh after owner regeneration for the RES-0084 member path |
| Traceability | PASS | 683 documents, 5,705 links, 51 archive direct links, 0 failures |
| Research package contract | PASS | 24 focused tests; RES-0002 declaration exact; 93 requested category keys unique; independent review PASS |
| Corpus lifecycle and recovery | PASS | 0 lifecycle violations; 3 frozen legacy migrations, 104 sealed tombstones, 140 preserved disposition paths, 250 decisions, 338 recovery rows |
| Diff whitespace | PASS | `git diff --check`, exit 0 |
| Frozen archive body diff | PASS | no changed path under `completed/`, `superseded/`, or `retired/` |
| Changed metadata | PASS | explicit `origin/main` merge base `47cadba8`; 565 selected, 0 violations after recovery corrections |
| Repository/active metadata | PASS | repository contracts 0 violations; active corpus 372 selected, 0 violations |
| Identity recovery regressions | PASS | exact member/Task reciprocal proof plus canonical, foreign-package, untyped-Task, and carrier-only-change cases |
| Changed gate | PASS | final staged snapshot, exit 0 after correcting RES-0085, identity deletion handling, hook parsing, security/audit/supply-chain generators, and authored lifecycle/schema findings |
| Full gate | PASS | local public `full` profile, exit 0 after final policy corrections |
| Hosted CI | PASS | corrected candidate `17a5564c` passed changed job `101110351847` in run `33899619212` and full job `101110407893` in workflow-dispatch run `33899635117` |
| Provider entitlement | PASS | current Codex access plus bounded no-tool Claude `ENTITLEMENT_OK`, exit 0 |
| Runtime | OBSERVED | Docker/Compose reachable; no named deployment target and no runtime-state mutation; four Dockerfiles have bounded equivalent instruction corrections plus build-time identity assertions |
| Remote protection | PASS | authenticated PATCH and full read-back applied strict aggregate checks `validation-changed` and `validation-full` with app ID 15368; non-check protections unchanged; exact 12-check rollback retained |
| Hardening and tech-stack provenance | PASS | 11 tiers; 19 tech-stack contract tests; DATA-0061 freshness; 19 components and 22 images |
| Storybook dependency security | PASS | clean install, exact high-severity audit with 0 vulnerabilities, lint, typecheck, and Storybook 10.6 production build |
| Next production build | PASS / SANDBOX-LIMITED | webpack production build passed; default Turbopack reached bundling but local worker port binding was denied |

The merged `RES-0085` request-scope file did not satisfy the Stage 90 package
envelope. The candidate adds the substantive canonical `README.md`, normalizes
the request evidence to `m0001-request-scope.md`, records the invalid predecessor
identity `RES-0085-SCOPE` as consolidated into `RES-0085-m0001`, and keeps Git
recovery through commit `db21aebf`. General `research-member` paths are now
admitted by the References consumer and validated by the Registry metadata path.

### Implemented slices

- Replaced raw Registry `profile_id` with `id` and role `profile_id` with a
  non-empty `profiles` list; consumers and schema now enforce unique IDs,
  unique `family/kind` types, and their one-to-one mapping.
- Renamed and closed the document frontmatter schema without a compatibility
  copy; regenerated its LLM Wiki consumers.
- Normalized registered Markdown tokens to `{{UPPER_SNAKE_CASE}}`, retained
  native `__UPPER_SNAKE__`, and added source/residue regression tests.
- Corrected current Stage 01/02/05/98/99 navigation and archive authority prose,
  including ADR-0031 supersession and `external-release-evidence` mode.
- Aligned REQ-0026, AD-0030, and ADR-0031 on frozen body, disposition record,
  and Git recovery responsibilities without changing frozen bodies.
- Added explicit entry and terminal states to 15 lifecycle graphs and mapped
  Requirements, Architecture Descriptions, ADRs, Specs, Plans, Tasks, Policies,
  Incidents, Postmortems, publications, and sealed archive records to their
  semantic lifecycle.
- Enforced the ordered common six fields across 35 authored Markdown profiles.
- Migrated 613 non-frozen governed corpus documents and 33 Markdown templates;
  the migration changed frontmatter only and was idempotent on re-run. Verified
  143 frozen evidence files unchanged: 140 disposition payloads plus 3 legacy
  migration ledgers, including their preserved `completed` status.
- Connected the authored corpus to the closed frontmatter value schema; aligned
  native hook condition arrays; enforced new-document initial state in changed
  validation; and rejected unreachable or false-terminal lifecycle graphs.
- Restricted template roles to the one profile their consumers implement and
  removed the unconsumed speculative `release` lifecycle.
- Established RES-0085 as a canonical research package while preserving the
  binding request as a typed generic research member.
- Restricted historical identity recovery to an unregistered source in the
  same research package, an exact `research-member` target, and one reciprocal
  `task` decision tuple; every allowed frontmatter key now has a canonical
  serialization position.
- Closed the Hosted hardening drift without weakening a validator: synchronized
  three image assertions, moved the Security trace check from retired SPEC-0003
  to active REQ-0003, registered Dozzle, and made DATA-0061 generation preserve
  the `data` profile lifecycle and common-six order.
- Removed the vulnerable Storybook transitive path without an override by
  selecting the 10.6.0 adapter family, restored the supported TypeScript 5.9.3
  toolchain, and made Next use its compiler API for deterministic configuration
  loading.
- Removed the Hosted runner-image dependency from the PR `zizmor` path by
  provisioning the same registered SHA-pinned `setup-uv` action in both public
  validation jobs, without broadening the PR job's read-only permission set.
- Converged the exact Ruff 0.15.12 12-Python and markdownlint-cli2 0.22.1
  one-Markdown drift reported only after Hosted CI reached the pre-commit leaf;
  the mechanical normalization changes no behavior.
- Replaced the exact sample-service shell-form healthcheck reported as
  `DL3025` with equivalent exec-form arguments; no image, endpoint, timing,
  service, deployment, hook, or validator behavior changed.
- Replaced the five exact `DL3066` symbolic user instructions with their same
  numeric user identities without changing group-resolution semantics, plus
  fail-closed build assertions where the account comes from an upstream image;
  synchronized the OAuth2 Proxy production hardening
  consumer, focused regression, and operator guide while preserving its dev
  identity contract; no global ignore or threshold was added.

## Review Evidence

Exact-diff self-review found and corrected missing `date-time` grammar, no-op
quoted mutations, lowercase placeholder fixtures, generator drift, and missing
negative coverage. The authorized independent policy review returned BLOCKED on
authority gaps, including a recovery carrier that proved only the package and
an untyped self-declared decision. The recovery carrier now belongs to the exact
member, and its Task tuple, source class, package boundary, and canonical order
are executable contracts. A final carrier-only-change concern was disproved by
the tracked-corpus collector and fixed as a regression contract. The policy
reviewer's final verdict is PASS with no actionable finding. The independent
code reviewer independently reproduced the recovery gaps and returned final
specification, quality, and overall PASS after correction.

The follow-up Storybook review initially blocked TypeScript 6.0.3 because it
missed `tsconfck`'s optional TypeScript 5 peer, the active Spec did not yet admit
build-only Hosted remediation, the Task said `staged` before staging, and a
root build trace remained untracked. TypeScript 5.9.3 now satisfies the complete
peer graph, Spec and Plan own the narrow remediation, the Task says `prepared`,
and the generated trace is removed. Both independent policy and code reviewers
returned final PASS with no actionable finding on the resulting six-file diff.

The numeric-user review initially blocked explicit `1000:1000` for n8n and
OpenSearch because it could change supplementary-group resolution, and then
blocked stale OAuth hardening ownership and overbroad image-invariance claims.
The final UID-only instructions, exact OAuth production consumer/test/guide,
and custom-image evidence boundary resolve those findings. Both independent
reviewers returned final specification, quality, policy, and overall PASS with
no actionable finding on the resulting nine-file diff.

## Commit Ledger

- `be7e1388 feat(governance): converge document contracts` — initial reviewed
  contract, lifecycle, corpus, template, and RES-0085 candidate.
- `787cafd2 merge(main): integrate latest research routing` — non-fast-forward
  integration of current `main` while preserving both sides' owned behavior.
- `40161548 fix(governance): prove research identity recovery` — exact
  RES-0085 member/Task reciprocal recovery proof and regression closure.
- `38e6b35a fix(ci): restore hosted validation contract` — hardening image,
  active Security trace, Dozzle Registry, and DATA-0061 generator closure.
- `c9c09f1f fix(ci): secure Storybook validation path` — compatible Storybook,
  TypeScript, and Next build-tool closure plus exact review evidence.
- `1a5de646 fix(ci): pin Dockerfile user identities` — exact numeric-user,
  fail-closed identity proof, canonical hardening consumer, regression, and
  operator-guide closure.

The PR-job `uvx` provisioning correction plus this evidence update are prepared
in `2aefde23`. The exact formatter normalization plus this new Hosted evidence
were committed as `8f0a3432`. The exact Hadolint correction and its Hosted
evidence were committed as `5ad8f0c0`. The exact numeric-user correction and
consumer evidence were committed as `1a5de646`; its exact successful Hosted
run evidence is prepared for one follow-up commit. Valid forward lifecycle
transitions remain post-merge work; they are not compressed into the initial PR
history.

## Rulings

- Preserve user changes; the initial worktree was clean.
- Never read secret values, credentials, certificates, auth files, shell history,
  or raw log databases.
- Never run reset, clean, stash, direct `main` mutation, secret reads, or a
  deployment/protection/tag/release mutation without its exact target contract.
- Use the current lifecycle CLI without the removed `--mode` option.
- Follow-up user approval on 2026-09-04 explicitly authorized the previously
  deferred profile lifecycle, common-six, and active-corpus semantic migration.
- A feature-branch push and PR are authorized after local gates and independent
  reviews pass. Merge remains prohibited until explicitly requested.

## Deferred Items

- Live deployment is blocked on a named stack/target, change set, observation
  plan, and rollback. Runtime reachability is not deployment acceptance.
- Tag and release are blocked on an exact version, release scope, and eligible
  merged commit. Merge itself requires explicit user authorization.

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
