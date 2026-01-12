---
trigger: always_on
glob: "**/*.md"
description: "Documentation: Writing effective technical tutorials and guides."
---
# Technical Tutorial Standards

## 1. Style & Tone

- **Direct**: Start with technical content immediately. No fluff.
- **Peer-to-Peer**: Write as if explaining to a colleague.
- **Practical**: Focus on "How" and "Why", not definitions.

## 2. Structure

- **Overview**: 1-2 sentences on what will be built.
- **Subtitles**: Meaningful, action-oriented headers.
- **Code**: Substantial, copy-pasteable examples.
- **Explanation**: Explain *why* specific approaches were chosen.

## 3. Anti-Patterns

- **Clichés**: Avoid "In today's world...", "Robust", "Crucial".
- **Wall of Text**: Break up text with code, alerts, or lists.
- **Generic Conclusions**: Consolidate "In conclusion" into a final "Next Steps" or summary.

## 4. Code Standards

- **Complete**: Provide substantial, copy-pasteable code snippets, not pseudo-code.
- **Context**: Indicate file paths and where the code belongs in the structure.
- **Explanation**: Explain *why* a specific approach was taken.

### Example: Introduction

#### Good

```markdown
# Building a REST API with FastAPI

This guide demonstrates how to build a type-safe REST API using FastAPI and Pydantic. We will implement CRUD operations, dependency injection for database sessions, and JWT authentication.
```

#### Bad

```markdown
# Introduction

In the modern landscape of web development, APIs are crucial. FastAPI is a robust framework... (fluff)
```

## 5. End-User Guide Standards (How-To)

- **Audience**: Non-technical users. Avoid jargon (e.g., "Hit the endpoint" -> "Click the button").
- **Title**: Action-oriented (e.g., "How to Log In", not "Login Functionality").
- **Structure**:
  1. **Goal**: 1 sentence summary.
  2. **Prereqs**: What is needed before starting.
  3. **Steps**: Numbered, imperative steps ("Click X", "Type Y").
  4. **Validation**: "You should see..."
  5. **Troubleshooting**: "If X happens, do Y".

## 6. How-To Guide Structure

- **Problem-First**: Start with the specific problem the user is solving.
- **Steps**: Numbered, clear instructions.
- **Verification**: Explicit "How to test this works" step.

## 7. How-To Guide Structure (Session-Aligned)

- **Problem-First**: Start with the specific problem the user is solving.
- **Steps**: Numbered, clear instructions.
- **Verification**: Explicit "How to test this works" step.
- **Relevance**: Exclude unrelated data. If documenting a session, redact sensitive info (`[REDACTED]`) and omit non-essential logs.