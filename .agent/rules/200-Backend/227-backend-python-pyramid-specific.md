---
trigger: always_on
glob: "**/*.py"
description: "Pyramid: Web Framework Best Practices."
---
# Pyramid Standards

## 1. Configuration

- **Include Mechanism**: Use `config.include()` to modularize app setup (routes, views, models). Avoid monolithic `__init__.py`.
- **Scan**: Use `config.scan()` to pick up declarative configuration (view decorators).

## 2. Views

- **Predicates**: Use view predicates (`request_method='POST'`, `xhr=True`) in `@view_config` to dispatch logic, rather than big `if/else` blocks inside a single view.
- **Renderers**: Perfer `renderer='json'` for APIs.

### Example: View Config

**Good**

```python
@view_config(route_name='users', request_method='GET', renderer='json')
def get_users(request):
    return {"users": []}
```

## 3. Transaction Management

- **pyramid_tm**: Use `pyramid_tm` middleware to handle transaction commit/rollback automatically based on request success/failure. Do not manually commit sessions in views.
