---
description: Standard workflow for releases and versioning
---

1. **Pre-Release Validation**

    Ensure branch is clean and tests pass.

    // turbo

    ```bash
    git status
    npm test
    npm run build
    ```

2. **Determine Version**

    SemVer rules:

    - **Major**: Breaking changes
    - **Minor**: New features (backward compatible)
    - **Patch**: Bug fixes

3. **Update Version & Changelog**

    Bump version and generate changelog.

    ```bash
    # Standard versioning (updates package.json & CHANGELOG)
    npx standard-version --dry-run
    # If looks good:
    npx standard-version
    ```

4. **Push Release**

    Push new version and tags.

    ```bash
    git push --follow-tags origin main
    ```

5. **Deploy**

    Monitor deployment pipeline.

    - Check CI/CD logs (GitHub Actions)
    - Verify production health check

6. **Post-Release Verification**

    Smoke test the deployed version.

    ```bash
    curl -I https://api.production.com/health
    ```
