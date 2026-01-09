---
trigger: always_on
glob: "README.md"
description: "README Maintenance Standards: Keeping documentation up-to-date."
---
# README Maintenance Standards

## 1. Freshness

- **Version Sync**: Ensure version numbers in the README match `package.json`/`pyproject.toml`.
- **New Features**: Update the "Features" section immediately when a new feature is merged.
- **Broken Links**: Regularly check that relative links `[Like This](docs/file.md)` point to existing files.

## 2. Sections to Maintain

- **Installation**: Update if dependencies or install steps change.
- **Configuration**: Keep env var lists and config options current.
- **Changelog**: Maintain a `CHANGELOG.md` or a "Changes" section for significant updates.

## 3. Badges

- **Health**: Use badges for CI status, coverage, and latest version to give immediate health signals.

### Example: Maintenance

**Good**

- [x] Updated version to 1.2.0
- [x] Added new 'Auth' section to README
- [x] Verified all local links
