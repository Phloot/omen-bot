import datetime
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class User:
    discord_id: str
    api_key: str
    created_date: datetime.datetime
