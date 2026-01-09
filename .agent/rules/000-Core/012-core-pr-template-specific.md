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
- Updated IAM policy to allow `s3:PutObject`.
- Added resize logic to `ProfileService` to prevent massive uploads.
- Added `test_upload_resize` unit test.

## 🧪 How to Test
1. Login as a Standard User.
2. Go to Settings > Profile.
3. Upload a 5MB PNG.
4. Verify it saves and displays correctly.

## ⚠️ Breaking Changes
- None
```

**Bad**

```markdown
Fixed the upload bug.
```

## 3. Visuals (Frontend)

- **Before/After**: Mandatory for UI changes. Use screenshots or Loom/GIFs.
- **Mobile/Desktop**: Show both if responsive.

### Example: UI PR

**Good**
> **Before**: [Image of broken layout]
> **After**: [Image of fixed layout]

## 4. Verification Checklist

- [ ] Self-Review performed?
- [ ] Tests passed locally?
- [ ] No secrets committed?
- [ ] Documentation updated?
