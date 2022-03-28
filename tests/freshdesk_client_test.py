import json

from werkzeug import Request, Response
from unittest import TestCase

from freshdesk_client import FreshdeskClient, FreshdeskContact


def test_create_user(httpserver):
    mock_server_url = httpserver.url_for("")
    actual_get_contacts_request_parameters = {}
    expected_get_contacts_request_parameters = {"email": "email", "twitter_id": "twitter-id"}

    def handle_get_contacts(req: Request):
        actual_get_contacts_request_parameters.update(req.args)
        return Response(status=200, response=json.dumps([CONTACT_RESPONSE]))

    httpserver.expect_request(
        method="GET",
        uri="/api/v2/contacts",
    ).respond_with_handler(handle_get_contacts)

    actual_update_contact_body = {}
    expected_update_contact_body = {"name": "name", "email": "email", "address": "address", "twitter_id": "twitter-id"}

    def handle_update_contact(req: Request):
        actual_update_contact_body.update(req.get_json())
        return Response(status=200, response=json.dumps([CONTACT_RESPONSE]))

    httpserver.expect_request(
        method="PUT",
        uri="/api/v2/contacts/2",
    ).respond_with_handler(handle_update_contact)

    freshdesk_client = FreshdeskClient(mock_server_url, "api-token")
    contact = FreshdeskContact("name", "email", "address", "twitter-id")
    freshdesk_client.create_or_update_contact(contact)

    TestCase().assertDictEqual(expected_update_contact_body, actual_update_contact_body)
    TestCase().assertDictEqual(expected_get_contacts_request_parameters, actual_get_contacts_request_parameters)


def test_update_user(httpserver):
    mock_server_url = httpserver.url_for("")
    actual_get_contacts_request_parameters = {}
    expected_get_contacts_request_parameters = {"email": "email", "twitter_id": "twitter-id"}

    def handle_get_contacts(req: Request):
        actual_get_contacts_request_parameters.update(req.args)
        return Response(status=200, response=json.dumps([]))  # empty response -> no such contact

    httpserver.expect_request(
        method="GET",
        uri="/api/v2/contacts",
    ).respond_with_handler(handle_get_contacts)

    actual_create_contact_body = {}
    expected_create_contact_body = {"name": "name", "email": "email", "address": "address", "twitter_id": "twitter-id"}

    def handle_create_contact(req: Request):
        actual_create_contact_body.update(req.get_json())
        return Response(status=200, response=json.dumps([CONTACT_RESPONSE]))

    httpserver.expect_request(
        method="POST",
        uri="/api/v2/contacts",
    ).respond_with_handler(handle_create_contact)

    freshdesk_client = FreshdeskClient(mock_server_url, "api-token")
    contact = FreshdeskContact("name", "email", "address", "twitter-id")
    freshdesk_client.create_or_update_contact(contact)

    TestCase().assertDictEqual(expected_create_contact_body, actual_create_contact_body)
    TestCase().assertDictEqual(expected_get_contacts_request_parameters, actual_get_contacts_request_parameters)


CONTACT_RESPONSE = {
    "active": True,
    "address": "address",
    "company_id": None,
    "description": None,
    "email": "some@email.com",
    "id": 2,
    "job_title": None,
    "language": "en",
    "mobile": None,
    "name": "Rachel",
    "phone": None,
    "time_zone": "Chennai",
    "twitter_id": None,
    "created_at": "2015-08-18T16:18:14Z",
    "updated_at": "2015-08-24T09:25:19Z",
    "other_companies": [4],
    "custom_fields": None
  }
