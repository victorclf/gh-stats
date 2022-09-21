from datetime import datetime
import json

from app.github.github_service import GitHubService

# curl -v -H "Accept: application/vnd.github+json" https://api.github.com/repos/elastic/kibana/commits -D mockdata_commits.head -o mockdata_commits.json
MOCK_DATA_COMMITS_JSON_FILE_PATH = 'app/github/mockdata_commits.json'
MOCK_DATA_COMMITS_HEADERS_FILE_PATH = 'app/github/mockdata_commits.head'

# curl -v -H "Accept: application/vnd.github+json" https://api.github.com/repos/elastic/kibana/contributors -D mockdata_contributors.head -o mockdata_contributors.json
MOCK_DATA_CONTRIBUTORS_JSON_FILE_PATH = 'app/github/mockdata_contributors.json'
MOCK_DATA_CONTRIBUTORS_HEADERS_FILE_PATH = 'app/github/mockdata_contributors.head'


def readHeaderDump(headerDumpFile):
    headers = {}
    with open(headerDumpFile) as fin:
        for line in fin.readlines():
            if ':' in line:  # skip first line with response code
                property, value = line.strip().split(':', 1)
                headers[property] = value
    return headers


def readJsonDump(jsonDumpFile):
    with open(jsonDumpFile) as fin:
        return json.load(fin)


class MockResponse:
    def __init__(self, json, headers):
        self._json = json
        self.headers = headers

    def json(self):
        return self._json


class GitHubServiceMock(GitHubService):
    """ Mock of external GitHub API.
    """
    
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
        json = readJsonDump(MOCK_DATA_COMMITS_JSON_FILE_PATH)
        headers = readHeaderDump(MOCK_DATA_COMMITS_HEADERS_FILE_PATH)
        return MockResponse(json[(page - 1) * per_page:per_page], headers)

    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ):
        json = readJsonDump(MOCK_DATA_CONTRIBUTORS_JSON_FILE_PATH)
        headers = readHeaderDump(MOCK_DATA_CONTRIBUTORS_HEADERS_FILE_PATH)
        return MockResponse(json[(page - 1) * per_page:per_page], headers)

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass  # no resources to close in this mock
