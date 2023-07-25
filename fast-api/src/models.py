from pydantic import BaseModel
from typing import Annotated, Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    email: Union[str, None] = None
    username: str

class UserInDB(User):
    id: int
    hashed_password: str

class RegisterUser(User):
    password: str