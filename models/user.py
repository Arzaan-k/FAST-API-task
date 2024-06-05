# models/user.py
from pydantic import BaseModel
from typing import List

class Subject(BaseModel):
    nameofSubject: str
    TotalNoOfChapters: int

class User(BaseModel):
    branchname: str
    studentsenrolled: str
    subjects: List[Subject]
