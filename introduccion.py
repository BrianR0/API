from fastapi import FastAPI

#INSTANCIA FASTAPI
app = FastAPI()

#PUNTO DE ENTRADA O ENDPOINT

@app.get('/')
def mensaje():
    return 'Hola, bienvenido a FastApi cambiar curso'


if __name__ == '__main__':
    print("HOLA MUNDO")
    pass