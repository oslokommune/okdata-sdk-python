import re
import json

from okdata.sdk.webhook.client import WebhookClient


def test_create_webhook_token(requests_mock):
    client = WebhookClient()
    dataset_id = "dataset-id"
    operation = "read"
    matcher = re.compile(f"{client.api_url}/{dataset_id}/tokens")

    def body_matcher(request):
        return request.json() == {"operation": operation}

    res = {
        "token": "774d8f35-fb4b-4e06-9d7f-54d1a08589b4",
        "created_by": "your-username",
        "dataset_id": dataset_id,
        "operation": operation,
        "created_at": "2020-02-29T00:00:00+00:00",
        "expires_at": "2022-02-28T00:00:00+00:00",
        "is_active": True,
    }
    requests_mock.register_uri(
        "POST",
        matcher,
        text=json.dumps(res),
        status_code=201,
        additional_matcher=body_matcher,
    )

    assert client.create_webhook_token(dataset_id, operation) == res


def test_list_webhook_tokens(requests_mock):
    client = WebhookClient()
    dataset_id = "dataset-id"
    matcher = re.compile(f"{client.api_url}/{dataset_id}/tokens")

    res = [
        {
            "token": "774d8f35-fb4b-4e06-9d7f-54d1a08589b4",
            "created_by": "your-username",
            "dataset_id": dataset_id,
            "operation": "read",
            "created_at": "2020-02-29T00:00:00+00:00",
            "expires_at": "2022-02-28T00:00:00+00:00",
            "is_active": True,
        }
    ]
    requests_mock.register_uri(
        "GET",
        matcher,
        text=json.dumps(res),
        status_code=200,
    )

    assert client.list_webhook_tokens(dataset_id) == res


def test_delete_webhook_token(requests_mock):
    client = WebhookClient()
    dataset_id = "dataset-id"
    token = "774d8f35-fb4b-4e06-9d7f-54d1a08589b4"
    matcher = re.compile(f"{client.api_url}/{dataset_id}/tokens/{token}")

    res = {"message": f"Deleted {token} for dataset {dataset_id}"}
    requests_mock.register_uri(
        "DELETE",
        matcher,
        text=json.dumps(res),
        status_code=200,
    )

    assert client.delete_webhook_token(dataset_id, token) == res


def test_authorize_webhook_token(requests_mock):
    client = WebhookClient()
    dataset_id = "dataset-id"
    token = "774d8f35-fb4b-4e06-9d7f-54d1a08589b4"
    operation = "write"
    matcher = re.compile(
        f"{client.api_url}/{dataset_id}/tokens/{token}/authorize\\?operation={operation}"
    )

    res = {"access": True, "reason": None}
    requests_mock.register_uri(
        "GET",
        matcher,
        text=json.dumps(res),
        status_code=200,
    )

    assert client.authorize_webhook_token(dataset_id, token, operation) == res
