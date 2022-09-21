import asyncio
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query, Depends, Path
from app.dependencies import get_github_facade

from app.github.github_facade import GitHubFacade
from app.models.commits import Commit, DailyCommits

router = APIRouter(
    prefix="/api/v1",
    tags=["commits"]
)


def _getDaysBetween(since: datetime, until: datetime, min_days=1, max_days=7) -> list[datetime]:
    """Generate a list with days between since and until with the range clipped according to clip_interval.

    :param datetime since: start date
    :param datetime util: end date
    :return list[datetime]: list with dates corresponding to each day in the range
    """
    n_days = (until - since).days + 1
    n_days = min(max_days, n_days)
    n_days = max(min_days, n_days)
    days = [since + timedelta(days=i) for i in range(n_days)]
    return days


@router.get("/repos/{owner}/{repo}/stats/daily_commits", response_model=list[DailyCommits])
async def get_daily_commits(owner: str = Path(description="The account owner of the repository. The name is not case sensitive."),
                            repo: str = Path(description="The name of the repository. The name is not case sensitive."),
                            author: str | None = Query(default=None, description="GitHub login of specific author"),
                            page: int = Query(default=1, description="Page number"),
                            per_page: int = Query(default=2, ge=1, le=5, description="Authors per page"),
                            since: datetime | None = Query(default=None, description="Start date (range will be trimmed to a maximum of 7 days after start date). Timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ"),
                            until: datetime | None = Query(default=None, description="End date  (range will be trimmed to a maximum of 7 days after start date). Timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ"),
                            github: GitHubFacade = Depends(get_github_facade)
                            ):
    if not since:
        since = datetime.now()
    if not until:
        until = datetime.now()
    days = _getDaysBetween(since, until, min_days=1, max_days=7)

    contributors = [author] if author else (await github.get_contributors(owner, repo, page, per_page))
    daily_commits = []
    for contributor in contributors:
        # TO IMPROVE: use asyncio.gather to run all calls to GitHub concurrently
        commits_on_day = {day: await (github.count_commits_on_day(owner, repo, contributor, day)) for day in days}
        daily_commits.append(DailyCommits(author=contributor, commits_on_day=commits_on_day))
    return daily_commits


@router.get("/repos/{owner}/{repo}/commits", response_model=list[Commit])
async def get_commits(owner: str = Path(description="The account owner of the repository. The name is not case sensitive."),
                      repo: str = Path(description="The name of the repository. The name is not case sensitive."),
                      author: str | None = Query(default=None, description="GitHub login or email address by which to filter by commit author."),
                      page: int = Query(default=1, description="Page number"),
                      per_page: int = Query(default=30, ge=1, le=100, description="Items per page"),
                      since: datetime | None = Query(default=None, description="Only show commits updated after the given time. Timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ"),
                      until: datetime | None = Query(default=None, description="Only commits before this date will be returned. Timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ"),
                      github: GitHubFacade = Depends(get_github_facade)
                      ):
    return await github.get_commits(owner, repo, author, page, per_page, since, until)
