import re
import json

from okdata.sdk.permission.client import PermissionClient
from okdata.sdk.permission.user_types import User


def test_update_permission(requests_mock):
    client = PermissionClient()
    matcher = re.compile("permissions/maskinporten%3Aclient%3Afoo")
    res = {
        "resource_name": "maskinporten:client:foo",
        "description": "Allows reading maskinporten:client:foo",
        "scope": "maskinporten:client:read",
        "teams": [],
        "users": ["janedoe"],
        "clients": [],
    }
    requests_mock.register_uri("PUT", matcher, text=json.dumps(res), status_code=200)
    assert (
        client.update_permission(
            "maskinporten:client:foo",
            "maskinporten:client:read",
            add_users=[User("janedoe")],
        )
        == res
    )


def test_get_my_permissions(requests_mock):
    client = PermissionClient()
    matcher = re.compile("my_permissions")
    res = {
        "maskinporten:client:foo": {"scopes": ["maskinporten:client:read"]},
    }
    requests_mock.register_uri("GET", matcher, text=json.dumps(res), status_code=200)
    assert client.get_my_permissions() == res


def test_get_permissions(requests_mock):
    client = PermissionClient()
    matcher = re.compile("permissions/maskinporten%3Aclient%3Afoo")
    res = [
        {
            "resource_name": "maskinporten:client:foo",
            "description": "Allows reading maskinporten:client:foo",
            "scope": "maskinporten:client:read",
            "teams": [],
            "users": ["janedoe"],
            "clients": [],
        }
    ]
    requests_mock.register_uri("GET", matcher, text=json.dumps(res), status_code=200)
    assert client.get_permissions("maskinporten:client:foo") == res
