# main.py

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()
items_db = []

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
     item_dict = {"item_id": item_id, **item.dict()}
     items_db.append(item_dict)
     return item_dict

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in items_db:
        if item["item_id"] == item_id:
            return item
    return {"message": "Item not found"}