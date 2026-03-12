# Agent Workflow

This guide describes the shared execution loop for agent work in this repository.

## Default Loop

1. Inspect the current state of the repository, docs, and working tree.
2. Confirm or write the relevant spec and implementation plan.
3. Activate the skills that match the task.
4. Execute changes with terminal-backed evidence.
5. Verify the result before claiming completion.
6. Update durable documentation when the work changes behavior or process.

## Execution Rules

- Use repository-local files as the source of truth for commands, paths, and workflows.
- Prefer direct, low-friction execution once the path is clear.
- Retry correctable command failures after reading stderr instead of stopping at the first error.
- Keep edits surgical unless the task explicitly calls for structural rewrites.
- Treat documentation-only work as real work: it still needs verification and link review.

## Maintenance Rules for Root Instruction Files

- `AGENTS.md` should contain only universal repository policy and navigation.
- `CLAUDE.md` should contain only Claude-specific execution behavior.
- `GEMINI.md` should contain only Gemini-specific reasoning behavior.
- Shared rules belong in this guide bundle, not repeated across the roots.
- Every repository-internal link must remain relative.

## Truth Checks

Before finishing an instruction-file change, confirm:

- Root files link to the shared guide bundle.
- Stale tool or artifact names are gone.
- New paths exist in the repository.
- The new structure is easier to skim than the old one.

## Recommended Validation Commands

```bash
rg -n "\\.claude/(core-governance|workflow|README\\.md)" AGENTS.md CLAUDE.md GEMINI.md
test -f docs/specs/agent-instructions/spec.md
test -f docs/plans/2026-03-12-agent-instruction-refactor.md
```
