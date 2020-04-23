import json
import pytest

from origo.dataset_authorizer.simple_dataset_authorizer_client import (
    SimpleDatasetAuthorizerClient,
)

prinical_id = "janedoe"
dataset_id = "dataset-id"
service_name = "service-name"

webhook_token_data = {
    "token": "27580f43-7674-4033-87e2-285db632903d",
    "created_by": prinical_id,
    "dataset_id": dataset_id,
    "service": service_name,
    "created_at": "2020-04-20T00:00:00+00:00",
    "expires_at": "2022-04-20T00:00:00+00:00",
    "is_active": True,
}
webhook_token = webhook_token_data["token"]

dataset_authorizer_client = SimpleDatasetAuthorizerClient()


def test_create_dataset_access(mock_create_dataset_access_request):
    assert dataset_authorizer_client.create_dataset_access(dataset_id, prinical_id) == {
        "message": "Created"
    }
    assert dataset_authorizer_client.create_dataset_access(
        dataset_id, prinical_id, webhook_token
    ) == {"message": "Created"}


def test_check_dataset_access(mock_check_dataset_access_request):
    assert dataset_authorizer_client.check_dataset_access(dataset_id) == {
        "access": True
    }
    assert dataset_authorizer_client.check_dataset_access(
        dataset_id, webhook_token
    ) == {"access": True}


def test_create_webhook_token(mock_create_webhook_token_request):
    assert (
        dataset_authorizer_client.create_webhook_token(dataset_id, service_name)
        == webhook_token_data
    )


def test_delete_webhook_token(mock_delete_webhook_token_request):
    assert dataset_authorizer_client.delete_webhook_token(
        dataset_id, webhook_token
    ) == {"message": f"Deleted {webhook_token} for dataset {dataset_id}"}


def test_authorize_webhook_token(mock_authorize_webhook_token_request):
    assert dataset_authorizer_client.authorize_webhook_token(
        dataset_id, webhook_token
    ) == {"access": True}


@pytest.fixture(scope="function")
def mock_create_dataset_access_request(requests_mock):
    requests_mock.register_uri(
        "POST",
        f"{dataset_authorizer_client.dataset_authorizer_url}/{dataset_id}",
        text=json.dumps({"message": "Created"}),
        status_code=201,
    )


@pytest.fixture(scope="function")
def mock_check_dataset_access_request(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{dataset_authorizer_client.dataset_authorizer_url}/{dataset_id}",
        text=json.dumps({"access": True}),
        status_code=200,
    )


@pytest.fixture(scope="function")
def mock_create_webhook_token_request(requests_mock):
    requests_mock.register_uri(
        "POST",
        f"{dataset_authorizer_client.dataset_authorizer_url}/{dataset_id}/webhook",
        text=json.dumps(webhook_token_data),
        status_code=201,
    )


@pytest.fixture(scope="function")
def mock_delete_webhook_token_request(requests_mock):
    requests_mock.register_uri(
        "DELETE",
        f"{dataset_authorizer_client.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}",
        text=json.dumps(
            {"message": f"Deleted {webhook_token} for dataset {dataset_id}"}
        ),
        status_code=200,
    )


@pytest.fixture(scope="function")
def mock_authorize_webhook_token_request(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{dataset_authorizer_client.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}/authorize",
        text=json.dumps({"access": True}),
        status_code=200,
    )
