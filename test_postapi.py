import requests

url = "http://127.0.0.1:8000/items/"  # Update this URL if your API is hosted elsewhere

data = {
    "name": "Laptop",
    "price": 1200.50,   
    "in_stock": True
}


def data_manipulate(data):
    response = requests.post(url, json=data).json()
    response['offer_price']=int(response['price']*0.8)
    
    print(response)
    
data_manipulate(data)