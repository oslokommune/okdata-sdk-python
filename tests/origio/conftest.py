import json
import re

import pytest

from tests.origio.test_utils import well_known_response, client_credentials_response


@pytest.fixture(autouse=True)
def mock_well_known(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://login-test.oslo.kommune.no/auth/realms/api-catalog/.well-known/openid-configuration",
        text=json.dumps(well_known_response),
        status_code=200,
    )


@pytest.fixture(autouse=True)
def mock_token_endpoint(requests_mock):
    requests_mock.register_uri(
        "POST",
        re.compile(".*/token$"),
        text=json.dumps(client_credentials_response),
        status_code=200,
    )


@pytest.fixture(scope="function", autouse=True)
def mock_home_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
