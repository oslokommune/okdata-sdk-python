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


def test_get_team_by_name(requests_mock):
    team_name = "Foo"
    team = {"team_id": "abc", "name": team_name}
    requests_mock.register_uri(
        "GET",
        re.compile(f"teams/name/{team_name}"),
        text=json.dumps(team),
        status_code=200,
    )
    assert TeamClient().get_team_by_name(team_name) == team
