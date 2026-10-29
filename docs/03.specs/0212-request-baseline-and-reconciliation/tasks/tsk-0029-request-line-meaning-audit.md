---
title: "Request Line Meaning Audit Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0029"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Request Line Meaning Audit Task

## Overview

### Objective

Execute W45: audit the meaning of each of the 355 non-blank lines of the
request's appendix R against the current repository, and correct a stale
statement the audit found. This Task owns criterion 40 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for the request-line meaning audit that
TSK-0026 recorded as not performed (CR-01.02), followed by commit, pull
request, and merge. The input is `main` at merged PR #626 and the owner's
pasted request, whose appendix R holds 383 line positions (355 non-blank). The
authorization covers this audit, the stale-text correction below, this
branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0029 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0029 | ready | in-progress | #objective |
| SPEC-0212-TSK-0029 | in-progress | completed | #evidence |

### Method

Appendix R is a normalized execution copy, not the raw request; the raw text
is not available, so wording and byte preservation stay unverified. Three
read-only reviewers split the 383 positions (L001–L100, L101–L200,
L201–L383). Each classified every line as blank, structure, context, or duty;
split each duty line into atoms; named one primary CR; and judged this
repository against the atoms with a current file path. The lead review
checked that every position appears once, that every primary CR exists among
the 148, and spot-read the weakest `MET` rows. It downgraded four of them to
`PARTIAL` (L147, L179, L265, L272) and confirmed the stale text behind L157.

### Result

| Result | Non-blank lines | Meaning |
| --- | --- | --- |
| `MET` | 159 | All atoms hold in this repository today |
| `PARTIAL` | 106 | Some atoms hold; the note names the rest |
| `NOT_MET` | 2 | This repository does not satisfy the line |
| `NOT_RUN` | 6 | Needs the other three repositories, held by the owner |
| No duty | 82 | Heading, label, or reference text |

The 28 blank positions and the 82 no-duty lines are L002–L011, L013–L029, L032, L087, L114, L143, L183–L185, L190–L200, L287, L303–L314, L321–L337, L343–L344, L346–L367, L370, L372–L381. Every other position is listed below.

### Correction made

`.agents/governance/environment-constraints.md` said that only two
`_workspace` READMEs are tracked and that runtime files stay under
`repo-support/`. Seven READMEs are tracked and `diagnostics/` is also a
runtime tree, as `_workspace/README.md` and `.gitignore` state. The policy
now matches (version 1.6.1). That closes L157.

### Rewritten lines

The request names 17 lines rewritten for execution. Judged only against the
lines around them:

| Line | Possible loss |
| --- | --- |
| L001, L012, L030, L280, L287 | None visible |
| L031 | Reads as permission to leave scope incomplete; L032–L034 require the investigation |
| L189 | May have lost its list marker and per-workspace scope |
| L202 | May have lost the fact-versus-candidate distinction that L208 keeps |
| L211, L235, L289 | May have lost "every" or ordering detail |
| L225 | Keeps "first" but not the ban on back-dating later research |
| L240 | Does not carry the archive-first, SDLC-second order of L300–L301 |
| L242 | Omits the no-time-based-deletion condition of L252 and L261 |
| L248 | May have dropped per-installation memory identity (CR-17.08) |
| L277 | Omits moving a continuing guarantee before deletion (CR-11.02) |
| L278 | Drops "global", which L279 restates |

### Line results

| Line | Primary CR | Result | Evidence | Note |
| --- | --- | --- | --- | --- |
| L001 | CR-01.03 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0026 (baseline readback, KEEP decisions) | Rewritten line; raw original unavailable. Text is a basis statement with no visible prohibition/exception; consistent with L012 and L031. Cannot rule out a dropped qualifier. |
| L012 | CR-01.05 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0026 (HEAD/ls-remote readback); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/t… | This repo met (TSK-0026). other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps). Rewritten; raw original unavailable; internally consistent with L007-L010, no visible condition l… |
| L030 | CR-03.03 | PARTIAL | .agents/governance/bootstrap.md; .agents/governance/providers/registry.yaml; .claude/provider.md | Local common+adapter split met. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps). Rewritten; raw original unavailable; consistent with L040-L042 (common vs local), no visibl… |
| L031 | CR-01.02 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0026 (line audit and CR pairs recorded UNVERIFIED/NOT_RUN) | Rewritten; raw original unavailable. Risk: may soften a full-inventory obligation into a deferral clause; sits in tension with L032-L034 which demand investigation. Flag for owner. |
| L033 | CR-04.01 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027, tsk-0028 (archive, SDLC, CI reads); docs/03.specs/0212-request-baseline-and-reconciliati… | Only archive/SDLC/CI areas read here; no full conflict inventory. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L034 | CR-04.01 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027, tsk-0028; tsk-0026 | Same as L033 (near-duplicate line). other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L035 | CR-06.05 | MET | .agents/governance/sdlc.md (promotion receipt); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0026 (KEEP/CHANGE) | Promotion receipt in Task Evidence; metadata contracts PASS in TSK-0026 |
| L036 | CR-05.04 | MET | docs/99.templates/registry.json (lifecycles navigation, operational-policy, incident, postmortem); .agents/governance/sdlc.md | Registry lifecycles cover READMEs and operations families |
| L037 | CR-05.13 | PARTIAL | docs/99.templates/registry.json lifecycles; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017 (editions differ) | Single lifecycle set locally. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L038 | CR-05.03 | PARTIAL | docs/99.templates/templates/; registry.json profiles | Local profiles/templates unified. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L039 | CR-05.03 | PARTIAL | docs/99.templates/contracts/document-frontmatter.schema.json | Local schema unified. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L040 | CR-03.03 | PARTIAL | .agents/governance/sdlc.md; .agents/governance/output-style.md | All four atoms met locally; commonality across repos other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L041 | CR-03.03 | MET | .agents/governance/providers/registry.yaml; .claude/provider.md; .codex/provider.md | Permission; repo uses its own native adapters |
| L042 | CR-03.03 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0020 (NFR quality characteristic+measure in requirement template) | Local selection mechanism exists via requirement template |
| L043 | CR-07.01 | MET | registry.json README profiles (documentation-readme, repository-readme, package-readme, readme...); .agents/governance/documentation-protocol.md#readme-navigat… | Per-role README profiles and navigation check |
| L044 | CR-07.01 | MET | registry.json README profiles; docs/99.templates/templates/ | Profiles differ by role |
| L045 | CR-07.02 | MET | .agents/governance/documentation-protocol.md#document-language; .agents/governance/standards.md | Language priority order and authoring rules stated |
| L046 | CR-03.07 | PARTIAL | .agents/governance/sdlc.md (acceptance domain) | Local acceptance contract exists. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L047 | CR-03.02 | PARTIAL | .github/CODEOWNERS; frontmatter owner @buenhyden | Owner found; no joint cross-repo decision body defined in .agents/governance (grep found none) |
| L048 | CR-03.06 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017 (Four repositories: no shared edition id) | Investigated and gap recorded; no edition-consumption condition added. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L049 | CR-06.01 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028 (SDLC read); .agents/governance/sdlc.md | This repo read and matched. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L050 | CR-06.07 | MET | .agents/governance/sdlc.md (Spec Kit adaptation); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028 | - |
| L051 | CR-06.02 | MET | .agents/governance/sdlc.md (Execution state has one owner); registry.json lifecycles.task | - |
| L052 | CR-06.02 | MET | .agents/governance/sdlc.md; docs/99.templates/templates/specs/ | - |
| L053 | CR-06.03 | MET | registry.json lifecycles (terminal sets per family); .agents/governance/sdlc.md | - |
| L054 | CR-06.06 | MET | .agents/governance/sdlc.md (Result vocab, acceptance domain, readiness not stored, lifecycle grants no permission) | - |
| L055 | CR-06.04 | MET | .agents/governance/sdlc.md (promotion receipt); registry Evidence/Criterion Acceptance shapes | - |
| L056 | CR-10.03 | MET | .agents/governance/quality-standards.md section 10; .markdownlint-cli2.yaml ignore list; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027 | Commit checks never rewrite; frozen bodies excluded |
| L057 | CR-14.02 | MET | .agents/governance/sdlc.md (summary derived on read); .agents/governance/github-governance.md#issues-and-projects; documentation-protocol.md (no second status… | - |
| L058 | CR-06.03 | MET | registry.json lifecycles; .agents/governance/sdlc.md | Distinct state sets per family |
| L059 | CR-08.06 | PARTIAL | .agents/governance/documentation-protocol.md#retirement-preconditions (current Task receipt); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-… | Practice met (archive done inside SPEC-0212 Tasks); no explicit prohibition text in governance |
| L060 | CR-04.02 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0024, tsk-0025, tsk-0027 | Stale paths/routes/reasons corrected |
| L061 | CR-07.03 | MET | .agents/governance/documentation-protocol.md#readme-navigation (historical quotation rule); docs/98.archive/README.md | - |
| L062 | CR-08.03 | MET | .agents/governance/documentation-protocol.md (Current assessment and Git-history-only availability); docs/03.specs/0212-request-baseline-and-reconciliation/tas… | - |
| L063 | CR-05.13 | MET | registry.json transitions; .agents/governance/sdlc.md; Task Lifecycle Events in docs/03.specs/0212-request-baseline-and-reconciliation/tasks/ | - |
| L064 | CR-06.06 | MET | .agents/governance/sdlc.md (promotion receipt, Outputs); .agents/governance/stage-authoring-matrix.md | Source line has typo 'yong' for acceptance; meaning clear |
| L065 | CR-06.01 | PARTIAL | .agents/governance/documentation-protocol.md#role-specific-authoring; .agents/governance/stage-authoring-matrix.md | Local roles defined. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L066 | CR-05.01 | PARTIAL | registry.json profiles (separate specs contracts: data-model/openapi/graphql/proto) | Separation exists in registry; no recorded analysis result for this request |
| L067 | CR-05.03 | MET | docs/99.templates/contracts/document-frontmatter.schema.json; registry.json archive-record profiles; .agents/governance/sdlc.md (archive keeps status) | - |
| L068 | CR-08.06 | MET | .agents/governance/documentation-protocol.md (retention by status, readiness derived; current Task receipt); docs/03.specs/0212-request-baseline-and-reconcilia… | Archive executed as Tasks of existing SPEC-0212 |
| L069 | CR-21.04 | MET | .agents/governance/approval-boundaries.md; .agents/governance/workflows.md#change-lifecycle | - |
| L070 | CR-10.04 | MET | .agents/governance/quality-standards.md sections 3-5 (local_only_gate_ids, wording-only rule) | - |
| L071 | CR-07.05 | PARTIAL | .agents/governance/documentation-protocol.md (Historical recovery route); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0013 (postmortem due… | No recorded review of operations-document volume found |
| L072 | CR-11.02 | MET | .agents/governance/quality-standards.md section 3 (Retire one-time QA in this order) | - |
| L073 | CR-10.06 | MET | .agents/governance/quality-standards.md#canonical-delivery-phase-matrix; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028 (CI/QA read) | - |
| L074 | CR-08.01 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027; .agents/governance/documentation-protocol.md Stage 98 | - |
| L075 | CR-07.05 | PARTIAL | .agents/governance/documentation-protocol.md#role-specific-authoring, #release-evidence-boundary | Local roles defined; no recorded per-workspace list. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L076 | CR-04.02 | PARTIAL | .agents/governance/documentation-protocol.md (retirement); registry deprecated states; .agents/governance/quality-standards.md section 3 | Rules exist; no recorded legacy/deprecated analysis result for this request |
| L077 | CR-04.01 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0026 (CR-04.04 not performed); tsk-0027, tsk-0028 | Area reads only; full duplication/conflict check recorded as not performed |
| L078 | CR-05.13 | PARTIAL | registry.json lifecycles; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017 | Unified locally. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L079 | CR-11.04 | PARTIAL | .agents/governance/quality-standards.md (ordinary documents get minimal checks); docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0014 | Rule exists; no recorded bottleneck investigation result |
| L080 | CR-08.01 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027, tsk-0011, tsk-0012; docs/98.archive/README.md | - |
| L081 | CR-06.05 | MET | .agents/governance/sdlc.md; Task Lifecycle Events; check-document-metadata contracts | - |
| L082 | CR-21.03 | MET | .agents/governance/approval-boundaries.md (approved local authoring may edit documentation) | - |
| L083 | CR-21.03 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0013 (blocked items), tsk-0015 (applied) | - |
| L084 | CR-13.01 | PARTIAL | .agents/governance/git-workflow.md sections 4-5 | Atomic logical commits met; merge-per-Spec not stated in governance and practice is one PR per Task |
| L085 | CR-11.04 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0014 (one slow check fixed) | No workspace-wide bottleneck analysis recorded. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L086 | CR-11.04 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0014 | Same as L085. other three repos NOT_RUN (owner holds four-repository adoption; TSK-0017/0018 read-only gaps) |
| L088 | CR-11.02 | MET | .agents/governance/quality-standards.md section 3; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0015, tsk-0016, tsk-0017 | - |
| L089 | CR-11.01 | PARTIAL | .agents/governance/quality-standards.md sections 3, 7; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017, tsk-0025 | Governance rule present; no recorded current inventory of legacy QA for this request |
| L090 | CR-11.01 | PARTIAL | .agents/governance/quality-standards.md sections 3, 7; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017, tsk-0025 | Governance rule present; no recorded current inventory of deprecated QA for this request |
| L091 | CR-11.01 | PARTIAL | .agents/governance/quality-standards.md sections 3, 7; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017, tsk-0025 | Governance rule present; no recorded current inventory of duplicated QA for this request |
| L092 | CR-11.01 | PARTIAL | .agents/governance/quality-standards.md sections 3, 7; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017, tsk-0025 | Governance rule present; no recorded current inventory of conflicting QA for this request |
| L093 | CR-11.01 | PARTIAL | .agents/governance/quality-standards.md sections 3, 7; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0017, tsk-0025 | Governance rule present; no recorded current inventory of excessive QA for this request |
| L094 | CR-10.01 | PARTIAL | scripts/manifest.yaml; check-script-manifest.py PASS in docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028 | Scripts covered by manifest check; no recorded tests/ compliance audit |
| L095 | CR-10.06 | MET | .agents/governance/quality-standards.md#canonical-delivery-phase-matrix; docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028 | - |
| L096 | CR-10.05 | MET | .agents/governance/quality-standards.md section 4 (local_only_gate_ids, hosted-unit set) and phase matrix | - |
| L097 | CR-10.05 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0028; .agents/governance/github-governance.md section 8 | - |
| L098 | CR-10.06 | MET | .agents/governance/quality-standards.md#canonical-delivery-phase-matrix (feature push none, main push no repeat) | - |
| L099 | CR-10.05 | MET | .agents/governance/quality-standards.md phase matrix; .agents/governance/git-workflow.md section 3 | - |
| L100 | CR-13.02 | MET | .cz.toml; .gitmessage; .pre-commit-config.yaml commitizen hook; .agents/governance/git-workflow.md section 1 | Commitizen chosen; .gitmessage is the authoring aid |
| L101 | CR-13.05 | MET | .github/workflows/publish-release.yml; scripts/operations/release.py; .agents/governance/git-workflow.md:114-118; TSK-0019 (0.0.1 has Release) | Sole main-only producer creates v-SemVer tag + Release; legacy bare 0.0.1 kept as history. |
| L102 | CR-13.05 | MET | CHANGELOG.md (Keep a Changelog + SemVer); .agents/governance/git-workflow.md:112-113 | Main-targeted release-prep PRs own CHANGELOG; no dev push generates one. |
| L103 | CR-10.05 | PARTIAL | .github/workflows/ci-quality.yml (candidate-quality changed profile, main-security); .agents/governance/quality-standards.md delivery phase matrix; SPEC-0211 T… | Stage matrix implemented; SPEC-0211 criteria 2-3 still pending and no measured per-stage before/after (CR-11.04). |
| L104 | CR-11.01 | PARTIAL | SPEC-0211 TSK-0001 (test retirement sections, in-progress); quality-standards.md:96-117 | Retirement done in part; SPEC-0211 criterion 1 pending; agent-governance/memory/release tests stay under CR-11.01 guarantee-based reconciliation with L201. |
| L105 | CR-11.01 | PARTIAL | docs/90.references/research/0084-github-actions-platform; research pack m0014; SPEC-0211 TSK-0001 | Research and partial pruning exist; SPEC-0211 acceptance pending, so consolidation not accepted. |
| L106 | CR-10.01 | MET | TSK-0025 (dead CI route), TSK-0028 (CI read), TSK-0007:510-520 workflow ownership; .github/repository-surface.md | Recorded results exist. |
| L107 | CR-10.01 | MET | .github/workflow-contract.yml; TSK-0028 (5 workflows, 7 jobs PASS); TSK-0007:510-520; scripts/manifest.yaml | Per-workflow owner recorded; manifest and contract checks pass. |
| L108 | CR-14.01 | PARTIAL | .github/ISSUE_TEMPLATE/*.yml; .agents/governance/github-governance.md:43-49,204-213 | Issue forms applied; no Project exists, Project automation needs owner approval (CR-14.03 projection tests not run). |
| L109 | CR-14.02 | MET | .agents/governance/github-governance.md:43-49,204-213 | Ownership split and both prohibitions stated. |
| L110 | CR-10.04 | MET | scripts/validation/run-ci-gate.py --profile changed; quality-standards.md:226-233 (wording edits select no implementation suites) | Change-impact selection in place. |
| L111 | CR-18.01 | MET | .agents/governance/agentic.md:36-42 | Before a required check, record tool, environment, permission and budget route. |
| L112 | CR-11.01 | PARTIAL | TSK-0013 Kept; TSK-0016/0017 absence-test dispositions; SPEC-0211 TSK-0001 | Improvements kept; remaining special cases (e.g. archive.py migration-0003 constants) not fully cleared; SPEC-0211 pending. |
| L113 | CR-11.02 | PARTIAL | .agents/governance/quality-standards.md:96-101; scripts/lib/document_governance/archive.py:44-51,705-800; lifecycle/recovery.py:32-33 | Policy states the distinction, but general archive/lifecycle code still runs migration-0003 and Task-10 cutover proofs (275-row check); no recorded separation. |
| L115 | CR-11.02 | MET | .agents/governance/quality-standards.md:96-101 | Sequence codified verbatim. |
| L116 | CR-10.04 | MET | .agents/governance/quality-standards.md:226-229 | Profile/parent/lifecycle remote; links in local lane. |
| L117 | CR-11.04 | PARTIAL | TSK-0014 (archive check 291s cost removed); quality-standards.md | Order not stated in governance; only one measured optimization recorded; SPEC-0211 pending. |
| L118 | CR-13.05 | MET | .agents/governance/git-workflow.md:112-118; publish-release.yml; CHANGELOG.md | - |
| L119 | CR-13.05 | MET | .agents/governance/git-workflow.md:112-113; TSK-0015 (git-cliff removed) | - |
| L120 | CR-13.06 | MET | publish-release.yml step 'Create draft, attach complete assets and publish'; scripts/operations/release.py | Draft-assets-publish order implemented unconditionally; immutable-release adoption state itself not recorded. |
| L121 | CR-10.06 | MET | TSK-0007 leaf producer inventory; TSK-0013 Kept (CI leaf de-dup); quality-standards.md:211-241 | Recorded inventory and one-owner-per-boundary matrix. |
| L122 | CR-10.05 | PARTIAL | quality-standards.md:211-241 (no feature-push QA); TSK-0014 | Stage matrix exists; no reproducible per-stage timing comparison recorded beyond the archive check. |
| L123 | CR-10.03 | MET | .agents/governance/quality-standards.md §10; .pre-commit-config.yaml; TSK-0028 CI/QA read | Check-only commit hooks, manual fixers, files selectors. |
| L124 | CR-11.01 | MET | TSK-0025 (56 missing paths scan); TSK-0024; scripts/validation/check-script-manifest.py | Recorded scans and fixes. |
| L125 | CR-10.02 | MET | quality-standards.md §7, §10; scripts/validation/run-ci-gate.py; scripts/manifest.yaml; .github/workflow-contract.yml | One orchestrator and one manifest. |
| L126 | CR-11.01 | PARTIAL | quality-standards.md:364-368; scripts/lib/document_governance/archive.py:789-800 (task10_rows) | Policy says a gate owns a current invariant; archive library still carries Task-10/migration-0003 specific logic. |
| L127 | CR-13.07 | PARTIAL | .agents/governance/git-workflow.md:60-76; TSK-0018 (merge methods) | Settings adjusted, but no recorded strategy evaluation against external workflows with alternatives/cost (CR-13.07). |
| L128 | CR-10.06 | MET | .github/workflows/ci-quality.yml:18-19,181-182; TSK-0028 | PR candidate vs main-push security only. |
| L129 | CR-10.06 | MET | quality-standards.md:211-241; .pre-commit-config.yaml; ci-quality.yml | Commit and PR lint differ by trust/input per CR-10.06. |
| L130 | CR-11.01 | PARTIAL | TSK-0016, TSK-0017; SPEC-0211 TSK-0001 'Completed-document and retired-file expectation retirement' | Dispositions recorded for absence tests; no full census accepted (SPEC-0211 criterion 1 pending). |
| L131 | CR-11.01 | MET | TSK-0019 (Task-path tests use synthetic fixtures); tests/lib/document_governance/test_archive.py:671 | Remaining real-file read is the digest-pinned frozen migration-0003 record, not a completed document's current state. |
| L132 | CR-11.01 | PARTIAL | TSK-0017 (check-repo-contracts guard removed); scripts/lib/document_governance/archive.py:45-48 ONE_TIME_VERIFIER_PATHS | archive.py still asserts two discarded one-time verifier paths stay absent (kept by TSK-0025). |
| L133 | CR-11.01 | MET | TSK-0025 (dead check-supply-chain prefix removed); check-script-manifest.py | - |
| L134 | CR-10.05 | MET | .pre-commit-config.yaml (commit-stage hooks incl. ruff, markdownlint, yamllint, commitizen) | - |
| L135 | CR-10.05 | MET | .github/workflows/ci-quality.yml candidate-quality; quality-standards.md:217 (pr-merge lint/format) | PR covered; no deployment workflow exists (matrix marks it future). |
| L136 | CR-12.01 | NOT_RUN | TSK-0018 cross-repo handoff (read-only) | Other repository; owner holds four-repository adoption. |
| L137 | CR-12.01 | NOT_RUN | TSK-0018 cross-repo handoff (read-only) | Other repository; owner holds adoption. |
| L138 | CR-12.01 | MET | gh repo view: PUBLIC; all .github/workflows runs-on ubuntu-latest; TSK-0017 remote protection read-back | No self-hosted runner; required candidate-quality context on main. |
| L139 | CR-12.01 | NOT_RUN | TSK-0018 cross-repo handoff (read-only) | Other repository; owner holds adoption. |
| L140 | CR-11.02 | MET | git ls-files tests scripts (no task-named files); quality-standards.md:96-101; TSK-0016/0017 | Task-10 proof logic in archive.py retained as preserved-bytes proof reader per policy. |
| L141 | CR-11.04 | PARTIAL | docs/90.references/research/0084-github-actions-platform; SPEC-0211 TSK-0001 | Applied in part; SPEC-0211 acceptance pending; no measured before/after set. |
| L142 | CR-15.01 | PARTIAL | .agents/governance/; TSK-0017 governance file versions per repo | This repo done; cross-repo comparison read-only, adoption NOT_RUN. |
| L144 | CR-15.01 | MET | .agents/governance/*.md; grep docs/0[123] in .agents | Remaining hits are path conventions and dated provenance (ADR refs, repository-map:100), not delegated policy. |
| L145 | CR-15.01 | MET | .codex/provider.md; no docs/0[123] reference in .codex | - |
| L146 | CR-15.01 | MET | .claude/provider.md; no docs/0[123] reference in .claude | - |
| L147 | CR-15.01 | PARTIAL | .agents canonical source; .agents/prompts/handoff.md; environment-constraints.md §5 shared memory | Shared store and handoff prompt exist; Codex loader not observed (owner holds it). Lead review downgraded from MET. |
| L148 | CR-15.01 | MET | bootstrap.md; .claude/provider.md; .codex/provider.md; providers/registry.yaml; git-workflow.md:73-76 | Native Codex acceptance NOT_RUN. |
| L149 | CR-17.02 | MET | .agents/governance/environment-constraints.md:124-170; scripts/operations/agent_memory.py; SPEC-0236 | - |
| L150 | CR-17.01 | MET | scripts/operations/agent_memory.py:31 TIERS; environment-constraints.md:126-130 | One store shared across worktrees. |
| L151 | CR-15.13 | PARTIAL | .agents/governance/agentic.md; workflows.md; scripts/hooks/agent-event-hook.sh | Policy and dispatcher exist; no per-entrypoint end-to-end trace; Codex loader NOT_RUN. |
| L152 | CR-18.02 | PARTIAL | .agents/governance/agentic.md:65-77; workflows.md:82-90 | Retry bound and stop on failure/budget exist; no explicit no-progress or cancel exit. |
| L153 | CR-18.03 | MET | .agents/governance/standards.md:22-26; bootstrap.md load order | - |
| L154 | CR-19.04 | MET | .agents/governance/git-workflow.md:73-76; .gitignore .worktrees/; TSK-0019, TSK-0021 | - |
| L155 | CR-19.01 | PARTIAL | _workspace/ (7 tracked READMEs); .agents/governance/environment-constraints.md:26-31 | environment-constraints.md:27-29 still says only 2 READMEs are tracked and artifacts only under repo-support; contradicts the 7-README ladder. |
| L156 | CR-04.01 | PARTIAL | TSK-0013, TSK-0024 | Reviews recorded, but stale _workspace statement in environment-constraints.md remains. |
| L157 | CR-04.01 | MET | TSK-0024; .agents/governance/environment-constraints.md:26-31 | environment-constraints.md now names the seven tracked _workspace READMEs and both runtime trees (fixed in TSK-0029). |
| L158 | CR-04.01 | PARTIAL | TSK-0013, TSK-0024; environment-constraints.md:26-31 vs .gitignore/_workspace | Same _workspace conflict remains. |
| L159 | CR-15.01 | PARTIAL | .agents/governance/providers/registry.yaml:145-159; provider-capability-matrix.md; output-style.md:14 | Prose is neutral; registry/capability matrix keep provider model and hook facts inside .agents by bootstrap design, which conflicts with the literal prohibition. |
| L160 | CR-15.01 | MET | .agents/governance/*.md; .agents/README.md | - |
| L161 | CR-15.01 | MET | .agents/governance; AGENTS.md; CLAUDE.md | - |
| L162 | CR-15.05 | PARTIAL | .agents/governance/hooks/; providers/registry.yaml; .claude/settings.json + .claude/hooks/; .codex/hooks.json | Claude loader observed (TSK-0017); Codex hook loading NOT_RUN (owner choice). |
| L163 | CR-15.02 | MET | .claude/provider.md; .codex/provider.md | - |
| L164 | CR-15.01 | MET | .codex/provider.md; .codex/config.toml | - |
| L165 | CR-15.01 | MET | .claude/provider.md; .claude/settings.json | - |
| L166 | CR-04.02 | PARTIAL | TSK-0022 (skills), TSK-0024 (paths), TSK-0013 | No recorded disposition for knowledge, prompts, output-styles, commands. |
| L167 | CR-16.03 | MET | TSK-0022 skill bundle audit; TSK-0021 link check | Recorded: 6 bundled, 18 route to canonical owners, none needs a bundle now. |
| L168 | CR-15.03 | MET | .agents/governance/providers/registry.yaml:140-160; .agents/skills/provider-model-evaluation | Entitlement unverified. |
| L169 | CR-21.04 | MET | .agents/governance/approval-boundaries.md; SPEC-0207 (common authorization) | - |
| L170 | CR-15.03 | MET | providers/registry.yaml (single model table); TSK-0021 (no dated model id elsewhere) | - |
| L171 | CR-18.02 | PARTIAL | .agents/governance/agentic.md:65-77; workflows.md:82-90 | Success, failure, budget covered; no-progress and cancel not stated. |
| L172 | CR-18.03 | MET | standards.md:22-26; .agents/prompts/handoff.md; hookify.require-logical-commits-before-stop.md:41-43; scripts/hooks/agent-event-hook.sh:348; output-style.md | stop_hook_active guard prevents re-block loop. |
| L173 | CR-15.04 | MET | AGENTS.md; CLAUDE.md; .agents/governance/standards.md; output-style.md | Codex loader runtime NOT_RUN. |
| L174 | CR-13.03 | MET | .pre-commit-config.yaml; .cz.toml; .agents/prompts/commit-message.md; hookify.warn-pre-commit-manual.md | - |
| L175 | CR-15.07 | NOT_MET | docs/90.references/research/README.md:138,152 | Research marks it unimplemented; no governance decision, adoption or recorded non-adoption reason. |
| L176 | CR-18.04 | PARTIAL | agentic.md:65-77; docs/90.references/research/README.md:139 | Context loading configured; no cost/rate-limit/retry policy, cost not measured. |
| L177 | CR-15.08 | PARTIAL | docs/90.references/research/README.md:140 | Research says partial; no recorded review of auto PR reviewer/test generation under CR-21 non-API rule. |
| L178 | CR-20.01 | MET | TSK-0020; TSK-0007:405-406; docs/01.requirements/0003-security.md:94,120; spec.md:401-402 | Applicability and paid-text limit recorded. |
| L179 | CR-20.03 | PARTIAL | TSK-0020 inputs (only REQ-0003 applied) | Only the requirement template and REQ-0003 carry ISO quality measures. Lead review downgraded from MET. |
| L180 | CR-20.03 | PARTIAL | requirement-package.template.md NFR line (TSK-0020) | Only the requirement template carries characteristic+measure; quality-standards.md has no quality-characteristic/measure rule. |
| L181 | CR-20.02 | PARTIAL | docs/01.requirements/0003-security.md | Other repos NOT_RUN; no Docker-service quality metric selection recorded here. |
| L182 | CR-20.03 | MET | TSK-0020; spec.md:401-402 | - |
| L186 | CR-03.05 | PARTIAL | TSK-0011..0028 (this repo) | This repo improved; other three repos NOT_RUN (owner holds adoption). |
| L187 | CR-03.01 | NOT_RUN | TSK-0017, TSK-0018 (no shared edition) | Needs the other three repositories; no common edition exists. |
| L188 | CR-03.03 | PARTIAL | .claude/provider.md, .codex/provider.md, repo-specific policies | This repo only; other repos NOT_RUN. |
| L189 | CR-02.07 | PARTIAL | docs/90.references/research/README.md:118-142 (Diataxis, C4, arc42 partial; ADR implemented; agency-agents partial) | Rewritten line, raw original unavailable. Internally consistent with L191-L197; no prohibition visible nearby to drop, but list marker and per-workspace scope may have been lost. Per-source adoption-to-test chain not re… |
| L201 | CR-04.05 | MET | .agents/governance/quality-standards.md (Gate and Fixture Ownership, s5 matrix); spec 0212 TSK-0012, TSK-0014 | Single gate owner per invariant and archive removal of finished-work payloads are in place |
| L202 | CR-02.07 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0027-archive-policy-read.md, tsk-0028-sdlc-and-ci-policy-read.md | Rewritten line. Neighbors (L208, L225) add "confirmed fact vs candidate" and "current valid edition first"; normalized text may have dropped an ordering or source-class condition. Per-topic linkage not shown for every t… |
| L203 | CR-18.01 | MET | .agents/governance/documentation-protocol.md (postmortem: no imposed completion deadline); TSK-0013 Timeboxes row | Only remaining time bounds are command timeouts and a 30-day npm risk-acceptance expiry (security, not a work timebox) |
| L204 | CR-18.01 | MET | docs/99.templates/templates/operations/postmortem.template.md; TSK-0013 | Postmortem due date removed; workflow timeout-minutes are execution timeouts allowed by CR-18.01 |
| L205 | CR-04.02 | PARTIAL | spec 0212 criterion 10 (inventory); 15 in-progress and 21 draft Spec/Task files remain | Inventory exists; rewrite against the new baseline not done (work still ongoing) |
| L206 | CR-03.03 | NOT_RUN | TSK-0026 row: Four-repository adoption NOT_RUN | Needs blog-data, Project-Template, hy-home.k8s; owner holds adoption |
| L207 | CR-03.01 | MET | docs/03.specs/0212-request-baseline-and-reconciliation/plan.md (P00-P09 scopes) | Plan partitions work by scope lanes |
| L208 | CR-02.02 | MET | tsk-0006-current-coordination-audit.md, tsk-0008-infra-audit-execution.md | Tasks record source IDs and CONFIRMED_GAP vs candidate classification (spec.md L196) |
| L209 | CR-03.02 | PARTIAL | TSK-0017/TSK-0018 (no shared revision) | Local owners and paths exist; no approved shared revision across repositories (NOT_RUN, owner-held) |
| L210 | CR-03.06 | PARTIAL | .github/workflows (no checkout of other repositories); .agents/governance/git-workflow.md s3 | Prohibition met locally (no cross-repo QA runs); scoped cross-repo conformance check does not exist yet (NOT_RUN) |
| L211 | CR-01.07 | PARTIAL | TSK-0026 (this repo re-run), TSK-0024, TSK-0025 | Rewritten line. Consistent with L289; may have dropped which differences count as required or an exception for workspace-specific items (L206). Other three repos NOT_RUN |
| L212 | CR-04.02 | MET | spec 0212 plan.md; TSK-0026 re-run | Re-run against full request recorded with KEEP/CHANGE decisions |
| L213 | CR-08.04 | MET | docs/98.archive/README.md (git-history-only recovery); TSK-0012 | Recovery path updated to Git history for removed archive payloads |
| L214 | CR-13.01 | MET | .agents/governance/git-workflow.md s5 Agent Completion Commit Discipline | - |
| L215 | CR-07.04 | MET | TSK-0024 stale agent paths, TSK-0025 dead CI route; check-document-links.py | - |
| L216 | CR-08.03 | MET | docs/98.archive/retention-catalog.md; TSK-0011, TSK-0012 | Units with live consumers retained with recorded reason |
| L217 | CR-04.01 | MET | TSK-0027, TSK-0028, TSK-0021 | - |
| L218 | CR-15.01 | MET | .agents/governance/bootstrap.md; .claude/provider.md; .codex/provider.md | - |
| L219 | CR-04.02 | MET | docs/03.specs/0221-request-precedence-and-enforcers/spec.md; bootstrap.md Authority and Precedence | - |
| L220 | CR-11.04 | MET | .agents/governance/quality-standards.md Gate and Fixture Ownership; TSK-0014 | - |
| L221 | CR-11.03 | PARTIAL | .agents/governance/quality-standards.md Gate and Fixture Ownership | Rule exists; no per-fixture size/consumer inventory (CR-11.03) found |
| L222 | CR-04.02 | PARTIAL | spec 0212 criterion 10 inventory | 15 in-progress and 21 draft Spec/Task files not yet reconciled |
| L223 | CR-13.01 | PARTIAL | .agents/governance/git-workflow.md s2, s5 | Commit units and .worktrees location stated; no rule that a new branch/worktree starts from the committed state; templates silent |
| L224 | CR-13.01 | PARTIAL | .agents/governance/workflows.md (stop on HEAD mismatch) | HEAD/handoff reconciliation exists; no explicit start-from-current-work rule in governance or templates |
| L225 | CR-02.02 | PARTIAL | TSK-0027, TSK-0028, docs/03.specs/0236-shared-agent-memory/tasks/tsk-0001-shared-agent-memory.md (read dates) | Rewritten line. "First" ordering kept; CR-01.02 forbids retroactive satisfaction, which the line does not repeat. Per-obligation edition records not complete |
| L226 | CR-21.03 | MET | .agents/governance/bootstrap.md Authority and Precedence (user first) | - |
| L227 | CR-21.03 | MET | .agents/governance/approval-boundaries.md; TSK-0013 governance edits | - |
| L228 | CR-21.03 | MET | .claude/settings.json, .agents/governance/environment-constraints.md (edited in TSK-0013) | - |
| L229 | CR-10.05 | PARTIAL | tsk-0007-r10-reconciliation.md; TSK-0014; TSK-0025; TSK-0028 | Restructuring done in parts; remote protection and four-repo parts NOT_RUN |
| L230 | CR-17.01 | MET | .agents/governance/environment-constraints.md s5; scripts/operations/agent_memory.py | SPEC-0236 criteria still pending owner acceptance |
| L231 | CR-17.01 | MET | .agents/governance/environment-constraints.md s5 (one store .workspace-memory/memory.sqlite3) | - |
| L232 | CR-07.03 | MET | .agents/governance/documentation-protocol.md Entry point for documents outside docs; leaf.docs-traceability entrypoint mode | - |
| L233 | CR-07.01 | MET | .agents/governance/documentation-protocol.md README navigation; registry common/readme, repository-readme, package-readme, documentation-readme | - |
| L234 | CR-05.01 | PARTIAL | docs/99.templates/registry.json | Single registry here; cross-workspace unification NOT_RUN. Typo 98 vs 99 handled by CR-07.06 |
| L235 | CR-02.07 | PARTIAL | TSK-0027, TSK-0028, TSK-0013 | Rewritten line. Consistent with L236/L264; may have dropped "every" scope. Not shown for every obligation |
| L236 | CR-10.05 | MET | .agents/governance/quality-standards.md s5 matrix; git-workflow.md s3 (remote PR owns aggregate QA); tsk-0007 | External research basis recorded in tsk-0007 |
| L237 | CR-04.01 | MET | TSK-0027, TSK-0028 | - |
| L238 | CR-04.01 | MET | TSK-0021, TSK-0027 | - |
| L239 | CR-05.13 | PARTIAL | docs/99.templates/registry.json lifecycles/transitions | Unified here; cross-workspace NOT_RUN |
| L240 | CR-01.05 | PARTIAL | docs/03.specs/0212-request-baseline-and-reconciliation/plan.md | Rewritten line. L300/L301 set archive first then SDLC docs; normalized line does not carry that order. Other repos NOT_RUN |
| L241 | CR-05.13 | MET | docs/99.templates/registry.json; .agents/governance/sdlc.md | - |
| L242 | CR-17.02 | PARTIAL | scripts/operations/agent_memory.py (TIERS, reuse_state); environment-constraints.md s5 | Rewritten line. Implemented; L252/L261 add "no time-based deletion" which this line omits. SRC-MEM research not found in SPEC-0236 |
| L243 | CR-17.02 | PARTIAL | environment-constraints.md s5; agent_memory.py TIER_BODY_BYTES | Retention (no deletion) and limits stated; tiers defined only in code and SPEC-0236, not in governance; no template |
| L244 | CR-03.05 | NOT_RUN | TSK-0017, TSK-0018 | Needs shared revision across four repositories; owner-held |
| L245 | CR-17.03 | MET | environment-constraints.md s5; agent_memory.py has no expiry | No deletion guidance found in .agents or provider adapters |
| L246 | CR-07.02 | MET | documentation-protocol.md Document language; check-document-links.py language mode | - |
| L247 | CR-06.02 | MET | docs/99.templates/templates/specs/task.template.md; registry sdlc/task | - |
| L248 | CR-17.08 | PARTIAL | environment-constraints.md s5; SPEC-0236 TSK-0001 W8 | Rewritten line. Store, single canonical and isolation verified; Codex native [memories] loader NOT_RUN (owner-held). Original may have included per-installation identification (CR-17.08) |
| L249 | CR-07.02 | MET | .agents/governance/documentation-protocol.md Document language | - |
| L250 | CR-21.03 | PARTIAL | .claude/settings.json autoMode.allow $defaults | Claude autoMode set; Codex has no approval setting; no governance statement of the rule |
| L251 | CR-17.01 | MET | scripts/operations/agent_memory.py; .codex/config.toml comment; SPEC-0236 W8 | - |
| L252 | CR-17.03 | MET | environment-constraints.md s5; agent_memory.py | - |
| L253 | CR-17.04 | MET | environment-constraints.md s5 (current vs historical); scripts/lib/ops/memory_sources.py reuse_state | - |
| L254 | CR-06.02 | MET | docs/99.templates/templates/specs/task.template.md (Execution Items, Criterion Acceptance prompts) | - |
| L255 | CR-04.03 | MET | bootstrap.md Authority; provider_surface_renderer.py generated adapters | - |
| L256 | CR-17.05 | PARTIAL | agent_memory.py (one SQLite file, one backup) | Met here; other workspaces NOT_RUN |
| L257 | CR-07.01 | MET | documentation-protocol.md README navigation; registry readme template roles | - |
| L258 | CR-17.08 | PARTIAL | .claude/settings.json autoMemoryEnabled false; .codex/config.toml memories false; no memory: in .claude/agents | Settings set; Codex [memories] effect not observed (NOT_RUN, owner-held) |
| L259 | CR-17.06 | MET | environment-constraints.md s5 (git-common-dir); agent_memory.py | - |
| L260 | CR-17.04 | MET | memory_sources.py reuse_state; environment-constraints.md s5 | - |
| L261 | CR-17.04 | MET | environment-constraints.md s5; agent_memory.py | - |
| L262 | CR-17.02 | MET | environment-constraints.md s5 (context only) | - |
| L263 | CR-17.02 | MET | agent_memory.py (single schema, one CLI) | - |
| L264 | CR-17.09 | PARTIAL | SPEC-0236 TSK-0001 W1 (provider docs, SQLite) | Provider and SQLite docs read; SRC-MEM reference implementation research not found |
| L265 | CR-06.02 | PARTIAL | environment-constraints.md s5; task.template.md | Memory is context only, but records have no field for reason, failure, fix, or reuse condition. Lead review downgraded from MET. |
| L266 | CR-17.05 | MET | scripts/operations/agent_memory.py MAX_* and TIER_BODY_BYTES | - |
| L267 | CR-07.03 | MET | documentation-protocol.md Entry point for documents outside docs | - |
| L268 | CR-04.03 | MET | scripts/operations/provider_surface_renderer.py; .claude/skills thin adapters | - |
| L269 | CR-07.01 | MET | registry roles common/repository-readme, package-readme, documentation-readme, reference/category-readme; _workspace READMEs | - |
| L270 | CR-07.02 | MET | documentation-protocol.md Document language | - |
| L271 | CR-10.02 | MET | .agents/governance/quality-standards.md s5 and Gate and Fixture Ownership | - |
| L272 | CR-03.04 | PARTIAL | task.template.md; spec 0212 (future acceptance criteria allowed) | No current rule states the ban on future commit/digest/approval preconditions. Lead review downgraded from MET. |
| L273 | CR-06.04 | PARTIAL | task.template.md Evidence prompts | Evidence contract exists; external research record for it not found |
| L274 | CR-10.05 | MET | TSK-0025, TSK-0028 | - |
| L275 | CR-15.01 | MET | TSK-0013, TSK-0024 | - |
| L276 | CR-05.03 | PARTIAL | docs/99.templates/templates; TSK-0015 | ### added only where a section holds several contents (TSK-0015) |
| L277 | CR-11.01 | PARTIAL | quality-standards.md (Retire one-time QA); TSK-0016, TSK-0017, TSK-0025 | Rewritten line. Text keeps both halves; L201/CR-11.02 condition (move continuing guarantee first) not in line. Absence tests kept, no full sweep proven |
| L278 | CR-13.03 | MET | .pre-commit-config.yaml; scripts/hooks/install-pre-push-guard.sh; tsk-0007-r10-reconciliation.md | Rewritten line. Consistent with L279; may have dropped "global" scope, which L279 restates |
| L279 | CR-13.03 | MET | git config: no global core.hooksPath; .git/hooks pre-commit, pre-push; tsk-0007 | - |
| L280 | CR-10.06 | PARTIAL | TSK-0014; quality-standards.md s5; git-workflow.md s3 | Rewritten line. Consistent with L236/L298. Duplicate removal shown for measured cases only |
| L281 | CR-04.02 | PARTIAL | spec 0212 criterion 10 | Draft/in-progress packages not yet reconciled |
| L282 | CR-04.02 | PARTIAL | TSK-0020 (requirement template) | No full Stage 01/02 conflict sweep recorded |
| L283 | CR-15.01 | PARTIAL | TSK-0013, TSK-0024 | Symlink skill route (L369) and AGENTS.md role (L316) still differ |
| L284 | CR-07.04 | MET | documentation-protocol.md; check-document-links.py | - |
| L285 | CR-07.04 | MET | documentation-protocol.md; check-document-links.py | - |
| L286 | CR-05.03 | MET | docs/99.templates/contracts/document-frontmatter.schema.json; check-document-metadata.py | - |
| L288 | CR-08.07 | PARTIAL | .agents/governance/sdlc.md (ready for archive review); TSK-0027 | Rules exist; external research record not found |
| L289 | CR-02.01 | PARTIAL | TSK-0026 (meaning audit NOT_RUN) | Rewritten line. Consistent with L211/L235; generic wording may hide order (research first, CR-02.01). Line-meaning audit recorded NOT_RUN |
| L290 | CR-10.05 | MET | tsk-0007; quality-standards.md | - |
| L291 | CR-10.05 | MET | TSK-0025, TSK-0028 | - |
| L292 | CR-21.01 | PARTIAL | github-governance.md s2-s3 (PR, required checks, no self-approve); .github/workflows contain no AI API calls | No named solo-review path or stated API prohibition in governance; workflows call no AI API |
| L293 | CR-07.04 | PARTIAL | documentation-protocol.md | Rules exist; external research record not found |
| L294 | CR-07.03 | PARTIAL | documentation-protocol.md Entry point | Outside-docs rule exists; in-docs scope limited to 99/05 not stated |
| L295 | CR-09.02 | PARTIAL | - | No full Stage 02 currency review recorded |
| L296 | CR-19.01 | MET | _workspace/README.md and six child READMEs (tracked) | - |
| L297 | CR-19.02 | PARTIAL | TSK-0016 writer list | Producers still write elsewhere; untracked dated folders sit at _workspace root |
| L298 | CR-11.01 | PARTIAL | tsk-0007, TSK-0014, TSK-0025 | Done in parts |
| L299 | CR-06.05 | MET | TSK-0024, TSK-0027, TSK-0028 | - |
| L300 | CR-08.01 | MET | TSK-0011, TSK-0012, TSK-0027 | - |
| L301 | CR-05.13 | PARTIAL | TSK-0028, TSK-0020 | SDLC/CI read done; ADR, architecture, operation not shown |
| L302 | CR-07.01 | MET | documentation-protocol.md README navigation and Entry point | - |
| L315 | CR-15.01 | MET | AGENTS.md; .agents/governance/bootstrap.md | AGENTS.md is the entry shim; .agents holds the content |
| L316 | CR-15.01 | PARTIAL | AGENTS.md | AGENTS.md holds no rules and names the Codex adapter; rules live in .agents |
| L317 | CR-16.04 | MET | .agents/governance vs .agents/skills | - |
| L318 | CR-15.11 | MET | .gitignore (.claude/settings.local.json, .workspace-memory/) | - |
| L319 | CR-16.04 | MET | TSK-0022 skill audit | - |
| L320 | CR-10.01 | MET | .pre-commit-config.yaml; .claude/settings.json hooks; .github/workflows | - |
| L338 | CR-16.03 | MET | .agents/skills/*/SKILL.md description | - |
| L339 | CR-16.03 | MET | ## Procedure in all 24 | - |
| L340 | CR-16.03 | PARTIAL | .agents/skills/*/SKILL.md | No skill has a Verification section; 10 of 24 state no success condition |
| L341 | CR-16.03 | MET | ## Outputs in all 24 | - |
| L342 | CR-16.03 | MET | infra-validate, style-validation scripts | - |
| L345 | CR-15.02 | MET | .claude/agents (14 md), .codex/agents (14 toml) | - |
| L368 | CR-15.10 | MET | .claude/provider.md; .claude/skills adapters; CLAUDE.md imports | - |
| L369 | CR-15.10 | NOT_MET | .claude/skills (generated files, no symlinks); .codex/provider.md | No symlinks; thin adapters instead; no recorded symlink support decision |
| L371 | CR-15.02 | MET | .claude/output-styles/hy-home.md routes to output-style.md | Example concise.md not used; hy-home.md instead |
| L382 | CR-15.10 | PARTIAL | .codex/provider.md; AGENTS.md | Static route present; Codex native loader check NOT_RUN (owner-held) |
| L383 | CR-15.10 | PARTIAL | .codex/provider.md (reads .agents/skills directly) | Codex reads .agents/skills natively without symlink; Claude uses adapters; no decision record |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Line coverage | 40 | W45 | Merge script: positions L001–L383 each present once, 7 columns, primary CR among the 148 | Three reviewer outputs | PASS | 383 positions, 355 non-blank | required | - |
| Lead spot review | 40 | W45 | Read of weakest `MET` rows against their files | Reviewer outputs | PASS | Four rows downgraded to `PARTIAL` | required | - |
| Metadata contracts | 40 | W45 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Agent governance | 40 | W45 | `check-agent-governance-contract.py` | This branch | PASS | Contract holds after the policy fix | required | - |
| Raw wording preservation | 40 | W45 | Compare raw request with appendix R | - | NOT_RUN | Raw original not available | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 40 | accepted | Line coverage, Lead spot review, Metadata contracts, Agent governance | Every non-blank request line has a recorded meaning judgement against this repository; gaps stay open as listed, and wording preservation stays unverified. | SPEC-0212 TSK-0029 |

## Review and Completion

This Task completes on the evidence above. It closes the audit, not the gaps:
`PARTIAL`, `NOT_MET`, and `NOT_RUN` lines stay open until a later Task the
owner authorizes changes them. Hosted checks and the merge are observed on
the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request re-run baseline](tsk-0026-request-rerun-baseline.md)
- [Requirement pair conflict check](tsk-0030-requirement-pair-conflict-check.md)
