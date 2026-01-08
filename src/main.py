from datetime import datetime
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Transport Status & Notifications API",
    version="0.1.0",
    description="Minimal API demo: workflow-based dispatch tracking and notifications.",
)

# ---- In-memory demo store (no DB yet) ----
ORDERS = {
    "GD-1001": {"order_id": "GD-1001", "status": "in_preparation", "updated_at": datetime.utcnow().isoformat()},
    "GD-1002": {"order_id": "GD-1002", "status": "in_transit", "updated_at": datetime.utcnow().isoformat()},
}

AllowedStatus = Literal["in_preparation", "in_transit", "delivered", "closed"]


class EventIn(BaseModel):
    order_id: str = Field(..., examples=["GD-1001"])
    event_type: Literal["created", "status_changed", "incident_reported", "pod_uploaded"] = Field(
        ..., examples=["status_changed"]
    )
    message: Optional[str] = Field(None, examples=["Moved to In Transit"])


class StatusPatch(BaseModel):
    status: AllowedStatus = Field(..., examples=["delivered"])
    changed_by: Optional[str] = Field(None, examples=["dispatcher"])


class IncidentIn(BaseModel):
    order_id: str = Field(..., examples=["GD-1001"])
    severity: Literal["low", "medium", "high"] = Field(..., examples=["medium"])
    description: str = Field(..., examples=["Package damaged during loading"])
    reported_by: Optional[str] = Field(None, examples=["driver"])


class PodIn(BaseModel):
    order_id: str = Field(..., examples=["GD-1001"])
    pod_url: str = Field(..., examples=["https://example.com/pod/GD-1001.pdf"])


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


@app.get("/health")
def health():
    return {"status": "ok", "time_utc": _now_iso()}


@app.get("/status/{order_id}")
def get_status(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/status")
def list_status():
    return {"items": list(ORDERS.values())}


@app.post("/events", status_code=201)
def create_event(payload: EventIn):
    # Minimal demo: just validate order exists and echo event
    if payload.order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"received": payload.model_dump(), "time_utc": _now_iso()}


@app.patch("/status/{order_id}")
def update_status(order_id: str, payload: StatusPatch):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Very simple workflow rule (demo)
    current = order["status"]
    next_status = payload.status

    allowed = {
        "in_preparation": {"in_transit"},
        "in_transit": {"delivered"},
        "delivered": {"closed"},
        "closed": set(),
    }

    if next_status not in allowed[current]:
        raise HTTPException(
            status_code=409,
            detail=f"Invalid transition: {current} -> {next_status}",
        )

    order["status"] = next_status
    order["updated_at"] = _now_iso()
    order["changed_by"] = payload.changed_by or "system"
    return order


@app.post("/incidents", status_code=201)
def create_incident(payload: IncidentIn):
    if payload.order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"incident": payload.model_dump(), "time_utc": _now_iso()}


@app.post("/pod", status_code=201)
def upload_pod(payload: PodIn):
    if payload.order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"pod": payload.model_dump(), "time_utc": _now_iso()}
