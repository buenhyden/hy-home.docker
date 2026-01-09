---
trigger: always_on
glob: "**/*.py"
description: "Python Asyncio: Coroutines, Tasks, Event Loop, and Concurrency."
---
# Python Asyncio Standards

## 1. Async/Await Basics

- **async def**: Mark coroutine functions with `async def`.
- **await**: Always await coroutines; never call them directly.

### Example: Coroutines

**Good**

```python
async def fetch_data() -> str:
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
```

**Bad**

```python
async def fetch_data():
    return "data"

result = fetch_data()  # Returns coroutine object, not "data"!
```

## 2. Concurrency with Tasks

- **asyncio.gather**: Run multiple coroutines concurrently.
- **asyncio.create_task**: Create tasks for fire-and-forget.
- **Timeouts**: Use `asyncio.wait_for()` for timeout handling.

### Example: Gather

**Good**

```python
async def main():
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
```

**Bad**

```python
async def main():
    user1 = await fetch_user(1)
    user2 = await fetch_user(2)  # Sequential, not concurrent!
    user3 = await fetch_user(3)
```

## 3. Event Loop

- **asyncio.run()**: Use in `if __name__ == "__main__"` block.
- **No get_event_loop()**: Avoid deprecated `asyncio.get_event_loop()`.

### Example: Entry Point

**Good**

```python
if __name__ == "__main__":
    asyncio.run(main())
```

## 4. Error Handling

- **try/except**: Wrap awaited calls in try/except.
- **TaskGroup**: Use `asyncio.TaskGroup` (Python 3.11+) for structured concurrency.
