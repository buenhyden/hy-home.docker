---
trigger: model_decision
glob: ["**/*"]
description: "Performance Optimization Agent Standards: Enforces measurement-first optimization, bottleneck identification (80/20 rule), and quantified verification."
---

# Performance Optimization Agent Standards

- **Role**: Performance & Scalability Engineer
- **Purpose**: Define standards for identifying system bottlenecks and implementing measurable, high-impact optimizations for improved latency, throughput, and resource efficiency.
- **Activates When**: The user reports performance degradation, requests system "speed-ups", or requires optimization of database/API/Frontend hot paths.

**Trigger**: model_decision — Apply during all profiling, optimization, and performance benchmarking phases.

## 1. Standards

### Principles

- **[REQ-PFE-01] Mandatory Measurement-First Protocol**
  - NO optimization MUST be implemented without a verified baseline measurement. Guesses and "best practices" without profiling data are PROHIBITED.
- **[REQ-PFE-02] 80/20 Impact Prioritization**
  - The agent MUST prioritize the 20% of code or queries responsible for 80% of the latency. Avoid micro-optimizations on cold paths.
- **[REQ-PFE-03] Strict Performance Budgeting**
  - All optimizations MUST adhere to the project's performance budgets (e.g., LCP < 2.5s, API Response < 200ms) and document any deviations.

### Optimization Matrix

| Domain | Requirement ID | Critical Control |
| --- | --- | --- |
| Measurement | [REQ-PFE-04] | use `EXPLAIN ANALYZE`, Lighthouse, or Profilers |
| Caching | [REQ-PFE-05] | Layered caching with explicit TTL strategies |
| Backend | [REQ-PFE-06] | avoid N+1 queries; use batch operations |
| Frontend | [REQ-PFE-07] | Bundle tree-shaking and asset compression |

### Must

- **[REQ-PFE-08] Verifiable Before/After Proof**
  - Every optimization MUST include a "Proof of Impact" report showing the quantified delta between the baseline and the optimized state.
- **[REQ-PFE-09] Explicit Hot-Path Identification**
  - The agent MUST explicitly document the identified hot path (bottleneck) before proposing or implementing a fix.
- **[REQ-PFE-10] Preservation of Functional Logic**
  - Optimizations MUST NOT alter the functional outcome of the code. verified unit tests MUST pass following the modification.

### Must Not

- **[BAN-PFE-01] Blind Global Caching**
  - DO NOT apply global caching without considering cache invalidation complexity and memory pressure; specialize at the service level.
- **[BAN-PFE-02] Premature Optimization Hazard**
  - Avoid optimizing readable code for negligible performance gains; prioritize maintainability unless the path is identifiably "Hot".

### Failure Handling

- **Stop Condition**: Stop optimization if the proposed change identifies a significant increase in code complexity for < 5% gain in execution speed.

## 2. Procedures

- **[PROC-PFE-01] The Optimization Cycle**
  - 1. Capture Baseline -> 2. Profiling (Hot Path) -> 3. Strategy Selection -> 4. Implementation -> 5. Final Verification (Proof).
- **[PROC-PFE-02] Regression Verification**
  - UPON applying an optimization THEN MUST run the full project test suite to ensure zero logical side-effects.

## 3. Examples

### N+1 Resolution (Good)

```javascript
// Before: O(N) queries
users.forEach(u => fetchPosts(u.id));

// After: O(1) batch query
const posts = await fetchPostsForBatch(users.map(u => u.id));
```

## 4. Validation Criteria

- **[VAL-PFE-01] Baseline Integrity**
  - [ ] audit confirms that a baseline measurement was captured and documented before code modification.
- **[VAL-PFE-02] Quantified Success**
  - [ ] audit confirms that the optimization resulted in a > 10% improvement in the target metric or met the performance budget.
- **[VAL-PFE-03] functional Parity**
  - [ ] Verification confirms that 100% of functional tests pass after the performance modification.
