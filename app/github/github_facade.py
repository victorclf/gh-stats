from datetime import datetime
import re

from app.github.github_service import GitHubService
from app.models.commits import Commit

"""
Regex to extract number of pages from headers['link']. For example:
link: <https://api.github.com/repositories/7833168/commits?per_page=1&page=2>; rel="next", <https://api.github.com/repositories/7833168/commits?per_page=1&page=56525>; rel="last"
"""
PAGE_COUNT_REGEX = re.compile(r'.*?rel="next".*?[^_]+page=([0-9]+).*?"last".*')


class GitHubFacade:
    """ Facade for external GitHub service. 
    Simplifies access to external GitHub service by providing methods closer to what we need in the business logic.
    """

    def __init__(self, github_service: GitHubService):
        self.github_service = github_service

    def _getNumberOfPages(self, response):
        return int(PAGE_COUNT_REGEX.match(response.headers['link']).group(1))

    async def get_commits(
        self,
        owner: str,
        repo: str,
        author: str | None = None,
        page: int = 1,
        per_page: int = 30,
        since: datetime | None = None,
        until: datetime | None = None
    ) -> list[Commit]:
        commits_json = (await self.github_service.get_commits(owner, repo, author, page, per_page, since, until)).json()
        return [Commit(author=c['author']['login'], message=c['commit']['message'], date=c['commit']['author']['date']) for c in commits_json]

    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> list[str]:
        contributors_json = (await self.github_service.get_contributors(owner, repo, page, per_page)).json()
        return [c['login'] for c in contributors_json]

    async def count_commits_on_day(
        self,
        owner: str,
        repo: str,
        author: str,
        day: datetime,
    ) -> int:
        page = 1
        per_page = 1
        since = day
        until = day

        response = await self.github_service.get_commits(owner, repo, author, page, per_page, since, until)
        n_commits = self._getNumberOfPages(response)  # since every page here has a single commit, the number of pages is the number of commits
        return n_commits
