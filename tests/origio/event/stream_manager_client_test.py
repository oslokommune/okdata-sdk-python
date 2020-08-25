import re

from origo.event.event_stream_client import EventStreamClient

dataset_id = "dataset-id"
version = "1"

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

    def test_get_event_stream(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri(
            "GET", matcher, json=event_stream_item_response, status_code=200
        )

        assert (
            event_stream_client.get_event_stream_info(dataset_id, version)
            == event_stream_item_response
        )

    def test_delete_event_stream(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}")
        requests_mock.register_uri(
            "DELETE", matcher, json=event_stream_deleted_response, status_code=200
        )

        assert (
            event_stream_client.delete_event_stream(dataset_id, version)
            == event_stream_deleted_response
        )


class TestSubscribable:
    def test_get_subscribable(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "GET", matcher, json=subscribable_item_response, status_code=200
        )

        response = event_stream_client.get_subscribable(dataset_id, version)
        assert response == subscribable_item_response

    def test_enable_subscribable(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "PUT", matcher, json=subscribable_item_response, status_code=200
        )
        response = event_stream_client.enable_subscribable(dataset_id, version)
        assert response == subscribable_item_response
        assert requests_mock.last_request.json() == {"enabled": True}

    def test_disable_subscribable(self, requests_mock):
        matcher = re.compile(f"streams/{dataset_id}/{version}/subscribable")
        requests_mock.register_uri(
            "PUT", matcher, json=subscribable_item_response, status_code=200
        )
        response = event_stream_client.disable_subscribable(dataset_id, version)
        assert response == subscribable_item_response
        assert requests_mock.last_request.json() == {"enabled": False}
