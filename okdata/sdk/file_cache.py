import json
import logging

from okdata.sdk.io_utils import write_to_okdata_cache, read_from_okdata_cache

log = logging.getLogger()


class FileCache:
    def __init__(self, config):
        self.credentials_cache_enabled = config.get("cacheCredentials")
        self.env = config.get("env")

    def write_credentials(self, credentials):
        if self.credentials_cache_enabled:
            filename = f"client_credentials-{self.env}.json"
            log.debug(f"Writing credentials to cache: {filename}")
            write_to_okdata_cache(content=str(credentials), filename=filename)
        else:
            log.debug("Skipping write_credentials: cache is not enabled")

    def read_credentials(self):
        if self.credentials_cache_enabled:
            filename = f"client_credentials-{self.env}.json"
            credentials = read_from_okdata_cache(filename=filename)
            if credentials:
                try:
                    log.debug(f"Reading credentials from cache: {filename}")
                    return json.loads(credentials)
                except ValueError as ve:
                    log.debug(f"Could not read credentials from cache: {ve}")
        else:
            log.debug("Skipping write_credentials: cache is not enabled")
        return None
