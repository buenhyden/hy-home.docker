---
trigger: always_on
glob: "**/*.py"
description: "ViewComfy API Standards: Client handling and workflow inference."
---
# ViewComfy API Standards

## 1. Client Setup

- **Credentials**: Client ID and Secret must be loaded from environment variables.
- **Endpoints**: Use the correct base URL for inference (`/infer` or `/infer_with_logs`).

## 2. Workflow Parameters

- **Formatting**: Flatten workflow JSON parameters using the `workflow_parameters_maker` pattern to ensure compatibility.
- **Logs**: Use `infer_with_logs` if you need real-time progress updates via Server-Sent Events (SSE).

### Example: Call

**Good**

```python
result = await client.infer(
    data={"params": json.dumps(parsed_params)},
    files=files
)
```

## 3. Outputs

- **Handling**: Outputs are base64 encoded. Always decode to binary before saving or processing images/files.
