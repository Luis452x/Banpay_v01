from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    user_name: str = Field(min_length=4)
    user_password: str = Field(min_length=8)
    user_rol: str = Field(default="films")

class TokenJWT(BaseModel):
    access_token: str
    token_type: str
    