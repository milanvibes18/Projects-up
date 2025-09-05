from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)      # e.g., health, environment
    model = Column(String)                     # device model, e.g., MAX30102
    location = Column(String)                  # e.g., ICU Room 2
    timezone = Column(String, default="UTC")   # timezone for data
    firmware = Column(String)                  # firmware version
    sampling_rate = Column(Integer)            # in seconds

    readings = relationship("DeviceData", back_populates="device")

class DeviceData(Base):
    __tablename__ = "device_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)

    device = relationship("Device", back_populates="readings")
