from requests.exceptions import HTTPError
import pytest
from origo.sdk.elasticsearch.queries import ElasticsearchQueries


def test_event_stat(requests_mock):
    sdk = ElasticsearchQueries()
    requests_mock.get(
        f"{sdk.elasticsearch_query_url}/my_dataset/events",
        status_code=200,
        json={"last_day": "Yup"},
    )

    assert sdk.event_stat("my_dataset") == {"last_day": "Yup"}


def test_not_owner(requests_mock):
    sdk = ElasticsearchQueries()
    requests_mock.get(
        f"{sdk.elasticsearch_query_url}/my_dataset/events",
        status_code=403,
        json={"message": "Forbidden"},
    )

    with pytest.raises(HTTPError):
        sdk.event_stat("my_dataset")


@pytest.mark.parametrize("status_code", [404, 500, 501])
def test_other_statuses(requests_mock, status_code):
    sdk = ElasticsearchQueries()
    requests_mock.get(
        f"{sdk.elasticsearch_query_url}/my_dataset/events",
        status_code=status_code,
        json={"last_day": "Yup"},
    )

    with pytest.raises(HTTPError):
        sdk.event_stat("my_dataset")
