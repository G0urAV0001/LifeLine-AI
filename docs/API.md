# LifeLine AI API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

Most endpoints require authentication via Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase_id_token>
```

## Response Format

All responses are in JSON format:

```json
{
  "data": {...},
  "status": "success",
  "message": "Operation successful"
}
```

## Error Handling

Errors return appropriate HTTP status codes:

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

```json
{
  "error": "Error message"
}
```

## Endpoints

### Authentication

#### Signup
```
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass@123",
  "display_name": "John Doe"
}

Response: 201 Created
{
  "message": "Signup successful",
  "user": {
    "uid": "user_id",
    "email": "user@example.com",
    "display_name": "John Doe"
  }
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "id_token": "firebase_id_token"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": {...},
  "session_cookie": "session_token"
}
```

#### Guest Login
```
POST /auth/guest

Response: 201 Created
{
  "message": "Guest session created",
  "guest_id": "guest_uuid",
  "guest_token": "guest_token",
  "created_at": "2024-01-01T00:00:00"
}
```

#### Verify Token
```
POST /auth/verify-token
Content-Type: application/json

{
  "token": "firebase_id_token"
}

Response: 200 OK
{
  "valid": true,
  "user_id": "uid",
  "email": "user@example.com"
}
```

#### Reset Password
```
POST /auth/reset-password
Content-Type: application/json

{
  "email": "user@example.com"
}

Response: 200 OK
{
  "message": "Password reset email sent"
}
```

### User Profile

#### Get Profile
```
GET /users/profile
Authorization: Bearer <token>

Response: 200 OK
{
  "uid": "user_id",
  "email": "user@example.com",
  "display_name": "John Doe",
  "phone": "+1-212-555-0100"
}
```

#### Update Profile
```
PUT /users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "display_name": "Jane Doe",
  "phone": "+1-212-555-0101"
}

Response: 200 OK
{
  "message": "Profile updated successfully"
}
```

### AI Analysis

#### Analyze Text
```
POST /ai/text
Content-Type: application/json

{
  "text": "I'm having severe chest pain"
}

Response: 200 OK
{
  "emergency_type": "cardiac",
  "severity": "high",
  "recommended_action": "Call ambulance immediately",
  "hospitals_needed": true,
  "guidance": "Sit down and try to stay calm"
}
```

#### Analyze Image
```
POST /ai/image
Content-Type: multipart/form-data

Form Data:
- image: <image_file>
- description: "Wound on arm"

Response: 200 OK
{
  "emergency_type": "injury",
  "severity": "moderate",
  "recommended_action": "Seek medical attention",
  "hospitals_needed": true,
  "guidance": "Clean the wound with water"
}
```

#### Analyze Voice
```
POST /ai/voice
Content-Type: application/json

{
  "transcript": "I fell and broke my arm",
  "language": "en"
}

Response: 200 OK
{
  "emergency_type": "fracture",
  "severity": "high",
  "recommended_action": "Emergency care needed",
  "hospitals_needed": true,
  "guidance": "Immobilize the arm"
}
```

### Emergency Services

#### Find Nearby Hospitals
```
GET /emergency/hospitals?latitude=40.7128&longitude=-74.0060&radius=5000

Query Parameters:
- latitude (required): User latitude
- longitude (required): User longitude
- radius (optional): Search radius in meters (default: 5000)

Response: 200 OK
{
  "hospitals": [
    {
      "id": "hospital_1",
      "name": "City General Hospital",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "address": "123 Main St, New York, NY",
      "phone": "+1-212-555-0100",
      "specialties": ["Emergency", "Trauma"],
      "beds_available": 15,
      "distance": 250
    }
  ],
  "count": 1
}
```

#### Trigger SOS
```
POST /emergency/sos
Content-Type: application/json

{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "emergency_type": "medical",
  "description": "Severe chest pain"
}

Response: 201 Created
{
  "message": "SOS alert activated",
  "sos_id": "sos_uuid"
}
```

### Emergency Contacts

#### Get Contacts
```
GET /users/contacts
Authorization: Bearer <token>

Response: 200 OK
{
  "contacts": [
    {
      "id": "contact_id",
      "name": "Emergency Contact",
      "phone": "+1-212-555-0100",
      "email": "contact@example.com",
      "relationship": "Family",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "count": 1
}
```

#### Add Contact
```
POST /users/contacts
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Emergency Contact",
  "phone": "+1-212-555-0100",
  "email": "contact@example.com",
  "relationship": "Family"
}

Response: 201 Created
{
  "message": "Contact created",
  "contact": {...}
}
```

#### Update Contact
```
PUT /users/contacts/<contact_id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Name",
  "phone": "+1-212-555-0101"
}

Response: 200 OK
{
  "message": "Contact updated"
}
```

#### Delete Contact
```
DELETE /users/contacts/<contact_id>
Authorization: Bearer <token>

Response: 200 OK
{
  "message": "Contact deleted"
}
```

### Emergency History

#### Get Emergency History
```
GET /users/history?limit=50&offset=0
Authorization: Bearer <token>

Query Parameters:
- limit (optional): Number of records (default: 50, max: 100)
- offset (optional): Pagination offset (default: 0)

Response: 200 OK
{
  "history": [
    {
      "id": "history_id",
      "user_id": "uid",
      "input_type": "text",
      "input_text": "Emergency description",
      "analysis": {...},
      "timestamp": "2024-01-01T00:00:00"
    }
  ],
  "count": 1,
  "total": 10,
  "limit": 50,
  "offset": 0
}
```

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
