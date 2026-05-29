---
name: code-review-dimensions
description: >
  Structured reference for four-domain code review: CWE vulnerability patterns (Python/JS/Java/Go),
  OWASP Top 10 checklist, SOLID violation identification, code smell-to-refactoring mapping,
  complexity metrics, and design pattern guidance. Use for 'CWE patterns', 'SQL injection', 'XSS',
  'SOLID violations', 'refactoring', 'code smells', 'complexity thresholds', 'architecture review',
  'performance review'. Enhances code-reviewer. Note: penetration testing execution is outside scope.
---

# Code Review Dimensions — Four-Domain Reference

Structured reference for the `code-reviewer` agent covering Security, Architecture, Performance, and Style analysis.

## Domain 1 — Security

### OWASP Top 10 Checklist (2021)

- [ ] A01: Broken Access Control — missing authorization checks, IDOR
- [ ] A02: Cryptographic Failures — plaintext storage, weak hash (MD5/SHA1), hardcoded keys
- [ ] A03: Injection — SQL, XSS, OS Command, LDAP, SSRF
- [ ] A04: Insecure Design — missing rate limiting, absent threat modeling
- [ ] A05: Security Misconfiguration — debug endpoints in production, default credentials
- [ ] A06: Vulnerable and Outdated Components — packages with known CVEs, unpinned dependencies
- [ ] A07: Identification and Authentication Failures — weak session tokens, missing MFA hooks
- [ ] A08: Software and Data Integrity Failures — unverified deserialization, missing SRI
- [ ] A09: Security Logging and Monitoring Failures — no audit trail for auth events
- [ ] A10: Server-Side Request Forgery (SSRF) — unvalidated URL forwarding

### CWE Top 25 — Priority Detection Targets

| CWE | Name | Severity | Workspace Signal |
|-----|------|----------|-----------------|
| CWE-89 | SQL Injection | Critical | String concat in DB queries |
| CWE-78 | OS Command Injection | Critical | shell=True with user-controlled input |
| CWE-798 | Hardcoded Credentials | Critical | Literal passwords/tokens in source |
| CWE-862 | Missing Authorization | Critical | Endpoints without auth middleware |
| CWE-306 | Missing Authentication | Critical | Admin routes without identity check |
| CWE-502 | Unsafe Deserialization | Critical | Permissive YAML/pickle loaders on untrusted input |
| CWE-79 | XSS | High | Raw HTML injection props, unescaped user output |
| CWE-22 | Path Traversal | High | os.path.join(base, user_input) without realpath check |
| CWE-352 | CSRF | High | State-changing endpoints without CSRF token |
| CWE-918 | SSRF | High | Unvalidated URL in HTTP client calls |
| CWE-611 | XXE | High | XML parsing without entity restriction |
| CWE-1321 | Prototype Pollution | High | Recursive merge including __proto__ key |
| CWE-1333 | ReDoS | Medium | Nested quantifiers in user-controlled regex |
| CWE-95 | Code Injection | Critical | Dynamic code evaluation with user-controlled input |

### Language-Specific Vulnerable Patterns and Safe Alternatives

#### Python

__CWE-89 SQL Injection__

- Vulnerable: f-string or % formatting of user_input directly into a SQL query string passed to cursor.execute.
- Safe: Parameterised queries — `cursor.execute("SELECT ... WHERE name = %s", (user_input,))` — or use ORM (SQLAlchemy, Django ORM).

__CWE-78 OS Command Injection__

- Vulnerable: os.system or subprocess with shell=True and a formatted string containing user input.
- Safe: subprocess.run with shell=False, passing arguments as a list — never as a shell string.

__CWE-22 Path Traversal__

- Vulnerable: os.path.join(BASE_DIR, user_input) opened directly without verifying the resolved path stays inside BASE_DIR.
- Safe: os.path.realpath the joined path, then assert it starts with os.path.realpath(BASE_DIR).

__CWE-502 Unsafe Deserialization__

- Vulnerable: Permissive YAML loader (yaml.load without SafeLoader) on untrusted input — allows arbitrary object construction.
- Safe: yaml.safe_load restricts to simple types.

#### JavaScript / TypeScript

__CWE-79 XSS__

- Vulnerable: Setting a raw-HTML injection prop with unescaped user-supplied content; direct innerHTML assignment in vanilla JS.
- Safe: Use React text-node rendering (auto-escaped). When HTML injection is required, sanitise input with DOMPurify before injection.

__CWE-1321 Prototype Pollution__

- Vulnerable: Recursive merge with for...in iteration assigning target[key] = source[key] without filtering — a crafted object with __proto__ key pollutes the base prototype.
- Safe: Iterate with Object.keys() (own keys only); explicitly skip __proto__ and constructor keys before assignment.

__CWE-95 Dynamic Code Evaluation__

- Vulnerable: Any construct that evaluates a user-controlled string as executable code.
- Safe: Replace with data-driven logic — lookup tables, JSON configuration, whitelisted dispatch maps. Never execute arbitrary strings.

#### Java

__CWE-89 SQL Injection__

- Vulnerable: Concatenating userId directly into a SQL string passed to Statement.executeQuery.
- Safe: PreparedStatement with ? placeholders and typed setter methods (ps.setInt, ps.setString).

__CWE-611 XXE__

- Vulnerable: DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(userInput) without disabling external entity resolution.
- Safe: Set disallow-doctype-decl and external-general-entities features on the factory before parsing.

#### Go

__CWE-89 SQL Injection__

- Vulnerable: fmt.Sprintf with user input interpolated into a SQL string, passed to db.Query.
- Safe: db.Query with $1 parameterised placeholder.

__CWE-22 Path Traversal__

- Vulnerable: filepath.Join(baseDir, r.URL.Path) served directly without validating that the resolved path remains inside baseDir.
- Safe: filepath.Clean the path, then strings.HasPrefix(fullPath, baseDir) — reject if outside.

### Docker / Container-Specific Security Patterns

```yaml
# BLOCK: Plaintext credentials in compose env (CWE-798)
# Prohibited — credentials visible via docker inspect
environment:
  DB_PASSWORD: mysecretpassword

# SAFE: Docker Secrets + _FILE convention
environment:
  DB_PASSWORD_FILE: /run/secrets/db_password
secrets:
  - db_password
```

---

## Domain 2 — Architecture (SOLID)

### SOLID Principle Violation Identification

| Principle | Violation Signal | Identification Criteria | Refactoring |
|-----------|-----------------|------------------------|-------------|
| __S — SRP__ | Class name contains "And", "Manager", "Handler" | Multiple reasons to change; imports from DB + HTTP + UI simultaneously | Extract Class, Layer Separation |
| __S — SRP__ | God Class (1000+ lines) | Single class covers multiple domain concerns | Extract Class, Extract Subclass |
| __O — OCP__ | Switch/if modified when adding new types | case blocks added to existing logic | Strategy Pattern, Polymorphism |
| __O — OCP__ | Hardcoded branching | New conditions added for each new type | Plugin/Registry Pattern |
| __L — LSP__ | Child class throws NotImplementedError | Parent contract violated by subtype | Interface Segregation, Composition |
| __L — LSP__ | Type-check before cast | isinstance / type(x) == branching on polymorphic type | Redesign with polymorphism |
| __I — ISP__ | Empty interface implementations | pass, {}, noop for methods that don't apply | Split into Role Interfaces |
| __I — ISP__ | Fat interface (10+ methods) | Implementors forced to stub unrelated methods | Separate by client need |
| __D — DIP__ | Direct concrete class instantiation | ConcreteService() hardcoded in business logic | Dependency Injection |
| __D — DIP__ | Upper module imports lower module | Domain layer directly imports DB/ORM library | Interface/Port abstraction |

### SOLID Checklist

- [ ] __S__ — Each class/module has only one reason to change
- [ ] __S__ — No God Classes exceeding 1000 lines
- [ ] __O__ — New features added without modifying existing code (polymorphism, not switch)
- [ ] __L__ — Subtypes can fully replace parent types without behavioural change
- [ ] __I__ — No fat interfaces forcing empty implementations
- [ ] __D__ — High-level modules depend on abstractions, not concrete implementations

---

## Domain 3 — Performance

### Complexity Thresholds

| Metric | Method/Function | Class/File | Action if Exceeded |
|--------|----------------|-----------|-------------------|
| Lines of Code | <= 20 | <= 300 | Extract Method / Extract Class |
| Cyclomatic Complexity | <= 10 | — | Refactor branching logic |
| Cognitive Complexity | <= 15 | — | Reduce nesting, extract sub-functions |
| Parameter count | <= 4 | — | Introduce Parameter Object |
| Nesting depth | <= 3 levels | — | Early return / Guard clause |
| Dependency count | — | <= 10 | Extract interface layer |

#### Cyclomatic Complexity

Branch points (if / else / switch / for / while / catch) + 1:

| Score | Level | Action |
|-------|-------|--------|
| 1-5 | Low | Appropriate |
| 6-10 | Medium | Review carefully |
| 11-20 | High | Refactoring recommended |
| 21+ | Very High | Refactoring required — WARN |

#### Cognitive Complexity

| Element | Base | Nesting Bonus |
|---------|------|---------------|
| if/else/switch | +1 | +nesting level |
| for/while/do | +1 | +nesting level |
| catch | +1 | +nesting level |
| break/continue to label | +1 | — |
| Logical operator chain | +1 | — |
| Recursive call | +1 | — |

### Performance Anti-Patterns

| Pattern | Detection Signal | Fix Direction |
|---------|-----------------|--------------|
| N+1 Query | DB query inside loop | Batch fetch / JOIN / eager load |
| Unbounded collection | List append in loop with no eviction | Size cap, streaming, pagination |
| Blocking I/O in async context | Synchronous sleep/HTTP in async handler | Async client and non-blocking primitives |
| Repeated identical DB reads | Same query within single request | Request-scoped cache / DataLoader pattern |
| Missing resource cleanup | File/DB connection opened without with/defer | Context manager / defer cleanup |
| Large object in hot path | Deserialising full payload for one field | Stream parsing / field projection |

---

## Domain 4 — Style

### Code Smell to Refactoring Mapping

#### Size-Related Smells

| Code Smell | Symptoms | Refactoring Technique |
|-----------|----------|----------------------|
| __Long Method__ | 20+ lines | Extract Method, Replace Temp with Query |
| __Large Class__ | 300+ lines or 10+ fields | Extract Class, Extract Subclass |
| __Long Parameter List__ | 4+ parameters | Introduce Parameter Object, Builder Pattern |
| __Data Clumps__ | Same field groups repeated across classes | Extract Class |
| __Primitive Obsession__ | Domain concepts represented as raw primitives | Value Object, Enum |

#### Structure-Related Smells

| Code Smell | Symptoms | Refactoring Technique |
|-----------|----------|----------------------|
| __Feature Envy__ | Excessive use of another class's data | Move Method |
| __Data Class__ | Class with only getters/setters, no behaviour | Move behaviour into class |
| __Shotgun Surgery__ | One change forces edits in multiple classes | Move Method/Field, Inline Class |
| __Divergent Change__ | One class changes for multiple unrelated reasons | Extract Class (SRP) |
| __Duplicated Code__ | Identical or near-identical blocks | Extract Method, Template Method |
| __Middle Man__ | Class that only delegates to another | Remove Middle Man, Inline Class |
| __Switch/If Chain__ | Long conditional branching on type | Replace Conditional with Polymorphism, Strategy |
| __Refused Bequest__ | Child class inherits but does not use parent methods | Replace Inheritance with Delegation |
| __Explanatory Comments__ | Complex logic requires comments to be understood | Extract Method to make code self-documenting |

### Language-Specific Style Guide Reference

| Language | Primary Standard | Auto-fix Tool |
|----------|-----------------|--------------|
| Python | PEP 8, Google Python Style | Black, Ruff |
| JavaScript/TypeScript | Airbnb, StandardJS | ESLint, Prettier |
| Java | Google Java Style | google-java-format |
| Go | Effective Go, gofmt | gofmt, golangci-lint |
| Rust | Rust Style Guide | rustfmt, clippy |

---

## Design Pattern Application Guide

### Smell-to-Pattern Mapping

| Problem Situation | Applicable Pattern | Benefit |
|------------------|--------------------|---------|
| Behavioural branching via conditionals on type | __Strategy__ | OCP compliance; new behaviours addable without modifying existing code |
| Complex object creation with many parameters | __Factory Method / Builder__ | Encapsulate creation logic; prevents invalid object state |
| Same algorithm skeleton, different implementation details | __Template Method__ | Remove duplication; isolate change points |
| Behaviour changes based on object state | __State__ | Remove nested conditionals; clarify state transitions |
| Event propagation to multiple subscribers | __Observer__ | Loose coupling between producers and consumers |
| Integrating incompatible interfaces | __Adapter__ | Integrate without modifying existing code |
| Simplifying complex subsystem | __Facade__ | Reduce surface area; lower coupling |
| Dynamically adding features without inheritance | __Decorator__ | Feature composition at runtime |

### Refactoring Priority — Impact / Difficulty Matrix

| | Low Difficulty | High Difficulty |
|--|---------------|----------------|
| __High Impact__ | Do immediately | Plan then execute in dedicated sprint |
| __Low Impact__ | When time allows (backlog) | Defer — low cost-benefit ratio |

### Refactoring Suggestion Format

```text
[Severity] Code Smell: [Smell Name]
Location: [file:line]
Current State: [Problem description]
Refactoring: [Technique name — e.g., Extract Method]
Expected Effect: [How the code improves]
Estimated Difficulty: [Low / Medium / High]
```

---

## Cross-Domain Conflict Resolution

| Conflict | Domain 1 | Domain 2 | Recommended Resolution |
|----------|----------|----------|----------------------|
| Security fix increases latency | Security: add input validation | Performance: hot path overhead | Apply validation; flag latency delta for profiling — security wins |
| DRY refactor introduces indirection | Architecture: remove duplication | Style: readability suffers | Extract only when duplication >= 3 occurrences; document the abstraction |
| Strict type checking slows startup | Architecture: DIP via interfaces | Performance: interface dispatch overhead | Accept overhead; startup cost is one-time; runtime safety wins |
| Logging for audit trail increases I/O | Security: A09 compliance | Performance: synchronous logging | Use async log sink; buffered write — both requirements satisfied |
