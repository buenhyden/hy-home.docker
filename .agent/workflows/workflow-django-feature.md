---
description: Workflow for Django Feature Development
---

1. **Model Design**

    Define data models in `[app]/models.py`.

    ```python
    from django.db import models

    class Feature(models.Model):
        name = models.CharField(max_length=100)
        is_active = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name
    ```

2. **Apply Migrations**

    Update database schema.

    // turbo

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Admin Registration**

    Register models for easy management.

    ```python
    # [app]/admin.py
    from django.contrib import admin
    from .models import Feature

    @admin.register(Feature)
    class FeatureAdmin(admin.ModelAdmin):
        list_display = ('name', 'is_active', 'created_at')
    ```

4. **Create Views**

    Implement logic in `[app]/views.py`.

    ```python
    from django.views.generic import ListView
    from .models import Feature

    class FeatureList(ListView):
        model = Feature
        template_name = 'feature_list.html'
    ```

5. **Configure URLs**

    Map URLs to views in `[app]/urls.py`.

    ```python
    from django.urls import path
    from .views import FeatureList

    urlpatterns = [
        path('features/', FeatureList.as_view(), name='feature-list'),
    ]
    ```

6. **Tests**

    Verify functionality.

    ```python
    # [app]/tests.py
    from django.test import TestCase
    from django.urls import reverse

    class FeatureTests(TestCase):
        def test_list_view(self):
            response = self.client.get(reverse('feature-list'))
            self.assertEqual(response.status_code, 200)
    ```

// turbo
7. **Run Tests**

    Execute test suite.

    ```bash
    python manage.py test
    ```
