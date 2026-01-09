---
trigger: always_on
glob: "**/*.py"
description: "Tornado: Non-blocking Web Server Best Practices."
---
# Tornado Framework Standards

## 1. Async Patterns

- **Native Async**: Prefer `async def` and `await` over the legacy `@gen.coroutine`.
- **Non-blocking**: Similar to other async frameworks, ensure all I/O is non-blocking.

### Example: Async Handlers

**Good**

```python
class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("http://friendfeed-api.com/v2/feed/bret")
        self.write(response.body)
```

**Bad**

```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Blocking call
        response = requests.get("http://friendfeed-api.com/v2/feed/bret")
        self.write(response.content)
```

## 2. Structure

- **Application Object**: Subclass `tornado.web.Application` to hold global state (db connections, etc.).
- **URL Routing**: Keep routing tables clean and separated if large.

## 3. Key Considerations

- **Single Threaded**: Remember Tornado is single-threaded. CPU-intensive tasks block the loop. Offload them to `ProcessPoolExecutor`.
- **Security**: Enable XSRF protection (`xsrf_cookies=True`) in settings unless strictly an API.

## 4. Error Handling

- **write_error**: Override `write_error` in your `RequestHandler` base class to format JSON error responses globally.
