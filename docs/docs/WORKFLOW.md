# Workflow (Order/Dispatch Status)

This API models a simple state workflow for dispatch/order tracking.

## Statuses

| Status | Meaning |
|---|---|
| in_preparation | Order created and being prepared |
| in_transit | Shipment is moving |
| delivered | Shipment delivered to destination |
| cancelled | Shipment cancelled |

## Allowed transitions

| From | To |
|---|---|
| in_preparation | in_transit, cancelled |
| in_transit | delivered |
| delivered | (final) |
| cancelled | (final) |

## Roles (who can change what)

| Role | Allowed actions |
|---|---|
| dispatcher | Update status, log events |
| ops | Report incidents |
| admin | Any operation (future scope) |

## Notes
- This is a minimal workflow model to demonstrate API design + business rules.
- Persistence (database), authentication and background jobs (email notifications) are planned next steps.
