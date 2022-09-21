from fastapi.testclient import TestClient
from app.dependencies import get_github_service
from app.github.github_service_mock import GitHubServiceMock

from app.main import app


client = TestClient(app)

owner = "elastic"
repo = "kibana"


def test_get_daily_commits():
    per_page = 1
    start_day = '2022-09-15'
    end_day = '2022-09-15'
    n_days = 1
    author = 'lgmys'

    response = client.get(f"/api/v1/repos/{owner}/{repo}/stats/daily_commits?start_day={start_day}&end_day={end_day}&per_page={per_page}&author={author}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for stat in j:
        assert len(stat['commits_on_day']) == n_days
        assert stat['author'] == author
        assert stat['commits_on_day'][start_day] == 2


def test_get_commits():
    per_page = 2
    start_day = '2022-09-15'
    end_day = '2022-09-15'
    author = 'lgmys'

    response = client.get(f"/api/v1/repos/{owner}/{repo}/commits?per_page={per_page}&author={author}&start_day={start_day}&end_day={end_day}")

    assert response.status_code == 200
    j = response.json()
    assert len(j) == per_page
    for commit in j:
        assert all((prop in commit for prop in ['author', 'date', 'message']))
        assert commit['author'] == author
        assert commit['date'].startswith('2022-09-15')