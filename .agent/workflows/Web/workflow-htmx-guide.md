---
description: Build hypermedia-driven web applications with HTMX and backend frameworks
---

1. **Setup project structure**

    Create project with HTMX + backend framework.

    **Recommended stacks:**

    - Go + Fiber/Echo + HTMX
    - Python + Django/FastAPI + HTMX
    - Node.js + Express + HTMX

    Create structure:

    ```bash
    mkdir htmx-app
    cd htmx-app

    # Backend structure
    mkdir -p {templates,static/{css,js},handlers}
    ```

2. **Install HTMX**

    Add HTMX to your project.

    **CDN (quickstart):**
    Create `templates/base.html`:

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>HTMX App</title>
      <script src="https://unpkg.com/htmx.org@1.9.10"></script>
      <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
      {% block content %}{% endblock %}
    </body>
    </html>
    ```

    **NPM (for build process):**

    ```bash
    npm install htmx.org
    ```

3. **Create basic HTMX interactions**

    Implement common HTMX patterns.

    **Click to load:**

    ```html
    <button
      hx-get="/api/data"
      hx-target="#result"
      hx-swap="innerHTML"
    >
      Load Data
    </button>

    <div id="result">
      <!-- Data will appear here -->
    </div>
    ```

    **Form submission (AJAX):**

    ```html
    <form
      hx-post="/api/users"
      hx-target="#user-list"
      hx-swap="beforeend"
    >
      <input type="text" name="name" placeholder="Name" required>
      <input type="email" name="email" placeholder="Email" required>
      <button type="submit">Add User</button>
    </form>

    <ul id="user-list">
      <!-- Users will be added here -->
    </ul>
    ```

    **Search with debounce:**

    ```html
    <input
      type="search"
      name="q"
      hx-get="/search"
      hx-trigger="keyup changed delay:500ms"
      hx-target="#search-results"
      placeholder="Search..."
    >

    <div id="search-results"></div>
    ```

4. **Implement backend endpoints**

    Create server endpoints that return HTML fragments.

    **Go + Fiber example:**

    ```go
    package main

    import (
     "github.com/gofiber/fiber/v2"
     "github.com/gofiber/template/html/v2"
    )

    func main() {
     engine := html.New("./templates", ".html")
     app := fiber.New(fiber.Config{
      Views: engine,
     })

     app.Static("/static", "./static")

     // Return HTML fragment
     app.Get("/api/data", func(c *fiber.Ctx) error {
      return c.SendString(`
       <div class="data-item">
        <h3>New Data</h3>
        <p>Loaded via HTMX</p>
       </div>
      `)
     })

     // Form submission
     app.Post("/api/users", func(c *fiber.Ctx) error {
      name := c.FormValue("name")
      email := c.FormValue("email")

      return c.SendString(fmt.Sprintf`
       <li>
        <strong>%s</strong> - %s
       </li>
      `, name, email))
     })

     app.Listen(":3000")
    }
    ```

    **Python + FastAPI example:**

    ```python
    from fastapi import FastAPI, Form
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")

    @app.get("/api/data", response_class=HTMLResponse)
    async def get_data():
        return """
        <div class="data-item">
            <h3>New Data</h3>
            <p>Loaded via HTMX</p>
        </div>
        """

    @app.post("/api/users", response_class=HTMLResponse)
    async def create_user(name: str = Form(...), email: str = Form(...)):
        return f"""
        <li>
            <strong>{name}</strong> - {email}
        </li>
        """
    ```

5. **Add loading indicators**

    Show feedback during requests.

    **Using hx-indicator:**

    ```html
    <button
      hx-get="/slow-endpoint"
      hx-target="#result"
      hx-indicator="#spinner"
    >
      Load Data
    </button>

    <div id="spinner" class="htmx-indicator">
      <span class="spinner"></span> Loading...
    </div>

    <div id="result"></div>
    ```

    **CSS for indicator:**

    ```css
    .htmx-indicator {
      display: none;
    }

    .htmx-request .htmx-indicator,
    .htmx-request.htmx-indicator {
      display: inline-block;
    }

    .spinner {
      border: 2px solid #f3f3f3;
      border-top: 2px solid #3498db;
      border-radius: 50%;
      width: 16px;
      height: 16px;
      animation: spin 1s linear infinite;
      display: inline-block;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    ```

6. **Implement infinite scroll**

    Load more content on scroll.

    ```html
    <div id="content">
      <!-- Initial items -->
      <div class="item">Item 1</div>
      <div class="item">Item 2</div>

      <!-- Load more trigger -->
      <div
        hx-get="/api/items?page=2"
        hx-trigger="revealed"
        hx-swap="afterend"
      >
        <span class="htmx-indicator">Loading more...</span>
      </div>
    </div>
    ```

    **Backend (pagination):**

    ```python
    @app.get("/api/items")
    async def get_items(page: int = 1):
        items = fetch_items(page=page, per_page=10)

        html = ""
        for item in items:
            html += f'<div class="item">{item.name}</div>\n'

        # Add next page trigger if more items exist
        if has_more_pages(page):
            html += f'''
            <div
              hx-get="/api/items?page={page + 1}"
              hx-trigger="revealed"
              hx-swap="afterend"
            >
              <span class="htmx-indicator">Loading more...</span>
            </div>
            '''

        return HTMLResponse(html)
    ```

7. **Add optimistic UI updates**

    Update UI immediately, then sync with server.

    ```html
    <button
      hx-post="/api/like"
      hx-swap="outerHTML"
      hx-vals='{"postId": "123"}'
    >
      ❤️ Like (10)
    </button>
    ```

    **Backend response:**

    ```html
    <button
      hx-post="/api/like"
      hx-swap="outerHTML"
      hx-vals='{"postId": "123"}'
    >
      ❤️ Liked (11)
    </button>
    ```

8. **Implement delete with confirmation**

    Add confirm dialog before destructive actions.

    ```html
    <button
      hx-delete="/api/users/123"
      hx-confirm="Are you sure you want to delete this user?"
      hx-target="closest tr"
      hx-swap="outerHTML swap:1s"
    >
      Delete
    </button>
    ```

    **Backend (Go):**

    ```go
    app.Delete("/api/users/:id", func(c *fiber.Ctx) error {
     id := c.Params("id")
     // Delete user from database
     deleteUser(id)

     // Return empty to remove element
     return c.SendString("")
    })
    ```

9. **Add WebSocket support (optional)**

    Real-time updates with HTMX WebSocket extension.

    **Include extension:**

    ```html
    <script src="https://unpkg.com/htmx.org/dist/ext/ws.js"></script>
    ```

    **WebSocket connection:**

    ```html
    <div hx-ext="ws" ws-connect="/ws">
      <div id="notifications">
        <!-- Real-time notifications appear here -->
      </div>
    </div>
    ```

    **Backend (Go + WebSocket):**

    ```go
    app.Get("/ws", websocket.New(func(c *websocket.Conn) {
     for {
      // Send HTML fragments
      c.WriteMessage(websocket.TextMessage, []byte(`
       <div hx-swap-oob="beforeend:#notifications">
        <div class="notification">New message!</div>
       </div>
      `))
      time.Sleep(5 * time.Second)
     }
    }))
    ```

10. **Add CSS transitions**

    Smooth animations for HTMX swaps.

    ```css
    /* Fade in new content */
    .htmx-swapping {
      opacity: 0;
      transition: opacity 200ms ease-in;
    }

    /* Slide in from right */
    [hx-swap*="fromright"] {
      animation: slideInRight 300ms ease-out;
    }

    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    /* Fade out removed elements */
    .htmx-swapping {
      opacity: 0;
      transition: opacity 200ms ease-out;
    }
    ```

11. **Handle errors gracefully**

    Show user-friendly error messages.

    **Error handling attribute:**

    ```html
    <form
      hx-post="/api/users"
      hx-target="#user-list"
      hx-on::after-request="handleResponse(event)"
    >
      <!-- Form fields -->
    </form>

    <script>
    function handleResponse(event) {
      if (event.detail.xhr.status >= 400) {
        alert('Error:  ' + event.detail.xhr.responseText);
      }
    }
    </script>
    ```

    **Backend error response:**

    ```python
    from fastapi import HTTPException

    @app.post("/api/users")
    async def create_user(name: str = Form(...)):
        if not name:
            return HTMLResponse(
                "<div class='error'>Name is required</div>",
                status_code=400
            )
        # Create user...
    ```

12. **Deploy HTMX application**

    Deploy to production.

    **Docker (Go app):**

    ```dockerfile
    FROM golang:1.21-alpine AS builder
    WORKDIR /app
    COPY . .
    RUN go build -o main .

    FROM alpine:latest
    WORKDIR /app
    COPY --from=builder /app/main .
    COPY templates templates/
    COPY static static/
    EXPOSE 3000
    CMD ["./main"]
    ```

    **Build and run:**

    ```bash
    docker build -t htmx-app .
    docker run -p 3000:3000 htmx-app
    ```

    **Deploy to:**

    - Fly.io
    - Railway
    - Heroku
    - DigitalOcean App Platform
