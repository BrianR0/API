from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field
from typing import Optional,List

from starlette.requests import Request
from config.base_de_datos import sesion, motor, base
from modelos.venta import Acuario
from jwt_config import *



#Crea instancia de fastapi
app = FastAPI()
app.title = "Aplicación de ventas"#Le damos titulo a la instancia en documentación
app.version = '1.0.2'#Modificamos la version en documentación
base.metadata.create_all(bind = motor)



#creamos el modelo
class User(BaseModel):
    email:str
    key:str

#Autenticación
class Portador(HTTPBearer):
    async def __call__(self, request:Request):
        autorizacion = await super().__call__(request)
        dato = validate_token(autorizacion.credentials)
        if dato['email'] != 'test@gmail.com':
            raise HTTPException(status_code=403, detail='No autorizado')

#MODELO
class Stock (BaseModel):

    id: int = Field(ge=0,le=20)
    Tipo: str 
    Importe: str 
    Tamanio: str

    class Config:
        schema_extra = {
            "example":{
                "id":3,
                "Tipo":"Ranchu Calico",
                "Importe":"$800.00",
                "Tamanio": "Grande",
            }

        }

#RUTA DE LOGIN
@app.post('/login', tags=['autentication'])
def login(Usuario:User):
    if Usuario.email == 'test@gmail.com' and Usuario.key == '1234':
        #Obtenemos el token con la funcion pasandole el diccionario de usuario
        token:str = get_token(Usuario.dict())
    
        return JSONResponse(status_code = 200, content = token)
    else:
        return JSONResponse(status_code = 404, content={'Error':'Datos erroneos'})

#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación
def mensaje():
    return HTMLResponse('<h2>HOLA, ESTA ES UNA API DE GOLDFISH </h2>')

@app.get('/GET_STOCK', tags=['Stock'], response_model = List[Stock], status_code = 200, dependencies = [Depends(Portador())])#INDICAMOS EL TIPO DE RESPUESTA CON response_model en este caso una lista
def get_stock() -> List[Stock]:
    db =  sesion()
    resultado = db.query(Acuario).all()
    return JSONResponse(content=jsonable_encoder(resultado), status_code = 200) #usamos JSONResponse

@app.get('/Get_stock/{id}', tags=['Stock'], response_model = Stock, status_code=200)
def get_stock(id: int = Path(ge=1,le=2000)) -> Stock:#Se valida que el id sea minimo 1 hasta 2000
    db = sesion()
    resultado = db.query(Acuario).filter(Acuario.id == id).first()
    if not resultado:
        return JSONResponse(status_code=404, content={'Mensaje':'No hay peces con ese id'})
    
    return JSONResponse(content= jsonable_encoder(resultado), status_code = 200)

@app.get('/Stock/', tags=['Stock'], response_model = List[Stock], status_code = 200)#Agregamos el codigo de respuesta
def get_stock_query(tamaño:str = Query(min_length=4, max_length=20)) -> List[Stock]:
    db = sesion()
    resultado = db.query(Acuario).filter(Acuario.Tamanio == tamaño).all()
    print(jsonable_encoder(resultado))
    if not resultado:
        return JSONResponse(status_code=404, content={'Mensaje':'No hay peces con ese tamaño'})
    
    return JSONResponse(content= jsonable_encoder(resultado), status_code = 200)

    
@app.post('/create_stock',tags=['Stock'], response_model = dict, status_code = 201)
def crea_stock(add:Stock) -> dict:
    db = sesion()
    #extraemos atributos para pasarlos como parametros
    new_stock = Acuario(**add.dict())
    
    #añadimos a la bd y hacemos un commit
    db.add(new_stock)
    db.commit()

    return JSONResponse(content={'mensaje':'Venta registrada'}, status_code = 201)

@app.put('/update_stock',tags=['Stock'], response_model = dict, status_code = 201 )
def update_stock(id:int, Stock:Stock) -> dict:
    db = sesion()

    select = db.query(Acuario).filter(Acuario.id == id).first()
    if not select:
        return JSONResponse(status_code=404, content={'Mensaje':'No hay peces con ese id'})
    select.Importe = Stock.Importe
    select.Tamanio = Stock.Tamanio
    select.Tamanio = Stock.Tipo
    db.commit()
    #return peces
    return JSONResponse(content = {'message':'Registro actualizado correctamente',
                                   'code':'200'}, status_code = 201)


@app.delete('/delete_stock', tags=['Stock'], response_model = List[Stock], status_code = 200)
def delete_stock(id:int) ->dict:
    db = sesion()
    select = db.query(Acuario).filter(Acuario.id == id).first()
    if not select:
        return JSONResponse(status_code=404, content={'Mensaje':'No hay peces con ese id'})
    db.delete(select)
    db.commit()
    #return peces
    return JSONResponse(content = {'message':'Registro borrado correctamente',
                                   'code':'200'}, status_code = 200)