---
title: "Reference: Spec-Driven Development and SDLC"
version: "1.2.1"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002-m0018"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Spec-Driven Development and SDLC

Repository baseline: `f30b168e2fbb0959e4a31749935568fd5b3942f1`. External sources checked: 2026-09-27. Document updated: 2026-09-27. Historical workspace observations retain their original dates/commits below. Current local adoption and implementation: **Not assessed in this run**. This non-normative research changes no policy, profile, service or integration.

## Current External Research

### SDD within the lifecycle

Spec Kit's public workflow distinguishes specification, technical plan, task derivation, implementation and convergence, with optional clarification/checklist/analysis gates and optional issue conversion. Current README offers separate bug/idea entry points; agent invocation syntax varies. Analyze reports cross-artifact conflicts without editing; converge assesses implementation and can append tasks. These reports are not independent acceptance (C-m0018-01).

Its persistence choices preserve historical feature directories, maintain a living contract with derived artifacts, or reconcile discoveries from implementation back into artifacts (C-m0018-02). Recommendation: select persistence by evidence/ownership needs, retaining accepted rationale and executed evidence rather than regenerating them. This comparison neither installs Spec Kit nor adopts its paths/commands; [m0016](m0016-sdlc-document-roles.md) owns role definitions and operations feedback.

### Requirement-to-test trace and change impact

Recommendation: link requirement ID/acceptance criterion → behavior/contract → task/dependency → test/check → actual result at commit/environment → reviewer/acceptor → operations handoff as relevant. A link proves association, not adequate testing. Review failure, authority and stakeholder-outcome cases; coverage percentages do not establish meaningful criteria (C-m0018-03).

| Element | Illustrative example, not an issued identity | Review question |
| --- | --- | --- |
| Need | REQ-X: bounded recovery meets an agreed objective | Accepted scope/measure/owner/exclusions? |
| Contract | AC-X: integrity checked; incomplete recovery cannot overwrite source | Observable oracle and safety/failure conditions? |
| Work | TASK-X depends on fixture and approved procedure | Dependency reason/target/authority? |
| Check | TC-X exercises isolated recovery, corrupt input and denied authority | Correct oracle, case coverage and environment? |
| Evidence | Commit/check/result/reviewer/unresolved gap/Runbook link | Actual execution and bounded acceptance? |

When need changes identify affected decisions/contracts/test oracles/tasks/guides/policies/runbooks/release constraints before dependent work resumes. Strategy-only changes preserve behavior/acceptance while reviewing sequence/dependencies. A failure showing incorrect implementation routes to code; ambiguous/wrong intended behavior routes upstream. Detect orphan tasks, uncovered criteria, contradictory parameters, stale assumptions/derived artifacts and cyclic dependencies. Removed requirements/tests need explicit disposition; exceptions need owners and rationale. Incident learning enters the same change process, not silent product-intent edits.

### One authority per field

Recommendation: documents own approved intent/contracts/decisions and durable evidence; a selected tracker owns assignment, scheduling, notifications and daily workflow. Link stable artifact/task IDs and exact change/verification references. Status mirroring needs field ownership, sync direction, conflict handling, idempotent key and recovery. Automated close/merge can update coordination, but cannot prove acceptance. Introduce bidirectional body sync only for a demonstrated need; it creates another conflict surface (C-m0018-04).

### Project tracking alternatives

The table compares public documentation, **not accounts, subscriptions or local configuration**. No preview label means only none appeared on the consulted page. Jira rows are Cloud; GitHub rows GitHub.com. Markdown is an analytical option using existing document owners, not a new tracker implementation.

| Criterion | Markdown in Git | GitHub Issues/Projects | Linear | Jira Cloud |
| --- | --- | --- | --- | --- |
| Hierarchy | Existing IDs/links/checklists reviewed in Spec/Tasks | Sub-issues: 100 children/parent, eight nested levels; Projects groups by parent | Parent/sub-issues; projects/initiatives for larger work | Epic→standard→Subtask; custom/extra epic-level types Premium/Enterprise |
| Dependencies | Explicit links/manual sequence | Native blocked-by/blocking distinct from parent | Issue blocking/related/duplicate; project end→start only | Work links; advanced plan dependency views Premium/Enterprise |
| Roadmap | Existing plan/milestone table, no live dashboard implied | Table/board/roadmap and fields | Milestones/project timelines/initiatives/dependencies | Space timeline vs advanced multi-space Plans; verify tier/scope |
| Workflow/automation | Versioned state/evidence; no notification service implied | Item status, auto-add/archive, issue-close/PR-merge workflows; API/Actions extension | Team-specific states; GitHub PR/commit status automation and optional issue sync; webhooks | Configurable workflows/flows; actor permissions, usage limits and audit matter |
| Permissions | Git/filesystem boundary; no Markdown issue ACL | Project read/write/admin separate from repository; private items still need repo access | Private teams Business/Enterprise; scoped keys; exports/integrations can widen access | Site/space/work permissions/security; Free control/audit limitations |
| Git integration | Exact local commit/evidence links | Same-host issues/PR/code; workflow state not acceptance | GitHub integration has broad read/write request; Enterprise variants differ | Development integrations; install/admin scope reviewed separately |
| API/MCP | Existing file access without SaaS account | Projects GraphQL, classic read:project/project scopes; official MCP read-only/tool allowlists | GraphQL/webhooks; action/team-scoped API keys; MCP HTTP/read-only endpoint or read OAuth scope; SSE deprecated | REST v3 operation permissions; Atlassian MCP OAuth 2.1/admin controls |
| Export/portability | Plain text/Git; unrecorded chat not recovered | View TSV; API for fuller record; not complete issue/history backup | Supported CSV/API/Markdown/PDF; no team CSV; assess relation/comment/attachment fidelity | Backup fields/comments/media/configuration; excludes flows/app data/access settings; separate flow export; Cloud/Data Center differ |
| Cost/admin | No extra tracker subscription; manual review/navigation cost remains | Free exists; paid controls/automation consumption need review | Free $0, unlimited members, 2 teams/250 issues; Basic $10 and Business $16 per user/month yearly-billed view | Free up to 10 Jira users/2 GB with control limits; advanced paid features; paid numeric quote not verified |

Claims C-m0018-05–14 route each product dimension to its own primary pages below. List prices were checked 2026-09-27 and are not invoice, tax, currency conversion, renewal or account entitlement. Linear credits/add-ons are separate. GitHub paid rendering included promotion/first-12-month wording; no unconditional paid price is asserted. Jira pricing yielded no usable body. A fresh user-count/currency/billing-term quote is required before purchase. Compare subscription plus administration, permission review, integration/conflicts, backup/export and migration effort; no time/cost savings were measured.

### Conditional local-first choice

Recommendation: retain existing Markdown Spec/Plan/Task owners when offline/versioned review, few collaborators and simple dependencies suffice. Add one shared tracker for a concrete assignment/triage/roadmap/notification need. If code coordination already centers on GitHub, Issues/Projects is the first candidate because work and code share a host; lower integration effort is a hypothesis, not measured savings.

Consider Linear when cycles and issue/project/initiative planning justify SaaS, caps, integration scope and export checks. Consider Jira Cloud when workflow/permission complexity or multi-team planning justify administration and paid controls. Free does not mean unlimited automation/all controls. A self-hosted tracker also has operational cost; do not introduce one solely to avoid fees without evaluating that burden (C-m0018-15).

A later synthetic pilot should demonstrate IDs, requirement/test links, blockers, visibility, conflicts and round-trip export without production/private data. MCP begins read-only with least-scoped identity; exposing write tools does not itself authorize actions. No connection, issue creation, purchase or migration happened. Local adoption is **Not assessed in this run**.

### Freshness and uncertainty

Current Spec Kit/MCP sources are mutable and no fresh immutable SHA was obtained. Historical pins/flows remain intact. Failed old/guessed URLs are not removal evidence: successful detailed routes below replaced guesses for GitHub managing-your-project, Spec Kit command/evolution and Atlassian MCP/dependencies. Jira export page contains old Data Center instructions beside a discontinuation note; it is not a migration runbook. Standards full text/catalog status was not freshly verified here, so existing limits remain historical. Reopen pricing/tier/API/MCP/permission/export claims before a consequential integration decision.

## Claims and Sources

Originals below were opened on 2026-09-27. Not stated means no publication/update date was visible in the substantive page. Crawler dates, copyright and event dates are not substituted. Mutable product documentation is not account entitlement or runtime evidence. These source/claim IDs are internal research labels.

| Claim ID | Claim | Source ID and detailed section | Publication/update | Actual check | Product/version/channel/status | Fact/interpretation/recommendation | Limitation and recheck |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0018-01 | Spec Kit separates core SDD, optional gates/issue conversion and convergence; bug/idea entry points are independent | S-speckit-agentic-sdd — Command overview; analyze; converge; taskstoissues; S-speckit-readme — Choose your process; Spec-Driven Development | Not stated | 2026-09-27 | Spec Kit current public Docs; release status not inferred; Spec Kit mutable main README; fresh pin not obtained | Fact | Mutable/unpinned; syntax differs; no installation or acceptance |
| C-m0018-02 | Spec persistence choices require artifact reconciliation while preserving relevant rationale/history | S-speckit-evolving-specs — Flow-Forward; Living; Flow-Back | Not stated | 2026-09-27 | Spec Kit current public Docs; fresh pin not obtained | Fact | No authorization to regenerate executed evidence |
| C-m0018-03 | Use bidirectional criterion/contract/task/test/result/acceptance trace and changed-dependent analysis | S-speckit-evolving-specs — Flow-Forward; Living; Flow-Back; S-arc42-section-10 — Quality Requirements; Quality Scenarios | Not stated | 2026-09-27 | Spec Kit current public Docs; fresh pin not obtained; Current public guidance; no release/status label | Recommendation | Associations not adequacy; local model owner-defined |
| C-m0018-04 | Documents own intent/evidence, tracker coordination; declare sync/conflict/idempotent ownership | S-github-projects-automations — Default workflows; auto-add/archive; S-linear-github — Overview; Permissions; Enterprise variants | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label; Linear SaaS current Docs; status as detailed section | Recommendation | No integration assessed; Done/merge not acceptance |
| C-m0018-05 | GitHub supports nested sub-issues and explicit issue dependencies | S-github-sub-issues — Introduction; 100 children/eight nesting levels; S-github-issue-dependencies — Blocking relationships | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label | Fact | Current documented limits; check before integrating |
| C-m0018-06 | Projects has views/workflows and separate project/repository access | S-github-projects-about — Introduction; table/board/roadmap views; S-github-projects-automations — Default workflows; auto-add/archive; S-github-projects-access — Roles; underlying repository access | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label | Fact | Definition not configuration/enforcement |
| C-m0018-07 | GitHub TSV view export/GraphQL and official MCP read-only are distinct capabilities | S-github-projects-export — TSV view export; S-github-projects-api — GraphQL; Authentication; Webhooks; S-github-mcp — Toolsets; Read-Only Mode | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label; Official GitHub MCP mutable main; unpinned | Fact | View snapshot not full backup; export fidelity untested |
| C-m0018-08 | Linear has sub-issues/initiatives/milestones/issue relations and end-to-start project dependencies | S-linear-parent-sub-issues — Overview; Create sub-issue; S-linear-initiatives — Overview; Projects; Views; S-linear-project-milestones — Overview; Milestones and Initiatives; S-linear-issue-relations — Blocked/blocking; Duplicate; S-linear-project-dependencies — Overview; end-to-start only | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section | Fact | Resolved blockers become Related; other project dependency types not claimed |
| C-m0018-09 | Linear team workflow/GitHub state and sync have tier/platform/permission differences | S-linear-workflows — Team statuses; auto-close/archive; S-linear-github — Overview; Permissions; Enterprise variants; S-linear-private-teams — Business/Enterprise; Visibility; Export/API risk | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section | Fact | Broad integration access requires review; no local/account check |
| C-m0018-10 | Linear API scopes team/action, MCP read-only exists/SSE deprecated; exports have defined limits | S-linear-api-webhooks — API Keys; teams/actions; Webhooks; S-linear-mcp — General/OAuth/read-only; FAQ/SSE deprecated; S-linear-export — CSV; API; Markdown/PDF; no team CSV | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section | Fact | Entitlement/fidelity not tested |
| C-m0018-11 | Linear public price/tier caps observed in yearly-billed view; GitHub Free exists | S-linear-pricing — Free/Basic/Business yearly-billed cards; credit footnote; S-github-pricing — Free/Team cards; first-12-month wording | Not stated | 2026-09-27 | Public USD price page; yearly-billed view; Public price page; account price not assessed | Fact | Actual tax/term/credits/invoice/renewal not assessed |
| C-m0018-12 | Jira default three levels; custom hierarchy and advanced plan dependencies paid | S-atlassian-jira-hierarchy — Default/custom hierarchy; irreversible change warning; S-atlassian-jira-dependencies — Premium/Enterprise Plans; dependency fields; S-atlassian-jira-planning-overview — Plans overview; FAQ comparing Plans and Jira timeline | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed | Fact | Premium/Enterprise; hierarchy changes can break relations and are warned irreversible |
| C-m0018-13 | Jira workflow/automation, REST permissions, MCP OAuth and Free-tier limits differ | S-atlassian-jira-automation — Flows; actions/triggers/conditions; permissions/actors routes; S-atlassian-jira-rest — Authentication; Permissions; S-atlassian-mcp-auth — OAuth 2.1/token/organizational authorization; S-atlassian-jira-plans — Free; limitations; S-atlassian-jira-github — Connect GitHub Cloud to Jira; integration/admin setup | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed; Jira Cloud REST v3 | Fact | Cloud only; paid numeric quote unavailable; product/account entitlement not assumed |
| C-m0018-14 | Jira Cloud export excludes flows/app data/access settings and differs from Data Center | S-atlassian-jira-export — Exportable/nonexportable; Cloud/Data Center; restrictions | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed | Fact | Mixed old/current migration instructions; no live export/migration |
| C-m0018-15 | Select existing Markdown/simple work, GitHub/host-centered, Linear/team planning, Jira/justified complexity | S-github-projects-about — Introduction; table/board/roadmap views; S-linear-pricing — Free/Basic/Business yearly-billed cards; credit footnote; S-atlassian-jira-plans — Free; limitations | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label; Public USD price page; yearly-billed view; Jira Cloud/Atlassian current Docs; no Data Center parity claimed | Recommendation | No measured savings/needs/account assessment; no purchase/adoption |

| Source ID | Original and detailed location | Publication/update | Actual check | Product/channel/status |
| --- | --- | --- | --- | --- |
| S-speckit-agentic-sdd | [Command overview; analyze; converge; taskstoissues](https://github.github.io/spec-kit/reference/agentic-sdd.html) | Not stated | 2026-09-27 | Spec Kit current public Docs; release status not inferred |
| S-speckit-readme | [Choose your process; Spec-Driven Development](https://github.com/github/spec-kit) | Not stated | 2026-09-27 | Spec Kit mutable main README; fresh pin not obtained |
| S-speckit-evolving-specs | [Flow-Forward; Living; Flow-Back](https://github.github.io/spec-kit/guides/evolving-specs.html) | Not stated | 2026-09-27 | Spec Kit current public Docs; fresh pin not obtained |
| S-arc42-section-10 | [Quality Requirements; Quality Scenarios](https://docs.arc42.org/section-10/) | Not stated | 2026-09-27 | Current public guidance; no release/status label |
| S-github-projects-automations | [Default workflows; auto-add/archive](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-linear-github | [Overview; Permissions; Enterprise variants](https://linear.app/docs/github) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-github-sub-issues | [Introduction; 100 children/eight nesting levels](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-issue-dependencies | [Blocking relationships](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-projects-about | [Introduction; table/board/roadmap views](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-projects-access | [Roles; underlying repository access](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-projects-export | [TSV view export](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/exporting-your-projects-data) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-projects-api | [GraphQL; Authentication; Webhooks](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects) | Not stated | 2026-09-27 | GitHub.com current Docs; no preview label |
| S-github-mcp | [Toolsets; Read-Only Mode](https://github.com/github/github-mcp-server) | Not stated | 2026-09-27 | Official GitHub MCP mutable main; unpinned |
| S-linear-parent-sub-issues | [Overview; Create sub-issue](https://linear.app/docs/parent-and-sub-issues) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-initiatives | [Overview; Projects; Views](https://linear.app/docs/initiatives) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-project-milestones | [Overview; Milestones and Initiatives](https://linear.app/docs/project-milestones) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-issue-relations | [Blocked/blocking; Duplicate](https://linear.app/docs/issue-relations) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-project-dependencies | [Overview; end-to-start only](https://linear.app/docs/project-dependencies) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-workflows | [Team statuses; auto-close/archive](https://linear.app/docs/configuring-workflows) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-private-teams | [Business/Enterprise; Visibility; Export/API risk](https://linear.app/docs/private-teams) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-api-webhooks | [API Keys; teams/actions; Webhooks](https://linear.app/docs/api-and-webhooks) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-mcp | [General/OAuth/read-only; FAQ/SSE deprecated](https://linear.app/docs/mcp) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-export | [CSV; API; Markdown/PDF; no team CSV](https://linear.app/docs/exporting-data) | Not stated | 2026-09-27 | Linear SaaS current Docs; status as detailed section |
| S-linear-pricing | [Free/Basic/Business yearly-billed cards; credit footnote](https://linear.app/pricing) | Not stated | 2026-09-27 | Public USD price page; yearly-billed view |
| S-github-pricing | [Free/Team cards; first-12-month wording](https://github.com/pricing) | Not stated | 2026-09-27 | Public price page; account price not assessed |
| S-atlassian-jira-hierarchy | [Default/custom hierarchy; irreversible change warning](https://support.atlassian.com/jira-cloud-administration/docs/configure-the-issue-type-hierarchy/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |
| S-atlassian-jira-dependencies | [Premium/Enterprise Plans; dependency fields](https://support.atlassian.com/jira-software-cloud/docs/view-all-of-an-issues-dependencies-on-your-timeline/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |
| S-atlassian-jira-automation | [Flows; actions/triggers/conditions; permissions/actors routes](https://support.atlassian.com/cloud-automation/docs/jira-cloud-automation/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |
| S-atlassian-jira-rest | [Authentication; Permissions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) | Not stated | 2026-09-27 | Jira Cloud REST v3 |
| S-atlassian-mcp-auth | [OAuth 2.1/token/organizational authorization](https://support.atlassian.com/atlassian-ai-gateway/docs/authentication-and-authorization/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |
| S-atlassian-jira-plans | [Free; limitations](https://support.atlassian.com/jira-cloud-administration/docs/explore-jira-cloud-plans/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |
| S-atlassian-jira-export | [Exportable/nonexportable; Cloud/Data Center; restrictions](https://support.atlassian.com/jira-cloud-administration/docs/export-issues/) | Not stated | 2026-09-27 | Jira Cloud/Atlassian current Docs; no Data Center parity claimed |

| S-atlassian-jira-planning-overview | [Jira Plans overview](https://www.atlassian.com/software/jira/guides/advanced-roadmaps/overview) | Plans overview; FAQ comparing Plans and Jira timeline | Not stated | Checked 2026-09-27; Jira Cloud current guide; no account entitlement claim |

| S-atlassian-jira-github | [Integrate Jira with GitHub](https://support.atlassian.com/jira-cloud-administration/docs/integrate-with-github/) | Connect GitHub Cloud to Jira; integration/admin setup | Not stated | Checked 2026-09-27; Jira Cloud/GitHub Cloud current Docs |

## Future Internal Checks

Every row is a design for later authorized assessment. Confirmed paths were read only for routing; other surfaces are hypothetical candidates. No implementation, account, execution, permission enforcement or adoption was assessed.

| Topic/claim ID | Analytical scope | Applicability condition | Future surface candidate | Specific question | Required evidence | Future method | Pass/fail criterion | Additional authority/risk | Expected owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Requirement/test trace / C-m0018-03 | Product/Spec; quality | Requirement/test strategy changes | Hypothetical approved criteria/contracts/tasks/tests/results | Which criteria are adequately checked, including failure/authority cases, and which gaps are owned? | IDs/bidirectional map/oracles/results at commit/environment/acceptor | Bounded trace review plus separately authorized checks | Pass: adequate evidence or owned gap; fail: orphan/uncovered/meaningless link | Test execution separately scoped; no live target by default | QA/requirement owner | Not assessed in this run |
| Change impact / C-m0018-02,03 | Spec/architecture/operations | Need/strategy/implementation insight changes | Hypothetical affected package/direct consumers | Which earlier owner and downstream artifacts disagree and what decision reconciles them? | Assumptions/dependent map/acceptance decision | Authorized cross-artifact review | Pass: impacts/disposition explicit; fail: stale contract/blind evidence regeneration | Tool report does not approve scope | Engineering/architecture | Not assessed in this run |
| Tracker authority / C-m0018-04 | Repository/provider; collaboration | Shared tracker needed | Hypothetical synthetic task/issue sample | Who owns each field and how are IDs/duplicates/conflicts recovered? | Approved ownership map/synthetic sync/conflict receipt | Separately authorized sandbox pilot | Pass: one owner/idempotent/recoverable; fail: duplicate authorities/Done implies acceptance | Remote connect/create/write separate approval | Engineering/tracker admin | Not assessed in this run |
| GitHub hierarchy/deps/views / C-m0018-05,06 | Repository; collaboration | GitHub-centered coordination | Hypothetical synthetic Issues/Project | Do documented hierarchy/dependencies/views and access meet real workload? | Plan/limit docs/sample/visibility evidence | Separately authorized sample review | Pass: required behavior supported; fail: hierarchy mistaken dependency or limit conflict | Account/create not authorized here | Project/tracker owner | Not assessed in this run |
| Linear planning/workflow / C-m0018-08,09 | Provider; collaboration/architecture | Cycles/initiative planning justified | Hypothetical Linear sample | Are end-to-start/state/tier sufficient and Git permission requests justified? | Current tier/dependency/status sample/permission manifest | Separate sandbox review | Pass: needed semantics/tier/scope; fail: incompatible dependency or excessive unapproved grant | Connect/write need approval; no private data | Project/security reviewer | Not assessed in this run |
| Jira hierarchy/workflow / C-m0018-12,13 | Organization; collaboration/governance | Complex controls/planning justified | Hypothetical Jira Cloud sample | Which tier/hierarchy/rules/access fit and how would hierarchy changes affect relations? | Quote/sample/actor/quota/permission model | Separate sandbox evaluation; no production hierarchy edit | Pass: controls/relations/admin burden accepted; fail: Free conflict or irreversible change unplanned | Account-wide admin risk/change approval | Jira/project admin | Not assessed in this run |
| API/MCP / C-m0018-07,10,13 | Provider; security/collaboration | Agent later needs tracker access | Hypothetical least-scoped read-only identity | Are tools/effective operations and private-team visibility limited to approved needs? | Docs/tool schemas/synthetic read-deny receipts | Read-only first; scoped later acceptance | Pass: intended read/no mutation/leak; fail: unexplained write/private scope | Credential/connect/install/action approval separate | Security/provider admin | Not assessed in this run |
| Export/portability / C-m0018-07,10,14 | Organization/provider; data/collaboration/governance | Adoption/migration proposed | Hypothetical synthetic source/export/destination | Can IDs/relations/comments/attachments/decisions/evidence restore and what needs separate export? | Manifest/export/mapping/round-trip diff | Separately authorized sample round-trip | Pass: needed facts restore or accepted exclusions; fail: undocumented loss/visibility change | Export can disclose; no production migration | Data/tracker owner | Not assessed in this run |
| Cost/selection / C-m0018-11,15 | Organization/provider; collaboration | Purchase/plan change considered | Hypothetical fresh quote/needs matrix | What users/currency/term/caps/credits/control/admin needs justify a tool change? | Fresh quote/requirements/ownership assumptions | Read-only compare; owner decision | Pass: cost/capability explicit; fail: unmeasured savings/account price inferred | Purchase/paid work separate approval | Project/finance owner | Not assessed in this run |

## Historical Workspace Observations

Original observations, source checks, corrections, measurements, access failures and recommendations below remain at their recorded boundaries and were not reassessed. Heading anchors are preserved for consumers. Historical instructions are not current authority.

> Historical evidence (not current authority; source: Git history):
>
> Current routing (2026-09-06): [canonical agent governance](../../../../.agents/README.md) and
> [ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md) own the active source location.
> Earlier Stage 00 paths, inventories, provider projections, and check results
> below remain dated observations, not current instructions or new runtime
> acceptance evidence. Source links now navigate to current owners; the
> original `observed_at`, `reviewed_at`, status, and measured facts are preserved.
>

## Overview

> Historical evidence (not current authority; source: Git history):
>
> Spec-driven development in this workspace is a traceable engineering lifecycle,
> not the installation of a particular AI tool. Product intent, architecture,
> technical contracts, prospective execution, observed execution, and operations
> evidence remain separate artifacts with named owners. Implementation is
> acceptable only when the applicable contract, change boundary, validation,
> review, and evidence chain agree.
>
> The historical analysis measured the tree at HEAD `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
> (2026-08-14, branch `docs/agentic-research-pack-deepening`). It does not reuse
> the predecessor pack's `59 specs / 0 archived specs` figure. The stale Graphify
> report was used only as a navigation aid and every relationship below was
> corroborated against tracked canonical agent governance, Stage 01-05, Stage 98, and Stage 99
> sources, re-derived with `find`/`rg` rather than trusted from the prior
> revision of this leaf.
>

## Purpose

> Historical evidence (not current authority; source: Git history):
>
> Define REQ-06 and REQ-09: the workspace's spec-driven concepts, lifecycle,
> traceability, gates, feedback, ownership, evidence, and enforcement boundaries.
> The companion references examine document-role and metadata distinctions;
> current role, profile, and state authority remains in canonical agent governance and Stage 99.
>

## Repository Role

> Historical evidence (not current authority; source: Git history):
>
> This is advisory Stage 90 research. It distinguishes dated tracked observations from
> external comparisons; it does not approve a requirement, choose architecture,
> authorize implementation, establish policy, execute a release, prove runtime
> state, or change any canonical governance and Stage 99 contract. Canonical authority remains in the
> [canonical agent governance SDLC](../../../../.agents/governance/sdlc.md),
> [documentation protocol](../../../../.agents/governance/documentation-protocol.md),
> and [Stage 99 Registry](../../../99.templates/registry.json). The current Task
> owns implementation and validation evidence; historical tables do not define
> current fields, paths, or gates.
>

## Scope

### In scope

> Historical evidence (not current authority; source: Git history):
>
> - The current Stage 01-05 lifecycle and Stage 90/98/99 support boundaries.
> - Entry and exit evidence, feedback routing, validation, review, and ownership.
> - Spec-driven tool comparison at immutable upstream revisions.
> - Current active/archive counts and lifecycle-state distribution.
>

### Out of scope

> Historical evidence (not current authority; source: Git history):
>
> - Adopting ISO, IETF, NIST, Spec Kit, OpenSpec, or another external method.
> - Changing templates, metadata profiles, lifecycle transitions, stages, or archives.
> - Starting services, observing private runtime state, or mutating remote controls.
> - Treating a tracked workflow, tag, Release record, or Stage 90 statement as
>   deployment/runtime proof.
>

## Definitions / Facts

### Working definition

> Historical evidence (not current authority; source: Git history):
>
> Spec-driven development is the practice of making an explicit, reviewable
> contract the controlling input to implementation and keeping bidirectional
> traceability among intent, decisions, design, work, validation, and outcomes.
> The contract must be specific enough to reject an implementation, not merely
> describe it after the fact. In this workspace, that principle spans more than a
> single `spec.md`: Requirement Package, Architecture Description/ADR, Spec
> and native contracts, Plan, Task evidence,
> and Operations each own a different question.
>
> The lifecycle is iterative rather than a one-way waterfall. A failed check,
> incident, postmortem, release outcome, vulnerability, or verified drift routes
> back to the earliest canonical owner whose truth must change. The downstream
> artifact links the correction; it does not copy the upstream contract and
> become a competing source of truth.
>

### Historical corpus measurement

> Historical evidence (not current authority; source: Git history):
>
> > Historical evidence (not current authority; source: Git history):
> > Observation boundary: 2026-08-14, corrected 2026-08-19.
> > Counts below exclude `README.md` navigation files. They are path and parsed
> > frontmatter measurements, not claims that every legacy leaf has completed typed
> > metadata migration. Re-verified at the 2026-08-14 boundary with `find`/`rg`
> > against HEAD `ece3eda9c3e1a60`: the leaf-count is now two higher than the prior
> > source-refresh baseline, and the `draft` bucket that previously held 2 leaves
> > is now empty. Both movements trace to the cause the prior revision of this
> > leaf predicted: this deepening effort's own governing Task,
> > `docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
> > (`status: active`, `artifact_type: task`), is itself a Stage 04 leaf, and it
> > entered the corpus already `active` rather than `draft`. This analysis's own
> > evidence trail is therefore part of the population it measures and will move
> > again the next time any Task in the corpus changes `status`.
> >
> > **Superseded 2026-08-19; read this table as a dated snapshot, not as current state.** A seat measured it against the working tree and the figures below are falsified by the taxonomy convergence, which moved Stage 04 evidence into `docs/03.specs/spec-*/task.md` and grew `docs/98.archive`. Re-derived at the review tree: `ls docs/03.specs/*/spec.md | wc -l` returns **32** against a stated 28; `find docs/98.archive -name '*.md' | wc -l` returns **275**, of which 274 carry `status: archived`, against a stated 52; `find docs/04.execution -name '*.md' | wc -l` returns **7** against stated Plan 103 and Task 133; and the registry's `profiles:` key has **23** children against a stated 21. The identical defect in the sibling leaf `document-metadata-lifecycle.md` was marked on 2026-08-19 and this one was missed. Any current figure must be re-derived with the commands above.
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Surface                            | Current measured result                                                                       | Interpretation                                                                                                                                                                                                                                                                                       |
> | ---------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | Stage 01-05 lifecycle leaves       | 533                                                                                           | 25 requirements, 50 architecture, 30 Spec-stage, 236 execution, and 192 operations leaves.                                                                                                                                                                                                           |
> | Lifecycle statuses in those leaves | 298 `active`, 235 `completed`, 0 `draft`                                                      | Status exists across the measured active-stage corpus; `completed` remains durable evidence, not archive. The `draft` bucket is transiently empty, not structurally forbidden.                                                                                                                       |
> | Current parent Specs               | 28 `docs/03.specs/*/spec.md`                                                                  | Replaces the predecessor's stale active-Spec count; unchanged since 2026-08-11.                                                                                                                                                                                                                      |
> | Archived parent Specs              | 32 `docs/98.archive/**/spec.md`                                                               | Archive is populated after the 2026-08-08 migration; zero is false.                                                                                                                                                                                                                                  |
> | Stage 98 non-README leaves         | 52, all `status: archived`                                                                    | Includes 32 typed archive leaves and 20 legacy tombstones without `artifact_type`; path/profile evidence and typed-field evidence must remain distinct.                                                                                                                                              |
> | Stage 99 Markdown                  | 43 total, 35 non-README                                                                       | Template/support corpus; 24 non-README sources declare `status: draft`, while support contracts are governance sources rather than copied target artifacts.                                                                                                                                          |
> | Current role paths                 | PRD 25; ARD 25; ADR 25; Plan 103; Task 133; Guide 66; Policy 64; Runbook 62                   | Role counts are derived from canonical paths. Legacy `artifact_type` coverage is incomplete and cannot replace path measurement. Task moved 132 -> 133 for the same reason the leaf-count and draft bucket moved.                                                                                    |
> | Typed `artifact_type` coverage     | PRD 1/25; ARD 1/25; ADR 1/25; Plan 16/103; Task 20/133; Guide 1/66; Policy 1/64; Runbook 2/62 | Directly re-counted via `grep -l 'artifact_type: <role>'` per family. Typed migration remains shallow outside Plan/Task; a path match is not a typed-field match.                                                                                                                                    |
> | Metadata-profile catalog           | 21 profiles under `profiles:`; 17 `readme_profiles:` entries                                  | `prd, ard, adr, spec, plan, task, guide, policy, runbook, incident, postmortem, release, reference, audit, readme, repo-support, generated, template-source, governance, archive, unsupported`. Nine of the 21 sit outside the twelve human-named SDLC roles the companion role reference documents. |
> | Event roles                        | Incident 0; Postmortem 0; Release 0                                                           | Registered templates/profiles are not proof that an event occurred or that the contracts have been exercised by a real target.                                                                                                                                                                       |
>
> > Historical evidence (not current authority; source: Git history):
> > Observation boundary: 2026-08-14 measurement interpretation.
> > The measured status total is deliberately not called an "active document"
> > count: `active`, `completed`, and `draft` are different lifecycle states, yet
> > all 533 leaves still reside in current Stage 01-05 paths. Likewise, Stage 98
> > tombstones preserve provenance and are not current guidance. The
> > metadata-profile catalog row is a fresh re-derivation this revision adds: the
> > registry's typed surface (21 profiles) is materially larger than the
> > lifecycle-document surface this pack narrates in prose (12 roles), because the
> > registry also types non-lifecycle governance surfaces such as README
> > variants, generated outputs, template sources, and archive tombstones. Do not
> > read "21 profiles" as "21 SDLC document roles"; the extra nine exist to type
> > things this workspace produces but does not treat as spec-driven-lifecycle
> > artifacts.
>
> Current corpus counts must be remeasured against registered paths. The commands
> and profile counts above are historical observations, not current inputs.
>

### Lifecycle and gates

> Historical evidence (not current authority; source: Git history):
>
> This explanatory flow follows [Canonical governance SDLC](../../../../.agents/governance/sdlc.md).
> The Registry owns exact lifecycle values; no table here grants approval.
>
> ```text
> stakeholder intent
>   -> Requirement Package
>   -> Architecture Description + decision-specific ADRs
>   -> parent Spec + focused child contracts
>   -> prospective Plan
>   -> Task implementation/validation/review evidence
>   -> Operations and Task-owned release evidence
>   -> feedback to the earliest owner that must change
> ```
>
> | Transition                                        | Entry evidence                                                                 | Owner and exit evidence                                                                                            | Gate and failure route                                                                                                    |
> | ------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
> | Intent -> Requirement Package                                     | Stakeholder problem, users, value, constraints, and verified current state     | Product owner; numbered Requirement Package with testable requirements, scope, success criteria, and links                         | Human approval plus template/metadata/repository checks; ambiguity returns to intent.                                     |
> | Requirement Package -> Architecture Description/ADR                                    | Approved intent and current architecture constraints                           | System Architect; enduring boundaries/quality attributes plus one ADR per significant choice                       | Architecture review and traceability; infeasibility returns to Requirement Package, while a changed decision creates/supersedes an ADR.   |
> | Architecture Description/ADR -> Spec                                   | Approved upstream constraints and applicable implementation evidence           | Engineering owner; implementable behavior, interfaces, failure modes, verification, and optional focused contracts | Spec and contract checks; gaps return to the earliest requirement/architecture owner.                                     |
> | Spec -> Plan                                      | Stable technical contract and known dependencies                               | Engineering/Project Lead; prospective sequence, risk, intended checks, rollback, and completion criteria           | Plan review and traceability; no executed-result claim belongs here.                                                      |
> | Plan -> Task evidence                             | Approved scope, authority, baseline, dependencies, and approvals               | Implementer/QA; actual changes, commands/results, impact, reviews, commits, deferrals, and blockers                | Focused checks and independent review; failure returns to Task implementation or an earlier contract.                     |
> | Task -> Operations/release evidence                        | Completed implementation evidence and operator/release impact                  | Operations owner; changed guidance/control/procedure or Task-owned release evidence                        | Runtime-specific checks and event evidence; a document, tag, changelog, or CI definition alone does not prove deployment. |
> | Incident/Postmortem/QA/Security -> earliest owner | Observed impact, reviewed learning, failed validation, vulnerability, or drift | Owner selected by gap-to-stage routing; corrected Requirement Package/Architecture Description/ADR/Spec/Plan/Task/Operations artifact                   | Re-run the applicable gate and retain the causal evidence; Stage 90 analysis cannot close the loop.                       |
>

### Traceability model

> Historical evidence (not current authority; source: Git history):
>
> Traceability has four distinct forms that must agree:
>
> 1. `artifact_id`, `type`, `parent_ids`, and `supersedes` encode typed
>    identity and direct relations where the target profile admits them.
> 2. Human `Related Documents` links explain the broader upstream/downstream
>    context; they are not a substitute for direct typed parents.
> 3. Requirement IDs, acceptance criteria, verification cases, Task evidence,
>    and commit identities connect intended behavior to observed results.
> 4. Runtime or remote claims require an authorized observation of the named
>    target and time. Tracked files prove definitions/configuration only.
>
> Broken or ambiguous traceability fails closed. An author must not invent a
> parent, infer priority from `parent_ids` order, or copy a requirement into a
> later artifact merely to make a check pass.
>

### Enforcement layers

> Historical evidence (not current authority; source: Git history):
>
> | Layer                                     | What it establishes                                                                                   | What it cannot establish                                                                   |
> | ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
> | Stage and role contracts                  | Canonical question, path, owner, template, consumer, and evidence duty                                | That a target followed the contract or was approved.                                       |
> | Metadata registry and checker             | Profile match, fields, relations, headings, lifecycle transitions, and changed/new blocking semantics | Product correctness, runtime state, or remote enforcement.                                 |
> | Specs and child contracts                 | Implementable behavior and verification criteria                                                      | That implementation or tests passed.                                                       |
> | Plans and Tasks                           | Intended work versus observed work/evidence                                                           | That a remote CI rule, provider, deployment, or service executed unless directly observed. |
> | Focused validation and independent review | Reproducible local results and a bounded verdict over an exact range                                  | Universal correctness beyond the reviewed inputs and environment.                          |
> | CI/workflow configuration                 | A tracked automation definition                                                                       | A successful run, required-check configuration, branch protection, or production outcome.  |
> | Release/operations evidence               | A bounded event or operating contract                                                                 | Deployment/runtime proof outside the separately evidenced chain.                           |
>
> > Historical evidence (not current authority; source: Git history):
> > Observation boundary: 2026-08-14 checker inspection.
> > Two named scripts implement the traceability/alignment slice of this table
> > and were re-read directly this revision rather than assumed from their names.
> > `check-doc-traceability.sh` (90 lines) is **not** requirement-ID or
> > artifact-graph tracing; it checks reciprocal README links between
> > `docs/04.execution/` and `docs/05.operations/`, priority-Plan links to the
> > operations policy catalog/index, and that catalog `OPER`/`RUN` targets exist —
> > a link-literal check, not a `parent_ids`/requirement-ID verifier.
> > `check-doc-implementation-alignment.sh` (261 lines, inline Python) walks
> > active Stage 01-05 Markdown, extracts referenced repository paths, and
> > confirms each resolves against a fixed prefix/file allowlist (`docs/`,
> > `infra/`, `scripts/`, `.github/`, `.claude/`, `.codex/`, `secrets/`,
> > `projects/`, `tests/`, named root files) — it catches a doc citing a path no
> > longer in the tree, not whether the cited path's content matches the doc's
> > claim about it. Neither performs end-to-end requirement-to-commit tracing;
> > both are narrower verifiers this repository composes with the metadata
> > checker and human review to approximate full traceability.
>
> The current document-graph validator implements the traceability/alignment
> slice of this table. `check-document-links.py --mode all` owns reciprocal
> catalog and operations links, rendered Markdown targets and anchors, and
> current document references to repository paths. It detects missing or
> prohibited graph edges; it does not prove that a referenced implementation
> behaves as the prose claims. End-to-end requirement-to-commit traceability
> therefore still requires metadata validation, Task evidence, and human review.
>

### External implementations and standards boundary

> Historical evidence (not current authority; source: Git history):
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source                                                                                                                     | Verified observation                                                                                                                                                                                                                                                                                                                                            | Workspace disposition                                                                                                                                                                                                                                                                                                                                                                              |
> | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | GitHub Spec Kit, re-pinned `83883a2ebad7e7de667fd00381b100d597faf846` (2026-08-14; was `684b3d8e0` on 2026-08-08)          | The flow grew from four phases to ten named phases/commands: `constitution` (governing principles; new first step), `specify`, `clarify`, `plan`, `tasks`, `analyze`, `checklist`, `taskstoissues` (new: converts tasks to GitHub Issues), `implement`, and `converge` (new: assesses codebase against spec/plan/tasks and appends remaining work).             | Its new `constitution` prefix and `converge` drift-detection step echo functions this workspace already separates into other owners (Stage 00 governance; QA/security drift routing). Still a comparative harness; this workspace's PRD/architecture prefixes, durable Task evidence, operations, archive, and feedback owners remain unadopted-but-analogous.                                     |
> | Fission-AI OpenSpec, re-pinned `2826b8889e5223a9a8095d4428b60b56597e1020` (2026-08-14; was `e50bd0983d` on 2026-08-08)     | Core artifact structure is unchanged (`proposal.md`, `specs/`, `design.md`, `tasks.md`, archived to `openspec/changes/archive/<date>-<name>/`), now fronted by slash commands `/opsx:explore` (new: pre-proposal exploration), `/opsx:propose`, `/opsx:apply`, and `/opsx:archive`, with tool-specific aliases for Cursor/Amazon Q/Codex.                       | The live-Spec/in-flight-change split and new pre-proposal explore step resemble this workspace's Spec-stability-before-Plan and clarification norms; paths, commands, and archive semantics remain unadopted.                                                                                                                                                                                      |
> | ISO/IEC/IEEE 12207:2026                                                                                                    | Public catalog says it covers conception through retirement and permits concurrent, iterative, recursive, and incremental application without requiring one lifecycle model.                                                                                                                                                                                    | Catalog/abstract comparison only. Purchased full text was not accessed and is **UNVERIFIED**; no conformance claim is made. Not re-fetched this revision: `iso.org` is a known HTTP-403 host for automated retrieval, so the claim needs revalidation by a browser-capable reviewer, not another automated attempt.                                                                                |
> | ISO/IEC/IEEE 29148:2018 and 42010:2022                                                                                     | Public catalogs describe requirements-engineering information items and architecture descriptions.                                                                                                                                                                                                                                                              | Context for PRD/architecture analysis only. Purchased full text was not accessed and is **UNVERIFIED**; same `iso.org` 403 condition applies.                                                                                                                                                                                                                                                      |
> | RFC Editor                                                                                                                 | Official home and archive for RFCs, including Standards and Best Current Practices.                                                                                                                                                                                                                                                                             | Example of a governed publication series, not a template or lifecycle owner for this repository.                                                                                                                                                                                                                                                                                                   |
> | Landscape survey (MarkTechPost, Augment Code, Glukhov, Daniliants — secondary/aggregator sources, 2026-05 through 2026-08) | By 2026, GitHub Spec Kit, AWS Kiro, Cursor, OpenSpec, BMAD, and Tessl each ship a distinct spec-driven flavor; Kiro is described as lightest (three Markdown files, IDE-native), Spec Kit as most customizable but heaviest (most artifacts per feature, CLI-driven), and Tessl as a language-agnostic "tiles" framework layered onto any MCP-compatible agent. | **Landscape context only — External mutable, lower confidence than the primary-vendor rows above.** Third-party comparison articles, not vendor documentation; not cross-verified against each tool's own repository. Cited only to show this workspace's multi-artifact, stage-gated approach sits at the heavier/more-durable end of a real 2026 tool spectrum, not to endorse or rank any tool. |
>

### Feedback and evidence rules

> Historical evidence (not current authority; source: Git history):
>
> - A validation failure changes Task evidence first; revise a Spec only when the
>   failure demonstrates that the technical contract is wrong or incomplete.
> - An incident owns live event state. A Postmortem owns reviewed causal learning
>   and preventive actions after stabilization.
> - A vulnerability can route to Policy, ADR, Spec, Plan, Task, Runbook, or all of
>   them through links, but each fact has one earliest canonical owner.
> - Release evidence follows the current
>   [external-release-evidence policy](../../../../.agents/governance/documentation-protocol.md#release-evidence-boundary),
>   not an independent Release profile. Notes, SemVer, tags, builds, and readiness
>   evidence each prove only their own observed fact.
> - A reference, audit, graph, generated index, or template may inform work but
>   cannot authorize a lifecycle transition or protected mutation.
>

### Carried source-evidence claims

> Historical evidence (not current authority; source: Git history):
>
> Source-evidence claims carried forward from the superseded 2026-07-05
> research pack on 2026-08-19. Each states what the upstream evidence supports
> and, where it matters more, what it does not.
>
> - **Two standards status claims carry unreconciled provenance.** The 29148:2018 and 42010:2022 status claims retain earlier retrieval provenance and were not re-verified on the date stated beside them. Carried as the contradiction rather than as either claim, because choosing one silently discards the other provenance.
>

## Scope Implications

> Historical evidence (not current authority; source: Git history):
>
> | Scope          | Application and disposition                                                                                                                                                          |
> | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
> | `agentic`      | Agents must load the applicable contract, preserve stage ownership, use bounded loops, record evidence, and stop on missing authority; automation does not collapse lifecycle roles. |
> | `architecture` | Architecture constraints belong in Architecture Descriptions and significant choices in ADRs before Specs consume them; runtime architecture remains separately evidenced.                                |
> | `backend`      | API, data, failure, and service behavior requires a parent Spec and focused contracts/tests where complexity warrants them.                                                          |
> | `common`       | Shared standards and review conventions support every gate but cannot create a parallel lifecycle or bypass canonical owners.                                                        |
> | `docs`         | Owns template-first authoring, metadata/link validation, archive boundaries, and Stage 90 advisory framing; Stage 01-99 writes still require explicit scope.                         |
> | `entry`        | Gateway changes route through requirements, architecture, Spec, Task, and operations evidence with explicit runtime/rollback boundaries.                                             |
> | `frontend`     | UI behavior, accessibility, state, and browser evidence follow the same Spec-to-Task chain; generated UI is not accepted from screenshots or prompts alone.                          |
> | `infra`        | Compose and infrastructure definitions are implementation evidence and require Spec, validation, rollback, and operations handoff; they are not the SDLC owner.                      |
> | `meta`         | The registry, templates, validators, and taxonomy encode lifecycle semantics; changes require their own approved metadata/docs chain rather than edits in this reference.            |
> | `mobile`       | No current mobile implementation is established; any future work needs an approved product/architecture/Spec chain plus device-specific evidence.                                    |
> | `ops`          | Owns guides, policies, runbooks, incidents, postmortems, and Task-owned release evidence; event evidence feeds upstream owners without turning operations prose into product intent.                    |
> | `product`      | Human stakeholders own intent, value, scope, requirements, and acceptance; an agent or external tool cannot infer approval.                                                          |
> | `qa`           | Owns verification strategy, focused evidence, failure routing, and independent quality review; a passing local check is bounded to its command/environment.                          |
> | `security`     | Security requirements, decisions, controls, tests, incidents, and remediation remain traceable with least privilege, redaction, and approval boundaries.                             |
>

## Sources

> Historical evidence (not current authority; source: Git history):
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source                                                                                                                                                   | Accessed   | Class                        | Use and verification state                                                                                                                               |
> | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | [GitHub Spec Kit documentation](https://github.github.com/spec-kit/)                                                                                     | 2026-08-08 | External mutable             | HTTP 200; current phase flow and artifact handoff.                                                                                                       |
> | [GitHub Spec Kit immutable tree, re-pinned](https://github.com/github/spec-kit/tree/83883a2ebad7e7de667fd00381b100d597faf846)                            | 2026-08-14 | External fixed               | `git ls-remote` HEAD re-pin (moved from `684b3d8e0`); ten-phase flow read from raw README at this commit.                                                |
> | [OpenSpec immutable README, re-pinned](https://raw.githubusercontent.com/Fission-AI/OpenSpec/2826b8889e5223a9a8095d4428b60b56597e1020/README.md)         | 2026-08-14 | External fixed               | `git ls-remote` HEAD re-pin (moved from `e50bd0983d`); slash-command workflow read at this commit.                                                       |
> | [Landscape survey articles](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/) | 2026-08-14 | External mutable, secondary  | Aggregator comparison of Spec Kit/Kiro/OpenSpec/Tessl/BMAD; landscape context only, not primary vendor evidence.                                         |
> | [ISO/IEC/IEEE 12207:2026 catalog](https://www.iso.org/standard/90219.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**. Not re-fetched 2026-08-14: `iso.org` returns HTTP 403 to automated retrieval. |
> | [ISO/IEC/IEEE 29148:2018 catalog](https://www.iso.org/standard/72089.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                                                                               |
> | [ISO/IEC/IEEE 42010:2022 catalog](https://www.iso.org/standard/74393.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                                                                               |
> | [RFC Editor](https://www.rfc-editor.org/)                                                                                                                | 2026-08-08 | External mutable catalog     | HTTP 200; official RFC series and publication classes only.                                                                                              |
> | [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)                                                                                   | 2026-08-08 | External fixed               | HTTP 200; April 2025 final CSF 2.0 incident-response profile. Rev. 2 is superseded and not used.                                                         |
> | [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/)                                                                         | 2026-08-08 | External fixed publication   | HTTP 200; learning, triggers, blamelessness, review, and preventive actions.                                                                             |
> | [Stage authoring matrix](../../../../.agents/governance/stage-authoring-matrix.md)                                                                   | 2026-08-08 | Workspace tracked            | Canonical stage purposes, inputs, templates, and done criteria at Task 5 baseline.                                                                       |
> | SDLC document contract (retired path: `../../../99.templates/support/sdlc-document-contract.md`)                                                                        | 2026-08-08 | Workspace tracked            | Human lifecycle and feedback boundary.                                                                                                                   |
> | Metadata profiles (retired path: `../../../99.templates/support/document-metadata-profiles.yaml`)                                                                       | 2026-08-14 | Workspace tracked            | Re-read to confirm 21 profiles / 17 README profiles at current HEAD.                                                                                     |
> | [Document graph validator](../../../../scripts/validation/check-document-links.py)                                                                       | 2026-09-04 | Workspace tracked executable | The typed `--mode all` route owns both rendered-link traceability and current-path alignment checks.                                                      |
> | Graphify report (`graphify-out/GRAPH_REPORT.md`, untracked local output since 2026-09-08)                                                                                              | 2026-08-08 | Workspace stale/advisory     | Built from `f8a72211`; all used claims corroborated against current tracked sources.                                                                     |
>

## Scope Application

> Historical evidence (not current authority; source: Git history):
>
> | Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
> | --- | --- | --- | --- | --- |
> | agentic | applies | Relate agent work to a durable Spec and Task. | Inspect the current Spec package. | No agent execution is proved. |
> | architecture | applies | Keep architecture intent in its typed owner. | Check the current Stage 03 Spec/Plan/Task route before a decision. | Tool phases do not assign architecture authority. |
> | common | applies | Preserve approved handoff and capture rules. | Review the scoped diff. | Advisory comparison only. |
> | docs | applies | Use Spec/Plan/Task roles when documenting work. | Check frontmatter and links. | No workflow adoption is implied. |
> | infra | applies | Connect infrastructure change intent to its Spec/Plan/Task owner. | Check the scoped package and infrastructure owner. | No runtime evidence. |
> | ops | applies | Feed operational incidents and learning back to their owner. | Confirm catalog or incident-packet path. | No operation is inferred. |
> | qa | applies | Capture checks against the Task. | Inspect recorded check evidence. | A record is not a green suite. |
> | security | applies | Retain approval and source boundaries. | Review cited local sources. | No control effectiveness is evaluated. |
>

## 2026-09-05 Revalidation

> Historical evidence (not current authority; source: Git history):
>
> Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
> The current repository route is Requirement → Architecture/ADR → Spec → Plan
> → Task → Verification → Independent Review, with Plan and Task co-located in
> the Spec package. GitHub Spec Kit's current public workflow likewise separates
> Spec, Plan, Tasks, and Implement, but this repository's Registry and SDLC are
> the local authority.
>
> | Capability | Repository implementation | Evidence depth | Gap | Verification route |
> | --- | --- | --- | --- | --- |
> | Intent decomposition | Registered Stage 01–03 roles and internal IDs | Repository-enforced | Product acceptance remains owner-specific | coverage and traceability checks |
> | Lifecycle | Profile-specific initial/transition/terminal graphs | Repository-enforced | No shortcut from draft to terminal | lifecycle transition validation |
> | Review boundary | Protected-surface and independent exact-diff review policy | Defined | Review quality is contextual | recorded verdict and rerun evidence |
> | Operations handoff | Stage 05 owns procedures and incidents | Repository-enforced | Live deployment target absent | Runbook and Task acceptance |
>
> Recommendation: use external SDD tools as comparative evidence, not as a
> replacement for the repository's identities or lifecycle. Official comparison:
> [GitHub Spec Kit](https://github.github.com/spec-kit/).
>

## Maintenance

> Historical evidence (not current authority; source: Git history):
>
> Re-measure counts and re-open mutable sources when stages, templates, metadata
> profiles, lifecycle/archive contracts, validator behavior, Spec Kit, OpenSpec,
> or official standard status changes. Keep current-path counts separate from
> typed-metadata coverage and never infer runtime, remote, release, or deployment
> outcomes from tracked documentation alone. Re-pin Spec Kit and OpenSpec at
> their current HEAD on each future revision: both moved substantially between
> 2026-08-08 and 2026-08-14 (four phases to ten for Spec Kit; a new explore
> command for OpenSpec), so treating either pin as durable across a longer gap
> would understate real upstream drift.
>


## Related Documents

- [Research pack](README.md)


- [Verification and validation](./m0019-verification-validation.md)
- [SDLC document roles](./m0016-sdlc-document-roles.md)
- [Document metadata lifecycle](./m0006-document-metadata-lifecycle.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
