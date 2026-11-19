---
title: "Repository Vocabulary"
version: "0.13.0"
type: "governance/vocabulary"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-20"
created: "2026-09-06"
observed_at: "2026-11-20"
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

Included: the adopted common Term IDs and shared execution, review and
agent/provider meanings. The pinned Repository Vocabulary table remains the
adopted `repository-vocabulary` 3.0.1 contract. Supplemental meanings below
have no new Term IDs or implied cross-repository adoption. Docker-specific
bindings and narrower local uses belong to the
[local vocabulary](../../docs/00.workspace/01.project/glossary.md).
Excluded: policy procedures, vendor identities owned by the Provider Registry,
service inventories and private session content.

## Normative Language

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY in governance
documents are interpreted as described in RFC 2119 and RFC 8174 when, and only
when, they appear in all capitals. The authority behind a rule comes from the
user and the canonical owner named in
[Authority and Precedence](../governance/bootstrap.md#authority-and-precedence),
not from the RFCs. A stronger keyword does not make an unenforced rule
enforced.

## Repository Vocabulary

| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-AUTHORITY | Authority | 권한 근거 | The decision maker and basis valid for a named scope, action and revision. A file's presence or a tool run does not create it | An execution result or a supported feature | [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md) | 3.0.1 |
| TERM-GOVERNANCE | Governance | 거버넌스 | The system that sets who proposes, owns, approves, applies, excepts and changes a rule | An index that copies every policy body | [Agent governance index](../README.md) | 3.0.1 |
| TERM-POLICY | Policy | 정책 | A current norm that states what is allowed, required, forbidden and excepted for a goal and scope | A single Task record | [Bootstrap](../governance/bootstrap.md#authority-and-precedence) | 3.0.1 |
| TERM-RULE | Rule | 규칙 | A norm under a policy that states a condition, the expected behavior and how a violation is judged | Changing only a check's expected value | [Bootstrap](../governance/bootstrap.md#authority-and-precedence) | 3.0.1 |
| TERM-CONTRACT | Contract | 계약 | A versioned agreement between producer and consumer on meaning, inputs and outputs, invariants and verification | A particular implementation language | [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md) | 3.0.1 |
| TERM-CANONICAL | Canonical Source | 단일 정본 | The single source with independent authoring authority for one meaning; a derived copy tracks its source and revision | Merely having one copy | [Agent governance index](../README.md) | 3.0.1 |
| TERM-APPROVAL | Approval | 승인 | A decision that grants authority to perform a named change or operation in a named scope; it is distinct from accepting the result | Acceptance, a passing test or a merge | [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md) | 3.0.1 |
| TERM-ADOPTION | Adoption | 채택 | The state in which one revision of a shared contract has been applied to the real workspace's producers and consumers and verified | Approval of the shared goal | [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md) | 3.0.1 |
| TERM-EXECUTION | Execution | 실행 | An action performed on a real target, environment and revision; it is distinct from a proposed command or a declared setting | A plan or a setting | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-VERIFICATION | Verification | 검증 | Confirming by observation, test or review that an output meets its stated requirement or contract | Validation or user acceptance | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-VALIDATION | Validation | 목적 적합성 확인 | Confirming that an output meets its intended use and the actual need under the stated conditions | A tool merely named `validate` | [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md) | 3.0.1 |
| TERM-ACCEPTANCE | Acceptance | 인수 | A decision by an authorized party to accept a named criterion and its evidence; the basis for handling required failures and exceptions is preserved | Approval or a merged PR | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-COMPLETION | Completion | 완료 | The scoped close of one work item once its required execution, checks and acceptance conditions hold. It does not close integration, deployment or another Task | Setting every status to completed | [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md) | 3.0.1 |
| TERM-PROMOTION | Promotion | 지속 의미 승격 | Handing an open change's lasting meaning to the current requirement, design, operations or governance owner through the Plan's mapping | Moving a file or copying a Task status | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-RETIREMENT | Retirement | 문서 종료 | A decision that ends a document's current effect and fixes its successor owner, lineage and any needed historical evidence | Unconditional deletion | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#document-retention-and-retirement) | 3.0.1 |
| TERM-ARCHIVE | Archive | 역사 보관 | The storage state of information whose preservation was actually approved. Development trial and error from before the final conversion is not kept through an archive route; an operational retention duty follows its own target and decision | Equating vault storage with ending development work | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#document-retention-and-retirement) | 3.0.1 |
| TERM-REMOVAL | Removal | 사본 제거 | Removing an approved target's actual copy or reachable reference. Deletion scope, what remains and authority are kept apart; the Q01/Q10 final conversion does not require a historical recovery copy | Rewriting Git history or destroying a source without a basis | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#retirement-preconditions) | 3.0.1 |
| TERM-SUPERSESSION | Supersession | 대체 | A relation in which a newer meaning owner takes over the valid scope of an earlier document or decision and connects their lineage | A title change | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) | 3.0.1 |
| TERM-HOLD | Preservation Hold | 보존 보류 | A preservation condition that blocks disposal of a named source or evidence until there is a basis for resolving it | A blanket stop on all work | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#retirement-preconditions) | 3.0.1 |
| TERM-REGISTRY | Registry | 등록 계약 | The machine-readable contract that states document profiles, forms, states, relations and generator bindings. Approved content stays open to reform | A frozen baseline | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) | 3.0.1 |
| TERM-TEMPLATE | Template | 템플릿 | The authoring form that implements one role's common rules, policies, fields, headings, tables, relations and lifecycle | A copied example or a heading list alone | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) | 3.0.1 |
| TERM-PROFILE | Document Profile | 문서 프로필 | The conditions under which fields, sections, relations, lifecycle and template apply to one document role; it is distinct from an execution profile that selects checks | A validation profile | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) | 3.0.1 |
| TERM-TASK | Task | 실행 업무 기록 | The single authored record of one scope's execution, blockers, observations, evidence and acceptance decision; other documents reference or derive from it | A progress table duplicated in a Plan | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-EVIDENCE | Evidence | 증거 | The actual source, target revision, conditions and result that support a claim, distinguishing static, local, remote, native and operational scope | A memory summary or a planned command | [Output style](../governance/output-style.md) | 3.0.1 |
| TERM-RESOLVES | Resolves | 증거 해소 관계 | A link stating that later evidence meets the same obligation, input conditions and guarantee and so resolves an earlier failure or non-run | The newest PASS erasing every failure | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-HARNESS | Harness | 에이전트 실행 체계 | The execution setup that connects instructions, routing, permissions, state, tools, observation, stop and recovery | Treating an instruction file's existence as actual application | [Agentic policy](../governance/agentic.md) | 3.0.1 |
| TERM-NATIVE-EVIDENCE | Native Runtime Evidence | 네이티브 실행 증거 | A result observed in the installed provider, at its revision, through the actual tool path | A direct function test or vendor documentation | [Provider capability matrix](../governance/provider-capability-matrix.md) | 3.0.1 |
| TERM-PROJECTION | Projection | 통제된 파생본 | A consumer file generated or synchronized from a canonical source and explicit local bindings; it has no policy authoring authority | An independent manual copy | [Providers index](../governance/providers/README.md) | 3.0.1 |
| TERM-EXCEPTION | Exception | 명시적 예외 | A limited departure from a standard with an approved condition, scope, reason, period or end condition, and verification | Keeping an existing difference forever | [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md) | 3.0.1 |
| TERM-UNVERIFIED | Unverified | 미검증 | The state of a claim whose needed evidence was not obtained. It asserts neither a gap, nor non-applicability, nor completion | A confirmed missing implementation | [Output style](../governance/output-style.md) | 3.0.1 |
| TERM-KEEP | Keep | 구현 유지 | A change action meaning the current target and real consumers were confirmed to fit, so no change is needed; open acceptance stays separate | Exempting an approved artifact from reform | This vocabulary; the verdict lives in the owning Task | 3.0.1 |
| TERM-RELEASE-OPERATION | Release Operation | 배포 버전 발행 | The operational work on tags, artifacts, GitHub Releases and public delivery. Release is not a document role | Bringing back a separate document type for releases | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#release-evidence-boundary) | 3.0.1 |
| TERM-PUBLIC-CONTRACT | Public Contract | 공개 계약 | The observable promise a consumer depends on: the keys, types, requiredness, headings, table columns, reference directions, states, diagnostics or generated output it reads | An implementation detail no consumer reads | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-COMPATIBILITY | Compatibility | 호환성 | Whether an earlier valid producer and consumer still work against a new revision without breaking its public contract | Fixing every consumer in the same PR | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-CONTRACT-VERSION | Contract Version | 계약 판본 | The three-number version of the meaning and form under one contract ID | An input-package label such as v14.7 | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-REGISTRY-SCHEMA-VERSION | Registry Schema Version | 레지스트리 스키마 판본 | The version of the data structure that code reading the Registry relies on, separate from the content of its profiles | An internal database migration integer | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-DOCUMENT-REVISION | Document Revision | 문서 개정 판본 | The three-number `version` that records a revision of one document's content | A product version or a document issue number | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-PRERELEASE | Prerelease | 사전 배포판 | SemVer's hyphen extension, such as -rc.1. The document and contract number profile does not use it | A draft status | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-BUILD-METADATA | Build Metadata | 빌드 메타데이터 | SemVer's plus extension, such as +build.7. The document and contract number profile does not use it | A document content revision | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-BASELINE-NAMESPACE | Baseline Namespace | 기준선 번호 공간 | The current scope that separates document identity numbers so that two issued identities never collide | A version reset | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#version-objects) | 3.0.1 |
| TERM-DRAFT | Draft | 초안 | A document that may be written, revised and reviewed. On its own it is neither authority nor evidence for implementation, an operational action or a completion decision; document status, a separate execution approval and actual completion or acceptance are different facts | Implementation authority, an operational action or completion | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |
| TERM-READINESS | Readiness | 착수 준비 | The state in which the current inputs, environment, permissions and scope meet the conditions to start a piece of work | Approval or acceptance | [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md#before-editing) | 3.0.1 |
| TERM-DESIGN-FIT | Design Fitness | 설계 적합성 | The result of comparing the target design derived from the current requirement with an existing implementation in meaning, interface and guarantee | Past completion or identical structure | [SDLC](../../docs/00.workspace/03.process/sdlc.md#sequence) | 3.0.1 |

## Local Extensions

These supplemental shared meanings are outside the pinned table above; the
registered heading is retained for its existing form. Repository-specific
narrowings are defined only in the linked local vocabulary.

| Term | Definition | Not to Confuse | Policy Owner |
| --- | --- | --- | --- |
| Workspace | The current working environment and checkout in which a request executes | A Repository identity or deployed product | [Bootstrap](../governance/bootstrap.md) |
| Repository | The versioned source and its Git identity, which may have several checkouts | One Workspace or runtime | [Git workflow](../../docs/00.workspace/03.process/git-workflow.md) |
| Requirement | A solution-independent need and observable acceptance condition | The design or implementation that meets it | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) |
| Design | A proposed structure, interface or decision derived from requirements | Implemented behavior or acceptance | [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md) |
| Implementation | A concrete change that realizes the selected design | Verification, Validation or Acceptance | [SDLC](../../docs/00.workspace/03.process/sdlc.md) |
| Brief | The current request-bound record of understood goal, scope, authority, questions and checks | New permission or an acceptance decision | [Agentic policy](../governance/agentic.md) |
| Shared Memory | Repository-governed reusable knowledge recalled across agent sessions | A raw transcript, policy authority or provider-private memory | [Environment constraints](../governance/environment-constraints.md#5-shared-agent-memory) |
| Session | One bounded agent conversation or execution context with its own identity | A Work Unit, repository or authorization | [Agentic policy](../governance/agentic.md) |
| Work Unit | A bounded outcome with an owner, inputs, dependencies and verification | A Session or an entire long-lived project | [SDLC](../../docs/00.workspace/03.process/sdlc.md) |
| Lease | A time-bounded, fenced claim to execute a named unit or write scope | User authority, permanent ownership or a role name | [Agentic policy](../governance/agentic.md) |
| Gate | A named verification or decision boundary whose required conditions control progression | Any successful command | [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md) |
| Independent Review | A separate assessment by a nonimplementer with the required expertise and actual permission boundary | Self-review or a role label alone | [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md) |
| Current Baseline | The actual revision, request and relevant inputs against which a claim or change is assessed | A prompt's input order or an older successful run | [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md) |
| Adapter | An authored provider file that owns loading and syntax differences only | A Projection | `.claude/provider.md`, `.codex/provider.md` |
| Native mechanics | Provider runtime configuration such as settings and hook registration | Native Runtime Evidence | [Providers index](../governance/providers/README.md) |
| Quarantine | The renderer's nonzero cleanup handoff | A successful regeneration | [Providers index](../governance/providers/README.md) |
| Work profile | A named workload class mapped to a provider model and reasoning control | A Document Profile | Provider Registry |
| Permission profile | `read-only` or `workspace-write`, translated per provider | Approval | Provider Registry |
| Explicit invocation | A skill runs only when named; discovery alone never selects or empowers it | Discovery | [Agentic policy](../governance/agentic.md) |

## Maintenance

### Provenance

Compiled from tracked sources at repository commit
`9ede309a5b1feba91e6f8b973a729716b14c55ab` on 2026-09-06 and revalidated on
2026-09-08 and 2026-11-03. On 2026-11-12 SPEC-0212 TSK-0059 moved it to the
Repository Vocabulary form at `main` `4cd25b95b`. The common terms follow
the four-repository target published under package label `v14.5`. The policy owners were
read at the lines cited in that Task. The local terms carry the earlier rows
unchanged in meaning. On 2026-11-13 SPEC-0212 TSK-0062 restored
twenty common rows to the contract wording and moved their local
narrowings into Local Extensions. On 2026-11-14 SPEC-0212 TSK-0064 pinned
the adopted contract's ID, version, source hash and Term ID to Term pairs in
the Registry `common.vocabulary_contract`; a Registry test fails when the
Repository Vocabulary rows differ from it in ID, order, Term or Contract
Version, or when a common Term ID appears under Local Extensions. Meaning
stays an independent review against the contract. On the owner's decision of
2026-11-14 the contract is versioned in SemVer: the first adoption (package
label `v14.5`) is 1.0.0, and 1.1.0 adds the eight SemVer terms from Public
Contract to Baseline Namespace. On 2026-11-15 the owner approved adopting the
shared contract `repository-vocabulary` 3.0.1 (package
`workspace_governance_3_0_1_20261115`) in this repository, recorded in
SPEC-0212 TSK-0068: the table gains the Korean column, Draft, Readiness and
Design Fitness join the common terms, and Historical Audit ID moves to Local
Extensions because the contract no longer carries it. Every common row cites
3.0.1, and the Korean labels are the contract's. Other repositories record
their own adoption. The same day each common row was compared with the
contract's meaning, and the rows that differed were rewritten as English
renderings of 3.0.1.
On 2026-11-19 SPEC-0212 TSK-0096 moved this vocabulary from
`.agents/knowledge/glossary.md` to the workspace project folder, because its
terms are shared by people and agents alike. No common row changed: the Term
IDs, order, Terms, Korean labels, definitions and Contract Version 3.0.1 are
byte-identical. Six agent- and provider-only Local Extensions (Adapter, Native
mechanics, Quarantine, Work profile, Permission profile, Explicit invocation)
moved unchanged to the then-current Agent Glossary, and Canonical location then named
`docs/00.workspace/` beside `.agents/`.

On 2026-11-20 the direct P03 1.1.0 requirement replaces only that glossary
placement: this file again owns common meanings, the six agent rows reunite
here unchanged, and repository-specific extensions stay in the local
vocabulary. ADR-0063 records the scoped replacement. The 43 adopted rows,
Term IDs, names, Korean labels, definitions, order and contract version remain
unchanged apart from rebased links. Supplemental foundation meanings are
not a new version of the adopted shared contract.

### Refresh Triggers

- A governance policy introduces, renames or retires a term.
- The shared Repository Vocabulary contract changes version.
- A Stage 99 lifecycle, profile or identity relation changes.
- A public suite or profile name changes in the workflow contract.

## References

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Bootstrap](../governance/bootstrap.md)
- [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md)
- [SDLC](../../docs/00.workspace/03.process/sdlc.md)
- [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md)
- [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md)
