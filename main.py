from typing import Union
import requests

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from search import run_search


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Query(BaseModel):
    data: str


@app.post("/query")
def query():
    res_data = run_search()
    return {"res": res_data}


@app.get("/")
def read_root():
    data = requests.get("https://607ea67e02a23c0017e8bcd6.mockapi.io/foo").json()
    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
