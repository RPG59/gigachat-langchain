import os
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from outline import Outline
from searcher import Searcher
from update_documents import update_documents
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from qdrant_client import QdrantClient
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_community.chat_models.gigachat import GigaChat
from starlette.templating import Jinja2Templates
import uvicorn

if os.getenv("GIGACHAT_CREDENTIALS") is None:
    raise ValueError("GIGACHAT_CREDENTIALS environment variable not set")

qdrant_url = os.getenv("QDRANT_URL")

if qdrant_url is None:
    ValueError("QDRANT_URL environment variable not set")

logging.basicConfig(level=logging.INFO)


class Query(BaseModel):
    data: str


outline = Outline()
qdrant_client = QdrantClient(qdrant_url)
embeddings = GigaChatEmbeddings(scope="GIGACHAT_API_CORP", verify_ssl_certs=False)
searcher = Searcher(GigaChat(model="GigaChat-Pro", scope="GIGACHAT_API_CORP", verify_ssl_certs=False), qdrant_client,
                    embeddings)
app = FastAPI()
templates = Jinja2Templates(directory="src/frontend-templates")


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # Every 24 hours
def update():
    update_documents(outline, qdrant_url, qdrant_client, embeddings)


@app.post("/query")
def query(query: Query):
    answer = searcher.search(query.data)

    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found in context")

    return {"data": answer}


@app.post("/test", response_class=HTMLResponse)
def query(query: Query):
    return '<tr><td>Joe Smith</td><td>joe@smith.com</td></tr>'


@app.get("/health")
def health():
    return "Ok"


app.mount("/", StaticFiles(directory="src/frontend-templates", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
