from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from datetime import date
from typing import List
import pandas as pd
import csv
import os
from fastapi.responses import JSONResponse


class Product(BaseModel):
    ProductKey: int
    ProductSubcategoryKey: int
    ProductSKU: str
    ProductName: str
    ModelName: str
    ProductDescription: str
    ProductColor: str
    ProductSize: str
    ProductStyle: str
    ProductCost: float
    ProductPrice: float

class ResponseModelCustomerSales(BaseModel):
    name: str
    last_name: str
    sales_quantity: int


app = FastAPI()

current_directory = os.path.dirname(os.path.abspath(__file__))
productTable = os.path.join(current_directory, "dataset-adventures-work", "AdventureWorks_Products.csv")

product_df = os.path.join(current_directory, "dataset-adventures-work", "AdventureWorks_Products.csv")


#Swagger

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    openapi_schema = get_openapi(
        title="Adventures Work",
        version="1.0.0",
        routes=app.routes,
    )
    return JSONResponse(openapi_schema) 

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Adventures Work API", version="1.0.0")

@app.get("/")
def home():
    return "Minha API está no ar."

@app.post("/products/")
async def createProduct(product: Product):
    with open(product_df, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(product.dict().values())
    
    return product


@app.get("/products/", response_model=List[Product])
def getProducts():
    readData = pd.read_csv(productTable)
    products = readData.to_dict(orient="records")
    return products


@app.get("/products/{id}", response_model=Product)
def getProduct(id: int):
    readData = pd.read_csv(productTable)
    product = readData.loc[readData['ProductKey'] == id]
    if product.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.iloc[0].to_dict()


@app.put("/products/{id}", response_model=Product)
def updateProduct(id: int, updated_product: Product):
    readData = pd.read_csv(productTable)
    product_index = readData.index[readData['ProductKey'] == id]
    
    if len(product_index) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    

    for key, value in updated_product.dict().items():
        readData.loc[product_index, key] = value
    

    readData.to_csv(productTable, index=False)
    
    return updated_product


@app.delete("/products/{id}")
def deleteProduct(id: int):
    readData = pd.read_csv(productTable)
    product_index = readData.index[readData['ProductKey'] == id]
    
    if len(product_index) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    

    readData.drop(product_index, inplace=True)
    

    readData.to_csv(productTable, index=False)
    
    return {"message": "Product deleted successfully"}


@app.get("/sales/top-products/category/{category}")
def get_top_products_by_category(category: str):
    df_produtos = pd.read_csv('dataset-adventures-work/AdventureWorks_Products.csv')
    df_categorias = pd.read_csv('dataset-adventures-work/AdventureWorks_Product_Categories.csv')
    df_subcategorias = pd.read_csv('dataset-adventures-work/AdventureWorks_Product_Subcategories.csv')
    df_pedidos = pd.read_csv('dataset-adventures-work/AdventureWorks_Sales_2017.csv')

    df_relacionado = df_produtos.merge(df_subcategorias, on='ProductSubcategoryKey') \
                            .merge(df_categorias, on='ProductCategoryKey') \
                            .merge(df_pedidos, on='ProductKey')

    df_vendas = df_relacionado.groupby(['CategoryName', 'ProductName']).sum()['OrderQuantity'].reset_index()

    df_vendas_sorted = df_vendas.groupby('CategoryName').apply(lambda x: x.nlargest(10, 'OrderQuantity')).reset_index(drop=True)

    categorias = df_vendas_sorted['CategoryName'].unique()


    produtos_categoria = df_vendas_sorted[df_vendas_sorted['CategoryName'] == category]
    top_ten_sales = []
    for _, produto in produtos_categoria.iterrows():
        top_ten_sales.append({'Produto_Nome': produto['ProductName'], 'Quantidade_Vendida': produto['OrderQuantity']})

    return top_ten_sales

@app.get("/sales/best-customer", response_model=ResponseModelCustomerSales)
def get_best_customer():
    df_pedidos = pd.read_csv('dataset-adventures-work/AdventureWorks_Sales_2017.csv')
    df_clientes = pd.read_csv('dataset-adventures-work/AdventureWorks_Customers.csv')
    df_produtos = pd.read_csv('dataset-adventures-work/AdventureWorks_Products.csv')

    df_relacionado = df_pedidos.merge(df_clientes, on='CustomerKey')

    df_total_pedidos = df_relacionado.groupby(['CustomerKey', 'FirstName', 'LastName']).size().reset_index(name='TotalPedidos')

    cliente_maior_pedidos = df_total_pedidos.loc[df_total_pedidos['TotalPedidos'].idxmax()]

    client = dict(cliente_maior_pedidos.items())

    return ResponseModelCustomerSales(name=cliente_maior_pedidos['FirstName'], last_name=cliente_maior_pedidos['LastName'], sales_quantity=cliente_maior_pedidos['TotalPedidos'])


#Não finalizado
@app.get("/sales/busiest-month", response_model=list)
def get_busiest_month():
    df_pedidos = pd.read_csv('dataset-adventures-work/AdventureWorks_Sales_2017.csv')
    df_produtos = pd.read_csv('dataset-adventures-work/AdventureWorks_Products.csv')
    df_territory = pd.read_csv('dataset-adventures-work/AdventureWorks_Territories.csv')

    df_relacionado = df_pedidos.merge(df_territory, on='TerritoryKey') \
                     .merge(df_produtos, on='ProductKey')

    busiest_month = df_relacionado.groupby('ProductPrice')['Region'].sum().idxmax()
    return {'busiest_month': busiest_month}

#Não finalizado
@app.get("/sales/top-sellers", response_model=list)
def get_top_sellers():
    df_produtos = pd.read_csv('dataset-adventures-work/AdventureWorks_Products.csv')
    df_categorias = pd.read_csv('dataset-adventures-work/AdventureWorks_Product_Categories.csv')
    df_subcategorias = pd.read_csv('dataset-adventures-work/AdventureWorks_Product_Subcategories.csv')
    df_pedidos = pd.read_csv('dataset-adventures-work/AdventureWorks_Sales_2017.csv')

    df_relacionado = df_produtos.merge(df_subcategorias, on='ProductSubcategoryKey') \
                            .merge(df_categorias, on='ProductCategoryKey') \
                            .merge(df_pedidos, on='ProductKey')


    average_sales = df_pedidos.groupby('Months')['Sales'].mean()
    top_sellers = average_sales.loc[average_sales > average_sales.mean()]
    return top_sellers.tolist()



