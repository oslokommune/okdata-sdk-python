import logging
from origo.sdk import SDK

log = logging.getLogger()


class EventStreamClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "event_stream_client"
        super().__init__(config, auth, env)
        self.event_stream_api_url = self.config.get("eventStreamApiUrl")

    def create_event_stream(self, dataset_id, version, create_raw=True):
        response = self.post(
            f"{self.event_stream_api_url}/{dataset_id}/{version}",
            data={"create_raw": create_raw},
        )
        return response.json()

    def get_event_stream_info(self, dataset_id, version):
        response = self.get(f"{self.event_stream_api_url}/{dataset_id}/{version}")
        return response.json()

    def delete_event_stream(self, dataset_id, version):
        response = self.delete(f"{self.event_stream_api_url}/{dataset_id}/{version}")
        return response.json()
