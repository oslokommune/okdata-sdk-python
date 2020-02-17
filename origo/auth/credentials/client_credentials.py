from dataclasses import dataclass

from keycloak.keycloak_openid import KeycloakOpenID

from origo.auth.credentials.common import TokenProvider, TokenProviderNotInitialized


@dataclass
class ClientCredentialsProvider(TokenProvider):
    client_id: str = None
    client_secret: str = None

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
