# Views and URLs

#### URL Structure

The application uses role-based URL routing:

```python
# Root patterns (DormitoriesPlus_project/urls.py)
/                           # Homepage (redirects based on role)
/login/                     # Login page  
/logout/                    # Logout
/student/                   # Student dashboard and features
/bm/                        # Building Manager dashboard and features
/om/                        # Office Manager dashboard and features
/api/                       # REST API endpoints
```

#### View Architecture

**Authentication & Authorization**

All views use a custom `@role_required` decorator:

```python
@role_required(['student'])           # Student-only access
@role_required(['building_staff'])    # Building Manager access  
@role_required(['office_staff'])      # Office Manager access
@role_required(['building_staff', 'office_staff'])  # Manager access
```

**Student Views (`@role_required(['student'])`)**

* **`Students_homepage`**: Dashboard with loan/fault summaries, pagination
* **`application`**: Equipment loan request form with validation
* **`faults`**: Fault reporting form with urgency levels

**Building Manager Views (`@role_required(['building_staff'])`)**

* **`BM_Homepage`**: Dashboard with building statistics and alerts
* **`BM_inventory`**: CRUD operations for inventory items
* **`BM_loan_requests`**: Approve/reject loan requests, mark returns
* **`BM_faults`**: Manage fault reports, update status/comments
* **`BM_manage_students`**: Add/remove students in managed buildings

**Office Manager Views (`@role_required(['office_staff'])`)**

* **`OM_Homepage`**: System-wide statistics and overview
* **`OM_inventory`**: Global inventory management
* **`OM_loan_requests`**: Manage all loan requests with filtering
* **`OM_faults`**: Handle all fault reports with advanced filters
* **`OM_manage_students`**: Student management across all buildings
* **`OM_manage_BM`**: Building manager assignment and management

#### Key View Features

**Pagination**

Most list views include pagination:

```python
# Example from Students_homepage
pending_paginator = Paginator(pending_loan_requests, 5)
pending_page_number = request.GET.get('pending_page')
pending_page_obj = pending_paginator.get_page(pending_page_number)
```

**Filtering & Search**

Office Manager views include filtering:

```python
# Example from OM_loan_requests
building_filter = request.GET.get('building')
date_from_filter = request.GET.get('date_from')
overdue_filter = request.GET.get('overdue')

if building_filter:
    requests_list = requests_list.filter(room__building_id=building_filter)
```

**Form Handling**

Views handle both GET (display) and POST (form submission):

```python
if request.method == 'POST':
    action = request.POST.get('action')
    if action == 'approve':
        # Handle approval logic
    elif action == 'reject':
        # Handle rejection logic
```

**Database Optimization**

Views use `select_related()` and `prefetch_related()` for efficient queries:

```python
requests = Request.objects.filter(
    status='pending'
).select_related('user', 'item', 'room', 'room__building').order_by('-created_at')
```
