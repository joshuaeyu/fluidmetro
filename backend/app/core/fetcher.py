import httpx
from google.protobuf.message import Message
from google.transit import gtfs_realtime_pb2

from util.util import read_api_key
from db.models import VehiclePosition
from db.db import Session
from sqlalchemy import select
import time

def request_vehicle_positions() -> httpx.Response:
  url = "http://api.511.org/transit/vehiclepositions"
  params = {'api_key': read_api_key(), 'agency': "SF"}
  r = httpx.get(url, params=params, timeout=60.0)
  return r

def save_vehicle_positions(positions: str) -> None:
  with open("positions.txt", 'wt') as f:
    f.write(positions)

def response_to_pbmessage(response: httpx.Response) -> Message:
  message: Message = gtfs_realtime_pb2.FeedMessage()
  message.ParseFromString(response.content)
  return message

# While running, fetch positions every 60 seconds and update database
def run():
  update_cooldown = 0
  res = request_vehicle_positions()
  msg = response_to_pbmessage(res)
  res_timestamp = msg.header.timestamp
  vehicles = []
  for entity in msg.entity:
    if entity.id in vehicles:
      print("duplicate")
    if entity.vehicle.HasField("trip"):
      vehicle = entity.vehicle.vehicle
      trip = entity.vehicle.trip
      position = entity.vehicle.position
      vehicles.append(VehiclePosition(
        timestamp=entity.vehicle.timestamp,
        route_id=trip.route_id,
        vehicle_id=vehicle.id,
        vehicle_label=vehicle.label,
        trip_id=trip.trip_id,
        latitude=position.latitude,
        longitude=position.longitude,
        speed=position.speed,
        bearing=position.bearing,
        odometer=position.odometer
      ))
  with Session() as session:
    session.add_all(vehicles)
    session.commit()
    for vp in session.scalars(select(VehiclePosition)).all():
      print(vp.__dict__)

  # while True:
  #   if update_cooldown >= 60:
  #     update_cooldown = 0
  #   else:
  #     update_cooldown += 1

if __name__ == "__main__":
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