---
title: "SDLC Structure Task"
version: "0.5.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0086"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# SDLC Structure Task

## Scope

### Objective and Parent

Own criterion 142 and work unit W158 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring the common policy layout to the 4.2.0
SDLC-STRUCTURE design: one owner per common rule across the W/P/R/C/A/I/T
layers, with the policies people and agents share in their own stage.

### Inputs and Authority

The direct 2026-11-18 request runs SDLC-STRUCTURE from the git-ignored 4.2.0
package with designs D26, D28 and D00 and the five Docker disposition rows
for this prompt. The attachment is a proposal and authorizes nothing. On
2026-11-18 the owner answered SDD-WOWNER with "Adopt docs/00.workspace",
so the physical move is in scope. SDD-PATHS, the later renumbering of the
docs subtrees, stays with DOC-PATH-PLAN and is not part of this Task.

## Execution Log

### Work Performed

#### Disposition of the Docker rows

| Row | Finding on `ebc758a4a` | Disposition |
| --- | --- | --- |
| D-A01 thin provider entries | Root `AGENTS.md` and `CLAUDE.md` both route to the one bootstrap policy | KEEP_VERIFIED |
| D-A02 hookify input stays machine-read | The rules, loader and native bindings stay under `.agents/governance/hooks/` | KEEP_VERIFIED, nothing moved |
| D-A04 no duplicate agent navigation | The Wiki stays retired, `llms.txt` is a pointer, and each of the four prompts has two to four consumers | KEEP_VERIFIED |
| D-W02 shared policy in a workspace layer | The shared policies sat in the agent layer | TARGETED_CHANGE in W158 |
| D-W05 README facts and `.gitmodules` | Already settled by TSK-0080: wording accurate, `.gitmodules` has consumers | KEEP_VERIFIED, not reopened |

#### W158 design

The eight policies whose meaning people and agents share moved with
`git mv`, keeping their names:

| Layer folder | Policies |
| --- | --- |
| `01.project` | stage authoring matrix |
| `02.process` | SDLC, documentation protocol, Git workflow, GitHub governance, approval boundaries |
| `03.quality` | quality standards, task checklists |

Bootstrap, agentic, persona, output style, postflight checklist, provider
capability matrix, standards, workflows and environment constraints stay
in `.agents/governance/`: they govern how an agent enters, routes, delegates,
reports and runs, which is the A layer. Workflows routes work between roles,
so it stays with the agent rules.

The stage authoring matrix now owns the responsibility layer table and three
rules: one owner per common rule, approval meaning only in Stage 00
approval boundaries, and hook inputs never moved as policy text. The
agentic policy already resolves authority through approval boundaries, so
no second approval source exists. The SDLC gained a proportional-record
table so a typo or link fix needs no new package. Bootstrap R3 and R16 name
both homes.

A script rewrote 231 live files: relative Markdown links recomputed from
each file's new location, and repository paths in code, Registry, provider
registry, workflow contract and pre-commit configuration. It skipped 33
terminal Task bodies. 198 changed documents took a patch version. The
renderer regenerated the Claude and Codex surfaces.

#### Checker defects found by the move

| Defect | Cause | Fix |
| --- | --- | --- |
| Agent governance contract never returned | The canonical-home scan climbed each source's parents to `.agents`, which a `docs/00.workspace` source never reaches | Sources outside the home are checked as regular files and skip the walk |
| Metadata check stopped on the base Registry | Relation owners of a past revision were checked in the working tree | `validate_registry` takes an owner predicate; the revision loader checks the revision's tree |
| Moved policies reported as new drafts | The base record was looked up only at the new path | The moved-baseline recovery maps a workspace policy to its `.agents/governance/` blob when type and identity match |
| Completed Tasks would hold broken links | Their bodies are immutable | Link alignment resolves a completed Task's old `.agents/governance/<name>.md` link to the one moved file of that name, and still checks the anchor |
| Gate leaves rejected the new rule owners | The rule-owner pattern allowed only `.agents/governance/` | The pattern also allows the three workspace folders |
| New paths unrouted | No selector route named them | `docs/00.workspace/` joins the agent-governance route |
| Policy links read as stage links | The outside-docs and folder-router link rules treat every `docs/NN.*` folder as a stage | A `docs/00.workspace/` target is a canonical policy owner, as `.agents/governance/` was |
| Two test fixtures lacked the new home | The workflow contract and folder-guide shim fixtures copied only `.agents` | Both also copy `docs/00.workspace` |
| Two hook warnings lost their targets | `warn-governance-memory-edit` and `warn-korean-in-governance` matched only `.agents/` paths | Their file-path matchers also name the moved SDLC and the workspace policies; the rule files stay in place |

The lifecycle check's internal error had the same base Registry cause and
cleared with that fix.

#### SDD-CONFORMANCE review

The 2026-11-18 SDD-CONFORMANCE request assigns this workspace one item,
D-W04: reuse the selection contract and the required aggregate and add
only path-change fixtures. The aggregate `candidate-quality` already fails
closed, as PR 1096 showed when `candidate-documents` failed. The existing
fixture covered the moved policies for the document suites only, so a new
case proves a `docs/00.workspace/` change selects the agent-governance
suite and its contract leaf. The Spec Package reader already refuses
unknown criteria and Work Units, forward or cyclic dependencies, a
resolution across checks and an acceptance without its rows, so no trace
export was needed. It accepts a criterion that no Work Unit maps until
removal readiness; every live package maps all criteria, and an
authoring-time check is left as an optional extension because the fixtures
build such Plans on purpose. The D24 common forms stay as W03-FORMS
delivered them.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0086 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0086 | ready | in-progress | #w158-design |

### Blockers and Decisions

None block W158. After the merge, a fresh headless Claude session in plan
mode and a fresh read-only `codex exec` session were each asked, without a
path, which files own the shared SDLC and approval boundaries. Both
followed their entry file and bootstrap to
`docs/00.workspace/02.process/sdlc.md` 2.3.0 and
`docs/00.workspace/02.process/approval-boundaries.md` 1.6.0 with the
correct titles; Claude cited BOOTSTRAP-R16 as its route.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Moved link RED | 142 | W158 | `MovedWorkspacePolicyLinkTests` | New tests before the link change | FAIL | 3 failures: the completed Task's old link was missing | required | - |
| Moved link GREEN | 142 | W158 | `MovedWorkspacePolicyLinkTests` | Link alignment change | PASS | 8 tests, including an editable Task and an unmoved name still failing | required | Moved link RED |
| Relation owner RED | 142 | W158 | `test_relations` | New owner-predicate test | FAIL | `validate_registry` had no owner predicate | required | - |
| Relation owner GREEN | 142 | W158 | `test_relations` | Owner predicate | PASS | 15 tests | required | Relation owner RED |
| Moved baseline RED | 142 | W158 | `test_workspace_policy_inherits_its_agent_governance_baseline` | New test with the workspace branch disabled | FAIL | The lookup went to the retired `docs/00.agent-governance/` path | required | - |
| Moved baseline GREEN | 142 | W158 | `test_workspace_policy_inherits_its_agent_governance_baseline` | Workspace baseline mapping | PASS | Type mismatch still refuses the baseline | required | Moved baseline RED |
| Workspace link RED | 142 | W158 | `test_workspace_policy_links_are_canonical_not_stage_links` | New test before the link rule change | FAIL | The outside-docs rule also flagged the workspace policy link | required | - |
| Workspace link GREEN | 142 | W158 | `test_workspace_policy_links_are_canonical_not_stage_links` | Link rule change | PASS | Only the Stage 03 link is flagged; the docs router may name a policy | required | Workspace link RED |
| Document checks | 142 | W158 | link alignment and commands, changed metadata, corpus lifecycle | Staged change | PASS | 0 failures; metadata 210 selected, 0 violations | required | - |
| All link modes | 142 | W158 | `check-document-links.py --mode all` | Staged change and an `origin/main` worktree | FAIL | 5 `stage-link-outside-docs` findings in the n8n and SearXNG READMEs, identical on `main`; none from this change | required | - |
| All link modes after fix | 142 | W158 | `check-document-links.py --mode all` | The n8n and SearXNG READMEs with the five 0110 links replaced by their IDs, 2026-11-19 | PASS | 907 documents, 0 failures | required | All link modes |
| Contract and renderer | 142 | W158 | agent governance contract, renderer check | Staged change | PASS | contract 0 failures; renderer drift 0 | required | - |
| Focused suites | 142 | W158 | links, relations, registry, gate contract, workflow contract, CI routing, script manifest, surface ownership, entrypoint and gate plan modules | Staged change, controller Python 3.14.8 | PASS | 666 tests; metadata modules 297 tests | required | - |
| Hosted candidate RED | 142 | W158 | PR 1096 candidate-documents | Commit `75a98d6c1` | FAIL | 46: template policy references pinned to `.agents/governance/`; generation-7 fixtures whose committed Registry names owners only the working tree holds | required | - |
| Hosted candidate GREEN | 142 | W158 | PR 1096 candidate-documents | Test pattern and an owner predicate accepting the working tree or the revision | PASS | Locally 111 tests across generation 6 and 7, template definition, relations and acceptance; hosted rerun pending | required | Hosted candidate RED |
| Hook matchers | 142 | W158 | `hook_rules.evaluate` probe | Moved SDLC, a moved policy, the workspace README, an agent policy | PASS | Memory warning on both watched files; Korean warning on both policy homes, not on the README | required | - |
| Native loading | 142 | W158 | a fresh provider session reading a moved policy | Claude and Codex | NOT_RUN | Not observed | required | - |
| Route fixture RED | 142 | W158 | `test_a_workspace_policy_change_selects_the_agent_governance_contract` | Workflow contract without the `docs/00.workspace/` route | FAIL | The selector refused the path as unmapped | required | - |
| Route fixture GREEN | 142 | W158 | `test_a_workspace_policy_change_selects_the_agent_governance_contract` | Current workflow contract | PASS | The agent-governance suite and `leaf.local-agent-governance-contract` selected | required | Route fixture RED |
| Native loading observed | 142 | W158 | a fresh provider session reading a moved policy | `claude -p` in plan mode and `codex exec` read-only on `dc53d574f` | PASS | Both named the SDLC 2.3.0 and approval boundaries 1.6.0 at their `docs/00.workspace/02.process/` paths from the bootstrap alone | required | Native loading |

### Resolution Links

Moved link GREEN resolves Moved link RED. Relation owner GREEN resolves
Relation owner RED. Moved baseline GREEN resolves Moved baseline RED.
Workspace link GREEN resolves Workspace link RED. Hosted candidate GREEN
resolves Hosted candidate RED. Native loading observed resolves Native
loading. Route fixture GREEN resolves Route fixture RED. The All link modes
failure predates this Task and stays with the SearXNG owner.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 142 | accepted | Moved link GREEN, Relation owner GREEN, Moved baseline GREEN, Document checks, Contract and renderer, Native loading observed, All link modes after fix | Owner @buenhyden accepted on 2026-11-19 in this chat (W11-ACCEPT) | @buenhyden |

### Remaining Conditions

The owner accepted criterion 142 on 2026-11-19.

Five outside-docs links in the n8n and SearXNG READMEs fail on `main` too and
are not this Task's change.

## Handoff

### Promotion Receipt

The stage authoring matrix holds the layer map and rules R34 to R36, the
SDLC holds the proportional records, and bootstrap R3 and R16 name both
homes.

### Next Owner

The owner decides criterion 142.
DOC-PATH-PLAN owns SDD-PATHS.
