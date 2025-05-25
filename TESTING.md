# Testing Documentation for DormitoriesPlus

This document provides information about the test suite for the DormitoriesPlus application.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have pytest and pytest-django installed:
```bash
pip install pytest pytest-django
```

## Running Tests

To run all tests:
```bash
pytest
```

For verbose output:
```bash
pytest -v
```

To run specific test classes:
```bash
pytest DormitoriesPlus/tests.py::TestUserModel
pytest DormitoriesPlus/tests.py::TestBuildingModel
pytest DormitoriesPlus/tests.py::TestRoomModel
pytest DormitoriesPlus/tests.py::TestRequestModel
pytest DormitoriesPlus/tests.py::TestRoomAssignmentModel
```

## Test Coverage

The test suite covers the following areas:

### 1. User Model Tests (`TestUserModel`)
- Creating student users
- Creating staff users
- Creating superusers
- Verifying user roles and permissions

### 2. Building Model Tests (`TestBuildingModel`)
- Creating buildings
- Assigning building staff members
- Verifying building-staff relationships

### 3. Room Model Tests (`TestRoomModel`)
- Creating rooms
- Setting room capacity
- Testing unique constraints for room numbers
- Verifying room-building relationships

### 4. Request Model Tests (`TestRequestModel`)
- Creating equipment rental requests
- Testing request status management
- Verifying due date calculations
- Testing overdue status

### 5. Room Assignment Tests (`TestRoomAssignmentModel`)
- Creating room assignments
- Testing assignment dates
- Verifying user-room relationships

## Test Structure

Each test class is decorated with `@pytest.mark.django_db` to handle database transactions properly. The tests use temporary test databases that are created and destroyed for each test session.

## Writing New Tests

To add new tests:

1. Create a new test class or add methods to existing classes in `DormitoriesPlus/tests.py`
2. Use the `@pytest.mark.django_db` decorator for database access
3. Follow the existing pattern of creating test data and making assertions

Example:
```python
@pytest.mark.django_db
class TestNewFeature:
    def test_something(self):
        # Create test data
        # Make assertions
        assert something == expected_value
```

## Best Practices

1. Each test should be independent and not rely on other tests
2. Use meaningful test names that describe what is being tested
3. Create fresh test data for each test
4. Clean up any resources created during tests
5. Test both positive and negative scenarios

## Common Issues

If you encounter issues:

1. Make sure all dependencies are installed
2. Check that the database settings are correct
3. Verify that the test database can be created
4. Ensure you're in the correct directory when running tests

## Contributing

When adding new features, please:
1. Write corresponding tests
2. Ensure all existing tests pass
3. Update this documentation if necessary 