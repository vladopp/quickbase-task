import argparse
import logging
from os import environ

from freshdesk_client import FreshdeskClient, URL_PREFIX, FRESHDESK_DOMAIN
from github_client import GithubClient
from utils import transform_github_user_to_freshdesk_contact, validate_github_username

FRESHDESK_TOKEN_ENV_KEY = "FRESHDESK_TOKEN"
GITHUB_TOKEN_ENV_KEY = "GITHUB_TOKEN"


def run():
    parser = argparse.ArgumentParser(description="""
    Retrieves the information of a GitHub User and creates a new Contact or updates an existing one in Freshdesk,
     using their respective APIs
    """)
    parser.add_argument('--github-username',
                        dest='username',
                        type=str,
                        help='The Github username that should be processed')
    parser.add_argument('--freshdesk-subdomain',
                        dest='freshdesk_subdomain',
                        type=str,
                        help='The Freshdesk subdomain to be used')

    args = parser.parse_args()
    validate_github_username(args.username)
    logging.info(f"Starting Github user to Freshdesk processing for user {args.username} "
                 f"and Freshdesk subdomain {args.freshdesk_subdomain}")

    github_client = GithubClient(environ[GITHUB_TOKEN_ENV_KEY])
    github_user = github_client.get_user(args.username)

    freshdesk_url = URL_PREFIX + args.freshdesk_subdomain + FRESHDESK_DOMAIN
    freshdesk_client = FreshdeskClient(freshdesk_url, environ[FRESHDESK_TOKEN_ENV_KEY])
    freshdesk_contact = transform_github_user_to_freshdesk_contact(github_user)
    freshdesk_client.create_or_update_contact(freshdesk_contact)
    logging.info(f"Github user {args.username} was successfully processed to freshdesk {args.freshdesk_subdomain}")


if __name__ == '__main__':
    # useful for local run setup - Set keys
    # environ[FRESHDESK_TOKEN_ENV_KEY] = ""
    # environ[GITHUB_TOKEN_ENV_KEY] = ""
    logging.basicConfig(level=environ.get("LOG_LEVEL", "DEBUG"))
    run()
