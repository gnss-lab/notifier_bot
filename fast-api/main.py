from datetime import timedelta, datetime

from src.models import User, UserInDB, Token, RegisterUser, TokenData
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from passlib.context import CryptContext

import src.db_functions as db
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = db.get_user_by_name(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.get_user_by_name(token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.get("/register", response_model=User)
async def register(user: RegisterUser):
    db_user = db.get_user_by_name(user.username)
    if not db_user:
        db.add_fastapi_user(user.username, user.email, get_password_hash(user.password))
        return db.get_user_by_name(user.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )

@app.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user: UserInDB = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/add/user")
async def add_user(user_id: int):
    """user_id = telegram_id"""
    db.add_user(user_id)

@app.get("/add/subscription")
async def add_subscription(sub_name: str, sub_description: str):
    db.add_subscription(sub_name, sub_description)

@app.get("/subscribe")
async def subscribe(sub_id:int, user_id:int, remind:bool = False):
    db.subscribe(sub_id, user_id, remind)

@app.get("/send_notification")
async def send_notification(message: str, sub_id: int):
    db.add_notification(message, sub_id)

@app.get("/get/users")
async def get_users():
    return db.get_users()

@app.get("/get/subscriptions")
async def get_subscriptions():
    return db.get_subscriptions()

@app.get("/get/users_subscriptions")
async def get_users_subscriptions():
    return db.get_users_subscriptions()

@app.get("/get/notifications")
async def get_notifications():
    return db.get_notifications()

# uvicorn main:app --reload --host 0.0.0.0