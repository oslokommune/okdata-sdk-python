import json
import pytest
from requests.exceptions import HTTPError
from okdata.sdk.event.post_event import PostEvent
from okdata.sdk.auth.auth import Authenticate
from okdata.sdk.config import Config
from okdata.sdk.file_cache import FileCache
from tests.auth.client_credentials_test_utils import (
    default_test_client_credentials,
)

config = Config()
file_cache = FileCache(config)
file_cache.credentials_cache_enabled = False
auth_default = Authenticate(config, file_cache=file_cache)
auth_default.client_credentials = default_test_client_credentials

event_collector_ok_response = {"message": "Ok"}
event_collector_error_response = {"message": "Bad Request"}


class TestPostEvent:
    def test_post_event_object(self, requests_mock):
        post_event = PostEvent(config=config, auth=auth_default)
        dataset_id, version_id = "test", "1"
        event = {"yo": "bro"}
        expected_url = (
            f"{post_event.event_collector_url}/event/{dataset_id}/{version_id}"
        )
        requests_mock.register_uri(
            "POST",
            expected_url,
            text=json.dumps(event_collector_ok_response),
            status_code=200,
        )

        post_event_response = post_event.post_event(event, dataset_id, version_id)
        assert event_collector_ok_response == post_event_response

    def test_post_event_list(self, requests_mock):
        post_event = PostEvent(config=config, auth=auth_default)
        dataset_id, version_id = "test", "1"
        event_list = [{"yo": "bro"}, {"zup": "dawg"}]
        expected_url = (
            f"{post_event.event_collector_url}/events/{dataset_id}/{version_id}"
        )
        requests_mock.register_uri(
            "POST",
            expected_url,
            text=json.dumps(event_collector_ok_response),
            status_code=200,
        )
        post_event_response = post_event.post_event(event_list, dataset_id, version_id)
        assert event_collector_ok_response == post_event_response

    def test_post_event_fail(self, requests_mock):
        post_event = PostEvent(config=config, auth=auth_default)
        dataset_id, version_id = "test", "1"
        event = {"yo": "bro"}
        exp_url = f"{post_event.event_collector_url}/event/{dataset_id}/{version_id}"
        requests_mock.register_uri(
            "POST",
            exp_url,
            text=json.dumps(event_collector_error_response),
            status_code=400,
        )

        with pytest.raises(HTTPError):
            post_event.post_event(event, dataset_id, version_id)
