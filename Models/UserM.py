from Database.Db import BaseD
from sqlalchemy import Integer, String, Column, Boolean

class UserTable(BaseD):
    __tablename__="User"
    Id= Column(Integer, primary_key=True)
    user_name=Column(String, unique=True)
    hashed_password=Column(String)
    rol=Column(String)
    is_admin=Column(Boolean)