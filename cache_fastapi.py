# FastAPI CSV Caching Example
from fastapi import FastAPI, HTTPException
import pandas as pd
from functools import lru_cache
from typing import Dict, Any

# Load the CSV file and create a cache
class DataCache:
    def __init__(self, csv_path: str):
        """
        Initialize the data cache by loading the CSV file
        """
        try:
            self.data = pd.read_csv(csv_path)
            # Convert the DataFrame to a dictionary for faster lookups
            self.data_dict = self.data.set_index('id').to_dict(orient='index')
        except Exception as e:
            raise RuntimeError(f"Error loading CSV file: {e}")

    def get_item(self, item_id: int) -> Dict[str, Any]:
        """
        Retrieve an item by its ID
        """
        item = self.data_dict.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

# Create the FastAPI app
app = FastAPI(title="CSV Cache Example")

# Global cache variable
_data_cache = None

@lru_cache(maxsize=1)
def get_data_cache() -> DataCache:
    """
    Cached function to load the CSV file
    Uses lru_cache to ensure the file is loaded only once
    """
    global _data_cache
    if _data_cache is None:
        _data_cache = DataCache('products.csv')
    return _data_cache

# Endpoint to get a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    Retrieve an item from the cached CSV data
    """
    cache = get_data_cache()
    return cache.get_item(item_id)

# Endpoint to get all items (demonstrating cache usage)
@app.get("/items")
async def list_items():
    """
    List all items from the cached CSV data
    """
    cache = get_data_cache()
    return list(cache.data_dict.values())

# Example of a CSV file (products.csv) that would be used with this application
# id,name,price,category
# 1,Laptop,999.99,Electronics
# 2,Smartphone,599.99,Electronics
# 3,Headphones,199.99,Accessories
# 4,Smartwatch,249.99,Wearables