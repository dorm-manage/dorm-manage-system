from rest_framework.views import APIView
from rest_framework.response import Response
from DormitoriesPlus.models import Building, Room, RoomAssignment, InventoryTracking, Item, Request
from django.contrib.auth import get_user_model
import os
import google.generativeai as genai
from django.conf import settings
import requests

class OMSummaryAPIView(APIView):
    def get(self, request):
        # Aggregate buildings
        buildings = []
        for building in Building.objects.all():
            rooms = []
            for room in building.rooms.all():
                # Occupancy: active assignments
                active_assignments = room.assignments.filter(end_date__isnull=True)
                assignments = [
                    {
                        'student': str(a.user),
                        'start_date': a.start_date,
                        'end_date': a.end_date
                    } for a in room.assignments.all()
                ]
                # Requests for this room
                room_requests = Request.objects.filter(room=room)
                rooms.append({
                    'room_number': room.room_number,
                    'capacity': room.capacity,
                    'notes': room.notes,
                    'assignments': assignments,
                    'active_occupancy': active_assignments.count(),
                    'requests': [
                        {
                            'id': r.id,
                            'type': r.request_type,
                            'status': r.status,
                            'created_at': r.created_at,
                            'fault_description': r.fault_description,
                            'urgency': r.urgency
                        } for r in room_requests
                    ]
                })
            # Requests for this building
            building_requests = Request.objects.filter(room__building=building)
            buildings.append({
                'building_name': building.building_name,
                'building_staff_member': str(building.building_staff_member) if building.building_staff_member else None,
                'created_at': building.created_at,
                'rooms': rooms,
                'requests': [
                    {
                        'id': r.id,
                        'type': r.request_type,
                        'status': r.status,
                        'created_at': r.created_at,
                        'fault_description': r.fault_description,
                        'urgency': r.urgency
                    } for r in building_requests
                ]
            })

        # Inventory
        inventory = []
        for inv in InventoryTracking.objects.all():
            items = Item.objects.filter(inventory=inv)
            inventory.append({
                'item_name': inv.item_name,
                'quantity': inv.quantity,
                'photo_url': inv.photo_url.url if inv.photo_url else None,
                'items': [
                    {
                        'id': item.id,
                        'status': item.status,
                        'created_at': item.created_at,
                        'updated_at': item.updated_at
                    } for item in items
                ]
            })

        # Requests not tied to a room/building
        other_requests = Request.objects.filter(room__isnull=True)
        other_requests_data = [
            {
                'id': r.id,
                'type': r.request_type,
                'status': r.status,
                'created_at': r.created_at,
                'fault_description': r.fault_description,
                'urgency': r.urgency
            } for r in other_requests
        ]

        return Response({
            'buildings': buildings,
            'inventory': inventory,
            'other_requests': other_requests_data
        })

class OMAISummaryAPIView(APIView):
    def get(self, request):
        buildings = []
        for building in Building.objects.all():
            rooms = []
            for room in building.rooms.all()[:2]:
                active_assignments = room.assignments.filter(end_date__isnull=True)
                rooms.append({
                    'room_number': room.room_number,
                    'capacity': room.capacity,
                    'active_occupancy': active_assignments.count(),
                })
            building_requests = Request.objects.filter(room__building=building)[:2]
            requests_data = [
                {
                    'type': r.request_type,
                    'status': r.status,
                } for r in building_requests
            ]
            buildings.append({
                'building_name': building.building_name,
                'rooms': rooms,
                'requests': requests_data,
            })
        inventory = []
        for inv in InventoryTracking.objects.all()[:5]:
            inventory.append({
                'item_name': inv.item_name,
                'quantity': inv.quantity,
            })
        other_requests = Request.objects.filter(room__isnull=True)[:5]
        other_requests_data = [
            {
                'type': r.request_type,
                'status': r.status,
            } for r in other_requests
        ]
        prompt = (
            """
            You are an assistant for a dormitory management system. Summarize the following dormitory data in detail, including all buildings, rooms, inventory, and requests. 
            1. First, provide a detailed summary in English.
            2. Then, provide the same summary in Hebrew.
            Data:
            """
            + str({
                'buildings': buildings,
                'inventory': inventory,
                'other_requests': other_requests_data
            })
        )
        # Use requests library to call Gemini REST API
        try:
            api_key = "AIzaSyDbQYOF_JD7zSJRmZWNmLyKKbr3b-G_wvE" 
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raises an exception for bad status codes
            result = response.json()
            summary = result['candidates'][0]['content']['parts'][0]['text']
        except requests.exceptions.HTTPError as http_err:
            error_details = http_err.response.json()
            return Response({'error': f"HTTP error: {error_details.get('error', {}).get('message', str(http_err))}"}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        return Response({
            'summary': summary
        })

class GeminiModelsAPIView(APIView):
    def get(self, request):
        try:
            genai.configure(api_key="AIzaSyDbQYOF_JD7zSJRmZWNmLyKKbr3b-G_wvE")
            models = genai.list_models()
            model_names = [m.name if hasattr(m, 'name') else str(m) for m in models]
            return Response({'models': model_names})
        except Exception as e:
            return Response({'error': str(e)}, status=500) 