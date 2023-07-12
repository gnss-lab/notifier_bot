from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    id: int
    message: str
    sub_id: int
    processed: int

@dataclass
class Subscription:
    id: int
    name: str
    description: str

@dataclass
class User:
    id: int

# user_id = telegram_id


@dataclass
class UsersSubscription:
    id: int
    sub_id: int
    user_id: int
    remind: int
    created_on: datetime
