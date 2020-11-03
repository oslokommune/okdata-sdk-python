from origo.sdk.file_cache import FileCache
from origo.sdk.config import Config

config = Config()


def test_write_client_credentials():
    fc = FileCache(config)
    fc.credentials_cache_enabled = True
    cc = {"access_token": "yo", "refresh_token": "bro"}
    fc.write_credentials(cc)
    assert cc.__eq__(fc.read_credentials())


def test_disable_cache():
    fc = FileCache(config)
    fc.credentials_cache_enabled = False
    cc = {"access_token": "yo-bro", "refresh_token": "zup-dawg"}
    fc.write_credentials(cc)

    assert fc.read_credentials() is None
