import logging
from urllib.parse import quote

from okdata.sdk import SDK

log = logging.getLogger()


class TeamClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "team"
        super().__init__(config, auth, env)
        self.api_url = self.config.get("permissionApiUrl")

    def get_teams(self, include=None, has_role=None):
        """Return a list of teams.

        The `include` parameter currently supports the following values:

        - `None`: Only the calling user's own teams are included.
        - `"all"`: All teams are included regardless of membership.

        When `has_role` is passed, return only teams with the given role.
        """
        url = f"{self.api_url}/teams"
        log.info(f"SDK:Listing teams from: {url}")
        params = {}

        if include:
            params["include"] = include
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
