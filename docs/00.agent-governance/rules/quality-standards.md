---
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

- Follow the sole load order in `rules/bootstrap.md#3-canonical-load-order`.
- Follow repeatable orchestration in `rules/workflows.md`.
- Apply the document-role language table in
  `rules/documentation-protocol.md#31-language-boundary-by-document-role`.
- Resolve write permission through `rules/approval-boundaries.md`.

## 5. Completion Routing

Use only `rules/task-checklists.md#3-completion-contract`. Its conditional
harness, evidence, documentation, and controlled-gate clauses determine which
quality checks apply. PR-specific completion remains owned by the Completion
Gate in `rules/github-governance.md`.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/agentic.md`
