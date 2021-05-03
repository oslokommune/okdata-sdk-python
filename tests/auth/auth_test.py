import json
import logging
import re

import pytest

from okdata.sdk.auth.auth import Authenticate
from okdata.sdk.auth.credentials.client_credentials import ClientCredentialsProvider
from okdata.sdk.config import Config
from okdata.sdk.exceptions import ApiAuthenticateError
from freezegun import freeze_time

from tests.auth.client_credentials_test_utils import (
    from_cache_not_expired_token,
    from_cache_expired_token,
    utc_now,
)
from tests.test_utils import client_credentials_response

logging.basicConfig(level=logging.INFO)


config = Config(env="prod")
token_endpoint = "https://login.oslo.kommune.no/auth/realms/api-catalog/protocol/openid-connect/token"


@pytest.fixture(scope="function")
def mock_home_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))


@freeze_time(utc_now)
class TestAuthenticate:
    def test_authenticate_cache_disabled(self, requests_mock, mock_home_dir):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = False

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth.access_token == client_credentials_response["access_token"]
        assert auth.refresh_token == client_credentials_response["refresh_token"]

    def test_authenticat_no_cache(self, requests_mock, mock_home_dir):

        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = True

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth.access_token == client_credentials_response["access_token"]
        assert auth.refresh_token == client_credentials_response["refresh_token"]

    def test_authenticate_cached_credentials(self, mock_home_dir):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = True
        cached_credentials = {
            "provider": "ClientCredentialsProvider",
            "access_token": from_cache_not_expired_token,
            "refresh_token": from_cache_not_expired_token,
        }

        auth.file_cache.write_credentials(json.dumps(cached_credentials))
        auth.login()
        assert auth.access_token == cached_credentials["access_token"]
        assert auth.refresh_token == cached_credentials["refresh_token"]

    def test_authenticate_refresh_credentials(self, requests_mock, mock_home_dir):

        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = True

        cached_credentials = {
            "provider": "ClientCredentialsProvider",
            "access_token": from_cache_not_expired_token,
            "refresh_token": from_cache_not_expired_token,
        }

        auth.file_cache.write_credentials(json.dumps(cached_credentials))

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth.access_token == cached_credentials["access_token"]
        assert auth.refresh_token == cached_credentials["refresh_token"]

    def test_authenticate_expired_tokens(self, requests_mock, mock_home_dir):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = True

        cached_credentials = {
            "provider": "TokenServiceProvider",
            "access_token": from_cache_expired_token,
            "refresh_token": from_cache_expired_token,
        }

        auth.file_cache.write_credentials(json.dumps(cached_credentials))

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        print(from_cache_not_expired_token)
        print(from_cache_expired_token)
        assert auth.access_token == client_credentials_response["access_token"]
        assert auth.refresh_token == client_credentials_response["access_token"]

    def test_authenticate_expired_access_token(self, requests_mock, mock_home_dir):
        client_credentials_provider = ClientCredentialsProvider(config)
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        auth.file_cache.credentials_cache_enabled = True

        cached_credentials = {
            "provider": "TokenServiceProvider",
            "access_token": from_cache_expired_token,
            "refresh_token": from_cache_not_expired_token,
        }

        auth.file_cache.write_credentials(json.dumps(cached_credentials))

        response = json.dumps(client_credentials_response)
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        auth.login()
        assert auth.access_token == from_cache_not_expired_token
        assert auth.refresh_token == cached_credentials["refresh_token"]

    def test_authenticate_fail(self, requests_mock, mock_home_dir):
        client_credentials_provider = ClientCredentialsProvider(
            config, client_id="wrong_id"
        )
        auth = Authenticate(config=config, token_provider=client_credentials_provider)

        response = json.dumps(
            {"error": "authenitcation error", "error_description": "No such client"}
        )
        matcher = re.compile(token_endpoint)
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        try:
            auth.login()
        except ApiAuthenticateError:
            assert True
