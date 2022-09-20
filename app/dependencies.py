from fastapi import Depends
from app.github.github_facade import GitHubFacade
from app.github.github_service import GitHubService
from app.github.github_service_mock import GitHubServiceMock


async def get_github_service() -> GitHubService:
    async with GitHubServiceMock() as service:
        yield service


async def get_github_facade(github_service: GitHubService = Depends(get_github_service)) -> GitHubFacade:
    return GitHubFacade(github_service)
