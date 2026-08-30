---
profile_id: governance-policy
layer: agentic
---

# Agent Quality and Security Standards

Universal quality gate for agent-driven changes in this repository.

## 1. Documentation Quality Rubric

| Grade | Description | Requirements                                                           |
| :---- | :---------- | :--------------------------------------------------------------------- |
| A     | Elite       | Accurate routing, valid commands, no policy conflicts, SSoT alignment  |
| B     | Strong      | Mostly aligned with minor omissions                                    |
| C     | Functional  | Works but has clarity or coverage gaps                                 |
| D     | Weak        | Multiple stale references or ambiguous guidance                        |
| F     | Failing     | Hardcoded secrets, broken governance links, contradictory instructions |

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
- Maintain a strict minimum of 90% unit test coverage for domain logic.
- Mark the 90% target N/A only for docs-only, policy-only, infrastructure configuration, or validation-script changes where no domain-code coverage signal applies.
- Bug fixes require regression evidence; refactors require behavior-preserving validation evidence.
- Agent-loop changes require deterministic fixture and mutation coverage for
  routing, retired-role rejection, boundary escalation, hook denial, bounded
  retry, completion evidence, adapter rendering, model fallback, and
  calibration.

## 4. Workflow and Language Routing

- Follow the sole load order in `policies/bootstrap.md#canonical-load-order`.
- Follow repeatable orchestration in `policies/workflows.md`.
- Apply the document-role language table in
  `policies/documentation-protocol.md#authoring-rules`.
- Resolve write permission through `policies/approval-boundaries.md`.

## 5. Completion Routing

Use only `policies/task-checklists.md#before-completion`. Its conditional
harness, evidence, documentation, and controlled-gate clauses determine which
quality checks apply. PR-specific completion remains owned by the Completion
Gate in `policies/github-governance.md`.

## Related Documents

- `docs/00.agent-governance/policies/github-governance.md`
- `docs/00.agent-governance/policies/git-workflow.md`
- `docs/00.agent-governance/policies/agentic.md`
