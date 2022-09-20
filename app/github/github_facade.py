""" Facade for external GitHub service

Simplifies access to external GitHub service by providing methods closer to what we need in the business logic.
"""

from datetime import datetime
import re

from app.github.github_service import GitHubService

"""
Regex to extract number of pages from headers['link']. For example:
link: <https://api.github.com/repositories/7833168/commits?per_page=1&page=2>; rel="next", <https://api.github.com/repositories/7833168/commits?per_page=1&page=56525>; rel="last"
"""
PAGE_COUNT_REGEX = re.compile(r'.*?rel="next".*?[^_]+page=([0-9]+).*?"last".*')


class GitHubFacade:
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
    ):
        # TODO return Commit objects here instead of raw response
        return self.github_service.get_commits(owner, repo, author, page, per_page, since, until).json

    async def count_commits_on_day(
        self,
        owner: str,
        repo: str,
        day: datetime,
        author: str | None = None,
    ) -> int:
        page = 1
        per_page = 1
        since = day
        until = day

        response = await self.github_service.get_commits(owner, repo, author, page, per_page, since, until)
        nCommits = self._getNumberOfPages(response)  # since every page here has a single commit, the number of pages is the number of commits
        return nCommits
