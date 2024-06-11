# routes/subject.py
from fastapi import APIRouter, HTTPException
from models.subject import Subject
from config.db import conn
from schemas.utils import serialize_dict, serialize_list
from bson import ObjectId

subject = APIRouter()

@subject.get('/')
async def find_all_subjects():
    try:
        subjects = serialize_list(conn.local.subject.find())
        return subjects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@subject.get('/{id}')
async def find_one_subject(id: str):
    try:
        subject = serialize_dict(conn.local.subject.find_one({"_id": ObjectId(id)}))
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@subject.post('/')
async def create_subject(subject: Subject):
    try:
        subject_dict = subject.dict()
        conn.local.subject.insert_one(subject_dict)
        return serialize_dict(subject_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@subject.put('/{id}')
async def update_subject(id: str, subject: Subject):
    try:
        subject_dict = subject.dict()
        update_result = conn.local.subject.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": subject_dict}
        )
        if update_result is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        return serialize_dict(conn.local.subject.find_one({"_id": ObjectId(id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@subject.delete('/{id}')
async def delete_subject(id: str):
    try:
        delete_result = conn.local.subject.find_one_and_delete({"_id": ObjectId(id)})
        if delete_result is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        return serialize_dict(delete_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
