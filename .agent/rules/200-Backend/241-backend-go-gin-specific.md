---
trigger: always_on
glob: "**/*.go"
description: "Go Gin: Micro-framework patterns, Binding, and Middleware."
---
# Go Gin Specifics

## 1. Request Binding

- **Method**: Use `ShouldBindJSON` over `BindJSON` (Panic vs Error).
- **Validation**: Use struct tags `binding:"required"`.

### Example: Binding

**Good**

```go
type CreateUser struct {
    Name string `json:"name" binding:"required"`
}

if err := c.ShouldBindJSON(&req); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
}
```

**Bad**

```go
c.BindJSON(&req) // Panics on 400 Bad Request, crashes if no generic recovery
```

## 2. Middleware

- **Context**: Use `c.Set("user", u)` to pass data.
- **Copy**: If passing context to a Goroutine, use `c.Copy()`.

### Example: Async

**Good**

```go
cp := c.Copy()
go func() {
    log.Println(cp.Request.URL.Path)
}()
```

**Bad**

```go
go func() {
    log.Println(c.Request.URL.Path) // Race condition!
}()
```
