import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


fichero = "../datos.sqlite"
#leemos el directorio actual del archivo de bd
directorio = os.path.dirname(os.path.realpath(__file__))
#direccion de la bd uniendo las 2 variables anteriores
ruta = f"sqlite:///{os.path.join(directorio,fichero)}"
#creamos el motor
motor = create_engine(ruta, echo=True)
#creamos la sesión
sesion = sessionmaker(bind=motor)
#creamos base para manejar las tablas
base = declarative_base()

ruta2 = "mysql+pymysql://bro1018:Dualcore159@db4free.net/credentials"

motor2 = create_engine(ruta2, echo=True)
sesion2 = sessionmaker(bind=motor2)

