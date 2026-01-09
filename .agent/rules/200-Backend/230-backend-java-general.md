---
trigger: always_on
glob: "**/*.{java,kt,kts}"
description: "Java/Kotlin General: Streams, Optionals, and Null Safety."
---
# Java General Standards

## 1. Modern Java (Streams & Optionals)

- **Streams**: Use for collections processing. Avoid imperative for-loops for mapping/filtering.
- **Optional**: Use `Optional<T>` for return types that might be absent. Never return `null` from public API.

### Example: Streams

**Good**

```java
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());
```

**Bad**

```java
List<String> names = new ArrayList<>();
for (User u : users) {
    if (u.isActive()) names.add(u.getName());
}
```

## 2. Kotlin Specifics

- **Null Safety**: Use `User?` instead of `Optional<User>`.
- **Expression Body**: Use `=` for single-expression functions.

### Example: Kotlin

**Good**

```kotlin
fun hasAccess(user: User): Boolean = user.role == "ADMIN"
```

**Bad**

```kotlin
fun hasAccess(user: User): Boolean {
    return user.role == "ADMIN"
}
```
