from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Transport Status API")


class StatusUpdate(BaseModel):
    status: str
    updated_by: str


class Incident(BaseModel):
    order_id: str
    description: str
    severity: Optional[str] = "medium"


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/status/{order_id}")
def get_status(order_id: str):
    return {
        "order_id": order_id,
        "status": "in_transit"
    }


@app.patch("/status/{order_id}")
def update_status(order_id: str, payload: StatusUpdate):
    return {
        "order_id": order_id,
        "new_status": payload.status,
        "updated_by": payload.updated_by
    }


@app.post("/incidents")
def report_incident(incident: Incident):
    return {
        "message": "Incident registered",
        "incident": incident
    }
