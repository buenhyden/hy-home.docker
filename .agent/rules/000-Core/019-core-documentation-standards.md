---
trigger: always_on
glob: "**/*.{md,txt,rst,adoc}"
description: "Documentation Standards: README, Docstrings, API Docs, ADRs, and Technical Writing."
---

# Documentation Standards

## 1. README Standards

### The Core Four

Every project README must include:

- **Purpose**: Clearly state *why* the project exists and what problem it solves.
- **Tech Stack**: List key technologies and versions.
- **Setup**: Installation and prerequisites
- **Usage**: Quick start examples
- **Contributing**: How to contribute (if applicable)
- **Folder Structure**: Include a logical map of important directories.

### Additional Sections

- **Badges**: CI/CD status, coverage %, dependency health
- **Features**: What the project does
- **License**: Licensing information

### Example Structure

````markdown
# Project Name

Brief description (1-2 sentences).

## Features
- Feature 1
- Feature 2

## Setup
```bash
npm install
```

## Usage

```javascript
import { foo } from 'bar';
foo();
```
````

## 2. Inline Documentation (Docstrings)

### Python (Google Style)

```python
def process_items(items: List[str], retry_count: int = 3) -> Optional[int]:
    """Processes a list of items with retry logic.

    Args:
        items (List[str]): List of item IDs to process.
        retry_count (int): Maximum number of retries.

    Returns:
        Optional[int]: Number of successfully processed items.
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    return len(items)
```

### TypeScript (JSDoc)

```typescript
/**
 * Fetches user data from the API
 * @param userId - The ID of the user to fetch
 * @returns Promise resolving to user object
 */
async function fetchUser(userId: string): Promise<User> {
  // Implementation
}
```

## 3. API Documentation

Document endpoints with:

- **Method**: GET, POST, PUT, DELETE
- **Path**: `/api/v1/users/:id`
- **Parameters**: Path, query, and body parameters
- **Response**: Status codes and body structure
- **Examples**: Request/response examples

## 4. Architecture Decision Records (ADRs)

### Format

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
Need ACID compliance and strong schema support.

## Decision
Use PostgreSQL instead of MongoDB.

## Consequences
**Positive:** ACID compliance, rich queries
**Negative:** Requires SQL expertise
```

## 5. Technical Writing Best Practices

### Style

- **Clarity & Brevity**: Use short, declarative sentences
- **Active Voice**: "The system sends" vs "is sent by"
- **Formatting**:
  - Use **bold** for UI elements
  - Use `backticks` for code
  - Use numbered lists for steps

## 6. Code Comments

### When to Comment

- **Why over What**: Explain *why* decisions were made
- **Non-Obvious Logic**: Complex algorithms
- **TODOs**: Only if tracked (include issue number)

### When NOT to Comment

- **Self-Explanatory Code**: Good naming eliminates need
- **Commented-Out Code**: Delete it (Git has history)

## See Also

- [008-core-session-documentation.md](./008-core-session-documentation.md) - Session documentation
- [012-core-pr-template-specific.md](./012-core-pr-template-specific.md) - PR templates
- [015-core-changelog-specific.md](./015-core-changelog-specific.md) - Changelog standards
