from fastapi import FastAPI, Body

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
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
    id: Optional[int]=None
    Tipo: str
    Importe: str
    Tamaño: str

#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación
def mensaje():
    return HTMLResponse('<h2>TITULO HTML DESDE FASTAPI </h2>')


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