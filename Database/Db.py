from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
import os

sqliteName = "BaseDeDatos.sqlite"
base_dir=os.path.dirname(os.path.realpath(__file__))
databaseUrl=f'sqlite:///{os.path.join(base_dir, sqliteName)}'

engine = create_engine(databaseUrl, connect_args={'check_same_thread': False})
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseD = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session, Depends(get_db)]
