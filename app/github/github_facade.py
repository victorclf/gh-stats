from datetime import date, datetime, time
import re

from app.github.github_service import GitHubService
from app.models.commits import Commit

"""
Regex to extract number of pages from headers['link'] in the GitHub API response. This is an example of that header field:

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
        try:
            return int(PAGE_COUNT_REGEX.match(response.headers['link']).group(1))
        except:
            return 0  # if 'link' header is not present, then no results were found

    async def get_commits(
        self,
        owner: str,
        repo: str,
        author: str | None = None,
        page: int = 1,
        per_page: int = 30,
        start_day: date | None = None,
        end_day: date | None = None
    ) -> list[Commit]:
        since = datetime.combine(start_day, time.min) if start_day else None # first second of 'since' day
        until = datetime.combine(end_day, time.max) if end_day else None # last second of 'until' day
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
        day: date,
    ) -> int:
        # To determine the number of commits using GitHub's REST API, we use a page size of 1 (per_page param)
        # so that the number of the last page is equal to the number of commits available. The number of the 
        # last page can be determined from the link to the last page in the response headers.
        page = 1
        per_page = 1
        since = datetime.combine(day, time.min) # first second of 'since' day
        until = datetime.combine(day, time.max) # last second of 'until' day

        response = await self.github_service.get_commits(owner, repo, author, page, per_page, since, until)
        n_commits = self._getNumberOfPages(response)
        return n_commits
