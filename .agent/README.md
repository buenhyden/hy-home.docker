# .agent Directory

This directory contains AI agent configuration for the project.

## Structure

```
.agent/
├── README.md        # This file
├── rules/           # Coding standards and guidelines
└── workflows/       # Executable workflow definitions
```

---

## Rules

Located in `rules/`, organized by domain:

| Category | Files | Focus |
|----------|-------|-------|
| **000-Core** | 25 | Clean code, Git, naming, debugging |
| **100-Frontend** | 31 | React, Vue, Svelte, CSS, state management |
| **200-Backend** | 38 | Python, Node, Go, Rust, Java, ORMs |
| **300-Data_AI** | 43 | Pandas, PyTorch, LangChain, DBs |
| **400-Infrastructure** | 19 | Docker, K8s, Terraform, CI/CD |
| **500-Mobile** | 5 | Android, iOS, React Native, Flutter |
| **600-Testing** | 13 | Pytest, Jest, Playwright, load testing |
| **700-Security** | 24 | OWASP, auth, injection, secrets |
| **800-Documentation** | 8 | README, MkDocs, technical writing |
| **900-Special** | 14 | Chrome extensions, scraping, Electron |

---

## Workflows

Located in `workflows/`. Invoke via `/workflow-name`.

| Workflow | Description |
|----------|-------------|
| `/workflow-project-setup` | Project context & understanding |
| `/workflow-bug-fix` | Repro → Test → Fix → Verify |
| `/workflow-git-commit` | Diff → Conventional Commit |
| `/workflow-feature-component` | Structure → Scaffold → Implement → Test |
| `/workflow-pr-review` | Requirements → Standards → Security → Feedback |
| `/workflow-release` | Version → Changelog → Tag → Deploy |
| `/workflow-api-design` | Resource → Methods → Versioning → Errors |
| `/workflow-testing` | Pyramid → AAA → Mocking → Coverage |
| `/workflow-security-audit` | Secrets → Deps → Code Analysis → Report |
| `/workflow-performance-optimization` | Measure → Hypothesize → Optimize → Verify |
| `/workflow-docs-update` | Content → Links → Timestamp |
| `/workflow-data-pipeline` | EDA → Clean → Feature → Model → Validate |

---

## Usage

- **Rules** are automatically loaded as context for AI agents.
- **Workflows** are triggered via slash commands (e.g., `/workflow-bug-fix`).
