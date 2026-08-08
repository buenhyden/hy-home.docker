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

This plan executes the active Spec 137 design as twelve sequential,
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
Eight independently reviewed authoring units build the nineteen leaves while
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

| Input | Baseline state |
| --- | --- |
| Branch base | `78b60974164ff5427ba8c64aaf3ecde4a7faf41a` |
| Written design commit | `3182daa8` |
| Active Spec 137 commit | `35318255` |
| Old pack | 20 regular files: README plus 19 leaves |
| LLM Wiki index | Fresh at design time |
| LLM Wiki coverage | Stale at design time |
| Security readiness snapshot | Stale and semantically unreliable because its generator misses typed workflow-registry resolution |
| Repository contract | Blocked by missing `html5lib` in the current validation environment |
| Document implementation alignment | 184 pre-existing archive-direct-link findings; Spec 137 introduces zero |
| Graphify | Advisory and stale; built from `f8a72211` |

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

The Task instantiates all `REQ-01` through `REQ-35` from Spec 137. A task may
add discoveries but may not merge or remove the thirty-five required rows.
Completion requires thirty-five reviewed canonical destinations and fourteen
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

### File map

| Responsibility | Files |
| --- | --- |
| Execution evidence | Create `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`; modify `docs/04.execution/tasks/README.md` |
| Foundation | Create `workspace-baseline.md`, `scope-application-matrix.md` in the new pack |
| Agentic core | Create `harness-engineering.md`, `loop-engineering.md`, `provider-implementation-comparison.md` |
| Agent instructions/models/memory | Create `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md` |
| SDLC contracts | Create `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `document-metadata-lifecycle.md` |
| Documentation systems | Create `documentation-architecture.md`, `llm-wiki-system.md` |
| Delivery quality | Create `automation-pipeline-workflow.md`, `quality-ci-formatting.md` |
| Infrastructure/security | Create `docker-compose-infrastructure.md`, `security-governance.md` |
| Human routing | Create new pack `README.md`; modify `docs/90.references/research/README.md` and other active clickable consumers discovered by the stale-path inventory |
| Machine routing | Regenerate `docs/90.references/llm-wiki/llm-wiki-index.md` and `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` |
| Retiring pack | Delete exactly the twenty files under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` after Task 11 gates pass |
| Final evidence | Modify the Task and `docs/00.agent-governance/memory/current.md`; update a durable memory note only when the memory contract selects one |

## Goals and Non-goals

### Goals

- Author nineteen focused, current leaves rather than moving or lightly editing
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

- Consumes: active Spec 137 at `35318255`, this Plan, and the old pack.
- Produces: the requirement, source/evidence, claim-migration,
  generated-artifact, old-path allowlist, verification, review, and commit
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
PASS claims. Add tables for all 35 requirement IDs, all 14 scopes, external
and workspace sources, old claims, four generated artifacts, old-path
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

Copy `REQ-01` through `REQ-35` verbatim from Spec 137 into the Task and create
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

- Consumes: REQ-33, nineteen reviewed leaves, 35 requirements, 14 scopes,
  source and claim ledgers.
- Produces: the human canonical route and pre-switch completeness verdict.

- [ ] **Step 1: Author the pack README**

Include Stage 90 boundary, grouped nineteen-leaf tree, current-state summary,
reading order, evidence classes, scope routing, maintenance rules, old/new
migration statement, and direct links to every leaf.

- [ ] **Step 2: Audit requirement, scope, source, and claim coverage**

Prove exactly 19 leaf files, 35/35 requirement destinations, 14/14 scope
dispositions, source entries for every load-bearing external claim, and a
disposition for every unique old claim. Any missing row stops this task.

```bash
find docs/90.references/research/2026-08-08-agentic-engineering-research-pack \
  -maxdepth 1 -type f -printf '%f\n' | sort
find docs/90.references/research/2026-08-08-agentic-engineering-research-pack \
  -maxdepth 1 -type f | wc -l
rg -n 'REQ-(0[1-9]|[12][0-9]|3[0-5])' \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
```

Expected: 20 regular files total (README plus 19 named leaves), exactly one
canonical destination for each of 35 requirements, and reviewed dispositions
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
`/tmp/agentic-research-route-paths.txt`; this scratch file is never committed.

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

The GREEN assertions must prove that all twenty retiring-pack paths are absent
from both generator inventories, the new `2026-08-08` pack remains present,
and similarly named Stage 04 Plan/Task history remains present. Do not use a
substring or date-wide exclusion. Run:

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

Confirm every line in the scratch path list is a classified route consumer,
self-review the route, generator/test, and generated diffs, then stage only
that list, the two generators, the focused test, the two generated outputs,
and the Task:

```bash
git add --pathspec-from-file=/tmp/agentic-research-route-paths.txt
git add scripts/knowledge/generate-llm-wiki-index.sh \
  scripts/knowledge/generate-llm-wiki-coverage.sh \
  tests/validation/test_llm_wiki_retiring_pack_exclusion.py \
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
- Modify: `docs/90.references/llm-wiki/llm-wiki-index.md` through its generator
- Modify: `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` through its generator
- Modify: execution Task ledger with proposed-deletion, staged-deletion,
  recoverability, freshness, review, and commit evidence

**Interfaces:**

- Consumes: REQ-33, REQ-34, reviewed new pack, complete claim ledger, zero
  clickable old-path references, fresh LLM outputs, and all pre-deletion
  validation evidence.
- Produces: sole active canonical pack and a recoverable deletion commit.

- [ ] **Step 1: Execute pre-deletion gates 1 through 8**

Confirm in the Task: 20/20 old files pinned; every unique claim mapped; every
retain/correct destination reviewed; every omission reasoned; 35/35
requirements; 14/14 scopes; C0/I0; zero clickable old references; reviewed
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

Use a temporary Git index to model the twenty deletions without changing the
real index or removing a worktree file. The two generators inherit the
temporary index and therefore render the proposed post-deletion state:

```bash
DELETION_REVIEW_DIR=$(mktemp -d /tmp/agentic-research-deletion-review.XXXXXX)
DELETION_REVIEW_INDEX="$DELETION_REVIEW_DIR/index"
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" git read-tree HEAD
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" git rm -r --cached \
  docs/90.references/research/2026-07-05-agentic-research-pack-refresh
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" \
  bash scripts/knowledge/generate-llm-wiki-index.sh
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" \
  bash scripts/knowledge/generate-llm-wiki-coverage.sh
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" git add \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
GIT_INDEX_FILE="$DELETION_REVIEW_INDEX" git diff --cached --binary \
  > "$DELETION_REVIEW_DIR/proposed-deletion.patch"
```

Inspect the proposed patch and confirm it contains exactly twenty deletions,
two generated-artifact updates, and the current Task evidence.

- [ ] **Step 4: Satisfy pre-deletion gate 9**

Dispatch independent migration/specification and quality reviewers with the
proposed patch, old/new manifests, immutable old blobs, claim ledger,
recoverability evidence, and Task brief. Require C0/I0 and record the proposed
deletion diff, recovery commit, and reviewer verdict in the Task. If recording
the verdict changes the Task, refresh the temporary-index patch and rerun both
independent reviewers so the reviewed proposal includes that evidence. Do not
touch the real index until gate 9 passes. Both separate verdicts must cover the
same final package. If the gate fails,
restore only the two generator-owned worktree files from `HEAD`, keep the old pack intact,
and return the findings to the implementer:

```bash
git restore --source=HEAD -- \
  docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
```

- [ ] **Step 5: Delete the old files in the real index**

Use `git rm` with the exact directory only after all nine gates pass:

```bash
git rm -r docs/90.references/research/2026-07-05-agentic-research-pack-refresh
```

- [ ] **Step 6: Run post-deletion checks before committing**

Regenerate both path-derived artifacts after the staged deletion removes the
old paths from the Git index, inspect their diff for the expected old-pack
removal and unchanged safety boundaries, then require byte-exact freshness:

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
requirement/scope/claim audit, and diff hygiene. Any regression restores the
directory from the parent commit and stops the task.

- [ ] **Step 7: Review the actual staged deletion**

Stage the two generated outputs and Task, write the actual cached diff to
`$DELETION_REVIEW_DIR/actual-deletion.patch`, and dispatch two fresh,
independent staged-diff reviewers over that same immutable patch: one owns
migration/specification compliance and one owns quality. Require both separate
verdicts at C0/I0. If evidence changes, rebuild the patch and rerun both. This
verifies the real index, including the recorded gate-9 evidence, before a
commit exists.

```bash
git add docs/90.references/llm-wiki/llm-wiki-index.md \
  docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md \
  docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md
git diff --cached --binary > "$DELETION_REVIEW_DIR/actual-deletion.patch"
```

- [ ] **Step 8: Self-review and commit the deletion unit**

Verify the exact staged set and deletion/generator diff, then:

```bash
git commit -m "docs(research): retire superseded agentic research pack"
```

The `git rm` entries are already staged; confirm the staged set is exactly the
twenty deletions, both regenerated LLM Wiki artifacts, and the Task update
before committing.

- [ ] **Step 9: Review the committed deletion unit**

Run the committed-unit SDD protocol for Task 11. Require two fresh independent
reviewers over the exact deletion commit range and record separate
migration/specification and quality verdicts. If a load-bearing route or claim
was lost, restore it in an implementer fix commit and complete both scoped
re-reviews before Task 12.

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
alignment, repository contracts, both LLM freshness checks, old-slug inventory,
complete requirement/scope/claim audit, `git diff --check`, and exact
base-to-head file review. Record commands, exit codes, and attributable
predecessors without raw logs or secrets.

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
git grep -n -I '2026-07-05-agentic-research-pack-refresh' -- \
  ':!docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**'
git diff --name-status \
  78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD
git diff --check \
  78b60974164ff5427ba8c64aaf3ecde4a7faf41a..HEAD
git status --short
```

The Task additionally records its deterministic 35-requirement, 14-scope, and
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

Expected before deletion: 20 new files, zero unreviewed old-slug occurrences,
and two generator PASS results. Expected after deletion: the same new pack,
zero clickable old routes, and only reviewed historical non-link literals.

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

| Risk | Control | Rollback |
| --- | --- | --- |
| Old prose copied with stale facts | Claim ledger and current-source remeasurement | Revert the affected leaf commit and re-author from the source/evidence rows |
| Mutable provider source changes mid-task | Access timestamps and per-unit review | Reopen source, correct only affected claims, rerun review |
| Unavailable/paywalled source | `UNVERIFIED` boundary | Remove unsupported conclusion; retain historical pointer only |
| Scope or requirement omission | Closed 35-row and 14-row matrices | Stop pack routing until missing row has a reviewed destination |
| Broken historical link after deletion | Whole tracked-text scan and zero clickable exceptions | Restore old pack from deletion parent and repair routes |
| Generated coverage remains stale | Canonical write then byte-exact checks | Revert generated outputs and diagnose generator before deletion |
| Fresh LLM navigation re-emits the retiring pack while both packs coexist | Focused RED/GREEN exact-prefix test in both LLM Wiki generators; retain new-pack and similarly named Stage 04 paths | Revert the route-switch unit, keep both packs, and do not enter deletion review |
| Security generator false gaps | Before separate approval, do not regenerate and derive direct tracked evidence; after approval, require focused RED/GREEN tests and canonical write/check | Before approval, preserve the stale predecessor; after approval, revert the isolated repair commit and keep both packs when tests, generated diff, or review fails |
| Repository contracts cannot load | Fail-closed deletion gate | Continue non-destructive authoring only; do not delete until environment gate passes |
| Subagent ownership conflict | One implementer per unit and exact file ownership | Interrupt conflicting agent; preserve reviewed predecessor commit |
| Secret/runtime/remote boundary crossed | Read-only tracked evidence and explicit exclusions | Stop immediately; exclude value/output; seek new authority if required |

The deletion commit is recoverable from its parent with targeted Git history.
Destructive reset, broad checkout, and filesystem removal outside the exact old
pack are forbidden.

## Approval Gates

| Gate | Required evidence | Blocks |
| --- | --- | --- |
| Spec active | Spec 137 active and C0/I0 review | Plan execution |
| Ledger ready | Task tables, old blobs, baseline results reviewed | Leaf authoring |
| Unit review | Specification and quality reviews C0/I0 over committed `BASE..HEAD` | Next task |
| Pack complete | 19 leaves, 35/35 requirements, 14/14 scopes, source/claim completeness | Human route switch |
| Security generator repair approved | Explicit user approval plus focused RED/GREEN test plan for the typed-registry fix | Task 10 mutations, machine route switch, and old-pack deletion |
| LLM retiring-path projection reviewed | Focused exact-prefix RED/GREEN contract and reviewed Plan correction | Task 10 LLM generator mutation and old-pack deletion |
| Route switch safe | Zero clickable old routes, reviewed allowlist, fresh LLM outputs | Old-pack deletion |
| Deletion safe | All nine Spec 137 pre-deletion gates, including repository contract PASS | `git rm` |
| Branch complete | Final exact-range validation and reviews C0/I0 | Task completion and finishing handoff |

## Completion Criteria

- The 2026-08-08 directory contains exactly one README and nineteen reviewed
  leaves and is the sole active canonical research pack.
- Every REQ-01 through REQ-35 row has a reviewed canonical destination.
- Every one of the fourteen normative scopes has a reviewed disposition.
- Every load-bearing external claim has direct source, access date, mutability,
  and verification state; every workspace claim has tracked evidence and a
  runtime limit.
- Every old file and unique claim has immutable provenance and a reviewed
  retain/correct/omit/supersede disposition.
- All clickable old-pack references are removed; allowed historical non-link
  literals are enumerated and reviewed.
- LLM Wiki index and coverage freshness checks pass after the route switch and
  after deletion.
- The old twenty files are deleted in their own reviewed, recoverable commit.
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
- [Current pack pending retirement](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Reference template](../../99.templates/templates/common/reference.template.md)
- [Task template](../../99.templates/templates/sdlc/task.template.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
