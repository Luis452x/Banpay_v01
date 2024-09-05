from fastapi import FastAPI
from Routers.UserR import UserRouter
from Routers.LoginR import LoginRouter
from Database.Db import BaseD, engine

BaseD.metadata.create_all(bind=engine)
app= FastAPI()
app.include_router(UserRouter)
app.include_router(LoginRouter)
Users=[]



@app.get("/", tags=["Root"])
def welcome():
    return {"message": "Bienvenido a la api"}
