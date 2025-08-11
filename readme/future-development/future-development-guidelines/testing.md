# Testing

#### Test Structure

```
DormitoriesPlus/tests/
├── test_models.py        # Model tests
├── test_views.py         # View tests
├── test_forms.py         # Form validation tests
├── test_utils.py         # Utility function tests
└── test_integration.py   # Integration tests
```

#### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test DormitoriesPlus.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

#### Test Configurations

* **Test settings**: `test_settings.py`
* **Test database**: In-memory SQLite for speed
* **Docker testing**: `docker-compose.test.yml`
