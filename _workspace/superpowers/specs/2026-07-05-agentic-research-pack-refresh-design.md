---
status: active
---

# Agentic Research Pack Refresh Design

## Overview

Refresh the existing `docs/90.references/research/agentic-engineering/`
research pack with current external source evidence and repository-local
analysis. The work uses a refresh-first strategy, then adds targeted new
reference documents only where the existing pack would become too broad.

This design document is a Superpowers workflow gate. It does not replace the
repository's canonical Stage 90 reference documents, active policy, execution
plans, operations runbooks, or runtime truth.

## Goals

- Revalidate and improve the current research pack against official external
  sources and repo-local evidence.
- Cover the requested categories: workspace purpose, roles, CI/CD, QA,
  formatting, linting, syntax error checks, automation, pipeline, workflow,
  overview, operating contracts, templates, scripts, integration guides, SDLC,
  governance, system structure, rules, and security.
- Include harness engineering, loop engineering, provider implementation
  comparison for Claude/Codex/Gemini, common provider-neutral environment
  elements, spec-driven development, Docker Compose, infrastructure, CI/CD, QA,
  formatting, linting, automation, pipeline, workflow, and security.
- Keep Stage 90 research as reference context rather than active policy.
- Record follow-up gaps instead of changing unrelated stages.
- Commit by logical units.

## Non-Goals

- Do not change runtime Docker Compose files, provider configs, secrets,
  GitHub remote settings, branch protections, or CI workflow behavior.
- Do not convert reference findings into active governance, policy, plan,
  runbook, or implementation changes in this pass.
- Do not create duplicate research documents when an existing document can be
  updated cleanly.
- Do not claim provider capability parity unless official current sources
  support it.

## Target Files

Update existing files:

- `docs/90.references/research/agentic-engineering/README.md`
- `docs/90.references/research/agentic-engineering/workspace-baseline.md`
- `docs/90.references/research/agentic-engineering/harness-engineering.md`
- `docs/90.references/research/agentic-engineering/loop-engineering.md`
- `docs/90.references/research/agentic-engineering/spec-driven-sdlc.md`
- `docs/90.references/research/agentic-engineering/quality-ci-formatting.md`
- `docs/90.references/research/agentic-engineering/provider-implementation-comparison.md`
- `docs/90.references/research/README.md`, only if the pack structure changes
- `docs/00.agent-governance/memory/progress.md`

Add targeted files only if needed:

- `docs/90.references/research/agentic-engineering/docker-compose-infrastructure.md`
- `docs/90.references/research/agentic-engineering/security-governance.md`
- `docs/90.references/research/agentic-engineering/automation-pipeline-workflow.md`

## Source Strategy

Use primary or official sources first. Recheck fast-moving provider and product
facts during implementation before writing final text.

- Provider sources: official Claude Code, OpenAI Codex, and Gemini CLI docs or
  official repositories.
- Infrastructure sources: Docker Compose official docs and Docker security
  guidance.
- CI/CD and workflow sources: GitHub Actions official docs and GitHub security
  guidance.
- QA/formatting/linting sources: pre-commit, EditorConfig, Prettier, language
  linting or syntax-check docs where directly relevant.
- Security and SDLC sources: NIST SSDF, OWASP SAMM, SLSA, OpenSSF Scorecard or
  other primary security references where appropriate.
- Harness/loop sources: ISTQB, pytest, eval harness projects, ReAct,
  Reflexion, official eval guidance, and official human-in-the-loop docs.
- Repo-local sources: Stage 00 governance, provider notes, HAFE docs, scripts
  inventory, CI workflow, docs templates, operations policies, `infra/`, and
  top-level shims.

## Architecture

The refreshed pack keeps one research category:

```text
docs/90.references/research/agentic-engineering/
├── README.md
├── workspace-baseline.md
├── harness-engineering.md
├── loop-engineering.md
├── spec-driven-sdlc.md
├── quality-ci-formatting.md
├── provider-implementation-comparison.md
├── docker-compose-infrastructure.md        # add if needed
├── security-governance.md                  # add if needed
└── automation-pipeline-workflow.md         # add if needed
```

Existing documents remain the canonical starting point. New documents are added
only when one of the requested topics would make an existing document unfocused.

## Document Responsibilities

- `workspace-baseline.md`: repo-local purpose, roles, CI/CD, QA, formatting,
  linting, automation, scripts, templates, integration guides, SDLC,
  governance, rules, and security baseline.
- `harness-engineering.md`: harness elements, repo-local harness surfaces,
  agent/runtime/test/eval harness components, and application gaps.
- `loop-engineering.md`: agent, validation, CI, memory, eval, approval, and
  human-in-the-loop feedback loops.
- `spec-driven-sdlc.md`: spec-driven development and stage-gated SDLC mapping.
- `quality-ci-formatting.md`: CI/CD, QA, formatting, linting, syntax checking,
  security gate placement, and evidence boundaries.
- `provider-implementation-comparison.md`: Claude, Codex, Gemini harness and
  loop implementation status, common environment elements, and gaps.
- `docker-compose-infrastructure.md`: Docker Compose, infrastructure topology,
  profiles, validation, networking, secrets, and runtime boundary analysis.
- `security-governance.md`: secure SDLC, secrets, provider approvals, workflow
  security, container security, supply-chain guardrails, and repo-local
  security controls.
- `automation-pipeline-workflow.md`: automation, pipeline, workflow, hook, CI
  job, provider action, and loop orchestration analysis.

## Data Flow

1. Read current repo-local references and target files.
2. Browse official external sources for updated facts and caveats.
3. Compare external patterns with repo-local evidence.
4. Update or create Stage 90 reference documents using the reference template
   contract.
5. Update README indexes only when structure changes.
6. Record gaps as reference follow-up items, not active-stage changes.
7. Update `memory/progress.md` with what changed and verification evidence.
8. Run repository validation gates and commit each logical unit.

## Error Handling

- If an external source is unavailable, use another official source or record
  the source gap explicitly.
- If provider documentation conflicts with repo-local provider notes, describe
  the conflict as a gap and do not change provider policy.
- If a requested item belongs in active policy, plan, operation, or runtime
  configuration, record it as a follow-up gap instead of editing that surface.
- If validation fails because of unrelated existing issues, record the gap and
  keep the research-pack changes scoped.

## Validation Plan

Run at minimum:

- `git diff --check`
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- `bash scripts/operations/sync-provider-surfaces.sh --check`
- `bash scripts/validation/check-doc-traceability.sh`
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

For changed reference files, also run targeted scans for placeholders,
non-English closed-surface drift if applicable, broken target-relative links,
and stale provider capability claims.

## Commit Strategy

- Commit the Superpowers design document first.
- Commit research refreshes by logical unit:
  - workspace/source baseline refresh
  - harness/loop/provider refresh
  - QA/CI/formatting/security refresh
  - Docker Compose/infrastructure or automation additions if created
  - README/progress/index finalization if not included in prior commits

## Acceptance Criteria

- Existing research pack is revalidated against current official sources.
- Requested categories are covered by either existing refreshed docs or targeted
  new docs.
- New or changed reference documents state repository role, scope, source rules,
  sources, maintenance, and related documents.
- No active policy, runtime, secret, provider config, or CI behavior is changed.
- `docs/00.agent-governance/memory/progress.md` records the completed research
  work and validation evidence.
- Repository validation gates pass, or any unrelated failure is explicitly
  recorded as out of scope.

## Open Assumptions

- The approved approach is "refresh existing pack plus targeted additions if
  needed."
- Human-facing README files may remain Korean, while non-README Stage 90
  reference documents remain English under the repository's closed-surface
  language contract.
- External facts about Claude, Codex, Gemini, Docker, GitHub Actions, and
  security frameworks must be rechecked during implementation because these
  sources can change quickly.

## Related Documents

- [Research pack index](../../../docs/90.references/research/agentic-engineering/README.md)
- [Research references](../../../docs/90.references/research/README.md)
- [Stage authoring matrix](../../../docs/00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation scope](../../../docs/00.agent-governance/scopes/docs.md)
