from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Definiendo prefix del Router, Tag para la documentacion y responses para el error
router = APIRouter(prefix="/api/products",
                   tags=["products"],
                   responses={404: {"description": "Not found"}})


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    tax: float
    tags: list[str] = []


products = [
    Product(id=1, name="Product 1", description="Description 1",
            price=10.0, tax=1.0, tags=["tag1", "tag2"]),
    Product(id=2, name="Product 2", description="Description 2",
            price=20.0, tax=2.0, tags=["tag2", "tag3"]),
    Product(id=3, name="Product 3", description="Description 3",
            price=30.0, tax=3.0, tags=["tag3", "tag4"]),
]


@router.get("/", response_model=list[Product])
async def get_product():
    return products


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
