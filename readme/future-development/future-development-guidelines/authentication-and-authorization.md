# Authentication & Authorization

#### User Roles

Implemented through Django's built-in User model with custom fields:

```python
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    building = models.ManyToManyField(Building)  # For managers
    room = models.ForeignKey(Room)               # For students
```

#### Permission System

* **Students**: Can view their own data, submit requests/reports
* **Building Managers**: Manage their assigned buildings
* **Office Managers**: Full system access

#### Decorators and Mixins

```python
# Custom decorators for role-based access
@role_required('student')
@role_required('building_manager')  
@role_required('office_manager')
```
