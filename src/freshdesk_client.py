import json
import logging
from dataclasses import dataclass
from typing import Tuple, Optional

import requests
from requests import RequestException


@dataclass
class FreshdeskContact:
    name: str
    email: str
    address: str
    twitter_id: str


CONTACTS_ENDPOINT = "/api/v2/contacts"
URL_PREFIX = "https://"
FRESHDESK_DOMAIN = ".freshdesk.com"


class FreshdeskClient:
    """
    Client for interacting with Freshdesk APIs
    """

    def __init__(self, url: str, api_token: str):
        logging.debug(f"Initializing Freshdesk client for url {url}")
        self._url = url
        self._api_token = api_token

    def create_or_update_contact(self, contact: FreshdeskContact) -> None:
        """
        Creates a Freshdesk contact. If there already exists contact with such email or twitter id its attributes will
        be updated with the provided ones.
        If the provided contact is softly deleted, then the operation would fail.

        :param contact: the contact to be created or updated
        """
        if contact.email is None and contact.twitter_id is None:
            raise ValueError("The contact provided has neither email nor twitter id."
                             " It is mandatory to have at least one of them.")

        contact_id = self._get_contact_id(contact)
        if contact_id is not None:
            logging.info("Existing contact was found, will attempt to update it.")
            self._update_contact(contact, contact_id)
        else:
            logging.info("No such contact was found, will attempt to create new one.")
            self._create_contact(contact)
        logging.info("Contact was successfully created or updated.")

    def _create_contact(self, contact: FreshdeskContact):
        logging.debug(f"Attempting to create contact")
        try:
            response = requests.post(url=self._url + CONTACTS_ENDPOINT,
                                     headers=self._get_headers(),
                                     data=json.dumps(contact.__dict__),
                                     auth=self._get_basic_auth())
            response.raise_for_status()
            logging.debug(f"Contact was successfully created")
        except RequestException as request_exception:
            logging.error(f"Error occurred while trying to create contact id for email {contact.email}")
            raise request_exception

    def _get_contact_id(self, contact: FreshdeskContact) -> Optional[int]:
        try:
            logging.debug(f"Attempting to retrieve contact id for email {contact.email} "
                          f"and twitter id {contact.twitter_id}")
            response = requests.get(url=self._url + CONTACTS_ENDPOINT,
                                    headers=self._get_headers(),
                                    params={"email": contact.email, "twitter_id": contact.twitter_id},
                                    auth=self._get_basic_auth())
            response.raise_for_status()
            json_resp = response.json()
            if len(json_resp) == 0:
                logging.debug(f"No existing contact with email {contact.email} "
                              f"and twitter id {contact.twitter_id} was found")
                return None  # no contact with this mail was found
            else:
                logging.debug(f"Found contact with email {contact.email} and twitter id {contact.twitter_id}")
                return json_resp[0]["id"]
        except RequestException as request_exception:
            logging.error(f"Error occurred while trying to retrieve contact id for email {contact.email} and "
                          f"twitter id {contact.twitter_id}")
            raise request_exception

    def _update_contact(self, contact: FreshdeskContact, contact_id: int):
        try:
            logging.debug(f"Attempting to update contact with id {contact_id}")
            response = requests.put(
                url=self._url + CONTACTS_ENDPOINT + "/" + str(contact_id),
                headers=self._get_headers(),
                data=json.dumps(contact.__dict__),
                auth=self._get_basic_auth())
            response.raise_for_status()
            logging.debug(f"Successfully updated contact with id {contact_id}")
        except RequestException as request_exception:
            logging.error(f"Error occurred while trying to update contact with id {contact_id}")
            raise request_exception

    @staticmethod
    def _get_headers() -> dict:
        return {"content-type": "application/json"}

    def _get_basic_auth(self) -> Tuple[str, str]:
        return self._api_token, "X"  # https://developers.freshdesk.com/api/#authentication
