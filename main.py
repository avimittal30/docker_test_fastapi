from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool


output_json={}
@app.post("/items/")
def create_item(item: Item):
    output_json['item_name']=item.name
    output_json['price']=item.price
    output_json['offer_price']=item.price*0.8
    return output_json


# app = FastAPI()
# @app.post("/items/")
# def create_item(item: dict):  # Accept raw dictionary
#     return {"item_name": item.get("name"), "price": item.get("price")}


# from fastapi import FastAPI, Request

# app = FastAPI()

# @app.post("/items/")
# async def create_item(request: Request):
#     data = await request.json()  # Extract raw JSON data
#     print(data)
#     return {"item_name": data.get("name"), "price": data.get("price")}