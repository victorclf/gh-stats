from datetime import datetime
from fastapi import APIRouter, Query, Depends
from app.dependencies import get_github_facade

from app.github.github_facade import GitHubFacade


router = APIRouter(
    prefix="/api/v1",
    tags=["commits"]
)

@router.get("/repos/{owner}/{repo}/stats/daily_commits")
async def get_daily_commits(owner: str,
                      repo: str,
                      page: int = Query(default=1, description="Page number"),
                      per_page: int = Query(default=1, ge=1, le=10, description="Authors per page"),
                      since: datetime | None = Query(default=None, description="Only show commits updated after the given time."),
                      until: datetime | None = Query(default=None, description="Only commits before this date will be returned."),
                      github: GitHubFacade = Depends(get_github_facade)
):
    return await github.count_commits_on_day(owner, repo, until)


@router.get("/repos/{owner}/{repo}/commits")
async def get_commits(owner: str,
                      repo: str,
                      author: str | None = Query(default=None, description="GitHub login or email address by which to filter by commit author."),
                      page: int = Query(default=1, description="Page number"),
                      per_page: int = Query(default=30, ge=30, le=100, description="Items per page"),
                      since: datetime | None = Query(default=None, description="Only show commits updated after the given time."),
                      until: datetime | None = Query(default=None, description="Only commits before this date will be returned."),
                      github: GitHubFacade = Depends(get_github_facade)
):
    # TODO finish this
    return await github.get_commits(owner, repo)
