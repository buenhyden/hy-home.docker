---
title: "Document Contract Convergence Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-04"
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
| Generated LLM Wiki freshness | PASS | both tracked outputs fresh |
| Traceability | PASS | 682 documents, 5,753 links, 51 archive direct links, 0 failures |
| Corpus lifecycle and recovery | PASS | 0 lifecycle violations; 3 frozen legacy migrations, 104 sealed tombstones, 140 preserved disposition paths, 250 decisions, 338 recovery rows |
| Diff whitespace | PASS | `git diff --check`, exit 0 |
| Frozen archive body diff | PASS | no changed path under `completed/`, `superseded/`, or `retired/` |
| Changed metadata | PASS | explicit `origin/main` merge base `47cadba8`; 565 selected, 0 violations after recovery corrections |
| Repository/active metadata | PASS | repository contracts 0 violations; active corpus 372 selected, 0 violations |
| Identity recovery regressions | PASS | exact member/Task reciprocal proof plus canonical, foreign-package, untyped-Task, and carrier-only-change cases |
| Changed gate | PASS | final staged snapshot, exit 0 after correcting RES-0085, identity deletion handling, hook parsing, security/audit/supply-chain generators, and authored lifecycle/schema findings |
| Full gate | PASS | local public `full` profile, exit 0 after final policy corrections |
| Hosted CI | FAIL / RETRY REQUIRED | runs `33866474442` and `33869471269` advanced through hardening to npm audit; both failures reproduced and corrected locally; final candidate rerun required |
| Provider entitlement | PASS | current Codex access plus bounded no-tool Claude `ENTITLEMENT_OK`, exit 0 |
| Runtime | OBSERVED | Docker/Compose reachable; no named deployment target and no runtime mutation |
| Remote protection | READY | exact 2-check target and exact 12-check rollback proved; mutate only after final candidate Hosted green |
| Hardening and tech-stack provenance | PASS | 11 tiers; 18 tech-stack contract tests; DATA-0061 freshness; 19 components and 22 images |
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

## Commit Ledger

- `be7e1388 feat(governance): converge document contracts` — initial reviewed
  contract, lifecycle, corpus, template, and RES-0085 candidate.
- `787cafd2 merge(main): integrate latest research routing` — non-fast-forward
  integration of current `main` while preserving both sides' owned behavior.
- `40161548 fix(governance): prove research identity recovery` — exact
  RES-0085 member/Task reciprocal recovery proof and regression closure.
- `38e6b35a fix(ci): restore hosted validation contract` — hardening image,
  active Security trace, Dozzle Registry, and DATA-0061 generator closure.

The Storybook audit and TypeScript/Next compatibility closure plus this evidence
update are prepared for one follow-up commit. Valid forward lifecycle transitions
remain post-merge work; they are not compressed into the initial PR history.

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
