import logging

from okdata.sdk import SDK

log = logging.getLogger()


class PostEvent(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "post_event"
        super().__init__(config, auth, env)
        self.event_collector_url = self.config.get("eventCollectorUrl")

    def post_event(self, event_payload, dataset_id, version_id, retries=0):

        if type(event_payload) is dict:
            post_url = f"{self.event_collector_url}/event/{dataset_id}/{version_id}"
        elif type(event_payload) is list:
            post_url = f"{self.event_collector_url}/events/{dataset_id}/{version_id}"
        else:
            raise TypeError(
                f"Invalid type: {type(event_payload)}. Must be either {list} or {dict}"
            )

        return self.post(post_url, event_payload, retries=retries).json()
