from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from models import DeviceModel, VolumeInputModel
from database import (
    retrieve_device,
    add_device,
    retrieve_devices,
    update_device_data,
    delete_device_data,
    add_telemetry
)

app = FastAPI(title="Sensor Platform API")

# CREATE
@app.post("/devices/", status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceModel):
    existing_device = await retrieve_device(device.device_id)
    if existing_device:
        raise HTTPException(status_code=400, detail="Device already exists")

    # .dict() yerine .model_dump() kullanıldı
    await add_device(device.model_dump())
    return {"message": "Device created successfully", "device_id": device.device_id}

# READ FOR ALL DEVICES
@app.get("/devices/")
async def get_devices():
    devices = await retrieve_devices()
    return devices

# READ FOR SPECIFIC DEVICE
@app.get("/devices/{device_id}")
async def get_device(device_id: str):
    device = await retrieve_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# UPDATE
@app.put("/devices/{device_id}")
async def update_device(device_id: str, updated_device: DeviceModel):
    if updated_device.device_id != device_id:
        raise HTTPException(
            status_code=400,
            detail="Device ID in path and body must match"
        )

    success = await update_device_data(device_id, updated_device.model_dump())
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device updated successfully"}

# DELETE
@app.delete("/devices/{device_id}")
async def delete_device(device_id: str):
    success = await delete_device_data(device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}


@app.post("/devices/{device_id}/telemetry", status_code=status.HTTP_201_CREATED)
async def post_telemetry(device_id: str, telemetry_in: VolumeInputModel):
    # 1. Kontrol: Bu cihaz sistemde kayıtlı mı?
    device = await retrieve_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found. Register the device first.")

    # 2. Veritabanına kaydedilecek dökümanı kurumsal standartta (zaman damgasıyla) hazırlıyoruz
    telemetry_payload = {
        "device_id": device_id,
        "sensor_type": "sound_level",
        "value": telemetry_in.volume,
        "timestamp": datetime.utcnow()  # Tarihsel sorgular için kritik öneme sahip
    }

    await add_telemetry(telemetry_payload)
    return {"message": "Telemetry saved successfully", "device_id": device_id}