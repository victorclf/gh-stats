from datetime import date, datetime
from pydantic import BaseModel


class DailyCommits(BaseModel):
    author: str
    commits_on_day: dict[date, int]


class Commit(BaseModel):
    author: str
    message: str
    date: datetime
