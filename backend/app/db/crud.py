from fastapi import HTTPException, Query
from sqlalchemy import select
from typing import Iterable
from models import *
from db import Session

# ===== VehiclePosition operations =====

# def create_vehiclepos(vp: VehiclePosition):
#     with Session() as session:
#         session.add(vp)
#         session.commit()
#         session.refresh(vp)
#         return vp

# def create_routes(routes: Iterable[RouteCreate]):
#     with Session(engine) as session:
#         creations: list[Route] = []
#         for route in routes:
#             db_route = Route.model_validate(route)
#             session.add(db_route)
#             session.commit()
#             session.refresh(db_route)
#             creations.append(db_route)
#         return creations
    
# def read_vehiclepos(*, vp_id: int, vehicle_id: str, trip_id: str, route_id: str):
#     with Session() as session:
#         statement = select(VehiclePosition) # Can also select indv columns
#         if vp_id:
#             return session.get(VehiclePosition, vp_id)
#         vp = session.scalars().get(VehiclePosition, vp_id)
#         if not vp:
#             raise HTTPException(404, "VehiclePosition not found")
#         return vp

# def read_routes(offset: int = 0, limit: int = Query(default=100, le=1000)):
#     with Session(engine) as session:
#         routes = session.exec(select(Route).offset(offset).limit(limit)).all()
#         return routes

# def update_route(route_id: int, route: RouteUpdate):
#     with Session(engine) as session:
#         db_route = session.get(Route, route_id)
#         if not db_route:
#             raise HTTPException(404, "Route not found")
#         route_data = route.model_dump(exclude_unset=True)
#         db_route.sqlmodel_update(route_data)
#         session.add(db_route)
#         session.commit()
#         session.refresh(db_route)
#         return db_route
    
# def delete_route(route_id: int):
#     with Session(engine) as session:
#         db_route = session.get(Route, route_id)
#         if not db_route:
#             raise HTTPException(404, "Route not found")
#         session.delete(db_route)
#         session.commit()
#         return {"ok": True}