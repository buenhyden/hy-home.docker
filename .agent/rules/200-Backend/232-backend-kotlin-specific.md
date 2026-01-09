---
trigger: always_on
glob: "**/*.kt"
description: "Kotlin Backend: Multiplatform, Ktor/Spring, and Idiomatic patterns."
---
# Kotlin Backend Standards

## 1. Idiomatic Kotlin

- **Null Safety**: Leverage `?` and `!!` (sparingly). Prefer `requireNotNull`.
- **Coroutines**: Use Suspending functions for non-blocking I/O.
- **Data Classes**: Use for DTOs and internal models to get free `equals`, `hashCode`, `copy`.

### Example: Coroutines

**Good**

```kotlin
suspend fun getUser(id: String): User {
    return repo.findById(id) // Non-blocking
}
```

**Bad**

```kotlin
fun getUser(id: String): User {
    return repo.findById(id).execute() // Blocking main thread
}
```

## 2. State & Immutability

- **Val vs Var**: Use `val` for everything by default.
- **Collection**: Prefer immutable collections (`listOf`, `mapOf`).

### Example: Immutability

**Good**

```kotlin
val users = usersRepo.findAll()
val activeUsers = users.filter { it.isActive }
```

**Bad**

```kotlin
var users = mutableListOf<User>()
// ... mutate list repeatedly
```

## 3. Frameworks

- **Ktor**: Light-weight, async-first.
- **Spring Boot (Kotlin)**: Use constructor injection and `@Service`/`@Repository` with Kotlin idioms.
