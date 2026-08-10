---
status: active
artifact_id: reference:agentic-research:agent-instructions-vibe-coding
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
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

The current implementation expresses that boundary through typed catalog,
path-authority, provider/model, semantic-event, and loop contracts. Generated
Claude, Codex, Gemini, and shared compatibility adapters are validation
surfaces, not additional instruction authorities.

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

| Criterion ID | Practice                                                                                                                    | Primary source                                                                                                                                                                                                                              | Workspace applicability                                                                                                                                                                                                                                | Required evidence                                                                      | Potential owner                      |
| ------------ | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------ |
| AIV-01       | Define one canonical instruction authority and explicit projection/precedence rules.                                        | OpenAI Codex `AGENTS.md`; GitHub repository instructions; Stage 00 governance                                                                                                                                                               | Stage 00 is canonical; root/provider files remain thin projections and GitHub-native instructions are not adopted policy.                                                                                                                              | Authority map; precedence test; provider no-drift check                                | Stage 00 agent governance            |
| AIV-02       | Scope instructions to repository, directory, file pattern, and task context.                                                | OpenAI Codex `AGENTS.md`; Claude Code memory/rules                                                                                                                                                                                          | Prefer nearest applicable tracked guidance and load only context relevant to the changed surface.                                                                                                                                                      | Scope/path examples; conflict resolution; context-size/overflow behavior               | Provider-neutral instruction owner   |
| AIV-03       | Keep instructions short, direct, specific, and verifiable.                                                                  | GitHub custom-instruction guidance                                                                                                                                                                                                          | Replace vague quality demands with named paths, commands, expected results, and exclusions.                                                                                                                                                            | Instruction review checklist; executable examples; stale-reference scan                | Stage 00 documentation owner         |
| AIV-04       | Declare available tools and their intended purpose; do not infer authority from tool presence.                              | OpenAI practical guide to building agents                                                                                                                                                                                                   | Tool access remains subordinate to task scope, sandbox, approval, and external-action boundaries.                                                                                                                                                      | Tool list; allowed action class; failure behavior; audit evidence                      | Agent/runtime contract owner         |
| AIV-05       | Default to least privilege and request approval for state-changing, sensitive, or out-of-scope actions.                     | Claude Code security; OpenAI agent guardrails                                                                                                                                                                                               | Matches repository sandbox and approval-boundary rules; permission metadata alone is not proof of enforcement.                                                                                                                                         | Sandbox/permission evidence; approval source; denied-action test                       | Security and approval-boundary owner |
| AIV-06       | Require tests, static analysis, and relevant security/contract checks before accepting generated code.                      | GitHub Review AI-generated code; NIST SSDF v1.1                                                                                                                                                                                             | Use the exact QA evidence classes applicable to the changed surface.                                                                                                                                                                                   | Named commands/jobs, results, skipped-check rationale, regression evidence             | QA scope and task owner              |
| AIV-07       | Assign AI-generated code to the same accountable human/team and canonical artifact owner as human-written code.             | NIST SSDF v1.1 is the primary source. GitHub's Review AI-generated code page supports the weaker claim that human judgment stays essential throughout review; re-verified 2026-08-07, it does not state a formal ownership-assignment rule. | “AI generated” may describe provenance but never transfers responsibility.                                                                                                                                                                             | Reviewer, accepted diff, traceable task/spec, license/provenance review where relevant | Change owner and reviewer            |
| AIV-08       | Increase independent review with complexity, sensitivity, irreversibility, novelty, and blast radius.                       | GitHub collaborative-review guidance; OpenAI human-intervention guidance                                                                                                                                                                    | Protected governance, security, runtime, secrets, CI, provider, and remote surfaces require explicit thresholds/approval.                                                                                                                              | Risk classification; reviewer independence; approval and rollback evidence             | Task owner plus specialist reviewer  |
| AIV-09       | Verify suggested dependencies, APIs, licenses, and maintenance rather than trusting plausible output.                       | GitHub Review AI-generated code, which names the concrete failure mode: "Watch out for hallucinated or suspicious packages (such as packages that don't actually exist), or slopsquatting."                                                 | Applies to every new package, action, image, API, or copied pattern. Slopsquatting is the attack that registers a package name models are known to hallucinate, so registry presence is not by itself verification.                                    | Authoritative lookup; lock/registry evidence; license and security check               | Dependency/security owner            |
| AIV-10       | Track shortcuts and unresolved generated-code defects as owned debt; never delete/skip tests merely to make the loop green. | GitHub Review AI-generated code; Google SRE postmortem action ownership                                                                                                                                                                     | Debt belongs in canonical Spec/Plan/Task or issue surface, with priority and verification, not chat history.                                                                                                                                           | Debt item, owner, rationale, due/review trigger, linked failing evidence               | Earliest canonical lifecycle owner   |
| AIV-11       | Escalate after declared retry/action thresholds or whenever a high-risk action is required.                                 | OpenAI practical guide to building agents                                                                                                                                                                                                   | Stop on repeated failure, missing authority, contradictory instructions, uncertain high-impact state, or irreversible action.                                                                                                                          | Threshold in task/agent contract; concise attempts; blocking question or handoff       | Workflow/task owner                  |
| AIV-12       | Treat repository content, web pages, tool output, and third-party agent packs as potentially untrusted instructions.        | Claude Code prompt-injection guidance; OpenAI guardrails                                                                                                                                                                                    | Data does not override Stage 00 or direct task authority; external catalogs remain offline/pinned references by default.                                                                                                                               | Source classification; injection review; tool/permission boundary                      | Security owner                       |
| AIV-13       | Bound vibe coding to a branch/worktree, explicit objective, small increments, and reversible commits.                       | GitHub vibe-coding tutorial                                                                                                                                                                                                                 | Suitable for prototypes and approved implementation when the same plan, review, and evidence gates apply.                                                                                                                                              | Scoped plan/task; isolated workspace; per-iteration diff/test; logical commits         | Implementation task owner            |
| AIV-14       | Keep vibe coding away from unapproved runtime, production data, secrets, remote mutations, and security-critical decisions. | GitHub vibe-coding permissions/testing; OpenAI/Claude security guidance                                                                                                                                                                     | Those surfaces need explicit authority, specialist review, rollback/recovery, and validation before action.                                                                                                                                            | Approval record; redaction boundary; rollback; specialist verdict                      | Security/operations owner            |
| AIV-15       | Use a closed loop: plan, act, observe tool results, verify, review, and either correct or stop.                             | OpenAI agent guide; Anthropic effective-agent/eval guidance                                                                                                                                                                                 | Agent completion text is not evidence; tracked outputs and checks determine completion.                                                                                                                                                                | Plan/task state, tool results, verification, review verdict, residual concerns         | Workflow supervisor / QA             |
| AIV-16       | Import external agent knowledge only through the canonical catalog intake boundary.                                         | Official provider instruction docs; pinned upstream catalog evidence                                                                                                                                                                        | The typed nine-entry capability intake records adopt/merge/reject/defer decisions; four bounded capabilities are adopted, no upstream persona or voice prose is installed, and catalog breadth or publisher maturity claims never authorize execution. | Pin/license/source review; rewritten scope; security and eval evidence                 | Stage 00 agent catalog owner         |

## Current Workspace Implementation

- Four role surfaces contain the same 14 canonical role IDs while preserving
  provider-native schemas; `.agents` remains compatibility/shared skills, not
  Gemini CLI configuration.
- Twenty-four canonical functions project to Claude and shared skill surfaces.
  Provider sync and repository contract checks detect drift from Stage 00.
- Seven semantic hook events and four typed loops bind instruction execution to
  approval, verification, review, retry, and escalation boundaries.
- Eleven deterministic fixtures and sixteen synthetic regressions exercise agent
  output/eval behavior without making a live-model quality claim.
- The controlled all-files wrapper is implemented but remains an explicit
  task-evidence gate; direct agent execution of `pre-commit run --all-files`
  remains prohibited.

## Current-State Assessment

Re-derived from the tracked tree on 2026-08-07. This restates the bullets above
as a status judgment so the criteria table is not read as uniformly satisfied.

| Criterion | Concern                                          | Current state                                                                                                                                                                                                                        | Status                               | Gap                                                                                                                           |
| --------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| CSA-01    | Instruction authority (AIV-01, AIV-02)           | Stage 00 is canonical; root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are thin shims; `.claude/`, `.codex/`, `.gemini/`, and `.agents/` hold 48, 16, 17, and 41 tracked files respectively, all generated.                           | Implemented                          | Provider precedence differs per vendor and cannot be enforced from this repository.                                           |
| CSA-02    | Tool and permission declaration (AIV-04, AIV-05) | Approval boundaries and environment constraints are tracked; adapter tool metadata is intent, not an enforced allowlist.                                                                                                             | Partially Implemented                | No tracked file proves the operator's active sandbox or permission mode.                                                      |
| CSA-03    | Verification before acceptance (AIV-06)          | Changed-file validation, CI routing, 11 fixtures, and 16 synthetic regressions are tracked. `scripts/hooks/post-tool-validate.sh` normalizes style and conditionally runs `shfmt`, `shellcheck`, `yamllint`, and `git diff --check`. | Implemented for repository semantics | The hook's style tools are all conditional on `command -v`, so a missing tool silently reduces coverage.                      |
| CSA-04    | Escalation thresholds (AIV-11)                   | Four typed `harness_loops` bind `max_attempts` of 1, 2, 2, and 1 with exact stop conditions and failure actions.                                                                                                                     | Implemented for those four           | The six remaining loops in the loop reference have owners but no typed ceiling.                                               |
| CSA-05    | Bounded iteration (AIV-13, AIV-14)               | The Stop gate blocks while task-owned uncommitted paths remain, and the all-files wrapper is a single controlled attempt.                                                                                                            | Implemented                          | All seven semantic event bindings carry `runtime_depth: configured-not-executed`, so no tracked artifact proves a gate fired. |
| CSA-06    | Catalog intake (AIV-16)                          | A typed nine-entry `capability_intake` registry records adopt, merge, reject, and defer decisions.                                                                                                                                   | Implemented                          | No live candidate-role acceptance benchmark exists.                                                                           |

## Adoption Boundary

The criteria above are comparison inputs. Three boundaries govern how they may
be used in this workspace, and each names the file that actually decides.

- **This document sets no instruction authority.** Stage 00 does. A criterion
  that appears to require a new rule becomes real only through
  `docs/00.agent-governance/rules/`, and the generated provider adapters are
  validation surfaces rather than places to write policy.
- **Vibe coding does not relax the Safe Boundary table below.** The permitted
  column is bounded by reversibility and review, not by how conversational the
  session felt. Nothing in the right-hand column becomes available because an
  agent iterated carefully.
- **A criterion is not evidence that it is met.** CSA-02, CSA-04, and CSA-05
  are partial today. Citing AIV-05, AIV-11, or AIV-15 in a task report does not
  discharge them; the named evidence classes do.

## Safe Boundary

| Safe for conversational iteration                                                                                    | Requires stop, explicit authority, or specialist review                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Read-only discovery, local prototypes, bounded code/docs edits, test generation, refactoring with preserved behavior | Secrets, credentials, production/live data, paid or remote actions, deployment/runtime mutation, security controls, model policy, provider adapters, CI protection |
| Small reversible diffs in an isolated branch/worktree with named checks                                              | Unclear scope, conflicting instructions, broad dependency changes, missing rollback, repeated failed verification                                                  |
| Human-reviewed output with task evidence and debt recorded canonically                                               | “Looks right” output, deleted/skipped tests, invented packages/APIs, unreviewed bulk generation                                                                    |

## Corrections to Stale Claims

- **Corrected 2026-08-07.** AIV-07's source attribution was too strong.
  GitHub's Review AI-generated code page emphasizes that human judgment stays
  essential throughout review but does not state a formal ownership-assignment
  rule for AI-generated code. NIST SSDF v1.1 now carries that criterion and the
  GitHub page is cited for the weaker claim it actually makes.
- **Corrected 2026-08-07.** The GitHub vibe-coding tutorial's workflow was
  summarized as "research/plan/implement/test/iterate". The page names six
  phases: Researching with Copilot, Planning the implementation, Building your
  application with Copilot cloud agent, Testing your application, Iterating on
  changes, and Improving your software project. The implementation phase is
  cloud-agent-specific, and the final phase was missing entirely.
- **Added 2026-08-07.** AIV-09 now names slopsquatting, the term the source
  uses for the supply-chain attack that exploits hallucinated package names.
  The earlier text described the risk generically and lost the reason registry
  presence is insufficient evidence.
- **Confirmed 2026-08-07.** Both GitHub pages still resolve at the cited URLs.
  The Review AI-generated code page still states "Make sure the code compiles
  and all tests pass", still warns against deleting or skipping tests, and
  still recommends asking teammates to review complex or sensitive changes,
  which are the claims AIV-06, AIV-08, and AIV-10 rest on.
- **NOT RE-VERIFIED 2026-08-07.** The OpenAI practical guide PDF is reachable
  and returns a 7,335,065-byte document, but no text layer was extractable by
  the available tooling on this pass. Its claims behind AIV-04, AIV-11, and
  AIV-15 are carried unchanged from the earlier verification and were not
  disproved. The prior HTTP 403 diagnosis on the marketing page is superseded:
  the CDN copy responds, the obstacle is extraction rather than access.

## Source Rules

- Mutable official provider sources were revalidated at
  `2026-08-07T12:45:40+09:00`, and the repo-local implementation comparison was
  reconciled on **2026-07-27**. OpenAI, Anthropic, and GitHub product guidance
  proves retrieval-time behavior only.
- NIST SSDF v1.1 is a February 2022 high-level secure-development framework;
  this reference does not claim formal conformance.
- GitHub's vibe-coding tutorial is official workflow guidance, not evidence that
  conversational iteration is safe for every repository surface.
- Repo-local applicability is based on tracked Stage 00 contracts, generated
  provider surfaces, validators, tests, and QA/CI definitions. Graphify remains
  advisory and must be corroborated against those sources.

## Sources

- [OpenAI Codex custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) - discovery, layering, and nearest-scope precedence
- [OpenAI practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - NOT RE-VERIFIED verbatim on the 2026-08-07 pass. The CDN URL resolves and returns a 7,335,065-byte PDF, but no text layer was extractable by the available tooling, so the cited content — tools in three classes, layered guardrails, explicit retry-threshold and high-risk escalation triggers, and human intervention — is carried from the earlier verification and was not disproved. The published title omits "AI"
- [Claude Code memory and rules](https://code.claude.com/docs/en/memory) - modular and path-scoped project instructions
- [Claude Code security](https://code.claude.com/docs/en/security) - least privilege, sandboxing, approval, prompt injection, and user review responsibility
- [GitHub repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) - repository/path/agent instruction scopes and precedence caveats
- [GitHub Review AI-generated code](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code) - tests, context, quality, dependencies, AI-specific failure modes, collaborative review, and automation
- [GitHub vibe-coding tutorial](https://docs.github.com/en/copilot/tutorials/vibe-coding) - re-verified 2026-08-07; six named phases from Researching with Copilot through Improving your software project, plus branch creation, per-iteration commits, permission prompts for sensitive files and commands, and project instructions
- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - secure development, verification, and vulnerability-response practices
- [Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) - transparent, testable agent/workflow patterns
- [Anthropic agent eval guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - multi-turn tool/state evaluation and lifecycle feedback
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - reviewed action ownership and prevention learning
- [agency-agents pinned repository](https://github.com/msitarzewski/agency-agents/tree/8ef49232e02431f7ca4792b487e5a85a7939ff3a) - immutable upstream catalog tree supporting the reference-only intake and pin/review boundary
- [Agent-first rule](../../../00.agent-governance/rules/agentic.md) - current workspace authority, evidence, and lifecycle behavior
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - current protected actions and escalation boundary
- [Spec 123](../../../98.archive/03.specs/123-agentic-engineering-audit-remediation/spec.md) - approved instruction/vibe and task-evidence constraints

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when provider instruction behavior, Stage 00 authority, QA evidence, or cited guidance changes
- **Update Trigger**: Instruction precedence, tool/permission model, generated-code review, escalation, or vibe-coding boundary changes

## Related Documents

- [research pack index](./README.md)
- [AI agent catalogs](./ai-agent-catalogs.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [document metadata and lifecycle](./document-metadata-lifecycle.md)
