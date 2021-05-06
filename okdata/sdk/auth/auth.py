import json
import logging

from okdata.sdk.auth.credentials.client_credentials import ClientCredentialsProvider
from okdata.sdk.auth.credentials.common import (
    TokenProviderNotInitialized,
    TokenRefreshError,
)
from okdata.sdk.auth.credentials.password_grant import TokenServiceProvider
from okdata.sdk.auth.util import is_token_expired
from okdata.sdk.exceptions import ApiAuthenticateError
from okdata.sdk.file_cache import FileCache

log = logging.getLogger()


class Authenticate(object):
    def __init__(self, config, token_provider=None, file_cache=None):
        self.token_provider = token_provider
        if not self.token_provider:
            try:
                self.token_provider = next(self._resolve_token_provider(config))
                log.info(
                    f"Found credentials for {self.token_provider.__class__.__name__}"
                )
            except StopIteration:
                log.info("No valid auth strategies available")

        self.file_cache = file_cache
        if not self.file_cache:
            self.file_cache = FileCache(config)

        self._access_token = None
        self._refresh_token = None

    def _resolve_token_provider(self, config):
        # Add more TokenProviders to accept different login methods
        strategies = [ClientCredentialsProvider, TokenServiceProvider]

        for strat in strategies:
            try:
                yield strat(config)
            except TokenProviderNotInitialized:
                continue
            except Exception as e:
                log.exception(e)
                raise e

    # read only
    @property
    def access_token(self):
        if not self.token_provider:
            return None
        if not self._access_token:
            self.login()
        # If expired, refresh
        if is_token_expired(self._access_token):
            self.refresh_access_token()
        return self._access_token

    def login(self, force=False):
        if not self.token_provider:
            return

        cached = self.file_cache.read_credentials()
        if cached:
            self._access_token = cached["access_token"]
            self._refresh_token = cached.get("refresh_token")

        if self._access_token and not is_token_expired(self._access_token):
            log.info("Token not expired, skipping")
            return
        self.refresh_access_token()

    def refresh_access_token(self):
        if not self.token_provider:
            return

        tokens = None

        if self._refresh_token and not is_token_expired(self._refresh_token):
            try:
                tokens = self.token_provider.refresh_token(self._refresh_token)
            except TokenRefreshError as e:
                log.warn(f"Error refreshing token: {e}")

        if not tokens:
            tokens = self.token_provider.new_token()
            if "access_token" not in tokens:
                raise ApiAuthenticateError
            self._refresh_token = tokens.get("refresh_token")

        self._access_token = tokens["access_token"]
        self.file_cache.write_credentials(credentials=self)

    def __repr__(self):
        return json.dumps(
            {
                "provider": self.token_provider.__class__.__name__,
                "access_token": self._access_token,
                "refresh_token": self._refresh_token,
            }
        )

    def __str__(self):
        return self.__repr__()


class Authorize:
    def __init__(self):
        pass
