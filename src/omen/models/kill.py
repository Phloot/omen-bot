import datetime

from pydantic.dataclasses import dataclass


@dataclass
class Kill:
    discord_id: str
    raid_day: datetime.date
    kills: int
