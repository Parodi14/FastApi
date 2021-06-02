from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:  str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name:  Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/") # Ruta
def home():  # Endpoint funcion
    return {"DATA": "Testing"} # Retornas información

""""
1) Metodotos
GET
POST
PUT
DELETE
@app.get("/about")
def about():
    return {"Data": "About"}

#localhost/hello

# endpoint Slash something

# Ruta y endpoint parametros devolver información de un item por su id

Deployment: uvicorn fpdf:app --reload 
"""

inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular"
        },
    2: {
        "name": "Pescado",
        "price": 4.33,
        "brand": "Pescadito"
    },

    14: {
        "name": "Lomo",
        "price": 14.05,
        "brand": "Lomo Fino"
    }
}
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="El id del item")):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str = Query(None, tittle="Name", description="name of item.")):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=404,
                        detail="Item no encontrado!")

# Request Body

@app.post("/create-item/{item_id}")
def create_item(item_id: int,  item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404,
                            detail="Item no encontrado!")
    # return {"Error": "Id item No existe"}


    inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_ite(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404,
                            detail="Item no encontrado!")
        #return {"Error": "Item ID no existe"}
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].name = item.price
    if item.brand != None:
        inventory[item_id].name = item.brand
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description = "El id del item ", gt = 0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404,
                            detail="Item no encontrado!")

    del inventory [item_id]
    return {"Success": "Item eliminado!"}



