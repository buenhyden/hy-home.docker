---
trigger: always_on
glob: "**/*.py"
description: "Trio: Structured Concurrency for Python Best Practices."
---
# Trio Framework Standards

## 1. Structured Concurrency

- **Nurseries**: Always use nurseries (`async with trio.open_nursery() as nursery:`) to manage concurrent tasks. This ensures tasks are properly cleaned up and errors are propagated.
- **No Floating Tasks**: Avoid spawning tasks that escape the scope of their parent (`fire-and-forget` without a nursery).

### Example: Nurseries

**Good**

```python
async with trio.open_nursery() as nursery:
    nursery.start_soon(my_task, 1)
    nursery.start_soon(my_task, 2)
# Both tasks finish before this block exits
```

**Bad**

```python
# asyncio style create_task without context management (in Trio context)
# Trio forces structure, making "bad" patterns harder, but avoid avoiding nurseries.
```

## 2. Error Handling

- **MultiError**: Be prepared to handle `trio.MultiError` since multiple concurrent tasks can fail simultaneously.
- **Cancellation/Checkpoints**: Respect checkpoints. Trio functions check for cancellation at `await` points.

## 3. Libraries

- **Trio-Compatible**: Use libraries designed for Trio (e.g., `httpx` with trio backend, `trio-postgres`) to ensure the event loop is not blocked.

## 4. Testing

- **pytest-trio**: Use the `pytest-trio` plugin and `@pytest.mark.trio` for robust async testing.
