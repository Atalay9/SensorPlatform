from fastapi import FastAPI, HTTPException, status
from models import DeviceModel
from database import device_collection

app = FastAPI(title="Sensor Platform API")


# CREATE
@app.post("/devices/", status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceModel):
    # Check Existing Device
    existing_device = await device_collection.find_one({"device_id": device.device_id})
    if existing_device:
        raise HTTPException(status_code=400, detail="Device already exists")

    await device_collection.insert_one(device.dict())
    return {"message": "Device created successfully", "device_id": device.device_id}


# READ FOR ALL DEVICES
@app.get("/devices/")
async def get_devices():
    devices = []
    async for device in device_collection.find():
        device.pop("_id", None)
        devices.append(device)
    return devices


# READ FOR SPESIFIC DEVICE
@app.get("/devices/{device_id}")
async def get_device(device_id: str):
    device = await device_collection.find_one({"device_id": device_id})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.pop("_id", None)
    return device


# UPDATE
@app.put("/devices/{device_id}")
async def update_device(device_id: str, updated_device: DeviceModel):
    device = await device_collection.find_one({"device_id": device_id})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    await device_collection.update_one(
        {"device_id": device_id}, {"$set": updated_device.dict()}
    )
    return {"message": "Device updated successfully"}


# DELETE
@app.delete("/devices/{device_id}")
async def delete_device(device_id: str):
    device = await device_collection.find_one({"device_id": device_id})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    await device_collection.delete_one({"device_id": device_id})
    return {"message": "Device deleted successfully"}
