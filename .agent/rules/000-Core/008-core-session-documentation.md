---
trigger: always_on
glob: "**/*"
description: "Session Documentation: Standards for logging AI agent sessions."
---
# AI Agent Session Documentation Rules

## 1. Core Principle (Sensitive Data & Relevance)

- **Relevance**: Include ONLY session-relevant data. Exclude unrelated files/logs.
- **Redaction**: Replace sensitive data (API keys, PII) with `[REDACTED]`.
- **References**: List full paths for attached/referenced files.

## 2. Documentation Protocol

- **Location**: Store session logs in `docs/conversations/`.
- **Naming**: `YYYY-MM-DD-session-topic.md`.
- **Metadata**: Date, Objective, Participants.
- **Order**: Chronological. Explicit User/Agent separation.

## 3. Structure Example

```markdown
# Conversation Log: <Topic>

**Date:** 2025-12-27
**Objective:** <Objective>

## 1. Request
> <User Request>

### Agent Response
<Agent Action>

## 2. Analysis & Planning
...

## 3. Execution
...

## 4. Summary
<Concise Summary>
```

## See Also

- [019-core-documentation-standards.md](./019-core-documentation-standards.md) - General documentation standards
- [012-core-pr-template-specific.md](./012-core-pr-template-specific.md) - PR documentation
