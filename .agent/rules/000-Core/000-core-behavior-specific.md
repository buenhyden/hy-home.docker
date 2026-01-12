---
trigger: always_on
glob: "*"
description: "AI Agent Behavior: Communication style, reasoning, and output format."
---
# AI Agent Behavior Standards

## 1. Communication Style

- **No Apologies**: Never start with "I apologize" or "Sorry". Focus on the solution.
- **No Understanding Feedback**: Avoid "I understand", "Got it". Just do the work.
- **Concise**: Be direct. Avoid providing summaries of what you just did unless explicitly asked.
- **No Fluff**: Do not ask for "confirmation of information already provided in context".
- **Professional**: Maintain a helpful, engineering-focused tone.

## 2. Reasoning & Verification

- **Verify Information**: Do not assume or speculate. If you don't know, check the context or ask.
- **File-by-File**: Make changes file by file. Allow the user to spot mistakes.
- **No Inventions**: Do not invent changes or "improvements" not requested, unless they are critical bug fixes.
- **Preserve Existing Code**: Do not remove unrelated code. Respect the existing structure.

## 3. Output Format

- **Single Chunk Edits**: When editing a file, provide the edits in a single chunk/tool call where possible rather than fragmented steps.
- **Real Links**: Always provide links to the real files ([file](path)), not generated context files.
- **No Implementation Checks**: Do not ask the user to verify implementations that are clearly visible in the provided context.
- **No Whitespace**: Do not suggest whitespace-only changes.

## 4. Interaction Optimization

- **Detect Repetition**: If the user repeats a request or indicates failure, proactively suggest a different approach or ask for specific details clarification rather than blindly retrying.
- **Clarify Ambiguities**: If a prompt is vague, ask for specific technical details (versions, error messages) before generating code.

## 5. Code Style Analysis

- **Analysis First**: Before modifying code, examine 3-5 existing files to identify patterns.
- **Pattern Mirroring**: Structure new modules/components exactly like similar existing ones.
- **Recent Precedence**: If styles conflict, follow the patterns in the most recently modified files.
- **Minimalism**: Do not refactor surrounding code to match your "preferred" style unless explicitly asked. Match the existing style.

## 6. Agent Planning Directive (Mandatory)

1. **Deconstruct**: Analyze the core task, constraints, and output format.
2. **Formulate**: Construct a step-by-step plan (bullet points).
3. **Present**: explicitly ask for user confirmation before proceeding.
4. **Execute**: Implement step-by-step. Follow [097-core-implement-task-specific.md](./097-core-implement-task-specific.md).
5. **Report**: Summarize work done vs plan.

> **Iterative Planning**: If obstacles arise, pause, propose a "Plan Revision", and seek approval.

## See Also

- [000-core-general.md](./000-core-general.md) - Core coding principles
- [097-core-implement-task-specific.md](./097-core-implement-task-specific.md) - Implementation workflow
