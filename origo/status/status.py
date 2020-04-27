import logging

from origo.sdk import SDK

log = logging.getLogger()


class Status(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "status"
        super().__init__(config, auth, env)

    def get_status(self, uuid):
        url = self.config.get("statusApiUrl")
        log.info(f"Retrieving status for UUID={uuid} from: {url}")
        response = self.get(f"{url}/{uuid}")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()
