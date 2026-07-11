---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md -->

# Reference: Agent Instructions and Safe Vibe-Coding Criteria

## Overview

This reference defines source-backed criteria for repository agent
instructions and for bounded, reviewable vibe coding. It treats AI-generated
code as ordinary owned code with additional context, provenance, dependency,
and verification risks.

## Purpose

Give Tasks 5, 7, 8, 9, and 10 one canonical criterion set for instruction
authority, context, tools, permissions, verification, generated-code ownership,
review thresholds, debt, escalation, and safe iteration.

## Repository Role

Stage 00 remains the instruction authority; provider files are projections.
[AI agent catalogs](./ai-agent-catalogs.md) owns third-party role intake, and
[quality/CI](./quality-ci-formatting.md) owns the tracked evidence-surface
inventory. This document owns instruction and vibe-coding comparison criteria,
not runtime or provider policy.

## Scope

### In Scope

- Instruction authority, scope/context, tools, permissions, and verification
- Ownership and review of AI-generated code
- Debt tracking, escalation thresholds, and bounded vibe-coding loops

### Out of Scope

- Adding a GitHub-native instruction hierarchy or changing provider adapters
- Granting tools, credentials, network access, remote actions, or runtime mutation
- Endorsing unreviewed generated output as production-ready

## Definitions / Facts

- **Instruction authority** is the tracked layer allowed to set repository behavior.
- **Vibe coding** here means conversational, iterative AI-assisted implementation;
  it is a workflow style, not an exemption from SDLC, ownership, or verification.
- **Generated-code owner** is the human/team and canonical artifact owner that
  accepts the change; the model is not an accountable owner.
- **Escalation threshold** is a predeclared retry, uncertainty, permission, or
  impact boundary at which the agent stops and returns control.

## Criteria

| Criterion ID | Practice | Primary source | Workspace applicability | Required evidence | Potential owner |
| --- | --- | --- | --- | --- | --- |
| AIV-01 | Define one canonical instruction authority and explicit projection/precedence rules. | OpenAI Codex `AGENTS.md`; GitHub repository instructions; Stage 00 governance | Stage 00 is canonical; root/provider files remain thin projections and GitHub-native instructions are not adopted policy. | Authority map; precedence test; provider no-drift check | Stage 00 agent governance |
| AIV-02 | Scope instructions to repository, directory, file pattern, and task context. | OpenAI Codex `AGENTS.md`; Claude Code memory/rules | Prefer nearest applicable tracked guidance and load only context relevant to the changed surface. | Scope/path examples; conflict resolution; context-size/fallback behavior | Provider-neutral instruction owner |
| AIV-03 | Keep instructions short, direct, specific, and verifiable. | GitHub custom-instruction guidance | Replace vague quality demands with named paths, commands, expected results, and exclusions. | Instruction review checklist; executable examples; stale-reference scan | Stage 00 documentation owner |
| AIV-04 | Declare available tools and their intended purpose; do not infer authority from tool presence. | OpenAI practical guide to building agents | Tool access remains subordinate to task scope, sandbox, approval, and external-action boundaries. | Tool list; allowed action class; failure behavior; audit evidence | Agent/runtime contract owner |
| AIV-05 | Default to least privilege and request approval for state-changing, sensitive, or out-of-scope actions. | Claude Code security; OpenAI agent guardrails | Matches repository sandbox and approval-boundary rules; permission metadata alone is not proof of enforcement. | Sandbox/permission evidence; approval source; denied-action test | Security and approval-boundary owner |
| AIV-06 | Require tests, static analysis, and relevant security/contract checks before accepting generated code. | GitHub Review AI-generated code; NIST SSDF v1.1 | Use the exact QA evidence classes applicable to the changed surface. | Named commands/jobs, results, skipped-check rationale, regression evidence | QA scope and task owner |
| AIV-07 | Assign AI-generated code to the same accountable human/team and canonical artifact owner as human-written code. | GitHub Review AI-generated code; NIST SSDF v1.1 | “AI generated” may describe provenance but never transfers responsibility. | Reviewer, accepted diff, traceable task/spec, license/provenance review where relevant | Change owner and reviewer |
| AIV-08 | Increase independent review with complexity, sensitivity, irreversibility, novelty, and blast radius. | GitHub collaborative-review guidance; OpenAI human-intervention guidance | Protected governance, security, runtime, secrets, CI, provider, and remote surfaces require explicit thresholds/approval. | Risk classification; reviewer independence; approval and rollback evidence | Task owner plus specialist reviewer |
| AIV-09 | Verify suggested dependencies, APIs, licenses, and maintenance rather than trusting plausible output. | GitHub Review AI-generated code | Applies to every new package, action, image, API, or copied pattern. | Authoritative lookup; lock/registry evidence; license and security check | Dependency/security owner |
| AIV-10 | Track shortcuts and unresolved generated-code defects as owned debt; never delete/skip tests merely to make the loop green. | GitHub Review AI-generated code; Google SRE postmortem action ownership | Debt belongs in canonical Spec/Plan/Task or issue surface, with priority and verification, not chat history. | Debt item, owner, rationale, due/review trigger, linked failing evidence | Earliest canonical lifecycle owner |
| AIV-11 | Escalate after declared retry/action thresholds or whenever a high-risk action is required. | OpenAI practical guide to building agents | Stop on repeated failure, missing authority, contradictory instructions, uncertain high-impact state, or irreversible action. | Threshold in task/agent contract; concise attempts; blocking question or handoff | Workflow/task owner |
| AIV-12 | Treat repository content, web pages, tool output, and third-party agent packs as potentially untrusted instructions. | Claude Code prompt-injection guidance; OpenAI guardrails | Data does not override Stage 00 or direct task authority; external catalogs remain offline/pinned references by default. | Source classification; injection review; tool/permission boundary | Security owner |
| AIV-13 | Bound vibe coding to a branch/worktree, explicit objective, small increments, and reversible commits. | GitHub vibe-coding tutorial | Suitable for prototypes and approved implementation when the same plan, review, and evidence gates apply. | Scoped plan/task; isolated workspace; per-iteration diff/test; logical commits | Implementation task owner |
| AIV-14 | Keep vibe coding away from unapproved runtime, production data, secrets, remote mutations, and security-critical decisions. | GitHub vibe-coding permissions/testing; OpenAI/Claude security guidance | Those surfaces need explicit authority, specialist review, rollback/recovery, and validation before action. | Approval record; redaction boundary; rollback; specialist verdict | Security/operations owner |
| AIV-15 | Use a closed loop: plan, act, observe tool results, verify, review, and either correct or stop. | OpenAI agent guide; Anthropic effective-agent/eval guidance | Agent completion text is not evidence; tracked outputs and checks determine completion. | Plan/task state, tool results, verification, review verdict, residual concerns | Workflow supervisor / QA |
| AIV-16 | Import external agent knowledge only through the canonical catalog intake boundary. | Official provider instruction docs; pinned upstream catalog evidence | Catalog breadth or publisher maturity claims never authorize installation or execution. | Pin/license/source review; rewritten scope; security and eval evidence | Stage 00 agent catalog owner |

## Safe Boundary

| Safe for conversational iteration | Requires stop, explicit authority, or specialist review |
| --- | --- |
| Read-only discovery, local prototypes, bounded code/docs edits, test generation, refactoring with preserved behavior | Secrets, credentials, production/live data, paid or remote actions, deployment/runtime mutation, security controls, model policy, provider adapters, CI protection |
| Small reversible diffs in an isolated branch/worktree with named checks | Unclear scope, conflicting instructions, broad dependency changes, missing rollback, repeated failed verification |
| Human-reviewed output with task evidence and debt recorded canonically | “Looks right” output, deleted/skipped tests, invented packages/APIs, unreviewed bulk generation |

## Source Rules

- External sources were revalidated on **2026-07-11**. OpenAI, Anthropic, and
  GitHub product guidance is mutable and proves retrieval-time behavior only.
- NIST SSDF v1.1 is a February 2022 high-level secure-development framework;
  this reference does not claim formal conformance.
- GitHub's vibe-coding tutorial is official workflow guidance, not evidence that
  conversational iteration is safe for every repository surface.
- Repo-local applicability is based on tracked files at baseline
  `84d88ee48085304ad5aa3adce0a9e74b574758b0`; Graphify is older and advisory.

## Sources

- [OpenAI Codex custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) - discovery, layering, and nearest-scope precedence
- [OpenAI practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) - tools, guardrails, retry/high-risk escalation, and human intervention
- [Claude Code memory and rules](https://code.claude.com/docs/en/memory) - modular and path-scoped project instructions
- [Claude Code security](https://code.claude.com/docs/en/security) - least privilege, sandboxing, approval, prompt injection, and user review responsibility
- [GitHub repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) - repository/path/agent instruction scopes and precedence caveats
- [GitHub Review AI-generated code](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code) - tests, context, quality, dependencies, AI-specific failure modes, collaborative review, and automation
- [GitHub vibe-coding tutorial](https://docs.github.com/en/copilot/tutorials/vibe-coding) - research/plan/implement/test/iterate workflow, permissions, branches, commits, and project instructions
- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - secure development, verification, and vulnerability-response practices
- [Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) - transparent, testable agent/workflow patterns
- [Anthropic agent eval guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - multi-turn tool/state evaluation and lifecycle feedback
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - reviewed action ownership and prevention learning
- [Agent-first rule](../../../00.agent-governance/rules/agentic.md) - current workspace authority, evidence, and lifecycle behavior
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - current protected actions and escalation boundary
- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md) - approved instruction/vibe and task-evidence constraints

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when provider instruction behavior, Stage 00 authority, QA evidence, or cited guidance changes
- **Update Trigger**: Instruction precedence, tool/permission model, generated-code review, escalation, or vibe-coding boundary changes

## Related Documents

- [research pack index](./README.md)
- [AI agent catalogs](./ai-agent-catalogs.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [document metadata and lifecycle](./document-metadata-lifecycle.md)
