---
title: "Repository Vocabulary"
version: "0.4.0"
type: "governance/vocabulary"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-12"
created: "2026-09-06"
observed_at: "2026-11-12"
review_cycle: "on-contract-change"
---

# Repository Vocabulary

## Purpose

This is the meaning owner for the shared governance terms used in this
repository. Each entry gives the meaning and names the policy that owns the
rule. The policy owns the procedure, the allowed commands, the state
transitions and the check algorithm; this file never restates them. A passing
check does not stand in for a policy approval or an owner acceptance.

## Scope

Included: the common terms that the four workspace repositories share at the
same Term ID and meaning, and the local terms that canonical governance, Stage
99 contracts, the workflow contract and validator output use with a narrower
meaning here. Excluded: general software terms used in their ordinary sense,
vendor product terms owned by the Provider Registry, and service-specific
names.

## Normative Language

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY in governance
documents are interpreted as described in RFC 2119 and RFC 8174 when, and only
when, they appear in all capitals. The authority behind a rule comes from the
user and the canonical owner named in
[Authority and Precedence](../governance/bootstrap.md#authority-and-precedence),
not from the RFCs. A stronger keyword does not make an unenforced rule
enforced.

## Repository Vocabulary

| Term ID | Term | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- |
| TERM-AUTHORITY | Authority | The decision maker and basis valid for a named scope, action and revision. A file's presence or a tool run does not create it | An execution result or a supported feature | [Approval boundaries](../governance/approval-boundaries.md) | v14.5 |
| TERM-GOVERNANCE | Governance | The system that sets who proposes, owns, approves, applies, excepts and changes a rule | An index that copies every policy body | [Agent governance index](../README.md) | v14.5 |
| TERM-POLICY | Policy | A current norm that states what is allowed, required, forbidden and excepted for a goal and scope | A single Task record | [Bootstrap](../governance/bootstrap.md#authority-and-precedence) | v14.5 |
| TERM-RULE | Rule | A norm under a policy that states a condition, the expected behavior and how a violation is judged | Changing only a check's expected value | [Bootstrap](../governance/bootstrap.md#authority-and-precedence) | v14.5 |
| TERM-CONTRACT | Contract | A versioned agreement between producer and consumer on meaning, inputs and outputs, invariants and verification | A particular implementation language | [Approval boundaries](../governance/approval-boundaries.md) | v14.5 |
| TERM-CANONICAL | Canonical Source | The single source with independent authoring authority for one meaning; a derived copy tracks its source and revision. Here, an authored file under `.agents/` | Merely having one copy | [Agent governance index](../README.md) | v14.5 |
| TERM-APPROVAL | Approval | A decision that grants authority to perform a named change or operation in a named scope | Acceptance, a passing check or a merged PR | [Approval boundaries](../governance/approval-boundaries.md) | v14.5 |
| TERM-ADOPTION | Adoption | Applying one revision of a shared contract to this workspace's producers and consumers and verifying it, recorded in this repository's own Task | Approval of the shared goal, or a configured surface alone (tracked configuration) | [Approval boundaries](../governance/approval-boundaries.md) | v14.5 |
| TERM-EXECUTION | Execution | An action performed on a real target, environment and revision | A plan, a proposed command or a declared setting | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-VERIFICATION | Verification | Confirming by observation, test or review that an output meets its stated requirement or contract | Validation or owner acceptance | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-VALIDATION | Validation | Confirming that an output meets its intended use and the actual need under the stated conditions | A tool merely named `validate` | [Quality standards](../governance/quality-standards.md) | v14.5 |
| TERM-ACCEPTANCE | Acceptance | An authorized owner's decision to accept a criterion and its evidence; required failures and exceptions keep their recorded handling | Approval, a merged PR, a runtime accepting a value, or a risk acceptance | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-COMPLETION | Completion | The scoped close of one work item once its required execution, checks and acceptance conditions hold. It does not close integration, deployment or another Task | Setting every status to completed | [Task checklists](../governance/task-checklists.md) | v14.5 |
| TERM-PROMOTION | Promotion | Handing an open change's lasting meaning to the current requirement, design, operations or governance owner through the Plan's mapping | Moving a file or copying a Task status | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-RETIREMENT | Retirement | Ending a document's current effect: its still-current meaning moves to its owner and the file is deleted once the retirement preconditions hold; Git history keeps the body | Unconditional deletion | [Documentation protocol](../governance/documentation-protocol.md#document-retention-and-retirement) | v14.5 |
| TERM-ARCHIVE | Archive | Preserving past evidence that is no longer normative. Here Git history is the archive and Stage 98 holds only its README | Equating a vault archive with ending development work | [Documentation protocol](../governance/documentation-protocol.md#document-retention-and-retirement) | v14.5 |
| TERM-REMOVAL | Removal | Deleting a file from the current tree after authority, holds, consumer handoff and recovery are confirmed | Rewriting Git history or destroying a source without a basis | [Documentation protocol](../governance/documentation-protocol.md#retirement-preconditions) | v14.5 |
| TERM-SUPERSESSION | Supersession | A newer owner taking over the valid scope of an earlier document or decision through a reciprocal lineage | A title change | [Documentation protocol](../governance/documentation-protocol.md) | v14.5 |
| TERM-HOLD | Preservation Hold | A recorded preservation condition that blocks disposal of a named source or evidence until it is resolved | A blanket stop on all work | [Documentation protocol](../governance/documentation-protocol.md#retirement-preconditions) | v14.5 |
| TERM-REGISTRY | Registry | The machine-readable contract for document profiles, forms, states, relations and template bindings, `docs/99.templates/registry.json`. Approved content stays open to reform | A frozen baseline | [Documentation protocol](../governance/documentation-protocol.md) | v14.5 |
| TERM-TEMPLATE | Template | The authoring form that implements one role's fields, headings, tables, relations and lifecycle | A copyable example or a heading list alone | [Documentation protocol](../governance/documentation-protocol.md) | v14.5 |
| TERM-PROFILE | Document Profile | A Registry entry binding a path pattern to the role's required frontmatter, sections, identity, lifecycle and template | A validation profile (`changed`, `full`) | [Documentation protocol](../governance/documentation-protocol.md) | v14.5 |
| TERM-TASK | Task | The single authored record of one scope's execution, blockers, observations, evidence and acceptance decision; other documents reference it | A progress table duplicated in a Plan | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-EVIDENCE | Evidence | The actual source, target revision, conditions and result that support a claim, labelled by the observation made: static, configured, native, hosted or operational | A memory summary or a planned command | [Output style](../governance/output-style.md) | v14.5 |
| TERM-RESOLVES | Resolves | A link stating that a later PASS row with the same Check and Work Unit meets the same obligation, inputs and guarantee as an earlier non-PASS row | A newer PASS erasing every failure | [SDLC](../governance/sdlc.md#sequence) | v14.5 |
| TERM-HISTORICAL-AUDIT | Historical Audit ID | A key such as OPEN-01 to OPEN-14 that names an item of an earlier audit. It is not a current state, file name or issue number | A currently open work item | This vocabulary; current verdicts live in the owning Task | v14.5 |
| TERM-HARNESS | Harness | The execution setup that connects instructions, routing, permissions, state, tools, observation, stop and recovery | An instruction file existing | [Agentic policy](../governance/agentic.md) | v14.5 |
| TERM-NATIVE-EVIDENCE | Native Runtime Evidence | A result observed in the installed provider, at its revision, through the actual tool path | A direct function test or vendor documentation | [Provider capability matrix](../governance/provider-capability-matrix.md) | v14.5 |
| TERM-PROJECTION | Projection | A consumer file generated from a canonical source and explicit local bindings; it has no policy authoring authority | An independent manual copy | [Providers index](../governance/providers/README.md) | v14.5 |
| TERM-EXCEPTION | Exception | A limited departure from a standard with an approved condition, scope, reason, end or review condition, and verification | Keeping an existing difference forever | [Quality standards](../governance/quality-standards.md) | v14.5 |
| TERM-UNVERIFIED | Unverified | The state of a claim whose needed evidence was not obtained. It asserts neither a gap, nor non-applicability, nor completion | A confirmed missing implementation | [Output style](../governance/output-style.md) | v14.5 |
| TERM-KEEP | Keep | A change action meaning the current target and real consumers were confirmed to fit, so no change is needed; open acceptance stays separate | Exempting an approved artifact from reform | This vocabulary; the verdict lives in the owning Task | v14.5 |
| TERM-RELEASE-OPERATION | Release Operation | The operational work on tags, artifacts, GitHub Releases and public delivery. Release is not a document role | Re-introducing a Release document role | [Documentation protocol](../governance/documentation-protocol.md#release-evidence-boundary) | v14.5 |

## Local Extensions

| Term | Definition | Not to Confuse | Policy Owner |
| --- | --- | --- | --- |
| Spec Package | A directory holding one bounded change's `spec.md`, optional `plan.md`, and numbered Tasks | A long-lived requirement or design | [Documentation protocol](../governance/documentation-protocol.md) |
| Lifecycle | The named status set and permitted transitions for a profile; `living` and `spec` differ | The SDLC stage or document stage | [Documentation protocol](../governance/documentation-protocol.md) |
| Identity space | The monotonic allocator for an artifact prefix; an issued number is never reused | A display order | [Documentation protocol](../governance/documentation-protocol.md) |
| Reserved history | The Registry list of retired numbers per identity space; it only grows | A removal record | [Documentation protocol](../governance/documentation-protocol.md#document-retention-and-retirement) |
| Promotion receipt | The Task section connecting each acceptance criterion to its durable Stage 01, 02 or 05 owner | Promotion itself | [SDLC](../governance/sdlc.md#sequence) |
| Adapter | An authored provider file that owns loading and syntax differences only | A Projection | `.claude/provider.md`, `.codex/provider.md` |
| Native mechanics | Provider runtime configuration such as settings and hook registration | Native Runtime Evidence | [Providers index](../governance/providers/README.md) |
| Tracked configuration | What a configured hook, provider surface or renderer parity proves: the setting is tracked | Adoption or a live event | [Approval boundaries](../governance/approval-boundaries.md) |
| Runtime acceptance | Whether an active provider runtime accepted a configured value, observed natively; a kind of Native Runtime Evidence | Acceptance | [Provider capability matrix](../governance/provider-capability-matrix.md) |
| Quarantine | The renderer's nonzero cleanup handoff | A successful regeneration | [Providers index](../governance/providers/README.md) |
| Work profile | A named workload class mapped to a provider model and reasoning control | A Document Profile | Provider Registry |
| Permission profile | `read-only` or `workspace-write`, translated per provider | Approval | Provider Registry |
| Explicit invocation | A skill runs only when named; discovery alone never selects or empowers it | Discovery | [Agentic policy](../governance/agentic.md) |
| Fail closed | An unknown or unsafe input is preserved and reported, never auto-deleted or auto-approved | Silent skip | [Agentic policy](../governance/agentic.md) |
| QA | Applicable verification and review of the changed contract | Acceptance | [Quality standards](../governance/quality-standards.md) |
| CI | Hosted validation of a named event and revision | Deployment | [GitHub governance](../governance/github-governance.md) |
| CD | Authorized artifact promotion and deployment; a changelog check or rehearsal alone is not deployment | Release Operation readiness | [Documentation protocol](../governance/documentation-protocol.md#release-evidence-boundary) |
| Workflow | GitHub event-triggered automation composed of jobs | A Spec Package workflow | `.github/workflow-contract.yml` |
| Job | One execution unit in a workflow; not necessarily a required status check | Required status check | `.github/workflow-contract.yml` |
| Required status check | A named source-bound context required by remote protection for the relevant revision | Any passing job | `.github/rulesets/main-protection.md` |
| Check | Validation that reports a result without rewriting source | Fix | [Quality standards](../governance/quality-standards.md) |
| Fix | An explicitly requested source transformation followed by diff review and verification | Check | [Quality standards](../governance/quality-standards.md) |
| Fixture | Deterministic input with a focused behavior or independent serialized consumer | Production data | [Quality standards](../governance/quality-standards.md) |
| Local completion | Reviewed local changes and applicable checks and commits with explicit limits | Completion of integration or deployment | [Task checklists](../governance/task-checklists.md) |
| Merge readiness | Actual required checks and reviews for the relevant PR revision and verified protection | Acceptance | [GitHub governance](../governance/github-governance.md) |
| Suite | One of the six named public groupings of gate nodes | A test module | `.github/workflow-contract.yml` |
| Gate node | One addressable entry in the executable graph | A workflow job | `.github/workflow-contract.yml` |
| Leaf | A gate node that executes an entrypoint rather than expanding to children | A suite | `.github/workflow-contract.yml` |
| Profile, gate sense | `changed` or `full`; the two public validation profiles | Document Profile | `.github/workflow-contract.yml` |
| Canonical invocation identity | Resolved path, normalized argv, profile and execution context; unique per plan | A command string | `scripts/validation/ci_gate_runner.py` |
| Changed-path rule | The prefix-to-suite mapping that selects suites for a changed file | A required status check | `.github/workflow-contract.yml` |
| Controlled wrapper | The single approved all-files pre-commit route; direct `pre-commit run` is prohibited | A direct hook run | [Quality standards](../governance/quality-standards.md#4-execution-boundary) |
| Generated-artifact freshness | A generated output must be reproduced by its generator, never hand-edited to pass | Projection | [Quality standards](../governance/quality-standards.md) |
| Evidence class | The weakest observation that supports a claim: configured, repository-enforced, local-executed, local-parser, official-source, or an unverified runtime, entitlement or remote state | Evidence itself; one class does not prove another | [Output style](../governance/output-style.md) |

## Maintenance

### Provenance

Compiled from tracked sources at repository commit
`9ede309a5b1feba91e6f8b973a729716b14c55ab` on 2026-09-06 and revalidated on
2026-09-08 and 2026-11-03. On 2026-11-12 SPEC-0212 TSK-0059 moved it to the
Repository Vocabulary form at `main` `4cd25b95b`. The common terms follow
the four-repository target at contract version v14.5. The policy owners were
read at the lines cited in that Task. The local terms carry the earlier rows
unchanged in meaning.

### Refresh Triggers

- A governance policy introduces, renames or retires a term.
- The shared Repository Vocabulary contract changes version.
- A Stage 99 lifecycle, profile or identity relation changes.
- A public suite or profile name changes in the workflow contract.

## References

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Bootstrap](../governance/bootstrap.md)
- [Documentation protocol](../governance/documentation-protocol.md)
- [SDLC](../governance/sdlc.md)
- [Approval boundaries](../governance/approval-boundaries.md)
- [Quality standards](../governance/quality-standards.md)
