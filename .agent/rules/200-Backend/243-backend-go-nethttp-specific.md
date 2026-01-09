---
trigger: always_on
glob: "**/*.go"
description: "Go Standard Library HTTP: net/http patterns, Middleware, and Timeouts."
---
# Go Standard Library HTTP Standards

## 1. Server Configuration

- **Timeouts**: ALWAYS set `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` on `http.Server`.
- **Mux**: Use `http.NewServeMux()` or Go 1.22+ pattern matching (`GET /users/{id}`).

### Example: Server

**Good**

```go
srv := &http.Server{
    Addr:         ":8080",
    Handler:      mux,
    ReadTimeout:  10 * time.Second,
    WriteTimeout: 10 * time.Second,
}
```

**Bad**

```go
http.ListenAndServe(":8080", mux) // No timeouts, vulnerable to Slowloris attacks
```

## 2. Handler Pattern

- **Signature**: `func(w http.ResponseWriter, r *http.Request)`.
- **Context**: Respect `r.Context()` for cancellation signals from the client.

### Example: Cancellation

**Good**

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    result, err := slowQuery(ctx) // Cancels if client disconnects
    ...
}
```

**Bad**

```go
func handler(w http.ResponseWriter, r *http.Request) {
    result, _ := slowQuery(context.Background()) // Ignores client cancellation
}
```

## 3. JSON Handling

- **Encoding**: Use `json.NewEncoder(w).Encode(v)` for streaming response.
- **Decoding**: Use `json.NewDecoder(r.Body).Decode(&v)` for request body.
