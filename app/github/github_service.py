""" Interface for GitHub service.
"""
from abc import ABC, abstractmethod
import abc
from datetime import datetime

class GitHubService(ABC):
    @abstractmethod
    async def get_commits(
        self,
        owner: str,
        repo: str,
        author: str | None = None,
        page: int = 1,
        per_page: int = 30,
        since: datetime | None = None,
        until: datetime | None = None
    ):
        pass
        
    async def __aenter__(self):
        return self

    # Abstract to make sure devs don't forget to close connections in derived classes.
    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

