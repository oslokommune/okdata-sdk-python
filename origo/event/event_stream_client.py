import logging
from origo.sdk import SDK

log = logging.getLogger()


class EventStreamClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "event_stream_client"
        super().__init__(config, auth, env)
        self.stream_manager_url = self.config.get("streamManagerUrl")

    def create_event_stream(self, dataset_id, version):
        response = self.post(self.event_stream_url(dataset_id, version), data=None)
        return response.json()

    def get_event_stream_info(self, dataset_id, version):
        response = self.get(self.event_stream_url(dataset_id, version))
        return response.json()

    def delete_event_stream(self, dataset_id, version):
        response = self.delete(self.event_stream_url(dataset_id, version))
        return response.json()

    def event_stream_url(self, dataset_id, version):
        return f"{self.stream_manager_url}/stream/{dataset_id}/{version}"
