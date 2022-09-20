from datetime import datetime
from pydantic import BaseModel

class DailyCommits(BaseModel):
    author: str
    commits_on_day: dict[datetime, int]

class Commit(BaseModel):
    author: str
    message: str
    date: datetime