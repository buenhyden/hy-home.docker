# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Use `rtk` as the shell-command proxy only when it is available on `PATH`.
If `rtk` is not installed or not visible in the active sandbox, run the command
directly and note that RTK filtering was unavailable when relevant.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
which rtk
rtk --version
rtk gain
```
