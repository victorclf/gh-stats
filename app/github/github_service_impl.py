from datetime import datetime
import os

import httpx
from app.github.github_service import GitHubService


class GitHubServiceImpl(GitHubService):
    BASE_URL = 'https://api.github.com'
    TOKEN_PATH = os.path.expanduser(os.path.join('~', '.ghstatsrc'))
    
    """ Implementation of GitHub service that connects to the public GitHub API.
    """
    def __init__(self):
        super().__init__()
        self.token = self._read_token()
        headers = {'accept': 'application/vnd.github+json'}
        if self.token:
            headers['authorization'] = f'token {self.token}'
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, headers=headers)
        
    def _read_token(self):
        try:
            with open(self.TOKEN_PATH) as fin:
                token = fin.read()
                return token.strip()
        except IOError:
            return None
    
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
        response = await self.client.get(f'/repos/{owner}/{repo}/commits', params=params)
        # TODO better way to log this
        print('\nget_commits response from GitHub')
        print(response.headers)
        print(response.json())
        
        return response

    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ):
        params = {'page': page, 'per_page': per_page}
        response = await self.client.get(f'/repos/{owner}/{repo}/contributors', params=params)
        # TODO better way to log this
        print('get_contributors response from GitHub')
        print(response.headers)
        print(response.json)
        
        return response

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()
