---
trigger: always_on
glob: "**/*"
description: "Implement Task: Systematic strategy for executing complex coding tasks."
---
# Implement Task Standard

## 1. Strategy & Planning

1. **Understand**: Read requirements and constraints fully.
2. **Break Down**: Decompose task into sub-components.
3. **Evaluate**: Choose the best approach (Trade-offs: Performance vs. Simplicity vs. Time).
4. **Verification Plan**: How will we know it works? (Tests, Manual check).

## 2. Implementation Steps

1. **Test First (TDD)**: Write a failing test or define the expected behavior.
2. **Core Logic**: Implement the "Happy Path" first.
3. **Error Handling**: Add edge case management and error flows.
4. **Refactor**: Clean up code, checking naming and structure.
5. **Docs**: Update comments and external documentation.

## 3. Definition of Done

- [ ] Functionality implemented.
- [ ] Tests passing.
- [ ] No regressions (linting, types).
- [ ] Code reviewed (self-review).
