---
title: 'Refactor Task Rule'
layer: agentic
---

# Refactor Task Rule

This rule applies to tasks involving repository structure changes, documentation realignment, or major code refactoring.

## 1. Required Skills

- `agent-md-refactor`: Use for splitting or merging large Markdown files.
- `claude-md-improver`: Use for validating content quality post-refactor.
- `doc-coauthoring`: Use when new PRDs/ARDs are needed for the refactor.
- **Skill Autonomy**: Use any additional tools (e.g., `grep_search`, `sequential-thinking`) proactively to ensure accuracy.

## 2. Refactor Workflow

1. **Analyze**: Use `ls -R` and `view_file` to map the current state.
2. **Decompose**: Identify redundant content or misaligned files according to the flat taxonomy in `docs/`.
3. **Execute**: Move content to specialized directories (`docs/specs/`, `docs/guides/`, etc.).
4. **Link Integrity**: Update all relative links in the refactored files.
5. **Metadata**: Ensure every file has the `layer:` key.

## 3. Mandatory Verification

- Run `rg "layer:" <refactored_dir>` to verify metadata.
- Check that all `README.md` index files reflect the new structure.
