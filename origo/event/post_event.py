import logging
import requests
import os

from origo.sdk import SDK

log = logging.getLogger()


class PostEvent(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "post_event"
        super().__init__(config, auth, env)
        self.event_collector_url = self.config.get("eventCollectorUrl")

    def post_event(self, event_payload, dataset_id, version_id):

        if type(event_payload) is dict:
            post_url = f"{self.event_collector_url}/event/{dataset_id}/{version_id}"
        elif type(event_payload) is list:
            post_url = f"{self.event_collector_url}/events/{dataset_id}/{version_id}"
        else:
            raise TypeError(
                f"Invalid type: {type(event_payload)}. Must be either {list} or {dict}"
            )

        log.info(f"SDK:Posting event to: {post_url}")
        headers = self.headers()
        api_key = os.getenv("ORIGO_API_KEY", default=None)
        if api_key:
            log.info("SDK:Setting x-api-key from environment variable ORIGO_API_KEY")
            headers["x-api-key"] = api_key

        return handle_event_collector_response(
            requests.post(url=post_url, json=event_payload, headers=headers)
        )


def handle_event_collector_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
