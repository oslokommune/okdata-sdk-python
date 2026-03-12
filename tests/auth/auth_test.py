import json
import logging
import re

import pytest
from freezegun import freeze_time

from okdata.sdk.auth.auth import Authenticate
from okdata.sdk.auth.credentials.client_credentials import ClientCredentialsProvider
from okdata.sdk.config import Config
from okdata.sdk.exceptions import ApiAuthenticateError
from tests.auth.client_credentials_test_utils import (
    not_expired_token,
    utc_now,
)
from tests.test_utils import (
    client_credentials_response,
    client_credentials_response_no_refresh,
)

logging.basicConfig(level=logging.INFO)


config = Config(env="prod")
token_endpoint = "https://login.oslo.kommune.no/auth/realms/api-catalog/protocol/openid-connect/token"


@freeze_time(utc_now)
class TestAuthenticate:
    def test_authenticate(self, requests_mock):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth._access_token == client_credentials_response["access_token"]
        assert auth._refresh_token == client_credentials_response["refresh_token"]

    def test_authenticate_refresh_credentials(self, requests_mock):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth._access_token == not_expired_token
        assert auth._refresh_token == not_expired_token

    def test_authenticate_fail(self, requests_mock):
        client_credentials_provider = ClientCredentialsProvider(
            config, client_id="wrong_id"
        )
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        response = json.dumps(
            {"error": "authentication error", "error_description": "No such client"}
        )
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        with pytest.raises(ApiAuthenticateError):
            auth.login()

    def test_refresh_no_refresh_token(self, requests_mock):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        response = json.dumps(client_credentials_response_no_refresh)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()

        assert auth._access_token == not_expired_token
        assert auth._refresh_token is None
