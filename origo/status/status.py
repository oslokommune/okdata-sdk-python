import requests
import logging

from origo.sdk import SDK

log = logging.getLogger()


class Status(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "status"
        super().__init__(config, auth)

    def get_status(self, uuid):
        url = self.config.get("statusApiUrl")
        log.info(f"Retrieving status for UUID={uuid} from: {url}")
        response = requests.get(url + uuid)
        if response.status_code == 200:
            return response.json()
        else:
            log.info(f"Was unable to retrieve status for UUID={uuid} from: {url}")
            raise KeyError(response.status_code, uuid)
