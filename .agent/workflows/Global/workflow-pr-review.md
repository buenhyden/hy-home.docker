---
description: Standard workflow for reviewing Pull Requests
---

1. **Checkout Branch**

    Switch to the PR branch locally for verification.

    ```bash
    # Assuming you have gh cli
    gh pr checkout <PR-NUMBER>
    ```

2. **Requirements Check (50%)**

    Verify against issue requirements.

    - [ ] Meets Acceptance Criteria?
    - [ ] Handles edge cases?
    - [ ] UI matches design (if applicable)?

3. **Automated Checks (30%)**

    Run local verification.

    // turbo

    ```bash
    npm install
    npm run lint
    npm run test
    ```

4. **Security & Standards Code Review (20%)**

    Manual inspection of code.

    - **Security**: Check for SQLi, XSS, exposed secrets.
    - **Performance**: N+1 queries, large loops.
    - **Style**: Naming conventions, function size.

5. **Submit Review**

    Provide structured feedback.

    - **[NIT]**: Minor style preference (Optional)
    - **[SUGGESTION]**: Better approach (Recommended)
    - **[BLOCKER]**: Critical issue (Required fix)

    ```bash
    # Approve using GH CLI
    gh pr review --approve -b "LGTM! Checked locally, tests pass."
    ```
