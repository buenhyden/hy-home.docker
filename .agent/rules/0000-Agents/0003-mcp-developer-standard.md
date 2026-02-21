---
trigger: model_decision
glob: ["**/*"]
description: "MCP Developer Agent Standards: Enforces Model Context Protocol compliance, type-safe tool/resource schemas, and rigorous Inspector-based verification."
---

# MCP Developer Agent Standards

- **Role**: MCP Implementation Architect
- **Purpose**: Define standards for the design, development, and verification of Model Context Protocol (MCP) servers to ensure secure and seamless tool integration for LLMs.
- **Activates When**: The user requests the creation of new MCP servers, implementation of protocol tools/resources, or debugging of JSON-RPC transport issues.

**Trigger**: model_decision — Apply during all phases of MCP server development and protocol integration.

## 1. Standards

### Principles

- **[REQ-MCE-01] Protocol-First Fidelity**
  - Every MCP implementation MUST strictly adhere to the official Model Context Protocol specification for Tools, Resources, and Prompts.
- **[REQ-MCE-02] Immutable Type Safety**
  - Every Tool and Resource input/output MUST be governed by a strict, non-ambiguous schema (Zod for TypeScript, Pydantic for Python).
- **[REQ-MCE-03] Mandatory Protocol Observability**
  - MCP servers MUST implement structured logging of protocol events (JSON-RPC requests/responses) to `stderr` for non-destructive debugging.

### Integration Baseline

| Component | Requirement ID | Critical Standard |
| --- | --- | --- |
| Schema | [REQ-MCE-04] | Zod / Pydantic (No `any`) |
| Transport | [REQ-MCE-05] | Stdio (CLI/Local) or SSE (Remote/Web) |
| Lifecycle | [REQ-MCE-06] | Explicit `connect` and `shutdown` handling |
| Error | [REQ-MCE-07] | Standard JSON-RPC error codes |

### Must

- **[REQ-MCE-08] Verified Inspector Boot**
  - All new or modified MCP servers MUST be successfully verified using the official MCP Inspector before being considered "Ready".
- **[REQ-MCE-09] Explicit Capability Declaration**
  - The server initialization MUST explicitly declare its capabilities (e.g., Tools: true, Resources: false) as per the client-server handshake.
- **[REQ-MCE-10] Non-Blocking Handlers**
  - Tool handlers MUST be implemented as asynchronous functions to prevent blocking the single-threaded JSON-RPC transport loop.

### Must Not

- **[BAN-MCE-01] Stdout Pollution in Stdio**
  - NEVER write non-protocol data (logs, prints) to `stdout` when using Stdio transport; doing so corrupts the JSON-RPC channel.
- **[BAN-MCE-02] Opaque Error Responses**
  - Do NOT return generic "Internal Error" messages; return specific error data that helps the LLM identify the failure cause.

### Failure Handling

- **Stop Condition**: Stop development if the server fails to initialize in the MCP Inspector or if a tool schema identifies as incompatible with LLM parsing.

## 2. Procedures

- **[PROC-MCE-01] Protocol Verification Cycle**
  - IF a tool is added/modified THEN MUST run `npx @modelcontextprotocol/inspector <command>` and execute the tool manually to verify schema alignment.
- **[PROC-MCE-02] Transport Hardening**
  - For SSE transports, verify that the application correctly handles connection timeouts and reconnections according to the protocol spec.

## 3. Examples

### Clean Tool Definition (Good)

```typescript
{
  name: "get_data",
  description: "Fetches structured data",
  inputSchema: z.object({ id: z.string() })
}
```

## 4. Validation Criteria

- **[VAL-MCE-01] Inspector Pass Rate**
  - [ ] audit confirms that the server initializes and lists all features in the Inspector without errors.
- **[VAL-MCE-02] Schema Compliance**
  - [ ] audit confirms that 100% of tools utilize strict, typed schemas without `any`.
- **[VAL-MCE-03] Logging Integrity**
  - [ ] verification confirms that zero non-protocol data is emitted to `stdout` during active operation.
