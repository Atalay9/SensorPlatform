from pydantic import BaseModel, Field
from datetime import datetime


# Device Model
class DeviceModel(BaseModel):
    device_id: str = Field(..., example="SN-9942A", description="Cihazın benzersiz seri numarası")
    name: str = Field(..., example="Domates Tarlası Kuzey Sensörü")
    location: str = Field(..., example="A-Blok")
    is_active: bool = Field(default=True)

# Telemetry Model
class TelemetryModel(BaseModel):
    device_id: str = Field(..., example="SN-9942A")
    sensor_type: str = Field(..., example="soil_moisture", description="temperature, humidity vb.")
    value: float = Field(..., example=38.4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# 3. Alarm Model
class AlarmModel(BaseModel):
    device_id: str = Field(..., example="SN-9942A")
    title: str = Field(..., example="Kritik Düşük Nem Uyarısı")
    severity: str = Field(..., example="CRITICAL", description="INFO, WARNING, CRITICAL")
    is_resolved: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)