from abc import ABC, abstractmethod
from datetime import datetime


class GitHubService(ABC):
    """ Interface for GitHub service."""
    
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
        """
        https://docs.github.com/en/rest/commits/commits#list-commits
        """
        pass
    
    @abstractmethod
    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ):
        """
        https://docs.github.com/en/rest/repos/repos#list-repository-contributors
        """
        pass
        
    async def __aenter__(self):
        return self

    # Abstract to make sure devs don't forget to close connections in derived classes.
    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

