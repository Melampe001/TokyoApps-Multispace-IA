# Tokyo-IA API Documentation

This document describes the REST API endpoints available in Tokyo-IA.

## Base URL

```
http://localhost:8080/api
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## Cost Prediction API

### Predict Cost

Predict the cost of an LLM request before execution.

**Endpoint:** `GET /api/cost/predict`

**Query Parameters:**
- `tokens` (int, required) - Number of tokens
- `model` (string, required) - Model name (e.g., "gpt-4", "gpt-3.5-turbo")
- `type` (string, optional) - Request type (default: "completion")
- `complexity` (float, optional) - Complexity score 0-1 (default: 0.5)

**Example Request:**
```bash
curl "http://localhost:8080/api/cost/predict?tokens=5000&model=gpt-4&complexity=0.7"
```

**Example Response:**
```json
{
  "estimated_cost": 7.5150,
  "confidence_min": 6.3878,
  "confidence_max": 8.6423,
  "confidence_level": 0.85,
  "model_version": "v1.0.0",
  "predicted_at": "2024-01-15T10:30:00Z",
  "recommendations": [
    "GPT-4 detected - consider GPT-3.5-turbo for simpler tasks"
  ],
  "breakdown_by_action": {
    "baseline": 0.001,
    "tokens": 0.5,
    "complexity": 0.035,
    "multiplier": 6.979
  }
}
```

### Optimize Cost

Get optimization suggestions for reducing costs.

**Endpoint:** `POST /api/cost/optimize`

**Request Body:**
```json
{
  "tokens": 5000,
  "model_name": "gpt-4",
  "request_type": "completion",
  "complexity": 0.7
}
```

**Example Response:**
```json
{
  "current_cost": 7.5150,
  "optimized_cost": 0.1520,
  "savings": 7.363,
  "savings_percentage": 97.98,
  "recommendations": [
    {
      "action": "Switch to GPT-3.5-turbo",
      "estimated_cost": 0.1520,
      "confidence": 0.90
    },
    {
      "action": "Reduce token count to 3000",
      "estimated_cost": 4.5090,
      "confidence": 0.85
    }
  ]
}
```

---

## Security API

### Scan Code

Scan code for security vulnerabilities.

**Endpoint:** `POST /api/security/scan`

**Request Body:**
```json
{
  "code": "SELECT * FROM users WHERE id = \" + userId",
  "file_path": "src/database.go",
  "language": "go"
}
```

**Example Response:**
```json
{
  "total_vulnerabilities": 1,
  "vulnerabilities_by_severity": {
    "CRITICAL": 1,
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
  },
  "vulnerabilities": [
    {
      "id": "OWASP-A03-1",
      "title": "Potential SQL Injection",
      "description": "String concatenation in SQL queries can lead to SQL injection",
      "level": "CRITICAL",
      "category": "OWASP A03 - Injection",
      "file": "src/database.go",
      "line": 1,
      "code": "SELECT * FROM users WHERE id = \" + userId",
      "cwe": "CWE-89",
      "cve": "",
      "fix_suggestion": "Use parameterized queries or prepared statements",
      "detected_at": "2024-01-15T10:30:00Z"
    }
  ],
  "compliance_score": 80,
  "scan_duration": "150ms",
  "scanned_at": "2024-01-15T10:30:00Z",
  "status": "FAIL"
}
```

### Get Compliance Report

Get compliance report for multiple standards.

**Endpoint:** `GET /api/security/compliance`

**Query Parameters:**
- `repo_url` (string, required) - Repository URL
- `standards` (string, optional) - Comma-separated list of standards (default: all)

**Example Request:**
```bash
curl "http://localhost:8080/api/security/compliance?repo_url=https://github.com/user/repo&standards=SOC2,GDPR"
```

**Example Response:**
```json
{
  "standards": ["SOC2", "GDPR"],
  "checks": [
    {
      "standard": "SOC2",
      "requirement": "CC6.1 - Access Controls",
      "status": "PASS",
      "description": "Logical and physical access controls",
      "findings": [],
      "checked_at": "2024-01-15T10:30:00Z"
    },
    {
      "standard": "GDPR",
      "requirement": "Article 32 - Data Security",
      "status": "FAIL",
      "description": "Security of processing personal data",
      "findings": [
        "Potential unencrypted password - ensure encryption"
      ],
      "checked_at": "2024-01-15T10:30:00Z"
    }
  ],
  "overall_score": 75,
  "passed_checks": 3,
  "failed_checks": 1,
  "warning_checks": 0,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

---

## Gamification API (Planned)

### Get Achievements

List all achievements for a user.

**Endpoint:** `GET /api/achievements`

**Query Parameters:**
- `user_id` (string, required) - User ID

**Example Response:**
```json
{
  "achievements": [
    {
      "id": "first_pr",
      "name": "First PR",
      "description": "Submitted your first pull request",
      "points": 10,
      "earned_at": "2024-01-10T14:30:00Z"
    },
    {
      "id": "code_reviewer",
      "name": "Code Reviewer",
      "description": "Reviewed 10 pull requests",
      "points": 30,
      "earned_at": "2024-01-12T16:45:00Z"
    }
  ],
  "total_points": 40,
  "total_achievements": 2
}
```

### Get Leaderboard

Get top users on the leaderboard.

**Endpoint:** `GET /api/leaderboard`

**Query Parameters:**
- `limit` (int, optional) - Number of users to return (default: 10)

**Example Response:**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": "user123",
      "username": "john_doe",
      "total_points": 520,
      "achievements_count": 15,
      "prs_count": 45,
      "reviews_count": 30
    },
    {
      "rank": 2,
      "user_id": "user456",
      "username": "jane_smith",
      "total_points": 485,
      "achievements_count": 12,
      "prs_count": 38,
      "reviews_count": 42
    }
  ],
  "total_users": 100,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### Claim Achievement

Claim an achievement.

**Endpoint:** `POST /api/achievements/claim`

**Request Body:**
```json
{
  "user_id": "user123",
  "achievement_id": "bug_hunter"
}
```

**Example Response:**
```json
{
  "success": true,
  "achievement": {
    "id": "bug_hunter",
    "name": "Bug Hunter",
    "description": "Fixed 5 bugs",
    "points": 50,
    "earned_at": "2024-01-15T10:30:00Z"
  },
  "new_total_points": 570,
  "new_rank": 1
}
```

---

## Analytics API (Planned)

### Get Predictions

Get incident predictions.

**Endpoint:** `GET /api/analytics/predict`

**Query Parameters:**
- `window` (int, optional) - Prediction window in hours (default: 24)

**Example Response:**
```json
{
  "predictions": [
    {
      "incident_type": "high_error_rate",
      "probability": 0.75,
      "expected_time": "2024-01-15T18:00:00Z",
      "recommended_actions": [
        "Review recent deployments",
        "Check database connection pool"
      ],
      "confidence_level": 0.80
    }
  ]
}
```

### Get Anomalies

Get detected anomalies.

**Endpoint:** `GET /api/analytics/anomalies`

**Query Parameters:**
- `since` (string, optional) - ISO 8601 timestamp (default: last 24h)

**Example Response:**
```json
{
  "anomalies": [
    {
      "type": "request_spike",
      "detected_at": "2024-01-15T09:15:00Z",
      "severity": "MEDIUM",
      "description": "Request rate 300% above normal",
      "baseline": 100,
      "observed": 400,
      "recommendation": "Check for potential DDoS or traffic surge"
    }
  ],
  "total_anomalies": 1
}
```

---

## Collaboration API (Planned)

### Get Active Users

Get currently active users.

**Endpoint:** `GET /api/presence/users`

**Example Response:**
```json
{
  "users": [
    {
      "user_id": "user123",
      "username": "john_doe",
      "status": "online",
      "current_room": "project-alpha",
      "last_seen": "2024-01-15T10:30:00Z"
    },
    {
      "user_id": "user456",
      "username": "jane_smith",
      "status": "away",
      "current_room": "project-beta",
      "last_seen": "2024-01-15T10:25:00Z"
    }
  ],
  "total_online": 2
}
```

### Send Chat Message

Send a message to a chat room.

**Endpoint:** `POST /api/chat/message`

**Request Body:**
```json
{
  "room_id": "project-alpha",
  "user_id": "user123",
  "username": "john_doe",
  "message": "Just pushed the fix for issue #42",
  "message_type": "text"
}
```

**Example Response:**
```json
{
  "success": true,
  "message_id": "msg_abc123",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get Chat History

Get chat history for a room.

**Endpoint:** `GET /api/chat/history`

**Query Parameters:**
- `room_id` (string, required) - Room ID
- `limit` (int, optional) - Number of messages (default: 50)

**Example Response:**
```json
{
  "messages": [
    {
      "id": "msg_abc123",
      "room_id": "project-alpha",
      "user_id": "user123",
      "username": "john_doe",
      "message": "Just pushed the fix for issue #42",
      "message_type": "text",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_messages": 1,
  "has_more": false
}
```

---

## Voice API (Planned)

### Process Voice Command

Process a voice command.

**Endpoint:** `POST /api/voice/command`

**Request Body:**
```json
{
  "user_id": "user123",
  "command_text": "deploy to production",
  "language": "en",
  "confidence": 0.95
}
```

**Example Response:**
```json
{
  "success": true,
  "command_id": "cmd_xyz789",
  "action_taken": "deploy_initiated",
  "response": "Deploying to production environment",
  "execution_time_ms": 150
}
```

### Get Voice Capabilities

Get available voice commands.

**Endpoint:** `GET /api/voice/capabilities`

**Example Response:**
```json
{
  "wake_word": "hey tokyo",
  "supported_languages": ["en", "es", "ja"],
  "commands": [
    {
      "command": "deploy to {environment}",
      "description": "Deploy code to specified environment",
      "parameters": ["environment"]
    },
    {
      "command": "run tests",
      "description": "Execute test suite",
      "parameters": []
    }
  ],
  "total_commands": 50
}
```

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

**Common HTTP Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Rate Limiting

API requests are rate limited to 60 requests per minute per user. Rate limit information is included in response headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705320600
```

---

## Webhooks (Planned)

Tokyo-IA can send webhooks for various events:

- `scan.completed` - Security scan completed
- `vulnerability.detected` - New vulnerability detected
- `achievement.earned` - User earned achievement
- `incident.predicted` - Incident prediction generated

Configure webhooks in `config/features.yaml`:

```yaml
webhooks:
  enabled: true
  url: "https://your-domain.com/webhook"
  secret: "your-webhook-secret"
  events:
    - scan.completed
    - vulnerability.detected
```

---

## WebSocket API (Planned)

Real-time features use WebSocket connections:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Event:', data);
};
```

**Events:**
- `presence.update` - User presence changed
- `chat.message` - New chat message
- `scan.progress` - Scan progress update

---

For more information, see the [Features Documentation](FEATURES.md).
