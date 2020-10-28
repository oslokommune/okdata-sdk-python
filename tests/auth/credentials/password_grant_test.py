import json
import logging

import pytest
from origo.sdk.auth.credentials.password_grant import TokenServiceProvider
from origo.sdk.config import Config
from tests.auth.client_credentials_test_utils import from_cache_not_expired_token

logging.basicConfig(level=logging.INFO)


@pytest.fixture
def token_service_provider(requests_mock):
    config = Config(env="dev")
    config.config["tokenService"] = "http://localhost/token"
    response = json.dumps(
        {
            "access_token": from_cache_not_expired_token,
            "refresh_token": from_cache_not_expired_token,
        }
    )
    requests_mock.register_uri(
        "POST", "http://localhost/token", text=response, status_code=200
    )
    return TokenServiceProvider(config, "username", "password")


def test_token_service_get_token(token_service_provider):
    tokens = token_service_provider.new_token()
    assert tokens["access_token"] == from_cache_not_expired_token
