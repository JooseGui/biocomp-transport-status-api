# API Endpoints

Base URL (local): http://127.0.0.1:8000

## Health
GET /health

Response 200:
{
  "status": "ok"
}

## Get current status
GET /status/{order_id}

Response 200:
{
  "order_id": "123",
  "status": "IN_PREPARATION",
  "updated_at": "2026-01-08T12:00:00Z"
}

## Update status
PATCH /status/{order_id}

Request body:
{
  "new_status": "IN_TRANSIT"
}

Response 200:
{
  "order_id": "123",
  "previous_status": "IN_PREPARATION",
  "status": "IN_TRANSIT"
}
