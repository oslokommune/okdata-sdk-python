from dataclasses import dataclass
from typing import Optional

from keycloak.exceptions import KeycloakGetError  # type: ignore
from keycloak.keycloak_openid import KeycloakOpenID  # type: ignore

from okdata.sdk.auth.credentials.common import (
    TokenProvider,
    TokenProviderNotInitialized,
    TokenRefreshError,
)


@dataclass
class ClientCredentialsProvider(TokenProvider):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

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
        try:
            return self.client.refresh_token(refresh_token=refresh_token)
        except KeycloakGetError as e:
            raise TokenRefreshError(str(e))

    def new_token(self):
        return self.client.token(grant_type=["client_credentials"])
