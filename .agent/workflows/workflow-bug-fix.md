---
description: Systematic workflow for reproducing, fixing, and verifying bug fixes
---

1. **Reproduce the bug**

    Create a minimal, reliable reproduction of the bug.

    **Document reproduction steps:**
    - Environment (OS, browser, versions)
    - Exact steps to trigger the bug
    - Expected vs actual behavior
    - Screenshots/logs if applicable

    **Create reproduction script or test:**

    Python example:

    ```python
    # tests/reproduction/test_bug_123.py
    def test_bug_user_creation_fails():
        """
        Bug #123: User creation fails when email contains plus sign.
        Expected: User created successfully
        Actual: ValidationError raised
        """
        user_data = {'email': 'user+test@example.com', 'name': 'Test'}
        
        # This should pass but currently fails
        user = create_user(user_data)
        assert user.email == 'user+test@example.com'
    ```

    JavaScript example:

    ```javascript
    // __tests__/bugs/bug-123.test.ts
    it('BUG #123: should handle plus sign in email', () => {
      const email = 'user+test@example.com';
      const result = validateEmail(email);
      expect(result.isValid).toBe(true);  // Currently fails
    });
    ```

// turbo
2. **Run reproduction test**

    Verify the test fails as expected (confirms bug exists).

    ```bash
    # Python
    pytest tests/reproduction/test_bug_123.py -v

    # JavaScript
    npm test -- --testNamePattern="BUG #123"

    # Go
    go test -run TestBug123 ./...
    ```

    Expected: **Test FAILS** (this confirms the bug).

    If test passes, bug may already be fixed or reproduction is incorrect.

3. **Investigate root cause**

    Use debugging tools to identify the source of the bug.

    **Debugging techniques:**
    - Add `console.log()` / `print()` statements
    - Use debugger (`pdb` in Python, Chrome DevTools in JS)
    - Review git history (`git log -p -- <file>`)
    - Check related issues/PRs

    **Common bug patterns to check:**
    - Off-by-one errors
    - Null/undefined handling
    - Type mismatches
    - Race conditions
    - Incorrect regex patterns

    ```bash
    # Check when this code was last modified
    git log --follow --oneline -- path/to/buggy/file.py

    # See full changes
    git log -p -- path/to/buggy/file.py
    ```

4. **Write failing test (Test-Driven Fix)**

    Before fixing, write a proper unit test that fails.

    **Follow AAA pattern** (Arrange-Act-Assert):

    ```python
    # tests/unit/test_user_validation.py
    def test_email_validation_handles_plus_sign():
        """Email addresses with + sign should be valid."""
        # Arrange
        valid_emails = [
            'user+tag@example.com',
            'test+123@domain.co.uk',
            'name+filter@company.org',
        ]
        
        # Act & Assert
        for email in valid_emails:
            result = validate_email(email)
            assert result.is_valid, f"Email {email} should be valid"
    ```

// turbo
5. **Run the failing test**

    Confirm the test fails before fixing.

    ```bash
    # Python
    pytest tests/unit/test_user_validation.py::test_email_validation_handles_plus_sign -v

    # JavaScript
    npm test -- test_user_validation

    # Go
    go test -run TestEmailValidation ./...
    ```

    Expected: **Test FAILS**.

6. **Implement the fix**

    Modify the code to fix the bug.

    **Example fix** (email validation):

    Before (buggy):

    ```python
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    ```

    After (fixed):

    ```python
    def validate_email(email: str) -> bool:
        # Added + to allowed characters before @
        pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    ```

    **Code review checklist:**
    - [ ] Fix addresses root cause (not just symptoms)
    - [ ] No breaking changes introduced
    - [ ] Code follows project style guide
    - [ ] Added comments explaining the fix if needed

    // turbo
7. **Run the test again**

    Verify the test now passes.

    ```bash
    # Python
    pytest tests/unit/test_user_validation.py::test_email_validation_handles_plus_sign -v

    # JavaScript  
    npm test -- test_user_validation

    # Go
    go test -run TestEmailValidation ./...
    ```

    Expected: **Test PASSES** ✅

    // turbo
8. **Run regression tests**

    Ensure the fix doesn't break existing functionality.

    ```bash
    # Run all tests for the affected module
    # Python
    pytest tests/unit/test_user*.py -v

    # JavaScript
    npm test -- tests/user

    # Run full test suite
    npm test

    # Go
    go test ./internal/user/... -v
    ```

    Expected: All tests pass.

    If any test fails:
    - Review the failing test
    - Determine if it's a real regression or outdated test
    - Fix regression or update test accordingly

9. **Test manually (if applicable)**

    For UI bugs, manually test the fix in browser/app.

    **Manual testing checklist:**
    - [ ] Bug is fixed in dev environment
    - [ ] No visual regressions
    - [ ] Works across browsers (if web)
    - [ ] Works on different screen sizes
    - [ ] Accessible (keyboard navigation, screen readers)

10. **Document the fix**

    Add comments and update documentation.

    **In code:**

    ```python
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Note: Supports RFC 5322 compliant addresses including plus (+) addressing.
        Fixed in #123 to handle plus sign in local part.
        """
        pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    ```

    **In CHANGELOG.md:**

    ```markdown
    ## [Unreleased]

    ### Fixed
    - Email validation now correctly accepts plus (+) sign in email addresses (#123)
    ```

11. **Commit the fix**

    Create a proper commit following conventional commits.

    ```bash
    git add .
    git commit -m "fix: handle plus sign in email validation (#123)

    - Updated regex pattern to include + character
    - Added test cases for plus-addressing
    - Resolves issue where emails like user+tag@example.com were rejected

    Fixes #123"
    ```

    **Commit message format:**

    ```text
    fix: <description> (#issue)

    <body explaining what and why>

    Fixes #<issue-number>
    ```

12. **Create pull request**

    Submit PR with proper documentation.

    **PR template:**

    ```markdown
    ## Description
    Fixes email validation to accept plus sign (+) in email addresses.

    ## Related Issue
    Fixes #123

    ## Changes
    - Updated `validate_email()` regex pattern
    - Added unit tests for plus-addressing

    ## Testing
    - [x] Added/updated unit tests
    - [x] All tests passing
    - [x] Manually tested in dev environment

    ## Screenshots (if UI change)
    N/A

    ## Checklist
    - [x] Code follows style guide
    - [x] Tests added/updated
    - [x] Documentation updated
    - [x] No breaking changes
    ```

    Push and create PR:

    ```bash
    git push origin fix/email-validation-plus-sign
    ```

    Then create PR via GitHub/GitLab UI.

13. **Request code review**

    Ask team member to review the fix.

    **Review checklist for reviewer:**
    - Root cause properly identified?
    - Fix is minimal and focused?
    - Tests are comprehensive?
    - No regressions introduced?
    - Documentation updated?

    **Next Steps:**
    - Monitor for related issues after deployment
    - Consider adding validation tests for other edge cases
    - Review `agent/rules/016-core-bug-fix-workflow-specific.md` for advanced patterns
