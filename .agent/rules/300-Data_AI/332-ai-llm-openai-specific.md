---
trigger: always_on
glob: "**/*.py,**/*.js"
description: "OpenAI/LLM: Prompt Engineering, Token Management, and Cost Control."
---
# OpenAI & LLM Standards

## 1. API Usage & Architecture

- **Client**: Initialize one client instance (Singleton). Use `AsyncOpenAI` for web services.
- **Retries**: Handle `RateLimitError` (429) and `APIError` (5xx) with exponential backoff (e.g., `tenacity` library in Python).
- **Timeouts**: Always set a timeout. LLM calls can hang.

### Example: Resilience

**Good**

```python
@retry(wait=wait_exponential(multiplier=1, min=2, max=10))
async def get_completion(prompt):
    return await client.chat.completions.create(...)
```

**Bad**

```python
# No retry logic. Fails immediately on transient network blip.
client.chat.completions.create(...)
```

## 2. Prompt Engineering

- **Separation**: Use `system` role for instructions and `user` role for data.
- **Structured Output**: Use JSON mode (`response_format={ "type": "json_object" }`) or tools/function calling for machine-readable output.
- **Context Window**: Truncate or summarize history to stay within token limits.

## 3. Cost & Observability

- **Token Counting**: Log input/output token usage for every request to track cost per user.
- **Tracing**: Trace the full chain (Prompt -> LLM -> Tool -> Response) using tools like LangSmith or custom logging.
- **Caching**: Cache identical prompts (with temperature=0) to save money.
