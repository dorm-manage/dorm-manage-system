# Models

The system uses several key models (refer to `DormitoriesPlus/models.py`):

#### Core Models

**User Model**

Extended Django `AbstractUser` with custom role-based functionality:

```python
class User(AbstractUser):
    STUDENT = 'student'
    BUILDING_STAFF = 'building_staff' 
    OFFICE_STAFF = 'office_staff'
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    email = models.EmailField(unique=True)  # Used as USERNAME_FIELD
```

**Building & Room Models**

```python
class Building(models.Model):
    building_name = models.CharField(max_length=255)
    building_staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=1)
    # Unique together: building + room_number

class RoomAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)  # Null = indefinite
```

**Inventory Models**

```python
class InventoryTracking(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    photo_url = models.ImageField(upload_to='inventory_photos/', null=True, blank=True)
    # item type

class Item(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('borrowed', 'Borrowed')]
    inventory = models.ForeignKey(InventoryTracking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # pysical item represntion
```

**Request Model**

Unified model for both equipment loans and fault reports:

```python
class Request(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('equipment_rental', 'Equipment Rental'),
        ('fault_report', 'Fault Report'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'),
        ('open', 'Open'), ('resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Equipment rental fields
    return_date = models.DateField(blank=True, null=True)
    note = models.TextField(max_length=200, blank=True, null=True)
    admin_note = models.TextField(max_length=200, blank=True, null=True)
    
    # Fault report fields  
    fault_description = models.TextField(blank=True, null=True)
    fault_type = models.CharField(max_length=50, blank=True, null=True)
    urgency = models.CharField(max_length=20, blank=True, null=True)
```

#### Key Relationships

```python
# User relationships
User -> RoomAssignment (One-to-One via room_assignments)
User -> Request (One-to-Many)
User -> Building (One-to-Many for building_staff_member)

# Building/Room relationships  
Building -> Room (One-to-Many via rooms)
Building -> User (building_staff_member)
Room -> RoomAssignment (One-to-Many via assignments)

# Inventory relationships
InventoryTracking -> Item (One-to-One)
Item -> Request (One-to-One for equipment rentals)

# Request relationships
Request -> User, Room, Item (Many-to-One)
```

#### Database Indexes

The models include strategic indexes for performance:

```python
# RoomAssignment indexes
models.Index(fields=['room'])
models.Index(fields=['user']) 
models.Index(fields=['end_date'])

# Request indexes
models.Index(fields=['user', 'request_type', 'status'])
models.Index(fields=['room'])
```
