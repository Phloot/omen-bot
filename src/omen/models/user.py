import datetime
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class User:
    discord_id: str
    api_key: str
    gw2_account_id: str
    gw2_account_name: str
    last_updated: datetime.datetime
