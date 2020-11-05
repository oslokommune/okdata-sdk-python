import logging
from okdata.sdk import SDK

log = logging.getLogger()


class EventStreamClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "event_stream_client"
        super().__init__(config, auth, env)
        self.event_stream_url = self.config.get("eventStreamUrl")

    def create_event_stream(self, dataset_id, version, create_raw=True):
        response = self.post(
            f"{self.event_stream_url}/{dataset_id}/{version}",
            data={"create_raw": create_raw},
        )
        return response.json()

    def get_event_stream_info(self, dataset_id, version):
        response = self.get(f"{self.event_stream_url}/{dataset_id}/{version}")
        return response.json()

    def delete_event_stream(self, dataset_id, version):
        response = self.delete(f"{self.event_stream_url}/{dataset_id}/{version}")
        return response.json()

    def get_subscribable(self, dataset_id, version):
        response = self.get(
            f"{self.event_stream_url}/{dataset_id}/{version}/subscribable"
        )
        return response.json()

    def enable_subscription(self, dataset_id, version):
        response = self.put(
            f"{self.event_stream_url}/{dataset_id}/{version}/subscribable",
            data={"enabled": True},
        )
        return response.json()

    def disable_subscription(self, dataset_id, version):
        response = self.put(
            f"{self.event_stream_url}/{dataset_id}/{version}/subscribable",
            data={"enabled": False},
        )
        return response.json()

    def get_sinks(self, dataset_id, version):
        response = self.get(f"{self.event_stream_url}/{dataset_id}/{version}/sinks")
        return response.json()

    def enable_sink(self, dataset_id, version, sink_type):
        response = self.post(
            f"{self.event_stream_url}/{dataset_id}/{version}/sinks",
            data={"type": sink_type},
        )
        return response.json()

    def get_sink(self, dataset_id, version, sink_type):
        response = self.get(
            f"{self.event_stream_url}/{dataset_id}/{version}/sinks/{sink_type}"
        )
        return response.json()

    def disable_sink(self, dataset_id, version, sink_type):
        response = self.delete(
            f"{self.event_stream_url}/{dataset_id}/{version}/sinks/{sink_type}"
        )
        return response.json()
