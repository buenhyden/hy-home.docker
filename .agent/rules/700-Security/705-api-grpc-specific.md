---
trigger: always_on
glob: "**/*.proto"
description: "gRPC: Protobuf design, Streaming, and Error handling."
---
# gRPC Standards

## 1. Protobuf Design

- **Style**: Google Style Guide (2-space indent, CamelCase messages, snake_case fields).
- **Compatibility**: Never renumber tags. Mark deleted fields as `reserved`.

### Example: Reserved

**Good**

```protobuf
message User {
  reserved 2, 5;
  reserved "email";
  string username = 1;
  string display_name = 3;
}
```

**Bad**

```protobuf
message User {
  string username = 1;
  string phone = 2; // Reused tag 2! Breaks compatibility
}
```

## 2. Streaming Patterns

- **Server Streaming**: Large result sets (e.g., file downloads, logs).
- **Client Streaming**: Uploads, batch writes.
- **Bidirectional**: Real-time chat, collaborative editing.

### Example: Streaming

**Good**

```protobuf
rpc ListLogs(ListLogsRequest) returns (stream LogEntry);
```

**Bad**

```protobuf
rpc ListLogs(ListLogsRequest) returns (LogEntries); // 1GB response in memory
```

## 3. Errors

- **Status**: Use `google.rpc.Status` for rich errors.
- **Codes**: Map App errors to Standard codes (`NOT_FOUND`, `INVALID_ARGUMENT`).

## 4. Deadlines

- **Always Set**: Clients MUST set deadlines. Servers should respect them.
