# models/branch.py
from pydantic import BaseModel
from typing import List

class Branch(BaseModel):
    name: str
    students_enrolled: int
