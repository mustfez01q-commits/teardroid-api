from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database import auth_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# MongoDB collection instance
auth_collection = auth_db()

class client(BaseModel):
    username: str
    password: str

class password(BaseModel):
    old_password: str
    new_password: str

async def check_auth():
    # MongoDB mein find() use hota hai fetch() nahi
    user_exists = await auth_collection.find_one({"username": "admin"})
    if not user_exists:
        await auth_collection.insert_one({"username": "admin", "password": "admin"})

@router.post("/login")
async def add_client(client: client, Authorize: AuthJWT = Depends()):
    # MongoDB find_one use kar rahe hain
    user = await auth_collection.find_one({"username": client.username, "password": client.password})
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    access_token = Authorize.create_access_token(subject=client.username, expires_time=False)
    return JSONResponse({
        "success": True,
        "token": access_token,
        "message": "login successfully",
    })

@router.post("/password/change")
async def get_client(password: password, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    
    # Purane password ko dhoondo
    user = await auth_collection.find_one({"password": password.old_password})
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect old password")
    
    # Password update karo
    await auth_collection.update_one(
        {"_id": user["_id"]}, 
        {"$set": {"password": password.new_password}}
    )
    return JSONResponse({"success": True, "message": "password changed successfully"})
