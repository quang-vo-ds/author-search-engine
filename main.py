from app.app import handler
from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

@app.get("/")
def hello():
    return {"Hello": "World"}

@app.post("/query")
def query(research_filed: str, topk: int):
    result = handler(research_filed, topk)
    if not research_filed or not topk:
        raise HTTPException(status_code=404, detail="Research field and topk are required")
    return {"result": result}

