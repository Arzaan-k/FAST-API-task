# 

# routes/user.py
from fastapi import APIRouter, HTTPException
from models.user import User
from config.db import conn
from schemas.user import serializeDict, serializeList
from bson import ObjectId

user = APIRouter()

@user.get('/')
async def find_all_users():
    try:
        users = serializeList(conn.local.user.find())
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.get('/{id}')
async def find_one_user(id: str):
    try:
        user = serializeDict(conn.local.user.find_one({"_id": ObjectId(id)}))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.post('/')
async def create_user(user: User):
    try:
        user_dict = user.dict()
        conn.local.user.insert_one(user_dict)
        return serializeDict(user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.put('/{id}')
async def update_user(id: str, user: User):
    try:
        user_dict = user.dict()
        update_result = conn.local.user.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user_dict}
        )
        if update_result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return serializeDict(conn.local.user.find_one({"_id": ObjectId(id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.delete('/{id}')
async def delete_user(id: str):
    try:
        delete_result = conn.local.user.find_one_and_delete({"_id": ObjectId(id)})
        if delete_result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return serializeDict(delete_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
