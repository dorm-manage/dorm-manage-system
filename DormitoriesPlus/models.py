from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        # Always set username to email if not provided
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # מצפין את הסיסמה
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        # Always set username to email if not provided
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    STUDENT = 'student'
    BUILDING_STAFF = 'building_staff'
    OFFICE_STAFF = 'office_staff'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (BUILDING_STAFF, 'Building Staff'),
        (OFFICE_STAFF, 'Office Staff'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)


    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',
                       'last_name']  # חשוב לשמור על username, כיוון ש-AbstractUser מוסיף אותו כבר

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    objects = CustomUserManager()  # שימוש במנהל המותאם


# מודל ניהול מלאי (InventoryTracking)
class InventoryTracking(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo_url = models.ImageField(upload_to='inventory_photos/', null=True, blank=True)

    def __str__(self):
        return self.item_name


# מודל פריט (Item)
# In models.py
class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]
    inventory = models.ForeignKey(InventoryTracking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inventory.item_name} - {self.status}"


# מודל בניין (Building)
class Building(models.Model):
    building_name = models.CharField(max_length=255)
    # אחראי בניין – קישור למשתמש בהתאם לתפקיד
    building_staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                              related_name='managed_buildings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.building_name


# מודל חדרים (Room)
class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=1)  # How many students can stay in this room
    notes = models.TextField(blank=True, null=True)  # Optional notes about the room
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        # Ensure a room number is unique within a building
        unique_together = ['building', 'room_number']
        indexes = [
            models.Index(fields=['building']),
        ]

    def __str__(self):
        return f"{self.building.building_name} - Room {self.room_number}"

    def is_occupied(self):
        """Check if this room currently has any active assignments"""
        # Use Python filtering for is_active property
        return any(a.is_active for a in self.assignments.all())


# מודל שיבוץ חדרים (RoomAssignment)
class RoomAssignment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_assignments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assignments')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)  # Null means indefinite assignment
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['user']),
            models.Index(fields=['end_date']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.room}"

    def clean(self):
        # Check if there's already an active assignment for this room
        if self.is_active and self.room.assignments.filter(is_active=True).exclude(id=self.id).exists():
            raise ValidationError("This room is already assigned to another student.")

    @property
    def is_active(self):
        """Return True if the assignment is currently active (no end_date or end_date in the future)"""
        return self.end_date is None or self.end_date >= timezone.now().date()


# מודל בקשות (Request)
class Request(models.Model):
    # סוגי בקשות
    EQUIPMENT_RENTAL = 'equipment_rental'
    FAULT_REPORT = 'fault_report'
    REQUEST_TYPE_CHOICES = [
        (EQUIPMENT_RENTAL, 'Equipment Rental'),
        (FAULT_REPORT, 'Fault Report'),
    ]

    # סטטוסים אפשריים לבקשה
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    OPEN = 'open'
    RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (OPEN, 'Open'),
        (RESOLVED, 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    # במקרה של השאלת ציוד – הפניה לפריט (ניתן לאפשר null)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    # שדה לתיאור התקלה – רלוונטי לבקשות מסוג fault_report
    fault_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(max_length=200, blank=True, null=True, verbose_name="הערות נוספות")
    admin_note = models.TextField(max_length=200, blank=True, null=True, verbose_name="הערות מנהל")
    return_date = models.DateField(blank=True, null=True, verbose_name="תאריך החזרה מתוכנן")
    fault_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="סוג התקלה")
    urgency = models.CharField(max_length=20, blank=True, null=True, verbose_name="דחיפות")

    class Meta:
        indexes = [
            models.Index(fields=['user', 'request_type', 'status']),
            models.Index(fields=['room']),
        ]

    def mark_as_resolved(self):
        self.status = Request.RESOLVED
        self.save()

    def push_to_top(self):
        # דוגמה: עדכון תאריך יצירה כדי לדחוף לראש התור
        from django.utils import timezone
        self.created_at = timezone.now()
        self.save()

    @property
    def is_due_soon(self):
        """Returns True if the return date is within 7 days from now but not passed yet"""
        if not self.return_date:
            return False

        today = timezone.now().date()
        days_remaining = (self.return_date - today).days
        return 0 <= days_remaining < 7

    @property
    def is_overdue(self):
        """Returns True if the return date has passed"""
        if not self.return_date:
            return False

        today = timezone.now().date()
        return self.return_date < today

    def __str__(self):
        return f"{self.user.email} - {self.request_type}"


# מודל הודעות (Message)
class Message(models.Model):
    # ניתן לקשר את ההודעה לבניין מסוים
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.building} at {self.created_at}"

