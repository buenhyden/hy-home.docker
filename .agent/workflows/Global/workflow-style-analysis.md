---
description: Workflow for analyzing and adopting existing code styles
---

# Code Style Analysis Workflow

Based on `005-code-style-consistency.md`.

1. **Selection**
    - Identify 3-5 representative files in the target module/project.
    - Focus on recent commits to capture evolving standards.

2. **Analysis (The "Style Profile")**
    - **Exec**: Analyze naming conventions (Variables, Functions).
    - **Exec**: Analyze formatting (Indentation, Brackets).
    - **Exec**: Analyze patterns (Async handling, Error patterns).

3. **Documentation**
    - Create a brief "Style Profile" summary.
    - *Example*: "Project uses snake_case, 4-space indent, and functional patterns."

4. **Implementation**
    - Apply the Style Profile to new code.
    - **Action**: Use "Pattern Mirroring" - Copy structure from existing files.

5. **Verification**
    - Compare new code side-by-side with reference files.
    - Ensure no "foreign" idioms were introduced.
