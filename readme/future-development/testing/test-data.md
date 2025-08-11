# Test Data

### Base Test Cases

The test suite includes base test cases that set up common test data:

* **BaseTestCase**: Common setup for all tests
* **BaseFormTestCase**: Setup for form tests
* **BaseUtilityTestCase**: Setup for utility tests
* **CompleteWorkflowTest**: Setup for integration tests

### Test Users

The tests create users with different roles:

* Students (`student@example.com`)
* Building Staff (`staff@example.com`)
* Office Staff (`office@example.com`)

### Test Data

Each test creates its own test data including:

* Buildings and rooms
* Inventory items
* Equipment items
* Room assignments
* Requests (equipment rental and fault reports)
* Messages
