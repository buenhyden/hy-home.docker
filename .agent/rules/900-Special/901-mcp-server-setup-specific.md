---
trigger: always_on
glob: "**/*.{json,sh,js,ts}"
description: "MCP Server Setup & Debugging: Configuration for Peekaboo, Inspector, and other MCP tools."
---
# MCP Server Standards

## 1. Installation Principles

- **No New Apps**: Do not recommend installing new apps (Claude Code, Cursor) if the user is already properly set up.
- **Environment**: Use `~/.zshrc` or `.env` for API keys (`OPENAI_API_KEY`, `GITHUB_TOKEN`). NEVER hardcode.
- **Global vs Local**: Prefer project-local `npx` execution for reproducibility, but support global `claude mcp add` for user convenience.

## 2. Server Configurations

### Peekaboo (Screenshots & Vision)

- **Command**: `npx -y @steipete/peekaboo-mcp`
- **Env Vars**:
  - `PEEKABOO_AI_PROVIDERS`: `openai/gpt-4o` or `ollama/llava:latest`.
  - `OPENAI_API_KEY`: Must be set.
- **Key Extraction**: Use `grep` to pull keys from shell config rather than asking user to paste them.

### Context7 (Docs)

- **Command**: `npx -y @upstash/context7-mcp`
- **Usage**: Use for fetching up-to-date documentation for libraries.

### MCP Inspector (Debugging)

- **Purpose**: Debug MCP servers using a web UI.
- **Start**: `npx @modelcontextprotocol/inspector ./start.sh`
- **Output**: Check `stderr` for server startup errors.

## 3. Configuration Files

- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor**: `~/.cursor/mcp.json`
- **VS Code**: `~/Library/Application Support/Code/User/settings.json`

## 4. Debugging

- **Logs**: Read logs using `tail -n 100 <log_file>`.
- **Connectivity**: Verify proxy ports (default `6274` for Inspector).
- **Permissions**: Ensure screen recording permissions if using visual tools like Peekaboo.

## 5. Automation Check (Peekaboo)

### Peekaboo Config

```json
"peekaboo": {
  "command": "npx",
  "args": ["-y", "@steipete/peekaboo-mcp"],
  "env": { "PEEKABOO_AI_PROVIDERS": "openai/gpt-4o", "OPENAI_API_KEY": "..." }
}
```

## 6. Debugging with Inspector

1. **Start**: `npx @modelcontextprotocol/inspector ./start.sh`
2. **Connect**: Use Playwright/Browser to `localhost:3000`.
3. **Logs**: Monitor `stderr`.
