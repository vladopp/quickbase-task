import logging
from dataclasses import dataclass

import requests
from requests import RequestException

GITHUB_API_URL = "https://api.github.com"
USER_ENDPOINT = "/users/"


@dataclass
class GithubUser:
    name: str
    email: str
    location: str
    twitter_username: str


class GithubClient:
    """
    Client for interacting with Github APIs
    """

    def __init__(self, api_key: str = None, url: str = GITHUB_API_URL, request_timeout: int = 10):
        logging.debug("Initializing Github client")
        self._api_key = api_key
        self._url = url
        self._request_timeout = request_timeout

    def get_user(self, username: str) -> GithubUser:
        """
        Retrieves information for specific user using Users API https://docs.github.com/en/rest/reference/users
        """

        logging.info(f"Retrieving information for username {username}")
        headers = {"Accept": "application/vnd.github.v3+json"}
        # auth is optional for retrieving user info
        if self._api_key is not None:
            headers["Authorization"] = "token " + self._api_key
        try:
            response = requests.get(url=self._url + USER_ENDPOINT + username,
                                    headers=headers,
                                    timeout=self._request_timeout)
            response.raise_for_status()
            return self._create_github_user(response.json())
        except RequestException as request_exception:
            logging.error(f"Error occurred while trying to retrieve information for user {username}")
            raise request_exception

    @staticmethod
    def _create_github_user(response: dict) -> GithubUser:
        return GithubUser(name=response["name"],
                          email=response["email"],
                          location=response["location"],
                          twitter_username=response["twitter_username"])
