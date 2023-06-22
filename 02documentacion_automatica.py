from fastapi import FastAPI



#Crea instancia de fastapi
app = FastAPI()
app.title = "Aplicación de ventas"#Le damos titulo a la instancia en documentación
app.version = 1.1#Modificamos la version en documentación

#PUNTO DE ENTRADA O ENDPOINT

@app.get('/',tags=['Inicio'])#tags para cambiar etiqueta en documentación

def mensaje():
    return 'Hola, bienvenido a FastApi '

if __name__ == '__main__':
    print("HOLA MUNDO")
    pass