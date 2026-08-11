---
status: draft
artifact_id: reference:agentic-engineering-research:scope-application-matrix
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-11
review_cycle: on-source-change
---

# Reference: Agentic Engineering Scope Application Matrix

## Overview

This reference is the scope-axis entry point for the agentic engineering
research pack. It dispositions all fourteen persona scopes defined by the
[persona protocol](../../../00.agent-governance/rules/persona.md), maps them to
the twenty planned research leaves, and separates real workspace surfaces from typed
catalog reachability.

At baseline commit `528c225d35d6c986b50f9b997fd08921a8df9a9b`, all fourteen
scope files exist. The [typed agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)
admits eight scope values. Six normative scopes are outside that enum:
`backend`, `entry`, `frontend`, `meta`, `mobile`, and `product`.
`architecture` is inside the enum but has no current agent record. Those are
different findings and must not be merged. Re-verified at commit
`55809319e462ed6ae9ed4a3f31055fc55c2a2294` on 2026-08-11: the fourteen scope
files, the eight-value enum, and every catalog/agent count below are unchanged.

## Purpose

Satisfy REQ-32 by giving every scope a current adoption or explicit
not-applicable disposition, including governed paths, applicable leaves,
implementation state, adoption rules and exceptions, evidence owner,
validation owner, and catalog reachability. Topic leaves can cite this matrix
without silently dropping a persona scope.

## Repository Role

This Stage 90 matrix is a research and routing aid. It reports current scope
applicability and gaps but does not alter the persona protocol, typed catalog,
File Ownership SSOT, lifecycle approvals, runtime configuration, or remote
enforcement.

## Scope

### In scope

- The fourteen tracked files under `docs/00.agent-governance/scopes/`.
- Persona-to-scope routing and the typed agent/function catalog.
- Tracked workspace surfaces named or governed by each scope.
- Applicability to all twenty leaves in the planned pack.

### Out of scope

- Adding a missing scope value, agent, function, or provider projection.
- Resolving ownership conflicts in Stage 00 policy.
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

External secure-development guidance such as NIST SSDF v1.1 assigns practices
and responsibilities, but repository scopes, agents, permissions, and stage
owners remain local contracts. External guidance is therefore a comparison
lens, never a catalog or adoption authority.

### Derivation commands and observations

The required derivations were run on 2026-08-08 at the baseline commit:

```bash
git ls-files > /tmp/agentic-research-tracked-paths.txt
find docs/00.agent-governance/scopes -maxdepth 1 -type f -name '*.md' \
  -printf '%f\n' | sort
sed -n '1,220p' docs/00.agent-governance/rules/persona.md
sed -n '1,220p' docs/00.agent-governance/contracts/agent-catalog.yaml
find docs/03.specs -mindepth 1 -maxdepth 1 -type d | wc -l
find docs/98.archive/03.specs -type f -name spec.md | wc -l
```

The results were 1,646 tracked paths; exactly 14 sorted scope filenames; 28
active Spec directories; and 32 archived `spec.md` files. Parsing the complete
typed catalog found 8 allowed scope values, 14 agent records, and 24 function
records. Agent records use 7 values: `agentic` 4, `common` 1, `docs` 1, `infra`
3, `ops` 2, `qa` 2, and `security` 1. Re-running the tracked-paths count on
2026-08-11 found 1,672 (repository growth unrelated to scope routing); the
scope, agent, function, and Spec-directory counts are unchanged.

### Catalog reachability finding

| Reachability class     | Scopes                                                        | Interpretation                                                                |
| ---------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Enum plus agent record | `agentic`, `common`, `docs`, `infra`, `ops`, `qa`, `security` | A current typed agent can declare the scope.                                  |
| Enum only              | `architecture`                                                | The value is legal, but no current agent record declares it.                  |
| Outside typed enum     | `backend`, `entry`, `frontend`, `meta`, `mobile`, `product`   | A catalog record cannot declare the value without a Stage 00 contract change. |

This is not a broken-link finding: every scope file exists and the persona
protocol routes to it. It is a typed delegation/reachability finding. For
`entry`, `frontend`, `meta`, and `product`, substantive tracked surfaces exist
despite the missing enum route. `backend` and `mobile` have no current
application surface matching their scopes.

## Scope Implications

Applicable leaf names below refer to the flat twenty-leaf pack contract in
[Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md).
`workspace-baseline.md` and this matrix apply to every row and are omitted from
the per-row leaf lists to keep the table readable.

| Scope and governance owner                                            | Governed or applicable paths/artifacts                                                                                            | Applicable topical leaves                                                                                                                                      | Current disposition                                                                                                                         | Adoption rules / exceptions                                                                                                                          | Evidence owner                                                                          | Validation owner                                                         | Catalog reachability     |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------ |
| [`agentic`](../../../00.agent-governance/scopes/agentic.md)           | Stage 00 catalogs/rules, root shims, `.claude/`, `.agents/`, `.codex/`, `.gemini/`, hooks                                         | harness, loop, provider comparison, instructions, provider/model landscape, model selection, AI catalogs, memory, automation, verification/validation          | **Implemented** as tracked contracts; provider loading/interception and model execution are **Unverified**                                  | Provider-neutral policy stays in Stage 00; provider-native mechanics stay in adapters; changes need approved Stage 03/04 ownership and parity checks | `hook-developer`, `skill-creator`; workflow supervision where applicable                | `rules-engineer`; repository contracts and provider-surface sync         | Enum + 4 agents          |
| [`architecture`](../../../00.agent-governance/scopes/architecture.md) | `docs/02.architecture/{requirements,decisions}/`, downstream Specs; no File Ownership SSOT row in this scope                      | spec-driven SDLC, document roles, Compose/infrastructure, security, automation, verification/validation                                                        | **Partial**: 53 Stage 02 files and 28 active Spec directories exist; mandated service protocols are not universal runtime proof             | Trade-offs route to ADRs; service boundaries route to Specs; protocol claims require a real service and tracked decision                             | System Architect persona; `infra-implementer` owns Stage 02 paths under the infra scope | Metadata/repository contracts plus an independent architecture review    | Enum only; 0 agents      |
| [`backend`](../../../00.agent-governance/scopes/backend.md)           | Future Node/Python/Go services; no matching tracked backend application found                                                     | quality, security, Compose/infrastructure, automation, verification/validation when a backend exists                                                           | **Not Applicable** to the current application corpus; catalog route is **Missing**                                                          | Do not apply stack, latency, ASVS, or 90% coverage claims until a backend surface and Spec exist                                                     | Backend Engineer persona; no typed agent                                                | Future layer owner plus QA/security reviewers; current code checks N/A   | Outside enum; 0 agents   |
| [`common`](../../../00.agent-governance/scopes/common.md)             | `.pre-commit-config.yaml`, shared conventions, `scripts/lib/`; claimed root `common/`, `lib/`, `shared/` are not all instantiated | instructions, metadata lifecycle, documentation architecture, quality, security, verification/validation                                                       | **Partial**: typed review route and 10 pre-commit repositories exist; some claimed shared-root patterns do not                              | Agents must not invoke direct pre-commit/lint/format; the controlled all-files wrapper is final-QA-only and approval-bound                           | Cross-layer implementer; shared review route is `code-reviewer`                         | `code-reviewer`, scoped checks, `git diff --check`                       | Enum + 1 agent           |
| [`docs`](../../../00.agent-governance/scopes/docs.md)                 | Stages 01-05, 90, 98, 99; root shims; metadata/template/link systems                                                              | spec-driven SDLC, document roles, metadata lifecycle, documentation architecture, LLM Wiki, memory, verification/validation; all leaves as authored references | **Implemented** as a tracked corpus and validator system; later route integration is pending                                                | Stage 01-99 is read-only by default; explicit approval, template-first authoring, direct links, and generated-index ownership apply                  | `doc-writer`                                                                            | Metadata/repository contracts plus independent documentation review      | Enum + 1 agent           |
| [`entry`](../../../00.agent-governance/scopes/entry.md)               | `infra/01-gateway/` (16 tracked files), Traefik/Nginx definitions                                                                 | Compose/infrastructure, security, automation, quality, verification/validation                                                                                 | **Partial**: gateway definitions exist; Cloudflare edge and live certificate/log forwarding are **Unverified**; typed route is **Missing**  | Route mutations through `infra-implementer`; validate config/Compose; runtime and certificate operations require concrete approval/evidence          | `infra-implementer` by adjacent infra ownership                                         | `iac-reviewer`, `drift-detector`, Compose/config checks                  | Outside enum; 0 agents   |
| [`frontend`](../../../00.agent-governance/scopes/frontend.md)         | `projects/storybook/` (51 tracked files), including 6 TSX/JSX files                                                               | quality, automation, security, instructions, verification/validation                                                                                           | **Partial**: a Storybook/Next fixture exists, but no general product frontend or catalog route is proven                                    | Treat the sandbox as QA-owned until a product Spec says otherwise; accessibility/performance outcomes need execution evidence                        | No typed frontend agent; Storybook path is assigned to `code-reviewer` by QA scope      | `code-reviewer` and frontend/Storybook quality gates                     | Outside enum; 0 agents   |
| [`infra`](../../../00.agent-governance/scopes/infra.md)               | 275 tracked `infra/` files, 11 numbered domains, root and domain Compose files, Stage 02 paths                                    | Compose/infrastructure, security, automation, quality, harness/provider environment, verification/validation                                                   | **Implemented** as tracked definitions; live service health, latency, backups, and secrets remain **Unverified**                            | Pre-flight Compose validation; concrete-target runtime approval with pre-check, rollback, and post-check; no secret values                           | `infra-implementer`                                                                     | `iac-reviewer`, `drift-detector`, Compose and repository contracts       | Enum + 3 agents          |
| [`meta`](../../../00.agent-governance/scopes/meta.md)                 | metadata profile registry, 33 template-tree files, metadata/corpus validators, staged taxonomy                                    | metadata lifecycle, documentation architecture, LLM Wiki, document roles, spec-driven SDLC, verification/validation                                            | **Partial**: subject is implemented, but typed meta route is **Missing**                                                                    | Route edits through `doc-writer`; use mapped templates; update indexes when authorized; significant folder changes require a Meta ADR                | `doc-writer` by adjacent docs ownership                                                 | metadata checker, corpus lifecycle, repository contracts                 | Outside enum; 0 agents   |
| [`mobile`](../../../00.agent-governance/scopes/mobile.md)             | No tracked Swift, Kotlin, Dart, Android, or iOS source matched the baseline query                                                 | quality, security, automation, verification/validation only after a mobile surface is approved                                                                 | **Not Applicable** to the current corpus; catalog route is **Missing**                                                                      | Do not claim React Native/Expo adoption, device verification, EAS deployment, or mobile accessibility without a surface and approved lifecycle chain | Mobile Engineer persona; no typed agent                                                 | Future mobile layer owner plus QA/security reviewers; current checks N/A | Outside enum; 0 agents   |
| [`ops`](../../../00.agent-governance/scopes/ops.md)                   | `docs/05.operations/` (263 files), `infra/06-observability/` (99), `scripts/operations/` (8)                                      | automation, quality, Compose/infrastructure, security, document roles, verification/validation                                                                 | **Partial**: tracked observability/operations surfaces exist; MTTR, availability, off-site backup, and drill outcomes are **Unverified**    | Live incident evidence stays in incident packets; runtime changes require the infra protocol; do not infer outcomes from config                      | `incident-responder`, `ci-cd-engineer`                                                  | Independent ops/infra review plus relevant local and remote gates        | Enum + 2 agents          |
| [`product`](../../../00.agent-governance/scopes/product.md)           | `docs/01.requirements/` (26 tracked files), PRD template/glossary routes                                                          | spec-driven SDLC, document roles, documentation architecture, verification/validation                                                                          | **Partial**: requirements corpus exists; typed product route and explicit File Ownership SSOT are **Missing**                               | Stakeholder approval precedes Spec; Stage 01 mutation needs explicit approval and template/metadata checks                                           | Product Manager persona/human stakeholder; no typed agent                               | Human approval plus documentation metadata/repository checks             | Outside enum; 0 agents   |
| [`qa`](../../../00.agent-governance/scopes/qa.md)                     | 41 validation files, 7 workflows/23 jobs, evaluation fixtures/regressions, Storybook/tests                                        | harness, loop, automation, quality, security, LLM Wiki, metadata lifecycle, verification/validation                                                            | **Partial**: extensive gates exist; current repository contract retains an unrelated Memory predecessor and remote gates are **Unverified** | Use the smallest applicable check; docs-only TDD/coverage is N/A; no direct pre-commit; record skipped checks and predecessors                       | `qa-engineer`                                                                           | `eval-engineer`; independent review and named repository gates           | Enum + 2 agents          |
| [`security`](../../../00.agent-governance/scopes/security.md)         | hardening/security scripts, supply-chain policies, incident routes, secret metadata boundaries                                    | security, Compose/infrastructure, quality, automation, harness/provider comparison, verification/validation                                                    | **Partial**: tracked controls exist; secret values, live runtime, and remote/provider enforcement are excluded or **Unverified**            | Metadata-only secret evidence; concrete target, redaction boundary, validation, and recovery path for approved secret/runtime work                   | Relevant layer implementer; `security-auditor` is read-only review                      | `security-auditor` plus hardening/template/quickwin/supply-chain gates   | Enum + 1 read-only agent |

### Six outside-catalog dispositions

- `backend`: no current application surface; retain as forward-looking scope,
  but treat application as not applicable until a lifecycle chain creates one.
- `entry`: live gateway subject matter is absorbed by `infra-implementer`; the
  missing typed route remains a Stage 00 ownership gap.
- `frontend`: Storybook/Next evidence exists as a QA/review fixture, not proof
  of a product frontend; route current work through its existing owner.
- `meta`: metadata and taxonomy are validator-backed and absorbed by `docs`;
  the missing typed route remains a catalog gap.
- `mobile`: no current source surface; retain only as forward-looking guidance
  until policy decides whether to instantiate or retire the route.
- `product`: Stage 01 corpus exists, but current catalog/ownership does not
  assign a typed implementation agent; human approval remains essential.

### Adoption environment and rules

1. Enter through the persona/scope file, then resolve a typed agent and concrete
   File Ownership SSOT before mutation. If no typed route exists, use the
   adjacent owner shown above only where Stage 00 already assigns it; otherwise
   stop for an ownership decision.
2. Route research adoption to Stage 01 requirements, Stage 02 decisions, Stage
   03 specifications, Stage 04 execution, or Stage 05 policy/operations as
   appropriate. This matrix cannot authorize the change.
3. Validate by change type. Definition, local execution, runtime state, remote
   enforcement, and provider behavior remain separate evidence classes.
4. Preserve the secret/private/runtime/remote boundary. No scope disposition
   authorizes secret-value inspection, service mutation, or remote changes.
5. Reconcile catalog scope values and agent records through the Stage 00 typed
   owner and provider projections; do not patch one adapter independently.

### Implementation status, limitations, and gap owners

The matrix covers 14 of 14 normative scopes. Seven have both a typed enum value
and at least one agent record; `architecture` is enum-only; six are outside the
enum. Current subject-matter states are two `Not Applicable` (`backend`,
`mobile`), one fully tracked contract surface (`agentic`), and eleven partial
or tracked-with-unverified-outcome dispositions.

The first owner of the reachability gap is the Stage 00 agent catalog, not this
Stage 90 document. Architecture protocol adoption routes through Stage 02/03;
backend/mobile applicability requires a product and specification decision;
product ownership requires an explicit governance decision; entry/meta/frontend
continue through their already-declared adjacent path owners unless Stage 00
changes. Runtime, remote, private, and provider-native gaps remain unverified
until separately approved evidence exists.

## Sources

| Source                                                                                                     | Accessed   | Class                  | Verification state                                                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | ---------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Persona protocol](../../../00.agent-governance/rules/persona.md)                                          | 2026-08-11 | Tracked mutable        | Re-verified directly; unchanged since 2026-08-08 access (last modified 2026-05-15); fourteen persona/scope mappings.                                                                               |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)                                 | 2026-08-11 | Tracked mutable        | Re-parsed at current HEAD; unchanged since 2026-08-08 access (last modified 2026-07-26); 8 scope values, 14 agents, 24 functions.                                                                  |
| [All scope files](../../../00.agent-governance/scopes/)                                                    | 2026-08-11 | Tracked mutable        | Re-read; fourteen sorted Markdown files confirmed at current HEAD.                                                                                                                                 |
| [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)                                    | 2026-08-11 | Tracked fixed baseline | Re-verified at current commit `af37969b` (2026-08-09); the amendment there adds REQ-36 and the twenty-one-file cardinality for `verification-validation.md`. REQ-32 and pack leaves are unchanged. |
| [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)             | 2026-08-11 | Tracked mutable        | Re-verified at current commit `0b9bd01b` (2026-08-10); later revisions add Gate 9/V&V evidence unrelated to REQ-32's derivations, which are unchanged.                                             |
| [Workspace baseline](./workspace-baseline.md)                                                              | 2026-08-11 | Tracked draft          | Companion measured inventory; re-derived at `55809319e4`.                                                                                                                                          |
| [NIST SP 800-218, Secure Software Development Framework v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 2026-08-08 | External fixed         | Direct primary page returned HTTP 200; comparison context only.                                                                                                                                    |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                | 2026-08-08 | Tracked stale/advisory | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                                 |

## Maintenance

Re-run the sorted scope-file query and parse the complete typed catalog whenever
persona scopes, catalog enums, agents, functions, File Ownership SSOT rows, or
provider projections change. Re-measure path counts when relevant surfaces are
added, removed, or renamed. A later topic leaf may refine applicability, but it
must retain an explicit disposition for every scope and link back to this
matrix.

## Related Documents

- [Workspace baseline](./workspace-baseline.md)
- [Verification and validation](./verification-validation.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Agent governance hub](../../../00.agent-governance/README.md)
- [Research category router](../README.md)
