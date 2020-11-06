from typing import Optional
from keycloak.keycloak_openid import KeycloakOpenID  # type: ignore

from okdata.sdk.auth.credentials.common import (
    TokenProvider,
    TokenProviderNotInitialized,
)
from okdata.sdk.config import Config


class ClientCredentialsProvider(TokenProvider):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    # TODO: Annotate the class with `@dataclass` and remove this once support
    # for Python 3.6 is dropped.
    def __init__(
        self, config: Config, client_id: str = None, client_secret: str = None
    ):
        super().__init__(config)
        self.client_id = client_id
        self.client_secret = client_secret
        self.__post_init__()

    def __post_init__(self):
        if not self.client_id:
            self.client_id = self.config.config.get("client_id")
        if not self.client_secret:
            self.client_secret = self.config.config.get("client_secret")

        if not (self.client_id and self.client_secret):
            raise TokenProviderNotInitialized

        self.client = KeycloakOpenID(
            server_url=self.config.config.get("keycloakServerUrl") + "/",
            realm_name=self.config.config.get("keycloakRealm"),
            client_id=self.client_id,
            client_secret_key=self.client_secret,
        )

    def refresh_token(self, refresh_token):
        return self.client.refresh_token(refresh_token=refresh_token)

    def new_token(self):
        return self.client.token(grant_type=["client_credentials"])
