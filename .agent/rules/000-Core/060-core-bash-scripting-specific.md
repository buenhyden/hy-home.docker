---
trigger: always_on
glob: "**/*.sh"
description: "Bash Scripting: Strict error handling, safe quoting, and modular structure."
---
# Bash Scripting Standards

## 1. Safety First (The "Unofficial" Bash Strict Mode)

Start every script with:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

- `-e`: Exit on error.
- `-u`: Exit on unset variables.
- `-o pipefail`: Fail pipeline if any command fails.

## 2. Quoting

- **Rule**: Double quote ALL variable expansions `"${VAR}"` to prevent globbing and word splitting.
- **Exception**: `[[ ]]` tests (though quoting is still good practice).

## 3. Structure

- **Shebang**: `#!/usr/bin/env bash` (Portability).
- **Functions**: Encapsulate logic in functions. Use `main` function.
- **Variables**: Use `local` for function variables. `readonly` for constants.
- **Naming**: `UPPER_CASE` for constants, `snake_case` for lower variables/functions.

## 4. Anti-Patterns

- **`eval`**: Avoid `eval`. It is a security risk.
- **`$(ls)`**: Don't parse `ls` output. Use globs `for f in *.txt`.
- **Backticks**: Use `$()` instead of `` `command` ``.

### Example: Robust Script

#### Good

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly BACKUP_DIR="/tmp/backup"

log() {
    local msg="${1}"
    echo "[INFO] ${msg}"
}

main() {
    local file="${1:-}"
    if [[ -z "${file}" ]]; then
        echo "Usage: ${0} <file>" >&2
        exit 1
    fi
    
    log "Processing ${file}..."
}

main "$@"
```
