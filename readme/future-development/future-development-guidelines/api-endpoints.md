# API Endpoints

The system provides REST API endpoints using Django REST Framework (see `api_views.py`):

#### API Implementation Details

**Authentication**

All API endpoints require user authentication. The system uses Django's built-in session authentication for API calls from the web interface.

**Data Aggregation**

The `OMSummaryAPIView` performs complex data aggregation:

```python
# Efficient querying with relationships
for building in Building.objects.all():
    rooms = building.rooms.all()
    for room in rooms:
        active_assignments = room.assignments.filter(end_date__isnull=True)
        room_requests = Request.objects.filter(room=room)
```

**AI Integration**

The system integrates with Google Gemini for AI-powered insights:

```python
# API call to Gemini
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
data = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}
response = requests.post(url, headers=headers, json=data)
```

**Error Handling**

APIs include comprehensive error handling:

```python
try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as http_err:
    error_details = http_err.response.json()
    return Response({'error': f"HTTP error: {error_details}"}, status=500)
except Exception as e:
    return Response({'error': str(e)}, status=500)
```

#### API Security Considerations

**Environment Variables**

Sensitive API keys are stored in environment variables: see ".evn" file
