from config.base_de_datos import base
from sqlalchemy import Column, Integer, String, Float


class Acuario(base):
    #Nombre de la tabla
    __tablename__ = "Acuario"
    id = Column(Integer, primary_key = True)
    Tipo = Column(String)
    Importe = Column(String)
    Tamanio = Column(String)
