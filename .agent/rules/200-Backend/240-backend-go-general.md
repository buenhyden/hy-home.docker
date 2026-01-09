---
trigger: always_on
glob: "**/*.go"
description: "Go General: Idioms, Error Handling, Concurrency, and Project Layout."
---
# Go General Standards

## 1. Error Handling

- **Check Immediately**: Handle errors where they occur. Avoid `else` blocks after error checks.
- **Wrap, Don't Hide**: Use `fmt.Errorf("context: %w", err)` to add context while preserving the underlying error for `errors.Is/As`.
- **Custom Errors**: Define sentinel errors (`var ErrNotFound = errors.New(...)`) for actionable failure states.

### Example: Wrapping

**Good**

```go
func getUser(id string) (*User, error) {
    u, err := db.Find(id)
    if err != nil {
        return nil, fmt.Errorf("getting user %s: %w", id, err)
    }
    return u, nil
}
```

**Bad**

```go
func getUser(id string) (*User, error) {
    u, err := db.Find(id)
    if err != nil {
        return nil, err // Context is lost
    }
    return u, nil
}
```

## 2. Concurrency (Goroutines & Channels)

- **Leak Prevention**: Never start a goroutine without knowing how it stops (Context cancellation or Done channel).
- **Synchronization**: Use `sync.Mutex` for state, `Channels` for data flow ("Share memory by communicating").
- **WaitGroups**: Always wait for goroutines to finish before exiting a function or test.

## 3. Project Structure (Standard Layout)

- **cmd/**: Main applications (`cmd/server/main.go`).
- **pkg/**: Library code ok to use by external apps (optional).
- **internal/**: Private application code (enforced by Go compiler).
- **api/**: OpenAPI/Protobuf definitions.

## 4. Interfaces

- **Consumer Defined**: Define interfaces where they are *used*, not where they are implemented.
- **Keep it Small**: Use single-method interfaces (`Reader`, `Writer`) for greater composability.
