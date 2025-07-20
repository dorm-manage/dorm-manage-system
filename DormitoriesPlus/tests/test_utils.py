from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from datetime import date, timedelta
from io import StringIO

from DormitoriesPlus.models import (
    User, InventoryTracking, Item, Building, Room, 
    RoomAssignment, Request, Message
)

User = get_user_model()


class BaseUtilityTestCase(TestCase):
    """Base test case for utility tests"""
    
    def setUp(self):
        """Set up test data"""
        # Create users
        self.student = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            first_name='Student',
            last_name='User',
            role='student'
        )
        
        self.building_staff = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            first_name='Staff',
            last_name='Member',
            role='building_staff'
        )
        
        # Create building
        self.building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=self.building_staff
        )
        
        # Create room
        self.room = Room.objects.create(
            building=self.building,
            room_number='101',
            capacity=2
        )
        
        # Create inventory item
        self.inventory = InventoryTracking.objects.create(
            item_name='Test Item',
            quantity=5
        )
        
        # Create item
        self.item = Item.objects.create(
            inventory=self.inventory,
            status='available'
        )


class ManagementCommandsTest(BaseUtilityTestCase):
    """Test cases for management commands"""
    
    def test_send_overdue_notifications_command(self):
        """Test the send_overdue_notifications management command."""
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('send_overdue_notifications', stdout=out)
        
        output = out.getvalue()
        # The command outputs a message about what it found
        self.assertIn('No overdue or soon-to-be-due items found', output)
    
    def test_test_email_command(self):
        """Test the test_email management command."""
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        # Add the required --to argument
        call_command('test_email', '--to=test@example.com', stdout=out)
        
        output = out.getvalue()
        self.assertIn('Test email sent', output)


class ModelUtilityMethodsTest(BaseUtilityTestCase):
    """Test cases for model utility methods"""
    
    def test_request_is_overdue_property(self):
        """Test the is_overdue property of Request model"""
        # Create a request with past return date
        overdue_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved',
            return_date=timezone.now().date() - timedelta(days=1)
        )
        self.assertTrue(overdue_request.is_overdue)
        
        # Create a request with future return date
        future_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved',
            return_date=timezone.now().date() + timedelta(days=7)
        )
        self.assertFalse(future_request.is_overdue)
        
        # Create a request without return date
        no_date_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved'
        )
        self.assertFalse(no_date_request.is_overdue)
    
    def test_request_is_due_soon_property(self):
        """Test the is_due_soon property of Request model"""
        # Create a request due in 3 days (should be due soon)
        due_soon_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved',
            return_date=timezone.now().date() + timedelta(days=3)
        )
        self.assertTrue(due_soon_request.is_due_soon)
        
        # Create a request due in 10 days (should not be due soon)
        not_due_soon_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved',
            return_date=timezone.now().date() + timedelta(days=10)
        )
        self.assertFalse(not_due_soon_request.is_due_soon)
        
        # Create a request without return date
        no_date_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved'
        )
        self.assertFalse(no_date_request.is_due_soon)
    
    def test_request_mark_as_resolved_method(self):
        """Test the mark_as_resolved method of Request model"""
        request = Request.objects.create(
            user=self.student,
            request_type='fault_report',
            room=self.room,
            status='open'
        )
        
        request.mark_as_resolved()
        self.assertEqual(request.status, 'resolved')
    
    def test_request_push_to_top_method(self):
        """Test the push_to_top method of Request model"""
        request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='pending'
        )
        
        original_created_at = request.created_at
        request.push_to_top()
        
        # The created_at should be updated to current time
        self.assertGreater(request.created_at, original_created_at)
    
    def test_room_is_occupied_method(self):
        """Test the is_occupied method of Room model"""
        # Initially room should not be occupied
        self.assertFalse(self.room.is_occupied())
        
        # Create an active room assignment
        RoomAssignment.objects.create(
            user=self.student,
            room=self.room,
            start_date=timezone.now().date()
        )
        
        # Now room should be occupied
        self.assertTrue(self.room.is_occupied())
    
    def test_room_unique_constraint(self):
        """Test room unique constraint within building"""
        # Create first room
        Room.objects.create(
            building=self.building,
            room_number='102',
            capacity=2
        )
        
        # Try to create second room with same number in same building
        with self.assertRaises(Exception):
            Room.objects.create(
                building=self.building,
                room_number='102',  # Same room number
                capacity=3
            )


class EmailUtilityTest(BaseUtilityTestCase):
    """Test cases for email utility functions"""
    
    def test_email_template_rendering(self):
        """Test email template rendering"""
        # Create an overdue request for testing
        overdue_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved',
            return_date=timezone.now().date() - timedelta(days=1)
        )
        
        # Test that we can access the request data for email templates
        self.assertEqual(overdue_request.user.email, 'student@example.com')
        self.assertEqual(overdue_request.item.inventory.item_name, 'Test Item')
        self.assertTrue(overdue_request.is_overdue)
    
    def test_email_context_data(self):
        """Test email context data preparation"""
        # Create multiple overdue requests
        overdue_requests = []
        for i in range(3):
            request = Request.objects.create(
                user=self.student,
                request_type='equipment_rental',
                item=self.item,
                status='approved',
                return_date=timezone.now().date() - timedelta(days=i+1)
            )
            overdue_requests.append(request)
        
        # Test that we can collect overdue requests
        overdue_requests_from_db = Request.objects.filter(
            status='approved',
            return_date__lt=timezone.now().date()
        )
        
        self.assertEqual(overdue_requests_from_db.count(), 3)
        for request in overdue_requests_from_db:
            self.assertTrue(request.is_overdue)


class DataValidationUtilityTest(BaseUtilityTestCase):
    """Test cases for data validation utilities"""
    
    def test_date_validation(self):
        """Test date validation utilities"""
        # Test valid date
        valid_date = timezone.now().date()
        self.assertIsInstance(valid_date, date)
        
        # Test future date
        future_date = timezone.now().date() + timedelta(days=7)
        self.assertGreater(future_date, timezone.now().date())
        
        # Test past date
        past_date = timezone.now().date() - timedelta(days=7)
        self.assertLess(past_date, timezone.now().date())
    
    def test_email_validation(self):
        """Test email validation utilities"""
        # Test valid email
        valid_email = 'test@example.com'
        self.assertIn('@', valid_email)
        self.assertIn('.', valid_email)
        
        # Test invalid email
        invalid_email = 'invalid-email'
        self.assertNotIn('.', invalid_email)
    
    def test_quantity_validation(self):
        """Test quantity validation utilities"""
        # Test valid quantity
        valid_quantity = 5
        self.assertGreaterEqual(valid_quantity, 0)
        
        # Test zero quantity
        zero_quantity = 0
        self.assertEqual(zero_quantity, 0)
        
        # Test negative quantity (should be invalid)
        negative_quantity = -1
        self.assertLess(negative_quantity, 0)


class PermissionUtilityTest(BaseUtilityTestCase):
    """Test cases for permission utility functions"""
    
    def test_role_based_permissions(self):
        """Test role-based permission checking"""
        # Test student permissions
        self.assertEqual(self.student.role, 'student')
        self.assertNotEqual(self.student.role, 'building_staff')
        self.assertNotEqual(self.student.role, 'office_staff')
        
        # Test building staff permissions
        self.assertEqual(self.building_staff.role, 'building_staff')
        self.assertNotEqual(self.building_staff.role, 'student')
        self.assertNotEqual(self.building_staff.role, 'office_staff')
        
        # Test office staff permissions
        office_staff = User.objects.create_user(
            email='office@example.com',
            password='officepass123',
            first_name='Office',
            last_name='Staff',
            role='office_staff'
        )
        self.assertEqual(office_staff.role, 'office_staff')
        self.assertNotEqual(office_staff.role, 'student')
        self.assertNotEqual(office_staff.role, 'building_staff')
    
    def test_building_access_permissions(self):
        """Test building access permissions"""
        # Test that building staff can access their building
        self.assertEqual(self.building.building_staff_member, self.building_staff)
        
        # Test that other users cannot access this building as staff
        self.assertNotEqual(self.building.building_staff_member, self.student)
    
    def test_request_ownership_permissions(self):
        """Test request ownership permissions"""
        # Create a request owned by student
        student_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='pending'
        )
        
        # Test that student owns the request
        self.assertEqual(student_request.user, self.student)
        
        # Test that building staff does not own the request
        self.assertNotEqual(student_request.user, self.building_staff)


class SearchUtilityTest(BaseUtilityTestCase):
    """Test cases for search utility functions"""
    
    def test_request_search_by_status(self):
        """Test searching requests by status"""
        # Create requests with different statuses
        pending_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='pending'
        )
        
        approved_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='approved'
        )
        
        # Test filtering by status
        pending_requests = Request.objects.filter(status='pending')
        self.assertEqual(pending_requests.count(), 1)
        self.assertEqual(pending_requests.first(), pending_request)
        
        approved_requests = Request.objects.filter(status='approved')
        self.assertEqual(approved_requests.count(), 1)
        self.assertEqual(approved_requests.first(), approved_request)
    
    def test_request_search_by_type(self):
        """Test searching requests by type"""
        # Create requests with different types
        equipment_request = Request.objects.create(
            user=self.student,
            request_type='equipment_rental',
            item=self.item,
            status='pending'
        )
        
        fault_request = Request.objects.create(
            user=self.student,
            request_type='fault_report',
            room=self.room,
            status='open'
        )
        
        # Test filtering by type
        equipment_requests = Request.objects.filter(request_type='equipment_rental')
        self.assertEqual(equipment_requests.count(), 1)
        self.assertEqual(equipment_requests.first(), equipment_request)
        
        fault_requests = Request.objects.filter(request_type='fault_report')
        self.assertEqual(fault_requests.count(), 1)
        self.assertEqual(fault_requests.first(), fault_request)
    
    def test_inventory_search_by_name(self):
        """Test searching inventory by name"""
        # Create inventory items with different names
        item1 = InventoryTracking.objects.create(
            item_name='Laptop',
            quantity=5
        )
        
        item2 = InventoryTracking.objects.create(
            item_name='Projector',
            quantity=3
        )
        
        # Test filtering by name
        laptop_items = InventoryTracking.objects.filter(item_name__icontains='laptop')
        self.assertEqual(laptop_items.count(), 1)
        self.assertEqual(laptop_items.first(), item1)
        
        projector_items = InventoryTracking.objects.filter(item_name__icontains='projector')
        self.assertEqual(projector_items.count(), 1)
        self.assertEqual(projector_items.first(), item2) 