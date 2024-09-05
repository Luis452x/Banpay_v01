from fastapi import APIRouter, Path, Query, status, Depends, HTTPException
from pydantic import BaseModel, Field
from Database.Db import BaseD, db_dependency
from sqlalchemy.orm import Session
from typing import Annotated
from Models.UserM import UserTable
from passlib.context import CryptContext
from Routers.LoginR import get_user_data_from_jwt
from Schemes.schemesC import UserRequest
import Studio_Ghibli_Api

UserRouter= APIRouter(
    prefix="/User",
    tags=["User"]
)
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
user_dependency = Annotated[dict, Depends(get_user_data_from_jwt)]



@UserRouter.get("/", status_code=status.HTTP_200_OK)
def get_all_users(db:db_dependency):
    return db.query(UserTable).all()



@UserRouter.get("/{user_name}", status_code=status.HTTP_200_OK)
def get_user_by_username(user: user_dependency,db: db_dependency, user_name: str=Path(min_length=4)):
    if user is None:
        raise HTTPException(status_code=401, detail="No esta validado")
    if not user.get('is_admin'):
        user_to_return = db.query(UserTable).filter(UserTable.user_name == user_name).filter(UserTable.Id==user.get('Id')).first()  
    else:
        user_to_return = db.query(UserTable).filter(UserTable.user_name == user_name).first()
    if user_to_return is not None:
        return user_to_return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@UserRouter.put("/{user_name}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user: user_dependency, db:db_dependency, updated_user: UserRequest, user_name: str = Path(min_length=4)):
    if user is None:
        raise HTTPException(status_code=401, detail="No esta validado")
    if not user.get('is_admin'):
        user_check=db.query(UserTable).filter(UserTable.user_name==user_name).filter(UserTable.Id==user.get('Id')).first()
    else:
        user_check=db.query(UserTable).filter(UserTable.user_name==user_name).first()
    if user_check is None:
        raise HTTPException(status_code=404, detail="No se encontro usuario con ese nombre")
    user_check.user_name=updated_user.user_name
    user_check.hashed_passwordssword=bcrypt_context.hash(updated_user.user_password)
    user_check.rol=updated_user.user_rol
    db.add(user_check)
    db.commit()
    return {"message":"Usuario actualizado"}

@UserRouter.delete('/{user_name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: user_dependency, db: db_dependency, user_name: str = Path(min_length=4)):
    if user is None:
        raise HTTPException(status_code=401, detail="No esta validado")
    if not user.get('is_admin'):
        usuario_base=db.query(UserTable).filter(UserTable.user_name==user_name).filter(UserTable.Id==user.get('Id')).first()
    else:
        usuario_base=db.query(UserTable).filter(UserTable.user_name==user_name).first()
    if usuario_base is None:
        raise HTTPException(status_code=404, detail="No se encontro usuario con ese nombre")
    db.query(UserTable).filter(UserTable.user_name==usuario_base.user_name).delete()
    db.commit()

@UserRouter.get("/Ghibli/", status_code=status.HTTP_200_OK)
def get_Ghibli_by_rol(user: user_dependency):
   if user is None:
        raise HTTPException(status_code=401, detail="No esta validado")
   return Studio_Ghibli_Api.get_data_by_rol(user.get('rol'))