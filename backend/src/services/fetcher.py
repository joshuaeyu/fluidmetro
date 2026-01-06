import pathlib
import pickle as pkl
import time

from google.protobuf.message import Message
from google.transit import gtfs_realtime_pb2
import httpx
from sqlalchemy import func, select

from ..db.db import Session, create_db_and_tables
from ..db.models import VehiclePosition
from ..util.util import read_api_key

CACHE_PATH: pathlib.Path = pathlib.Path(__file__).parents[2].joinpath("data/cache.pkl").resolve()
FETCH_INTERVAL: int = 60
MAX_NUM_RECORDS: int = 1_000_000

current_vehicles: list[VehiclePosition] = []

def fetch_vehicle_positions() -> Message:
  # HTTP GET
  url = "http://api.511.org/transit/vehiclepositions"
  params = {'api_key': read_api_key(), 'agency': "SF"}
  res = httpx.get(url, params=params, timeout=60.0)
  # Parse protobuf
  message: Message = gtfs_realtime_pb2.FeedMessage()
  message.ParseFromString(res.content)
  return message

def convert_msg_to_objects(message: Message) -> list[VehiclePosition]:
  vehicles: list[VehiclePosition] = []
  for entity in message.entity:
    if entity.vehicle.HasField("trip"):
      vehicle_msg = entity.vehicle.vehicle
      trip_msg = entity.vehicle.trip
      position_msg = entity.vehicle.position
      vehicle = VehiclePosition(
        timestamp_fetch=message.header.timestamp,
        timestamp=entity.vehicle.timestamp,
        trip_id=trip_msg.trip_id,
        route_id=trip_msg.route_id,
        vehicle_id=vehicle_msg.id,
        vehicle_label=vehicle_msg.label,
        latitude=position_msg.latitude,
        longitude=position_msg.longitude,
        speed=position_msg.speed,
        bearing=position_msg.bearing,
        odometer=position_msg.odometer
      )
      vehicles.append(vehicle)
  return vehicles

def save_to_cache(vehicles: dict[str, VehiclePosition]) -> None:
  with open(CACHE_PATH, 'wb') as file:
    pkl.dump(vehicles, file)

def load_from_cache() -> dict[str, VehiclePosition]:
  with open(CACHE_PATH, 'rb') as file:
    return pkl.load(file)

# While running, fetch positions every 60 seconds and update database
def run() -> None:
  while True:
    # Fetch vehicle positions
    msg = fetch_vehicle_positions()
    vehicles = convert_msg_to_objects(msg)
    # Update database and cache
    if vehicles:
      current_vehicles = vehicles
      # Update database
      with Session() as session:
        session.add_all(current_vehicles)
        session.commit()
        for vp in session.scalars(select(VehiclePosition)).all():
          print(vp.__dict__)
        count = session.execute(select(func.count(VehiclePosition.id))).scalar_one()
        print(f"VehiclePosition database size: {count}")
        if count > MAX_NUM_RECORDS:
          print(f"The number of VehiclePosition records has exceeded the configured max of {MAX_NUM_RECORDS}.")
      # Update cache file
      vehicles_dict = {vp.vehicle_id: vp for vp in vehicles}
      save_to_cache(vehicles_dict)
    # Sleep
    print(f"Sleeping for {FETCH_INTERVAL} seconds...")
    time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
  create_db_and_tables()
  run()

# message (FeedMessage)
# - header (FeedHeader)
#   - gtfs_realtime_version (string)
#   - incrementality (Incrementality)
#   - timestamp (uint64)
#   - feed_version (string)
# - entity (FeedEntity, many)
#   - id (string)
#   - is_deleted (bool)
#   - trip_update (TripUpdate)
#   - vehicle (VehiclePosition)
#     - trip (TripDescriptor)
#       - trip_id (string)
#       - route_id (string)
#       - direction_id (uint32)
#       - start_time (string)
#       - start_date (string)
#       - schedule_relationship (ScheduleRelationship)
#       - modified_trip (ModifiedTripSelector)
#     - vehicle (VehicleDescriptor)
#       - id (string)
#       - label (string)
#       - license_plate (string)
#       - wheelchair_accessible (WheelchairAccessible)
#       - id (string)
#     - position (Position)
#       - latitude (float)
#       - longitude (float)
#       - bearing (float)
#       - odometer (float)
#       - speed (float)
#     - current_stop_sequence (uint32)
#     - stop_id (string)
#     - current_status (VehicleStopStatus)
#     - timestamp (uint64)
#     - congestion_level (CongestionLevel)
#     - occupancy_status (OccupancyStatus)
#     - occupancy_percentage (uint32)
#     - multi_carriage_details (CarriageDetails)
#   - alert (Alert)
#   - shape (Shape)
#   - stop (Stop)
#   - trip_modifications (TripModifications)