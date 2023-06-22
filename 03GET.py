from fastapi import FastAPI

from fastapi.responses import HTMLResponse

#Crea instancia de fastapi
app = FastAPI()
app.title = "Aplicación de ventas"#Le damos titulo a la instancia en documentación
app.version = '1.0.2'#Modificamos la version en documentación

peces = [
    {
        "id":1,
        "Tipo":"Ranchu",
        "Importe":"$400.00",
        "Tamaño": "Grande",
    },
    {
        "id":2,
        "Tipo":"Escama de perla",
        "Importe":"$600.00",
        "Tamaño":"Chico"
    }   
]


#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación
def mensaje():
    return HTMLResponse('<h2>TITULO HTML DESDE FASTAPI </h2>')
@app.get('/Stock',tags=['Stock'])
def stock():
    return peces

