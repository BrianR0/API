from jwt import encode, decode


def get_token(login:dict)-> str:
    token:str = encode(payload=login, key='mi_clave', algorithm= 'HS256')
    return token

def validate_token(token:str)->dict:
    dato:dict = decode(token, key='mi_clave', algorithms=['SH256'])
    return dato