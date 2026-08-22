---
profile_id: governance-policy
layer: agentic
---

# Approval Boundaries

Approval is bound to a named surface, operation, evidence route, and recovery.
It never expands through delegation or provider handoff.

**Core Rules**

- Never read or record secret values, credentials, private keys, raw logs, auth
  files, shell history, or tokens.
- Runtime restart, rollout, deployment, remote mutation, credential change, and
  destructive recovery require separate explicit approval.
- Provider, model, permission, retry, and stop bounds come from the canonical
  role frontmatter and `providers/registry.yaml`.
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
