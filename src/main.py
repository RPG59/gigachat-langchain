import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.responses import PlainTextResponse
from langchain_community.chat_models import GigaChat

from src.review_manager import ReviewManager

APP_PORT = 3000

if os.getenv("GIGACHAT_CREDENTIALS") is None:
    raise ValueError("GIGACHAT_CREDENTIALS not found in environment variables")


class ReviewQuery(BaseModel):
    diff: str
    language: str


app = FastAPI()
review_manager = ReviewManager(GigaChat(verify_ssl_certs=False))


@app.on_event("startup")
def startup():
    print(f"Listen on port {APP_PORT}")


@app.post("/review", response_class=PlainTextResponse)
def query(query: ReviewQuery):
    return review_manager.review(query.diff, query.language)


@app.get("/health")
def health():
    return "Ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
