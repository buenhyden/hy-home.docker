---
layer: ops
---

# INC-20260314: Broken Documentation Discovery Path

> **Status**: Resolved
> **Severity**: SEV-2
> **Owner**: Antigravity

## Summary

During the documentation refactoring, the `gateway.md` markers incorrectly pointed to legacy directory structures, causing AI agents to fail discovery of technical specifications.

## Timeline

- **22:00**: Issue identified - Agent unable to find `refactor-docs-spec.md`.
- **22:05**: Root cause traced to stale relative links in `gateway.md`.
- **22:10**: Fix applied - Corrected markers to `[LOAD:SPEC]` and pointed to flat taxonomy.
- **22:15**: Verification complete - Discovery restored.

## Resolution

Updated `docs/agentic/gateway.md` to use the standardized flat taxonomy paths.
