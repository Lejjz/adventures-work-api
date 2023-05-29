import os
import sys
import pytest
from fastapi.testclient import TestClient
from app.main import app


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


client = TestClient(app)


def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_get_product():
    response = client.get("/products/214")
    assert response.status_code == 200

def test_get_product_not_found():
    response = client.get("/products/99999")
    assert response.status_code == 404

def test_create_product():
    payload = {
    "ProductKey": 608,
    "ProductSubcategoryKey": 2,
    "ProductSKU": "ABCD1234",
    "ProductName": "Product 1",
    "ModelName": "Model 1",
    "ProductDescription": "Description 1",
    "ProductColor": "Red",
    "ProductSize": 10.5,
    "ProductStyle": 1,
    "ProductCost": 50.0,
    "ProductPrice": 100.0
}
    response = client.post("/products", json=payload)
    assert response.status_code == 200

def test_update_product():
    payload = {
    "ProductKey": 608,
    "ProductSubcategoryKey": 2,
    "ProductSKU": "ABCD1234",
    "ProductName": "Product 1",
    "ModelName": "Model 1",
    "ProductDescription": "Description 1",
    "ProductColor": "Red",
    "ProductSize": 11,
    "ProductStyle": 1,
    "ProductCost": 50.0,
    "ProductPrice": 100.0
}
    response = client.put("/products/608", json=payload)
    assert response.status_code == 200

def test_delete_product():
    response = client.delete("/products/608")
    assert response.status_code == 200

