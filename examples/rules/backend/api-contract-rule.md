---
layer: backend
description: "Rule for API contract-first design, versioning, and request validation discipline."
---

# Backend — API Contract Rule

## Case
- **[REQ-API-01]** Define formal contracts before implementation.
- **[REQ-API-02]** Use major-version increments for breaking changes.
- **[REQ-API-04]** Apply semantic HTTP/gRPC/GraphQL conventions.
- **[REQ-API-06]** Validate all inbound payloads at the service boundary.

## Style
- **[REQ-API-05]** Keep status/error semantics consistent and predictable.
- **[PROC-API-01]** Require consumer review for interface-breaking edits.
- **[BAN-API-01]** No silent contract mutation.
- **[BAN-API-02]** No internal stack traces or sensitive internals in public error payloads.

## Validation
- [ ] Active endpoints are represented in authoritative contracts.
- [ ] Validation middleware enforces schema constraints.
- [ ] Versioning policy is respected for breaking changes.
