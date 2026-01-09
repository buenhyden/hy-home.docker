---
trigger: always_on
glob: "**/*.py"
description: "Django & DRF: Architecture, ORM Optimization, and Testing."
---
# Django Standards

## 1. Architecture Application

- **Domain Separation**: One Django app per bounded context (`users`, `billing`).
- **Fat Models, Thin Views**: Encapsulate business logic in Models or Services, never in Views/Serializers.
- **Settings**: Split into `base.py`, `dev.py`, `prod.py` (using `django-environ` or `pydantic-settings`).

## 2. ORM Optimization (N+1)

- **Select Related**: Use `select_related()` for ForeignKey (1-to-1/Many).
- **Prefetch Related**: Use `prefetch_related()` for Many-to-Many.
- **Indexing**: All fields used in `filter()`, `order_by()`, or `distinct()` must be indexed.

### Example: N+1

**Good**

```python
# Fetches Books AND Authors in 1 query
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)
```

**Bad**

```python
# 1 query for Books + N queries for Authors
books = Book.objects.all()
for book in books:
    print(book.author.name)
```

## 3. Django REST Framework (DRF)

- **ViewSets**: Use `ModelViewSet` for standard CRUD resources to reduce boilerplate.
- **Serializers**: Explicitly define `fields = [...]`. Never use `fields = '__all__'` in public APIs.

### Example: Serializers

**Good**

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

**Bad**

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # Exposes password/admin flags
```

## 4. Async & Testing

- **Async (4.2+)**: Use `aget` / `acreate` for async views.
- **Testing**: Use `pytest-django`. Mark DB tests with `@pytest.mark.django_db`.
