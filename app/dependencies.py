from typing import AsyncIterator

from fastapi import Depends

from app.github.github_facade import GitHubFacade
from app.github.github_service import GitHubService
from app.github.github_service_impl import GitHubServiceImpl


async def get_github_service() -> AsyncIterator[GitHubService]:
    async with GitHubServiceImpl() as service:
        yield service


async def get_github_facade(github_service: GitHubService = Depends(get_github_service)) -> GitHubFacade:
    return GitHubFacade(github_service)
