from django.test import TestCase
import pytest
from django.utils import timezone
from datetime import timedelta
from .models import User, Building, Room, RoomAssignment, Request, InventoryTracking, Item

# Create your tests here.

@pytest.mark.django_db
class TestUserModel:
    def test_create_student(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Student',
            role='student'
        )
        assert user.email == 'student@test.com'
        assert user.role == 'student'
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_staff(self):
        user = User.objects.create_user(
            email='staff@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Staff',
            role='building_staff'
        )
        assert user.email == 'staff@test.com'
        assert user.role == 'building_staff'

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        assert admin.email == 'admin@test.com'
        assert admin.is_staff is True
        assert admin.is_superuser is True

@pytest.mark.django_db
class TestBuildingModel:
    def test_create_building(self):
        staff = User.objects.create_user(
            email='staff@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Staff',
            role='building_staff'
        )
        building = Building.objects.create(
            building_name='Test Building',
            building_staff_member=staff
        )
        assert building.building_name == 'Test Building'
        assert building.building_staff_member == staff

@pytest.mark.django_db
class TestRoomModel:
    def test_create_room(self):
        building = Building.objects.create(building_name='Test Building')
        room = Room.objects.create(
            building=building,
            room_number='101',
            capacity=2
        )
        assert room.room_number == '101'
        assert room.capacity == 2
        assert room.building == building

    def test_room_unique_constraint(self):
        building = Building.objects.create(building_name='Test Building')
        Room.objects.create(building=building, room_number='101')
        with pytest.raises(Exception):  # Should raise an integrity error
            Room.objects.create(building=building, room_number='101')

@pytest.mark.django_db
class TestRequestModel:
    def test_create_equipment_request(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
        inventory = InventoryTracking.objects.create(
            item_name='Test Item',
            quantity=1
        )
        item = Item.objects.create(
            inventory=inventory,
            status='available'
        )
        request = Request.objects.create(
            user=user,
            request_type='equipment_rental',
            item=item,
            return_date=timezone.now().date() + timedelta(days=7)
        )
        assert request.request_type == 'equipment_rental'
        assert request.status == 'pending'
        assert request.item == item

    def test_request_due_soon(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
        request = Request.objects.create(
            user=user,
            request_type='equipment_rental',
            return_date=timezone.now().date() + timedelta(days=3)
        )
        assert request.is_due_soon is True

    def test_request_overdue(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
        request = Request.objects.create(
            user=user,
            request_type='equipment_rental',
            return_date=timezone.now().date() - timedelta(days=1)
        )
        assert request.is_overdue is True

@pytest.mark.django_db
class TestRoomAssignmentModel:
    def test_create_room_assignment(self):
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
        building = Building.objects.create(building_name='Test Building')
        room = Room.objects.create(
            building=building,
            room_number='101'
        )
        assignment = RoomAssignment.objects.create(
            user=user,
            room=room,
            start_date=timezone.now().date()
        )
        assert assignment.user == user
        assert assignment.room == room
        assert assignment.end_date is None  # Indefinite assignment
