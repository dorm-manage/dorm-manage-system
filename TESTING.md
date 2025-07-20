# Testing Documentation for DormitoriesPlus

This document provides comprehensive information about the testing setup for the DormitoriesPlus dorm management system.

## Overview

The testing suite includes:
- **Model Tests**: Test all Django models and their relationships
- **View Tests**: Test all views and their functionality
- **Form Tests**: Test form validation and data processing
- **Integration Tests**: Test complete workflows and user interactions
- **Utility Tests**: Test utility functions and management commands

## Test Structure

```
DormitoriesPlus/tests/
├── __init__.py
├── test_models.py      # Model tests
├── test_views.py       # View tests
├── test_forms.py       # Form tests
├── test_utils.py       # Utility tests
└── test_integration.py # Integration tests
```

## Running Tests

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

## Test Categories

### 1. Model Tests (`test_models.py`)

Tests all Django models and their functionality:

- **User Model**: User creation, role management, authentication
- **InventoryTracking Model**: Inventory item management
- **Item Model**: Individual item status and relationships
- **Building Model**: Building management and staff assignments
- **Room Model**: Room management and occupancy tracking
- **RoomAssignment Model**: Student-room assignments
- **Request Model**: Equipment rental and fault report requests
- **Message Model**: Building announcements and messages

### 2. View Tests (`test_views.py`)

Tests all views and their functionality:

- **Authentication Views**: Login, logout, access control
- **Student Views**: Student-specific pages and functionality
- **Building Manager Views**: Building manager pages and operations
- **Office Manager Views**: Office manager pages and operations
- **Request Views**: Request creation, approval, rejection
- **Inventory Views**: Inventory management operations
- **Role-Based Access**: Permission testing for different user roles
- **Pagination**: Pagination functionality testing

### 3. Form Tests (`test_forms.py`)

Tests form validation and data processing:

- **Request Forms**: Equipment rental and fault report forms
- **Inventory Forms**: Inventory item creation and updates
- **Room Assignment Forms**: Student-room assignment forms
- **Message Forms**: Building announcement forms
- **User Forms**: User creation and management forms
- **Building Forms**: Building management forms
- **Room Forms**: Room management forms

### 4. Integration Tests (`test_integration.py`)

Tests complete workflows and user interactions:

- **Equipment Rental Workflow**: Complete rental process from request to approval
- **Fault Report Workflow**: Complete fault reporting and resolution
- **Inventory Management Workflow**: Complete inventory management process
- **Student Management Workflow**: Student assignment and removal
- **Message Workflow**: Building announcement system
- **Role-Based Access Workflow**: Permission testing across roles
- **Authentication Workflow**: Complete login/logout process
- **Pagination Workflow**: Pagination with multiple items
- **Data Integrity Workflow**: Data consistency across operations

### 5. Utility Tests (`test_utils.py`)

Tests utility functions and management commands:

- **Management Commands**: Custom Django management commands
- **Model Utility Methods**: Model methods and properties
- **Email Utilities**: Email template rendering and context
- **Data Validation**: Input validation utilities
- **Permission Utilities**: Role-based permission checking
- **Search Utilities**: Search and filtering functionality

## Test Configuration

### Test Settings (`DormitoriesPlus_project/test_settings.py`)

The test settings include:
- In-memory SQLite database for fast testing
- Disabled password hashing for faster tests
- Console email backend for testing
- Disabled logging during tests
- Simplified middleware for testing

### Coverage Configuration

The project is configured to require 80% code coverage. Coverage reports are generated in HTML format and can be viewed in the `htmlcov/` directory.

## Test Data

### Base Test Cases

The test suite includes base test cases that set up common test data:

- **BaseTestCase**: Common setup for all tests
- **BaseFormTestCase**: Setup for form tests
- **BaseUtilityTestCase**: Setup for utility tests
- **CompleteWorkflowTest**: Setup for integration tests

### Test Users

The tests create users with different roles:
- Students (`student@example.com`)
- Building Staff (`staff@example.com`)
- Office Staff (`office@example.com`)

### Test Data

Each test creates its own test data including:
- Buildings and rooms
- Inventory items
- Equipment items
- Room assignments
- Requests (equipment rental and fault reports)
- Messages

## Best Practices

### Writing Tests

1. **Test Naming**: Use descriptive test method names
2. **Test Isolation**: Each test should be independent
3. **Test Data**: Create fresh test data for each test
4. **Assertions**: Use specific assertions for better error messages
5. **Documentation**: Include docstrings for test classes and methods

### Test Organization

1. **Group Related Tests**: Organize tests by functionality
2. **Use Base Classes**: Extend base test cases for common setup
3. **Test One Thing**: Each test should test one specific behavior
4. **Clean Up**: Use `setUp` and `tearDown` methods appropriately

### Running Tests

1. **Run Tests Frequently**: Run tests after each change
2. **Check Coverage**: Ensure new code is covered by tests
3. **Fix Failures**: Address test failures immediately
4. **Update Tests**: Update tests when functionality changes

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=DormitoriesPlus --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Troubleshooting

### Common Issues

1. **Database Errors**: Ensure test database is properly configured
2. **Import Errors**: Check that all required packages are installed
3. **Permission Errors**: Ensure test user has proper permissions
4. **Template Errors**: Check that all templates exist and are accessible

### Debugging Tests

1. **Use `pdb`**: Add `import pdb; pdb.set_trace()` for debugging
2. **Check Logs**: Review test output for error messages
3. **Isolate Tests**: Run individual tests to identify issues
4. **Check Dependencies**: Ensure all required packages are installed

## Contributing

When adding new features:

1. **Write Tests First**: Follow TDD principles
2. **Update Test Documentation**: Document new test cases
3. **Maintain Coverage**: Ensure new code is covered by tests
4. **Run Full Suite**: Run all tests before submitting changes

## Coverage Reports

After running tests with coverage, view the HTML report:

```bash
# Generate coverage report
pytest --cov=DormitoriesPlus --cov-report=html

# Open coverage report
open htmlcov/index.html
```

The coverage report shows:
- Overall coverage percentage
- Line-by-line coverage details
- Missing coverage areas
- Branch coverage information 