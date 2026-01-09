---
trigger: always_on
glob: "**/*"
description: "MCP (Model Context Protocol): Server Setup, Resources, Tools, and Integration."
---
# MCP Standards

## 1. Server Architecture

- **Purpose**: MCP servers expose resources and tools to AI agents.
- **Transport**: Use stdio for local, SSE for remote servers.
- **Registry**: Register servers in Claude/Cursor settings.

### Example: Server Setup

**Good**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

## 2. Resources

- **Definition**: Resources are read-only data sources (files, DB, APIs).
- **URI**: Use descriptive URIs (`file:///path`, `db://table`).
- **Caching**: Cache expensive resource reads.

### Example: Resource

**Good**

```typescript
server.resources.add({
  uri: "config://app-settings",
  name: "Application Settings",
  description: "Current app configuration",
  read: async () => JSON.stringify(config),
});
```

## 3. Tools

- **Definition**: Tools are actions agents can invoke.
- **Validation**: Use Zod/JSON Schema for input validation.
- **Error Handling**: Return structured errors.

### Example: Tool

**Good**

```typescript
server.tools.add({
  name: "search_documents",
  description: "Search internal documents",
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => searchDocs(query),
});
```

## 4. Security

- **Permissions**: Grant minimal permissions to servers.
- **Sandboxing**: Run untrusted servers in isolated environments.
- **Audit**: Log all tool invocations.
