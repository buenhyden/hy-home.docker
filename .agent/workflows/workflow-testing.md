---
description: Standard workflow for testing strategy
---

# Testing Workflow

Based on `600-testing-general.md`.

1. **Test Pyramid**
   - Unit Tests: 70-80% (isolated functions)
   - Integration Tests: 15-20% (component interaction)
   - E2E Tests: 5-10% (user journey)

2. **AAA Pattern**
   - **Arrange**: Set up state
   - **Act**: Execute function
   - **Assert**: Verify outcome

3. **Mocking**
   - Mock external APIs (Stripe, Twilio).
   - Use Dependency Injection for testability.

4. **Naming**
   - Pattern: `should_[expected]_when_[condition]`
   - Example: `test_user_creation_returns_201_when_valid_data`

5. **Coverage**
   - Focus on critical business logic.
   - Test edge cases: nulls, empty collections, boundaries.
