---
trigger: always
glob: [".github/PULL_REQUEST_TEMPLATE.md"]
description: "Pull Request Template: Standardized Description, Checklist, and Breaking Changes."
---

# 0850-Documentation-PR

- **Role**: Developer
- **Purpose**: Enforce standardized PR descriptions to ensure context, testability, and breaking change awareness.
- **Activates When**: Creating or reviewing Pull Requests.

## 1. Standards

### 1.1 Principles

- **[REQ-PR-GEN-01] Context**: Every PR MUST explain the *Why* (business value/bug).
- **[REQ-PR-GEN-02] Testability**: Every PR MUST provide specific "How to Test" steps.
- **[REQ-PR-GEN-03] Safety**: Breaking changes MUST be explicitly flagged.

### 1.2 Scope

- **In-Scope**: PR Descriptions, Merge Requests.
- **Out-of-Scope**: Commit messages (see Git standards).

### 1.3 Inputs & Outputs

- **Inputs**: Code changes, JIRA/Linear ticket.
- **Outputs**: Comprehensive PR description.

### 1.4 Must / Must Not

- **[REQ-PR-SEC-01] Required Sections**: Why, What, How to Test, Breaking Changes.
- **[REQ-PR-VIS-01] Visuals**: UI changes MUST include screenshots or video.
- **[BAN-PR-LOL-01] Empty Description**: PRs MUST NOT have empty descriptions.

## 2. Procedures

### 2.1 Writing a PR Description

1. **Ticket**: Link the tracker issue.
2. **Context**: Summarize the problem.
3. **Changes**: List technical changes (bullet points).
4. **Test**: Numbered steps to verify.
5. **Visuals**: Attach media if UI changed.

## 3. Examples

### 3.1 Good PR Description

```markdown
### 🎫 Ticket
[JIRA-123](https://jira.company.com/browse/JIRA-123)

### 📖 Context
Users were unable to update profiles due to missing S3 permission.

### 🛠 Changes
- Updated IAM policy to allow s3:PutObject.
- Added resize logic.

### 🧪 How to Test
1. Login as Standard User.
2. Settings > Profile.
3. Upload 5MB PNG.
4. Verify success.

### ⚠️ Breaking Changes
- None
```

## 4. Validation Criteria

- [ ] **[VAL-PR-STR-01]** All required sections (Why, What, Test) are present.
- [ ] **[VAL-PR-VIS-01]** UI changes have screenshots.
- [ ] **[VAL-PR-TST-01]** Test steps are reproducible.

## 5. References

- None.
