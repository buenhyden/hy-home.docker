---
trigger: always_on
glob: "CHANGELOG.md"
description: "Changelog Standards: Format and updating guidelines using Keep a Changelog."
---
# Changelog Standards

## 1. Format

- **Standard**: Follow [Keep a Changelog](https://keepachangelog.com).
- **Sections**: Group by `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- **Versioning**: Use Semantic Versioning (SemVer).

## 2. Helper Command

- **Add Entry**: Use `/add-to-changelog <version> <type> <message>` if available.

### Example: Entry

#### Good

```markdown
## [1.1.0] - 2025-01-15

### Added
- New authentication module.

### Fixed
- Crash on login page.
```

## See Also

- [010-core-git-specific.md](./010-core-git-specific.md) - Git workflow and versioning
- [012-core-pr-template-specific.md](./012-core-pr-template-specific.md) - PR templates
