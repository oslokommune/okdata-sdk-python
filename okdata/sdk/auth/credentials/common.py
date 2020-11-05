from okdata.sdk.config import Config


class TokenProviderNotInitialized(Exception):
    pass


class TokenProvider:
    config: Config

    # TODO: Annotate the class with `@dataclass` and remove this once support
    # for Python 3.6 is dropped.
    def __init__(self, config: Config):
        self.config = config

    def new_token(self):
        raise NotImplementedError

    def refresh_token(self, refresh_token):
        raise NotImplementedError
