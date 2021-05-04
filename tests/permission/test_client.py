import re
import json

from okdata.sdk.permission.client import PermissionClient
from okdata.sdk.permission.user_types import User


def test_update_permission(requests_mock):
    client = PermissionClient()
    matcher = re.compile("permissions/okdata%3Adataset%3Afoo")
    res = {
        "resource_name": "okdata:dataset:foo",
        "description": "Allows reading okdata:dataset:foo",
        "scope": "okdata:dataset:read",
        "teams": [],
        "users": ["janedoe"],
        "clients": [],
    }
    requests_mock.register_uri("PUT", matcher, text=json.dumps(res), status_code=200)
    assert (
        client.update_permission(
            "okdata:dataset:foo", "okdata:dataset:read", add_users=[User("janedoe")]
        )
        == res
    )


def test_get_my_permissions(requests_mock):
    client = PermissionClient()
    matcher = re.compile("my_permissions")
    res = {
        "okdata:dataset:foo": {"scopes": ["okdata:dataset:read"]},
    }
    requests_mock.register_uri("GET", matcher, text=json.dumps(res), status_code=200)
    assert client.get_my_permissions() == res


def test_get_permissions(requests_mock):
    client = PermissionClient()
    matcher = re.compile("permissions/okdata%3Adataset%3Afoo")
    res = [
        {
            "resource_name": "okdata:dataset:foo",
            "description": "Allows reading okdata:dataset:foo",
            "scope": "okdata:dataset:read",
            "teams": [],
            "users": ["janedoe"],
            "clients": [],
        }
    ]
    requests_mock.register_uri("GET", matcher, text=json.dumps(res), status_code=200)
    assert client.get_permissions("okdata:dataset:foo") == res
