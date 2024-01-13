import os

from fastapi import FastAPI
from pydantic import BaseModel
from outline import Outline
from searcher import Searcher
from update_documents import update_documents
from fastapi_utils.tasks import repeat_every
from qdrant_client import QdrantClient
import uvicorn


class Query(BaseModel):
    data: str


qdrant_url = os.getenv("QDRANT_URL")

if qdrant_url is None:
    ValueError("Invalid QDRANT_URL")

outline = Outline()
qdrant_client = QdrantClient(qdrant_url)
searcher = Searcher(qdrant_client)
app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)
def update():
    update_documents(outline, qdrant_url, qdrant_client)


@app.post("/query")
def query(query: Query):
    return searcher.search(query.data)


@app.get("/health")
def health():
    return "Ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
