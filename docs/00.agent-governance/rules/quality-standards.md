---
layer: agentic
---

# Agent Quality and Security Standards

Universal quality gate for agent-driven changes in this repository.

## 1. Documentation Quality Rubric

| Grade | Description | Requirements |
| :--- | :--- | :--- |
| A | Elite | Accurate routing, valid commands, no policy conflicts, SSoT alignment |
| B | Strong | Mostly aligned with minor omissions |
| C | Functional | Works but has clarity or coverage gaps |
| D | Weak | Multiple stale references or ambiguous guidance |
| F | Failing | Hardcoded secrets, broken governance links, contradictory instructions |

Quality dimensions:

- Actionability: instructions are concrete and testable.
- Conciseness: avoid generic filler.
- Accuracy: references match current repository structure.

## 2. Security Baseline

- Never commit plaintext credentials.
- Prefer secret managers or mounted secret files.
- Keep inter-service networking restricted by intended network boundaries.
- Use least-privilege runtime defaults when modifying infrastructure.

## 3. Reliability Baseline

- Include health checks for long-running services when applicable.
- Keep validation explicit in plans and task evidence.
- Avoid introducing commands that do not exist in this repository.

## 4. Workflow Compliance

- Use JIT routing: bootstrap -> persona -> checklists -> one scope -> stage docs.
- Keep governance docs English-only.
- Keep user-facing communication Korean-first.
- Treat `docs/01` to `docs/99` as read-only unless explicitly approved.

## 5. Verification Checklist

Before completion:

1. Execute applicable checks for changed layers.
2. Confirm changed root/governance files have no broken internal links.
3. Confirm no stale or nonexistent command references remain in editable scope.
4. Confirm documentation reflects current workspace state.
5. Record out-of-scope issues (read-only stages) in `docs/00.agent-governance/memory/`.
