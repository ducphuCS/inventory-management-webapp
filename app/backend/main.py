from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

# Configuration for GinServices
GIN_SERVICES_URL = os.environ.get("GIN_SERVICES_URL", "http://inventory-service:8080/v1")

app = FastAPI(title="Prototype WebApp API", description="A FastAPI backend bridging to GinServices.")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float # Map to stock_count for compatibility with frontend for now

def gin_fetch_analysis(item_id: str):
    """
    Dedicated function to call GinServices for product analysis.
    The correct GinServices route is: GET /v1/items/:id/analysis
    """
    try:
        url = f"{GIN_SERVICES_URL}/items/{item_id}/analysis"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling GinServices analysis: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prototype WebApp API (bridged to GinServices)!"}

@app.get("/items/")
def get_items():
    try:
        response = requests.get(f"{GIN_SERVICES_URL}/items")
        response.raise_for_status()
        data = response.json()
        
        items = []
        for item in data.get("items", []):
            items.append({
                "id": str(item["id"]),
                "name": item["product_name"],
                "description": item["item_details"],
                "price": float(item["stock_count"])
            })
        return {"items": items}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to GinServices: {str(e)}")

@app.get("/items/{item_id}/analyze")
def analyze_item_endpoint(item_id: str):
    """
    Endpoint for WebApp frontend to trigger the analysis from inventory-service.
    """
    data = gin_fetch_analysis(item_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found or analysis failed")
    
    # Extract only the python analysis result
    return data.get("python_analysis", {})

@app.get("/items/{item_id}")
def get_item(item_id: str):
    """
    Return basic item info (without analysis by default, or with it if needed).
    """
    try:
        # We can reuse the analysis endpoint as it also includes item_info
        data = gin_fetch_analysis(item_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        item_info = data["item_info"]
        return {
            "id": str(item_info["id"]),
            "name": item_info["product_name"],
            "description": item_info["item_details"],
            "price": float(item_info["stock_count"]),
            "analysis_snapshot": data.get("python_analysis")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/items/")
def create_item(item: Item):
    try:
        payload = {
            "product_name": item.name,
            "stock_count": int(item.price), # Using price as stock_count for POC
            "item_details": item.description
        }
        response = requests.post(f"{GIN_SERVICES_URL}/items", json=payload)
        response.raise_for_status()
        data = response.json()
        
        return {
            "id": str(data["id"]),
            "name": data["product_name"],
            "description": data["item_details"],
            "price": float(data["stock_count"])
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error creating item in GinServices: {str(e)}")
