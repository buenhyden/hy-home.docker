---
description: Standard workflow for releases and versioning
---

# Release Workflow

Based on `460-infra-automation-workflow-specific.md` and `015-core-changelog-specific.md`.

1. **Pre-Release Check**
   - All tests pass.
   - No uncommitted changes.

2. **Version Bump**
   - Determine version type (major/minor/patch) based on commits.
   - Update version in config files.

3. **Changelog**
   - Update `CHANGELOG.md` following Keep a Changelog format.
   - Sections: Added, Changed, Fixed, Removed, Deprecated, Security.

4. **Tag & Push**

   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

5. **Deploy**
   - Trigger CI/CD pipeline or manual deployment.
