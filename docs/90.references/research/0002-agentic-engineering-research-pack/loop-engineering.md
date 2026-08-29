---
status: active
artifact_id: reference:agentic-engineering-research:loop-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Loop Engineering

## Overview

Loop engineering turns agent work into an observable, bounded sequence rather
than an unbounded prompt-retry cycle. This analysis describes tracked contracts
and retained provider observations; it does not report a live agent loop.

## Purpose

Define a reusable input-to-exit structure with explicit ceilings, feedback,
independent review, and escalation.

## Scope

The subject is the four registered harness loops and the workflow state data.
It excludes hidden reasoning, provider telemetry, live retries, and new hooks.

## Definitions / Facts

A loop has: a current input, an authorized bounded action, a deterministic or
reviewed feedback signal, an exit condition, and an escalation target. Repeating
the same action after its ceiling without new authority is an endless retry,
not controlled remediation.

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `LE-001` | The registry defines four loops: context-bootstrap, bounded-implementation, independent-review, and approved-all-files-gate. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Select the loop by work state rather than inventing a prompt-local process. |
| `LE-002` | Their ceilings are respectively 1, 2, 2, and 1 attempts; failures escalate, narrow then escalate, or record and stop as specified. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | A two-attempt loop permits an initial attempt plus one narrow correction; a failed correction escalates. |
| `LE-003` | Independent review is a distinct read-only loop with a critical-and-important-zero stop condition. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Author validation cannot substitute for independent review. |
| `LE-004` | Historical official agent documentation describes orchestration and sandbox capability, but no provider execution is evidenced for this draft. | retained official observation | HISTORICAL VERIFIED | Task 0001 source ledger | Keep provider behavior separate from local contract evidence. |
| `LE-005` | A retained 2026-08-14 study identifies ReAct, generate-test-repair, plan-execute, multi-attempt retry, and tree search as composable coding-agent loop primitives; it does not make the four local registry loops a one-to-one taxonomy. | retained external study | HISTORICAL VERIFIED | retained dated loop analysis | Treat a one-attempt gate as a checkpoint and map retries only where the local contract has a ceiling. |

### Bounded feedback pattern

| Phase | Required content | Exit or escalation |
| --- | --- | --- |
| Input | Approved objective, current repository state, applicable authority, and changed-path boundary. | Stop when authority or ownership is unknown. |
| Action | A permission-compatible, scoped mutation or read-only inspection. | Do not broaden paths or tools implicitly. |
| Feedback | Focused validator output, a reviewer finding, or an explicit skip record. | Fix only the stated scoped failure. |
| Exit | Named gate and evidence fields are satisfied. | Hand off to the next owner. |
| Escalation | Ceiling reached, protected boundary encountered, or source is insufficient. | Request direction; do not loop indefinitely. |

The workflow data places discovery before design/plan, approval before
implementation, validation before independent review, and evidence before
handoff. These states describe intended routing. They do not prove that a
provider invoked a hook or that a remote CI gate accepted a change.

Historical provider observations add useful, non-local context: Claude's
subagent page described role/schema/model/effort facts, while Codex's described
orchestration, schema, model, and sandbox facts. Both are inputs to choosing a
bounded action; neither proves that this workspace dispatched a subagent or
received hook feedback. The local registry remains the owner of actual loop
ceilings and review gates. Its generic independent-review threshold is
critical-and-important-zero; the approved D0–D7 unit contract is stricter and
requires external C0/I0/M0 before publication.

The retained taxonomy gives a useful interpretation of the actual four local
loops: context-bootstrap precedes a control loop; bounded-implementation is
nearest to multi-attempt retry but has only initial work plus one correction;
independent review is a verdict gate, not test execution; and the one-attempt
approved-all-files gate is a checkpoint rather than a multi-turn loop. The
contract's exit and escalation fields, not the taxonomy, remain operative.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LE-SRC-001` | `LE-001`, `LE-002`, `LE-003` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Contract values are not observed runtime behavior. |
| `LE-SRC-002` | `LE-004` | Claude Code subagents / Anthropic | [official page](https://code.claude.com/docs/en/sub-agents) | retained official observation | retrieval-time page | 2026-08-08T15:48:51+09:00 | Historical role/schema/model/effort capability only. |
| `LE-SRC-003` | `LE-004` | Codex subagents / OpenAI | [official page](https://learn.chatgpt.com/docs/agent-configuration/subagents) | retained official observation | retrieval-time page | 2026-08-08T15:48:51+09:00 | Historical orchestration/schema/model/sandbox facts do not establish local invocation. |
| `LE-SRC-004` | `LE-005` | Inside the Scaffold / arXiv | [primary paper](https://arxiv.org/abs/2604.03515) | retained external study | version not recorded; retained dated loop-source row | 2026-08-14 | The study examined pinned scaffold commits; that is its input, not a paper revision or local execution record. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Use the registered loop for state. | Inspect `harness_loops`, `workflow_states`, and named owner/reviewer fields. | No live loop run. |
| architecture | applies | Escalate design ambiguity to its owner. | Confirm owner before action. | No design accepted here. |
| common | applies | Bound shared-worktree retries. | Inspect exact owned paths. | A ceiling is not enforcement proof. |
| docs | applies | Use feedback to correct only documented gaps. | Review links and metadata. | No broad cleanup. |
| infra | applies | Stop before runtime actions lacking approval. | Require target and rollback. | No service loop. |
| ops | applies | Hand off operational failure to ops owner. | Record sanitized evidence. | No operational result. |
| qa | applies | Use focused gates before review. | Inspect the registered gate and record its actual exit status. | Broad gates remain separate. |
| security | applies | Escalate sensitive or protected failures. | Verify redaction boundary. | No security test. |

## Maintenance

Update only when the registered workflow states or loop fields change. Preserve
actual attempt ceilings and do not infer a successful retry from configuration.

## Related Documents

- [Harness engineering](./harness-engineering.md)
- [Research pack README](./README.md)
