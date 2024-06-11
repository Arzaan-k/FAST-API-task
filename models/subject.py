
# models/subject.py
from pydantic import BaseModel

class Subject(BaseModel):
    name: str
    total_no_of_chapters: int
    branch_id: str
