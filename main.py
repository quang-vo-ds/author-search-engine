from app.app import handler
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello!"

@app.post("/query")
def query(research_filed: str, topk: int):
    result = handler(research_filed, topk)
    return {"result": result}

