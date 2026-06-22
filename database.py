import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sensor_platform")

if MONGO_USER and MONGO_PASSWORD:
    MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
else:
    MONGO_DETAILS = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[MONGO_DB_NAME]
device_collection = database.get_collection("devices")
telemetry_collection = database.get_collection("telemetries")

async def add_device(device_data: dict) -> dict:
    """Veritabanına yeni cihaz ekler"""
    await device_collection.insert_one(device_data)
    return device_data

async def retrieve_devices() -> list:
    """Tüm cihazları listeler"""
    devices = []
    async for device in device_collection.find():
        device.pop("_id", None)
        devices.append(device)
    return devices

async def retrieve_device(device_id: str) -> dict:
    """Tek bir cihazı ID ile getirir"""
    device = await device_collection.find_one({"device_id": device_id})
    if device:
        device.pop("_id", None)
        return device

async def update_device_data(device_id: str, data: dict) -> bool:
    """Cihaz verilerini günceller"""
    device = await device_collection.find_one({"device_id": device_id})
    if device:
        await device_collection.update_one({"device_id": device_id}, {"$set": data})
        return True
    return False

async def delete_device_data(device_id: str) -> bool:
    """Cihazı siler"""
    device = await device_collection.find_one({"device_id": device_id})
    if device:
        await device_collection.delete_one({"device_id": device_id})
        return True
    return False

async def add_telemetry(telemetry_data: dict) -> dict:
    """Ses verisini zaman damgasıyla kaydeder"""
    await telemetry_collection.insert_one(telemetry_data)
    return telemetry_data

async def retrieve_telemetry_by_date(device_id: str, start_date: datetime, end_date: datetime) -> list:
    """Belirli bir cihaza ait, iki tarih arasındaki tüm telemetri kayıtlarını getirir"""
    telemetries = []
    query = {
        "device_id": device_id,
        "timestamp": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    async for telemetry in telemetry_collection.find(query):
        telemetry.pop("_id", None)
        telemetries.append(telemetry)
    return telemetries