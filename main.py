
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Voorbeelddata
service_points = [
    {"id": 1, "name": "SP A", "location": "Amsterdam", "status": "pending", "next_pickup_time": "2024-11-26T15:00:00"},
    {"id": 2, "name": "SP B", "location": "Rotterdam", "status": "completed", "next_pickup_time": "2024-11-26T16:00:00"},
]

rides = [
    {"id": 101, "sp_id": 1, "driver": "John Doe", "pickup_time": "2024-11-26T14:50:00"},
    {"id": 102, "sp_id": 2, "driver": "Jane Smith", "pickup_time": "2024-11-26T15:50:00"},
]

alerts = []


class Ride(BaseModel):
    id: int
    sp_id: int
    driver: str
    pickup_time: datetime


class ServicePoint(BaseModel):
    id: int
    name: str
    location: str
    status: str
    next_pickup_time: datetime


@app.get("/service-points", response_model=List[ServicePoint])
def get_service_points():
    return service_points


@app.get("/service-points/{sp_id}/rides", response_model=List[Ride])
def get_rides_for_service_point(sp_id: int):
    return [ride for ride in rides if ride["sp_id"] == sp_id]


@app.get("/alerts")
def get_alerts():
    global alerts
    current_time = datetime.now()
    alerts = [
        {
            "sp_id": sp["id"],
            "alert_type": "te laat" if datetime.fromisoformat(sp["next_pickup_time"]) < current_time else "te vroeg",
        }
        for sp in service_points
        if sp["status"] == "pending"
    ]
    return alerts
