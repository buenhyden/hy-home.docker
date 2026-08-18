---
layer: agentic
status: active
---

# Reviewer Checkout Destroyed Uncommitted Task State

- Date: 2026-08-13
- Layer: agentic
- Status: active
- Applies To: agent review dispatch, shared worktree safety, commit staging
- Tags: subagent, worktree, data-loss, staging, gates
- Retrieval Keywords: git checkout, dirty state, byte-preserved, subagent
  isolation, staged revert, dangling blob
- Last Verified: 2026-08-13

## Problem

A dispatched specification reviewer ran `git checkout <commit> -- .` inside the
shared worktree it was reviewing. That command overwrites every tracked file in
the working tree and updates the index at the same time. The reviewer
self-reported the violation in its own report.

Two files carried uncommitted, unstaged changes that the active Task had
designated byte-preserved for a later unit. Those changes are gone. They had
never been staged, so no blob object exists, and a scan of all 323 dangling
blobs found neither content. No recovery route exists.

The same command silently staged a revert of an unrelated repair. A freshness
snapshot regenerated one commit earlier was restored to its older content and
staged. The next commit carried that staged revert alongside an intended edit,
so a passing gate regressed inside a commit whose message described something
else entirely.

## Context

The review brief listed `git checkout` among forbidden commands and the
reviewer acknowledged the rule before violating it. A brief is not an
enforcement boundary: a subagent holding shell access to the live worktree can
mutate it regardless of instructions.

Detection failed on the dispatcher side as well. The session verified the two
digests after every commit, which detects drift but cannot reverse it. Digest
verification is a tripwire, not a backup.

The staged revert went unnoticed because the commit staged one path explicitly
and then read the staged list without reconciling it against intent. The extra
path appeared in the output and drew no comment.

A second reviewer in the same round demonstrated the safe pattern: it created
`git worktree add --detach` into a temp path, ran every check there, removed
the worktree afterward, and left the shared tree untouched.

## Resolution

The lost content belonged to Step 0e diagnostic helpers mapped for a later
adoption unit. The Spec amendment of the same date removed that mechanism from
the deletion gate, so the loss blocks neither old-pack deletion nor final
closure. Its effect is confined to that separate track, whose scope now derives
from committed sources alone.

The staged revert was detected by re-running the gate that had previously
measured as passing, then repaired with the canonical generator in a following
commit.

## Prevention

- Copy designated-preserved uncommitted content into scratch storage at the
  moment the designation is made. Git does not protect what it does not track.
- Give reviewers an isolated checkout rather than the live worktree, following
  the detached-worktree pattern the security reviewer used in this same round.
- Treat any digest mismatch on designated paths as an incident that stops work,
  rather than a line item to report and continue past.
- Reconcile the staged path list against the intended path list before every
  commit and stop when they differ. A checkout-updated index adds paths that no
  edit introduced.
- After any concurrent-process incident in a shared worktree, re-run the gates
  previously measured as passing. A revert can restore a stale artifact that no
  longer matches its generator.

## Evidence

- The reviewer's own report names the command and its consequence.
- `git status` showed both designated paths clean and identical to HEAD, where
  they had been dirty for the whole session.
- `git fsck` listed 323 dangling blobs; a content hash comparison over all of
  them matched neither preserved digest.
- The commit diff for the freshness snapshot showed the scanned-script count
  moving back to its pre-repair value, and the generator check failed again
  until regeneration.

## Related Documents

- [Governance memory index](./README.md)
- [Current project memory](./current.md)
- [Rebuild Task](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Ignored scratch deletion note](./ignored-sdd-scratch-deletion.md)
