from fastapi import FastAPI, Path, Query

from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

#Crea instancia de fastapi
app = FastAPI()
app.title = "Aplicación de ventas"#Le damos titulo a la instancia en documentación
app.version = '1.0.2'#Modificamos la version en documentación

peces = [
    {
        "id":1,
        "Tipo":"Ranchu",
        "Importe":"$800.00",
        "Tamaño": "Grande",
    },
    {
        "id":2,
        "Tipo":"Escama de perla",
        "Importe":"$600.00",
        "Tamaño":"Chico"
    },
    {
        "id":3,
        "Tipo":"Ranchu Calico",
        "Importe":"$800.00",
        "Tamaño": "Grande",
    },   
]

#creamos el modelo
class Stock (BaseModel):

    id: int = Field(default = "None",ge=0,le=20)
    Tipo: str 
    Importe: str = Field(default="$00.00",max_length=8)
    Tamaño: str

    class Config:
        schema_extra = {
            "example":{
                "id":3,
                "Tipo":"Ranchu Calico",
                "Importe":"$800.00",
                "Tamaño": "Grande",
            }

        }

#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación
def mensaje():
    return HTMLResponse('<h2>TITULO HTML DESDE FASTAPI </h2>')

@app.get('/Get_stock/{id}', tags=['Stock'])
def get_stock(id: int = Path(ge=1,le=2000)):#Se valida que el id sea minimo 1 hasta 2000
    for element in peces:
        if element['id'] == id:
            return element
    return[]

@app.get('/Stock/{Tamaño}', tags=['Stock'])
def get_stock_query(tamaño:str ):
    return [element for element in peces if element['Tamaño'] == tamaño]
            
    

@app.post('/create_stock',tags=['Stock'])
def crea_stock(add:Stock):
    
    peces.append(add)
    return peces

@app.put('/update_stock',tags=['Stock'])
def update_stock(id:int, Stock:Stock):
    for element in peces:
        if element['id'] == id:
            element["Tipo"] = Stock.Tipo
            element["Tamaño"] = Stock.Tamaño
            element["Importe"] = Stock.Importe
    return peces


@app.delete('/delete_stock', tags=['Stock'])
def delete_stock(tamaño:str, importe:str):
    for element in peces:
        if element['Tamaño'] == tamaño and element['Importe'] == importe:
            peces.remove(element)
    return peces