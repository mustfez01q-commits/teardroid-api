import motor.motor_asyncio
import os

# Teri asali MongoDB link yahan hai
MONGO_URL = "mongodb+srv://a31692342_db_user:Arhambhai123@cluster0.cyrntn3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["teardroid_database"]

def client_db():
    return db["clients"]

def notification_db():
    return db["notifications"]

def command_db():
    return db["commands"]

def auth_db():
    return db["auth"]

async def tear_drive():
    return db["drive"]
