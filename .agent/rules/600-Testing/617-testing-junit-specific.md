---
trigger: always_on
glob: "**/*.java"
description: "JUnit 5: Annotations, Assertions, and Parameterized Tests."
---
# JUnit 5 Standards

## 1. Annotations

- **Lifecycle**: `@BeforeEach`, `@AfterAll` (not `@Before`).
- **Display**: `@DisplayName("Should return 404...")` for readable logs.

### Example: Display

**Good**

```java
@Test
@DisplayName("Should throw exception on invalid input")
void throwOnInvalid() { ... }
```

**Bad**

```java
@Test
void test1() { ... }
```

## 2. Assertions (AssertJ)

- **Fluid**: Use `assertThat(result).isEqualTo(expected)` over `assertEquals`.

### Example: AssertJ

**Good**

```java
assertThat(users).hasSize(1).extracting("name").contains("Alice");
```

**Bad**

```java
assertEquals(1, users.size());
assertEquals("Alice", users.get(0).getName());
```
