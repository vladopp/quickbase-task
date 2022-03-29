import json

from werkzeug import Request, Response

from github_client import GithubClient, GithubUser


def test_get_user(httpserver):
    mock_server_url = httpserver.url_for("")
    test_username = "username"
    actual_request_headers = {}
    expected_request_headers = {"Authorization": "token api_key", "Accept": "application/vnd.github.v3+json"}

    def store_headers_and_return_result(req: Request):
        actual_request_headers.update(req.headers)
        return Response(status=200, response=json.dumps(GITHUB_RESPONSE))

    httpserver.expect_request(
        method="GET",
        uri="/users/" + test_username
    ).respond_with_handler(store_headers_and_return_result)

    github_client = GithubClient("api_key", mock_server_url)
    actual_github_user = github_client.get_user(test_username)
    expected_github_user = GithubUser("Some Name", "some@email.com", "some location", "twitter username")

    assert actual_github_user == expected_github_user
    assert actual_request_headers["Authorization"] == expected_request_headers["Authorization"]
    assert actual_request_headers["Accept"] == expected_request_headers["Accept"]


GITHUB_RESPONSE = {
    "login": "username",
    "id": 11111111,
    "node_id": "MDQ6VXNlcjEwODUxNDQx",
    "avatar_url": "https://avatars.githubusercontent.com/u/10851441?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/username",
    "html_url": "https://github.com/username",
    "followers_url": "https://api.github.com/users/username/followers",
    "following_url": "https://api.github.com/users/username/following{/other_user}",
    "gists_url": "https://api.github.com/users/username/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/username/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/username/subscriptions",
    "organizations_url": "https://api.github.com/users/username/orgs",
    "repos_url": "https://api.github.com/users/username/repos",
    "events_url": "https://api.github.com/users/username/events{/privacy}",
    "received_events_url": "https://api.github.com/users/username/received_events",
    "type": "User",
    "site_admin": False,
    "name": "Some Name",
    "company": "company",
    "blog": "",
    "location": "some location",
    "email": "some@email.com",
    "hireable": True,
    "bio": None,
    "twitter_username": "twitter username",
    "public_repos": 12,
    "public_gists": 3,
    "followers": 19,
    "following": 7,
    "created_at": "2015-02-04T16:01:58Z",
    "updated_at": "2022-03-26T11:31:17Z",
    "private_gists": 7,
    "total_private_repos": 0,
    "owned_private_repos": 0,
    "disk_usage": 5815,
    "collaborators": 0,
    "two_factor_authentication": False,
    "plan": {
        "name": "free",
        "space": 976562499,
        "collaborators": 0,
        "private_repos": 10000
    }
}
