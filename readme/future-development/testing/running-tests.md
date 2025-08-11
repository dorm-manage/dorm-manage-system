# Running Tests

### Using Django's test runner

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test DormitoriesPlus.tests.test_models

# Run specific test class
python manage.py test DormitoriesPlus.tests.test_models.UserModelTest

# Run specific test method
python manage.py test DormitoriesPlus.tests.test_models.UserModelTest.test_create_user
```

### Using pytest (recommended)

```bash
# Install pytest dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest DormitoriesPlus/tests/test_models.py

# Run specific test class
pytest DormitoriesPlus/tests/test_models.py::UserModelTest

# Run specific test method
pytest DormitoriesPlus/tests/test_models.py::UserModelTest::test_create_user

# Run tests with coverage
pytest --cov=DormitoriesPlus --cov-report=html

# Run tests by marker
pytest -m models
pytest -m views
pytest -m integration
```

### Using the custom test runner

```bash
# Run all tests with custom runner
python run_tests.py
```
