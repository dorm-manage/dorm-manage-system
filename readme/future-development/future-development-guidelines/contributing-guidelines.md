# Contributing Guidelines

#### Code Style

* Follow PEP 8 for Python code
* Use meaningful variable and function names
* Add docstrings for complex functions
* Comment non-obvious code sections

#### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add: your feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

**Transaction Management**

Use transactions for complex operations:

```python
from django.db import transaction

@transaction.atomic
def handle_add_student(request, managed_buildings):
    # Create user
    user = User.objects.create_user(...)
    
    # Create room assignment  
    assignment = RoomAssignment.objects.create(...)
    
    # If any operation fails, all will be rolled back
```

**Database Migrations**

```bash
# Create migration after model changes
python manage.py makemigrations 

# Check migration SQL before applying
python manage.py sqlmigrate DormitoriesPlus 0001

# Apply migrations
python manage.py migrate

# Reset migrations (development only)
python manage.py migrate DormitoriesPlus zero
rm DormitoriesPlus/migrations/0*.py
python manage.py makemigrations DormitoriesPlus
```

#### Adding New Features

When adding new functionality to the DormitoriesPlus system:

**1. Model Changes**

```python
# Update models.py and create migrations
python manage.py makemigrations

# Review the migration before applying
python manage.py sqlmigrate DormitoriesPlus migration_number

# Apply migrations
python manage.py migrate
```

**2. API Endpoints**

Follow the existing pattern in `api_views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class NewFeatureAPIView(APIView):
    def get(self, request):
        # Handle GET requests
        return Response({'data': 'your_data'})
    
    def post(self, request):
        # Handle POST requests
        return Response({'status': 'success'})
```

**3. View Functions**

Add new views in `views.py` following the role-based pattern:

```python
@login_required
@role_required(['office_staff'])  # or appropriate roles
def new_feature_view(request):
    pass
    return render(request, 'template.html', context)
```

**4. URL Routing**

Update URL patterns appropriately:

```python
# In DormitoriesPlus/urls.py
urlpatterns = [
    path('new-feature/', views.new_feature_view, name='new_feature'),
    path('api/new-feature/', api_views.NewFeatureAPIView.as_view(), name='api_new_feature'),
]
```

**5. Templates**

Create templates following the existing structure:

```html
<!-- templates/role_pages/feature.html -->
{% extends 'base.html' %}
{% block content %}
<!-- Your content here -->
{% endblock %}
```

**6. Static Files**

Add CSS/JS following the modular approach:

```css
/* static/css/feature.css */
.feature-specific-styles {
    /* Your styles */
}
```

**7. Testing**

Write tests for new functionality:

```python
# DormitoriesPlus/tests/test_new_feature.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class NewFeatureTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass',
            role='student'
        )
    
    def test_new_feature(self):
        # Your test logic
        pass
```

#### Performance Considerations

* Implement pagination for large datasets
* Optimize image uploads and storage
* Monitor database query performance

#### Security Best Practices

* Validate all user inputs
* Use Django's built-in security features
* Implement proper authentication checks
* Sanitize file uploads
* Use HTTPS in production
