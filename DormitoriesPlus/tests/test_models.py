from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from DormitoriesPlus.models import (
    User, InventoryTracking, Item, Building, Room, 
    RoomAssignment, Request, Message
)

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_user_str_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'Test User')
    
    def test_user_role_choices(self):
        """Test that user roles are properly set."""
        # Test different roles with unique emails
        roles = ['student', 'building_staff', 'office_staff']
        
        for i, role in enumerate(roles):
            user_data = {
                'email': f'role_test_{i}@example.com',  # Unique email for each test
                'password': 'testpass123',
                'first_name': f'Test{i}',
                'last_name': f'User{i}',
                'role': role
            }
            user = User.objects.create_user(**user_data)
            self.assertEqual(user.role, role)


class InventoryTrackingModelTest(TestCase):
    """Test cases for the InventoryTracking model"""
    
    def setUp(self):
        """Set up test data"""
        self.inventory_data = {
            'item_name': 'Test Item',
            'quantity': 10
        }
    
    def test_create_inventory_item(self):
        """Test creating an inventory item"""
        item = InventoryTracking.objects.create(**self.inventory_data)
        self.assertEqual(item.item_name, 'Test Item')
        self.assertEqual(item.quantity, 10)
        self.assertIsNotNone(item.created_at)
        self.assertIsNotNone(item.updated_at)
    
    def test_inventory_str_representation(self):
        """Test the string representation of inventory item"""
        item = InventoryTracking.objects.create(**self.inventory_data)
        self.assertEqual(str(item), 'Test Item')
    
    def test_inventory_photo_url_optional(self):
        """Test that photo_url is optional"""
        item = InventoryTracking.objects.create(**self.inventory_data)
        self.assertFalse(item.photo_url)


class ItemModelTest(TestCase):
    """Test cases for the Item model"""
    
    def setUp(self):
        """Set up test data"""
        self.inventory = InventoryTracking.objects.create(
            item_name='Test Item',
            quantity=5
        )
        self.item_data = {
            'inventory': self.inventory,
            'status': 'available'
        }
    
    def test_create_item(self):
        """Test creating an item"""
        item = Item.objects.create(**self.item_data)
        self.assertEqual(item.inventory, self.inventory)
        self.assertEqual(item.status, 'available')
        self.assertIsNotNone(item.created_at)
        self.assertIsNotNone(item.updated_at)
    
    def test_item_str_representation(self):
        """Test the string representation of item"""
        item = Item.objects.create(**self.item_data)
        self.assertEqual(str(item), 'Test Item - available')
    
    def test_item_status_choices(self):
        """Test that item status choices work correctly"""
        statuses = ['available', 'borrowed']
        for status in statuses:
            item_data = self.item_data.copy()
            item_data['status'] = status
            item = Item.objects.create(**item_data)
            self.assertEqual(item.status, status)


class BuildingModelTest(TestCase):
    """Test cases for the Building model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            first_name='Staff',
            last_name='Member',
            role='building_staff'
        )
        self.building_data = {
            'building_name': 'Test Building',
            'building_staff_member': self.user
        }
    
    def test_create_building(self):
        """Test creating a building"""
        building = Building.objects.create(**self.building_data)
        self.assertEqual(building.building_name, 'Test Building')
        self.assertEqual(building.building_staff_member, self.user)
        self.assertIsNotNone(building.created_at)
    
    def test_building_str_representation(self):
        """Test the string representation of building"""
        building = Building.objects.create(**self.building_data)
        self.assertEqual(str(building), 'Test Building')
    
    def test_building_without_staff(self):
        """Test creating a building without staff member"""
        building = Building.objects.create(building_name='No Staff Building')
        self.assertIsNone(building.building_staff_member)


class RoomModelTest(TestCase):
    """Test cases for the Room model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            first_name='Staff',
            last_name='Member',
            role='building_staff'
        )
        self.building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=self.user
        )
        self.room_data = {
            'building': self.building,
            'room_number': '101',
            'capacity': 2,
            'notes': 'Test room'
        }
    
    def test_create_room(self):
        """Test creating a room"""
        room = Room.objects.create(**self.room_data)
        self.assertEqual(room.building, self.building)
        self.assertEqual(room.room_number, '101')
        self.assertEqual(room.capacity, 2)
        self.assertEqual(room.notes, 'Test room')
        self.assertIsNotNone(room.created_at)
    
    def test_room_str_representation(self):
        """Test the string representation of room"""
        room = Room.objects.create(**self.room_data)
        self.assertEqual(str(room), 'Test Building - Room 101')
    
    def test_room_unique_constraint(self):
        """Test that room numbers are unique within a building"""
        Room.objects.create(**self.room_data)
        
        # Try to create another room with same number in same building
        with self.assertRaises(Exception):
            Room.objects.create(**self.room_data)
    
    def test_room_is_occupied(self):
        """Test the is_occupied method"""
        room = Room.objects.create(**self.room_data)
        
        # Initially should not be occupied
        self.assertFalse(room.is_occupied())
        
        # Create an active assignment
        user = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            first_name='Student',
            last_name='User',
            role='student'
        )
        RoomAssignment.objects.create(
            user=user,
            room=room,
            start_date=timezone.now().date()
        )
        
        # Now should be occupied
        self.assertTrue(room.is_occupied())


class RoomAssignmentModelTest(TestCase):
    """Test cases for the RoomAssignment model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            first_name='Staff',
            last_name='Member',
            role='building_staff'
        )
        self.building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=self.user
        )
        self.room = Room.objects.create(
            building=self.building,
            room_number='101',
            capacity=2
        )
        self.student = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            first_name='Student',
            last_name='User',
            role='student'
        )
        self.assignment_data = {
            'user': self.student,
            'room': self.room,
            'start_date': timezone.now().date()
        }
    
    def test_create_room_assignment(self):
        """Test creating a room assignment"""
        assignment = RoomAssignment.objects.create(**self.assignment_data)
        self.assertEqual(assignment.user, self.student)
        self.assertEqual(assignment.room, self.room)
        self.assertEqual(assignment.start_date, timezone.now().date())
        self.assertIsNone(assignment.end_date)
        self.assertIsNotNone(assignment.assigned_at)
    
    def test_room_assignment_str_representation(self):
        """Test the string representation of room assignment"""
        assignment = RoomAssignment.objects.create(**self.assignment_data)
        self.assertEqual(str(assignment), 'student@example.com -> Test Building - Room 101')
    
    def test_room_assignment_with_end_date(self):
        """Test creating a room assignment with end date"""
        end_date = timezone.now().date() + timedelta(days=30)
        assignment_data = self.assignment_data.copy()
        assignment_data['end_date'] = end_date
        
        assignment = RoomAssignment.objects.create(**assignment_data)
        self.assertEqual(assignment.end_date, end_date)


class RequestModelTest(TestCase):
    """Test cases for the Request model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            first_name='Student',
            last_name='User',
            role='student'
        )
        self.inventory = InventoryTracking.objects.create(
            item_name='Test Item',
            quantity=5
        )
        self.item = Item.objects.create(
            inventory=self.inventory,
            status='available'
        )
        self.request_data = {
            'user': self.user,
            'request_type': 'equipment_rental',
            'item': self.item,
            'status': 'pending'
        }
    
    def test_create_equipment_request(self):
        """Test creating an equipment rental request"""
        request = Request.objects.create(**self.request_data)
        self.assertEqual(request.user, self.user)
        self.assertEqual(request.request_type, 'equipment_rental')
        self.assertEqual(request.item, self.item)
        self.assertEqual(request.status, 'pending')
        self.assertIsNotNone(request.created_at)
        self.assertIsNotNone(request.updated_at)
    
    def test_create_fault_report(self):
        """Test creating a fault report"""
        fault_data = {
            'user': self.user,
            'request_type': 'fault_report',
            'fault_description': 'Broken window',
            'status': 'open',
            'fault_type': 'Maintenance',
            'urgency': 'High'
        }
        request = Request.objects.create(**fault_data)
        self.assertEqual(request.request_type, 'fault_report')
        self.assertEqual(request.fault_description, 'Broken window')
        self.assertEqual(request.fault_type, 'Maintenance')
        self.assertEqual(request.urgency, 'High')
    
    def test_request_str_representation(self):
        """Test the string representation of request"""
        request = Request.objects.create(**self.request_data)
        self.assertEqual(str(request), 'student@example.com - equipment_rental')
    
    def test_mark_as_resolved(self):
        """Test marking a request as resolved"""
        request = Request.objects.create(**self.request_data)
        request.mark_as_resolved()
        self.assertEqual(request.status, 'resolved')
    
    def test_push_to_top(self):
        """Test pushing a request to top"""
        request = Request.objects.create(**self.request_data)
        original_created_at = request.created_at
        request.push_to_top()
        self.assertGreater(request.created_at, original_created_at)
    
    def test_is_due_soon(self):
        """Test the is_due_soon property"""
        request = Request.objects.create(**self.request_data)
        
        # No return date
        self.assertFalse(request.is_due_soon)
        
        # Return date in 3 days (should be due soon)
        request.return_date = timezone.now().date() + timedelta(days=3)
        request.save()
        self.assertTrue(request.is_due_soon)
        
        # Return date in 10 days (should not be due soon)
        request.return_date = timezone.now().date() + timedelta(days=10)
        request.save()
        self.assertFalse(request.is_due_soon)
    
    def test_is_overdue(self):
        """Test the is_overdue property"""
        request = Request.objects.create(**self.request_data)
        
        # No return date
        self.assertFalse(request.is_overdue)
        
        # Return date in the past (should be overdue)
        request.return_date = timezone.now().date() - timedelta(days=1)
        request.save()
        self.assertTrue(request.is_overdue)
        
        # Return date in the future (should not be overdue)
        request.return_date = timezone.now().date() + timedelta(days=1)
        request.save()
        self.assertFalse(request.is_overdue)


class MessageModelTest(TestCase):
    """Test cases for the Message model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            first_name='Staff',
            last_name='Member',
            role='building_staff'
        )
        self.building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=self.user
        )
        self.message_data = {
            'building': self.building,
            'content': 'Test message content'
        }
    
    def test_create_message(self):
        """Test creating a message"""
        message = Message.objects.create(**self.message_data)
        self.assertEqual(message.building, self.building)
        self.assertEqual(message.content, 'Test message content')
        self.assertIsNotNone(message.created_at)
    
    def test_message_str_representation(self):
        """Test the string representation of message"""
        message = Message.objects.create(**self.message_data)
        self.assertIn('Test Building', str(message))
        self.assertIn(str(message.created_at), str(message))
    
    def test_message_without_building(self):
        """Test creating a message without building"""
        message = Message.objects.create(content='General message')
        self.assertIsNone(message.building) 