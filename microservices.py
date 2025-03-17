from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Product Service
class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# Inventory Service
class InventoryItem(BaseModel):
    product_id: int
    quantity: int

# Product Catalog Microservice
class ProductService:
    def __init__(self):
        self.products = [
            Product(id=1, name="Laptop", category="Electronics", price=999.99, description="High-performance laptop", in_stock=True),
            Product(id=2, name="Smartphone", category="Electronics", price=599.99, description="Latest model smartphone", in_stock=True),
            Product(id=3, name="Headphones", category="Electronics", price=199.99, description="Noise-canceling wireless headphones", in_stock=False)
        ]
    
    def get_all_products(self) -> List[Product]:
        return self.products
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return next((product for product in self.products if product.id == product_id), None)
    
    def create_product(self, product: Product) -> Product:
        if any(p.id == product.id for p in self.products):
            raise HTTPException(status_code=400, detail="Product ID already exists")
        self.products.append(product)
        return product

# Inventory Microservice
class InventoryService:
    def __init__(self):
        self.inventory = [
            InventoryItem(product_id=1, quantity=50),
            InventoryItem(product_id=2, quantity=100),
            InventoryItem(product_id=3, quantity=0)
        ]
    
    def get_inventory_for_product(self, product_id: int) -> Optional[InventoryItem]:
        return next((item for item in self.inventory if item.product_id == product_id), None)
    
    def update_inventory(self, product_id: int, quantity: int) -> InventoryItem:
        inventory_item = self.get_inventory_for_product(product_id)
        if inventory_item:
            inventory_item.quantity = quantity
            return inventory_item
        print(inventory_item)
        new_item = InventoryItem(product_id=product_id, quantity=quantity)
        self.inventory.append(new_item)
        return new_item

# Create a single FastAPI application with all routes
app = FastAPI(
    title="E-Commerce Microservices API",
    description="Comprehensive API for Product Catalog and Inventory Management",
    version="1.0.0"
)

# Initialize services
product_service = ProductService()
inventory_service = InventoryService()

# Product Catalog Endpoints
@app.get("/products", response_model=List[Product], tags=["Products"])
async def list_products():
    """
    Retrieve all products in the catalog
       - Returns a list of all available products
    """
    print(product_service.get_all_products())
    return product_service.get_all_products()

@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(product_id: int):
    """
    Retrieve a specific product by its ID
    - Requires a valid product ID
    - Returns detailed product information
    """
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, tags=["Products"])
async def create_product(product: Product):
    """
    Create a new product in the catalog
    - Requires a unique product ID
    - Returns the created product details
    """
    return product_service.create_product(product)

# Inventory Endpoints
@app.get("/inventory/{product_id}", response_model=InventoryItem, tags=["Inventory"])
async def get_inventory(product_id: int):
    """
    Get inventory details for a specific product
    - Requires a valid product ID
    - Returns current stock quantity
    """
    inventory_item = inventory_service.get_inventory_for_product(product_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory_item

@app.put("/inventory/{product_id}", response_model=InventoryItem, tags=["Inventory"])
async def update_inventory(product_id: int, quantity: int):
    """
    Update inventory quantity for a specific product
    - Requires product ID and new quantity
    - Returns updated inventory details
    """
    return inventory_service.update_inventory(product_id, quantity)

# Combined Endpoint
@app.get("/product-details/{product_id}", tags=["Combined"])
async def get_product_details(product_id: int):
    """
    Retrieve comprehensive product details including inventory
    - Combines product and inventory information
    - Returns product details with current stock
    """
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    inventory = inventory_service.get_inventory_for_product(product_id)
    
    return {
        "product": product,
        "inventory": {
            "quantity": inventory.quantity if inventory else 0
        }
    }

# Run the application (for local testing)
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)