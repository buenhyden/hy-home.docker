---
title: "Approval Boundaries"
version: "1.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
---

# Approval Boundaries

Approval is bound to a named surface, operation, evidence route, and recovery.
It never expands through delegation or provider handoff.

**Core Rules**

- Never read or record secret values, credentials, private keys, raw logs, auth
  files, shell history, or tokens.
- Runtime restart, rollout, deployment, remote mutation, credential change, and
  destructive recovery require separate explicit approval.
- Role permissions come from canonical role frontmatter; provider/model and
  permission translations come from `providers/registry.yaml`; lifecycle,
  retry, and stop behavior comes from [workflows.md](workflows.md). Provider
  facts cannot override Stage 00 policy.
- Untracked or ignored scratch state is not evidence. Preserve other workers'
  dirty state and stop if ownership cannot be proven.
- A configured hook or provider surface proves tracked adoption only.

**Shared-worktree Safeguards**

- Never infer deletion safety from parent ignore probes. Bind scratch ownership
  to the controller that created the path and separate inspection and deletion.
- Delete ignored or untracked scratch only after review of its exact owner,
  path, and disposition. Stop when that ownership cannot be proven.
- Isolate reviewer worktrees from implementation worktrees and preserve every
  task-owned or user-owned dirty path.
- Stop on digest mismatch, reconcile staged paths against the approved ledger,
  and do not mutate the index during an unstaged review-fix round.
- Rerun all affected gates after a concurrency incident before reporting
  completion.

**Documentation Write Permission**

- `doc-writer` may edit approved documentation.
- All other roles are read-only unless their Task explicitly includes a
  documentation update.
- `workflow-supervisor`, `rules-engineer`, `eval-engineer`, and
  `code-reviewer` remain read-only even when they route or review writable work.
- Policy changes require `rules-engineer` review.

**Protected Surfaces**

| Surface | Required evidence | Recovery |
| --- | --- | --- |
| Compose and `infra/**` | scoped Compose validation and Task approval | revert config; no implicit runtime action |
| `secrets/**` and real environment values | path-only redacted evidence | revert mapping; rotate only with approval |
| `.github/workflows/**` | workflow contract and security review | revert logical commit |
| `scripts/**` | focused tests and harness validation | revert logical commit |
| `.agents/**`, `.claude/**`, `.codex/**` | Stage 00 contract and renderer parity | regenerate from canonical source |
| `docs/00.agent-governance/**` | Stage 00 contract, links, and Task evidence | revert logical commit |
| `docs/99.templates/**` | registry/schema validation and Task evidence | revert logical commit |

## Related Documents

- [Environment constraints](environment-constraints.md)
- [Agentic policy](agentic.md)
- [Provider registry](../providers/registry.yaml)
- [GitHub governance](github-governance.md)
