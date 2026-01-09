---
trigger: always_on
glob: "**/*.{sh,bash,zsh}"
description: "Shell scripting standards (Bash/Zsh): Safety, Portability, and Style."
---
# Shell Scripting Standards

## 1. Safety & Robustness

- **Shebang**: Use `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`.
- **Strict Mode**: Start every script with:

  ```bash
  set -euo pipefail
  # Zsh specific: setopt errreturn nounset pipefail
  ```

- **Quoting**: ALWAYS quote variables (`"${VAR}"`).

## 2. Variables & Naming

- **Naming**: `UPPER_SNAKE_CASE` for exported, `lower_snake_case` for locals.
- **Scope**: Use `local` keyword inside functions.

## 3. Zsh Specifics

- **Arrays**: SQL-style indexing (1-based). Use `"${(@)array}"` to preserve empty elements.
- **Globbing**: Enable `setopt extended_glob` for advanced matching.
- **Efficiency**: Use internal parameter expansion (`${var:h}`, `${var:t}`) over `dirname`/`basename`.

## 4. Best Practices

- **Conditions**: Use `[[ ... ]]` over `[ ... ]`.
- **Formatting**: Indent with 2 spaces.
- **Linting**: Use `shellcheck` (works for Bash, and mostly for Zsh).
