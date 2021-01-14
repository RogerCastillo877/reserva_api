from typing import Dict
from pydantic import BaseModel

# Se definen Transacciones en base de datos No1
class UserInDB (BaseModel):
    username: str
    nombre: str
    password: str

database_users = Dict[str, UserInDB]

database_users = {
    "karen45":  UserInDB(**{"username":"karen45",
                            "nombre":"Karen Daniela",
                            "password":"12345"}),
    
    "roger23":  UserInDB(**{"username":"roger23",
                            "nombre":"Roger Castillo",
                            "password":"proyecto4"}),
    
    "erick37":  UserInDB(**{"username":"erick37",
                            "nombre":"Erick Escorcia",
                            "password":"holahola"}),
    
    "juan88":   UserInDB(**{"username":"juan88",
                            "nombre":"Juan David",
                            "password":"pepito"}),
    
    "julian96": UserInDB(**{"username":"julian96",
                            "nombre":"Julian Lozano",
                            "password":"32hi165"}),
    }

# Se define una base de datos ficticia y una función No1
def get_user(username: str):
    if username in database_users.keys():
        return database_users[username]
    else:
        return None

# def update_user(user_in_db: UserInDB):
#     database_users[user_in_db.username] = user_in_db
#     return user_in_db