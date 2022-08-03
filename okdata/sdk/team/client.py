import logging
from urllib.parse import quote

from okdata.sdk import SDK

log = logging.getLogger()


class TeamClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "team"
        super().__init__(config, auth, env)
        self.api_url = self.config.get("permissionApiUrl")

    def get_teams(self, has_role=None):
        """Return a list of teams.

        When `has_role` is passed, return only teams with the given role.
        """
        url = f"{self.api_url}/teams"
        log.info(f"SDK:Listing teams from: {url}")
        params = {}

        if has_role:
            params["has_role"] = has_role

        return self.get(url, params=params).json()

    def get_team(self, team_id):
        """Return details for a team."""
        url = "{}/teams/{}".format(self.api_url, quote(team_id))
        log.info(f"SDK:Getting team from: {url}")
        return self.get(url).json()

    def get_team_by_name(self, team_name):
        """Return details for a team by name."""
        url = "{}/teams/name/{}".format(self.api_url, quote(team_name))
        log.info(f"SDK:Getting team from: {url}")
        return self.get(url).json()

    def add_team_member(self, team_id, username):
        """Add user with `username` as member to team with ID `team_id`."""
        url = "{}/teams/{}/members/{}".format(
            self.api_url, quote(team_id), quote(username)
        )
        log.info(f"SDK:Adding member to team: {url}")
        self.put(url, data=None)
        return None

    def remove_team_member(self, team_id, username):
        """Remove user with `username` as member from team with
        ID `team_id`.
        """
        url = "{}/teams/{}/members/{}".format(
            self.api_url, quote(team_id), quote(username)
        )
        log.info(f"SDK:Removing member from team: {url}")
        self.delete(url)
        return None
