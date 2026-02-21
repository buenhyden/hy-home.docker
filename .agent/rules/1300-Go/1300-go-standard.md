---
trigger: model_decision
glob: ["**/*.go"]
description: "Go Standards: Enforces idiomatic Go patterns, explicit error handling, and high-concurrency safety."
---

# Go Development Standards

- **Role**: Senior Go (Golang) Engineer
- **Purpose**: Define standards for writing simple, efficient, and idiomatic Go code that leverages the language's strengths in concurrency and performance.
- **Activates When**: Developing Go microservices, implementing CLI tools, or managing Go modules.

**Trigger**: model_decision — Apply during the development of Go-based backend and systems logic.

## 1. Standards

### Principles

- **[REQ-GO-01] Explicit Error Handling**
  - Go errors MUST be handled explicitly where they occur. Wrapping errors with context (`fmt.Errorf("...: %w", err)`) is required for traceability.
- **[REQ-GO-02] Concurrency via Communication**
  - Favor Channels and Goroutines for managing concurrency (CSP model). Avoid shared memory and complex mutex locking where channels suffice.
- **[REQ-GO-03] Consumer-Side Interfaces**
  - Define interfaces at the site of consumption (where they are used) rather than at the site of implementation, following Go's decoupling philosophy.

### Go Toolset Baseline

| Category | Requirement ID | Mandatory Tooling |
| --- | --- | --- |
| Formatting | [REQ-GO-04] | `gofmt` / `goimports` |
| Linting | [REQ-GO-05] | `golangci-lint` |
| Testing | [REQ-GO-06] | `go test` with Table-Driven tests |
| Modules | [REQ-GO-07] | `go mod tidy` / `go.sum` |

### Must

- **[REQ-GO-08] Standard Directory Layout**
  - Projects SHOULD follow the `golang-standards/project-layout` (e.g., `/cmd`, `/internal`, `/pkg`) to maintain ecosystem consistency.
- **[REQ-GO-09] Context Propagation**
  - All long-running or network-dependent functions MUST accept a `context.Context` as their first parameter to support cancellation.
- **[REQ-GO-10] Zero-Value Safety**
  - Structs and functions MUST be designed to have safe and useful "zero-value" states wherever possible.

### Must Not

- **[BAN-GO-01] Recoverable Panic**
  - DO NOT utilize `panic()`/`recover()` for control flow. Reserve `panic()` only for truly unrecoverable system initialization errors.
- **[BAN-GO-02] Unchecked Named Returns**
  - Avoid "Naked Returns" in large functions; always specify the return values explicitly for clarity.

### Failure Handling

- **Stop Condition**: Stop execution if the Go race detector (`-race`) identifies a data race condition during the test phase.

## 2. Procedures

- **[PROC-GO-01] Table-Driven Testing**
  - IF testing a function with multiple edge cases THEN MUST utilize the Table-Driven Test pattern for exhaustive coverage.
- **[PROC-GO-02] Dependency Management**
  - Run `go mod tidy` before every PR submission to ensure `go.mod` and `go.sum` are accurately synced.

## 3. Examples

### Idiomatic Error Handling (Good)

```go
func FetchUser(id int) (*User, error) {
    user, err := db.Find(id)
    if err != nil {
        return nil, fmt.Errorf("fetching user %d: %w", id, err)
    }
    return user, nil
}
```

## 4. Validation Criteria

- **[VAL-GO-01] Gofmt Compliance**
  - [ ] Automated check confirms zero formatting diffs in all `.go` files.
- **[VAL-GO-02] Race Detector Pass**
  - [ ] Concurrency-heavy tests pass with the `-race` flag enabled without warnings.
- **[VAL-GO-03] Lint Threshold**
  - [ ] `golangci-lint` returns zero errors for the current package.
