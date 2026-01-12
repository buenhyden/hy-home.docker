---
trigger: always_on
glob: "**/*.{sh,bash,ps1,zsh}"
description: "Shell Scripting: Standards for Bash and PowerShell automation."
---
# Shell Scripting Standards

## 1. General Principles

- **Shebang**: Always include `#!/bin/bash` or `#!/usr/bin/env pwsh`.
- **Error Handling**: Fail fast.
  - Bash: `set -e` (Exit on error), `set -u` (No unset vars), `set -o pipefail`.
  - PowerShell: `$ErrorActionPreference = "Stop"`.
- **Comments**: Explain *why*, not *what*.

## 2. Bash Best Practices

- **Variables**: Quote variables `"$VAR"` to handle spaces.
- **Functions**: Use functions for code reuse.
- **Naming**: `SCREAMING_SNAKE` for globals/env, `snake_case` for locals.

### Example: Bash

```bash
#!/bin/bash
set -euo pipefail

validate_input() {
  local input="$1"
  if [[ -z "$input" ]]; then
    echo "Error: Input required" >&2
    exit 1
  fi
}

validate_input "$1"
```

## 3. PowerShell Best Practices

- **Cmdlets**: Use `Verb-Noun` naming for functions.
- **Parameters**: Use `param()` block.
- **Output**: Return objects, not text (where possible).

### Example: PowerShell

```powershell
function Get-SystemInfo {
    param(
        [string]$TargetHost = "localhost"
    )
    $ErrorActionPreference = "Stop"
    
    Get-CimInstance -ClassName Win32_OperatingSystem -ComputerName $TargetHost
}
```

## See Also

- [030-core-cli-commands-specific.md](../000-Core/030-core-cli-commands-specific.md) - CLI commands
- [400-infra-general.md](./400-infra-general.md) - Infrastructure General
