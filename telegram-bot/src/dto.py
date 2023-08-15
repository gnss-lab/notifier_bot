from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    id: int
    message: str
    sub_id: int
    initiator_id: int
    processed: int
    created_on: datetime

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

@dataclass
class MonitoredServices:
    id: int
    url: str
    message: str
    sub_id: int
    initiator_id: int
    cron_time: str
    created_on: datetime
    processed: int
    need_delete: int