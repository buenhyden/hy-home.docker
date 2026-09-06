---
title: "Agent Prompts"
version: "0.1.0"
type: "governance/prompt-index"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
---

# Agent Prompts

## Overview

`.agents/prompts/` holds reusable prompt contracts for recurring agent work.
A prompt declares what it needs, what it must produce, what it must not do, and
what to do when it cannot proceed. It is the envelope around work, not the work
itself.

Both providers read these files from the same canonical path, so a prompt
survives a session boundary and a provider change.

## Scope

- Included: purpose, required inputs, output contract, prohibitions, failure
  handling, and applicable roles, skills, and evaluation criteria.
- Excluded: ordered procedure steps, which belong to `skills/`; obligations,
  which belong to `governance/`; execution state and results, which belong to
  the current Spec Package Task.

Reading a prompt selects no role and grants no permission. The already selected
role's permission profile and the approved Task scope continue to govern.

## Structure

```text
.agents/prompts/
├── README.md
├── commit-message.md
├── diff-review.md
├── handoff.md
└── test-design.md
```

| Prompt | Answers |
| --- | --- |
| `handoff.md` | How does the next session resume from files and Git state alone? |
| `diff-review.md` | How is an exact diff reviewed independently of its author? |
| `commit-message.md` | How is a commit message drafted from the staged diff? |
| `test-design.md` | How are tests derived from a requirement and its failure conditions? |

Prompt slugs are kept distinct from skill ids so a name never resolves to two
different things.

## How to Work in This Area

1. Confirm the need is an input and output contract, not a procedure. A
   procedure belongs in a skill.
2. Copy `docs/99.templates/templates/governance/prompt.template.md` and keep its
   registered sections in order.
3. Name the owning skill and role rather than restating either one.
4. Write prohibitions as concrete refusals, so a reader can tell whether a given
   output violates one.
5. Register the file in `canonical_sources` in the Provider Registry, then run
   the document metadata and agent governance contract checks.

### Applying a Prompt

Load the prompt, supply every required input, and produce exactly the declared
output. If an input is unavailable, follow the prompt's failure handling rather
than substituting an approximation. Record where a prompt was applied in the
current Task; the prompt itself records nothing.

## Related Documents

- [Agent governance index](../README.md)
- [Knowledge index](../knowledge/README.md)
- [Agentic policy](../governance/agentic.md)
- [Canonical knowledge and prompt surfaces decision](../../docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
