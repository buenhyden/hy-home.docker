---
trigger: always_on
glob: "**/*.{php,feature,md}"
description: "Test Documentation: Maintaining tests and docs validation."
---
# Test Documentation Maintenance

## 1. Maintenance

- **New Features**: Must include corresponding Unit (backend) or Behat (frontend) tests.
- **Updates**: Modifying code requires updating related tests.

## 2. Validation

- **README**: Ensure every module has an up-to-date `README.md`.
- **Coverage**: Verify test coverage for new logic.

### Example: Requirement

#### Good

```php
// Added new Service class
// ✅ Added ServiceTest.php
```
