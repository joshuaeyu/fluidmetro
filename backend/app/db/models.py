from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class VehiclePosition(Base): # Data model
    __tablename__ = "vehicle_position"

    id: Mapped[int] = mapped_column(primary_key=True)

    timestamp: Mapped[int] = mapped_column(index=True)
    
    route_id: Mapped[str | None]
    vehicle_id: Mapped[str]
    vehicle_label: Mapped[str]
    
    trip_id: Mapped[str | None]
    
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    speed: Mapped[float | None]
    bearing: Mapped[float | None]
    odometer: Mapped[float | None]

# delete config options
# - cascade_delete=True, ondelete="CASCADE"
# - ondelete="SET NULL"
# - passive_deletes="all", ondelete="SET NULL"
# - passive_deletes="all", ondelete="RESTRICT"

# Use a link table for many-to-many relationships