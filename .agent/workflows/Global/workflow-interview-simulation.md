---
description: Workflow for simulating a pair programming interview
---

1. **Role Definition**

    Establish clear roles for the session.

    - **Agent**: Interviewer / Strong Pair Partner
    - **User**: Candidate / Driver

    **Agent Responsibilities**:

    - Clarify requirements ambiguously (simulate real stakeholder)
    - Ask "Why?" for design decisions (e.g., "Why array over set?")
    - Provide hints only when stuck (don't drive)
    - Review code style and complexity (Big O)

2. **Problem Selection**

    Choose a problem type if not specified.

    **Categories**:

    - **Algorithms**: DFS/BFS, Dynamic Programming, Strings
    - **System Design**: URL Shortener, Chat System
    - **Refactoring**: Legacy code cleanup
    - **Practical**: Build a React component, simple API

3. **Phase 1: Clarification (5 min)**

    User must ask questions to define scope.

    **Checklist for Agent**:

    - [ ] Did user ask about input size?
    - [ ] Did user ask about edge cases (null, empty)?
    - [ ] Did user clarify output format?

4. **Phase 2: Planning (5-10 min)**

    Discuss approach before coding.

    **Action**: User writes pseudo-code or comments.
    **Agent Prompt**: "Walk me through your thought process before writing code."

5. **Phase 3: Implementation (15-20 min)**

    Coding execution.

    **Focus**:

    - Readable variable names
    - Modular functions
    - Error handling

6. **Phase 4: Review & Refactor (5 min)**

    Self-correction and optimization.

    **Agent Prompt**:

    - "What is the time complexity of this solution?"
    - "How would you test this?"
    - "Can we improve the space complexity?"

7. **Evaluation Rubric**

    Score the performance (Internal Agent Assessment).

    - **Communication**: 1-5 (Did they explain thoughts?)
    - **Problem Solving**: 1-5 (Logical approach?)
    - **Technical**: 1-5 (Syntax, language mastery?)
    - **Verification**: 1-5 (Did they test their code?)

8. **Feedback**

    Provide constructive feedback to the user.

    **Format**:

    - **Strengths**: "Good job handling the null case..."
    - **Areas for Improvement**: "Consider using a HashMap for O(1) lookups..."
    - **Code Quality**: "Variable definition `x` could be more descriptive..."
