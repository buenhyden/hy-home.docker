---
trigger: always
glob: ["**/*mcp*/**/*"]
description: "MCP Server Standards: Polyglot standards (TS, Python, Java) for Model Context Protocol servers, covering tools, resources, and transport isolation."
---

# MCP Server Standards

- **Role**: AI Systems & MCP Architect
- **Purpose**: Define standards for building high-fidelity, secure, and polyglot Model Context Protocol (MCP) servers that expose specialized tools and data to LLMs.
- **Activates When**: Initializing new MCP servers, defining context resources, or implementing LLM-accessible tools.

**Trigger**: always — Apply during the development and orchestration of MCP-based infrastructure.

## 1. Standards

### Principles

- **[REQ-MCP-01] Atomic Tool Responsibility**
  - MCP tools MUST be atomic, idempotent, and specialized. A single tool SHOULD perform one logical operation to minimize LLM confusion.
- **[REQ-MCP-02] Transport Isolation (Stdio)**
  - For Stdio transport, servers MUST isolate the JSON-RPC channel. All logs and non-protocol output MUST be routed to `stderr` to prevent channel corruption.
- **[REQ-MCP-03] Strict Schema Validation**
  - Every tool input MUST be governed by a strict schema (Zod for TS, Pydantic for Python, JsonSchema for Java) with descriptive field metadata.

### Lifecycle Matrix

| Strategy | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| TypeScript | [REQ-MCP-04] | `@modelcontextprotocol/sdk` (ESM) |
| Python | [REQ-MCP-05] | `FastMCP` with strict type hints |
| Java | [REQ-MCP-06] | Spring AI / Project Reactor (Async) |
| Validation | [REQ-MCP-07] | Descriptive Docstrings / JSDoc |

### Must

- **[REQ-MCP-08] Informative Error Returns**
  - Tools MUST return descriptive error messages in the `content` block (`isError: true`) rather than throwing exceptions that crash the server process.
- **[REQ-MCP-09] Explicit Version Identity**
  - Every MCP server MUST declare a clear name and semantic version in its initialization metadata for traceability.
- **[REQ-MCP-10] Standardized Folder Layout**
  - Servers MUST organize logic into `tools/`, `resources/`, and `prompts/` directories to maintain ecosystem consistency.

### Must Not

- **[BAN-MCP-01] Stdout Logging**
  - NEVER write logs, status messages, or any non-RPC data to `stdout` when using the Stdio transport.
- **[BAN-MCP-02] Unchecked Input Parsing**
  - Do NOT trust LLM-generated inputs; always validate types, ranges, and mandatory fields before execution.

### Failure Handling

- **Stop Condition**: Stop server execution if a JSON-RPC communication error is identified in the transport layer or if a tool schema fails to compile.

## 2. Procedures

- **[PROC-MCP-01] Inspector Verification**
  - IF a tool is modified THEN MUST verify its behavior using the MCP Inspector before deploying to a production agent environment.
- **[PROC-MCP-02] Resource Quota Review**
  - Regularly audit dynamic resource generators to ensure they do not exceed the context window limits of the target LLMs.

## 3. Examples

### compliant Python Tool (Good)

```python
@mcp.tool()
def get_user(id: int) -> str:
    """Fetch user summary by ID.
    Args:
        id: Unique user identifier.
    """
    return f"User {id}"
```

## 4. Validation Criteria

- **[VAL-MCP-01] Inspector Integrity Pass**
  - [ ] MCP Inspector confirms that all tools are correctly registered and return expected JSON structures.
- **[VAL-MCP-02] Error Resilience**
  - [ ] Verification confirms that passing "invalid" arguments returns a descriptive `isError: true` response without a process crash.
- **[VAL-MCP-03] Logging Directionality**
  - [ ] Audit confirms that 100% of log output is correctly routed to `stderr`.
