---
description: Workflow for Java Spring Boot feature development
---

# Java Spring Boot Workflow

Based on `242-backend-spring-boot-specific.md`.

1. **Requirement Analysis**
    - Identify Domain Entities involved.
    - specialized logic needed? (Service).
    - API Endpoints needed? (Controller).

2. **Domain Modelling**
    - Create/Update `@Entity` classes in `model/` package.
    - Define `@Id`.
    - Create `Repository` interface extending `JpaRepository`.

3. **Service Layer Implementation**
    - Create/Update `@Service` class.
    - Implement Business Logic.
    - **Transaction**: Annotate methods with `@Transactional` if writing.
    - **DTOs**: Map Entites to DTOs for return values.

4. **API Implementation**
    - Create/Update `@RestController`.
    - Define Endpoints (`@GetMapping`, etc.).
    - Inject Service (Constructor Injection).
    - Validation (`@Valid`).

5. **Verification**
    - Write `DataJpaTest` for queries.
    - Write `WebMvcTest` for API contract.
