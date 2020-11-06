from freezegun import freeze_time

from okdata.sdk.auth.util import is_token_expired
from tests.auth.client_credentials_test_utils import (
    not_expired_token,
    expired_token,
    utc_now,
)


class TestClientCredentials:
    @freeze_time(utc_now)
    def test_token_expiery(self):
        cc1 = {"access_token": expired_token, "refresh_token": expired_token}

        cc2 = {"access_token": not_expired_token, "refresh_token": not_expired_token}

        assert is_token_expired(cc1["access_token"])
        assert is_token_expired(cc1["refresh_token"])

        assert not is_token_expired(cc2["access_token"])
        assert not is_token_expired(cc2["refresh_token"])
