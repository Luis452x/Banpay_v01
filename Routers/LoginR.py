from fastapi import APIRouter, status, Depends, HTTPException
from passlib.context import CryptContext
from Models.UserM import UserTable
from pydantic import BaseModel, Field
from Database.Db import db_dependency
from jose import jwt, JWTError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
from Schemes.schemesC import UserRequest, TokenJWT

LoginRouter = APIRouter(
    prefix='/Login',
    tags=['Login']
)



bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer= OAuth2PasswordBearer(tokenUrl='/Login/token')

def authenticate_user(user_name: str, user_password: str, db):
    user = db.query(UserTable).filter(UserTable.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(user_password, user.hashed_password):
        return False
    return user


def create_access_token(user_name: str, Id: int, rol: str, is_admin: bool,exp_time: timedelta):
    encode={'user_name': user_name, 'Id': Id, 'rol': rol, 'is_admin': is_admin}
    exp=datetime.now(timezone.utc)+exp_time
    encode.update({'exp': exp})
    #Para este ejercicio se utilizo una secret_key='SECRET_KEY' por practicidad, pero por cuestiones de seguridad nunca debe ir la secret key en el codigo
    token=jwt.encode(encode, 'SECRET_KEY', algorithm='HS256')
    return token

async def get_user_data_from_jwt(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, 'SECRET_KEY', algorithms='HS256')
        user_name: str = payload.get('user_name')
        Id: int = payload.get('Id')
        rol: str = payload.get('rol')
        is_admin: bool = payload.get('is_admin')
        if user_name is None or rol is None:
            raise HTTPException(status_code=401, detail="Usuario con token invalido")
        return {'user_name': user_name, 'Id': Id,'rol': rol, 'is_admin': is_admin}
    except JWTError:
        raise HTTPException(status_code=401, detail="Usuario invalido error con el token")


@LoginRouter.post("/token", response_model=TokenJWT)
def login_for_acceess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency,):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario invalido por token")
    token= create_access_token(user.user_name, user.Id, user.rol, user.is_admin, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}


@LoginRouter.post('/CreateUser', status_code=status.HTTP_201_CREATED)
def create_new_user(db: db_dependency, new_user: UserRequest, is_admin_f: bool):
    user_check=db.query(UserTable).filter(UserTable.user_name==new_user.user_name).first()
    if user_check is None:
        user_to_db=UserTable(
            user_name=new_user.user_name,
            hashed_password=bcrypt_context.hash(new_user.user_password),
            rol=new_user.user_rol,
            is_admin=is_admin_f
        )
        db.add(user_to_db)
        db.commit()
        return {'message':"Usuario Registrado con exito"}
    raise HTTPException(status_code=400, detail='Ya existe un usuario con ese nombre')
