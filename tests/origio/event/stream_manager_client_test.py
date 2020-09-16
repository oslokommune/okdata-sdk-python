import re
import pytest
from requests.exceptions import HTTPError

from origo.event.event_stream_client import EventStreamClient

dataset_id = "dataset-id"
version = "1"
sink_id = "a1b2c3"

event_stream_client = EventStreamClient()

event_stream_item_response = {
    "id": f"{dataset_id}/{version}",
    "status": "SOME_STATUS",
    "updated_by": "janedoe",
    "updated_at": "2020-08-03T07:42:18.114531+00:00",
    "create_raw": True,
    "deleted": False,
    "confidentiality": "green",
}
event_stream_deleted_response = {
    "message": f"Deleted event stream with id {dataset_id}/{version}"
}
subscribable_item_response = {
    "status": "SOME_STATUS",
    "updated_by": "janedoe",
    "updated_at": "2020-08-03T07:42:18.114531+00:00",
    "enabled": True,
}
sink_item_response = {"id": sink_id, "status": "SOME_STATUS", "type": "elasticsearch"}
sink_items_response = [sink_item_response]
sink_deleted_response = {
    "message": f"Deleted sink {sink_id} from stream {dataset_id}/{version}"
}


class TestEventStream:
    def test_create_event_stream(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri(
            "POST", matcher, json=event_stream_item_response, status_code=201
        )

        assert (
            event_stream_client.create_event_stream(dataset_id, version)
            == event_stream_item_response
        )

        assert (
            event_stream_client.create_event_stream(
                dataset_id, version, create_raw=True
            )
            == event_stream_item_response
        )

        assert requests_mock.last_request.json() == {"create_raw": True}

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 500])
    def test_create_event_stream_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri("POST", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.create_event_stream(
                dataset_id, version, create_raw=False
            )

    def test_get_event_stream(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri(
            "GET", matcher, json=event_stream_item_response, status_code=200
        )

        response = event_stream_client.get_event_stream_info(dataset_id, version)
        assert response == event_stream_item_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
    def test_get_event_stream_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri("GET", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.get_event_stream_info(dataset_id, version)

    def test_delete_event_stream(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri(
            "DELETE", matcher, json=event_stream_deleted_response, status_code=200
        )

        response = event_stream_client.delete_event_stream(dataset_id, version)
        assert response == event_stream_deleted_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 500])
    def test_delete_event_stream_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri("DELETE", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.delete_event_stream(dataset_id, version)


class TestSubscribable:
    def test_get_subscribable(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "GET", matcher, json=subscribable_item_response, status_code=200
        )

        response = event_stream_client.get_subscribable(dataset_id, version)
        assert response == subscribable_item_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
    def test_get_subscribable_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri("GET", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.get_subscribable(dataset_id, version)

    def test_enable_subscription(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "PUT", matcher, json=subscribable_item_response, status_code=200
        )
        response = event_stream_client.enable_subscription(dataset_id, version)
        assert response == subscribable_item_response
        assert requests_mock.last_request.json() == {"enabled": True}

    def test_disable_subscription(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "PUT", matcher, json=subscribable_item_response, status_code=200
        )
        response = event_stream_client.disable_subscription(dataset_id, version)
        assert response == subscribable_item_response
        assert requests_mock.last_request.json() == {"enabled": False}

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 500])
    def test_toggle_subscription_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri("PUT", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.enable_subscription(dataset_id, version)

        with pytest.raises(HTTPError):
            event_stream_client.disable_subscription(dataset_id, version)


class TestSinks:
    def test_get_sinks(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks")
        requests_mock.register_uri(
            "GET", matcher, json=sink_items_response, status_code=200
        )

        response = event_stream_client.get_sinks(dataset_id, version)
        assert response == sink_items_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 500])
    def test_get_sinks_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks")
        requests_mock.register_uri("GET", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.get_sinks(dataset_id, version)

    def test_enable_sink(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks")
        requests_mock.register_uri(
            "POST", matcher, json=sink_item_response, status_code=201
        )

        response = event_stream_client.enable_sink(dataset_id, version, sink_type="s3")
        assert response == sink_item_response
        assert requests_mock.last_request.json() == {"type": "s3"}

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 500])
    def test_enable_sink_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks")
        requests_mock.register_uri("POST", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.enable_sink(dataset_id, version, sink_type="s3")

    def test_get_sink(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks/{sink_id}")
        requests_mock.register_uri(
            "GET", matcher, json=sink_item_response, status_code=200
        )

        response = event_stream_client.get_sink(dataset_id, version, sink_id)
        assert response == sink_item_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
    def test_get_sink_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks/{sink_id}")
        requests_mock.register_uri("GET", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.get_sink(dataset_id, version, sink_id)

    def test_disable_sink(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks/{sink_id}")
        requests_mock.register_uri(
            "DELETE", matcher, json=sink_deleted_response, status_code=200
        )

        response = event_stream_client.disable_sink(dataset_id, version, sink_id)
        assert response == sink_deleted_response

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 500])
    def test_disable_sink_fail(self, requests_mock, status_code):
        matcher = re.compile(f"streams/{dataset_id}/{version}/sinks/{sink_id}")
        requests_mock.register_uri("DELETE", matcher, status_code=status_code)
        with pytest.raises(HTTPError):
            event_stream_client.disable_sink(dataset_id, version, sink_id)
