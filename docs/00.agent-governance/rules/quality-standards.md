---
layer: agentic
---

# Agent Quality and Security Standards

Universal quality gate for agent-driven changes in this repository.

## 1. Documentation Quality Rubric

| Grade | Description | Requirements |
| :--- | :--- | :--- |
| **A** | Elite | Accurate routing, valid commands, no policy conflicts, SSoT alignment |
| **B** | Strong | Mostly aligned with minor omissions |
| **C** | Functional | Works but contains clarity or coverage gaps |
| **D** | Weak | Multiple stale references or ambiguous guidance |
| **F** | Failing | Hardcoded secrets, broken governance links, or contradictory instructions |

Quality dimensions:

- Actionability: instructions are concrete and testable.
- Conciseness: avoid generic filler.
- Accuracy: references match real repository structure.

## 2. Security Baseline

- Never commit plaintext credentials.
- Prefer secret managers or mounted secret files.
- Keep inter-service networking restricted by intended network boundaries.
- Use least-privilege runtime defaults when modifying infrastructure.

## 3. Reliability and Performance Baseline

- Include health checks for long-running services when applicable.
- Keep service-level validation explicit in plans and task evidence.
- Avoid introducing commands that do not exist in this repository.

## 4. Workflow Compliance

- Use JIT routing: bootstrap -> persona -> one scope -> needed stage docs.
- Keep governance files English-only.
- Keep user-facing communication Korean-first.

## 5. Verification Checklist

Before completion:

1. Run relevant checks for changed layers.
2. Confirm no stale links or nonexistent command references remain.
3. Validate that modified guidance reflects repository reality.
