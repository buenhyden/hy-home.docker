---
trigger: always_on
glob: "**/*.md"
description: "Documentation: Technical Writing, README, Changelogs, and ADRs."
---
# Documentation & Technical Writing Standards

## 1. The README Standard

- **The Core Four**: Title, Setup, Usage, Contributing.
- **Examples**: Always include a "Hello World" snippet for libraries/APIs.
- **Badges**: Show CI/CD build status, coverage %, and dependency health.

- **Badges**: Show CI/CD build status, coverage %, and dependency health.

## 2. Documentation Types

- **README**: Project overview, setup, and quick start.
- **API Reference**: Endpoints, parameters, and inputs/outputs.
- **Architecture**: Design decisions (ADRs) and diagrams.
- **Tutorials**: Step-by-step guides for specific tasks.

## 3. Component Documentation Template

For UI components or modules, follow this structure:

1. **Overview**: What is this? Why does it exist?
2. **Usage**: Code examples of how to consume it.
3. **API/Props**: Detailed interface specification (inputs, outputs, events).
4. **Behavior**: Edge cases, error handling, performance notes.

## 4. Technical Writing Style

- **Clarity & Brevity**: Prefer short, declarative sentences.
- **Active Voice**: "The system sends an alert" vs "An alert is sent by the system".
- **Formatting**: Use bold for UI elements (**Click Save**) and backticks for code (`npm start`).

### Example: Writing

**Good**
> To build the app, run `npm run build`. This generates the `dist` folder.

**Bad**
> One should potentially consider running the compilation procedure so that the distribution assets might be successfully generated.

## 3. Inline Documentation (Docstrings)

- **Public API**: Document every public function/class.
- **Why > What**: Explain *why*, not just *what*.
- **Params/Returns**: Explicitly define input types and return values.

## 4. Changelogs

- **Keep A Changelog**: Maintain `CHANGELOG.md` following keepachangelog.com.
- **Sections**: Added, Changed, Fixed, Removed, Deprecated, Security.

## 5. Architecture Decision Records (ADRs)

- **When**: Document significant architectural decisions.
- **Location**: Store in `docs/adrs/` or `docs/decisions/`.
- **Format**: Title, Context, Decision, Status, Consequences.

### Example: ADR

**Good**

```markdown
# ADR-001: Use PostgreSQL for Primary Database
## Status: Accepted
## Context: Need ACID and strong schema.
## Decision: PostgreSQL over MongoDB.
## Consequences: Requires SQL expertise.
```
