---
trigger: always_on
glob: "**/*.py"
description: "Flask: Blueprints, Application Factory, and Extensions."
---
# Flask Standards

## 1. Architecture

- **App Factory**: Use `create_app()` pattern. Never use a global `app` object.
- **Blueprints**: Register routes via Blueprints, not directly on app.

### Example: Factory

**Good**

```python
def create_app(config):
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    return app
```

**Bad**

```python
app = Flask(__name__)
@app.route("/") # Global state makes testing hard
def index(): ...
```

## 2. Contexts

- **Proxy**: Be careful with `g`, `request`, `current_app`.
- **Local Proxy**: Avoid passing `request` deeper into services. Extract data in the View function and pass explicit arguments.

### Example: Explicit Args

**Good**

```python
@bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    return user_service.create(data['name'])
```

**Bad**

```python
# In Service Layer
def create():
    data = request.json # Service coupled to HTTP layer
    ...
```
