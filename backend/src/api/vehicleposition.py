import pickle as pkl

from fastapi import APIRouter
from sqlalchemy import select

from ..db.db import Session
from ..db.models import VehiclePosition
from ..services.fetcher import load_from_cache, CACHE_PATH

router = APIRouter()

@router.get("/vehicleposition/live/{vehicle_id}", response_model=None)
def get_vehicleposition(vehicle_id: str) -> VehiclePosition | None:
    vehicle_dict = load_from_cache()
    return vehicle_dict.get(vehicle_id)

@router.get("/vehicleposition/live", response_model=None)
def get_vehiclepositions():
    return load_from_cache()

# @router.get("/vehiclepositions/history/{vehicle_id}", response_model=None)
# def get_vehicleposition(vp_id: int) -> VehiclePosition | None:
#     with Session() as session:
#         return session.get(VehiclePosition, vp_id)

# @router.get("/vehiclepositions/live/all", response_model=None)
# def get_vehiclepositions() -> list[VehiclePosition]:
#     return current_vehicles.copy()