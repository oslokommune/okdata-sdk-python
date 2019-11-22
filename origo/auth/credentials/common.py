from dataclasses import dataclass

from origo.config import Config


class TokenProviderNotInitialized(Exception):
    pass


@dataclass
class TokenProvider:
    config: Config

    def new_token(self):
        raise NotImplementedError

    def refresh_token(self, refresh_token):
        raise NotImplementedError
