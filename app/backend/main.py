from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Prototype WebApp API", description="A FastAPI backend for a Streamlit frontend.")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

# In-memory database
db = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prototype WebApp API!"}

@app.get("/items/")
def get_items():
    return {"items": list(db.values())}

@app.post("/items/")
def create_item(item: Item):
    item_id = str(int(time.time() * 1000))
    db[item_id] = {"id": item_id, **item.model_dump()}
    return db[item_id]

@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]
