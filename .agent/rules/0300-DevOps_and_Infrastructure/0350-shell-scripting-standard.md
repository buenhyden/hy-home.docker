---
trigger: always
glob: ["**/*.{sh,bash,ps1,zsh}"]
description: "Shell Scripting Standards: Enforces 'fail-fast' logic, robust error handling, and cross-platform automation patterns."
---

# Shell Scripting Standards

- **Role**: Automation & Scripting Specialist
- **Purpose**: Define standards for writing safe, maintainable, and robust automation scripts using Bash, PowerShell, or Zsh.
- **Activates When**: Writing system automation scripts, CI/CD pipeline steps, or developer utility tools.

**Trigger**: always — Apply during the development and maintenance of all shell-based scripts.

## 1. Standards

### Principles

- **[REQ-SHL-01] Fail-Fast Execution**
  - Scripts MUST terminate immediately upon encountering an error to prevent cascading failures. (Bash: `set -e`, PowerShell: `$ErrorActionPreference = "Stop"`).
- **[REQ-SHL-02] Explicit State Declaration**
  - Avoid relying on global environmental state; explicitly define required variables and paths at the script's initialization.
- **[REQ-SHL-03] Robust Input Validation**
  - All script parameters and environment variables MUST be validated for presence and format before core logic execution.

### Shell Stack Baseline

| Language | Requirement ID | Mandatory Flag / Pattern |
| --- | --- | --- |
| Bash | [REQ-SHL-04] | `set -euo pipefail` |
| PowerShell | [REQ-SHL-05] | `param()` block and strict mode |
| Shebang | [REQ-SHL-06] | Fixed shebang (e.g., `#!/bin/bash`) |
| Formatting | [REQ-SHL-07] | `shfmt` / `ShellCheck` compliance |

### Must

- **[REQ-SHL-08] Mandatory Quoting**
  - In Bash, always quote variables (e.g., `"$VAR"`) to prevent word splitting and globbing issues.
- **[REQ-SHL-09] Explicit Error Propagation**
  - Functions MUST return non-zero exit codes upon failure. Utilize `stderr` for logging error messages.
- **[REQ-SHL-10] Atomic Utility Usage**
  - Prefer small, targeted utility scripts over monolithic automation files for better testability and reuse.

### Must Not

- **[BAN-SHL-01] Silent Failure Adoption**
  - Do NOT ignore the exit codes of primary commands (e.g., `cp`, `mv`, `rm`) unless explicitly handled via a conditional check.
- **[BAN-SHL-02] Global Namespace Pollution**
  - In complex scripts, utilize `local` variables within functions to prevent unintentional shadowing of global states.

### Failure Handling

- **Stop Condition**: Stop script execution if `ShellCheck` identifies a "Critical" or "Error" level violation in the script logic.

## 2. Procedures

- **[PROC-SHL-01] Pre-Flight Linter Scan**
  - IF committing a `.sh` file THEN MUST run `shellcheck` to identify potential syntax and logic flaws.
- **[PROC-SHL-02] Cross-Platform Verification**
  - IF a script is intended for multi-environment use THEN MUST verify compatibility across the project's target OS baselines.

## 3. Examples

### Safe Bash Template (Good)

```bash
#!/bin/bash
set -euo pipefail
main() {
  local target="$1"
  [[ -d "$target" ]] || { echo "Error: Missing dir" >&2; exit 1; }
}
main "$@"
```

## 4. Validation Criteria

- **[VAL-SHL-01] ShellCheck Purity**
  - [ ] Automated scan confirms zero "Error" or "Warning" level findings in all project scripts.
- **[VAL-SHL-02] Exit Behavior**
  - [ ] Manual test confirms that the script correctly terminates and returns code `1` when a prerequisite dependency is missing.
- **[VAL-SHL-03] Idempotency Pass**
  - [ ] Execution logs confirm that running the script twice on the same target does not cause unintended side effects.
