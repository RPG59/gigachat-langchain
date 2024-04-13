import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from src.searcher import Searcher

APP_PORT = 3000

if os.getenv("GIGACHAT_CREDENTIALS") is None:
    raise ValueError("GIGACHAT_CREDENTIALS not found in environment variables")


class Query(BaseModel):
    data: str


app = FastAPI()
searcher = Searcher()

@app.on_event("startup")
def startup():
    print(f"Listen on port {APP_PORT}")


@app.post("/query")
def query(query: Query):
    return searcher.search(query.data)


@app.get("/health")
def health():
    return "Ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
