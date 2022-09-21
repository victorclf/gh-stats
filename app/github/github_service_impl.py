from datetime import datetime

import httpx
from app.github.github_service import GitHubService


class GitHubServiceImpl(GitHubService):
    BASE_URL = 'https://api.github.com'
    
    """ Implementation of GitHub service that connects to the public GitHub API.
    """
    def __init__(self):
        super().__init__()
        self.client = httpx.AsyncClient(base_url=self.BASE_URL)
    
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
        params = {'page': page, 'per_page': per_page}
        if author:
            params['author'] = author
        if since:
            params['since'] = since.isoformat()
        if until:
            params['until'] = until.isoformat()

    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ):
        params = {'page': page, 'per_page': per_page}
        return await self.client.get(f'/repos/{owner}/{repo}/contributors', params=params)

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()
