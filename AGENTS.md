# AGENTS.md

## Bootstrap

1. Explicitly read `.agents/governance/bootstrap.md`.
2. Explicitly read `.codex/provider.md`; Markdown links are not automatic imports.
3. Load the active Spec Package and its current Task when the request changes repository state.
4. Use `.agents/README.md` to select only the applicable policy and role. Invoke
   `.agents/skills/<name>/SKILL.md` explicitly when the task needs that procedure;
   discovery and invocation never expand the approved scope or permissions.
