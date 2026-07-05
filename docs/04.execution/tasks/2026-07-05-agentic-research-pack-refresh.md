---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md -->

# Agentic Research Pack Refresh Task

## Overview

This document tracks implementation and verification work for refreshing and
extending the Stage 90 agentic engineering research pack. The work is
documentation-only and keeps Stage 90 research as source-backed reference
context rather than active policy, operations procedure, runtime truth, or CI
configuration.

## Inputs

- **Parent Spec**: [Agentic Research Pack Refresh Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md)
- **Parent Plan**: [Agentic Research Pack Refresh Plan](../plans/2026-07-05-agentic-research-pack-refresh.md)
- **Target Research Pack**: [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)

## Working Rules

- Refresh existing research documents before adding new reference files.
- Use official external sources and repo-local canonical evidence.
- Record active-stage, runtime, CI, provider, or security improvement ideas as
  gaps unless the user expands scope.
- Do not change runtime Compose files, provider configs, scripts, CI workflow
  behavior, secrets, `.env`, branch protection, or remote GitHub state.
- Commit by logical unit.

## Task Scope

- Refresh existing Stage 90 research documents under `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`.
- Add targeted reference documents only when existing documents would become unfocused.
- Update README indexes and progress memory.
- Preserve source rules, maintenance notes, and related document links.

## Approved Surface Evidence

No high-risk approved runtime, policy, CI, secrets, remote GitHub, model policy,
or provider adapter surface is in scope. This task may edit Stage 90 research,
Stage 04 evidence, README indexes, and Stage 00 progress memory only.

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 90 research references | User request on 2026-07-05 | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` | Existing research pack | Refreshed source-backed references | Revert documentation commits | No secret values or raw logs |
| Stage 04 evidence | Stage 03 spec and Stage 04 plan | This task document | No task evidence for this refresh | Execution evidence and validation summary | Revert task documentation commit | No shell history or raw secret logs |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-RSRCH-001 | Create task evidence and plan link closure | doc | `VAL-SPC-006` / Memory and evidence | `PLN-001` | Task document exists and repo links validate | Documentation Specialist | Done |
| T-RSRCH-002 | Revalidate external source set and repo-local evidence | doc | `VAL-SPC-002`, `VAL-SPC-003` | `PLN-002` | Source inventory and revalidation notes | Documentation Specialist | Done |
| T-RSRCH-003 | Refresh existing research pack documents | doc | `VAL-SPC-002`, `VAL-SPC-003`, `VAL-SPC-004` | `PLN-003` | Git diff and source-backed updates | Documentation Specialist | Done |
| T-RSRCH-004 | Add targeted references if required | doc | `VAL-SPC-003`, `VAL-SPC-004` | `PLN-004` | New reference docs or N/A rationale | Documentation Specialist | Done |
| T-RSRCH-005 | Update indexes, progress memory, and validation evidence | doc | `VAL-SPC-006`, `VAL-SPC-007` | `PLN-005` | Final validation summary | Documentation Specialist | Done |

## Phase View

### Phase 1: Planning and Evidence Scaffold

- [x] T-RSRCH-001 Create task evidence and close plan link validation.

### Phase 2: Source Revalidation

- [x] T-RSRCH-002 Revalidate external and repo-local source set.

### Phase 3: Research Refresh

- [x] T-RSRCH-003 Refresh existing research pack documents.
- [x] T-RSRCH-004 Add targeted references or record N/A rationale.

### Phase 4: Final Evidence

- [x] T-RSRCH-005 Update indexes, progress memory, and final validation summary.

## Source Inventory

Revalidated on 2026-07-05 by read-only web/source research and repo-local
evidence discovery. Official vendor, standards, primary-paper, and canonical
project sources are preferred for downstream Stage 90 edits.

| Source Class | URL / Source | What It Supports | Current Caveat / Update Needed |
| --- | --- | --- | --- |
| Stage 03 Spec | [Agentic Research Pack Refresh Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md) | Design contract, source priority, provider parity guardrail, no-runtime-change boundary | Active; downstream research edits must stay advisory and must not claim provider parity without official support. |
| Stage 04 Plan | [Agentic Research Pack Refresh Plan](../plans/2026-07-05-agentic-research-pack-refresh.md) | Execution sequencing for source revalidation, research refresh, targeted additions, and final validation | Completed; this evidence covers source revalidation, existing research refresh, targeted additions, and final validation. |
| Stage 90 Research Pack | [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md) | Target research category and existing document set | Active; refresh existing files before adding Docker/security/automation references. |
| Claude Code Provider Docs | <https://code.claude.com/docs/en/overview>, <https://code.claude.com/docs/en/sub-agents>, <https://code.claude.com/docs/en/hooks> | Claude Code overview, CLAUDE.md/project memory, custom subagents, hooks, tool/permission scoping, parallel work | Update provider comparison to current `code.claude.com` URLs; Claude official docs support first-class subagents and hooks. |
| OpenAI Codex Provider Docs | <https://developers.openai.com/codex/cli>, <https://developers.openai.com/codex/subagents>, <https://developers.openai.com/codex/hooks>, <https://developers.openai.com/codex/guides/agents-md>, <https://developers.openai.com/codex/security> | Codex CLI, custom subagents, hooks, AGENTS.md discovery, sandbox/approval/security model | Update provider comparison to current Codex docs; Codex official docs support first-class subagents and hooks. |
| Gemini CLI Provider Docs | <https://developers.google.com/gemini-code-assist/docs/gemini-cli>, <https://google-gemini.github.io/gemini-cli/docs/>, <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>, <https://google-gemini.github.io/gemini-cli/docs/cli/commands.html>, <https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html> | Gemini CLI overview, ReAct loop, GEMINI.md/context files, settings, MCP servers, commands, tool configuration, trusted/security controls | Official Gemini sources reviewed here do not show first-class subagents comparable to Claude/Codex. Treat Gemini as agentic CLI + ReAct/MCP/context-file support, not subagent parity, unless a later official source proves otherwise. |
| Docker Compose Docs | <https://docs.docker.com/compose/>, <https://docs.docker.com/reference/compose-file/>, <https://docs.docker.com/compose/how-tos/profiles/>, <https://docs.docker.com/compose/how-tos/networking/>, <https://docs.docker.com/compose/how-tos/use-secrets/>, <https://docs.docker.com/compose/how-tos/production/> | Compose concepts, Compose file reference, profiles, networks, secrets, and production guidance | Use for Docker/infrastructure reference facts only; do not imply repo runtime Compose changes in this refresh. |
| GitHub Actions Docs | <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>, <https://docs.github.com/en/actions/reference/security/secure-use>, <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches> | Workflow syntax, jobs, secure use, and protected-branch required checks/status checks | Use for CI/security analysis; do not change workflows or remote branch protection in this task. |
| Quality Tool Docs | <https://pre-commit.com/>, <https://editorconfig.org/>, <https://prettier.io/docs/cli> | pre-commit hook framework, EditorConfig formatting convention, Prettier CLI/check behavior | Supports quality/formatting/linting discussion; downstream docs should cite commands without adopting new tooling behavior. |
| Secure SDLC / Supply Chain Standards | <https://csrc.nist.gov/pubs/sp/800/218/final>, <https://owasp.org/www-project-samm/>, <https://slsa.dev/> | NIST SSDF secure development practices, OWASP SAMM maturity model, SLSA supply-chain integrity framing | Treat as external reference frameworks, not adopted repo policy. NIST SSDF final publication date is February 2022; OWASP SAMM page lists v2.0.3 (2022); SLSA site currently exposes SLSA v1.2. |
| Agent Loop / Evaluation Sources | <https://arxiv.org/abs/2210.03629>, <https://arxiv.org/abs/2303.11366>, <https://developers.openai.com/api/docs/guides/evals> | ReAct reason-act loop, Reflexion verbal feedback/memory loop, OpenAI eval data/criteria/run model | ReAct and Reflexion are research papers, not vendor product docs. Use OpenAI eval docs for eval mechanics; HITL should be framed as ground-truth/human-label and review-loop practice, not a complete governance model. |
| Repo-local Evidence | [Root README](../../../README.md), [Root AGENTS.md](../../../AGENTS.md), [Stage 00 Governance](../../00.agent-governance/README.md), [Scripts README](../../../scripts/README.md), [Infra README](../../../infra/README.md), `.github/workflows/` | Workspace purpose, agent governance, validation scripts, Docker Compose infrastructure, CI workflow surface, provider/runtime boundaries | Read-only evidence discovery found broad matching surfaces. Downstream claims must cite exact local files and avoid raw logs, secrets, or runtime/provider/CI edits. |

### Current Research Pack Inventory

| File | Current Role |
| --- | --- |
| [README.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md) | Pack index, scope, reading order, and maintenance guidance |
| [workspace-baseline.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md) | Repo-local purpose, roles, CI/CD, QA, automation, formatting, templates, scripts, SDLC, governance, and rules baseline |
| [harness-engineering.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md) | Harness components, runtime/test/eval/governance harness mapping, and workspace application gaps |
| [loop-engineering.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md) | Agent, validation, CI, memory, eval, approval, automation, and workflow loop mapping |
| [provider-implementation-comparison.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md) | Claude, Codex, Gemini harness/loop implementation comparison and provider-neutral normalization |
| [quality-ci-formatting.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) | CI/CD, QA, formatting, linting, syntax checks, and security gate analysis |
| [spec-driven-sdlc.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) | Spec-driven development, SDLC, traceability, and secure SDLC reference mapping |
| [docker-compose-infrastructure.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) | Docker Compose, infrastructure harness, profile, network, secret, validation, and hardening analysis |
| [security-governance.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md) | Secure SDLC references, workflow security, secret boundaries, approval evidence, and repo-local security governance analysis |
| [automation-pipeline-workflow.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md) | Automation, pipeline, workflow loops, provider hooks, local/remote action boundaries, and task evidence analysis |

### Revalidation Notes

- Gemini official sources reviewed for this slice show an agentic CLI using a
  ReAct loop, built-in tools, local/remote MCP servers, hierarchical
  `GEMINI.md` context files, settings, commands, and trusted/security controls.
  They do not show first-class subagents comparable to Claude Code subagents or
  Codex subagents.
- Claude and Codex official sources both currently document first-class
  subagent workflows and hooks. Provider comparison updates should therefore
  distinguish "first-class subagents" from Gemini's ReAct/MCP/context-file
  capabilities.
- Docker, GitHub Actions, quality-tool, SSDF/SAMM/SLSA, ReAct, Reflexion, and
  OpenAI eval sources remain suitable as external references for Stage 90
  research. They should not be written as adopted workspace policy without a
  separate active-stage change.

### Repo-local Evidence Notes

- Stage 00 remains the policy SSoT for governance, subagent protocol,
  provider-neutral workflows, QA/CI/CD scope, template contract, protected
  surfaces, and approval boundaries.
- `.github/workflows/ci-quality.yml` currently separates documentation
  traceability, implementation alignment, repo contracts, Git flow, Compose
  validation, all-profile Compose validation, hardening, template/security
  baseline, QuickWin baseline, pre-commit, frontend lint/type/build/coverage,
  and GitHub Actions security analysis.
- `scripts/README.md` groups the local automation surface into validation,
  hardening, hooks, knowledge, operations, and shared library paths. It also
  names `run-local-qa-gates.sh`, provider-surface sync, tech-stack version
  sync, Compose validation, and hook-mediated post-tool validation as canonical
  automation entrypoints.
- `infra/README.md` describes the Compose infrastructure as tiered service
  definitions aggregated through the root Compose file, with profiles,
  root-active versus optional/standalone inventory rules, non-secret config
  evidence, secret-reference-only documentation, healthcheck expectations, and
  validation links.
- `.github/SECURITY.md`, the Stage 00 security scope, and GitHub governance
  define security-reporting, secret redaction, container hardening, workflow
  security, and protected-branch behavior as active governance surfaces.
- This pass did not change runtime Compose files, infrastructure definitions,
  scripts, workflow behavior, provider runtime configuration, secret material,
  `.env` files, remote GitHub state, or branch protection.

## Existing Research Refresh Notes

Task 3 refreshed the existing Stage 90 research documents in place. Task 4 then
added targeted reference documents for the topics that were too broad to keep
only inside the existing baseline, quality, and loop documents.

Changed research documents:

- [workspace-baseline.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md) - added explicit Security, Linting / Syntax, and Docker Compose / Infrastructure category rows with repo-local evidence and reference boundaries.
- [harness-engineering.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md) - added infrastructure and security harness rows, source-freshness caveat, and distinction from test/eval harnesses.
- [loop-engineering.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md) - added automation pipeline and security review loops and clarified approval requirements for external actions.
- [provider-implementation-comparison.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md) - updated Claude Code URLs, refreshed Gemini subagent-gap date to 2026-07-05, and added Docker/infra, security/approval, and common-rule-substrate rows.
- [spec-driven-sdlc.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) - clarified Compose infrastructure lifecycle, QA evidence classes, and secure SDLC reference-only status.
- [quality-ci-formatting.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) - clarified QA evidence classes, Compose infrastructure lifecycle, and secure SDLC reference-only status.

## Targeted Reference Addition Notes

Task 4 created all three targeted reference documents because Docker
Compose/infrastructure, security governance, and automation/pipeline/workflow
coverage would make the existing baseline, quality, and loop documents too
broad if expanded further.

Created targeted references:

- [docker-compose-infrastructure.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) - analyzes Docker Compose and infrastructure harness evidence against official Docker guidance and repo-local Compose, infra, validation, hardening, profile, network, secret, and healthcheck surfaces.
- [security-governance.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - analyzes secure SDLC and supply-chain references against repo-local reporting, approval, redaction, workflow security, hardening, and template/security baseline evidence.
- [automation-pipeline-workflow.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md) - analyzes GitHub Actions, provider hooks, scripts, CI, task evidence, and local/remote automation authority boundaries.

README index updates:

- [Agentic Engineering Research Pack README](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md) now lists the three targeted references in the structure, current references, and reading order.
- [Research References README](../../90.references/research/README.md) now names the expanded targeted-reference scope in the agentic engineering pack summary.

## Deviation Log

| Deviation | Reason | Resolution |
| --- | --- | --- |
| Task 4 implementation ran locally after a subagent dispatch attempt hit the current agent thread limit. | The multi-agent tool reported `agent thread limit reached` after Task 3 reviews completed. | Completed Task 4 in the controller session with the same write-scope boundary, validation gates, and logical commit discipline. No document scope, runtime, provider, CI, secret, or remote boundary changed. |

## Verification Summary

Task validation and final validation were run after the existing research
documents, targeted references, README indexes, LLM Wiki index, and progress
memory were updated.

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | PASS | No whitespace or conflict-marker issues. |
| `rg -n "TBD\|TODO\|FIXME\|\\[.*\\]\|\\{.*\\}\|first-class subagent parity" docs/90.references/research/2026-07-05-agentic-research-pack-refresh -g '*.md'` | PASS with expected matches | Output is valid Markdown links plus caveat/gap uses of `first-class subagent parity`; no unresolved template placeholders found. |
| `rg -n "docs\\.anthropic\|2026-07-02" docs/90.references/research/2026-07-05-agentic-research-pack-refresh -g '*.md'` | PASS | No stale Anthropic URL or old provider revalidation-date claims remain in the research pack. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS | `failures=0`; LLM Wiki contract passed, so no `llm-wiki-index.md` regeneration was required. |
| `git diff --check` after targeted additions | PASS | No whitespace or conflict-marker issues. |
| `bash scripts/validation/check-repo-contracts.sh` after targeted additions | PASS | `failures=0`; LLM Wiki contract passed after regeneration. |
| `git diff --check` final | PASS | No output. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` final | PASS | Generated LLM Wiki index is fresh. |
| `bash scripts/operations/sync-provider-surfaces.sh --check` final | PASS | `sync-provider-surfaces: no drift`. |
| `bash scripts/validation/check-doc-traceability.sh` final | PASS | `failures=0`. |
| `bash scripts/validation/check-doc-implementation-alignment.sh` final | PASS | `failures=0`. |
| `bash scripts/validation/check-repo-contracts.sh` final | PASS | `failures=0`. |

## Related Documents

- [Plan](../plans/2026-07-05-agentic-research-pack-refresh.md)
- [Spec](../../03.specs/104-agentic-research-pack-refresh/spec.md)
- [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Research references](../../90.references/research/README.md)
