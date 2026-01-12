---
trigger: always_on
glob: ".github/pull_request_template.md"
description: "Pull Request Template: Standardized Description, Checklist, and Breaking Changes."
---
# Pull Request Template Standards

## 1. Required Sections

- **Why**: The business value or bug being solved. Link to JIRA/Linear ticket.
- **What**: Technical summary of changes.
- **How to Test**: Step-by-step specific instructions.
- **Breaking Changes**: Explicit warning if API/Schema changes occur.

## 2. The Golden Template

Use this structure for all repositories:

### Example: Full Template

**Good**

```markdown
## 🎫 Ticket
[JIRA-123](https://jira.company.com/browse/JIRA-123)

## 📖 Context (Why)
Users were unable to update their profile pictures due to a missing S3 permission.

## 🛠 Changes (What)
- Updated IAM policy to allow s3:PutObject.
- Added resize logic to ProfileService to prevent massive uploads.
- Added 	est_upload_resize unit test.

## 🧪 How to Test
1. Login as a Standard User.
2. Go to Settings > Profile.
3. Upload a 5MB PNG.
4. Verify it saves and displays correctly.

## ⚠️ Breaking Changes
- None
```

## 3. Visuals (Frontend)

- **Before/After**: Mandatory for UI changes. Use screenshots or Loom/GIFs.
- **Mobile/Desktop**: Show both if responsive.

## 4. Verification Checklist

- [ ] Self-Review performed?
- [ ] Tests passed locally?
- [ ] No secrets committed?
- [ ] Documentation updated?

## 5. Automated Changelists (Agent)

If generating a PR description automatically:

- **Structure**: Start with # Summary of Changes, then use ## Categories.
- **Items**: Past tense verbs (Added, Fixed), backticks for code (ariable).
- **Validation**: Ensure output starts with  `markdown  and # Summary.

### Example: Automated Output

```markdown
# Summary of Changes

## Auth
- Added login function.
- Fixed token expiration bug.
```

## 6. Platform Specifics

- **GitHub/GitLab/Azure**: Adapt the template syntax (Markdown) slightly for the specific platform's rendering quirks if necessary, but keep the core sections consistent.

## See Also

- [010-core-git-specific.md](./010-core-git-specific.md) - Git commit standards
- [015-core-changelog-specific.md](./015-core-changelog-specific.md) - Changelog maintenance
- [019-core-documentation-standards.md](./019-core-documentation-standards.md) - Documentation practices
