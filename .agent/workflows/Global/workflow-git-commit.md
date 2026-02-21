---
description: Workflow for generating Conventional Commits
---

1. **Check Status**

    Review staged changes.

    ```bash
    git status
    git diff --staged
    ```

2. **Run Pre-checks**

    Verify code quality before committing.

    // turbo

    ```bash
    # Run linting/formatting checks
    npm run lint
    ```

    // turbo

    ```bash
    # Run tests related to changes
    npm test
    ```

3. **Analyze Changes**

    Determine `type` and `scope`.

    - **feat**: New feature
    - **fix**: Bug fix
    - **docs**: Documentation only
    - **style**: Formatting (white-space, etc)
    - **refactor**: No functionality change
    - **perf**: Performance improvement
    - **test**: Adding tests
    - **chore**: Build process, deps

4. **Create Commit**

    Use Commitizen or manual conventional format.

    **Format**: `<type>(<scope>): <description>`

    ```bash
    # Interactive mode (Recommended)
    npx cz
    ```

    OR manual:

    ```bash
    git commit -m "feat(auth): implement jwt strategy"
    ```

5. **Verify Commit History**

    Ensure messages are clean and descriptive.

    ```bash
    git log --oneline -n 5
    ```
