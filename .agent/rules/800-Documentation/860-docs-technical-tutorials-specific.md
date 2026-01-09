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
