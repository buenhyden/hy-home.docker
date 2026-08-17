---
status: draft
artifact_id: reference:agentic-engineering-research:scope-application-matrix
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: Agentic Engineering Scope Application Matrix

## Overview

This reference is the scope-axis entry point for the agentic engineering
research pack. It dispositions all fourteen persona scopes defined by the
[persona protocol](../../../00.agent-governance/rules/persona.md), maps them to
the twenty planned research leaves, and separates real workspace surfaces from
typed catalog reachability.

At baseline commit `528c225d35d6c986b50f9b997fd08921a8df9a9b`, all fourteen
scope files exist. The [typed agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)
admits eight scope values. Six normative scopes are outside that enum:
`backend`, `entry`, `frontend`, `meta`, `mobile`, and `product`. The findings
were re-verified at commit `55809319e462ed6ae9ed4a3f31055fc55c2a2294` on
2026-08-11 and re-derived again at commit
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on 2026-08-14.

The 2026-08-14 re-derivation **corrects one previously stated disposition**.
Earlier revisions described `architecture` as "enum only" with the gloss that
no current agent record declares it. Reading the typed contract directly shows
that `architecture` has zero agent records _and two active function records_,
`adr-writing` and `requirements-to-design-agent`, whose owner agents are
declared in other scopes. `architecture` is therefore not an empty enum value;
it is a scope whose typed work is owned across a scope boundary. The corrected
four-class reachability taxonomy is below.

## Purpose

Satisfy REQ-32 by giving every scope a current adoption or explicit
not-applicable disposition, including governed paths, applicable leaves,
implementation state, adoption rules and exceptions, evidence owner,
validation owner, and catalog reachability. Topic leaves can cite this matrix
without silently dropping a persona scope.

The 2026-08-14 deepening adds a second obligation: state where the scope axis
is _enforced_ rather than merely declared, and name every place two tracked
surfaces assign the same path to different owners.

## Repository Role

This Stage 90 matrix is a research and routing aid. It reports current scope
applicability and gaps but does not alter the persona protocol, typed catalog,
File Ownership SSOT, lifecycle approvals, runtime configuration, or remote
enforcement.

## Scope

### In scope

- The fourteen tracked files under `docs/00.agent-governance/scopes/`.
- Persona-to-scope routing and the typed agent/function catalog.
- The three tracked contracts under `docs/00.agent-governance/contracts/`,
  including the path-authority records that earlier revisions did not cite.
- Tracked workspace surfaces named or governed by each scope.
- The validators and tests that do or do not assert the scope axis.
- Applicability to all twenty leaves in the planned pack.

### Out of scope

- Adding a missing scope value, agent, function, or provider projection.
- Resolving ownership conflicts in Stage 00 policy. This matrix reports them;
  the Stage 00 owner decides them.
- Inspecting secrets/private state, starting services, proving runtime health,
  or reading remote provider/GitHub enforcement.
- Treating this Stage 90 analysis as authority to adopt a recommendation.

## Definitions / Facts

### Concept and evidence model

This matrix treats a scope as a policy-and-routing lens, not as proof that an
application surface exists. `Implemented` means the relevant tracked surface
and route exist. `Partial` means the subject exists but ownership, coverage, or
verification is incomplete. `Missing` means an expected tracked implementation
is absent. `Not Applicable` means no current surface exists to which the scope
can bind. `Unverified` is reserved for runtime, remote, private, or other
unobserved state.

Three external models sharpen what a scope taxonomy can and cannot carry. They
are comparison lenses, never catalog or adoption authority:

- The Backstage software catalog requires `spec.owner` on `Component`, `API`,
  `Resource`, `System`, and `Domain`, but explicitly leaves `type` taxonomies
  open — the descriptor format "accepts any type value, but an organization
  should take great care to establish a proper taxonomy". It also warns that
  owners are not to be used by automated processes to assign authorization in
  runtime systems. This repository sits on both sides of that line: its
  eight-value catalog scope enum is _closed and validator-enforced_, while its
  fourteen-value persona axis is _open and enforced only by convention_. The
  two-axis split below is the direct consequence.
- The A2A v1.0 Agent Card separates `capabilities` — protocol-level features
  such as streaming — from `skills`, the functional offerings an agent
  performs, each with its own `id`, `name`, and modes. The repository's typed
  catalog makes exactly this split: 14 `agents` are roles with permission and
  work profiles, and 24 `functions` are named units of work with owners, gates,
  and reviewers. A2A also makes declaration binding — an undeclared capability
  MUST produce an error rather than a silent attempt — which is the external
  analogue of `provider_projections` gating which surfaces receive a skill body.
- The Model Context Protocol 2026-07-28 specification negotiates capabilities
  per request, keeps extensions opt-in and mutually agreed, and states that the
  protocol "cannot enforce these security principles at the protocol level". A
  declared scope, like a declared capability, is a contract about intent rather
  than evidence of behavior.

NIST SSDF v1.1 remains a comparison vocabulary for secure-development
responsibility assignment; it deliberately leaves tool and owner choice to the
adopting organization, so it cannot arbitrate a local scope disposition.

### Derivation commands and observations

The 2026-08-14 re-derivation ran the following against the tracked workspace:

```bash
git ls-files | wc -l
find docs/00.agent-governance/scopes -maxdepth 1 -type f -name '*.md' \
  -printf '%f\n' | sort
find docs/03.specs -mindepth 1 -maxdepth 1 -type d | wc -l
find docs/98.archive/03.specs -type f -name spec.md | wc -l
python3 -c "import yaml; ..."   # full parse of all three typed contracts
python3 scripts/validation/check-agent-governance-contract.py --mode contract
python3 scripts/validation/check-agent-governance-contract.py \
  --mode repository --section all
python3 -m unittest tests.validation.test_agent_governance_contract
```

Results: 1,673 tracked paths; exactly 14 sorted scope filenames; 28 active Spec
directories; 32 archived `spec.md` files. The complete typed catalog parse
found 8 allowed scope values, 14 agent records, and 24 function records. The
two validator invocations returned
`PASS contracts=3 agents=14 functions=24 providers=3 failures=0` and
`PASS mode=repository section=all failures=0`, and the 159-test suite returned
`OK`. All three executions required an interpreter satisfying
`scripts/requirements.txt`; the default interpreter in this workspace exits
with `AGC-DEPENDENCY-MISSING path=html5lib`, the pre-existing unowned gap. The
2026-08-11 measurement of 1,646 → 1,672 → 1,673 tracked paths reflects
repository growth unrelated to scope routing; the scope, agent, function, and
Spec-directory counts are unchanged across all three measurements.

### The canonical enum, read from the contract

The eight admitted values are read from `scopes:` in `agent-catalog.yaml`, not
from prose. They are `agentic`, `architecture`, `common`, `docs`, `infra`,
`ops`, `qa`, and `security`. The validator enforces membership at two points —
`agent_governance_contract.py:2661` for agent records and `:2778` for function
records — using `_is_registered_string(entry.get("scope"), scopes)` against the
contract's own list.

The fourteen persona values come from a different artifact,
`rules/persona.md:25-38`, which maps each persona to a `Primary Layer` and a
`Primary Governance` scope file. Each scope file carries `layer: <name>` in its
frontmatter.

These are two axes, not one list with holes. Distribution across the enum:

| Enum value     | Agent records | Function records | Function names                                                                              |
| -------------- | ------------: | ---------------: | ------------------------------------------------------------------------------------------- |
| `agentic`      |             4 |                4 | execution-plan-agent, policy-gate-agent, task-breakdown-agent, workspace-audit-revalidation |
| `architecture` |             0 |                2 | adr-writing, requirements-to-design-agent                                                   |
| `common`       |             1 |                2 | code-review-dimensions, code-reviewer                                                       |
| `docs`         |             1 |                2 | knowledge-map-agent, project-memory-stewardship                                             |
| `infra`        |             3 |                4 | compose-stack-agent, docker-compose-patterns, infra-cross-validate, infra-validate          |
| `ops`          |             2 |                4 | ci-cd-patterns, deployment-pipeline-design, incident-response, ops-runbook-agent            |
| `qa`           |             2 |                4 | e2e-testing, provider-model-evaluation, style-validation, test-automator                    |
| `security`     |             1 |                2 | container-threat-modeling, security-audit                                                   |

Agents use seven of the eight values; functions use all eight. Four functions
are owned across a scope boundary — the owner agent's declared scope differs
from the function's scope:

| Function                       | Function scope | Owner agent      | Owner agent's scope |
| ------------------------------ | -------------- | ---------------- | ------------------- |
| `adr-writing`                  | `architecture` | `doc-writer`     | `docs`              |
| `requirements-to-design-agent` | `architecture` | `rules-engineer` | `agentic`           |
| `ops-runbook-agent`            | `ops`          | `doc-writer`     | `docs`              |
| `workspace-audit-revalidation` | `agentic`      | `eval-engineer`  | `qa`                |

Both `architecture` functions are cross-scope owned. That is the mechanism by
which `architecture` work is routable today despite having no agent of its own,
and it is why "enum only" was the wrong label.

### Catalog reachability finding

The corrected taxonomy has four classes, not three.

| Reachability class                        | Scopes                                                        | Interpretation                                                                       |
| ----------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Enum, with agent and function records     | `agentic`, `common`, `docs`, `infra`, `ops`, `qa`, `security` | A current typed agent can declare the scope and owns functions in it.                |
| Enum, functions only, no agent record     | `architecture`                                                | The value is legal and carries two owned functions; both owners sit in other scopes. |
| Outside the enum, tracked subject surface | `entry`, `frontend`, `meta`, `product`                        | Substantive tracked material exists; no catalog record may name the value.           |
| Outside the enum, no tracked surface      | `backend`, `mobile`                                           | No current application surface exists for the scope to bind to.                      |

This is not a broken-link finding: every scope file exists and the persona
protocol routes to it. It is a typed delegation and reachability finding. A
catalog record cannot declare any of the six outside values without a Stage 00
contract change, because the validator rejects an unregistered scope string.

Each of the four outside-enum-but-tracked scopes was re-derived rather than
assumed. `entry` has 16 tracked files under `infra/01-gateway/`. `frontend` has
51 tracked files under `projects/storybook/`, of which 50 are under `nextjs/`,
with exactly one tracked `package.json` and 16 tracked `.ts`/`.tsx` files.
`meta` is backed by 25 typed artifact profiles, 3 README profiles, and 3
governed families in `agent-governance-artifacts.yaml`, plus 33 template-tree
files. `product` is backed by 26 tracked Stage 01 files.

The two `Not Applicable` scopes were re-derived by negative enumeration, which
is stronger than the absence of a directory. Across the whole tracked corpus,
zero files match `.go`, `.rs`, `.java`, `.kt`, `.swift`, `.dart`, `.rb`,
`.php`, `.cs`, `.js`, or `.jsx`. All 45 tracked `.py` files live under
`scripts/` or `tests/`; all 16 tracked `.ts`/`.tsx` files live under
`projects/storybook/nextjs/`. `backend.md` claims a Node.js 22+/Prisma/Zod and
Python 3.12+/SQLAlchemy/FastAPI stack, and `mobile.md` claims React Native
0.74+/Expo 51+. No tracked file uses either stack. Both dispositions hold.

`frontend` is deliberately **not** in the same class. One bounded Storybook and
Next fixture exists and is assigned to a typed owner by the QA scope, so the
correct label is `Partial`, not `Not Applicable`. Collapsing `frontend` into
the backend/mobile class would overstate the gap.

### Scope-file structural tiers

The fourteen scope files are not structurally uniform, and the split is exact.
Six carry a `File Ownership SSOT` section and a `Subagent Bridge` section on
top of the shared five-section body; eight carry only the five-section body.

| Tier                                            | Scopes                                                                                 | Count |
| ----------------------------------------------- | -------------------------------------------------------------------------------------- | ----: |
| Full: 5 sections + File Ownership SSOT + Bridge | `common`, `docs`, `infra`, `ops`, `qa`, `security`                                     |     6 |
| Base: 5 sections only                           | `agentic`, `architecture`, `backend`, `entry`, `frontend`, `meta`, `mobile`, `product` |     8 |

The six full-tier scopes are exactly the enum-plus-agent scopes minus
`agentic`. That is not a coincidence: `agentic`-scoped paths are instead
covered by the typed `path_authority` records, four of whose seven canonical
owners are agentic-scope agents (`rules-engineer` twice, `skill-creator`,
`hook-developer`). Ownership for the agentic surface migrated from prose into
the typed contract; ownership for the other five stayed in prose. No scope file
carries ownership in both places.

File size varies by nearly an order of magnitude, which is a proxy for how much
operational detail each scope has accumulated: `qa.md` is 13,319 bytes and 162
lines, while `agentic.md` is 1,389 bytes and 45 lines. The eight base-tier
files range from 1,389 to 2,566 bytes and are, in content, aspirational
standard sheets — `frontend.md` names Next.js 15+, React 19+, Tailwind v4, and
WCAG 2.2 AA; `backend.md` names OWASP ASVS L2 and a 90 percent domain-logic
coverage floor; `mobile.md` names Expo Application Services builds. None of
those claims has a tracked surface to bind to today, which is why the matrix
labels their targets as adoption exceptions rather than as current state.

`docs.md` numbers its ownership and bridge sections `5` and `6` while the other
five full-tier files number them `6` and `7`. `frontend.md` also renders its
Related Documents as bare paths where the other thirteen use Markdown links.
Both are cosmetic, and both are recorded here only so a later reader does not
mistake them for a missing section.

### Three parallel ownership surfaces

Path ownership is asserted in three tracked places with three vocabularies and
three precedence rules. Reading only one of them produces a wrong answer.

| Surface                                               | Records           | Vocabulary         | Precedence rule                                           | Validator                                                     |
| ----------------------------------------------------- | ----------------- | ------------------ | --------------------------------------------------------- | ------------------------------------------------------------- |
| `path_authority` in `agent-governance-artifacts.yaml` | 7 records         | `agent_id`         | none stated                                               | `check-agent-governance-contract.py` — executed, `failures=0` |
| `File Ownership SSOT` in six scope files              | 6 tables, 24 rows | `agent_id`         | "the most specific scope wins", stated only in `infra.md` | none found                                                    |
| `.github/CODEOWNERS`                                  | 30 path rules     | one GitHub account | last matching pattern wins (GitHub semantics)             | `check-repo-contracts.sh` requires 11 of the 30 patterns      |

The three surfaces govern largely disjoint paths. All seven typed
`path_authority` records cover Stage 00, provider adapters, `.github` quality
workflow, the metadata contract, and the governance validators. None covers
`docs/01`-`docs/05`, `infra/`, or `projects/`. The prose tables cover exactly
those omitted areas. `CODEOWNERS` covers a third overlapping set and resolves
every rule to the same human account, so it encodes neither the fourteen scopes
nor the fourteen agents.

Three assignment conflicts are visible in tracked text at this commit. They are
reported, not resolved:

| Path                            | Claim A                                                 | Claim B                                                                                                                  |
| ------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `docs/05.operations/`           | `docs.md` §5 — `doc-writer` owns, all other agents read | `ops.md` §6 — `incident-responder` owns, all other agents read                                                           |
| `docs/05.operations/incidents/` | `ops.md` §6 — `incident-responder` owns                 | `security.md` §6 — `security-auditor` owns                                                                               |
| `docs/00.agent-governance/`     | `docs.md` §5 — `doc-writer` owns                        | typed `stage00-policy-and-contracts` — `rules-engineer` is canonical owner; `doc-writer` is only a permitted contributor |

The first two are prose-versus-prose and both sides declare the other agent
read-only, so they cannot both hold. The third is prose-versus-typed, and the
typed record is the one a validator checks. `infra/*/` is _not_ a conflict:
`infra.md` grants ownership to `infra-implementer` and `security.md` records
itself as read-only over the same paths, which is consistent.

Three path patterns in the prose tables have no tracked instance. `common.md`
claims `common/`, `lib/`, and `shared/` at the repository root; `git ls-files`
returns zero files for each. The one tracked analogue is `scripts/lib/`, a
single file, which the table does not name.

### Validation coverage of the scope axis

The scope axis is enforced in fragments, and the fragments do not meet.

| Assertion                                           | Where                                                          | Coverage                                     |
| --------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------- |
| Agent `scope` ∈ catalog enum                        | `agent_governance_contract.py:2661`                            | 14 of 14 agent records                       |
| Function `scope` ∈ catalog enum                     | `agent_governance_contract.py:2778`                            | 24 of 24 function records                    |
| Scope-file `layer:` frontmatter equals its name     | `tests/validation/test_agent_governance_contract.py:1955-1967` | **13 of 14 files; `docs` omitted**           |
| Placeholder-path hygiene in scope prose             | `check-repo-contracts.sh:465-468` scans the scopes directory   | all 14 files, but only for path placeholders |
| Named content checks on individual scope files      | `check-repo-contracts.sh:1576-1577, 2898-2903`                 | `infra`, `security`, `common`, `qa`          |
| Doc/implementation alignment                        | `check-doc-implementation-alignment.sh:28`                     | `qa` only                                    |
| Prose File Ownership SSOT tables                    | no match for `File Ownership` under `scripts/` or `tests/`     | **none**                                     |
| Fourteen-file axis reconciled with eight-value enum | no validator found                                             | **none**                                     |

Two of these are new findings. The scope-frontmatter test enumerates thirteen
names and omits `docs`, so `docs.md` is the single scope file whose frontmatter
no test asserts. And nothing anywhere reconciles the two axes: the validator
checks catalog scope strings against the catalog's own list, never against the
directory of fourteen files, so the six-value divergence is structurally
invisible to automation. It survives only because documents like this one
restate it.

### Capability-intake evidence bearing on scope disposition

`agent-catalog.yaml` carries nine `capability_intake` records, each with a
source, a source URL, a retrieval date of 2026-07-26, a decision, an owner
agent, and an evaluation function. Eight decisions are `merge`. One is `defer`:

| Capability          | Decision | Owner agent           | Evaluation function            |
| ------------------- | -------- | --------------------- | ------------------------------ |
| `product-discovery` | `defer`  | `workflow-supervisor` | `workspace-audit-revalidation` |

This materially improves the `product` disposition. The absence of a typed
product route is not an oversight the catalog has failed to notice; it is a
recorded, sourced, dated deferral with a named owner, whose stated rationale is
to wait until a distinct approved output is required. `product` should
therefore be read as _deliberately deferred_, not as _missing_. No comparable
record exists for `backend`, `entry`, `frontend`, `meta`, or `mobile`, so those
five remain undecided rather than deferred.

## Scope Implications

Applicable leaf names below refer to the flat twenty-leaf pack contract in
[Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md).
`workspace-baseline.md` and this matrix apply to every row and are omitted from
the per-row leaf lists to keep the table readable. The `Catalog reachability`
column now reports agent and function counts separately, because the two differ
for `architecture`.

| Scope and governance owner                                            | Governed or applicable paths/artifacts                                                                                                                       | Applicable topical leaves                                                                                                                                      | Current disposition                                                                                                                         | Adoption rules / exceptions                                                                                                                          | Evidence owner                                                                      | Validation owner                                                         | Catalog reachability          |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------- |
| [`agentic`](../../../00.agent-governance/scopes/agentic.md)           | Stage 00 catalogs/rules, root shims, `.claude/`, `.agents/`, `.codex/`, `.gemini/`, hooks; 4 of 7 typed path-authority records                               | harness, loop, provider comparison, instructions, provider/model landscape, model selection, AI catalogs, memory, automation, verification/validation          | **Implemented** as tracked contracts; provider loading/interception and model execution are **Unverified**                                  | Provider-neutral policy stays in Stage 00; provider-native mechanics stay in adapters; changes need approved Stage 03/04 ownership and parity checks | `hook-developer`, `skill-creator`; workflow supervision where applicable            | `rules-engineer`; repository contracts and provider-surface sync         | Enum · 4 agents · 4 functions |
| [`architecture`](../../../00.agent-governance/scopes/architecture.md) | `docs/02.architecture/{requirements,decisions}/`, downstream Specs; no prose or typed ownership row in this scope                                            | spec-driven SDLC, document roles, Compose/infrastructure, security, automation, verification/validation                                                        | **Partial**: 53 Stage 02 files, 28 active Spec directories, and 2 owned functions exist; both owners sit in other scopes                    | Trade-offs route to ADRs; service boundaries route to Specs; protocol claims require a real service and tracked decision                             | `doc-writer` for `adr-writing`; `rules-engineer` for `requirements-to-design-agent` | `rules-engineer` and `workflow-supervisor` per the function records      | Enum · 0 agents · 2 functions |
| [`backend`](../../../00.agent-governance/scopes/backend.md)           | Future Node/Python/Go services; negative enumeration found zero tracked files in any claimed stack                                                           | quality, security, Compose/infrastructure, automation, verification/validation when a backend exists                                                           | **Not Applicable** to the current corpus; catalog route is **Missing** and no intake decision exists                                        | Do not apply stack, latency, ASVS L2, or 90% coverage claims until a backend surface and Spec exist                                                  | Backend Engineer persona; no typed agent                                            | Future layer owner plus QA/security reviewers; current code checks N/A   | Outside enum · 0 · 0          |
| [`common`](../../../00.agent-governance/scopes/common.md)             | `.pre-commit-config.yaml` (10 repositories, 24 hooks), shared conventions, `scripts/lib/`; claimed root `common/`, `lib/`, `shared/` have zero tracked files | instructions, metadata lifecycle, documentation architecture, quality, security, verification/validation                                                       | **Partial**: typed review route and local gates exist; three of its three claimed shared roots do not                                       | Agents must not invoke direct pre-commit/lint/format; the controlled all-files wrapper is final-QA-only and approval-bound                           | Cross-layer implementer; shared review route is `code-reviewer`                     | `code-reviewer`, scoped checks, `git diff --check`                       | Enum · 1 agent · 2 functions  |
| [`docs`](../../../00.agent-governance/scopes/docs.md)                 | Stages 01-05, 90, 98, 99 (980 tracked files); root shims; metadata/template/link systems                                                                     | spec-driven SDLC, document roles, metadata lifecycle, documentation architecture, LLM Wiki, memory, verification/validation; all leaves as authored references | **Implemented** as a tracked corpus and validator system; its own scope file is the one no frontmatter test asserts                         | Stage 01-99 is read-only by default; explicit approval, template-first authoring, direct links, and generated-index ownership apply                  | `doc-writer`                                                                        | Metadata/repository contracts plus independent documentation review      | Enum · 1 agent · 2 functions  |
| [`entry`](../../../00.agent-governance/scopes/entry.md)               | `infra/01-gateway/` (16 tracked files), Traefik/Nginx definitions                                                                                            | Compose/infrastructure, security, automation, quality, verification/validation                                                                                 | **Partial**: gateway definitions exist; Cloudflare edge and live certificate/log forwarding are **Unverified**; typed route is **Missing**  | Route mutations through `infra-implementer`; validate config/Compose; runtime and certificate operations require concrete approval/evidence          | `infra-implementer` by adjacent infra ownership                                     | `iac-reviewer`, `drift-detector`, Compose/config checks                  | Outside enum · 0 · 0          |
| [`frontend`](../../../00.agent-governance/scopes/frontend.md)         | `projects/storybook/` (51 tracked files, 50 under `nextjs/`), one `package.json`, 16 `.ts`/`.tsx` files                                                      | quality, automation, security, instructions, verification/validation                                                                                           | **Partial**: one bounded Storybook/Next fixture exists; no general product frontend and no catalog route is proven                          | Treat the sandbox as QA-owned until a product Spec says otherwise; accessibility/performance outcomes need execution evidence                        | No typed frontend agent; Storybook path is assigned to `code-reviewer` by QA scope  | `code-reviewer` and frontend/Storybook quality gates                     | Outside enum · 0 · 0          |
| [`infra`](../../../00.agent-governance/scopes/infra.md)               | 275 tracked `infra/` files, 11 numbered domains, 49 Compose-named files, 11 Dockerfiles, Stage 02 paths                                                      | Compose/infrastructure, security, automation, quality, harness/provider environment, verification/validation                                                   | **Implemented** as tracked definitions; live service health, latency, backups, and secrets remain **Unverified**                            | Pre-flight Compose validation; concrete-target runtime approval with pre-check, rollback, and post-check; no secret values                           | `infra-implementer`                                                                 | `iac-reviewer`, `drift-detector`, Compose and repository contracts       | Enum · 3 agents · 4 functions |
| [`meta`](../../../00.agent-governance/scopes/meta.md)                 | 25 typed artifact profiles, 3 README profiles, 3 governed families, 33 template-tree files, metadata/corpus validators                                       | metadata lifecycle, documentation architecture, LLM Wiki, document roles, spec-driven SDLC, verification/validation                                            | **Partial**: subject is implemented and typed in `agent-governance-artifacts.yaml`, but the scope value itself is **Missing** from the enum | Route edits through `doc-writer`; use mapped templates; update indexes when authorized; significant folder changes require a Meta ADR                | `doc-writer` by adjacent docs ownership                                             | metadata checker, corpus lifecycle, repository contracts                 | Outside enum · 0 · 0          |
| [`mobile`](../../../00.agent-governance/scopes/mobile.md)             | Negative enumeration found zero tracked Swift, Kotlin, Dart, Java, Android, or iOS source files                                                              | quality, security, automation, verification/validation only after a mobile surface is approved                                                                 | **Not Applicable** to the current corpus; catalog route is **Missing** and no intake decision exists                                        | Do not claim React Native/Expo adoption, device verification, EAS deployment, or mobile accessibility without a surface and approved lifecycle chain | Mobile Engineer persona; no typed agent                                             | Future mobile layer owner plus QA/security reviewers; current checks N/A | Outside enum · 0 · 0          |
| [`ops`](../../../00.agent-governance/scopes/ops.md)                   | `docs/05.operations/` (263 files), `infra/06-observability/` (99), `scripts/operations/` (8)                                                                 | automation, quality, Compose/infrastructure, security, document roles, verification/validation                                                                 | **Partial**: tracked surfaces exist; two of its three prose ownership rows conflict with other scopes; outcomes are **Unverified**          | Live incident evidence stays in incident packets; runtime changes require the infra protocol; do not infer outcomes from config                      | `incident-responder`, `ci-cd-engineer`                                              | Independent ops/infra review plus relevant local and remote gates        | Enum · 2 agents · 4 functions |
| [`product`](../../../00.agent-governance/scopes/product.md)           | `docs/01.requirements/` (26 tracked files), PRD template/glossary routes                                                                                     | spec-driven SDLC, document roles, documentation architecture, verification/validation                                                                          | **Partial**: requirements corpus exists; the typed route is **deliberately deferred** by a dated `capability_intake` record                 | Stakeholder approval precedes Spec; Stage 01 mutation needs explicit approval and template/metadata checks                                           | Product Manager persona/human stakeholder; `workflow-supervisor` holds the deferral | Human approval plus documentation metadata/repository checks             | Outside enum · 0 · 0          |
| [`qa`](../../../00.agent-governance/scopes/qa.md)                     | 42 validation scripts, 26 validation tests, 31 fixtures, 7 workflows/23 jobs, evaluation fixtures/regressions, Storybook                                     | harness, loop, automation, quality, security, LLM Wiki, metadata lifecycle, verification/validation                                                            | **Partial**: extensive gates exist; the default interpreter cannot run the governance contract, and remote gates are **Unverified**         | Use the smallest applicable check; docs-only TDD/coverage is N/A; no direct pre-commit; record skipped checks and predecessors                       | `qa-engineer`                                                                       | `eval-engineer`; independent review and named repository gates           | Enum · 2 agents · 4 functions |
| [`security`](../../../00.agent-governance/scopes/security.md)         | hardening/security scripts, supply-chain policies, incident routes, 19 placeholder-only `secrets/` files                                                     | security, Compose/infrastructure, quality, automation, harness/provider comparison, verification/validation                                                    | **Partial**: tracked controls exist; secret values, live runtime, and remote/provider enforcement are excluded or **Unverified**            | Metadata-only secret evidence; concrete target, redaction boundary, validation, and recovery path for approved secret/runtime work                   | Relevant layer implementer; `security-auditor` is read-only review                  | `security-auditor` plus hardening/template/quickwin/supply-chain gates   | Enum · 1 agent · 2 functions  |

### Six outside-catalog dispositions

- `backend`: no current application surface, confirmed by negative enumeration
  across eleven language extensions. Retain as a forward-looking scope, but
  treat application as not applicable until a lifecycle chain creates one. No
  intake record covers it, so it is undecided rather than deferred.
- `entry`: live gateway subject matter is absorbed by `infra-implementer`
  through adjacent infra ownership; the missing typed route remains a Stage 00
  ownership gap.
- `frontend`: one Storybook and Next fixture of 51 tracked files exists as a
  QA/review artifact, not as proof of a product frontend; route current work
  through its existing owner. This is materially different from `backend` and
  `mobile` and must not be collapsed into them.
- `meta`: metadata and taxonomy are the most heavily typed of the six —
  25 artifact profiles, 3 README profiles, and 3 governed families in
  `agent-governance-artifacts.yaml` — yet the scope value itself cannot appear
  in a catalog record. This is the widest gap between subject implementation
  and catalog reachability in the matrix.
- `mobile`: no current source surface, confirmed by negative enumeration.
  Retain only as forward-looking guidance until policy decides whether to
  instantiate or retire the route.
- `product`: the Stage 01 corpus exists and the catalog carries an explicit,
  sourced, dated `defer` on the product-discovery capability with
  `workflow-supervisor` as owner. Human approval remains essential, and the
  deferral is the governing record rather than an omission.

### Adoption environment and rules

1. Enter through the persona/scope file, then resolve a typed agent and a
   concrete ownership row before mutation. Check all three ownership surfaces,
   because they are disjoint and can disagree. If no typed route exists, use
   the adjacent owner shown above only where Stage 00 already assigns it;
   otherwise stop for an ownership decision.
2. Route research adoption to Stage 01 requirements, Stage 02 decisions, Stage
   03 specifications, Stage 04 execution, or Stage 05 policy/operations as
   appropriate. This matrix cannot authorize the change.
3. Validate by change type. Definition, local execution, runtime state, remote
   enforcement, and provider behavior remain separate evidence classes.
4. Preserve the secret/private/runtime/remote boundary. No scope disposition
   authorizes secret-value inspection, service mutation, or remote changes.
5. Reconcile catalog scope values and agent records through the Stage 00 typed
   owner and provider projections; do not patch one adapter independently.
6. Treat a scope's stated stack, threshold, or SLO as an aspiration until a
   tracked surface binds to it. Eight of the fourteen scope files are base-tier
   standard sheets, and three of those describe stacks with no tracked file.
7. When a function's scope differs from its owner agent's scope, cite both.
   Four of twenty-four functions are cross-scope owned, and citing only one
   side misroutes the work.

### Implementation status, limitations, and gap owners

The matrix covers 14 of 14 normative scopes. Seven have an enum value with both
agent and function records; one (`architecture`) has an enum value with
functions but no agent; four are outside the enum with tracked subject
surfaces; two are outside the enum with no tracked surface. Current
subject-matter states are two `Not Applicable` (`backend`, `mobile`), one fully
tracked contract surface (`agentic`), one implemented corpus-and-validator
surface (`docs`), one implemented definition surface (`infra`), and nine
partial or tracked-with-unverified-outcome dispositions.

The first owner of the reachability gap is the Stage 00 agent catalog, not this
Stage 90 document. Named gaps and their closing observations:

| Gap                                                                        | First owner                   | Closing observation                                                                                                   |
| -------------------------------------------------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Six persona values unreachable from the typed enum                         | Stage 00 catalog owner        | A contract change, or a recorded decision that the axes are intentionally different sizes.                            |
| `architecture` carries functions but no agent                              | Stage 00 catalog owner        | Either an `architecture`-scope agent record, or a decision that cross-scope function ownership is the intended model. |
| Fourteen-file axis never reconciled with the eight-value enum by any check | Stage 00 validator/test owner | A validator that reads the scopes directory and the enum together.                                                    |
| `docs` omitted from the scope-frontmatter test tuple                       | Stage 00 validator/test owner | Adding the fourteenth name and observing the suite still pass.                                                        |
| Prose ownership tables unvalidated and disjoint from typed authority       | Stage 00 catalog owner        | A validator over the prose tables, or a decision that typed authority supersedes them.                                |
| Two prose ownership conflicts on `docs/05.operations/` paths               | Stage 00 catalog owner        | A single owner recorded in one place, with the other file updated to read-only.                                       |
| `common/`, `lib/`, `shared/` claimed but absent                            | Stage 00 catalog owner        | Either instantiating the roots or removing the claim.                                                                 |
| `backend`, `entry`, `frontend`, `meta`, `mobile` have no intake record     | Stage 00 catalog owner        | Intake decisions comparable to the `product-discovery` deferral.                                                      |
| Applied remote enforcement of any ownership rule                           | repository owner              | Authenticated `gh api` readback of rulesets and required reviews.                                                     |

Architecture protocol adoption routes through Stage 02/03; backend and mobile
applicability requires a product and specification decision; product ownership
is already deferred by a dated record; entry, meta, and frontend continue
through their already-declared adjacent path owners unless Stage 00 changes.
Runtime, remote, private, and provider-native gaps remain unverified until
separately approved evidence exists.

## Sources

| Source                                                                                                 | Accessed   | Class                  | Verification state                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------ | ---------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Persona protocol](../../../00.agent-governance/rules/persona.md)                                      | 2026-08-14 | Tracked mutable        | Re-read in full; fourteen persona-to-scope rows at lines 25-38; unchanged since 2026-05-15.                                                                                                                                         |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)                             | 2026-08-14 | Tracked mutable        | Fully parsed; 8 scope values, 14 agents, 24 functions, 9 intake decisions. Confirmed by an executed validator run.                                                                                                                  |
| [Governance artifact contract](../../../00.agent-governance/contracts/agent-governance-artifacts.yaml) | 2026-08-14 | Tracked mutable        | Newly cited. 7 `path_authority` records, 25 artifact profiles, 3 README profiles, 3 governed families.                                                                                                                              |
| [Provider-model contract](../../../00.agent-governance/contracts/provider-models.yaml)                 | 2026-08-14 | Tracked mutable        | Parsed for projection targets; unchanged since 2026-07-26.                                                                                                                                                                          |
| [All scope files](../../../00.agent-governance/scopes/)                                                | 2026-08-14 | Tracked mutable        | All fourteen read in full; structural tiers, sizes, and ownership tables derived directly.                                                                                                                                          |
| [Governance contract validator](../../../../scripts/validation/check-agent-governance-contract.py)     | 2026-08-14 | Local observation      | Newly cited. Executed; `PASS` in both modes under an isolated environment, dependency-blocked by default.                                                                                                                           |
| [Governance contract tests](../../../../tests/validation/test_agent_governance_contract.py)            | 2026-08-14 | Local observation      | Newly cited. 159 tests `OK`; `scope_names` at lines 1955-1967 enumerates 13 of 14 scopes.                                                                                                                                           |
| [Contract validator module](../../../../scripts/validation/agent_governance_contract.py)               | 2026-08-14 | Tracked mutable        | Newly cited. Scope-enum membership enforced at lines 2661 and 2778 against the catalog's own list only.                                                                                                                             |
| [Repository contract script](../../../../scripts/validation/check-repo-contracts.sh)                   | 2026-08-14 | Tracked mutable        | Newly cited. Scans the scopes directory for path placeholders; requires 11 CODEOWNERS patterns.                                                                                                                                     |
| [`.github/CODEOWNERS`](../../../../.github/CODEOWNERS)                                                 | 2026-08-14 | Tracked mutable        | Newly cited. 30 path rules, all assigning one GitHub account; no scope or agent vocabulary.                                                                                                                                         |
| [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)                                | 2026-08-14 | Tracked fixed baseline | Re-verified; REQ-32 and the pack leaf list are unchanged.                                                                                                                                                                           |
| [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)         | 2026-08-14 | Tracked mutable        | Re-verified; REQ-32's derivations are unchanged.                                                                                                                                                                                    |
| [Workspace baseline](./workspace-baseline.md)                                                          | 2026-08-14 | Tracked draft          | Companion measured inventory; re-derived at `ece3eda9`.                                                                                                                                                                             |
| [Backstage descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/)  | 2026-08-14 | External mutable       | Newly cited. `spec.owner` required per kind; `type` taxonomy explicitly open; owners not for runtime authorization.                                                                                                                 |
| [A2A protocol specification](https://github.com/a2aproject/A2A)                                        | 2026-08-14 | External mutable       | Newly cited. Agent Card separates protocol `capabilities` from functional `skills`; undeclared capability MUST error.                                                                                                               |
| [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)               | 2026-08-14 | External mutable       | Newly cited. Per-request capability negotiation; opt-in extensions; cannot enforce its principles at protocol level.                                                                                                                |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                               | 2026-08-14 | External fixed         | Re-fetched; live. Published February 2022; leaves tool and owner choice to the adopting organization.                                                                                                                               |
| ISO/IEC 42001 landing page                                                                             | 2026-08-14 | External, unretrieved  | Direct retrieval returned HTTP 403, the known `iso.org` refusal. No claim here depends on it.                                                                                                                                       |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                            | 2026-08-08 | Tracked stale/advisory | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                                                                  |
| Predecessor scope matrix, retiring 2026-07-05 pack                                                     | 2026-08-14 | Historical retained    | Read for structural comparison only; its dispositions were re-derived rather than carried forward. Cited without a path because pre-deletion gate 4 admits no clickable link and the canonical router surface carries no allowlist. |

## Maintenance

Re-run the sorted scope-file query and parse all three typed contracts whenever
persona scopes, catalog enums, agents, functions, path-authority records, prose
ownership tables, or provider projections change. Re-measure path counts when
relevant surfaces are added, removed, or renamed. Re-check the three ownership
surfaces against one another whenever any of them is edited, since no validator
does it. A later topic leaf may refine applicability, but it must retain an
explicit disposition for every scope and link back to this matrix.

## Related Documents

- [Workspace baseline](./workspace-baseline.md)
- [Verification and validation](./verification-validation.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Agent governance hub](../../../00.agent-governance/README.md)
- [Research category router](../README.md)
