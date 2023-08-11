import os
from datetime import timedelta, datetime

from src.models import User, UserInDB, Token, RegisterUser, TokenData
from src.RequestLimiter import RequestLimiter
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from passlib.context import CryptContext

import src.db_functions as db
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



SECRET_KEY = os.getenv('FAST_API_SECRET')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
send_notif_limiter = RequestLimiter(10)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = db.get_fastapi_user_by_name(username)
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
    user = db.get_fastapi_user_by_name(token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.post("/register", response_model=User)
async def register(user: RegisterUser):
    db_user = db.get_fastapi_user_by_name(user.username)
    if not db_user:
        db.add_fastapi_user(user.username, user.email, get_password_hash(user.password))
        return db.get_fastapi_user_by_name(user.username)
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


@app.get("/fastapi-users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

@app.get("/user/add")
async def add_user(user_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    """user_id = telegram_id"""
    user_id = db.add_user(user_id)
    return {"user_id":user_id}

@app.get("/subscription/add")
async def add_subscription(sub_name: str, sub_description: str, current_user: Annotated[User, Depends(get_current_user)]):
    sub_id = db.add_subscription(sub_name, sub_description)
    return {"sub_id":sub_id}

@app.get("/subscribe")
async def subscribe(current_user: Annotated[User, Depends(get_current_user)],
                    sub_id:int, user_id:int, remind:bool = False):
    usub_id = db.subscribe(sub_id, user_id, remind)
    return {"usub_id":usub_id}

@app.get("/send_notification_by_id", dependencies=[Depends(send_notif_limiter)])
async def send_notification_by_id(current_user: Annotated[User, Depends(get_current_user)],
                            message: str, sub_id: int):
    notif_id = db.add_notification(message, sub_id, current_user.id)
    return {"notif_id":notif_id}

@app.get("/send_notification_by_name", dependencies=[Depends(send_notif_limiter)])
async def send_notification_by_name(current_user: Annotated[User, Depends(get_current_user)],
                            message: str, sub_name: str):
    sub_id = db.get_subscription_id_by_name(sub_name)
    notif_id = db.add_notification(message, sub_id, current_user.id)
    return {"notif_id": notif_id}

@app.get("/monitored_service/add")
async def add_monitored_service(error_message: str, sub_id: int, url: str, current_user: Annotated[User, Depends(get_current_user)]):
    ser_id = db.add_monitored_service(url, error_message, sub_id)
    return {"sub_id":ser_id}

@app.get("/monitored_service/delete")
async def delete_monitored_service(service_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    db.delete_monitored_services(service_id)

@app.get("/users/get")
async def get_users():
    return db.get_users()

@app.get("/subscriptions/get")
async def get_subscriptions():
    return db.get_subscriptions()

@app.get("/users_subscriptions/get")
async def get_users_subscriptions():
    return db.get_users_subscriptions()

@app.get("/notifications/get")
async def get_notifications():
    return db.get_notifications()

@app.get("/monitored_services/get")
async def get_monitored_services():
    return db.get_monitored_services()

@app.get("/monitored_service/get")
async def get_monitored_service_by_id(ser_id: int):
    return db.get_monitored_service_by_id(ser_id)