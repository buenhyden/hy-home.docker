---
status: active
artifact_id: plan:2026-08-08-agentic-research-pack-rebuild
artifact_type: plan
parent_ids:
  - spec:137-agentic-research-pack-rebuild
---

# Agentic Engineering Research Pack Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan
> task-by-task. `superpowers:executing-plans` supplied the general execution
> discipline but is not the selected execution mode for this same-session
> workstream. Steps use checkbox (`- [ ]`) syntax for tracking.

## Overview

This plan executes the active Spec 137 design as thirteen sequential,
independently reviewed units. It establishes execution evidence before
authoring, builds and validates the new pack while the old pack remains
recoverable, switches human and machine routes, deletes the old pack behind a
fail-closed gate, and closes the branch with exact-range evidence.

**Goal:** Replace the stale 2026-07-05 agentic engineering research pack with
a newly authored, primary-source-backed 2026-08-08 pack, preserve claim-level
provenance, switch every canonical route and affected generated artifact, and
delete the old twenty files only after fail-closed migration gates pass.

**Architecture:** A Stage 04 Task owns four typed ledgers: requirements,
sources/evidence, old-claim migration, and verification/generated artifacts.
Nine independently reviewed authoring units build the twenty leaves while
the old pack remains intact. Routing and generated artifacts switch only after
pack review; deletion is a separate commit behind a second independent gate.

**Tech Stack:** Markdown, Git, repository Stage 00/99 contracts, official
primary web sources, `rg`, Bash, Python 3 validators, LLM Wiki generators, and
subagent-driven specification/quality review.

## Global Constraints

- Work only in the isolated
  `/home/hy/projects/hy-home.docker/.worktrees/codex-agentic-research-rebuild`
  worktree on branch `codex/agentic-research-rebuild`.
- The active specification is
  [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md).
- The new canonical route is exactly
  `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`.
- The old pack remains intact until Task 11's pre-deletion gate passes.
- Stage 90 analysis is advisory and never becomes policy, runtime truth, or
  remote-enforcement proof merely by being cited.
- Every load-bearing external claim uses a direct primary source, access date,
  mutability class, and verification state. Unavailable evidence is
  `UNVERIFIED`; it is never guessed from the old pack.
- Every workspace fact cites a tracked owner, baseline commit, and derivation
  command or identifier. Tracked definitions do not prove live execution.
- Analyze all fourteen persona scopes: `agentic`, `architecture`, `backend`,
  `common`, `docs`, `entry`, `frontend`, `infra`, `meta`, `mobile`, `ops`,
  `product`, `qa`, and `security`.
- Preserve secret, credential, raw-log, shell-history, ignored-volume, and
  private-provider boundaries. Do not start containers or mutate remote state.
- Graphify is stale at `f8a72211` and remains advisory; corroborate every lead
  against tracked sources and stage documents.
- Use one fresh implementer per logical unit. The implementer validates,
  self-reviews, and commits before the controller creates a `BASE..HEAD` review
  package. Independent specification and quality review then gates task
  completion and the next unit; findings are fixed in reviewed follow-up
  commits through the SDD fix loop.
- Every topical leaf contains an explicit scope-implication section covering
  all fourteen normative scopes directly or by a precise scope-matrix mapping,
  with an explicit not-applicable disposition where appropriate.
- Commit each logical unit separately. Never combine the route switch with the
  old-pack deletion.
- Do not push, open a pull request, merge, or delete the branch without a later
  user choice through the finishing workflow.

---

## Context and Inputs

### Pinned baseline

| Input                             | Baseline state                                                                                                                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Branch base                       | `78b60974164ff5427ba8c64aaf3ecde4a7faf41a`                                                                                                                                                                                |
| Written design commit             | `3182daa8`                                                                                                                                                                                                                |
| Original active Spec 137 commit   | `35318255`                                                                                                                                                                                                                |
| V&V/Gate 9 Spec amendment         | `90eca714`, `76808636`, and `af37969b`; aggregate range `b77abacb610c853db3e9fef2bdef8cc7855c62a2..af37969b26f7e96d684fa0fdf8a0ee2418a4ac23`; final independent specification and documentation reviews Approved C0/I0/M0 |
| Old pack                          | 20 regular files: README plus 19 leaves                                                                                                                                                                                   |
| LLM Wiki index                    | Fresh at design time                                                                                                                                                                                                      |
| LLM Wiki coverage                 | Stale at design time                                                                                                                                                                                                      |
| Security readiness snapshot       | Stale and semantically unreliable because its generator misses typed workflow-registry resolution                                                                                                                         |
| Repository contract               | Blocked by missing `html5lib` in the current validation environment                                                                                                                                                       |
| Document implementation alignment | 184 pre-existing archive-direct-link findings; Spec 137 introduces zero                                                                                                                                                   |
| Graphify                          | Advisory and stale; built from `f8a72211`                                                                                                                                                                                 |

Every invocation of `scripts/validation/check-repo-contracts.sh` after Task 1
uses the isolated interpreter provisioned at
`/tmp/agentic-research-validation-venv`. The reproducible command is:

```bash
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
```

The environment is disposable and outside the repository. If package download
or environment creation is blocked, request the required tool approval and
keep the deletion gate closed; never substitute a partial contract check.

### Closed requirement set

The Task instantiates all `REQ-01` through `REQ-36` from Spec 137. A task may
add discoveries but may not merge or remove the thirty-six required rows.
Completion requires thirty-six reviewed canonical destinations and fourteen
reviewed scope dispositions.

### Committed-unit SDD protocol

The execution resource is pinned to the installed Superpowers 6.2.0 skill at:

`/home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/subagent-driven-development/`

Before Task 1, verify `SKILL.md`, `implementer-prompt.md`,
`task-reviewer-prompt.md`, `re-review-prompt.md`, and the three versioned shell
scripts `scripts/sdd-workspace`, `scripts/task-brief`, and
`scripts/review-package`. Initialize this Plan's ignored SDD workspace with:

```bash
bash /home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/subagent-driven-development/scripts/sdd-workspace \
  docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md
```

The installed 6.2.0 files are readable shell scripts but do not carry an
executable mode bit. Therefore invoke all three through `bash` and always pass
an explicit output path so `task-brief`/`review-package` never attempt their
internal direct call to `sdd-workspace`:

```bash
bash /home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/subagent-driven-development/scripts/task-brief \
  docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md TASK_NUMBER \
  .superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-TASK_NUMBER-brief.md
bash /home/hy/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/subagent-driven-development/scripts/review-package \
  docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md BASE HEAD \
  .superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/review-BASE..HEAD.diff
```

Replace the uppercase placeholders with literal task/range values. Prompts
come from the three pinned Markdown templates above; the five-round breaker
and ledger lines follow the pinned `SKILL.md` verbatim.
If this exact resource is unavailable, stop before dispatch rather than falling
back to an unreviewed inline workflow; re-pinning a different installed version
requires a reviewed Plan update.

Every Task below uses the same execution sequence:

1. The controller records `BASE=$(git rev-parse HEAD)` and generates the
   task brief with the SDD `task-brief` script.
2. One fresh implementer reads only that brief and required interfaces,
   authors the unit, runs its checks, self-reviews, commits, and writes its
   report.
3. The controller generates one review package for the exact `BASE..HEAD`
   range with the SDD `review-package` script and dispatches two fresh,
   independent reviewers over that same immutable package: one reviewer owns
   specification compliance and one owns documentation/code quality. Both use
   the pinned `task-reviewer-prompt.md` with their role-specific lens and both
   verdicts are recorded separately.
4. Critical/Important findings enter the bounded SDD fix loop. The implementer
   commits fixes; the controller packages only the fix range and dispatches a
   scoped re-review.
5. Only two clean verdicts mark the Task complete in the SDD ledger and permit
   the next Task. The five-round breaker may park documented Minor findings,
   but it never permits an unresolved Critical or Important finding to advance;
   an unresolved Critical/Important result after round five stops execution and
   requires a reviewed Plan correction or user decision.

The controller never edits an implementer's owned files during the unit. Minor
findings are recorded in the SDD ledger for final whole-branch triage. Task 11
adds non-destructive proposed-deletion and actual staged-diff reviews before
commit to satisfy Spec 137's no-unreviewed-deletion gate; those reviews do not
replace its normal committed-unit SDD review.

### Plan-amendment execution barrier

No V&V authoring, Task backfill, Gate 9 recovery, bundle construction, Phase A
rerun, staging, deletion, or lifecycle mutation may start from this amendment
until this Plan is committed with exact subject
`docs(plan): integrate verification validation and tree object recovery` and
two fresh independent reviewers approve its exact predecessor-to-commit range
at C0/I0/M0: one specification reviewer and one documentation/security-quality
reviewer. A fix changes the reviewed range and repeats both reviews; the normal
five-round breaker applies. Review receipts remain controller evidence until
the later Task-only backfill, so this Plan does not self-assert its own review
result.

### File map

| Responsibility                   | Files                                                                                                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Execution evidence               | Create `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`; modify `docs/04.execution/tasks/README.md`                                               |
| Foundation                       | Create `workspace-baseline.md`, `scope-application-matrix.md` in the new pack                                                                                          |
| Agentic core                     | Create `harness-engineering.md`, `loop-engineering.md`, `provider-implementation-comparison.md`                                                                        |
| Agent instructions/models/memory | Create `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md`                   |
| SDLC contracts                   | Create `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `document-metadata-lifecycle.md`                                                                               |
| Documentation systems            | Create `documentation-architecture.md`, `llm-wiki-system.md`                                                                                                           |
| Delivery quality                 | Create `automation-pipeline-workflow.md`, `quality-ci-formatting.md`                                                                                                   |
| Verification and validation      | Create `verification-validation.md`; update the pack README and supporting owner-leaf cross-links; update Spec/Task routing evidence and generated LLM Wiki navigation |
| Infrastructure/security          | Create `docker-compose-infrastructure.md`, `security-governance.md`                                                                                                    |
| Human routing                    | Create new pack `README.md`; modify `docs/90.references/research/README.md` and other active clickable consumers discovered by the stale-path inventory                |
| Machine routing                  | Regenerate `docs/90.references/llm-wiki/llm-wiki-index.md` and `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`                                 |
| Retiring pack                    | Delete exactly the twenty files under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` after Task 11 gates pass                                 |
| Final evidence                   | Modify the Task and `docs/00.agent-governance/memory/current.md`; update a durable memory note only when the memory contract selects one                               |

## Goals and Non-goals

### Goals

- Author twenty focused, current leaves rather than moving or lightly editing
  old prose.
- Reconcile every old unique claim as retain, correct, omit, or supersede with
  immutable old commit/blob provenance.
- Cover every explicit research category, every SDLC document role, and every
  persona scope.
- Separate upstream capability, local definition, local execution,
  enforcement, runtime/remote proof, and gap.
- Keep all affected human and machine routes fresh after deletion.
- Produce reviewable logical commits and exact Task evidence.

### Non-goals

- Fixing provider, Compose, infrastructure, workflow, security, or deployment
  implementation gaps identified by the research.
- Correcting the security-readiness generator in this documentation-only
  workstream unless the user separately approves Task 10's narrow tested
  prerequisite.
- Resolving the 184 unrelated archive-direct-link predecessors.
- Refreshing Graphify without separate authorization.
- Inspecting secrets or proving live service, backup, restore, deployment, or
  remote GitHub state.

## Work Breakdown

### Task 1: Create the execution ledger and capture immutable baselines

**Files:**

- Create: `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: original Spec activation `35318255`, amended active Spec 137 at
  `af37969b26f7e96d684fa0fdf8a0ee2418a4ac23`, this Plan, and the old pack;
  Task 9a owns the immutable amendment-evidence backfill.
- Produces: the requirement, source/evidence, claim-migration,
  closed generated-artifact, old-path allowlist, verification, review, and commit
  ledgers consumed by every later task.

- [ ] **Step 1: Create the Task from the canonical template**

Use `docs/99.templates/templates/sdlc/task.template.md` and exact metadata:

```yaml
status: active
artifact_id: task:2026-08-08-agentic-research-pack-rebuild
artifact_type: task
parent_ids:
  - plan:2026-08-08-agentic-research-pack-rebuild
```

Populate every required heading with current evidence rather than prospective
PASS claims. Add tables for all 36 requirement IDs, all 14 scopes, external
and workspace sources, old claims, the closed generated-artifact inventory, old-path
allowlist, verification results, reviews, and commits.

- [ ] **Step 2: Pin the old file objects**

Run:

```bash
find docs/90.references/research/2026-07-05-agentic-research-pack-refresh \
  -maxdepth 1 -type f -printf '%f\n' | sort
git ls-tree -r HEAD \
  docs/90.references/research/2026-07-05-agentic-research-pack-refresh
```

Expected: 20 filenames and 20 blob records. Record the current commit and each
blob ID in the Task before any old file changes.

- [ ] **Step 3: Capture the validation predecessors**

Run and record exact exit/result summaries:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected design-time classifications: LLM index PASS; LLM coverage FAIL;
security readiness FAIL; alignment 184 predecessor findings; repository
contract dependency failure for `html5lib`. If current output differs, record
the observation without rewriting the design-time fact.

- [ ] **Step 4: Provision the isolated repository-contract environment**

Create a disposable virtual environment and install the repository-pinned
validation requirements, which include `html5lib>=1.1,<2.0`:

```bash
python3 -m venv /tmp/agentic-research-validation-venv
/tmp/agentic-research-validation-venv/bin/python -m pip install \
  --requirement scripts/requirements.txt
/tmp/agentic-research-validation-venv/bin/python -c \
  'import html5lib; print(html5lib.__version__)'
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
```

Expected: the import succeeds and the repository contract no longer fails for
the missing dependency. Record any remaining contract failure separately. If
the install cannot be authorized or completed, stop before Task 10 and keep
the deletion gate closed.

- [ ] **Step 5: Instantiate requirements and scopes**

Copy `REQ-01` through `REQ-36` verbatim from amended Spec 137 into the Task and create
one row for each of the fourteen normative scopes. Set unperformed evidence to
`Not Run`, not PASS.

- [ ] **Step 6: Validate and self-review the ledger**

Run:

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref 35318255 \
  --changed-path docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --changed-path docs/04.execution/tasks/README.md
bash scripts/validation/check-doc-traceability.sh
git diff --check
```

- [ ] **Step 7: Commit the execution-control unit**

```bash
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  docs/04.execution/tasks/README.md
git commit -m "docs(task): initialize agentic research rebuild ledger"
```

- [ ] **Step 8: Review the committed unit**

Run the committed-unit SDD protocol with the BASE recorded before Task 1.
Resolve every Critical/Important finding through implementer fix commits and
scoped re-review before Task 2.

### Task 2: Author the workspace foundation and scope axis

**Files:**

- Create: `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/workspace-baseline.md`
- Create: `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/scope-application-matrix.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-31, REQ-32, tracked workspace paths, scope files, typed
  registries, audit findings, and pinned baseline.
- Produces: current corpus/system counts and the fourteen-scope matrix every
  topic leaf cites.

- [ ] **Step 1: Re-measure the workspace**

Use `git ls-files`, `rg`, the typed contracts under
`docs/00.agent-governance/contracts/`, provider adapters, workflows, scripts,
templates, stages, and `infra/`. Record derivation commands and distinguish
tracked, ignored-local, runtime, and remote state. Re-derive all counts; do not
copy values from the old pack.

Run and preserve the exact derivations in the Task:

```bash
git ls-files > /tmp/agentic-research-tracked-paths.txt
find docs/00.agent-governance/scopes -maxdepth 1 -type f -name '*.md' \
  -printf '%f\n' | sort
sed -n '1,220p' docs/00.agent-governance/rules/persona.md
sed -n '1,220p' docs/00.agent-governance/contracts/agent-catalog.yaml
find docs/03.specs -mindepth 1 -maxdepth 1 -type d | wc -l
find docs/98.archive/03.specs -type f -name spec.md | wc -l
```

Expected scope filenames are exactly the fourteen names in Global
Constraints; the two spec counts are observations and must be recorded rather
than copied from the predecessor pack.

- [ ] **Step 2: Analyze all fourteen scopes**

Read every file under `docs/00.agent-governance/scopes/` plus
`rules/persona.md` and `contracts/agent-catalog.yaml`. For each normative scope,
record paths, applicable leaves, current state, rules, exceptions, evidence
owner, validation owner, and catalog reachability. Explicitly disposition the
six scopes outside the typed catalog.

- [ ] **Step 3: Apply the Stage 90 leaf contract**

Use the canonical reference template headings. Include concept/evidence,
workspace implementation, adoption environment/rules, scope impacts,
implementation status, limitations, gaps/owners, and direct dated sources.

- [ ] **Step 4: Validate and self-review**

Run the literal-path checks below and update the Task rows with actual results:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/workspace-baseline.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/scope-application-matrix.md
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
rg -n '^## Scope Implications|agentic|architecture|backend|common|docs|entry|frontend|infra|meta|mobile|ops|product|qa|security' \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{workspace-baseline,scope-application-matrix}.md
git diff --check
```

Expected: metadata/repository/diff checks PASS and the authored evidence
explicitly dispositions all fourteen scopes.

- [ ] **Step 5: Commit the foundation unit**

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/workspace-baseline.md \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/scope-application-matrix.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): establish workspace and scope baseline"
```

- [ ] **Step 6: Review the committed unit**

Run the committed-unit SDD protocol for Task 2 and complete its fix/re-review
loop before Task 3.

### Task 3: Author harness, loop, and Claude/Codex implementation analysis

**Files:**

- Create: new pack `harness-engineering.md`
- Create: new pack `loop-engineering.md`
- Create: new pack `provider-implementation-comparison.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-01 through REQ-05, foundation leaves, official Claude Code and
  Codex documentation, Stage 00 provider contracts, adapters, hooks, agents,
  skills, functions, harness, loops, and tests.
- Produces: harness/loop element models and the required Claude/Codex
  construction matrix.

- [ ] **Step 1: Reopen current official provider sources**

At minimum verify Claude hooks, subagents, settings/memory and Codex hooks,
subagents, AGENTS.md, skills, configuration, and model controls using current
official pages. Record access times and mutable-page status in the source
ledger.

The minimum direct source set is:

```text
https://code.claude.com/docs/en/hooks
https://code.claude.com/docs/en/sub-agents
https://code.claude.com/docs/en/settings
https://code.claude.com/docs/en/memory
https://learn.chatgpt.com/docs/hooks
https://learn.chatgpt.com/docs/agent-configuration/subagents
https://learn.chatgpt.com/docs/agent-configuration/agents-md
https://learn.chatgpt.com/docs/config-file/config-basic
https://learn.chatgpt.com/docs/models
```

Record redirects and unavailable pages as observations; do not silently reuse
the predecessor pack's retrieval result.

- [ ] **Step 2: Trace the local implementation**

Measure canonical role/function counts, provider projections, hook/event
bindings, harness layers, typed loops, eval fixtures/regressions, configured vs
executed depth, and unsupported mappings from tracked contracts and tests.
Correct known drift such as Codex `SessionEnd`, semantic-binding depth, Claude
effort overlays, and prose-loop counts from current evidence.

The minimum tracked surfaces are
`docs/00.agent-governance/contracts/{agent-catalog,provider-models}.yaml`,
`docs/00.agent-governance/providers/`, `.claude/`, `.codex/`, `.agents/`,
`.gemini/`, and the matching scripts/tests found with:

```bash
git ls-files docs/00.agent-governance .claude .codex .agents .gemini \
  scripts tests | sort
rg -n 'SessionEnd|semantic_binding|effort|loop|harness' \
  docs/00.agent-governance .claude .codex .agents .gemini scripts tests
```

- [ ] **Step 3: Build the common construction matrix**

Include exact columns from Spec 137: semantic capability, provider-neutral
contract, Claude native, Codex native, shared implementation, translation,
irreducibly native, tracked state, execution/enforcement evidence, and gap.

- [ ] **Step 4: Validate, self-review, and commit**

Validate the three leaf contracts and cross-links, update REQ-01 through
REQ-05 and claim mappings, and verify explicit fourteen-scope implications.
Run the exact metadata and hygiene checks, expecting PASS, then commit:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/harness-engineering.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/loop-engineering.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{harness-engineering,loop-engineering,provider-implementation-comparison}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): analyze harness loops and providers"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 3 and complete its fix/re-review
loop before Task 4.

### Task 4: Author instructions, models, agent catalogs, and memory

**Files:**

- Create: new pack `agent-instructions-vibe-coding.md`
- Create: new pack `provider-model-landscape.md`
- Create: new pack `agent-model-selection.md`
- Create: new pack `ai-agent-catalogs.md`
- Create: new pack `memory-hierarchy.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-28 through REQ-30, provider construction matrix, current
  provider model sources, local model registry/overlays, official agency-agents
  repository, and memory contracts.
- Produces: evidence-cutoff model landscape, task-aware selection rules,
  external-catalog intake boundary, and full memory lifecycle analysis.

- [ ] **Step 1: Verify mutable model and agent sources**

Reopen official Claude and OpenAI model/configuration sources. For
agency-agents, pin the exact upstream commit inspected and derive agent/division
counts from that revision; distinguish current upstream from the workspace's
historical immutable pin.

Use the official/model-owner sources
`https://docs.anthropic.com/en/docs/about-claude/models/overview`,
`https://code.claude.com/docs/en/model-config`,
`https://learn.chatgpt.com/docs/models`,
`https://learn.chatgpt.com/docs/config-file/config-reference`, and
`https://github.com/msitarzewski/agency-agents`. Resolve the agency-agents
default-branch commit with the GitHub API or an immutable commit page and store
that SHA plus the exact file-list/count command in the source ledger.

- [ ] **Step 2: Analyze local instruction and selection systems**

Trace instruction authority, context loading, tool/permission boundaries,
generated-code ownership, model tier/effort settings, fallback policy,
entitlement/runtime limits, evaluation needs, and coupled change surfaces.

Read the local owners explicitly:

```bash
sed -n '1,260p' docs/00.agent-governance/contracts/provider-models.yaml
sed -n '1,260p' docs/00.agent-governance/contracts/agent-catalog.yaml
sed -n '1,260p' docs/00.agent-governance/subagent-protocol.md
git ls-files .claude .codex .agents .gemini docs/00.agent-governance/memory | sort
```

- [ ] **Step 3: Analyze the memory lifecycle**

Cover short-term, long-term, domain memory, promotion, retrieval, retention,
eviction/deletion, archival, domain partition, privacy, size/freshness, and
provider-native memory boundaries. Re-measure current memory files and avoid
recording raw interaction data.

- [ ] **Step 4: Validate, self-review, and commit**

Update requirement/source/claim rows, validate all five leaves and their
fourteen-scope implications, self-review, and run:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/agent-instructions-vibe-coding.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/provider-model-landscape.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/agent-model-selection.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/ai-agent-catalogs.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/memory-hierarchy.md
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: metadata/repository/diff checks PASS, the agent-catalog SHA is
immutable, and all memory lifecycle dimensions have explicit evidence or gap
dispositions. Then commit:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{agent-instructions-vibe-coding,provider-model-landscape,agent-model-selection,ai-agent-catalogs,memory-hierarchy}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): analyze agents models instructions and memory"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 4 and complete its fix/re-review
loop before Task 5.

### Task 5: Author spec-driven SDLC and document contracts

**Files:**

- Create: new pack `spec-driven-sdlc.md`
- Create: new pack `sdlc-document-roles.md`
- Create: new pack `document-metadata-lifecycle.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-06, REQ-09 through REQ-21, current stage topology, templates,
  metadata profiles, lifecycle contracts, and primary SDLC/ADR/SRE sources.
- Produces: a current spec-driven lifecycle and separate role contracts for
  every requested document type.

- [ ] **Step 1: Re-measure the SDLC corpus**

Derive active/archive counts and lifecycle states from the current tree after
the 2026-08-08 archive migration. Do not reuse the old pack's `59 specs / 0
archived specs` conclusion.

Use the canonical stage/template/profile owners and record exact results:

```bash
find docs/01.product docs/02.design docs/03.specs docs/04.execution \
  docs/05.operations -type f -name '*.md' | sort
find docs/98.archive -type f -name '*.md' | sort
find docs/99.templates -type f -name '*.md' | sort
sed -n '1,280p' docs/00.agent-governance/rules/documentation-protocol.md
sed -n '1,260p' docs/99.templates/support/template-selection.md
sed -n '1,260p' docs/99.templates/support/lifecycle-status.md
```

- [ ] **Step 2: Verify primary sources**

Use official standards catalog pages where accessible, the ADR community and
original Nygard ADR article, current spec-driven tool repositories, NIST
incident guidance, Google SRE postmortem guidance, and official release/version
sources. Mark paywalled or rate-limited text `UNVERIFIED` instead of
paraphrasing unseen content.

Minimum primary/direct source routes are the IETF/RFC index at
`https://www.rfc-editor.org/`, Nygard's ADR article at
`https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions`, the
ADR organization at `https://adr.github.io/`, NIST SP 800-61 Rev. 3 at
`https://csrc.nist.gov/pubs/sp/800/61/r3/final`, Google SRE postmortem guidance
at `https://sre.google/sre-book/postmortem-culture/`, and immutable repository
commits for any spec-driven tool evaluated.

- [ ] **Step 3: Separate every document role**

Give PRD, ARD, ADR, Spec/child contract, Plan, Task, Guide, Incident,
Postmortem, Policy, Release, and Runbook separate rows for purpose, question,
trigger, owner, consumer, stage/path, template, lifecycle, relations, and
forbidden substitutions. Label ARD as local coinage and Release as distinct
from deployment proof.

- [ ] **Step 4: Validate, self-review, and commit**

Verify REQ-06 and REQ-09 through REQ-21 individually, validate three leaves,
their fourteen-scope implications, and all role rows. Run:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/sdlc-document-roles.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/document-metadata-lifecycle.md
bash scripts/validation/check-doc-traceability.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: all checks PASS and every named document role has a separate row.
Self-review, then commit:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{spec-driven-sdlc,sdlc-document-roles,document-metadata-lifecycle}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): define spec driven SDLC contracts"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 5 and complete its fix/re-review
loop before Task 6.

### Task 6: Author Diataxis and LLM Wiki analysis

**Files:**

- Create: new pack `documentation-architecture.md`
- Create: new pack `llm-wiki-system.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-22, REQ-23, Diataxis primary material, LLM-facing convention
  sources, repository templates/profiles, `llms.txt`, LLM Wiki generators, and
  current generated outputs.
- Produces: reader-mode architecture and machine-navigation/freshness design.

- [ ] **Step 1: Verify Diataxis and map document modes**

Reopen `https://diataxis.fr/` and record the access result. Analyze tutorial,
how-to, reference, and explanation by reader need; do not create empty folders
or confuse the lens with the normative SDLC stage taxonomy.

- [ ] **Step 2: Trace LLM Wiki generation and safety**

Read both generators, `llms.txt`, AGENTS/README discovery surfaces, metadata
profiles, safety exclusions, and actual generated files. Explicitly report that
repository contracts do not replace named byte-exact generator checks.

Use these exact local owners and baseline checks:

```bash
sed -n '1,260p' scripts/knowledge/generate-llm-wiki-index.sh
sed -n '1,320p' scripts/knowledge/generate-llm-wiki-coverage.sh
sed -n '1,220p' llms.txt
sed -n '1,220p' AGENTS.md
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

The index/coverage results are baseline observations in this authoring task;
Task 10 owns their canonical regeneration.

- [ ] **Step 3: Validate, self-review, and commit**

Update REQ-22/23 and relevant old claims, validate both leaves and their
fourteen-scope implications, self-review, and run:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/documentation-architecture.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/llm-wiki-system.md
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: document contracts and diff hygiene PASS; the Diataxis access result
and both named freshness baselines are recorded without conflation. Then:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{documentation-architecture,llm-wiki-system}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): analyze documentation and LLM wiki systems"
```

- [ ] **Step 4: Review the committed unit**

Run the committed-unit SDD protocol for Task 6 and complete its fix/re-review
loop before Task 7.

### Task 7: Author automation, CI/CD, GitHub Actions, and QA analysis

**Files:**

- Create: new pack `automation-pipeline-workflow.md`
- Create: new pack `quality-ci-formatting.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-24 through REQ-26, typed workflow registry/DAG, workflows,
  actions, local QA runner, pre-commit, tests, and official GitHub Actions
  documentation.
- Produces: exact tracked pipeline topology and separate QA capability states.

- [ ] **Step 1: Re-derive tracked automation topology**

Measure workflows, jobs, roots, gate nodes, profiles, actions, ordered
expansions, hooks, permissions, SHA pins, environment/deploy jobs, and local QA
steps from canonical tracked owners. Do not simplify ordered multi-leaf
expansion into a false one-job/one-command rule.

Run these non-mutating owners/checks and record their exact outputs:

```bash
python3 scripts/validation/check-github-workflow-contract.py
bash scripts/validation/run-local-qa-gates.sh --list
find .github/workflows .github/actions -type f | sort
sed -n '1,260p' .github/workflow-contract.yml
```

Expected: the typed workflow contract validates; `--list` reports the ordered
local-script-backed profile without executing it.

- [ ] **Step 2: Separate QA capabilities**

Analyze formatting, linting, syntax, type checking, unit/integration/E2E tests,
coverage, security scanning, failure propagation, retries, local/CI/remote
enforcement, CD, promotion, rollback, and observability separately.

- [ ] **Step 3: Verify current official GitHub sources**

Reopen workflow syntax, secure use, permissions, pinning, environments,
deployments, artifacts/attestations, rulesets, and monitoring pages. Record
remote control-plane state as `UNVERIFIED` unless an authorized observation is
actually performed.

Use direct GitHub Docs routes beginning with
`https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions`,
`https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions`,
`https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments`,
and `https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations`.

- [ ] **Step 4: Validate, self-review, and commit**

Complete requirement and claim rows, leaf checks, fourteen-scope implications,
and self-review. Run:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/quality-ci-formatting.md
python3 scripts/validation/check-github-workflow-contract.py
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: all local static checks PASS; remote enforcement remains separately
`UNVERIFIED`. Then:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{automation-pipeline-workflow,quality-ci-formatting}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): analyze delivery automation and quality"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 7 and complete its fix/re-review
loop before Task 8.

### Task 8: Author Docker Compose, infrastructure, and security analysis

**Files:**

- Create: new pack `docker-compose-infrastructure.md`
- Create: new pack `security-governance.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-07, REQ-08, REQ-27, Compose inventory/coverage, infra scopes,
  hardening/provenance scripts, security controls, and primary Docker/NIST/
  OWASP/SLSA/OpenSSF sources.
- Produces: configuration-grounded infrastructure/security state with explicit
  runtime limits.

- [ ] **Step 1: Re-measure Compose and infrastructure**

Derive Compose files, services, profiles, networks, ports, volumes, secrets,
images, pins/exceptions, hardening, gateway exposure, SLO, backup/restore, and
rollback evidence from tracked sources. Do not run Compose commands that create
`.env`, dummy secrets, networks, containers, or volumes.

Use only these non-mutating inventory/freshness routes for the baseline:

```bash
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
bash scripts/operations/generate-compose-profile-service-coverage.sh --dry-run
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --dry-run
bash scripts/hardening/check-all-hardening.sh
git ls-files 'docker-compose*.yml' 'docker-compose*.yaml' 'infra/**/*.yml' \
  'infra/**/*.yaml' | sort
```

Do not run `validate-docker-compose.sh`; its default path can create local
`.env`/dummy-secret evidence and can depend on live Docker networks.

- [ ] **Step 2: Reconcile scope requirements**

Apply `scopes/infra.md` and `scopes/security.md` requirements explicitly,
including gateway exposure exceptions, localhost binding, no-new-privileges,
persistent-volume backup evidence, latency SLO ownership, secret-read policy
conflict, supply chain, approvals, incident response, and secure SDLC.

- [ ] **Step 3: Handle the stale security snapshot honestly**

Run its `--check` and `--dry-run` modes without writing. Explain the typed
workflow-registry false-gap defect and derive current tracked control evidence
directly. Do not regenerate the known-invalid artifact.

```bash
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --dry-run
sed -n '1,220p' docs/00.agent-governance/scopes/infra.md
sed -n '1,220p' docs/00.agent-governance/scopes/security.md
```

The expected readiness check is FAIL for the known semantic predecessor. Task
8 records that result. Because the generated snapshot also links to the old
pack, Task 10 must stop for separate approval of a tested generator correction
before that snapshot can be regenerated canonically and the old pack deleted.

- [ ] **Step 4: Validate, self-review, and commit**

Complete REQ-07/08/27 rows, both leaf contracts, fourteen-scope implications,
and self-review. Verify this minimum direct current primary-source set and
record retrieval time/mutability:

```text
https://docs.docker.com/reference/compose-file/
https://csrc.nist.gov/pubs/sp/800/218/final
https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
https://owaspsamm.org/model/
https://slsa.dev/spec/v1.2/
https://github.com/ossf/scorecard
```

Treat NIST SP 800-218 as SSDF 1.1, the NIST publication as CSF 2.0, OWASP SAMM
as model 2.0, and SLSA as approved specification 1.2. Because the OpenSSF
Scorecard repository is mutable, record the exact inspected commit rather than
using `main` as immutable evidence. Then run:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255 \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md \
  --changed-path docs/90.references/research/2026-08-08-agentic-engineering-research-pack/security-governance.md
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: document, Compose coverage, provenance, repository, and diff checks
PASS; the security-readiness check remains a named FAIL predecessor. Then:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{docker-compose-infrastructure,security-governance}.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): analyze infrastructure and security"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 8 and complete its fix/re-review
loop before Task 9.

### Task 9: Build the pack router and prove complete coverage

**Files:**

- Create: new pack `README.md`
- Modify: `docs/90.references/research/README.md`
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-33, twenty reviewed leaves, 36 requirements, 14 scopes,
  source and claim ledgers.
- Produces: the human canonical route and pre-switch completeness verdict.

Task 9's final verdict is held open until Task 9a adds and reviews REQ-36 and
the twentieth leaf. A historical 19-leaf router commit is only an intermediate
checkpoint and is not current pack-completeness evidence.

- [ ] **Step 1: Author the pack README**

Include Stage 90 boundary, grouped twenty-leaf tree, current-state summary,
reading order, evidence classes, scope routing, maintenance rules, old/new
migration statement, and direct links to every leaf.

- [ ] **Step 2: Audit requirement, scope, source, and claim coverage**

Prove exactly 20 leaf files, 36/36 requirement destinations, 14/14 scope
dispositions, source entries for every load-bearing external claim, and a
disposition for every unique old claim. Any missing row stops this task.

```bash
find docs/90.references/research/2026-08-08-agentic-engineering-research-pack \
  -maxdepth 1 -type f -printf '%f\n' | sort
find docs/90.references/research/2026-08-08-agentic-engineering-research-pack \
  -maxdepth 1 -type f | wc -l
rg -n 'REQ-(0[1-9]|[12][0-9]|3[0-6])' \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
```

Expected: 21 regular files total (README plus 20 named leaves), exactly one
canonical destination for each of 36 requirements, and reviewed dispositions
for all fourteen scopes and all old-claim rows.

- [ ] **Step 3: Switch only the parent human router**

Update `docs/90.references/research/README.md` to name the new pack as the
canonical route and add the old path to its superseded mapping. Do not delete
or rewrite the old files yet.

- [ ] **Step 4: Validate, self-review, and commit**

Run all leaf metadata/link contracts, the closed matrices, whole-pack
preflight checks, and self-review:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255
bash scripts/validation/check-doc-traceability.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: all checks PASS, the parent research README points to the new pack,
and the old pack still exists. Commit:

```bash
git add docs/90.references/research/2026-08-08-agentic-engineering-research-pack/README.md \
  docs/90.references/research/README.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): route canonical agentic research pack"
```

- [ ] **Step 5: Review the committed unit**

Run the committed-unit SDD protocol for Task 9, using reviewers capable of
whole-pack requirement and documentation-quality review. Complete the fix/
re-review loop before Task 10.

### Task 9a: Integrate the verification-and-validation amendment before Gate 9

This separately reviewable unit is mandatory even when Tasks 1 through 9 have
already been committed. It starts only after the Plan-amendment execution
barrier above is satisfied. It adds REQ-36 and the twentieth leaf without
rewriting the retiring pack, then makes the 21-file/36-requirement cardinality
the only current contract consumed by Task 10, Gate 9, and Task 12.

**Files:**

- Create:
  `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/verification-validation.md`
- Modify:
  `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/README.md`
- Modify the parent category router:
  `docs/90.references/research/README.md`
- Modify these supporting owner leaves only to add precise supporting
  cross-links; `workspace-baseline.md` and `scope-application-matrix.md` also
  receive the required body cardinality/applicability updates, while the other
  eight change only their `Related Documents` links and keep their topical
  matrices authoritative:
  `workspace-baseline.md`, `scope-application-matrix.md`, `spec-driven-sdlc.md`, `sdlc-document-roles.md`,
  `document-metadata-lifecycle.md`, `llm-wiki-system.md`,
  `automation-pipeline-workflow.md`, `quality-ci-formatting.md`,
  `docker-compose-infrastructure.md`, and `security-governance.md`
- Modify `docs/03.specs/README.md` to change both stale Spec 137 `Draft`
  labels to `Active` without changing another Spec's status.
- Modify the execution Task for amendment provenance, REQ-36, source,
  workspace-owner, fourteen-scope, generated-artifact, verification, review,
  and commit evidence.
- Regenerate only through the canonical owners:
  `docs/90.references/llm-wiki/llm-wiki-index.md` and
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`.
- Modify `tests/validation/test_llm_wiki_retiring_pack_exclusion.py` to pin
  separate old-pack exactly-20 and new-pack exactly-21 inventories, the one
  new tracked safe path, and the exact generated cardinality deltas.

**Interfaces:**

- Consumes: amended active Spec 137 at
  `af37969b26f7e96d684fa0fdf8a0ee2418a4ac23`, the ignored V&V external-source
  report, the ignored workspace audit, the current tracked owner files, the
  14-scope matrix, and the independently reviewed Plan-amendment range.
- Produces: REQ-36 owner `verification-validation.md`, exactly 20 reviewed
  leaves/21 pack files, the exact 18-path implementation scope, 36/36 Task
  coverage, current Stage 03 and parent-category routing, explicit topical
  cross-links, and fresh generated navigation.

- [ ] **Step 1: Backfill immutable amendment authority in one Task-only unit**

From the clean, independently reviewed Plan-amendment `HEAD`, modify only the
Task. Record the Spec amendment commits `90eca714`, `76808636`, and
`af37969b`, aggregate range
`b77abacb610c853db3e9fef2bdef8cc7855c62a2..af37969b26f7e96d684fa0fdf8a0ee2418a4ac23`,
the exact external review report identities supplied by the controller, and
both final independent amended-Spec verdicts Approved C0/I0/M0. Also record
the exact Plan-amendment commit/range and its two external C0/I0/M0 receipts;
do not make the Task claim a review whose immutable controller evidence is
missing. Add REQ-36, its owner, all source/evidence rows, all 14 scope
dispositions, the target cardinalities, and set authoring/generator/review
results to `Not Run`.

```bash
VV_TASK_BASE=$(git rev-parse --verify HEAD)
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref "$VV_TASK_BASE" \
  --changed-path \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --check
git diff --name-only "$VV_TASK_BASE" --
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(task): record verification validation amendment"
```

Expected: metadata `selected=1 violations=0`; the changed and staged set is
exactly the Task. Dispatch one fresh specification reviewer and one fresh
documentation-quality reviewer over the exact Task-only range. Both must
return C0/I0/M0 before authoring begins. A fix receives its own commit and
both scoped re-reviews through the five-round breaker.

- [ ] **Step 2: Author the exact REQ-36 leaf contract from current primary sources**

Use the Stage 90 reference profile and exactly these nine H2 headings in this
order: `Overview`, `Purpose`, `Repository Role`, `Scope`,
`Definitions / Facts`, `Scope Implications`, `Sources`, `Maintenance`, and
`Related Documents`. Put the V&V system model and workspace-adoption rules
under `Definitions / Facts` as H3 sections; do not introduce a tenth H2.

The leaf must distinguish conformance verification from intended-use and
stakeholder-need validation; cover planning, entry/readiness, success and
exit/completion criteria, static/dynamic methods, traceability, independence
and risk-based depth, environments/data/oracles, defect disposition,
acceptance/decision authority, residual risk, release acceptance, monitoring,
and revalidation. Include all fourteen scopes with explicit `Direct`,
`Partial`, `Not applicable`, `Gap`, or `UNVERIFIED` limits: `agentic`,
`architecture`, `backend`, `common`, `docs`, `entry`, `frontend`, `infra`,
`meta`, `mobile`, `ops`, `product`, `qa`, and `security`.

Reopen these current official primary routes during implementation and record
access time, evidence class, supported claim, and limitation:

```text
https://standards.ieee.org/ieee/1012/7324/
https://www.iso.org/standard/90219.html
https://standards.ieee.org/ieee/12207/11416/
https://www.nasa.gov/reference/systems-engineering-handbook/
https://www.nasa.gov/reference/5-0-product-realization/
https://csrc.nist.gov/pubs/sp/800/218/final
https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final
https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software
https://docs.github.com/en/pull-requests/reference/status-checks
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
```

IEEE 1012-2024 and ISO/IEC/IEEE 12207:2026 are the current routes; mark IEEE
1012-2016 and 12207:2017 superseded/historical if mentioned. Public IEEE/ISO
pages support route, status, and abstract-level claims only; clause-level
normative claims require licensed access. NASA is official systems-engineering
guidance, NIST sources are bounded security/trustworthy-systems evidence, and
GitHub Docs prove available product semantics rather than this repository's
hosted enforcement. No source may be stretched into remote, runtime, release,
branch-protection, provider, Docker, secret, backup/restore, rollback, or
incident-exercise evidence.

- [ ] **Step 3: Re-measure and route workspace evidence without overclaiming**

Add one owner table with exact tracked path, exact command or gate,
baseline-specific count where meaningful, classification (`verification`,
`validation`, `both`, or `gap`), explicit implementation gap, and runtime
limit. At minimum cover Stage
contracts, changed metadata, traceability, implementation alignment, workflow
contract and typed gate runner, pre-commit, LLM Wiki freshness, security
readiness, lifecycle contracts, Compose structure, generated Compose and
tech-stack reports, hardening, template security, supply-chain fixtures,
Storybook/frontend gates, Python tests, and independent Task reviews.

Remeasure mutable counts at the implementation commit; do not copy the
ignored audit's `1669`, `26`, `64/42`, `7/23/80/16/3/8`, or other values
without rerunning its declared owner command. Preserve the status vocabulary
`configured`, `reachable`, `selected`, `executed`, `passed`, `reviewed`,
`hosted`, `enforced`, `runtime-observed`, and `UNVERIFIED`. The leaf must
include an explicit do-not-infer boundary for provider behavior, hosted
GitHub enforcement, Compose runtime, security posture, release acceptance,
and generated freshness.

Update the pack README to route 20 leaves in the Spec-defined groups and link
REQ-36. Add reciprocal supporting links from the ten owner leaves listed in
the file scope; update the baseline/scope bodies for 21-file/REQ-36 evidence,
but change only `Related Documents` in the other eight and do not move or
duplicate their detailed matrices. Update the Task requirement/source/scope/
workspace/generated ledgers and correct exactly the two stale `Draft` labels
for Spec 137 in `docs/03.specs/README.md` to `Active`.

Update exactly two current cardinality lines in the parent research README:
the structure-tree comment changes `19-leaf pack` to `20-leaf / 21-file pack`,
and the localized canonical-route sentence changes its leaf count from 19 to
20 and states that the pack contains 21 total files. Preserve its category
router structure: the parent links to the pack README, which owns the 20 direct
leaf routes. Do not add a direct `verification-validation.md` link to the
parent because that router does not enumerate individual leaves.

- [ ] **Step 4: Regenerate and prove the 21-file machine route**

First add a RED method
`test_verification_validation_leaf_changes_only_new_pack_cardinality` to the
focused LLM Wiki test. It must distinguish the retiring 20-file inventory from
the canonical 21-file inventory and fail while the leaf/output contract is
missing. Because both generators enumerate `git ls-files`, stage the new leaf
before invoking either generator; an untracked leaf is invisible and a
canonical write without this step is invalid. Stage no other path yet:

```bash
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_verification_validation_leaf_changes_only_new_pack_cardinality \
  -v
git add \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/verification-validation.md
git diff --cached --name-only
```

The RED must be attributable to the absent leaf/cardinality/output contract,
and the staged listing must contain exactly the new leaf. Then run the
canonical generators only after the new leaf and all routes are complete:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_verification_validation_leaf_changes_only_new_pack_cardinality \
  -v
```

Expected from current `af37969b`: tracked files change from 1,669 to 1,670 and
the currently reviewed 20-file-pack snapshots gain exactly one safe path and
no folder-index delta. The index changes from 1,338 to 1,339
path rows; coverage safe paths from 1,337 to 1,338;
`docs/90.references` from 95 to 96; `Reference and template docs` from 142 to
143; `Markdown reference` from 840 to 841; and `folder index` remains 221.
The parent research README is already tracked, so correcting its two text
lines changes none of these path-set or generated cardinalities.
Any other cardinality delta must be explained by an exact independently
reviewed path-set change before Gate 9. Subsequent proposed/actual deletion
runs are no-ops for these outputs because the exact retiring prefix is already
excluded; for the final 21-file pack they must remain byte-identical at
1,339 index rows and 1,338 coverage paths.

- [ ] **Step 5: Validate the exact implementation unit**

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref "$VV_TASK_BASE"
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_verification_validation_leaf_changes_only_new_pack_cardinality \
  -v
python3 - <<'PY'
from pathlib import Path

root = Path("docs/90.references/research/2026-08-08-agentic-engineering-research-pack")
files = sorted(path.name for path in root.iterdir() if path.is_file())
assert len(files) == 21, files
assert "README.md" in files
assert "verification-validation.md" in files
assert len([path for path in files if path != "README.md"]) == 20
PY
git diff --name-only "$VV_TASK_BASE" --
git diff --check
```

Expected: metadata, traceability, repository contracts, both generator checks,
and diff hygiene PASS; implementation alignment has zero attributable delta
and no increase over the pinned 184-finding predecessor; the Task proves
36/36 requirements and 14/14 scopes. The changed-path listing contains the
exact 18-path implementation scope, including the parent research README. The
embedded pack assertion is read-only with no placeholder values; Step 7 adds
the exact parent-router assertions required by the current recovery.
Self-review must distinguish that final 18-path scope from the immutable
initial 17-path commit described in Step 6.

- [ ] **Step 6: Stage, commit, and independently review the V&V unit**

Stage exactly the new leaf, pack README, ten supporting leaves, Stage 03
README, Task, the parent research README, the focused generator test, and two
generated outputs:

```bash
git add \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/verification-validation.md \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/README.md \
  docs/90.references/research/2026-08-08-agentic-engineering-research-pack/{workspace-baseline,scope-application-matrix,spec-driven-sdlc,sdlc-document-roles,document-metadata-lifecycle,llm-wiki-system,automation-pipeline-workflow,quality-ci-formatting,docker-compose-infrastructure,security-governance}.md \
  docs/90.references/research/README.md \
  docs/03.specs/README.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git diff --cached --name-only
git diff --cached --check
git commit -m "docs(research): add verification and validation system"
```

The normative staged listing contains exactly these 18 paths. Execution
instead produced immutable initial commit
`139ced00f7008f7161891aef6debfd67cefcfe7a`, exact range
`ac51a53211887a12bb18e2209aa3af1af6eb4b7f..139ced00f7008f7161891aef6debfd67cefcfe7a`,
with the previous 17-path listing and omitted only
`docs/90.references/research/README.md`. Do not amend, rebase, replace, or
otherwise rewrite that history. Its documentation-quality review returned
Needs fixes C0/I1/M0 because the two current parent-router cardinality lines
still described 19 leaves. The initial 17-path commit is therefore evidence,
not the final implementation contract; continue only through Step 7 after
this Plan correction receives its required independent reviews.

- [ ] **Step 7: Correct the parent router in one bounded two-path fix**

Start from clean reviewed Plan-correction `HEAD`, prove that
`139ced00f7008f7161891aef6debfd67cefcfe7a` is an ancestor, and capture that
`HEAD` as `VV_ROUTER_FIX_BASE`. Modify exactly the parent research README and
the execution Task. In the parent README, change only these two current lines:

1. Make the structure-tree suffix exactly
   `# Canonical human route for the rebuilt 20-leaf / 21-file pack`.
2. In the localized canonical-route sentence, replace the 19-leaf count with
   20 leaves and add the 21-total-file count. Preserve its single link to the
   pack README and add no direct leaf route.

In the Task, preserve the initial implementation commit and exact 17-path
range as immutable history; record the documentation-quality Needs fixes
C0/I1/M0 receipt supplied by the controller, the omitted parent-router path,
the exact two-line correction, and the final exact 18-path unique scope. Set
the two-path fix identity and both scoped re-reviews to `Not Run` until their
immutable evidence exists. Do not forward-claim review closure, Step 0e, Gate
9, deletion, runtime observation, remote state, or generated-output changes.

```bash
git merge-base --is-ancestor \
  139ced00f7008f7161891aef6debfd67cefcfe7a HEAD
VV_ROUTER_FIX_BASE=$(git rev-parse --verify HEAD)
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref "$VV_ROUTER_FIX_BASE" \
  --changed-path docs/90.references/research/README.md \
  --changed-path \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_verification_validation_leaf_changes_only_new_pack_cardinality \
  -v
python3 - <<'PY'
from pathlib import Path

parent = Path("docs/90.references/research/README.md").read_text(encoding="utf-8")
tree_route = (
    "2026-08-08-agentic-engineering-research-pack/ # Canonical human route "
    "for the rebuilt 20-leaf / 21-file pack"
)
pack_route = (
    "[2026-08-08-agentic-engineering-research-pack/README.md]"
    "(./2026-08-08-agentic-engineering-research-pack/README.md)"
)
assert parent.count("19-leaf pack") == 0
assert parent.count("19\uac1c leaf") == 0
assert parent.count(tree_route) == 1
assert parent.count("20\uac1c leaf, 21\uac1c file") == 1
assert parent.count(pack_route) == 1
assert "verification-validation.md" not in parent
PY
git diff --quiet "$VV_ROUTER_FIX_BASE" -- \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
test "$(git diff --numstat "$VV_ROUTER_FIX_BASE" -- \
  docs/90.references/research/README.md)" = \
  $'2\t2\tdocs/90.references/research/README.md'
test "$(git diff --name-only "$VV_ROUTER_FIX_BASE" -- | wc -l)" -eq 2
git diff --name-only "$VV_ROUTER_FIX_BASE" --
git diff --check
```

Expected: metadata `selected=2 violations=0`; traceability, repository
contracts, both generator checks, the focused test, and diff hygiene PASS;
alignment has no attributable increase over the pinned predecessor. The
changed set is exactly the parent README and Task. The generated outputs stay
byte-identical at 1,339/1,338 because this is an already-tracked content edit,
not a path-set change. Self-review must report the final implementation as the
union of the immutable initial 17 paths and the parent README: exactly 18
unique paths, with the Task intentionally revisited in the fix.

Stage and commit only the bounded fix:

```bash
git add \
  docs/90.references/research/README.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --cached --name-only
git diff --cached --check
git commit -m "docs(research): correct verification validation parent route"
```

The staged listing is exactly two paths. Dispatch fresh independent
specification and documentation-quality reviewers over
`VV_ROUTER_FIX_BASE..HEAD`; both must return C0/I0/M0. Any correction receives
its own commit and both scoped re-reviews within the five-round breaker. After
the reviews, complete Step 8; no downstream gate opens before its receipts are
durable. If rollback is required, first set
`VV_ROUTER_FIX_OID=$(git rev-parse --verify HEAD)` at the exact two-path fix,
then use targeted `git revert --no-commit "$VV_ROUTER_FIX_OID"`; never rewrite
or remove `139ced00`. Only the reviewed 18-path final implementation and its
Task evidence may feed Task 10, Step 0e, or Gate 9. Ignored research reports
remain advisory inputs, not durable authority.

- [ ] **Step 8: Close the implementation reviews in one Task-only evidence unit**

Start only after this Plan-fix range and the complete Step 7 fix range each
have both required C0/I0/M0 re-review receipts. From a clean `HEAD`, capture
`VV_TASK9A_CLOSURE_BASE=$(git rev-parse --verify HEAD)` and modify exactly
`docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`. Record
all of the following as immutable evidence without changing their history:

1. Initial implementation commit
   `139ced00f7008f7161891aef6debfd67cefcfe7a`, exact range
   `ac51a53211887a12bb18e2209aa3af1af6eb4b7f..139ced00f7008f7161891aef6debfd67cefcfe7a`,
   exact 17-path scope, and both initial controller receipts: specification
   Approved C0/I0/M0; documentation quality Needs fixes C0/I1/M0 because the
   parent research router's structure line still contained `19-leaf pack` and
   its localized canonical-route line still contained `19\uac1c leaf`.
2. Plan correction commit
   `c4ebff545a8dcb319beeb4fc16c053371126cc56`, exact range
   `139ced00f7008f7161891aef6debfd67cefcfe7a..c4ebff545a8dcb319beeb4fc16c053371126cc56`,
   and both initial Plan-review receipts: specification Needs fixes C0/I1/M0
   because Task 9a lacked an explicit Task-only immutable-evidence closure
   after the Step 7 reviews; documentation quality Approved C0/I0/M0. Also
   record the subsequent Plan-fix commit/range and both C0/I0/M0 re-review
   receipts exactly as supplied by the controller after they exist.
3. The reviewed Step 7 two-path fix commit/range, its exact scope of the parent
   research README plus this Task, and both scoped C0/I0/M0 re-review receipts.
4. The final union of the immutable initial implementation and correction:
   exactly 18 unique paths, one README plus 20 leaves in the 21-file pack,
   36/36 requirements, 14/14 scopes, and byte-unchanged generated outputs at
   1,339 index rows and 1,338 coverage paths.
5. Task 10 finalization, Step 0e, Gate 9, deletion, lifecycle reconciliation,
   runtime/remote action, and push remain `Not Run` and closed.

For the Step 8 row itself, write `Pending self-identity closure`, the literal
captured closure-base OID, the exact subject below, exact one-Task scope, and
closure-integrity reviews `Not Run`. Do not guess the commit's own OID or
claim its reviews before they run.

Validate the exact Task-only edit:

```bash
VV_TASK9A_CLOSURE_BASE=$(git rev-parse --verify HEAD)
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref "$VV_TASK9A_CLOSURE_BASE" \
  --changed-path \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
bash scripts/validation/check-doc-traceability.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_verification_validation_leaf_changes_only_new_pack_cardinality \
  -v
git diff --quiet "$VV_TASK9A_CLOSURE_BASE" -- \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
test "$(git diff --name-only "$VV_TASK9A_CLOSURE_BASE" -- | wc -l)" -eq 1
test "$(git diff --name-only "$VV_TASK9A_CLOSURE_BASE" --)" = \
  "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
git diff --check
```

Expected: metadata `selected=1 violations=0`; traceability and repository
contracts PASS; both generator checks and the focused test PASS; generated
bytes remain unchanged at 1,339/1,338; diff hygiene PASS; and the changed set
is exactly the Task.

Stage and commit exactly that one path:

```bash
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --cached --name-only
git diff --cached --check
git commit -m "docs(task): close verification validation implementation reviews"
VV_TASK9A_CLOSURE_OID=$(git rev-parse --verify HEAD)
git diff --check "$VV_TASK9A_CLOSURE_BASE" "$VV_TASK9A_CLOSURE_OID" --
git diff --name-only \
  "$VV_TASK9A_CLOSURE_BASE" "$VV_TASK9A_CLOSURE_OID" --
```

The staged and committed listing must contain exactly the Task. Dispatch one
fresh specification reviewer and one fresh documentation-quality reviewer
over the exact
`VV_TASK9A_CLOSURE_BASE..VV_TASK9A_CLOSURE_OID` closure range. Each external
controller receipt must record both literal OIDs, the exact range, reviewer
identity, verdict, and finding disposition; these two receipts are the
immutable identity of the closure commit, so the Task intentionally does not
attempt to embed its own SHA. No extra Task backfill exists solely to repeat
that SHA.

Both closure-integrity reviewers must return C0/I0/M0. The initial closure is
review round 1; any nonzero Critical, Important, or Minor finding receives one
Task-only fix commit and both re-reviews in rounds 2 through 5. If either
review remains nonzero after round 5, mark the unit blocked and stop; there is
no round 6 and no downstream execution. Before a successor consumes the
closure, rollback only with the targeted command below; if reviewed fix
commits exist, revert them newest to oldest before the initial closure. Never
amend, rebase, reset, or rewrite the initial implementation, Plan corrections,
or Step 7 fix.

```bash
git revert --no-commit "$VV_TASK9A_CLOSURE_OID"
```

### Task 10: Switch cross-links and machine-generated routes

**Files:**

- Modify: every tracked clickable consumer found by the exact old-slug scan
- Conditional on separate user approval: modify
  `scripts/validation/generate-security-automation-readiness.sh` to resolve the
  typed workflow registry and retarget its two old-pack destinations
- Conditional on that approval: modify
  `tests/validation/test_security_automation_readiness.py` and regenerate
  `docs/90.references/data/security/security-automation-readiness.md` only
  through its canonical generator
- Modify: `docs/90.references/llm-wiki/llm-wiki-index.md` through its generator
- Modify: `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` through its generator
- Modify: `scripts/knowledge/generate-llm-wiki-index.sh` and
  `scripts/knowledge/generate-llm-wiki-coverage.sh` to exclude only the exact
  retiring research-pack directory while it remains tracked during the
  pre-deletion review window
- Create: `tests/validation/test_llm_wiki_retiring_pack_exclusion.py` for the
  exact-prefix exclusion and sibling-route retention contract
- Modify: `scripts/validation/check-document-metadata.py` to remove only the
  retiring pack's sixteen mutable `APPROVED_MIGRATION_PATHS` exceptions while
  preserving the seven commit-pinned target-surface baseline selectors
- Modify: `tests/validation/test_document_metadata.py` with a focused
  mutable-exception removal and immutable-baseline preservation regression
- Modify: execution Task ledgers

**Interfaces:**

- Consumes: REQ-34, new canonical route, full tracked text, reviewed historical
  non-link allowlist.
- Produces: zero clickable old-pack references and fresh machine navigation
  while both packs still exist.

- [ ] **Step 1: Inventory every old-path occurrence**

Run:

```bash
git grep -n -I '2026-07-05-agentic-research-pack-refresh' -- \
  ':!docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**'
```

Classify every result as clickable route, current canonical statement, or
factual historical non-link literal. Retarget every non-generated clickable
route. Assign the generator-owned security snapshot occurrence to Step 2; do
not edit it directly. Record each permitted non-link literal by path, stable
anchor, reason, and reviewer. Write the exact reviewed non-generated
changed-consumer paths, one per line, to
`/tmp/agentic-research-route-paths.txt`; this staging list is never committed.

- [ ] **Step 1a: Retire mutable metadata exceptions and preserve pinned baseline evidence**

The seven paths in `TARGET_SURFACE_DIRECT_SOURCE_PATHS` and the matching YAML
list are not current routing exceptions: they select files from baseline
commit `32c40e11747bc0bd03789c24861d2e5d60c0e999` for an already reviewed,
blocking 483-row manifest. Preserve those exact seven selectors, their seven
manifest rows, and seven plain-text summary rows as immutable historical
evidence. Record all four owning files in the reviewed non-link allowlist with
the wave, baseline commit, stable anchors, and reason. Run and classify the
canonical `check-manifest`, `check-promoted`, and `check-summary` modes against
their exact measured predecessors; do not regenerate or silently re-promote
the historical manifest before deletion.

By contrast, the sixteen old-pack entries in `APPROVED_MIGRATION_PATHS` are
mutable current exceptions and may not survive deletion. Add a focused RED
assertion proving those sixteen entries exist before the production edit.
Then remove only those exact-prefix exceptions from
`scripts/validation/check-document-metadata.py`. Do not replace them with new
pack entries: the new documents must satisfy current metadata contracts
without a migration exception.

The GREEN test must assert all of these boundaries directly:

- old and new research-pack prefixes are both absent from
  `APPROVED_MIGRATION_PATHS`;
- the exact seven Python/YAML baseline selectors remain equal;
- the promoted manifest and generated summary retain exactly seven matching
  historical rows and stay pinned to the original wave/baseline;
- the pre/post exception-set difference is exactly the sixteen old-pack rows;
- audit-pack exceptions and the Spec 123/related Stage 04 sentinels are
  unchanged.

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-manifest --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-promoted
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-summary --wave target-surface-convergence
```

The root branch baseline for these lifecycle checks is already nonzero:
`check-manifest=9`, `check-promoted=25`, and `check-summary=9`. The Task 10
pre-route Plan-correction baseline is `9/26/9`; the additional promoted finding
is recorded workstream evidence outside these seven rows. Expected: the new
regression and existing parity checks PASS; all seven pinned rows remain
byte-identical in the manifest/summary; no lifecycle finding is attributable to
the mutable-exception removal; and totals do not increase. Do not report the
three lifecycle commands as PASS. The complete literal scan reports no
retiring-pack value in mutable migration exceptions; only reviewed
pinned-baseline literals remain in these four historical-evidence owners.

- [ ] **Step 2: Pass the separately approved security-generator prerequisite**

The security-readiness generator and its generated snapshot both contain two
clickable destinations to the retiring pack. The snapshot cannot be hand-edited
and cannot be regenerated truthfully until the generator resolves commands in
`.github/workflow-contract.yml` rather than relying only on raw workflow text.
Before changing either file, obtain explicit user approval for this narrow
non-documentation scope. Without that approval, stop Task 10, preserve both
packs, and do not enter the deletion gate.

After approval, use test-driven remediation in
`tests/validation/test_security_automation_readiness.py`: add failing fixtures
for typed gate/action resolution, correct the generator, and retarget its two
destinations to
`../../research/2026-08-08-agentic-engineering-research-pack/security-governance.md`.
Then run the canonical write/check sequence:

```bash
python3 -m unittest discover -s tests/validation \
  -p 'test_security_automation_readiness.py'
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
```

Expected: focused tests PASS, the generated snapshot is byte-exactly fresh,
its control rows are supported by typed registry resolution, and its only
research-pack destinations use the new canonical route. Inspect the full
generated diff; do not preserve the earlier false counts merely to minimize
changes.

- [ ] **Step 3: Commit and review the approved generator repair**

Commit this non-documentation prerequisite separately from routing:

```bash
git add scripts/validation/generate-security-automation-readiness.sh \
  tests/validation/test_security_automation_readiness.py \
  docs/90.references/data/security/security-automation-readiness.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "fix(validation): resolve typed security automation gates"
```

Run the normal two-reviewer committed-unit SDD protocol over this exact commit
range. Both specification and quality verdicts must be C0/I0 before any human
or LLM route switch.

- [ ] **Step 4: Correct the retiring-path projection and regenerate LLM Wiki outputs canonically**

The existing generators enumerate every safe path returned by `git ls-files`.
While both packs coexist, a canonical write therefore recreates twenty
clickable old-pack rows and makes the zero-clickable-reference pre-deletion
gate impossible to satisfy. Treat this as a fail-closed generator defect, not
as a historical-literal exception: generated navigation has no allowlist.

First add focused RED fixtures proving that both generators include the exact
retiring prefix before the production change. Then add a shared, literal
prefix exclusion for only:

```text
docs/90.references/research/2026-07-05-agentic-research-pack-refresh/
```

The focused test must run both canonical generators in a temporary Git fixture
containing the twenty-file retiring pack, the twenty-one-file new pack,
similarly named Stage
04 Plan/Task history, and an exact-prefix sibling such as
`2026-07-05-agentic-research-pack-refresh-notes/README.md`. Its RED comparison
uses the coexisting tracked-path tuple versus the same canonical NUL-safe tuple
with exactly the twenty retiring paths removed in memory; no Git index or
filesystem projection is an oracle. Before the filter, it must observe exactly these
coverage deltas: safe paths `-20`, `docs/90.references` `-20`, `Reference and
template docs` `-20`, `folder index` `-1`, and `Markdown reference` `-19`.

The GREEN assertions must prove that the coexisting-pack outputs match the
in-memory projected path tuple for both generators, all twenty retiring-pack
paths are absent, and all twenty-one new-pack paths, Stage 04 history, and
the exact-prefix sibling remain present. Step 0e later replaces this path-tuple
oracle with the stronger raw-tree/sealed-manifest authority replay. Do not use
a substring or date-wide exclusion. Run:

```bash
python3 -m unittest \
  tests.validation.test_llm_wiki_retiring_pack_exclusion -v
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

Expected: the focused test and both checks PASS. Inspect diffs for only the
new-pack additions, exact retiring-pack exclusions, and derived count changes.
After the old pack is actually deleted, the same filter becomes a no-op over
`git ls-files`; it remains explicit lifecycle documentation until a separately
reviewed cleanup removes it.

Rerun the complete retiring-path literal scan after the generator and test
edits. Record their exact prefix constants as reviewed lifecycle non-link
literals in the Task allowlist with path, stable anchor, reason, and review
verdict. They are not clickable-route exceptions.

- [ ] **Step 5: Run the pre-deletion path/link checks**

Run the exact checks below. Repository contracts must pass; the alignment
result must add zero attributable findings and not increase the pinned 184
predecessor:

```bash
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-implementation-alignment.sh
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 35318255
bash scripts/validation/check-doc-traceability.sh
git grep -n -I '2026-07-05-agentic-research-pack-refresh' -- \
  ':!docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**'
git diff --check
```

- [ ] **Step 6: Self-review and commit the route-switch unit**

Confirm every line in the staging path list is a classified route consumer,
self-review the route, generator/test, and generated diffs, then stage only
that list, the two generators, their focused test, the metadata validator,
its focused test, the two generated outputs, and the Task:

```bash
git add --pathspec-from-file=/tmp/agentic-research-route-paths.txt
git add scripts/knowledge/generate-llm-wiki-index.sh \
  scripts/knowledge/generate-llm-wiki-coverage.sh \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py \
  scripts/validation/check-document-metadata.py \
  tests/validation/test_document_metadata.py \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(research): switch agentic pack links and indexes"
```

- [ ] **Step 7: Review the committed route-switch unit**

Run the committed-unit SDD protocol for Task 10 with migration and quality
verdicts. Complete the fix/re-review loop before Task 11.

### Task 11: Pass the deletion gate and remove the old pack

**Files:**

- Delete: exactly 20 files under the old pack directory
- Modify before any deletion review:
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md`
  by preserving its reviewed direct Spec and Task provenance
- Modify before any deletion review:
  `docs/99.templates/support/document-metadata-profiles.yaml` and
  `tests/validation/test_document_metadata.py` so the audit profile admits an
  archived SDLC parent without widening any other profile
- Add before any new Gate 9 attempt:
  `scripts/validation/agentic-research-gate9-evidence.py` and
  `tests/validation/test_agentic_research_gate9_evidence.py` for canonical
  package, receipt, closure, evidence-ref, and authorization validation
- Verify, but expect no byte changes in:
  `docs/90.references/llm-wiki/llm-wiki-index.md` and
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`
  after rerunning their generators against the proposed and actual deletion
- Modify: `docs/90.references/data/governance/target-surface-delta-manifest.yaml`
  by adding exactly the six changed target paths missing at the Task 10b commit
- Modify: `docs/90.references/data/governance/target-surface-delta-summary.md`
  only through `check-target-surface-delta-contract.py --write-summary`
- Modify: `docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml`
  after the deletion commit by changing exactly seven pinned old-pack rows and
  the already-archived Spec 133 source row to evidenced `delete` results
- Modify: `docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md`
  only through the lifecycle summary generator
- Modify: `tests/validation/test_target_surface_delta_contracts.py` and
  `tests/validation/test_target_surface_contracts.py` for the exact new
  lifecycle evidence and generated-summary contracts
- Modify: execution Task ledger with proposed-deletion, staged-deletion,
  recoverability, freshness, review, and commit evidence

**Interfaces:**

- Consumes: REQ-33, REQ-34, reviewed new pack, complete claim ledger, zero
  clickable old-path references, fresh LLM outputs, and all pre-deletion
  validation evidence.
- Produces: sole active canonical pack and a recoverable deletion commit.

- [ ] **Step 0: Clear the changed-document metadata blocker in a reviewed unit**

The Task 10 route switch makes the active audit overview part of the changed
document set. Its frontmatter currently names both the completed remediation
Task and the now-archived Spec 123 as direct parents. The audit profile permits
the Task parent but not an archive parent, so the mandatory changed-document
metadata gate fails with one `invalid-parent-type` finding. This is a real
deletion blocker, not an allowed predecessor.

Use the existing validator as the RED test and record the single expected
finding before editing:

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref 35318255 \
  --changed-path \
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md
```

The first bounded repair removed only the direct Spec parent and kept
`task:2026-07-11-agentic-engineering-audit-remediation`, whose own typed
parents retain the archived Spec and current Plan provenance. That repair made
the metadata command GREEN but changed the promoted target's `parent_ids`, so
the target-surface lifecycle checkpoint increased from `9/26/9` to
`10/27/10`. Record the attempted repair and its reviews as historical execution
evidence, but do not treat it as permission to enter the deletion gate.

- [ ] **Step 0b: Reconcile the audit archive-parent contract without lifecycle drift**

The audit overview's direct Spec 123 parent is reviewed target-surface
provenance and must remain byte-equal to the blocking manifest. The typed audit
profile currently permits `spec`, `plan`, `task`, `reference`, and `audit`
parents, but not the same Spec after it is represented by its Stage 98
`artifact_type: archive`. This creates a lifecycle-dependent type error for an
otherwise unchanged relation. Resolve the contract rather than rewriting the
promoted target or its lifecycle evidence.

First add a focused RED assertion to
`tests/validation/test_document_metadata.py` requiring the audit profile's
exact allowed-parent sequence to be
`[spec, archive, plan, task, reference, audit]`; inserting `archive`
immediately after `spec` preserves the existing relative order while making
the promoted archived-Spec parent sort before the Task parent. The test must
use a literal expected parent-type mapping for every profile rather than derive
the unchanged values from the edited registry, so the audit delta is exactly
one inserted type and no other profile can drift. Record that the test fails
before the profile edit. Then:

1. restore only `spec:123-agentic-engineering-audit-remediation` to the audit
   overview beside its existing Task parent;
2. insert only `archive` immediately after `spec` in the audit profile's
   `allowed_parent_types`; and
3. leave the target-surface manifest, summary, and all other profiles
   byte-identical.

Run the focused test, the full metadata module, focused and full
changed-document metadata checks, traceability, repository contracts, and the
three target-surface lifecycle checkpoint modes. GREEN requires metadata exit
0 and the lifecycle checkpoint returning exactly to `9/26/9`, with no new
finding or generated lifecycle write. Commit the overview, typed profile,
focused test, and Task evidence as one separate logical unit. Require two fresh
independent committed-unit reviews at C0/I0 before restarting deletion gates 1
through 8. Any broader parent-type change, manifest/summary mutation, or
failure to restore `9/26/9` is a blocker.

- [ ] **Step 0c: Install and review the finite Gate 9 evidence contract**

The previously reviewed filesystem package artifacts were built at
`6025478eddc1e0a15e2633b195b1781e9ce1d031`. They became stale when later
Plan commits advanced `HEAD` and are historical diagnostics only. They cannot
authorize deletion and must not be copied into a new attempt.

Add `scripts/validation/agentic-research-gate9-evidence.py` and
`tests/validation/test_agentic_research_gate9_evidence.py`. The helper owns
only this deletion gate's evidence state; it must never remove a worktree file,
write a generated output in the current worktree, write the real Git index,
advance the current branch, or update a remote ref. Step 0d supersedes the
round-5 projection only as historical evidence and then failed its own breaker.
Step 0e removes every filesystem/index projection, generator-write,
materialization, and cleanup path. The finite evidence state machine, logical
package/evidence schemas, attempt bounds, and reviewer identity contract below
remain unchanged.

**Amendment, 2026-08-17: Step 0e is no longer gating.** This step's text
previously called Step 0e "the sole current recovery" for pre-deletion gate 9.
That clause is withdrawn. The user approved a Spec 137 deletion-evidence
decoupling amendment on 2026-08-17, recorded in that Spec's `Deletion-evidence
decoupling amendment` section, under which pre-deletion gate 9 is satisfied by
the Task recording the before/after file manifest, deletion diff, recovery
commit, and reviewer verdict directly. That is what Spec 137's gate 9 text
already required.

Consequences for this step, and nothing beyond them:

- Step 0e and its helper become a separately tracked durability enhancement.
  Every constraint in this step and in the Spec's Gate 9 evidence architecture
  boundary continues to govern the helper whenever it is exercised.
- Step 0e is not a precondition for deletion, lifecycle reconciliation, or any
  pre-deletion gate. Its round accounting no longer bounds deletion: four of
  five implementation rounds are consumed, and round 5 is available for the
  enhancement track but is not required by any gate.
- Every statement elsewhere in this retained historical Plan that makes a Gate 9
  package, bundle, evidence ref, or Step 0e round a condition of deletion is
  historical and not executable. Where such a statement conflicts with this
  amendment, this amendment governs.
- Four per-fix statements in the Plan-only correction gate below record the
  implementation count as three of five. Each was accurate when written, before
  round 4 landed, so they are preserved as pre-round-4 records rather than
  rewritten. The current count is the one stated in this amendment.
- Nothing else changes. All nine pre-deletion gates and every post-deletion gate
  stay in force verbatim, and deletion stays unauthorized until each is
  independently satisfied and recorded in the Task.
- The tracked-direct-deletion-controller design on the unmerged branch is not
  adopted and grants no authority here, per the same Spec section.

Its public modes are:

```text
build-package
verify-package
verify-assignments
verify-backfill
publish-evidence-ref
verify-authorized
```

Use TDD. RED must cover stale package `HEAD`, attachment or checksum drift,
non-canonical JSON, unsorted attachment sets, duplicate/colliding reviewers,
any Critical or Important count, a Task edit outside the one Gate 9 marker,
dirty real-index state, an existing non-identical evidence ref, and a third
attempt. GREEN must prove the valid two-reviewer path without changing the
branch, real index, old pack, lifecycle artifacts, or generated outputs.

Add one unique `GATE9-EVIDENCE/v1` marker block to the Task before the first
package build. Its initial state is `PACKAGE_REVIEW_PENDING` with attempt 1.
There are only two forward marker paths:

```text
PACKAGE_REVIEW_PENDING(attempt 1) -> TASK_BACKFILLED
PACKAGE_REVIEW_PENDING(attempt 1) -> ATTEMPT_2_PENDING
ATTEMPT_2_PENDING                  -> TASK_BACKFILLED
```

The `ATTEMPT_2_PENDING` transition is allowed only after a create-only attempt
1 evidence ref records `REJECTED` or `INVALIDATED` before any backfill. It must
record that ref, package ID, tree identity, terminal state, and finding or
drift reason. Attempt 2 is not available after `TASK_BACKFILLED`; any closure,
publication, or authorization failure after backfill is immediately
`BLOCKED`. An attempt 2 failure is also `BLOCKED`.

The successful transition to `TASK_BACKFILLED` contains the proposed deletion
manifest/diff and recovery commit; package hash and fixed evidence-ref name;
both package-review receipt identities, hashes, roles, verdicts, and C/I/M
counts; and the explicit statement that actual staged and committed deletion
reviews remain `Not Run`. Claims, destinations, requirements, scopes,
allowlist membership, sources, generated artifacts, and every byte outside the
marker are immutable during each marker transition. Between a durably rejected
attempt 1 and attempt 2 package construction, an implementer may correct only
the reviewer-identified Task prose outside the marker; that correction becomes
part of attempt 2's frozen `task-candidate.md`.

Commit the helper, tests, pending marker, and Task evidence as one logical
unit, then require two fresh independent committed-unit reviews at C0/I0.
Record those reviews in a separate Task-only closure commit before entering a
Gate 9 attempt. Round 5 did not satisfy that gate: the Step 0d prerequisite
below first closes the Task's stale review evidence, then the separately
approved recovery unit must close before Phase A. The first package must
therefore be rebuilt at the resulting clean, live reviewed `HEAD`; neither
existing `/tmp` package is reusable.

- [x] **Historical Step 0d: failed Gate 9 projection recovery (`BLOCKED`, superseded by Step 0e)**

Everything from this heading through the final Step 0d breaker paragraph is
immutable execution history, not an executable alternative or fallback. Step
0e removes its filesystem-backed projection and transport from every current
Gate 9 path. No command or interface in this historical block may be reused.

On 2026-08-09 (Asia/Seoul), after the Step 0c round-5 breaker, the user
explicitly approved this Plan correction and the recommended separately
bounded recovery design: a temporary Git index plus `--stdout` execution of
the two canonical LLM Wiki generators. That approval does not authorize
executing the round-5 helper, a package-selected or historical generator blob,
constructing or consuming a Gate 9 package, publishing an evidence ref,
staging deletion, or any other closed action. Recovery implementation may
start only after the Task-only evidence prerequisite below is committed and
independently approved; all unsafe execution remains prohibited. The round-5
implementation commit is
`4796b46225a019343888557343ca7ca9938fb36a`, exact range
`71cff032aed5f469d59b4f8406b5d9b78a9a4e8d..4796b46225a019343888557343ca7ca9938fb36a`.
Its fresh committed-unit specification review returned C0/I1/M1 and its fresh
Python/security review returned C0/I1/M0. The combined blockers are
load-bearing: later authority modes can accept a canonically resealed package
without freshly replaying the deletion projection, and the linked-worktree
cleanup still permits recursive/path-based cleanup after ancestor
substitution. The specification Minor is not parked; this recovery must close
all findings at C0/I0/M0.

This is a new recovery task with its own independently bounded five-round SDD
breaker. It is not round 6 of Step 0c, does not reopen or reset the two-attempt
Gate 9 evidence state machine, and does not consume a Gate 9 attempt. Recovery
round 1 is the first committed implementation below; each subsequent round is
one reviewer-driven fix commit over the exact preceding range. Every round
gets two fresh independent committed-unit reviews, one for specification and
one for Python/security. Any finding after recovery round 5 stops execution
for a new user decision. Phase A, Gate 9 package construction, evidence-ref
publication, real-index staging, old-pack deletion, lifecycle reconciliation,
Task 12, remote actions, and push remain closed throughout Step 0d.

**Pre-implementation prerequisite — close the round-5 Task evidence only:**

1. From the clean Plan-correction `HEAD`, modify only
   `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`.
   Replace the stale round-5 identity and `Not Run` review claims with exact
   commit `4796b46225a019343888557343ca7ca9938fb36a`, exact range
   `71cff032aed5f469d59b4f8406b5d9b78a9a4e8d..4796b46225a019343888557343ca7ca9938fb36a`,
   the formal specification verdict C0/I1/M1, and the formal Python/security
   verdict C0/I1/M0. Adjudicate Step 0c as `BLOCKED`, record the exact
   2026-08-09 approval boundary above, keep Gate 9/deletion/lifecycle/Phase A
   closed, and record Step 0d implementation and its reviews as `Not Run`.
   Do not imply that approval waived either blocker or authorized unsafe
   package-controlled execution.
2. Validate the focused Task-only delta before commit:

   ```bash
   STEP0D_TASK_BASE=$(GIT_NO_REPLACE_OBJECTS=1 git rev-parse --verify HEAD)
   python3 scripts/validation/check-document-metadata.py \
     --mode check-changed \
     --base-ref "$STEP0D_TASK_BASE" \
     --changed-path \
     docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
   git diff --check
   git diff --name-only "$STEP0D_TASK_BASE" --
   ```

   The final command must list only the Task, and the diff must contain no
   implementation or generated-output change.

3. Commit that one-file evidence closure with exact subject
   `docs(task): record gate 9 recovery approval`. Dispatch two fresh,
   independent committed-unit reviews over that exact Task-only range: one
   specification review and one Python/security review. Both must return
   C0/I0/M0. The Task-only commit becomes the clean reviewed closure `HEAD`
   only after both verdicts arrive; it does not self-assert those verdicts.
   Record their immutable receipts in the controller evidence for later Task
   closure, then start recovery round 1 from that unchanged reviewed `HEAD`.
   Any finding keeps Step 0d `Not Run` and returns to Plan correction.
   Immediately after commit, require
   `git diff --name-only "$STEP0D_TASK_BASE" HEAD --` to print only the Task
   path and `git diff --check "$STEP0D_TASK_BASE" HEAD --` to pass.

**Exact implementation scope (six files):**

1. Modify
   `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` only
   to preserve the already reviewed approval/blocker closure, record Step 0d
   RED/GREEN/full command evidence and recovery round state, leave the new
   implementation reviews `Not Run`, and preserve the closed-gate state. The
   later Task-only closure—not this six-file commit—records the exact
   implementation commit/range and completed review verdicts.
2. Modify `scripts/validation/agentic-research-gate9-evidence.py` for the
   projected-index authority verifier and descriptor-pinned scratch lifecycle.
3. Modify `tests/validation/test_agentic_research_gate9_evidence.py` for the
   helper's focused security, authority-path, projection, and state-invariant
   regressions.
4. Modify `scripts/knowledge/generate-llm-wiki-index.sh` to add `--stdout`.
5. Modify `scripts/knowledge/generate-llm-wiki-coverage.sh` to add `--stdout`.
6. Modify `tests/validation/test_llm_wiki_retiring_pack_exclusion.py` for
   stdout parity and write-free generator coverage.

No generated-output file is in scope. The stdout bytes must remain identical
to the two tracked canonical outputs, and the existing write and `--check`
behaviors must remain byte-compatible. Therefore this recovery expects no diff
in `docs/90.references/llm-wiki/llm-wiki-index.md` or
`docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`; any
generated-output diff is a blocker, not an additional file to stage.

**Generator interfaces:**

```text
bash scripts/knowledge/generate-llm-wiki-index.sh [--check|--stdout]
bash scripts/knowledge/generate-llm-wiki-coverage.sh [--check|--stdout]
```

No argument retains canonical write mode and its current status message.
`--check` retains its current comparison, exit status, and PASS/FAIL messages.
`--stdout` is mutually exclusive with `--check`, writes no repository file or
directory, and emits exactly the rendered UTF-8/LF Markdown bytes to stdout
with no banner, status, diagnostic, or other non-Markdown byte. Usage errors
remain exit 2 and diagnostics remain on stderr.

**Projected-index and authority interfaces:**

- Replace `projected_generated_outputs(root, commit)` and all production
  linked-worktree helpers with one index-only projection result containing the
  package `HEAD`, live reviewed `HEAD`, reviewed Step 0d code commit, initial
  tree OID, final tree OID, exact old-path tuple, exact `D` status tuple,
  proposed binary deletion patch, and both generated stdout byte strings.
- Add one common authority preflight used by `build-package`,
  `verify-package`, `verify-assignments`, `verify-backfill`,
  `publish-evidence-ref`, and both `verify-authorized` package sources. Every
  invocation requires `--require-live-head`,
  `--live-reviewed-head FULL_OID`, and `--reviewed-code-head FULL_OID`;
  omission of any binding fails with `LIVE_HEAD_REQUIRED` and exit 2 before
  projection or shell execution. In particular,
  the retired path-selected package verification without the live binding is a
  verification
  usage failure, cannot execute a generator, and cannot authorize projection.
  For each external-bundle source, parser validation and the controller-bound
  transport read/hash comparison defined by Step 0e precede this authority
  preflight; the ref-only source has no external transport group.
- Before reading or executing either generator blob, set
  `GIT_NO_REPLACE_OBJECTS=1` for every Git lookup and fail closed if the
  repository has any `refs/replace/*`, a non-empty common-dir `info/grafts`, a
  shallow boundary/common-dir `shallow` file, or reports a shallow repository.
  Parse package `HEAD`, `--live-reviewed-head`, current live `HEAD`, and
  `--reviewed-code-head` only as full object-format-width immutable commit
  OIDs; never resolve user-controlled revision syntax. Require package
  `HEAD ==` current live `HEAD == --live-reviewed-head`, where the supplied
  live OID is the exact independently reviewed closure `HEAD`. Reject
  arbitrary, abbreviated, historical, grafted,
  replaced, missing, or package-selected alternate commits before any
  generator bytes reach Bash.
- Bind the executable code independently of package choice. Require the
  reviewed Step 0d code commit to be the exact full OID recorded by the final
  recovery review, prove it is an unambiguous ancestor of live `HEAD`, and
  compare the blob OIDs for the helper and both canonical generators at live
  `HEAD` with those at that reviewed commit. Also require those three tracked
  paths to have no real-index or worktree modification. Any mismatch fails
  before generator-object read or shell execution. Only after this proof may
  the helper read the two generator bytes from the already proved live
  reviewed `HEAD`; it must never read executable bytes from a differing
  package-selected commit.
- After that equality proof, seed a new scratch index with
  `git read-tree $PACKAGE_HEAD`, then require
  `git write-tree` to equal both `$PACKAGE_HEAD^{tree}` and
  `$LIVE_REVIEWED_HEAD^{tree}` before mutation.
  Enumerate the old prefix from both `git ls-tree` and the projected index,
  require the same byte-sorted twenty paths, and feed only that exact
  NUL-delimited tuple to `git update-index --force-remove -z --stdin`; no
  recursive pathspec is permitted. Require
  `git diff --cached --name-status --no-renames -z $PACKAGE_HEAD --` to
  contain exactly twenty `D` records and no outside path. Recheck the final
  projected tree and generate the binary patch from this same index.
- Hold the proved live-HEAD generator bytes independently of checkout-local
  script content and execute them with trusted Bash as
  `bash -s -- --stdout`. Pass the generator bytes on stdin, run from the
  repository root, and use only the projected `GIT_INDEX_FILE`, trusted system
  `PATH`, `LANG`, `LC_ALL`, and the existing Python
  no-user-site/no-bytecode safety variables. Do not execute a checkout script
  and do not write or seed either generated output.
- Decode stdout strictly as UTF-8, require LF-only Markdown with one canonical
  terminal LF and no diagnostic/noise, and compare its exact bytes both to the
  package attachment and to
  `git show $LIVE_REVIEWED_HEAD:$CANONICAL_OUTPUT`. Empty output, exit-zero
  no-op output, non-UTF-8 bytes, CR/CRLF, extra stdout, package drift, or
  tracked-live-HEAD drift fails closed with no repository write.
- Make the authoritative package verifier repeat the preflight and projection
  freshly for every public mode above. A command-local in-memory memo keyed by
  repository identity, package `HEAD`, live reviewed `HEAD`, reviewed code
  OID, and proved helper/generator blob OIDs may deduplicate identical replays
  inside one CLI invocation; no process-global, filesystem, ref, or
  cross-command cache is allowed. Attempt-2 terminal-prehistory replay must
  use the same verifier rather than an attachment-only path.
- Keep all existing package, receipt, closure, evidence-tree, marker, and
  create-only ref schemas byte-compatible. Step 0d changes projection authority
  and generator transport only; it does not widen evidence states, attempts,
  Task transitions, ref names, or review identity rules.

**Scratch and cleanup contract:**

- Step 0d helper production code must not call `git worktree add`,
  `git worktree remove`, `git worktree prune`, `shutil.rmtree`, or another
  recursive scratch-deletion path.
  Replace every helper-owned `TemporaryDirectory`/`mkdtemp` cleanup path used
  for indexes or evidence replay with one descriptor-pinned scratch owner.
- Open and pin the scratch parent and scratch directory with `O_DIRECTORY`,
  `O_NOFOLLOW`, and `O_CLOEXEC`; record device/inode/mode identities. Address
  the projected index through the inherited pinned directory descriptor (for
  example `/proc/self/fd/$SCRATCH_FD/index` with `pass_fds`) so renaming or replacing
  the visible ancestor cannot redirect Git or generator access.
- Register only helper-created direct children and their current identities.
  Cleanup may unlink a proved direct regular child through its parent
  descriptor and may remove an empty proved directory with descriptor-relative
  `rmdir`, bottom-up. It must never follow a symlink, traverse an unregistered
  child, recursively remove a path, or delete through a visible ancestor whose
  identity no longer matches. A substituted holding ancestor must preserve the
  outside victim, fail closed, and report the unremoved proved scratch object
  without attempting a destructive fallback.
- Snapshot the real index bytes/type/mode/device/inode, branch `HEAD`, old-pack
  objects, both canonical output bytes and file identities, and linked-worktree
  registry before projection. Require all snapshots and the registry to be
  unchanged after success and every injected failure.

Use these stable fail-closed error classes in new coverage while preserving
the existing evidence-schema errors:

| Error                         | Required trigger                                                                                                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LIVE_HEAD_REQUIRED`          | a package-consuming mode omits `--require-live-head`, `--live-reviewed-head`, or `--reviewed-code-head`, or supplies a non-full/non-commit OID; reject with exit 2 before projection or shell |
| `AMBIGUOUS_GIT_HISTORY`       | replace refs, grafts, shallow history, replacement-aware resolution, or another non-immutable commit interpretation is present                                                                |
| `UNTRUSTED_PACKAGE_HEAD`      | package `HEAD`, supplied live reviewed `HEAD`, and current live `HEAD` are not the same exact full commit OID                                                                                 |
| `REVIEWED_CODE_DRIFT`         | helper/generator live blob OIDs differ from the reviewed Step 0d code commit, that commit is not an unambiguous ancestor, or a bound tracked code path is dirty in the real index/worktree    |
| `PROJECTED_INDEX_SCOPE_DRIFT` | scratch/index ownership, initial tree, real-index alias, or package-HEAD binding cannot be proved                                                                                             |
| `PROJECTED_DELETION_DRIFT`    | old-path cardinality/set or exact twenty-`D`/zero-outside status differs                                                                                                                      |
| `GENERATOR_STDOUT_DRIFT`      | stdout is empty/noisy/noncanonical or differs from the package attachment or tracked live reviewed `HEAD` output                                                                              |
| `SCRATCH_SCOPE_DRIFT`         | a pinned scratch ancestor or registered child is substituted or cannot be re-proved                                                                                                           |
| `SCRATCH_CLEANUP_FAILURE`     | proved direct-child cleanup cannot complete without recursive or unproved deletion                                                                                                            |
| `PACKAGE_SEMANTIC_DRIFT`      | a resealed attachment, manifest, patch, or other package semantic differs from the freshly derived result                                                                                     |

Implement in small TDD slices:

1. **RED — pin generator stdout and authority failures.** Add the new test
   methods before production edits. Require stdout byte parity/no write for
   both generators; conflicting `--check --stdout`/`--stdout --check`, extra
   `--stdout extra`, and unknown-argument cases for each generator returning
   exit 2 with empty stdout, stderr-only diagnostics, and unchanged output
   paths; exact initial tree and twenty-`D` projection; outside-index drift
   rejection; empty, noisy, CR/CRLF, and non-UTF-8 stdout rejection by the
   projector without a repository write; and forged exit-zero no-op generator
   plus canonically resealed package rejection through every public authority
   mode. Put a marker-writing malicious/no-op generator in a valid non-live
   commit and package/ref fixtures that select it; each package-consuming mode
   must return `UNTRUSTED_PACKAGE_HEAD` before the marker, generator mutation,
   or shell execution can occur. Also cover missing live-binding flags,
   replace/graft/shallow ambiguity, ancestor-substitution victim preservation,
   no linked-worktree command/registry drift, and valid replay from both
   retired directory-transport authorization sources with
   branch/index/output/old-pack invariants.
   Run:

   ```bash
   python3 -m unittest \
     tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_stdout_mode_is_byte_exact_and_write_free \
     tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_generator_cli_rejects_conflicting_and_extra_arguments_without_writes \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projected_index_proves_exact_twenty_deletions_without_worktree_mutation \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projected_index_rejects_outside_status_drift \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projector_rejects_empty_noisy_crlf_and_non_utf8_stdout_without_writes \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_every_public_mode_reprojects_and_rejects_resealed_noop_generator \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_non_live_package_generator_is_rejected_before_shell_across_all_modes \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_package_authority_requires_live_binding_and_unambiguous_history \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_pinned_scratch_cleanup_preserves_victim_after_ancestor_substitution \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projection_never_invokes_worktree_or_drifts_registry \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_valid_package_and_ref_replay_preserve_repository_state \
     -v
   ```

   RED must fail only for the missing strict generator parser/`--stdout`,
   still-present linked-worktree projector/recursive cleanup, missing
   live-reviewed-code preflight/fresh authority replay, or missing
   stdout/exact-status/invariant enforcement. Fixture setup errors,
   environment errors, a created malicious execution marker, a repository
   mutation, or an already-green assertion are not accepted as RED evidence.

2. **GREEN A — add stdout without changing canonical bytes.** Implement
   one strict zero-or-one-argument parser and `--stdout` in both generators,
   keep write/check paths unchanged, reject every conflicting/extra argument
   before rendering, and make the retiring-pack fixture prove output
   inode/mode/bytes are unchanged on success and usage failure. Require:

   ```bash
   bash scripts/knowledge/generate-llm-wiki-index.sh --stdout | \
     cmp - docs/90.references/llm-wiki/llm-wiki-index.md
   bash scripts/knowledge/generate-llm-wiki-coverage.sh --stdout | \
     cmp - docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
   bash scripts/knowledge/generate-llm-wiki-index.sh --check
   bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
   python3 -m unittest \
     tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_generator_cli_rejects_conflicting_and_extra_arguments_without_writes \
     -v
   ```

3. **GREEN B — replace projection and cleanup.** Implement the pinned scratch
   owner, live/reviewed-code/Git-history preflight, temporary-index
   tree/path/status proof, proved-live-HEAD blob stdin execution, minimal
   environment, strict UTF-8/LF Markdown parsing, exact patch/output
   comparisons, and direct-child-only cleanup. Delete the obsolete
   linked-worktree projection and recursive cleanup code; do not retain a
   fallback branch. Require the two projector negative methods to pass before
   routing any authority mode:

   ```bash
   python3 -m unittest \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projector_rejects_empty_noisy_crlf_and_non_utf8_stdout_without_writes \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_package_authority_requires_live_binding_and_unambiguous_history \
     -v
   ```

4. **GREEN C — make every authority path replay.** Route all six public modes
   and both authorized package sources through the authoritative projector,
   add command-local memoization only after correctness tests pass, and build a
   forged no-op/resealed package plus manually forged ref fixture so neither
   package inputs nor ref-only inputs can bypass projection. The non-live
   fixture must contain executable marker/mutation bytes and prove zero
   execution through each mode. Run the exact RED command again and require
   every named method to pass.

5. **Full regression and evidence.** Run the existing classes by their current
   module/class names:

   ```bash
   python3 -m unittest \
     tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests \
     tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest \
     -v
   python3 -m py_compile \
     scripts/validation/agentic-research-gate9-evidence.py \
     tests/validation/test_agentic_research_gate9_evidence.py \
     tests/validation/test_llm_wiki_retiring_pack_exclusion.py
   ruff check \
     scripts/validation/agentic-research-gate9-evidence.py \
     tests/validation/test_agentic_research_gate9_evidence.py \
     tests/validation/test_llm_wiki_retiring_pack_exclusion.py
   bash -n scripts/knowledge/generate-llm-wiki-index.sh \
     scripts/knowledge/generate-llm-wiki-coverage.sh
   shellcheck scripts/knowledge/generate-llm-wiki-index.sh \
     scripts/knowledge/generate-llm-wiki-coverage.sh
   python3 scripts/validation/check-document-metadata.py \
     --mode check-changed \
     --base-ref 35318255 \
     --changed-path \
     docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
   git diff --check
   ```

   Re-run both canonical `--check` and stdout `cmp` commands after the full
   suite. Confirm `git diff --` for the two generated outputs is empty, the old
   pack is still 20/20 at `HEAD` and in the real index, the real index has no
   staged change, `git worktree list --porcelain` is unchanged, the Gate 9 ref
   namespace is unchanged, and the implementation diff is exactly the six
   files above.

Commit the recovery implementation as its own logical unit with subject
`fix(validation): recover gate 9 stdout projection`. Generate one immutable
review package for the exact recovery `BASE..HEAD` and dispatch two fresh,
independent committed-unit reviewers over it: specification and
Python/security. Both must return C0/I0/M0. Record the exact implementation
commit/range, commands, results, unchanged invariants, and both verdicts in a
Task-only closure commit with subject
`docs(task): close gate 9 projection recovery`. A review fix starts the next
recovery round and repeats RED/GREEN/full checks plus both reviews over the new
committed delta. After the Task-only closure is committed, dispatch two final,
fresh independent closure-integrity reviews—specification and
Python/security—over the exact recovery base through that closure `HEAD`.
Both must return C0/I0/M0; their reviewed target OID is
`GATE9_LIVE_REVIEWED_HEAD`, while the last reviewed six-file implementation
commit is `GATE9_REVIEWED_CODE_HEAD`. These external receipts do not trigger a
self-referential Task edit. Do not start Phase A until the recovery closure is
committed and reviewed, the worktree and real index are clean, and both the
implementation and closure-integrity review pairs are C0/I0/M0.

Step 0d reached its final breaker at commit
`b77abacb610c853db3e9fef2bdef8cc7855c62a2`, exact range
`db39e644974c0f2540f3ccb42409e8bd6c36b929..b77abacb610c853db3e9fef2bdef8cc7855c62a2`.
The independent specification and Python/security reviews both returned Needs
fixes C0/I1/M0 on the same load-bearing defect: substitution between the
holding `mkdir` and first `os.open` can cause the opened descriptor, `fstat`,
and same-parent `stat` to bind the attacker replacement and later remove it,
while the helper-created directory remains. The committed regression begins
substitution later and does not cover that interval. Step 0d is therefore
`BLOCKED`; there is no recovery round 6, its reviewed-code binding remains
`71eb4feb7d4a085fd2910038a374987773de1e1d`, and its incomplete Task-only
closure cannot open Phase A or Gate 9.

**End historical Step 0d record.** None of its commands, flags, error classes,
projection mechanics, cleanup mechanics, or test names is current. Step 0e
below is the sole executable recovery contract and overrides the entire
historical block.

- [ ] **Step 0e: Replace the failed filesystem projection with tree objects, sealed memfd manifests, and one atomic bundle**

On 2026-08-09 (Asia/Seoul), after the Step 0d breaker, the user explicitly
approved the Git tree-object, sealed anonymous-memory descriptor, and atomic
canonical-bundle design, including append-only content-addressed Git-object
writes during package construction. This approval creates a new, separately
bounded recovery task. It permits only the exact implementation below. It does
not authorize reuse of any old package, receipt, closure, hash, or diagnostic;
a real Gate 9 bundle, evidence ref, real-index staging, deletion, lifecycle
mutation, remote action, and push remain closed until this recovery and its
closure-integrity reviews are C0/I0/M0 and Phase A is rerun from the resulting
fresh reviewed `HEAD`.

This is not Step 0d round 6. It has at most five implementation/fix review
rounds total: round 1 is the initial implementation, rounds 2 and 3 resume the
same implementer for reviewer-driven fixes, and rounds 4 and 5 use a fresh
more-capable implementer. Every initial or fix commit receives two fresh
independent reviews over the exact delta, one specification and one
Python/security. Step 0e requires C0/I0/M0 from both reviewers; no Minor is
parked. Any finding left after round 5 trips the new breaker and requires
another reviewed Plan decision.

**Reviewed correction gate — publication linearization and raw evidence-ref
discovery:**

The first Step 0e implementation is recovery round 1, its first fix is round
2, and the `96d0622110dbe5fd6a2f0c7b14d2a75686697357` fix is round 3. The
remaining findings do not authorize another same-implementer edit. Before any
production or test change, amend and independently review this Plan-only
contract. Commit only this Plan with exact subject
`docs(plan): define gate 9 bundle publication linearization`; both a
specification reviewer and a Python/security reviewer must return C0/I0/M0
over that one-file range. That commit and its review pair are the superseded
initial gate: the range is immutable, its review produced the `--bundle`
finding recorded below, and the operative gate is now the one stated in the pass
condition below, as amended through fix-9. The Task owns the actual review
receipts. Package
construction, package or ref consumption, Phase A, evidence-ref publication,
deletion, lifecycle mutation, Task 12, remote actions, and push remain closed.

The first Plan-only review identified that `--bundle` alone cannot bind a
later consumer to the controller-captured build receipt. Correct only this
Plan from clean `1cd723fa1458e464e6e7d257f799f5803e1dee28`, commit it with
exact subject `docs(plan): bind gate 9 bundle receipt identity`, and review its
one-file fix range. That fix-1 specification review is Approved C0/I0/M0; its
Python/security review is Needs fixes C0/I1/M0 because a FIFO substituted
after raw snapshot can block the subsequent Git ref enumeration. That verdict
is recorded as returned; direct measurement has since shown that the command
it names is not the one that blocks, which is why the fix-2 control derived
from it missed. The measured hazard surface is recorded normatively in the
discovery contract below.

Correct only this Plan again from clean
`bb1794cde08ecc846b460a37f7201c29f237982e`, with exact subject
`docs(plan): bound gate 9 ref discovery latency`. Both fix-2 independent
re-reviews are complete and both failed: the specification re-review returned
Needs fixes C0/I1/M4 and the Python/security re-review returned Needs fixes
C0/I3/M3. Both found that the fix-2 bound was scoped to `git for-each-ref`,
which does not block, while the calls that do block remained on the generic
unbounded runner; the Python/security re-review additionally found that
mandated RED method 4 asserted a timeout that cannot occur and that the
create-only CAS can leave a stale `<ref>.lock` behind.

Correct only this Plan a third time from clean
`0b9bd01b548e615dcdfa5e893acbaa07cd3550be`. Commit exact subject
`docs(plan): retarget gate 9 hazard bounds to execution funnels`. Both fix-3
independent re-reviews are complete and both failed: the specification
re-review returned Needs fixes C0/I4/M4 and the Python/security re-review
returned Needs fixes C0/I4/M4. Both found that the introduced
`STALE_REF_LOCK` clearance unlinks a file inside `.git`, that its clearance
conditions cannot establish ownership, that the funnel-closure claim is
broader than funnel 2's own definition, and that mandated RED method 4 still
carries assertions its specified injection cannot reach.

Correct only this Plan a fourth time from clean
`b6e2219fcfb7fb0ce1b0f660e8a2d18fbb7a7802`. Commit exact subject
`docs(plan): fail closed on gate 9 lock residue`. Both fix-4 independent
re-reviews are complete and both failed: the specification re-review returned
Needs fixes C0/I4/M5 and the Python/security re-review returned Needs fixes
C0/I2/M5. Both confirmed the structural core: the lock-residue path is
read-only end to end, the Spec 137 architecture boundary is respected and
correctly cited, the Plan's own static scan banning the `unlink` token
independently forecloses re-derived clearance, the index guard anchor precedes
every index-reading `git diff` in the authority preflight, the create-only CAS
sub-case's `commit-tree` boundary sits where the Plan claims, and the declared
indistinguishability of lock origins adds no hazard beyond a denial that
already requires total-bypass capability. The remaining findings were a
`for-each-ref` baseline that contradicts the Plan's own raw-loose-first
ordering, mandated `SIGKILL` assertions the terminate-then-conditional-kill
sequence never fires, a lock residue that same sequence cannot produce, a
`zero-byte` trigger stated inconsistently across four locations, a named
descriptor deadline that cannot bound the `open` it exists for under the
permitted `poll()` option, and a `STALE_REF_LOCK` exit status mandated on a
false premise about this contract's own convention.

Correct only this Plan a fifth time from clean
`a6613da90cd9b8e2c5a21ae420065b3af28dbcfb`. Commit exact subject
`docs(plan): correct gate 9 deadline and terminal status`. Both fix-5
independent re-reviews are complete and they split. The Python/security
re-review returned Approved C0/I0/M6 — the second approval any correction in
this gate has earned — after verifying the no-mutation property, the
`setitimer`-before-`open` mechanism, the exit-1 convention, and the
size-independent lock predicate against the primitives and the helper source
rather than against this Plan's prose. The specification re-review returned
Needs fixes C0/I2/M5, closing five of the six fix-4 defects: the unfirable
`SIGKILL` assertion, the unbuildable lock-residue fixture, the four-location
zero-byte inconsistency, the deadline that could not bound its own `open`, and
the exit status mandated on a false premise. Structure, Spec 137 boundary
compliance, round accounting, and the entire security dimension are settled by
that pair, and no later correction may reopen or weaken them. The two
remaining Important findings sit wholly inside the `for-each-ref` baseline
passage: an absolute "never reaches `for-each-ref` through the gate" claim that
this Plan's own sub-case 2 falsifies, and a retargeted raw/union disagreement
instantiation that direct measurement shows cannot reach the omission branch it
is assigned to.

Correct only this Plan a sixth time from clean
`a17281a85531c1a9986d35f9f063ed6bd4f1bfc5`. Commit exact subject
`docs(plan): reconcile gate 9 omission claims`. Both fix-6 independent
re-reviews are complete and both failed: the specification re-review returned
Needs fixes C0/I2/M5 and the Python/security re-review returned Needs fixes
C0/I3/M4. Both confirmed that fix-6 paid its principal debt — the
concurrent-unlink instantiation of the raw/union omission clause is reachable,
and each reviewer reproduced it independently on `git version 2.43.0` — and the
Python/security re-review re-derived all five properties its fix-5 approval
rested on as intact. Their five remaining Important findings are dispositioned
by the fix-7 scope reduction below rather than repaired one by one.

Correct only this Plan a seventh time. Commit exact subject
`docs(plan): scope gate 9 to liveness and reviewer identity`. Fix-7 is not a
seventh repair of the same material; it is a scope reduction, which the user
approved on 2026-08-14 (Asia/Seoul). Six Plan-only corrections each closed
their named defects while introducing roughly one new defect of the same class,
and the Important-finding count ran four, eight, six, two, five — it reversed
rather than converged, and the hardest failures were corrections repairing a
defect a previous correction had introduced. Fix-7 therefore removes the class
of obligation that produced those findings from this gate's passing
requirements: it separates liveness from adversarial proof and keeps only
liveness in the gate. Both fix-7 independent re-reviews are complete and both
failed: the specification re-review returned Needs fixes C0/I4/M6 and the
Python/security re-review returned Needs fixes C0/I3/M3. Their findings are
dispositioned by fix-8 below.

Correct only this Plan an eighth time. Commit exact subject
`docs(plan): split gate 9 obligations at assertion granularity`. Both fix-7
reviewers independently upheld the fix-7 premise, and fix-8 reopens none of it:
no implemented control was removed; all five properties the fix-5
Python/security approval rested on survive; the restatement of the Spec 137
pre-deletion gates is item-for-item accurate; Spec 137 requires
filesystem-substitution resistance nowhere; and no substitution hazard in the
demoted set is reachable by a principal that does not already hold a cheaper
total bypass. Four of the five outstanding fix-6 Important findings are
genuinely closed. What both re-reviews found are defects in how fix-7 carried
the reduction out, and fix-8 corrects those five: it completes the
withdrawal the fix-7 disposition table promised but did not perform; it redraws
the split at assertion granularity rather than by whole fixture, so the liveness
obligations this gate keeps mandatory have gate-blocking demonstrations again;
it corrects the restated pass condition's own count and gives every contract
area a defined blocking status instead of leaving five of them unassigned; it
brings method 4 sub-case 2 into line with the prohibition its own preamble and
R1 state; and it resolves the conflict between the new non-blocking language and
this Plan's unchanged C0/I0/M0 requirement. As a sixth change outside that
enumerated set, fix-8 also rewrites R3 to bar the `SIGALRM`-blocking closure
route as deadline-defeating. Both fix-8 independent re-reviews are complete and
they split. The Python/security re-review returned Approved C0/I0/M4 — the
third approval any correction in this gate has earned — after tracing the
helper source rather than this Plan's prose to verify that every retained
liveness control now carries a gate-blocking assertion at a site where it can
actually fire, that all five properties the fix-5 approval rested on survive,
and that method 4 sub-cases 4 and 6 were promoted to fully gate-blocking rather
than demoted. The specification re-review returned Needs fixes C0/I2/M6: it
confirmed everything else fix-8 claimed — the liveness demonstrations, sub-case
3's independence from R1, the performed withdrawal, the corrected pass-condition
count, the default rule, and the no-amnesty blocking-status resolution — and
left two internal contradictions between how the new per-assertion rule is
stated and how it is applied. Those two, and the ten Minors across both fix-8
reviews, are dispositioned by fix-9 below.

Correct only this Plan a ninth time. Commit exact subject
`docs(plan): align gate 9 backlog enumeration with placements`. Fix-9 moves no
boundary and reopens nothing either fix-8 review upheld: every retained liveness
control keeps a gate-blocking assertion at a site where it can fire, the five
properties the fix-5 and fix-8 Python/security approvals rested on survive,
method 4 sub-cases 4 and 6 stay gate-blocking in full, the no-amnesty
blocking-status resolution stands unchanged, and R3's removal of the
`SIGALRM`-blocking route stands. Fix-9 closes the two fix-8 specification
Important findings and the ten Minors across both fix-8 reviews. It makes R2's
enumeration agree with the RED scoping list and with sub-case 3 itself on where
sub-case 3's `FOREIGN_REF` verdict sits, and it replaces the demotion criterion's
`in the evidence namespace` qualifier — which selected neither the placements
this Plan makes nor a consistent rule — with one criterion, three named retained
exceptions, and an explicit statement that the RED scoping enumeration is that
criterion's closed application, stated identically in all four places the
criterion appears. Both fix-9 independent re-reviews are `Not Run` until that
one-file commit is dispatched; do not predict their verdicts. One fresh
independent specification reviewer and one fresh independent Python/security
reviewer must each return C0/I0/M0 over that one-file range before recovery
round 4 may begin. No Plan-only fix consumes a Step 0e implementation round, so
the implementation count remains three of five. Do not begin recovery round 4 or
edit the Task, helper, or tests until both fix-9 re-reviews return C0/I0/M0.
Package construction, package or ref consumption, Phase A, evidence-ref
publication, real-index staging, deletion, lifecycle mutation, Task 12, remote
actions, and push all remain closed.

Both fix-9 re-reviews returned Approved. The Python/security re-review returned
Approved C0/I0/M0 with no finding at any severity, after anchoring the
code-agnostic fail-closed form in the helper's own `Gate9Error` message
construction and single `main()` exception boundary, confirming empty stdout
because every stdout write in the helper is a terminal-success statement, and
confirming that the first stderr line is the only position where a mapped
diagnostic and an interpreter traceback differ. It also checked the four
statements of the demotion criterion mechanically as byte-identical. The
specification re-review returned Approved C0/I0/M3, the second specification
approval any correction in this gate has earned, and judged the closed-enumeration
device an honest resolution rather than a concealed rule because an unplaced case
requires a reviewed Plan amendment.

Step 0e admits no parked Minor, so those three specification Minors still block.
Correct only this Plan again from clean
`f87746db9eb273425b9ecc05693cf53e46a5c235`. Commit exact subject
`docs(plan): close residual gate 9 wording findings`. The correction attaches the
criterion's narrowing to the moved-out bullet without restating or overriding its
three retained exceptions, repairs an approval count that this Plan states one too
low in two places rather than only in the sentence fix-9 added, and gives the two
verbless criterion lead-ins a main verb so all four read as sentences. It changes
no criterion body, no placement, no error code, and no blocking status. Both
fix-10 independent re-reviews are `Not Run` until that one-file commit is
dispatched; do not predict their verdicts. One fresh independent specification
reviewer and one fresh independent Python/security reviewer must each return
C0/I0/M0 over that one-file range before recovery round 4 may begin. No Plan-only
fix consumes a Step 0e implementation round, so the implementation count remains
three of five. Every downstream action named above remains closed.

Both fix-10 re-reviews returned Needs fixes, specification C0/I2/M0 and
Python/security C0/I1/M1, on two defects that the fix-10 paragraph itself
introduced and that both reviewers found independently. Each seat also confirmed,
within its own scope, that nothing either fix-9 approval rested on had moved.
Both seats confirmed the demotion criterion body stayed byte-identical across all
four sites, that the three retained classes named inside that body were therefore
unaltered, and that the narrowing clause narrowed by reference to an unchanged
normative criterion without re-placing anything. The Python/security seat alone
verified that R2's applied list still agreed with the RED scoping enumeration
case for case and that the code-agnostic fail-closed form stayed anchored to the
unmodified helper.

The first defect is a fabricated identifier. The fix-10 paragraph cited a clean
base whose eight-character prefix was correct and whose remaining thirty-two
characters were invented rather than read from the repository. Every other full
object identifier this Plan cites resolves. An identifier that resolves only by
prefix abbreviation and fails an exact check leaves the round's provenance
unverifiable, which is why this is recorded as a defect of record rather than a
typo. The second defect is a third instance of the approval-count error that
fix-10 existed to repair: its own new sentence called the fix-9 specification
approval the first in this gate, against this Plan's record of fix-1's approved
specification review.

Correct only this Plan again from clean
`684f5fc33635d228c9ce2e9faef4a72c4d2ebabf`. Commit exact subject
`docs(plan): correct fabricated base identifier and approval count`. The
correction replaces the invented identifier with the object identifier read from
the repository, and makes the fix-9 specification approval read as the second.
It changes no criterion body, no placement, no error code, no blocking status,
and no liveness assertion. Both fix-11 independent re-reviews are `Not Run` until
that one-file commit is dispatched; do not predict their verdicts. One fresh
independent specification reviewer and one fresh independent Python/security
reviewer must each return C0/I0/M0 over that one-file range before recovery
round 4 may begin. No Plan-only fix consumes a Step 0e implementation round, so
the implementation count remains three of five. Every downstream action named
above remains closed.

The fix-11 Python/security re-review returned Approved C0/I0/M0. It confirmed the
corrected base resolves and is the exact parent of the fix-10 commit, that the
fabricated predecessor no longer appears and still fails an object existence
check, that every full object identifier this Plan cites resolves apart from the
Git null-OID sentinel, which is a literal command argument rather than a
citation, and that a whole-document paragraph comparison returns a single
non-equal opcode covering two word substitutions and the inserted bookkeeping
paragraphs and nothing else. It also re-confirmed the criterion body, the
error-code multiset, the fail-closed form, and byte-identical helper and test
blobs across the range.

The fix-11 specification re-review returned Needs fixes C0/I1/M1. It confirmed
both named fix-10 defects fully repaired, then found two further defects in the
bookkeeping text. The Important one is a scope defect with a downstream
consequence: the round-4 Task-recording clause enumerated fixes by name and
stated a fixed count of review pairs, so a round following it literally would
omit the later rounds from the evidence ledger. That clause was already one round
stale before fix-11 and fix-11 widened the gap rather than closing it. The Minor
is an overclaim: a sentence attributed to both seats a set of confirmations that
only the Python/security seat made.

Correct only this Plan again from clean
`82287daa5708901c0801af52652c1c5c3a6f47fb`. Commit exact subject
`docs(plan): make round four evidence scope count-independent`. The correction
replaces the enumerated fix list and fixed pair count with a count-independent
obligation covering every numbered Plan-only fix and every review pair each one
received, and splits the confirmation sentence so each claim is attributed to the
seat that made it. It changes no criterion body, no placement, no error code, no
blocking status, and no liveness assertion. Both fix-12 independent re-reviews
are `Not Run` until that one-file commit is dispatched; do not predict their
verdicts. One fresh independent specification reviewer and one fresh independent
Python/security reviewer must each return C0/I0/M0 over that one-file range
before recovery round 4 may begin. No Plan-only fix consumes a Step 0e
implementation round, so the implementation count remains three of five. Every
downstream action named above remains closed.

Both fix-12 re-reviews returned Approved with zero Critical and zero Important,
each carrying the same single Minor, found independently and with the same
prescribed repair. The specification seat confirmed the repaired round-4 clause is
genuinely count-independent and binds strictly more than the enumerated form it
replaced, because review pairs now attach per item rather than by a fixed total;
it swept the Plan for sibling enumerations and found that the repaired clause was
the only forward-looking one over the fix set; and it re-derived the approval
ordinals and the historical counts as accurate. The Python/security seat
re-confirmed the criterion body at four occurrences of identical content, an
identical code-token multiset, and byte-identical helper and test blobs across
the range, with the whole-document paragraph comparison returning changes only in
bookkeeping prose.

The shared Minor is an over-correction this Plan made when repairing an earlier
over-claim. Splitting a confirmation sentence by seat moved one item too far: the
three retained classes are named inside the demotion criterion body, so a seat
confirming that body byte-identical has thereby confirmed those classes
unaltered, and attributing that item to one seat alone contradicted the sentence
immediately before it. Step 0e admits no parked Minor, so it is repaired rather
than carried.

Correct only this Plan again from clean
`339688ec9dd691a7d51b7fea28960e330f6671fb`. Commit exact subject
`docs(plan): attribute retained-class confirmation to both seats`. The correction
moves the retained-class item back into the both-seats clause and leaves R2's
applied list and the helper anchoring as the Python/security-only pair. It
changes no criterion body, no placement, no error code, no blocking status, and
no liveness assertion. Both fix-13 independent re-reviews are `Not Run` until
that one-file commit is dispatched; do not predict their verdicts. One fresh
independent specification reviewer and one fresh independent Python/security
reviewer must each return C0/I0/M0 over that one-file range before recovery
round 4 may begin. No Plan-only fix consumes a Step 0e implementation round, so
the implementation count remains three of five. Every downstream action named
above remains closed.

Fix-4 replaces the fix-3 stale-lock clearance with a fail-closed terminal
state because the clearance violated the Gate 9 evidence architecture boundary
approved on 2026-08-09 and recorded in Spec 137. That boundary permits package
construction to append Git objects but forbids deleting or rewriting objects,
mutating a branch, index, or worktree, or cleaning up unreachable objects, and
it makes a separately reviewed create-only evidence-ref publication the only
permitted Gate 9 ref mutation. Unlinking a `<ref>.lock` inside `.git` is a ref
mutation that is not that publication, so no refinement of clearance
conditions could have made the fix-3 design admissible. A later round must not
re-derive a self-clearing lock design; the boundary, not the strength of the
conditions, is what closes it. The Plan owns executable schemas only within
that boundary and may not relax it.

Fix-5 moves no boundary and deletes no control. It corrects the places where
fix-4 mandated behavior its own sequences cannot produce or justified a rule
with a false premise: it reconciles the `for-each-ref` baseline with the
raw-loose-first ordering, replaces the unfirable `SIGKILL` assertions with the
termination the fix-4 specification review actually measured, plants the lock
residue in the fixture instead of chaining it off a termination path that
removes it, makes the `STALE_REF_LOCK` trigger size-independent in all four
locations so every reachable lock state has one code, requires an alarm armed
before `open` rather than a descriptor-only `poll()`, and moves the terminal
exit status off the value reserved for `LIVE_HEAD_REQUIRED`. The read-only,
no-clearance design and its Spec 137 justification are unchanged and remain
closed to re-derivation.

Fix-6 moves no boundary, deletes no control, and reopens nothing the fix-5
Python/security approval rested on: the no-mutation property, the
`setitimer`-before-`open` mechanism, the exit-1 convention, the
size-independent lock predicate, and the fixture's test-side creation boundary
are all carried forward unchanged. It corrects two statements this Plan's own
other clauses contradict. It bounded the `for-each-ref` omission claim to the
snapshot phase it is true of, so that it would no longer contradict sub-case 2's
mid-flight injection, which this Plan at that time still required to reach the
exact-ref fallback. Both fix-6 re-reviews found that scoping still contradictory
with this Plan's own snapshot ordering, and fix-7 and fix-8 superseded it: the
classification is now robustness-backlog item R1, and sub-case 2 is backlog in
whole and explicitly not a specification round 4 may build from, so this Plan no
longer requires that mid-flight injection of any round. And it settles the
raw/union disagreement rule's reachability
question that fix-4 and fix-5 each answered with an instantiation that cannot
occur: rather than naming a third construction, it records the one measured
condition under which the two views actually disagree by omission — a leaf
unlinked between the raw walk and the `for-each-ref` of the same snapshot —
and routes the two previously misassigned cases to the clauses they really
land in. The remaining edits are text corrections to the same passage and to
mandated RED method 4.

Fix-7 moves no boundary and removes no implemented control. It changes what
this gate requires for passage, not what the helper does. It separates the
liveness obligations — the bounded funnels, the deadline mechanism, termination
and reaping, the no-follow and regular-file checks, the index-guard ordering,
the fail-closed terminal states, and the no-mutation property — from the
obligation to prove a named adversarial substitution produces a named code, and
keeps only the first kind in the gate's passing requirements. The second kind
becomes a non-blocking robustness backlog with named items, stated in the
hazard-class boundary below together with this gate's restated pass condition
and the disposition of every outstanding fix-6 Important finding. Fix-7 also
withdraws the two claims fix-6 introduced that its own re-reviewers measured to
be unsatisfiable or self-contradictory, and replaces each with the honest
residual rather than with a third attempt at the same claim.

Fix-8 moves no boundary, removes no implemented control, and reopens nothing the
two fix-7 reviews upheld. It corrects where fix-7 drew its line and how it
recorded the drawing. Fix-7 applied its own criterion at fixture granularity — a
whole sub-case moved out if its fixture injected — but the injecting fixtures
were also the only mandated demonstration of the liveness controls this gate
keeps mandatory, so after fix-7 no gate-blocking assertion exercised a funnel
bound, a termination grace, a reap, park prevention, or the `STALE_REF_LOCK`
classification. Fix-8 redraws the line at assertion granularity instead, because
the same injection produces two claims that belong on different sides: that the
operation finishes within its stated bound, that any child this gate spawned is
terminated and synchronously reaped, that no site parks, and that the gate
reaches a mapped fail-closed terminal state — exit 1, empty stdout, and a stderr
whose first line is a `<CODE>: <detail>` diagnostic rather than an unmapped
traceback — instead of proceeding all stay gate requirements, while the named
code and the classification argument about which clause catches which
substitution are the part that moves. The criterion for that is stated here in
the form this Plan repeats identically in every place it states it. Demoted: a claim that
names one specific error code as the outcome of an adversarial substitution or
removal the fixture directs at a path the gate reads. Retained: every other claim
those same fixtures make, and three named classes of code claim — methods 1 and
2's external-bundle transport codes, whose surface this Plan's capability
analysis places with a weaker different-UID local principal rather than with the
total-bypass principal whose proof obligation is unbounded; method 4 sub-case 4's
`STALE_REF_LOCK`, whose residue is planted and arises with no adversary; and
method 4 sub-case 6's `FOREIGN_REF` guards, which the fixture injects into
`git`'s own output rather than at a path the gate reads. A criterion of this
shape cannot decide every case unaided, because a leaf a fixture creates and one
it substitutes are the same file on disk, so the RED scoping enumeration that
applies it to every method and sub-case is its closed application, and where the
two could be read apart that enumeration governs. Fix-8 also completes the
withdrawal the fix-7 disposition
table recorded but the fix-7 commit did not make, gives every area of the
executable contract a defined blocking status instead of leaving most of it
unassigned between two lists, and states one answer where fix-7 left two on
whether a finding naming a backlog item blocks passage.

Fix-9 moves no boundary, removes no implemented control, and reopens nothing
either fix-8 review upheld. It corrects two ways fix-8 stated its own line
rather than where fix-8 drew it. First, fix-8's R2 enumeration excluded method 4
sub-case 3 from that item while the RED scoping list and sub-case 3 itself
placed sub-case 3's `FOREIGN_REF` verdict inside it, so this Plan carried two
normative routes to opposite answers on one assertion — the same undefined-status
class fix-8 exists to eliminate. Fix-9 corrects the enumeration rather than the
placement, because sub-case 3's `FOREIGN_REF` verdict is exactly what the split
moves — one named code claimed as the outcome of an injected substitution — while
its funnel-1 bound, process-group signal, child absence, and synchronous reap are
exactly what the split keeps. Promoting the verdict instead would have returned a
named-code obligation to the gate that the split exists to remove, and it is not
needed to make sub-case 3's gate-blocking claim meaningful: fix-9 states the
retained fail-closed assertion in a form that proves the run left through the
contract's own mapped fail-closed path, and therefore did not surface an unmapped
traceback, without naming which code it emitted. Second, fix-8's demotion
criterion was scoped `in the evidence namespace` in three places and unscoped in a
fourth; with the qualifier it retained method 4 sub-case 5's `CONTROL_FILE_DRIFT`
against two explicit demotions, and without it it demoted methods 1 and 2's
transport codes against their explicit retention, so the stated rule selected the
placements this Plan makes under neither reading. Fix-9 replaces it with one
criterion, three named retained exceptions, and an explicit statement that the
RED scoping enumeration is that criterion's closed application, and states the
whole of it identically in all four places it appears.

After the Plan-only gate passes, recovery round 4 uses a fresh more-capable
implementer and modifies exactly these three files within the existing
six-file ceiling:

1. `scripts/validation/agentic-research-gate9-evidence.py` for the publication
   linearization, transport-first consumption, and raw evidence-ref namespace
   discovery.
2. `tests/validation/test_agentic_research_gate9_evidence.py` for the focused
   concurrency, transport-ordering, dangling-loose-symref, canonical-ref, and
   stable-identity regressions.
3. `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` only
   for the actual immutable Plan
   correction and every numbered Plan-only fix in this gate, whatever their
   final count, with their commit ranges and every independent
   review/re-review pair each one received, the round-3
   implementation
   findings, and round-4 RED/GREEN/full evidence with the new implementation
   reviews left `Not Run` until dispatch. No separate Task-only prerequisite
   is needed; the round-4 implementation commit records only reviews that
   already completed and makes no forward verdict claim.

No generator, generated output, Spec, Plan, old-pack path, lifecycle artifact,
real index, branch, worktree registration, package, or ref is in the round-4
implementation scope. Use exact commit subject
`fix(validation): linearize gate 9 bundle publication`. Round 4 and, only if
its reviewers find an issue, round 5 both keep the fresh more-capable
implementer rule. A finding after round 5 trips the existing breaker; it does
not create round 6.

**Hazard-class boundary — what these controls are for:**

Reviewer-identity binding is the security boundary of Gate 9. Step 4 states
it: the controller's observed spawn result, the frozen assignment attestation
echoed by both reviewers, and the content-addressed create-only evidence ref
are what prevent a reviewer role from being claimed by self-asserted receipt
text. The controls in this subsection that resist filesystem substitution —
nonblocking no-follow opens, descriptor identity checks, bounded execution
funnels, and read-only lock-residue diagnosis — are an availability and
robustness obligation, not a security boundary. This reclassification licenses
no relaxation of the create-only evidence-ref CAS and no write, unlink, or
rename inside the evidence namespace. Lock _residue_ is diagnosed; lock
_clearance_ is not a Gate 9 operation at all, and its exclusion is a Spec 137
architecture-boundary constraint rather than a tuning choice.

The reason is capability, stated separately for the two substitution surfaces
because they admit different principals. Substitution inside `.git`, or of a
tracked path the gate reads, implies total bypass: that principal can rewrite
the helper that performs the checks, shadow `git` on the inherited `PATH`, or
write the evidence ref, its objects, and the Task binding directly. Bundle
substitution at the literal `/tmp` direct child is reachable by a weaker,
different-UID local principal, because `/tmp` is world-writable; that
principal cannot forge acceptance, because `/tmp` is sticky and acceptance is
gated on the controller-captured `--expected-bundle-sha256` and
`--expected-package-sha256`, so the reachable outcome is a hang, not forgery.
Either way the residual exposure is availability. Treating substitution as a
security boundary therefore produces an unbounded and unclosable obligation,
because every round can name one more window between two syscalls and no POSIX
primitive closes that class — a limit this Plan already concedes below.

This reclassification deletes no control. Every substitution control stated
here stays, and is kept for its real purpose: a gate that hangs or wedges on a
stray leftover file is an availability defect with no adversary involved at
all. What changes is the standard a control in this class is held to. It is
complete when the gate reaches a fail-closed verdict within a stated bound and
leaves no unreaped child or unrecoverable residue, not when substitution is
proved impossible.

**Gate 9 pass condition, as amended through fix-9 — what this gate requires for
passage:**

Gate 9 passes when the Spec 137 pre-deletion gates are satisfied and the
reviewer-identity attestation holds. Spec 137 requires, before deletion: every
old file and every unique material claim mapped; every retained or corrected
claim resolved to a reviewed new destination; every omission carrying a reason
and preserved provenance; zero clickable old-pack references across tracked
text outside the retiring directory; all thirty-six requirements and all
fourteen scopes complete; independent reviews with zero unresolved Critical or
Important findings; changed-document metadata and traceability passing,
implementation alignment with no attributable finding and no increase over its
pinned 184-finding predecessor, and the whole repository contract passing; the
named LLM Wiki and security-readiness freshness checks passing with the
commit-pinned target-surface manifest and summary unchanged; and the Task
recording the before/after file manifest, deletion diff, recovery commit, and
reviewer verdict. Spec 137 requires filesystem-substitution resistance nowhere;
its Gate 9 clauses bound the evidence architecture — no scratch-directory,
temporary-index, or linked-worktree projection, pathless content-addressed
projection, sealed `memfd` manifests, one atomically published read-only
bundle, and no mutation beyond appended objects and the create-only evidence-ref
publication — and grant this Plan the executable schemas within that boundary.
The substitution-proof obligations are this Plan's own addition, not a Spec
requirement.

To the Spec list this Plan adds exactly one further _trust-boundary_ condition,
the reviewer-identity attestation stated in Step 4, because that is the trust
boundary this gate actually names: the controller's observed spawn result, the
frozen assignment attestation echoed by both reviewers, and the
content-addressed create-only evidence ref together prevent a reviewer role
from being claimed by self-asserted receipt text. That principal can emit text
only.

That is one condition of one kind, not the whole count. Beyond it this Plan
carries the five implementation requirements listed next into passage; four of
them are this Plan's own additions that the Spec nowhere states, and the fifth,
the no-mutation property, is Spec-required directly. Kept as passing
requirements, each with the one sentence that justifies it, because each
protects the gate from failing to reach a verdict even with no adversary
present:

- the three bounded execution funnels and their deadline mechanism, including
  the `setitimer` armed before `open` — an unbounded gate is a hung gate, and a
  stray leftover file causes that with no adversary at all;
- funnel 1's termination, 0.5-second grace, conditional kill, and synchronous
  reap — a gate that exits leaving a live or unreaped child has not finished;
- `O_NOFOLLOW`, `O_NONBLOCK`, the `fstat`-before-read regular-file type checks,
  and the index regular-file guard running before the first index-reading Git
  invocation — each prevents a park or an unbounded read that would otherwise
  hang the gate at a site it must pass through;
- fail-closed terminal states on anything unexpected, including
  `STALE_REF_LOCK` and `FOREIGN_REF` — a state the gate cannot classify must
  never resolve in the gate's favour;
- the entire no-mutation property, which Spec 137 requires directly and on
  which the fix-5 Python/security approval rested.

Moved out of the passing requirements and into the robustness backlog below.
Fix-8 states this list at assertion granularity, because fix-7 stated it at
fixture granularity and thereby carried the mandated demonstrations of the kept
liveness requirements out of the gate along with it:

- the obligation to _prove_ that a named adversarial substitution produces one
  named error code, as narrowed by the criterion stated immediately below, whose
  three retained classes this bullet does not restate and does not override —
  but not the obligation that the gate finish within its
  bound, park nowhere, leave no live or unreaped child, and reach a mapped
  fail-closed terminal state, meaning exit 1, empty stdout, and a stderr whose
  first line is a `<CODE>: <detail>` diagnostic rather than an unmapped
  traceback, under that same injection, which stays a passing requirement and is
  what the injecting fixtures now demonstrate;
- the raw/union omission classification claims, which three consecutive rounds
  failed to state consistently, and every argument about which clause catches
  which substitution;
- RED method 4 sub-case 2 in whole, because its stated injection point and its
  naming of the observing call are that same unsettled classification;
- the descriptor-slot requirement fix-6 introduced, which both fix-6 reviewers
  measured to be unsatisfiable.

State the criterion that places a code claim on one side or the other, in the
form fix-9 repeats identically in every place this Plan states it — here, in R2
below, in the RED scoping paragraph below, and in the fix-8 narrative above.
Demoted: a claim that names one specific error code as the outcome of an
adversarial substitution or removal the fixture directs at a path the gate reads.
Retained: every other claim those same fixtures make, and three named classes of
code claim — methods 1 and 2's external-bundle transport codes, whose surface
this Plan's capability analysis places with a weaker different-UID local
principal rather than with the total-bypass principal whose proof obligation is
unbounded; method 4 sub-case 4's `STALE_REF_LOCK`, whose residue is planted and
arises with no adversary; and method 4 sub-case 6's `FOREIGN_REF` guards, which
the fixture injects into `git`'s own output rather than at a path the gate reads.
A criterion of this shape cannot decide every case unaided, because a leaf a
fixture creates and one it substitutes are the same file on disk, so the RED
scoping enumeration that applies it to every method and sub-case is its closed
application, and where the two could be read apart that enumeration governs.

Nothing outside those two lists is left without a status. State the default
rather than leaving it to be derived: every obligation the executable contract
states that the robustness backlog below does not name is a passing requirement.
That default is load-bearing, not a formality, because it is what carries the
contract's structural obligations into passage. Named so the reader does not
have to infer them, each gate-blocking: the publication-linearization contract
and its final post-`fsync` paired validation; the all-or-none external-bundle
transport group and its `BUNDLE_TRANSPORT_DRIFT` and `BUNDLE_READ_FAILURE`
binding; the raw evidence-ref discovery admission rules and
`EVIDENCE_REF_PATTERN`; the raw/union disagreement rule and the omission clause,
both of which this Plan keeps normative; and Step 4's finite two-attempt state
machine with its `REJECTED`, `INVALIDATED`, and `BLOCKED` terminal fail-closed
states and its requirement that every consumed attempt end in a create-only
evidence ref. Only what the backlog names is non-blocking.

State the reason for the split rather than leaving it to be inferred. An
obligation to prove behaviour under an adversary who already holds total bypass
is unbounded: this Plan itself names that adversary a concurrent same-UID
actor, and such a principal can rewrite the helper that performs the checks,
shadow `git` on the inherited `PATH`, or write the evidence ref, its objects,
and the Task binding directly, so each proof closes one window out of an
unbounded set while strictly easier total-bypass paths stay open. This Plan
already concedes that no POSIX primitive closes that class. Six Plan-only
rounds of iteration produced no convergence on it.

This reclassification changes what the gate requires, not what the helper does.
No implemented control is removed: every substitution control stated in this
subsection remains mandatory in the executable contract, and the robustness
backlog is a real backlog with named items rather than a discard.

State what a backlog item's status is under review, because fix-7 left this
document with two answers to it. The pass condition is unchanged and absolute:
Step 0e requires C0/I0/M0 from both independent reviewers with no Minor parked,
and Spec 137 pre-deletion gate 6, recited above, requires independent reviews
with zero unresolved Critical or Important findings before a deletion that
cannot be undone. A robustness-backlog item is removed from what this gate
_requires_, so a reviewer following this Plan has no ground to raise the absence
of a backlog assertion as a finding at all — that is the whole operative effect
of the demotion. It is not an amnesty for findings that are filed anyway. A
Critical or Important finding that names a backlog item is a finding of record
and remains unresolved until it is repaired or until a reviewed Plan amendment
re-scopes it, and until then it blocks the Step 0e closure and every Gate 9
action exactly as any other finding does. Citing the backlog does not resolve a
finding, and no round may treat this demotion as authority to close the gate
over a standing Critical or Important verdict.

**Robustness backlog — named, owned by no round yet, and removed from what this
gate requires rather than from what a finding does:**

- **R1 — omission-clause classification.** Which window a substituted or
  concurrently removed leaf lands in, and which clause catches it, is unsettled.
  Recorded observations, attributed to the reviews that produced them: the fix-5
  and fix-6 specification reviews measured on `git version 2.43.0` that a
  regular, canonically named leaf whose recorded OID names a missing object
  makes `git for-each-ref` exit 128 with a `fatal:` line on stderr and empty
  stdout under both selectors, and that a leaf whose OID names a blob or a tree
  is reported with that object type at exit 0; the fix-6 Python/security review
  added that the missing-object result is contingent on the mandated four-field
  format. Both fix-6 re-reviews then found the fix-6 scoping still contradicted
  this Plan's own snapshot ordering. Whichever round takes this item must
  reconcile the scoped claim, the snapshot ordering, and the omission clause in
  one statement; until then no round may assert any direction as settled.
- **R2 — adversarial code assertions under injection.** This item is the named
  error code an injection is asserted to produce, not the fixture that produces
  it, and the criterion that places it is the one stated in the pass condition
  above, repeated here in the same words. Demoted: a claim that names one
  specific error code as the outcome of an adversarial substitution or removal
  the fixture directs at a path the gate reads. Retained: every other claim those
  same fixtures make, and three named classes of code claim — methods 1 and 2's
  external-bundle transport codes, whose surface this Plan's capability analysis
  places with a weaker different-UID local principal rather than with the
  total-bypass principal whose proof obligation is unbounded; method 4 sub-case
  4's `STALE_REF_LOCK`, whose residue is planted and arises with no adversary;
  and method 4 sub-case 6's `FOREIGN_REF` guards, which the fixture injects into
  `git`'s own output rather than at a path the gate reads. A criterion of this
  shape cannot decide every case unaided, because a leaf a fixture creates and
  one it substitutes are the same file on disk, so the RED scoping enumeration
  that applies it to every method and sub-case is its closed application, and
  where the two could be read apart that enumeration governs. Applied, this item
  covers the code asserted by method 3's injection cases together with the clause
  attribution R1 owns, by method 4 sub-case 1, by method 4 sub-case 3, and by the
  control-file FIFO part of method 4 sub-case 5. The same fixtures' assertions
  that the gate finishes within its bound, parks nowhere, leaves no live or
  unreaped child, and reaches a mapped fail-closed terminal state — exit 1, empty
  stdout, and a stderr whose first line is a `<CODE>: <detail>` diagnostic rather
  than an unmapped traceback — instead of proceeding are gate-blocking and are
  not in this item. It also covers method 4 sub-case 2 in whole, because that
  sub-case's injection point and observing call are the direction R1 owns, so it
  can carry no gate requirement until R1 closes. Methods 1 and 2, method 4
  sub-cases 4 and 6, the `--task`/`--spec`/`--plan` FIFO part of sub-case 5, and
  the index part of sub-case 5 are not in this item at all. The RED scoping
  paragraph below places each assertion individually, and the text below it
  remains the description of how to build the fixtures, except sub-case 2, whose
  retained text is R1's unreconciled starting point rather than a build
  specification. The controls they exercise stay mandatory regardless.
- **R3 — the descriptor bind window.** An alarm landing between the C-level
  `open()` returning and the Python bind leaves one read-only `O_CLOEXEC`
  descriptor unclosed until the fail-closed process exits. This is accepted as a
  CPython/POSIX residue of the same class as the uninterruptible driver sleep
  already conceded below. A round that takes this item may close it by
  reconciling the open descriptor set at the funnel boundary, and must state the
  residual cost of that choice. The `SIGALRM`-blocking route offered when this
  item was written is marked deadline-defeating and is not a permitted closure:
  no user code runs between `open()` returning in C and the Python bind, so the
  block would have to be established before the `open`, at which point
  `ITIMER_REAL` cannot interrupt a parked `open` and the
  `setitimer`-armed-before-`open` requirement this gate keeps mandatory is
  defeated. A later round must not adopt it as the cheap option. No round may
  record the window as closed while it is not.
- **R4 — funnel-1 `SIGKILL` escalation coverage.** The 0.5-second grace, the
  conditional kill, and the synchronous reap stay mandatory in the executable
  contract. The escalation branch is unexercised by the four mandated methods.
  This is a named, accepted coverage gap, not an unknown: the fix-6
  Python/security review showed that the fixture's own generator-script writer
  and `git` wrapper already reach a `SIGTERM`-surviving child through funnel 1.
  A round that takes this item asserts grace expiry, `SIGKILL` delivered only to
  the group this gate created, child absence, and synchronous reap, reusing the
  process-group observation point already specified below.

**Disposition of the five outstanding fix-6 Important findings:**

No finding is dropped by this reclassification. Each is recorded here with
where it now lives.

| Finding                                                                                                            | Disposition                                                                                                                                                                                                                                                                                              |
| :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Specification I1 — scoped omission claim contradicts sub-case 2 and the new omission clause                        | Closed by removal from the gate's passing requirements. The contradictory sentences are deleted below; the classification obligation moves to R1.                                                                                                                                                        |
| Python/security I1 — the same passage contradicts the snapshot ordering and misdirects sub-case 2's fixture        | Closed by removal from the gate's passing requirements, by the same deletion. Sub-case 2 is an R2 backlog item; R1 owns the reconciliation.                                                                                                                                                              |
| Specification I2 — the descriptor-slot mandate cannot be satisfied                                                 | Closed by removal of the mandate. The residual is stated honestly below; closing it is R3.                                                                                                                                                                                                               |
| Python/security I2 — measurement shows CPython cannot satisfy the pre-syscall slot                                 | Closed by removal of the same mandate, on that measurement, attributed to that review. R3 owns any achievable mechanism.                                                                                                                                                                                 |
| Python/security I3 — the `SIGKILL` escalation branch ships mandatory and untested on a refuted reachability ground | Still open, and now stated as such. Fix-7 recorded this withdrawal but did not perform it, and both fix-7 re-reviews found the false "open reachability question" ground still standing; fix-8 performs the withdrawal in method 4 sub-case 2 below. The control stays mandatory and the gap becomes R4. |

The round-4 implementation must apply this publication contract:

- POSIX does not provide a finite `stat`/`open` sequence that can promise a
  pathname will continue to name the same inode until a later Python return
  when a concurrent same-UID actor may unlink or rename entries. Do not add an
  unbounded recheck loop, lock-file convention, retained-directory rename,
  inode claim, or another filesystem authority channel to simulate that
  impossible guarantee.
- After the final successful parent-directory `fsync`, immediately perform one
  final paired validation of the already read-back bundle FD and its literal
  direct-child entry with `follow_symlinks=False`. Both observations must
  match the expected regular-file type, device, inode, `0444` mode, link count
  one, exact byte size, modification time, and already proved bundle bytes and
  digest. The successful completion of the second member of that pair is the
  writer operation's linearization point. Any substitution detected before or
  during that pair is `BUNDLE_CREATE_FAILURE` and emits no receipt.
- A namespace mutation after that linearization point, including one before
  the caller observes Python return or stdout, is external post-publication
  drift rather than a file the writer accepted. It may therefore leave a
  `BUILT` receipt. No further finite pathname probe extends the publication
  interval. The writer closes its descriptors and constructs its return only
  from the already validated in-memory bytes and the receipt identity tuple
  `(bundle_sha256, package_sha256, literal_bundle_path)`.
- The receipt is content identity, not an inode lease. A byte-for-byte
  canonical replacement with the same three tuple values is indistinguishable
  after the writer's descriptors close and carries no additional authority;
  it is the same receipt identity. Any non-identical path, metadata, byte,
  package, or bundle-hash replacement is transport drift and must fail closed
  when consumed. This unavoidable POSIX boundary does not weaken the existing
  digest-bound package, control-file, evidence-tree, or create-only-ref
  authority.
- The controller captures the canonical `build-package` stdout exactly once
  and extracts `bundle_path`, `bundle_sha256`, and `package_sha256` directly
  from that trusted build receipt. It must not derive an expected value from
  the later bundle bytes, an attestation, a review receipt, a closure, the Task,
  or an evidence ref. For a new attempt it captures an entirely new receipt;
  no path or digest from an old, rejected, invalidated, diagnostic, or prior
  attempt receipt may be reused.
- Every external-bundle consumer—`verify-package`, `verify-assignments`,
  `verify-backfill`, `publish-evidence-ref`, and `verify-authorized --bundle`
  —requires the exact all-or-none transport group: `--bundle PATH`,
  `--expected-bundle-sha256 <64-lowercase-hex>`, and
  `--expected-package-sha256 <64-lowercase-hex>`. For these five sources all
  three arguments are mandatory; the literal `--bundle` path is the expected
  path component of the receipt tuple. Omission, partial supply, duplication,
  malformed hex, or any attempt to source the expected values from package or
  control bytes is a usage failure before input consumption. The expected
  hashes are trust-binding validation inputs only; they do not grant attempt,
  review, ref-publication, or deletion authority.
- The single `read_bundle_once` result is the first untrusted-input operation
  after argument parsing. It opens and reads the literal `/tmp` direct child
  once, validates stable descriptor metadata and EOF, reconstructs canonical
  outer bytes, and compares the observed literal path, `bundle_sha256`, and
  `package_sha256` to the controller-trusted arguments before any authority
  preflight, Task/control semantic replay, ref discovery, root-tree projection,
  generator execution, object write, or ref publication. Metadata or
  bounded-read instability fails `BUNDLE_READ_FAILURE`; any canonical but
  non-identical path/bundle/package tuple fails `BUNDLE_TRANSPORT_DRIFT`.
  Neither failure may invoke a generator, grant an attempt, discover or mutate
  a ref, or write an object.
- `verify-authorized --bundle-from-ref` has no external pathname or expected
  receipt arguments. Its parser rejects either expected-hash flag with that
  source, and it retains the separately required in-memory reconstruction and
  digest comparison from a strictly discovered direct ref.

The same round must replace `for-each-ref`-only namespace discovery with this
raw discovery contract:

- `for-each-ref` remains a packed/direct-ref view but is not the sole source:
  Git omits a dangling loose symbolic ref from that output. Open the repository
  common directory and every literal component below
  `refs/codex/review-evidence/agentic-research/gate9/v1` read-only with
  descriptor-relative, `O_NOFOLLOW|O_CLOEXEC` traversal. Absence of the
  namespace is an empty loose snapshot; a symlink, non-directory ancestor, or
  unreadable/ambiguous entry is `FOREIGN_REF`.
- Enumerate every loose descendant as raw names and bytes without following a
  symbolic target. The only admitted leaf paths match the exact canonical
  `attempt-[12]/[0-9a-f]{64}` pattern. Reject extra depth, malformed or
  non-ASCII names, file/directory-prefix collisions, symlink/non-regular
  leaves, duplicate names, symbolic-ref bytes including dangling `ref:`
  targets, non-full object-format OIDs, non-commit targets, and any name not
  admitted by `EVIDENCE_REF_PATTERN`.
- Open each candidate loose leaf descriptor-relative with
  `O_RDONLY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`, then immediately require by
  `fstat` a regular file, link count one, and size `1..65` bytes. Perform one
  bounded read through exact EOF and a stable closing `fstat` before parsing;
  a direct ref must then be exactly `object_format_width + 1` bytes including
  its sole terminal LF. A FIFO, socket, device,
  directory, symlink, oversized file, unstable identity/size, partial read, or
  extra byte is `FOREIGN_REF`; discovery must never block waiting for a writer.
- Record the measured Git behavior normatively, so no later round re-derives a
  control scoped to the wrong command. On the Git in this environment,
  `git for-each-ref` against one exact Gate 9 evidence ref does not block on a
  FIFO, symlink-to-FIFO, symlink loop, directory, dangling symlink, or
  symlink-to-device leaf. It exits zero with empty stdout and empty stderr and
  omits the entry silently, which satisfies a nonzero-exit-or-stderr guard and
  falls straight through to the exact-ref fallback that does block. The calls
  measured to block are `git symbolic-ref`, `git update-ref --no-deref`, the
  index-reading `git diff [--cached] --quiet` and `git status --porcelain`, the
  `O_RDONLY|O_NOFOLLOW` control-file open, the descriptor-relative bundle open,
  and every whole-file `read_bytes`-class read. A bound attached to
  `for-each-ref` by name therefore bounds nothing, and no silently omitted leaf
  is ever caught by a timeout. Scope that to the phase it is true of, because
  this Plan's own ordering makes the unscoped form false. A leaf of one of
  those omitted types that is already present when the raw loose enumeration
  runs never reaches `for-each-ref` through the gate: it is non-regular,
  symbolic, or otherwise inadmissible, and the raw walk rejects it as
  `FOREIGN_REF` before any Git query is issued. What becomes of a leaf
  substituted _after_ the raw walk has already admitted the name — which
  `for-each-ref` invocation observes it, and which clause catches it — is not a
  passing requirement of this gate. Three consecutive rounds stated it
  inconsistently, and both fix-6 re-reviews found the fix-6 statement still
  contradicted this Plan's own snapshot ordering. That classification is
  robustness-backlog item R1; no round may assert any direction as settled
  until it is reconciled there, and the unsettled classification is not licence
  to weaken the raw/union disagreement rule below, which stays normative
  exactly as stated there.
- Attach the bound to the execution funnels rather than to an enumerated
  command list. Exactly three funnels carry the obligation; no Gate 9 call
  site may reach a subprocess, a descriptor-opening read of an
  outside-influenceable path, or a whole-file read outside them, and every
  call site must reach its hazard through one of them:
  1. every Gate 9 subprocess invocation, whatever the program or arguments,
     including the generic Git runner, the repository-root probe, and the
     sealed-manifest generator execution;
  2. every descriptor-opening read of a path an outside actor could influence,
     explicitly including the control-file reader for every `--attestation`,
     `--*-report`, `--*-receipt`, `--*-closure`, `--drift-proof`, and
     `--terminal-report` argument, and the descriptor-relative bundle reader;
  3. every `Path.read_bytes()`-class whole-file read reached in the Gate 9
     flow, including `--task`, `--spec`, `--plan`, the fixed tracked Task path,
     and the Git common-directory grafts probe.
- State the funnel scope exactly so the closure claim above is true as
  written. Funnel 2 admits descriptor-opening _reads_ of outside-influenceable
  paths. Descriptor opens that create an entry or open a directory are outside
  every funnel, and are excluded deliberately: an `O_CREAT|O_EXCL|O_NOFOLLOW`
  create cannot open a pre-existing special file at all; the `scandir` walk and
  the exclusive-create `os.open` were measured non-blocking under the
  substitutions prepared for them; and the bundle writer's `/tmp`
  `O_DIRECTORY` open, against which no substitution was prepared, is excluded
  by reasoning rather than by a measurement, and the reasoning is stated here
  rather than left to the reader: `O_DIRECTORY` fails `ENOTDIR` against
  anything that is not a directory, so a substituted FIFO, socket, or device
  node at that path cannot be opened at all, let alone parked in, and a
  substituted directory is not a parking hazard. The bundle writer's `/tmp`
  directory open, its
  exclusive create, the anonymous `memfd` descriptor, and the
  worktree-registry directory open and `scandir` traversal are therefore named
  here as out of funnel scope rather than routed through a funnel described as
  a reader. The exclusion reaches those directory opens and traversals only:
  every per-entry `Path.read_bytes()`-class whole-file read performed inside
  the worktree-registry walk stays inside funnel 3 and carries the funnel-3
  bound. They keep their existing `O_NOFOLLOW`, exclusivity, and identity
  checks.
- Give funnel 1 the spawn bound, stated as a property of the funnel: stdin
  closed, captured or size-bounded output, a separate process session, exactly
  2.0 seconds for completion, then termination to the child process group,
  0.5 seconds of grace, kill if still live, and a synchronous reap. Do not
  retry. A signal is sent only to a process group this gate created; no funnel
  may signal the gate's own group, its session, or its parent.
- Give funnels 2 and 3 the descriptor bound, stated in terms a non-spawning
  operation can satisfy, because they spawn nothing and therefore have no
  child, no stdin, no captured output, and no process group of their own:
  open with `O_RDONLY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`; `fstat` the descriptor
  and require the expected regular type and identity before the first read;
  cap the bytes read; complete the open-plus-read sequence within the same
  2.0-second budget measured against a monotonic clock; and on expiry close
  the descriptor if one was obtained, fail closed, and send no signal and reap
  nothing.
- Name the deadline mechanism rather than implying it, and require one that can
  actually bound the call the deadline exists for. The mechanism is
  `signal.setitimer(ITIMER_REAL, ...)` armed **before** the
  `open()` call, with a handler that raises, and disarmed in a `finally`. It
  must be armed before the open because a park inside `open` is the residual
  hazard this deadline exists for. State the delivery invariant this mechanism
  actually needs, rather than the arming thread: `ITIMER_REAL` delivers
  `SIGALRM` to the process, and the kernel may hand it to any thread that is
  not blocking it, so arming from the main thread does not by itself guarantee
  that the parked call is the one interrupted. The gate must therefore be
  entered as its own single-threaded process, and if any round ever gives it a
  thread, that thread must `pthread_sigmask(SIG_BLOCK, {SIGALRM})` so delivery
  can only land on the thread that performs the guarded open. Method 3's
  bounded join/timeout is a property of the test-side driver, not of the gate
  process, and does not license running the gate off a worker thread. Close the
  two windows around the guarded region as well: the raising handler's
  exception must be caught at the funnel boundary and mapped to that site's
  fail-closed code even when it arrives after the guarded call has returned and
  before the disarm, so a late alarm cannot surface as an unmapped traceback.
  Close the descriptor with the ordinary sentinel-slot-plus-`finally` idiom and
  state the residual honestly instead of mandating a construction that cannot
  produce the property it is stated to produce: the fix-6 Python/security
  review measured on CPython 3.12.3 that an alarm arriving between `open()`
  returning in C and the Python bind leaves the pre-written slot still holding
  its sentinel, so one read-only `O_CLOEXEC` descriptor stays unclosed until
  the fail-closed process exits. That residue is accepted, is
  robustness-backlog item R3, and is not a passing requirement of this gate; no
  round may record the window as closed while it is not.
  `poll()` cannot serve that purpose: it needs
  a descriptor, so it cannot be entered until `open()` has already returned,
  and for the only file type that survives the `fstat` check — a regular file —
  it reports ready immediately and bounds nothing that `O_NONBLOCK` and the
  type check have not already excluded. `poll()` against a monotonic deadline
  is therefore permitted only as an additional read-phase cap, never as the
  sole mechanism and never as an alternative to the armed alarm. A bare
  `subprocess`-style timeout keyword does not exist for these sites, and PEP
  475 retries an interrupted syscall unless the handler raises, so an
  unmechanized cap is not a cap. Arming an interval timer is not "sending a
  signal" in the sense funnel 1's rule prohibits: that rule governs process
  groups, sessions, and parents, while an `ITIMER_REAL` alarm interrupts only
  this process's own execution. The residual limit is an uninterruptible driver
  sleep, which no user-space deadline can preempt; that is the same class of
  POSIX limit this Plan already concedes for substitution windows between
  syscalls.
- Qualify what `O_NONBLOCK` buys, and credit it only for what it does. It
  prevents a FIFO open with no writer from parking the process, which is the
  measured hazard here. It buys nothing for a socket: `open()` on a
  UNIX-domain socket file fails with `ENXIO` whether or not the flag is set, so
  that case is closed by `open()` semantics rather than by the flag. It is not
  a general non-parking guarantee: a character or block device driver may block
  inside `open` irrespective of it, and real non-symlinked device behavior at
  these paths was not determined in the measurement this contract is built on.
  The guarantee is therefore carried jointly by `O_NONBLOCK`, `open()`'s own
  refusal of a socket, the `fstat`-before-read type check, and the alarm armed
  before `open` — not by `O_NONBLOCK` alone, and not by a descriptor-only
  read-phase cap, which reaches none of the residual.
- Bound-expiry cleanup may not mutate a ref, object, lock file, victim path,
  branch, index, or worktree. The 2.0-second budget is a fail-closed liveness
  cap, not a performance budget.
- Map a funnel fault to the fail-closed code of the site that used the funnel,
  not to one global code. For any query, CAS, or read whose selector, argument,
  or lock target is the Gate 9 evidence namespace or one exact Gate 9 evidence
  ref, the code is `FOREIGN_REF`. For the bundle reader it is
  `BUNDLE_READ_FAILURE`; for the control-file reader it is
  `CONTROL_FILE_DRIFT`; for the before/after repository invariant capture and
  proof it is `PROJECTED_INDEX_SCOPE_DRIFT`, which wins over `FOREIGN_REF` on
  the drift-evidence path so the operator diagnosis names the failing
  invariant.
- Preserve the existing `FOREIGN_REF` conditions that remain correct for
  evidence-ref queries: nonzero exit, any stderr byte, output over 4 KiB, a
  malformed or incomplete four-field `refname/objectname/objecttype/symref`
  NUL record, or an unexpected extra row. Use one explicit trailing-NUL format
  for both prefix and exact selectors rather than line-splitting ref names.
  The 4 KiB ceiling is the fail-closed cap for a namespace that admits at most
  two canonical attempt leaves, and the stderr rule deliberately classifies a
  benign Git advisory as foreign; run these queries with isolated
  configuration so stderr stays deterministic.
- Guard the index before it is read, not after. The regular-file guard on the
  repository index path must run before the first Git invocation that reads
  the index, so a substituted non-regular index is rejected by the guard
  instead of blocking that first index read. Name the actual first site rather
  than the assertion that is easiest to point at: in every package-consuming
  mode the first index-reading Git invocation is inside the authority
  preflight, whose per-path `git diff --quiet -- <path>` and
  `git diff --cached --quiet -- <path>` pairs run once for the helper and once
  for each generator, and both of those were measured to block under a
  non-regular index. The guard therefore runs immediately after the
  repository-root probe and before the authority preflight in every mode. It
  is unconditional: it is not gated by `--require-clean-real-index`,
  `--require-task-only-worktree`, or any other flag, and the clean-real-index
  and Task-only worktree assertions run after it, never before it — which in
  `verify-authorized` is more than a hundred lines later and conditional, so
  anchoring the guard to them would leave the measured blocking reads
  unguarded. A dangling symlink index, which makes `git status` exit zero with
  empty output, must also be rejected by the guard rather than surfacing later
  as an emptied worktree path set under an unrelated code.
- Diagnose an evidence-ref lock residue and stop; never clear it.
  `git update-ref --no-deref` creates `<ref>.lock` before the read that can
  block, so a `<ref>.lock` can sit inside the evidence namespace with no live
  writer behind it. This gate's own termination is not what leaves one: the
  fix-4 specification review measured that a blocked
  `git update-ref --no-deref` exits on `SIGTERM` within one second and that
  Git's own lock-file signal handler removes the lock on the way out, so
  funnel 1's terminate-then-conditional-kill sequence normally leaves nothing
  behind. A residue reaches the namespace from a writer killed outright with
  `SIGKILL`, a crashed or interrupted writer, a live concurrent writer, or a
  planted file. Once the raw loose walk specified here exists it would
  otherwise reject that residue as `FOREIGN_REF`, because
  `<canonical-leaf>.lock` is not a name `EVIDENCE_REF_PATTERN` admits; the
  helper's current `for-each-ref`-only enumeration does not list `.lock` files
  at all, so the residue is invisible today rather than misreported. Diagnose
  it distinctly as `STALE_REF_LOCK`; `FOREIGN_REF` stays reserved for a
  genuinely foreign ref. Raw loose enumeration must classify any
  `<canonical-leaf>.lock` sibling inside the fixed namespace as this distinct
  state, whatever its byte size and whatever its observed file type, instead of
  rejecting it as a name not admitted by `EVIDENCE_REF_PATTERN`.
- `STALE_REF_LOCK` is a terminal fail-closed state that performs no filesystem
  mutation of any kind. The gate does not unlink, truncate, rename, open for
  writing, or otherwise touch the lock, its siblings, its directory, the
  corresponding ref leaf, any object, the branch, the index, or the worktree.
  It does not retry, does not wait for the lock to age out, and does not
  proceed to exact ref resolution, the create-only CAS, or any later step.
  This is required by the Gate 9 evidence architecture boundary in Spec 137:
  the only permitted Gate 9 ref mutation is the separately reviewed
  create-only evidence-ref publication, and unlinking a lock file inside
  `.git` is neither that publication nor an append. No round may reintroduce
  clearance by tightening its conditions.
- Because the gate performs no clearance, it does not need to and cannot
  establish ownership of the lock, and it makes no ownership claim. A lock left
  behind by an earlier attempt of this gate whose child was killed outright, a
  lock held by a live concurrent writer, and a same-UID lock planted with a
  backdated modification time are indistinguishable to it and are all the same
  terminal state. No attempt
  ordinal, age threshold, byte size, own-children-reaped condition, or
  provenance record is used to discriminate them; the fix-3 attribution
  machinery is removed rather than refined, because its only consumer was the
  clearance it authorized. Byte size is explicitly not a discriminator, because
  a writer that has already written the new object ID into its lock leaves a
  non-empty one, and a size-scoped trigger would leave that reachable state
  with no code at all.
- The diagnosis is read-only and bounded: an
  `fstatat(dir_fd, name, AT_SYMLINK_NOFOLLOW)` of the exact `.lock` sibling
  against the namespace directory descriptor the descriptor-relative raw walk
  already pinned, never a pathname `lstat`, so the diagnosis cannot be
  redirected by a renamed ancestor. Report exactly what
  a human operator must inspect and remove — the repository common directory,
  the full literal `<ref>.lock` path, its observed file type, byte size, and
  modification time, and whether the corresponding ref leaf is absent, an
  admitted canonical direct commit ref, or something else. Do not report the
  lock's contents, and do not open it.
- Exit status for `STALE_REF_LOCK` is 1, with empty stdout and stderr-only
  diagnostics. That matches `FOREIGN_REF`, `BLOCKED`, `INVALIDATED`, and every
  other fail-closed code in this contract. Exit 2 is reserved for
  `LIVE_HEAD_REQUIRED` alone, as stated above, and no second cause may be
  collided onto it: the helper has two nonzero statuses precisely so a
  controller or wrapper can tell omitted live-HEAD bindings apart from every
  other fail-closed outcome, and a lock file sitting in the evidence namespace
  is not that cause. The empty-stdout half is an ordering requirement, not only
  a formatting one: the after repository-invariant capture must complete before
  any stdout emission in every mode, including publish mode, so a residue
  observed in that capture can never follow a canonical JSON payload onto
  stdout and hand an exit-status-blind consumer a success-shaped result under a
  terminal code. Any ambiguity — an unreadable `.lock` sibling, a `.lock`
  whose leaf name is not admitted, or a residue the walk cannot classify —
  also fails closed rather than being resolved in the gate's favour; where the
  name is not an admitted canonical leaf plus `.lock`, the existing
  `FOREIGN_REF` rejection stands. Resolve the one state that would otherwise
  carry two candidate codes: a non-regular `.lock` sibling whose leaf name
  **is** an admitted canonical leaf is `STALE_REF_LOCK`, not `FOREIGN_REF`,
  which is what the diagnosis bullet's mandate to report "its observed file
  type" already presumes. That costs nothing, because the diagnosis is an
  `fstatat` and the gate never opens the lock, so a non-regular residue is
  reported without being entered.
- Recovery is an operator action outside the gate, followed by a fresh run.
  The next run is not a continuation and inherits nothing from the terminated
  one.
- Within each complete namespace snapshot, take the raw loose enumeration
  first and the `for-each-ref` packed/direct view second, so the ordering the
  regressions rely on is fixed by this contract rather than by test prose.
  Merge the byte-sorted raw loose names with the `for-each-ref` names, then
  prove every union member is one direct commit ref with the exact same OID in
  two complete namespace snapshots surrounding validation. Bind raw loose
  file identity/bytes where present and reject any name, kind, OID, target, or
  object-type change as `FOREIGN_REF`. State the raw/union disagreement rule
  normatively rather than leaving it implied, because the claim above rests on
  it: where both views observe the same name they must agree on the OID and on
  the direct-commit kind, and any disagreement is `FOREIGN_REF`; a name the
  raw loose walk admits that `for-each-ref` omits is `FOREIGN_REF`; and a name
  `for-each-ref` reports
  with no corresponding loose file is admitted only as a packed direct commit
  ref, which is the one legitimate one-sided membership. Reuse this strict
  snapshot for attempt
  derivation and the before/after repository-invariant capture so dangling
  symbolic refs cannot be treated as an empty namespace or disappear from
  drift evidence. Exact ref resolution, leaf replay, create-only no-deref CAS,
  and post-read OID revalidation retain their existing checks.
- Keep the omission clause normative and do not retire it as vacuous. Its
  reachability was contested across three rounds; the fix-6 specification and
  Python/security re-reviews each measured independently on
  `git version 2.43.0` that a regular, canonically named leaf holding a valid
  commit OID that the raw walk has already admitted, and that is unlinked
  before the `for-each-ref` of the same snapshot runs, is dropped with exit 0,
  empty stdout, and empty stderr, so no preserved guard fires on it. Those are
  recorded observations of those reviews. State the split at assertion
  granularity here too, since fix-8 redrew it and this sentence was left at
  fixture granularity. Classifying every other candidate condition against this
  clause is robustness-backlog item R1, and the named code plus the clause
  attribution that a constructed regression is asserted to yield are R2; neither
  is a passing requirement. The regression itself is not deferred with them:
  method 3 mandates one, and its assertions that discovery finishes within its
  bound, parks nowhere, and reaches a mapped fail-closed terminal state rather
  than proceeding are passing requirements. The clause's job in this contract is
  to fail closed on a one-sided raw/union membership the contract does not
  otherwise admit, and it does that whatever produced the membership.

Write RED first with these exact focused methods. Fix-8 scopes which of their
_assertions_ round 4 must satisfy for passage, at assertion granularity rather
than by whole sub-case, because the same injection produces two claims that
belong on different sides; fix-9 corrects where fix-8 stated that line
inconsistently with how it applied it. The gate-blocking kind: that the
operation finishes within its stated bound, that any child this gate spawned is
terminated and synchronously reaped, that no site parks, and that the gate
reaches a mapped fail-closed terminal state — exit 1, empty stdout, and a stderr
whose first line is a `<CODE>: <detail>` diagnostic rather than an unmapped
traceback — instead of proceeding. State that last one in that form rather than
leaving its form to the implementer: an unhandled Python traceback also exits
nonzero with empty stdout and a non-empty stderr, so a generic "reached some
fail-closed state" assertion cannot tell a mapped terminal code from a crash,
while this form proves the run left through the contract's own mapped
fail-closed path — the same path the late-alarm mapping clause above requires —
without naming which code it emitted, and so adds nothing to the demoted
obligation. The kind moved to robustness-backlog items R1 and R2: the named
error code, and the classification argument about which clause catches which
substitution. Constructing an injection is not what places an assertion; what
the assertion claims is.

The criterion that places a code claim is stated here in the same words the pass
condition and R2 above use. Demoted: a claim that names one specific error code as the outcome
of an adversarial substitution or removal the fixture directs at a path the gate
reads. Retained: every other claim those same fixtures make, and three named
classes of code claim — methods 1 and 2's external-bundle transport codes, whose
surface this Plan's capability analysis places with a weaker different-UID local
principal rather than with the total-bypass principal whose proof obligation is
unbounded; method 4 sub-case 4's `STALE_REF_LOCK`, whose residue is planted and
arises with no adversary; and method 4 sub-case 6's `FOREIGN_REF` guards, which
the fixture injects into `git`'s own output rather than at a path the gate reads.
A criterion of this shape cannot decide every case unaided, because a leaf a
fixture creates and one it substitutes are the same file on disk, so the RED
scoping enumeration that applies it to every method and sub-case is its closed
application, and where the two could be read apart that enumeration governs.

That enumeration is the following list. It is the closed application to the four
methods, so that no method and no sub-case is left with an undefined status,
including the one sub-case whose own premise puts all of its assertions in the
backlog. A round that finds a case the criterion does not place cleanly amends
this list in a reviewed Plan amendment rather than reasoning from the criterion
to a placement this list does not state.

- Methods 1 and 2 stay gate-blocking in full, including their
  `BUNDLE_TRANSPORT_DRIFT` and `BUNDLE_READ_FAILURE` codes. They are the first of
  the criterion's three named retained classes: they bind the external bundle at
  the literal `/tmp` direct child, a surface this Plan's capability analysis
  places with a weaker different-UID local principal rather than with the
  total-bypass principal, and their codes are the all-or-none transport binding
  the default rule above already carries into passage.
- Method 3 stays gate-blocking for its non-injection coverage, including the
  codes that coverage asserts, and for the bounded, non-parking, non-reopening,
  mapped fail-closed behaviour of each of its injection cases, including the FIFO
  case's bounded join/timeout. Only the named code each injection is asserted to
  yield, and the clause attribution R1 owns, are backlog — stated together
  because R1 forbids any round to assert a clause attribution as settled, so
  leaving the attribution gate-blocking would mandate exactly what R1 forbids.
- Method 4's opening proof that a regular raw/direct snapshot succeeds stays
  gate-blocking.
- Sub-case 1 stays gate-blocking for the absence it asserts — no timeout, no
  termination grace, no reaped child, no `<ref>.lock` — because that is a
  liveness claim that depends on no unsettled classification. Only its
  `FOREIGN_REF` verdict is backlog, under R2.
- Sub-case 2 is backlog in whole, and the reason is stated rather than left to
  be derived: its injection point and its naming of the observing call are the
  direction R1 owns and this Plan does not assert as settled, so it can carry no
  gate requirement until R1 closes.
- Sub-case 3 carries the mandatory funnel-1 demonstration and stays
  gate-blocking for it — bound expiry, the signal delivered to the child process
  group this gate created, child absence, and synchronous reap within the bound
  plus grace, together with reaching a mapped fail-closed terminal state — because
  its injection point is the `commit-tree` boundary between an absent-ref lookup
  and the CAS, which does not depend on R1. Only its `FOREIGN_REF` verdict is
  backlog, under R2, because that verdict names one specific code as the outcome
  of a substitution the fixture directs at a path the gate reads, which is the
  demoted class exactly. Demoting the code identity does not hollow out the
  demonstration: the four liveness assertions and the mapped fail-closed form
  above are gate-blocking without it. This is the gate-blocking demonstration of
  funnel 1's bound, grace, and reap; no other gate-blocking assertion in these
  four methods supplies one.
- Sub-case 4 is gate-blocking in full, including the size-independent
  `STALE_REF_LOCK` predicate across both variants, exit 1 with stderr-only
  diagnostics, and the assertion that the run performed no unlink and changed
  nothing. It is the second of the criterion's three named retained classes: its
  residue is planted by the fixture rather than substituted at a path the gate
  reads, and it arises with no adversary at all, so no assertion in it is an
  adversarial code assertion.
- Sub-case 5 has three parts and each is placed individually rather than as a
  half. The FIFO at a control-file argument stays gate-blocking for park
  prevention, the absence of an unbounded read, and reaching a mapped fail-closed
  terminal state rather than proceeding; only its named `CONTROL_FILE_DRIFT` code
  is backlog, under R2. The FIFO at `--task`, `--spec`, or `--plan` is
  gate-blocking in full, because it names no code at all: its whole claim is that
  funnel 3 fails closed without an unbounded read, so the demotion has nothing to
  cover there and R2 does not name it. The non-regular repository index part is
  gate-blocking in full, because it names no substitution code and asserts guard
  ordering against the first index-reading Git invocation.
- Sub-case 6 is gate-blocking in full, including its `FOREIGN_REF` assertions.
  Its byte-for-byte victim, outside-ref, and object-inventory comparison is the
  verification of the no-mutation property Spec 137 requires directly and that
  the fix-5 Python/security approval rested on, so it cannot be non-blocking. Its
  separate injected nonzero-exit and stderr-with-zero-exit cases are the third of
  the criterion's three named retained classes, and their placement is stated
  rather than left to the default rule: the fixture injects them into `git`'s own
  output rather than at a path the gate reads, and they exercise the preserved
  nonzero-exit and stderr guards this contract keeps normative rather than a
  classification R1 owns.

Round 4 must satisfy every gate-blocking assertion above. It may also implement
the backlog assertions; their text below remains the specification of how to
build them, except sub-case 2, whose retained text is R1's unreconciled starting
point rather than a build specification and which no round may implement until
R1 reconciles it. A review finding that names only a backlog assertion is
recorded against the item that owns it and is governed by the status stated in
the pass condition above — a reviewer following this Plan has no ground to raise
the absence of a backlog assertion, and a Critical or Important finding filed
against one anyway remains unresolved and blocking until repaired or re-scoped.
This scoping removes no control: everything these sub-cases exercise stays
mandatory in the executable contract above.

1. Rename
   `test_atomic_bundle_writer_rejects_late_directory_entry_substitution` to
   `test_atomic_bundle_publication_linearizes_at_final_post_fsync_pair` and
   move its existing finite late-substitution cases to their correct boundary:
   every substitution before or during the final pair fails without a receipt,
   while one non-identical substitution injected immediately after the pair
   may leave the original `BUILT` receipt.
2. `test_all_external_bundle_consumers_reject_post_publication_transport_drift_before_authority`
   captures the first build receipt, creates a second fully canonical,
   metadata-valid bundle with a different valid bundle/package tuple, and
   substitutes the second inode at the first literal path after publication.
   Feed the first controller-captured expected hashes and that unchanged path
   to all five external-bundle consumers. Each must fail
   `BUNDLE_TRANSPORT_DRIFT` before any authority/ref-discovery/projection/generator
   function or `hash-object`/`mktree`/`commit-tree`/`update-ref` call, with
   unchanged branch/index/worktree, generated-output, old-pack, lifecycle, and
   evidence-ref snapshots. Add parser cases proving the expected hashes are
   required together for every external source, are exact lowercase 64-hex,
   and are forbidden with `--bundle-from-ref`.
3. `test_evidence_ref_discovery_finds_dangling_loose_symbolic_refs_and_stays_stable`
   first proves the fixture's dangling canonical loose symref is absent from
   `for-each-ref`, then requires `FOREIGN_REF`; it also covers malformed raw
   names, a filesystem symlink, a FIFO substituted before leaf open, a
   noncanonical/direct-object leaf, and substitution between the two namespace
   snapshots without changing the victim or creating an outside ref. The FIFO
   case runs with a bounded join/timeout and proves discovery returns
   `FOREIGN_REF` without blocking or opening the FIFO again. It also covers the
   raw/union omission clause with the one condition measured to reach it: a
   regular, canonically named leaf holding a valid commit OID, admitted by the
   raw loose walk and then unlinked before the `for-each-ref` of that same
   snapshot runs, using that snapshot's `for-each-ref` invocation as the
   observable boundary — the same hooking technique the between-snapshots case
   already uses. That invocation exits zero with empty stdout and empty stderr,
   so no preserved nonzero-exit or stderr guard can fire, and the case must
   fail `FOREIGN_REF` out of the omission clause specifically, with the victim,
   outside-ref namespace, and object inventory unchanged. Do not substitute a
   missing-object or non-commit-OID leaf for this case: measurement places
   those in the nonzero-exit guard and the kind-agreement clause respectively,
   so neither would exercise the clause under test.
4. `test_evidence_ref_hazard_funnels_are_bounded_reaped_and_fail_closed`
   first proves a regular raw/direct snapshot succeeds, then pins the measured
   baseline with a direct out-of-gate `git for-each-ref` invocation in the
   fixture: with a FIFO at the canonical leaf, that invocation exits zero with
   empty stdout and empty stderr far inside the bound. That is a recorded
   environment fact, not a gate outcome — a leaf of that type already present
   when the raw loose enumeration runs never reaches `for-each-ref` through the
   gate, because the raw walk rejects it first. Where a leaf substituted after
   the raw walk has admitted the name is observed, and which clause catches it,
   is the classification fix-7 moved to robustness-backlog item R1; do not
   restate it here as settled. The test must not assert a timeout, a termination
   grace, or a reaped child for that call, and must not assert that the
   omitted leaf is caught by
   raw/union disagreement. Each remaining sub-case must state either its own
   mid-flight injection point, which must be one this Plan's own ordering
   actually reaches, or — where this Plan's own sequences cannot produce the
   state under test — its own directly constructed fixture, because raw loose
   enumeration runs first and rejects a non-regular leaf before any Git query
   is issued. Each sub-case asserts only what its site produces:
   1. **Pre-snapshot FIFO.** A FIFO placed at the canonical leaf before the
      strict namespace snapshot must fail `FOREIGN_REF` out of raw loose
      enumeration, without reaching `for-each-ref`, `symbolic-ref`, or
      `update-ref`, and therefore without a timeout, a termination grace, a
      reaped child, or any `<ref>.lock`. Assert that absence, not a bound.
   2. **Exact-ref fallback.** This whole sub-case is a robustness-backlog item
      under R2, and the reason is its premise, not its fixture. To reach the
      fallback the strict snapshot must first succeed, so the injection goes
      after both complete namespace snapshots and before exact ref resolution.
      The construction previously recorded here — using the second snapshot's
      final `for-each-ref` invocation as the observable boundary, with that
      invocation then exiting zero and empty and falling through to
      `git symbolic-ref` as the call measured to block — is exactly the
      classification R1 owns, and the fix-6 specification and Python/security
      reviews both found its observer naming wrong, because under this injection
      point that invocation has already returned and cannot be the observer. It
      is retained here as R1's unreconciled starting point, explicitly not as a
      settled direction and not as a specification round 4 may build from. A
      round may implement this sub-case only after R1 reconciles the injection
      point with the observing call, and must restate both here in the same
      commit. None of this sub-case's own assertions is gate-blocking; the
      mandatory funnel-1 demonstration is sub-case 3, whose injection point does
      not depend on R1. The process-group observation point named at the end of
      this sub-case is a definition rather than one of its assertions, and it is
      not demoted with them: backlog item R4 uses it, and gate-blocking sub-case
      3 restates it below in full rather than reading it out of this sub-case, so
      no gate-blocking assertion is sourced from demoted text.
      A round that does implement it asserts that funnel 1 expires the
      2.0-second bound, signals the child
      process group, and that within that bound plus the 0.5-second grace the
      child is gone, has been reaped synchronously, and the verdict is
      `FOREIGN_REF`. Do not assert that the `SIGKILL` escalation fired: the
      fix-4 specification review measured that a blocked `git symbolic-ref` or
      `git update-ref --no-deref` exits on `SIGTERM` well inside one second, so
      the conditional kill normally never runs and asserting it would fail for
      a reason unrelated to the missing Step 0e contract. Assert the escalation
      only in a sub-case that first proves its child survived `SIGTERM`. Record
      the consequence rather than leaving it silent: funnel 1 still requires the
      0.5-second grace, the conditional kill, and the synchronous reap, and
      these four methods leave that escalation branch unexercised. Fix-8
      withdraws the ground fix-7's disposition table recorded as withdrawn but
      left standing here: reachability is not an open question. The fix-6
      Python/security review showed that the fixture's own generator-script
      writer and `git` wrapper already reach a `SIGTERM`-surviving child through
      funnel 1, so the escalation branch is constructible. It is left unexercised
      because it is the accepted, named coverage gap owned by robustness-backlog
      item R4, not because reachability is unknown. A round that takes R4 builds
      the fixture from that established reachability rather than inventing one on
      assumption. Name the
      observation point for the process-group claim rather than leaving it to
      the implementer: the fixture records the helper's descendant PIDs and
      their process-group ID before the bound expires, then requires every
      recorded PID gone and `os.killpg(pgid, 0)` to raise `ESRCH` after bound
      plus grace. Where a sub-case's fixture cannot observe that group, it
      asserts only the child absence and synchronous reap it can observe and
      does not assert group targeting at all.
   3. **Create-only CAS.** To reach `update-ref --no-deref`, exact ref
      resolution must first report the ref absent, so inject the FIFO after
      that lookup returns absent and before the CAS runs, using the
      `commit-tree` invocation between them as the observable boundary — the
      same mid-flight substitution technique the sibling method already uses
      between the two namespace snapshots. State this sub-case's assertions in
      full here rather than by reference, because it is the mandatory funnel-1
      demonstration and must not read its assertion list out of demoted
      sub-case 2. Assert that funnel 1 expires its 2.0-second bound; that the
      signal goes to the child process group this gate created, observed by
      recording the
      helper's descendant PIDs and their process-group ID before the bound
      expires and then requiring every recorded PID gone and
      `os.killpg(pgid, 0)` to raise `ESRCH` after bound plus grace; that within
      that bound plus the 0.5-second grace the child is absent and has been
      reaped synchronously; and that the run reaches a mapped fail-closed
      terminal state — exit 1, empty stdout, and a stderr whose first line is a
      `<CODE>: <detail>` diagnostic rather than an unmapped traceback. Also
      assert `FOREIGN_REF`. Do not assert that the `SIGKILL` escalation fired:
      the fix-4 specification review measured that a blocked
      `git update-ref --no-deref` exits on `SIGTERM` well inside one second, so
      the conditional kill normally never runs and asserting it would fail for a
      reason unrelated to the missing Step 0e contract. This sub-case carries the
      gate-blocking funnel-1 demonstration: its expiry, process-group signal,
      child-absence, synchronous-reap, and mapped fail-closed assertions are
      passing requirements, and its injection point is fixed by this contract's
      own ordering rather than by the classification R1 owns, so it does not
      inherit sub-case 2's unsettled premise. Only its `FOREIGN_REF` verdict is a
      backlog assertion under R2, because that verdict is the one thing here that
      names a specific code as the outcome of the substitution; every assertion
      listed above it is gate-blocking without it.
   4. **Lock residue.** Do not chain this sub-case off sub-case 3. The residue
      cannot arise from this gate's own termination path: per the measurement
      recorded above, the blocked child exits on `SIGTERM` and Git's lock-file
      handler removes `<ref>.lock` on the way out, so the
      terminate-then-conditional-kill sequence leaves nothing to diagnose, and
      a fixture that waits for one would never reach the assertion. Plant the
      residue directly instead: create a regular `<canonical-leaf>.lock` file
      inside the fixed evidence namespace, with no FIFO and no blocked child
      anywhere in the fixture. Run it in two variants — one zero-byte and one
      holding a full-width OID plus its terminal LF — to prove the
      classification does not depend on byte size. De-chaining removed this
      sub-case's inherited helper mode, so name it: run each variant in
      `build-package`, which reaches `derive_attempt` and therefore the strict
      namespace snapshot that classifies the residue. A fresh run must diagnose
      each as `STALE_REF_LOCK` rather than `FOREIGN_REF`, exit 1 with
      stderr-only diagnostics naming the literal lock path, and terminate.
      Assert that the
      lock file is still present, byte-identical, and unchanged in type, size,
      and modification time after that run, that the ref leaf, its siblings,
      its directory, the object inventory, the branch, the index, and the
      worktree are unchanged, and that the run performed no unlink. There is
      no clearable-lock case and no clearance-condition matrix to assert,
      because the gate performs no clearance.
   5. **Control-file, whole-file, and index sites.** A FIFO at a control-file
      argument must fail `CONTROL_FILE_DRIFT` without parking in `open`. A
      FIFO at `--task`, `--spec`, or `--plan` must fail through funnel 3
      without an unbounded read. A non-regular repository index must be
      rejected by the index guard before any index-reading Git invocation
      runs, asserted against the first `git diff` inside the authority
      preflight rather than against the clean-real-index assertion, and
      asserted in a mode where `--require-clean-real-index` and
      `--require-task-only-worktree` are absent, proving the guard is
      unconditional.
   6. **Every sub-case.** Compare the victim, outside-ref namespace, and Git
      object inventory byte-for-byte with their before snapshots. Separate
      injected nonzero-exit and stderr-with-zero-exit cases must also fail
      `FOREIGN_REF` without retry or state change.

Run the four methods as tests-only RED, implement the minimum correction, and
run them as GREEN before the remaining twenty existing exact Step 0e methods
plus these four methods (twenty-four total), the complete two-class suite,
public generator parity/freshness, static checks, metadata, whitespace, exact
three-file scope, and repository/lifecycle invariants. The focused command is:

```bash
python3 -m unittest \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_atomic_bundle_publication_linearizes_at_final_post_fsync_pair \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_all_external_bundle_consumers_reject_post_publication_transport_drift_before_authority \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_evidence_ref_discovery_finds_dangling_loose_symbolic_refs_and_stays_stable \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_evidence_ref_hazard_funnels_are_bounded_reaped_and_fail_closed \
  -v
```

Package the exact round-4 predecessor-to-commit range for two new independent
reviews. Both must return C0/I0/M0 before the Task-only Step 0e closure or any
Gate 9 action. The closure-integrity reviews remain separately required after
that Task-only closure.

**Pre-implementation prerequisite — close the Step 0d breaker and bind the new approval:**

1. Require the Plan-amendment execution barrier and Task 9a to be complete,
   including the amended-Spec aggregate range
   `b77abacb610c853db3e9fef2bdef8cc7855c62a2..af37969b26f7e96d684fa0fdf8a0ee2418a4ac23`,
   both final amended-Spec reviews Approved C0/I0/M0, exactly 21 new-pack
   files/20 leaves, 36/36 requirements, and both generator freshness checks.
   From that clean reviewed `HEAD`, modify only
   `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`.
   Record the exact Step 0d final range and both Needs fixes C0/I1/M0 verdicts,
   mark Step 0d `BLOCKED`, record the English approval boundary above, keep
   `GATE9_REVIEWED_CODE_HEAD` at `71eb4feb7d4a085fd2910038a374987773de1e1d`,
   and set Step 0e implementation/reviews plus every Gate 9 downstream action
   to `Not Run`. Do not change the pending Gate 9 marker.
2. Run focused Task metadata, `git diff --check`, and exact one-file scope
   checks. Commit with exact subject
   `docs(task): record gate 9 tree object recovery approval`, then obtain fresh
   independent specification and Python/security reviews at C0/I0/M0 over
   that Task-only range. Any finding returns to a Plan correction; it does not
   authorize implementation.
3. Record both immutable prerequisite receipts outside the self-referential
   Task. Start implementation from that unchanged, clean reviewed `HEAD`.

The prerequisite stages exactly the Task and nothing else:

```bash
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --cached --name-only
git diff --cached --check
git commit -m "docs(task): record gate 9 tree object recovery approval"
```

**Exact implementation scope after the prerequisite (six files):**

1. Modify
   `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` only
   for Step 0e RED/GREEN/full evidence, invariants, and `Not Run` review state.
2. Modify `scripts/validation/agentic-research-gate9-evidence.py` to replace
   every scratch/index/directory-package path with the approved tree-object,
   sealed-memfd, in-memory replay, and atomic-bundle design.
3. Modify `tests/validation/test_agentic_research_gate9_evidence.py` for the
   complete helper, security, transport, authority, and invariant matrix.
4. Modify `scripts/knowledge/generate-llm-wiki-index.sh` only to admit the
   helper-only sealed-manifest input while preserving its public interface.
5. Modify `scripts/knowledge/generate-llm-wiki-coverage.sh` under the same
   boundary.
6. Modify `tests/validation/test_llm_wiki_retiring_pack_exclusion.py` for both
   public byte-compatibility and internal sealed-manifest coverage.

No generated output, Spec, Plan, lifecycle artifact, old-pack path, index,
worktree registration, or ref is in the implementation scope. The later
Task-only closure is not part of this six-file implementation commit.

**Mutation and object-write envelope:**

- Delete `PinnedScratch`, `ScratchOwnership`, every helper use of
  `GIT_INDEX_FILE`, and every helper invocation of `read-tree`, `update-index`,
  or `write-tree`. Delete all helper paths that call or wrap linked worktrees,
  `TemporaryDirectory`, `mkdtemp`, `mkdir`, `rmdir`, `unlink`, or `rmtree`,
  including deletion projection, Task patches/transitions, evidence-tree
  writing, terminal replay, and authorized ref replay. Do not retain a
  compatibility branch or fallback.
- Git object writes are append-only and limited to
  `git hash-object -w --stdin`, `git mktree -z`, and `git commit-tree`.
  `git update-ref` remains allowed only inside `publish-evidence-ref` for the
  reviewed create-only Gate 9 ref. No mode may delete or roll back an object,
  invoke Git GC/prune, write an index, change a branch/worktree/generated
  output/lifecycle artifact/old-pack file, or mutate a remote.
- Failed or superseded object writes are intentionally unreachable and are
  left to normal Git object-store GC. The helper never cleans the object DB or
  a produced bundle. Every bundle is retained for explicit controller
  disposition; only an `AUTHORIZED` create-only evidence ref is durable Gate 9
  authority.

**Pathless projected root-tree contract:**

- Read the live commit's root tree and each component of
  `docs/90.references/research/2026-07-05-agentic-research-pack-refresh`
  with raw `git ls-tree -z`. Parse each record as
  `mode SP type SP full-object-format-OID TAB raw-name NUL`; reject a missing
  terminator, duplicate/raw-unsorted name, slash-bearing component, `.`/`..`,
  wrong mode/type pair, non-full OID, missing object, or non-tree ancestor.
  Require the exact retiring entry to be one `040000 tree`, and require its
  recursive raw manifest to contain exactly twenty `100644 blob` leaves.
- Remove only that exact raw entry from the `research` tree. Rebuild exactly
  four container trees bottom-up with `git mktree -z`: `research`,
  `90.references`, `docs`, then the root. For every level, preserve every
  sibling's raw mode, type, OID, and name byte-for-byte, replace only the one
  descendant tree OID, reread the new tree with raw `ls-tree -z`, and compare
  it to the expected entry tuple before advancing upward.
- Enumerate the final projected root recursively with raw
  `git ls-tree -r -z --full-tree`, validate every entry and object, and derive
  the exact byte-sorted unique path tuple. The tuple must omit the old subtree,
  retain all siblings, and use strict UTF-8 only at the generator boundary;
  invalid UTF-8 or an unsafe absolute, empty, dot, dot-dot, NUL, or duplicate
  path fails closed.
- Derive and retain all three tree-to-tree deletion artifacts from the same
  initial and projected root OIDs: raw `--raw -z`, `--name-status -z`, and the
  binary/full-index patch. Run `git diff-tree -r --no-commit-id --no-renames`
  with `--no-ext-diff --no-textconv`, `LC_ALL=C`,
  `GIT_NO_REPLACE_OBJECTS=1`, `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, no inherited `GIT_*` configuration, and
  `GIT_ATTR_SOURCE=<initial-root-tree>`. Also pass
  `-c core.attributesFile=/dev/null`. Require exactly the same byte-sorted
  twenty `D` paths in raw and name-status output and exactly twenty deleted
  `100644` files in the patch, with zero outside path. Hostile user/system Git
  config, diff drivers, textconv, environment, or projected-tree attributes
  may not change the bytes; attributes are read only from the initial tree.

**Generic in-memory Git-tree contract:**

- Replace both Task patch builders and evidence-tree writing with one generic
  in-memory trie that consumes `Mapping[path, (logical_mode, bytes)]`. Validate
  every complete POSIX path, reject duplicate and file/directory-prefix
  collisions, hash each leaf with `hash-object -w --stdin`, and write each
  directory bottom-up with `mktree -z`. Re-read and verify every emitted tree.
  Task candidate and marker-transition patches are deterministic tree-to-tree
  diffs between two one-leaf mappings; evidence attachments are normal
  `100644` leaves in the resulting evidence tree.
- Ref reads return `Mapping[path, bytes]`. `build_evidence_leaves`, terminal
  replay, attempt-2 prehistory replay, and both authorized sources consume
  mappings directly. Delete evidence materialization and every filesystem
  extraction path. Canonical JSON, reports, receipts, closures, Task bytes,
  and package attachments are parsed and hashed from the one in-memory byte
  value supplied to each validator.
- Open each external attestation, report, receipt, closure, terminal report,
  and drift proof once with `O_RDONLY|O_NOFOLLOW|O_CLOEXEC`; require a regular
  file, `st_nlink == 1`, stable identity/size, offset zero, and a maximum size
  of 4 MiB. Read it completely from that descriptor once, require EOF, recheck
  `fstat`, and pass only bytes downstream. No validator may reopen a control
  path to recompute a digest.

**Sealed generator-manifest contract:**

- Keep both public CLIs byte-compatible:

  ```text
  bash scripts/knowledge/generate-llm-wiki-index.sh [--check|--stdout]
  bash scripts/knowledge/generate-llm-wiki-coverage.sh [--check|--stdout]
  ```

  No argument, `--check`, `--stdout`, help, exit statuses, stdout/stderr, and
  generated bytes retain their reviewed behavior when no internal variables
  are set.

- The helper creates a fresh memfd for each generator with
  `MFD_CLOEXEC|MFD_ALLOW_SEALING`. Its canonical NUL record sequence is
  `schema=agentic-research-llm-wiki-manifest/v1`,
  `object-format=<sha1|sha256>`, `live-commit=<full OID>`,
  `projected-tree=<full OID>`, `count=<canonical decimal>`, followed by the
  exact byte-sorted unique projected paths, with a NUL after every field and
  final path. The manifest is at most 8 MiB.
- Write the complete bytes, rewind to offset zero, then require
  `F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE`. Pass the descriptor
  only to trusted Bash executing the proved-live-reviewed generator blob as
  `bash -s -- --stdout`, with exactly these all-or-none environment variables:
  `GATE9_LLM_MANIFEST_FD`, `GATE9_LLM_MANIFEST_SIZE`, and
  `GATE9_LLM_MANIFEST_SHA256`. The helper passes no index variable, path,
  pipe, or checkout script.
- Internal mode is legal only with the sole public argument `--stdout`.
  Each generator requires all three variables or none; parses canonical
  decimal values; requires current FD offset zero; requires a regular memfd
  with `st_nlink == 0`, the exact byte size and SHA-256, the four required
  seals, EOF after the declared size, exact schema/object-format/OID/count,
  and safe byte-sorted unique paths. It then renders from that manifest only.
  It must not invoke `git ls-files`, `pathlib.Path.exists`, or another
  filesystem-presence fallback in internal mode. Malformed, unsealed,
  wrong-type, oversized, offset, digest, schema, OID, count, path, or partial
  environment input fails before rendering with empty stdout.
- Compare each output byte-for-byte with the tracked output blob at the live
  reviewed commit and, during bundle verification, with the matching logical
  attachment. Require strict UTF-8, LF only, one terminal LF, no stderr, and
  nonempty output. Every one of the six public authority modes and both
  `verify-authorized` sources must freshly rerun the root-tree projection and
  a new sealed memfd per generator before accepting executable bytes or
  authorization. Memoization may exist only inside one CLI invocation and its
  key includes repository identity, package/live/reviewed-code OIDs, projected
  tree OID, generator blob OIDs, and manifest digest.

**Atomic canonical bundle contract:**

- The logical package retains exactly these fifteen attachment paths:
  `HEAD.txt`, `SHA256SUMS`, `assignments.json`, `gate-results.json`,
  `llm-wiki-index.md`, `llm-wiki-stage-category-coverage.md`,
  `new-manifest.tsv`, `old-manifest.tsv`, `package.json`, `plan.md`,
  `proposed-deletion.patch`, `spec.md`, `task-before.md`,
  `task-before-to-candidate.patch`, and `task-candidate.md`.
  Inner package JSON remains canonical `agentic-research-gate9/v1`.
  `package_sha256` remains exactly the SHA-256 of the logical
  `SHA256SUMS` attachment bytes.
- Transport is one canonical UTF-8/LF JSON file, schema
  `agentic-research-gate9-bundle/v1`, with exact top-level keys
  `attachments`, `kind`, `package_sha256`, and `schema`, where `kind` is
  `gate9-package-bundle`. `attachments` is byte-sorted by path and has exactly
  fifteen records with exact keys `base64`, `bytes`, `mode`, `path`, and
  `sha256`; every logical mode is the string `0444`. Base64 is canonical RFC
  4648 with padding and no whitespace. Decode/re-encode equality, byte count,
  digest, path set, checksum manifest, package ID, and inner schemas are all
  mandatory. The SHA-256 of the exact outer canonical bytes is
  `bundle_sha256`; because the random filename is not encoded, ref-only replay
  can reconstruct and verify the same bundle bytes from the fifteen leaves.
- `build-package` accepts no output directory or caller-selected output path.
  It opens literal `/tmp` once with
  `O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`, chooses a direct-child name
  `agentic-research-gate9-attempt-<N>-<32 lowercase hex>.bundle.json`, and
  retries at most 128 random-name collisions. Open the child relative to that
  descriptor with
  `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC` at `0600`; reject a token that
  is not exact lowercase hex before `openat`. Write with a complete-write loop,
  `fsync` the file, `fchmod` it to `0444`, rewind, and read back the exact bytes
  from the same descriptor. Require a stable regular file with `st_nlink == 1`,
  exact mode/size/digest and maximum size 32 MiB, then `fsync` the `/tmp`
  descriptor and immediately complete the final paired FD/direct-child entry
  validation defined by the reviewed correction gate. Completion of that pair
  is the publication linearization point; it is not a promise that the
  pathname remains unchanged until Python return or receipt observation. A
  collision, symlink, traversal, short/zero write, partial write,
  chmod/fsync/readback mismatch, or ancestor error emits no receipt, grants no
  attempt authority, and never unlinks or overwrites an object.
- Successful stdout is one canonical receipt with schema
  `agentic-research-gate9-build-receipt/v1` and exact keys `bundle_path`,
  `bundle_sha256`, `package_sha256`, `schema`, and `state`, where the path is
  the literal canonical `/tmp/<direct-child>` and state is `BUILT`.
  `verify-package` and every later external consuming mode accept only the
  controller-captured `--bundle`, `--expected-bundle-sha256`, and
  `--expected-package-sha256` transport group and read that file once before
  authority, semantic, generator, object, or ref work: open `/tmp` and the
  validated direct child with
  `O_RDONLY|O_NOFOLLOW|O_CLOEXEC`, require regular/nlink-one/`0444`, offset
  zero, stable identity and size `1..32 MiB`, read through the same FD, require
  EOF, then close it. Decode to `Mapping[path, bytes]` in memory; never extract
  an attachment or create a package directory.
- Assignment attestations, receipts, closures, `evidence.json`, and terminal
  verification bind both `package_sha256` and the reconstructed
  `bundle_sha256`. Evidence refs store the fifteen package attachments as
  normal `100644` leaves below `package/`, not the external bundle file.
  `verify-authorized --bundle-from-ref` reconstructs the canonical outer
  bundle in memory, verifies its SHA, and completes full authority replay with
  no external transport.

**Preserved evidence and authorization contract:**

- Preserve the live/reviewed-code/unambiguous-history authority checks, exact
  two-attempt state machine, controller attestation, distinct reviewer IDs and
  task paths, marker-only Task transition, C/I/M integer validation,
  same-reviewer closures, canonical sentinel slots, create-only ref identity,
  and ref-only replay. The evidence ref remains the only permitted
  `update-ref`; a foreign or non-identical collision is immediately blocked.
- All six public modes remain `build-package`, `verify-package`,
  `verify-assignments`, `verify-backfill`, `publish-evidence-ref`, and
  `verify-authorized`. The four always-external consumers require the exact
  three-argument transport group. `verify-authorized` has mutually exclusive
  source groups: either `--bundle PATH`, `--expected-bundle-sha256 HASH`, and
  `--expected-package-sha256 HASH` together, or sole source flag
  `--bundle-from-ref` with neither expected hash. The optional read-only
  `inspect-package` mode is not added because reviewers can consume the
  canonical JSON/base64 bundle directly and no extraction is allowed.
- No old bundle, directory package, package ID, bundle SHA, report, receipt,
  closure, Task candidate, or failed diagnostic may be reused. Attempt 1 and,
  if authorized by the existing terminal prehistory, attempt 2 each receive a
  newly built bundle, controller attestation, two reports/receipts, and two
  closures. Bundle files and unreachable objects remain for controller/normal
  GC disposition; they are not deleted by the helper.

Use these additional stable fail-closed codes while preserving all unaffected
existing state-machine and evidence-schema codes:

| Error                         | Required trigger                                                                                                                                                                                                                  |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PROJECTED_TREE_SCOPE_DRIFT`  | raw tree record, object format/type, ancestor count, sibling identity, `mktree` reread, or initial/projected root binding is invalid                                                                                              |
| `PROJECTED_DELETION_DRIFT`    | retiring subtree cardinality/set or raw/name-status/binary diff is not exact twenty `D` and zero outside path                                                                                                                     |
| `GENERATOR_MANIFEST_REQUIRED` | the three internal environment variables are partial or internal mode is requested outside sole `--stdout`                                                                                                                        |
| `GENERATOR_MANIFEST_INVALID`  | memfd schema, digest, seals, type/nlink, object format/OIDs, count, NUL termination, or path tuple is malformed                                                                                                                   |
| `GENERATOR_MANIFEST_OVERSIZE` | memfd bytes exceed 8 MiB or declared and observed size differ                                                                                                                                                                     |
| `GENERATOR_MANIFEST_OFFSET`   | the inherited memfd is not positioned at offset zero before its single read                                                                                                                                                       |
| `BUNDLE_CREATE_FAILURE`       | literal `/tmp` open, random direct-child validation/collision budget, complete write, fsync/chmod, same-FD readback, parent fsync, or the final post-fsync paired FD/direct-child validation fails before its linearization point |
| `BUNDLE_READ_FAILURE`         | a supplied bundle is outside literal `/tmp`, not an exclusive `0444` regular file, changes during the one bounded transport-first read, or cannot reach exact EOF                                                                 |
| `BUNDLE_SIZE_DRIFT`           | a bundle is empty, exceeds 32 MiB, or its declared and observed byte count differs                                                                                                                                                |
| `BUNDLE_SCHEMA_DRIFT`         | outer keys, path set/order, logical mode, base64, inner schema, checksums, byte counts, or package ID differ                                                                                                                      |
| `BUNDLE_TRANSPORT_DRIFT`      | observed external canonical bytes/path/bundle hash/package hash differ from the controller-captured expected arguments, or the reconstructed tuple differs across attestation, receipt, closure, evidence, bundle, or ref replay  |
| `CONTROL_FILE_DRIFT`          | an attestation/report/receipt/closure/terminal/drift input is not a stable regular nlink-one file, exceeds 4 MiB, changes during its one read, or is reopened                                                                     |
| `STALE_REF_LOCK`              | a `<canonical-leaf>.lock` sibling of any byte size is observed at an admitted evidence-leaf path inside the fixed namespace; the gate stops here with exit 1 and mutates nothing, and makes no claim about which process left it  |

Implement in these TDD slices; every RED must fail for the missing Step 0e
contract, not fixture setup or a repository mutation:

1. **RED A — forbid every scratch/index/directory path and pin raw tree behavior.**
   Add `test_helper_has_no_scratch_index_directory_or_forbidden_git_verbs`,
   `test_projected_tree_removes_exact_subtree_and_preserves_raw_siblings`,
   `test_projected_tree_rejects_malformed_nul_paths_types_and_object_width`,
   and
   `test_tree_diff_is_exact_under_hostile_config_and_initial_tree_attributes`.
   The static regression scans every helper call site, not just the former
   projector. The tree fixtures include tabs/newlines in safe sibling names,
   malformed/nonterminated records, prefix collisions, wrong tree/blob modes,
   sibling substitution, SHA-width drift, hostile diff/textconv config, and
   initial versus projected `.gitattributes` disagreement.
2. **GREEN A — land raw tree projection and the generic trie.** Replace
   projection, manifests, Task patches/transitions, and evidence-tree writing.
   Add `test_task_patches_and_evidence_tree_use_one_in_memory_trie` and require
   both Task patch byte identities plus evidence leaf modes/tree OIDs to match
   their reviewed semantics without an index or directory.
3. **RED/GREEN B — seal one manifest per generator.** Add
   `test_internal_manifest_mode_is_byte_exact_for_both_generators` and
   `test_internal_manifest_rejects_partial_malformed_unsealed_wrong_type_oversize_and_offset`.
   Cover missing/extra variables, pipe/directory FD, writable or partially
   sealed memfd, size/digest/schema/OID/count/path drift, duplicate/unsorted/
   unsafe/non-UTF-8 paths, nonzero offset, and reuse of one FD for both
   generators. Public no-argument/`--check`/`--stdout` bytes and inode/mode
   no-write assertions must remain unchanged.
4. **RED/GREEN C — create and consume one atomic bundle.** Add
   `test_bundle_build_is_atomic_read_only_canonical_and_collision_safe`,
   `test_bundle_build_rejects_symlink_collision_traversal_and_partial_write_without_receipt`,
   and `test_bundle_verification_reads_once_without_extraction`. Inject exact
   random-name collisions, a symlink collision, a traversal token, short and
   midstream writes, fsync/chmod/readback drift, oversize input, base64/path/
   mode/order/checksum drift, and an attempted second read. Require no success
   receipt and no overwritten or removed victim on every failure.
5. **RED/GREEN D — replay all authority from mappings.** Add
   `test_every_public_mode_freshly_replays_tree_and_memfd_projection`,
   `test_full_ref_only_replay_uses_in_memory_package_attachments`, and
   `test_all_public_modes_preserve_repository_and_lifecycle_invariants`.
   Add `test_bundle_binds_twenty_one_file_pack_and_thirty_six_requirements` so
   the current new-pack authority is exactly 21 regular files/20 leaves and
   REQ-01 through REQ-36, while the retiring projection remains exactly 20
   deletions.
   Exercise all six modes, both authorization sources, both attempt-authority
   sources, malicious historical generators, canonically resealed bundles,
   package/ref parent drift, and external control-file substitution. Except
   for the one expected create-only evidence ref in publication fixtures,
   require no branch/index/worktree/ref/generated/old-pack/lifecycle drift.

Run the exact new named methods first, then the complete two classes:

```bash
python3 -m unittest \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_helper_has_no_scratch_index_directory_or_forbidden_git_verbs \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projected_tree_removes_exact_subtree_and_preserves_raw_siblings \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_projected_tree_rejects_malformed_nul_paths_types_and_object_width \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_tree_diff_is_exact_under_hostile_config_and_initial_tree_attributes \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_task_patches_and_evidence_tree_use_one_in_memory_trie \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_internal_manifest_mode_is_byte_exact_for_both_generators \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest.test_internal_manifest_rejects_partial_malformed_unsealed_wrong_type_oversize_and_offset \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_bundle_build_is_atomic_read_only_canonical_and_collision_safe \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_bundle_build_rejects_symlink_collision_traversal_and_partial_write_without_receipt \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_bundle_verification_reads_once_without_extraction \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_every_public_mode_freshly_replays_tree_and_memfd_projection \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_full_ref_only_replay_uses_in_memory_package_attachments \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_bundle_binds_twenty_one_file_pack_and_thirty_six_requirements \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests.test_all_public_modes_preserve_repository_and_lifecycle_invariants \
  -v
python3 -m unittest \
  tests.validation.test_agentic_research_gate9_evidence.AgenticResearchGate9EvidenceTests \
  tests.validation.test_llm_wiki_retiring_pack_exclusion.LlmWikiRetiringPackExclusionTest \
  -v
```

Then require public generator parity, static checks, metadata, and exact scope:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh --stdout | \
  cmp - docs/90.references/llm-wiki/llm-wiki-index.md
bash scripts/knowledge/generate-llm-wiki-coverage.sh --stdout | \
  cmp - docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 -m py_compile \
  scripts/validation/agentic-research-gate9-evidence.py \
  tests/validation/test_agentic_research_gate9_evidence.py \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py
ruff check \
  scripts/validation/agentic-research-gate9-evidence.py \
  tests/validation/test_agentic_research_gate9_evidence.py \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py
bash -n scripts/knowledge/generate-llm-wiki-index.sh \
  scripts/knowledge/generate-llm-wiki-coverage.sh
shellcheck scripts/knowledge/generate-llm-wiki-index.sh \
  scripts/knowledge/generate-llm-wiki-coverage.sh
if rg -n \
  'PinnedScratch|ScratchOwnership|GIT_INDEX_FILE|read-tree|update-index|write-tree|TemporaryDirectory|mkdtemp|mkdir|rmdir|unlink|rmtree|worktree (add|remove|prune)' \
  scripts/validation/agentic-research-gate9-evidence.py; then exit 1; fi
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref 35318255 \
  --changed-path \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --check
```

The Task metadata result must be `selected=1 violations=0`. Recheck that both
generated-output diffs and all four lifecycle-artifact diffs are empty; the
old pack is exactly 20/20 and the new pack exactly 21/21 at live `HEAD` and in
the real index; the Task is 36/36; the real index has no staged change; branch
`HEAD`, registered worktree state, and the Gate 9 ref namespace are unchanged;
and the implementation range contains exactly the six files above.

Stage exactly the six implementation files and commit with the exact subject:

```bash
git add \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  scripts/validation/agentic-research-gate9-evidence.py \
  tests/validation/test_agentic_research_gate9_evidence.py \
  scripts/knowledge/generate-llm-wiki-index.sh \
  scripts/knowledge/generate-llm-wiki-coverage.sh \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py
git diff --cached --name-only
git diff --cached --check
git commit -m "fix(validation): replace gate 9 scratch with tree objects"
```

Package the exact
prerequisite-closure `BASE..HEAD` implementation range and dispatch fresh
independent specification and Python/security reviews. Fix findings only
through the new five-round loop, rerunning the covering RED/GREEN slice, full
two-class suite, static/parity checks, and invariants before each re-review.

After both implementation reviews are C0/I0/M0, make one Task-only closure
commit with subject `docs(task): close gate 9 tree object recovery`. It records
the exact final implementation commit/range, commands, results, append-only
object boundary, retained-bundle disposition, unchanged repository/lifecycle
invariants, both verdicts, and the new `GATE9_REVIEWED_CODE_HEAD`; it does not
create or consume a Gate 9 bundle. Obtain two final fresh closure-integrity
reviews, specification and Python/security, over the exact Step 0e
prerequisite base through that Task-only closure `HEAD`. Both must be C0/I0/M0.
That reviewed closure OID becomes `GATE9_LIVE_REVIEWED_HEAD`. Only then rerun a
fresh Phase A gates 1 through 8; no Step 0d gate result, package, receipt, hash,
or bundle may be carried forward.

- [ ] **Step 1: Execute Phase A pre-deletion gates 1 through 8**

Confirm in the Task: 20/20 old files pinned; every unique claim mapped; every
retain/correct destination reviewed; every omission reasoned; 21/21 new-pack
files, 20/20 new leaves, 36/36 requirements; 14/14 scopes; C0/I0/M0; zero clickable old references; reviewed
non-link allowlist; metadata/traceability PASS; LLM index/coverage PASS;
alignment delta 0; repository contracts PASS. A missing dependency stops here.

- [ ] **Step 2: Record the recoverability boundary**

Record the current commit, old tree listing, and all old blob IDs. Verify before
staging deletion that these exact commands recover representative files
without changing the worktree:

```bash
git show HEAD:docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md >/dev/null
git show HEAD:docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md >/dev/null
```

- [ ] **Step 3: Build a non-destructive proposed-deletion package**

Do not change the target-surface manifest or either lifecycle summary before
the deletion commit exists. A valid destructive row requires the source to be
physically absent and its rollback command to name the real, already existing
deletion commit, so pre-populating those rows would be false evidence.

The helper, not the caller, derives the next ordinal by enumerating the exact
Gate 9 evidence-ref prefix and validating every existing ref. Attempt 1 is
required when no terminal ref exists. Attempt 2 is allowed only when one valid
attempt 1 ref records pre-backfill `REJECTED` or `INVALIDATED` and the Task is
`ATTEMPT_2_PENDING` with the same identity. No third ordinal exists. The
`--attempt` argument asserts that derived value; it does not authorize attempt
selection or reuse. The helper must use the Step 0e reviewed pathless root-tree
projection, a fresh sealed manifest for each generator, and in-memory
attachment replay. It may append only the named content-addressed Git objects;
it performs no object cleanup or GC/prune. It leaves the current worktree,
real index, registered worktree state, old pack, and generated outputs
unchanged. Build and verify with the exact interface:

```bash
GATE9_HELPER=scripts/validation/agentic-research-gate9-evidence.py
GATE9_LIVE_REVIEWED_HEAD=$(GIT_NO_REPLACE_OBJECTS=1 git rev-parse --verify HEAD)
: "${GATE9_REVIEWED_CODE_HEAD:?set this to the full Step 0e code OID recorded in the Task}"
GATE9_BUILD_RECEIPT=$(python3 "$GATE9_HELPER" build-package \
  --attempt 1 \
  --spec docs/03.specs/137-agentic-research-pack-rebuild/spec.md \
  --plan docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD")
GATE9_BUNDLE=$(printf '%s\n' "$GATE9_BUILD_RECEIPT" | \
  python3 -c 'import json,sys; print(json.load(sys.stdin)["bundle_path"])')
GATE9_BUNDLE_SHA256=$(printf '%s\n' "$GATE9_BUILD_RECEIPT" | \
  python3 -c 'import json,sys; print(json.load(sys.stdin)["bundle_sha256"])')
GATE9_PACKAGE_SHA256=$(printf '%s\n' "$GATE9_BUILD_RECEIPT" | \
  python3 -c 'import json,sys; print(json.load(sys.stdin)["package_sha256"])')
python3 "$GATE9_HELPER" verify-package \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

The controller sets `GATE9_REVIEWED_CODE_HEAD` from the exact full OID already
recorded and independently reviewed in the Task; the shell guard rejects an
unset value. The Task must record it as the final Step 0e
implementation commit and its two C0/I0/M0 implementation reviews. The two
external closure-integrity receipts bind `GATE9_LIVE_REVIEWED_HEAD` to the
subsequent Task-only closure commit without inserting that commit's identity
back into itself. The helper rejects any code OID that does not equal the
Task-recorded value, and the controller must supply the closure OID from both
matching receipts; the live-HEAD shell derivation is convenience, not
authority.

`build-package` must fail unless the real index is clean, `HEAD` is the
committed reviewed evidence-contract checkpoint, the old and new packs are
exactly 20 and 21 files respectively, the Task is 36/36, the Task has exactly
one pending marker, and the only worktree change is that Task. It must encode
this exact sorted logical attachment set in one atomic bundle:

```text
HEAD.txt
SHA256SUMS
assignments.json
gate-results.json
llm-wiki-index.md
llm-wiki-stage-category-coverage.md
new-manifest.tsv
old-manifest.tsv
package.json
plan.md
proposed-deletion.patch
spec.md
task-before.md
task-before-to-candidate.patch
task-candidate.md
```

`old-manifest.tsv` has exactly 20 rows and `new-manifest.tsv` exactly 21;
both are byte-sorted
`mode<TAB>type<TAB>object<TAB>path` rows from the package `HEAD`.
`proposed-deletion.patch` is binary-safe and contains exactly twenty `D`
paths and twenty deleted-file modes under the retiring prefix, with no other
status. The two generated attachments come from the pathless projected tree
through separate sealed manifests and must be byte-identical to the tracked
Task 9a/Task 10 outputs at the 1,339-index-row/1,338-coverage-path baseline.
`gate-results.json`
records gates 1 through 8 and their pinned predecessor classifications.
`assignments.json` contains exactly the `migration-specification` and `quality`
roles. Each has a deterministic attempt-local run ID derived from the package
`HEAD`, attempt number, and role; the later receipt must add the immutable
agent ID and canonical task path returned by the subagent runtime.

All inner JSON uses schema `agentic-research-gate9/v1`, UTF-8, LF, recursively
sorted keys, compact separators, and one final newline. `package.json` lists
the other payload attachments in byte-sorted path order with their SHA-256 and
byte count. `SHA256SUMS` is a byte-sorted GNU-format checksum list over every
attachment except itself. The SHA-256 of the exact `SHA256SUMS` bytes is the
package ID. The outer canonical `agentic-research-gate9-bundle/v1` JSON/base64
transport binds that logical package ID, all fifteen attachment bytes/modes,
and `bundle_sha256`. `build-package` returns only the canonical
`agentic-research-gate9-build-receipt/v1` receipt with the `/tmp` direct-child
path plus both hashes after same-descriptor fsync/chmod/readback succeeds. The
bundle stays `0444`, is never extracted, and is retained for controller
disposition. Any later bundle/package byte, mode, path-set, `HEAD`, Task,
generated-output, manifest, or lifecycle drift sets the attempt to
`INVALIDATED`.

- [ ] **Step 4: Satisfy pre-deletion gate 9**

The finite state sequence is:

```text
CHECKPOINT -> BUILT -> ASSIGNED -> PACKAGE_REVIEWED -> TASK_BACKFILLED
                       -> CLOSURE_REVIEWED -> REF_PUBLISHED -> AUTHORIZED
```

`REJECTED`, `INVALIDATED`, `FOREIGN_REF`, `STALE_REF_LOCK`, and `BLOCKED` are
fail-closed states, and every one of them is terminal. `STALE_REF_LOCK` names
an observed `<canonical-leaf>.lock` sibling of any byte size inside the fixed
evidence namespace. Its transition is the same as every other fail-closed
member: whatever state the run had reached moves to this terminal state and
the sequence ends there, with exit 1 — the status every fail-closed code other
than `LIVE_HEAD_REQUIRED` uses — and stderr-only diagnostics. It is not a
recoverable member and has no recovery edge back into
`CHECKPOINT -> BUILT -> ...`. The gate clears no lock and mutates nothing;
removal is an operator action outside the gate, after which a fresh run starts
from the beginning under the ordinary rules. A `.lock` whose leaf name is not
an admitted canonical leaf name is not this state and fails closed as
`FOREIGN_REF`. A package becomes a consumed attempt only at `ASSIGNED`, after
the trusted controller attestation is frozen. A build that fails or drifts before
`ASSIGNED` is discarded as an unassigned construction failure and cannot
produce review authority; its bundle remains retained but has no authority.
Except for an untrusted `FOREIGN_REF` collision and a `STALE_REF_LOCK`
residue, both of which the pre-publication namespace snapshot raises before any
ref can be written, every consumed attempt, accepted or not, must end in a
create-only evidence ref. The same strict snapshot is reused for the after
repository-invariant capture, which in publish mode runs after publication, so
a residue first observed there is diagnosed once a ref already exists; the
invariant still holds on that path. A
pre-backfill rejection stores the complete logical package attachments and all
available reports/receipts plus a canonical terminal reason; a drift
invalidation stores those attachments, drift evidence, and canonical terminal
reason. The external bundle is retained transport, not durable attempt
authority; the helper derives the next ordinal only from validated durable
refs.

Dispatch one fresh migration/specification reviewer and one fresh quality
reviewer. Capture each spawn result before accepting a review. The trusted
controller writes one canonical `assignment-attestation.json` containing the
package ID, bundle SHA-256, package `HEAD`, attempt, source literal
`collaboration.spawn_agent/result`, controller task `/root`, and exactly two
role records with the immutable agent ID and canonical task path returned by
the runtime plus the assigned attempt-local run ID. The two agent IDs and task
paths must differ. Hash and freeze the attestation before sending the final
review package; both reviewers must echo its SHA-256. This attestation is the
explicit trust boundary: Git makes the captured bytes tamper-evident, while
the controller's observed spawn result—not self-asserted receipt text—binds
the role to the runtime identity.

```bash
python3 "$GATE9_HELPER" verify-assignments \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --attestation "$GATE9_ASSIGNMENT_ATTESTATION" \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

Each reviewer returns one exact UTF-8/LF
report plus one canonical JSON package receipt with the package ID, bundle
SHA-256, and `HEAD`,
role, all three identity fields, verdict, C/I/M counts, and SHA-256/byte count
of that exact report and the assignment-attestation hash. Both receipts must
bind the same package and controller attestation, and neither may contain a
Critical or Important finding. If either review rejects the package, allow the
other independent review to finish so the `REJECTED` terminal tree contains
both exact report/receipt pairs; do not infer or fabricate the missing slot.

Verify the receipts before changing the Task:

```bash
python3 "$GATE9_HELPER" verify-backfill \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --migration-receipt "$GATE9_MIGRATION_RECEIPT" \
  --quality-receipt "$GATE9_QUALITY_RECEIPT" \
  --assignment-attestation "$GATE9_ASSIGNMENT_ATTESTATION" \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --expect-state PACKAGE_REVIEWED \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

Then transition the Task marker exactly once from `PACKAGE_REVIEW_PENDING` to
`TASK_BACKFILLED`. Its before bytes are `task-candidate.md`; its after bytes
must differ only inside that marker. The marker records the 20-file retiring
and 21-file canonical manifest identities, proposed patch hash, recovery
`HEAD`, package ID, bundle SHA-256, fixed evidence ref, both receipt
identities/hashes/verdicts, and actual staged
and committed deletion reviews as `Not Run`. The helper computes the binary
Task diff, before/after Git blob OIDs, SHA-256 values, and byte counts. Any
other Task edit rejects the attempt.

```bash
python3 "$GATE9_HELPER" verify-backfill \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --migration-receipt "$GATE9_MIGRATION_RECEIPT" \
  --quality-receipt "$GATE9_QUALITY_RECEIPT" \
  --assignment-attestation "$GATE9_ASSIGNMENT_ATTESTATION" \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --expect-state TASK_BACKFILLED \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

The same two reviewers then receive the immutable bundle exactly once, both
reports and receipts, and the exact Task before/after/diff tuple. Each returns one exact
UTF-8/LF closure report plus one canonical closure JSON binding their own
package receipt and identity to that tuple and to the closure report's
SHA-256/byte count and the same assignment-attestation hash. Both closures
must be C0/I0 and must state that the marker matches the receipt while all
non-marker bytes are unchanged. Closure hashes are deliberately not inserted
back into the Task.

Publish all evidence under this create-only local ref:

```text
refs/codex/review-evidence/agentic-research/gate9/v1/
  attempt-N/<package-sha256>
```

The evidence commit uses the package `HEAD` as its sole parent. Every terminal
state uses one closed path schema: the exact package attachment set below
`package/`, plus these literal paths and no others:

```text
SHA256SUMS
assignment-attestation.json
closures/migration-specification/closure.json
closures/migration-specification/report.md
closures/quality/closure.json
closures/quality/report.md
drift/drift-proof.json
evidence.json
reviews/migration-specification/receipt.json
reviews/migration-specification/report.md
reviews/quality/receipt.json
reviews/quality/report.md
task/task-after.md
task/task-candidate-to-after.patch
terminal/report.md
```

All leaf entries use mode `100644`; Git directory-tree entries use mode
`040000`. A state that has not reached a review, closure, backfill, or drift
slot uses the exact sentinel report bytes `NOT_RUN\n` and a canonical JSON
object with schema `agentic-research-gate9/v1`, its kind and role, and state
`NOT_RUN`. Before backfill, `task/task-after.md` equals
`package/task-candidate.md` and the candidate-to-after patch is zero bytes.
When drift is not the terminal cause, `drift-proof.json` is the canonical
`NOT_APPLICABLE` object. `REJECTED` requires both completed package-review
pairs; `INVALIDATED` requires the drift proof and retains any already completed
review pair; `AUTHORIZED` requires both review pairs, both closure pairs, and
the exact closure-reviewed Task-after and binary diff bytes.

`evidence.json` has exactly these top-level keys: `schema`, `state`, `attempt`,
`package_head`, `package_sha256`, `bundle_sha256`, `evidence_ref`, `assignment`, `task`,
`reviews`, `closures`, `drift`, and `terminal_report`. Every referenced file
record includes literal path, SHA-256, and byte count; identity-bearing review
records also include role, agent ID, task path, run ID, attestation hash,
verdict, and C/I/M counts. Root `SHA256SUMS` excludes itself and contains one
GNU-format `<64 lowercase hex><two spaces><path><LF>` row for every other leaf
file, byte-sorted by path. Ref replay reads every leaf once into a
`Mapping[path, bytes]`, validates those checksum bytes in memory, and never
extracts an evidence root.

Evidence publication identity is the tuple `(package HEAD, canonical evidence
tree OID, canonical commit message)`, not the commit OID. The exact commit
message is `agentic-research-gate9-evidence/v1`, a blank line, then
byte-sorted `attempt`, `package-sha256`, and `state` lines with one final LF.
Author/committer timestamps therefore cannot make an identical retry appear
foreign. On a create-only race or any nonzero `update-ref`, reread the existing
ref: identical parent, tree, and message is idempotent success; any difference
is `FOREIGN_REF`. Tests must cover first publication, identical retry,
non-identical collision, and concurrent create-race recovery without changing
the branch, real index, or worktree and without materializing an evidence
directory.

Publish only with
`git update-ref <ref> <evidence-commit> 0000000000000000000000000000000000000000`.
An absent ref may be created once; an existing byte-identical ref is an
idempotent success; any other existing value is `FOREIGN_REF` and stops. The
ref is local, append-free review evidence: it does not advance the branch or
real index, must remain reachable through Task 12 and branch handoff, and must
not be pushed without a separate user decision.

```bash
python3 "$GATE9_HELPER" publish-evidence-ref \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --terminal-state AUTHORIZED \
  --terminal-report "$GATE9_TERMINAL_REPORT" \
  --migration-report "$GATE9_MIGRATION_REPORT" \
  --migration-receipt "$GATE9_MIGRATION_RECEIPT" \
  --quality-report "$GATE9_QUALITY_REPORT" \
  --quality-receipt "$GATE9_QUALITY_RECEIPT" \
  --assignment-attestation "$GATE9_ASSIGNMENT_ATTESTATION" \
  --migration-closure-report "$GATE9_MIGRATION_CLOSURE_REPORT" \
  --migration-closure "$GATE9_MIGRATION_CLOSURE" \
  --quality-closure-report "$GATE9_QUALITY_CLOSURE_REPORT" \
  --quality-closure "$GATE9_QUALITY_CLOSURE" \
  --evidence-ref auto \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

Run the terminal check immediately after publication and again immediately
before `git rm`:

```bash
python3 "$GATE9_HELPER" verify-authorized \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --evidence-ref auto \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD" \
  --require-clean-real-index \
  --require-task-only-worktree
python3 "$GATE9_HELPER" verify-authorized \
  --bundle-from-ref \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --evidence-ref auto \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD" \
  --require-clean-real-index \
  --require-task-only-worktree
```

`verify-authorized` must first prove current live `HEAD ==` supplied live
reviewed `HEAD == bundle package HEAD == evidence-ref parent`, plus the exact
reviewed helper/generator code binding, then prove bundle/package/evidence
attachment sets, both hashes, checksums, canonical schemas, distinct role/identity bindings,
receipt-to-closure identity, exact
Task before/after/diff and marker transition, C/I=0, exact twenty-file
projection, byte-identical generated attachments, and no current-worktree or
real-index drift outside the exact closure-bound Task-only change. Only then is
Gate 9 `AUTHORIZED`.

The focused suite closes every external fixture descriptor after publication,
hides those inputs from replay, and reproduces the same authorization result
from only the live `HEAD`, live Task, and evidence ref by reconstructing the
canonical bundle bytes from in-memory attachment mappings. The real run
repeats this ref-only form immediately before `git rm`. The retained `/tmp`
bundle is transport evidence under controller disposition and never durable
authority.

Before backfill, any package-review C/I finding or byte drift consumes the
attempt and requires `publish-evidence-ref --terminal-state REJECTED` or
`INVALIDATED`; there is no object or bundle cleanup. Attempt 1 may then transition the Task
marker to `ATTEMPT_2_PENDING`; the helper requires the matching durable ref and
derives ordinal 2. Attempt 2 uses a newly built atomic bundle and new logical
package ID, new controller attestation,
and fresh reviewer report/receipt bytes and may not overwrite attempt 1.

```bash
python3 "$GATE9_HELPER" publish-evidence-ref \
  --bundle "$GATE9_BUNDLE" \
  --expected-bundle-sha256 "$GATE9_BUNDLE_SHA256" \
  --expected-package-sha256 "$GATE9_PACKAGE_SHA256" \
  --task docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  --terminal-state "$GATE9_TERMINAL_STATE" \
  --terminal-report "$GATE9_TERMINAL_REPORT" \
  --assignment-attestation "$GATE9_ASSIGNMENT_ATTESTATION" \
  --evidence-ref auto \
  --require-live-head \
  --live-reviewed-head "$GATE9_LIVE_REVIEWED_HEAD" \
  --reviewed-code-head "$GATE9_REVIEWED_CODE_HEAD"
```

For `REJECTED`, append both completed `--role-report`/`--role-receipt` pairs;
for `INVALIDATED`, append `--drift-proof`. Because a consumed attempt begins
only at `ASSIGNED`, the attestation is mandatory for every terminal ref. The
helper fills all state-inapplicable fixed slots with their canonical sentinels
and rejects an incomplete or extra path.

After `TASK_BACKFILLED`, any identity collision, closure C/I finding,
publication conflict, `HEAD` change, Task drift, or authorization failure is
immediately `BLOCKED`; marker rollback and attempt 2 are forbidden. Any
attempt 2 failure is also `BLOCKED`. A `FOREIGN_REF` is always immediately
`BLOCKED` because the namespace cannot be trusted. Resuming a blocked state
requires explicit user approval and a newly reviewed Plan boundary, not a
third attempt. Keep the old pack and real index intact, preserve the terminal
ref or foreign-ref observation in the controller report, do not mutate a
backfilled Task, and retain every produced bundle for explicit controller
disposition. Leave appended unreachable objects to ordinary Git garbage
collection; the helper must not unlink a bundle or invoke object cleanup, GC,
or prune.

- [ ] **Step 5: Delete the old files in the real index**

Use `git rm` with the exact directory only after all nine gates pass:

```bash
git rm -r docs/90.references/research/2026-07-05-agentic-research-pack-refresh
```

- [ ] **Step 6: Run staged-deletion checks before committing**

Regenerate both path-derived artifacts after the staged deletion removes the
old paths from the Git index. Because Task 10 already excludes that exact
retiring prefix, both outputs must remain byte-identical; any diff is a blocker.
Then require byte-exact freshness:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
git diff -- docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

Then repeat the old-slug inventory, Markdown/link contracts, metadata,
traceability, document alignment delta, repository contracts,
requirement/scope/claim audit, and diff hygiene. The target-surface lifecycle
files remain unchanged in this deletion commit; classify their temporary
post-delete missing-target findings as the exact input to Step 10, not as a
PASS. Any other regression restores the directory from the parent commit and
stops the task.

- [ ] **Step 7: Review the actual staged deletion**

Keep the Task evidence unstaged, confirm the two generated outputs have no
diff, create one exclusive staged-review patch file directly under `/tmp`, and
write the actual cached diff to it; do not reuse or mutate the authorized Gate
9 bundle. Then
dispatch two fresh, independent staged-diff reviewers over that same immutable
patch: one owns migration/specification compliance and one owns quality.
Require both separate verdicts at C0/I0. If evidence changes, rebuild the patch
and rerun both. Supply the current unstaged Task evidence as a separate
immutable review input, but
require the immutable patch itself to contain exactly the twenty deletions.
This verifies the real index before a commit exists.

```bash
STAGED_DELETION_REVIEW_PATCH=$(mktemp \
  /tmp/agentic-research-staged-deletion-review.XXXXXX.patch)
git diff --quiet -- \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
git diff --cached --binary \
  > "$STAGED_DELETION_REVIEW_PATCH"
chmod 0444 "$STAGED_DELETION_REVIEW_PATCH"
```

- [ ] **Step 8: Self-review and commit the deletion unit**

Verify the exact staged set and deletion/generator diff, then:

```bash
git commit -m "docs(research): retire superseded agentic research pack"
```

The `git rm` entries are already staged; confirm the staged set is exactly the
twenty deletions. The Task, lifecycle manifests/summaries, tests, and two LLM
Wiki artifacts must not appear in the staged set. This commit creates the real
immutable rollback SHA required by the following evidence unit.

- [ ] **Step 9: Review the committed deletion unit**

Run the committed-unit SDD protocol for Task 11. Require two fresh independent
reviewers over the exact deletion commit range and record separate
migration/specification and quality verdicts. If a load-bearing route or claim
was lost, restore it in an implementer fix commit and complete both scoped
re-reviews before lifecycle reconciliation.

- [ ] **Step 10: Build the post-deletion lifecycle evidence package**

Use the actual deletion commit SHA; do not predict or self-reference it. First
add focused RED assertions to the existing target-surface delta and lifecycle
test modules for these exact facts:

- the advisory delta manifest lacks exactly the three root-predecessor scripts
  plus the two Task 10b LLM Wiki generators and its focused test;
- the seven retiring-pack target rows and the already-archived Spec 133 source
  row have not yet converged to delete results;
- the six new delta rows are all `update`, raising the exact repository
  invariants from 158 entries / 85 preserve / 73 update to
  164 entries / 85 preserve / 79 update, with the exact update-path set;
- the final target-surface counts are eleven `delete`, ten `migrate`, and 462
  `preserve` rows; and
- the generated summaries contain the exact reviewed rows and canonical
  counts.

Run this exact focused command and record the intended RED before changing
production data:

```bash
python3 -m unittest \
  tests.validation.test_target_surface_delta_contracts.RepositoryManifestTests.test_repository_manifest_has_fixed_baselines_and_truthful_owners \
  tests.validation.test_target_surface_contracts.DeprecatedRuntimeContractTests.test_agentic_research_retirement_rows_record_exact_delete_evidence \
  -v
```

Then add the exact six missing advisory-delta rows as `update` with bounded
consumers and review evidence. Use each path's real latest source-changing
commit for provenance and rollback: Task 10b only for its two LLM Wiki
generators and focused test,
`a8d56a7ad99deabe37b4baad498fa64afe43a225` for
`scripts/validation/check-storybook-contract.sh`, and
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a` for both
`scripts/validation/generate-audit-implementation-matrix.sh` and
`scripts/validation/report-provider-hook-parity.sh`. Do not rely on the
validator's weaker commit-exists check as proof that a commit changed a path.
Run the advisory checker, then regenerate its summary only after the manifest
has no finding other than stale summary bytes:

```bash
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory --write-summary
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
```

The first command must exit 1 with exactly `delta-summary-stale`; any other
finding blocks generation. The `--write-summary` command must exit 0, and the
final advisory command must exit 0 quietly with canonical summary bytes.

Next draft exactly eight target-surface delete rows: the seven retiring paths
and `docs/03.specs/133-target-surface-contract-convergence/spec.md`. Preserve
each baseline `source_path`, `artifact_id`, `artifact_type_before`,
`status_before`, `status_after`, and `parent_ids`; set `target_path: null`,
`artifact_type_after: null`, `disposition: delete`,
`canonical_replacement: null`, and `preservation_class: git-history`. The
seven retiring rows use the actual deletion commit in their commands and
`git revert --no-commit` rollback. The Spec 133 row uses its actual historical
archive/deletion commit
`d8e0c659035f1085d314812470e6f9290958bcbf`. Every row has non-empty bounded
commands, sources, repository paths, zero-consumer scan, rollback, and starts
with external review evidence not yet encoded as `pass`.

Dispatch one migration/specification reviewer and one quality reviewer over
the draft rows, six delta rows, tests, immutable commit evidence, and expected
summary projection. Only after both return C0/I0 may the eight destructive
rows encode `pass/pass`. Regenerate the target summary with its required
explicit output and run the exact lifecycle checks:

```bash
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-manifest --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode generate-summary --wave target-surface-convergence \
  --output docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-summary --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-promoted
```

Expected: the target-surface manifest and summary commands PASS; the advisory
delta command and its canonical summary freshness PASS; and `check-promoted`
reports exactly sixteen root-predecessor Foundation findings plus the one
recorded Task 10 Foundation consumer finding for the Task index, not a
target-surface finding. Require the focused test and Task ledger to assert that
exact identity set rather than count alone. Rerun both independent reviewers
if any encoded verdict, evidence, manifest, summary, or test byte changes.

- [ ] **Step 11: Commit and review the lifecycle evidence unit**

Run the focused command above and the exact full affected modules, then run
metadata/traceability, repository contracts, both LLM Wiki freshness checks,
old-slug allowlist scan, and diff hygiene:

```bash
python3 -m unittest \
  tests.validation.test_target_surface_delta_contracts \
  tests.validation.test_target_surface_contracts -v
```

Stage exactly the two delta artifacts, two convergence artifacts, two test
files, and the Task:

```bash
git add \
  docs/90.references/data/governance/target-surface-delta-manifest.yaml \
  docs/90.references/data/governance/target-surface-delta-summary.md \
  docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml \
  docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md \
  tests/validation/test_target_surface_delta_contracts.py \
  tests/validation/test_target_surface_contracts.py \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git commit -m "docs(governance): record agentic pack retirement lifecycle"
```

Run the committed-unit SDD protocol with two fresh reviewers over this exact
commit range. Resolve every Critical or Important finding and rerun affected
checks before Task 12.

### Task 12: Close evidence and run the finishing workflow

**Files:**

- Modify: execution Task
- Modify: `docs/00.agent-governance/memory/current.md`

**Interfaces:**

- Consumes: REQ-35, exact base-to-head range, all logical commits, final tree,
  and final review results.
- Produces: honest closure evidence and user-facing branch choices.

- [ ] **Step 1: Run the pre-closure verification ladder**

Run changed metadata against the branch base
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a`, traceability, implementation
alignment, repository contracts, both LLM freshness checks, the target-surface
delta and convergence manifest/summary checks, old-slug inventory, complete
requirement/scope/claim audit, `git diff --check`, and exact base-to-head file
review. Record commands, exit codes, and attributable predecessors without raw
logs or secrets.

- [ ] **Step 2: Run pre-closure whole-branch reviews**

Dispatch fresh specification and quality reviewers over
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD`. Resolve every Critical and
Important finding through the SDD final fix wave, rerun affected checks, and
obtain a fresh verdict for the new exact range.

- [ ] **Step 3: Prepare closure evidence without claiming completion**

Set all actual task rows, verification results, and pre-closure review
verdicts. Keep Task status `active`. Update current memory with the canonical
new route, exact review-pending state, remaining predecessor defects, and next
action; do not copy command output.

- [ ] **Step 4: Commit the closure candidate**

```bash
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  docs/00.agent-governance/memory/current.md
git commit -m "docs(task): prepare agentic research rebuild closure"
```

This preparation commit and the later completed-status commit are the two
atomic commits needed to realize Spec 137's nominal final closure boundary: a
review must observe a committed closure candidate, while the completion state
itself must also be included in the final exact-range review. They are one
logical closure unit but cannot be collapsed without making the final verdict
exclude either the candidate evidence or the completed-status transition.

- [ ] **Step 5: Verify and review the closure candidate**

Repeat the full verification ladder on the committed closure candidate and
dispatch fresh final reviewers over
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD`. If any load-bearing finding
remains, keep the Task active, dispatch the single SDD final fix wave, commit
the fixes, and rerun this step.

- [ ] **Step 6: Commit completed status and reverify the exact final range**

Only after Step 5 passes, record its exact commands/range/verdicts, set the Task
and current memory to `completed`, and commit:

```bash
git add docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md \
  docs/00.agent-governance/memory/current.md
git commit -m "docs(task): close agentic research pack rebuild"
```

Immediately rerun the full verification ladder and two fresh independent
whole-branch reviews over
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD`, which now includes the
completed-status commit. One reviewer owns specification compliance and one
owns quality; both separate verdicts must cover the same exact range. A failure
requires a corrective commit that reopens the Task to `active`, followed by
the same verification/two-reviewer sequence. Do not change tracked files after
the final clean verdict.

- [ ] **Step 7: Use `superpowers:finishing-a-development-branch`**

On the unchanged, final-reviewed HEAD, run its mandatory verification and
present the exact local branch state plus integration choices. If its suite
fails, reopen the Task and return to Step 6. Do not push, open a PR, merge, or
delete the worktree until the user chooses.

## Verification Plan

### Per-unit document checks (Tasks 1 through 11)

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref 35318255
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
```

The metadata checker discovers the complete changed path set against the active
Spec commit for per-unit review. Per-unit invocations may additionally repeat
`--changed-path` with the literal paths owned by that unit, and the Task records
those expanded commands. This `35318255` base is not the Task 12 closure base.

### Exact closure ladder (Task 12 only)

Every “full verification ladder” invocation in Task 12 uses the branch base,
not the active-Spec commit:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed \
  --base-ref 78b60974164ff5427ba8c64aaf3ecde4a7faf41a
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
python3 scripts/validation/check-target-surface-delta-contract.py \
  --mode advisory
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-manifest --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-summary --wave target-surface-convergence
python3 scripts/validation/check-document-corpus-lifecycle.py \
  --mode check-promoted
git grep -n -I '2026-07-05-agentic-research-pack-refresh' -- \
  ':!docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**'
git diff --name-status \
  78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD
git diff --check \
  78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD
git status --short
```

The Task additionally records its deterministic 36-requirement, 14-scope, and
old-claim ledger queries. Reviewers receive the exact binary diff for
`78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD`; any later commit invalidates
both verdicts and requires the entire closure ladder and both reviews again.

### Pack completeness checks

```bash
find docs/90.references/research/2026-08-08-agentic-engineering-research-pack \
  -maxdepth 1 -type f -printf '%f\n' | sort
git grep -n -I '2026-07-05-agentic-research-pack-refresh' -- \
  ':!docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**'
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

Expected before deletion: 21 new files (README plus 20 leaves), zero unreviewed
old-slug occurrences, 1,339 index rows, 1,338 coverage paths, and two generator
PASS results. Expected after deletion: the same byte-identical 21-file new
pack and generated cardinalities, zero clickable old routes, and only reviewed
historical non-link literals.

### Repository checks

```bash
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
env PATH=/tmp/agentic-research-validation-venv/bin:$PATH \
  bash scripts/validation/check-repo-contracts.sh
git diff --check
git status --short
```

Expected: traceability and repository contracts PASS; implementation alignment
has zero attributable delta and no increase over the pinned 184 predecessor;
diff hygiene PASS; status contains only the expected unit while work is in
progress and is clean after each commit.

## Risks and Rollback

| Risk                                                                                                                                 | Control                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Rollback                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Old prose copied with stale facts                                                                                                    | Claim ledger and current-source remeasurement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Revert the affected leaf commit and re-author from the source/evidence rows                                                                                                                                                                                                                                                                                                                                                                         |
| Mutable provider source changes mid-task                                                                                             | Access timestamps and per-unit review                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Reopen source, correct only affected claims, rerun review                                                                                                                                                                                                                                                                                                                                                                                           |
| Unavailable/paywalled source                                                                                                         | `UNVERIFIED` boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Remove unsupported conclusion; retain historical pointer only                                                                                                                                                                                                                                                                                                                                                                                       |
| Scope or requirement omission                                                                                                        | Closed 36-row and 14-row matrices                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Stop pack routing until missing row has a reviewed destination                                                                                                                                                                                                                                                                                                                                                                                      |
| V&V source status or workspace count is copied past its evidence                                                                     | Reopen current official IEEE 1012-2024, ISO/IEC/IEEE 12207:2026, NASA, NIST, and GitHub primary routes; remeasure owner commands; preserve paywall and runtime/remote limits                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Mark the affected claim `UNVERIFIED`, revert the V&V unit if needed, and repeat both independent reviews before Gate 9                                                                                                                                                                                                                                                                                                                              |
| Parent research router retains the pre-amendment leaf count                                                                          | Treat the immutable 17-path `139ced00` commit as historical evidence; require the separately reviewed two-path parent-README/Task fix, exact two-line assertions, and final 18-path unique-scope self-review                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Targeted revert of the two-path fix only; keep `139ced00` unchanged, retain 1,339/1,338 generated bytes, and keep Step 0e and Gate 9 closed until a corrected fix is reviewed                                                                                                                                                                                                                                                                       |
| Broken historical link after deletion                                                                                                | Whole tracked-text scan and zero clickable exceptions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Restore old pack from deletion parent and repair routes                                                                                                                                                                                                                                                                                                                                                                                             |
| Generated coverage remains stale                                                                                                     | Canonical write then byte-exact checks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Revert generated outputs and diagnose generator before deletion                                                                                                                                                                                                                                                                                                                                                                                     |
| Fresh LLM navigation re-emits the retiring pack while both packs coexist                                                             | Focused RED/GREEN exact-prefix test in both LLM Wiki generators; retain new-pack and similarly named Stage 04 paths                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Revert the route-switch unit, keep both packs, and do not enter deletion review                                                                                                                                                                                                                                                                                                                                                                     |
| Mutable metadata exceptions retain paths scheduled for deletion                                                                      | Remove the exact sixteen exceptions; separately preserve and verify the seven commit-pinned baseline selectors and promoted evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Revert the route-switch unit, keep both packs, and restore the reviewed baseline/exception boundary                                                                                                                                                                                                                                                                                                                                                 |
| Deletion makes promoted baseline result targets disappear                                                                            | Commit only the independently reviewed twenty-file deletion first; then use its real SHA to encode seven retiring rows and the historical Spec 133 row as reviewed delete results, close the six-row advisory-delta predecessor, and regenerate both summaries canonically                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Revert the deletion commit if the post-delete lifecycle unit cannot reach target-manifest/summary PASS; otherwise revert only the lifecycle-evidence commit and re-review its bounded package                                                                                                                                                                                                                                                       |
| Security generator false gaps                                                                                                        | Before separate approval, do not regenerate and derive direct tracked evidence; after approval, require focused RED/GREEN tests and canonical write/check                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Before approval, preserve the stale predecessor; after approval, revert the isolated repair commit and keep both packs when tests, generated diff, or review fails                                                                                                                                                                                                                                                                                  |
| Repository contracts cannot load                                                                                                     | Fail-closed deletion gate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Continue non-destructive authoring only; do not delete until environment gate passes                                                                                                                                                                                                                                                                                                                                                                |
| Gate 9 verifier accepts resealed attachments or executes package-controlled/historical shell bytes                                   | Step 0e reviewed Task prerequisite; replace/graft/shallow rejection; exact bundle/live-reviewed-HEAD and reviewed-code binding before shell; fresh pathless raw-tree projection plus a new sealed manifest per generator in every public authority mode; exact twenty-`D` proof; and proved-live-HEAD byte comparison                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Reject before generator-object read/shell, preserve the zero-execution marker and all repository invariants, stop before Phase A, and use only the independently bounded Step 0e five-round recovery loop                                                                                                                                                                                                                                           |
| Gate 9 tree, anonymous-memory manifest, or bundle transport is substituted or malformed                                              | Raw NUL-safe tree validation with sibling preservation and exactly four rebuilt ancestors; required descriptor seals/type/nlink/size/digest/offset checks; explicit final-post-fsync FD/direct-child publication linearization; controller-captured expected bundle/package hashes plus literal path; and transport-first bounded once-read verification in every external-bundle consumer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Reject any pre/during-linearization substitution without a receipt; treat a later namespace mutation as external post-publication drift and reject any canonical but non-identical tuple as `BUNDLE_TRANSPORT_DRIFT` before authority; retain a published bundle, leave unreachable objects to ordinary Git GC, and never invoke helper cleanup, prune, or extraction                                                                               |
| Gate 9 package becomes stale or Task review evidence becomes self-referential                                                        | Canonical JSON/base64 bundle builder, one marker-only backfill, same-reviewer closures, both package and bundle hashes, create-only content-addressed evidence ref, in-memory ref-only replay, and Step 0e implementation/closure C0/I0/M0 reviews                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Invalidate the attempt without staging; preserve the old pack and retained bundle; use the one fresh correction attempt or return to user-approved Plan work                                                                                                                                                                                                                                                                                        |
| Gate 9 evidence ref collides, becomes unreachable, hides as a dangling loose symbolic ref, or is replaced by a blocking special file | Raw descriptor-relative loose-namespace discovery with nonblocking no-follow leaf opens; a 2.0-second bound on all three Gate 9 execution funnels — every subprocess, every descriptor-opening read of an outside-influenceable path, and every whole-file read — rather than on one named command, with a separate process session plus terminate/kill/reap for the spawning funnel and a nonblocking open with an `fstat` type check and an alarm armed before the open for the two descriptor funnels, and no retry anywhere; index regular-file guard before the authority preflight's first index-reading Git call; exact canonical direct-commit patterns; stable two-snapshot OID identity; raw/union disagreement rejection; create-only no-deref CAS; distinct read-only `STALE_REF_LOCK` diagnosis that stops the gate and clears nothing; exact ref/tree/checksum verification; in-memory reconstruction of bundle bytes; and retention through Task 12/branch handoff | Stop as `FOREIGN_REF`, `STALE_REF_LOCK`, or `BLOCKED` within the 2.0-second funnel bound plus, for a spawned child, the 0.5-second termination grace rather than indefinitely, without leaving an unreaped child, overwriting, unlinking, or following the entry; a lock residue is reported for operator removal, never cleared by the gate; never infer an empty namespace or authorization from `for-each-ref` alone or a retained `/tmp` bundle |
| Subagent ownership conflict                                                                                                          | One implementer per unit and exact file ownership                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Interrupt conflicting agent; preserve reviewed predecessor commit                                                                                                                                                                                                                                                                                                                                                                                   |
| Secret/runtime/remote boundary crossed                                                                                               | Read-only tracked evidence and explicit exclusions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Stop immediately; exclude value/output; seek new authority if required                                                                                                                                                                                                                                                                                                                                                                              |

The deletion commit is recoverable from its parent with targeted Git history.
Destructive reset, broad checkout, and filesystem removal outside the exact old
pack are forbidden.

## Approval Gates

| Gate                                      | Required evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Blocks                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Spec and Plan amendment active            | Spec 137 amendments `90eca714`, `76808636`, `af37969b` plus two final amended-Spec reviews C0/I0/M0; this exact Plan-amendment commit plus two independent reviews C0/I0/M0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Any Task backfill, V&V authoring, Gate 9 recovery, or deletion execution |
| Ledger ready                              | Task tables, old blobs, baseline results reviewed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Leaf authoring                                                           |
| Unit review                               | Specification and quality reviews C0/I0 over committed `BASE..HEAD`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Next task                                                                |
| Pack complete                             | 20 leaves/21 files, 36/36 requirements, 14/14 scopes, source/claim completeness                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Human route switch and Gate 9                                            |
| Verification and validation unit reviewed | Task-only amendment evidence; immutable 17-path initial commit `139ced00` and both initial receipts; reviewed Plan correction/fix chain; separately reviewed two-path parent-router/Task fix; exact final 18-path unique scope; parent router states 20 leaves/21 files and still links only the pack README; exact nine-H2 REQ-36 leaf; current primary-source/status/paywall boundaries; remeasured owner table; all 14 scopes; README/cross-links/Stage 03 status; unchanged 1,339/1,338 generated cardinalities; explicit Step 8 Task-only evidence closure; and both external closure-integrity receipts binding its exact commit/range at C0/I0/M0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Task 10 finalization, Phase A, and Gate 9                                |
| Security generator repair approved        | Explicit user approval plus focused RED/GREEN test plan for the typed-registry fix                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Task 10 mutations, machine route switch, and old-pack deletion           |
| LLM retiring-path projection reviewed     | Focused exact-prefix RED/GREEN contract and reviewed Plan correction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Task 10 LLM generator mutation and old-pack deletion                     |
| Metadata exception retirement reviewed    | Exact sixteen mutable-exception removals, zero new-pack exceptions, and unchanged seven-row pinned baseline evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Task 10 route-switch commit and old-pack deletion                        |
| Gate 9 evidence contract reviewed         | Step 0c finite schemas/state machine plus the separately approved Step 0e recovery: reviewed Task-only blocker/approval prerequisite; exact six-file ceiling; raw pathless tree objects; fresh sealed manifests; final-post-fsync bundle-publication linearization; controller-captured literal path plus expected bundle/package hashes required for every external source; transport-first once-read comparison; nonblocking raw dangling-loose-symref/special-file discovery; a 2.0-second bound on every Gate 9 subprocess, every outside-influenceable descriptor-opening read, and every whole-file read, with separate process session and terminate/kill/reap for the spawning funnel and a nonblocking open with an `fstat` type check and an alarm armed before the open for the two descriptor funnels; index regular-file guard before the authority preflight's first index-reading Git call; distinct read-only `STALE_REF_LOCK` diagnosis that stops the gate and clears nothing; stable direct-ref snapshots; in-memory Task/evidence/ref replay; append-only named object writes; no cleanup/extraction; fresh projection in every authority mode; the preserved five-round breaker with round 4 assigned to a fresh more-capable implementer; and fresh implementation plus closure-integrity specification/Python-security reviews at C0/I0/M0 | Phase A, any new Gate 9 attempt, and old-pack deletion                   |
| Lifecycle result mapping reviewed         | The deletion commit exists and has two C0/I0 reviews; the post-delete package contains six exact delta rows, eight evidenced delete results with real rollback SHAs, canonical summaries, target-surface manifest/summary PASS, and no target-surface promoted finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Lifecycle-evidence commit and Task 12                                    |
| Route switch safe                         | Zero clickable old routes, reviewed allowlist, fresh LLM outputs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Old-pack deletion                                                        |
| Deletion safe                             | All nine Spec 137 pre-deletion gates, including repository contract PASS and `verify-authorized` over the live bundle plus full in-memory evidence-ref replay                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `git rm`                                                                 |
| Branch complete                           | Final exact-range validation and reviews C0/I0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Task completion and finishing handoff                                    |

## Completion Criteria

- The 2026-08-08 directory contains exactly one README and twenty reviewed
  leaves and is the sole active canonical research pack.
- The parent research router states exactly 20 leaves/21 files, links once to
  the pack README, and does not directly enumerate the V&V leaf; the reviewed
  final Task 9a implementation scope contains exactly 18 unique paths.
- Every REQ-01 through REQ-36 row has a reviewed canonical destination.
- Every one of the fourteen normative scopes has a reviewed disposition.
- Every load-bearing external claim has direct source, access date, mutability,
  and verification state; every workspace claim has tracked evidence and a
  runtime limit.
- Every old file and unique claim has immutable provenance and a reviewed
  retain/correct/omit/supersede disposition.
- All clickable old-pack references are removed; allowed historical non-link
  literals are enumerated and reviewed.
- LLM Wiki index and coverage freshness checks pass at 1,339 index rows and
  1,338 coverage paths after the V&V route switch and remain byte-identical
  after deletion.
- Step 0e closes within its five-round breaker with the explicit POSIX bundle
  publication linearization, controller-trusted expected receipt hashes,
  transport-first rejection of a fully canonical but non-identical
  post-publication tuple, nonblocking raw discovery of dangling loose symbolic
  or special-file evidence refs, bounded Gate 9 execution funnels covering
  every subprocess, every outside-influenceable descriptor-opening read, and
  every whole-file read — fully reaped where the funnel spawns and closed on an
  alarm armed before the open where it only opens a descriptor — with a
  distinct terminal read-only stale-ref-lock state that clears nothing,
  stable canonical direct-ref identity, and both implementation and
  closure-integrity review pairs at C0/I0/M0 before Phase A or Gate 9 runs.
- The old twenty files are deleted in their own reviewed, recoverable commit.
- The advisory target-surface delta and both canonical summaries are fresh;
  the target-surface convergence manifest/summary pass, and promoted lifecycle
  output contains only the separately classified Foundation predecessor.
- Metadata, traceability, repository contracts, diff hygiene, and old-path
  checks pass; implementation alignment has zero attributable delta.
- Final whole-branch specification and quality reviews report zero unresolved
  Critical or Important findings.
- The Task and current memory state actual outcomes without prospective PASS
  claims, raw logs, or secrets.
- No runtime, secret, remote, push, PR, merge, or branch-deletion action occurs
  without separate authority or final user choice.

## Related Documents

- [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Tasks index](../tasks/README.md)
- [Research references](../../90.references/research/README.md)
- [New canonical pack](../../90.references/research/2026-08-08-agentic-engineering-research-pack/README.md)
- [Reference template](../../99.templates/templates/common/reference.template.md)
- [Task template](../../99.templates/templates/sdlc/task.template.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
