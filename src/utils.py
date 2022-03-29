import re

from freshdesk_client import FreshdeskContact
from github_client import GithubUser

USERNAME_PATTERN = "^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"


def transform_github_user_to_freshdesk_contact(user: GithubUser) -> FreshdeskContact:
    """
    Transforms GithubUser to FreshdeskContact.

    :param user: the Github user to transform
    :return: FreshdeskContact object with the compatible attributes populated
    """
    return FreshdeskContact(name=user.name,
                            email=user.email,
                            address=user.location,
                            twitter_id=user.twitter_username)


def validate_github_username(username: str) -> None:
    """
    Checks if the provided string is valid Github username.

    :param username: the string to check
    :raises ValueError if the username is invalid
    """
    if username is None or len(username) < 1 or len(username) > 39 or not re.match(USERNAME_PATTERN, username):
        raise ValueError(f"Invalid github username is provided {username}.Username may only contain alphanumeric"
                         f" characters or single hyphens, and cannot begin or end with a hyphen.")
