from fastapi import FastAPI
from routes.branch import branch
from routes.subject import subject

app = FastAPI()

app.include_router(branch, prefix="/branches", tags=["branches"])
app.include_router(subject, prefix="/subjects", tags=["subjects"])
