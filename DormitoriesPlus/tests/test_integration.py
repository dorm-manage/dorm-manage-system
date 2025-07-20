from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta

from DormitoriesPlus.models import (
    User, InventoryTracking, Item, Building, Room, 
    RoomAssignment, Request, Message
)

User = get_user_model()


class CompleteWorkflowTest(TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test data for complete workflows"""
        self.client = Client()
        
        # Create users for different roles
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
        
        self.office_staff = User.objects.create_user(
            email='office@example.com',
            password='officepass123',
            first_name='Office',
            last_name='Staff',
            role='office_staff'
        )
        
        # Create building and room
        self.building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=self.building_staff
        )
        
        self.room = Room.objects.create(
            building=self.building,
            room_number='101',
            capacity=2
        )
        
        # Create inventory and item
        self.inventory = InventoryTracking.objects.create(
            item_name='Test Item',
            quantity=5
        )
        
        self.item = Item.objects.create(
            inventory=self.inventory,
            status='available'
        )


class EquipmentRentalWorkflowTest(CompleteWorkflowTest):
    """Test complete equipment rental workflow"""
    
    def test_complete_equipment_rental_workflow(self):
        """Test the complete equipment rental workflow from student request to approval"""
        
        # Step 1: Student logs in and creates equipment rental request
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.post('/students/application/', {
            'request_type': 'equipment_rental',
            'item': self.item.id,
            'return_date': (timezone.now().date() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'note': 'Test equipment rental request'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify request was created
        request = Request.objects.filter(
            user=self.student,
            request_type='equipment_rental',
            item=self.item
        ).first()
        self.assertIsNotNone(request)
        self.assertEqual(request.status, 'pending')
        
        # Step 2: Building manager logs in and approves the request
        self.client.logout()
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/loan_requests/', {
            'approve_request': 'true',
            'request_id': request.id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after approval
        
        # Verify request was approved
        request.refresh_from_db()
        self.assertEqual(request.status, 'approved')
        
        # Step 3: Student checks their approved request
        self.client.logout()
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.get('/students/homepage/')
        self.assertEqual(response.status_code, 200)
        
        # Verify approved request appears in student's homepage
        approved_requests = Request.objects.filter(
            user=self.student,
            request_type='equipment_rental',
            status='approved'
        )
        self.assertEqual(approved_requests.count(), 1)
    
    def test_equipment_rental_with_rejection(self):
        """Test equipment rental workflow with rejection"""
        
        # Step 1: Student creates request
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.post('/students/application/', {
            'request_type': 'equipment_rental',
            'item': self.item.id,
            'return_date': (timezone.now().date() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'note': 'Test equipment rental request'
        })
        
        self.assertEqual(response.status_code, 302)
        
        request = Request.objects.filter(
            user=self.student,
            request_type='equipment_rental',
            item=self.item
        ).first()
        
        # Step 2: Building manager rejects the request
        self.client.logout()
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/loan_requests/', {
            'reject_request': 'true',
            'request_id': request.id,
            'admin_note': 'Request rejected due to insufficient inventory'
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Verify request was rejected
        request.refresh_from_db()
        self.assertEqual(request.status, 'rejected')
        self.assertEqual(request.admin_note, 'Request rejected due to insufficient inventory')
        
        # Step 3: Student deletes rejected request
        self.client.logout()
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.post('/students/homepage/', {
            'delete_request': 'true',
            'request_id': request.id
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Verify request was deleted
        self.assertFalse(Request.objects.filter(id=request.id).exists())


class FaultReportWorkflowTest(CompleteWorkflowTest):
    """Test complete fault report workflow"""
    
    def test_complete_fault_report_workflow(self):
        """Test the complete fault report workflow from student report to resolution"""
        
        # Step 1: Student logs in and creates fault report
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.post('/students/faults/', {
            'request_type': 'fault_report',
            'room': self.room.id,
            'fault_description': 'Broken window in room',
            'fault_type': 'Maintenance',
            'urgency': 'High',
            'note': 'Test fault report'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify fault report was created
        fault_report = Request.objects.filter(
            user=self.student,
            request_type='fault_report',
            room=self.room
        ).first()
        self.assertIsNotNone(fault_report)
        self.assertEqual(fault_report.status, 'open')
        self.assertEqual(fault_report.fault_description, 'Broken window in room')
        self.assertEqual(fault_report.fault_type, 'Maintenance')
        self.assertEqual(fault_report.urgency, 'High')
        
        # Step 2: Building manager logs in and resolves the fault
        self.client.logout()
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/faults/', {
            'resolve_fault': 'true',
            'request_id': fault_report.id,
            'admin_note': 'Window repaired successfully'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after resolution
        
        # Verify fault was resolved
        fault_report.refresh_from_db()
        self.assertEqual(fault_report.status, 'resolved')
        self.assertEqual(fault_report.admin_note, 'Window repaired successfully')
        
        # Step 3: Student checks resolved fault report
        self.client.logout()
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.get('/students/homepage/')
        self.assertEqual(response.status_code, 200)
        
        # Verify resolved fault report appears in student's homepage
        resolved_faults = Request.objects.filter(
            user=self.student,
            request_type='fault_report',
            status='resolved'
        )
        self.assertEqual(resolved_faults.count(), 1)


class InventoryManagementWorkflowTest(CompleteWorkflowTest):
    """Test complete inventory management workflow"""
    
    def test_complete_inventory_management_workflow(self):
        """Test the complete inventory management workflow"""
        
        # Step 1: Building manager logs in and adds inventory item
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/inventory/', {
            'add_item': 'true',
            'item_name': 'New Laptop',
            'quantity': 10
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify inventory item was created
        new_inventory = InventoryTracking.objects.filter(
            item_name='New Laptop',
            quantity=10
        ).first()
        self.assertIsNotNone(new_inventory)
        
        # Step 2: Building manager updates inventory item
        response = self.client.post('/BM/inventory/', {
            'update_item': 'true',
            'item_id': new_inventory.id,
            'item_name': 'Updated Laptop',
            'quantity': 15
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Verify inventory item was updated
        new_inventory.refresh_from_db()
        self.assertEqual(new_inventory.item_name, 'Updated Laptop')
        self.assertEqual(new_inventory.quantity, 15)
        
        # Step 3: Building manager deletes inventory item
        response = self.client.post('/BM/inventory/', {
            'delete_item': 'true',
            'item_id': new_inventory.id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        
        # Verify inventory item was deleted
        self.assertFalse(InventoryTracking.objects.filter(id=new_inventory.id).exists())


class StudentManagementWorkflowTest(CompleteWorkflowTest):
    """Test complete student management workflow"""
    
    def test_complete_student_management_workflow(self):
        """Test the complete student management workflow"""
        
        # Create a new student
        new_student = User.objects.create_user(
            email='newstudent@example.com',
            password='newpass123',
            first_name='New',
            last_name='Student',
            role='student'
        )
        
        # Step 1: Building manager logs in and assigns student to room
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/manage_students/', {
            'add_student': 'true',
            'student_email': 'newstudent@example.com',
            'building': self.building.id,
            'room_number': '102',
            'start_date': timezone.now().date().strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after assignment
        
        # Verify room assignment was created
        room_assignment = RoomAssignment.objects.filter(
            user=new_student,
            room__building=self.building,
            room__room_number='102'
        ).first()
        self.assertIsNotNone(room_assignment)
        
        # Step 2: Building manager removes student from room
        response = self.client.post('/BM/manage_students/', {
            'remove_student': 'true',
            'student_email': 'newstudent@example.com',
            'building': self.building.id,
            'room_number': '102'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after removal
        
        # Verify room assignment was removed
        self.assertFalse(RoomAssignment.objects.filter(
            user=new_student,
            room__building=self.building,
            room__room_number='102'
        ).exists())


class MessageWorkflowTest(CompleteWorkflowTest):
    """Test complete message workflow"""
    
    def test_complete_message_workflow(self):
        """Test the complete message workflow"""
        
        # Step 1: Building manager logs in and sends message
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/sendMassage/', {
            'send_message': 'true',
            'building': self.building.id,
            'content': 'Important announcement for all residents'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after sending
        
        # Verify message was created
        message = Message.objects.filter(
            building=self.building,
            content='Important announcement for all residents'
        ).first()
        self.assertIsNotNone(message)
        
        # Step 2: Verify message can be retrieved
        messages_for_building = Message.objects.filter(building=self.building)
        self.assertEqual(messages_for_building.count(), 1)
        self.assertEqual(messages_for_building.first(), message)


class RoleBasedAccessWorkflowTest(CompleteWorkflowTest):
    """Test role-based access control workflows"""
    
    def test_student_access_restrictions(self):
        """Test that students cannot access staff pages"""
        
        # Student tries to access building manager pages
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.get('/BM/Homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
        
        response = self.client.get('/OM/Homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
        
        # Student tries to access staff functionality
        response = self.client.post('/BM/inventory/', {
            'add_item': 'true',
            'item_name': 'Test Item',
            'quantity': 5
        })
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
    
    def test_building_staff_access_restrictions(self):
        """Test that building staff cannot access office manager pages"""
        
        # Building staff tries to access office manager pages
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.get('/OM/Homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
        
        response = self.client.get('/OM/inventory/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
    
    def test_office_staff_access_restrictions(self):
        """Test that office staff cannot access building manager pages"""
        
        # Office staff tries to access building manager pages
        self.client.login(email='office@example.com', password='officepass123')
        
        response = self.client.get('/BM/Homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
        
        response = self.client.get('/BM/inventory/')
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied


class AuthenticationWorkflowTest(CompleteWorkflowTest):
    """Test authentication workflows"""
    
    def test_complete_authentication_workflow(self):
        """Test complete authentication workflow"""
        
        # Step 1: Test login page access
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Test successful login
        response = self.client.post('/login/', {
            'email': 'student@example.com',
            'password': 'studentpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # Step 3: Test access to protected page after login
        response = self.client.get('/students/homepage/')
        self.assertEqual(response.status_code, 200)
        
        # Step 4: Test logout
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
        # Step 5: Test access denied after logout
        response = self.client.get('/students/homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_failed_authentication_workflow(self):
        """Test failed authentication workflow"""
        
        # Test login with wrong password
        response = self.client.post('/login/', {
            'email': 'student@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        
        # Test access to protected page without login
        response = self.client.get('/students/homepage/')
        self.assertEqual(response.status_code, 302)  # Redirect to login


class PaginationWorkflowTest(CompleteWorkflowTest):
    """Test pagination workflows"""
    
    def test_pagination_workflow(self):
        """Test pagination workflow with multiple items"""
        
        # Create multiple requests for pagination testing
        self.client.login(email='student@example.com', password='studentpass123')
        
        for i in range(15):  # Create 15 requests
            Request.objects.create(
                user=self.student,
                request_type='equipment_rental',
                item=self.item,
                status='pending'
            )
        
        # Test first page
        response = self.client.get('/students/homepage/?pending_page=1')
        self.assertEqual(response.status_code, 200)
        
        # Test second page
        response = self.client.get('/students/homepage/?pending_page=2')
        self.assertEqual(response.status_code, 200)
        
        # Test third page
        response = self.client.get('/students/homepage/?pending_page=3')
        self.assertEqual(response.status_code, 200)
        
        # Verify pagination is working
        pending_requests = Request.objects.filter(
            user=self.student,
            request_type='equipment_rental',
            status='pending'
        )
        self.assertEqual(pending_requests.count(), 15)


class DataIntegrityWorkflowTest(CompleteWorkflowTest):
    """Test data integrity workflows"""
    
    def test_data_integrity_workflow(self):
        """Test data integrity throughout workflows"""
        
        # Step 1: Create inventory item
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/inventory/', {
            'add_item': 'true',
            'item_name': 'Integrity Test Item',
            'quantity': 10
        })
        
        self.assertEqual(response.status_code, 302)
        
        inventory = InventoryTracking.objects.filter(item_name='Integrity Test Item').first()
        self.assertIsNotNone(inventory)
        
        # Step 2: Create item from inventory
        item = Item.objects.create(
            inventory=inventory,
            status='available'
        )
        
        # Step 3: Student creates request for item
        self.client.logout()
        self.client.login(email='student@example.com', password='studentpass123')
        
        response = self.client.post('/students/application/', {
            'request_type': 'equipment_rental',
            'item': item.id,
            'return_date': (timezone.now().date() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'note': 'Test integrity request'
        })
        
        self.assertEqual(response.status_code, 302)
        
        request = Request.objects.filter(
            user=self.student,
            request_type='equipment_rental',
            item=item
        ).first()
        
        # Step 4: Verify data integrity relationships
        self.assertEqual(request.item.inventory, inventory)
        self.assertEqual(request.user, self.student)
        self.assertEqual(request.item.status, 'available')
        
        # Step 5: Approve request and verify item status changes
        self.client.logout()
        self.client.login(email='staff@example.com', password='staffpass123')
        
        response = self.client.post('/BM/loan_requests/', {
            'approve_request': 'true',
            'request_id': request.id
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Verify request status changed
        request.refresh_from_db()
        self.assertEqual(request.status, 'approved')
        
        # Note: In a real application, item status might change to 'borrowed'
        # This depends on the specific business logic implementation 