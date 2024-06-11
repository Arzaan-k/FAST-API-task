# routes/branch.py
from fastapi import APIRouter, HTTPException
from models.branch import Branch
from models.subject import Subject
from config.db import conn
from schemas.utils import serialize_dict, serialize_list
from bson import ObjectId

branch = APIRouter()

@branch.get('/')
async def find_all_branches():
    try:
        branches = serialize_list(conn.local.branch.find())
        return branches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@branch.get('/{id}')
async def find_one_branch(id: str):
    try:
        branch = serialize_dict(conn.local.branch.find_one({"_id": ObjectId(id)}))
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found")

        # Fetch subjects related to the branch
        subjects = serialize_list(conn.local.subject.find({"branch_id": id}))
        branch["subjects"] = subjects

        return branch
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@branch.post('/')
async def create_branch(branch: Branch):
    try:
        branch_dict = branch.dict()
        conn.local.branch.insert_one(branch_dict)
        return serialize_dict(branch_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@branch.put('/{id}')
async def update_branch(id: str, branch: Branch):
    try:
        branch_dict = branch.dict()
        update_result = conn.local.branch.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": branch_dict}
        )
        if update_result is None:
            raise HTTPException(status_code=404, detail="Branch not found")
        return serialize_dict(conn.local.branch.find_one({"_id": ObjectId(id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@branch.delete('/{id}')
async def delete_branch(id: str):
    try:
        delete_result = conn.local.branch.find_one_and_delete({"_id": ObjectId(id)})
        if delete_result is None:
            raise HTTPException(status_code=404, detail="Branch not found")
        return serialize_dict(delete_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
