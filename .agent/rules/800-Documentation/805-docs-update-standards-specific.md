---
trigger: always_on
glob: "docs/**/*.md"
description: "Documentation Update Standards: LLM-friendly formats and timestamping."
---
# Documentation Update Standards

## 1. LLM-Optimized Format

- **Specific References**: Always cite file paths and line number ranges (e.g., `src/core.c:15-45`).
- **No Fluff**: Be concise. Avoid generic intros. Focus on architecture, logic, and patterns.
- **Flexibility**: Use subsections and checklists over rigid narrative.

## 2. Required Structure

1. **Timestamp**: `<!-- Generated: YYYY-MM-DD HH:MM:SS UTC -->` at the top.
2. **Overview**: 2-3 paragraphs max.
3. **Key Files**: List of main entry points and configs.
4. **Workflows**: "How to Build", "How to Test", "How to Deploy".

## 3. Maintenance

- **No Duplication**: Single source of truth. Link between docs (`See [build.md]`).
- **Files Catalog**: Maintain `docs/files.md` with one-line descriptions of project files.
