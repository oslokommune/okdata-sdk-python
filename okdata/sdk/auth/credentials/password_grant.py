import logging
import requests
from typing import Optional
from okdata.sdk.auth.credentials.common import (
    TokenProviderNotInitialized,
    TokenProvider,
)
from okdata.sdk.config import Config

log = logging.getLogger()


class TokenServiceProvider(TokenProvider):
    username: Optional[str] = None
    password: Optional[str] = None

    # TODO: Annotate the class with `@dataclass` and remove this once support
    # for Python 3.6 is dropped.
    def __init__(self, config: Config, username: str = None, password: str = None):
        super().__init__(config)
        self.username = username
        self.password = password
        self.__post_init__()

    def __post_init__(self):
        self.token_service_url = self.config.config.get("tokenService")
        if not self.username:
            self.username = self.config.config.get("username")
        if not self.password:
            self.password = self.config.config.get("password")

        if not (self.username and self.password):
            raise TokenProviderNotInitialized

    def refresh_token(self, refresh_token):
        log.warning(
            f"Refresh token not implemented for {self.__class__}. Requesting new token"
        )
        return self.new_token()

    def new_token(self):
        payload = {"username": self.username, "password": self.password}
        response = requests.post(url=self.token_service_url, json=payload)
        return response.json()
