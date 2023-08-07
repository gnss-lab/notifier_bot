from pydantic import BaseModel
from typing import Annotated, Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class BaseUser(BaseModel):
    email: Union[str, None] = None
    username: str

class User(BaseUser):
    id: int

class UserInDB(User):
    hashed_password: str

class RegisterUser(BaseUser):
    password: str