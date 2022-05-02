import re
import json

from okdata.sdk.team.client import TeamClient


def test_get_teams(requests_mock):
    teams = [
        {"team_id": "abc", "name": "Team Foo"},
        {"team_id": "123", "name": "Team Bar"},
    ]
    requests_mock.register_uri(
        "GET", re.compile("teams"), text=json.dumps(teams), status_code=200
    )
    assert TeamClient().get_teams() == teams


def test_get_team(requests_mock):
    team_id = "abc"
    team = {"team_id": team_id, "name": "Team Foo"}
    requests_mock.register_uri(
        "GET",
        re.compile(f"teams/{team_id}"),
        text=json.dumps(team),
        status_code=200,
    )
    assert TeamClient().get_team(team_id) == team


def test_get_team_members(requests_mock):
    team_id = "abc"
    members = [
        {"id": "abc", "username": "Foo"},
        {"id": "123", "username": "Bar"},
    ]
    requests_mock.register_uri(
        "GET",
        re.compile(f"teams/{team_id}/members"),
        text=json.dumps(members),
        status_code=200,
    )
    assert TeamClient().get_team_members(team_id) == members
