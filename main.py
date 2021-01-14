from dataBase.user_db import get_user

from dataBase.movements_db import ReservaInDB
from dataBase.movements_db import get_reserva, save_reserva, update_reserva

from models.user_models import UserIn
from models.user_models import UserInRegistro, UserOutRegistro
from models.movements_models import ReservaOut, ReservaIn, ReservaCancelIn, ReservaCancelOut

# Se importan algunos paquetes adicionales y se crea la api
from fastapi import FastAPI
from fastapi import HTTPException

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = ["http://localhost.tiangolo.com",
            "https://localhost.tiangolo.com",
            "http://localhost",
            "http://localhost:8080",
            "http://localhost:8081"
            ## "https://reservas-hotel-app37.herokuapp.com"
            ]

api.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],)

## Se implementa la funcionalidad get_reservation
@api.get("/user/reserva/{id_reserva}")
async def get_reservation(id_reserva: int):
    reserva_in_db = get_reserva(id_reserva)
    if reserva_in_db == None:
        raise HTTPException(status_code = 404, detail = "La reserva no existe")
    user_in_db = get_user(reserva_in_db.username)
    reserva_out = ReservaOut(**reserva_in_db.dict(), nombre = user_in_db.nombre)
    return reserva_out

@api.put("/user/reserva/make/")
async def make_reservation(reserva_in: ReservaIn):
    user_in_db = get_user(reserva_in.username)
    if user_in_db == None:
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    reserva_in_db = ReservaInDB(**reserva_in.dict())
    reserva_in_db = save_reserva(reserva_in_db)
    reserva_out = ReservaOut(**reserva_in_db.dict(), nombre = user_in_db.nombre)
    return reserva_out

@api.put("/user/reserva/cancel/")
async def cancel_reservation(reserva_cancel_in: ReservaCancelIn):
    reserva_in_db = get_reserva(reserva_cancel_in.id_reserva)
    if reserva_in_db == None:
        raise HTTPException(status_code = 404, detail = "La reserva no existe")
    estado = reserva_in_db.estado
    if estado == "CANCELADA":
        raise HTTPException(status_code = 404, detail = "La reserva ya está cancelada")
    reserva_in_db.estado = "CANCELADA"
    update_reserva(reserva_in_db)
    reserva_cancel_out = ReservaCancelOut(**reserva_in_db.dict())
    return reserva_cancel_out

@api.post("/user/login/")
async def login_user(user_in: UserIn):
    user_in_db = get_user(user_in.username)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")
    return  {"Autenticado": True}

@api.put("/user/register/")
async def register_user(user_in_registro: UserInRegistro):
    valor = get_keys(user_in_registro.username)
    if valor:
        raise HTTPException(status_code = 404, detail = "Usuario no disponible")
    user_in_db = UserInDB(**user_in_registro.dict())
    user_in_db = save_user(user_in_registro)
    user_out = UserOutRegistro(**user_in_db.dict())
    return user_out
 
# user_in_db.balance = user_in_db.balance - transaction_in.value update_user(user_in_db)

# transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)

# transaction_in_db =  save_transaction(transaction_in_db) transaction_out = TransactionOut(**transaction_in_db.dict())
#     return transaction_out