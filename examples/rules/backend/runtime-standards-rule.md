---
layer: backend
description: "Rule for backend runtime behavior, reliability posture, and service-level quality."
---

# Backend — Runtime Standards Rule

## Case
- **[REQ-BE-01]** Keep backend behavior deterministic and observable.
- **[REQ-NODE-01]** Apply framework/runtime-safe defaults for service execution.
- **[REQ-PY-01]** Preserve typed validation and explicit error paths in Python services.
- **[REQ-GO-01]** Maintain clear context handling and cancellation discipline in Go services.

## Style
- **[PROC-NODE-01]** Follow standardized startup, config, and shutdown patterns.
- **[PROC-PY-01]** Use explicit validation and exception handling boundaries.
- **[BAN-NODE-01]** Avoid unbounded runtime side effects.
- **[BAN-PY-01]** Avoid implicit dynamic behavior that hides failures.

## Validation
- [ ] Service runtime contracts are explicit and testable.
- [ ] Error handling behavior is consistent across language runtimes.
- [ ] Observability signals exist for critical runtime paths.
