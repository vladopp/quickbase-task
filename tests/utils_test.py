import unittest

from freshdesk_client import FreshdeskContact
from github_client import GithubUser
from utils import validate_github_username, transform_github_user_to_freshdesk_contact


class UtilsTest(unittest.TestCase):

    def test_validate_github_username_valid_username(self):
        validate_github_username("valid-username")

    def test_validate_github_username_invalid_username_none(self):
        with self.assertRaises(ValueError):
            validate_github_username(None)

    def test_validate_github_username_invalid_username_empty(self):
        with self.assertRaises(ValueError):
            validate_github_username("")

    def test_validate_github_username_invalid_username_dash_prefix(self):
        with self.assertRaises(ValueError):
            validate_github_username("-username")

    def test_validate_github_username_invalid_username_dash_suffix(self):
        with self.assertRaises(ValueError):
            validate_github_username("username-")

    def test_validate_github_username_invalid_username_two_dashes(self):
        with self.assertRaises(ValueError):
            validate_github_username("in--valid")

    def test_validate_github_username_invalid_username_underscore(self):
        with self.assertRaises(ValueError):
            validate_github_username("in_valid")

    def test_validate_github_username_invalid_username_long(self):
        with self.assertRaises(ValueError):
            validate_github_username("tooooooloooooooooooooooooooooooooooooong")

    def test_transform_github_user_to_freshdesk_contact(self):
        github_user = GithubUser("name", "email", "location", "tweet")
        actual_freshdesk_contact = transform_github_user_to_freshdesk_contact(github_user)
        expected_freshdesk_contact = FreshdeskContact("name", "email", "location", "tweet")
        self.assertEqual(actual_freshdesk_contact, expected_freshdesk_contact)
