import json
import pytest

from origo.event.event_stream_client import EventStreamClient

dataset_id = "dataset-id"
version = "1"

event_stream_client = EventStreamClient()

event_stream_url = (
    f"{event_stream_client.stream_manager_url}/stream/{dataset_id}/{version}"
)

event_stream_info = {
    "id": f"{dataset_id}/{version}",
    "status": "ACTIVE",
    "createdBy": "jd",
    "createdAt": "2020-01-21T09:28:57.831435+00:00",
}

error_message_from_api = "Event stream with id: some-id does not exist"


def test_create_event_stream(mock_create_event_stream_request):

    assert event_stream_client.create_event_stream(dataset_id, version) == {
        "message": "Accepted"
    }


def test_get_event_stream_info(mock_get_event_stream_info_request):
    assert (
        event_stream_client.get_event_stream_info(dataset_id, version)
        == event_stream_info
    )


def test_delete_event_stream(mock_delete_event_stream_request):
    assert event_stream_client.delete_event_stream(dataset_id, version) == {
        "message": "Delete initiated"
    }


@pytest.fixture(scope="function")
def mock_create_event_stream_request(requests_mock):
    requests_mock.register_uri(
        "POST",
        event_stream_url,
        text=json.dumps({"message": "Accepted"}),
        status_code=202,
    )


@pytest.fixture(scope="function")
def mock_get_event_stream_info_request(requests_mock):
    requests_mock.register_uri(
        "GET", event_stream_url, text=json.dumps(event_stream_info), status_code=200,
    )


@pytest.fixture(scope="function")
def mock_delete_event_stream_request(requests_mock):
    requests_mock.register_uri(
        "DELETE",
        event_stream_url,
        text=json.dumps({"message": "Delete initiated"}),
        status_code=202,
    )
