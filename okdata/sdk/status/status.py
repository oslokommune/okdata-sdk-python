import logging

from okdata.sdk import SDK

log = logging.getLogger()


class Status(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "status"
        super().__init__(config, auth, env)

    def get_status(self, uuid, retries=0):
        url = self.config.get("statusApiUrl")
        log.info(f"Retrieving status for UUID={uuid} from: {url}")
        response = self.get(f"{url}/{uuid}", retries=retries)
        response.raise_for_status()
        return response.json()

    def update_status(self, trace_id, data, retries=0):
        url = self.config.get("statusApiUrl")
        response = self.post(f"{url}/{trace_id}", data, retries=retries)
        response.raise_for_status()
        return response.json()
