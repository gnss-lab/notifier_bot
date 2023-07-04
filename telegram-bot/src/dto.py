from dataclasses import dataclass

@dataclass
class Notification:
    id: int
    message: str
    group_id: int
    processed: int

@dataclass
class NotifGroup:
    id: int
    description: str

@dataclass
class User:
    id: int
    telegram_id: int

@dataclass
class Subscription:
    id: int
    group_id: int
    user_id: int
    remind: int
