# Transport Status & Notifications API

Backend/API project focused on workflow automation, traceability and notifications.

## What it does

- Tracks order/dispatch status through a state workflow (e.g. In Preparation → In Transit → Delivered)
- Logs events when a dispatch guide is created or updated
- Sends email notifications on status changes
- Allows incident reporting with description and alert email
- Supports proof-of-delivery upload and workflow closure

## Tech stack

- Python
- REST API architecture
- SQL (relational database)
- Email notifications (SMTP / service-based)
- Modular backend structure

## Project structure

```text
/src        # Application source code
/docs       # API documentation and diagrams
## Run locally
API docs (Swagger): http://127.0.0.1:8000/docs

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn src.main:app --reload
## Endpoints (summary)

GET  /health  
GET  /status/{order_id}  
PATCH /status/{order_id}  
POST /incidents  

More details: see `docs/ENDPOINTS.md` and `docs/WORKFLOW.md`.
