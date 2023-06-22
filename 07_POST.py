from fastapi import FastAPI, Body

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
    },
    {
        "id":3,
        "Tipo":"Ranchu Calico",
        "Importe":"$800.00",
        "Tamaño": "Grande",
    },   
]


#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación
def mensaje():
    return HTMLResponse('<h2>TITULO HTML DESDE FASTAPI </h2>')

#Muestra toda la información GET
@app.get('/Stock',tags=['Stock'])
def stock():
    return peces

#Muestra la información dada un parametro GET(PATH)
@app.get('/Stock/{id}',tags=['Stock'])
def stock(id:int):
    for elem in peces:
        if elem['id']==id:
            return elem
    return []

#Muestra la información dado un query GET(QUERY)
@app.get('/Stock/',tags=['Stock'])
def get_stock_tamaño(tamaño:str,id:int):
    return [elem for elem in peces if elem['Tamaño']==tamaño and elem['id']==id]

#Insertamos elementos POST
@app.post('/ventas',tags=['Ventas'])
def crea_stock(id:int = Body(), Tipo:str=Body(), Importe:str=Body(), Tamaño:str=Body()):
    
    peces.append(
        {
            "id":id,
            "Tipo":Tipo,
            "Importe":Importe,
            "Tamaño": Tamaño,  
        }
    )
    return peces