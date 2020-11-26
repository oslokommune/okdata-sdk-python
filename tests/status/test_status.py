import json
import re
from requests.exceptions import HTTPError

from okdata.sdk.status import Status
from okdata.sdk.auth.auth import Authenticate
from okdata.sdk.config import Config
from okdata.sdk.file_cache import FileCache

config = Config()
file_cache = FileCache(config)
file_cache.credentials_cache_enabled = False
auth_default = Authenticate(config, file_cache=file_cache)


get_status_response = [{"trace_event_id": "my-id"}, {"trace_event_id": "my-other-id"}]


class TestGetStatus:
    def test_get_status(self, requests_mock):
        uuid = "my-uu-ii-dd-1"
        status = Status(config=config, auth=auth_default)
        response = json.dumps(get_status_response)
        matcher = re.compile(uuid)
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        body = status.get_status(uuid)
        assert len(body) == 2

    def test_get_status_fails_will_produce_http_error(self, requests_mock):
        uuid = "my-uu-ii-dd-2"
        status = Status(config=config, auth=auth_default)
        response = json.dumps(get_status_response)
        matcher = re.compile(uuid)
        requests_mock.register_uri("GET", matcher, text=response, status_code=404)
        try:
            status.get_status(uuid)
        except HTTPError:
            assert True


class TestUpdateStatus:
    def test_update_status(self, requests_mock):
        uuid = "dead-beef-cafe"
        data = {
            "trace_id": uuid,
            "something": "like this",
        }

        requests_mock.register_uri(
            "POST", f"/status-api/status/{uuid}", json=data, status_code=200
        )
        status = Status(config=config, auth=auth_default).update_status(uuid, {})
        assert status == data
