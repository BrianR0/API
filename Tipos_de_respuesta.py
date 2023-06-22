from fastapi import FastAPI, Body, Path, Query

from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional,List

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

    id: int = Field(ge=0,le=20)
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

@app.get('/GET_STOCK', tags=['Stock'], response_model = List[Stock])#INDICAMOS EL TIPO DE RESPUESTA CON response_model en este caso una lista
def get_stock() -> List[Stock]:
    return JSONResponse(content=peces) #usamos JSONResponse

@app.get('/Get_stock/{id}', tags=['Stock'], response_model = Stock)
def get_stock(id: int = Path(ge=1,le=2000)) -> Stock:#Se valida que el id sea minimo 1 hasta 2000
    for element in peces:
        if element['id'] == id:
            return JSONResponse(content = element)
    return JSONResponse(content=[])

@app.get('/Stock/', tags=['Stock'], response_model = List[Stock])
def get_stock_query(tamaño:str = Query(min_length=4, max_length=20)) -> List[Stock]:
    get_datos = [element for element in peces if element['Tamaño'] == tamaño]
    return JSONResponse(content = get_datos)



    
@app.post('/create_stock',tags=['Stock'], response_model = dict)
def crea_stock(add:Stock) -> dict:
    peces.append(dict(add))
    #return peces
    return JSONResponse(content={'mensaje':'Venta registrada'})

@app.put('/update_stock',tags=['Stock'], response_model = dict)
def update_stock(id:int, Stock:Stock) -> dict:
    for element in peces:
        if element['id'] == id:
            element["Tipo"] = Stock.Tipo
            element["Tamaño"] = Stock.Tamaño
            element["Importe"] = Stock.Importe
    #return peces
    return JSONResponse(content = {'message':'Registro actualizado correctamente',
                                   'code':'200'})


@app.delete('/delete_stock', tags=['Stock'], response_model = List[Stock])
def delete_stock(id:int) ->dict:
    for element in peces:
        if element['id'] == id:
            peces.remove(element)
    #return peces
    return JSONResponse(content = {'message':'Registro actualizado correctamente',
                                   'code':'200'})