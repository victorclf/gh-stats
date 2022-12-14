import pytest
from app.dependencies import get_github_service
from app.github.github_service_mock import GitHubServiceMock
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


async def mock_github_service():
    async with GitHubServiceMock() as service:
        yield service

@pytest.fixture(scope="module", autouse=True)
def mock_github_fixture():
    app.dependency_overrides[get_github_service] = mock_github_service
    yield
    app.dependency_overrides = {}



owner = "abc"
repo = "abc"


def test_get_daily_commits():
    per_page = 3
    start_day = '2022-09-17'
    end_day = '2022-09-20'
    n_days = 4

    response = client.get(f"/api/v1/repos/{owner}/{repo}/stats/daily_commits?start_day={start_day}&end_day={end_day}&per_page={per_page}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for stat in j:
        assert len(stat['commits_on_day']) == n_days


def test_get_daily_commits_clip_min_days():
    per_page = 3
    start_day = '2020-09-20'
    end_day = start_day
    n_days = 1

    response = client.get(f"/api/v1/repos/{owner}/{repo}/stats/daily_commits?start_day={start_day}&end_day={end_day}&per_page={per_page}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for stat in j:
        assert len(stat['commits_on_day']) == n_days


def test_get_daily_commits_clip_max_days():
    per_page = 3
    start_day = '2020-09-10'
    end_day = '2022-09-20'
    n_days = 7

    response = client.get(f"/api/v1/repos/{owner}/{repo}/stats/daily_commits?start_day={start_day}&end_day={end_day}&per_page={per_page}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for stat in j:
        assert len(stat['commits_on_day']) == n_days


def test_get_commits():
    per_page = 5

    response = client.get(f"/api/v1/repos/{owner}/{repo}/commits?per_page={per_page}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for commit in j:
        assert all((prop in commit for prop in ['author', 'date', 'message']))
