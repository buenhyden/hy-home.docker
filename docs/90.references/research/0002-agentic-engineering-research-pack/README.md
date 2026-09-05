---
title: "Agentic Engineering Research Pack"
version: "2.2.0"
type: "reference/research-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0002"
parent_ids:
- "SPEC-0158"
created: "2026-08-28"
observed_at: "2026-09-05"
---

# Agentic Engineering Research Pack

## Question

How should this repository structure an agentic workspace, spec-driven SDLC,
operations corpus, documentation architecture, Compose platform, quality
system, and security controls so that every claim has one canonical owner and
an explicit evidence depth?

The detailed questions are:

1. Which provider-neutral behavior belongs to Stage 00, and which Claude or
   Codex behavior must remain a native adapter concern?
2. How should instructions, model routing, catalogs, loops, memory, handoff,
   hooks, context, cost, and editor integration be governed and verified?
3. How do Requirement, Architecture/ADR, Spec, Plan, Task, Operations, and
   Stage 90 evidence differ in ownership, lifecycle, and substitution rules?
4. Which Diátaxis, C4, arc42, ADR, README, and generated-navigation practices
   improve discovery without creating parallel authority?
5. What do the tracked Compose, CI/CD, QA, verification, and security surfaces
   prove, and what still requires runtime, provider, or remote observation?

This package can identify gaps and route recommendations. It cannot approve
policy, implementation, provider entitlement, deployment, release, or residual
risk on behalf of their current owners.

## Scope

- Repository: `buenhyden/hy-home.docker`.
- Comparison branch and commit: `main` at
  `71da6654e2fa3def174b238ad309c92fe46e9dae`. The earlier assessed baseline
  `4c6d211129615eab372d720ebd209b6c27618c86` stays preserved in the dated
  member revalidations and in RES-0085; it is not rewritten into current state.
- Repository observation date and external-source confirmation date:
  2026-09-05.
- Observation checkout scope: an isolated `main`-only clone and a developer
  clone holding unmerged local branches. The two disagree on one registered
  check at the same commit, so both readings are recorded rather than one being
  presented as the repository verdict.
- Included: `docs/00.agent-governance/`, Stages 01, 02, 03, 05, 90, 98, and
  99; root entrypoints; `.agents/`, `.claude/`, `.codex/`, workflows, Compose
  declarations, scripts, tests, and generated navigation ownership.
- Included external families: official Claude Code, OpenAI Codex, GitHub,
  Docker, MCP, Diátaxis, C4, arc42, GitHub Spec Kit, ISO public definitions,
  NIST SSDF, SLSA, and upstream agency-agents material.
- Excluded: secret or credential values, user-global provider configuration,
  shell history, raw logs, unapproved provider/runtime mutation, new live
  deployment, tag, and release.
- Evidence boundary: configuration is not execution; local execution is not
  Hosted CI; Hosted CI is not deployment; point-in-time entitlement is not a
  future guarantee; tracked protection intent is not remote enforcement.
- [m0020](m0020-workspace-baseline.md) owns the current repository-local
  baseline. [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md)
  preserves the dated 2026-09-05 assessment scope and identity-recovery
  evidence. [RES-0084](../0084-github-actions-platform/README.md) owns detailed
  GitHub Actions platform mechanics. This package owns topical research and
  their cross-category navigation.

## Method

1. Enumerate every active research package and member by path, title,
   `artifact_id`, `parent_ids`, lifecycle metadata, headings, links, and
   observation date before allocating or restructuring anything.
2. Search filenames and bodies for the requested terms, synonyms, acronyms,
   old Stage 04 routes, outdated counts, duplicated claims, conflicting
   evidence, and `UNVERIFIED` boundaries.
3. Read the current canonical Requirement, Architecture/ADR, Spec/Task,
   Operations, audit, data, Registry, template, validator, workflow, and
   generated-output owners instead of inheriting repository truth from Stage
   90 prose.
4. Re-open mutable external claims from official primary sources on
   2026-09-05. Retain older fixed-commit or dated observations as historical
   evidence and label any unrefreshed claim accordingly.
5. Classify adoption as Defined, Configured, Local-executed,
   Repository-enforced, Runtime-verified, Remote-verified, or Unverified.
6. Treat a duplicate as the same question, evidence model, lifecycle, and
   decision route. Update that owner in place; create a package only when all
   four differ materially.
7. Run focused document/reference checks, generated-index freshness, link and
   lifecycle checks, then the canonical full gate. Keep local, Hosted,
   provider, runtime, and remote results in separate evidence rows.

### Existing Artifact Decision Record

| Existing artifact | Related requested categories | Current problem | Decision | Target artifact |
| --- | --- | --- | --- | --- |
| RES-0002 README | A–G navigation and cross-category summary | Detailed claims, sources, and historical routing duplicated member content | Rewrite as question/scope/method/router/traceability owner | RES-0002 README, same identity |
| RES-0002-m0001–m0020 | All topical categories | Strong historical analysis but observation metadata and several current routes were stale | Preserve IDs and content; add current revalidation evidence | Same 20 members |
| RES-0084 | GitHub Actions, CI, remote enforcement | Platform analysis predated the aggregate-check rollout | Update adoption and evidence boundary in place | RES-0084 |
| RES-0085 | Current `main` baseline | Its question duplicated the current-baseline purpose already owned by m0020 | Consolidate current ownership into m0020; preserve RES-0085 as dated recovery evidence in `review` | RES-0002-m0020 and RES-0085 evidence |
| New RES-0096 candidate | Same question set | Would duplicate existing owners and observation cycle | Do not create | None |

### 2026-09-05 Baseline 71da6654 Decision Record

This pass re-observed the same question set at
`main@71da6654e2fa3def174b238ad309c92fe46e9dae` and made no structural change.
Every requested category already resolved to exactly one owning member, so the
package identity, member identities, `created` values, and the member
allocation below are unchanged.

| Existing artifact | Related requested categories | Current problem | Decision | Target artifact |
| --- | --- | --- | --- | --- |
| RES-0002 README | A–G navigation | Scope cited a baseline three commits behind `main` | Advance the current-baseline pointer; preserve the dated one | RES-0002 README, same identity |
| RES-0002-m0006 | B12, D10, D11 | Identity-space evidence for `SPEC-0173` was unrecorded | Leave the member untouched while SPEC-0172 work is in flight; record the observation with the verification owner instead | RES-0002-m0019 |
| RES-0002-m0014 | F1–F13 | A quoted gate verdict carried no checkout identity | Add a dated reproduction qualifier; route analysis to m0019 | RES-0002-m0014 |
| RES-0002-m0019 | F14–F18 | Verification determinism across checkouts was unanalyzed | Add the three-environment comparison as the canonical analysis | RES-0002-m0019 |
| RES-0002-m0020 | A3, A20 | Current-baseline pointer lagged the delta | Advance the pointer and record the delta effect | RES-0002-m0020 |
| RES-0002-m0001–m0005, m0007–m0013, m0015–m0018 | Remaining categories | No owner changed in the delta | Preserve unchanged; no re-dating without re-observation | Same members |
| RES-0084 | E7, E9 | Its dated observations are outside this delta | Leave unchanged | RES-0084 |
| RES-0085 | Dated request scope | Its `4c6d2111` citations are its purpose | Do not update; preserving the dated baseline is the reason it exists | RES-0085 |
| New research package candidate | Same question set | Would duplicate owners that already exist | Do not create | None |

The one substantive addition is that a local gate verdict is checkout-relative:
at this single commit the full profile passes in an isolated `main`-only clone
and fails in a developer clone that can reach an unmerged branch. Both readings
are recorded. The repository contract that this observation touches belongs to
Stage 00 and Stage 99, so the follow-up runs through the normal
Requirement-to-Task chain rather than through this package.

## Findings

### Member Navigation

| Category | Member | Core question | Repository state | Evidence depth | Priority |
| --- | --- | --- | --- | --- | --- |
| Instructions and prompt hierarchy | [m0001](m0001-agent-instructions-vibe-coding.md) | How are durable instructions separated from ad-hoc prompts? | Root adapters load Stage 00; hooks enforce selected boundaries | Defined, Configured, Repository-enforced | High |
| Model routing | [m0002](m0002-agent-model-selection.md) | How should task class select provider/model/effort? | Work profiles are registered; quality/cost effectiveness is unmeasured | Configured, Repository-enforced, Unverified effectiveness | High |
| Agent catalogs | [m0003](m0003-ai-agent-catalogs.md) | How are external roles admitted without copying authority? | 14 roles and 23 skills are canonical; external catalogs are research inputs | Repository-enforced | Medium |
| Automation and delivery | [m0004](m0004-automation-pipeline-workflow.md) | Where do hooks, CI, CD, promotion, and rollback differ? | CI aggregate gates exist; live deployment remains unverified | Configured, Repository-enforced, Hosted-executed | High |
| Compose infrastructure | [m0005](m0005-docker-compose-infrastructure.md) | What do profiles and service controls prove? | 28 selections render; four domain defects remain owner-routed | Configured, Local-executed, Repository-enforced | High |
| Metadata and lifecycle | [m0006](m0006-document-metadata-lifecycle.md) | How are identity, status, retention, and retirement enforced? | Common-six and profile lifecycle contracts are active | Repository-enforced | High |
| Documentation architecture | [m0007](m0007-documentation-architecture.md) | How should Diátaxis, C4, arc42, ADR, and README compose? | Selective composition exists; no parallel taxonomy is required | Defined, Configured | Medium |
| Harness engineering | [m0008](m0008-harness-engineering.md) | Which controls make agents effective and bounded? | Canonical roles/skills/adapters/hooks are enforced; outcomes are partly observed | Repository-enforced, Runtime-verified in bounded probes | High |
| LLM Wiki | [m0009](m0009-llm-wiki-system.md) | How can generated navigation remain non-authoritative and fresh? | Generator ownership and freshness checks are active | Repository-enforced | Medium |
| Loop engineering | [m0010](m0010-loop-engineering.md) | How are discovery, retry, stop, review, and handoff bounded? | Stage 00 defines the loop; live provider equivalence is unverified | Defined, Repository-enforced | High |
| Memory | [m0011](m0011-memory-hierarchy.md) | What is durable, what expires, and who may delete it? | Task evidence exists; durable semantic memory lifecycle remains partial | Defined, Configured, Unverified | High |
| Provider comparison | [m0012](m0012-provider-implementation-comparison.md) | What is shared and what must stay Claude/Codex-native? | Shared control plane projects into native surfaces | Repository-enforced, point-in-time Runtime-verified | High |
| Provider/model landscape | [m0013](m0013-provider-model-landscape.md) | Which model, effort, fallback, entitlement, and cost claims are supportable? | Registry is configured; entitlement is dated and cost is unmeasured | Configured, point-in-time Runtime-verified | High |
| Quality and CI | [m0014](m0014-quality-ci-formatting.md) | Which quality layers block drift? | Registered local/full and Hosted aggregate gates exist | Local-executed, Repository-enforced, Hosted-executed | High |
| Scope application | [m0015](m0015-scope-application-matrix.md) | Where does every requested concern apply and who owns it? | All requested categories route to existing owners | Defined | Medium |
| SDLC document roles | [m0016](m0016-sdlc-document-roles.md) | What does each artifact own and never replace? | Registered roles and operations composition are enforced | Repository-enforced | High |
| Security | [m0017](m0017-security-governance.md) | Which controls are local, remote, runtime, or missing? | Static and supply-chain controls are strong; production posture is unverified | Repository-enforced, point-in-time Remote-verified | High |
| Spec-driven SDLC | [m0018](m0018-spec-driven-sdlc.md) | How does intent flow into verified work? | Current package form is enforced; intended-use acceptance remains owner-bound | Repository-enforced | High |
| Verification and validation | [m0019](m0019-verification-validation.md) | Does evidence prove conformance and intended use? | Conformance gates exist; deployment acceptance is absent | Local-executed, Repository-enforced | High |
| Workspace baseline | [m0020](m0020-workspace-baseline.md) | What is actually present at the repository boundary? | Current baseline and dated measurements are consolidated here; RES-0085 preserves recovery evidence | Configured, Local-executed | High |

### Complete Requested Category Routing

| Requested category | Owning member | Current status | Evidence depth | Principal gap |
| --- | --- | --- | --- | --- |
| A1 Harness engineering | [m0008](m0008-harness-engineering.md) | Partial | Repository-enforced | Outcome metrics absent |
| A2 Loop engineering | [m0010](m0010-loop-engineering.md) | Partial | Repository-enforced | Cross-provider outcome parity unverified |
| A3 Workspace harness, loop, rules, environment | [m0020](m0020-workspace-baseline.md) | Partial | Configured, Local-executed | Editor/runtime acceptance incomplete |
| A4 Claude Code implementation | [m0012](m0012-provider-implementation-comparison.md) | Adopted | Configured, point-in-time Runtime-verified | Full native event coverage partial |
| A5 Codex implementation | [m0012](m0012-provider-implementation-comparison.md) | Adopted | Configured, point-in-time Runtime-verified | Native hook surface is smaller |
| A6 Shared Claude/Codex governance | [m0012](m0012-provider-implementation-comparison.md) | Implemented | Repository-enforced | Behavioral equivalence unverified |
| A7 Provider-native differences | [m0012](m0012-provider-implementation-comparison.md) | Documented | Defined, Configured | Mutable upstream capabilities |
| A8 System prompt and command hierarchy | [m0001](m0001-agent-instructions-vibe-coding.md) | Implemented | Repository-enforced | Provider system prompts remain external |
| A9 Context loading and priority | [m0001](m0001-agent-instructions-vibe-coding.md) | Implemented | Defined, Configured | Runtime adherence is probabilistic |
| A10 Task-aware model selection | [m0002](m0002-agent-model-selection.md) | Implemented as policy | Repository-enforced | Outcome validation absent |
| A11 Model, effort, fallback, entitlement | [m0013](m0013-provider-model-landscape.md) | Partial | Configured, point-in-time Runtime-verified | Current entitlement/fallback not guaranteed |
| A12 Agent catalog and agency-agents | [m0003](m0003-ai-agent-catalogs.md) | Partial | Repository-enforced | No automatic external intake |
| A13 Roles, capabilities, tools, permissions | [m0003](m0003-ai-agent-catalogs.md) | Implemented structurally | Repository-enforced | Runtime least-privilege proof partial |
| A14 Agent memory hierarchy | [m0011](m0011-memory-hierarchy.md) | Partial | Defined, Configured | No single durable semantic-memory authority |
| A15 Short-, long-, domain-memory | [m0011](m0011-memory-hierarchy.md) | Partial | Defined | Long/domain lifecycle incomplete |
| A16 Memory promotion, retention, expiry, privacy, deletion | [m0011](m0011-memory-hierarchy.md) | Gap | Defined | Enforced lifecycle absent |
| A17 Claude/Codex context sharing | [m0012](m0012-provider-implementation-comparison.md) | Structural only | Configured | Semantic transfer acceptance unverified |
| A18 Session handoff and evidence sharing | [m0012](m0012-provider-implementation-comparison.md) | Partial | Defined, Repository-enforced | Live handoff quality unmeasured |
| A19 Test and CI agent hooks | [m0004](m0004-automation-pipeline-workflow.md) | Partial | Configured, Repository-enforced | Native parity differs |
| A20 Editor shortcuts, tasks, code actions | [m0020](m0020-workspace-baseline.md) | Gap | Unverified | No repository-wide contract |
| A21 Rate limit, cost, token, context management | [m0013](m0013-provider-model-landscape.md) | Partial | Configured | Direct cost/rate evidence absent |
| B1 Spec-driven development | [m0018](m0018-spec-driven-sdlc.md) | Implemented | Repository-enforced | Intended-use acceptance owner-bound |
| B2 SDLC purpose and necessity | [m0018](m0018-spec-driven-sdlc.md) | Defined | Defined | Effectiveness metric absent |
| B3 SDLC governance | [m0018](m0018-spec-driven-sdlc.md) | Implemented | Repository-enforced | None for registered scope |
| B4 Full SDLC lifecycle | [m0018](m0018-spec-driven-sdlc.md) | Implemented structurally | Repository-enforced | Deployment/release completion conditional |
| B5 Requirement-to-operations traceability | [m0016](m0016-sdlc-document-roles.md) | Implemented structurally | Repository-enforced | Runtime evidence remains separate |
| B6 PRD | [m0016](m0016-sdlc-document-roles.md) | Registered perspective | Repository-enforced | Not an independent package type |
| B7 SPEC | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | None for current form |
| B8 PLAN | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Must remain prospective |
| B9 TASK | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Must remain evidence-focused |
| B10 ADR | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Decision quality is reviewer-bound |
| B11 Ownership and non-substitution | [m0016](m0016-sdlc-document-roles.md) | Implemented | Repository-enforced | None for registered roles |
| B12 State transition, completion, supersession, retention, retirement | [m0006](m0006-document-metadata-lifecycle.md) | Implemented | Repository-enforced | Historical records remain separate |
| B13 Approval, review, independent-review boundary | [m0018](m0018-spec-driven-sdlc.md) | Implemented | Defined, Repository-enforced | Human acceptance remains owner-bound |
| C1 Guide | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Subject coverage varies |
| C2 Incident | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Event-created only |
| C3 Postmortem | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Requires resolved incident evidence |
| C4 Policy | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Subject coverage varies |
| C5 Release | [m0016](m0016-sdlc-document-roles.md) | Composed evidence | Defined | No independent profile |
| C6 Runbook | [m0016](m0016-sdlc-document-roles.md) | Registered | Repository-enforced | Runtime rehearsal varies |
| C7 Operations-document relationships | [m0016](m0016-sdlc-document-roles.md) | Implemented | Repository-enforced | None for registered topology |
| C8 Release evidence vs deployment evidence | [m0016](m0016-sdlc-document-roles.md) | Defined | Defined | No current release target |
| C9 Incident, recovery, postmortem, improvement traceability | [m0016](m0016-sdlc-document-roles.md) | Implemented structurally | Repository-enforced | Live incidents are event-dependent |
| D1 Diátaxis | [m0007](m0007-documentation-architecture.md) | Selectively applied | Defined, Configured | No full corpus classification needed |
| D2 C4 Model | [m0007](m0007-documentation-architecture.md) | Partial | Defined | View coverage is demand-driven |
| D3 arc42 | [m0007](m0007-documentation-architecture.md) | Partial | Defined | Not a parallel folder taxonomy |
| D4 ADR operating model | [m0016](m0016-sdlc-document-roles.md) | Implemented | Repository-enforced | Review quality remains human-bound |
| D5 LLM Wiki | [m0009](m0009-llm-wiki-system.md) | Implemented | Repository-enforced | Graphify snapshot remains advisory/stale |
| D6 Generated index vs authored-document boundary | [m0009](m0009-llm-wiki-system.md) | Implemented | Repository-enforced | Generated files require owner command |
| D7 README purpose and role | [m0007](m0007-documentation-architecture.md) | Implemented | Repository-enforced | Legacy prose can still age |
| D8 Repository/stage/package/service README differences | [m0007](m0007-documentation-architecture.md) | Implemented | Repository-enforced | Service coverage varies |
| D9 Documentation navigation | [m0007](m0007-documentation-architecture.md) | Implemented | Configured, Repository-enforced | Graph noise remains advisory |
| D10 Duplication prevention and canonical ownership | [m0006](m0006-document-metadata-lifecycle.md) | Implemented structurally | Repository-enforced | Semantic duplication still needs review |
| D11 Metadata and document lifecycle | [m0006](m0006-document-metadata-lifecycle.md) | Implemented | Repository-enforced | None for active registered corpus |
| E1 Docker Compose | [m0005](m0005-docker-compose-infrastructure.md) | Implemented statically | Configured, Local-executed | Live service acceptance absent |
| E2 Service boundaries and profiles | [m0005](m0005-docker-compose-infrastructure.md) | Implemented with known defects | Repository-enforced | AUD-0097 remains open |
| E3 Network, volume, secret, healthcheck | [m0005](m0005-docker-compose-infrastructure.md) | Partial | Configured, Repository-enforced | Runtime behavior unverified |
| E4 Configuration vs runtime state | [m0005](m0005-docker-compose-infrastructure.md) | Explicitly separated | Defined | No new runtime observation |
| E5 Continuous Integration | [m0004](m0004-automation-pipeline-workflow.md) | Implemented | Repository-enforced, Hosted-executed | Point-in-time Hosted evidence |
| E6 Continuous Delivery/Deployment | [m0004](m0004-automation-pipeline-workflow.md) | Partial / gap | Defined | No live target or promotion acceptance |
| E7 GitHub Actions | [m0004](m0004-automation-pipeline-workflow.md) | Implemented for CI | Configured, Hosted-executed | See RES-0084 for platform detail |
| E8 Promotion, release, deployment, rollback | [m0004](m0004-automation-pipeline-workflow.md) | Partial | Defined, Configured rehearsal | No current production target/version |
| E9 Remote control plane and branch protection | [m0004](m0004-automation-pipeline-workflow.md) | Verified at cutoff | Remote-verified | Later drift requires new read-back |
| E10 Operational readiness and recoverability | [m0005](m0005-docker-compose-infrastructure.md) | Partial | Repository-enforced | Four owner-routed defects, no live rehearsal |
| F1 Quality Assurance | [m0014](m0014-quality-ci-formatting.md) | Implemented structurally | Repository-enforced | Intended-use acceptance separate |
| F2 Formatting | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced | Tool-version drift monitored |
| F3 Linting | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced | Surface-specific coverage |
| F4 Syntax validation | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced | Runtime semantics separate |
| F5 Static analysis | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced, Hosted-executed | Remote configuration can drift |
| F6 Unit test | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced | Coverage varies by domain |
| F7 Integration test | [m0014](m0014-quality-ci-formatting.md) | Partial | Repository-enforced | Live external integration limited |
| F8 Contract test | [m0014](m0014-quality-ci-formatting.md) | Implemented strongly | Repository-enforced | Runtime contracts remain separate |
| F9 Regression test | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced | Historical gap-specific coverage |
| F10 Coverage | [m0014](m0014-quality-ci-formatting.md) | Partial | Hosted-executed for Storybook | Repository-wide threshold absent |
| F11 Pre-commit hook | [m0014](m0014-quality-ci-formatting.md) | Implemented | Configured, Repository-enforced in CI | Local installation is user-dependent |
| F12 Local validation | [m0014](m0014-quality-ci-formatting.md) | Implemented | Local-executed | Point-in-time result |
| F13 CI quality gate | [m0014](m0014-quality-ci-formatting.md) | Implemented | Repository-enforced, Hosted-executed | Hosted future runs can vary |
| F14 Verification | [m0019](m0019-verification-validation.md) | Implemented | Repository-enforced | Evidence remains artifact-specific |
| F15 Validation | [m0019](m0019-verification-validation.md) | Partial | Defined | Intended-use owner evidence varies |
| F16 Intended-use acceptance | [m0019](m0019-verification-validation.md) | Partial | Unverified for deployment | Exact target absent |
| F17 Residual risk | [m0019](m0019-verification-validation.md) | Owner-bound | Defined | No universal acceptance authority |
| F18 Revalidation and monitoring | [m0019](m0019-verification-validation.md) | Partial | Configured | Mutable external/runtime state |
| G1 Security governance | [m0017](m0017-security-governance.md) | Implemented structurally | Repository-enforced | Production acceptance absent |
| G2 Secret and credential handling | [m0017](m0017-security-governance.md) | Implemented as boundary | Defined, Repository-enforced | Secret stores not inspected |
| G3 Least privilege | [m0017](m0017-security-governance.md) | Partial | Configured, Repository-enforced | Runtime identity proof varies |
| G4 Supply-chain security | [m0017](m0017-security-governance.md) | Implemented for registered sample | Repository-enforced | Full service fleet provenance absent |
| G5 Dependency analysis | [m0017](m0017-security-governance.md) | Partial | Repository-enforced | Ecosystem breadth varies |
| G6 Code/infrastructure static analysis | [m0017](m0017-security-governance.md) | Implemented | Repository-enforced, Hosted-executed | Runtime findings separate |
| G7 Approval boundaries | [m0017](m0017-security-governance.md) | Implemented | Defined, Repository-enforced | Provider enforcement differs |
| G8 Audit evidence | [m0017](m0017-security-governance.md) | Implemented structurally | Repository-enforced | Live platform audit log not inspected |
| G9 Local security validation vs remote enforcement | [m0017](m0017-security-governance.md) | Explicitly separated | Local-executed, Remote-verified at cutoff | Later drift possible |
| G10 Runtime security state | [m0017](m0017-security-governance.md) | Unverified | Unverified | No live deployment observation |
| G11 Security readiness and gaps | [m0017](m0017-security-governance.md) | Partial | Defined, Repository-enforced | AUD-0097 and production posture remain |

No requested category is missing. The principal conclusion changes since the
prior research are the merged document-contract lifecycle/common-six corpus,
the consolidation of current baseline ownership into m0020 while RES-0085
preserves dated recovery evidence, Hosted acceptance of both aggregate CI
routes, and the 2026-09-05 remote protection read-back. Those changes
strengthen repository evidence but do not close live deployment,
persistent-memory, editor-integration, cost, or provider-outcome gaps.

## Sources

Common official sources re-opened on 2026-09-05:

- [Claude Code feature model](https://code.claude.com/docs/en/features-overview),
  [hooks](https://code.claude.com/docs/en/hooks),
  [subagents](https://code.claude.com/docs/en/sub-agents), and
  [memory](https://code.claude.com/docs/en/memory).
- [OpenAI Codex app architecture](https://openai.com/index/introducing-the-codex-app/),
  [Codex safety controls](https://openai.com/index/running-codex-safely/), and
  [harness engineering](https://openai.com/index/harness-engineering/).
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture).
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use),
  [OIDC](https://docs.github.com/en/actions/reference/security/oidc), and
  [ruleset status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [Docker Compose specification](https://docs.docker.com/compose/compose-file/),
  [services and healthchecks](https://docs.docker.com/reference/compose-file/services/),
  [profiles](https://docs.docker.com/compose/how-tos/profiles/), and
  [secrets](https://docs.docker.com/reference/compose-file/secrets/).
- [Diátaxis](https://diataxis.fr/), [C4 Model](https://c4model.com/), and
  [arc42 documentation](https://arc42.org/documentation/).
- [GitHub Spec Kit](https://github.github.com/spec-kit/),
  [ISO 29148 public terminology](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:29148:ed-2:v1:en),
  [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final), and
  [SLSA 1.2](https://slsa.dev/spec/v1.2/).
- [agency-agents division authority](https://github.com/msitarzewski/agency-agents/blob/main/divisions.json).

Repository sources:

- Baseline commit `71da6654e2fa3def174b238ad309c92fe46e9dae`, with the earlier
  assessed baseline `4c6d211129615eab372d720ebd209b6c27618c86` preserved as
  dated evidence.
- [Stage 00](../../../00.agent-governance/README.md),
  [Stage 99 Registry](../../../99.templates/registry.json),
  [Stage 03](../../../03.specs/README.md), and
  [Stage 05](../../../05.operations/README.md).
- [Workflow contract](../../../../.github/workflow-contract.yml),
  [CI workflow](../../../../.github/workflows/ci-quality.yml), and
  [main protection record](../../../../.github/rulesets/main-protection.md).
- [Implementation audits](../../audits/README.md),
  [Compose profile data](../../data/0059-compose-profile-service-coverage/README.md),
  [LLM Wiki index](../../data/0082-llm-wiki-index/README.md), and
  [repository map](../../data/0083-repository-map/README.md).

Each member owns its detailed claim and source inventory. This package-level
list contains only sources shared across categories.

## Implications

1. Preserve Stage 00 as provider-neutral policy and Stage 99 as document
   contract authority; do not promote Stage 90 findings into either owner.
2. Keep the 20-member topical split. It maps the full request without adding a
   competing package or making the README repeat detailed analysis.
3. Preserve the two aggregate CI checks and their app binding while current
   read-back matches. Use the recorded 12-check rollback on mismatch.
4. Route durable memory lifecycle, editor tasks/actions, cost/rate evidence,
   broad supply-chain provenance, Compose defect closure, and production
   deployment/release acceptance through separate approved SDLC work.
5. Apply Diátaxis, C4, and arc42 as reader/viewpoint tools inside current
   owners; do not introduce a second documentation tree.
6. Keep every recommendation on this route:
   Research → Requirement → Architecture/ADR → Spec → Plan → Task →
   Verification → Independent Review.

## Traceability

- Members: [m0001](m0001-agent-instructions-vibe-coding.md),
  [m0002](m0002-agent-model-selection.md),
  [m0003](m0003-ai-agent-catalogs.md),
  [m0004](m0004-automation-pipeline-workflow.md),
  [m0005](m0005-docker-compose-infrastructure.md),
  [m0006](m0006-document-metadata-lifecycle.md),
  [m0007](m0007-documentation-architecture.md),
  [m0008](m0008-harness-engineering.md),
  [m0009](m0009-llm-wiki-system.md),
  [m0010](m0010-loop-engineering.md),
  [m0011](m0011-memory-hierarchy.md),
  [m0012](m0012-provider-implementation-comparison.md),
  [m0013](m0013-provider-model-landscape.md),
  [m0014](m0014-quality-ci-formatting.md),
  [m0015](m0015-scope-application-matrix.md),
  [m0016](m0016-sdlc-document-roles.md),
  [m0017](m0017-security-governance.md),
  [m0018](m0018-spec-driven-sdlc.md),
  [m0019](m0019-verification-validation.md), and
  [m0020](m0020-workspace-baseline.md).
- Related research: [RES-0084](../0084-github-actions-platform/README.md) and
  dated baseline/recovery evidence in
  [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md).
- Policy: [Stage 00](../../../00.agent-governance/README.md) and
  [documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md).
- Requirements: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [REQ-0025](../../../01.requirements/0025-operational-readiness-closure.md), and
  [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md).
- Architecture/ADR: [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md),
  [AD-0028](../../../02.architecture/descriptions/0028-operational-readiness-closure.md),
  [AD-0030](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md),
  [ADR-0028](../../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [ADR-0029](../../../02.architecture/decisions/0029-workspace-governance-authority.md), and
  [ADR-0031](../../../02.architecture/decisions/0031-preserved-archive-record.md).
- Current Spec/Task: [SPEC-0172](../../../03.specs/0172-document-contract-convergence/spec.md)
  and [SPEC-0172-TSK-0001](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md).
- Operations: [Stage 05](../../../05.operations/README.md).
- Audit/data: [AUD-0026](../../audits/0026-implementation-overview/README.md),
  [AUD-0097](../../audits/0097-compose-domain-defect-register/README.md),
  [DATA-0082](../../data/0082-llm-wiki-index/README.md), and
  [DATA-0083](../../data/0083-repository-map/README.md).
- Package/index/template authority: [research index](../README.md),
  [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  [research-member template](../../../99.templates/templates/references/research.template.md),
  and [Registry](../../../99.templates/registry.json).

## Preservation Declaration

SPEC-0158 protects every file listed below even when it has no consumer. The
declaration is the durable path oracle; it contains no pinned count, hash, or
commit. Files may be corrected and expanded, but they are not deleted,
archived, tombstoned, or substantively reduced. A member-set change must update
this declaration atomically.

- `README.md`
- `m0001-agent-instructions-vibe-coding.md`
- `m0002-agent-model-selection.md`
- `m0003-ai-agent-catalogs.md`
- `m0004-automation-pipeline-workflow.md`
- `m0005-docker-compose-infrastructure.md`
- `m0006-document-metadata-lifecycle.md`
- `m0007-documentation-architecture.md`
- `m0008-harness-engineering.md`
- `m0009-llm-wiki-system.md`
- `m0010-loop-engineering.md`
- `m0011-memory-hierarchy.md`
- `m0012-provider-implementation-comparison.md`
- `m0013-provider-model-landscape.md`
- `m0014-quality-ci-formatting.md`
- `m0015-scope-application-matrix.md`
- `m0016-sdlc-document-roles.md`
- `m0017-security-governance.md`
- `m0018-spec-driven-sdlc.md`
- `m0019-verification-validation.md`
- `m0020-workspace-baseline.md`

Historical continuity is retained: the canonical pack was rebuilt under
SPEC-0158 in August 2026, all members received source refresh and deepening,
the loop coverage gap was repaired on 2026-08-17, and the 2026-09-05 renewal
preserves all identities and the exact member set. The subsequent baseline
consolidation changes no protected path and makes m0020 the single current
workspace-baseline owner.

## Limitations

- No user-global Claude/Codex configuration, secret, credential, private key,
  environment value, shell history, or raw log was read.
- No new provider call, Compose service start, deployment, rollback, tag, or
  release action was performed for this renewal.
- Provider entitlement and remote protection are point-in-time observations
  recorded by SPEC-0172; future state is not inferred.
- The clean full gate proves local conformance at the baseline commit, not
  production fitness, service health, durability, performance, or recovery.
- Four Compose domain defects remain in AUD-0097 even though all profiles can
  render statically.
- External sources are mutable after 2026-09-05. Purchased ISO text was not
  accessed; only public catalog and terminology material was used.
- The Graphify report predates the baseline and is noisy, so it is advisory;
  current generated LLM Wiki freshness is decided only by its registered
  generator and checks.
