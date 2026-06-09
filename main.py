from fastapi import FastAPI, HTTPException, status
from models import DeviceModel
from database import (
    retrieve_device,
    add_device,
    retrieve_devices,
    update_device_data,
    delete_device_data
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