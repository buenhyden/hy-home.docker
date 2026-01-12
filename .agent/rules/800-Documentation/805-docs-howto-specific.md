---
trigger: when writing How-To documentation
glob: "docs/**/*.md"
description: Standards for creating user-friendly "How-To" guides.
---

# How-To Documentation Rules

## 1. Persona & Tone

- **Audience**: Non-technical users.
- **Language**: Simple, direct, Action-oriented.
- **Avoid**: Jargon, complex technical details (unless necessary).

## 2. Structure

1. **Title**: Action-oriented ("How To Log In").
2. **Introduction**: Brief purpose (1-3 sentences).
3. **Prerequisites**: What is needed before starting?
4. **Steps**: Numbered, logical sequence.
    - Start with explicit actions ("Click...", "Type...").
5. **Expected Results**: Verification step ("You should see...").
6. **Troubleshooting**: Common issues/solutions.

## 3. Formatting

- **Visuals**: Mention UI elements exactly as they appear (Bold buttons etc.).
- **Markdown**: Use headers, lists, and code blocks for clarity.

## 4. Conversion (Tech -> User)

- **Source**: Test scripts/API docs.
- **Process**: Extract user actions -> Simplify terms -> Add context -> Logical flow.
