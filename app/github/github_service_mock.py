""" Mock of external GitHub API.
"""
from datetime import datetime

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
    with open(MOCK_DATA_COMMITS_JSON_FILE_PATH) as fin:
        return fin.read()


class MockResponse:
    pass


class GitHubServiceMock(GitHubService):
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
        r = MockResponse()
        r.json = readJsonDump(MOCK_DATA_COMMITS_JSON_FILE_PATH)
        r.headers = readHeaderDump(MOCK_DATA_COMMITS_HEADERS_FILE_PATH)
        return r
    
    async def get_contributors(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ):
        r = MockResponse()
        with open(MOCK_DATA_CONTRIBUTORS_JSON_FILE_PATH) as fin:
            r.json = fin.read()
        r.headers = readHeaderDump(MOCK_DATA_CONTRIBUTORS_HEADERS_FILE_PATH)
        return r

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass  # no resources to close in this mock
