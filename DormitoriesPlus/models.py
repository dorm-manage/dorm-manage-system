from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
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
    REQUIRED_FIELDS = ['username', 'first_name',
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

    def __str__(self):
        return self.item_name


# מודל פריט (Item)
class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('damaged', 'Damaged'),
        ('returned', 'Returned'),
    ]
    inventory = models.ForeignKey(InventoryTracking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inventory.item_name} - {self.status}"


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
    # שילוב בניין ודירה בפורמט "בניין-דירה"
    room_num = models.CharField(max_length=50, blank=True)
    # שדה לתיאור התקלה – רלוונטי לבקשות מסוג fault_report
    fault_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_resolved(self):
        self.status = Request.RESOLVED
        self.save()

    def push_to_top(self):
        # דוגמה: עדכון תאריך יצירה כדי לדחוף לראש התור
        from django.utils import timezone
        self.created_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.request_type}"


# מודל בניין (Building)
class Building(models.Model):
    building_name = models.CharField(max_length=255)
    # אחראי בניין – קישור למשתמש בהתאם לתפקיד
    building_staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                              related_name='managed_buildings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_name


# מודל הודעות (Message)
class Message(models.Model):
    # ניתן לקשר את ההודעה לבניין מסוים
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.building} at {self.created_at}"


# מודל שיבוץ חדרים (RoomAssignment)
class RoomAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # שמירת מספר החדר בפורמט "בניין-חדר"
    room = models.CharField(max_length=50)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} -> {self.room}"
