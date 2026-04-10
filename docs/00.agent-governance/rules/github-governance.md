---
layer: agentic
---

# GitHub Governance Policy

Normative policy baseline aligning agent behavior with GitHub repository operations.
Repo-local stricter rules always override this document; never weaken them on the basis of this policy.

## 1. Repository Protection Contract

- Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks.
- Branch protection is enforced via GitHub rulesets. Agents reading or reviewing workflow files must assume ruleset enforcement is active unless explicitly told otherwise.
- Required status checks must pass before any PR is considered ready to merge. Agents must not declare "done" until required checks are green.
- CODEOWNERS-triggered reviews are mandatory. If a changed path is owned by a CODEOWNERS entry, that review must be obtained before merge — agents must note this requirement when completing PR review tasks.

## 2. Pull Request and Review Contract

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved BLOCK-severity findings remain.
- Agents must not self-approve or bypass required reviewers.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Merge method discipline: prefer squash or rebase to keep `main` history linear unless the project explicitly allows merge commits.

## 3. Merge and Branch Discipline

- Feature branches must be deleted after merge.
- Long-lived branches other than `main` require explicit user authorization.
- Rebase onto `main` before requesting merge if the branch diverges by more than a trivial number of commits.
- Agents must never modify another agent's in-progress branch without explicit coordination.

## 4. GitHub Actions Security Contract

- Workflows must use least-privilege `GITHUB_TOKEN` — request only the permissions the job actually needs.
- Prefer OIDC-based cloud credentials over long-lived secrets stored as repository secrets. When proposing or reviewing workflow changes, flag any use of long-lived cloud secrets as a WARN finding.
- Pin actions to a specific commit SHA or a digest-verified tag, not a floating branch or `@latest`.
- Secrets must never appear in log output (`echo $SECRET`, `run: env`, etc.). Flag any such pattern as BLOCK.
- Untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT`, or `run:` interpolation is a security injection risk — flag as BLOCK.
- Reusable workflows called from external repositories must be pinned and reviewed before use.

## 5. AI Instruction Hierarchy and Copilot Compatibility

- GitHub Copilot repository instructions (`.github/copilot-instructions.md` or path-level files) are advisory inputs.
- When Copilot-style instructions conflict with this repository's governance, the stricter repo-local rule wins.
- Agents must not silently adopt Copilot instructions that contradict `docs/00.agent-governance/` policy.
- If a Copilot instruction supplements rather than conflicts with local governance, it may be followed.
- Root shim files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) remain the primary entry points; Copilot instruction files do not replace them.

## 6. Completion Gate (GitHub-Specific)

Before an agent declares any PR-related task complete, it must confirm:

1. All required status checks are green (or note which are pending and why).
2. All required reviews are approved (or note which are outstanding and who owns them).
3. No BLOCK-severity findings remain from code review or security audit.
4. CODEOWNERS-triggered reviewers have been notified if paths are owned.
5. No secrets, long-lived credentials, or unpinned action references were introduced.

If any gate is unmet, the task status is "blocked" not "done."

## Related Documents

- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/memory/progress.md`

## References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
- <https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions>
