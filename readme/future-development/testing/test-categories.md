# Test Categories

### 1. Model Tests (`test_models.py`)

Tests all Django models and their functionality:

* **User Model**: User creation, role management, authentication
* **InventoryTracking Model**: Inventory item management
* **Item Model**: Individual item status and relationships
* **Building Model**: Building management and staff assignments
* **Room Model**: Room management and occupancy tracking
* **RoomAssignment Model**: Student-room assignments
* **Request Model**: Equipment rental and fault report requests
* **Message Model**: Building announcements and messages

### 2. View Tests (`test_views.py`)

Tests all views and their functionality:

* **Authentication Views**: Login, logout, access control
* **Student Views**: Student-specific pages and functionality
* **Building Manager Views**: Building manager pages and operations
* **Office Manager Views**: Office manager pages and operations
* **Request Views**: Request creation, approval, rejection
* **Inventory Views**: Inventory management operations
* **Role-Based Access**: Permission testing for different user roles
* **Pagination**: Pagination functionality testing

### 3. Form Tests (`test_forms.py`)

Tests form validation and data processing:

* **Request Forms**: Equipment rental and fault report forms
* **Inventory Forms**: Inventory item creation and updates
* **Room Assignment Forms**: Student-room assignment forms
* **Message Forms**: Building announcement forms
* **User Forms**: User creation and management forms
* **Building Forms**: Building management forms
* **Room Forms**: Room management forms

### 4. Integration Tests (`test_integration.py`)

Tests complete workflows and user interactions:

* **Equipment Rental Workflow**: Complete rental process from request to approval
* **Fault Report Workflow**: Complete fault reporting and resolution
* **Inventory Management Workflow**: Complete inventory management process
* **Student Management Workflow**: Student assignment and removal
* **Message Workflow**: Building announcement system
* **Role-Based Access Workflow**: Permission testing across roles
* **Authentication Workflow**: Complete login/logout process
* **Pagination Workflow**: Pagination with multiple items
* **Data Integrity Workflow**: Data consistency across operations

### 5. Utility Tests (`test_utils.py`)

Tests utility functions and management commands:

* **Management Commands**: Custom Django management commands
* **Model Utility Methods**: Model methods and properties
* **Email Utilities**: Email template rendering and context
* **Data Validation**: Input validation utilities
* **Permission Utilities**: Role-based permission checking
* **Search Utilities**: Search and filtering functionality
