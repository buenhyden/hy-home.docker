---
trigger: always_on
glob: "**/*.java"
description: "Spring Boot: Architecture, Dependency Injection, and Security."
---
# Spring Boot Standards

## 1. Project Architecture

- **Layered Design**: Follow the Controller -> Service -> Repository pattern strictly.
- **Package by Feature**: Group code by business domain rather than technical type for larger apps.

### Example: Packaging

**Good**

```text
com.app.auth
  ├── AuthController.java
  ├── AuthService.java
  ├── UserDetailsImpl.java
com.app.product
  ├── ProductController.java
```

**Bad**

```text
com.app.controllers
  ├── AuthController.java
  ├── ProductController.java
com.app.services
  ├── AuthService.java
```

## 2. Dependency Injection

- **Constructor Injection**: ALWAYS use constructor injection over `@Autowired` on fields. This makes testing easier and ensures final fields.
- **Lombok**: Use `@RequiredArgsConstructor` to reduce boilerplate.

### Example: Injection

**Good**

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository; // Final and injected via constructor
}
```

**Bad**

```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository; // Field injection (hard to unit test)
}
```

## 3. Error Handling

- **Global Controller Advice**: Use `@ControllerAdvice` and `@ExceptionHandler` to centralize error responses.
- **Standardized Response**: Return a consistent JSON error object (as per rule 700).

## 4. Security

- **Spring Security**: Use method-level security (`@PreAuthorize`) for fine-grained access control.
- **Defaults**: Disable CSRF only for stateless APIs with JWT.
