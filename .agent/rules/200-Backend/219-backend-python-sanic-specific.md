---
trigger: always_on
glob: "**/*.py"
description: "Sanic: Async High Performance Web Framework Best Practices."
---
# Sanic Framework Standards

## 1. Code Organization

- **Blueprints**: Always use Blueprints to organize routes by feature or domain.
- **Factory Pattern**: Use `create_app()` factory pattern for better testing and configuration.

### Example: Blueprints

**Good**

```python
# routes/user.py
from sanic import Blueprint
user_bp = Blueprint('user', url_prefix='/users')

@user_bp.route('/')
async def get_users(request):
    ...

# main.py
app.blueprint(user_bp)
```

**Bad**

```python
# Putting all routes in main.py
@app.route('/users')
async def get_users(request):
    ...
```

## 2. Async Performance

- **Non-blocking I/O**: Never perform blocking operations (DB calls, Requests) inside async handlers. Use `aiohttp` or async drivers.
- **Gather**: Use `asyncio.gather` for concurrent independent tasks.

### Example: Non-blocking

**Good**

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
        return await resp.json()
```

**Bad**

```python
import requests
# Blocks the Event Loop!
resp = requests.get(url)
```

## 3. Configuration

- **Environment Variables**: Use `app.config` loaded from environment variables (e.g., using `python-dotenv` or built-in config loaders).
- **Workers**: Run with multiple workers in production (`fastapi run` equivalent or `gunicorn` with worker class).

## 4. Error Handling

- **Centralized Handling**: Use `@app.exception` to handle errors globally and return consistent JSON responses.
